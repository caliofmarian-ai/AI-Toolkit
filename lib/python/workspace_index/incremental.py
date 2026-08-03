"""
Incremental Workspace Index — CORE-006

Implements change-aware indexing to avoid full repository rebuilds on every execution.

Architecture (Phase 6 pipeline):
    Repository
    ↓
    RepositoryPolicy
    ↓
    ChangeDetector  (snapshot comparison)
    ↓
    Workspace Cache  (.ai/runtime/cache/workspace_index/)
    ↓
    Incremental Update  (partial or full rebuild)
    ↓
    WorkspaceIndex  (immutable, unchanged public interface)
    ↓
    Analysis Engines
"""

import json
import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from .models import WorkspaceFile, WorkspaceDirectory, WorkspaceStatistics, WorkspaceIndex
from .builder import WorkspaceIndexBuilder
from .exporter import WorkspaceIndexExporter
from .policy import RepositoryPolicy


# Increment this constant whenever the snapshot / index cache format changes.
# A version mismatch forces a full rebuild and replaces the stale cache.
CACHE_VERSION = 1

# When fewer than this fraction of known files changed, a partial rebuild is
# performed instead of a full traversal.  Above the threshold a full rebuild
# is cheaper than merging individual entries.
PARTIAL_REBUILD_THRESHOLD = 0.50


# ---------------------------------------------------------------------------
# Snapshot models
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class FileSnapshot:
    """Lightweight per-file state stored in the repository snapshot."""

    path: str    # relative path from repository root
    size: int    # file size in bytes
    mtime: float # last-modification timestamp (st_mtime)


@dataclass(frozen=True)
class RepositorySnapshot:
    """
    Lightweight image of the repository filesystem state.

    Stored as JSON under `.ai/runtime/cache/workspace_index/snapshot.json`.
    Used by ChangeDetector to determine what has changed since the last run.
    """

    version: int
    repository_root: str
    repository_name: str
    created_at: float
    files: Tuple[FileSnapshot, ...]

    # ------------------------------------------------------------------
    # Serialization
    # ------------------------------------------------------------------

    def to_dict(self) -> dict:
        return {
            "version": self.version,
            "repository_root": self.repository_root,
            "repository_name": self.repository_name,
            "created_at": self.created_at,
            "files": {
                f.path: {"size": f.size, "mtime": f.mtime}
                for f in self.files
            },
        }

    @staticmethod
    def from_dict(data: dict) -> "RepositorySnapshot":
        files = tuple(
            FileSnapshot(path=path, size=meta["size"], mtime=meta["mtime"])
            for path, meta in data.get("files", {}).items()
        )
        return RepositorySnapshot(
            version=int(data.get("version", 0)),
            repository_root=data.get("repository_root", ""),
            repository_name=data.get("repository_name", ""),
            created_at=float(data.get("created_at", 0.0)),
            files=files,
        )


# ---------------------------------------------------------------------------
# Delta model
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class IndexDelta:
    """
    Describes the difference between a persisted RepositorySnapshot and the
    current state of the repository.

    Produced exclusively by ChangeDetector.detect().
    """

    added: Tuple[str, ...]               # relative paths of new files
    removed: Tuple[str, ...]             # relative paths of deleted files
    modified: Tuple[str, ...]            # relative paths of changed files
    renamed: Tuple[Tuple[str, str], ...] # (old_path, new_path) — best-effort

    @property
    def is_empty(self) -> bool:
        return (
            not self.added
            and not self.removed
            and not self.modified
            and not self.renamed
        )

    @property
    def total_changes(self) -> int:
        return (
            len(self.added)
            + len(self.removed)
            + len(self.modified)
            + len(self.renamed)
        )

    def __repr__(self) -> str:
        return (
            f"IndexDelta(added={len(self.added)}, removed={len(self.removed)}, "
            f"modified={len(self.modified)}, renamed={len(self.renamed)})"
        )


# ---------------------------------------------------------------------------
# Performance metrics
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class IncrementalStats:
    """
    Performance metrics collected during an incremental index build.

    Exposed in the Profiler summary and Development Report.
    """

    cache_hit: bool            # True when cache was valid and no changes detected
    cache_miss: bool           # True when cache was absent or failed validation
    files_reused: int          # files taken from cache without re-scanning
    files_rebuilt: int         # files that required re-scanning
    rebuild_percentage: float  # percentage of total files that were rebuilt
    saved_time_estimate: float # estimated seconds saved compared with a full rebuild

    def to_dict(self) -> dict:
        return {
            "cache_hit": self.cache_hit,
            "cache_miss": self.cache_miss,
            "files_reused": self.files_reused,
            "files_rebuilt": self.files_rebuilt,
            "rebuild_percentage": round(self.rebuild_percentage, 4),
            "saved_time_estimate": round(self.saved_time_estimate, 6),
        }


# ---------------------------------------------------------------------------
# Build result container
# ---------------------------------------------------------------------------


@dataclass
class IncrementalBuildResult:
    """
    Result returned by IncrementalWorkspaceIndex.build().

    Contains the immutable WorkspaceIndex alongside incremental metrics.
    The WorkspaceIndex public interface is identical to the one produced by
    WorkspaceIndexBuilder, preserving full engine compatibility.
    """

    index: WorkspaceIndex
    stats: IncrementalStats
    delta: IndexDelta


# ---------------------------------------------------------------------------
# Change detector
# ---------------------------------------------------------------------------


class ChangeDetector:
    """
    Detects filesystem changes between a stored RepositorySnapshot and the
    current state of the repository.

    Produces an IndexDelta describing added, removed, modified, and renamed
    files.  Renamed file detection is best-effort: a removal and an addition
    that share the same file size are considered a probable rename.
    """

    def detect(
        self,
        old_snapshot: RepositorySnapshot,
        current_files: Dict[str, FileSnapshot],
    ) -> IndexDelta:
        """
        Compare old_snapshot against current_files and return an IndexDelta.

        Parameters
        ----------
        old_snapshot:
            Previously persisted RepositorySnapshot.
        current_files:
            Mapping of relative path → FileSnapshot representing the current
            filesystem state (produced by IncrementalWorkspaceIndex._scan).
        """
        old_by_path: Dict[str, FileSnapshot] = {f.path: f for f in old_snapshot.files}
        old_paths = set(old_by_path.keys())
        new_paths = set(current_files.keys())

        potentially_added = new_paths - old_paths
        potentially_removed = old_paths - new_paths
        common_paths = old_paths & new_paths

        modified: List[str] = [
            path for path in common_paths
            if (
                current_files[path].size != old_by_path[path].size
                or current_files[path].mtime != old_by_path[path].mtime
            )
        ]

        # Best-effort rename detection:
        # Match removed files to added files that share the same byte size.
        renamed: List[Tuple[str, str]] = []
        remaining_added: set = set(potentially_added)
        remaining_removed: set = set(potentially_removed)

        if remaining_added and remaining_removed:
            removed_by_size: Dict[int, List[str]] = {}
            for path in remaining_removed:
                size = old_by_path[path].size
                removed_by_size.setdefault(size, []).append(path)

            for added_path in sorted(remaining_added):
                added_size = current_files[added_path].size
                candidates = removed_by_size.get(added_size)
                if candidates:
                    old_path = candidates.pop(0)
                    renamed.append((old_path, added_path))
                    remaining_added.discard(added_path)
                    remaining_removed.discard(old_path)

        return IndexDelta(
            added=tuple(sorted(remaining_added)),
            removed=tuple(sorted(remaining_removed)),
            modified=tuple(sorted(modified)),
            renamed=tuple(renamed),
        )


# ---------------------------------------------------------------------------
# Incremental workspace index
# ---------------------------------------------------------------------------


class IncrementalWorkspaceIndex:
    """
    Incremental workspace indexer.

    On the first run (or whenever the cache is missing / invalid) it delegates
    to WorkspaceIndexBuilder for a full traversal and then persists a snapshot
    and a serialised WorkspaceIndex under the cache directory.

    On subsequent runs it compares the persisted snapshot to the current
    filesystem state.  When nothing changed the cached WorkspaceIndex is
    deserialised directly (zero filesystem traversal overhead).  When only a
    subset of files changed only those entries are rebuilt; the rest are taken
    from the cache.

    Usage
    -----
    result = IncrementalWorkspaceIndex(root=".", policy=policy).build()
    index  = result.index   # standard immutable WorkspaceIndex
    stats  = result.stats   # IncrementalStats (cache hit/miss, files reused …)
    delta  = result.delta   # IndexDelta (what changed since last run)
    """

    SNAPSHOT_FILENAME = "snapshot.json"
    INDEX_FILENAME = "index.json"

    def __init__(self, root=".", policy=None, cache_dir=None):
        self.root = Path(root).resolve()
        self.policy = policy if policy is not None else RepositoryPolicy()
        if cache_dir is None:
            cache_dir = self.root / ".ai" / "runtime" / "cache" / "workspace_index"
        self.cache_dir = Path(cache_dir)
        self._detector = ChangeDetector()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def build(self) -> IncrementalBuildResult:
        """
        Return an immutable WorkspaceIndex, using cached data wherever possible.

        Decision tree:
        1. No valid snapshot on disk          → full rebuild (cache miss)
        2. Valid snapshot, no changes         → deserialise cached index (cache hit)
        3. Valid snapshot, few changes        → partial rebuild (reuse unchanged entries)
        4. Valid snapshot, many changes       → full rebuild (cache stale)
        """
        started = time.perf_counter()

        snapshot = self._load_snapshot()

        if snapshot is None or not self._is_snapshot_valid(snapshot):
            return self._full_rebuild(cache_miss=True, started=started)

        current_files = self._scan_current_files()
        delta = self._detector.detect(snapshot, current_files)

        if delta.is_empty:
            cached_index = self._load_cached_index()
            if cached_index is not None:
                elapsed = time.perf_counter() - started
                total = len(snapshot.files)
                stats = IncrementalStats(
                    cache_hit=True,
                    cache_miss=False,
                    files_reused=total,
                    files_rebuilt=0,
                    rebuild_percentage=0.0,
                    saved_time_estimate=max(
                        0.0,
                        cached_index.statistics.scan_duration - elapsed,
                    ),
                )
                return IncrementalBuildResult(
                    index=cached_index,
                    stats=stats,
                    delta=delta,
                )

        total_known = len(snapshot.files)
        changed_count = delta.total_changes
        if total_known > 0 and changed_count / total_known < PARTIAL_REBUILD_THRESHOLD:
            return self._partial_rebuild(snapshot, delta, current_files, started)

        return self._full_rebuild(cache_miss=False, started=started)

    def invalidate_cache(self):
        """Remove all cached files for this repository root."""
        for filename in (self.SNAPSHOT_FILENAME, self.INDEX_FILENAME):
            try:
                (self.cache_dir / filename).unlink()
            except FileNotFoundError:
                pass

    # ------------------------------------------------------------------
    # Full rebuild
    # ------------------------------------------------------------------

    def _full_rebuild(self, cache_miss: bool, started: float) -> IncrementalBuildResult:
        """Full filesystem traversal via WorkspaceIndexBuilder."""
        index = WorkspaceIndexBuilder(self.root, policy=self.policy).build()
        self._persist(index)

        stats = IncrementalStats(
            cache_hit=False,
            cache_miss=cache_miss,
            files_reused=0,
            files_rebuilt=index.statistics.total_files,
            rebuild_percentage=100.0,
            saved_time_estimate=0.0,
        )
        return IncrementalBuildResult(
            index=index,
            stats=stats,
            delta=IndexDelta(added=(), removed=(), modified=(), renamed=()),
        )

    # ------------------------------------------------------------------
    # Partial rebuild
    # ------------------------------------------------------------------

    def _partial_rebuild(
        self,
        old_snapshot: RepositorySnapshot,
        delta: IndexDelta,
        current_files: Dict[str, FileSnapshot],
        started: float,
    ) -> IncrementalBuildResult:
        """
        Reuse unchanged entries from the cached WorkspaceIndex and rebuild
        only the files identified by delta.
        """
        cached_index = self._load_cached_index()
        if cached_index is None:
            return self._full_rebuild(cache_miss=False, started=started)

        # Paths that must be removed from the cached collection
        removed_paths = (
            set(delta.removed)
            | {old for old, _ in delta.renamed}
        )
        # Paths that must be rebuilt (newly added or modified)
        rebuild_paths = (
            set(delta.added)
            | set(delta.modified)
            | {new for _, new in delta.renamed}
        )

        reused_files = [
            f for f in cached_index.files
            if f.path not in rebuild_paths and f.path not in removed_paths
        ]

        rebuilt_files = []
        for rel_path in sorted(rebuild_paths):
            abs_path = self.root / rel_path
            if not abs_path.exists():
                continue
            try:
                size = abs_path.stat().st_size
            except OSError:
                size = 0
            rebuilt_files.append(
                WorkspaceFile(
                    path=rel_path,
                    name=abs_path.name,
                    size=size,
                    extension=abs_path.suffix,
                )
            )

        all_files = reused_files + rebuilt_files
        files_reused = len(reused_files)
        files_rebuilt = len(rebuilt_files)
        total = files_reused + files_rebuilt
        rebuild_pct = (files_rebuilt / total * 100.0) if total > 0 else 0.0

        elapsed = time.perf_counter() - started
        fps = total / elapsed if elapsed > 0 else float(total)

        new_stats = WorkspaceStatistics(
            total_files=len(all_files),
            total_directories=cached_index.statistics.total_directories,
            ignored_files=cached_index.statistics.ignored_files,
            ignored_directories=cached_index.statistics.ignored_directories,
            scan_duration=round(elapsed, 6),
            files_per_second=round(fps, 2),
        )

        new_index = WorkspaceIndex(
            repository_name=cached_index.repository_name,
            repository_root=cached_index.repository_root,
            files=all_files,
            directories=list(cached_index.directories),
            ignored_files=list(cached_index.ignored_files),
            ignored_dirs=list(cached_index.ignored_dirs),
            statistics=new_stats,
            created_at=time.time(),
        )

        self._persist(new_index)

        inc_stats = IncrementalStats(
            cache_hit=False,
            cache_miss=False,
            files_reused=files_reused,
            files_rebuilt=files_rebuilt,
            rebuild_percentage=round(rebuild_pct, 4),
            saved_time_estimate=max(
                0.0,
                cached_index.statistics.scan_duration - elapsed,
            ),
        )
        return IncrementalBuildResult(index=new_index, stats=inc_stats, delta=delta)

    # ------------------------------------------------------------------
    # Filesystem scan (lightweight — used only for change detection)
    # ------------------------------------------------------------------

    def _scan_current_files(self) -> Dict[str, FileSnapshot]:
        """
        Walk the repository and collect current file states (path, size, mtime).

        Applies the same RepositoryPolicy pruning as WorkspaceIndexBuilder so
        that the set of tracked files is identical.  The cache directory itself
        is always excluded to prevent snapshot/index artefacts from appearing
        as repository files.
        """
        # Compute cache_dir relative to root so we can prune it during walk.
        try:
            cache_rel = self.cache_dir.relative_to(self.root)
            cache_rel_parts = cache_rel.parts
        except ValueError:
            cache_rel_parts = None  # cache_dir is outside the repo root

        current: Dict[str, FileSnapshot] = {}
        for dirpath, dirnames, filenames in os.walk(str(self.root), topdown=True):
            current_dir = Path(dirpath)
            try:
                current_rel = current_dir.relative_to(self.root)
            except ValueError:
                continue
            current_parts = current_rel.parts

            kept = []
            for d in dirnames:
                candidate_parts = current_parts + (d,)
                # Prune the cache directory to avoid treating cached artefacts
                # as repository files.
                if (
                    cache_rel_parts is not None
                    and candidate_parts == cache_rel_parts[: len(candidate_parts)]
                    and len(candidate_parts) <= len(cache_rel_parts)
                ):
                    continue
                if (
                    self.policy.is_excluded_dir(d)
                    or self.policy.should_prune(candidate_parts)
                ):
                    pass
                else:
                    kept.append(d)
            dirnames[:] = kept

            for filename in filenames:
                file_path = current_dir / filename
                ext = file_path.suffix
                if self.policy.is_excluded_file(filename, ext):
                    continue
                rel = (
                    str(current_rel / filename)
                    if str(current_rel) != "."
                    else filename
                )
                try:
                    st = file_path.stat()
                    size = st.st_size
                    # Round to milliseconds for a stable round-trip through JSON.
                    mtime = round(st.st_mtime, 3)
                except OSError:
                    size = 0
                    mtime = 0.0
                current[rel] = FileSnapshot(path=rel, size=size, mtime=mtime)
        return current

    # ------------------------------------------------------------------
    # Cache management
    # ------------------------------------------------------------------

    def _is_snapshot_valid(self, snapshot: RepositorySnapshot) -> bool:
        """Return True when the snapshot is compatible with the current run."""
        return (
            snapshot.version == CACHE_VERSION
            and snapshot.repository_root == str(self.root)
        )

    def _persist(self, index: WorkspaceIndex):
        """Save both the snapshot and the serialised index to the cache directory."""
        self._save_snapshot(self._snapshot_from_index(index))
        self._save_cached_index(index)

    def _snapshot_from_index(self, index: WorkspaceIndex) -> RepositorySnapshot:
        """Build a RepositorySnapshot from a freshly constructed WorkspaceIndex."""
        snapshot_files: List[FileSnapshot] = []
        for f in index.files:
            abs_path = Path(index.repository_root) / f.path
            try:
                # Round to milliseconds for a stable round-trip through JSON.
                mtime = round(abs_path.stat().st_mtime, 3)
            except OSError:
                mtime = 0.0
            snapshot_files.append(
                FileSnapshot(path=f.path, size=f.size, mtime=mtime)
            )
        return RepositorySnapshot(
            version=CACHE_VERSION,
            repository_root=index.repository_root,
            repository_name=index.repository_name,
            created_at=index.created_at,
            files=tuple(snapshot_files),
        )

    def _load_snapshot(self) -> Optional[RepositorySnapshot]:
        path = self.cache_dir / self.SNAPSHOT_FILENAME
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            return RepositorySnapshot.from_dict(data)
        except (FileNotFoundError, json.JSONDecodeError, KeyError, TypeError):
            return None

    def _save_snapshot(self, snapshot: RepositorySnapshot):
        path = self.cache_dir / self.SNAPSHOT_FILENAME
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(snapshot.to_dict(), indent=2), encoding="utf-8")

    def _load_cached_index(self) -> Optional[WorkspaceIndex]:
        path = self.cache_dir / self.INDEX_FILENAME
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            return _index_from_dict(data)
        except (FileNotFoundError, json.JSONDecodeError, KeyError, TypeError):
            return None

    def _save_cached_index(self, index: WorkspaceIndex):
        path = self.cache_dir / self.INDEX_FILENAME
        path.parent.mkdir(parents=True, exist_ok=True)
        WorkspaceIndexExporter.export(index, str(path))


# ---------------------------------------------------------------------------
# Deserialization helper (module-level so it can be tested independently)
# ---------------------------------------------------------------------------


def _index_from_dict(data: dict) -> WorkspaceIndex:
    """
    Deserialise a WorkspaceIndex from the JSON dict produced by
    WorkspaceIndexExporter.to_dict().
    """
    s = data["statistics"]
    stats = WorkspaceStatistics(
        total_files=s["total_files"],
        total_directories=s["total_directories"],
        ignored_files=s["ignored_files"],
        ignored_directories=s["ignored_directories"],
        scan_duration=s["scan_duration"],
        files_per_second=s["files_per_second"],
    )
    files = [
        WorkspaceFile(
            path=f["path"],
            name=f["name"],
            size=f["size"],
            extension=f["extension"],
        )
        for f in data.get("files", [])
    ]
    directories = [
        WorkspaceDirectory(path=d["path"], name=d["name"])
        for d in data.get("directories", [])
    ]
    ignored_files = [
        WorkspaceFile(
            path=f["path"],
            name=f["name"],
            size=f["size"],
            extension=f["extension"],
        )
        for f in data.get("ignored_files", [])
    ]
    ignored_dirs = [
        WorkspaceDirectory(path=d["path"], name=d["name"])
        for d in data.get("ignored_dirs", [])
    ]
    return WorkspaceIndex(
        repository_name=data["repository_name"],
        repository_root=data["repository_root"],
        files=files,
        directories=directories,
        ignored_files=ignored_files,
        ignored_dirs=ignored_dirs,
        statistics=stats,
        created_at=float(data.get("created_at", time.time())),
    )

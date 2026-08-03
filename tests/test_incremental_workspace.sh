#!/bin/bash
# tests/test_incremental_workspace.sh
# CORE-006 — Incremental Workspace Index test suite
set -e

python3 - <<'PY'
import os
import sys
import json
import shutil
import tempfile
import time
sys.path.insert(0, "lib")

from python.workspace_index import (
    RepositoryPolicy,
    IncrementalWorkspaceIndex,
    IndexDelta,
    ChangeDetector,
    RepositorySnapshot,
    FileSnapshot,
    IncrementalStats,
    IncrementalBuildResult,
    CACHE_VERSION,
)
from python.workspace_index.incremental import _index_from_dict
from python.workspace_index.exporter import WorkspaceIndexExporter

print("=" * 60)
print("IncrementalWorkspaceIndex — Test Suite (CORE-006)")
print("=" * 60)
print()

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_repo(base):
    """Create a minimal fake repository tree under base."""
    (base / "src").mkdir(parents=True)
    (base / "src" / "main.py").write_text("print('hello')", encoding="utf-8")
    (base / "src" / "util.py").write_text("def helper(): pass", encoding="utf-8")
    (base / "README.md").write_text("# Test Repo\n", encoding="utf-8")
    (base / "setup.py").write_text("from setuptools import setup\nsetup()", encoding="utf-8")


# ---------------------------------------------------------------------------
# Test 1 — Initial full build (cache miss)
# ---------------------------------------------------------------------------

tmp1 = tempfile.mkdtemp(prefix="core006_")
try:
    repo = __import__("pathlib").Path(tmp1)
    make_repo(repo)
    cache_dir = repo / ".cache_test"

    incremental = IncrementalWorkspaceIndex(root=repo, cache_dir=cache_dir)
    result = incremental.build()

    assert isinstance(result, IncrementalBuildResult), "build() must return IncrementalBuildResult"
    assert result.index is not None, "WorkspaceIndex must not be None"
    assert result.stats.cache_miss is True, "First run must be a cache miss"
    assert result.stats.cache_hit is False
    assert result.stats.files_rebuilt == result.index.statistics.total_files
    assert result.stats.rebuild_percentage == 100.0
    assert result.delta.is_empty, "Delta must be empty on first run"

    # Cache files must now exist
    assert (cache_dir / "snapshot.json").exists(), "snapshot.json must be persisted"
    assert (cache_dir / "index.json").exists(), "index.json must be persisted"

    total_files = result.index.statistics.total_files
    assert total_files > 0

    print(f"[PASS] Test 1 — Initial full build (files={total_files})")
finally:
    shutil.rmtree(tmp1)


# ---------------------------------------------------------------------------
# Test 2 — Second run without changes (cache hit)
# ---------------------------------------------------------------------------

tmp2 = tempfile.mkdtemp(prefix="core006_")
try:
    repo = __import__("pathlib").Path(tmp2)
    make_repo(repo)
    cache_dir = repo / ".cache_test"

    # First run: builds cache
    IncrementalWorkspaceIndex(root=repo, cache_dir=cache_dir).build()

    # Second run: must be a cache hit
    result2 = IncrementalWorkspaceIndex(root=repo, cache_dir=cache_dir).build()

    assert result2.stats.cache_hit is True, "Second run with no changes must be cache hit"
    assert result2.stats.cache_miss is False
    assert result2.stats.files_rebuilt == 0
    assert result2.stats.files_reused > 0
    assert result2.delta.is_empty

    print(f"[PASS] Test 2 — Second run without changes (cache hit, reused={result2.stats.files_reused})")
finally:
    shutil.rmtree(tmp2)


# ---------------------------------------------------------------------------
# Test 3 — Single file modification
# ---------------------------------------------------------------------------

tmp3 = tempfile.mkdtemp(prefix="core006_")
try:
    repo = __import__("pathlib").Path(tmp3)
    make_repo(repo)
    cache_dir = repo / ".cache_test"

    r1 = IncrementalWorkspaceIndex(root=repo, cache_dir=cache_dir).build()

    # Modify one file (change size to ensure mtime/size change is detected)
    time.sleep(0.01)
    (repo / "src" / "main.py").write_text("print('hello modified')", encoding="utf-8")

    r2 = IncrementalWorkspaceIndex(root=repo, cache_dir=cache_dir).build()

    assert r2.stats.cache_hit is False
    assert r2.stats.cache_miss is False
    assert r2.stats.files_rebuilt >= 1, "Modified file must be rebuilt"
    assert r2.stats.files_reused >= 1, "Unchanged files must be reused"
    assert not r2.delta.is_empty, "Delta must not be empty"
    assert len(r2.delta.modified) >= 1 or len(r2.delta.added) >= 1

    # Analysis results must still be valid
    assert r2.index.statistics.total_files == r1.index.statistics.total_files

    print(
        f"[PASS] Test 3 — Single file modification "
        f"(rebuilt={r2.stats.files_rebuilt}, reused={r2.stats.files_reused})"
    )
finally:
    shutil.rmtree(tmp3)


# ---------------------------------------------------------------------------
# Test 4 — File deletion
# ---------------------------------------------------------------------------

tmp4 = tempfile.mkdtemp(prefix="core006_")
try:
    repo = __import__("pathlib").Path(tmp4)
    make_repo(repo)
    cache_dir = repo / ".cache_test"

    r1 = IncrementalWorkspaceIndex(root=repo, cache_dir=cache_dir).build()
    original_count = r1.index.statistics.total_files

    (repo / "src" / "util.py").unlink()

    r2 = IncrementalWorkspaceIndex(root=repo, cache_dir=cache_dir).build()

    assert r2.index.statistics.total_files == original_count - 1, "Deleted file must be removed"
    assert not r2.delta.is_empty
    # Removed OR detected via rebuilt count
    removed_paths = {f.path for f in r1.index.files} - {f.path for f in r2.index.files}
    assert len(removed_paths) == 1

    print(f"[PASS] Test 4 — File deletion (files before={original_count}, after={r2.index.statistics.total_files})")
finally:
    shutil.rmtree(tmp4)


# ---------------------------------------------------------------------------
# Test 5 — File addition
# ---------------------------------------------------------------------------

tmp5 = tempfile.mkdtemp(prefix="core006_")
try:
    repo = __import__("pathlib").Path(tmp5)
    make_repo(repo)
    cache_dir = repo / ".cache_test"

    r1 = IncrementalWorkspaceIndex(root=repo, cache_dir=cache_dir).build()
    original_count = r1.index.statistics.total_files

    (repo / "src" / "new_module.py").write_text("# new file", encoding="utf-8")

    r2 = IncrementalWorkspaceIndex(root=repo, cache_dir=cache_dir).build()

    assert r2.index.statistics.total_files == original_count + 1, "Added file must appear in index"
    assert not r2.delta.is_empty
    new_paths = {f.path for f in r2.index.files} - {f.path for f in r1.index.files}
    assert len(new_paths) == 1

    print(f"[PASS] Test 5 — File addition (files before={original_count}, after={r2.index.statistics.total_files})")
finally:
    shutil.rmtree(tmp5)


# ---------------------------------------------------------------------------
# Test 6 — Cache invalidation (version mismatch)
# ---------------------------------------------------------------------------

tmp6 = tempfile.mkdtemp(prefix="core006_")
try:
    repo = __import__("pathlib").Path(tmp6)
    make_repo(repo)
    cache_dir = repo / ".cache_test"

    IncrementalWorkspaceIndex(root=repo, cache_dir=cache_dir).build()

    # Corrupt the snapshot version
    snap_path = cache_dir / "snapshot.json"
    data = json.loads(snap_path.read_text())
    data["version"] = 999
    snap_path.write_text(json.dumps(data))

    r = IncrementalWorkspaceIndex(root=repo, cache_dir=cache_dir).build()

    assert r.stats.cache_miss is True, "Version mismatch must trigger cache miss / full rebuild"
    assert r.stats.rebuild_percentage == 100.0

    print(f"[PASS] Test 6 — Cache invalidation (version mismatch → full rebuild)")
finally:
    shutil.rmtree(tmp6)


# ---------------------------------------------------------------------------
# Test 7 — Identical analysis results (cache hit vs fresh build)
# ---------------------------------------------------------------------------

tmp7 = tempfile.mkdtemp(prefix="core006_")
try:
    repo = __import__("pathlib").Path(tmp7)
    make_repo(repo)
    cache_dir = repo / ".cache_test"

    r_full = IncrementalWorkspaceIndex(root=repo, cache_dir=cache_dir).build()
    r_cached = IncrementalWorkspaceIndex(root=repo, cache_dir=cache_dir).build()

    assert r_cached.stats.cache_hit is True
    assert r_full.index.statistics.total_files == r_cached.index.statistics.total_files

    full_paths = {f.path for f in r_full.index.files}
    cached_paths = {f.path for f in r_cached.index.files}
    assert full_paths == cached_paths, "Cached index must contain identical file paths"

    print(f"[PASS] Test 7 — Identical analysis results (full build == cached build)")
finally:
    shutil.rmtree(tmp7)


# ---------------------------------------------------------------------------
# Test 8 — ChangeDetector unit test
# ---------------------------------------------------------------------------

detector = ChangeDetector()

old_files = (
    FileSnapshot(path="a.py", size=100, mtime=1000.0),
    FileSnapshot(path="b.py", size=200, mtime=2000.0),
    FileSnapshot(path="c.py", size=300, mtime=3000.0),
)
old_snapshot = RepositorySnapshot(
    version=CACHE_VERSION,
    repository_root="/repo",
    repository_name="repo",
    created_at=1000.0,
    files=old_files,
)

current = {
    "a.py": FileSnapshot(path="a.py", size=100, mtime=1000.0),   # unchanged
    "b.py": FileSnapshot(path="b.py", size=999, mtime=2001.0),   # modified
    "d.py": FileSnapshot(path="d.py", size=50,  mtime=4000.0),   # added
    # c.py removed
}

delta = detector.detect(old_snapshot, current)

assert "b.py" in delta.modified, "b.py must be detected as modified"
assert "c.py" in delta.removed, "c.py must be detected as removed"
assert "d.py" in delta.added, "d.py must be detected as added"
assert "a.py" not in delta.modified
assert "a.py" not in delta.removed
assert "a.py" not in delta.added
assert delta.total_changes == 3

print(f"[PASS] Test 8 — ChangeDetector unit test "
      f"(added={len(delta.added)}, removed={len(delta.removed)}, modified={len(delta.modified)})")


# ---------------------------------------------------------------------------
# Test 9 — IndexDelta is_empty
# ---------------------------------------------------------------------------

empty_delta = IndexDelta(added=(), removed=(), modified=(), renamed=())
assert empty_delta.is_empty is True

non_empty_delta = IndexDelta(added=("x.py",), removed=(), modified=(), renamed=())
assert non_empty_delta.is_empty is False

print(f"[PASS] Test 9 — IndexDelta.is_empty")


# ---------------------------------------------------------------------------
# Test 10 — IncrementalStats to_dict
# ---------------------------------------------------------------------------

stats = IncrementalStats(
    cache_hit=True,
    cache_miss=False,
    files_reused=42,
    files_rebuilt=0,
    rebuild_percentage=0.0,
    saved_time_estimate=0.012,
)
d = stats.to_dict()
assert d["cache_hit"] is True
assert d["files_reused"] == 42
assert d["rebuild_percentage"] == 0.0

print(f"[PASS] Test 10 — IncrementalStats.to_dict()")


# ---------------------------------------------------------------------------
# Test 11 — WorkspaceIndex immutability preserved through incremental build
# ---------------------------------------------------------------------------

tmp11 = tempfile.mkdtemp(prefix="core006_")
try:
    repo = __import__("pathlib").Path(tmp11)
    make_repo(repo)
    cache_dir = repo / ".cache_test"

    result = IncrementalWorkspaceIndex(root=repo, cache_dir=cache_dir).build()
    index = result.index

    mutation_blocked = False
    try:
        index.repository_name = "hacked"
    except AttributeError:
        mutation_blocked = True

    assert mutation_blocked, "WorkspaceIndex must remain immutable after incremental build"

    print(f"[PASS] Test 11 — WorkspaceIndex immutability preserved")
finally:
    shutil.rmtree(tmp11)


# ---------------------------------------------------------------------------
# Test 12 — invalidate_cache removes cache files
# ---------------------------------------------------------------------------

tmp12 = tempfile.mkdtemp(prefix="core006_")
try:
    repo = __import__("pathlib").Path(tmp12)
    make_repo(repo)
    cache_dir = repo / ".cache_test"

    inc = IncrementalWorkspaceIndex(root=repo, cache_dir=cache_dir)
    inc.build()

    assert (cache_dir / "snapshot.json").exists()
    assert (cache_dir / "index.json").exists()

    inc.invalidate_cache()

    assert not (cache_dir / "snapshot.json").exists(), "snapshot.json must be deleted"
    assert not (cache_dir / "index.json").exists(), "index.json must be deleted"

    # Next build must be a full rebuild
    r = IncrementalWorkspaceIndex(root=repo, cache_dir=cache_dir).build()
    assert r.stats.cache_miss is True

    print(f"[PASS] Test 12 — invalidate_cache() removes cache files")
finally:
    shutil.rmtree(tmp12)


# ---------------------------------------------------------------------------
# Test 13 — Existing WorkspaceIndex tests still pass (engine compatibility)
# ---------------------------------------------------------------------------

from python.workspace_index import WorkspaceIndexBuilder, RepositoryPolicy
from python.repository_engine.engine import RepositoryEngine
from python.dependency_engine.engine import DependencyEngine
from python.planning_engine.engine import PlanningEngine
from python.canonical_audit.engine import CanonicalAuditEngine

tmp13 = tempfile.mkdtemp(prefix="core006_")
try:
    repo = __import__("pathlib").Path(tmp13)
    make_repo(repo)
    # Add a canonical document so CanonicalAuditEngine finds something
    (repo / "docs").mkdir()
    (repo / "docs" / "canonical").mkdir()
    (repo / "docs" / "canonical" / "CANON-001.md").write_text("# CANON-001\n", encoding="utf-8")
    cache_dir = repo / ".cache_test"

    inc_result = IncrementalWorkspaceIndex(root=repo, cache_dir=cache_dir).build()
    index = inc_result.index

    repo_stats = RepositoryEngine(str(repo), workspace_index=index).statistics()
    assert repo_stats["files"] == index.statistics.total_files

    dep_stats = DependencyEngine(str(repo), workspace_index=index).statistics()
    assert "dependencies" in dep_stats

    plan = PlanningEngine(str(repo), workspace_index=index).build_plan()
    assert hasattr(plan, "tasks")

    canonical = CanonicalAuditEngine(str(repo), workspace_index=index).audit()
    assert "canonical_documents" in canonical

    print(f"[PASS] Test 13 — Engine compatibility with incremental index")
finally:
    shutil.rmtree(tmp13)


# ---------------------------------------------------------------------------
# Test 14 — RepositorySnapshot serialization round-trip
# ---------------------------------------------------------------------------

snap = RepositorySnapshot(
    version=CACHE_VERSION,
    repository_root="/some/path",
    repository_name="myrepo",
    created_at=12345.0,
    files=(
        FileSnapshot(path="foo.py", size=100, mtime=9999.5),
        FileSnapshot(path="bar.md", size=200, mtime=8888.0),
    ),
)

d = snap.to_dict()
snap2 = RepositorySnapshot.from_dict(d)

assert snap2.version == snap.version
assert snap2.repository_root == snap.repository_root
assert snap2.repository_name == snap.repository_name
assert len(snap2.files) == len(snap.files)
assert snap2.files[0].path == "foo.py"
assert snap2.files[0].size == 100

print(f"[PASS] Test 14 — RepositorySnapshot round-trip serialization")


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------

print()
print("=" * 60)
print("All IncrementalWorkspaceIndex tests PASS")
print("=" * 60)
PY

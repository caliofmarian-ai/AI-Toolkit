# CORE-006 — Incremental Workspace Index

## Status

Implemented

## Module

`lib/python/workspace_index/incremental.py`

---

## Overview

CORE-006 implements incremental repository indexing for AI Toolkit.

Before this change, `DevelopmentAgent` rebuilt the entire `WorkspaceIndex` on every execution by performing a full `os.walk` traversal regardless of whether any files had changed.

After this change, AI Toolkit detects repository changes and reuses previously indexed data whenever possible.  A full rebuild is only performed when strictly necessary.

This architecture delivers significant performance improvements for large repositories such as Trading Signals Platform, DROPi, and dropi-mobile.

---

## Components

### FileSnapshot

`lib/python/workspace_index/incremental.py`

Immutable frozen dataclass capturing per-file state for change detection:

- `path` — relative path from repository root
- `size` — file size in bytes
- `mtime` — modification timestamp (millisecond precision for stable JSON round-trips)

### RepositorySnapshot

`lib/python/workspace_index/incremental.py`

Lightweight image of the repository filesystem state.

Stored as JSON under `.ai/runtime/cache/workspace_index/snapshot.json`.

Fields:

- `version` — cache format version (`CACHE_VERSION = 1`)
- `repository_root` — absolute path (used for cache validation)
- `repository_name` — human-readable name
- `created_at` — Unix timestamp of last build
- `files` — dict mapping relative path → `{size, mtime}`

### IndexDelta

`lib/python/workspace_index/incremental.py`

Immutable description of what changed between two snapshots:

- `added` — relative paths of new files
- `removed` — relative paths of deleted files
- `modified` — relative paths of files whose size or mtime changed
- `renamed` — `(old_path, new_path)` pairs (best-effort, size-based matching)

Properties:

- `is_empty` — True when no changes were detected
- `total_changes` — sum of all change categories

### ChangeDetector

`lib/python/workspace_index/incremental.py`

Compares a `RepositorySnapshot` to a current filesystem scan and produces an `IndexDelta`.

Rename detection is best-effort: a removed file and an added file sharing the same byte size are treated as a probable rename.

### IncrementalStats

`lib/python/workspace_index/incremental.py`

Performance metrics for an incremental build.  Exposed in `Profiler` and `DevelopmentReport`.

Fields:

- `cache_hit` — True when no changes were detected and the cached index was returned as-is
- `cache_miss` — True when no valid cache existed (first run or after invalidation)
- `files_reused` — number of files taken from cache without re-scanning
- `files_rebuilt` — number of files that required re-scanning
- `rebuild_percentage` — percentage of total files that were rebuilt
- `saved_time_estimate` — estimated seconds saved compared with a full rebuild

### IncrementalBuildResult

`lib/python/workspace_index/incremental.py`

Container returned by `IncrementalWorkspaceIndex.build()`:

- `index` — the immutable `WorkspaceIndex` (identical public interface to CORE-005)
- `stats` — `IncrementalStats`
- `delta` — `IndexDelta` describing what changed since the last run

### IncrementalWorkspaceIndex

`lib/python/workspace_index/incremental.py`

Top-level orchestrator.

```python
result = IncrementalWorkspaceIndex(root=".", policy=policy).build()
index  = result.index   # standard immutable WorkspaceIndex
stats  = result.stats   # IncrementalStats
delta  = result.delta   # IndexDelta
```

---

## Cache Storage

Cache files are stored under:

```
.ai/runtime/cache/workspace_index/
├── snapshot.json   # lightweight per-file metadata (path, size, mtime)
└── index.json      # full serialised WorkspaceIndex
```

The `cache` directory is already excluded by `RepositoryPolicy.DEFAULT_EXCLUDE_DIRS`, so cache artefacts are never included in the `WorkspaceIndex`.

---

## Execution Flow (Phase 6)

```
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
WorkspaceIndex  (immutable)
↓
Analysis Engines
```

---

## Decision Tree

```
build() called
│
├── No valid snapshot on disk?
│     → Full rebuild (cache miss)
│     → Save snapshot + index
│
├── Valid snapshot + no changes (delta.is_empty)?
│     → Deserialise cached index  ← cache hit, zero traversal overhead
│
├── Valid snapshot + few changes (< 50 % of files)?
│     → Partial rebuild
│     → Reuse unchanged WorkspaceFile entries from cache
│     → Re-stat only added / modified / renamed files
│     → Save updated snapshot + index
│
└── Valid snapshot + many changes (≥ 50 % of files)?
      → Full rebuild  (cheaper than merging many individual entries)
      → Save snapshot + index
```

---

## Cache Management

### Cache Version

`CACHE_VERSION = 1`

Increment this constant whenever the snapshot or index format changes.  A version mismatch causes automatic cache invalidation and a full rebuild.

### Cache Validation

On every run `IncrementalWorkspaceIndex` validates:

1. `version == CACHE_VERSION`
2. `repository_root == str(self.root)` (guards against repo moves / renames)

Any validation failure triggers a full rebuild.

### Cache Invalidation

Programmatic invalidation:

```python
IncrementalWorkspaceIndex(root=repo).invalidate_cache()
```

This removes `snapshot.json` and `index.json`.  The next `build()` call will perform a full rebuild.

---

## Performance Metrics

`IncrementalStats` are recorded by `Profiler.record_incremental()` and displayed in the engine profile summary:

```
INCREMENTAL INDEX
  Status       cache hit
  Files reused 1843
  Files rebuilt   0
  Rebuild      0.0%
  Time saved  ~0.250s
```

They are also embedded in the `workspace_index` section of the Development Report:

```markdown
### Incremental Cache
Status: **cache hit** — no changes detected
Files reused: 1843
Files rebuilt: 0
Rebuild percentage: 0.0%
Estimated time saved: 0.2500s
```

---

## WorkspaceIndex Compatibility

The `WorkspaceIndex` returned by `IncrementalWorkspaceIndex.build()` is identical in structure and interface to the one produced by `WorkspaceIndexBuilder.build()`.

All existing engines (`RepositoryEngine`, `DependencyEngine`, `ValidationEngine`, `PlanningEngine`, `RepositoryInspectorV2`, `CanonicalAuditEngine`, `SemanticEngine`, `KnowledgeGraphEngine`) consume the incremental index without modification.

`WorkspaceIndex` remains immutable.  Mutation raises `AttributeError`.

---

## DevelopmentAgent Integration

`DevelopmentAgent` now uses `IncrementalWorkspaceIndex` instead of `WorkspaceIndexBuilder`.

Before (CORE-005):

```python
workspace_index = WorkspaceIndexBuilder(repository, policy=policy).build()
```

After (CORE-006):

```python
incremental_result = IncrementalWorkspaceIndex(repository, policy=policy).build()
workspace_index = incremental_result.index
```

The rest of the agent pipeline is unchanged.

---

## Tests

`tests/test_incremental_workspace.sh`

Covers 14 test cases:

1. Initial full build (cache miss)
2. Second run without changes (cache hit)
3. Single file modification
4. File deletion
5. File addition
6. Cache invalidation (version mismatch → full rebuild)
7. Identical analysis results (full build == cached build)
8. `ChangeDetector` unit test (added / removed / modified detection)
9. `IndexDelta.is_empty`
10. `IncrementalStats.to_dict()`
11. `WorkspaceIndex` immutability preserved through incremental build
12. `invalidate_cache()` removes cache files
13. Engine compatibility with incremental index
14. `RepositorySnapshot` serialization round-trip

---

## Canonical Compliance

- CANON-001: Modular, immutable, observable, performance-aware — Satisfied
- CANON-005: WorkspaceIndex interface unchanged — Satisfied
- CANON-006: Observability — IncrementalStats exposed in Profiler and Report
- CANON-007: Autonomous execution — cache-aware, no manual intervention required
- CANON-008: Performance — full rebuild only when necessary; cache hit = zero traversal
- CANON-011 Invariant 1: Exactly one WorkspaceIndex per execution — Satisfied
- CANON-011 Invariant 2: Filesystem traversal exactly once — Satisfied (zero on cache hit)
- CANON-011 Invariant 6: WorkspaceIndex is immutable — Satisfied
- CANON-011 Invariant 7: RepositoryPolicy is sole authority — Satisfied
- CANON-011 Invariant 15: Backward compatibility — all existing engines and tests pass

# CORE-005 — Workspace Index Architecture

## Status

Implemented

## Module

`lib/python/workspace_index/`

---

## Overview

CORE-005 implements the canonical Workspace Index architecture as defined in CANON-005.

Filesystem traversal now happens exactly once per execution.

All analysis engines consume the same immutable WorkspaceIndex instance.

---

## Components

### RepositoryPolicy

`lib/python/workspace_index/policy.py`

Single authority for inclusion and exclusion rules.

No engine may define its own ignore rules.

Default exclusions:

- `.git`
- `__pycache__`
- `node_modules`
- `venv`, `.venv`, `env`
- `build`, `dist`
- `.cache`, `cache`
- `.tox`, `.mypy_cache`, `.pytest_cache`
- `.pyc`, `.pyo`, `.pyd` extensions

### WorkspaceIndexBuilder

`lib/python/workspace_index/builder.py`

Sole authority for filesystem traversal.

Uses `os.walk` with top-down directory pruning to avoid entering excluded directories.

Only component permitted to call `os.walk()`.

### WorkspaceIndex

`lib/python/workspace_index/models.py`

Immutable canonical in-memory representation of the repository.

Raises `AttributeError` on any mutation attempt after construction.

Provides categorized file views:

- `python_files()` — all `.py` files
- `markdown_files()` — all `.md` files
- `shell_scripts()` — all `.sh` files
- `json_files()` — all `.json` files
- `yaml_files()` — all `.yml`/`.yaml` files
- `test_files()` — files named `test_*`
- `canonical_documents()` — markdown files under `canonical/`
- `files_by_extension(*exts)` — general extension filter
- `files_matching(predicate)` — arbitrary predicate filter
- `extension_histogram()` — extension → count mapping

### WorkspaceFile

Immutable frozen dataclass:
- `path` — relative path from repository root
- `name` — filename
- `size` — file size in bytes
- `extension` — file extension including dot

### WorkspaceDirectory

Immutable frozen dataclass:
- `path` — relative path from repository root
- `name` — directory name

### WorkspaceStatistics

Immutable frozen dataclass:
- `total_files` — scanned files count
- `total_directories` — scanned directories count
- `ignored_files` — files excluded by RepositoryPolicy
- `ignored_directories` — directories excluded by RepositoryPolicy
- `scan_duration` — traversal time in seconds
- `files_per_second` — traversal performance metric

### WorkspaceIndexExporter

`lib/python/workspace_index/exporter.py`

Serialises WorkspaceIndex to JSON.

---

## Execution Flow

```
Repository
↓
RepositoryPolicy
↓
WorkspaceIndexBuilder  (single os.walk traversal)
↓
WorkspaceIndex  (immutable)
↓
RepositoryEngine
↓
DependencyEngine
↓
ValidationEngine
↓
PlanningEngine
↓
RepositoryInspectorV2
↓
CanonicalAuditEngine
↓
SemanticEngine
↓
KnowledgeGraphEngine
↓
Review
↓
Recommendations
↓
Batch Generation
↓
Execution
↓
Development Report
```

---

## Engine Integration

All engines support `workspace_index=None` as a constructor parameter.

When a WorkspaceIndex is provided, the engine consumes it directly without any filesystem traversal.

When no WorkspaceIndex is provided, the engine builds one internally for backward compatibility.

Engines:
- `RepositoryEngine`
- `DependencyEngine`
- `PlanningEngine`
- `RepositoryInspectorV2`
- `CanonicalAuditEngine`
- `SemanticEngine`
- `KnowledgeGraphEngine`

---

## Performance

On AI-Toolkit the single traversal completes in approximately 8ms scanning ~240 files at ~27,000 files/second.

All subsequent engines operate in sub-millisecond time since they read from the in-memory index.

---

## Tests

`tests/test_workspace_index.sh`

Covers:

1. WorkspaceIndex creation
2. RepositoryPolicy application (exclusions verified)
3. Exactly one repository traversal (os.walk call count verified)
4. Immutable WorkspaceIndex (mutation raises AttributeError)
5. Engine compatibility (all engines consume WorkspaceIndex)
6. Performance metrics (all statistics fields present and valid)
7. Serialization (JSON export verified)

---

## Canonical Compliance

- CANON-005: WorkspaceIndex — Implemented
- CANON-011 Invariant 1: Exactly one WorkspaceIndex per execution — Satisfied
- CANON-011 Invariant 2: Filesystem traversal exactly once — Satisfied
- CANON-011 Invariant 6: WorkspaceIndex is immutable — Satisfied
- CANON-011 Invariant 7: RepositoryPolicy is sole authority — Satisfied

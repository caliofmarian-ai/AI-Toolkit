# REPOSITORY HYGIENE SPECIFICATION

Version: 1.0.0

Status: CANONICAL

Project: AI Toolkit

Owner: Marian Caliof

============================================================

PURPOSE

Define the official repository hygiene policy.

Only source artifacts belong in Git.

Generated runtime artifacts shall never be committed.

============================================================

SOURCE ARTIFACTS

Version controlled

- source code
- documentation
- canonical specifications
- development batch documents
- tests
- configuration
- examples
- assets

============================================================

GENERATED ARTIFACTS

Never version controlled

.ai/audit/

.ai/memory/

.ai/work/

__pycache__/

.pytest_cache/

.mypy_cache/

.ruff_cache/

*.pyc

*.pyo

*.log

============================================================

EXCEPTIONS

The following placeholders may remain in Git

.ai/context/.gitkeep

.ai/work/.gitkeep

============================================================

RULES

Generated files are reproducible.

Generated files must never become the source of truth.

Canonical documents remain authoritative.

============================================================

VALIDATION

Repository Hygiene Audit shall verify

No generated artifacts.

No cache directories.

No compiled Python files.

No temporary files.

============================================================

STATUS

ACTIVE


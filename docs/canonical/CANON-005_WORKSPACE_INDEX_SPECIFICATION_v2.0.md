# CANON-005 — Workspace Index Specification v2.0

## Status

Canonical — Implemented (CORE-005)

---

# Purpose

WorkspaceIndex is the canonical repository model.

Every analysis engine must consume WorkspaceIndex instead of scanning the filesystem independently.

WorkspaceIndex is the foundation of AI Toolkit.

---

# Responsibilities

WorkspaceIndex is responsible for representing the complete repository state after a single filesystem traversal.

No engine may directly access the filesystem after WorkspaceIndex has been built.

---

# Construction

WorkspaceIndex is created exclusively by

WorkspaceIndexBuilder

No other component may instantiate or modify it.

---

# Immutability

WorkspaceIndex becomes read-only after construction.

Consumers may only read data.

Mutation is prohibited.

---

# Repository Information

WorkspaceIndex stores

- repository name
- repository root
- repository type
- creation timestamp
- generation timestamp

---

# Filesystem Metadata

WorkspaceIndex contains

- all files
- all directories
- ignored files
- ignored directories
- extension statistics

No duplicate entries.

---

# File Categories

WorkspaceIndex maintains categorized collections.

Examples

Python Files

Markdown Files

Shell Scripts

JSON Files

YAML Files

Configuration Files

Documentation

Canonical Documents

Test Files

Hidden Files

---

# Statistics

WorkspaceIndex provides

- total files
- total directories
- scanned files
- ignored files
- ignored directories
- largest directories
- extension histogram

---

# Repository Policy

WorkspaceIndexBuilder applies RepositoryPolicy while scanning.

Ignored paths are excluded before analysis.

RepositoryPolicy is the only authority for inclusion and exclusion.

---

# Performance

WorkspaceIndexBuilder records

- scan duration
- files per second
- average traversal rate
- ignored percentage

These metrics are exported to the Observability Layer.

---

# Engine Integration

The following engines consume WorkspaceIndex

RepositoryEngine

DependencyEngine

ValidationEngine

PlanningEngine

RepositoryInspector

CanonicalAudit

SemanticEngine

KnowledgeGraph

ReviewAgent

Future engines must use WorkspaceIndex.

---

# Forbidden Operations

After WorkspaceIndex exists, engines must not call

Path.rglob()

glob()

os.walk()

manual recursive scans

Filesystem traversal is centralized.

---

# Persistence

WorkspaceIndex supports future serialization.

Supported targets

JSON

Binary cache

Persistent cache

Future database storage

---

# Checkpoint Support

WorkspaceIndex is compatible with

- execution checkpoints
- resume after interruption
- incremental analysis

---

# Multi-Repository Support

WorkspaceIndex instances can be aggregated into

WorkspaceGraph

allowing analysis across multiple repositories.

---

# Future Extensions

WorkspaceIndex may later include

- Git metadata
- commit history
- branch information
- ownership
- code metrics
- language statistics
- dependency graph
- build metadata

without changing the public API.

---

# Acceptance Criteria

WorkspaceIndex is the only canonical repository model.

Every engine must consume it.

Filesystem traversal occurs exactly once.

WorkspaceIndex remains immutable.

RepositoryPolicy is applied centrally.

Future engines integrate without architectural changes.


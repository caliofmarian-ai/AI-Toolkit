# CANON-003 — Repository Standards v2.0

## Status

Canonical

---

# Purpose

This document defines the mandatory repository structure for AI Toolkit.

Every future module must comply with these standards.

---

# Root Structure

Required top-level directories

docs/
lib/
tests/
.ai/

Optional

examples/
scripts/
benchmarks/

---

# Python Package Layout

Every package must contain

__init__.py

Example

lib/python/example_engine/

    __init__.py

    engine.py

    models.py

    exceptions.py

    validators.py

Only create files when required.

---

# Engine Standards

Every engine should expose a single public class.

Naming

RepositoryEngine

PlanningEngine

SemanticEngine

KnowledgeGraphEngine

ReviewAgent

ExecutionCoordinator

Avoid multiple unrelated public classes.

---

# Data Models

Shared models belong inside

lib/python/common/

Rules

- dataclasses preferred
- immutable where possible
- serialization supported
- validation supported

---

# Testing Standards

Every engine must have

tests/test_<engine>.sh

Tests must verify

- successful execution
- expected output
- edge cases
- regression scenarios

---

# Documentation Standards

Every major subsystem must include

Purpose

Architecture

Responsibilities

Inputs

Outputs

Dependencies

Limitations

---

# Naming

Directories

snake_case

Files

snake_case.py

Classes

PascalCase

Functions

snake_case

Constants

UPPER_CASE

---

# Imports

Absolute imports preferred.

Avoid circular dependencies.

---

# Dependency Rules

Analysis Layer

↓

Intelligence Layer

↓

Planning Layer

↓

Execution Layer

Reverse dependencies are prohibited.

---

# Repository Health

Repository should always maintain

- passing tests
- canonical compliance
- documentation updated
- no duplicated implementations
- consistent naming

---

# Acceptance Criteria

Every Pull Request must preserve these standards.

Non-compliant implementations should be considered non-canonical until corrected.


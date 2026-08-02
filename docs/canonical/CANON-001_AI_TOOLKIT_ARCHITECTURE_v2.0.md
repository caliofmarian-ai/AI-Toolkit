# CANON-001 — AI Toolkit Canonical Architecture v2.0

## Status

Canonical

## Purpose

This document defines the canonical architecture of AI Toolkit.

Every future implementation MUST comply with this specification.

No new engine may be introduced unless it integrates into this architecture.

---

# Core Principles

The platform shall be:

- Modular
- Immutable where possible
- Observable
- Testable
- Repository-agnostic
- Multi-repository capable
- Autonomous
- Performance-aware
- AI-provider agnostic

---

# Architectural Layers

Workspace Layer

↓

Repository Layer

↓

Analysis Layer

↓

Intelligence Layer

↓

Planning Layer

↓

Execution Layer

↓

Review Layer

↓

Observability Layer

↓

Persistence Layer

↓

Autonomous Evolution Layer

---

# Repository Layer

Responsible for exactly one filesystem traversal.

Contains:

- WorkspaceIndex
- WorkspaceIndexBuilder
- RepositoryPolicy
- Ignore Rules
- Shared Models

Filesystem traversal occurs exactly once.

---

# Analysis Layer

Contains:

- RepositoryEngine
- DependencyEngine
- ValidationEngine
- RepositoryInspector
- SemanticEngine
- KnowledgeGraph
- CanonicalAudit

Rules:

- Read-only
- Consume WorkspaceIndex
- Never scan filesystem directly

---

# Intelligence Layer

Contains:

- Recommendation Engine
- Planning Engine
- Review Agent
- Complexity Estimator
- Cost Estimator
- Time Estimator
- Risk Assessment

Produces decisions only.

---

# Planning Layer

Produces:

- Roadmaps
- Tasks
- Priorities
- Execution batches
- Time estimation

No execution.

---

# Execution Layer

Contains:

- Batch Generator
- GitHub Materialization
- Execution Engine
- Execution Coordinator
- Workspace Orchestrator

Executes plans only.

---

# Review Layer

Responsible for:

- Quality Gates
- Review Agent
- Findings
- Acceptance Criteria

---

# Observability Layer

Every engine exposes:

- Progress
- ETA
- Throughput
- CPU
- Memory
- Current Engine
- Current Repository
- Current Phase

---

# Persistence Layer

Stores:

- WorkspaceIndex
- Reports
- Checkpoints
- Execution State
- Metrics
- Batch State

Supports resume after interruption.

---

# Autonomous Layer

Responsible for:

- Continuous Improvement
- Automatic Recommendations
- Architectural Drift Detection
- Dead Code Detection
- Missing Canonical Modules
- Duplicate Detection

---

# Long-Term Pipeline

Workspace

↓

Workspace Index

↓

Analysis

↓

Intelligence

↓

Planning

↓

Execution

↓

Review

↓

Observability

↓

Persistence

↓

Continuous Improvement

---

# Canonical Invariants

Mandatory rules:

- Single filesystem traversal
- Immutable WorkspaceIndex
- Read-only analysis engines
- Execution separated from Planning
- RepositoryPolicy centralized
- Dependency Injection
- Zero duplicated repository scans
- Zero duplicated business logic
- Mandatory observability
- Mandatory persistence
- Full automated testing
- Multi-repository support
- Autonomous operation


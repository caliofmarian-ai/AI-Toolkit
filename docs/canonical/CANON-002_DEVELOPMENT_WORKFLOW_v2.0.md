# CANON-002 — Development Workflow v2.0

## Status

Canonical

---

# Purpose

This document defines the mandatory development workflow for every feature, engine, module and architectural change inside AI Toolkit.

Every implementation MUST follow this workflow.

---

# Phase 1 — Research

Objectives

- Understand the problem.
- Inspect current architecture.
- Review canonical documents.
- Identify affected modules.
- Estimate implementation effort.

Deliverables

- Research notes
- Impact analysis
- Initial estimation

---

# Phase 2 — Planning

Produce

- implementation roadmap
- affected components
- risks
- dependencies
- execution order
- estimated duration

No implementation.

---

# Phase 3 — Architecture Validation

Verify alignment with

- CANON-001
- Repository standards
- Workspace architecture
- Layer separation
- Dependency rules

Reject non-canonical solutions.

---

# Phase 4 — Implementation

Rules

- Small logical commits.
- Preserve backwards compatibility.
- No duplicated code.
- Dependency Injection preferred.
- Immutable shared models where possible.

---

# Phase 5 — Testing

Mandatory

- unit tests
- integration tests
- regression tests
- performance tests

No implementation is complete without passing tests.

---

# Phase 6 — Review

Verify

- architecture
- coding standards
- canonical compliance
- documentation
- performance

---

# Phase 7 — Documentation

Update

- canonical documents
- architecture diagrams
- README when required
- developer documentation

---

# Phase 8 — Materialization

Generate

- implementation batches
- GitHub issues
- pull request templates
- execution plans

---

# Phase 9 — Execution

Execution Layer performs

- implementation
- validation
- review
- completion

Execution never changes planning.

---

# Phase 10 — Continuous Improvement

After every execution

- collect metrics
- detect regressions
- identify improvements
- generate new recommendations

---

# Canonical Rules

Every Pull Request must:

- follow this workflow
- preserve architecture
- include tests
- include documentation updates
- pass validation


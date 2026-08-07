# Engineering Implementation Transition Package

Status: Draft

Date: 2026-08-07

---

## Dependency-Driven Implementation Order

1. Canonical Validation Engine
2. CSL Toolchain (lexer, parser, AST, compiler, diagnostics)
3. CDM Graph and Query Services
4. Governance Automation and Approval Workflows
5. Artifact Generation and Runtime Integration
6. Product Surface Integrations and Observability

## Executable Engineering Epics

### Epic 1 — Canonical Validation Engine
- Purpose: Enforce CSS/CDM/CSL conformance automatically.
- Dependencies: CDM-008, CDM-010, CSL-011, CSL-020.
- Inputs: canonical standards and repository artifacts.
- Outputs: validation results and actionable diagnostics.
- Acceptance Criteria: deterministic pass/fail output with traceable evidence.
- Validation Criteria: conformance suite coverage across standards families.
- Implementation Risks: false positives from partial rule coverage.
- Estimated Repository Impact: `tools/`, `tests/`, CI workflows.
- Implementation Sequence: first.
- Repository Areas: `tools/`, `.github/workflows/`, `tests/`.

### Epic 2 — CSL Toolchain Baseline
- Purpose: Implement lexer, parser, AST, and compiler pipeline for CSL v2.
- Dependencies: CSL-001, CSL-002, CSL-013, CSL-014, CSL-010.
- Inputs: CSL source modules and canonical standards.
- Outputs: parsed AST, diagnostics, compiled artifacts.
- Acceptance Criteria: conformance tests pass for grammar and AST invariants.
- Validation Criteria: CSL-020 suite plus error/diagnostics model checks.
- Implementation Risks: grammar ambiguity and compatibility drift.
- Estimated Repository Impact: `lib/`, `runtime/`, `tests/`.
- Implementation Sequence: second.
- Repository Areas: `lib/`, `runtime/`, `tests/`.

### Epic 3 — Canonical Graph and Query Services
- Purpose: Materialize document graph, index, namespace, and query execution.
- Dependencies: CDM-011 through CDM-016, CSL-025.
- Inputs: canonical documents and relationship metadata.
- Outputs: queryable canonical graph with traceability paths.
- Acceptance Criteria: deterministic graph build and query reproducibility.
- Validation Criteria: dependency integrity and orphan/cycle detection checks.
- Implementation Risks: inconsistent identifiers or stale index updates.
- Estimated Repository Impact: `lib/`, `generated/`, `tests/`.
- Implementation Sequence: third.
- Repository Areas: `lib/`, `generated/`, `tests/`.

### Epic 4 — Governance Execution Layer
- Purpose: Operationalize approvals, exceptions, and deprecation governance flows.
- Dependencies: CDM-007, CSL_V2_GOVERNANCE_MODEL, CSL_V2_DEPRECATION_POLICY.
- Inputs: change proposals, validation evidence, dependency impact records.
- Outputs: approved decisions, rejection rationale, governed audit trail.
- Acceptance Criteria: no unmanaged authority transitions.
- Validation Criteria: governance traceability for all standard-impacting changes.
- Implementation Risks: policy bypass through informal workflows.
- Estimated Repository Impact: `governance/`, `tools/`, workflow definitions.
- Implementation Sequence: fourth.
- Repository Areas: `governance/`, `tools/`, `.github/workflows/`.

### Epic 5 — Runtime and Product Integration
- Purpose: Connect canonical outputs to runtime services and product interfaces.
- Dependencies: CSL-026, CSL-027, CSL-028, architecture cycle controls.
- Inputs: compiled canonical artifacts and validated governance decisions.
- Outputs: runtime-executed capabilities and observed evidence streams.
- Acceptance Criteria: runtime behavior remains traceable to canonical intent.
- Validation Criteria: security, performance, and observability conformance checks.
- Implementation Risks: integration drift between generated artifacts and runtime.
- Estimated Repository Impact: `runtime/`, `docs/`, `tests/`.
- Implementation Sequence: fifth.
- Repository Areas: `runtime/`, `docs/`, `tests/`.

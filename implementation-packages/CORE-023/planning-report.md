# Phase 1 Implementation Roadmap

CORE: CORE-023

## Refactoring Plan

- Phase A: establish canonical implementation boundaries.
- Phase B: normalize repository structure to CSL.
- Phase C: consolidate duplicate engines and graph implementations.
- Phase D: implement compliance infrastructure.
- Phase E: harden governance kernel.
- Phase F: realign tests to CSL conformance levels.

## Ordered Implementation Plan

| Batch | Status | Risk | Priority | Affected |
|-------|--------|------|----------|----------|
| CORE-023-001 | READY | HIGH | CRITICAL | lib/python/canonical_parser, lib/python/canonical_repository, lib/python/engineering_engine |
| CORE-023-002 | READY | MEDIUM | HIGH | lib/python, lib/*.sh, bin |
| CORE-023-003 | READY | MEDIUM | HIGH | docs, standards/csl, implementation-packages |
| CORE-023-004 | PLANNED | HIGH | CRITICAL | lib/python/canonical_parser, lib/python/canonical_entities |
| CORE-023-005 | PLANNED | HIGH | CRITICAL | lib/python/canonical_entities, lib/python/knowledge_graph, lib/python/knowledge_graph_v2, lib/python/canonical_intelligence |
| CORE-023-006 | PLANNED | HIGH | CRITICAL | lib/python/validation_engine, lib/python/compliance_engine |
| CORE-023-007 | PLANNED | MEDIUM | HIGH | lib/python/engineering_engine, implementation-packages |
| CORE-023-008 | PLANNED | HIGH | HIGH | lib/python/engineering_engine, lib/python/autonomous_*, lib/python/workspace_* |
| CORE-023-009 | PLANNED | HIGH | CRITICAL | lib/python/rule_engine, lib/python/autonomous_execution_engine, lib/python/runtime |
| CORE-023-010 | PLANNED | MEDIUM | HIGH | ., .ai, docs, implementation-packages |
| CORE-023-011 | PLANNED | MEDIUM | HIGH | tests, standards/csl/tests |
| CORE-023-012 | PLANNED | LOW | MEDIUM | docs, implementation-packages |

## Details

### CORE-023-001

Objective: Define authoritative CSL subsystem architecture

Status: READY

Risk: HIGH

Priority: CRITICAL

Affected modules: lib/python/canonical_parser, lib/python/canonical_repository, lib/python/engineering_engine

Reason: Define the official subsystem map: source loader, parser, semantic analyzer, UEM, validator, compiler, generators, governance kernel, repository adapters, runtime integrations.

Suggested tests: tests/test_canonical_parser.sh, tests/test_compliance_engine.sh, tests/test_validation_engine.sh

### CORE-023-002

Objective: Inventory and classify modules

Status: READY

Risk: MEDIUM

Priority: HIGH

Affected modules: lib/python, lib/*.sh, bin

Reason: Classify every existing module into keep/refactor/replace/deprecate and freeze legacy modules as compatibility-only.

Suggested tests: tests/test_canonical_parser.sh, tests/test_compliance_engine.sh, tests/test_validation_engine.sh

### CORE-023-003

Objective: Publish formal compliance declaration

Status: READY

Risk: MEDIUM

Priority: HIGH

Affected modules: docs, standards/csl, implementation-packages

Reason: Create the supported feature declaration, conformance statement, known limitations register, and deviation register.

Suggested tests: tests/test_canonical_parser.sh, tests/test_compliance_engine.sh, tests/test_validation_engine.sh

### CORE-023-004

Objective: Build canonical source loader and parser boundary

Status: PLANNED

Risk: HIGH

Priority: CRITICAL

Affected modules: lib/python/canonical_parser, lib/python/canonical_entities

Reason: Replace the markdown-section parser approach with a real CSL lexical/syntax parsing boundary and diagnostics contract.

Suggested tests: tests/test_canonical_parser.sh, tests/test_compliance_engine.sh, tests/test_validation_engine.sh

### CORE-023-005

Objective: Add AST, semantic analysis, and UEM

Status: PLANNED

Risk: HIGH

Priority: CRITICAL

Affected modules: lib/python/canonical_entities, lib/python/knowledge_graph, lib/python/knowledge_graph_v2, lib/python/canonical_intelligence

Reason: Introduce first-class AST, semantic analyzer, and Universal Engineering Model subsystems.

Suggested tests: tests/test_canonical_parser.sh, tests/test_compliance_engine.sh, tests/test_validation_engine.sh

### CORE-023-006

Objective: Rework validation to normative CSL categories

Status: PLANNED

Risk: HIGH

Priority: CRITICAL

Affected modules: lib/python/validation_engine, lib/python/compliance_engine

Reason: Implement lexical, syntax, semantic, relationship, constraint, dependency, governance, and safety validation with deterministic diagnostics.

Suggested tests: tests/test_canonical_parser.sh, tests/test_compliance_engine.sh, tests/test_validation_engine.sh

### CORE-023-007

Objective: Reframe audit and planning outputs as generators

Status: PLANNED

Risk: MEDIUM

Priority: HIGH

Affected modules: lib/python/engineering_engine, implementation-packages

Reason: Move existing audit/planning/report engines behind compiler/UEM-driven generator contracts.

Suggested tests: tests/test_canonical_parser.sh, tests/test_compliance_engine.sh, tests/test_validation_engine.sh

### CORE-023-008

Objective: Consolidate duplicate graph and engine subsystems

Status: PLANNED

Risk: HIGH

Priority: HIGH

Affected modules: lib/python/engineering_engine, lib/python/autonomous_*, lib/python/workspace_*

Reason: Collapse overlapping graph, planning, execution, and validation abstractions around the authoritative CSL core.

Suggested tests: tests/test_canonical_parser.sh, tests/test_compliance_engine.sh, tests/test_validation_engine.sh

### CORE-023-009

Objective: Implement governance kernel

Status: PLANNED

Risk: HIGH

Priority: CRITICAL

Affected modules: lib/python/rule_engine, lib/python/autonomous_execution_engine, lib/python/runtime

Reason: Promote rule/policy pieces into mandatory permission, risk, approval, audit, authorization, and emergency-stop services.

Suggested tests: tests/test_canonical_parser.sh, tests/test_compliance_engine.sh, tests/test_validation_engine.sh

### CORE-023-010

Objective: Align repository structure with RFC-0009

Status: PLANNED

Risk: MEDIUM

Priority: HIGH

Affected modules: ., .ai, docs, implementation-packages

Reason: Introduce canonical separation for knowledge, generated outputs, runtime assets, and implementation responsibilities.

Suggested tests: tests/test_canonical_parser.sh, tests/test_compliance_engine.sh, tests/test_validation_engine.sh

### CORE-023-011

Objective: Remap tests to CSL conformance levels

Status: PLANNED

Risk: MEDIUM

Priority: HIGH

Affected modules: tests, standards/csl/tests

Reason: Map and expand tests to core reader, validator, compiler, reference implementation, and platform conformance categories.

Suggested tests: tests/test_canonical_parser.sh, tests/test_compliance_engine.sh, tests/test_validation_engine.sh

### CORE-023-012

Objective: Publish Phase 1 status and migration path

Status: PLANNED

Risk: LOW

Priority: MEDIUM

Affected modules: docs, implementation-packages

Reason: Publish conformance status, supported/unsupported capabilities, known limitations, and migration guidance.

Suggested tests: tests/test_canonical_parser.sh, tests/test_compliance_engine.sh, tests/test_validation_engine.sh


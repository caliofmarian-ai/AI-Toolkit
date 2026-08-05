# Module Classification Register

Version: 1.0.0

Status: Canonical

Classification: Implementation Inventory

CORE: CORE-023-002

Generated: Phase 1 Implementation

---

# 1. Purpose

This document classifies every module in the AI-Toolkit repository against the CSL subsystem architecture.

Every module is assigned a disposition: `KEEP`, `REFACTOR`, `REPLACE`, or `DEPRECATE`.

Legacy modules are frozen as compatibility-only.

---

# 2. Classification Legend

| Classification | Meaning |
|---------------|---------|
| CSL-CORE | Implements a mandatory CSL subsystem |
| CSL-SUPPORT | Supports CSL operations; not a mandated subsystem boundary |
| LEGACY | Maintained for compatibility only; no new features |
| GENERATED | Compiler/generator output; not authoritative |
| RUNTIME-STATE | Ephemeral runtime state; not canonical |

| Disposition | Meaning |
|------------|---------|
| KEEP | Reuse without modification |
| REFACTOR | Align to CSL subsystem contract |
| REPLACE | Superseded by CSL-CORE subsystem |
| DEPRECATE | Freeze; mark for eventual removal |

---

# 3. Python Modules

## canonical_parser

- Path: `lib/python/canonical_parser`
- Classification: CSL-CORE
- Disposition: REFACTOR
- CSL Subsystem: CSL Lexer, CSL Parser, AST, Semantic Analyzer
- Current state: markdown-section parser only; lexer and AST missing
- Required changes: add lexer, typed AST nodes, semantic analyzer
- Reusable: parser.py base (extend, not replace)

## canonical_entities

- Path: `lib/python/canonical_entities`
- Classification: CSL-CORE
- Disposition: REFACTOR
- CSL Subsystem: Canonical Entities, Universal Engineering Model
- Current state: good entity models; UEM API not published
- Required changes: add UEM module with Engineering Objects API
- Reusable: models.py (extend)

## canonical_repository

- Path: `lib/python/canonical_repository`
- Classification: CSL-CORE
- Disposition: REFACTOR
- CSL Subsystem: Source Loader
- Current state: basic document ingestion
- Required changes: formalize source loader abstraction
- Reusable: yes

## canonical_audit

- Path: `lib/python/canonical_audit`
- Classification: CSL-SUPPORT
- Disposition: KEEP
- CSL Subsystem: Audit Engine (support)
- Current state: functional audit reporting
- Required changes: none in Phase 1

## canonical_intelligence

- Path: `lib/python/canonical_intelligence`
- Classification: CSL-SUPPORT
- Disposition: KEEP
- CSL Subsystem: Semantic analysis support
- Current state: intelligence/analysis utilities
- Required changes: none in Phase 1; refactor in Phase 2

## validation_engine

- Path: `lib/python/validation_engine`
- Classification: CSL-CORE
- Disposition: REFACTOR
- CSL Subsystem: Validation Engine
- Current state: partial; heuristic categories
- Required changes: implement normative CSL validation categories
- Reusable: engine.py framework (extend)

## compliance_engine

- Path: `lib/python/compliance_engine`
- Classification: CSL-SUPPORT
- Disposition: KEEP
- CSL Subsystem: Compliance reporting support
- Current state: functional compliance scoring
- Required changes: none in Phase 1

## coverage_engine

- Path: `lib/python/coverage_engine`
- Classification: CSL-SUPPORT
- Disposition: KEEP
- Current state: functional coverage analysis
- Required changes: none in Phase 1

## drift_engine

- Path: `lib/python/drift_engine`
- Classification: CSL-SUPPORT
- Disposition: KEEP
- Current state: functional drift detection
- Required changes: none in Phase 1

## evidence_engine

- Path: `lib/python/evidence_engine`
- Classification: CSL-SUPPORT
- Disposition: KEEP
- Current state: functional evidence tracking
- Required changes: none in Phase 1

## engineering_engine

- Path: `lib/python/engineering_engine`
- Classification: CSL-CORE (partial) + CSL-SUPPORT
- Disposition: REFACTOR
- CSL Subsystem: Engineering Compiler, Artifact Generator Framework
- Current state: broad orchestration; not a clean compiler boundary
- Required changes: add compiler module, generator framework contracts
- Reusable: existing engines (keep, wrap under compiler boundary)

## rule_engine

- Path: `lib/python/rule_engine`
- Classification: CSL-CORE
- Disposition: REFACTOR
- CSL Subsystem: Safety and Governance Kernel
- Current state: rule and policy components; no unified kernel
- Required changes: add governance_kernel with Permission/Risk/Approval/Audit/EmergencyStop
- Reusable: base.py, rules/

## runtime

- Path: `lib/python/runtime`
- Classification: CSL-CORE
- Disposition: KEEP
- CSL Subsystem: Runtime Integrations
- Current state: comparatively mature
- Required changes: governance integration hardening (Phase 1 scope: interface only)
- Reusable: yes

## planning_engine

- Path: `lib/python/planning_engine`
- Classification: CSL-SUPPORT
- Disposition: KEEP
- Current state: functional planning engine
- Required changes: none in Phase 1

## planning_optimizer

- Path: `lib/python/planning_optimizer`
- Classification: CSL-SUPPORT
- Disposition: KEEP
- Required changes: none in Phase 1

## batch_generator

- Path: `lib/python/batch_generator`
- Classification: CSL-SUPPORT
- Disposition: KEEP
- Required changes: none in Phase 1

## batch_planner

- Path: `lib/python/batch_planner`
- Classification: CSL-SUPPORT
- Disposition: KEEP
- Required changes: none in Phase 1

## autonomous_execution_engine

- Path: `lib/python/autonomous_execution_engine`
- Classification: CSL-SUPPORT
- Disposition: KEEP
- Required changes: none in Phase 1; governance integration in Phase 1 scope

## autonomous_planner

- Path: `lib/python/autonomous_planner`
- Classification: CSL-SUPPORT
- Disposition: KEEP
- Required changes: none in Phase 1

## autonomous_planning_engine

- Path: `lib/python/autonomous_planning_engine`
- Classification: CSL-SUPPORT
- Disposition: KEEP
- Required changes: none in Phase 1

## knowledge_graph

- Path: `lib/python/knowledge_graph`
- Classification: CSL-SUPPORT
- Disposition: KEEP
- Current state: functional graph; overlaps with UEM semantically
- Required changes: none in Phase 1; superseded by UEM in Phase 2+

## knowledge_graph_v2

- Path: `lib/python/knowledge_graph_v2`
- Classification: CSL-SUPPORT
- Disposition: DEPRECATE
- Note: Duplicate of knowledge_graph; freeze as compatibility-only
- Required changes: none in Phase 1; migration path published in CORE-023-012

## knowledge_graph_engine.py

- Path: `lib/python/knowledge_graph_engine.py`
- Classification: LEGACY
- Disposition: DEPRECATE
- Note: Top-level module; predates module refactoring; freeze

## decision_engine.py

- Path: `lib/python/decision_engine.py`
- Classification: LEGACY
- Disposition: DEPRECATE
- Note: Top-level module; freeze

## foundation_audit.py

- Path: `lib/python/foundation_audit.py`
- Classification: LEGACY
- Disposition: DEPRECATE
- Note: Top-level module; freeze

## memory_engine.py

- Path: `lib/python/memory_engine.py`
- Classification: LEGACY
- Disposition: DEPRECATE
- Note: Top-level module; freeze

## repository_inventory.py

- Path: `lib/python/repository_inventory.py`
- Classification: LEGACY
- Disposition: DEPRECATE
- Note: Top-level module; freeze

## repository_profile.py

- Path: `lib/python/repository_profile.py`
- Classification: LEGACY
- Disposition: DEPRECATE
- Note: Top-level module; freeze

## autonomous_workflow_engine.py

- Path: `lib/python/autonomous_workflow_engine.py`
- Classification: LEGACY
- Disposition: DEPRECATE
- Note: Top-level module; freeze

## development_validator.py

- Path: `lib/python/development_validator.py`
- Classification: LEGACY
- Disposition: DEPRECATE
- Note: Superseded by development_validator/ module

## repository_engine

- Path: `lib/python/repository_engine`
- Classification: CSL-SUPPORT
- Disposition: KEEP
- Required changes: none in Phase 1

## discovery_engine

- Path: `lib/python/discovery_engine`
- Classification: CSL-SUPPORT
- Disposition: KEEP

## reporting_engine

- Path: `lib/python/reporting_engine`
- Classification: CSL-SUPPORT
- Disposition: KEEP

## dependency_engine

- Path: `lib/python/dependency_engine`
- Classification: CSL-SUPPORT
- Disposition: KEEP

## context_synchronization_engine

- Path: `lib/python/context_synchronization_engine`
- Classification: CSL-SUPPORT
- Disposition: KEEP

## semantic_engine

- Path: `lib/python/semantic_engine`
- Classification: CSL-SUPPORT
- Disposition: KEEP

## semantic_matching

- Path: `lib/python/semantic_matching`
- Classification: CSL-SUPPORT
- Disposition: KEEP

## workspace_index

- Path: `lib/python/workspace_index`
- Classification: CSL-SUPPORT
- Disposition: KEEP

## workspace_manager

- Path: `lib/python/workspace_manager`
- Classification: CSL-SUPPORT
- Disposition: KEEP

## workspace_orchestrator

- Path: `lib/python/workspace_orchestrator`
- Classification: CSL-SUPPORT
- Disposition: KEEP

## agent_runtime

- Path: `lib/python/agent_runtime`
- Classification: CSL-SUPPORT
- Disposition: KEEP

## agents

- Path: `lib/python/agents`
- Classification: CSL-SUPPORT
- Disposition: KEEP

## cli

- Path: `lib/python/cli`
- Classification: CSL-SUPPORT
- Disposition: KEEP

## common

- Path: `lib/python/common`
- Classification: CSL-SUPPORT
- Disposition: KEEP

---

# 4. Shell Modules

All shell modules in `lib/*.sh` are classified as LEGACY.

Disposition: DEPRECATE (freeze; do not add features).

| Module | Disposition |
|--------|------------|
| lib/context_engine.sh | DEPRECATE |
| lib/execution_engine.sh | DEPRECATE |
| lib/git_engine.sh | DEPRECATE |
| lib/github_engine.sh | DEPRECATE |
| lib/issue_engine.sh | DEPRECATE |
| lib/planner_engine.sh | DEPRECATE |
| lib/repository_inspector.sh | DEPRECATE |
| lib/repository_summary.sh | DEPRECATE |
| lib/review_engine.sh | DEPRECATE |
| lib/work_engine.sh | DEPRECATE |

Shell modules are preserved for backward compatibility only.

No new features shall be added to shell modules.

Python equivalents are authoritative.

---

# 5. Summary

| Classification | Count |
|---------------|-------|
| CSL-CORE | 7 |
| CSL-SUPPORT | 29 |
| LEGACY | 12 shell + 7 top-level py |
| GENERATED | 0 (to be created by compiler) |
| RUNTIME-STATE | .ai/ directory |

| Disposition | Count |
|------------|-------|
| KEEP | 29 |
| REFACTOR | 5 (canonical_parser, canonical_entities, canonical_repository, engineering_engine, rule_engine) |
| REPLACE | 0 |
| DEPRECATE | 19 (legacy modules) |

---

End of Module Classification Register.

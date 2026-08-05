# CSL Compliance Declaration

Version: 1.0.0

Status: Canonical

Classification: Conformance Statement

CORE: CORE-023-003

---

# 1. Purpose

This document is the formal compliance declaration of the AI-Toolkit Reference Implementation against the Canonical Specification Language v1.0.0.

Every conforming CSL implementation shall publish its compliance declaration.

This document fulfills that requirement.

---

# 2. Implementation Identity

| Property | Value |
|----------|-------|
| Implementation Name | AI-Toolkit |
| Implementation Version | 3.0.0 |
| CSL Standard Version | 1.0.0 |
| Implementation Phase | Phase 1 — Core Engineering Platform |
| Designation | First Official Reference Implementation |
| Repository | AI-Toolkit |

---

# 3. Conformance Level

Claimed Conformance Level: **Level 1 — Core Reader** (Implemented)

Targeted Conformance Level: **Level 4 — Reference Implementation** (Phase 1 target)

---

# 4. Supported Features

The following CSL features are currently supported:

## 4.1 Document Loading

- Load Canonical Documents from repository path
- Read document metadata (id, title, version, status)
- Parse document sections
- Recognize document relationships (dependency references)
- Parse scope (included/excluded)
- Parse invariants, objectives, purpose

## 4.2 Entity Recognition

- CANON document nodes
- Section nodes
- Module nodes
- Service nodes
- Engine nodes
- Component nodes

## 4.3 Lifecycle Status

- DRAFT
- REVIEW
- APPROVED / CANONICAL
- IMPLEMENTED
- MAINTAINED
- DEPRECATED
- ARCHIVED

## 4.4 Validation (Partial)

- Coverage validation (partial)
- Compliance scoring (partial)
- Drift detection (partial)

## 4.5 Runtime Platform

- HTTP API
- Scheduler
- Event bus
- Lifecycle management
- Health monitoring
- Metrics
- External interface registry

---

# 5. Unsupported Features

The following features are not yet implemented and are explicitly unsupported:

| Feature | CSL Reference | Phase Target |
|---------|--------------|-------------|
| CSL Lexer | Vol. IV Ch. 4–5 | Phase 1 |
| Typed AST Nodes | Vol. V Ch. 7 | Phase 1 |
| Deterministic Grammar Parser | Vol. IV Ch. 6–17 | Phase 1 |
| Formal Semantic Analyzer | Vol. III, Vol. V Ch. 8 | Phase 1 |
| Universal Engineering Model API | Vol. VI | Phase 1 |
| Normative Validation Categories | Vol. V Ch. 10 | Phase 1 |
| Generator Framework (UEM-driven) | RFC-0004 | Phase 1 |
| Governance Kernel (unified) | Vol. VII, RFC-0005 | Phase 1 |
| Diagnostic Error-Code Registry | Vol. V Ch. 13 | Phase 1 |
| Compiler Pipeline (end-to-end) | Vol. V | Phase 1 |
| Repository Adapter Contracts | RFC-0007 | Phase 1 |
| Knowledge Package Format | RFC-0008 | Phase 2 |
| Plugin Architecture | RFC Phase 2 | Phase 2 |
| AI Provider Interface | RFC-0006 | Phase 3+ |
| Cloud AI Provider Adapters | RFC Phase 4 | Phase 4 |
| Distributed Engineering | Phase 7 | Phase 7 |

---

# 6. Known Limitations

| ID | Component | Limitation |
|----|-----------|-----------|
| LIM-001 | canonical_parser | Parser is a markdown-section parser; not a formal CSL grammar/lexer |
| LIM-002 | canonical_parser | No typed AST nodes; document sections are untyped text blocks |
| LIM-003 | validation_engine | Validation categories are heuristic; not normative CSL categories |
| LIM-004 | engineering_engine | No clean compiler boundary; orchestration and compilation are mixed |
| LIM-005 | canonical_entities | No UEM API published; entity model is a data model, not an engineering model |
| LIM-006 | rule_engine | Governance components exist but no unified governance kernel |
| LIM-007 | knowledge_graph_v2 | Duplicate of knowledge_graph; creates architectural drift |
| LIM-008 | lib/python/*.py | 7 top-level Python files outside module structure |
| LIM-009 | lib/*.sh | 12 legacy shell modules; no Python equivalent for all |
| LIM-010 | repository structure | Does not conform to RFC-0009 canonical project structure |

---

# 7. Deviation Register

| ID | Type | Description | Justification | Resolution |
|----|------|-------------|---------------|-----------|
| DEV-001 | Implementation | Markdown parser instead of CSL grammar parser | Pre-CSL implementation; inherited from Phase 0 | CORE-023-004 |
| DEV-002 | Architecture | No explicit UEM layer | Pre-UEM implementation | CORE-023-005 |
| DEV-003 | Validation | Heuristic categories instead of normative | Pre-standard implementation | CORE-023-006 |
| DEV-004 | Generator | Generators not driven by UEM | Pre-compiler implementation | CORE-023-007 |
| DEV-005 | Governance | No unified governance kernel | Pre-governance implementation | CORE-023-009 |
| DEV-006 | Structure | Repository not RFC-0009 aligned | Pre-RFC implementation | CORE-023-010 |

---

# 8. Compatibility Statement

AI-Toolkit v3.0.0 is compatible with:

- CSL v1.0.0 — Level 1 (Core Reader): YES
- CSL v1.0.0 — Level 2 (Core Validator): PARTIAL
- CSL v1.0.0 — Level 3 (Compiler): NO (Phase 1 target)
- CSL v1.0.0 — Level 4 (Reference Implementation): NO (Phase 1 target)
- CSL v1.0.0 — Level 5 (Complete Engineering Platform): NO (Phase 5+ target)

---

# 9. Phase 1 Completion Criteria

Phase 1 is complete when:

- Level 4 conformance is achieved
- All mandatory Phase 1 components are implemented
- All Phase 1 automated tests pass
- Compliance declaration is updated to Level 4
- Deviation register shows DEV-001 through DEV-006 resolved

---

# 10. Migration Notes

Existing consumers of AI-Toolkit APIs should note:

- The canonical_parser API will gain lexer and AST modules in Phase 1; existing parse_file/parse_directory interface is preserved
- The canonical_entities models will gain UEM objects; existing dataclass models are preserved
- The validation_engine will gain normative categories; existing engine.validate() interface is preserved
- The engineering_engine will gain compiler and generator boundaries; existing planning/reporting modules are preserved

No breaking changes to existing public interfaces are planned for Phase 1.

---

End of CSL Compliance Declaration.

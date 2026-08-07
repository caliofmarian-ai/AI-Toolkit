# CSL v2 Reference Architecture

Version: 2.0.0

Status: Draft

Owner: AI CTO

---

# 1. Purpose

Defines the canonical architecture joining lexer/parser/compiler/runtime/validator/tooling.

---

# 2. Scope

This document is authoritative for CSL v2 governance and implementation operations in the AI-Toolkit repository.

---

# 3. Normative Requirements

1. Requirements in this document SHALL be applied repository-first with explicit evidence links.
2. All process decisions SHALL preserve Human Authority as final decision maker.
3. Every lifecycle transition SHALL produce traceable evidence artifacts.
4. Every dependency decision SHALL be aligned with CDM, CSS, and CSL core specifications.
5. Every unresolved exception SHALL be explicitly recorded and governance-tracked.

---

# 4. Validation and Evidence

Conformance SHALL be validated through documented checklists, dependency verification outputs, and approval records.

---

# 5. Governance

This document evolves only through governed change control and compatibility review.

# 6. Normative Process Requirements

1. Reference architecture SHALL define interfaces between lexer, parser, semantic analyzer, compiler, validator, runtime, and diagnostics.
2. Each interface SHALL define input schema, output schema, and error contract.
3. Architecture SHALL enforce separation of concerns and governance checkpoints.
4. Architecture SHALL preserve determinism and traceability end-to-end.
5. Architecture changes SHALL include migration impact analysis.

# CSL-005 — Relationship Model

Version: 2.0.0

Status: Draft

Classification: Canonical Standard

Standard Family: CSL

Identifier: CSL-005

Owner: AI CTO

Dependencies: Derived from CSL v2 dependency chain and CDM/CSS governance constraints

---

# 1. Purpose

This specification defines normative requirements for CSL v2 relationship model behavior.

---

# 2. Scope

Applies to canonical language authoring, parsing, compilation, validation, runtime behavior, and governance-controlled evolution within AI-Toolkit.

---

# 3. Normative Requirements

1. Relationships SHALL be typed, directional, and authority-aware.
2. Cardinality constraints SHALL be declared per relationship type.
3. Relationship validity SHALL include existence and compatibility checks.
4. Cycles SHALL be explicitly handled by policy.
5. Relationship model SHALL support traceability traversal.

---

# 4. Integration Contract

This specification SHALL integrate with grammar, lexer, AST, semantic, compiler, runtime, diagnostics, conformance, security, and governance standards as applicable.

---

# 5. Validation and Evidence

Conformance SHALL be validated by executable checks that emit deterministic diagnostics, rule IDs, artifact IDs, and compatibility status.

---

# 6. Governance

Human Authority is final for release approval, compatibility exceptions, and deprecation decisions.

---

# 7. Completion Criteria

This specification is complete when its requirements are machine-checkable, cross-references resolve, and conformance coverage exists.

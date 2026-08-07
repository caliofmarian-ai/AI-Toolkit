# CSL-003 — Semantic Type System

Version: 2.0.0

Status: Draft

Classification: Canonical Standard

Standard Family: CSL

Identifier: CSL-003

Owner: AI CTO

Dependencies: Derived from CSL v2 dependency chain and CDM/CSS governance constraints

---

# 1. Purpose

This specification defines normative requirements for CSL v2 semantic type system behavior.

---

# 2. Scope

Applies to canonical language authoring, parsing, compilation, validation, runtime behavior, and governance-controlled evolution within AI-Toolkit.

---

# 3. Normative Requirements

1. Type system SHALL include scalar, composite, graph, evidence, and governance reference types.
2. Type inference rules SHALL be deterministic and terminating.
3. Implicit narrowing conversions are prohibited unless explicitly declared.
4. Type compatibility SHALL be explicitly versioned.
5. Type errors SHALL map to CSL-021 taxonomy.

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

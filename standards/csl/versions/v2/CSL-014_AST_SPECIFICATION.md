# CSL-014 — AST Specification

Version: 2.0.0

Status: Draft

Classification: Canonical Standard

Standard Family: CSL

Identifier: CSL-014

Owner: AI CTO

Dependencies: Derived from CSL v2 dependency chain and CDM/CSS governance constraints

---

# 1. Purpose

This specification defines normative requirements for CSL v2 ast specification behavior.

---

# 2. Scope

Applies to canonical language authoring, parsing, compilation, validation, runtime behavior, and governance-controlled evolution within AI-Toolkit.

---

# 3. Normative Requirements

1. AST node set SHALL be finite, versioned, and schema-defined.
2. Every AST node SHALL include type, source span, and child ordering constraints.
3. AST SHALL support deterministic serialization and hashing.
4. AST invariants SHALL be validated before semantic analysis.
5. AST schema evolution SHALL follow compatibility policy.

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

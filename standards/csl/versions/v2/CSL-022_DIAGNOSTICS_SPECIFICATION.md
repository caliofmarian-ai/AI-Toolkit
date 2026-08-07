# CSL-022 — Diagnostics Specification

Version: 2.0.0

Status: Draft

Classification: Canonical Standard

Standard Family: CSL

Identifier: CSL-022

Owner: AI CTO

Dependencies: Derived from CSL v2 dependency chain and CDM/CSS governance constraints

---

# 1. Purpose

This specification defines normative requirements for CSL v2 diagnostics specification behavior.

---

# 2. Scope

Applies to canonical language authoring, parsing, compilation, validation, runtime behavior, and governance-controlled evolution within AI-Toolkit.

---

# 3. Normative Requirements

1. Diagnostics SHALL support human-readable and machine-readable output channels.
2. Diagnostics SHALL reference CSL-021 error taxonomy.
3. Diagnostics SHALL include context, severity, and actionable next step.
4. Output ordering SHALL be deterministic.
5. Diagnostics generation SHALL be covered by conformance tests.

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

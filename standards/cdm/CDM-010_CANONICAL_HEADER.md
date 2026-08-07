# CDM-010 — Canonical Header

Version: 1.0.0

Status: Draft

Classification: Canonical Standard

Standard Family: CDM

Identifier: CDM-010

Parent Standard: CDM-000_DOCUMENT_MODEL

Owner: AI CTO

---

# 1. Purpose

This specification defines the normative canonical header requirements for Canonical Document Model conformance.

---

# 2. Scope

Applies to canonical standards, governance artifacts, architecture artifacts, implementation packages, generated artifacts, and validation evidence governed by AI-Toolkit canonical controls.

---

# 3. Normative Requirements

1. Mandatory header fields SHALL include Identifier, Title, Version, Status, Owner, Classification, and Dependencies.
2. Header field semantics SHALL be type-checked against CDM schema definitions.
3. Identifier SHALL satisfy CDM-002 uniqueness constraints.
4. Dependencies declared in header SHALL resolve to existing canonical artifacts.
5. Header mismatch with document body metadata SHALL fail validation.

---

# 4. Integration Contract

This specification SHALL integrate with CSS authoring rules, CDM dependency/traceability/versioning standards, CSL machine-readable models, repository validation tooling, and governed runtime evidence capture.

---

# 5. Validation and Evidence

Conformance checks SHALL emit deterministic results and include artifact identifiers, rule identifiers, defect severity, and governance status. Validation evidence SHALL be stored as canonical records.

---

# 6. Governance

Human Authority is final for approval, exception handling, deprecation, and enforcement decisions.

---

# 7. Completion Criteria

This specification is complete when all requirements are enforceable, cross-references resolve, and no placeholder or undefined semantics remain.

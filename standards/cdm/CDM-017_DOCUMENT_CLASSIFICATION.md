# CDM-017 — Document Classification

Version: 1.0.0

Status: Draft

Classification: Canonical Standard

Standard Family: CDM

Identifier: CDM-017

Parent Standard: CDM-000_DOCUMENT_MODEL

Owner: AI CTO

---

# 1. Purpose

This specification defines the normative document classification requirements for Canonical Document Model conformance.

---

# 2. Scope

Applies to canonical standards, governance artifacts, architecture artifacts, implementation packages, generated artifacts, and validation evidence governed by AI-Toolkit canonical controls.

---

# 3. Normative Requirements

1. Classification levels SHALL at minimum distinguish normative, informative, governance, and evidence artifacts.
2. Classification SHALL control lifecycle, validation strictness, and release requirements.
3. Reclassification SHALL require governance approval and impact analysis.
4. Classification SHALL be reflected in canonical header metadata.
5. Undefined classification values SHALL fail validation.

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

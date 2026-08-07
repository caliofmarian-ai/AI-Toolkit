# 05 — Canonical Dependency Analysis

**Audit:** Canonical System Forensic Audit  
**Date:** 2026-08-07  
**Classification:** Engineering Artifact  
**Status:** Final  

---

## 1. Purpose

This document maps all dependency relationships between canonical components and analyzes the completeness of the canonical dependency chain.

---

## 2. Canonical Dependency Graph

### 2.1 Top-Level Dependencies

```
Governance (governance/)
    │
    ▼
CSS (standards/css/)
    │  Governs how specifications are written
    ▼
CDM (standards/cdm/)
    │  Governs document objects and identity
    ▼
CSL (standards/csl/)
    │  Expresses knowledge in machine-readable form
    ▼
Canonical Standards (docs/canonical/ — CANON series)
    │  Platform knowledge expressed using canonical language
    ▼
Engineering Engines (lib/python/engineering_engine/)
    │  Implementations derived from canonical knowledge
    ▼
Platforms (Trading Signals Platform, DROPi)
```

**Evidence:** This chain is explicitly defined in `standards/cdm/architecture/CDM_ARCHITECTURE.md`.

### 2.2 Inter-Component Dependencies

| Dependent | Depends On | Dependency Type |
|---|---|---|
| CDM | CSS | Structural: CDM documents must conform to CSS authoring rules |
| CSL | CDM | Containment: CSL documents are CDM-governed documents |
| CSL | CSS | Structural: CSL specifications must conform to CSS authoring rules |
| CANON | CSS | Structural: CANON documents must conform to CSS authoring rules |
| CANON | CDM | Containment: CANON documents are CDM-governed documents |
| Engineering Engines | CSL | Semantic: engines must be derived from canonical knowledge |
| Engineering Engines | CANON | Semantic: engines implement CANON specifications |
| Parser | CSL Grammar | Technical: parser implements CSL grammar |
| Validator | CSS-003, CSS-004 | Technical: validator enforces CSS normative rules |

---

## 3. Dependency Chain Breaks

### 3.1 Critical Break: CSL v2 Grammar

**FACT:** CSL v2 Grammar (CSL-002) is empty.

**Impact:** Any system intended to parse v2 CSL expressions has no grammar to implement against. The dependency chain from "Engineering Engines" upward to "CSL" is broken at the grammar level.

### 3.2 Significant Break: CDM Lifecycle and Validation

**FACT:** CDM-003 (Lifecycle), CDM-008 (Validation), and CDM-010 (Canonical Header) are placeholders.

**Impact:** No formal lifecycle states are defined for document validation. Any validator attempting to enforce CDM compliance has no authoritative lifecycle or validation specification to reference.

### 3.3 Partial Break: CSS ↔ CANON Compliance

**FACT:** No automated enforcement of CSS rules exists.

**Impact:** CANON documents may drift from CSS compliance without detection. The CSS → CANON dependency is notionally defined but not mechanically enforced.

---

## 4. Shared Components

### 4.1 CSL Shared Directory

**FACT:** `standards/csl/shared/` contains multiple sub-directories shared across CSL versions:

| Directory | Contents |
|---|---|
| `shared/ontology/` | 18 ontology model documents |
| `shared/metamodel/` | 8 metamodel documents |
| `shared/knowledge/` | 13 knowledge domain documents |
| `shared/schemas/` | 5 core schema documents |
| `shared/reference/` | Glossary, keyword reference, entity reference, relationship reference |
| `shared/rfc/` | 10 RFCs covering CSL evolution |
| `shared/examples/` | Basic, advanced, reference project examples |
| `shared/tests/` | Compiler, conformance, and validator test suite specs |
| `shared/implementation/` | Implementation phases document |

**Engineering Conclusion:** The shared directory is the most semantically rich part of CSL. It contains the ontological foundation and metamodel that both v1 and v2 should depend on. This content would normally be treated as the semantic backbone of the language.

### 4.2 CDM Shared Schemas

**FACT:** `standards/cdm/shared/schemas/` contains four JSON schemas:
- `document.schema.json`
- `header.schema.json`
- `metadata.schema.json`
- `relationship.schema.json`

**Engineering Conclusion:** These JSON schemas provide machine-enforceable structure that could be used immediately for document validation, even before CDM-008 (Validation Model) is written.

---

## 5. Dependency Completeness Score

| Dependency | Defined | Implemented | Automated |
|---|---|---|---|
| Governance → CSS | Yes | Yes (CSS written) | No |
| CSS → CDM | Yes | Partial (CDM-000 to CDM-002 only) | No |
| CSS → CSL | Yes | Yes (CSL v1 written per CSS precursor) | No |
| CDM → CSL | Yes | Yes (structurally) | No |
| CSL → Canonical Standards | Yes | No (CSL v2 empty) | No |
| Canonical Standards → Engineering Engines | Yes | Partial | No |
| Engineering Engines → Platforms | Yes | Partial | No |

**Overall dependency chain completeness: Conceptually defined, partially implemented, not automated at any layer.**

---

## 6. Dependency Risks

| Risk | Description |
|---|---|
| Grammar gap | CSL v2 grammar empty — any v2 parser would be speculative |
| Validation gap | CDM validation model missing — no formal validation rules |
| Compliance gap | CSS rules not enforced — documents may not conform |
| Knowledge expression gap | CANON documents in Markdown, not in CSL — machine-readable canonical knowledge effectively zero |

# 14 — Recommended Continuation Strategy

**Audit:** Canonical System Forensic Audit  
**Date:** 2026-08-07  
**Classification:** Engineering Artifact  
**Status:** Final  

---

## 1. Purpose

This document recommends a concrete continuation strategy for the Canonical System based on the audit findings.

---

## 2. Strategic Context

The audit has established that the Canonical System is Foundation-Ready but not production-ready. The system has a coherent architecture and solid core in CSS and CSL v1, but has two major gaps:

1. **CSL v2 is empty** — the language evolution that would enable machine-readable canonical knowledge has not been authored.
2. **No validator exists** — canonical compliance cannot be mechanically enforced.

These gaps must be closed before the platform can achieve its autonomous engineering vision.

---

## 3. Recommended Execution Phases

### Phase 1 — Establish Enforcement (Immediate)

**Goal:** Stop canonical drift. Enforce CSS compliance on all new canonical documents.

**Actions:**
1. Build CSS Document Validator (V-01)
   - Input: CSS-003 (Normative Language), CSS-004 (Specification Checklist)
   - Output: Python script that validates any markdown file against CSS rules
   - Estimated effort: ~100 lines of Python
2. Build CDM Header Validator (V-02)
   - Input: CDM-001, CDM-002, `standards/cdm/shared/schemas/`
   - Output: Python script that validates canonical document headers
   - Estimated effort: ~150 lines of Python
3. Integrate validators into GitHub Actions CI
4. Populate empty READMEs for `standards/cdm/README.md` and `standards/css/README.md`

**Outcome:** Every new canonical document is automatically validated on PR. Canonical drift becomes detectable.

---

### Phase 2 — Complete CDM Core (Short-Term)

**Goal:** Complete the CDM specifications required for validator and governance work.

**Priority order:**
1. CDM-010: Canonical Header — defines the mandatory header structure for all documents
2. CDM-008: Validation Model — defines formal validation rules
3. CDM-003: Document Lifecycle — defines document lifecycle states
4. CDM-004: Dependency Model — defines dependency relationships
5. CDM-005: Traceability Model — defines traceability requirements
6. CDM-006: Versioning Model — defines versioning rules

**Do not start:** CDM-009 (Executable Document Model) and CDM-011 through CDM-019 until Phase 3.

**Outcome:** CDM core is complete enough to support a full CDM validator.

---

### Phase 3 — Author CSL v2 Grammar (Critical Path)

**Goal:** Unblock all CSL v2 work by authoring the grammar specification.

**Actions:**
1. Author CSL-002 (Grammar) — the minimum required for any v2 work
2. Author CSL-013 (Lexer Specification) — formally defines tokenization
3. Author CSL-003 (Semantic Type System) — defines type semantics
4. Write one v2 example document demonstrating v2 syntax

**Note:** Do not author all 47 v2 specifications at once. Focus on the critical path: grammar → lexer → semantic type system. Everything else depends on these three.

**Outcome:** CSL v2 has a normative grammar. Parser work can begin.

---

### Phase 4 — Validate CSL v1 Implementation

**Goal:** Validate that the existing Python parser correctly implements CSL v1 grammar.

**Actions:**
1. Write one end-to-end integration test using `standards/csl/shared/examples/`
2. Document parser conformance level against v1 grammar
3. Fix any grammar violations found

**Outcome:** CSL v1 parser is validated. Foundation for v2 parser exists.

---

### Phase 5 — Express First CANON in CSL

**Goal:** Prove that CSL v2 can express real canonical knowledge.

**Actions:**
1. Select one CANON document (recommend CANON-001 or CANON-003)
2. Re-express its content in CSL v2 syntax
3. Parse and validate the CSL expression
4. Use this as the conformance reference for all future CSL work

**Outcome:** CSL v2 is proven capable. Machine-readable canonical knowledge exists for one document.

---

### Phase 6 — Complete Remaining CDM and CSL v2

**Goal:** Complete the remaining CDM and CSL v2 specifications.

**Sequence:** CDM-007 through CDM-019, then CSL-004 through CSL-030.

**Note:** This phase is large. It should be executed across multiple engineering epics, not in one batch.

---

## 4. What NOT To Do

| Action | Reason to avoid |
|---|---|
| Add new CANON documents before CSL v2 grammar exists | Increases the knowledge expression gap |
| Build v2 runtime before v2 grammar is authored | Will need to be rewritten |
| Author all 47 v2 specs in one sprint | Leads to superficial placeholder content |
| Implement CDM-011 through CDM-019 before CDM-003 through CDM-010 | Out of dependency order |

---

## 5. Success Criteria

The Canonical System can be considered production-ready when:

- [ ] CSS validator enforced in CI on every PR
- [ ] CDM header validator enforced in CI on every PR
- [ ] CSL v2 grammar authored and declared normative
- [ ] CSL v1 parser validated end-to-end
- [ ] At least one CANON document expressed in CSL v2
- [ ] CDM-003 through CDM-010 authored
- [ ] Version governance defined for CDM and CSS

---

## 6. Recommended Next Engineering Epic

See `docs/planning/CANONICAL_SYSTEM_NEXT_EPIC.md` for the formal next epic definition.

The recommended next epic is:

**"Canonical System Phase 1 — Enforcement and Grammar Foundation"**

Scope: Build CSS and CDM validators. Integrate into CI. Author CSL-002 grammar. Validate v1 parser.

This is a small, high-impact epic that closes the two most critical gaps: enforcement and grammar.

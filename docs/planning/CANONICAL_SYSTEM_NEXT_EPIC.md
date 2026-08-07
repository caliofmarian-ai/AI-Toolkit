# CANONICAL_SYSTEM_NEXT_EPIC.md

**Type:** Engineering Epic Planning Document  
**Status:** Ready for Execution  
**Date:** 2026-08-07  
**Reference Audit:** `docs/audits/canonical-system/`  

---

## 1. What Has Already Been Completed

### 1.1 Canonical System Forensic Audit

A complete forensic audit of the AI-Toolkit Canonical System was performed during a Copilot engineering session. The audit examined:

- All CSL v1 specifications (8 volumes, ~5,700 lines)
- All CSL v2 files (47 files, all empty)
- All CDM specifications (3 substantive, 17 placeholders)
- All CSS specifications (6 substantive, templates, architecture)
- CANON specification series (80+ documents)
- Prior audit artifacts in `docs/audits/`
- Repository structure, naming conventions, cross-references

The findings have been materialized as a permanent audit package in `docs/audits/canonical-system/` (15 documents).

### 1.2 CSS — Complete Core

CSS-000 through CSS-005 are authored and substantive. CSS provides the meta-standard for how specifications are written. It is the most complete canonical sub-system.

### 1.3 CDM — Core Foundation

CDM-000 (Document Model), CDM-001 (Metadata Model), and CDM-002 (Identifier Model) are authored. JSON schemas for document, header, metadata, and relationship exist in `standards/cdm/shared/schemas/`.

### 1.4 CSL v1 — Specification Complete

All 8 CSL v1 volumes are authored and frozen as normative. CSL v1 covers foundations through reference implementation. A Python parser exists in `lib/python/canonical_parser/`.

### 1.5 CANON Series — Knowledge Captured

80+ CANON specifications have been authored covering system architecture, development workflow, agent specifications, autonomous execution, observability, governance, and AI-CTO platform capabilities.

---

## 2. What Remains Unfinished

### 2.1 CSL v2 — Not Started

All 47 CSL v2 specification files are empty. CSL v2 is a declared structure without content. The most critical missing piece is CSL-002 (Grammar).

### 2.2 CDM Peripheral Specifications — All Placeholders

CDM-003 through CDM-019 are 21-line placeholder stubs. Seventeen specifications covering lifecycle, dependencies, traceability, versioning, governance, validation, executable documents, headers, graph, query language, index, namespace, schema, relationships, classification, security, and reference implementation are not authored.

### 2.3 No Canonical Validator

No tooling enforces CSS rules, CDM headers, or CSL grammar. Canonical compliance is entirely manual.

### 2.4 CSL v1 Parser Not Validated

The Python parser exists but has no end-to-end integration test.

### 2.5 CANON Knowledge Not Machine-Readable

All CANON documents are in natural language Markdown. No CANON document is expressed in CSL.

---

## 3. Why the Canonical System Must Be Completed First

### 3.1 The Platform's Foundation Is the Canonical Language

The AI-Toolkit's autonomous engineering capability is predicated on machine-readable canonical knowledge. The AI-CTO cannot reason over natural language Markdown documents the same way it can reason over formally structured CSL. Until CSL v2 is capable of expressing canonical knowledge, the autonomous engineering vision cannot be fully realized.

### 3.2 Canonical Drift Is Accumulating

Every CANON document added in Markdown increases the migration effort when CSL v2 is completed. Every new specification that violates CSS rules adds to technical debt. Without a validator, this drift is undetectable and accelerating.

### 3.3 Major Platform Work Depends on Canonical Foundations

The AI Platform evolution documented in CANON-058 through CANON-080 describes complex platform capabilities: commercial platform, cloud deployment, consciousness kernel, memory architecture, goal engine, autonomous governance. All of these depend on the canonical language being able to formally express their specifications. Without CSL v2, these specifications cannot be machine-enforced.

### 3.4 Cost of Deferral Increases Exponentially

The canonical language specification work that was deferred during rapid platform design growth (the CANON v3–v5 expansion) must eventually be done. Each engineering epic that adds more natural language specifications without completing the canonical language foundation makes the eventual migration harder.

---

## 4. Recommended Execution Order for the Next Engineering Epic

**Epic Name:** Canonical System Phase 1 — Enforcement and Grammar Foundation

**Scope:** Small, high-impact. No new platform capabilities.

### 4.1 Step 1: CSS Document Validator

Build a Python script that validates any markdown file against CSS-003 and CSS-004 requirements.

**Input specs:**
- `standards/css/CSS-003_NORMATIVE_LANGUAGE.md`
- `standards/css/CSS-004_SPECIFICATION_CHECKLIST.md`

**Output:** `tools/canonical_validator/css_validator.py` (or similar)

### 4.2 Step 2: CDM Header Validator

Build a Python script that validates canonical document headers against CDM-001, CDM-002, and JSON schemas.

**Input specs:**
- `standards/cdm/CDM-001_METADATA_MODEL.md`
- `standards/cdm/CDM-002_IDENTIFIER_MODEL.md`
- `standards/cdm/shared/schemas/`

### 4.3 Step 3: CI Integration

Add a GitHub Actions workflow that runs both validators on every PR. Fail the PR if any canonical document does not pass validation.

### 4.4 Step 4: Author CSL-002 Grammar

Author the CSL v2 Grammar specification.

**Approach:** Start from the v1 grammar in `standards/csl/versions/v1/04_GRAMMAR.md` and extend it to cover v2 capabilities. Use the shared ontology and metamodel for semantic grounding.

**Outcome:** CSL-002 is normative. V2 lexer and parser work can begin.

### 4.5 Step 5: Validate CSL v1 Parser

Write one end-to-end integration test that parses a CSL v1 example document and validates the output structure.

**Input:** `standards/csl/shared/examples/basic/HELLO_CSL.md` or similar

---

## 5. What This Epic Does NOT Include

- No new CANON documents
- No new platform capabilities
- No runtime implementation
- No CDM-003 through CDM-019 (except CDM-010 if needed for validator)
- No CSL v2 parser or compiler
- No commercial platform work

---

## 6. Expected Duration

This epic is scoped for a single focused engineering session or sprint. It is explicitly scoped small.

---

## 7. Success Criteria

- [ ] CSS validator passes on all existing CDM-000, CDM-001, CDM-002, CSS-000 through CSS-005
- [ ] CSS validator fails on CDM placeholder stubs (by design — they are incomplete)
- [ ] CI workflow rejects PRs with non-compliant canonical documents
- [ ] CSL-002 Grammar has content and is marked Draft status minimum
- [ ] One end-to-end CSL v1 parser test passes

---

## 8. References

- Audit Executive Summary: `docs/audits/canonical-system/00_EXECUTIVE_SUMMARY.md`
- Risk Assessment: `docs/audits/canonical-system/13_ENGINEERING_RISK_ASSESSMENT.md`
- Continuation Strategy: `docs/audits/canonical-system/14_RECOMMENDED_CONTINUATION_STRATEGY.md`
- Validator Requirements: `docs/audits/canonical-system/11_FUTURE_VALIDATOR_REQUIREMENTS.md`
- Grammar Analysis: `docs/audits/canonical-system/06_GRAMMAR_ANALYSIS.md`

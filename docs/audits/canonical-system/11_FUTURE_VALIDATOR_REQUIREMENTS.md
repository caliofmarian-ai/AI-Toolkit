# 11 — Future Validator Requirements

**Audit:** Canonical System Forensic Audit  
**Date:** 2026-08-07  
**Classification:** Engineering Artifact  
**Status:** Final  

---

## 1. Purpose

This document specifies the requirements for future canonical validators based on the audit findings. These requirements are derived from CSS, CDM, and CSL specifications.

---

## 2. Validator Taxonomy

Three distinct validators are required for the Canonical System:

| Validator | Name | Scope | Priority |
|---|---|---|---|
| V-01 | CSS Document Validator | Validates documents against CSS authoring rules | High |
| V-02 | CDM Header Validator | Validates canonical document headers against CDM metadata model | High |
| V-03 | CSL Syntax Validator | Validates CSL expressions against grammar | Medium (blocked on CSL-002) |

---

## 3. V-01 — CSS Document Validator

### 3.1 Purpose

Validate any markdown file against CSS-004 (Specification Checklist) and CSS-003 (Normative Language) requirements.

### 3.2 Input

A markdown file claimed to be a canonical specification.

### 3.3 Required Checks

Based on CSS-004 content:

**Structure Checks:**
- [ ] Document has a front matter section with Version, Status, Classification, Standard Family, Identifier, Owner
- [ ] Document has a numbered Abstract or Purpose section
- [ ] Document has a numbered Scope section
- [ ] Document has a numbered Objectives section
- [ ] Document contains at least one normative requirement (SHALL, MUST)
- [ ] Document is not a placeholder stub (not less than 50 lines)

**Normative Language Checks (CSS-003):**
- [ ] Requirements use SHALL, MUST, SHOULD, MAY, MUST NOT, SHOULD NOT
- [ ] No mixing of normative terms across the same requirement
- [ ] Informal requirements use plain present tense

**Naming Convention Checks:**
- [ ] Filename matches the declared Identifier field
- [ ] Version format is X.Y.Z
- [ ] Status is one of: Draft, Normative, Deprecated, Archived

### 3.4 Implementation Notes

CSS-004 provides a checklist that maps directly to validator rules. Implementation is straightforward — ~100 lines of Python using standard markdown parsing.

**Source specifications:** `standards/css/CSS-004_SPECIFICATION_CHECKLIST.md`, `standards/css/CSS-003_NORMATIVE_LANGUAGE.md`

---

## 4. V-02 — CDM Header Validator

### 4.1 Purpose

Validate the canonical document header against the CDM metadata model and the JSON schemas in `standards/cdm/shared/schemas/`.

### 4.2 Input

A markdown file with a canonical header section.

### 4.3 Required Checks

Based on CDM-001 (Metadata Model) and CDM-002 (Identifier Model):

**Metadata Checks:**
- [ ] Identifier field present and non-empty
- [ ] Identifier matches declared Standard Family prefix
- [ ] Version field present and in X.Y.Z format
- [ ] Status field present and in allowed value set
- [ ] Classification field present
- [ ] Owner field present

**Identifier Checks:**
- [ ] Identifier format: `[FAMILY]-[NNN]` or `[FAMILY]-[NNN]_[TITLE]`
- [ ] Numeric portion is zero-padded to three digits
- [ ] Family is one of: CSL, CDM, CSS, CANON, or declared custom family

**Header Schema Validation:**
- [ ] Validate against `standards/cdm/shared/schemas/header.schema.json`
- [ ] Validate against `standards/cdm/shared/schemas/metadata.schema.json`

### 4.4 Blocked By

CDM-010 (Canonical Header specification) is currently a placeholder. Full header validation requirements will be defined when CDM-010 is authored. However, CDM-001 and CDM-002 plus the JSON schemas provide sufficient basis for an initial validator.

---

## 5. V-03 — CSL Syntax Validator

### 5.1 Purpose

Validate a CSL source file against the CSL grammar.

### 5.2 Blocked By

**CSL-002 (Grammar) is empty.** This validator cannot be specified or implemented until CSL v2 grammar is authored.

For v1 CSL content only, a partial validator could be built against the v1 grammar rules in `standards/csl/versions/v1/04_GRAMMAR.md`.

### 5.3 Requirements When Unblocked

When CSL-002 is authored:
- [ ] Lexical validation against CSL-013 (Lexer Specification)
- [ ] Syntactic validation against CSL-002 (Grammar)
- [ ] AST construction per CSL-014 (AST Specification)
- [ ] Semantic type checking per CSL-003 (Semantic Type System)
- [ ] Error reporting per CSL-021 (Error Model)
- [ ] Diagnostic output per CSL-022 (Diagnostics)

---

## 6. Integration Requirements

### 6.1 CI/CD Integration

All validators must be integrable into GitHub Actions to run on every PR.

The check sequence should be:
1. V-01 (CSS) runs first — structural validation
2. V-02 (CDM) runs second — identity validation
3. V-03 (CSL) runs last — when available

### 6.2 Validator Output Format

Validators must produce:
- Exit code 0 on success
- Exit code 1 on validation failure
- Human-readable error messages with file path and line number
- Machine-readable JSON output for CI integration

---

## 7. Implementation Priority

| Priority | Validator | Blocking Factor | Estimated Effort |
|---|---|---|---|
| 1 | V-01 CSS Document Validator | None — CSS-003 and CSS-004 are complete | ~100 lines Python |
| 2 | V-02 CDM Header Validator | Partial — CDM-001, CDM-002, JSON schemas exist | ~150 lines Python |
| 3 | V-03 CSL Syntax Validator | Blocked — CSL-002 grammar empty | Requires grammar first |

---

## 8. Validator Assessment Summary

**Immediate action available:** V-01 and V-02 can be built now from existing specifications.

**Blocked action:** V-03 requires CSL v2 grammar to be authored first.

**Impact of not building validators:** Canonical drift is undetectable. New documents may not conform to CSS or CDM requirements. Repository quality degrades silently.

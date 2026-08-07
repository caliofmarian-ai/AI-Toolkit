# 05 — Lifecycle and Version Evolution

**Research Package:** Canonical Foundation Deep Research  
**Document:** 05  
**Status:** Complete  
**Date:** 2026-08-07  

---

## 1. Purpose

This document traces the complete lifecycle and version evolution of the Canonical Foundation — the sequence of phases through which CSL, CDM, and CSS were created, evolved, and stopped.

---

## 2. The Canonical System Lifecycle Phases

### 2.1 Phase 1 — CSL v1 Authoring

**FACT:** `standards/csl/versions/v1/` contains 8 specification volumes totaling approximately 5,694 lines, all marked `Status: Normative` and `Version: 1.0.0`.

**FACT:** The volumes are numbered Vol I through Vol VIII and follow a deliberate architectural sequence: Foundations → Language → Semantic Model → Grammar → Compiler → Universal Engineering Model → Safety and Governance → Reference Implementation.

**ENGINEERING CONCLUSION:** CSL v1 was authored as a complete, coherent language specification. The sequential volume numbering and consistent internal cross-references suggest these documents were authored in order, with each volume building on the previous. This was a disciplined, high-quality specification authoring effort.

**ENGINEERING HYPOTHESIS:** CSL v1 was authored in a single concentrated engineering effort — not incrementally over time. The consistency of style, formatting, and cross-referencing across all 8 volumes suggests a single authoring session or a tightly coordinated sequence of sessions.

### 2.2 Phase 2 — CSL v1 Freeze and v2 Scaffolding

**FACT:** `standards/csl/versions/v1/README.md` states: "Version 1 is frozen. No new engineering features shall be introduced into Version 1. Future language evolution SHALL occur exclusively in Version 2."

**FACT:** 47 files exist in `standards/csl/versions/v2/`, all empty (zero bytes).

**ENGINEERING CONCLUSION:** After v1 was frozen, a structural scaffolding pass was performed that created all 47 v2 specification files simultaneously. All files are empty — this is a structural declaration, not an authoring effort.

**ENGINEERING HYPOTHESIS:** The v2 file structure was created by an automated or scripted process — perhaps a single command or a template-based scaffolding tool — because it would be unusual for 47 distinct files to all be exactly zero bytes if they were created manually one at a time. A manual process would typically include at least a front-matter header on some files.

**ENGINEERING HYPOTHESIS:** The intent of the scaffolding was to provide a structure for subsequent authoring sessions. The sessions that would fill in the content never occurred, leaving the scaffolding permanently empty.

### 2.3 Phase 3 — CDM Authoring

**FACT:** CDM-000 (1,083 lines), CDM-001 (344 lines), and CDM-002 (307 lines) are substantive specifications.

**FACT:** CDM-003 through CDM-019 are all 21-line placeholder stubs with this content: "> Placeholder / This specification will be authored according to the Canonical Document Model authoring process."

**ENGINEERING CONCLUSION:** CDM was partially authored after CSL v1. CDM-000 through CDM-002 were written with full content — these form the core identity model. CDM-003 through CDM-019 were scaffolded in the same placeholder pattern as CSL v2 — structural declarations without content.

**ENGINEERING HYPOTHESIS:** CDM was introduced to address a gap in CSL v1: CSL v1 defines a language but not the container the language lives in. CDM was designed to formalize the document-as-object model. CDM-000 through CDM-002 were authored first because they define the minimum required for document identity, which is needed to validate any canonical document at all.

### 2.4 Phase 4 — CSS Authoring

**FACT:** CSS-000 through CSS-005 are all substantive (183 to 371 lines each). All are marked `Status: Draft`.

**ENGINEERING CONCLUSION:** CSS was authored as a complete core set — all six core specifications have content. Unlike CSL v2 and CDM peripherals, CSS was not scaffolded and then abandoned; it was fully authored.

**ENGINEERING HYPOTHESIS:** CSS was written as a response to quality drift in the canonical document corpus — as more specifications were authored (CSL v1, CDM), inconsistencies in authoring style became apparent, motivating the creation of a meta-standard for specification writing. CSS was retrofitted as the governing standard for all existing specifications.

### 2.5 Phase 5 — CANON Series Expansion

**FACT:** 80+ CANON specification documents exist in `docs/canonical/`. These are written in natural language Markdown.

**FACT:** CANON documents cover: system architecture, development workflow, agent specifications, workspace indexes, observability, autonomous execution, performance benchmarks, testing, roadmaps, system invariants, AI-CTO platform capabilities, Telegram control plane, owner intelligence, project memory, workspace registry, knowledge persistence, and many more domains.

**ENGINEERING CONCLUSION:** The CANON series expanded dramatically — covering the full AI-Toolkit platform design surface — while CSL v2 and CDM peripherals remained empty. The platform's knowledge grew far beyond the canonical language's ability to represent it formally.

**ENGINEERING CONCLUSION:** The CANON series represents the intended content that CSL v2 was supposed to express formally. The natural language CANON documents are forward declarations of knowledge that was designed to eventually be expressed in CSL.

### 2.6 Current State

**ENGINEERING CONCLUSION:** The Canonical System is currently frozen between Phase 4 and Phase 5. CSL v1 is frozen. CSL v2 is scaffolded but empty. CDM has a foundation. CSS has a complete core. CANON has a large natural language corpus. No validator exists. The evolution stopped at the point of transition from specification to tooling.

---

## 3. Why the Evolution Stopped

### 3.1 The v2 Grammar Gap as the Primary Cause

**ENGINEERING CONCLUSION:** The most proximate cause of the evolution stopping is the missing CSL-002 Grammar. Without v2 grammar, no v2 parser can be built. Without a parser, no v2 compiler can be built. Without a compiler, no CSL v2 documents can be validated or compiled. The entire v2 toolchain is blocked on one document.

**ENGINEERING HYPOTHESIS:** The v2 grammar was the first document that needed to be written in the v2 authoring session, and writing a formal language grammar is the most technically demanding specification task in the entire canonical system. The difficulty of this specific task may have been the primary reason the v2 authoring session did not proceed.

### 3.2 The CDM Scaffold Pattern

**ENGINEERING CONCLUSION:** CDM-003 through CDM-019 follow the same scaffolding-without-content pattern as CSL v2. This suggests the same engineering decision was made in both cases: declare the structure, defer the content. The deferral in both cases appears to have been permanent — at least until the next engineering epic.

### 3.3 The Platform Growth Outpacing the Foundation

**ENGINEERING CONCLUSION:** The CANON series grew to 80+ documents covering sophisticated platform capabilities while the foundational language (CSL v2) remained empty. This is a common pattern in large engineering projects: feature work (the CANON series describing capabilities) advances faster than infrastructure work (CSL v2, validators, CDM completeness). The result is increasing technical debt — each new CANON document adds to the migration effort when CSL v2 is eventually completed.

### 3.4 No External Forcing Function

**ENGINEERING HYPOTHESIS:** In the absence of an automated validator that would fail PRs with non-compliant canonical documents, there was no forcing function that required completing the canonical infrastructure before adding more canonical content. Platform growth continued freely. If a CI validator had been in place from Phase 2 onward, it would have forced resolution of each canonical gap before allowing the platform to proceed. The absence of enforcement allowed indefinite deferral.

---

## 4. Document Lifecycle Model

### 4.1 Canonical Document Status Values

**FACT:** CSS-004 defines allowed Status values as: Draft, Normative, Deprecated, Archived.

**ENGINEERING CONCLUSION:** The canonical document lifecycle has four states:

```
[new] → Draft → Normative → Deprecated → Archived
                           ↗
               [also: Draft → Archived if abandoned]
```

**ENGINEERING CONCLUSION:** Current state of the canonical document corpus by status:

| Status | Documents |
|---|---|
| Normative | CSL v1 volumes (all 8) |
| Draft | CSS-000 through CSS-005, CDM-000 through CDM-002, CANON documents |
| Not specified (empty) | CSL v2 all 47, CDM-003 through CDM-019 placeholders |
| Deprecated | None |
| Archived | None |

**ENGINEERING CONCLUSION:** No canonical document has been formally deprecated or archived. The placeholder CDM specs and empty CSL v2 files do not carry a lifecycle status — they are pre-lifecycle, not in a valid lifecycle state.

### 4.2 CDM-003 Lifecycle Model Dependency

**FACT:** CDM-003 (Document Lifecycle) is a placeholder.

**ENGINEERING CONCLUSION:** The formal lifecycle state machine for canonical documents has not been specified. CSS-004 names the status values, but the transitions between states, the governance required for each transition, and the rules for lifecycle state enforcement are not specified. CDM-003 would provide this — but it is empty.

---

## 5. Version Model

### 5.1 CSL Versioning Strategy

**FACT:** `standards/csl/migration/CSL_VERSIONING_AND_MIGRATION_STRATEGY.md` exists but was not confirmed to have content.

**FACT:** The v2 file `CSL_V2_MIGRATION_GUIDE.md` is empty.

**FACT:** The v2 file `CSL_V1_TO_V2_MAPPING.md` is empty.

**ENGINEERING CONCLUSION:** The versioning strategy for CSL and the migration path from v1 to v2 have not been documented. This means that when CSL v2 is authored, the compatibility decisions — what is backwards compatible, what is breaking, how v1 documents are migrated — must be determined from scratch. No engineering work has been done to define the migration path.

### 5.2 CDM Versioning

**FACT:** CDM-006 (Versioning Model) is a placeholder.

**ENGINEERING CONCLUSION:** The CDM versioning model has not been specified. How CDM documents are versioned, how version conflicts are resolved, and how version history is preserved are all undefined.

### 5.3 The Version Identifier Convention

**FACT:** CSS-004 requires `Version: X.Y.Z` format for all canonical documents.

**FACT:** CDM-002 (Identifier Model) defines the canonical identifier format as `[FAMILY]-[NNN]_[TITLE]`.

**ENGINEERING CONCLUSION:** The surface-level version identifier convention is established (X.Y.Z) and consistently applied across the existing canonical documents. The deeper versioning semantics — what constitutes a major vs minor vs patch change, who governs version changes, how version history is maintained — are not specified.

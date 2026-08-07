# 07 — Unfinished Work

**Research Package:** Canonical Foundation Deep Research  
**Document:** 07  
**Status:** Complete  
**Date:** 2026-08-07  

---

## 1. Purpose

This document determines precisely what remains unfinished before the Canonical Foundation can be considered structurally complete — and in what order that work must proceed.

This document differs from the prior audit's "Remaining Work Dashboard" in `docs/ENGINEERING_ARTIFACTS.md` in that it provides architectural reasoning for each gap, not merely a task list.

---

## 2. Definition of Completeness

### 2.1 The Completeness Criterion

**ENGINEERING CONCLUSION:** The Canonical Foundation is complete when:

1. Every canonical specification can be validated automatically against its governing standard
2. Every canonical document has a formally verifiable identity
3. The canonical language (CSL) can express any canonical knowledge that the CANON series describes
4. Canonical knowledge is machine-readable in a formally specified form
5. The compilation pipeline from CSL source to Engineering Artifacts is operational end-to-end

None of these conditions are currently satisfied.

### 2.2 The Minimum Viable Completeness Criterion

**ENGINEERING CONCLUSION:** The Minimum Viable Completeness (MVC) — the minimum state at which the Canonical Foundation can begin enforcing itself — requires:

1. A CSS validator that checks document authoring compliance
2. A CDM header validator that checks document identity compliance
3. CSL-002 (v2 Grammar) authored at Draft level
4. The CSL v1 parser validated end-to-end against at least one test case

The MVC is achievable without completing all 47 CSL v2 specifications or all 17 CDM placeholders.

---

## 3. Critical Path — What Must Be Done First

### 3.1 Step 1: CSS Validator (Unblocked)

**Status:** Unblocked. All required specifications exist.

**What's needed:**
- CSS-003 (Normative Language) — exists, 323 lines
- CSS-004 (Specification Checklist) — exists, 218 lines

**What it produces:**
- Automated validation of any markdown document against CSS authoring rules
- Ability to detect: missing front matter fields, absent normative language, placeholder status

**Why it matters architecturally:** CSS is the root of the dependency chain. Until CSS enforcement exists, no canonical document can be reliably classified as CSS-compliant. This affects the entire canonical corpus.

**Blocking nothing:** The CSS validator depends on no other unimplemented work.

---

### 3.2 Step 2: CDM Header Validator (Unblocked)

**Status:** Unblocked. All required specifications exist.

**What's needed:**
- CDM-001 (Metadata Model) — exists, 344 lines
- CDM-002 (Identifier Model) — exists, 307 lines
- `standards/cdm/shared/schemas/header.schema.json` — exists
- `standards/cdm/shared/schemas/metadata.schema.json` — exists

**What it produces:**
- Automated validation of canonical document headers for correct identifier format, version format, status values, mandatory fields
- JSON schema validation of document headers

**Why it matters architecturally:** CDM identity validation is the second enforcement layer. Without it, documents can have malformed or missing identifiers, corrupting the canonical identity model.

---

### 3.3 Step 3: CI Integration (Depends on Steps 1 and 2)

**Status:** Blocked on Steps 1 and 2.

**What it produces:**
- Every PR that touches a canonical document is automatically validated
- Non-compliant canonical documents fail CI before merge

**Why it matters architecturally:** CI enforcement creates the forcing function. Once validators run in CI, canonical drift becomes detectable and blockable. Without CI enforcement, validators have no authority.

---

### 3.4 Step 4: CSL-002 Grammar — Draft (Unblocked but Technically Demanding)

**Status:** Unblocked. The v1 grammar exists as reference material. No external dependency.

**What's needed:**
- CSL v1 Volume IV (Grammar, 744 lines) — exists as reference
- CSL v1 Volume II (Language Specification, 724 lines) — exists as reference
- Engineering judgment to determine v2 scope

**What it produces:**
- A Draft grammar specification for CSL v2
- The foundation for a v2 lexer and parser

**Why it matters architecturally:** CSL-002 is the single highest-priority unwritten specification in the Canonical System. Every other CSL v2 specification depends on it. No v2 toolchain can be built without it.

**What CSL-002 must answer:**
- Is v2 grammar a superset of v1? Or a breaking redesign?
- Does v2 use a formal grammar notation (BNF, EBNF, PEG)?
- What new constructs does v2 grammar introduce?
- How does the v2 grammar handle references to other canonical documents?
- How does the v2 grammar handle the module system?

---

### 3.5 Step 5: CSL v1 Parser End-to-End Test (Unblocked)

**Status:** Unblocked. Parser exists. Test fixtures exist.

**What's needed:**
- `lib/python/canonical_parser/` — exists
- `standards/csl/shared/examples/basic/HELLO_CSL.md` — exists
- `standards/csl/shared/examples/basic/MINIMAL_PROJECT.md` — exists

**What it produces:**
- One end-to-end test confirming the parser accepts a valid v1 CSL document and produces a correct parse tree

**Why it matters architecturally:** Without an end-to-end test, the parser's conformance to the v1 grammar is unknown. Any canonical work that assumes the parser is correct may be built on a faulty foundation.

---

## 4. Second Tier — Required Before Full CDM Is Complete

### 4.1 CDM-010: Canonical Header Definition

**FACT:** CDM-010 is a placeholder.

**ENGINEERING CONCLUSION:** The canonical header format — the specific fields, order, and constraints that every canonical document's header must contain — is not formally defined. CDM-001 and CDM-002 define metadata and identifiers, but CDM-010 would define the precise header syntax that appears at the top of every canonical document.

**Blocking:** CDM header validator completeness. Until CDM-010 is authored, the header validator enforces what CDM-001 and CDM-002 specify but lacks the complete header structure definition.

---

### 4.2 CDM-003: Document Lifecycle

**FACT:** CDM-003 is a placeholder.

**ENGINEERING CONCLUSION:** The canonical document lifecycle state machine — what states exist (Draft, Normative, Deprecated, Archived), what transitions are allowed, what governance is required for each transition — is not formally defined. CSS-004 names the states; CDM-003 would define their meaning.

**Blocking:** Lifecycle-aware validation. A validator that enforces lifecycle rules cannot be built without this specification.

---

### 4.3 CDM-008: Validation Model

**FACT:** CDM-008 is a placeholder.

**ENGINEERING CONCLUSION:** The validation model — what constitutes a valid canonical document, what classes of validation exist, what the severity levels of violations are — is not specified. This is the architectural specification that would unify the validation behaviors of CSS validator, CDM validator, and CSL validator into a coherent model.

---

## 5. Third Tier — Required for Machine-Readable Semantics

### 5.1 Shared Ontology (21 empty files)

**ENGINEERING CONCLUSION:** The shared ontology is the machine-readable formalization of CSL's semantic vocabulary. Until ontology files have content, the semantic model exists only in prose. All 21 ontology model files are empty.

**What they provide when authored:**
- ENTITY_MODEL — formal definition of what an Entity is
- RELATIONSHIP_MODEL — formal definition of what a Relationship is
- KNOWLEDGE_MODEL — formal definition of what Knowledge is
- TYPE_SYSTEM — formal definition of the CSL type hierarchy
- POLICY_MODEL, RULE_MODEL, CONSTRAINT_MODEL — governance semantics
- LIFECYCLE_MODEL — lifecycle state semantics
- GOVERNANCE_MODEL — governance framework

---

### 5.2 Shared Metamodel (8 empty files)

**ENGINEERING CONCLUSION:** The metamodel formally defines the meta-concepts from which the ontology is built. All 8 metamodel files are empty.

**What they provide when authored:**
- METAMODEL — the top-level model of models
- META_ENTITY — what makes something an entity
- META_RELATIONSHIP — what makes something a relationship
- META_TYPE — what makes something a type
- META_RULE, META_POLICY, META_CONSTRAINT, META_NAMESPACE — meta-governance concepts

---

## 6. Distant Tier — Required for Full v2 Platform

### 6.1 CSL v2 Core Language (CSL-000 through CSL-007)

**ENGINEERING CONCLUSION:** The entire CSL v2 core language is unwritten. Before any v2 platform capability can be built, the language itself must be specified. Priority within this tier:

1. CSL-000: Language Manifest (defines v2 scope and design goals)
2. CSL-002: Grammar (critical path, enables parser)
3. CSL-001: Engineering Alphabet (foundation of grammar)
4. CSL-003: Semantic Type System (enables semantic validation)
5. CSL-004: Object Model (defines the object system)
6. CSL-005: Relationship Model (defines the relationship type system)
7. CSL-006: Knowledge Representation (defines how knowledge is expressed)
8. CSL-007: Reasoning Model (enables knowledge inference)

---

### 6.2 CSL v2 Tooling (CSL-008 through CSL-016)

**ENGINEERING CONCLUSION:** No v2 tooling specification exists. The tooling tier (runtime, compiler, validator, parser, lexer, AST, package format, module system) cannot be implemented until the core language is specified.

---

### 6.3 CDM Peripheral Specifications (CDM-004 through CDM-019)

**ENGINEERING CONCLUSION:** Fourteen CDM peripheral specifications are placeholders. These enable: dependency tracking, traceability, versioning, governance, executable documents, document graph, query language, indexing, namespacing, schema, relationship model, classification, security, and reference implementation. All are important but none are on the MVC critical path.

---

## 7. Summary: Canonical Foundation Completeness Map

| Component | Current State | MVC Critical? | Blocks What |
|---|---|---|---|
| CSS-000 through CSS-005 | Complete | No (governance only) | CSS validator design |
| CDM-000, CDM-001, CDM-002 | Complete | Yes (used by validators) | CDM header validator |
| CDM-003 (Lifecycle) | Placeholder | No (second tier) | Lifecycle enforcement |
| CDM-008 (Validation) | Placeholder | No (second tier) | Validation model |
| CDM-010 (Header) | Placeholder | No (second tier) | Complete header validator |
| CDM-004 through CDM-019 | Placeholder | No (third/distant tier) | Advanced CDM features |
| CSS Validator | Not built | **Yes** | CI enforcement |
| CDM Header Validator | Not built | **Yes** | CI enforcement |
| CI Integration | Not built | **Yes** | Canonical drift prevention |
| CSL v1 Volume I-VIII | Complete, frozen | Yes (v1 knowledge only) | v1 parser |
| CSL v1 Parser | Prototype, untested | **Yes (needs test)** | v1 parser reliability |
| CSL v1 End-to-End Test | Not built | **Yes** | Parser reliability |
| CSL-002 (v2 Grammar) | Empty | **Yes** | Entire v2 toolchain |
| CSL v2 Core (CSL-000..007) | Empty (except 002 gap) | Yes (after 002) | v2 language |
| CSL v2 Tooling (CSL-008..016) | Empty | No (after core) | v2 platform |
| Shared Ontology (21 files) | Empty | No (second tier) | Machine-readable semantics |
| Shared Metamodel (8 files) | Empty | No (second tier) | Formal model theory |
| CANON v1-v5 Series | Complete (natural language) | No | AI knowledge consumption |
| CANON in CSL | Not started | No (future) | Machine-readable CANON |

---

## 8. The One Thing That Would Unlock the Most Progress

**ENGINEERING CONCLUSION:** A single document — CSL-002 (Grammar) — is the highest-leverage unwritten specification in the entire Canonical Foundation.

Without CSL-002:
- No v2 parser can be designed
- No v2 lexer can be designed
- No v2 AST can be specified
- No v2 compiler can be built
- No v2 validator can be built
- CSL v2 remains permanently scaffolded

With CSL-002 even at Draft level:
- The v2 language scope is defined
- A v2 lexer can be designed
- A v2 parser can begin
- The remaining 29 CSL v2 specifications can be authored in parallel
- The CANON series migration path becomes visible

The next Engineering Epic should treat CSL-002 as its primary authoring objective.

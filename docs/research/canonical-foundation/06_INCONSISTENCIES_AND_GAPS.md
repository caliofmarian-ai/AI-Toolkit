# 06 — Inconsistencies and Gaps

**Research Package:** Canonical Foundation Deep Research  
**Document:** 06  
**Status:** Complete  
**Date:** 2026-08-07  

---

## 1. Purpose

This document identifies:

- Internal inconsistencies within the Canonical Foundation
- Contradictions between canonical documents
- Duplicated concepts across the three sub-systems
- Undefined concepts referenced but not specified
- Incomplete concepts with missing specification coverage
- Architectural risks arising from current gaps
- Future consequences of unresolved gaps

---

## 2. Inconsistencies

### 2.1 Inconsistency I-001: CSS Compliance of CSL v1

**DESCRIPTION:** CSL v1 volumes were authored before CSS existed. They do not conform to CSS authoring standards.

**EVIDENCE:**
- CSS-003 requires uppercase normative terms (SHALL, MUST, SHOULD). CSL v1 volumes use lowercase ("shall", "must") and mix the two forms inconsistently.
- CSS-001 requires a mandatory front matter section. CSL v1 volumes use a Volume/Chapter format instead of the CSS numbered section format.
- CSS-004 requires explicit `Identifier:` and `Standard Family:` fields. CSL v1 volumes do not have these fields.

**ENGINEERING CONCLUSION:** CSL v1 documents are normative but do not comply with the CSS authoring standard that was later defined to govern all canonical specifications. This creates an architectural awkwardness: the most authoritative CSL specification (v1) does not conform to the meta-standard (CSS).

**CONSEQUENCE:** When CSS validators are implemented, they will fail on CSL v1 documents. If validators are applied to the full canonical corpus, CSL v1 will generate false positives. This must be addressed either by: (a) exempting CSL v1 from CSS compliance as grandfathered normative documents, or (b) authoring CSL v1 compliant wrappers that reference the original volumes.

**SEVERITY:** Medium. Functionally harmless today (no validator exists), but creates a design decision that must be made when validators are built.

---

### 2.2 Inconsistency I-002: Dual Naming Convention in CSL v2

**DESCRIPTION:** CSL v2 uses two different naming conventions within the same directory.

**EVIDENCE:**
- Numbered specifications: `CSL-NNN_TITLE_SPECIFICATION.md`
- Process documents: `CSL_V2_PROCESS_NAME.md`

**ENGINEERING CONCLUSION:** This inconsistency is cosmetic (since all files are empty) but will need resolution when content is authored. It is unclear whether the process documents (GOVERNANCE_MODEL, LIFECYCLE, MIGRATION_GUIDE, etc.) are intended to be CDM-governed canonical documents with full identifiers or process artifacts outside the formal identifier system.

**SEVERITY:** Low. Cosmetic inconsistency in an empty directory.

---

### 2.3 Inconsistency I-003: CSS Document Status Discrepancy

**DESCRIPTION:** CSS documents are marked `Status: Draft` despite being the most complete and authoritative CSS sub-system.

**EVIDENCE:** CSS-000 through CSS-005 all have `Status: Draft` in their headers.

**ENGINEERING CONCLUSION:** No CSS document has been promoted to `Status: Normative`. This is structurally inconsistent with the fact that CSS is the governing meta-standard that all other canonical documents must follow. If CSS is a Draft, what is it governing? The meta-standard should be normative before it can be enforceable.

**CONSEQUENCE:** When a CSS validator is built, the status check may need to handle the Bootstrap Problem: CSS-003 and CSS-004 must be normative before they can be used as validation sources, but they are currently Draft.

**SEVERITY:** Medium. Requires a governance decision to promote CSS core specifications to Normative before enforcement begins.

---

### 2.4 Inconsistency I-004: The Ownership of the Execution Model

**DESCRIPTION:** The execution model is claimed by two different specifications.

**EVIDENCE:**
- CSL-026 is titled "Execution Model Specification" (CSL sub-system)
- CDM-009 is titled "Executable Document Model" (CDM sub-system)

**ENGINEERING CONCLUSION:** There is a conceptual overlap between "how CSL knowledge executes" (CSL-026) and "what an executable document is" (CDM-009). These could be complementary specifications (CDM-009 defines the document format; CSL-026 defines the execution semantics) or they could be competing specifications with overlapping scope.

**ENGINEERING HYPOTHESIS:** CDM-009 was intended to define the envelope for executable documents (the document as an object) while CSL-026 was intended to define the execution semantics (what execution means for CSL knowledge). The boundary is not defined because both are empty.

**SEVERITY:** High. When these specifications are authored, their boundary must be explicitly resolved to avoid conceptual duplication.

---

### 2.5 Inconsistency I-005: Terminology Inconsistency — "Module"

**DESCRIPTION:** The keyword `Module` appears in the CSL v1 keyword reference as a structural unit, but `CSL-016` in v2 is titled "Module System Specification" suggesting a more elaborate concept.

**EVIDENCE:**
- `standards/csl/shared/reference/keywords/KEYWORDS_REFERENCE.md` defines `Module` as "Organizational unit grouping related knowledge."
- `standards/csl/versions/v2/CSL-016_MODULE_SYSTEM_SPECIFICATION.md` is empty, but the title implies a module system (import/export, namespacing, package resolution).

**ENGINEERING CONCLUSION:** In v1, a Module is a simple organizational grouping. In v2, a Module System suggests a more powerful concept with explicit import/export semantics, versioning, and dependency resolution. The v1 and v2 meanings of "module" may be incompatible.

**SEVERITY:** Medium. Requires explicit scope definition in CSL-016 when authored.

---

## 3. Contradictions

### 3.1 Contradiction C-001: Who Governs the Canonical Foundation?

**DESCRIPTION:** Two different governance roots are implied by different parts of the canonical system.

**EVIDENCE:**
- CDM Architecture defines: `Governance → CDM → CSL → Canonical Standards`
- CSS defines: `CSS → CDM → CSL`
- The architecture implies CSS governs CDM which governs CSL — making CSS the root
- CDM Architecture implies an external "Governance" layer above CDM — but this layer is not defined

**ENGINEERING CONCLUSION:** There is a mild contradiction between CDM's view of itself (governed by an external "Governance" entity) and CSS's view of itself (the meta-standard governing all standards). If CSS governs CDM, what is the "Governance" layer in the CDM architecture? This is unresolved.

**ENGINEERING HYPOTHESIS:** The "Governance" node in CDM architecture was a placeholder for a future governance specification that was never authored. CSS may have been intended to be that governance specification, but was named differently and focused on authoring rather than governance.

**SEVERITY:** Low. Conceptually confusing but not operationally blocking.

---

### 3.2 Contradiction C-002: CSL Grammar Determinism vs. Prose Specification

**DESCRIPTION:** CSL v1 Grammar requires "The grammar shall be deterministic" but specifies the grammar in prose, not in a formal grammar notation.

**EVIDENCE:**
- Volume IV, Chapter 2: "The grammar shall be: Deterministic."
- The grammar itself is written in prose descriptions, not in BNF/EBNF/PEG.

**ENGINEERING CONCLUSION:** A prose grammar cannot be mechanically verified as deterministic. The requirement is normative but cannot be enforced against the specification itself. Two independent implementations of the v1 grammar might make different parsing decisions for ambiguous inputs while both claiming conformance.

**SEVERITY:** High. This is a fundamental quality issue with the v1 grammar specification. It means "conforming parser" cannot be rigorously verified.

---

### 3.3 Contradiction C-003: CDM Status vs. CDM Completeness

**DESCRIPTION:** CDM-000 describes itself as the governing foundation for all canonical documents, but 17 of its 20 child specifications are placeholders. A governing model cannot govern what it has not specified.

**EVIDENCE:**
- CDM-000 references CDM-003 through CDM-019 as required components of a complete CDM
- All 17 of these are placeholders

**ENGINEERING CONCLUSION:** CDM is self-contradictory in its completeness claims. It defines itself as the authoritative document model but is missing 85% of its specified components.

**SEVERITY:** Medium. Acknowledged in the prior audit; not a surprise. The placeholder structure is an accurate representation of intent that exceeds current completion.

---

## 4. Duplicated Concepts

### 4.1 Duplication D-001: Validation Rules Across Three Standards

**DESCRIPTION:** Validation rules are defined in multiple places:

- CSS-004 (Specification Checklist) — validation rules for canonical documents
- CDM-008 (Validation Model, placeholder) — validation model for CDM documents
- CSL v1 Volume IV — semantic validation as layer 4 of the grammar
- `standards/cdm/shared/schemas/` — JSON schemas for document validation

**ENGINEERING CONCLUSION:** Four separate validation specifications exist (one partially, three partially or as placeholders). They address different validation scopes (authoring quality vs. document identity vs. semantic correctness vs. schema conformance) but their boundaries are not explicitly defined. When validators are built, the scope of each must be explicitly delineated.

**SEVERITY:** Medium. Likely designed as complementary tiers but not explicitly coordinated.

---

### 4.2 Duplication D-002: Identifier System Across CDM and CSL

**DESCRIPTION:** Both CDM and CSL define identifier systems.

**EVIDENCE:**
- CDM-002 (Identifier Model) defines canonical document identifiers
- CSL v1 Volume II (Language Specification) defines CSL identifier grammar
- CSL Glossary defines "Identifier" as "unique canonical name for an engineering object"

**ENGINEERING CONCLUSION:** CDM identifiers are document-level identifiers (FAMILY-NNN_TITLE). CSL identifiers are knowledge-level identifiers (names for entities within a CSL document). These operate at different levels and are complementary, not duplicative. However, the relationship between them — can a CDM document identifier be used as a CSL reference? — is not explicitly specified.

**SEVERITY:** Low. Different levels of the hierarchy; complementary rather than truly duplicated.

---

### 4.3 Duplication D-003: Governance Specifications

**DESCRIPTION:** Governance concepts appear in multiple specifications across CDM and CSL.

**EVIDENCE:**
- CDM-007 (Governance Model, placeholder)
- CSL v1 Volume VII (Safety and Governance)
- CSL-027 (Security Model, empty v2)
- CSS-001 (Standard Authoring Guide includes governance rules)

**ENGINEERING CONCLUSION:** Governance is addressed at multiple levels: CSL specifies knowledge governance (what can be expressed and how), CDM specifies document governance (how documents are changed and controlled), and CSS specifies authoring governance (how specifications are written). These are distinct governance domains. The overlap is conceptual, not technical. However, the boundaries need explicit definition when CDM-007 and CSL-027 are authored.

**SEVERITY:** Low-Medium. Requires explicit coordination when those specifications are authored.

---

## 5. Undefined Concepts

### 5.1 Undefined U-001: The Engineering Alphabet

**DESCRIPTION:** CSL-001 is titled "Engineering Alphabet" — but this concept does not appear in CSL v1 or in any existing shared document.

**ENGINEERING HYPOTHESIS:** The "Engineering Alphabet" may refer to the primitive elements of CSL v2 — the atomic units from which all CSL expressions are composed. In formal language theory, an alphabet is the set of terminal symbols. In CSL v2, this may be the set of primitive tokens or fundamental concepts from which all engineering knowledge is expressed.

**STATUS:** Undefined. Requires authoring of CSL-001 to clarify.

---

### 5.2 Undefined U-002: The Reasoning Model

**DESCRIPTION:** CSL-007 is titled "Reasoning Model" — but reasoning capabilities are not defined anywhere in the existing canonical system.

**ENGINEERING HYPOTHESIS:** The Reasoning Model would define how a CSL v2 engine reasons over canonical knowledge to derive conclusions — e.g., inferring that a Capability is satisfied when all its child Requirements are satisfied, or that a Risk is active when its triggering Constraints are violated. This is inference logic over the knowledge graph.

**STATUS:** Undefined. Represents a significant undocumented capability.

---

### 5.3 Undefined U-003: Knowledge Packages

**DESCRIPTION:** RFC-0008 is titled "Knowledge Package Format" suggesting a formal packaging mechanism for CSL knowledge.

**ENGINEERING HYPOTHESIS:** A Knowledge Package would be a distributable bundle of CSL documents with a manifest, versioning, and dependency declarations — analogous to a npm package or Python pip package but for engineering knowledge. This would enable sharing reusable canonical knowledge across projects.

**STATUS:** Undefined. Requires RFC-0008 authoring.

---

### 5.4 Undefined U-004: The Standard Library

**DESCRIPTION:** CSL-017 is titled "Standard Library Specification" — implying CSL v2 has a standard library of reusable knowledge constructs.

**ENGINEERING HYPOTHESIS:** The standard library would provide common, pre-defined CSL constructs that any CSL document can import — e.g., standard risk categories, common requirement patterns, governance frameworks. This is the CSL equivalent of a programming language's standard library.

**STATUS:** Undefined.

---

## 6. Incomplete Concepts

### 6.1 Incomplete IC-001: The Type System

**DESCRIPTION:** CSL v1 Volume III defines a type hierarchy but the machine-readable type system (`standards/csl/shared/ontology/TYPE_SYSTEM.md`) is empty.

**CONSEQUENCE:** No compiler can validate type correctness algorithmically without a machine-readable type system. The type system exists only in prose.

---

### 6.2 Incomplete IC-002: The Shared Ontology

**DESCRIPTION:** `standards/csl/shared/ontology/` contains 21 model files, all empty. This includes: ARTIFACT_MODEL, CAPABILITY_MODEL, DECISION_MODEL, DEPENDENCY_MODEL, ENGINE_MODEL, ENTITY_MODEL, EVENT_MODEL, GOAL_MODEL, GOVERNANCE_MODEL, KNOWLEDGE_MODEL, LIFECYCLE_MODEL, MATURITY_MODEL, ONTOLOGY, POLICY_MODEL, RELATIONSHIP_MODEL, REPOSITORY_MODEL, RULE_MODEL, SECURITY_MODEL, TRACEABILITY_MODEL, TYPE_SYSTEM.

**CONSEQUENCE:** The formal ontology that would make CSL semantics machine-interpretable does not exist. Every model that would ground CSL semantics in a shared vocabulary is empty.

---

### 6.3 Incomplete IC-003: The Metamodel

**DESCRIPTION:** `standards/csl/shared/metamodel/` contains 8 metamodel files, all empty. This includes: METAMODEL, META_CONSTRAINT, META_ENTITY, META_NAMESPACE, META_POLICY, META_RELATIONSHIP, META_RULE, META_TYPE.

**CONSEQUENCE:** The metamodel — the model of the model — does not exist as an artifact. The semantic model specification in Volume III is all that exists, and it is prose.

---

## 7. Architectural Risks

### 7.1 Risk R-001: CSL v2 Drift from v1

**DESCRIPTION:** As time passes without v2 being authored, the platform capabilities described in CANON documents may diverge from what v1 can express, creating a larger migration gap.

**ENGINEERING CONCLUSION:** Each new CANON document added without CSL v2 completion adds to the eventual migration effort. The gap between v1 expressibility and the platform's actual knowledge surface widens continuously.

**SEVERITY:** High. Accumulating technical debt.

---

### 7.2 Risk R-002: No Canonical Enforcement

**DESCRIPTION:** Without a validator, any document can claim to be canonical without satisfying any canonical requirement. The word "canonical" loses precision.

**CONSEQUENCE:** The term "canonical" may already be informally applied to documents that would fail CSS, CDM, or CSL validation if validators existed. This means the canonical corpus may include non-canonical documents, creating a false baseline.

**SEVERITY:** High. Undermines the reliability of the canonical foundation.

---

### 7.3 Risk R-003: Parser Drift

**DESCRIPTION:** The existing Python parser (`lib/python/canonical_parser/`) was written without end-to-end test validation. It may have diverged from the v1 grammar specification without detection.

**CONSEQUENCE:** A parser that does not match the grammar specification produces non-conforming output silently. Any canonical documents validated by this parser may have been validated against the wrong grammar.

**SEVERITY:** Medium. Requires end-to-end parser test to assess.

---

### 7.4 Risk R-004: Prose Grammar Interpretation Divergence

**DESCRIPTION:** The v1 grammar is in prose. Two different engineers implementing a parser from this grammar may make different decisions on ambiguous constructs.

**CONSEQUENCE:** Multiple CSL v1 parsers could produce different ASTs from the same input document without either implementation being demonstrably wrong. This undermines the determinism guarantee.

**SEVERITY:** Medium. Mitigated by having only one parser, but unmitigated for future implementations.

---

### 7.5 Risk R-005: Bootstrap Problem for Canonical Validators

**DESCRIPTION:** Canonical validators must themselves be canonical artifacts. But until validators exist, canonical artifacts cannot be validated. The first validator cannot be validated by the system it is validating.

**CONSEQUENCE:** The first generation of canonical validators must be produced outside the canonical system's own validation constraints. This is a known bootstrapping problem (similar to compilers compiling themselves) but must be explicitly acknowledged and handled.

**SEVERITY:** Low. Known problem with a known engineering solution (build, then self-validate).

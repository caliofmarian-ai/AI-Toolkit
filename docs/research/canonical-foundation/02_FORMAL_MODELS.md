# 02 — Formal Models

**Research Package:** Canonical Foundation Deep Research  
**Document:** 02  
**Status:** Complete  
**Date:** 2026-08-07  

---

## 1. Purpose

This document describes every formal model that the Canonical Foundation intended to implement:

- The Information Model
- The Semantic Model
- The Syntax Model
- The Mathematical Model
- The Validation Model
- The Compilation Model
- The Execution Model

For each model, this document records what was specified, what was left unspecified, and the engineering conclusions that follow.

---

## 2. The Information Model

### 2.1 Definition

The Information Model defines how engineering knowledge is organized as a structured information object — independently of syntax, programming language, or storage format.

### 2.2 CDM Information Model

**FACT:** CDM-000 defines the Information Model as follows:

> "Every Canonical Document represents a structured engineering information object. The Information Model defines how information is organized, identified, related and governed throughout its lifecycle."

**FACT:** CDM-000 defines the following canonical entities:

- **Document** — the primary information container
- **Metadata** — descriptive attributes governing identity, classification, and lifecycle
- **Identifier** — the globally unique identity of a document
- **Namespace** — the organizational scope containing identifiers
- **Version** — the declared revision state of a document
- **Author** — the ownership attribution
- **Status** — the lifecycle state (Draft, Normative, Deprecated, Archived)
- **Relationship** — a formal directed edge between documents
- **Dependency** — a relationship expressing that one document requires another
- **Lifecycle** — the sequence of states through which a document transitions

**ENGINEERING CONCLUSION:** The CDM information model is a complete, relational information model for engineering documents. It is equivalent in conceptual sophistication to an entity-relationship data model for a database schema. Documents are not files — they are information objects with identity, attributes, relationships, and lifecycle.

### 2.3 CSL Information Model

**FACT:** CSL v1 Volume I defines information as organized into five engineering layers:

- Layer 1: Human Vision (Purpose, Mission, Values, Constraints)
- Layer 2: Canonical Knowledge (Requirements, Policies, Rules, Concepts, Decisions)
- Layer 3: Universal Engineering Model (Semantic Entities, Relationships, Constraints)
- Layer 4: Engineering Artifacts (Documentation, Architecture, Code, Tests)
- Layer 5: Execution Environment (Runtime, Platform, Infrastructure)

**ENGINEERING CONCLUSION:** The CSL information model is a layer model in which information flows downward: human intent is the source, execution is the output. Each layer is a transformation of the layer above it. This is a pipeline architecture for information.

### 2.4 Incomplete Information Model Areas

**FACT:** CDM-011 (Document Graph) is a placeholder. CDM-013 (Document Index) is a placeholder. CDM-014 (Document Namespace) is a placeholder.

**ENGINEERING CONCLUSION:** The information model as defined in CDM-000 is architecturally complete at the conceptual level but lacks three child specifications that would formalize: how documents are organized into traversable graphs, how documents are indexed for retrieval, and how namespaces are structured and scoped.

---

## 3. The Semantic Model

### 3.1 Definition

The Semantic Model defines the meaning of canonical knowledge — what an engineering statement represents independently of how it is written.

### 3.2 CSL Semantic Model

**FACT:** CSL v1 Volume III (Semantic Model, 602 lines) defines:

> "While the Language Specification defines how knowledge is written, the Semantic Model defines what that knowledge represents. Every conforming implementation shall construct the same semantic representation from equivalent Canonical Knowledge."

**FACT:** Volume III establishes:

- **Semantic Objects** — everything in the semantic model is a Semantic Object with: Identity, Type, Meaning, Properties, Relationships, Constraints, Lifecycle, Provenance
- **Semantic Categories** — Knowledge, Entity, Relationship, Constraint, Policy, Rule, Artifact, Action
- **Semantic Equivalence** — multiple syntactic representations may describe identical semantics; equivalent semantics shall produce equivalent Universal Engineering Models
- **Type System** — a hierarchy of semantic types governing what kinds of objects can exist and what relationships are valid between them
- **Semantic Validation** — rules that determine whether a semantic representation is internally consistent

**ENGINEERING CONCLUSION:** The CSL semantic model is a formal object model — closer to a type-theoretic foundation than to informal documentation semantics. It is designed for machine interpretation: two different textual representations of the same concept must yield the same semantic object. This is the property that makes CSL "machine-readable" in a meaningful engineering sense.

### 3.3 Semantic Independence

**FACT:** Volume III states: "The Semantic Model is independent of: syntax, compiler implementation, programming language, repository structure, Artificial Intelligence provider, deployment platform."

**ENGINEERING CONCLUSION:** Semantic independence is the cornerstone of the CSL design. The semantic model is intended to be the stable layer — it does not change when the syntax changes, when the compiler is reimplemented, or when the AI provider changes. This stability allows the Universal Engineering Model to be a long-lived artifact even as its surrounding infrastructure evolves.

### 3.4 Shared Ontology — State of Implementation

**FACT:** `standards/csl/shared/ontology/` contains 21 files, all with exactly zero bytes. This includes: ARTIFACT_MODEL.md, CAPABILITY_MODEL.md, DECISION_MODEL.md, DEPENDENCY_MODEL.md, ENGINE_MODEL.md, ENTITY_MODEL.md, EVENT_MODEL.md, GOAL_MODEL.md, GOVERNANCE_MODEL.md, KNOWLEDGE_MODEL.md, LIFECYCLE_MODEL.md, MATURITY_MODEL.md, ONTOLOGY.md, POLICY_MODEL.md, RELATIONSHIP_MODEL.md, REPOSITORY_MODEL.md, RULE_MODEL.md, SECURITY_MODEL.md, TRACEABILITY_MODEL.md, TYPE_SYSTEM.md.

**FACT:** `standards/csl/shared/metamodel/` contains 8 files, all with exactly zero bytes. This includes: META_CONSTRAINT.md, META_ENTITY.md, META_NAMESPACE.md, META_POLICY.md, META_RELATIONSHIP.md, META_RULE.md, META_TYPE.md, METAMODEL.md.

**ENGINEERING CONCLUSION:** The shared ontology and metamodel — which would be the machine-readable formalization of the semantic model — are entirely empty. The semantic model as described in Volume III exists as text specification. Its machine-readable instantiation was never authored. This is a major gap.

---

## 4. The Syntax Model

### 4.1 Definition

The Syntax Model defines the textual representation of canonical knowledge — how semantic objects are written as tokens, statements, and documents.

### 4.2 CSL v1 Syntax Model

**FACT:** CSL v1 Volume II (Language Specification, 724 lines) defines:

- **Document Structure** — how a CSL document is organized at the top level
- **Language Constructs** — the set of expressions available in CSL
- **Keywords** — reserved words with predefined engineering meaning
- **Blocks** — delimited regions containing related knowledge
- **Identifiers** — naming rules for engineering objects
- **Attributes** — key-value properties attached to objects
- **Relationships** — syntactic declarations of dependencies and associations
- **References** — cross-document identifier citations
- **Data Types** — String, Integer, Decimal, Boolean, Date, Timestamp, Duration, Enumeration, Null
- **Comments** — non-semantic annotations
- **Extensions** — mechanism for adding domain-specific constructs
- **Conformance** — levels of compliance with the language specification

**FACT:** CSL v1 Volume IV (Grammar, 744 lines) defines the formal grammar in four layers:

```
Lexical Grammar (tokens)
↓
Syntactic Grammar (structure)
↓
Structural Grammar (composition rules)
↓
Semantic Validation (meaning constraints)
```

**ENGINEERING CONCLUSION:** The CSL v1 syntax model is complete. It defines a text-based specification language with a four-layer grammar that progresses from tokens through structure to semantics. The grammar is explicitly designed to be deterministic and human-readable.

### 4.3 CSL v1 Grammar Architecture

**FACT:** Volume IV defines the following grammatical units in order of composition:

1. **Tokens** — Identifier, Keyword, Literal, Number, String, Boolean, Reference, Operator, Delimiter, Comment, Whitespace
2. **Identifiers** — unique names for engineering objects, case-sensitive, whitespace-prohibited
3. **Statements** — complete grammatical declarations containing attributes, relationships, nested statements, references, metadata
4. **Blocks** — delimited groups of statements with a common scope
5. **Documents** — top-level containers with a document header, namespace declaration, and body

**ENGINEERING CONCLUSION:** The grammar follows a compositional hierarchy: tokens compose into statements, statements compose into blocks, blocks compose into documents. This is a well-understood grammar architecture used in programming language design.

### 4.4 CSL v2 Syntax Model — State

**FACT:** CSL-002 (Grammar) is empty. CSL-001 (Engineering Alphabet) is empty. CSL-013 (Lexer Specification) is empty. CSL-014 (AST Specification) is empty.

**ENGINEERING CONCLUSION:** The v2 syntax model does not exist. The v1 syntax model serves as the available reference. The v2 specification names suggest an expanded grammar with: an explicit engineering alphabet (CSL-001), a formal grammar (CSL-002), a lexer specification (CSL-013), and an explicit AST specification (CSL-014). None of these have been authored.

---

## 5. The Mathematical Model

### 5.1 Intended Mathematical Foundation

**FACT:** CSL v1 Volume III (Semantic Model) defines semantic objects with the properties: Identity, Type, Meaning, Properties, Relationships, Constraints, Lifecycle, Provenance.

**FACT:** CSL v1 Volume VI (Universal Engineering Model) defines the Universal Engineering Model as a semantic graph — entities connected by typed, directed relationships.

**ENGINEERING CONCLUSION:** The intended mathematical model of CSL is a **typed directed graph** over a **constrained type system**. Formally:

- A CSL knowledge base is a graph G = (V, E, T) where:
  - V is a set of semantic objects (vertices)
  - E is a set of typed, directed relationships (edges)
  - T is a type system defining valid vertex types and valid edge types for each vertex type pair
- A compilation is a transformation function f: G → A where A is an artifact set
- A validation is a predicate P: G → {valid, invalid, error} under a constraint set C

**ENGINEERING HYPOTHESIS:** The formal mathematical model was never written explicitly as a mathematical formalization. It is implied by the semantic model specification but was never expressed as a mathematical structure (e.g., category theory, type theory, graph theory). The absence of a formal mathematical model is an architectural gap — it means that two implementations of the CSL compiler could be semantically inequivalent without a formal proof of equivalence being possible.

### 5.2 The Universal Engineering Model as Mathematical Object

**FACT:** CSL v1 Volume VI (Universal Engineering Model, 591 lines) defines the UEM as the intermediate representation between canonical knowledge and engineering artifacts.

**ENGINEERING CONCLUSION:** The UEM is the mathematical object that CSL compilation produces. It is a normalized, typed, directed knowledge graph that is independent of the source CSL syntax. Artifact generation is a projection from the UEM onto a target artifact type. This is structurally analogous to an intermediate representation (IR) in a traditional compiler — the UEM is CSL's IR.

---

## 6. The Validation Model

### 6.1 Intended Validation Architecture

**FACT:** CDM-008 (Validation Model) is a 21-line placeholder.

**FACT:** CSL v1 Volume IV defines "Semantic Validation" as the fourth layer of the grammar.

**FACT:** CSS-004 (Specification Checklist) provides a validator-ready checklist for canonical specification compliance.

**FACT:** `docs/audits/canonical-system/11_FUTURE_VALIDATOR_REQUIREMENTS.md` specifies three validators: V-01 (CSS Document Validator), V-02 (CDM Header Validator), V-03 (CSL Syntax Validator).

**ENGINEERING CONCLUSION:** The intended validation model has three levels:

| Level | Scope | Specification Ready? | Tooling Exists? |
|---|---|---|---|
| CSS Compliance | Document authoring rules | Yes (CSS-003, CSS-004) | No |
| CDM Header | Document identity and metadata | Yes (CDM-001, CDM-002 + JSON schemas) | No |
| CSL Grammar | CSL expression validity | Partial (v1 grammar only) | No (parser is prototype) |

**ENGINEERING CONCLUSION:** The validation model is architecturally designed and the first two levels are specification-ready. No validator implementation exists. The third level (CSL grammar validation) requires CSL-002 before a v2 validator can be built.

### 6.2 Validation Levels

**ENGINEERING CONCLUSION:** The complete validation model as intended would have five levels:

1. **Syntactic Validation** — is the CSL text grammatically well-formed?
2. **Structural Validation** — does the document satisfy mandatory structural requirements (sections, headers)?
3. **Semantic Validation** — are semantic objects type-correct and constraint-satisfying?
4. **Reference Validation** — do all cross-document references resolve?
5. **Consistency Validation** — is the canonical knowledge graph internally consistent?

Levels 1-2 are partially specified. Levels 3-5 are undocumented.

---

## 7. The Compilation Model

### 7.1 CSL Compilation Pipeline

**FACT:** CSL v1 Volume V (Compiler Specification, 617 lines) defines the following compilation pipeline:

```
Knowledge Acquisition
↓
Lexical Analysis
↓
Parsing
↓
Abstract Syntax Tree Construction
↓
Semantic Analysis
↓
Universal Engineering Model Construction
↓
Validation
↓
Optimization
↓
Artifact Generation
↓
Verification
```

**ENGINEERING CONCLUSION:** The compilation model is a classic compiler pipeline. It is architecturally sound and follows established compiler theory. The pipeline produces the Universal Engineering Model as its primary intermediate product, then generates artifacts from that product.

### 7.2 Compilation Outputs

**FACT:** Volume V defines the following artifact categories that the compiler can generate:

- Documentation artifacts
- Architecture artifacts
- Source code structure artifacts
- Test artifacts
- Deployment artifacts
- AI prompt artifacts

**ENGINEERING CONCLUSION:** The compilation model is not a traditional code compiler — it generates a diverse set of artifacts from a single knowledge source. This is a code generation / knowledge projection system, not a traditional language compiler.

### 7.3 Incremental Compilation

**FACT:** Volume V states: "Support incremental compilation."

**ENGINEERING CONCLUSION:** Incremental compilation was a declared requirement. This means the compiler was intended to track what knowledge had changed and regenerate only the affected artifacts, rather than recompiling the entire knowledge base on every change. This requirement has significant implementation complexity.

### 7.4 Compilation State

**FACT:** A Python parser exists in `lib/python/canonical_parser/`. It has not been validated end-to-end.

**ENGINEERING CONCLUSION:** The compilation model is fully specified in v1 but only partially implemented. The existing parser implements the first stages (lexical analysis and parsing) but does not implement semantic analysis, UEM construction, or artifact generation.

---

## 8. The Execution Model

### 8.1 CSL v2 Execution Intent

**FACT:** CSL-026 (Execution Model Specification) was scaffolded in v2 but is empty.

**FACT:** CSL-008 (Runtime Specification) was scaffolded in v2 but is empty.

**ENGINEERING CONCLUSION:** An execution model was planned for CSL v2 but never specified. CSL v1 has no execution model — v1 is a specification language, not an executable language.

**ENGINEERING HYPOTHESIS:** The v2 execution model would define how CSL specifications with executable semantics (such as Rules and Policies) are evaluated at runtime. This extends CSL from a static specification language to one that can express executable governance logic — e.g., "this rule SHALL be enforced at deployment time."

### 8.2 CDM Executable Documents

**FACT:** CDM-009 (Executable Document Model) is a 21-line placeholder.

**ENGINEERING HYPOTHESIS:** The "executable document" concept is the point where CSL's specification-language capabilities meet runtime execution. An executable document is a canonical specification that can be both authored as knowledge and evaluated as executable logic. This bridges the specification layer and the execution layer — a significant architectural capability that was designed but never specified.

### 8.3 Current Execution Model Status

**ENGINEERING CONCLUSION:** No execution model exists in the repository. The execution model is the most forward-looking and least developed component of the Canonical Foundation. It was planned, scaffolded, and not written.

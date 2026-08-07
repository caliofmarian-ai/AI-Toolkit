# 04 — Canonical Knowledge Position

Version: 1.1.0-draft

Status: Draft — Pending Human Review and Approval

Classification: Canonical Research Document

Package: docs/research/governance-reconciliation/

---

## 1. Purpose

This document determines where Canonical Knowledge belongs in the governance
architecture, whether it has an authoritative definition, and how it evolves.

---

## 2. Does Canonical Knowledge Have an Authoritative Definition?

**Verified Fact:** The `knowledge/README.md` defines the location and format of
Canonical Knowledge:
> "This directory stores project-specific Canonical Knowledge.
> Contents shall include: Capabilities, Requirements, Engineering decisions,
> Domain knowledge, Knowledge packages.
> Contents shall be in CSL format.
> Contents shall never include generated artifacts.
> Contents shall be the authoritative source for engineering knowledge."

*Source: `knowledge/README.md`*

**Verified Fact:** The `standards/csl/shared/knowledge/` directory contains 13
Canonical Knowledge definition files including:
- KNOWLEDGE_GRAPH.md
- CANONICAL_ENTITIES.md
- CANONICAL_RELATIONSHIPS.md
- CANONICAL_DECISIONS.md
- CANONICAL_TRACEABILITY.md
- CANONICAL_REASONING.md
- CANONICAL_CONSTRAINTS.md
- CANONICAL_CAPABILITIES.md
- CANONICAL_POLICIES.md
- CANONICAL_EVENTS.md
- CANONICAL_ATTRIBUTES.md
- CANONICAL_DEPENDENCIES.md
- CANONICAL_QUERIES.md

**Verified Fact:** The `standards/csl/versions/v1/03_SEMANTIC_MODEL.md` and
`standards/csl/versions/v1/01_FOUNDATIONS.md` reference Canonical Knowledge as part
of the CSL semantic model (filenames confirm this; full content not reproduced here).

**Architectural Conclusion:** Canonical Knowledge has two defining document sets:

1. `knowledge/README.md` — defines the repository location and storage rules for
   project-specific canonical knowledge.

2. `standards/csl/shared/knowledge/` — defines the structural types and schemas
   of canonical knowledge elements within the CSL standard.

These two locations are **complementary, not redundant**:
— `standards/csl/shared/knowledge/` defines the *types* of knowledge (what Canonical
   Knowledge can contain).
— `knowledge/` is the *store* of actual project knowledge in those types.

---

## 3. Where Does Canonical Knowledge Belong?

**Architectural Conclusion:** Based on repository evidence, Canonical Knowledge
belongs at two levels:

### Level 1: Standards Level (Type Definitions)
Location: `standards/csl/shared/knowledge/`
Governed by: CSL standard
Defines: What kinds of knowledge exist (entities, relationships, decisions, etc.)
Status: Populated (13 definition files exist)

### Level 2: Project Level (Knowledge Store)
Location: `knowledge/`
Governed by: CSL format, knowledge/README.md
Stores: Actual project engineering knowledge
Status: Minimal (only README.md exists in knowledge/)

**Engineering Inference:** The knowledge store at `knowledge/` is essentially empty
beyond its README. The knowledge type definitions at `standards/csl/shared/knowledge/`
exist but have not yet been used to populate the knowledge store.

---

## 4. Relationship to Governance

**Repository Evidence** from `governance/PROJECT_CONSTITUTION.md`, Article XIII:
> "Knowledge is a strategic asset.
> Engineering knowledge shall remain independent from individual implementations,
> contributors or technologies."

**Repository Evidence** from `governance/PROJECT_PHILOSOPHY.md`:
> "Knowledge precedes architecture.
> Architecture precedes implementation.
> Implementation precedes execution.
> Execution produces evidence.
> Evidence improves knowledge.
> Engineering is therefore a continuous knowledge cycle rather than a linear
> software process."

**Governance Conclusion:** Governance places Canonical Knowledge at the apex
of the engineering cycle. Knowledge is not a product of governance; it is the
foundation that governance protects and the evidence that governance evolves through.

---

## 5. How Does Canonical Knowledge Evolve?

**Repository Evidence** from `governance/STANDARDIZATION_PROCESS.md`:
The standardization lifecycle applies to canonical standards. Canonical Knowledge
stored in CSL format would follow the CSL governance lifecycle.

**Repository Evidence** from `knowledge/README.md`:
> "See: standards/csl/rfc/RFC-0009-CANONICAL-PROJECT-STRUCTURE.md"

**Verified Fact:** The reference to RFC-0009 indicates that the knowledge structure
is governed by an RFC within the CSL standard.

**Governance Conclusion:** Canonical Knowledge evolves through:
1. New knowledge proposals following the governance Decision Process
2. CSL-format authoring following CSL structural rules
3. Validation through the Validator engine
4. Compilation through the Compiler engine
5. Promotion through the governance lifecycle (Draft → Review → Approved → etc.)

Human authority is required for promotion beyond Draft state. This is implied by
the governance model's approval requirements but not explicitly stated for knowledge
artifacts specifically.

---

## 6. Relationship to Governance Documents

**Governance Conclusion:** Governance documents (in `governance/`) are themselves
canonical knowledge, but of a specific type: governance knowledge.

They are not stored in `knowledge/` (which stores project engineering knowledge) but
in `governance/` (which stores governance specification knowledge).

The two stores are:
- `governance/` — governance specifications (normative)
- `knowledge/` — project engineering knowledge (CSL-formatted)

Both are canonical, but they serve different purposes and are governed by
different authorities:
- `governance/` is governed by the PROJECT_CONSTITUTION and governance workflow
- `knowledge/` is governed by CSL and the Knowledge Engine

---

## 7. Knowledge Engine Position

**Engineering Inference:** The Knowledge Engine (referenced in architecture documents
and specifications) is responsible for:
- reading the `knowledge/` directory
- interpreting CSL-formatted knowledge
- making knowledge available to other engines (Compiler, Validator, Runtime)

The Knowledge Engine is an implementation artifact. It depends on:
- CSL standard (format)
- knowledge/ directory (content)
- governance decisions about what knowledge is canonical

**Verified Fact:** The `architecture/requirements/backlog/AR-0003_CANONICAL_KNOWLEDGE_GRAPH.md`
exists, confirming that Canonical Knowledge Graph is a recognized architecture
requirement. (Full content not reproduced here by filename evidence.)

---

## 8. Summary

| Question | Answer | Evidence Type |
|----------|--------|---------------|
| Does Canonical Knowledge have an authoritative definition? | Yes, in two locations | Verified Fact |
| Where does it belong? | knowledge/ (store) + standards/csl/shared/knowledge/ (types) | Verified Fact |
| Is the knowledge store populated? | Minimal (README only) | Verified Fact |
| How does it evolve? | Through CSL governance lifecycle + human approval | Governance Conclusion |
| Does governance protect it? | Yes, Constitution Article XIII | Verified Fact |
| Does the Knowledge Engine have a requirement? | Yes, AR-0003 | Verified Fact |

---

## 9. Canonical Engineering Cycle

### 9.1 Purpose of This Section

The governance package previously documented governance hierarchy, canonical knowledge
position, and governance lifecycle. It did not explicitly document the complete
engineering cycle through which human intent becomes running systems, and through
which observed reality feeds back into canonical knowledge.

This section derives and documents that cycle from repository evidence, identifying
which transitions are supported by repository fact and which remain Engineering Inference.

---

### 9.2 The Canonical Engineering Cycle

The following cycle is derived from repository evidence. Each step is annotated with
its evidence category.

```
Human Intent
     ↓
Canonical Knowledge
     ↓
Canonical Models
     ↓
Universal Engineering Model
     ↓
Generated Artifacts
     ↓
Executable Runtime
     ↓
Observed Reality
     ↓
Feedback
     ↓
Canonical Knowledge
```

---

### 9.3 Transition-by-Transition Evidence

#### Step 1 — Human Intent → Canonical Knowledge

**Engineering Inference:** No repository document uses the term "Human Intent" as a
named cycle stage. However, repository evidence consistently establishes that canonical
knowledge originates from human-originated decisions and requirements.

**Repository Evidence** from `governance/DECISION_PROCESS.md`:
> "Idea → AR → Initial Analysis → Architecture Audit → ADR → Impact Analysis →
> Approval → Roadmap Planning → Implementation → Validation → Audit → Release →
> Continuous Review"

**Repository Evidence** from `governance/ENGINEERING_PRINCIPLES.md`, Principle 1:
> "Every engineering activity begins with a canonical specification.
> Specifications define intent. Implementations realize intent."

**Repository Evidence** from `governance/PROJECT_PHILOSOPHY.md`:
> "Knowledge precedes architecture."

**Engineering Inference:** "Human Intent" refers to the engineering ideas, requirements
and decisions that originate in the governance process and are formalized as canonical
knowledge. The Idea stage of the Decision Process is the entry point for human intent
into the cycle.

---

#### Step 2 — Canonical Knowledge → Canonical Models

**Verified Fact:** `standards/csl/versions/v1/01_FOUNDATIONS.md` defines a layered
structure:
> Layer 1 (Canonical Knowledge): Rules, Concepts, Decisions
> Layer 2 (Canonical Models): formal model layer built from Layer 1

**Repository Evidence** from `governance/ARCHITECTURE_PRINCIPLES.md`, Principle 3:
> "Models define concepts. Standards define rules. Governance defines authority."

**Repository Evidence** from `governance/GOVERNANCE_MODEL.md` hierarchy:
> "Project Constitution → Governance Policies → Canonical Models → Canonical Standards
> → Reference Architecture → Reference Implementations → Operational Implementations"

**Architectural Conclusion:** Canonical Knowledge (Layer 1) is the input from which
Canonical Models (Layer 2) are derived. The CSL standard defines this layering
explicitly.

---

#### Step 3 — Canonical Models → Universal Engineering Model

**Verified Fact:** `standards/csl/versions/v1/01_FOUNDATIONS.md` defines Layer 3 as:
> "Universal Engineering Model: Semantic Entities, Semantic Relationships, Semantic
> Constraints, Dependency Graph"

**Verified Fact:** `standards/csl/versions/v1/03_SEMANTIC_MODEL.md` states:
> "The Semantic Model is the foundation of the Universal Engineering Model.
> Equivalent semantics shall produce equivalent Universal Engineering Models."

**Verified Fact:** `standards/csl/versions/v1/05_COMPILER_SPECIFICATION.md` states:
> "The Engineering Compiler transforms Canonical Knowledge into the Universal Engineering
> Model and subsequently into Engineering Artifacts."
> Compiler objective: "Construct the Universal Engineering Model."

**Architectural Conclusion:** The Universal Engineering Model is an explicitly defined
artifact in the CSL standard. It is produced from Canonical Models through the
Engineering Compiler. This transition is one of the most strongly evidenced steps
in the cycle.

---

#### Step 4 — Universal Engineering Model → Generated Artifacts

**Verified Fact:** `standards/csl/versions/v1/05_COMPILER_SPECIFICATION.md` states:
> "The Engineering Compiler transforms Canonical Knowledge into the Universal Engineering
> Model and subsequently into Engineering Artifacts."
> Compiler objective: "Generate Engineering Artifacts."

**Verified Fact:** `standards/csl/versions/v1/01_FOUNDATIONS.md` defines Layer 4 as:
> "Engineering Artifacts: Documentation, Architecture"

**Verified Fact:** `standards/csl/versions/v1/01_FOUNDATIONS.md` states:
> "Consistency shall always be restored by returning to Canonical Knowledge rather
> than editing generated artifacts independently."

**Architectural Conclusion:** Generated Artifacts are the output of the Engineering
Compiler acting on the Universal Engineering Model. This transition is explicitly
defined in the CSL Compiler Specification.

---

#### Step 5 — Generated Artifacts → Executable Runtime

**Repository Evidence** from `governance/ARCHITECTURE_PRINCIPLES.md`, Principle 3:
> "Engines implement capabilities. Runtime executes behavior."

**Repository Evidence** from `governance/ARCHITECTURE_PRINCIPLES.md`, Principle 18:
> "The ecosystem architecture is organized around:
> Governance, Canonical Models, Canonical Standards, Reference Architecture, Platforms,
> Engineering Engines, Runtime, Products"

**Repository Evidence** from `governance/GOVERNANCE_MODEL.md`:
> "Project Constitution → ... → Reference Implementations → Operational Implementations"

**Architectural Conclusion:** Generated Artifacts flow into the Runtime layer, where
they are executed. The architecture stack explicitly places Runtime as the layer that
executes the outputs of the engineering process. The exact mechanism by which generated
artifacts are deployed to Runtime is not defined in governance documents.

---

#### Step 6 — Executable Runtime → Observed Reality

**Repository Evidence** from `governance/PROJECT_PHILOSOPHY.md`:
> "Implementation precedes execution.
> Execution produces evidence."

**Repository Evidence** from `governance/PROJECT_IDENTITY.md`, Section 4 (Vision):
> "To make software engineering deterministic, auditable, reproducible and
> knowledge-driven by replacing informal documentation with executable canonical
> specifications."

**Engineering Inference:** "Observed Reality" is the evidence produced by execution.
The Philosophy explicitly names this as "evidence." The Identity document frames
this as the goal of the system: deterministic, auditable, reproducible outcomes.

---

#### Step 7 — Observed Reality → Feedback → Canonical Knowledge

**Repository Evidence** from `governance/PROJECT_PHILOSOPHY.md`:
> "Execution produces evidence.
> Evidence improves knowledge.
> Engineering is therefore a continuous knowledge cycle rather than a linear
> software process."

**Repository Evidence** from `governance/DECISION_PROCESS.md`:
> "Continuous Review" (final stage of the decision lifecycle)
> "implementation feedback" (listed as an input to continuous review)

**Repository Evidence** from `governance/ENGINEERING_PRINCIPLES.md`, Principle 8:
> "Engineering decisions shall be supported by evidence whenever possible."

**Repository Evidence** from `governance/PROJECT_CONSTITUTION.md`, Article XII:
> "Architectural decisions shall be documented.
> Engineering rationale shall be preserved.
> Historical decisions shall remain traceable."

**Verified Fact:** The `PROJECT_PHILOSOPHY.md` explicitly describes a continuous
knowledge cycle in which evidence from execution feeds back into canonical knowledge.
This is not an inference — the Philosophy defines this as the fundamental nature of
the engineering discipline.

**Governance Conclusion:** The feedback loop that returns Observed Reality to Canonical
Knowledge requires human authority. Constitution Article XVI requires governance process
for any evolution. Governance Conclusion: feedback cannot alter Canonical Knowledge
directly — it must pass through the human-governed decision process.

---

### 9.4 Cycle Support Summary

| Cycle Step | Supported by Repository Evidence? | Evidence Category |
|------------|----------------------------------|-------------------|
| Human Intent → Canonical Knowledge | Partial (governance process starts from human-originated ideas) | Engineering Inference |
| Canonical Knowledge → Canonical Models | Yes — CSL FOUNDATIONS layers, GOVERNANCE_MODEL hierarchy | Verified Fact |
| Canonical Models → Universal Engineering Model | Yes — CSL FOUNDATIONS Layer 3, CSL_SEMANTIC_MODEL, COMPILER_SPECIFICATION | Verified Fact |
| Universal Engineering Model → Generated Artifacts | Yes — COMPILER_SPECIFICATION explicitly | Verified Fact |
| Generated Artifacts → Executable Runtime | Yes — ARCHITECTURE_PRINCIPLES stack, GOVERNANCE_MODEL hierarchy | Architectural Conclusion |
| Executable Runtime → Observed Reality | Partial — PROJECT_PHILOSOPHY "Execution produces evidence" | Engineering Inference |
| Observed Reality → Feedback → Canonical Knowledge | Yes — PROJECT_PHILOSOPHY knowledge cycle statement | Verified Fact |

**Governance Conclusion:** The complete Canonical Engineering Cycle is substantially
supported by repository evidence. The core loop (Canonical Knowledge → UEM → Artifacts
→ Runtime → Evidence → Knowledge) is the most strongly evidenced. The "Human Intent"
entry point is an Engineering Inference. The feedback loop's requirement for human
governance authority before re-entering Canonical Knowledge is a Governance Conclusion
derived from Constitution Article VII and Article XVI.

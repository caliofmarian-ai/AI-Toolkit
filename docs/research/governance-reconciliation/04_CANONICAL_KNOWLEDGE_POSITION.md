# 04 — Canonical Knowledge Position

Version: 1.0.0-draft

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

**Architectural Conclusion:** Governance places Canonical Knowledge at the apex
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

**Architectural Conclusion:** Canonical Knowledge evolves through:
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

**Architectural Conclusion:** Governance documents (in `governance/`) are themselves
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
| How does it evolve? | Through CSL governance lifecycle + human approval | Architectural Conclusion |
| Does governance protect it? | Yes, Constitution Article XIII | Verified Fact |
| Does the Knowledge Engine have a requirement? | Yes, AR-0003 | Verified Fact |

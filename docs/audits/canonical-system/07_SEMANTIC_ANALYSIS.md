# 07 — Semantic Analysis

**Audit:** Canonical System Forensic Audit  
**Date:** 2026-08-07  
**Classification:** Engineering Artifact  
**Status:** Final  

---

## 1. Purpose

This document analyzes the semantic model of the Canonical System and identifies semantic inconsistencies across components.

---

## 2. CSL v1 Semantic Model

### 2.1 Overview

**FACT:** `standards/csl/versions/v1/03_SEMANTIC_MODEL.md` is 602 lines and defines the type system and semantic validation layer of CSL v1.

### 2.2 Core Semantic Concepts

**FACT:** The v1 Semantic Model defines:
- Engineering types (entity, attribute, relationship, constraint, event, policy)
- Type hierarchy
- Type compatibility rules
- Constraint semantics
- Relationship semantics
- Reference resolution rules
- Scope rules

**Engineering Conclusion:** The v1 semantic model is complete at the specification level. It provides a formal type system that a compiler can implement.

### 2.3 Universal Engineering Model

**FACT:** `standards/csl/versions/v1/06_UNIVERSAL_ENGINEERING_MODEL.md` (591 lines) defines the output semantic model — the normalized representation of canonical knowledge after compilation.

**Engineering Conclusion:** The UEM separates compilation output from source language, enabling language evolution without invalidating compiled knowledge artifacts.

---

## 3. CSL Shared Ontology

### 3.1 Overview

**FACT:** `standards/csl/shared/ontology/` contains 18 model documents.

**FACT:** These include:
- `ONTOLOGY.md` — top-level ontology definition
- `ENTITY_MODEL.md` — entity semantics
- `RELATIONSHIP_MODEL.md` — relationship semantics
- `TYPE_SYSTEM.md` — type hierarchy
- `KNOWLEDGE_MODEL.md` — knowledge representation
- `POLICY_MODEL.md` — policy semantics
- `GOVERNANCE_MODEL.md` — governance semantics
- `SECURITY_MODEL.md` — security semantics
- `LIFECYCLE_MODEL.md` — lifecycle semantics
- `MATURITY_MODEL.md` — maturity semantics
- `DEPENDENCY_MODEL.md` — dependency semantics
- `TRACEABILITY_MODEL.md` — traceability semantics

**Engineering Conclusion:** The shared ontology provides a rich semantic foundation that both v1 and v2 can reference. This is the most semantically sophisticated part of the Canonical System.

### 3.2 Shared Knowledge Domain

**FACT:** `standards/csl/shared/knowledge/` contains 13 knowledge domain documents including CANONICAL_ENTITIES, CANONICAL_ATTRIBUTES, CANONICAL_RELATIONSHIPS, CANONICAL_CONSTRAINTS, CANONICAL_EVENTS, CANONICAL_POLICIES, CANONICAL_DECISIONS, CANONICAL_REASONING, CANONICAL_TRACEABILITY, and KNOWLEDGE_GRAPH.

**Engineering Conclusion:** These documents define the semantic vocabulary of canonical engineering — the terms, concepts, and constructs that CSL expresses.

---

## 4. Semantic Inconsistencies

### 4.1 Semantic Inconsistency SI-001: Version Gap

**FACT:** CSL v1 defines its own semantic model in Volume III.

**FACT:** CSL v2 has an empty Semantic Type System (CSL-003).

**FACT:** The shared ontology exists independently of either version.

**Engineering Conclusion:** It is unclear whether CSL v2 was intended to inherit, extend, or replace the v1 semantic model. The relationship between v1 semantics, shared ontology, and v2 semantic type system is architecturally undefined.

**[ADDITIONAL OBSERVATION]:** The presence of the shared ontology in `standards/csl/shared/` suggests the intent was for both v1 and v2 to reference a common semantic foundation. The v2 CSL-003 would then define how v2 syntax maps onto that foundation.

### 4.2 Semantic Inconsistency SI-002: Natural Language vs. Machine-Readable Semantics

**FACT:** The CANON specification series (CANON-001 through CANON-080+) are written in natural language Markdown.

**FACT:** CSL was designed to make canonical knowledge machine-readable.

**Engineering Conclusion:** There is a fundamental semantic inconsistency between the platform's knowledge surface (CANON series in Markdown) and the canonical language designed to express it (CSL). The knowledge exists but is not in the language designed to hold it.

### 4.3 Semantic Inconsistency SI-003: Metamodel vs. Type System

**FACT:** `standards/csl/shared/metamodel/` defines a metamodel with META_ENTITY, META_TYPE, META_RELATIONSHIP, META_CONSTRAINT, META_POLICY, META_RULE, META_NAMESPACE.

**FACT:** `standards/csl/versions/v1/03_SEMANTIC_MODEL.md` defines a type system.

**Engineering Conclusion:** The relationship between the shared metamodel and the v1 semantic model is not explicitly documented. They appear to cover overlapping conceptual territory from different angles (metamodel = structural schema, type system = value semantics).

### 4.4 Semantic Inconsistency SI-004: CDM vs. CSL Document Model

**FACT:** CDM-000 defines a document object model with identity, metadata, lifecycle, and relationships.

**FACT:** CSL v1 Volume II (Language) also defines document structure (sections, blocks, attributes).

**Engineering Conclusion:** There is an overlap between CDM's document object model and CSL's document structure definition. The boundary between "CDM governs the document container" and "CSL governs the knowledge within it" is conceptually defined but not precisely delineated.

---

## 5. Semantic Strengths

### 5.1 Coherent Philosophy

**Engineering Conclusion:** The core semantic philosophy of the Canonical System — maintain knowledge exactly once, derive everything else — is coherent, well-motivated, and consistently expressed across CSL v1 Foundations, CSS-000, and CDM-000.

### 5.2 Rich Ontology

**Engineering Conclusion:** The shared ontology and knowledge domains represent significant conceptual work. If completed and properly wired to v2, they would constitute a sophisticated semantic foundation for machine-readable engineering knowledge.

---

## 6. Semantic Assessment Summary

| Dimension | Status |
|---|---|
| v1 semantic model | Complete |
| Universal Engineering Model | Complete (v1) |
| Shared ontology | Substantive (18 documents) |
| Shared metamodel | Substantive (8 documents) |
| v2 semantic type system | Empty |
| Machine-readable canonical knowledge | Effectively zero (CANON in Markdown) |
| Semantic consistency | Partial — version gap and boundary ambiguity |

**Overall Semantic Maturity: Philosophically Coherent, Technically Incomplete**

# 06 — Grammar Analysis

**Audit:** Canonical System Forensic Audit  
**Date:** 2026-08-07  
**Classification:** Engineering Artifact  
**Status:** Final  

---

## 1. Purpose

This document analyzes the grammar specifications of CSL v1 and the grammar gap in CSL v2.

---

## 2. CSL v1 Grammar

### 2.1 Overview

**FACT:** `standards/csl/versions/v1/04_GRAMMAR.md` is 744 lines and marked `Status: Normative`.

### 2.2 Grammar Architecture

**FACT:** The v1 grammar defines a layered architecture:

```
Lexical Grammar
    │  Character set, tokens, literals, identifiers, comments
    ▼
Syntactic Grammar
    │  Block structure, document structure, declarations
    ▼
Structural Grammar
    │  Sections, attributes, relationships, references
    ▼
Semantic Validation
    │  Type checking, constraint validation, reference resolution
    ▼
Universal Engineering Model
    Output: structured engineering knowledge graph
```

### 2.3 Grammar Objectives

**FACT:** The v1 grammar specifies the following objectives:
- Deterministic
- Human Readable
- Machine Readable
- Predictable
- Consistent
- Extensible
- Versioned

**Engineering Conclusion:** The v1 grammar was designed from first principles to be both human-readable and machine-parseable. This dual requirement influenced the grammar's structure: it uses an indentation-based, keyword-driven syntax rather than a symbol-heavy notation.

### 2.4 Grammar Completeness

**Engineering Conclusion:** The v1 grammar specification covers the structural requirements for a working parser. However, based on the audit of the parser implementation, no conformance tests validate the parser against this grammar.

**Engineering Conclusion:** The v1 grammar does not define a formal notation (BNF, EBNF, PEG). It defines grammar rules in natural language. This makes it well-readable but less directly usable as a parser generator input.

---

## 3. CSL v2 Grammar Gap

### 3.1 Current State

**FACT:** `standards/csl/versions/v2/CSL-002_GRAMMAR.md` contains zero bytes.

**FACT:** CSL v2 was planned to add capabilities not present in v1: binary format, package system, module system, query language, extension framework, execution model.

**Engineering Conclusion:** Without a v2 grammar, none of the v2 capabilities can be formally defined in a parseable way. This is the single most critical missing piece of the entire Canonical System.

### 3.2 Grammar Evolution Requirements

Based on analysis of the v2 file set and the capabilities declared in v2 identifiers, the v2 grammar must extend v1 to cover:

| New Capability | Grammar Changes Required |
|---|---|
| Object model (CSL-004) | Object declaration syntax |
| Relationship model (CSL-005) | Relationship declaration syntax |
| Knowledge representation (CSL-006) | Knowledge block syntax |
| Reasoning model (CSL-007) | Inference rule syntax |
| Module system (CSL-016) | Import/export syntax |
| Package format (CSL-015) | Package declaration syntax |
| Query language (CSL-025) | Query expression syntax |
| Extension framework (CSL-018) | Extension declaration syntax |

**Engineering Conclusion:** The v2 grammar is not a minor extension of v1. It represents a significant language evolution requiring substantial new grammar work.

---

## 4. Grammar and Parser Relationship

### 4.1 Current Parser

**FACT:** A Python parser exists in `lib/python/canonical_parser/`.

**FACT:** The parser imports successfully but has no end-to-end test.

**Engineering Hypothesis:** The Python parser was likely implemented against the v1 grammar or an informal grammar derived from observing existing CSL document structure. Without a v2 grammar, the parser cannot be evolved to support v2 features.

### 4.2 Required Validation

**Engineering Conclusion:** Before any parser work can be accepted as production-ready, a conformance test suite must be written. CSL-020 (Conformance Test Suite Specification) is one of the 47 empty v2 files — it would need to be authored as part of completing v2.

---

## 5. Grammar Inconsistencies Found

### 5.1 Grammar Format Inconsistency

**FACT:** CSL v1 Grammar uses natural language rules rather than a formal grammar notation.

**FACT:** CSL v2 Lexer Specification (CSL-013) and Parser Specification (CSL-012) filenames suggest formal lexer/parser specifications were intended.

**Engineering Conclusion:** There is an architectural inconsistency between the v1 approach (natural language grammar) and the v2 intent (formal lexer + parser + AST split). The v2 architecture is more rigorous but requires significantly more specification work.

### 5.2 Grammar Coverage Inconsistency

**FACT:** CSL v1 Grammar covers lexical, syntactic, structural, and semantic layers in one document.

**FACT:** CSL v2 separates these into: CSL-002 (Grammar), CSL-013 (Lexer), CSL-012 (Parser), CSL-014 (AST), CSL-003 (Semantic Type System).

**Engineering Conclusion:** The v2 separation is architecturally superior but means the grammar work is spread across five separate documents all of which are currently empty.

---

## 6. Grammar Assessment Summary

| Dimension | v1 | v2 |
|---|---|---|
| Grammar document | Complete, normative | Empty |
| Grammar format | Natural language rules | Intended: formal notation |
| Lexer specification | Embedded in grammar | Empty (CSL-013) |
| Parser specification | Embedded in compiler spec | Empty (CSL-012) |
| AST specification | Not separately defined | Empty (CSL-014) |
| Semantic type system | Defined in Volume III | Empty (CSL-003) |
| Conformance tests | Not implemented | Not started |

**Overall Grammar Maturity: Adequate for v1 prototype, blocking for v2 development**

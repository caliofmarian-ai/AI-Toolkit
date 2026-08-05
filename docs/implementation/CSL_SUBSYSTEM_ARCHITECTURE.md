# CSL Subsystem Architecture

Version: 1.0.0

Status: Canonical

Classification: Reference Implementation Architecture

CORE: CORE-023-001

---

# 1. Purpose

This document defines the authoritative subsystem architecture for the AI-Toolkit Reference Implementation of the Canonical Specification Language.

Every conforming module shall be implemented within the boundaries defined here.

This document is normative for all Phase 1 and subsequent implementation work.

---

# 2. Architecture Principle

The AI-Toolkit Reference Implementation follows the canonical layering defined by the CSL Standard:

```
Canonical Repository
        ↓
  Source Loader
        ↓
   CSL Lexer
        ↓
   CSL Parser
        ↓
Abstract Syntax Tree
        ↓
 Semantic Analyzer
        ↓
Universal Engineering Model
        ↓
  Validation Engine
        ↓
Engineering Compiler
        ↓
Artifact Generator Framework
        ↓
Safety & Governance Kernel
        ↓
 Runtime Integrations
```

No stage shall be bypassed.

No artifact shall be produced before validation.

No action shall execute without governance authorization.

---

# 3. Subsystem Map

## 3.1 Source Loader

Path: `lib/python/canonical_repository`

Responsibility: Load and enumerate Canonical Knowledge sources from the repository.

CSL Reference: Volume V Chapter 4 (Knowledge Acquisition)

Inputs: Repository path, document patterns

Outputs: Source file references

---

## 3.2 CSL Lexer

Path: `lib/python/canonical_parser` (module: `lexer`)

Responsibility: Transform source text into a deterministic token stream.

CSL Reference: Volume IV Chapters 4–5 (Tokens, Keywords)

Inputs: Source text

Outputs: Token stream, lexical diagnostics

---

## 3.3 CSL Parser

Path: `lib/python/canonical_parser` (module: `parser`)

Responsibility: Transform token stream into an Abstract Syntax Tree conforming to CSL grammar.

CSL Reference: Volume IV Chapters 6–17 (Grammar)

Inputs: Token stream

Outputs: Abstract Syntax Tree, parse diagnostics

---

## 3.4 Abstract Syntax Tree

Path: `lib/python/canonical_parser` (module: `ast_nodes`)

Responsibility: Represent syntactic structure of a CSL document as typed, traversable nodes.

CSL Reference: Volume V Chapter 7 (Abstract Syntax Tree Construction)

Properties:
- Immutable node types
- Source location tracking
- Typed children

---

## 3.5 Semantic Analyzer

Path: `lib/python/canonical_parser` (module: `semantic_analyzer`)

Responsibility: Assign engineering meaning to AST nodes. Validate semantic rules. Produce semantic diagnostics.

CSL Reference: Volume III (Semantic Model), Volume V Chapter 8 (Semantic Analysis)

Inputs: Abstract Syntax Tree

Outputs: Semantic annotations, semantic diagnostics

---

## 3.6 Universal Engineering Model

Path: `lib/python/canonical_entities` (module: `uem`)

Responsibility: Represent the technology-independent semantic model constructed from Canonical Knowledge.

CSL Reference: Volume VI (Universal Engineering Model)

Inputs: Semantic analyzer output

Outputs: UEM graph of Engineering Objects and Relationships

---

## 3.7 Validation Engine

Path: `lib/python/validation_engine`

Responsibility: Execute normative CSL validation across all mandated categories.

CSL Reference: Volume II Chapter 7 (Validation), Volume V Chapter 10 (Validation)

Validation categories (normative):
- Lexical validation
- Syntax validation
- Semantic validation
- Relationship validation
- Constraint validation
- Dependency validation
- Governance validation
- Safety validation

Inputs: UEM, Canonical Documents

Outputs: ValidationResult, categorized Diagnostics

---

## 3.8 Engineering Compiler

Path: `lib/python/engineering_engine` (module: `compiler`)

Responsibility: Orchestrate the full compilation pipeline from Knowledge Acquisition through Artifact Generation.

CSL Reference: Volume V (Compiler Specification)

Inputs: Canonical Repository path

Outputs: Compiled UEM, Engineering Artifacts

---

## 3.9 Artifact Generator Framework

Path: `lib/python/engineering_engine` (module: `generators`)

Responsibility: Generate Engineering Artifacts from a compiled UEM via registered generator contracts.

CSL Reference: RFC-0004 (Artifact Generator Framework)

Properties:
- Generator registration
- UEM-driven outputs only
- Deterministic generation
- Traceability preserved

---

## 3.10 Safety and Governance Kernel

Path: `lib/python/rule_engine` (module: `governance_kernel`)

Responsibility: Enforce mandatory permission, risk, approval, audit, authorization, and emergency-stop controls.

CSL Reference: Volume VII (Safety and Governance), RFC-0005 (Safety and Governance Kernel)

Components:
- Permission Engine
- Risk Engine
- Approval Engine
- Audit Engine
- Emergency Stop

---

## 3.11 Runtime Integrations

Path: `lib/python/runtime`

Responsibility: Provide continuous platform, HTTP API, scheduler, lifecycle, secrets, metrics, external interfaces.

CSL Reference: Volume VIII Chapter 4 (Mandatory Components), RFC-0007 (Repository Adapter Architecture)

Status: Comparatively mature. Incremental governance integration required.

---

# 4. Module Classification

All modules are classified as one of:

- `CSL-CORE`: implements a mandatory CSL subsystem
- `CSL-SUPPORT`: supports CSL operations without being a mandated subsystem
- `LEGACY`: shell modules maintained for compatibility only
- `GENERATED`: outputs from the compiler/generators
- `RUNTIME-STATE`: ephemeral state managed at runtime

Full module classification register: `docs/implementation/MODULE_CLASSIFICATION.md`

---

# 5. Dependency Ordering

Implementation shall respect the following dependency order:

1. canonical_entities (models, UEM types)
2. canonical_parser (lexer, AST, parser, semantic analyzer)
3. canonical_repository (source loader)
4. validation_engine (normative validation)
5. engineering_engine / compiler (compiler pipeline)
6. engineering_engine / generators (generator framework)
7. rule_engine / governance_kernel (governance)
8. runtime (runtime integrations)

No subsystem shall depend on a subsystem lower in this list.

---

# 6. Diagnostics Contract

Every subsystem shall produce Diagnostics conforming to:

```
DiagnosticSeverity: ERROR | WARNING | INFO | HINT
DiagnosticCategory: LEXICAL | SYNTAX | SEMANTIC | RELATIONSHIP | CONSTRAINT | DEPENDENCY | GOVERNANCE | SAFETY
DiagnosticCode: string identifier
message: human-readable description
source_ref: canonical source reference
```

Diagnostics shall be deterministic.

Equivalent inputs shall always produce equivalent diagnostics.

---

# 7. Traceability Requirement

Every Engineering Artifact shall carry a traceability chain from:

Canonical Document → AST Node → Semantic Object → UEM Entity → Generator → Artifact

No artifact shall exist without a complete traceability chain.

---

End of CSL Subsystem Architecture.

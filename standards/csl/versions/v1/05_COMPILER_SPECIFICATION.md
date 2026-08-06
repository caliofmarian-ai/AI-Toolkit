# Canonical Specification Language (CSL)

# Volume V

# COMPILER SPECIFICATION

Version: 1.0.0

Status: Normative

Classification: Core Specification

---

# Chapter 1

Purpose

This specification defines the Engineering Compiler.

The Engineering Compiler transforms Canonical Knowledge into the Universal Engineering Model and subsequently into Engineering Artifacts.

The compiler shall be deterministic.

The compiler shall preserve engineering semantics.

The compiler shall never alter Canonical Knowledge.

---

# Chapter 2

Compiler Objectives

The Engineering Compiler shall:

Load Canonical Knowledge.

Validate Canonical Knowledge.

Construct the Universal Engineering Model.

Optimize the Engineering Model.

Generate Engineering Artifacts.

Produce deterministic diagnostics.

Preserve complete traceability.

Support incremental compilation.

Support future extensions.

---

# Chapter 3

Compilation Pipeline

Compilation consists of the following conceptual stages.

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

↓

Publication

Every conforming implementation shall preserve the logical ordering of these stages.

---

# Chapter 4

Knowledge Acquisition

The compiler acquires Canonical Knowledge from one or more canonical sources.

Supported sources may include:

CSL Documents

Knowledge Packages

Canonical Repositories

Future Canonical Formats

Knowledge acquisition shall preserve provenance.

Knowledge acquisition shall never modify Canonical Knowledge.

---

# Chapter 5

Lexical Analysis

Lexical Analysis converts source text into Tokens.

Lexical Analysis shall:

recognize reserved keywords,

recognize identifiers,

recognize literals,

recognize references,

recognize delimiters,

ignore insignificant whitespace,

preserve source locations.

Lexical errors terminate compilation.

---

# Chapter 6

Parsing

Parsing transforms Tokens into an Abstract Syntax Tree.

Parsing shall detect:

unexpected tokens,

missing structures,

invalid block nesting,

grammar violations,

unexpected end of document.

Successful parsing produces a deterministic Abstract Syntax Tree.

---

# Chapter 7

Abstract Syntax Tree

The Abstract Syntax Tree represents syntactic structure.

The AST contains:

Nodes

Properties

References

Source Locations

Metadata

The AST possesses no semantic meaning.

Semantic interpretation begins only after AST construction.

---

# Chapter 8

Semantic Analysis

Semantic Analysis assigns engineering meaning.

Semantic Analysis resolves:

identities,

references,

relationships,

constraints,

ownership,

dependencies,

visibility,

lifecycle states.

Semantic Analysis constructs the Universal Engineering Model.

---

# Chapter 9

Universal Engineering Model Construction

The compiler transforms semantic information into the Universal Engineering Model.

The Universal Engineering Model shall be:

complete,

consistent,

deterministic,

technology independent,

implementation independent,

traceable.

Equivalent Canonical Knowledge shall always produce equivalent Engineering Models.

---

# Chapter 10

Validation

Validation verifies engineering correctness.

Validation categories include:

Lexical Validation

Syntax Validation

Semantic Validation

Relationship Validation

Constraint Validation

Dependency Validation

Governance Validation

Safety Validation

Compilation shall terminate upon mandatory validation failure.

# Chapter 11

Optimization

Optimization improves Engineering Model quality without modifying engineering meaning.

Optimization may include:

Relationship normalization

Reference resolution

Dependency reduction

Constraint simplification

Entity deduplication

Graph optimization

Metadata normalization

Optimization shall never modify Canonical Knowledge.

Optimization shall preserve semantic equivalence.

Optimization shall be deterministic.

Given the same Universal Engineering Model as input, the same optimization pass shall always produce an identical output model.

Non-deterministic optimization is prohibited.

Every optimization pass shall document:

its purpose,

its input requirements,

its semantic equivalence guarantee,

its performance characteristics.

Conformance tests shall verify that optimization does not alter the semantic meaning of the Engineering Model.

---

# Chapter 12

Artifact Generation

The Engineering Compiler generates Engineering Artifacts from the Universal Engineering Model.

Generators may produce:

Documentation

Architecture

Roadmaps

Milestones

Epics

Executable Issues

Source Code

Configuration

Infrastructure

Deployment Specifications

Test Suites

Validation Reports

Knowledge Graphs

Dependency Graphs

AI Tasks

Future generators may be added without changing Canonical Knowledge.

Generators operate only upon the Universal Engineering Model.

---

# Chapter 13

Diagnostics

Diagnostics communicate compiler findings.

Diagnostic categories include:

Information

Warning

Error

Critical Error

Every diagnostic shall include:

Identifier

Severity

Message

Location

Recommendation

Related Engineering Object

Diagnostics shall remain deterministic.

---

# Chapter 14

Compiler Errors

Compilation errors prevent successful compilation.

Compiler errors include:

Lexical Errors

Syntax Errors

Semantic Errors

Constraint Violations

Dependency Failures

Reference Failures

Governance Violations

Safety Violations

Every error shall possess a unique identifier.

Hidden errors are prohibited.

---

# Chapter 15

Incremental Compilation

The compiler shall support incremental compilation.

Incremental compilation recompiles only Engineering Objects affected by changes.

Incremental compilation shall preserve semantic equivalence with full compilation.

---

# Chapter 16

Parallel Compilation

Independent Engineering Objects may be compiled concurrently.

Parallel compilation shall never modify compilation results.

Concurrency affects performance only.

Semantics remain identical.

---

# Chapter 17

Compiler Extensions

Compiler implementations may introduce extensions.

Extensions may include:

New Generators

New Validators

Optimization Passes

Alternative Storage

Diagnostics

Monitoring

Extensions shall never violate the Constitution.

---

# Chapter 18

Compiler Versioning

Every compiler release shall identify:

Compiler Version

Supported CSL Version

Supported Grammar Version

Supported Semantic Model Version

Supported Generator Versions

Compiler versions shall remain traceable.

---

# Chapter 19

Compiler Conformance

A compiler is conforming only if it:

accepts valid Canonical Knowledge,

rejects invalid Canonical Knowledge,

constructs a valid Universal Engineering Model,

generates semantically equivalent Engineering Artifacts,

preserves traceability,

preserves determinism.

Partial implementations shall declare unsupported capabilities.

---

# Chapter 20

Error Code Registry

Every compiler diagnostic shall carry a unique error code from the registry defined in this chapter.

Error codes are permanent identifiers.

Error codes shall never be reused.

Error code format: `CSL-XXXX` where XXXX is a zero-padded four-digit number.

## Lexical Error Codes (CSL-0001 through CSL-0099)

| Code     | Severity | Description                                          |
|----------|----------|------------------------------------------------------|
| CSL-0001 | Error    | Invalid character in source document.                |
| CSL-0002 | Error    | Invalid character in identifier.                     |
| CSL-0003 | Error    | Unterminated string literal.                         |
| CSL-0004 | Error    | Tab character used for indentation.                  |
| CSL-0005 | Error    | Unexpected end of document during lexical analysis.  |
| CSL-0010 | Warning  | Source file encoding may not be UTF-8.               |

## Syntax Error Codes (CSL-0100 through CSL-0199)

| Code     | Severity | Description                                          |
|----------|----------|------------------------------------------------------|
| CSL-0100 | Error    | Unexpected token encountered.                        |
| CSL-0101 | Error    | Missing required block field.                        |
| CSL-0102 | Error    | Invalid block nesting.                               |
| CSL-0103 | Error    | Missing block termination.                           |
| CSL-0104 | Error    | Reserved keyword used as identifier.                 |
| CSL-0105 | Error    | Invalid indentation level.                           |
| CSL-0106 | Error    | Statement is incomplete.                             |
| CSL-0110 | Warning  | Unknown attribute name encountered.                  |

## Semantic Error Codes (CSL-0200 through CSL-0399)

| Code     | Severity | Description                                              |
|----------|----------|----------------------------------------------------------|
| CSL-0200 | Error    | Duplicate identifier within the same scope.              |
| CSL-0201 | Error    | Unresolvable reference.                                  |
| CSL-0202 | Error    | Circular dependency detected where not permitted.        |
| CSL-0203 | Error    | Required property missing.                               |
| CSL-0204 | Error    | Property type mismatch.                                  |
| CSL-0205 | Error    | Relationship cardinality violation.                      |
| CSL-0206 | Error    | Invalid lifecycle transition.                            |
| CSL-0207 | Error    | Visibility constraint violation.                         |
| CSL-0208 | Error    | Ownership constraint violated; entity has no owner.      |
| CSL-0210 | Warning  | Entity has no outgoing relationships.                    |
| CSL-0211 | Warning  | Property value is empty.                                 |
| CSL-0300 | Error    | Constraint violation.                                    |
| CSL-0301 | Error    | Dependency cycle in planning graph.                      |

## Governance Error Codes (CSL-0400 through CSL-0499)

| Code     | Severity       | Description                                      |
|----------|----------------|--------------------------------------------------|
| CSL-0400 | Critical Error | Unauthorized execution attempted.                |
| CSL-0401 | Critical Error | Critical action attempted without approval.      |
| CSL-0402 | Error          | Permission denied for requested operation.       |
| CSL-0403 | Error          | Policy violation detected.                       |
| CSL-0404 | Error          | Risk classification exceeds approved threshold.  |

## Compatibility Error Codes (CSL-0500 through CSL-0599)

| Code     | Severity | Description                                              |
|----------|----------|----------------------------------------------------------|
| CSL-0500 | Error    | CSL version unsupported by this compiler.                |
| CSL-0501 | Error    | Grammar version mismatch.                                |
| CSL-0502 | Warning  | Document targets a newer CSL version than this compiler. |
| CSL-0510 | Info     | Migration may be required for this document version.     |

Future error codes shall be assigned sequentially within the appropriate range.

Additional ranges may be defined through approved RFCs.

---

# Chapter 21

Closing Statement

The Engineering Compiler is the bridge between Canonical Knowledge and Engineering Artifacts.

Its purpose is not merely compilation.

Its purpose is the deterministic transformation of engineering knowledge into reproducible engineering systems.

Every future compiler shall preserve the principles established by this specification.

End of Volume V — Compiler Specification.
# Canonical Specification Language (CSL)

# COMPILER TEST SUITE

Version: 1.0.0

Status: Normative

Classification: Compiler Verification

---

# Purpose

This document defines the mandatory test suite used to verify CSL compiler implementations.

Every conforming compiler shall execute this suite.

Equivalent implementations shall produce equivalent results.

Test cases are identified by their Test ID (`CT-XXXX`). Test IDs are permanent and shall never be reused.

---

# Test Categories

The Compiler Test Suite consists of the following categories:

Lexical Tests (CT-0001 through CT-0099)

Grammar Tests (CT-0100 through CT-0199)

Parser Tests (CT-0200 through CT-0299)

Semantic Tests (CT-0300 through CT-0399)

Relationship Tests (CT-0400 through CT-0499)

Constraint Tests (CT-0500 through CT-0599)

Dependency Tests (CT-0600 through CT-0699)

Universal Engineering Model Tests (CT-0700 through CT-0799)

Artifact Generation Tests (CT-0800 through CT-0899)

Regression Tests (CT-0900 through CT-0999)

Compatibility Tests (CT-1000 through CT-1099)

---

# Lexical Tests

## CT-0001 — Valid Identifier Recognition

Input:

```
Project:
    Identifier: MY-PROJECT-001
```

Expected: Identifier token `MY-PROJECT-001` produced. Error code: none.

Expected Result: PASS

---

## CT-0002 — Reserved Keyword Recognition

Input: The token `Project` appearing as a block declaration keyword.

Expected: Keyword token produced, not an identifier token.

Expected Result: PASS

---

## CT-0003 — String Literal Recognition

Input:

```
Requirement:
    Name: "Authenticate users securely"
```

Expected: String token `Authenticate users securely` produced.

Expected Result: PASS

---

## CT-0004 — Invalid Identifier — Starts with Digit

Input:

```
Project:
    Identifier: 001-MY-PROJECT
```

Expected: Lexical error CSL-0002 produced.

Expected Result: FAIL (CSL-0002)

---

## CT-0005 — Reserved Keyword Used as Identifier

Input:

```
Feature:
    Identifier: Project
```

Expected: Semantic error CSL-0104 produced.

Expected Result: FAIL (CSL-0104)

---

## CT-0006 — Tab in Indentation

Input: A block field indented with a tab character instead of spaces.

Expected: Lexical error CSL-0004 produced.

Expected Result: FAIL (CSL-0004)

---

## CT-0007 — Unterminated String

Input:

```
Requirement:
    Name: "Unterminated string
```

Expected: Lexical error CSL-0003 produced.

Expected Result: FAIL (CSL-0003)

---

## CT-0008 — Comment Ignored

Input:

```
# This is a comment
Project:
    Identifier: PROJ-001
```

Expected: Comment produces no tokens. Project block parsed correctly.

Expected Result: PASS

---

# Grammar Tests

## CT-0100 — Minimal Valid Document

Input: The HELLO_CSL example document (see examples/basic/HELLO_CSL.md).

Expected: Document parses without errors.

Expected Result: PASS

---

## CT-0101 — Missing Required Block Field

Input:

```
Feature:
    Name: "Login"
```

(Identifier field absent)

Expected: Semantic error CSL-0203 produced for missing Identifier.

Expected Result: FAIL (CSL-0203)

---

## CT-0102 — Invalid Block Nesting

Input: A nested block that violates grammar structure (e.g., a Project block inside a Feature block).

Expected: Syntax error CSL-0102 produced.

Expected Result: FAIL (CSL-0102)

---

## CT-0103 — Relationship Block Correct Syntax

Input:

```
Relationship:
    FEAT-001 implements REQ-001
```

Expected: Relationship parsed as source=FEAT-001, verb=implements, target=REQ-001.

Expected Result: PASS

---

## CT-0104 — Unknown Relationship Verb

Input:

```
Relationship:
    FEAT-001 supersedes REQ-001
```

Expected: Syntax error or warning CSL-0110 produced.

Expected Result: FAIL (CSL-0100 or CSL-0110)

---

# Parser Tests

## CT-0200 — AST Construction from Minimal Document

Input: The HELLO_CSL example document.

Expected: Abstract Syntax Tree contains Project node, Capability node, Requirement node, Feature node, and two Relationship nodes.

Expected Result: PASS

---

## CT-0201 — Source Location Preservation

Input: Any valid CSL document.

Expected: Every AST node carries a source file path, line number, and column number.

Expected Result: PASS

---

## CT-0202 — Deterministic AST

Input: The same valid CSL document compiled twice.

Expected: Both resulting ASTs are structurally identical.

Expected Result: PASS

---

# Semantic Tests

## CT-0300 — Engineering Entity Creation

Input: The MINIMAL_PROJECT example document.

Expected: Semantic analysis produces Engineering Entities for Project, Capability, Requirement, Feature.

Expected Result: PASS

---

## CT-0301 — Duplicate Identifier Detection

Input:

```
Feature:
    Identifier: FEAT-001
    Name: "First Feature"

Feature:
    Identifier: FEAT-001
    Name: "Duplicate"
```

Expected: Semantic error CSL-0200 produced.

Expected Result: FAIL (CSL-0200)

---

## CT-0302 — Unresolvable Reference

Input:

```
Relationship:
    FEAT-999 implements REQ-001
```

Where FEAT-999 does not exist.

Expected: Semantic error CSL-0201 produced.

Expected Result: FAIL (CSL-0201)

---

## CT-0303 — Lifecycle Validation

Input: A document where an entity transitions directly from Draft to Operational, skipping intermediate states.

Expected: Semantic error CSL-0206 produced.

Expected Result: FAIL (CSL-0206)

---

## CT-0304 — Visibility Default

Input: An entity declared without a Visibility attribute.

Expected: Entity receives default visibility Public in the semantic model.

Expected Result: PASS

---

# Relationship Tests

## CT-0400 — Valid Relationship Type

Input: `FEAT-001 implements REQ-001` where both entities exist.

Expected: Relationship created in the Universal Engineering Model.

Expected Result: PASS

---

## CT-0401 — Cardinality Violation — belongs_to Many-to-One

Input: An entity that belongs_to two different parent entities simultaneously.

Expected: Semantic error CSL-0205 produced.

Expected Result: FAIL (CSL-0205)

---

## CT-0402 — Relationship Direction

Input: `REQ-001 implements FEAT-001` (reversed direction for implements).

Expected: Relationship is created with the declared direction. Direction is preserved in the UEM.

Expected Result: PASS (direction preserved as declared)

---

# Constraint Tests

## CT-0500 — Constraint Violation Terminates Compilation

Input: A document with a constraint declared as mandatory that is violated.

Expected: Compilation terminates with error CSL-0300.

Expected Result: FAIL (CSL-0300)

---

## CT-0501 — Valid Constraint Passes

Input: A document where all declared constraints are satisfied.

Expected: Compilation completes without constraint errors.

Expected Result: PASS

---

# Dependency Tests

## CT-0600 — Circular Dependency Detection

Input: Entity A depends_on Entity B; Entity B depends_on Entity A.

Expected: Semantic error CSL-0202 produced.

Expected Result: FAIL (CSL-0202)

---

## CT-0601 — Valid Dependency Chain

Input: Entity A depends_on Entity B; Entity B depends_on Entity C; no cycle.

Expected: Dependency graph constructed. Compilation order: C → B → A.

Expected Result: PASS

---

# Universal Engineering Model Tests

## CT-0700 — UEM Determinism

Input: The same valid Canonical Knowledge compiled by two conforming implementations.

Expected: Both Universal Engineering Models are semantically equivalent.

Expected Result: PASS

---

## CT-0701 — UEM Contains All Required Objects

Input: The MINIMAL_PROJECT example document.

Expected: The UEM contains Project, Capability, Requirement, Feature, and all declared Relationships.

Expected Result: PASS

---

## CT-0702 — UEM Provenance

Input: Any valid Canonical Knowledge document.

Expected: Every Engineering Object in the UEM carries origin, creator, compiler version, and CSL version in its provenance record.

Expected Result: PASS

---

# Artifact Generation Tests

## CT-0800 — Documentation Generation

Input: The MINIMAL_PROJECT example document.

Expected: A documentation artifact is produced. The artifact identifies its originating canonical source.

Expected Result: PASS

---

## CT-0801 — Artifact Contains Metadata

Input: Any valid Canonical Knowledge document.

Expected: Every generated artifact contains: generator identifier, compiler version, CSL version, generation timestamp, and traceability reference.

Expected Result: PASS

---

# Regression Tests

## CT-0900 — Backward Compatibility

Input: A document conforming to CSL Version 1.0.0 compiled by a Version 1.x.x compiler.

Expected: Compilation succeeds without modification to the source document.

Expected Result: PASS

---

# Compatibility Tests

## CT-1000 — CSL Version Declaration

Input: A document declaring `Version: 1.0.0`.

Expected: Compiler accepts the document and reports no version compatibility errors.

Expected Result: PASS

---

## CT-1001 — Unsupported CSL Version

Input: A document declaring a CSL version higher than the compiler supports.

Expected: Error CSL-0500 produced.

Expected Result: FAIL (CSL-0500)

---

# Required Reporting

Every compiler execution shall generate:

Compiler Version

CSL Version

Test Results including Test ID, Input Description, Expected Result, Actual Result, Pass or Fail

Warnings

Errors with error codes

Execution Duration

Summary

Reports shall remain auditable.

---

# Conformance Requirements

A compiler shall not claim conformance unless every mandatory test produces the expected result.

Partial implementations shall explicitly declare unsupported functionality.

---

# Closing Statement

The Compiler Test Suite provides the canonical verification process for CSL compiler implementations.

Successful execution demonstrates deterministic compilation, semantic correctness and conformance with the Canonical Specification Language.

End of Compiler Test Suite.
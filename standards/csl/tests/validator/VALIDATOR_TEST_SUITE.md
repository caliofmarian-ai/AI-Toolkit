# Canonical Specification Language (CSL)

# VALIDATOR TEST SUITE

Version: 1.0.0

Status: Normative

Classification: Validator Verification

---

# Purpose

This document defines the mandatory verification suite for CSL Validator implementations.

The Validator is responsible for ensuring that Canonical Knowledge conforms to the CSL Standard before compilation.

Every conforming Validator shall execute this suite.

Test cases are identified by their Test ID (`VT-XXXX`). Test IDs are permanent and shall never be reused.

---

# Validation Objectives

The Validator shall verify:

Lexical correctness.

Grammar correctness.

Document structure.

Semantic correctness.

Engineering Relationships.

Engineering Properties.

Engineering Constraints.

Engineering Dependencies.

Engineering Provenance.

Governance compliance.

Safety compliance.

Validation shall never modify Canonical Knowledge.

---

# Test Categories

The Validator Test Suite consists of:

Document Validation (VT-0001 through VT-0099)

Lexical Validation (VT-0100 through VT-0199)

Grammar Validation (VT-0200 through VT-0299)

Schema Validation (VT-0300 through VT-0399)

Entity Validation (VT-0400 through VT-0499)

Relationship Validation (VT-0500 through VT-0599)

Property Validation (VT-0600 through VT-0699)

Constraint Validation (VT-0700 through VT-0799)

Dependency Validation (VT-0800 through VT-0899)

Lifecycle Validation (VT-0900 through VT-0999)

Reference Validation (VT-1000 through VT-1099)

Governance Validation (VT-1100 through VT-1199)

Safety Validation (VT-1200 through VT-1299)

Regression Validation (VT-1300 through VT-1399)

Compatibility Validation (VT-1400 through VT-1499)

---

# Document Validation

## VT-0001 — Valid Document Header

Input: A CSL document with all required header fields: Document Type, Version, Status, Classification.

Expected: Document header validation passes.

Expected Result: PASS

---

## VT-0002 — Missing Required Header Field

Input: A CSL document missing the Status field in its header.

Expected: Validation error CSL-0203 produced.

Expected Result: FAIL (CSL-0203)

---

## VT-0003 — Invalid Status Value

Input: A document with `Status: UnknownState`.

Expected: Validation warning CSL-0110 produced.

Expected Result: FAIL (CSL-0110)

---

## VT-0004 — Valid Version Format

Input: A document with `Version: 1.0.0`.

Expected: Version validation passes.

Expected Result: PASS

---

# Lexical Validation

## VT-0100 — UTF-8 Encoding

Input: A CSL document encoded in UTF-8.

Expected: Encoding validation passes.

Expected Result: PASS

---

## VT-0101 — Identifier Beginning with Letter

Input: `Identifier: REQ-001`

Expected: Lexical validation passes.

Expected Result: PASS

---

## VT-0102 — Identifier Beginning with Digit

Input: `Identifier: 001-REQ`

Expected: Lexical error CSL-0002 produced.

Expected Result: FAIL (CSL-0002)

---

## VT-0103 — Whitespace in Identifier

Input: `Identifier: REQ 001`

Expected: Lexical error CSL-0002 produced.

Expected Result: FAIL (CSL-0002)

---

# Grammar Validation

## VT-0200 — Valid Block Structure

Input: A block with correct indentation and field declarations.

Expected: Grammar validation passes.

Expected Result: PASS

---

## VT-0201 — Invalid Block Nesting

Input: A Project block declared inside a Feature block.

Expected: Grammar error CSL-0102 produced.

Expected Result: FAIL (CSL-0102)

---

## VT-0202 — Incomplete Statement

Input: A block field with a name but no value.

Expected: Grammar error CSL-0106 produced.

Expected Result: FAIL (CSL-0106)

---

# Schema Validation

## VT-0300 — Entity Conforms to Entity Schema

Input: A Feature entity with all mandatory fields (Identifier, Name, Status, Lifecycle, Owner).

Expected: Schema validation passes.

Expected Result: PASS

---

## VT-0301 — Entity Missing Mandatory Schema Field

Input: A Requirement entity without an Identifier field.

Expected: Validation error CSL-0203 produced.

Expected Result: FAIL (CSL-0203)

---

## VT-0302 — Relationship Conforms to Relationship Schema

Input: A relationship block with Identifier, Type, Source, and Target fields.

Expected: Schema validation passes.

Expected Result: PASS

---

# Entity Validation

## VT-0400 — Unique Identifier Within Scope

Input: Two Feature entities with different Identifiers in the same document.

Expected: Validation passes.

Expected Result: PASS

---

## VT-0401 — Duplicate Identifier Within Scope

Input: Two Feature entities with the same Identifier in the same document.

Expected: Validation error CSL-0200 produced.

Expected Result: FAIL (CSL-0200)

---

## VT-0402 — Entity Identity Immutability

Input: An entity that changes its Identifier between document versions.

Expected: Validation warning produced indicating identity change creates a new object.

Expected Result: WARNING

---

# Relationship Validation

## VT-0500 — Valid Relationship References Existing Entities

Input: `FEAT-001 implements REQ-001` where both exist.

Expected: Relationship validation passes.

Expected Result: PASS

---

## VT-0501 — Broken Relationship Reference

Input: `FEAT-001 implements REQ-999` where REQ-999 does not exist.

Expected: Semantic error CSL-0201 produced.

Expected Result: FAIL (CSL-0201)

---

## VT-0502 — Cardinality Violation

Input: An entity with two `belongs_to` relationships to different parents.

Expected: Semantic error CSL-0205 produced.

Expected Result: FAIL (CSL-0205)

---

# Property Validation

## VT-0600 — Valid Property Type

Input: A property declared as Integer containing a numeric value.

Expected: Property validation passes.

Expected Result: PASS

---

## VT-0601 — Property Type Mismatch

Input: A property declared as Integer containing a string value.

Expected: Validation error CSL-0204 produced.

Expected Result: FAIL (CSL-0204)

---

# Constraint Validation

## VT-0700 — Satisfied Constraint

Input: A document where all declared constraints are satisfied.

Expected: Constraint validation passes.

Expected Result: PASS

---

## VT-0701 — Violated Constraint

Input: A document where a mandatory constraint is violated.

Expected: Validation error CSL-0300 produced.

Expected Result: FAIL (CSL-0300)

---

# Dependency Validation

## VT-0800 — Valid Dependency Chain

Input: Entity A depends_on Entity B; Entity B depends_on Entity C; no cycle exists.

Expected: Dependency validation passes.

Expected Result: PASS

---

## VT-0801 — Circular Dependency

Input: Entity A depends_on Entity B; Entity B depends_on Entity A.

Expected: Validation error CSL-0202 produced.

Expected Result: FAIL (CSL-0202)

---

## VT-0802 — Unresolved Mandatory Dependency

Input: Entity A depends_on Entity B; Entity B is not declared.

Expected: Validation error CSL-0201 produced.

Expected Result: FAIL (CSL-0201)

---

# Lifecycle Validation

## VT-0900 — Valid Lifecycle State

Input: An entity with `Status: Approved` in a document context consistent with the Approved lifecycle state.

Expected: Lifecycle validation passes.

Expected Result: PASS

---

## VT-0901 — Invalid Lifecycle Transition

Input: An entity transitioning directly from Draft to Operational.

Expected: Validation error CSL-0206 produced.

Expected Result: FAIL (CSL-0206)

---

# Reference Validation

## VT-1000 — Valid Reference

Input: A Reference pointing to an Engineering Entity that exists in the same Knowledge Package.

Expected: Reference validation passes.

Expected Result: PASS

---

## VT-1001 — Broken Reference

Input: A Reference pointing to an Engineering Entity that does not exist.

Expected: Validation error CSL-0201 produced.

Expected Result: FAIL (CSL-0201)

---

# Governance Validation

## VT-1100 — Critical Action with Approval

Input: A critical action request with an explicit Approval record attached.

Expected: Governance validation passes.

Expected Result: PASS

---

## VT-1101 — Critical Action without Approval

Input: A critical action request without an Approval record.

Expected: Critical error CSL-0401 produced.

Expected Result: FAIL (CSL-0401)

---

# Safety Validation

## VT-1200 — Authorized Execution Request

Input: An execution request from an authenticated actor with the required permissions.

Expected: Safety validation passes.

Expected Result: PASS

---

## VT-1201 — Unauthorized Execution Request

Input: An execution request from an actor without the required permissions.

Expected: Critical error CSL-0400 produced.

Expected Result: FAIL (CSL-0400)

---

# Regression Validation

## VT-1300 — CSL Version 1.0.0 Backward Compatibility

Input: Any document conforming to CSL Version 1.0.0.

Expected: Validation succeeds without modification.

Expected Result: PASS

---

# Compatibility Validation

## VT-1400 — Supported CSL Version

Input: A document declaring `Version: 1.0.0` validated by a Version 1.x.x validator.

Expected: Compatibility validation passes.

Expected Result: PASS

---

## VT-1401 — Unsupported CSL Version

Input: A document declaring a CSL version higher than the validator supports.

Expected: Error CSL-0500 produced.

Expected Result: FAIL (CSL-0500)

---

# Validation Reports

Every validation execution shall generate:

Validator Version

CSL Version

Validation Timestamp

Validated Documents

Test ID

Expected Result

Actual Result

Pass or Fail per test

Warnings with codes

Errors with codes

Execution Duration

Summary

Reports shall remain immutable and auditable.

---

# Conformance Requirements

A Validator shall not claim conformance unless every mandatory validation category succeeds.

Partial Validators shall explicitly declare unsupported validation capabilities.

---

# Closing Statement

The Validator Test Suite establishes the canonical verification process for Validator implementations.

Successful execution demonstrates deterministic validation, semantic correctness and full conformance with the Canonical Specification Language.

End of Validator Test Suite.

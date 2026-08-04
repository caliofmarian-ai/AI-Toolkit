# Canonical Specification Language (CSL)

# Volume II

# LANGUAGE SPECIFICATION

Version: Draft 0.1

Status: Normative

Classification: Core Specification

---

# Chapter 1

Purpose

This specification defines the Canonical Specification Language itself.

Where the Foundations specification defines engineering concepts,

this document defines how those concepts are represented.

This specification defines:

document structure,

language structure,

keywords,

blocks,

identifiers,

attributes,

relationships,

references,

data types,

comments,

extensions,

conformance.

Every conforming compiler shall implement this specification.

---

# Chapter 2

Language Objectives

The CSL language shall be:

Human Readable.

Machine Readable.

Deterministic.

Technology Independent.

Implementation Independent.

Extensible.

Versionable.

Self-describing.

Stable.

Unambiguous.

The language shall prioritize engineering clarity over syntactic brevity.

---

# Chapter 3

Language Design Principles

The language follows six design principles.

Clarity before brevity.

Semantics before syntax.

Consistency before convenience.

Determinism before flexibility.

Extensibility before specialization.

Knowledge before implementation.

Every future language feature shall remain consistent with these principles.

---

# Chapter 4

Document Structure

Every CSL document represents one canonical engineering document.

Every document shall contain:

Header

Metadata

Body

References

Optional Appendices

The compiler shall reject documents that violate mandatory document structure.

---

# Chapter 5

Document Header

Every document begins with a header.

Minimum required fields:

Document Type

Title

Version

Status

Classification

Optional fields include:

Identifier

Author

Approver

Created

Modified

Compiler Version

Language Version

Reference Version

Future versions may define additional metadata.

---

# Chapter 6

Identifiers

Every engineering object possesses an identifier.

Identifiers shall be unique within their scope.

Identifiers are immutable.

Identifiers may contain:

letters,

numbers,

hyphen,

underscore.

Identifiers shall never contain whitespace.

Identifiers are case-sensitive.

Changing an identifier creates a new engineering object.

---

# Chapter 7

Reserved Keywords

The following keywords are reserved.

Project

Capability

Feature

Requirement

Decision

Constraint

Policy

Rule

Risk

Issue

Epic

Milestone

Task

Component

Module

Service

API

Entity

Relationship

Generator

Validator

Compiler

Runtime

Knowledge

Reference

Approval

Deployment

Environment

Provider

Model

Prompt

Future specifications may reserve additional keywords.

Reserved keywords shall not be used as user-defined identifiers.

---

# Chapter 8

Blocks

The language is block oriented.

Each block represents one engineering object.

A block begins with its object declaration.

A block terminates explicitly.

Nested blocks are permitted where defined by the specification.

Block boundaries shall remain explicit.

Implicit block termination is prohibited.

---

# Chapter 9

Attributes

Attributes define properties.

Every attribute consists of:

Name

Value

Optional Metadata

Attributes may be:

Required

Optional

Computed

Generated

Compiler Reserved

Unknown attributes shall produce validation warnings unless explicitly permitted.

---

# Chapter 10

Relationships

Relationships connect engineering objects.

Relationship declarations shall include:

Source

Relationship Type

Target

Optional Metadata

Relationships are directional unless declared otherwise.

Relationship semantics are defined by the Semantic Model specification.

---

# Chapter 11

References

References create semantic links without ownership.

References never duplicate engineering knowledge.

A reference shall always target an existing engineering object.

Broken references are compilation errors.

Circular references are permitted only when explicitly allowed by the Semantic Model.

---

# Chapter 12

Language Philosophy

The Canonical Specification Language is intentionally descriptive rather than procedural.

It describes engineering knowledge.

It does not describe execution order.

Execution belongs to implementations.

Knowledge belongs to CSL.

This distinction shall remain fundamental throughout every future version of the language.

# Chapter 13

Data Types

The Canonical Specification Language defines a common set of primitive data types.

Every conforming implementation shall support these primitive types.

String

Represents textual information.

Integer

Represents whole numbers.

Decimal

Represents fractional numbers.

Boolean

Represents true or false values.

Date

Represents calendar dates.

Time

Represents time values.

Timestamp

Represents date and time.

Duration

Represents elapsed time.

Identifier

Represents immutable engineering identities.

Reference

Represents semantic references to Engineering Entities.

Enumeration

Represents predefined value sets.

List

Represents ordered collections.

Map

Represents key-value collections.

Object

Represents structured engineering data.

Null

Represents the absence of a value.

Future versions may introduce additional primitive types.

---

# Chapter 14

Collections

Collections group multiple engineering values.

Supported collection types include:

List

Set

Dictionary

Ordered Map

Graph Collection

Collections may contain primitive values or Engineering Entities.

Nested collections are permitted.

Recursive collections shall be validated.

---

# Chapter 15

Naming Rules

Names shall be meaningful.

Names shall describe engineering intent.

Abbreviations should be avoided unless universally recognized.

Identifiers remain immutable.

Display names may evolve.

Duplicate names are permitted.

Duplicate identifiers are prohibited.

---

# Chapter 16

Comments

Comments provide explanatory information.

Comments never become Canonical Knowledge.

Comments shall never modify engineering semantics.

Compilers may ignore comments.

Validators may preserve comments.

Generators may reproduce comments where appropriate.

---

# Chapter 17

Whitespace

Whitespace improves readability.

Whitespace shall never modify engineering meaning.

Indentation shall remain consistent.

Future language profiles may define preferred formatting rules.

Formatting differences shall never change semantic interpretation.

---

# Chapter 18

Ordering

Document ordering exists solely to improve readability.

Compilers shall not infer semantic meaning from ordering unless explicitly defined.

Engineering relationships define semantics.

Document position does not.

---

# Chapter 19

Validation Rules

Every CSL document shall satisfy lexical validation.

Every CSL document shall satisfy structural validation.

Every CSL document shall satisfy semantic validation.

Every CSL document shall satisfy reference validation.

Documents failing mandatory validation shall not be compiled.

Validation shall produce deterministic diagnostics.

---

# Chapter 20

Language Profiles

Future versions may define language profiles.

Examples include:

Core Profile

Enterprise Profile

Embedded Profile

Education Profile

Research Profile

Profiles may extend the language.

Profiles shall never contradict the Core Language.

---

# Chapter 21

Extensibility

The language is intentionally extensible.

Extensions may introduce:

keywords,

entity types,

relationship types,

attributes,

validators,

compiler directives,

metadata.

Extensions shall preserve backward compatibility whenever technically feasible.

---

# Chapter 22

Compiler Directives

Compiler directives influence compilation.

Compiler directives never modify Canonical Knowledge.

Directives affect:

validation,

optimization,

generation,

diagnostics,

output selection.

Directives remain optional.

Unsupported directives shall produce explicit diagnostics.

---

# Chapter 23

Language Stability

The language shall evolve conservatively.

Existing documents should remain valid whenever possible.

Breaking language changes require:

formal proposal,

technical justification,

migration strategy,

version increment,

approval according to governance rules.

---

# Chapter 24

Conformance

A CSL Language implementation is conforming only if it correctly parses,

validates,

and represents Canonical Knowledge according to this specification.

Partial implementations shall explicitly identify unsupported language features.

Silent feature omission is prohibited.

---

# Chapter 25

Closing Statement

The Language Specification defines how Canonical Knowledge is expressed.

Meaning is defined by the Semantic Model.

Processing is defined by the Compiler Specification.

Governance is defined by the Constitution.

Together these specifications establish the complete Canonical Specification Language.

End of Volume II — Language Specification.
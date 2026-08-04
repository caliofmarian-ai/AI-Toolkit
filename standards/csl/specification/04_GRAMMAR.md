# Canonical Specification Language (CSL)

# Volume IV

# GRAMMAR

Version: Draft 0.1

Status: Normative

Classification: Core Specification

---

# Chapter 1

Purpose

This specification defines the formal grammar of the Canonical Specification Language.

The grammar specifies how Canonical Knowledge is represented in textual form.

Every conforming parser shall interpret CSL documents according to this grammar.

The grammar defines structure.

Semantics are defined separately.

---

# Chapter 2

Grammar Objectives

The grammar shall be:

Deterministic.

Human Readable.

Machine Readable.

Predictable.

Consistent.

Extensible.

Versioned.

The grammar shall minimize ambiguity.

---

# Chapter 3

Grammar Architecture

The grammar consists of:

Lexical Grammar

↓

Syntactic Grammar

↓

Structural Grammar

↓

Semantic Validation

↓

Universal Engineering Model

Each layer depends upon the previous layer.

No semantic interpretation shall occur before syntactic correctness.

---

# Chapter 4

Tokens

The smallest grammatical unit is the Token.

Token categories include:

Identifier

Keyword

Literal

Number

String

Boolean

Reference

Operator

Delimiter

Comment

Whitespace

Compilers shall tokenize deterministically.

---

# Chapter 5

Keywords

Keywords possess reserved meaning.

Reserved keywords shall never be interpreted as identifiers.

Future versions may introduce additional keywords.

Existing keyword semantics shall remain stable.

---

# Chapter 6

Identifiers

Identifiers uniquely identify engineering objects.

Identifier grammar shall guarantee uniqueness within scope.

Identifiers shall be immutable.

Identifier comparison is case-sensitive.

Whitespace is prohibited.

---

# Chapter 7

Literals

Supported literals include:

String

Integer

Decimal

Boolean

Date

Timestamp

Duration

Enumeration

Null

Future language revisions may introduce additional literal types.

---

# Chapter 8

Statements

A Statement represents one grammatical declaration.

Statements shall be complete.

Incomplete statements are syntactic errors.

Statements may contain:

Attributes

Relationships

Nested Statements

References

Metadata

---

# Chapter 9

Blocks

Blocks group related statements.

Every block begins explicitly.

Every block ends explicitly.

Nested blocks shall remain structurally valid.

Implicit block termination is prohibited.

---

# Chapter 10

Expressions

Expressions represent values.

Expressions may consist of:

Literals

Identifiers

References

Collections

Computed Values

Expressions shall remain deterministic.

Expressions shall never modify Canonical Knowledge.

# Chapter 11

Collections

Collections group engineering values.

Supported collection types include:

List

Set

Dictionary

Ordered Collection

Map

Graph Collection

Collections may contain:

Primitive Values

Engineering Entities

References

Nested Collections

Collections shall preserve deterministic ordering where required.

---

# Chapter 12

References

References connect Engineering Objects.

A Reference shall contain:

Reference Identifier

Target Type

Target Identifier

Optional Version

Optional Constraint

Broken references are compilation errors.

Dangling references are prohibited.

Circular references shall be validated according to the Semantic Model.

---

# Chapter 13

Attributes

Attributes define Engineering Properties.

Each Attribute consists of:

Name

Type

Value

Optional Constraint

Optional Metadata

Attributes shall conform to their declared type.

Type mismatches are validation errors.

---

# Chapter 14

Comments

Comments improve readability.

Comments possess no engineering meaning.

Comments shall never modify Canonical Knowledge.

Compilers may ignore comments.

Documentation generators may preserve comments.

---

# Chapter 15

Whitespace

Whitespace exists only for readability.

Whitespace shall never influence engineering meaning.

Formatting differences shall never change semantic interpretation.

Automatic formatting tools shall preserve semantics.

---

# Chapter 16

Ordering

Statement order improves readability.

Ordering shall never define engineering meaning unless explicitly defined.

Relationships define meaning.

Document order does not.

---

# Chapter 17

Parser Requirements

Every conforming parser shall:

recognize valid grammar,

reject invalid grammar,

produce deterministic diagnostics,

construct equivalent syntax trees,

preserve source locations,

support incremental parsing where possible.

Parser implementations may differ internally.

Parser behavior shall remain semantically equivalent.

---

# Chapter 18

Grammar Validation

Grammar validation consists of:

Lexical Validation

Token Validation

Syntax Validation

Block Validation

Reference Validation

Document Validation

Successful grammar validation precedes semantic analysis.

---

# Chapter 19

Grammar Evolution

Grammar shall evolve conservatively.

Existing documents should remain valid whenever technically feasible.

Breaking grammar changes require:

RFC approval,

version increment,

migration documentation,

compatibility analysis.

Silent grammar changes are prohibited.

---

# Chapter 20

Closing Statement

The Grammar Specification defines the textual representation of Canonical Knowledge.

Every conforming parser shall implement this specification.

Every future language revision shall remain consistent with the constitutional principles established by the CSL standard.

End of Volume IV — Grammar.
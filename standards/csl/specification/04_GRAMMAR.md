# Canonical Specification Language (CSL)

# Volume IV

# GRAMMAR

Version: 1.0.0

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

Formal Grammar

This chapter defines the normative grammar of the Canonical Specification Language using Extended Backus-Naur Form (EBNF).

The notation conventions are as follows.

`::=` denotes production rules.

`|` denotes alternatives.

`[ ]` denotes optional elements.

`{ }` denotes zero or more repetitions.

`( )` groups alternatives.

`" "` denotes literal terminals.

Terminals in UPPER_CASE denote token categories defined in the Lexical Grammar section below.

---

## 20.1 File and Encoding

Every CSL source file shall be encoded in UTF-8.

The recommended file extension is `.csl`.

Line endings may be LF or CRLF; compilers shall treat both equivalently.

---

## 20.2 Lexical Grammar

```
WHITESPACE    ::= ( " " | "\t" | "\r" | "\n" )+

NEWLINE       ::= "\r\n" | "\n"

LINE_COMMENT  ::= "#" { any character except NEWLINE } NEWLINE

IDENTIFIER    ::= LETTER { LETTER | DIGIT | "-" | "_" }
                  (* Must begin with a letter. Case-sensitive. *)

LETTER        ::= "A".."Z" | "a".."z"

DIGIT         ::= "0".."9"

STRING        ::= '"' { STRING_CHAR } '"'
STRING_CHAR   ::= any Unicode character except '"' and '\n'
                | '\\"' | '\\\\'

INTEGER       ::= [ "-" ] DIGIT { DIGIT }

DECIMAL       ::= [ "-" ] DIGIT { DIGIT } "." DIGIT { DIGIT }

BOOLEAN       ::= "true" | "false"

DATE          ::= DIGIT DIGIT DIGIT DIGIT "-" DIGIT DIGIT "-" DIGIT DIGIT

TIMESTAMP     ::= DATE "T" DIGIT DIGIT ":" DIGIT DIGIT ":" DIGIT DIGIT [ "Z" ]

DURATION      ::= INTEGER ( "d" | "h" | "m" | "s" )

NULL          ::= "null"

VERSION       ::= DIGIT { DIGIT } "." DIGIT { DIGIT } "." DIGIT { DIGIT }

KEYWORD       ::= "Project" | "Capability" | "Feature" | "Requirement"
                | "Decision" | "Constraint" | "Policy" | "Rule" | "Risk"
                | "Issue" | "Epic" | "Milestone" | "Task" | "Component"
                | "Module" | "Service" | "API" | "Entity" | "Relationship"
                | "Generator" | "Validator" | "Compiler" | "Runtime"
                | "Knowledge" | "Reference" | "Approval" | "Deployment"
                | "Environment" | "Provider" | "Model" | "Prompt"
```

---

## 20.3 Syntactic Grammar

```
document          ::= document_header NEWLINE { document_section }

document_header   ::= document_type_decl
                      version_decl
                      status_decl
                      [ classification_decl ]
                      { optional_header_field }

document_type_decl ::= KEYWORD ":" NEWLINE
                      |  IDENTIFIER ":" NEWLINE

version_decl       ::= "Version" ":" version_value NEWLINE
version_value      ::= VERSION | STRING

status_decl        ::= "Status" ":" STATUS_VALUE NEWLINE
STATUS_VALUE       ::= IDENTIFIER { " " IDENTIFIER }

classification_decl ::= "Classification" ":" STRING NEWLINE

optional_header_field ::= IDENTIFIER ":" ( value | NEWLINE ) NEWLINE

document_section   ::= block_declaration
                      | relationship_declaration
                      | property_declaration
                      | comment
                      | NEWLINE

block_declaration  ::= KEYWORD ":"  NEWLINE
                       INDENT { block_field } DEDENT

block_field        ::= attribute_field
                      | relationship_field
                      | nested_block
                      | comment

attribute_field    ::= IDENTIFIER ":" value NEWLINE
                     | IDENTIFIER ":" NEWLINE INDENT value_list DEDENT

nested_block       ::= KEYWORD ":" NEWLINE INDENT { block_field } DEDENT

relationship_declaration ::= "Relationship" ":" NEWLINE
                             INDENT relationship_body DEDENT

relationship_body  ::= source_ref relationship_verb target_ref NEWLINE
                      { relationship_attribute }

source_ref         ::= IDENTIFIER | KEYWORD
target_ref         ::= IDENTIFIER | KEYWORD
relationship_verb  ::= "implements" | "contains" | "depends_on" | "extends"
                      | "references" | "requires" | "owns" | "approves"
                      | "tests" | "validates" | "generates" | "deploys"
                      | "publishes" | "consumes" | "supports" | "belongs_to"

relationship_attribute ::= IDENTIFIER ":" value NEWLINE

property_declaration ::= IDENTIFIER ":" value NEWLINE

value              ::= STRING
                      | INTEGER
                      | DECIMAL
                      | BOOLEAN
                      | DATE
                      | TIMESTAMP
                      | DURATION
                      | VERSION
                      | NULL
                      | IDENTIFIER
                      | list_value
                      | map_value

value_list         ::= { "-" value NEWLINE }

list_value         ::= "[" [ value { "," value } ] "]"

map_value          ::= "{" [ map_entry { "," map_entry } ] "}"
map_entry          ::= STRING ":" value

comment            ::= "#" { any character except NEWLINE } NEWLINE

INDENT             ::= increase in indentation level (four spaces per level)
DEDENT             ::= decrease to matching indentation level
```

---

## 20.4 Identifier Rules

An Identifier shall:

Begin with an ASCII letter (A-Z or a-z).

Contain only ASCII letters, ASCII digits, hyphens, and underscores.

Contain no whitespace.

Be case-sensitive.

Not be identical to a reserved KEYWORD.

Have a minimum length of one character.

Have no defined maximum length, though implementations should support at least 128 characters.

---

## 20.5 Identifier Uniqueness Scope

Identifiers shall be unique within their declaring document scope.

When Knowledge Packages combine multiple documents, identifiers shall be unique within the Knowledge Package scope.

The Knowledge Package manifest defines the scope boundary.

Identifiers that are identical across separate Knowledge Packages are not in conflict unless the packages are combined in the same compilation unit.

---

## 20.6 Indentation Rules

CSL uses indentation to denote block structure.

One indentation level equals four spaces.

Tabs shall not be used for indentation.

Compilers shall report a lexical error when tabs appear in indentation context.

---

## 20.7 Grammar Examples

The following examples are normative representations of correct CSL syntax.

**Minimal valid document:**

```
Project:
    Identifier: MY-PROJECT
    Name: "My Engineering Project"
    Version: 1.0.0
    Status: Approved
```

**Entity with relationships:**

```
Capability:
    Identifier: CAP-001
    Name: "User Authentication"
    Status: Approved

Feature:
    Identifier: FEAT-001
    Name: "Login"
    Status: Approved

Requirement:
    Identifier: REQ-001
    Name: "Users shall authenticate with credentials"
    Status: Approved

Relationship:
    FEAT-001 implements REQ-001

Relationship:
    CAP-001 contains FEAT-001
```

**Property with list value:**

```
Requirement:
    Identifier: REQ-002
    Name: "Supported Environments"
    Tags: [ "production", "staging", "development" ]
    Status: Approved
```

---

## 20.8 Visibility Declaration

Visibility may be declared on any Engineering Entity using the reserved attribute `Visibility`.

Valid values are:

`Private` — accessible only within the declaring scope.

`Internal` — accessible within the same Knowledge Package.

`Protected` — accessible to direct dependants.

`Public` — accessible to any conforming implementation.

`Restricted` — accessibility governed by explicit policy rules.

The default visibility is `Public` when the attribute is absent.

Example:

```
Component:
    Identifier: COMP-001
    Name: "Internal Cache"
    Visibility: Internal
    Status: Approved
```

---

End of Chapter 20 — Formal Grammar.

---

# Chapter 21

Closing Statement

The Grammar Specification defines the textual representation of Canonical Knowledge.

Every conforming parser shall implement this specification.

Every future language revision shall remain consistent with the constitutional principles established by the CSL standard.

End of Volume IV — Grammar.

End of Volume IV — Grammar.
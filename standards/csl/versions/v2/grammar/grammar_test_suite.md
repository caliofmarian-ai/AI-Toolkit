# CSL v2 — Grammar Test Suite

Identifier: CSL-002-TESTS  
Version: 2.0.0  
Status: Normative  
Classification: Canonical Standard  
Depends: csl_v2.ebnf, CSL-020_CONFORMANCE_TEST_SUITE_SPECIFICATION, CSL-021_ERROR_MODEL_SPECIFICATION

---

## 1. Purpose

This document is the canonical grammar test suite for CSL v2.  Every conforming
CSL v2 parser implementation MUST pass all tests in §2 (Valid) and §3 (Invalid).
Tests in §4 (Ambiguous) define the required disambiguation behaviour.

---

## 2. Notation

```
[TEST-ID]
Input:    <CSL v2 source text>
Expected: VALID | INVALID <diagnostic-code>
Notes:    <explanation>
```

Diagnostic codes follow CSL-021 / CSL-022 taxonomy:
- `CSL-LEX-NNN` — lexical errors
- `CSL-PARSE-NNN` — syntactic errors
- `CSL-SEM-NNN` — semantic errors (included here for completeness)

---

## 3. Valid Syntax Tests

### [GTEST-V-001] Minimal module

```csl
module ai-toolkit.test
version: 1.0.0
status: draft
```

Expected: VALID  
Notes: Minimum conformant module.

---

### [GTEST-V-002] Module with import

```csl
module ai-toolkit.test
version: 1.0.0
status: draft
import ai-toolkit.cdm.identity as identity version 2.0.0
```

Expected: VALID

---

### [GTEST-V-003] Minimal entity

```csl
module ai-toolkit.test
version: 1.0.0
status: draft

Entity:
    Identifier: ENT-001
    Name: "Test Entity"
    Status: approved
```

Expected: VALID

---

### [GTEST-V-004] Entity with all scalar attribute types

```csl
module ai-toolkit.test
version: 1.0.0
status: draft

Entity:
    Identifier: ENT-SCALARS
    Name: "Scalar Attributes Test"
    Status: approved
    StringAttr: "hello"
    IntAttr: 42
    NegInt: -7
    DecAttr: 3.14
    BoolTrue: true
    BoolFalse: false
    NullAttr: null
    DateAttr: 2026-08-07
    TsAttr: 2026-08-07T20:00:00Z
    DurAttr: 30d
    VerAttr: 2.0.0
```

Expected: VALID

---

### [GTEST-V-005] Entity with list value

```csl
module ai-toolkit.test
version: 1.0.0
status: draft

Entity:
    Identifier: ENT-LIST
    Name: "List Test"
    Status: approved
    Tags: [ "a", "b", "c" ]
```

Expected: VALID

---

### [GTEST-V-006] Entity with map value

```csl
module ai-toolkit.test
version: 1.0.0
status: draft

Entity:
    Identifier: ENT-MAP
    Name: "Map Test"
    Status: approved
    Config: { "key": "value", "count": 5 }
```

Expected: VALID

---

### [GTEST-V-007] Standalone relationship

```csl
module ai-toolkit.test
version: 1.0.0
status: draft

Entity:
    Identifier: ENT-A
    Name: "A"
    Status: approved

Entity:
    Identifier: ENT-B
    Name: "B"
    Status: approved

Relationship:
    ENT-A depends_on ENT-B
```

Expected: VALID

---

### [GTEST-V-008] Rule with when/then/otherwise

```csl
module ai-toolkit.test
version: 1.0.0
status: draft

rule RULE-001
    Name: "Test rule"
    Status: approved

    when:
        entity is approved

    then:
        has Identifier

    otherwise:
        warning "Entity lacks Identifier."
```

Expected: VALID

---

### [GTEST-V-009] Evidence declaration

```csl
module ai-toolkit.test
version: 1.0.0
status: draft

evidence EVD-001
    Name: "Test Evidence"
    Status: approved
    Type: TestResult
    RunDate: 2026-08-07
```

Expected: VALID

---

### [GTEST-V-010] Constraint declaration

```csl
module ai-toolkit.test
version: 1.0.0
status: draft

constraint CON-001
    Name: "Test Constraint"
    Status: approved

    Expression:
        entity has Identifier
```

Expected: VALID

---

### [GTEST-V-011] Policy declaration

```csl
module ai-toolkit.test
version: 1.0.0
status: draft

policy POL-001
    Name: "Test Policy"
    Status: approved
    rule: RULE-001
```

Expected: VALID

---

### [GTEST-V-012] Type declaration

```csl
module ai-toolkit.test
version: 1.0.0
status: draft

type TestType
    required Name: String
    optional Count: Integer
    optional Tags: List[String]
```

Expected: VALID

---

### [GTEST-V-013] Enum declaration

```csl
module ai-toolkit.test
version: 1.0.0
status: draft

enum Severity
    Low
    Medium
    High
    Critical
```

Expected: VALID

---

### [GTEST-V-014] Alias declaration

```csl
module ai-toolkit.test
version: 1.0.0
status: draft

alias EntityId = String
alias Tags     = List[String]
```

Expected: VALID

---

### [GTEST-V-015] Namespace block

```csl
module ai-toolkit.test
version: 1.0.0
status: draft

namespace core
    Entity:
        Identifier: ENT-NS
        Name: "Namespaced Entity"
        Status: draft
```

Expected: VALID

---

### [GTEST-V-016] Versioned entity reference

```csl
module ai-toolkit.test
version: 1.0.0
status: draft

Relationship:
    COMP-001@2.0.0 supersedes COMP-001@1.0.0
```

Expected: VALID

---

### [GTEST-V-017] Metadata block

```csl
module ai-toolkit.test
version: 1.0.0
status: draft

Entity:
    Identifier: ENT-META
    Name: "Metadata Test"
    Status: approved

    metadata
        Author: "Test"
        CreatedAt: 2026-01-01
```

Expected: VALID

---

### [GTEST-V-018] Compound AND condition

```csl
module ai-toolkit.test
version: 1.0.0
status: draft

rule RULE-AND
    Name: "Compound AND"
    Status: approved

    when:
        ENT-A is approved and ENT-B is approved

    then:
        emit "Both approved."
```

Expected: VALID

---

### [GTEST-V-019] NOT condition

```csl
module ai-toolkit.test
version: 1.0.0
status: draft

rule RULE-NOT
    Name: "NOT condition"
    Status: approved

    when:
        not entity is deprecated

    then:
        emit "Entity is active."
```

Expected: VALID

---

### [GTEST-V-020] Line comment preservation

```csl
module ai-toolkit.test
version: 1.0.0
status: draft

# This is a top-level comment
Entity:
    # This is an inline comment
    Identifier: ENT-COMMENT
    Name: "Comment Test"
    Status: approved
```

Expected: VALID  
Notes: Comments are discarded by the lexer; their presence MUST NOT affect parse result.

---

### [GTEST-V-021] All governance status values

```csl
module ai-toolkit.test
version: 1.0.0
status: draft

Entity:
    Identifier: ENT-DRAFT
    Name: "Draft Entity"
    Status: draft

Entity:
    Identifier: ENT-APPROVED
    Name: "Approved Entity"
    Status: approved

Entity:
    Identifier: ENT-DEPRECATED
    Name: "Deprecated Entity"
    Status: deprecated

Entity:
    Identifier: ENT-EXPERIMENTAL
    Name: "Experimental Entity"
    Status: experimental

Entity:
    Identifier: ENT-WITHDRAWN
    Name: "Withdrawn Entity"
    Status: withdrawn
```

Expected: VALID

---

### [GTEST-V-022] All visibility values

```csl
module ai-toolkit.test
version: 1.0.0
status: draft

Entity:
    Identifier: ENT-PUBLIC
    Name: "Public"
    Status: approved
    Visibility: public

Entity:
    Identifier: ENT-INTERNAL
    Name: "Internal"
    Status: approved
    Visibility: internal

Entity:
    Identifier: ENT-PRIVATE
    Name: "Private"
    Status: approved
    Visibility: private

Entity:
    Identifier: ENT-PROTECTED
    Name: "Protected"
    Status: approved
    Visibility: protected

Entity:
    Identifier: ENT-RESTRICTED
    Name: "Restricted"
    Status: approved
    Visibility: restricted
```

Expected: VALID

---

### [GTEST-V-023] All relationship verbs

```csl
module ai-toolkit.test
version: 1.0.0
status: draft

Relationship:
    A implements B
Relationship:
    A contains B
Relationship:
    A depends_on B
Relationship:
    A extends B
Relationship:
    A references B
Relationship:
    A requires B
Relationship:
    A owns B
Relationship:
    A approves B
Relationship:
    A tests B
Relationship:
    A validates B
Relationship:
    A generates B
Relationship:
    A deploys B
Relationship:
    A publishes B
Relationship:
    A consumes B
Relationship:
    A supports B
Relationship:
    A belongs_to B
Relationship:
    A traces_to B
Relationship:
    A supersedes B
```

Expected: VALID

---

## 4. Invalid Syntax Tests

### [GTEST-I-001] Missing module header

```csl
Entity:
    Identifier: ENT-001
    Name: "No module"
    Status: approved
```

Expected: INVALID CSL-PARSE-001  
Diagnostic: "Expected module declaration at start of compilation unit."

---

### [GTEST-I-002] Missing identifier after entity kind

```csl
module ai-toolkit.test
version: 1.0.0
status: draft

Entity:
    : COMP-001
    Name: "Bad"
    Status: approved
```

Expected: INVALID CSL-PARSE-001  
Diagnostic: "Expected IDENTIFIER for field name, found ':'."

---

### [GTEST-I-003] Keyword used as identifier

```csl
module ai-toolkit.test
version: 1.0.0
status: draft

Entity:
    Identifier: rule
    Name: "Keyword as identifier"
    Status: approved
```

Expected: INVALID CSL-PARSE-002  
Diagnostic: "'rule' is a reserved keyword and cannot be used as an identifier."

---

### [GTEST-I-004] Tab indentation

```csl
module ai-toolkit.test
version: 1.0.0
status: draft

Entity:
	Identifier: ENT-TAB
	Name: "Tab indented"
	Status: approved
```

Expected: INVALID CSL-LEX-001  
Diagnostic: "Tab character in indentation context; use 4 spaces per level."

---

### [GTEST-I-005] Mismatched DEDENT

```csl
module ai-toolkit.test
version: 1.0.0
status: draft

Entity:
    Identifier: ENT-001
      Name: "Bad indent"
    Status: approved
```

Expected: INVALID CSL-LEX-003  
Diagnostic: "Indentation does not align to any open INDENT level."

---

### [GTEST-I-006] Unknown relationship verb

```csl
module ai-toolkit.test
version: 1.0.0
status: draft

Relationship:
    ENT-A connects_to ENT-B
```

Expected: INVALID CSL-PARSE-003  
Diagnostic: "'connects_to' is not a recognised relationship verb."

---

### [GTEST-I-007] Unterminated string literal

```csl
module ai-toolkit.test
version: 1.0.0
status: draft

Entity:
    Identifier: ENT-001
    Name: "unterminated
    Status: approved
```

Expected: INVALID CSL-LEX-004  
Diagnostic: "Unterminated string literal; missing closing '\"'."

---

### [GTEST-I-008] Invalid version literal

```csl
module ai-toolkit.test
version: 2.0
status: draft
```

Expected: INVALID CSL-LEX-005  
Diagnostic: "Version literal '2.0' does not conform to MAJOR.MINOR.PATCH semver format."

---

### [GTEST-I-009] Rule with missing when clause

```csl
module ai-toolkit.test
version: 1.0.0
status: draft

rule RULE-BAD
    Name: "No when"
    Status: approved

    then:
        emit "ok."
```

Expected: INVALID CSL-PARSE-004  
Diagnostic: "Rule 'RULE-BAD' is missing required 'when:' clause."

---

### [GTEST-I-010] Rule with missing then clause

```csl
module ai-toolkit.test
version: 1.0.0
status: draft

rule RULE-BAD
    Name: "No then"
    Status: approved

    when:
        entity is approved
```

Expected: INVALID CSL-PARSE-005  
Diagnostic: "Rule 'RULE-BAD' is missing required 'then:' clause."

---

### [GTEST-I-011] Evidence with missing Type field

```csl
module ai-toolkit.test
version: 1.0.0
status: draft

evidence EVD-BAD
    Name: "No type field"
    Status: approved
```

Expected: INVALID CSL-PARSE-006  
Diagnostic: "Evidence 'EVD-BAD' is missing required 'Type:' field."

---

### [GTEST-I-012] Empty list value with trailing comma

```csl
module ai-toolkit.test
version: 1.0.0
status: draft

Entity:
    Identifier: ENT-001
    Name: "Trailing comma"
    Status: approved
    Tags: [ "a", ]
```

Expected: INVALID CSL-PARSE-007  
Diagnostic: "Trailing comma in list literal; remove the comma after the last element."

---

### [GTEST-I-013] Future reserved word used as identifier

```csl
module ai-toolkit.test
version: 1.0.0
status: draft

Entity:
    Identifier: interface
    Name: "Future reserved"
    Status: draft
```

Expected: INVALID CSL-PARSE-002  
Diagnostic: "'interface' is a future reserved word and cannot be used as an identifier."

---

### [GTEST-I-014] Invalid status value

```csl
module ai-toolkit.test
version: 1.0.0
status: published
```

Expected: INVALID CSL-PARSE-008  
Diagnostic: "'published' is not a valid governance status value."

---

## 5. Ambiguous Syntax Tests

CSL v2 grammar is designed to be unambiguous.  The following cases define the
required disambiguation rule where superficially similar syntax patterns exist.

### [GTEST-A-001] `Module` (entity-kind keyword) vs `module` (module keyword)

Source:
```csl
module ai-toolkit.test
version: 1.0.0
status: draft

Module:
    Identifier: MOD-001
    Name: "A module entity"
    Status: approved
```

Expected: VALID  
Disambiguation: `module` (lowercase) at the start of the compilation unit is
the module-level keyword.  `Module:` (capitalised) inside a module body is the
entity-kind keyword.  The lexer MUST emit them as distinct token types.

---

### [GTEST-A-002] Attribute field vs entity-kind declaration — same indentation

Source:
```csl
module ai-toolkit.test
version: 1.0.0
status: draft

Component:
    Identifier: COMP-001
    Name: "Component"
    Status: approved
    Policy: POL-001
```

Expected: VALID  
Disambiguation: `Policy: POL-001` at the entity body indentation level is an
attribute field (IDENTIFIER ":" value) where the value is a QNAME.  It is NOT
a nested Policy entity declaration because the value on the same line is not
followed by NEWLINE + INDENT.  A nested entity declaration always ends its
first line with a bare `:` followed by NEWLINE + INDENT.

---

### [GTEST-A-003] Rule reference in policy vs inline rule

Source:
```csl
module ai-toolkit.test
version: 1.0.0
status: draft

policy POL-001
    Name: "Policy"
    Status: approved
    rule: RULE-001
```

Expected: VALID  
Disambiguation: `rule: RULE-001` is a `policy_rule_ref` production (KEYWORD_RULE
":" entity_ref NEWLINE).  It is NOT a `rule_decl` because it occurs inside a
policy body, lacks an IDENTIFIER immediately after `rule`, and does not contain
`when:` / `then:` clauses.

---

### [GTEST-A-004] OR condition precedence

Source (within a rule when-clause):
```
A is approved or B is approved and C is approved
```

Expected parse (AND binds tighter than OR):
```
A is approved OR (B is approved AND C is approved)
```

Disambiguation: CSL v2 grammar applies standard logic precedence:
NOT > AND > OR.  A compound condition with mixed AND and OR operators MUST be
parenthesised by the author if a non-default precedence is intended.  Parsers
MUST apply this precedence rule deterministically.

---

## 6. Expected Diagnostics Reference

| Code            | Category | Description                                                  |
|-----------------|----------|--------------------------------------------------------------|
| CSL-LEX-000     | Lexical   | Unrecognised input character(s)                              |
| CSL-LEX-001     | Lexical   | Tab in indentation context                                   |
| CSL-LEX-002     | Lexical   | Mixed spaces and tabs on same line                           |
| CSL-LEX-003     | Lexical   | DEDENT does not align to open INDENT level                   |
| CSL-LEX-004     | Lexical   | Unterminated string literal                                  |
| CSL-LEX-005     | Lexical   | Malformed version literal                                    |
| CSL-PARSE-001   | Syntactic | Missing or misplaced token                                   |
| CSL-PARSE-002   | Syntactic | Reserved keyword / future reserved word used as identifier   |
| CSL-PARSE-003   | Syntactic | Unrecognised relationship verb                               |
| CSL-PARSE-004   | Syntactic | Rule missing `when:` clause                                  |
| CSL-PARSE-005   | Syntactic | Rule missing `then:` clause                                  |
| CSL-PARSE-006   | Syntactic | Evidence missing `Type:` field                               |
| CSL-PARSE-007   | Syntactic | Trailing comma in list or map literal                        |
| CSL-PARSE-008   | Syntactic | Invalid governance status value                              |

---

## 7. Conformance Levels

Implementations MUST declare which test tier they claim:

| Level | Coverage required                                   |
|-------|-----------------------------------------------------|
| L1    | All §3 Valid tests pass                             |
| L2    | L1 + All §4 Invalid tests produce correct diagnostics |
| L3    | L2 + All §5 Ambiguous tests produce correct ASTs   |

Full conformance requires L3.

---

*End of grammar_test_suite.md — CSL-002-TESTS v2.0.0*

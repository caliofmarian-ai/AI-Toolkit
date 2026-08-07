# CSL v2 — Parser Examples

Identifier: CSL-002-PARSER  
Version: 2.0.0  
Status: Normative  
Classification: Canonical Standard  
Depends: csl_v2.ebnf, CSL-012_PARSER_SPECIFICATION, CSL-014_AST_SPECIFICATION

---

## 1. Purpose

This document demonstrates how a conforming CSL v2 parser interprets every
canonical construct.  For each example, the source text is shown alongside the
expected Abstract Syntax Tree (AST) structure.  The AST notation uses a
simplified indented s-expression form:

```
(NodeType  field=value  field=value
    (ChildNodeType  ...)
    ...)
```

All node types correspond to §3 of CSL-014_AST_SPECIFICATION.

---

## 2. Module Header

### Source

```csl
module ai-toolkit.example
version: 2.0.0
status: approved
```

### AST

```
(Module
    name=(QName "ai-toolkit" "example")
    version=(VersionLit major=2 minor=0 patch=0)
    status=APPROVED)
```

---

## 3. Import Declaration

### Source

```csl
import ai-toolkit.cdm.identity as identity version 2.0.0
```

### AST

```
(ImportDecl
    path=(QName "ai-toolkit" "cdm" "identity")
    alias=(Identifier "identity")
    version=(VersionLit major=2 minor=0 patch=0))
```

---

## 4. Entity Declaration

### Source

```csl
Component:
    Identifier: COMP-001
    Name: "Authentication Service"
    Version: 1.3.0
    Status: approved
    Visibility: internal
    Tags: [ "auth", "security" ]
```

### AST

```
(EntityDecl
    kind=COMPONENT
    name=(Identifier "COMP-001")
    fields=[
        (IdentifierField value=(Identifier "COMP-001"))
        (NameField value=(StringLit "Authentication Service"))
        (VersionField value=(VersionLit major=1 minor=3 patch=0))
        (StatusField value=APPROVED)
        (VisibilityField value=INTERNAL)
        (AttributeField
            key=(Identifier "Tags")
            value=(ListLit [
                (StringLit "auth")
                (StringLit "security")
            ]))
    ])
```

---

## 5. Relationship Declaration

### Source

```csl
Relationship:
    FEAT-001 implements REQ-001
    Strength: "mandatory"
```

### AST

```
(RelationshipDecl
    source=(EntityRef name=(QName "FEAT-001") version=null)
    verb=IMPLEMENTS
    target=(EntityRef name=(QName "REQ-001") version=null)
    attributes=[
        (RelAttr key=(Identifier "Strength") value=(StringLit "mandatory"))
    ])
```

### Source (versioned reference)

```csl
Relationship:
    COMP-001@1.3.0 supersedes COMP-001@1.2.0
```

### AST

```
(RelationshipDecl
    source=(EntityRef name=(QName "COMP-001") version=(VersionLit major=1 minor=3 patch=0))
    verb=SUPERSEDES
    target=(EntityRef name=(QName "COMP-001") version=(VersionLit major=1 minor=2 patch=0))
    attributes=[])
```

---

## 6. Rule Declaration

### Source

```csl
rule RULE-001
    Name: "Approved entities require approval record"
    Status: approved

    when:
        entity is approved

    then:
        has Approval

    otherwise:
        error "Missing approval record."
```

### AST

```
(RuleDecl
    name=(Identifier "RULE-001")
    nameField=(StringLit "Approved entities require approval record")
    status=APPROVED
    when=(ConditionExpr
        term=(ConditionAtom
            ref=(EntityRef name=(QName "entity"))
            predicate=(IsStatus status=APPROVED)))
    then=(ActionList [
        (ActionHas attr=(Identifier "Approval"))
    ])
    otherwise=(ActionList [
        (ActionError msg=(StringLit "Missing approval record."))
    ]))
```

---

## 7. Evidence Declaration

### Source

```csl
evidence EVD-001
    Name: "Unit Test Results"
    Status: approved
    Type: TestResult
    RunDate: 2026-08-07
    PassRate: "100%"
```

### AST

```
(EvidenceDecl
    name=(Identifier "EVD-001")
    nameField=(StringLit "Unit Test Results")
    status=APPROVED
    evidenceType=(Identifier "TestResult")
    attributes=[
        (EvidenceAttr key=(Identifier "RunDate") value=(DateLit 2026-08-07))
        (EvidenceAttr key=(Identifier "PassRate") value=(StringLit "100%"))
    ])
```

---

## 8. Constraint Declaration

### Source

```csl
constraint CON-001
    Name: "Entity must have Identifier"
    Status: approved
    Description: "All entities require an Identifier field."

    Expression:
        entity has Identifier
```

### AST

```
(ConstraintDecl
    name=(Identifier "CON-001")
    nameField=(StringLit "Entity must have Identifier")
    status=APPROVED
    description=(StringLit "All entities require an Identifier field.")
    expression=(ConditionExpr
        term=(ConditionAtom
            ref=(EntityRef name=(QName "entity"))
            predicate=(HasAttr attr=(Identifier "Identifier")))))
```

---

## 9. Policy Declaration

### Source

```csl
policy POL-001
    Name: "Release Gate Policy"
    Status: approved
    rule: RULE-001
    rule: RULE-002
    Scope: "release"
```

### AST

```
(PolicyDecl
    name=(Identifier "POL-001")
    nameField=(StringLit "Release Gate Policy")
    status=APPROVED
    rules=[
        (PolicyRuleRef ref=(EntityRef name=(QName "RULE-001")))
        (PolicyRuleRef ref=(EntityRef name=(QName "RULE-002")))
    ]
    attributes=[
        (PolicyAttr key=(Identifier "Scope") value=(StringLit "release"))
    ])
```

---

## 10. Type Declaration

### Source

```csl
type ContactInfo
    required Name:  String
    optional Phone: String
```

### AST

```
(TypeDecl
    name=(Identifier "ContactInfo")
    parent=null
    fields=[
        (TypeField
            modifier=REQUIRED
            name=(Identifier "Name")
            typeAnnotation=(ScalarType STRING))
        (TypeField
            modifier=OPTIONAL
            name=(Identifier "Phone")
            typeAnnotation=(ScalarType STRING))
    ])
```

---

## 11. Enum Declaration

### Source

```csl
enum RiskLevel
    Low
    Medium
    High
    Critical
```

### AST

```
(EnumDecl
    name=(Identifier "RiskLevel")
    values=[
        (Identifier "Low")
        (Identifier "Medium")
        (Identifier "High")
        (Identifier "Critical")
    ])
```

---

## 12. Metadata Block

### Source

```csl
metadata
    CreatedAt: 2026-01-01
    Author: "AI CTO"
    ReviewCycle: 90d
```

### AST

```
(MetadataBlock
    fields=[
        (MetadataField key=(Identifier "CreatedAt") value=(DateLit 2026-01-01))
        (MetadataField key=(Identifier "Author")    value=(StringLit "AI CTO"))
        (MetadataField key=(Identifier "ReviewCycle") value=(DurationLit amount=90 unit=d))
    ])
```

---

## 13. Compound Condition Expression

### Source (within a rule when-clause)

```
COMP-001 has RiskLevel and COMP-001 is approved
```

### AST

```
(ConditionExpr
    op=AND
    left=(ConditionAtom
        ref=(EntityRef name=(QName "COMP-001"))
        predicate=(HasAttr attr=(Identifier "RiskLevel")))
    right=(ConditionAtom
        ref=(EntityRef name=(QName "COMP-001"))
        predicate=(IsStatus status=APPROVED)))
```

---

## 14. Value Literals

### Source → AST mapping

| Source text             | AST Node                                      |
|-------------------------|-----------------------------------------------|
| `"hello world"`         | `(StringLit "hello world")`                   |
| `42`                    | `(IntLit 42)`                                 |
| `-7`                    | `(IntLit -7)`                                 |
| `3.14`                  | `(DecimalLit 3.14)`                           |
| `true`                  | `(BoolLit true)`                              |
| `false`                 | `(BoolLit false)`                             |
| `null`                  | `(NullLit)`                                   |
| `2026-08-07`            | `(DateLit 2026 8 7)`                          |
| `2026-08-07T20:00:00Z`  | `(TimestampLit 2026 8 7 20 0 0 UTC)`          |
| `30d`                   | `(DurationLit 30 d)`                          |
| `2.0.0`                 | `(VersionLit 2 0 0 null null)`                |
| `[ "a", "b" ]`          | `(ListLit [(StringLit "a")(StringLit "b")])`   |
| `{ "k": 1 }`            | `(MapLit [(MapEntry (StringLit "k")(IntLit 1))])` |
| `core.security.Policy`  | `(QName "core" "security" "Policy")`          |

---

## 15. Parser Error Recovery Examples

When the parser encounters an invalid token, it MUST:

1. Emit a diagnostic with rule ID and source span (CSL-022).
2. Attempt to recover by advancing to the next statement boundary (NEWLINE at
   the current indentation level or DEDENT).
3. Continue parsing from the recovery point.

### Example: missing IDENTIFIER after entity keyword

Source:
```
Component:
    : COMP-001
```

Parser action:
- Emits `CSL-PARSE-001`: expected IDENTIFIER at line 2, column 5.
- Recovers at line 2 NEWLINE.
- Continues parsing body.

---

*End of parser_examples.md — CSL-002-PARSER v2.0.0*

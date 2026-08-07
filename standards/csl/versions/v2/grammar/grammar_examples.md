# CSL v2 — Grammar Examples

Identifier: CSL-002-EXAMPLES  
Version: 2.0.0  
Status: Normative  
Classification: Canonical Standard  
Depends: csl_v2.ebnf, reserved_keywords.md

---

## 1. Purpose

This document provides canonical CSL v2 source examples for every major
language construct.  Each example is normative: it defines the expected textual
representation of the corresponding construct and SHALL parse without error
under a conforming CSL v2 parser.

---

## 2. Module Declaration

A module is the top-level compilation unit.

```csl
module ai-toolkit.core

version: 2.0.0
status: approved
namespace: ai-toolkit.core

# Import the CDM identity types
import ai-toolkit.cdm.identity as identity version 2.0.0
import ai-toolkit.cdm.governance as gov version 2.0.0
```

---

## 3. Namespace Block

Namespaces scope declarations within a module.

```csl
module ai-toolkit.security

namespace security
    Entity:
        Identifier: SEC-NS-001
        Name: "Security Namespace Root"
        Status: approved

    namespace policies
        Policy:
            Identifier: POL-001
            Name: "Zero-Trust Access Policy"
            Status: approved
```

---

## 4. Entity Declaration

### 4.1 Minimal Entity

```csl
Entity:
    Identifier: ENT-001
    Name: "Canonical Engineering Entity"
    Status: approved
```

### 4.2 Full Entity with All Optional Fields

```csl
Component:
    Identifier: COMP-001
    Name: "Authentication Service"
    Version: 1.3.0
    Status: approved
    Classification: "Internal"
    Owner: "Platform Team"
    Visibility: internal
    Description: "Handles credential validation and session management."
    Tags: [ "auth", "security", "platform" ]

    metadata
        CreatedAt: 2026-01-15
        LastModified: 2026-08-07T20:00:00Z
        ReviewCycle: 90d
```

### 4.3 Project Declaration

```csl
Project:
    Identifier: AI-TOOLKIT
    Name: "AI-Toolkit Platform"
    Version: 2.0.0
    Status: approved
    Description: "Canonical engineering knowledge platform for AI-assisted development."
    Owner: "AI CTO"
    Tags: [ "canonical", "governance", "ai-toolkit" ]
```

### 4.4 Capability and Feature

```csl
Capability:
    Identifier: CAP-AUTH
    Name: "User Authentication"
    Status: approved

Feature:
    Identifier: FEAT-LOGIN
    Name: "Password Login"
    Status: approved

Feature:
    Identifier: FEAT-SSO
    Name: "Single Sign-On"
    Status: approved
```

---

## 5. Relationship Declaration

### 5.1 Standalone Relationship Block

```csl
Relationship:
    FEAT-LOGIN implements REQ-CRED-001
    Strength: "mandatory"
    Evidence: "TEST-AUTH-042"

Relationship:
    CAP-AUTH contains FEAT-LOGIN

Relationship:
    CAP-AUTH contains FEAT-SSO
```

### 5.2 Inline Relationship within Entity

```csl
Component:
    Identifier: COMP-CACHE
    Name: "Redis Cache Layer"
    Status: approved

    Relationship:
        COMP-CACHE depends_on ENV-REDIS-PROD
```

### 5.3 Versioned Entity Reference

```csl
Relationship:
    COMP-001@1.3.0 supersedes COMP-001@1.2.0
```

---

## 6. Rule Declaration

```csl
rule RULE-APPROVAL-REQUIRED

    Name: "All approved entities require an approval record"
    Status: approved

    when:
        entity is approved

    then:
        has Approval

    otherwise:
        error "Entity claims approved status but lacks an Approval record."
```

### 6.1 Compound Condition Rule

```csl
rule RULE-SECURITY-CLASSIFICATION

    Name: "High-risk components must be restricted"
    Status: approved

    when:
        COMP-001 has RiskLevel
        and COMP-001 is approved

    then:
        emit "Verify restricted visibility for high-risk component."
```

---

## 7. Evidence Declaration

```csl
evidence EVD-TEST-001

    Name: "Authentication Unit Test Results"
    Status: approved
    Type: TestResult

    TestSuite: "auth-unit-suite"
    PassRate: "100%"
    RunDate: 2026-08-07
    Artifact: "ci/builds/8821/test-report.xml"
```

---

## 8. Constraint Declaration

```csl
constraint CON-IDENTIFIER-FORMAT

    Name: "Identifier must follow canonical format"
    Status: approved
    Description: "Entity identifiers must be uppercase alphanumeric with hyphens."

    Expression:
        entity has Identifier

```

---

## 9. Policy Declaration

```csl
policy POL-RELEASE-GATE

    Name: "Release Gate Policy"
    Status: approved
    Description: "All artifacts must pass quality and security gates before release."

    rule: RULE-APPROVAL-REQUIRED
    rule: RULE-SECURITY-CLASSIFICATION

    Scope: "release"
    Authority: "AI CTO"
```

---

## 10. Type Declarations

### 10.1 Structured Type

```csl
type ContactInfo
    required Name: String
    required Email: String
    optional Phone: String
    optional Organization: String
```

### 10.2 Type Inheritance

```csl
type EngineeringArtifact
    required Identifier: String
    required Version: Version
    required Status: String

type CanonicalDocument extends EngineeringArtifact
    required Classification: String
    optional Owner: String
    optional Tags: List[String]
```

### 10.3 Enumeration

```csl
enum RiskLevel
    Low
    Medium
    High
    Critical
```

### 10.4 Type Alias

```csl
alias ArtifactId = String
alias Tags       = List[String]
alias OwnerRef   = Ref[Provider]
```

---

## 11. Metadata Block

```csl
Project:
    Identifier: AI-TOOLKIT
    Name: "AI-Toolkit Platform"
    Status: approved

    metadata
        CreatedAt: 2025-01-01
        ModifiedAt: 2026-08-07T20:00:00Z
        Author: "AI CTO"
        ReviewBoard: "Engineering Council"
        ExpiresAfter: 365d
        ApprovalRef: "APPROVAL-2026-001"
```

---

## 12. Import Declaration

```csl
module ai-toolkit.runtime

# Named import
import ai-toolkit.cdm.identity as identity version 2.0.0

# Path import without alias
import "standards/cdm/versions/v2/CDM-001_IDENTITY.csl"

# Versioned import with alias
import ai-toolkit.governance.policies as gov version 2.0.0
```

---

## 13. Complete Module Example

```csl
module ai-toolkit.example

version: 2.0.0
status: approved
namespace: ai-toolkit.example

import ai-toolkit.cdm.identity as identity version 2.0.0

Project:
    Identifier: EXAMPLE-PROJECT
    Name: "CSL v2 Example Project"
    Version: 1.0.0
    Status: approved
    Owner: "Engineering Team"
    Tags: [ "example", "canonical", "v2" ]

Capability:
    Identifier: CAP-001
    Name: "Data Processing"
    Status: approved

Feature:
    Identifier: FEAT-001
    Name: "Batch Ingestion"
    Status: approved

Requirement:
    Identifier: REQ-001
    Name: "System shall process 10,000 records per second"
    Status: approved

Relationship:
    CAP-001 contains FEAT-001

Relationship:
    FEAT-001 implements REQ-001

rule RULE-PERF-001
    Name: "Performance requirement traceability"
    Status: approved

    when:
        FEAT-001 is approved

    then:
        has REQ-001

evidence EVD-001
    Name: "Load Test Results"
    Status: approved
    Type: TestResult
    RunDate: 2026-08-01
    PassRate: "100%"

policy POL-001
    Name: "Feature Release Policy"
    Status: approved
    rule: RULE-PERF-001
```

---

*End of grammar_examples.md — CSL-002-EXAMPLES v2.0.0*

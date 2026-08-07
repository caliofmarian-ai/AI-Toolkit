# CSL v2 — Reserved Keywords

Identifier: CSL-002-KEYWORDS  
Version: 2.0.0  
Status: Normative  
Classification: Canonical Standard  
Depends: CSL-001_ENGINEERING_ALPHABET, CSL-002_GRAMMAR, csl_v2.ebnf §2

---

## 1. Purpose

This document is the authoritative taxonomy of every reserved word in CSL v2.
No conforming implementation SHALL accept a reserved word as a user-defined
identifier.  Future additions require an approved RFC and a minor or major
version increment.

---

## 2. Keyword Categories

### 2.1 Module-Level Keywords

| Keyword     | Role                                               |
|-------------|----------------------------------------------------|
| `module`    | Declares the top-level compilation unit            |
| `namespace` | Introduces a named scope within a module           |
| `import`    | Imports declarations from another module           |
| `export`    | Makes a declaration visible outside the module     |
| `as`        | Alias binding in import / export                   |
| `from`      | Source path qualifier in import                    |
| `version`   | Declares the module or entity version              |
| `status`    | Declares the governance lifecycle status           |
| `metadata`  | Introduces a metadata sub-block                    |

### 2.2 Declaration Keywords

| Keyword        | Role                                             |
|----------------|--------------------------------------------------|
| `entity`       | Generic entity declaration                       |
| `relationship` | Declares an explicit relationship block          |
| `rule`         | Declares a deterministic logic rule              |
| `evidence`     | Declares an evidence record                      |
| `constraint`   | Declares a standalone constraint                 |
| `policy`       | Declares a governance policy                     |
| `type`         | Declares a structured type                       |
| `enum`         | Declares an enumeration                          |
| `alias`        | Declares a type alias                            |

### 2.3 Entity-Kind Keywords (Canonical Vocabulary)

These words act as shorthand entity kinds.  They share keyword status — they
MUST NOT be used as identifiers — but they resolve to typed entity declarations
in the AST.

| Keyword       | Canonical Entity Kind                              |
|---------------|----------------------------------------------------|
| `Project`     | Highest-level engineering container                |
| `Capability`  | Major engineering ability                          |
| `Feature`     | Concrete engineering function                      |
| `Requirement` | Engineering objective                              |
| `Decision`    | Engineering decision with rationale                |
| `Constraint`  | Validation rule (inline form)                      |
| `Policy`      | Governance rule (inline form)                      |
| `Rule`        | Deterministic logic rule (inline form)             |
| `Risk`        | Engineering threat                                 |
| `Issue`       | Work item                                          |
| `Epic`        | Large engineering objective                        |
| `Milestone`   | Measurable engineering objective                   |
| `Task`        | Executable engineering activity                    |
| `Component`   | Logical implementation unit                        |
| `Module`      | Cohesive implementation grouping                   |
| `Service`     | Independently deployable capability                |
| `API`         | Formal communication interface                     |
| `Entity`      | Generic uniquely identifiable engineering object   |
| `Relationship`| Semantic connection (standalone block form)        |
| `Generator`   | Artifact-generating component                      |
| `Validator`   | Validation component                               |
| `Compiler`    | Compiler component description                     |
| `Runtime`     | Execution environment description                  |
| `Knowledge`   | Custom engineering concept grouping                |
| `Reference`   | Traceability link                                  |
| `Approval`    | Governance authorization record                    |
| `Deployment`  | Artifact publication record                        |
| `Environment` | Execution context description                      |
| `Provider`    | External capability provider                       |
| `Model`       | Abstract engineering representation                |
| `Prompt`      | AI provider input configuration                    |

### 2.4 Modifier Keywords

| Keyword      | Role                                                |
|--------------|-----------------------------------------------------|
| `extends`    | Type inheritance                                    |
| `implements` | Relationship verb: satisfies an interface/contract  |
| `required`   | Field modifier: value must be present               |
| `optional`   | Field modifier: value may be absent                 |
| `readonly`   | Field modifier: value cannot be mutated after init  |
| `unique`     | Field modifier: value must be unique within scope   |

### 2.5 Relationship Verb Keywords

| Keyword      | Semantics                                          |
|--------------|----------------------------------------------------|
| `implements` | Source satisfies contract of target                |
| `contains`   | Source is a parent container of target             |
| `depends_on` | Source has a runtime/build dependency on target    |
| `extends`    | Source is a specialisation of target               |
| `references` | Source cross-references target (informational)     |
| `requires`   | Source mandates the existence/state of target      |
| `owns`       | Source has authoritative ownership of target       |
| `approves`   | Source provides governance approval of target      |
| `tests`      | Source validates the behaviour of target           |
| `validates`  | Source formally validates target                   |
| `generates`  | Source produces target as an artifact              |
| `deploys`    | Source publishes target to an environment          |
| `publishes`  | Source makes target externally available           |
| `consumes`   | Source uses output of target                       |
| `supports`   | Source provides capability support for target      |
| `belongs_to` | Source is a member of target                       |
| `traces_to`  | Source provides traceability to target             |
| `supersedes` | Source replaces a deprecated target                |

### 2.6 Rule and Logic Keywords

| Keyword     | Role                                               |
|-------------|----------------------------------------------------|
| `when`      | Condition clause in a rule                         |
| `then`      | Consequence clause in a rule                       |
| `otherwise` | Default/fallback consequence clause                |
| `and`       | Logical conjunction                                |
| `or`        | Logical disjunction                                |
| `not`       | Logical negation                                   |
| `is`        | Identity / status predicate                        |
| `in`        | Membership predicate                               |
| `has`       | Attribute existence predicate                      |

### 2.7 Governance Status Keywords

| Keyword        | Lifecycle State                                  |
|----------------|--------------------------------------------------|
| `approved`     | Ratified and in effect                           |
| `draft`        | Under development, not yet ratified              |
| `deprecated`   | Superseded; removal planned                      |
| `experimental` | Subject to change without RFC                    |
| `withdrawn`    | Removed from active use                          |

### 2.8 Visibility Keywords

| Keyword      | Scope of Access                                    |
|--------------|----------------------------------------------------|
| `public`     | Accessible to any conforming implementation        |
| `internal`   | Accessible within the same knowledge package       |
| `private`    | Accessible only within the declaring scope         |
| `protected`  | Accessible to direct dependants                    |
| `restricted` | Accessibility governed by explicit policy rules    |

### 2.9 Rule Action Keywords

| Keyword   | Role                                               |
|-----------|----------------------------------------------------|
| `emit`    | Emit an informational message from a rule action   |
| `error`   | Emit a compilation error from a rule action        |
| `warning` | Emit a warning from a rule action                  |
| `info`    | Emit an informational diagnostic from a rule action|

### 2.10 Built-In Type Keywords

| Keyword     | Type                               |
|-------------|------------------------------------|
| `String`    | UTF-8 text                         |
| `Integer`   | Signed integer                     |
| `Decimal`   | Floating-point decimal             |
| `Boolean`   | `true` / `false`                   |
| `Date`      | ISO 8601 date                      |
| `Timestamp` | ISO 8601 date-time with timezone   |
| `Duration`  | Time interval                      |
| `Version`   | Semantic version (semver)          |
| `Null`      | Absence of value                   |
| `Any`       | Unconstrained type                 |
| `List`      | Ordered collection                 |
| `Set`       | Unordered unique collection        |
| `Map`       | Key-value collection               |
| `Optional`  | Nullable wrapper                   |
| `Ref`       | Cross-entity reference             |

---

## 3. Future Reserved Words

The following identifiers are reserved for planned future use.  They MUST NOT
be used as user-defined identifiers in CSL v2.  They carry no current semantics
but will be assigned semantics in a future minor or major version.

| Word          | Anticipated Use                              |
|---------------|----------------------------------------------|
| `interface`   | Formal interface declaration                 |
| `abstract`    | Abstract entity modifier                     |
| `final`       | Non-extensible entity modifier               |
| `sealed`      | Closed inheritance hierarchy                 |
| `override`    | Explicit override declaration                |
| `default`     | Default value / clause marker                |
| `async`       | Asynchronous execution context               |
| `await`       | Async suspension point                       |
| `match`       | Pattern-matching expression                  |
| `case`        | Pattern-match branch                         |
| `let`         | Local binding                                |
| `const`       | Immutable local binding                      |
| `for`         | Iteration expression                         |
| `return`      | Value return in rule consequence             |
| `yield`       | Generator yield                              |
| `with`        | Scoped context introduction                  |
| `using`       | Resource-scoped binding                      |
| `assert`      | Inline assertion                             |
| `trace`       | Traceability annotation                      |
| `audit`       | Audit annotation                             |
| `signal`      | Event emission                               |
| `on`          | Event handler                                |
| `trigger`     | Trigger declaration                          |

---

## 4. Identifier vs. Keyword Resolution

The lexer applies the following precedence rule:

> If the scanned token exactly matches (case-sensitive) any reserved keyword
> or future reserved word in this document, it is emitted as that keyword
> token.  Otherwise it is emitted as an IDENTIFIER token.

Keywords are case-sensitive.  `Module` (entity-kind keyword) ≠ `module`
(module-level keyword).

---

## 5. Governance

Additions to any keyword table require:

1. An approved RFC (RFC-0001 process).
2. A minor version increment for backward-compatible additions.
3. A major version increment for removals or semantic changes.

Silent keyword changes are prohibited.

---

*End of reserved_keywords.md — CSL-002-KEYWORDS v2.0.0*

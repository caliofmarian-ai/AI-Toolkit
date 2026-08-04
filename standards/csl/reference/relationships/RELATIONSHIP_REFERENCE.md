# Canonical Specification Language (CSL)

# RELATIONSHIP REFERENCE

Version: Draft 1.0

Status: Normative

Classification: Reference

---

# Purpose

This document defines the canonical semantic relationships recognized by the Canonical Specification Language.

Relationships express engineering meaning between Engineering Entities.

Relationships are independent of implementation technology.

Every conforming implementation shall preserve relationship semantics.

---

# contains

The source Entity structurally contains the target Entity.

Examples:

Project contains Capability.

Capability contains Feature.

Knowledge Package contains Document.

Containment defines structural organization.

---

# depends_on

The source Entity requires the target Entity.

Dependencies influence:

Compilation

Validation

Execution

Planning

Mandatory dependencies shall be satisfied before execution.

---

# implements

The source Entity implements the engineering intent defined by the target Entity.

Examples:

Component implements Feature.

Feature implements Requirement.

Service implements Capability.

---

# extends

The source Entity extends the behavior or definition of the target Entity.

Extension preserves compatibility.

Extension shall never redefine the original semantic meaning.

---

# references

The source Entity creates a semantic reference to the target Entity.

References preserve traceability.

References do not imply ownership.

---

# requires

The source Entity requires the existence of the target Entity.

Requirements express mandatory engineering conditions.

---

# owns

The source Entity owns the target Entity.

Ownership identifies engineering responsibility.

Ownership does not imply implementation.

---

# approves

The source Entity authorizes the target Entity.

Approval establishes governance.

Approval shall remain auditable.

---

# validates

The source Entity validates the correctness of the target Entity.

Validators perform deterministic verification.

Validation never modifies engineering meaning.

---

# tests

The source Entity verifies the operational behavior of the target Entity.

Testing confirms implementation correctness.

Testing supports engineering confidence.

---

# generates

The source Entity produces the target Entity.

Examples:

Generator generates Documentation.

Compiler generates Universal Engineering Model.

Generator generates Source Code.

Generation preserves provenance.

---

# deploys

The source Entity publishes the target Entity into an execution environment.

Deployment occurs after successful validation.

Deployment never modifies Canonical Knowledge.

---

# publishes

The source Entity makes the target Entity available for consumption.

Publishing may include:

Documentation

Packages

Releases

Artifacts

---

# consumes

The source Entity uses the target Entity as input.

Examples:

Compiler consumes Canonical Knowledge.

Generator consumes Universal Engineering Model.

Validator consumes Engineering Objects.

Consumption never modifies the source.

---

# supports

The source Entity provides capabilities to the target Entity.

Support relationships describe engineering assistance.

Support shall remain implementation independent.

---

# belongs_to

The source Entity is a member of the target Entity.

Membership defines engineering organization.

Belonging does not imply ownership.

---

# Cardinality

Relationships support:

One-to-One

One-to-Many

Many-to-One

Many-to-Many

Cardinality shall be explicitly validated.

---

# Direction

Relationships are directional unless explicitly declared bidirectional.

Direction influences semantic interpretation.

---

# Lifecycle

Relationships progress through:

Draft

Review

Approved

Canonical

Deprecated

Archived

Lifecycle transitions shall remain traceable.

---

# Validation

Relationship validation shall verify:

Identity

Type

Direction

Cardinality

Dependencies

Lifecycle

Constraints

Reference Integrity

Validation failures invalidate the affected Engineering Knowledge.

---

# Extensibility

Future relationship types may be introduced through approved RFCs.

New relationships shall preserve compatibility with existing engineering semantics.

---

# Closing Statement

Relationship definitions establish the semantic links connecting Engineering Entities throughout the Canonical Specification Language.

Together with Engineering Entities, these relationships form the semantic graph represented by the Universal Engineering Model.

End of Relationship Reference.
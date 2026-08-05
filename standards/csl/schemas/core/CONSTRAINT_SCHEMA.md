# Canonical Specification Language (CSL)

# CONSTRAINT SCHEMA

Version: 1.0.0

Status: Normative

Classification: Core Schema

---

# 1. Purpose

The Constraint Schema defines the canonical representation of engineering constraints.

Constraints preserve engineering correctness.

Constraints define the rules that Engineering Entities, Relationships and Properties shall satisfy.

Constraints are executable engineering knowledge.

---

# 2. Schema Definition

Every Constraint shall contain:

Constraint Identifier

Constraint Name

Constraint Type

Target Scope

Validation Rule

Severity

Lifecycle

Metadata

---

# 3. Required Fields

Identifier

Name

Type

Target

Rule

Severity

Status

Version

Created

Modified

---

# 4. Optional Fields

Description

Category

Examples

Documentation

Tags

References

Audit Metadata

Notes

---

# 5. Constraint Categories

Supported categories include:

Structural

Semantic

Relationship

Property

Identity

Reference

Dependency

Lifecycle

Visibility

Governance

Security

Safety

Future specifications may introduce additional categories.

---

# 6. Severity Levels

Constraint severity shall be one of:

Information

Warning

Error

Critical

Fatal

Severity determines compiler behavior.

---

# 7. Target Scope

Constraints may apply to:

Entities

Relationships

Properties

Documents

Knowledge Packages

Universal Engineering Model

Compiler Output

Generators

Validation Rules

---

# 8. Validation Rules

Validation rules shall be deterministic.

Validation shall verify:

Presence

Uniqueness

Cardinality

Reference Integrity

Type Compatibility

Lifecycle Consistency

Dependency Consistency

Governance Compliance

Safety Compliance

---

# 9. Evaluation

Constraint evaluation shall produce one of:

Passed

Warning

Failed

Not Applicable

Evaluation results shall be reproducible.

---

# 10. Constraint Lifecycle

Every Constraint progresses through:

Draft

Review

Approved

Canonical

Deprecated

Archived

Lifecycle transitions shall remain traceable.

---

# 11. Provenance

Every Constraint shall preserve:

Origin

Author

Approval

Revision History

Compiler Version

CSL Version

Audit History

Provenance is immutable.

---

# 12. Compatibility

Future schema revisions shall preserve compatibility whenever technically feasible.

Breaking changes require formal approval.

---

# 13. Extensibility

Future Constraint Types,

Validation Rules,

Evaluation Methods,

and Severity Levels

may be introduced without invalidating existing Canonical Knowledge.

---

# 14. Conformance

Every conforming implementation shall validate Constraints according to this schema.

Validation behavior shall remain deterministic.

---

# Closing Statement

The Constraint Schema establishes the canonical representation of engineering constraints and forms the foundation of deterministic validation throughout the Canonical Specification Language ecosystem.
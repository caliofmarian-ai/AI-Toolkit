# Canonical Specification Language (CSL)

# RELATIONSHIP SCHEMA

Version: Draft 1.0

Status: Normative

Classification: Core Schema

---

# 1. Purpose

The Relationship Schema defines the canonical representation of semantic relationships between Engineering Entities.

Relationships establish engineering meaning.

Relationships are first-class objects.

---

# 2. Schema Definition

Every Relationship shall contain:

Relationship Identifier

Relationship Type

Source Entity

Target Entity

Status

Lifecycle

Provenance

Metadata

---

# 3. Required Fields

Identifier

Type

Source

Target

Version

Created

Modified

Status

---

# 4. Optional Fields

Description

Constraints

Documentation

Tags

Notes

References

Audit Metadata

---

# 5. Relationship Types

Mandatory relationship categories include:

contains

depends_on

implements

extends

references

requires

owns

approves

tests

validates

generates

deploys

publishes

consumes

supports

belongs_to

Future specifications may introduce additional relationship types.

---

# 6. Cardinality

Supported cardinalities include:

One-to-One

One-to-Many

Many-to-One

Many-to-Many

Cardinality shall be validated.

---

# 7. Direction

Relationships are directional by default.

Bidirectional relationships shall be explicitly declared.

---

# 8. Constraints

Relationships may define:

Multiplicity

Visibility

Lifecycle Restrictions

Dependency Rules

Governance Rules

Constraint violations invalidate the relationship.

---

# 9. Lifecycle

Relationships progress through:

Draft

Review

Approved

Canonical

Deprecated

Archived

---

# 10. Validation

Validation shall verify:

Identity

Source

Target

Relationship Type

Cardinality

Lifecycle

Constraints

Dependencies

---

# 11. Traceability

Every Relationship shall preserve:

Origin

Author

Approval

History

Compiler Version

CSL Version

Audit Records

---

# 12. Compatibility

Future versions shall preserve semantic compatibility whenever technically feasible.

---

# 13. Extensibility

Future relationship categories may be introduced without invalidating existing relationships.

---

# 14. Conformance

A conforming implementation shall validate every relationship against this schema.

---

# Closing Statement

The Relationship Schema defines the canonical structure used to represent engineering relationships within the Universal Engineering Model.
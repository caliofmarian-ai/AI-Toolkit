# Canonical Specification Language (CSL)

# PROPERTY SCHEMA

Version: 1.0.0

Status: Normative

Classification: Core Schema

---

# 1. Purpose

The Property Schema defines the canonical representation of Engineering Properties.

Properties describe Engineering Entities.

Properties never replace Engineering Relationships.

Properties extend engineering meaning.

---

# 2. Schema Definition

Every Property shall contain:

Property Identifier

Property Name

Property Type

Property Value

Status

Lifecycle

Metadata

---

# 3. Required Fields

Identifier

Name

Type

Value

Status

Version

Created

Modified

---

# 4. Optional Fields

Description

Default Value

Constraints

Validation Rules

Examples

Documentation

Tags

Notes

Audit Metadata

---

# 5. Primitive Types

Supported primitive types include:

String

Integer

Decimal

Boolean

Date

Time

Timestamp

Duration

Identifier

Reference

Enumeration

Binary

Null

---

# 6. Composite Types

Supported composite types include:

Object

Array

List

Set

Dictionary

Map

Graph

Composite types may contain primitive or composite values.

---

# 7. Cardinality

Properties may define:

Single Value

Optional Value

Required Value

Multiple Values

Validation shall enforce cardinality.

---

# 8. Default Values

Properties may define default values.

Default values shall never override explicitly defined values.

---

# 9. Validation

Validation shall verify:

Property Type

Property Value

Cardinality

Constraints

Default Value

Required Fields

Reference Integrity

---

# 10. Constraints

Properties may define constraints including:

Minimum Value

Maximum Value

Minimum Length

Maximum Length

Regular Expression

Allowed Values

Required Pattern

Future constraint types may be introduced.

---

# 11. Lifecycle

Property lifecycle:

Draft

Review

Approved

Canonical

Deprecated

Archived

---

# 12. Provenance

Every Property shall preserve:

Origin

Creator

Approval

Revision History

Compiler Version

CSL Version

Audit Records

---

# 13. Compatibility

Future versions shall preserve semantic compatibility whenever technically feasible.

---

# 14. Extensibility

Future property types may be introduced without invalidating existing Canonical Knowledge.

---

# 15. Conformance

Every conforming implementation shall validate properties according to this schema.

---

# Closing Statement

The Property Schema defines the canonical representation of Engineering Properties and provides the foundation for deterministic validation throughout the CSL ecosystem.
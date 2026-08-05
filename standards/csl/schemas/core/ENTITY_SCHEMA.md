# Canonical Specification Language (CSL)

# ENTITY SCHEMA

Version: Draft 1.0

Status: Normative

Classification: Core Schema

---

# 1. Purpose

This schema defines the canonical structure of every Engineering Entity represented within the Canonical Specification Language.

Every Engineering Entity shall conform to this schema unless explicitly extended by a future RFC.

---

# 2. Mandatory Fields

Every Entity shall contain the following mandatory fields.

Identifier

Type

Name

Description

Version

Status

Lifecycle

Owner

Created

Modified

Provenance

Relationships

Properties

Metadata

---

# 3. Identifier

Identifier uniquely identifies an Engineering Entity.

Rules:

Globally unique within the Canonical Knowledge scope.

Immutable.

Case-sensitive.

Whitespace prohibited.

Identifier format shall be implementation independent.

---

# 4. Entity Type

Entity Type defines semantic meaning.

Examples include:

Project

Capability

Feature

Requirement

Decision

Constraint

Policy

Rule

Risk

Issue

Epic

Milestone

Task

Component

Module

Service

API

Database

Generator

Validator

Compiler

Runtime

Additional entity types may be introduced through RFCs.

---

# 5. Name

The Name provides the primary human-readable representation.

Names should be concise.

Names should remain meaningful.

Names are mutable.

Changing a Name shall not modify Identity.

---

# 6. Description

Description explains engineering intent.

Descriptions remain human-oriented.

Descriptions never redefine semantics.

Semantics belong to the Entity Type and Relationships.

---

# 7. Version

Every Entity possesses a Version.

Version identifies engineering evolution.

Entity Version is independent from CSL Version.

---

# 8. Status

Minimum Status values:

Draft

Review

Approved

Deprecated

Archived

Implementations may introduce additional states.

---

# 9. Lifecycle

Lifecycle defines engineering progression.

Default lifecycle:

Draft

↓

Review

↓

Approved

↓

Canonical

↓

Compiled

↓

Generated

↓

Operational

↓

Archived

---

# 10. Ownership

Every Entity possesses an Owner.

Owner identifies engineering responsibility.

Ownership never changes Entity Identity.

Ownership remains traceable.

---

# 11. Provenance

Provenance records:

Origin

Creator

Approval

Revision History

Related Decisions

Compiler Version

CSL Version

Knowledge Source

Generation Timestamp

---

# 12. Relationships

Relationships connect Engineering Entities.

Relationship identifiers shall reference valid Engineering Entities.

Broken relationships invalidate the Entity.

---

# 13. Properties

Properties describe engineering characteristics.

Properties possess:

Name

Type

Value

Constraint

Optional Metadata

Properties shall remain deterministic.

---

# 14. Metadata

Metadata provides implementation-independent supplementary information.

Metadata shall never redefine engineering semantics.

---

# 15. Validation Rules

An Entity is valid only if:

Identifier exists.

Type exists.

Name exists.

Status exists.

Lifecycle exists.

Ownership exists.

Relationships resolve.

Properties validate.

Provenance exists.

---

# 16. Extensibility

Future RFCs may extend this schema.

Extensions shall preserve backward compatibility whenever technically feasible.

---

# Closing Statement

This Entity Schema establishes the canonical structure of Engineering Entities within the Canonical Specification Language.

Every conforming compiler, validator and reference implementation shall recognize and validate Engineering Entities according to this schema.

End of Entity Schema.
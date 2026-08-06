# CDM-002 — Canonical Universal Identifier (CUID)

Version: 1.0.0

Status: Draft

Classification: Canonical Standard

Standard Family: CDM

Identifier: CDM-002

Parent Standard: CDM-000_DOCUMENT_MODEL

Owner: AI CTO

---

# 1. Purpose

This specification defines the Canonical Universal Identifier (CUID), the authoritative identification system for every engineering artifact within the AI-Toolkit ecosystem.

The CUID provides globally unique, deterministic, version-aware and technology-independent identifiers.

---

# 2. Scope

The Canonical Universal Identifier applies to every canonical engineering artifact, including but not limited to:

- documents
- standards
- specifications
- Architecture Requirements (AR)
- Architecture Decision Records (ADR)
- RFCs
- audits
- policies
- roadmaps
- repositories
- engines
- platforms
- implementations
- tests
- knowledge graph entities
- runtime objects
- future engineering artifacts

No canonical artifact shall exist without a CUID.

---

# 3. Objectives

The Canonical Universal Identifier shall:

- uniquely identify every artifact
- remain stable throughout the artifact lifecycle
- support traceability
- support repository intelligence
- support distributed repositories
- enable graph relationships
- enable deterministic referencing

---

# 4. Canonical Definition

A Canonical Universal Identifier (CUID) is the permanent engineering identity assigned to a canonical artifact.

The identifier represents the artifact itself rather than its storage location.

---

# 5. Fundamental Principles

The CUID shall be:

- globally unique
- immutable
- deterministic
- human-readable
- machine-readable
- technology-independent
- version-aware
- repository-independent

---

# 6. Canonical Structure

The canonical structure is:

namespace

↓

domain

↓

artifact type

↓

artifact identifier

↓

version

General form:

namespace:domain:type:id:version

Example:

aitk:cdm:standard:002:v1

The exact serialization is defined by the reference implementation.

---

# 7. Namespace

Namespaces isolate engineering domains.

Examples include:

aitk

cdm

csl

canon

platform

engine

runtime

future namespaces

Namespaces shall remain globally unique.

---

# 8. Artifact Types

Examples:

standard

document

policy

audit

adr

ar

rfc

repository

engine

platform

knowledge

implementation

test

release

Additional artifact types may be introduced through governance.

---

# 9. Identifier Allocation

Identifiers shall never be reused.

Retired identifiers remain permanently reserved.

---

# 10. Version Identity

Artifact identity and artifact version are separate concepts.

The CUID identifies the artifact.

Version metadata identifies the release.

---

# 11. Repository Independence

Moving an artifact between repositories shall never change its CUID.

Repository paths are implementation details.

---

# 12. Relationship Support

CUIDs shall be used for:

dependencies

references

ownership

traceability

knowledge graph relationships

audit evidence

validation results

---

# 13. Machine Representation

CUIDs shall support serialization into canonical machine-readable formats.

Every representation shall preserve semantic equivalence.

---

# 14. Validation Rules

Validation shall verify:

uniqueness

format

namespace validity

artifact type validity

identifier integrity

version consistency

---

# 15. Lifecycle

A CUID is assigned once.

It shall never change.

Lifecycle changes affect metadata, not identity.

---

# 16. Governance

Creation of new namespaces, artifact types or allocation rules requires governance approval.

---

# 17. Relationship to Other Standards

CDM-000 defines document identity.

CDM-001 defines metadata.

This specification defines canonical identifiers.

All future standards shall reference artifacts using CUIDs.

---

# 18. Conformance Requirements

An artifact conforms to this specification when:

- exactly one CUID exists
- the CUID is globally unique
- the CUID remains immutable
- the CUID is machine-readable
- the CUID supports deterministic referencing

---

# 19. Success Criteria

The Canonical Universal Identifier is considered successful when every engineering artifact within AI-Toolkit can be uniquely identified, referenced, traced and validated without ambiguity, regardless of repository, implementation or technology.

---

# 20. Closing Statement

The Canonical Universal Identifier establishes the permanent identity layer of the AI-Toolkit ecosystem.

By separating identity from storage, implementation and lifecycle, the CUID enables scalable engineering, interoperability and long-term traceability across every canonical standard and engineering artifact.
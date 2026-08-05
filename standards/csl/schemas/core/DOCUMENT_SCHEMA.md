# Canonical Specification Language (CSL)

# DOCUMENT SCHEMA

Version: 1.0.0

Status: Normative

Classification: Core Schema

---

# 1. Purpose

The Document Schema defines the canonical structure of every CSL document.

Every Canonical Document shall conform to this schema.

The Document Schema provides a uniform structure that enables deterministic parsing, validation and compilation.

---

# 2. Schema Definition

Every Canonical Document shall contain:

Document Header

Document Metadata

Document Body

Optional Appendices

Document Provenance

Document Version

Document Status

---

# 3. Required Header Fields

Document Identifier

Document Title

Document Type

Version

Status

Classification

Language

(Valid values: `csl/1.0` for documents written in CSL, or an IETF BCP 47 language tag such as `en` for documents whose body is in a natural language. The field identifies the document authoring language, not a programming language.)

Created

Modified

---

# 4. Optional Header Fields

Author

Organization

Reviewers

Approvers

Compiler Version

CSL Version

Reference Version

License

Keywords

Tags

---

# 5. Metadata

Metadata describes document properties.

Metadata may include:

Category

Audience

Priority

Dependencies

Related Documents

Related RFCs

Related Specifications

Generation Information

Metadata shall never modify engineering meaning.

---

# 6. Document Body

The document body contains Canonical Knowledge.

The body may contain:

Engineering Entities

Relationships

Properties

Constraints

Definitions

Examples

Normative Statements

Informative Statements

Appendices

The body represents the authoritative engineering content.

---

# 7. References

Documents may reference:

Other Documents

RFCs

Engineering Entities

Knowledge Packages

Reference Implementations

Relationships shall remain resolvable.

Broken references invalidate the document.

---

# 8. Provenance

Every document shall preserve provenance.

Provenance records include:

Origin

Author

Approvals

Revision History

Compiler Version

CSL Version

Generation History

Audit Information

Provenance is immutable.

---

# 9. Versioning

Documents shall follow semantic versioning.

Every document version shall identify:

Major Version

Minor Version

Patch Version

Revision Date

Compatibility Information

Migration Guidance

---

# 10. Lifecycle

Document lifecycle consists of:

Draft

Review

Approved

Canonical

Deprecated

Archived

Lifecycle transitions shall remain traceable.

---

# 11. Validation

Validation shall verify:

Header

Metadata

Document Structure

References

Relationships

Version

Lifecycle

Provenance

Constraint Compliance

Validation failures prevent successful compilation.

---

# 12. Determinism

Equivalent Canonical Documents shall always produce equivalent semantic representations.

Formatting differences shall never modify engineering meaning.

---

# 13. Extensibility

Future document types,

metadata,

sections,

and appendices

may be introduced without invalidating existing Canonical Documents.

---

# 14. Conformance

Every Canonical Document shall conform to this schema.

Reference implementations shall reject documents that violate mandatory requirements.

---

# 15. Closing Statement

The Document Schema establishes the canonical structure shared by every document within the Canonical Specification Language.

It guarantees consistency, interoperability, deterministic compilation and long-term maintainability across all CSL-compliant implementations.

End of Document Schema.
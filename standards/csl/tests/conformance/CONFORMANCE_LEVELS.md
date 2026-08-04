# Canonical Specification Language (CSL)

# CONFORMANCE LEVELS

Version: Draft 1.0

Status: Normative

Classification: Conformance Standard

---

# Purpose

This specification defines the official conformance levels for implementations of the Canonical Specification Language.

Conformance levels allow implementations to declare precisely which parts of the CSL Standard they support.

Every implementation shall publish its supported conformance level.

---

# Fundamental Principle

Conformance measures implementation behavior.

Conformance does not measure implementation performance.

Implementations are evaluated only against the requirements defined by the CSL Standard.

---

# Conformance Levels

The CSL Standard defines five official conformance levels.

Level 1

Core Reader

Level 2

Core Validator

Level 3

Compiler

Level 4

Reference Implementation

Level 5

Complete Engineering Platform

---

# Level 1 — Core Reader

A Level 1 implementation shall:

Load Canonical Documents.

Read document metadata.

Recognize Engineering Entities.

Recognize Relationships.

Recognize Properties.

Recognize Constraints.

Reject invalid document structures.

Artifact generation is not required.

---

# Level 2 — Core Validator

A Level 2 implementation shall satisfy all Level 1 requirements.

Additionally it shall:

Perform lexical validation.

Perform grammar validation.

Perform semantic validation.

Validate relationships.

Validate constraints.

Validate dependencies.

Produce deterministic diagnostics.

Compilation is optional.

---

# Level 3 — Compiler

A Level 3 implementation shall satisfy all previous levels.

Additionally it shall:

Construct the Universal Engineering Model.

Support deterministic compilation.

Generate Engineering Artifacts.

Support incremental compilation.

Support deterministic validation.

---

# Level 4 — Reference Implementation

A Level 4 implementation shall satisfy all previous levels.

Additionally it shall:

Implement all Core Specifications.

Implement all approved RFCs.

Provide the Reference Compiler.

Provide the Reference Validator.

Provide Generator Framework support.

Provide Repository Adapter support.

Provide Safety and Governance.

Maintain complete traceability.

---

# Level 5 — Complete Engineering Platform

A Level 5 implementation shall satisfy all previous levels.

Additionally it shall:

Support Plugin Architecture.

Support AI Provider Adapters.

Support Repository Adapters.

Support Knowledge Packages.

Support distributed engineering.

Support engineering automation.

Support migration tooling.

Support compliance reporting.

---

# Compliance Statement

Every implementation shall publish:

Supported Conformance Level.

Supported CSL Version.

Supported RFC Version.

Unsupported Features.

Known Limitations.

Compatibility Information.

---

# Certification

An implementation shall not claim a conformance level unless all mandatory requirements for that level have been satisfied.

Partial compliance shall be explicitly declared.

---

# Validation

Conformance verification shall be repeatable.

Equivalent implementations shall achieve equivalent conformance results when evaluated against identical test suites.

---

# Future Levels

Future CSL versions may introduce additional conformance levels.

Existing conformance levels shall remain stable whenever technically feasible.

---

# Closing Statement

Conformance Levels provide a common language for evaluating CSL implementations.

They ensure interoperability, transparency and long-term compatibility throughout the CSL ecosystem.

End of Conformance Levels.
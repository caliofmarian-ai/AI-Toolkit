# Canonical Specification Language (CSL)

# GLOSSARY

Version: 1.0.0

Status: Normative

Classification: Reference

---

# Purpose

This glossary defines the official meaning of terminology used throughout the Canonical Specification Language.

Whenever a term defined in this glossary appears within a CSL specification, RFC, schema or reference implementation, it shall carry the meaning defined here.

Future versions may extend this glossary.

Existing definitions shall remain stable whenever technically feasible.

---

# Abstract Syntax Tree (AST)

A structured representation of parsed CSL source prior to semantic interpretation.

---

# Approval

A governance decision authorizing an engineering action.

Approvals shall be explicit.

Approvals shall be auditable.

---

# Artifact

A derived engineering output generated from the Universal Engineering Model.

Artifacts are not Canonical Knowledge.

---

# Audit

The permanent historical record describing engineering actions.

Audit information shall be immutable.

---

# Canonical Knowledge

The authoritative engineering knowledge represented using the Canonical Specification Language.

Canonical Knowledge is the single source of engineering truth.

---

# Compiler

A system that transforms Canonical Knowledge into the Universal Engineering Model and Engineering Artifacts.

---

# Constraint

A rule that limits or validates Engineering Knowledge.

Constraint violations prevent successful validation.

---

# Dependency

A semantic relationship expressing engineering necessity.

Dependencies may be mandatory or optional.

---

# Engineering Entity

A uniquely identifiable engineering object represented within the Universal Engineering Model.

---

# Engineering Artifact

A generated engineering output derived from Canonical Knowledge.

Examples include:

Documentation

Source Code

Configuration

Roadmaps

Issues

Deployment Specifications

---

# Generator

A component that transforms the Universal Engineering Model into Engineering Artifacts.

Generators never modify Canonical Knowledge.

---

# Knowledge Package

A portable package containing Canonical Knowledge together with metadata and validation information.

---

# Parser

A component responsible for transforming CSL source into an Abstract Syntax Tree.

---

# Property

A descriptive value belonging to an Engineering Entity.

Properties never replace Relationships.

---

# Provenance

The historical origin of Engineering Knowledge.

Provenance includes authorship, approvals, revisions and generation history.

---

# Reference Implementation

An implementation demonstrating complete conformance with the CSL Standard.

AI-Toolkit is the first Reference Implementation.

---

# Relationship

A semantic connection between Engineering Entities.

Relationships define engineering meaning.

---

# Repository Adapter

A provider-specific integration layer isolating repository implementations from Canonical Knowledge.

---

# Schema

A formal definition describing the structure of Engineering Knowledge.

Schemas support deterministic validation.

---

# Semantic Model

The implementation-independent representation of engineering meaning.

---

# Universal Engineering Model (UEM)

The canonical semantic representation constructed by every conforming CSL compiler.

The Universal Engineering Model serves as the foundation for all Engineering Artifact generation.

---

# Validation

The deterministic verification of Canonical Knowledge against the CSL Standard.

Validation confirms correctness.

Validation never modifies engineering meaning.

---

# Visibility

A property of an Engineering Entity that determines its accessibility outside its declaring scope.

Valid values are Private, Internal, Protected, Public, and Restricted.

The default visibility is Public when no visibility attribute is declared.

---

# Prompt

A Prompt is a Canonical Knowledge entity that defines reusable, versioned configuration of structured input for an Artificial Intelligence Provider.

Prompt entities are maintained as Canonical Knowledge and may reference Requirements, Features and Components.

The runtime input actually transmitted to an AI Provider is derived from a Prompt entity through the Generator Framework. That derived runtime input is an Engineering Artifact, not a new Canonical Knowledge entity.

---

# Lifecycle

The defined sequence of states that an Engineering Entity progresses through during its existence.

The canonical lifecycle sequence is: Draft, Review, Approved, Canonical, Compiled, Generated, Operational, Deprecated, Archived.

---

# CSL Foundation

The governing body of the Canonical Specification Language.

The CSL Foundation maintains the canonical standard, approves RFCs, issues official releases, and protects the long-term integrity of Canonical Knowledge.

The CSL Foundation operates by consensus of active maintainers as defined in the Constitution.

---

# Closing Statement

This glossary establishes the official terminology used throughout the Canonical Specification Language.

Every conforming implementation shall interpret these terms consistently.

End of Glossary.
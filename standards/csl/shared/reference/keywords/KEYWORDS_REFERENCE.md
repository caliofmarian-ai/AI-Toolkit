# Canonical Specification Language (CSL)

# KEYWORDS REFERENCE

Version: 1.0.0

Status: Normative

Classification: Reference

---

# Purpose

This document defines the official reserved keywords of the Canonical Specification Language.

Reserved keywords possess predefined engineering meaning.

Reserved keywords shall not be used as user-defined identifiers.

Future CSL versions may introduce additional keywords.

Existing keyword semantics shall remain stable.

---

# Project

Represents the highest-level engineering container.

A Project groups Engineering Knowledge into a coherent engineering system.

---

# Capability

Represents a major engineering ability delivered by the system.

Capabilities group Features.

---

# Feature

Represents a concrete engineering function implementing a Capability.

Features satisfy Requirements.

---

# Requirement

Represents an engineering objective that shall be satisfied.

Requirements describe intent rather than implementation.

---

# Decision

Represents an engineering decision together with its rationale.

Decisions preserve engineering history.

---

# Constraint

Represents a validation rule limiting acceptable engineering states.

Constraints preserve engineering correctness.

---

# Policy

Represents governance rules controlling engineering behavior.

Policies regulate execution.

---

# Rule

Represents deterministic engineering logic.

Rules may be validated automatically.

---

# Risk

Represents a potential engineering threat.

Risk classification influences governance requirements.

---

# Issue

Represents an engineering work item requiring implementation.

Issues may be generated automatically.

---

# Epic

Represents a large engineering objective grouping multiple Issues.

---

# Milestone

Represents a measurable engineering objective within project planning.

---

# Task

Represents an executable engineering activity.

Tasks possess ownership and lifecycle.

---

# Component

Represents a logical implementation unit.

Components implement Features.

---

# Module

Represents a cohesive implementation grouping.

Modules may contain multiple Components.

---

# Service

Represents an independently deployable engineering capability.

---

# API

Represents a formal communication interface between engineering systems.

---

# Entity

Represents a uniquely identifiable Engineering Object.

Entities become nodes within the Universal Engineering Model.

---

# Relationship

Represents semantic connections between Engineering Entities.

Relationships define engineering meaning.

---

# Generator

Represents a component generating Engineering Artifacts.

Generators consume the Universal Engineering Model.

---

# Validator

Represents a component responsible for deterministic validation.

Validators never modify Canonical Knowledge.

---

# Compiler

Represents a formal description of an Engineering Compiler within canonical knowledge.

When used as a keyword in a CSL document, Compiler describes a compiler component as an engineering object — for example, when documenting the reference compiler's capabilities, version, supported features, or conformance level.

The Compiler keyword operates at the engineering description level, not the meta-compiler level. It is the canonical way to declare compiler configuration and capability documentation within a Knowledge Package.

Example use: A project may declare the supported compiler version and its conformance level as Compiler entities within its canonical knowledge.

---

# Runtime

Represents the execution environment of an implementation.

Runtime behavior remains implementation specific.

---

# Knowledge

Represents a named grouping of Canonical Engineering statements that do not map to a more specific entity type.

The Knowledge keyword may be used to introduce custom engineering concepts that are not yet formally represented by an established keyword.

Use of the Knowledge keyword is discouraged when a more specific entity type exists.

The Universal Engineering Model treats Knowledge entities as generic engineering objects with full lifecycle, provenance, and relationship support.

---

# Reference

Represents a semantic connection to another Engineering Object.

References preserve traceability.

---

# Approval

Represents explicit governance authorization.

Approvals remain auditable.

---

# Deployment

Represents publication of Engineering Artifacts into operational environments.

---

# Environment

Represents an execution context.

Examples include:

Development

Testing

Staging

Production

---

# Provider

Represents an external implementation offering engineering capabilities.

Examples include:

Repository Providers

AI Providers

Storage Providers

Authentication Providers

---

# Model

Represents an abstract engineering representation.

Examples include:

Semantic Model

Universal Engineering Model

Execution Model

---

# Prompt

Represents canonical configuration of structured input supplied to an Artificial Intelligence Provider.

A Prompt entity defines reusable, versioned AI task inputs as part of the engineering model.

Prompt entities are Canonical Knowledge. They define how AI tasks shall be executed, and may be generated from the Universal Engineering Model.

The content supplied to an AI Provider at runtime is derived from a Prompt entity through the Generator Framework. That derived runtime content is an Engineering Artifact, not Canonical Knowledge.

Prompt entities may reference Requirements, Features and Components to establish AI task context from canonical sources.

---

# Closing Statement

Reserved keywords establish the engineering vocabulary of the Canonical Specification Language.

Every conforming implementation shall interpret these keywords according to the definitions contained within this reference.

End of Keywords Reference.
# Canonical Specification Language (CSL)

# KEYWORDS REFERENCE

Version: Draft 1.0

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

Represents the Engineering Compiler responsible for constructing the Universal Engineering Model.

---

# Runtime

Represents the execution environment of an implementation.

Runtime behavior remains implementation specific.

---

# Knowledge

Represents Canonical Engineering Knowledge.

Knowledge remains the authoritative engineering source.

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

Represents structured input supplied to an Artificial Intelligence Provider.

Prompts never become Canonical Knowledge.

---

# Closing Statement

Reserved keywords establish the engineering vocabulary of the Canonical Specification Language.

Every conforming implementation shall interpret these keywords according to the definitions contained within this reference.

End of Keywords Reference.
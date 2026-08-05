# Canonical Specification Language (CSL)

# ENTITY REFERENCE

Version: Draft 1.0

Status: Normative

Classification: Reference

---

# Purpose

This document defines the canonical Engineering Entities recognized by the Canonical Specification Language.

Engineering Entities are the fundamental semantic building blocks of the Universal Engineering Model.

Every conforming implementation shall recognize these entities.

---

# Project

Represents the highest-level engineering container.

A Project defines the engineering boundary within which Canonical Knowledge exists.

A Project may contain multiple Capabilities, Requirements, Components, Policies and Knowledge Packages.

---

# Capability

Represents a major engineering objective delivered by a system.

Capabilities group Features and express business value.

Capabilities are implementation independent.

---

# Feature

Represents a concrete engineering function.

Features implement Capabilities.

Features satisfy Requirements.

---

# Requirement

Represents an engineering objective.

Requirements define intent.

Requirements remain independent of implementation technology.

---

# Decision

Represents a documented engineering decision.

Decisions preserve rationale, alternatives and historical context.

Decisions shall remain permanently traceable.

---

# Policy

Represents engineering governance.

Policies regulate engineering behavior.

Policies influence authorization and execution.

---

# Rule

Represents deterministic engineering logic.

Rules may be evaluated automatically.

Rules support validation.

---

# Constraint

Represents engineering limitations.

Constraints preserve semantic correctness.

Constraint violations invalidate Engineering Knowledge.

---

# Risk

Represents an identified engineering uncertainty or threat.

Risks influence governance, approval and mitigation planning.

---

# Component

Represents a logical implementation unit.

Components implement Features.

Components remain technology independent.

---

# Module

Represents a cohesive engineering grouping.

Modules organize Components.

Modules improve maintainability.

---

# Service

Represents an independently deployable engineering capability.

Services expose defined interfaces.

Services may communicate through APIs.

---

# API

Represents a formal communication contract.

APIs define interactions between Components and Services.

APIs remain implementation independent.

---

# Entity

Represents any uniquely identifiable Engineering Object.

Entities form the nodes of the Universal Engineering Model.

---

# Relationship

Represents semantic connections between Engineering Entities.

Relationships define engineering meaning.

Relationships are first-class Engineering Objects.

---

# Generator

Represents a component that generates Engineering Artifacts.

Generators consume the Universal Engineering Model.

Generators never modify Canonical Knowledge.

---

# Validator

Represents a component responsible for deterministic validation.

Validators verify correctness.

Validators never change engineering meaning.

---

# Compiler

Represents the Engineering Compiler.

The Compiler transforms Canonical Knowledge into the Universal Engineering Model and Engineering Artifacts.

---

# Runtime

Represents the execution environment of an implementation.

Runtime behavior remains implementation specific.

---

# Knowledge Package

Represents a portable engineering package containing Canonical Knowledge.

Knowledge Packages support exchange, validation and compilation.

---

# Repository Adapter

Represents the integration layer between Canonical Knowledge and repository providers.

Repository Adapters preserve repository independence.

---

# AI Provider

Represents an external Artificial Intelligence implementation.

AI Providers execute engineering tasks through standardized interfaces.

AI Providers never become sources of engineering truth.

---

# Universal Engineering Model

Represents the canonical semantic representation constructed by every conforming compiler.

The Universal Engineering Model is the central engineering representation within the CSL ecosystem.

---

# Closing Statement

Engineering Entities establish the common semantic vocabulary shared by every Canonical Specification Language implementation.

Every future entity introduced into the standard shall remain consistent with the definitions established in this reference.

End of Entity Reference.
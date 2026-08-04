# RFC-0009

# Canonical Project Structure

Version: Draft 1.0

Status: Proposed

Category: Project Architecture

---

# 1. Purpose

This RFC defines the Canonical Project Structure used by every CSL-compliant engineering project.

The project structure organizes engineering knowledge in a predictable, deterministic and implementation-independent manner.

It standardizes how Canonical Knowledge is stored while remaining independent of programming languages and repository providers.

---

# 2. Motivation

Modern repositories evolve without consistent organization.

Different directory structures reduce discoverability, automation and interoperability.

A Canonical Project Structure enables automated tooling to understand projects without repository-specific assumptions.

---

# 3. Objectives

The Canonical Project Structure shall:

provide deterministic organization,

separate Canonical Knowledge from generated artifacts,

support incremental evolution,

support multiple repositories,

support multiple programming languages,

remain extensible,

remain implementation independent.

---

# 4. Architectural Principles

A Canonical Project shall separate:

Canonical Knowledge

Reference Documentation

Engineering Specifications

RFCs

Schemas

Validation Assets

Examples

Generated Artifacts

Implementation Source Code

Runtime Assets

Canonical Knowledge shall remain independent from implementation artifacts.

---

# 5. Root Structure

A conforming project may contain the following top-level directories:

standards/

knowledge/

schemas/

examples/

tests/

reference/

generated/

runtime/

tools/

docs/

Additional directories are permitted provided they do not modify Canonical Knowledge.

---

# 6. Standards Directory

The `standards/` directory contains normative specifications.

Examples:

Manifesto

Constitution

Roadmap

Core Specifications

RFCs

The Standards directory defines engineering rules.

---

# 7. Knowledge Directory

The `knowledge/` directory stores project-specific Canonical Knowledge.

Examples:

Capabilities

Requirements

Features

Policies

Engineering Decisions

Knowledge Graphs

Knowledge Packages

The contents of this directory become compiler input.

---

# 8. Generated Directory

The `generated/` directory stores artifacts produced by the Engineering Compiler.

Examples include:

Documentation

Roadmaps

Source Code

Configuration

Infrastructure

Deployment

Tests

AI Tasks

Generated artifacts shall never become Canonical Knowledge.

---

# 9. Runtime Directory

The `runtime/` directory contains implementation-specific runtime assets.

Examples include:

Executables

Containers

Scripts

Binaries

Runtime configuration

Runtime assets remain replaceable.

---

# 10. Tools Directory

The `tools/` directory contains engineering utilities.

Examples:

Validators

Generators

Migration Tools

Converters

Diagnostics

Utilities never redefine Canonical Knowledge.

---

# 11. Documentation Directory

The `docs/` directory contains human-oriented documentation.

Documentation may be generated.

Documentation may contain explanatory material.

Documentation shall never replace Canonical Knowledge.

---

# 12. Separation of Concerns

Every directory possesses one primary responsibility.

Knowledge shall not be mixed with generated artifacts.

Runtime assets shall not modify Canonical Knowledge.

Generated files shall remain reproducible.

---

# 13. Traceability

Every generated artifact shall identify:

Originating Canonical Knowledge

Compiler Version

Generator

Generation Timestamp

Traceability Reference

Project organization shall preserve traceability.

---

# 14. Extensibility

Projects may introduce additional directories.

Additional directories shall:

possess a clearly defined responsibility,

avoid duplicating Canonical Knowledge,

preserve deterministic organization.

---

# 15. Compatibility

Existing projects may migrate incrementally.

Migration shall preserve:

Engineering Identity

Engineering Provenance

Canonical Knowledge

Project History

Migration shall remain deterministic.

---

# 16. Governance

Project organization shall comply with:

Constitution

Core Specifications

Safety & Governance

Repository Policies

Project organization shall remain auditable.

---

# 17. Implementation Impact

Affected Components:

Knowledge Loader

Repository Engine

Engineering Compiler

Reference Implementation

Documentation Generator

Project Validator

---

# 18. Acceptance Criteria

The RFC is complete when:

Canonical Knowledge is separated from generated artifacts.

Project organization is deterministic.

Repository independence is preserved.

Traceability is maintained.

Migration is supported.

---

# Closing Statement

The Canonical Project Structure provides a predictable engineering organization that enables automation, interoperability and long-term maintainability while preserving Canonical Knowledge as the authoritative foundation of every CSL-compliant project.
# Canonical Specification Language (CSL)

# HELLO CSL

Version: Draft 1.0

Status: Normative Example

Classification: Basic Example

---

# Purpose

This document provides the smallest valid Canonical Specification Language example.

Its purpose is educational.

It demonstrates the minimum concepts required to construct a valid Canonical Knowledge document.

---

# Example

Project:

    Identifier: HELLO-CSL

    Name: Hello CSL

    Version: 1.0.0

Capability:

    Identifier: HELLO-CAPABILITY

    Name: Greeting

Requirement:

    Identifier: HELLO-REQUIREMENT

    Name: Produce Greeting

Feature:

    Identifier: HELLO-FEATURE

    Name: Hello World

Relationship:

    Feature implements Requirement

Relationship:

    Capability contains Feature

---

# Semantic Interpretation

The Project defines one engineering system.

The Capability describes a single engineering ability.

The Requirement specifies engineering intent.

The Feature implements that intent.

The Relationships connect the Engineering Entities.

The Compiler constructs an equivalent Universal Engineering Model.

---

# Expected Universal Engineering Model

Engineering Objects:

Project

Capability

Requirement

Feature

Relationships:

contains

implements

Validation:

Successful

Compilation:

Successful

Artifact Generation:

Permitted

---

# Expected Validation Result

Lexical Validation

PASS

Grammar Validation

PASS

Semantic Validation

PASS

Relationship Validation

PASS

Constraint Validation

PASS

Compilation

PASS

---

# Learning Objectives

After studying this example the reader should understand:

How a Project is defined.

How Engineering Entities are declared.

How Relationships connect Engineering Knowledge.

How Canonical Knowledge becomes the Universal Engineering Model.

---

# Closing Statement

This example represents the smallest complete Canonical Specification Language project.

Every conforming implementation shall successfully parse, validate and compile this document.

End of Hello CSL.
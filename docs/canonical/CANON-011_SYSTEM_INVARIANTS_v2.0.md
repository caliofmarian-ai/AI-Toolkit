# CANON-011 — System Invariants v2.0

## Status

Canonical

---

# Purpose

This document defines the architectural invariants of AI Toolkit.

System invariants are rules that must remain true regardless of future implementation changes.

Violating an invariant means the implementation is non-canonical.

---

# Invariant 1

Exactly one WorkspaceIndex exists for each repository execution.

---

# Invariant 2

Filesystem traversal occurs exactly once.

No engine may independently scan the repository.

---

# Invariant 3

Analysis engines are read-only.

Analysis engines never modify repositories.

---

# Invariant 4

Planning is independent from execution.

Planning produces plans.

Execution executes plans.

---

# Invariant 5

Execution never changes planning decisions.

---

# Invariant 6

WorkspaceIndex is immutable.

---

# Invariant 7

RepositoryPolicy is the only authority for inclusion and exclusion rules.

---

# Invariant 8

Every engine reports observability metrics.

---

# Invariant 9

Every execution produces a persistent execution state.

---

# Invariant 10

Every Pull Request preserves canonical architecture.

---

# Invariant 11

Business logic must never be duplicated.

---

# Invariant 12

Every public component must be testable.

---

# Invariant 13

Dependency direction is always

Repository

↓

Analysis

↓

Intelligence

↓

Planning

↓

Execution

Reverse dependencies are prohibited.

---

# Invariant 14

Every architectural change requires canonical validation.

---

# Invariant 15

Backward compatibility is preferred whenever reasonably possible.

---

# Acceptance Criteria

Every implementation must satisfy every invariant defined in this document.


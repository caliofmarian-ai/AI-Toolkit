# CANON-004 — AI Agent Specification v2.0

## Status

Canonical

---

# Purpose

This document defines the canonical behavior of every AI Agent inside AI Toolkit.

Every agent must follow this specification.

---

# General Principles

Every AI Agent must be:

- deterministic
- modular
- observable
- testable
- repository-independent
- stateless whenever possible

Agents never modify repositories directly unless explicitly operating inside the Execution Layer.

---

# Agent Lifecycle

Every agent follows the same lifecycle.

1. Receive Context
2. Validate Context
3. Load Shared Models
4. Execute Task
5. Produce Result
6. Report Metrics
7. Return Structured Output

No hidden side effects.

---

# Mandatory Interface

Every agent exposes:

run(context)

Returns:

AgentResult

AgentResult must include

- success
- messages
- data
- metrics

---

# Shared Context

Every agent receives

- WorkspaceIndex
- RepositoryContext
- RepositoryPolicy
- ExecutionState (optional)

Agents must never rebuild these objects.

---

# Agent Categories

Analysis Agents

Examples

- RepositoryAgent
- DependencyAgent
- SemanticAgent
- KnowledgeGraphAgent

Responsibilities

- inspect
- analyze
- collect metadata

Never modify repositories.

---

# Intelligence Agents

Examples

- PlanningAgent
- RecommendationAgent
- ReviewAgent
- RiskAgent

Responsibilities

- evaluate
- prioritize
- estimate
- recommend

Never execute plans.

---

# Execution Agents

Examples

- BatchGenerator
- ExecutionCoordinator
- WorkspaceOrchestrator

Responsibilities

- execute plans
- update execution state
- generate artifacts

No planning logic.

---

# Review Agents

Responsibilities

- quality gates
- validation
- acceptance criteria
- scoring
- review summary

---

# Observability

Every agent reports

- elapsed time
- repository
- current phase
- processed items
- warnings
- errors

Direct stdout logging should be avoided.

Metrics are sent to the Observability Layer.

---

# Error Handling

Agents must

- fail gracefully
- return structured errors
- preserve execution state
- never terminate the platform unexpectedly

---

# Dependency Rules

Agents communicate through

- shared models
- dependency injection
- immutable data

Avoid direct agent-to-agent coupling.

---

# Performance Rules

Every agent should expose

- execution time
- throughput
- memory usage (future)
- CPU usage (future)

---

# Future Compatibility

Agents should support

- parallel execution
- distributed execution
- remote execution
- AI-assisted execution
- checkpoint recovery

without architectural changes.

---

# Acceptance Criteria

Every new AI Agent must comply with this specification.

Agents violating these rules are considered non-canonical.


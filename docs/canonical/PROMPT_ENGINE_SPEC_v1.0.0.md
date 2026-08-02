# PROMPT ENGINE SPECIFICATION

Version: 1.0.0

Status: CANONICAL

Authority: OWNER

---

# PURPOSE

The Prompt Engine is responsible for generating deterministic, context-aware prompts for every AI model integrated with AI Toolkit.

The Prompt Engine is model-independent.

No engine communicates directly with an AI model.

All communication passes through the Prompt Engine.

---

# OBJECTIVES

Generate deterministic prompts.

Inject canonical context.

Inject repository context.

Inject workflow context.

Inject memory context.

Reduce prompt duplication.

Guarantee reproducibility.

---

# INPUTS

User request

Repository context

Canonical documents

Project memory

Knowledge Graph

Decision Engine

Execution state

Workflow stage

Repository metadata

---

# OUTPUTS

System Prompt

Developer Prompt

Execution Prompt

Review Prompt

Planning Prompt

Testing Prompt

Documentation Prompt

Pull Request Prompt

Release Prompt

---

# PROMPT PIPELINE

Receive Request

↓

Load Canonical Context

↓

Load Repository Context

↓

Load Memory

↓

Load Knowledge Graph

↓

Generate Prompt

↓

Validate Prompt

↓

Deliver Prompt

---

# PROMPT TYPES

Discovery

Inspection

Planning

Execution

Review

Testing

Documentation

Release

Recovery

Learning

---

# CONTEXT PRIORITY

Canonical Documents

↓

Decision Engine

↓

Knowledge Graph

↓

Repository Memory

↓

Workspace

↓

User Request

---

# MODEL ABSTRACTION

Supported Models

OpenAI

GitHub Copilot

Codex

Claude

Gemini

Ollama

Future Providers

---

# PROMPT TEMPLATE

Objective

Context

Constraints

Inputs

Expected Output

Validation Rules

Acceptance Criteria

---

# VALIDATION

Every generated prompt shall

Be deterministic

Reference canonical rules

Avoid ambiguity

Contain acceptance criteria

Be reproducible

---

# PROMPT STORAGE

.ai/prompts/

planning/

execution/

review/

documentation/

release/

history/

---

# INVARIANTS

Prompts never bypass canonical documents.

Prompts always include execution context.

Prompt generation is deterministic.

Prompt history is preserved.

Prompt templates are versioned.

---

# FUTURE

Adaptive Prompting

Semantic Prompt Expansion

Self-Optimizing Prompts

Multi-Agent Prompt Routing

Prompt Marketplace

Prompt Learning


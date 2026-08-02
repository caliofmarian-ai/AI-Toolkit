# Engine Interface Specification
Version: 1.0.0
Status: CANONICAL
Authority: OWNER

# PURPOSE

This specification defines the mandatory interface implemented by every AI Toolkit engine.

No engine may expose custom behavior outside this contract.

---

# ENGINE LIFECYCLE

Every engine follows the same lifecycle:

Initialize

↓

Validate Input

↓

Load State

↓

Execute

↓

Generate Output

↓

Save State

↓

Return Exit Code

---

# REQUIRED FILE LOCATION

lib/<engine_name>.sh

---

# REQUIRED PUBLIC ENTRYPOINT

Every engine shall expose exactly one public entry function.

Example:

run_engine()

---

# REQUIRED INPUT

Repository path

Optional arguments

Execution context

Current state

Environment

---

# REQUIRED OUTPUT

Human-readable console output

Machine-readable artifacts

Log entries

Exit code

---

# STATE RULES

Every engine shall read from:

.ai/state/

Every engine shall write only to its own directory under:

.ai/

No engine shall overwrite another engine's data.

---

# LOGGING

Each engine shall create:

logs/<engine>.log

The log shall contain:

Timestamp

Engine name

Input

Output

Errors

Execution time

---

# ERROR HANDLING

Every error must:

Return a non-zero exit code

Write a log entry

Display a readable message

Never terminate unrelated engines

---

# INTER-ENGINE COMMUNICATION

Engines communicate only through:

.ai/context/

.ai/status/

.ai/work/

.ai/history/

.ai/memory/

No direct engine-to-engine execution is allowed except through the orchestrator.

---

# VERSIONING

Each engine exposes:

ENGINE_NAME

ENGINE_VERSION

ENGINE_DESCRIPTION

---

# TEST REQUIREMENTS

Every engine must have:

Unit test

Integration test

Failure test

Smoke test

---

# DESIGN PRINCIPLES

Single responsibility

Deterministic behavior

Idempotent execution

Observable state

Modular implementation

Replaceable implementation

Backward compatibility


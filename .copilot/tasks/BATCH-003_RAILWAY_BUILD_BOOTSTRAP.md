# BATCH-003 — Railway Build Bootstrap & Production Deployment

## Mission

Implement Railway build compatibility for AI Toolkit.

The Runtime Server (CORE-021) is already implemented and validated.

The current blocker is Railway build detection.

Do NOT redesign the Runtime.

Do NOT modify the canonical architecture.

Fix only the production build bootstrap.

---

## Current Failure

Railway Build Logs report:

Nixpacks was unable to generate a build plan for this app.

The Runtime implementation is functional.

The repository structure is not currently recognized by Nixpacks as a Python application.

---

## Objective

Make AI Toolkit deploy successfully on Railway.

---

## Required Deliverables

### Python Build Detection

Provide the canonical Python project definition.

Use the most appropriate approach for the existing architecture.

Examples include:

- pyproject.toml

or

- requirements.txt

or

another canonical Nixpacks-compatible configuration.

Choose the best solution for this repository.

---

### Dependency Installation

Ensure Railway installs Runtime dependencies automatically.

No manual installation.

No interactive steps.

---

### Runtime Startup

Validate that:

bash bin/runtime-server

starts successfully on Railway.

---

### Railway Compatibility

Validate:

- Nixpacks detects Python.
- Build succeeds.
- Runtime starts.
- Health endpoint responds.
- Readiness endpoint responds.
- Restart policy works.

---

### Runtime Validation

Validate:

/health

/ready

/status

/metrics

---

### Tests

Run all Runtime regression tests.

Run Railway deployment validation.

Ensure no Runtime regressions.

---

### Acceptance Criteria

Railway build succeeds.

Deployment succeeds.

Runtime starts automatically.

Health endpoint returns success.

Readiness endpoint returns success.

Runtime remains operational.

No canonical violations.

No Runtime regressions.

---

### Constraints

Do NOT redesign Runtime.

Do NOT remove Runtime components.

Do NOT modify CANON-055 through CANON-059.

Implement only Railway build compatibility.

---

### Pull Request

Create one implementation branch.

Create one Draft Pull Request.

Include:

- Root Cause Analysis
- Files Added
- Files Modified
- Railway Validation
- Deployment Evidence
- Remaining Limitations

Do not mark Ready for Review until Railway deploys successfully.


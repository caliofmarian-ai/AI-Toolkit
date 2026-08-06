# Implementation Backlog

**Status:** Active  
**Created:** 2026-08-06  
**Source:** `docs/audits/EXECUTIVE_REPOSITORY_AUDIT.md`

Issues are ordered by implementation dependency. Complete in sequence.

---

## Issue #1 — Repository Engine: File Classification and CLI

**Priority:** Critical  
**Sprint:** 1  
**Complexity:** Medium

### Purpose

`bin/ai inspect <path>` must produce a human-readable Markdown report for any repository.
Currently `RepositoryEngine.discover()` lists files but does not classify them, and there is
no CLI entry point.

### Files to Modify / Create

| Action | File |
|---|---|
| Extend | `lib/python/repository_engine/engine.py` |
| Extend | `lib/python/repository_engine/models.py` |
| Create | `lib/python/repository_engine/classifier.py` |
| Create | `lib/python/repository_engine/report.py` |
| Create | `lib/python/repository_engine/cli.py` |
| Create | `lib/python/repository_engine/metrics.py` |
| Modify | `bin/ai` — add `inspect` command |
| Create | `tests/test_repository_engine_inspect.sh` |

**Source code to consolidate (do not rewrite — copy logic):**
- `lib/python/executable_repository_intelligence/file_classifier.py`
- `lib/python/executable_repository_intelligence/zone_classifier.py`
- `lib/python/engineering_engine/repository_scanner.py`

### Dependencies

- `lib/python/workspace_index/` (already used by engine)

### Implementation Steps

1. In `classifier.py`: implement `FileClassifier.classify(path) -> FileClass` where
   `FileClass` ∈ {source, test, config, doc, generated, build, unknown}.
   Port logic from `executable_repository_intelligence/file_classifier.py`.
2. In `metrics.py`: implement `RepositoryMetrics` dataclass and
   `MetricsExtractor.extract(root) -> RepositoryMetrics` computing:
   language distribution, file counts by class, entry point list,
   test file count, doc coverage ratio.
3. In `models.py`: add `RepositoryProfile` dataclass containing
   `path`, `name`, `metrics`, `classified_files`, `tech_stack`, `entry_points`.
4. In `engine.py`: add `RepositoryEngine.profile(root) -> RepositoryProfile`
   using classifier + metrics.
5. In `report.py`: implement `ReportRenderer.render(profile) -> str` producing
   a Markdown report with required sections (see Acceptance Criteria).
6. In `cli.py`: implement `inspect(path)` function that calls profile + render
   and writes output to `<path>/.ai/reports/inspect-<date>.md`.
7. In `bin/ai`: add `inspect` routing to `cli.py`.
8. Write `tests/test_repository_engine_inspect.sh`.

### Acceptance Criteria

- [ ] `bin/ai inspect .` completes without error on AI-Toolkit
- [ ] Report file written to `.ai/reports/inspect-<date>.md`
- [ ] Report contains sections: Summary, File Distribution, Language Distribution,
      Tech Stack, Entry Points, Test Coverage Ratio, Documentation Coverage
- [ ] `bin/ai inspect /path/to/trading-signals-platform` completes without error
- [ ] `bin/ai inspect /path/to/dropi` completes without error
- [ ] Integration test `test_repository_engine_inspect.sh` passes

### Expected Deliverables

- Working `bin/ai inspect <path>` command
- Markdown report for AI-Toolkit committed to `.ai/reports/`
- Integration test in `tests/`

---

## Issue #2 — Repository Engine: Dependency Graph

**Priority:** High  
**Sprint:** 1  
**Complexity:** Low

### Purpose

The inspect report must include a dependency summary (imports, requires, package.json deps,
requirements.txt, go.mod, etc.). This is a prerequisite for Knowledge Engine.

### Files to Modify / Create

| Action | File |
|---|---|
| Create | `lib/python/repository_engine/deps.py` |
| Extend | `lib/python/repository_engine/models.py` — add `DependencyMap` |
| Extend | `lib/python/repository_engine/report.py` — add Dependencies section |

**Source to consolidate:**
- `lib/python/executable_repository_intelligence/executable_dep_graph.py`
- `lib/python/dependency_engine/engine.py`

### Implementation Steps

1. In `deps.py`: scan `requirements.txt`, `package.json`, `go.mod`, `Gemfile` at root.
2. Add `dependencies: DependencyMap` field to `RepositoryProfile`.
3. Add Dependencies section to Markdown report.

### Acceptance Criteria

- [ ] Report includes dependency list for Python projects
- [ ] Report includes dependency list for Node projects when present
- [ ] Test verifies dependencies are non-empty for AI-Toolkit

---

## Issue #3 — CLI: Add `validate` Command

**Priority:** High  
**Sprint:** 3  
**Complexity:** Low (wiring only)

### Purpose

`bin/ai validate <path>` must run the validation engine and produce a scored report.
`ValidationEngine.validate()` already exists but only checks path existence.
This issue extends it to check canonical document presence and structure.

### Files to Modify / Create

| Action | File |
|---|---|
| Extend | `lib/python/validation_engine/engine.py` |
| Extend | `lib/python/validation_engine/models.py` |
| Create | `lib/python/validation_engine/report.py` |
| Create | `lib/python/validation_engine/cli.py` |
| Modify | `bin/ai` — add `validate` command |
| Create | `tests/test_validation_engine_cli.sh` |

### Implementation Steps

1. Add checks: README present, `bin/` present, `tests/` present, `docs/` present,
   `lib/` or `src/` present.
2. Score: `passed / total * 100`.
3. In `report.py`: render Markdown report with pass/fail table + score.
4. In `cli.py`: write report to `<path>/.ai/reports/validate-<date>.md`.
5. In `bin/ai`: add `validate` routing.

### Acceptance Criteria

- [ ] `bin/ai validate .` produces a scored report on AI-Toolkit
- [ ] Score is between 0 and 100
- [ ] Report written to `.ai/reports/validate-<date>.md`
- [ ] Test passes

---

## Issue #4 — CLI: Add `briefing generate` Command

**Priority:** High  
**Sprint:** 4  
**Complexity:** Low (wiring only — engine is implemented)

### Purpose

`bin/ai briefing generate <path>` must invoke `ExecutiveBriefingEngine.generate()` and
write the output. The engine is fully implemented; it is not wired to the CLI.

### Files to Modify / Create

| Action | File |
|---|---|
| Create | `lib/python/executive_briefing_engine/cli.py` |
| Modify | `bin/ai` — add `briefing generate` command |
| Create | `tests/test_executive_briefing_cli.sh` |

### Implementation Steps

1. In `cli.py`: call `ExecutiveBriefingEngine(repository=path).generate()`.
2. Write markdown output to `<path>/AI_CTO_EXECUTIVE_BRIEFING.md`.
3. In `bin/ai`: add routing for `briefing generate`.
4. Write test.

### Acceptance Criteria

- [ ] `bin/ai briefing generate .` runs without error
- [ ] `AI_CTO_EXECUTIVE_BRIEFING.md` is written to the target path
- [ ] Test passes

---

## Issue #5 — Knowledge Engine: Semantic Extraction

**Priority:** High  
**Sprint:** 2  
**Complexity:** High

### Purpose

`bin/ai knowledge extract <path>` must extract entities, relationships, and architectural zones
from a repository and persist them to `.ai/knowledge/graph.json`.

### Files to Modify / Create

| Action | File |
|---|---|
| Extend | `lib/python/knowledge_engine/engine.py` |
| Extend | `lib/python/knowledge_engine/models.py` |
| Create | `lib/python/knowledge_engine/extractor.py` |
| Create | `lib/python/knowledge_engine/graph.py` |
| Create | `lib/python/knowledge_engine/report.py` |
| Create | `lib/python/knowledge_engine/cli.py` |
| Modify | `bin/ai` — add `knowledge extract` command |
| Create | `tests/test_knowledge_engine_extract.sh` |

**Source to consolidate:**
- `lib/python/canonical_intelligence/engine.py`
- `lib/python/knowledge_graph/`
- `lib/python/knowledge_graph_v2/`
- `lib/python/semantic_repository_intelligence/`

### Implementation Steps

1. In `extractor.py`: walk files classified by Repository Engine. Extract:
   - modules (Python packages, directories with __init__.py)
   - entry points (bin/, main.py, app.py)
   - canonical documents (CANON-*.md)
   - relationships (import statements)
2. In `graph.py`: assemble into a `KnowledgeGraph` dataclass.
3. In `engine.py`: add `KnowledgeEngine.extract(root, profile=None) -> KnowledgeGraph`
   (accepts optional RepositoryProfile to avoid re-scanning).
4. In `report.py`: render Markdown summary.
5. In `cli.py`: call extract + write to `.ai/knowledge/graph.json` + Markdown summary.
6. In `bin/ai`: add routing.

### Acceptance Criteria

- [ ] `bin/ai knowledge extract .` runs without error on AI-Toolkit
- [ ] `.ai/knowledge/graph.json` is written
- [ ] Graph contains at least: module list, entry points, canonical doc list
- [ ] Same command works on Trading Signals Platform
- [ ] Test passes

---

## Issue #6 — Validation Engine: Consolidation

**Priority:** Medium  
**Sprint:** 3  
**Complexity:** Medium

### Purpose

Three overlapping validation subsystems exist: `audit_engine/`, `compliance_engine/`,
`development_validator/`. They must be consolidated into a single entry point under
`lib/python/validation_engine/`.

### Files to Modify / Create

| Action | File |
|---|---|
| Extend | `lib/python/validation_engine/engine.py` |
| Create | `lib/python/validation_engine/rules.py` |
| Create | `lib/python/validation_engine/score.py` |
| Deprecate | `lib/python/audit_engine/` (keep, redirect to validation_engine) |
| Deprecate | `lib/python/compliance_engine/` (keep, redirect to validation_engine) |

### Acceptance Criteria

- [ ] `ValidationEngine.validate()` runs all checks from all three subsystems
- [ ] Output score is numeric (0–100)
- [ ] Existing tests for audit_engine, compliance_engine, development_validator still pass

---

## Issue #7 — Runtime Server: End-to-End Test

**Priority:** Medium  
**Sprint:** 6  
**Complexity:** Low

### Purpose

`bin/runtime-server` and `lib/python/runtime/` are implemented but never tested
end-to-end. The server must start, respond to `/health`, and shut down cleanly.

### Files to Create

| Action | File |
|---|---|
| Create | `tests/test_runtime_server_e2e.sh` |

### Implementation Steps

1. Start server: `bin/runtime-server &`; capture PID.
2. Wait for `/health` to return 200.
3. Verify `/api/v1/runtime` returns JSON.
4. Send SIGTERM; verify clean exit (code 0).

### Acceptance Criteria

- [ ] Server starts in < 5 seconds
- [ ] `/health` returns `{"ready": true}`
- [ ] Server shuts down cleanly on SIGTERM
- [ ] Test passes in CI

---

## Issue #8 — Dashboard: Phase 1 (Inspect-First Local)

**Priority:** Medium  
**Sprint:** 1  
**Complexity:** Medium

### Purpose

A minimal local web UI that becomes usable as soon as inspect output exists.
It starts with the latest inspect report and an Engineering Session header, then grows with later engines.

See `DASHBOARD_IMPLEMENTATION_STRATEGY.md` for full phased plan.

### Acceptance Criteria

- [ ] `bin/ai dashboard serve` starts a local HTTP server on port 8080
- [ ] Dashboard displays latest inspect report
- [ ] Dashboard shows the Engineering Session header
- [ ] No external dependencies beyond Python stdlib
- [ ] Dashboard can evolve without redesign when later engine outputs are added

---

## Issue #9 — GitHub Actions: Weekly Briefing Cron

**Priority:** Low  
**Sprint:** 4  
**Complexity:** Low

### Purpose

Auto-generate and commit `AI_CTO_EXECUTIVE_BRIEFING.md` weekly via GitHub Actions.

### Files to Create

| Action | File |
|---|---|
| Create | `.github/workflows/weekly_briefing.yml` |

### Acceptance Criteria

- [ ] Workflow runs every Sunday at 08:00 UTC
- [ ] Workflow runs `bin/ai briefing generate .`
- [ ] Commits and pushes the updated briefing to main

---

## Issue #10 — AI Agent + Provider Layer

**Priority:** Low  
**Sprint:** 6  
**Complexity:** High

See `AI_PROVIDER_INTEGRATION_PLAN.md` for full design.

### Purpose

A combined AI Agent + Provider path through which every engine that needs AI-assisted inference must pass.
Engines communicate with agents. Agents communicate with providers. No engine communicates directly with an AI provider.

### Acceptance Criteria

- [ ] existing `agent_runtime` / `agents` foundations are aligned into an Agent Layer contract
- [ ] `lib/python/ai_provider/` module exists
- [ ] engines request AI assistance through agents rather than direct provider calls
- [ ] at least one provider is implemented (stub or Ollama)
- [ ] tests verify both agent and provider interface contracts


---

## Issue #11 — Project Manager and Multi-Repository Context

**Priority:** Medium  
**Sprint:** 5  
**Complexity:** Medium

### Purpose

AI-Toolkit needs an explicit Project Manager runtime service so project registration, workspace selection, repository metadata, lifecycle state, and active context are not scattered across the Dashboard and runtime.

This sprint builds on the Engineering Session already introduced earlier in the Dashboard and validation track.
Its purpose is to connect that session to multi-repository project management, context switching, and persistent project-level metadata.

### Files to Modify / Create

| Action | File |
|---|---|
| Extend | existing workspace state / registry modules |
| Create or extend | Project Manager runtime service module |
| Extend | dashboard session/context handling |
| Extend | runtime state persistence for Engineering Session |
| Create | tests for project registration and active-context switching |

### Acceptance Criteria

- [ ] project registration works without introducing a new engine type
- [ ] active repository and workspace can be selected explicitly
- [ ] Project Manager reuses the existing Engineering Session fields during context switching
- [ ] Dashboard reflects active-context changes consistently
- [ ] multi-repository Dashboard work reuses this service instead of duplicating state logic

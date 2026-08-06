# Executable Roadmap

**Status:** Active  
**Created:** 2026-08-06  
**Philosophy:** Every milestone ends with working software, and the Dashboard evolves with the engines.

---

## Roadmap Overview

```
M1: Repository Inspection Foundation   bin/ai inspect + dashboard serve
M2: Knowledge Expansion                bin/ai knowledge extract
M3: Validation + Engineering Session   bin/ai validate
M4: Executive Briefing + Actions       bin/ai briefing generate
M5: Project Manager + Multi-Repo       project registration + context switching
M6: AI Agent + Provider Layer          optional AI-assisted engine enrichment
M7: Runtime Operations                 bin/runtime-server
M8: Telegram + Railway                 notifications + deployment
M9: GitHub Integration                 PR/issue/workflow triggers
```

The Dashboard is a parallel companion track from M1 onward.
It does not wait until the engine track is complete.

---

## M1 — Repository Inspection Foundation

**Objective:** Any repository can be inspected with a single command, and the first Dashboard view becomes usable immediately from that output.

**Sprint:** 1 (2 weeks)

**Deliverables:**
- `lib/python/repository_engine/classifier.py`
- `lib/python/repository_engine/metrics.py`
- `lib/python/repository_engine/deps.py`
- `lib/python/repository_engine/report.py`
- `lib/python/repository_engine/cli.py`
- `bin/ai inspect <path>` CLI command
- Markdown report written to `<path>/.ai/reports/inspect-<date>.md`
- `bin/ai dashboard serve` CLI command
- inspect-first local Dashboard with Engineering Session header

**Tests:**
- `tests/test_repository_engine_inspect.sh`
- `tests/test_dashboard_phase1.sh`

**Validation repositories:**
- AI-Toolkit
- Trading Signals Platform
- DROPi

**Acceptance:**
- `bin/ai inspect .` produces a valid Markdown report
- `bin/ai dashboard serve` displays the latest inspect report without error
- Dashboard shows current Engineering Session context

---

## M2 — Knowledge Expansion

**Objective:** Extract repository knowledge and expand the Dashboard beyond inspection-only use.

**Sprint:** 2 (2 weeks)

**Prerequisite:** M1 complete

**Deliverables:**
- `lib/python/knowledge_engine/extractor.py`
- `lib/python/knowledge_engine/graph.py`
- `lib/python/knowledge_engine/report.py`
- `lib/python/knowledge_engine/cli.py`
- `bin/ai knowledge extract <path>` CLI command
- Knowledge graph written to `<path>/.ai/knowledge/graph.json`
- Dashboard knowledge surface linked from inspect results

**Tests:**
- `tests/test_knowledge_engine_extract.sh`

**Acceptance:**
- `bin/ai knowledge extract .` produces repository knowledge output
- Dashboard can surface inspect and knowledge outputs together

---

## M3 — Validation + Engineering Session

**Objective:** Produce validation scores and unify the active working context.

**Sprint:** 3 (2 weeks)

**Prerequisite:** M2 complete

**Deliverables:**
- `bin/ai validate <path>` CLI command
- scored validation report written to `<path>/.ai/reports/validate-<date>.md`
- unified Engineering Session model carrying active project, repository, branch, workspace, issue, sprint, AI provider, and engineering task
- Dashboard validation surface using the same session context

**Tests:**
- `tests/test_validation_engine_cli.sh`
- Engineering Session state tests added to runtime or dashboard coverage

**Acceptance:**
- `bin/ai validate .` produces a scored report
- active context remains consistent across the Dashboard surfaces built so far

---

## M4 — Executive Briefing + Dashboard Actions

**Objective:** Turn the Dashboard into an operational workspace.

**Sprint:** 4 (1 week)

**Prerequisite:** M3 complete

**Deliverables:**
- `lib/python/executive_briefing_engine/cli.py`
- `bin/ai briefing generate <path>` CLI command
- `AI_CTO_EXECUTIVE_BRIEFING.md` generated in target repository
- dashboard action panel for inspect, validate, and briefing generation
- dashboard job history and job state display
- `.github/workflows/weekly_briefing.yml`

**Tests:**
- `tests/test_executive_briefing_cli.sh`
- dashboard action/job tests

**Acceptance:**
- `bin/ai briefing generate .` produces a briefing from real data
- Dashboard can trigger inspect, validate, and briefing runs and show their status

---

## M5 — Project Manager + Multi-Repository Dashboard

**Objective:** Make repository management and active context selection first-class product capabilities.

**Sprint:** 5 (2 weeks)

**Prerequisite:** M4 complete

**Deliverables:**
- Project Manager runtime service built from existing workspace registry/state foundations
- project registration and repository metadata management
- workspace selection and active-context switching
- multi-repository Dashboard views
- repository browser and project-level navigation foundation

**Tests:**
- project registration tests
- repository context switching tests
- multi-repository dashboard tests

**Acceptance:**
- Owner can manage multiple repositories from one dashboard
- Active Engineering Session updates correctly when project context changes

---

## M6 — AI Agent + Provider Layer

**Objective:** Add optional AI-assisted engine enrichment without coupling engines directly to providers.

**Sprint:** 6 (2 weeks)

**Prerequisite:** M5 complete

**Deliverables:**
- aligned Agent Layer using `lib/python/agent_runtime/` and `lib/python/agents/`
- `lib/python/ai_provider/` provider abstraction layer
- `StubProvider`
- at least one real provider implementation
- agent-to-provider execution path for optional engine enrichment
- Dashboard visibility into agent and provider status

**Tests:**
- provider interface tests
- stub provider tests
- agent/provider integration tests

**Acceptance:**
- engines remain functional without AI providers
- all provider traffic goes through the Provider Layer
- AI-assisted paths go through the Agent Layer first

---

## M7 — Runtime Operations

**Objective:** Validate and expose the continuously running operational substrate.

**Sprint:** 6 (parallel completion) / 7

**Prerequisite:** M6 in progress or complete

**Deliverables:**
- `tests/test_runtime_server_e2e.sh`
- Runtime server responds to `/health` and runtime API endpoints
- Dashboard Runtime, Logs, Jobs, Monitoring, and Metrics surfaces

**Tests:**
- `tests/test_runtime_server_e2e.sh`
- runtime operational view tests

**Acceptance:**
- `bin/runtime-server` starts, responds, and shuts down cleanly
- Dashboard exposes runtime state and job evidence

---

## M8 — Telegram + Railway

**Objective:** Extend operational visibility and notifications to hosted and remote channels.

**Sprint:** 7 (1 week)

**Prerequisite:** M7 complete

**Deliverables:**
- Telegram notifications for inspect / validate / briefing completion
- Runtime deployed on Railway with health checks
- Dashboard surfaces Telegram and Railway status

**Tests:**
- `tests/test_runtime_telegram.sh`
- `tests/test_railway_bootstrap.sh`

**Acceptance:**
- Telegram receives operational notifications
- Railway deployment passes health checks

---

## M9 — GitHub Integration

**Objective:** Close the loop between repository hosting events and AI-Toolkit operations.

**Sprint:** 8 (2 weeks)

**Prerequisite:** M8 complete

**Deliverables:**
- GitHub-triggered inspect/validate flows
- PR validation feedback publication
- Dashboard GitHub surface for workflow and review state

**Tests:**
- manual or automated GitHub integration validation

**Acceptance:**
- Opening a PR or relevant repository event triggers the planned AI-Toolkit workflow
- Dashboard shows GitHub-connected operational state

---

## Milestone Summary Table

| # | Milestone | Primary command / capability | Sprint | Prerequisite |
|---|---|---|---|---|
| M1 | Repository Inspection Foundation | `bin/ai inspect`, `bin/ai dashboard serve` | 1 | — |
| M2 | Knowledge Expansion | `bin/ai knowledge extract` | 2 | M1 |
| M3 | Validation + Engineering Session | `bin/ai validate` | 3 | M2 |
| M4 | Executive Briefing + Actions | `bin/ai briefing generate` | 4 | M3 |
| M5 | Project Manager + Multi-Repo | project/context management | 5 | M4 |
| M6 | AI Agent + Provider Layer | provider-assisted engine enrichment | 6 | M5 |
| M7 | Runtime Operations | `bin/runtime-server` | 6/7 | M6 |
| M8 | Telegram + Railway | notifications + hosting | 7 | M7 |
| M9 | GitHub Integration | repository event triggers | 8 | M8 |

---

## What This Roadmap Does Not Include

- additional canonical specifications
- architecture redesign
- speculative cloud-only platform work
- commercial platform features
- dashboard-only logic that duplicates engines

---

## Start implementing Sprint 1

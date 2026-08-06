# Executable Roadmap

**Status:** Active  
**Created:** 2026-08-06  
**Philosophy:** Every milestone ends with working software, not documentation.

---

## Roadmap Overview

```
M1: Repository Engine     bin/ai inspect
M2: Knowledge Engine      bin/ai knowledge extract
M3: Validation Engine     bin/ai validate
M4: Executive Briefing    bin/ai briefing generate
M5: Dashboard Phase 1     bin/ai dashboard serve
M6: AI Provider Layer     provider abstraction
M7: Runtime Server        bin/runtime-server (end-to-end)
M8: Telegram              notifications + commands
M9: Railway Deployment    production hosting
M10: GitHub Integration   PR/issue triggers
```

Each milestone is a prerequisite for the next. No milestone begins until the previous
one passes acceptance tests on all three validation repositories.

---

## M1 — Repository Engine

**Objective:** Any repository can be inspected with a single command.

**Sprint:** 1 (2 weeks)

**Deliverables:**

- `lib/python/repository_engine/classifier.py`
- `lib/python/repository_engine/metrics.py`
- `lib/python/repository_engine/deps.py`
- `lib/python/repository_engine/report.py`
- `lib/python/repository_engine/cli.py`
- `bin/ai inspect <path>` CLI command
- Markdown report written to `<path>/.ai/reports/inspect-<date>.md`

**Tests:**

- `tests/test_repository_engine_inspect.sh`

**Validation repositories:**

- AI-Toolkit (self-inspection)
- Trading Signals Platform
- DROPi

**Acceptance:**

`bin/ai inspect .` produces a valid Markdown report on all three repositories.

---

## M2 — Knowledge Engine

**Objective:** Semantic knowledge graph extracted from any repository.

**Sprint:** 2 (2 weeks)

**Prerequisite:** M1 complete

**Deliverables:**

- `lib/python/knowledge_engine/extractor.py`
- `lib/python/knowledge_engine/graph.py`
- `lib/python/knowledge_engine/report.py`
- `lib/python/knowledge_engine/cli.py`
- `bin/ai knowledge extract <path>` CLI command
- Knowledge graph written to `<path>/.ai/knowledge/graph.json`

**Tests:**

- `tests/test_knowledge_engine_extract.sh`

**Validation repositories:**

- AI-Toolkit
- Trading Signals Platform
- DROPi

**Acceptance:**

`bin/ai knowledge extract .` produces a `graph.json` containing modules, entry points,
and canonical document references for all three repositories.

---

## M3 — Architecture Revision Cycle

**Objective:** Update only the specs that M1 and M2 proved wrong or incomplete.

**Sprint:** 3 (1 week)

**Prerequisite:** M1 and M2 complete

**Deliverables:**

- `docs/audits/PHASE_1_2_LEARNINGS.md` — list of spec changes made and why
- Only revise specs that implementation referenced and found incorrect

**Constraint:** No new CANON-XXX documents. Revisions only.

---

## M4 — Validation Engine

**Objective:** Any repository can be scored for canonical conformance.

**Sprint:** 4 (2 weeks)

**Prerequisite:** M2 complete

**Deliverables:**

- `lib/python/validation_engine/rules.py` (extended from stub)
- `lib/python/validation_engine/score.py`
- `lib/python/validation_engine/report.py`
- Consolidation of `audit_engine/`, `compliance_engine/`, `development_validator/`
- `bin/ai validate <path>` CLI command
- Scored report written to `<path>/.ai/reports/validate-<date>.md`

**Tests:**

- `tests/test_validation_engine_cli.sh`

**Validation repositories:**

- AI-Toolkit
- Trading Signals Platform
- DROPi

**Acceptance:**

`bin/ai validate .` produces a scored report (0–100) on all three repositories.

---

## M5 — Executive Briefing

**Objective:** Auto-generated executive briefing from real data.

**Sprint:** 5 (1 week)

**Prerequisite:** M4 complete

**Deliverables:**

- `lib/python/executive_briefing_engine/cli.py` (wiring only — engine exists)
- `bin/ai briefing generate <path>` CLI command
- `AI_CTO_EXECUTIVE_BRIEFING.md` generated in target repository
- `.github/workflows/weekly_briefing.yml` — cron job

**Tests:**

- `tests/test_executive_briefing_cli.sh`

**Validation repositories:**

- AI-Toolkit

**Acceptance:**

`bin/ai briefing generate .` produces a briefing that includes real data from
the inspect and validate reports. Briefing is automatically committed weekly.

---

## M6 — Dashboard Phase 1

**Objective:** Read-only local web dashboard displaying engine outputs.

**Sprint:** 6 (2 weeks)

**Prerequisite:** M5 complete

**Deliverables:**

- `lib/python/dashboard/__init__.py`
- `lib/python/dashboard/reader.py`
- `lib/python/dashboard/renderer.py`
- `lib/python/dashboard/server.py`
- `bin/ai dashboard serve` CLI command
- HTML dashboard served on port 8080
- Three panels: Inspect, Validate, Briefing

**Tests:**

- `tests/test_dashboard_phase1.sh`

**Validation repositories:**

- AI-Toolkit (local)

**Acceptance:**

`bin/ai dashboard serve` starts a local server. Dashboard displays reports from
`.ai/reports/` without error. No external dependencies.

---

## M7 — AI Provider Layer + Runtime Server

**Objective:** Provider abstraction layer and end-to-end runtime server test.

**Sprint:** 7 (2 weeks)

**Prerequisite:** M6 complete

**Deliverables:**

- `lib/python/ai_provider/` module (full structure as per `AI_PROVIDER_INTEGRATION_PLAN.md`)
- `StubProvider` (always available)
- `OllamaProvider` (local)
- `OpenAIProvider`
- `AnthropicProvider`
- `tests/test_runtime_server_e2e.sh`
- Runtime server responds to `/health`, `/api/v1/runtime`

**Tests:**

- `tests/test_ai_provider_stub.sh`
- `tests/test_ai_provider_ollama.sh` (requires Ollama, skipped if not available)
- `tests/test_runtime_server_e2e.sh`

**Acceptance:**

`bin/runtime-server` starts, responds to `/health`, shuts down cleanly.
`StubProvider.complete()` returns a response.
All provider calls go through `ProviderInterface`.

---

## M8 — Telegram Integration

**Objective:** Receive notifications and send basic commands via Telegram.

**Sprint:** 8 (1 week)

**Prerequisite:** M7 complete

**Deliverables:**

- `lib/python/runtime/telegram.py` extended with outbound notification
- Notifications sent when inspect / validate / briefing complete
- Basic command: `/status` returns runtime health
- Configuration via `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` env vars

**Tests:**

- `tests/test_runtime_telegram.sh` (existing, extend)

**Acceptance:**

When `bin/ai inspect .` completes, a Telegram message is sent with a summary.
`/status` command returns `{"ready": true}`.

---

## M9 — Railway Deployment

**Objective:** Runtime server running continuously on Railway.

**Sprint:** 9 (1 week)

**Prerequisite:** M8 complete

**Deliverables:**

- `railway.json` updated to confirmed working configuration
- `requirements.txt` complete with all production dependencies
- Deployed and responding to health checks on Railway URL
- Environment variables configured in Railway dashboard

**Tests:**

- `tests/test_railway_bootstrap.sh` (existing, verify)
- Manual health check against deployed Railway URL

**Acceptance:**

`https://<railway-url>/health` returns `{"ready": true}`.
Server restarts automatically on crash.

---

## M10 — GitHub Integration

**Objective:** Engine runs triggered by GitHub events (PR open, push to main).

**Sprint:** 10 (2 weeks)

**Prerequisite:** M9 complete

**Deliverables:**

- `.github/workflows/inspect_on_push.yml` — run inspect on push to main
- `.github/workflows/validate_on_pr.yml` — run validate on PR, post result as comment
- PR comment includes validation score and summary

**Tests:**

- Manual test via test PR

**Acceptance:**

Opening a PR on AI-Toolkit triggers validation. Result posted as PR comment with score.

---

## Milestone Summary Table

| # | Milestone | Command | Sprint | Prerequisite |
|---|---|---|---|---|
| M1 | Repository Engine | `bin/ai inspect` | 1 | — |
| M2 | Knowledge Engine | `bin/ai knowledge extract` | 2 | M1 |
| — | Architecture Revision | — | 3 | M1+M2 |
| M4 | Validation Engine | `bin/ai validate` | 4 | M2 |
| M5 | Executive Briefing | `bin/ai briefing generate` | 5 | M4 |
| M6 | Dashboard Phase 1 | `bin/ai dashboard serve` | 6 | M5 |
| M7 | AI Provider + Runtime | `bin/runtime-server` | 7 | M6 |
| M8 | Telegram | — | 8 | M7 |
| M9 | Railway Deployment | — | 9 | M8 |
| M10 | GitHub Integration | — | 10 | M9 |

---

## What This Roadmap Does Not Include

- Additional canonical specifications
- New governance documents
- CSL compiler (deferred — no engine needs it yet)
- Commercial platform features (billing, licensing, identity)
- Multi-tenant cloud platform
- Autonomous governance

These are deferred until implementation demonstrates a real need.

---

## Start implementing Issue #1

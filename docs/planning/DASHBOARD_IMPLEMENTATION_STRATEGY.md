# Dashboard Implementation Strategy

**Status:** Planning  
**Created:** 2026-08-06  
**First phase starts:** Sprint 6 (after inspect, knowledge extract, validate are complete)

---

## Purpose

The Admin Dashboard is not a reporting interface.

It is the operational control center of AI-Toolkit.

Its purpose is to operate every engine from one place, show real-time status, and allow
the owner to trigger inspection, validation, knowledge extraction, and briefing generation
without using the CLI.

---

## What Already Exists (reusable)

| Asset | Location | Reusable for |
|---|---|---|
| Runtime server skeleton | `lib/python/runtime/` | HTTP server backend |
| Runtime REST API spec | `docs/openapi/runtime-api-v1.yaml` | API contract |
| GraphQL schema | `docs/graphql/runtime-schema.graphql` | Alternative API contract |
| Health endpoint | `lib/python/runtime/health.py` | Dashboard health indicator |
| Scheduler | `lib/python/runtime/scheduler.py` | Trigger scheduled runs |
| Metrics | `lib/python/runtime/metrics.py` | Dashboard metrics panel |
| Reports storage | `.ai/reports/` (per-repo convention) | Report display |
| Executive briefing engine | `lib/python/executive_briefing_engine/` | Briefing panel |
| Validation engine | `lib/python/validation_engine/` | Validation panel |
| Repository engine | `lib/python/repository_engine/` | Inspect panel |

No dashboard UI framework is used. The dashboard is pure HTML + CSS served by the existing
Python runtime HTTP server. No JavaScript framework. No build step.

---

## Phased Implementation Strategy

### Phase 1 — Read-Only Local Dashboard (Sprint 6)

**Goal:** Display existing report files in a browser. No actions.

**Implementation:**

1. Add a `dashboard` route to the runtime HTTP server (`lib/python/runtime/`).
2. Implement `lib/python/dashboard/reader.py` — reads `.ai/reports/*.md`, converts to HTML.
3. Implement `lib/python/dashboard/renderer.py` — renders a single-page HTML dashboard
   with three panels: Inspect, Validate, Briefing.
4. Add `bin/ai dashboard serve [--port 8080]` CLI command.

**Engine dependency:** Repository Engine (Issue #1) must be complete.

**Acceptance criteria:**
- `bin/ai dashboard serve` starts a server on port 8080
- Dashboard displays latest inspect report in readable HTML
- Dashboard displays latest validate report
- Dashboard displays latest briefing
- No external dependencies beyond Python stdlib
- No JavaScript framework

**Files created:**
```
lib/python/dashboard/__init__.py
lib/python/dashboard/reader.py
lib/python/dashboard/renderer.py
lib/python/dashboard/server.py
tests/test_dashboard_phase1.sh
```

---

### Phase 2 — Action Panel (Sprint 7)

**Goal:** Allow the owner to trigger engine runs from the browser.

**Prerequisite:** Phase 1 complete.

**Implementation:**

1. Add a form-based action panel to the HTML dashboard (no JS required — plain HTML forms).
2. Add POST handlers to the runtime server for:
   - `POST /inspect` — runs `bin/ai inspect <target>`
   - `POST /validate` — runs `bin/ai validate <target>`
   - `POST /briefing` — runs `bin/ai briefing generate <target>`
3. Show job status (running / complete / error) by polling a status endpoint.
4. Persist job history to `.ai/runtime/sessions/`.

**Acceptance criteria:**
- Owner can click "Inspect" in the browser and see results appear
- Job history is shown in the dashboard
- All actions also available via CLI (no dashboard-only features)

**Files modified:**
```
lib/python/dashboard/server.py   (add POST handlers)
lib/python/dashboard/renderer.py (add action panel)
lib/python/runtime/job_queue.py  (extend for dashboard jobs)
tests/test_dashboard_phase2.sh
```

---

### Phase 3 — Multi-Repository Panel (Sprint 8+)

**Goal:** Manage multiple repositories from one dashboard.

**Prerequisite:** Phase 2 complete + AI Provider Layer complete.

**Implementation:**

1. Add workspace registry integration (`lib/python/workspace_manager/`).
2. Show a list of registered repositories.
3. Show health indicators for each repository.
4. Allow running any engine against any registered repository.
5. Show knowledge graph visualization (simple text-based tree, no JS graphing library).

**Acceptance criteria:**
- Dashboard shows AI-Toolkit, Trading Signals Platform, and DROPi simultaneously
- Health indicator per repository (green/yellow/red)
- Owner can trigger inspection on any repository from dashboard

---

### Phase 4 — Telegram Control Bridge (Sprint 9+)

**Goal:** Receive dashboard notifications via Telegram.

**Prerequisite:** Phase 3 complete + Telegram integration complete.

**Implementation:**

1. Wire `lib/python/runtime/` Telegram connector to dashboard events.
2. Send notification when an inspection or briefing completes.
3. Allow Telegram commands to trigger inspections (not full control — notifications only
   in this phase).

---

## Design Constraints

1. No JavaScript framework. No React. No Vue. No build step.
2. No external CSS framework. Plain CSS only.
3. Dashboard must work with Python stdlib only (no Flask, no FastAPI, no Jinja2)
   until a dependency is strictly necessary.
4. Dashboard is always a consumer of engine outputs — it never implements engine logic.
5. Dashboard evolves together with the engines. It must never wait for all engines.
6. Every dashboard panel corresponds to exactly one engine command.

---

## Panel Map (target state)

| Panel | Engine Command | Implemented in Phase |
|---|---|---|
| Inspect | `bin/ai inspect` | 1 |
| Validate | `bin/ai validate` | 1 |
| Briefing | `bin/ai briefing generate` | 1 |
| Knowledge Graph | `bin/ai knowledge extract` | 2 |
| Job History | — (internal) | 2 |
| Multi-Repository | workspace manager | 3 |
| Telegram Notifications | Telegram connector | 4 |
| AI Provider Status | provider registry | 4 |

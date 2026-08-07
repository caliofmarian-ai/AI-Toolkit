# Dashboard Implementation Strategy

**Status:** Planning  
**Created:** 2026-08-06  
**First phase starts:** Sprint 1 (as soon as Repository Engine produces the first inspect report)

---

## Purpose

The Dashboard is not a reporting interface added after the engines are finished.

It is the operational control center of AI-Toolkit.
It must become usable as soon as Repository Engine starts producing output and then evolve together with every engine and runtime capability.

---

## Alignment Decision

### Dashboard Position
The Dashboard shall evolve in parallel with the engines.
It shall not wait until inspect, knowledge, validate, and briefing are all complete.

The first Dashboard value appears the moment inspect output exists.
Each subsequent sprint expands the same Dashboard instead of creating a later visualization layer.

### Project Manager Decision
AI-Toolkit requires an explicit Project Manager.
It should not be a separate scoring or analysis engine.
It should be a runtime service, backed by the existing workspace registry and state-management capabilities, and surfaced through the Dashboard Projects and Engineering Workspace areas.

Responsibilities:
- project registration;
- repository metadata;
- workspace selection;
- lifecycle state;
- active project context;
- project configuration.

### Engineering Session Decision
AI-Toolkit requires an explicit Engineering Session.
The Engineering Session is the current working context managed by the Project Manager service and surfaced throughout the Dashboard.

The Engineering Session always carries explicit values for:
- active project;
- active repository;
- active branch;
- active workspace;
- active issue;
- active sprint;
- active AI provider;
- active engineering task.

### AI Agent Layer Decision
AI-Toolkit also requires an AI Agent Layer.
This does not replace the existing engines.
It gives engines a stable way to request optional AI-assisted reasoning without coupling engine logic to provider-specific prompts or APIs.

The recommended implementation is to use the existing `lib/python/agent_runtime/` and `lib/python/agents/` structure as the internal Agent Layer, with the Provider Layer beneath it.

---

## What Already Exists (reusable)

| Asset | Location | Reusable for |
|---|---|---|
| Runtime server skeleton | `lib/python/runtime/` | HTTP server backend |
| Health endpoint | `lib/python/runtime/health.py` | Dashboard health indicator |
| Scheduler | `lib/python/runtime/scheduler.py` | Trigger scheduled runs |
| Metrics | `lib/python/runtime/metrics.py` | Dashboard metrics panel |
| Reports storage | `.ai/reports/` | Dashboard display panels |
| Executive briefing engine | `lib/python/executive_briefing_engine/` | Briefing panel |
| Validation engine | `lib/python/validation_engine/` | Validation panel |
| Repository engine | `lib/python/repository_engine/` | Inspect panel |
| Workspace manager | `lib/python/workspace_manager/` | initial project discovery |
| Workspace registry and state manager | `lib/python/workspace_orchestrator/` | Project Manager foundation |
| Agent runtime | `lib/python/agent_runtime/` | Agent orchestration foundation |
| Existing agents | `lib/python/agents/` | Agent Layer foundation |

No dashboard UI framework is required. The dashboard remains pure HTML + CSS served by the existing Python runtime HTTP server. No JavaScript framework. No build step.

---

## Phased Implementation Strategy

### Phase 1 — Inspect-First Dashboard (Sprint 1)

**Goal:** Show the first usable Dashboard as soon as inspect output exists.

**Implementation:**
1. Add a `dashboard` route to the runtime HTTP server.
2. Render a local dashboard page that displays the latest inspect report.
3. Add a persistent Engineering Session header showing current project, repository, branch, workspace, issue, sprint, AI provider, and engineering task.
4. Add `bin/ai dashboard serve [--port 8080]` CLI command.

**Engine dependency:** Repository Engine output only.

**Acceptance criteria:**
- `bin/ai dashboard serve` starts a server on port 8080
- Dashboard displays the latest inspect report in readable HTML
- Dashboard shows the Engineering Session header
- No external dependencies beyond Python stdlib
- No JavaScript framework

---

### Phase 2 — Dashboard Grows with Knowledge and Validation (Sprint 2–3)

**Goal:** Expand the same Dashboard as new engine outputs become available.

**Implementation:**
1. Add Knowledge and Validation panels or pages as soon as those outputs exist.
2. Add repository navigation links so the user can move from inspect to knowledge to validation.
3. Keep the Engineering Session visible on every page.

**Acceptance criteria:**
- Dashboard shows inspect, knowledge, and validation outputs when available
- The same dashboard URL remains the operational entry point
- The Dashboard remains repository-aware and session-aware

---

### Phase 3 — Briefing, Action Panel, and Job History (Sprint 4)

**Goal:** Turn the Dashboard into an operational workspace instead of a read-only display.

**Implementation:**
1. Add executive briefing panels.
2. Add a form-based action panel for inspect, validate, and briefing generation.
3. Show job status and recent job history.
4. Persist job history to runtime state.

**Acceptance criteria:**
- Owner can trigger inspect, validate, and briefing from the Dashboard
- Dashboard shows running, complete, and failed jobs
- All actions remain available via CLI

---

### Phase 4 — Project Manager and Multi-Repository Control (Sprint 5)

**Goal:** Make project and repository context explicit and manageable.

**Implementation:**
1. Introduce the Project Manager runtime service backed by workspace registry/state management.
2. Add project registration, workspace selection, and active-context switching.
3. Show multiple repositories and repository health in the Dashboard.
4. Make Engineering Session changes visible immediately across Dashboard pages.

**Acceptance criteria:**
- Owner can register and select projects from the Dashboard
- Dashboard shows active project and repository context persistently
- Multiple repositories can be managed from one dashboard

---

### Phase 5 — AI Agent, Provider, Runtime, and Integration Visibility (Sprint 6+)

**Goal:** Add the internal AI operating surfaces required for later scale without changing engine architecture.

**Implementation:**
1. Introduce the AI Agent Layer using existing runtime/agent modules.
2. Surface agent activity, provider status, and runtime health in the Dashboard.
3. Add Telegram, Railway, and GitHub operational visibility as integrations become available.
4. Expand Logs, Jobs, Monitoring, and Metrics pages.

**Acceptance criteria:**
- Dashboard shows agent and provider status without bypassing engine logic
- Runtime and integration health are visible from the Dashboard
- The Dashboard remains the operational face of AI-Toolkit as capabilities grow

---

## Design Constraints

1. No JavaScript framework. No React. No Vue. No build step.
2. No external CSS framework. Plain CSS only.
3. Dashboard must work with Python stdlib only until a dependency is strictly necessary.
4. Dashboard consumes engine outputs and runtime state. It does not replace engine logic.
5. Dashboard evolves together with the engines. It never waits for all engines to finish first.
6. Project Manager remains a runtime service and Dashboard capability, not a separate analysis engine.
7. Engineering Session is persistent operational state, not transient page state.
8. Agent Layer remains optional enhancement infrastructure. Rule-based engine behavior must still work without AI providers.

---

## Panel Map (aligned target state)

| Panel / Capability | Primary source | First phase |
|---|---|---|
| Inspect | `bin/ai inspect` | 1 |
| Engineering Session Header | Project Manager runtime service | 1 |
| Knowledge | `bin/ai knowledge extract` | 2 |
| Validation | `bin/ai validate` | 2 |
| Executive Briefing | `bin/ai briefing generate` | 3 |
| Action Panel | runtime server + CLI commands | 3 |
| Job History | runtime job state | 3 |
| Project Manager | workspace registry/state manager | 4 |
| Multi-Repository | Project Manager + Repository Engine | 4 |
| AI Agent Status | `agent_runtime` / `agents` | 5 |
| AI Provider Status | provider registry | 5 |
| Runtime / Logs / Metrics | runtime services | 5 |
| Telegram / Railway / GitHub | integration connectors | 5 |

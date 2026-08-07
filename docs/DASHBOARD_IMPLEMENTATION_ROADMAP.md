# AI-Toolkit Dashboard Implementation Roadmap

## Purpose
This roadmap aligns Dashboard delivery with implementation readiness.

The Dashboard is the operational face of AI-Toolkit.
It becomes usable as soon as Repository Engine produces output and then evolves together with the engines, runtime services, Project Manager, and AI operating layers.

Every phase ends with a working Dashboard.

## Planning Baseline Reused
This roadmap reuses and aligns:
- `docs/planning/DASHBOARD_IMPLEMENTATION_STRATEGY.md`
- `docs/planning/EXECUTABLE_IMPLEMENTATION_PLAN.md`
- `docs/planning/EXECUTABLE_ROADMAP.md`
- `docs/planning/AI_PROVIDER_INTEGRATION_PLAN.md`
- `docs/planning/IMPLEMENTATION_BACKLOG.md`
- `docs/planning/SPRINT_001_PLAN.md`

## Phase 1 — Inspect-First Dashboard
**Working dashboard outcome**  
A local Dashboard that opens in the browser, shows the latest inspect report, and exposes the current Engineering Session header.

**Required engines/services**  
- Runtime
- Repository Engine
- initial Engineering Session state

**Implementation tasks**  
- expose a local dashboard route through the runtime server;
- render the latest inspect report in readable HTML;
- show active project, repository, branch, workspace, issue, sprint, AI provider, and engineering task in a persistent session header;
- add minimal navigation shell for future pages.

**Acceptance criteria**  
- `bin/ai dashboard serve` starts locally;
- the Dashboard shows the latest inspect output;
- the Engineering Session header is visible;
- no front-end framework or separate build system is introduced.

**Tests**  
- dashboard startup test;
- inspect panel rendering test;
- session header rendering test.

---

## Phase 2 — Knowledge Expansion
**Working dashboard outcome**  
The same Dashboard now supports repository inspection and knowledge review together.

**Required engines/services**  
- Runtime
- Repository Engine
- Knowledge Engine
- Engineering Session state

**Implementation tasks**  
- add Knowledge navigation and page or panel support;
- link inspect findings to knowledge outputs;
- keep session context visible while moving between repository views.

**Acceptance criteria**  
- the user can open inspect and knowledge outputs from the same Dashboard;
- repository context remains consistent across both surfaces.

**Tests**  
- knowledge page rendering test;
- repository-context persistence test.

---

## Phase 3 — Validation and Session-Aware Operations
**Working dashboard outcome**  
The Dashboard becomes session-aware across inspect, knowledge, and validation views.

**Required engines/services**  
- Runtime
- Repository Engine
- Knowledge Engine
- Validation Engine
- Engineering Session persistence

**Implementation tasks**  
- add Validation page or panel support;
- unify the Engineering Session as shared operational state;
- make validation results repository-aware and session-aware.

**Acceptance criteria**  
- the user can inspect validation outputs in the current repository context;
- active session values remain consistent while navigating the Dashboard.

**Tests**  
- validation panel rendering test;
- Engineering Session consistency test.

---

## Phase 4 — Executive Briefings, Actions, and Jobs
**Working dashboard outcome**  
A working operational workspace where the user can trigger core flows and watch them execute.

**Required engines/services**  
- Runtime
- Repository Engine
- Validation Engine
- Executive Briefing Engine
- job queue and scheduler services

**Implementation tasks**  
- add Executive Briefings surface;
- add action controls for inspect, validate, and briefing generation;
- show job state and recent execution history;
- keep the Dashboard action model aligned with CLI commands.

**Acceptance criteria**  
- the user can trigger inspect, validate, and briefing actions from the Dashboard;
- the Dashboard shows queued, running, completed, and failed jobs;
- all actions remain available outside the Dashboard as well.

**Tests**  
- action submission test;
- job lifecycle rendering test;
- briefing panel population test.

---

## Phase 5 — Project Manager and Multi-Repository Control
**Working dashboard outcome**  
The Dashboard becomes the control center for projects, repositories, and active context.

**Required engines/services**  
- Runtime
- Project Manager runtime service
- workspace registry/state foundations
- Repository Engine
- report publication services

**Implementation tasks**  
- implement Project Manager as a runtime service that reuses workspace registry and state management;
- add project registration, repository metadata, workspace selection, and lifecycle controls;
- add multi-repository views and context switching;
- connect the Engineering Session to Project Manager state changes.

**Acceptance criteria**  
- the user can register and select projects from the Dashboard;
- multiple repositories are visible from the same Dashboard;
- changing project context updates the active Engineering Session everywhere.

**Tests**  
- project registration test;
- multi-repository selection test;
- active-context switching test.

---

## Phase 6 — Engineering Workspace, Merge, and Runtime Operations
**Working dashboard outcome**  
The Dashboard supports deeper engineering work and operational supervision.

**Required engines/services**  
- Runtime
- Project Manager
- Repository Engine
- Knowledge Engine
- Validation Engine
- GitHub integration foundation
- logging, monitoring, and metrics services

**Implementation tasks**  
- add Engineering Workspace and Merge surfaces;
- add Runtime, Logs, Jobs, Monitoring, and Metrics pages;
- make evidence traceable from summary views to operational details.

**Acceptance criteria**  
- the user can move from repository understanding to merge readiness in one Dashboard;
- runtime and operational evidence are visible without leaving the Dashboard.

**Tests**  
- workspace navigation flow test;
- merge readiness summary test;
- runtime/logs/metrics rendering tests.

---

## Phase 7 — AI Agent and Provider Visibility
**Working dashboard outcome**  
The Dashboard supervises AI operating dependencies without changing engine identity.

**Required engines/services**  
- Agent Layer
- Provider Layer
- Runtime
- Project Manager
- monitoring and reporting services

**Implementation tasks**  
- surface active AI provider from the Engineering Session;
- show provider availability and policy posture;
- show agent activity and agent-to-provider execution status where relevant;
- keep AI-assisted behavior optional and observable.

**Acceptance criteria**  
- the user can understand which provider is active and whether it is healthy;
- the user can see when agent-assisted enrichment is being used;
- Dashboard behavior remains coherent when no provider is configured.

**Tests**  
- provider visibility test;
- agent activity rendering test;
- no-provider fallback test.

---

## Phase 8 — Integrations, Governance, and Complete Dashboard
**Working dashboard outcome**  
A complete Dashboard spanning repositories, runtime, integrations, standards, governance, administration, and executive control.

**Required engines/services**  
- all previously required engines/services;
- Telegram integration;
- Railway integration;
- GitHub integration;
- canonical intelligence and governance services.

**Implementation tasks**  
- add Telegram, Railway, GitHub, Standards, Canonical Documents, Governance, Settings, and Administration surfaces;
- unify navigation across all major Dashboard sections;
- ensure every product area is discoverable from the Dashboard.

**Acceptance criteria**  
- every major Dashboard section in the Dashboard Blueprint is represented;
- the Dashboard functions as the single operational overview of AI-Toolkit;
- no additional planning layer is needed before implementation continues.

**Tests**  
- end-to-end dashboard navigation test;
- representative multi-repository workflow test;
- degraded integration state handling test;
- regression suite across major Dashboard sections.

---

## Roadmap Rules
- every phase preserves a working Dashboard;
- the Dashboard remains a consumer of engine outputs and runtime state rather than a replacement for engine logic;
- Project Manager owns active project context and Engineering Session state;
- AI agents sit between engines and providers when AI assistance is used;
- future implementation extends this roadmap rather than reopening product-definition work.

AI-Toolkit is now ready to begin implementation.

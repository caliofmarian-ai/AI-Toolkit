# AI-Toolkit Dashboard Implementation Roadmap

## Purpose
This roadmap defines how the AI-Toolkit Dashboard is implemented in phases without redesigning existing architecture.

It reuses the accepted planning direction already present in the repository and turns it into an implementation reference for the Dashboard as a product surface.

Every phase ends with a working Dashboard.
Each completed phase remains useful while enabling the next phase.

## Planning Baseline Reused
This roadmap reuses the existing implementation direction already established by:
- `docs/planning/DASHBOARD_IMPLEMENTATION_STRATEGY.md`
- `docs/planning/EXECUTABLE_IMPLEMENTATION_PLAN.md`
- `docs/planning/EXECUTABLE_ROADMAP.md`
- existing runtime, repository, validation, briefing, monitoring, and integration plans.

## Phase 1 — Local Read-Only Dashboard
**Working dashboard outcome**  
A local Dashboard that opens in the browser and shows the latest inspection, validation, and executive briefing outputs for one repository.

**Required engines**  
- Runtime
- Repository Engine
- Validation Engine
- Executive Briefing Engine
- report publication services

**Implementation tasks**  
- expose a local dashboard route through the existing runtime server;
- present the latest inspection, validation, and briefing outputs in readable dashboard panels;
- provide a simple project context header and navigation shell;
- ensure the Dashboard works without introducing a front-end framework or a separate build system.

**Acceptance criteria**  
- the Dashboard starts locally from the existing product entry points;
- the user can see the latest inspect output;
- the user can see the latest validation output;
- the user can see the latest executive briefing output;
- the page is usable without JavaScript frameworks or extra dashboard-only infrastructure.

**Tests**  
- dashboard startup test;
- read-only page rendering test;
- panel population test for inspect, validate, and briefing outputs;
- regression test confirming the Dashboard remains a consumer of existing engine outputs.

---

## Phase 2 — Action Panel and Job History
**Working dashboard outcome**  
A local interactive Dashboard where the user can trigger core engineering actions and observe job progress and history.

**Required engines**  
- Runtime
- Repository Engine
- Validation Engine
- Executive Briefing Engine
- job queue and scheduler services
- logging and reporting services

**Implementation tasks**  
- add action controls for inspection, validation, and briefing generation;
- show job state transitions from queued through completion or failure;
- publish recent execution history inside the Dashboard;
- connect actions to existing command and runtime flows rather than introducing dashboard-only logic.

**Acceptance criteria**  
- the user can trigger inspect from the Dashboard;
- the user can trigger validate from the Dashboard;
- the user can trigger briefing generation from the Dashboard;
- the Dashboard shows running, completed, and failed job states;
- all actions remain available through existing non-dashboard interfaces.

**Tests**  
- action submission test;
- job lifecycle rendering test;
- job history persistence test;
- regression test verifying action results appear in the expected dashboard panels.

---

## Phase 3 — Multi-Project and Repository Browser Foundation
**Working dashboard outcome**  
A Dashboard that can switch between repositories, show multiple managed projects, and provide repository browsing as a first-class experience.

**Required engines**  
- Runtime
- workspace management services
- Repository Engine
- report publication services
- knowledge publication services

**Implementation tasks**  
- add a project selector and workspace-aware navigation;
- display multiple registered repositories and their health summaries;
- introduce the Repository Browser page with access to important artifacts and generated outputs;
- allow inspection and validation views to operate in the context of the selected repository.

**Acceptance criteria**  
- the user can see more than one managed repository in the Dashboard;
- the user can switch repository context without leaving the Dashboard;
- the user can browse key repository artifacts and generated reports;
- repository-specific health indicators remain visible and understandable.

**Tests**  
- multi-repository selection test;
- repository context switching test;
- repository browser rendering test;
- regression test for per-repository panel isolation.

---

## Phase 4 — Engineering Workspace, Knowledge, Validation, and Merge Flow
**Working dashboard outcome**  
A working engineering control surface where the user can move from repository understanding to knowledge review, validation analysis, and merge readiness in one Dashboard.

**Required engines**  
- Runtime
- Repository Engine
- Knowledge Engine
- Validation Engine
- Executive Briefing Engine
- GitHub integration
- approval and governance services

**Implementation tasks**  
- add the Engineering Workspace as the central action surface;
- add dedicated Knowledge and Validation pages with deeper detail than the home panels;
- add a Merge area focused on readiness, approvals, and blockers;
- connect repository findings, knowledge outputs, validation findings, and merge readiness into a coherent navigation flow.

**Acceptance criteria**  
- the user can navigate from inspection to knowledge to validation to merge without leaving the Dashboard;
- the Knowledge page shows repository understanding and context outputs;
- the Validation page shows actionable readiness information;
- the Merge page communicates whether work is blocked, risky, or ready for advancement.

**Tests**  
- navigation flow test across workspace pages;
- knowledge page population test;
- validation detail rendering test;
- merge readiness summary test.

---

## Phase 5 — Runtime, Logs, Jobs, Monitoring, and Metrics
**Working dashboard outcome**  
A Dashboard that is operationally complete for day-to-day supervision of the running platform.

**Required engines**  
- Runtime lifecycle services
- scheduler and job queue services
- logging services
- health and recovery services
- metrics and monitoring services
- Executive Briefing Engine

**Implementation tasks**  
- add Runtime, Logs, Jobs, Monitoring, and Metrics pages;
- present current runtime state, operational health, and historical job activity;
- surface incident and alert views that connect to underlying jobs and runtime events;
- make operational evidence easy to trace from summary to detail.

**Acceptance criteria**  
- the user can understand runtime status from the Dashboard alone;
- the user can inspect recent jobs and related logs;
- the user can review health and monitoring indicators in one place;
- the user can correlate metrics, alerts, and execution history.

**Tests**  
- runtime status rendering test;
- logs and jobs visibility test;
- monitoring alert presentation test;
- metrics panel population test.

---

## Phase 6 — Integrations and AI Provider Operations
**Working dashboard outcome**  
A Dashboard that supervises the external systems AI-Toolkit depends on and the AI providers it uses.

**Required engines**  
- Runtime
- GitHub integration
- Railway integration
- Telegram gateway
- provider registry and policy services
- monitoring and reporting services

**Implementation tasks**  
- add GitHub, Railway, Telegram, and AI Providers pages;
- show integration health, readiness, and recent operational history;
- present provider availability, policy posture, and usage visibility;
- connect integration pages back to repository, runtime, and executive views.

**Acceptance criteria**  
- the user can see whether GitHub, Railway, and Telegram are healthy and connected;
- the user can understand AI provider availability and policy posture;
- integration status is visible from both the home summary and dedicated pages;
- the Dashboard remains coherent even when some integrations are unavailable.

**Tests**  
- integration status rendering test;
- provider visibility test;
- degraded integration state handling test;
- navigation test between integrations and dependent product areas.

---

## Phase 7 — Executive, Standards, Governance, and Administration
**Working dashboard outcome**  
A Dashboard that is complete enough to operate AI-Toolkit as the authoritative engineering control center.

**Required engines**  
- Executive Briefing Engine
- canonical intelligence services
- governance and approval services
- Runtime
- standards and validation services
- workspace and administration services

**Implementation tasks**  
- add Executive Briefings, Canonical Documents, Standards, Governance, Settings, and Administration pages;
- expose the governing references and approval context behind operational decisions;
- show how standards, validations, and executive recommendations reinforce each other;
- provide administrative controls for workspace setup and product behavior.

**Acceptance criteria**  
- the user can understand both operational state and governing context from the Dashboard;
- executive summaries, standards, and governance views are linked to real engineering evidence;
- settings and administration pages support practical product operation;
- the Dashboard functions as the single operational overview of AI-Toolkit.

**Tests**  
- executive briefing page test;
- canonical and standards navigation test;
- governance visibility test;
- administrative configuration rendering test.

---

## Phase 8 — Complete Platform Dashboard
**Working dashboard outcome**  
A complete Dashboard spanning local operation, multi-repository supervision, integrations, governance, executive control, and future cloud-ready evolution.

**Required engines**  
- all previously required engines;
- synchronization services;
- portfolio and organization intelligence services as they become available.

**Implementation tasks**  
- unify page relationships into a consistent product-wide navigation system;
- refine portfolio summaries and cross-page recommendations;
- ensure every major AI-Toolkit capability has a discoverable dashboard surface;
- prepare the Dashboard to extend into cloud and organization-level experiences without redefining the product.

**Acceptance criteria**  
- every major Dashboard section in the Dashboard Blueprint is present or intentionally represented;
- the user can operate AI-Toolkit from the Dashboard as the primary control center;
- product navigation, evidence flow, and action flow feel coherent across repositories and integrations;
- the Dashboard is ready for long-term expansion without architectural redesign.

**Tests**  
- end-to-end dashboard navigation test;
- representative multi-repository workflow test;
- operational resilience test under partial integration failure;
- regression suite covering all major dashboard sections.

---

## Roadmap Rules
- every phase must preserve a working Dashboard;
- the Dashboard must remain a consumer of engine outputs rather than a replacement for engine logic;
- new Dashboard capability should reuse existing runtime, report, and engine contracts whenever possible;
- the user should gain visible product value at the end of every phase;
- future work should extend this roadmap, not replace the product blueprint.

AI-Toolkit is now ready to begin implementation.

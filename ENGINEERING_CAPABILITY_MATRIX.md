# ENGINEERING_CAPABILITY_MATRIX

## 1. Executive Summary

AI-Toolkit is a **Python-first engineering platform** whose strongest implemented surface is the **CORE-021 runtime server + dashboard + persisted engineering state** stack. The repository contains real runtime bootstrapping, HTTP endpoints, dashboard rendering, GitHub webhook ingestion, Telegram gateway wiring, and a large `.ai/` persistence layer. The canonical foundation (CSS/CDM/CSL, parser, materialization) is also materially implemented.

The largest maturity gap is the **Runtime API Platform**: `/api/v1/*` exists, but auth is not enforced in request handling, bearer auth is broken in `api_auth.py`, GraphQL/MCP are stubs, and several API surfaces return placeholders. Agents are present but only partly matured: the runtime registers only two agents, and there is overlap between the registered `AICTOScannerAgent` and the unregistered `RepositoryInspectorAgent`.

A second major issue is **duplication / legacy debt**. The repository intentionally preserves many frozen compatibility modules, and there are overlapping implementations for knowledge graphs, planning, audits, and repository inspection. Tests exist broadly, but most are shell smoke tests; structured Python tests are limited.

**Highest-priority next milestone after PR #49:** **CORE-022 — Runtime API Platform**.

---

## 2. Repository Structure Overview

### Top-level structure

- `bin/`
  - Runtime and CLI entrypoints, including `bin/runtime-server`
- `lib/python/`
  - **Primary implementation surface**
- `tests/`
  - 100+ shell smoke/acceptance tests, plus a small Python test set
- `.ai/`
  - Persisted runtime/planning/execution/context/report/session artifacts
- `docs/`
  - Implementation notes, classifications, architecture docs
- `standards/`
  - Canonical standards and specifications
- `architecture/`
  - Architecture reference material
- `knowledge/`
  - Knowledge artifacts
- `development/`
  - Batch / project planning documents
- `implementation-packages/`
  - Packaged implementation support artifacts
- `runtime/`
  - Runtime-related non-package artifacts
- `requirements.txt`
  - Declares stdlib-only runtime bootstrap marker

### Key implementation subdirectories under `lib/python/`

- `runtime/`
  - `bootstrap.py`, `process.py`, `health.py`, `diagnostics.py`, `metrics.py`
  - `interfaces/` for HTTP, GitHub, Telegram, auth, GraphQL placeholder, MCP placeholder
- `dashboard/`
  - `service.py`, `server.py`
- `ai_platform/`
  - Provider settings, model manager, repository chat, sessions
- `agent_runtime/`, `agents/`
  - Agent registry/runtime and concrete agents
- Canonical foundation:
  - `css_engine/`, `cdm_engine/`, `csl_engine/`
  - `canonical_parser/`, `canonical_entities/`, `canonical_intelligence/`, `canonical_repository/`
- Engineering / analysis engines:
  - `repository_engine/`, `dependency_engine/`, `validation_engine/`
  - `autonomous_planning_engine/`, `autonomous_execution_engine/`
  - `context_synchronization_engine/`, `development_state_engine/`
  - `semantic_repository_intelligence/`, `executable_repository_intelligence/`
  - `workspace_orchestrator/`, `knowledge_materialization/`
- Legacy / overlap areas:
  - `knowledge_graph/`, `knowledge_graph_v2/`
  - `audit_engine/` (stub)
  - `foundation_audit/`, `canonical_audit/`

### Test structure

- `tests/*.sh`
  - Main validation surface
- `tests/engineering/*.py`
  - Best structured automated tests
- Root:
  - `test_csl_grammar.py`, `test_csl_semantic.py`

### Structural observations

- The repo is overwhelmingly **Python-based**; there are no meaningful JS/TS application implementations.
- `.ai/` contains real persisted operational artifacts, but some reference a different filesystem root, so provenance is mixed.

---

## 3. Capability Matrix Table

| ID | Name | Canonical Refs | Implementation Modules | Runtime Integration | Dashboard Integration | Tests | Dependencies | Status | Missing Components | Next Action |
|---|---|---|---|---|---|---|---|---|---|---|
| RT-001 | Runtime bootstrap/server | `CORE-021`, `CANON-055` | `lib/python/runtime/bootstrap.py`, `process.py`, `process_identity.py`, `lifecycle.py` | `bin/runtime-server` launches `python.runtime.process`; bootstrap registers engines/services and starts HTTP/scheduler/event loop | Runtime state shown on `/runtime`, `/diagnostics`, `/status` | `tests/test_runtime_bootstrap.sh`, `test_runtime_acceptance.sh`, `test_runtime_lifecycle.sh` | stdlib, runtime services, dashboard, registry | **OPERATIONAL** | API hardening, richer ops controls | Keep bootstrap stable; use it as base for CORE-022 |
| RT-002 | Runtime HTTP API + health/metrics | `CORE-021` → `CORE-022` | `runtime/interfaces/http_server.py`, `runtime/interfaces/runtime_api.py`, `runtime/interfaces/api_auth.py`, `health.py`, `metrics.py` | `/health`, `/ready`, `/metrics`, `/status`, `/api/v1/runtime` exposed from HTTP server | Runtime/diagnostics pages consume persisted status | `tests/test_runtime_health.sh`, `test_runtime_acceptance.sh` | stdlib HTTP server, health, metrics | **PARTIALLY_IMPLEMENTED** | Auth not enforced; bearer check broken; reports endpoint placeholder; no typed API contract | Implement/authenticate `/api/v1/*`, add contract tests, finish reports/API surface |
| UI-001 | Engineering dashboard | `CORE-021` | `dashboard/service.py`, `dashboard/server.py` | Mounted by runtime bootstrap and HTTP server | Native capability: pages for `/`, `/projects`, `/repository`, `/session`, `/ai-control-center`, `/runtime`, `/diagnostics` | `tests/test_dashboard.sh`, `test_dashboard_navigation.sh`, `test_runtime_dashboard_navigation.sh` | runtime state files, `.ai/*`, AI platform | **OPERATIONAL** | Capability status is heuristic; synthetic fallback views can overstate reality | Replace heuristic capability scoring with registry/evidence-backed status |
| AI-001 | AI control center / repository chat | `CORE-020/021`-adjacent | `ai_platform/service.py`, `adapters.py`, `model_manager.py`, `pipeline.py`, `sessions.py`, `settings.py` | Not a core runtime dependency, but surfaced through dashboard and repository page flows | `/ai-control-center` and repository Q&A page | `tests/test_ai_platform.sh` | local JSON settings/sessions, static provider adapters | **INTEGRATED** | Real provider API execution absent; connection tests are mostly configuration health checks | Convert provider adapters from static/simulated to real API-backed connectors |
| CAN-001 | CSS engine | CSS baseline | `css_engine/engine.py` | Registered in runtime bootstrap engine registry | Indirect only via capability listing / reports | `tests/test_canonical_execution_stack.sh` | markdown parsing via stdlib text processing | **FUNCTIONAL** | Limited evidence of end-to-end runtime use | Add runtime/API exposure and coverage assertions |
| CAN-002 | CDM engine | CDM baseline | `cdm_engine/engine.py` | Registered in runtime bootstrap | Indirect via reports/capabilities | `tests/test_canonical_execution_stack.sh` | canonical docs, parser helpers | **FUNCTIONAL** | Limited integration evidence beyond engine registration | Add explicit materialization pipeline tests |
| CAN-003 | CSL engine + parser | CSL baseline | `csl_engine/engine.py`, `canonical_parser/lexer.py`, `parser.py`, `semantic_analyzer.py` | Registered in runtime bootstrap | Indirect only | `test_csl_grammar.py`, `test_csl_semantic.py`, `tests/test_csl_level*.sh` | stdlib parsing stack | **FUNCTIONAL** | No strong runtime-facing product surface yet | Expose compilation/validation results through runtime API or dashboard |
| CAN-004 | Knowledge materialization | Canonical knowledge stack | `knowledge_materialization/engine.py`, `canonical_entities/*` | Registered in runtime bootstrap | Indirect via reports/capabilities | `tests/test_canonical_execution_stack.sh`, `test_knowledge_graph_canonical.sh` | CDM/CSS outputs, canonical entities | **FUNCTIONAL** | Limited direct runtime/dashboard views | Publish materialized graph/results into dashboard/runtime reports |
| ENG-001 | Development state / engineering context persistence | Core context stack | `development_state_engine/runtime.py`, `repository.py`, `models.py` | Runtime diagnostics load `.ai/development_state/current_state.json` | Dashboard reads current project/repo/branch/task context | `tests/test_development_state_persistence.sh`, `test_development_state_runtime*.sh` | JSON persistence, `.ai/development_state` | **OPERATIONAL** | Mixed artifact provenance; temp-file persistence pattern needs consistency review | Normalize state provenance and validate current-environment freshness |
| ENG-002 | Context synchronization engine | Context sync | `context_synchronization_engine/engine.py` | Feeds engineering context used by runtime health/diagnostics | Dashboard consumes synchronized context-derived artifacts | `tests/test_context_synchronization_engine.sh` | git context, GitHub context, dev state | **OPERATIONAL** | No stronger freshness/consistency validation | Add explicit drift/freshness checks and surfaced sync errors |
| ENG-003 | Repository engine / workspace index | Repository analysis core | `repository_engine/engine.py`, `workspace_index/*` | Used by CLI, agents, downstream engines | Dashboard repository pages use repository-derived summaries | `tests/test_repository_engine_v2.py`, `test_repository_engine_inspect.sh`, `test_workspace_index.sh` | stdlib AST/path scanning | **OPERATIONAL** | Main entrypoint detection and execution chain are still coarse | Strengthen execution-model accuracy and link outputs to API |
| ENG-004 | Dependency, validation, and basic planning engines | Support analysis stack | `dependency_engine/engine.py`, `validation_engine/engine.py`, `planning_engine/engine.py` | Registered in runtime bootstrap (dependency/validation/planning) | Indirect via reports/capabilities | `tests/test_dependency_engine.sh`, `test_validation_engine.sh`, `test_planning_engine.sh` | repository/workspace index, rule logic | **INTEGRATED** | `PlanningEngine` is basic compared with newer planning stacks | Consolidate around one authoritative planning pipeline |
| ENG-005 | Autonomous planning engine | Planning milestone | `autonomous_planning_engine/engine.py` | Not startup-critical, but part of active persisted workflow | Dashboard can surface persisted planning artifacts indirectly | `tests/test_autonomous_planning_engine.sh` | development state, executive briefing, persisted `.ai/planning` | **OPERATIONAL** | Direct runtime command/API surface is limited | Promote as primary planning API and deprecate older planner paths |
| ENG-006 | Autonomous execution engine | Execution milestone | `autonomous_execution_engine/engine.py` | Not directly mounted as runtime service; participates in artifact generation | Indirect via persisted execution artifacts | `tests/test_autonomous_execution_engine.sh` | planning artifacts, policies, validators, reports | **INTEGRATED** | End-to-end mutation/execution governance remains light | Add explicit execution controls, approval gates, and API endpoints |
| ENG-007 | Workspace orchestrator | `CORE-012` | `workspace_orchestrator/engine.py`, `persistence.py` | Not a core runtime startup service | Dashboard has workspace sections, but current repo lacks `.ai/workspace` artifacts | `tests/test_workspace_orchestrator.sh` | registry, repository scans, `.ai/workspace` JSON | **FUNCTIONAL** | No evidence of active local workspace artifacts; dashboard falls back | Generate and persist real workspace scans during runtime workflows |
| ENG-008 | Semantic repository intelligence | Semantic analysis stack | `semantic_repository_intelligence/engine.py` | Used by scanner/reporting flows | Indirect | `tests/test_semantic_repository_intelligence.sh` | repository model, heuristics, knowledge outputs | **INTEGRATED** | Recommendation quality is heuristic; no formal API surface | Turn semantic findings into first-class runtime/dashboard entities |
| ENG-009 | Executable repository intelligence | Execution-model analysis | `executable_repository_intelligence/engine.py` | Used in repository intelligence stack, not directly mounted | Indirect | `tests/test_executable_repository_intelligence.sh` | semantic intelligence, dependency modeling | **FUNCTIONAL** | No direct runtime/API/dashboard surface | Expose executable model through reports/API |
| AGT-001 | Agent runtime registry | `CORE-025/026` precursor | `agent_runtime/runtime.py`, `registry.py`, `models.py` | Separate agent runtime; bootstrap does not yet expose multi-agent platform features | Indirect capability listing only | `tests/test_agent_runtime.sh`, `test_agent_cli.sh` | BaseAgent, AgentContext/Result | **INTEGRATED** | Only two agents registered; no memory/comms/orchestration layers | Build registry/memory/comms milestones on top of current runtime |
| AGT-002 | AI CTO scanner agent | `CORE-008A` | `agents/ai_cto_scanner_agent.py`, `ai_cto_scanner/engine.py` | Registered as `inspect` in agent runtime | Not a dedicated dashboard page; outputs appear via reports/capabilities | `tests/test_ai_cto_scanner.sh` | semantic intelligence, canonical intelligence, report generation | **OPERATIONAL** | Agent namespace conflicts with repository inspector | Keep as authoritative `inspect`; retire or rename overlapping inspector agent |
| AGT-003 | Development agent | Legacy orchestration agent | `agents/development_agent.py` | Registered as `develop` in agent runtime | No dedicated UI | `tests/test_development_agent.sh` | many legacy engines, profiler, workspace manager | **INTEGRATED** | Pulls in deprecated/overlapping modules; pipeline is too broad | Refactor around current authoritative engines only |
| AGT-004 | Repository inspector agent | Legacy/overlap agent | `agents/repository_inspector_agent.py` | **Not registered** by default; only works when manually registered | None | `tests/test_agent_runtime.sh` manually registers it; `test_repository_inspector*.sh` | `repository_inspector_v2` | **FUNCTIONAL** | Unregistered; duplicates `inspect` name used by scanner agent | Deprecate or rename and explicitly migrate callers |
| INT-001 | GitHub webhook interface | `CORE-021`, `CANON-048` | `runtime/interfaces/github_webhook.py` | Mounted at `/webhook/github`; publishes runtime events | Indirect via runtime state/reports | `tests/test_runtime_webhooks.sh`, `test_runtime_acceptance.sh` | event dispatcher, HMAC, JSON | **OPERATIONAL** | Downstream workflow actions are still thin | Add richer event handling, persistence, and audit trails |
| INT-002 | GitHub materialization | GitHub workflow support | `github_materialization/engine.py` | Not mounted in runtime; used by development agent pipeline | None direct | `tests/test_github_materialization.sh` | local `.ai/batches` file generation | **FUNCTIONAL** | Creates local issue/PR markdown only; no GitHub API execution | Connect generated artifacts to actual GitHub API workflows |
| INT-003 | Telegram gateway | `CORE-021` | `runtime/interfaces/telegram_gateway.py` | Mounted at `/webhook/telegram`; polling + command dispatch wired in bootstrap | Indirect via runtime/ops flows | `tests/test_runtime_telegram.sh`, `test_runtime_acceptance.sh` | optional `requests`, event dispatcher | **INTEGRATED** | Disabled without token/`requests`; dependency mismatch with stdlib-only claim | Formalize dependency declaration and add credentialed integration tests |
| DEP-001 | Railway deployment | `CORE-021`, README roadmap | `railway.json`, `bin/runtime-server` | Railway start command and `/health` healthcheck configured | Serves same runtime/dashboard app | `tests/test_railway_bootstrap.sh` | Railway/Nixpacks, runtime server | **INTEGRATED** | Limited environment hardening / deployment validation evidence | Add deployment smoke/rollback/ops checks under CORE-024 |
| IFC-001 | GraphQL runtime interface | Planned | `runtime/interfaces/graphql/__init__.py` | None | None | None found | placeholder only | **SCAFFOLD** | No schema, transport, auth, or resolvers | Either implement under CORE-022 or remove from active capability claims |
| IFC-002 | MCP runtime interface | Planned | `runtime/interfaces/mcp/__init__.py` | None | None | None found | placeholder only | **SCAFFOLD** | No protocol, transport, tooling, or tests | Same as GraphQL: implement or explicitly defer |
| AUD-001 | Audit engine package | Audit placeholder | `audit_engine/*` | None | None | None meaningful | zero-byte files | **SCAFFOLD** | Entire package is stubbed | Remove from maturity claims or implement a real audit engine |
| AUD-002 | Foundation audit / canonical audit | Audit utilities | `foundation_audit/*`, `canonical_audit/engine.py` | Standalone/offline, not core runtime services | Indirect via reports only | `tests/test_foundation_audit*.sh`, `test_canonical_audit.sh` | evidence engine, workspace index | **FUNCTIONAL** | Mostly heuristic/string matching; not authoritative governance | Unify into a single evidence-backed audit/reporting path |
| AUX-001 | Session runtime | Session tracking | `session_runtime/runtime.py`, `storage.py` | Not wired into main runtime flows | None | `tests/test_session_runtime.sh` | `.ai/sessions` JSON storage | **FUNCTIONAL** | Minimal model; weak integration with main runtime state | Consolidate with development state / runtime diagnostics session model |

---

## 4. Detailed Capability Assessments

### 4.1 Runtime

The runtime is the most mature subsystem in the repository. `bin/runtime-server` launches `python.runtime.process`, which imports `RuntimeBootstrap`. `RuntimeBootstrap` wires health, recovery, supervisor, metrics, scheduler, event loop, job queue, HTTP server, dashboard, GitHub webhooks, Telegram, and an engine/service registry. The HTTP server exposes `/health`, `/ready`, `/metrics`, `/status`, `/api/v1/runtime`, and dashboard routes.

This is enough to classify the runtime server itself as **OPERATIONAL**. The runtime also persists status snapshots via `RuntimeDiagnosticsService`, and README explicitly marks `CORE-021` complete.

However, the **Runtime API Platform** is not mature enough to inherit that same rating. `RuntimeApiRouter` constructs `ApiAuth`, but request handling does not actually enforce auth, and `ApiAuth.authorized()` contains a broken bearer comparison:

- `if self.bearer and auth == f"******":`

That makes the API surface **PARTIALLY_IMPLEMENTED**, not operational as a hardened platform.

### 4.2 Dashboard

The dashboard is a real, server-rendered HTML surface, not a placeholder. `EngineeringDashboardService` and `dashboard/server.py` render multiple pages and integrate with persisted `.ai` artifacts. A smoke check successfully built the payload and returned navigation, capability, report, workspace, and runtime content.

Strengths:
- Real route integration
- Pulls repository/runtime/planning/execution context from persisted state
- Has shell tests for navigation and runtime dashboard behavior

Weaknesses:
- Capability maturity is computed heuristically from file/test presence and runtime health
- When runtime or workspace artifacts are missing, the dashboard can render synthetic/fallback content that looks healthier than the underlying implementation really is

Overall: **OPERATIONAL**, but not yet evidence-rigorous.

### 4.3 Canonical Foundation (CSS / CDM / CSL)

The canonical stack is materially present:

- `CSSEngine` validates canonical markdown structure
- `CdmEngine` extracts metadata, sections, dependencies, traceability
- `CslEngine` wraps lexer/parser/semantic analysis into an executable pipeline
- Root CSL tests exist (`test_csl_grammar.py`, `test_csl_semantic.py`)

This is not scaffold code. It is real parsing/validation/materialization logic. The main limitation is that canonical execution is not yet exposed as a strong runtime product surface, so the stack is best classified as **FUNCTIONAL** rather than integrated end-to-end.

### 4.4 Knowledge Materialization

`knowledge_materialization/engine.py` plus `canonical_entities` show a meaningful attempt to materialize canonical artifacts into structured graph/object models. This is stronger than a simple import graph and is aligned with the platform’s long-term “engineering knowledge” vision.

Current weakness: there is little direct runtime or dashboard presentation of these outputs beyond indirect reporting and scanner integration.

Overall: **FUNCTIONAL**.

### 4.5 Engineering Context and Persistence

The `.ai/` persistence layer is extensive and central:

- `.ai/development_state`
- `.ai/context`
- `.ai/planning`
- `.ai/execution`
- `.ai/executive`
- `.ai/self_evaluation`
- `.ai/self_improvement`
- `.ai/runtime/state`
- `.ai/sessions`
- `.ai/batches`

`development_state_engine` and `context_synchronization_engine` are not passive libraries; their artifacts are actively loaded by runtime diagnostics and the dashboard. That justifies **OPERATIONAL** for engineering context persistence.

Important caveat: some persisted artifacts reference `/storage/emulated/...` instead of the current CI path, so “operational” here means the mechanism exists and is being used, not that every artifact is freshly generated in this exact environment.

### 4.6 Repository / Analysis / Planning / Execution Engines

There are multiple generations of analysis and orchestration engines.

**Strongest current engines**
- `repository_engine`
- `autonomous_planning_engine`
- `semantic_repository_intelligence`
- `context_synchronization_engine`
- `development_state_engine`

**More transitional / overlapping engines**
- `planning_engine`
- `knowledge_graph_v2`
- `foundation_audit`
- `canonical_audit`

`RepositoryEngine` is actively useful and validated. `AutonomousPlanningEngine` appears materially used, with persisted planning artifacts present. `AutonomousExecutionEngine` is substantial, but still feels more like an artifact-generating orchestrator than a fully governed execution platform. `WorkspaceOrchestrator` is substantial but lacks evidence of active `.ai/workspace` output in this repo state.

Result:
- repository analysis: **OPERATIONAL**
- planning/execution support: **INTEGRATED**
- workspace orchestration: **FUNCTIONAL**

### 4.7 Agents

The agent story is not yet aligned with the roadmap implied by CORE-025 through CORE-028.

What exists:
- `agent_runtime` with a real runtime/registry model
- registered agents: `AICTOScannerAgent`, `DevelopmentAgent`
- unregistered but implemented: `RepositoryInspectorAgent`

Problems:
- only two agents are registered
- no real agent memory/comms/orchestrator layer yet
- namespace conflict: both scanner and repository inspector use `NAME = "inspect"`
- `DevelopmentAgent` pulls in many older overlapping modules

So the agent subsystem is **INTEGRATED**, but not yet a mature agent framework.

### 4.8 GitHub Integration

There are two distinct GitHub-related capabilities:

1. **Webhook ingestion**
   - real runtime-mounted webhook
   - HMAC validation
   - canonical event mapping
   - runtime event publication  
   This is **OPERATIONAL**.

2. **Materialization**
   - `GitHubMaterializationEngine` generates local issue/PR/checklist markdown under `.ai/batches`
   - no actual GitHub API write path  
   This is only **FUNCTIONAL**.

This is an important distinction: GitHub events are integrated; GitHub actioning is mostly local artifact generation.

### 4.9 Telegram Integration

Telegram is genuinely wired into the runtime: webhook handler, polling path, command routing, outbound message helpers. But it depends on optional `requests`, while `requirements.txt` claims stdlib-only runtime. Tests mostly validate disabled mode or local behavior.

That makes Telegram **INTEGRATED**, not fully operational.

### 4.10 Deployment

Railway deployment is clearly intended and wired:

- `railway.json`
- `bin/runtime-server`
- `/health` healthcheck
- README says deployment target is Railway

That is enough for **INTEGRATED**. It is not yet **PRODUCTION_READY** because operational hardening, rollback, and environment validation evidence are still thin.

### 4.11 Stub / Deferred Interfaces

Three areas should not be counted as implemented capabilities:

- GraphQL interface: `runtime/interfaces/graphql/__init__.py`
- MCP interface: `runtime/interfaces/mcp/__init__.py`
- `audit_engine/` package: zero-byte stubs

All three are **SCAFFOLD**.

---

## 5. Duplication & Overlap Analysis

### 5.1 Agent command overlap: `inspect`

Highest-confidence duplication:

- `AICTOScannerAgent.NAME = "inspect"`
- `RepositoryInspectorAgent.NAME = "inspect"`

Only the scanner is registered in `agent_runtime/registry.py`. The repository inspector still exists and is even manually registered in `tests/test_agent_runtime.sh`. This is a direct namespace conflict and a clear obsolete overlap.

**Recommendation:** keep `AICTOScannerAgent` as the authoritative `inspect` agent and deprecate or rename `RepositoryInspectorAgent`.

### 5.2 Planning overlap

There are at least three planning paths:

- `planning_engine`
- `autonomous_planner`
- `autonomous_planning_engine`

`planning_engine` is simple/basic; `autonomous_planning_engine` is the stronger artifact-backed implementation. `DevelopmentAgent` still pulls both old and new paths into one pipeline.

**Recommendation:** designate one planning engine as authoritative (likely `autonomous_planning_engine`) and freeze the others.

### 5.3 Knowledge graph overlap

Overlapping graph capabilities exist in:

- `knowledge_graph`
- `knowledge_graph_v2`
- top-level `knowledge_graph_engine.py`
- `knowledge_materialization`
- semantic/canonical entity graph concepts

`docs/implementation/MODULE_CLASSIFICATION.md` explicitly says `knowledge_graph_v2` is a duplicate and should be deprecated.

**Recommendation:** keep one graph stack for simple repository import graphing and one for canonical materialization; deprecate the rest.

### 5.4 Audit overlap

Audit-related logic is split across:

- `audit_engine/` (stub)
- `foundation_audit/`
- `canonical_audit/`
- dashboard heuristic capability checks

These do not form one coherent authoritative audit system.

**Recommendation:** eliminate `audit_engine` from active claims until implemented; merge foundation/canonical/dashboard heuristics into one evidence-backed audit/reporting path.

### 5.5 Dashboard status vs runtime truth

The dashboard’s `CAPABILITY_DEFINITIONS` can imply integration based on:
- file presence
- test presence
- runtime health
- fallback synthetic views

This can diverge from actual runtime registration and end-to-end operability.

**Recommendation:** drive capability status from the runtime registry, persisted health evidence, and real route/agent registration.

### 5.6 Legacy shell surface vs Python surface

`docs/implementation/MODULE_CLASSIFICATION.md` explicitly freezes shell modules as deprecated compatibility-only. The Python equivalents are authoritative.

**Recommendation:** keep shell tests where useful, but stop treating shell implementations as active capability surfaces.

---

## 6. Priority Recommendation for Next PR After #49

## Recommended milestone: **CORE-022 — Runtime API Platform**

### Why this is the highest-priority next step

The repository already has:
- a working runtime bootstrap/server
- dashboard integration
- health/readiness/metrics/status surfaces
- persisted engineering context
- webhook and Telegram wiring

The most important missing layer is turning that into a **real platform API**.

Today’s biggest gaps are exactly in that band:

1. **Auth is incomplete**
   - `RuntimeApiRouter` creates `ApiAuth`
   - request handling does not enforce it
   - bearer token comparison is broken

2. **API surface is shallow/incomplete**
   - `/api/v1/runtime` exists
   - `reports()` returns placeholder data
   - no clear typed API contract or broader operational surface

3. **Deferred interfaces remain stubs**
   - GraphQL placeholder
   - MCP placeholder

4. **Several strong subsystems are not first-class platform services yet**
   - planning
   - execution
   - canonical validation/materialization
   - semantic intelligence
   - workspace orchestration

### Best next PR scope

A strong post-#49 PR should:

- enforce auth on `/api/v1/*`
- fix bearer auth logic
- formalize runtime API contracts for status/reports/capabilities/context
- expose selected planning/execution/canonical/runtime state through API
- add API-focused tests
- explicitly decide whether GraphQL/MCP are implemented now or formally deferred

### Why not another milestone first?

- **CORE-023 Runtime Operations** depends on a trustworthy API/control surface.
- **CORE-024 Deployment Platform** is weaker without hardened API/ops endpoints.
- **CORE-025+ Agent milestones** should sit on a stable runtime platform, not bypass it.

### Note on “after PR #49”

No repository artifact directly identified the content of **PR #49**, so this recommendation is anchored to:
- the documented roadmap in `README.md`
- the actual implementation state of the repository
- the most obvious maturity gap between completed `CORE-021` and the next viable platform step

**Final recommendation:** make the next PR a **CORE-022 Runtime API Platform hardening and formalization PR**.
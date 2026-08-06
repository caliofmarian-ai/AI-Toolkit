# Executable Implementation Plan

**Status:** Active  
**Created:** 2026-08-06  
**Based on:** `docs/audits/EXECUTIVE_REPOSITORY_AUDIT.md`  
**Scope:** Transform the accepted planning baseline into shipped code

---

## Philosophy

Architecture is frozen.
Planning alignment is complete.
Implementation begins now.

Every sprint must end with working software, and the Dashboard must evolve in parallel with the engines instead of waiting until the end.

---

## Current State

| Capability | Module | Status |
|---|---|---|
| Repository Engine | `lib/python/repository_engine/` | Stub — no complete inspect CLI yet |
| Knowledge Engine | `lib/python/knowledge_engine/` | Stub — no extract CLI yet |
| Validation Engine | `lib/python/validation_engine/` | Stub — path checks only |
| Executive Briefing | `lib/python/executive_briefing_engine/` | Implemented — not wired to CLI |
| Dashboard | — | Blueprint complete — implementation not started |
| Project Manager | `workspace_manager` / `workspace_orchestrator` foundation exists | Not unified as a runtime service |
| Engineering Session | runtime and state concepts exist in fragments | Not unified as one working context |
| AI Agent Layer | `lib/python/agent_runtime/`, `lib/python/agents/` exist | Not aligned with provider strategy |
| AI Provider Layer | — | Not started |
| Runtime Server | `lib/python/runtime/` | Implemented — end-to-end validation still needed |

---

## Implementation Order

Implementation now proceeds on coordinated tracks rather than a single delayed dashboard step.

### Track A — Core Engineering Outputs
`inspect` → `knowledge extract` → `validate` → `briefing generate`

### Track B — Dashboard Evolution
Inspect-first dashboard → knowledge/validation expansion → action panel/jobs → project manager/multi-repository control

### Track C — Operational Context
Workspace registry/state → Project Manager runtime service → Engineering Session persistence → active-context aware dashboard

### Track D — AI Assistance
Existing `agent_runtime` / `agents` alignment → provider abstraction → optional AI-assisted engine enrichment

### Track E — Runtime and Integrations
Runtime server validation → Telegram → Railway → GitHub triggers

These tracks share outputs, but the Dashboard starts as soon as Track A produces the first inspect report.

---

## Sprint Map

| Sprint | Goal | Duration |
|---|---|---|
| Sprint 1 | `bin/ai inspect` + inspect-first Dashboard | 2 weeks |
| Sprint 2 | `bin/ai knowledge extract` + dashboard knowledge expansion | 2 weeks |
| Sprint 3 | `bin/ai validate` + Engineering Session unification | 2 weeks |
| Sprint 4 | `bin/ai briefing generate` + dashboard action panel | 1 week |
| Sprint 5 | Project Manager runtime service + multi-repository dashboard | 2 weeks |
| Sprint 6 | AI Agent Layer + AI Provider Layer + runtime server validation | 2 weeks |
| Sprint 7 | Telegram + Railway deployment | 1 week |
| Sprint 8 | GitHub integration | 2 weeks |

---

## Constraints

1. No new canonical specification documents are required for implementation.
2. Every new module must have at least one automated test before merge.
3. The Dashboard must stay simple: HTML + CSS served by the existing runtime server.
4. Project Manager must reuse existing workspace/state foundations rather than inventing a new orchestration system.
5. Engineering Session must be the authoritative current working context across CLI, runtime, and Dashboard.
6. Engines remain deterministic and provider-independent.
7. AI-assisted enrichment, when present, must flow through the Agent Layer and then the Provider Layer.

---

## Definition of Done (per sprint)

- [ ] New code has unit or integration tests
- [ ] The sprint’s primary command or UI surface works on AI-Toolkit
- [ ] Existing tests still pass
- [ ] The Dashboard remains working after the sprint’s changes
- [ ] Engineering Session context remains visible and consistent where applicable
- [ ] No new planning-only sprint is introduced

---

## Reuse, Don’t Redesign

| Target capability | Existing foundation to reuse |
|---|---|
| Repository Engine | `engineering_engine/repository_scanner.py`, `executable_repository_intelligence/*` |
| Knowledge Engine | `canonical_intelligence/`, `knowledge_graph/`, `knowledge_graph_v2/`, `semantic_repository_intelligence/` |
| Validation Engine | `audit_engine/`, `compliance_engine/`, `development_validator/` |
| Project Manager | `workspace_manager/`, `workspace_orchestrator/registry.py`, `workspace_orchestrator/state_manager.py` |
| AI Agent Layer | `agent_runtime/`, `agents/` |
| Dashboard | existing runtime server + report outputs |

---

## Immediate Next Action

**Start Sprint 1 implementation:** deliver `bin/ai inspect <path>` and the first usable Dashboard from the inspect output.

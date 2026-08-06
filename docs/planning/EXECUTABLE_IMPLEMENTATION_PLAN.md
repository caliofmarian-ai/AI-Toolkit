# Executable Implementation Plan

**Status:** Active  
**Created:** 2026-08-06  
**Based on:** `docs/audits/EXECUTIVE_REPOSITORY_AUDIT.md`  
**Scope:** Transform audit recommendations into shipped code

---

## Philosophy

Architecture is frozen. Implementation starts now.

Every two-week sprint must end with working software running on at least one of:
- AI-Toolkit (self)
- Trading Signals Platform
- DROPi

No sprint ends with documentation only.

---

## Current State (as of audit)

| Engine | Module | Status |
|---|---|---|
| Repository Engine | `lib/python/repository_engine/` | Stub — `discover()` wraps workspace index, no file classification, no CLI |
| Knowledge Engine | `lib/python/knowledge_engine/` | Stub — entity registry only, no extraction |
| Validation Engine | `lib/python/validation_engine/` | Stub — path-existence checks only |
| Executive Briefing | `lib/python/executive_briefing_engine/` | Implemented — not wired to CLI |
| Runtime Server | `lib/python/runtime/` | Implemented — not tested end-to-end |
| CLI | `bin/ai` | Routes only to `engineering` — no `inspect`, `validate`, `briefing` |
| Dashboard | — | Not started |
| AI Provider Layer | — | Not started |

---

## Implementation Order

The order is determined by data dependencies between engines:

```
Repository Engine (inspect)
    └─► Knowledge Engine (extract)
            └─► Validation Engine (validate)
                    └─► Executive Briefing (briefing generate)
                                └─► Dashboard (display)
                                └─► Runtime Server (serve)
```

AI Provider Layer is independent; it is introduced when Knowledge Engine needs LLM inference.

---

## Sprint Map

| Sprint | Goal | Duration |
|---|---|---|
| Sprint 1 | `bin/ai inspect` working on 3 repositories | 2 weeks |
| Sprint 2 | `bin/ai knowledge extract` producing a knowledge graph | 2 weeks |
| Sprint 3 | Architecture revision cycle | 1 week |
| Sprint 4 | `bin/ai validate` producing a scored report | 2 weeks |
| Sprint 5 | `bin/ai briefing generate` auto-generating from real data | 1 week |
| Sprint 6 | Dashboard phase 1 (read-only, local) | 2 weeks |
| Sprint 7 | AI Provider Layer + Runtime Server | 2 weeks |
| Sprint 8 | Telegram + Railway deployment | 1 week |

---

## Constraints

1. No new canonical specification documents until Sprint 3 architecture revision.
2. Every new module must have at least one integration test before merge.
3. Tests must run on AI-Toolkit itself as the default target.
4. `requirements.txt` must list every dependency before it is used.
5. All CLI commands follow the pattern: `bin/ai <engine> <command> [path]`.

---

## Definition of Done (per sprint)

- [ ] All new code has unit or integration tests
- [ ] `bin/ai <command>` runs without error on AI-Toolkit
- [ ] `bin/ai <command>` runs without error on Trading Signals Platform
- [ ] `bin/ai <command>` runs without error on DROPi
- [ ] Results are committed to `.ai/reports/` in each target repository
- [ ] All existing tests still pass

---

## Files to Never Modify

- `standards/css/` — frozen
- `standards/csl/` — frozen
- `governance/` — frozen
- `docs/canonical/v4/`, `docs/canonical/v5/` — frozen
- `architecture/` — read-only reference

---

## Files to Consolidate (not rewrite)

| Target module | Sources to merge |
|---|---|
| `lib/python/repository_engine/` | `engineering_engine/repository_scanner.py`, `engineering_engine/repository_model.py`, `executable_repository_intelligence/file_classifier.py`, `executable_repository_intelligence/zone_classifier.py` |
| `lib/python/validation_engine/` | `audit_engine/`, `compliance_engine/`, `development_validator/` |
| `lib/python/knowledge_engine/` | `canonical_intelligence/engine.py`, `knowledge_graph/`, `knowledge_graph_v2/`, `semantic_repository_intelligence/` |

---

## Immediate Next Action

**Start implementing Issue #1** — see `IMPLEMENTATION_BACKLOG.md`.

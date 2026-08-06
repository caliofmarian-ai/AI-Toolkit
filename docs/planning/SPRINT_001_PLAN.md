# Sprint 001 Plan

**Duration:** 2 weeks (2026-08-07 — 2026-08-20)  
**Goal:** `bin/ai inspect <path>` working on AI-Toolkit, Trading Signals Platform, and DROPi, with the first usable Dashboard served from inspect output  
**Sprint ends with:** a committed Markdown inspection report for each repository and a local dashboard page that displays the latest inspect report for AI-Toolkit

---

## Sprint Objective

Deliver the first complete AI-Toolkit operational loop:

```bash
bin/ai inspect /path/to/repository
bin/ai dashboard serve
```

This sprint must:
1. walk the repository directory tree;
2. classify every file;
3. extract repository metrics and dependency summaries;
4. render a Markdown inspection report;
5. write the report to `<path>/.ai/reports/inspect-<date>.md`;
6. display the latest inspect report in a local Dashboard;
7. show the current Engineering Session header in the Dashboard.

This sprint delivers **Issue #1**, **Issue #2**, and **Issue #8** from the backlog.

---

## Issues in Scope

| Issue | Title | Complexity |
|---|---|---|
| #1 | Repository Engine: File Classification and CLI | Medium |
| #2 | Repository Engine: Dependency Graph | Low |
| #8 | Dashboard Phase 1: Inspect-First Local Dashboard | Medium |

---

## Day-by-Day Plan

### Day 1–2: Audit existing code and fix the inspect contract
- Read `lib/python/repository_engine/engine.py`.
- Read reusable classification and scanning code from existing modules.
- Confirm report shape and inspect CLI contract.
- Sketch the minimum Engineering Session fields required in Sprint 1.
- Write `tests/test_repository_engine_inspect.sh` skeleton.

### Day 3–5: Implement repository profiling
- Create `classifier.py`, `metrics.py`, and report rendering support.
- Extend `models.py` with the inspect profile structure.
- Add dependency extraction for root package files.
- Run tests and iterate until the report is stable.

### Day 6–7: Wire the inspect CLI
- Create `lib/python/repository_engine/cli.py`.
- Modify `bin/ai` to add `inspect <path>` routing.
- Run `bin/ai inspect .` on AI-Toolkit.
- Commit the first working inspect report to `.ai/reports/`.

### Day 8–10: Build the inspect-first Dashboard
- Add dashboard serving support to the runtime server or dashboard module.
- Render the latest inspect report as readable HTML.
- Add the Engineering Session header with active project, repository, branch, workspace, issue, sprint, AI provider, and engineering task.
- Add `bin/ai dashboard serve` routing.

### Day 11–12: Validate across repositories
- Run `bin/ai inspect /path/to/trading-signals-platform`.
- Run `bin/ai inspect /path/to/dropi`.
- Fix any failures.
- Verify the AI-Toolkit dashboard still displays the latest local inspect report.

### Day 13: Tests and cleanup
- Complete `tests/test_repository_engine_inspect.sh`.
- Add or complete `tests/test_dashboard_phase1.sh`.
- Ensure existing tests still pass.
- Update `requirements.txt` only if genuinely required.

### Day 14: Sprint review
- Verify all acceptance criteria.
- Confirm the Dashboard is usable from inspect output.
- Merge PR.

---

## Acceptance Criteria

- [ ] `bin/ai inspect .` completes without error on AI-Toolkit
- [ ] report written to `.ai/reports/inspect-<date>.md`
- [ ] report contains: Summary, File Distribution, Language Distribution, Tech Stack, Entry Points, Test Coverage Ratio, Documentation Coverage, Dependencies
- [ ] `bin/ai inspect /path/to/trading-signals-platform` completes without error
- [ ] `bin/ai inspect /path/to/dropi` completes without error
- [ ] `bin/ai dashboard serve` starts a local HTTP server on port 8080
- [ ] Dashboard displays the latest inspect report
- [ ] Dashboard shows the Engineering Session header
- [ ] `tests/test_repository_engine_inspect.sh` passes
- [ ] `tests/test_dashboard_phase1.sh` passes
- [ ] all previously passing tests still pass
- [ ] no new canonical specification documents were created during the sprint

---

## Files Created or Modified This Sprint

```
lib/python/repository_engine/classifier.py
lib/python/repository_engine/metrics.py
lib/python/repository_engine/models.py
lib/python/repository_engine/report.py
lib/python/repository_engine/deps.py
lib/python/repository_engine/cli.py
lib/python/dashboard/__init__.py
lib/python/dashboard/reader.py
lib/python/dashboard/renderer.py
lib/python/dashboard/server.py
bin/ai
tests/test_repository_engine_inspect.sh
tests/test_dashboard_phase1.sh
requirements.txt
```

---

## Done Condition

The sprint is done when these commands succeed on a clean AI-Toolkit clone:

```bash
bin/ai inspect .
bin/ai dashboard serve
bin/ai inspect ../trading-signals-platform
cat .ai/reports/inspect-*.md
```

And the Dashboard shows the latest inspect report in readable form.


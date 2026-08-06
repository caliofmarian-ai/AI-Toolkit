# Sprint 001 Plan

**Duration:** 2 weeks (2026-08-07 — 2026-08-20)  
**Goal:** `bin/ai inspect <path>` working on AI-Toolkit, Trading Signals Platform, and DROPi  
**Sprint ends with:** A committed Markdown inspection report for each of the three repositories

---

## Sprint Objective

Deliver one complete, useful, testable command:

```bash
bin/ai inspect /path/to/repository
```

The command must:
1. Walk the repository directory tree.
2. Classify every file (source, test, config, doc, generated, build, unknown).
3. Extract metrics: language distribution, file counts, entry points, test ratio.
4. Detect tech stack.
5. Render a Markdown report.
6. Write report to `<path>/.ai/reports/inspect-<date>.md`.

This sprint delivers **Issue #1** and **Issue #2** from the backlog.

---

## Issues in Scope

| Issue | Title | Complexity |
|---|---|---|
| #1 | Repository Engine: File Classification and CLI | Medium |
| #2 | Repository Engine: Dependency Graph | Low |

Issue #3 (validate CLI wiring) is stretch goal if both primary issues complete early.

---

## Day-by-Day Plan

### Day 1–2: Audit existing code, design interface

- Read `lib/python/repository_engine/engine.py` (current stub).
- Read `lib/python/executable_repository_intelligence/file_classifier.py`.
- Read `lib/python/executable_repository_intelligence/zone_classifier.py`.
- Read `lib/python/engineering_engine/repository_scanner.py`.
- Design `RepositoryProfile` dataclass (no code yet).
- Write `tests/test_repository_engine_inspect.sh` skeleton (failing tests first).

### Day 3–4: Implement classifier and metrics

- Create `lib/python/repository_engine/classifier.py`.
- Port classification logic from `executable_repository_intelligence/file_classifier.py`.
- Create `lib/python/repository_engine/metrics.py`.
- Write unit tests embedded in the shell test.
- Run tests — fix until green.

### Day 5–6: Implement profile and report

- Extend `lib/python/repository_engine/models.py` with `RepositoryProfile`.
- Add `RepositoryEngine.profile(root) -> RepositoryProfile`.
- Create `lib/python/repository_engine/report.py` with `ReportRenderer.render()`.
- Verify report output is valid Markdown.

### Day 7: Implement dependency extraction

- Create `lib/python/repository_engine/deps.py`.
- Parse `requirements.txt`, `package.json`, `go.mod` at repository root.
- Add `DependencyMap` to `RepositoryProfile`.
- Add Dependencies section to report renderer.

### Day 8–9: Wire CLI

- Create `lib/python/repository_engine/cli.py` with `inspect(path)` function.
- Modify `bin/ai` to add `inspect <path>` routing.
- Run `bin/ai inspect .` on AI-Toolkit — fix until clean.
- Commit first working report to `.ai/reports/`.

### Day 10–11: Validate on all three repositories

- Clone or access Trading Signals Platform.
- Run `bin/ai inspect /path/to/trading-signals-platform`.
- Fix any failures.
- Run `bin/ai inspect /path/to/dropi`.
- Fix any failures.
- Commit reports to each repository's `.ai/reports/`.

### Day 12–13: Tests and cleanup

- Complete `tests/test_repository_engine_inspect.sh`.
- Ensure all 8 existing test categories still pass.
- Remove any dead code introduced.
- Update `requirements.txt` with any new dependencies.

### Day 14: Sprint review and merge

- Run full test suite.
- Verify all acceptance criteria.
- Merge PR.
- Tag `v0.1.0-inspect`.

---

## Acceptance Criteria

- [ ] `bin/ai inspect .` completes without error on AI-Toolkit
- [ ] Report written to `.ai/reports/inspect-<date>.md`
- [ ] Report contains: Summary, File Distribution, Language Distribution, Tech Stack,
      Entry Points, Test Coverage Ratio, Documentation Coverage, Dependencies
- [ ] `bin/ai inspect /path/to/trading-signals-platform` completes without error
- [ ] `bin/ai inspect /path/to/dropi` completes without error
- [ ] `tests/test_repository_engine_inspect.sh` PASS
- [ ] All previously passing tests still pass
- [ ] No new canonical specification documents were created during the sprint

---

## Files Created or Modified This Sprint

```
lib/python/repository_engine/classifier.py     (new)
lib/python/repository_engine/metrics.py        (new)
lib/python/repository_engine/models.py         (extend)
lib/python/repository_engine/report.py         (new)
lib/python/repository_engine/deps.py           (new)
lib/python/repository_engine/cli.py            (new)
bin/ai                                          (extend)
tests/test_repository_engine_inspect.sh        (new)
requirements.txt                               (extend if needed)
```

---

## Done Condition

The sprint is done when this command succeeds on a clean clone:

```bash
git clone <trading-signals-platform>
cd AI-Toolkit
bin/ai inspect ../trading-signals-platform
cat ../trading-signals-platform/.ai/reports/inspect-*.md
```

And the output contains a readable, structured report.

---

## Start implementing Issue #1

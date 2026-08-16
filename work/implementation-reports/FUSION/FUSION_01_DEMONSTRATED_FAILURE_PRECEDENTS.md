# FUSION-01 — Demonstrated Failure and Orchestration Precedents

## Authority classification

This material conserves demonstrated execution precedents from FUSION-01.

It is evidence and operational memory.

It is not Canon.

It does not independently authorize repository mutation.

Human Authority remains the mutation authority.

---

## PRECEDENT 1 — Import topology

### Demonstrated event

Initial FUSION-01 focused-test collection failed with:

`ModuleNotFoundError: No module named 'python'`

### Demonstrated cause

The repository uses an existing import topology in which runtime/dashboard
execution requires the repository `lib` root on `PYTHONPATH`, while existing
epistemic invocation also has demonstrated compatible package roots.

### Recovery

Respect the demonstrated topology narrowly.

Do not perform broad package normalization merely because two valid invocation
forms exist.

### Result

Focused FUSION-01 tests subsequently passed 7/7.

---

## PRECEDENT 2 — Runtime regression TIMEOUT

A runtime regression invocation reached HTTP server configuration and exceeded
its 180-second execution bound.

Classification:

`TIMEOUT 180s`

This remains TIMEOUT.

It is not retroactively PASS.

---

## PRECEDENT 3 — Bounded bootstrap TIMEOUT

A bounded RuntimeBootstrap diagnosis reached HTTP server configuration but
`RuntimeBootstrap.bootstrap()` did not return within 90 seconds.

Classification:

`TIMEOUT 90s`

This remains TIMEOUT.

---

## PRECEDENT 4 — Engineering-context reconstruction

Instrumentation demonstrated that synchronous engineering-context
reconstruction can consume or exceed startup execution bounds.

Recovery introduced during FUSION-01 keeps this startup physiology bounded.

If reconstruction exceeds its bound, runtime may continue with engineering
context unavailable.

A timeout does not become successful reconstruction.

Unavailable does not become PASS.

---

## PRECEDENT 5 — Subsequent bootstrap TIMEOUT

A later bounded complete bootstrap exceeded 45 seconds.

Classification:

`TIMEOUT 45s`

This remains TIMEOUT.

---

## PRECEDENT 6 — Subsequent bootstrap TIMEOUT

A later bounded execution reached:

`engineering context initialized=False`

and exceeded its 40-second bound.

Classification:

`TIMEOUT 40s`

This remains TIMEOUT.

---

## PRECEDENT 7 — Do not infer blocker from last visible log line

Punctual instrumentation demonstrated that the dashboard path returned.

Observed operations included successful return from:

- engineering-context loading;
- AI control-center loading;
- session loading;
- repository-profile loading;
- workspace-summary loading;
- report loading;
- runtime loading;
- diagnostics loading;
- capability loading;
- `EngineeringDashboardService.build(refresh=False)`;
- `_step_initialize_dashboard()`.

Therefore the last visible line before a process timeout is not sufficient
evidence that the corresponding component is the blocker.

Instrument the operation itself before recovery.

---

## PRECEDENT 8 — Complete bootstrap success does not rewrite history

A phase-timed complete bootstrap subsequently returned successfully.

Demonstrated phase result included:

- engineering-context reconstruction bounded at 5 seconds;
- dashboard initialization returned;
- external interfaces returned;
- health verification returned;
- runtime snapshot persistence returned;
- runtime reached READY;
- organism boundary was reachable;
- existing API reached organism state;
- existing dashboard shared the organism boundary;
- graceful shutdown returned.

A later final acceptance execution returned in approximately 6.646 seconds.

These later successful executions do not rewrite earlier TIMEOUT executions.

---

## PRECEDENT 9 — Continuation artifact ordering

### Demonstrated orchestration error

A FUSION-01 conservation script stopped while classifying generated repository
effects.

Because execution stopped before the later report-materialization step,
`FUSION_01_RUNTIME_EPISTEMIC_ORGANISM.md` had not yet been produced.

A subsequent continuation script incorrectly required that future output file
to exist as a precondition.

The continuation therefore stopped with:

`expected completed FUSION-01 material missing`

even though the production implementation itself remained intact.

### Demonstrated cause

The continuation contract confused:

1. artifacts already produced before the real stop point;

with:

2. artifacts scheduled to be produced after that stop point.

### Canonical operational lesson

An artifact produced after the actual stop point of a run cannot be treated
as a precondition for continuation of that run.

Continuation must reconstruct the real execution frontier first.

Artifacts before that frontier may be preconditions.

Artifacts after that frontier remain outputs.

### Recovery

The corrected continuation verifies only the already-demonstrated production
implementation as its precondition.

The implementation report, generated-effect report and final conservation
artifacts are materialized as outputs.

No reset is performed.

No already-demonstrated test is repeated merely to recover from this
orchestration error.

---

## General demonstrated-failure discipline

For future transformations:

1. identify the real execution frontier;
2. preserve historical classifications exactly;
3. do not infer PASS from later success;
4. do not infer FAIL from UNKNOWN;
5. do not infer a blocker from the last visible log line;
6. instrument individual operations with local bounds;
7. distinguish cumulative latency from deadlock;
8. classify generated state by producer and content;
9. do not delete unexplained effects automatically;
10. do not require future outputs as continuation preconditions;
11. do not let orchestration assumptions erase successfully completed work;
12. Human Authority remains the execution authority.


---

## PRECEDENT 10 — Untracked directory compaction in Git status

### Demonstrated orchestration event

During final FUSION-01 worktree classification, Git reported:

`?? tests/fusion/`

and:

`?? work/implementation-reports/FUSION/`

rather than enumerating every untracked file beneath those directories.

The classifier recognized only exact deliberate file paths.

As a result, the two deliberate directory roots were incorrectly classified
as UNKNOWN even though their intended files had already been explicitly
created and verified.

Execution stopped safely before staging or commit.

### Demonstrated cause

`git status --porcelain` may represent a fully untracked directory as one
directory-level entry.

A classifier that understands only exact intended file paths cannot safely
classify such a status representation.

### Operational lesson

Repository-effect classification must understand both:

1. exact deliberate file paths;

and:

2. deliberate directory roots when Git legitimately collapses their untracked
   contents into a directory-level status entry.

A collapsed untracked directory must not automatically become UNKNOWN when
its root and intended contents are already part of the deliberate
transformation boundary.

### Recovery

The corrected conservation classifier recognizes:

`tests/fusion/`

and:

`work/implementation-reports/FUSION/`

as deliberate roots.

Before staging, it still verifies the exact intended files individually.

Staging remains file-explicit rather than directory-wide.

Therefore recognizing a deliberate directory root for classification does not
authorize arbitrary files beneath that root to enter the commit.

No reset was required.

No previously demonstrated test was repeated.


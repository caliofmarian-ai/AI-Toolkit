# FUSION-02 — Demonstrated Termux Execution Error Memory

## Epistemic status

These records are demonstrated execution precedents.

They are Evidence of observed execution behavior.

They are not Canon.

They do not create autonomous epistemic authority.

## Precedent — `/tmp` is not a portable writable evidence destination

### Demonstrated observation

During the FUSION-02 durable-conversation execution in Termux, commands using:

`tee /tmp/fusion02-focused.log`

and:

`tee /tmp/fusion02-ai-platform-regression.log`

reported:

`Permission denied`

The focused Python tests themselves subsequently completed successfully.

### Demonstrated conclusion

For this demonstrated Termux environment, `/tmp` cannot be assumed to be a writable portable evidence location.

### Recovery demonstrated

Subsequent execution stored evidence under repository-local execution/evidence paths rather than depending on `/tmp`.

No broader claim is made about every Termux installation or every Android environment.

---

## Precedent — hardcoded GitHub Actions workspace path is not portable

### Demonstrated observation

The repository regression script attempted:

`cd /home/runner/work/AI-Toolkit/AI-Toolkit`

during local Termux execution.

The path did not exist.

The regression therefore failed for execution-environment reasons rather than because its tested AI Platform behavior had failed.

### Demonstrated conclusion

A hardcoded GitHub Actions workspace path cannot be treated as a portable repository root for local Termux execution.

### Recovery demonstrated

The same regression body was executed from the actual repository root in Termux.

Four AI Platform regression tests then passed.

### Boundary

This precedent does not claim that the GitHub Actions path is invalid inside GitHub Actions.

It records only that the path is not portable across the demonstrated execution environments.

---

## Error Memory semantics

These precedents may inform future execution planning and context reconstruction.

They remain demonstrated failure/recovery Evidence.

They are not:

- Canon;
- automatic Sedimentation;
- Human Authority;
- permission for autonomous mutation.

---

## Precedent — circular import introduced by context reconstruction integration

### Demonstrated observation

During FUSION-02 focused acceptance, pytest collection failed before test
execution with:

`ImportError: cannot import name 'EpistemicOrganismAccess' from partially initialized module 'python.runtime.organism'`

The demonstrated import path was:

`python.runtime.organism`
→ `python.ai_platform.sessions`
→ package initialization of `python.ai_platform`
→ `python.ai_platform.service`
→ `python.ai_platform.conversation_context`
→ `python.runtime.organism`

### Demonstrated cause

`python.ai_platform.__init__` eagerly imports `AIPlatformService`.

The new `conversation_context` module imported
`EpistemicOrganismAccess` at module-import time.

Therefore importing `python.ai_platform.sessions` while
`python.runtime.organism` was still initializing caused package
initialization to return to the partially initialized organism module.

### Recovery applied

The context reconstructor continues to reuse the REAL
`EpistemicOrganismAccess`, but its import is deferred until
`ConversationContextReconstructor` construction.

This removes the module-initialization cycle without:

- creating another organism;
- changing epistemic authority;
- replacing AISessionEngine;
- replacing Persistent Experience;
- changing RAW/Evidence/Canon semantics.

### Epistemic status

This is demonstrated implementation failure/recovery Evidence.

It is not Canon.

It does not create automatic Sedimentation.

---

## Observed execution event — real-provider implementation preflight

### Observed condition

The real-provider implementation Bash stopped before modifying provider code
because its preflight used the following overly broad condition:

`git status --porcelain != empty`

The working tree contained FUSION-02 runtime/evidence artifacts:

- `.ai/ai_sessions/`
- `.fusion-02-evidence/`
- `work/implementation-reports/FUSION/FUSION_02_TERMUX_EXECUTION_ERROR_MEMORY.md`

These were untracked artifacts rather than pre-existing tracked source-code
modifications.

### Failure classification

**Preflight classification error.**

The implementation correctly failed closed, so no provider source code was
partially transformed.

However, the preflight incorrectly treated legitimate untracked FUSION-02
runtime/evidence state as equivalent to tracked implementation changes.

### Conserved lesson

Future implementation preflight must distinguish:

1. tracked source modifications;
2. staged modifications;
3. legitimate untracked runtime/evidence/report artifacts.

Untracked evidence must not be deleted or reset merely to obtain a clean
working tree.

Source transformation may proceed when tracked and staged state are clean,
while explicitly preserving legitimate evidence artifacts.

### Recovery rule

Never use destructive cleanup (`git clean`, reset of evidence, deletion of
sessions) to solve this condition.

Verify tracked state independently with:

- `git diff --quiet`
- `git diff --cached --quiet`

and preserve runtime/evidence artifacts.


## Demonstrated execution precedent — incompatible test discovery

### Observation

During the FUSION-02 real-provider transformation, validation invoked a
test-discovery mechanism that executed zero tests:

    Ran 0 tests in 0.000s
    NO TESTS RAN

### Classification

DEMONSTRATED EXECUTION / ORCHESTRATION ERROR.

Zero executed tests are:

- not PASS;
- not evidence that production is defective;
- not evidence that production is correct.

The production transformation must therefore be preserved and validated
with the repository's actual pytest physiology.

### Recovery

Continue from the materialized worktree without reset or provider
reimplementation and execute the relevant tests with pytest.

### Boundary

This precedent contains no provider credential or secret.

Human Authority remains the mutation authority.

## Demonstrated execution precedent — provider acceptance tests absent

Observed during FUSION-02 real-provider validation:

- the real-provider implementation had already been materialized locally;
- validation searched for executable pytest acceptance for that transformation;
- no matching provider acceptance tests existed;
- execution stopped before declaring provider readiness.

Classification:

`PROVIDER TESTS ABSENT -> ACCEPTANCE CANNOT DECLARE PASS`

This result is not evidence that the production provider implementation is
defective. It demonstrates an acceptance-topology deficiency: the transformed
provider boundary existed without executable focused acceptance proving its
contract.

Recovery:

Materialize focused pytest tests against the actual adapter and pipeline
contracts, with the external HTTP boundary replaced only inside the tests.

Epistemic distinction:

`NO TESTS FOUND != PASS`
`NO TESTS FOUND != PRODUCTION FAILURE`

## Real-provider focused acceptance exposed a contract mismatch

The newly materialized pytest acceptance executed against the already
materialized real-provider implementation and returned non-zero.

This result is a demonstrated test/production contract mismatch and is not
converted to PASS.

The exact pytest output is retained locally in:

`.fusion-02-evidence/real-provider-pytest.log`

No automatic broad production rewrite was performed by this continuation.
Recovery must be limited to the exact failed contract demonstrated by that log.
## Demonstrated precedent — stale provider test-double contract

Classification: TEST CONTRACT PRECEDENT

Demonstrated during FUSION-02 real-provider acceptance.

Production contract:

AIRequestPipeline.run()
→ adapter.complete(..., provider_settings=provider_settings)

Observed failure:

Provider acceptance tests executed with pytest, but legacy test doubles
remained on the earlier adapter.complete contract and rejected the
provider_settings keyword argument.

Interpretation:

stale provider test-double
→ incompatibility with provider_settings
≠ demonstrated production defect.

Recovery rule:

When production and the real provider adapter agree on an evolved
contract, update stale test doubles to represent that demonstrated
contract. Do not weaken production merely to satisfy the stale fake.

The provider_settings argument must remain part of the production
boundary because provider credentials/configuration are resolved through
that boundary.

No secret value is recorded here.
## Demonstrated precedent — HTTP monkeypatch must follow the real adapter boundary

Classification: TEST INFRASTRUCTURE PRECEDENT

During FUSION-02 real-provider acceptance, provider tests attempted to
patch an assumed HTTP callable rather than the callable actually used by
the materialized provider adapter.

Observed result:

AttributeError during monkeypatch setup.

Interpretation:

incorrect test HTTP patch target
!= demonstrated production provider defect.

Recovery rule:

Inspect the real provider adapter first and patch the exact external HTTP
boundary it invokes. Do not modify production merely to make an assumed
test patch target exist.

No external provider call and no provider secret are recorded by this
precedent.
## Demonstrated precedent — compiled test artifact must not substitute source regression

Classification: TEST DISCOVERY / EXECUTION INFRASTRUCTURE PRECEDENT

Observed during FUSION-02 provider conservation:

Context-regression discovery selected:

`tests/fusion/__pycache__/test_fusion_02_context_reconstruction.cpython-312.pyc`

Pytest therefore reported that no executable test source was found.

Demonstrated interpretation:

test discovery selecting `.pyc` / `__pycache__`
!= FUSION-02 production defect.

A compiled Python artifact cannot substitute execution of the real
source regression.

Recovery rule:

Test discovery must operate only on source files matching `*.py` and
must explicitly exclude `__pycache__`, `.pyc`, and compiled artifacts.

Previously demonstrated PASS results must not be invalidated or rerun
merely because a later discovery mechanism selected a compiled artifact.
## Demonstrated precedent — generated execution scratch requires provenance

Classification: EXECUTION EFFECT CLASSIFICATION PRECEDENT

During FUSION-02 conservation, the untracked `.fusion-02-run/` effect
was encountered after the real context regression had already passed.

The effect was inspected before disposition.

Result:

`GENERATED_FUSION02_EXECUTION_SCRATCH`

Demonstrated rule:

An untracked execution directory must not be classified solely from
its name.

Its tracked status, contents, and available producer/execution
references must be examined first.

A demonstrated execution scratch/evidence effect is not deliberate
production material and must not be staged merely because it exists
in the worktree.

The effect is preserved locally and is not automatically deleted.

This classification does not invalidate previously demonstrated
acceptance results.
## Demonstrated precedent — git diff --check diagnostic continuation line

Classification: EXECUTION / ORCHESTRATION PRECEDENT

During final FUSION-02 conservation, `git diff --check` reported one
demonstrated trailing-whitespace defect using a diagnostic pair:

- an error header identifying the file and line;
- a following `+` patch-context line showing the offending added line.

The execution instrument incorrectly filtered the error header and then
classified the diagnostic `+` continuation line as a second independent
integrity defect.

This was a Bash diagnostic-parsing error.

It was not:

- a second source defect;
- a provider defect;
- an AIRequestPipeline defect;
- a FUSION-02 behavioral regression.

Recovery:

Parse actual `git diff --check` error headers as defects and do not
reinterpret their patch-context continuation lines as independent
errors.

Demonstrated rule:

Diagnostic output belonging to one reported failure must not be
reclassified as an additional failure merely because it occupies a
separate output line.

## FUSION-02 — pytest repository import-path precedent

Observed during OpenAI HTTP diagnostic acceptance:

`pytest` reached test collection but failed with:

`ModuleNotFoundError: No module named 'python'`

The repository package under test is rooted beneath `lib/`, while that
execution did not establish `lib/` on Python's import path.

Classification:

`PYTEST_IMPORT_PATH_NOT_ESTABLISHED`

This is test-runner/environment infrastructure evidence.

It is not evidence of a production defect in OpenAIProviderAdapter and
must not cause production code to be modified.

Recovery rule:

When repository tests import the `python.*` package from `lib/python`,
execute the bounded pytest invocation with the repository `lib/`
directory present on `PYTHONPATH`, unless the repository's canonical
runner establishes the equivalent import path itself.

## FUSION-02 — stale provider test-helper reference

Observed during OpenAI HTTP diagnostic acceptance:

Two newly materialized provider tests called:

`_openai_adapter()`

The established test module helper is:

`_adapter()`

Observed result:

`NameError: name '_openai_adapter' is not defined`

Classification:

`STALE_PROVIDER_TEST_HELPER_REFERENCE`

This is test-infrastructure evidence and is not evidence of a production
defect in OpenAIProviderAdapter.

Recovery rule:

New acceptance tests must reuse the demonstrated helper vocabulary of the
existing test module unless a new helper is deliberately introduced and
defined.

Do not modify or weaken production code to satisfy an undefined test helper.

## FUSION-02 — undefined diagnostic logger

### Classification

`UNDEFINED_DIAGNOSTIC_LOGGER`

### Observed failure

The OpenAI token-budget diagnostic introduced:

`logger.info(...)`

inside `OpenAIProviderAdapter.complete()`.

The module did not import `logging` and did not define `logger`.

This caused every provider path reaching the diagnostic boundary to fail
before `urllib.request.urlopen()` with:

`NameError: name 'logger' is not defined`

Eight provider tests therefore failed from one shared instrumentation defect.

### Root cause

The instrumentation patch introduced a new module-level dependency without
first verifying that the target module already possessed that dependency.

### Conservation rule

Before inserting instrumentation that references a symbol:

1. verify whether the symbol is imported or defined in the target module;
2. if not, materialize the smallest explicit dependency required;
3. run static compilation before behavioral tests;
4. treat multiple downstream failures caused by one missing shared symbol as
   one root defect, not as independent production defects;
5. do not weaken provider failure behavior to make instrumentation pass.

### Recovery

The module now imports Python standard-library `logging` and defines:

`logger = logging.getLogger(__name__)`

The OpenAI request path, provider failure semantics, credentials, conversation
content, and persistence semantics are otherwise unchanged.

## FUSION-02 — generated test blank line at EOF

### Classification

`GENERATED_TEST_BLANK_LINE_AT_EOF`

### Observed failure

After all bounded FUSION-02 tests passed, staged-diff integrity stopped with:

`tests/fusion/test_fusion_02_real_provider.py:652: new blank line at EOF.`

### Root cause

The generated test append operation left more than the canonical single
terminal newline after the final substantive Python line.

This was not a behavioral test failure and not a production defect.

### Conservation rule

For generated or appended source files:

1. normalize CRLF/CR to LF;
2. remove trailing spaces and tabs;
3. remove empty lines following the final substantive line;
4. terminate the file with exactly one newline;
5. run `git diff --cached --check` before conservation.

Previously demonstrated behavioral tests do not need to be rerun when the
only subsequent mutation is deterministic EOF normalization and static syntax
validation remains PASS.

## Railway structured logging visibility precedent

Observed during FUSION-02 OpenAI token-budget diagnosis:

- Python `logging` accepted the diagnostic measurements through
  `extra={"openai_request_budget": ...}`.
- Railway retained the log event but its inspected JSON did not expose
  that custom `extra` object.
- Therefore successful insertion into Python `logging.extra` is not
  sufficient evidence that an operational diagnostic is visible in
  Railway.
- For bounded operational measurements required during live acceptance,
  non-sensitive scalar values must also be serialized into the standard
  log message while structured metadata may be retained in parallel.
- Never serialize credentials, Authorization headers, human message
  content, reconstructed context content, or complete provider payloads
  merely to improve log visibility.

## FUSION-02 — local/runtime session boundary

### Classification

`LOCAL_RUNTIME_SESSION_BOUNDARY_ASSUMPTION`

### Demonstrated failure

A Termux diagnostic attempted to locate the live Owner AI Chat session at:

`.ai/ai_sessions`

The directory did not exist in the local checkout.

### Root cause

AISessionEngine persists session files relative to the repository root of the
running process.

The live Owner AI Chat request is executed on Railway.

Therefore runtime session state created on Railway is not automatically
present in the separate Termux checkout.

### Engineering rule

Never assume ephemeral or deployment-local runtime state exists in another
repository checkout merely because both checkouts share the same Git commit.

When diagnosis depends on runtime-generated state:

1. inspect static contracts locally;
2. identify the runtime observation boundary;
3. instrument sanitized measurements at that boundary;
4. deploy through the normal Git path;
5. observe the real runtime execution;
6. never substitute synthetic state and call it production evidence.

Runtime diagnostics must report metadata, not secret or conversational
content.

## FUSION-02 — pipeline context argument contract

### Classification

`PIPELINE_CONTEXT_OVERRIDE_ARGUMENT`

### Demonstrated failure

A diagnostic instrument attempted to discover the reconstructed context at
`self.pipeline.run()` by searching for a keyword argument named `context`.

The actual production call uses:

`context_override=reconstructed_context`

The instrument therefore stopped before mutation.

### Root cause

The diagnostic relied on an assumed argument name instead of first proving
the exact production call contract.

### Engineering rule

Before AST-based mutation at a function-call boundary:

1. inspect the exact current call;
2. prove the receiver and method;
3. enumerate the actual keyword arguments;
4. derive the target expression from the demonstrated source;
5. fail closed when the contract differs;
6. never substitute an assumed keyword name.

For FUSION-02, the provider-bound reconstructed context is passed through
`context_override`.

## RUN-01 / T1 execution error — 2026-08-16T20:37:40Z

- Stage: `repository-authority`
- Exit code: `14`
- Error: Worktree is not clean before RUN-01.
- Conservation rule: fail closed; no production mutation authorized.
- Required prevention: inspect this demonstrated failure before the next recovery run.

## RUN-01 / T1 execution error — 2026-08-16T20:46:05Z

- Stage: `integrity-validation`
- Exit code: `62`
- Error: git diff --cached --check failed.
- Production mutation authorized: NO
- Recovery rule: inspect demonstrated failure before retry.

## RUN-02 / T2+T3 execution failure

- Timestamp: 2026-08-16T20:57:35Z
- Stage: authority
- Failure: Worktree must be clean before RUN-02.
- HEAD: e1015e71d7888045e825c94dcd60edeaab6e739d
- Branch: main
- Recovery rule: inspect demonstrated anatomy before further mutation.

## RUN-02 / T2+T3 execution failure

- Timestamp: 2026-08-16T21:04:46Z
- Authority: 0fc3c166c78c09e57329307398e6421bc7169d44
- Stage: authority
- Failure: Worktree is not clean.
- Recovery: inspect demonstrated anatomy before mutation.

## RUN-04 false UEM preflight anatomy

**Classification:** deterministic Bash generated from an unverified API assumption

**Observed failure:**

The first RUN-04 execution stopped during the UEM physiology preflight with:

`AssertionError: outgoing`

The generated preflight asserted that `UniversalEngineeringModel` exposed:

- `outgoing`
- `incoming`
- `neighbors`

Direct inspection of the exact repository authority demonstrated that these methods do not exist.

The real `UniversalEngineeringModel` interface at the affected authority exposes:

- `add_object`
- `get_object`
- `all_objects`
- `objects_by_type`
- `has_object`
- `add_relationship`
- `all_relationships`
- `relationships_of_type`
- `statistics`
- `__len__`
- `__iter__`

`UemBuilder.build(semantic_results)` is the demonstrated construction boundary.

**Root cause:**

The Bash contained a convenience traversal API assumption that was not verified against the exact source before execution.

This violated the established execution discipline:

`INSPECT REPOSITORY → KNOW ANATOMY → GENERATE DETERMINISTIC BASH → PREFLIGHT VERIFY`

The failure was not a defect in UEM.

It was a defect in the generated preflight contract.

**Secondary execution defect:**

The failing Python block used:

`python ... || exit 30`

instead of routing the failure through the Bash `fail()` function.

Therefore the original RUN-04 failure did not automatically update Error Memory.

**Permanent prevention rule:**

A deterministic repository preflight may assert only exact symbols, signatures, fields, methods and boundaries verified from the expected repository authority.

Do not infer convenience methods from architectural descriptions.

All qualifying Python preflight failures must return through the Bash error-conservation path rather than bypassing it with a direct shell exit.

**Recovery:**

RUN-04 recovery replaces the false method assumptions with the exact demonstrated UEM interface and routes all subsequent preflight failures through Error Memory conservation.

## RUN-04 recovery execution error — 2026-08-16T22:06:12Z

**Stage:** materialization-preflight

**Failure:** Knowledge Materialization anatomy differs from inspected authority.

**Preventive rule:** Deterministic Termux Bash must verify only repository anatomy already demonstrated from the exact authority. A preflight must never assert convenience APIs that were not verified in source.

## FUSION-02 — E13/T9 stale retrieval fixture authority contract

### Classification

`STALE_T9_RETRIEVAL_TEST_FIXTURE_AUTHORITY_CONTRACT`

### Demonstrated observation

The E13/T9 focused acceptance constructed a synthetic retrieval mapping
without the established field:

`authority_conferred=False`

The existing production contract explicitly refuses retrieval input unless
that field is exactly false.

Observed result:

`ValueError: Retrieval must not confer epistemic authority`

### Root cause

The new test fixture omitted an already-established retrieval invariant.

This failure did not demonstrate a defect in the production authority guard.

### Recovery rule

When constructing retrieval fixtures for Working Context acceptance, preserve
the established retrieval contract explicitly, including
`authority_conferred=False`.

Do not weaken or remove the production authority guard to satisfy an
incomplete test fixture.

This is demonstrated execution Evidence, not Canon.

## FUSION-02 — E13/T9 incomplete synthetic retrieval contract

### Classification

`INCOMPLETE_T9_SYNTHETIC_RETRIEVAL_CONTRACT`

### Demonstrated observation

The focused E13/T9 test fixture was repaired once for
`authority_conferred=False` but still omitted the second already-established
Working Context retrieval invariant:

`working_context_materialized=False`

The production guard correctly stopped with:

`ValueError: Working Context must be materialized exactly once from candidate retrieval`

### Direct repository verification

The pre-existing authoritative test
`tests/fusion/test_fusion_02_first_working_context_materialization.py`
demonstrates that valid candidate retrieval fixtures explicitly contain both:

- `authority_conferred: False`
- `working_context_materialized: False`

It also contains negative tests proving that authority promotion and an
already-materialized retrieval must be rejected.

### Recovery rule

Before constructing a new synthetic retrieval fixture, inspect and reuse the
complete established retrieval contract from existing acceptance tests.

Do not discover required fixture fields one exception at a time.

Do not weaken production guards to accommodate an incomplete fixture.

This is demonstrated execution Evidence, not Canon.

## FUSION-02 — E13/T9 generated report EOF whitespace

### Classification

`GENERATED_REPORT_BLANK_LINE_AT_EOF`

### Demonstrated observation

All E13/T9 acceptance and conservation checks passed, but
`git diff --cached --check` stopped the commit because the generated
implementation report ended with an additional blank line.

Observed diagnostic:

`FUSION_02_E13_T9_IMPLEMENTATION.md:587: new blank line at EOF.`

### Root cause

The report generator concatenated a newline after evolution-tree content that
already terminated with newline characters.

### Recovery rule

Generated Markdown reports must be normalized with `rstrip() + "\n"` before
staging.

Do not alter production or acceptance semantics to recover from a whitespace
failure.

This is demonstrated execution Evidence, not Canon.

## FUSION-02 — E13/T9 Error Memory gate assumed an absent precedent

### Classification

`ERROR_MEMORY_GATE_FALSE_REQUIRED_PRECEDENT`

### Demonstrated observation

The E13/T9 semantic-completion batch stopped before production mutation
because its Error Memory gate asserted that the literal precedent:

`TERMUX_BATCH_MESSAGE_FRAGMENTATION`

must already exist in the authoritative Error Memory file.

Direct GitHub inspection of the authoritative file demonstrated that this
literal record was not present there.

The batch therefore confused:

- consulting Error Memory before mutation;

with:

- requiring one particular historical label to exist in Error Memory.

### Root cause

The execution gate encoded an invented completeness assumption about Error
Memory instead of reading and respecting the records that actually exist.

### Recovery rule

Before mutation:

1. Error Memory must be read;
2. its demonstrated precedents must constrain execution;
3. absence of an unrelated historical label must not fail the batch;
4. no precedent may be invented merely to satisfy a gate;
5. newly demonstrated failures are appended as Evidence, not Canon.

Production was not modified by this failure.

## FUSION-02 — E13/T9 certification/tree authority mismatch

### Classification

`AUTHORITY_BRANCH_LEFT_UNCHECKED_AFTER_CERTIFICATION`

### Demonstrated observation

E13/T9 was marked FINALIZAT / CERTIFICAT while its persistent evolution tree
still showed the authority branch as incomplete.

Production already demonstrated:

- technical observations do not become epistemic authority;
- retrieval has authority_conferred=False;
- Human Authority remains preserved.

The defect was therefore in evolution-state conservation, not in production
physiology.

### Recovery

The authority branch was reconciled with demonstrated production behavior.

No production mutation was required.

## FUSION-02 — E14/T10 representative budget fixture omitted relationships

### Classification

`E14-ERR-001 — REPRESENTATIVE_BUDGET_FIXTURE_OMITTED_RELATIONSHIPS`

### Demonstrated observation

The first E14/T10 focused acceptance executed five tests.

Four passed.

The representative compaction test expected one complete evidence object to
fit, but the calculated fixture budget included:

- base Working Context;
- first evidence object;
- matching provenance;
- matching epistemic result;

while omitting the relationship collection that the production governor also
preserves before evaluating the candidate.

Production therefore correctly determined that the complete candidate did not
fit and retained zero evidence objects rather than partially truncating one.

### Root cause

The synthetic acceptance budget did not measure the same complete candidate
shape that production evaluates.

This was a test-fixture construction error, not demonstrated production
corruption.

### Recovery rule

Representative budget fixtures must calculate capacity from the complete
candidate object that production is required to preserve.

Production whole-object and provenance-preservation guards must not be weakened
to satisfy an undersized synthetic fixture.

### Conservation

The failed production mutation is preserved.

No reset is authorized.

No force push is authorized.

This record is demonstrated execution Evidence, not Canon.

## FUSION-02 — E15/T11 shadow interface regression

### Classification

`E15_SHADOW_PIPELINE_TEST_DOUBLE_SIGNATURE_REGRESSION`

### Demonstrated observation

The first E15/T11 Shadow Pipeline implementation passed its dedicated
acceptance group but failed the complete FUSION regression:

- 8 historical tests failed;
- 173 historical tests passed;
- all failures occurred before certification/commit;
- the failure was caused by service.py passing a new
  `shadow_working_context` keyword directly through the historical
  `pipeline.run(...)` call boundary.

Historical tests intentionally replace `pipeline.run` with bounded test
doubles implementing the established call contract. The new keyword therefore
changed the service-level invocation contract even though the intended
production behavior was observation-only.

### Root cause

The attempted shadow physiology was attached by expanding an established
service-to-pipeline method invocation instead of introducing an orthogonal
observation channel.

This violated conservation of the historical invocation boundary.

### Recovery rule

For E15/T11:

1. `AIPlatformService.ask_repository()` must retain the established
   `pipeline.run(...)` call signature;
2. shadow state must be supplied through a separate observation interface;
3. historical test doubles must not need modification merely to accommodate
   shadow physiology;
4. the provider payload remains legacy-authoritative;
5. shadow observation must not persist epistemic state;
6. complete FUSION regression must pass before E15 certification.

The failed attempt did not reach GitHub main.

## FUSION-02 — E18/T14 Session/Journey integration regression

### Classification

`E18_SESSION_JOURNEY_LIFETIME_IDENTITY_AND_TEST_BOUNDARY_REGRESSION`

### Demonstrated failures

The first E18/T14 implementation passed its focused acceptance but failed the
complete FUSION regression in two established behaviors.

1. A durable Conversation may receive a new human request and therefore begin
   a new Journey while retaining the same session identity.

   The failed implementation incorrectly treated the first Journey ID as a
   lifetime identity of the session and rejected a later Journey.

2. Existing service-level tests replace the session persistence boundary with
   controlled test doubles.

   The failed integration introduced a new direct persistence call that was
   not part of those established doubles, causing the service to attempt a
   physical session lookup for a synthetic session.

### Root cause

Conversation identity and Journey identity were coupled too strongly.

The correct relation is:

Conversation = durable dialogue container.

Journey = cognitive trajectory for a particular information need/request.

A Conversation may therefore reference the CURRENT Journey and later replace
that reference when a new request starts a new Journey.

The integration must also preserve the established service test boundary.

### Recovery rule

- update the compact current Journey reference;
- do not reject a legitimate new Journey on the same Conversation;
- preserve Conversation history and Experience identity;
- preserve Working Context separation;
- make service binding compatible with established session doubles;
- run the complete FUSION regression before certification.

This failure is Evidence, not Canon.

---

## Demonstrated execution precedent — Python source newline escaped as literal text

### Observation

During FUSION-02 E19/T15 implementation, the Session organ transformation
completed its textual write, but the immediate Python syntax gate failed with:

`SyntaxError: unexpected character after line continuation character`

The demonstrated corrupted source fragment was:

`return {}\n`

where `\n` existed as two literal source characters rather than as an actual
line ending.

### Classification

**E19-ERR-001 — PYTHON_SOURCE_LITERAL_NEWLINE_ESCAPE_CORRUPTION**

This was an implementation-script serialization error.

It is not evidence that the E19/T15 physiology is conceptually invalid.

The failure occurred before E19/T15 acceptance and before commit/push.

### Root cause

The previous Bash generated Python source through a transformation whose final
write encoded a newline escape incorrectly, materializing the characters
backslash+n into `sessions.py`.

### Recovery rule

When a Bash transforms Python source, the resulting source must be syntax
checked immediately.

If an exact literal newline escape is demonstrated in source, repair only the
demonstrated corruption and preserve the remaining materialized implementation.

Do not use a repository-wide reset when the failed mutation can be causally and
exactly recovered.

### Epistemic boundary

This record is demonstrated Error Memory Evidence.

It is not Canon.

It does not confer authority.

Human Authority remains conserved.

## FUSION-02 — E19/T15 synthetic session fixture bypassed established experience boundary

### Classification

`E19-ERR-002 — INCOMPLETE_SYNTHETIC_SESSION_EXPERIENCE_BOUNDARY_FIXTURE`

### Demonstrated observation

The E19/T15 focused acceptance failed before provider execution.

The synthetic service test replaced `AISessionEngine.create()` and `AISessionEngine.get()`
but left the real `bind_experience()` persistence operation active.

The real `bind_experience()` correctly rejected the synthetic session because that
session was intentionally absent from persistent storage.

### Root cause

The new acceptance fixture modeled only part of the already-established synthetic
service boundary.

The defect is in the test fixture, not in production persistence physiology.

### Recovery rule

Synthetic service tests must mock the complete established pre-provider persistence
boundary they intentionally replace.

Production `bind_experience()` must remain fail-closed for unknown persistent sessions.

No production guard may be weakened merely to satisfy a synthetic fixture.

Evidence, not Canon.

## FUSION-02 — E19/T15 synthetic session omitted ConversationContext boundary

### Classification

`E19-ERR-003 — INCOMPLETE_SYNTHETIC_SESSION_CONTEXT_RECONSTRUCTION_FIXTURE`

### Demonstrated observation

After repairing the synthetic Experience persistence boundary, the focused
E19/T15 acceptance advanced farther through `AIPlatformService.ask_repository`
but stopped before provider invocation.

`ConversationContextEngine.build()` attempted normal organism-backed recovery
for `synthetic-e19-session`.

That recovery correctly failed because the test intentionally creates no
persistent session.

### Root cause

The synthetic service fixture still modeled only part of the established
pre-provider boundary.

The test intended to validate provider-failure behavior without creating
persistence, but it did not replace Conversation Context reconstruction even
though that reconstruction legitimately requires a persistent session.

### Recovery rule

For this synthetic acceptance only, replace the complete persistence-dependent
pre-provider boundary:

- Experience binding;
- raw-source persistence;
- Conversation Context reconstruction.

Do not weaken production recovery semantics.

Do not teach the organism that an unknown synthetic session is a real
persistent session.

Evidence, not Canon.

## FUSION-02 — E19/T15 recovery audit gate assumed fixture formatting

### Classification

`E19-ERR-004 — RECOVERY_AUDIT_GATE_FORMAT_ASSUMPTION`

### Demonstrated observation

The recovery batch stopped before mutation because its audit gate required
specific fixture text that was not guaranteed by the actual evolving worktree.

The preceding pytest traceback had already demonstrated the relevant semantic
fact: the synthetic session was intentionally non-persistent, while the final
assertion called `journey_reference()` on that unknown persistent identity.

### Root cause

The recovery gate tested an unnecessary representation detail instead of the
demonstrated semantic failure.

### Recovery rule

Recovery gates must validate only facts required by the demonstrated failure.
They must not require incidental formatting or an assumed intermediate fixture
representation.

Production was not modified by this failed recovery gate.

Evidence, not Canon.

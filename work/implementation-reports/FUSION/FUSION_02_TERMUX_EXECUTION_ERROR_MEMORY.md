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

## E20-ERR-001 — LEGACY_RETIREMENT_COMPATIBILITY_BOUNDARY_REGRESSION

Classification:
RECOVERED IMPLEMENTATION-BOUNDARY ERROR

Observed during:
FUSION-02 / E20 / T16 — Legacy Default Context Retirement

Failure:
The first T16 implementation removed the historical implicit
`context_builder.build()` fallback from `AIRequestPipeline.run()`.

Demonstrated regressions:
- T11 shadow pipeline could no longer execute its historical legacy provider path;
- T1 characterization baseline could no longer transport the built repository profile;
- T1 production characterization contract no longer found
  `self.context_builder.build()` in the pipeline.

Root cause:
"Legacy Default Context Retirement" was interpreted as physical removal of the
legacy pipeline compatibility physiology.

That interpretation exceeded the demonstrated architectural boundary.

Correct semantic boundary:
- AIPlatformService real request physiology is cognitive;
- AIPlatformService supplies `provider_cognitive_context`;
- the historical pipeline fallback remains available for compatibility,
  characterization, shadow observation, and direct legacy callers;
- legacy existence does not mean legacy is the organism's implicit real service physiology.

Recovery rule:
Never delete a historical compatibility physiology merely because it has been
retired from the organism's primary/default service path.

Acceptance required:
- restore T1;
- restore T11;
- preserve E16/E17/E18/E19 cognitive service cutover;
- prove real service requests do not depend on implicit legacy context;
- full FUSION regression must pass before E20 certification.

## E20-ERR-002 — EXACT_BOUNDARY_REQUIRED_UNCHANGED_COMPATIBILITY_FILE

Classification:
RECOVERED COMMIT-GATE ERROR

Observed during:
FUSION-02 / E20 / T16 final certification

Demonstrated observation:
The final exact-mutation-boundary gate required
`lib/python/ai_platform/pipeline.py` to appear in the staged diff.

The recovered T16 implementation had already restored that file exactly to
its conserved pre-E20 compatibility state. Therefore the file was correctly
absent from the staged diff.

Root cause:
The gate confused two different sets:

- files allowed to be modified;
- files required to be modified.

A compatibility file inspected and conserved by a batch does not need to
appear in the commit when its final content is identical to the conserved
authority.

Recovery rule:
Exact mutation boundaries must reject unexpected mutations, but must require
only files that actually contain the demonstrated implementation,
certification, Error Memory, tree, test, or report delta.

No production repair is required for this error.

## FUSION-02 — Natural-language repository discovery gap

### Classification

`FUSION02_NATURAL_LANGUAGE_REPOSITORY_DISCOVERY_GAP`

### Demonstrated observation

After FUSION-02 closure, the deployed AI Partner reported that it could not
inspect the Railway repository filesystem.

Direct source audit demonstrated that repository filesystem access already
existed:

- AIPlatformService already owned EvidenceEngine(repository_root);
- EvidenceEngine already traversed repository_root;
- bounded repository reads already used real local Path.read_text.

The demonstrated failure was therefore not absence of repository access.

The actual defect was that EvidenceEngine.find() treated the complete human
question as one literal filename substring. Natural-language questions could
therefore fail to discover repository files that were physically present and
readable.

### Recovery rule

Repository access diagnostics must distinguish:

1. physical repository filesystem access;
2. discovery/navigation capability;
3. bounded file read capability;
4. provider/network capability.

Failure of natural-language discovery must not be reported as absence of the
repository filesystem when local repository access is demonstrably present.

This record is Evidence, not Canon.

## FUSION-02 — Railway repository root unavailable to AI Partner

### Classification

`RUNTIME_REPOSITORY_ROOT_DISCOVERY_FAILURE`

### Demonstrated observation

After commit `c6bb238e38f1a7921bfb960cb46429619a297267`,
the deployed AI Partner still reported:

- `RUNTIME_REPOSITORY_ROOT: UNKNOWN`;
- FUSION_02 evolution tree not found;
- AI Platform service.py not found;
- repository search as last working stage;
- bounded read as first failed stage.

The authoritative checkout demonstrably contains those files.

### Recovery rule

Do not mutate natural-language EvidenceEngine discovery again.

First identify the actual deployed filesystem root and the exact
bootstrap path by which AIPlatformService receives repository_root.

The repository root must be derived from demonstrated runtime anatomy,
not assumed from process current-working-directory semantics.

This record is Evidence, not Canon.

## FUSION-02 — Session persistence coupled to deployment filesystem

### Classification

`DEPLOYMENT_COUPLED_SESSION_STORAGE`

### Demonstrated observation

AISessionEngine historically derived its session directory from
`repository_root/.ai/ai_sessions`.

On an ephemeral deployment filesystem this couples conversation state to
one deployment checkout.

A redeploy may therefore replace the filesystem containing:

- session identity;
- conversation history;
- raw sources;
- Experience identity;
- Journey reference;
- interruption/recovery state.

### Recovery

Repository identity and durable runtime state now have separate roots.

`AI_TOOLKIT_STATE_ROOT` may identify durable mounted storage.

When that variable is absent, historical repository-local behavior remains
available for local development and compatibility.

The implementation acceptance demonstrates recovery of the same Session
after changing repository/deployment root while retaining the same durable
state root.

This record is Evidence, not Canon.

## FUSION-02-ERR-AI-PARTNER-REATTACH-001 — INVENTED_DASHBOARD_SERVICE_CLASS

- Status: RECOVERED
- Observed: 2026-08-21T00:07:44.290920+00:00
- Failure stage: test collection
- Demonstrated failure:
  ImportError: cannot import name DashboardService from python.dashboard.service
- Root cause:
  the acceptance fixture assumed a DashboardService class that is not
  part of the authoritative dashboard anatomy.
- Recovery authority:
  inspect and use the real AI Partner request boundary already present
  in the dashboard/runtime implementation.
- Conservation:
  no reset; no production rollback; durable AISessionEngine physiology
  remains authoritative.
FUSION-02-ERR — SESSION_REATTACHMENT_TEST_ASSUMED_NONEXISTENT_RUNTIME_PATH
STATUS: RECOVERED
CAUSE: acceptance test assumed lib/python/runtime/server.py without repository evidence.
OBSERVED_REAL_HTTP_ORGAN: lib/python/runtime/interfaces/http_server.py
RECOVERY: production remains untouched; test now discovers and binds to the demonstrated HTTP runtime anatomy.
AUTHORITY: Human Authority conserved.
RECORDED_AT: 2026-08-22T17:33:24.479669+00:00
FUSION-02-ERR — SESSION_REATTACHMENT_REPORT_TRAILING_WHITESPACE_COMMIT_GATE
STATUS: RECOVERED
CAUSE: git diff --cached --check detected trailing whitespace in the generated anatomy report at lines 42 and 56.
RECOVERY: only demonstrated trailing whitespace was normalized; production physiology was unchanged.
CONSERVATION: prior staged reattachment implementation preserved.
RECORDED_AT: 2026-08-22T17:38:02.025265+00:00

FUSION-02 — Historical orphan continuity acceptance recovery

Failure classification:
ACCEPTANCE_TEST_BOUNDARY_ERROR

Observed failure:
test_bridge_does_not_insert_continuity_into_repository

Root cause:
The test inspected an arbitrary 300-character window beginning at
historical_continuity(session).

That textual window crossed from the historical-orphan branch into the
separate new-Experience branch and therefore observed the legitimate
self.experiences.add(experience) call used for newly created Experiences.

Production defect:
NO

Production mutation required for recovery:
NO

Correction:
Constrain the assertion to the exact historical-orphan branch boundary.

Conservation:
- historical continuity implementation preserved
- canonical Experience model preserved
- new Experience creation preserved
- repository persistence preserved
- no reset
- no restore
- no stash

FUSION-02 — Real browser continuation second recovery boundary

Observed through real Railway browser execution:

Browser
-> AIPlatformService.ask_repository
-> ConversationContext.build
-> EpistemicOrganism.conversation_session
-> PersistentExperienceRepository.get
-> ExperienceNotFoundError

Classification:
SECOND_UNINTEGRATED_EXPERIENCE_RECOVERY_BOUNDARY

The earlier ConversationExperienceBridge recovery was successful enough
for execution to advance into context reconstruction.

EpistemicOrganism.conversation_session still assumed that every session
Experience reference must resolve to a physically persisted canonical
Experience.

For historical sessions created before durable Experience storage, this
assumption is false.

Required conservation:
- repository lookup remains first authority
- only ExperienceNotFoundError may enter historical continuity
- canonical persisted Experience remains authoritative when present
- historical continuity must not be inserted into Experience repository
- original historical Experience identity must remain unchanged
- exact historical created_at must not be fabricated
- unrelated repository failures must propagate

## FUSION-02 — Interrupted Human Turn Recovery / PYTHONPATH recovery

Previous targeted acceptance failed during pytest collection with:

    ModuleNotFoundError: No module named 'python'

Classification:

    EXECUTION ENVIRONMENT ERROR

The implementation was preserved. The Termux command had omitted the
repository `lib` directory from PYTHONPATH.

Recovery uses:

    PYTHONPATH=<repository-root>/lib

No production rollback was performed.

## Browser continuation — HTTP boundary assumption failure

Classification: ACCEPTANCE / IMPLEMENTATION SCRIPT ANATOMY ERROR

Observed failure:

`FAIL: HTTP session_id forwarding boundary not found.`

Cause:

The implementation script assumed that the HTTP boundary forwarded
`session_id` directly from `payload.get(...)` inside the
`ask_repository(...)` call.

The real deployed/source anatomy is:

- parse `question`
- parse `session_id`
- parse `provider_id`
- parse `model`
- parse `prompt_name`
- validate question/prompt
- call `ask_repository(...)` with `session_id=session_id`

Therefore the failed script searched for a source pattern that does
not exist.

Conservation:

- the already implemented service continuation contract is preserved;
- no reset, restore, or stash is authorized;
- the HTTP integration must follow the demonstrated source anatomy.

## Browser continuation — Python literal corruption

Classification: IMPLEMENTATION SCRIPT DEFECT

The failed implementation inserted JavaScript immediately after a
Python string literal without creating a separate quoted Python
literal. This produced:

    'session.addEventListener(...);'continueButton...

and therefore an unterminated Python string.

Canonical correction:

Dashboard JavaScript in `lib/python/dashboard/service.py` is emitted
through adjacent Python string literals. Any new JavaScript fragment
must itself be represented by valid adjacent Python string literals.

The recovery must preserve already-valid local service and HTTP
continuation work and replace only the malformed dashboard mutation.

## FUSION-02 browser continuation — invalid temporary path

Classification: IMPLEMENTATION SCRIPT EXECUTION ERROR

A previous recovery script attempted to write a Git-authoritative
dashboard copy under `/tmp`. In the actual Termux execution
environment that path was not writable for this operation and the
script stopped before the dashboard mutation.

Correction:
- repository-local scratch storage only;
- no `/tmp`;
- no reset;
- no restore;
- no stash;
- Git-authoritative dashboard reconstruction remains isolated from
  already-valid local service and HTTP work.
## FUSION-02 — semantic validator must not require diagnostic prose

Classification: VALIDATOR DEFECT

Demonstrated failure:

A materialized implementation successfully patched the service and HTTP
continuation contracts and passed Python syntax validation. A later validator
then failed because it required the literal diagnostic text
`session has no recoverable interrupted human turn`.

That literal message was not a demonstrated production contract.

Conservation rule:

- Never validate semantic behavior by requiring arbitrary diagnostic prose.
- Never infer implementation failure solely from absence of an error-message
  string.
- After a successful materialization and syntax check, preserve the worktree.
- Validate Python structure through AST/signatures and behavior through tests.
- Do not reapply an already successful mutation merely because a later
  validator was defective.

This is demonstrated execution-error Evidence, not Canon.
## FUSION-02 — continuation raw-source construction ordering defect

Classification: PRODUCTION ORDERING DEFECT

Observed browser failure:

`raw conversation content must not be empty`

Root cause:

The explicit browser continuation correctly submitted an empty `question`
because the durable interrupted HUMAN source already existed. However,
`ask_repository()` attempted to construct a new HUMAN raw source from that
empty request before recovering the preserved interrupted HUMAN turn.

The raw-source invariant correctly rejected empty content.

Required physiology:

1. recover interrupted durable HUMAN turn first;
2. when `resume_interrupted_turn=True`, use its preserved content;
3. do not construct or append another HUMAN raw source;
4. when this is a normal new turn, construct and append exactly one HUMAN
   raw source normally.

Conservation:

The raw-source non-empty invariant remains unchanged.
The durable HUMAN turn remains authoritative raw conversation history.
No duplicate HUMAN source may be created during continuation.

This is demonstrated execution-error Evidence, not Canon.
## FUSION-02 — stale textual resume-contract acceptance

Classification: TEST CONTRACT STALENESS

Observed failure:

The corrected production implementation passed compilation and the new
raw-source-order acceptance, but an older browser-continuation test required
the literal source substring:

`resume_interrupted_turn and interrupted_turn is None`

That textual shape ceased to exist after the continuation physiology was
correctly reorganized into an explicit `if resume_interrupted_turn:` branch
containing the `interrupted_turn is None` guard.

Correction:

Do not deform production code to satisfy obsolete textual assertions.
Acceptance must inspect the structural AST contract:

- explicit resume branch exists;
- missing interrupted turn is rejected inside that branch;
- preserved interrupted content is used;
- continuation creates no duplicate HUMAN raw source.

This is demonstrated execution-error Evidence, not Canon.

---

## Demonstrated execution precedent — missing repository Python import root

### Demonstrated observation

During FUSION-02 Productive Bounded Cognitive Journey validation,
pytest collection stopped before executing the targeted tests with:

`ModuleNotFoundError: No module named 'python'`

The affected tests imported production modules through:

`from python.ai_platform...`

The repository package anatomy places that package below:

`lib/python/`

The validation command had been invoked without making repository `lib`
available as a Python import root.

### Failure classification

**EXECUTION ENVIRONMENT / VALIDATION ORCHESTRATION ERROR.**

The failure occurred during pytest collection.

Therefore it did not demonstrate failure of:

- Productive Bounded Cognitive Journey behavior;
- JourneyState;
- cognitive step evaluation;
- cognitive loop guards;
- search/read physiology;
- provider finalization.

No cognitive test body had executed at the point of failure.

### Demonstrated cause

For this repository anatomy:

`lib/python/...`

combined with imports of:

`python.ai_platform...`

requires repository `lib` to be present on the Python import path when
the project is executed directly from the Termux repository checkout.

### Recovery rule

Before invoking repository Python tests from Termux, establish the
repository import root explicitly:

`export PYTHONPATH="$REPOSITORY_ROOT/lib${PYTHONPATH:+:$PYTHONPATH}"`

Then perform an import preflight before pytest:

`import python`

and import the exact production symbols required by the targeted test.

### Prevention rule

Future AI-Toolkit implementation Bash scripts that execute Python tests
from the demonstrated Termux checkout MUST:

1. determine the real Git repository root;
2. place `<repository-root>/lib` on `PYTHONPATH`;
3. verify importability before pytest;
4. distinguish import/collection failure from test failure;
5. never modify production imports merely to hide an execution-environment
   configuration error;
6. never declare PASS when pytest collected or executed zero tests.

### Conservation boundary

This precedent is demonstrated Error Memory Evidence.

It is not:

- Canon;
- Human Authority;
- permission for autonomous mutation;
- permission to alter Python package anatomy;
- permission to create a second environment/bootstrap system.

Its purpose is to prevent recurrence of an already demonstrated execution
failure.

---

## Demonstrated execution precedent — mixed repository Python import roots

### Observation

AI-Toolkit currently contains production/test imports from more than one
repository-relative Python namespace.

Demonstrated import probes established:

- `<repo>/lib` resolves `python.*`;
- `<repo>/lib/python` resolves top-level `epistemic.*`;
- the combined environment resolves both families.

The demonstrated combined Termux validation environment is therefore:

`PYTHONPATH="$PWD:$PWD/lib:$PWD/lib/python${PYTHONPATH:+:$PYTHONPATH}"`

### Prevention rule

Before a repository-wide pytest invocation, validation orchestration MUST
preflight every demonstrated package family required by that suite.

A targeted suite may use a narrower import environment only when its complete
import anatomy has been demonstrated.

Production package code MUST NOT be rewritten merely to compensate for an
incorrect test-runner import root.

---

## Demonstrated execution precedent — diagnostic script blocked by incidental diff hygiene

### Observation

A diagnostic-only FUSION-02 script successfully captured the required failure
anatomy but terminated with code 2 because `git diff --check` detected:

`new blank line at EOF`

in the Error Memory artifact modified by the preceding run.

### Classification

This was not a cognitive-runtime failure and not a failure of the diagnostic
evidence collection.

It was orchestration ordering/hygiene failure.

### Prevention rule

When a script intentionally modifies a Markdown evidence/report artifact:

1. normalize the artifact before `git diff --check`;
2. run semantic/behavioral validation before final hygiene validation;
3. do not allow an incidental whitespace defect to erase already captured
   diagnostic evidence;
4. still report and correct the whitespace defect before conservation;
5. never convert a real non-zero behavioral test result into PASS.

---

## Demonstrated execution precedent — patch notation leaked into generated source

### Observation

A FUSION-02 recovery Bash embedded Python source intended for `conftest.py`,
but the generated source retained leading `+` characters originating from
patch notation.

Python AST validation rejected the candidate before it was written.

### Classification

This was generator contamination in the orchestration Bash. It was not a CSL
failure, UEM failure, pytest failure, or Productive Bounded Cognitive Journey
regression.

### Prevention rule

1. Embedded generated source must be inspected for leaked diff prefixes.
2. Bash syntax validation alone is insufficient when Bash generates another
   programming language.
3. The exact generated candidate must be parsed before it is written.
4. Validation must precede mutation.


---

## Demonstrated execution precedent — recovery depended on an unverified download path

### Observation

A corrective command assumed that the recovery Bash existed in Android's
shared `Download` directory. The Human had executed the Bash directly by
copying it, so no downloaded script existed at that path.

The recovery stopped before any mutation.

### Classification

This was an orchestration input-location assumption.

### Prevention rule

1. A recovery command must not assume that a previously delivered chat script
   was saved as a local file.
2. File-dependent recovery must first have evidence that the file exists.
3. When the Human used direct copy-paste execution, the next recovery must also
   be self-contained and directly executable.

---

## Demonstrated execution precedent — executable diagnostic collected as pytest

### Observation

The root-level `test_csl_semantic.py` was an executable historical diagnostic
that ran compilation and UEM inspection during module import. Its filename
caused pytest to collect it automatically.

The diagnostic targeted `docs/canonical`, where no `.csl` source files
existed. Compilation therefore did not produce a UEM, after which the
diagnostic dereferenced `result.uem.statistics()`.

### Classification

This was a pytest collection-boundary failure combined with a stale
diagnostic input contract. It was not proof of a production CSL/UEM failure.

### Prevention rule

1. Executable diagnostics must not enter automated pytest collection only
   because their filename begins with `test_`.
2. Preserved historical diagnostics should be excluded at the collection
   boundary.
3. Production CSL/UEM semantics must not be weakened to satisfy stale
   diagnostics.
4. Diagnostics must prove compilation success and UEM presence before using
   UEM methods.

---

## Demonstrated execution precedent — focused tests discovered only by filename

### Observation

The CSL/UEM recovery validation searched for focused tests using only test
filenames containing `csl`, `uem`, or `compiler`.

No matching filenames were found, so the orchestration marked the focused
verification as failed even though:

- pytest collection succeeded;
- Productive Bounded Cognitive Journey passed 28 tests;
- the complete FUSION suite passed 317 tests;
- the repository-wide suite passed 808 tests;
- `git diff --check` passed.

### Classification

This was a false-negative test-discovery failure in the validation
orchestration. It was not a product failure and not a CSL/UEM regression.

### Prevention rule

1. Focused tests must be discovered using test contents and collected node
   identities, not filenames alone.
2. A missing filename convention must not be treated as a failed physiology.
3. A validation report must distinguish:
   - test execution failure;
   - no test discovered;
   - test discovery defect;
   - repository-wide regression success.
4. Repository-wide green results do not erase a discovery defect, but the
   discovery defect must not be misclassified as a production failure.

---

## Demonstrated execution precedent — unverified optional command dependency

### Observation

A FUSION-02 recovery Bash attempted to discover CSL/UEM-related tests using
`rg`, but ripgrep was not installed in the Human's Termux environment.

The command therefore returned no discovered tests and the validation stopped
before branch creation, commit, or push.

### Classification

This was an orchestration dependency-assumption failure.

It was not:

- a CSL failure;
- a UEM failure;
- a Productive Bounded Cognitive Journey regression;
- a FUSION regression;
- a repository-wide regression.

### Prevention rule

1. A Bash must not assume an optional Termux package exists.
2. Required commands must be preflighted before their first use.
3. When the same operation can be performed with repository-required Python,
   Python should be used instead of introducing an optional dependency.
4. Absence of a discovery utility must not be reported as absence of tests.
5. A failed discovery mechanism must be distinguished from a failed test.

---

## Demonstrated execution precedent — sequential rewrite invalidated a later match

### Observation

A test-recovery generator performed multiple in-memory string replacements.

The first replacement changed the literal
`SECOND-MUST-NOT-BE-READ` to `SECOND-SELECTED-SOURCE`.

A later replacement then searched for an assertion containing the original
literal. That anchor no longer existed in the already-modified in-memory text,
so the generator stopped before writing either test file.

The production service and coordinator mutations from preceding Bash stages
had already been written and remained syntactically valid.

### Classification

This was an ordered text-transformation dependency failure in the Bash
generator.

It was not a failure of the multi-source production physiology and not a test
execution failure.

### Prevention rule

1. Interdependent textual replacements must be applied from the same original
   source or as one atomic block replacement.
2. A replacement must not silently invalidate a later required anchor.
3. Every generated candidate must be fully validated before writing.
4. Recovery must certify which earlier mutations were written and which later
   mutations were not.
5. Already-valid production mutations must not be discarded merely because a
   later test generator failed.

## Demonstrated execution precedent — simulated acceptance was treated as organism physiology

### Observed error

A service acceptance replaced settings, sessions, Persistent Experience,
context reconstruction, cognitive initialization, search navigation and
the provider pipeline through runtime substitution.

A provider suite called itself real while replacing HTTP transport,
generating responses and using a credential explicitly identified as
not real.

### Classification

SIMULATED-EVIDENCE CONTAMINATION

### Consequence

The affected green results cannot authorize organism physiology. They
prove only the substituted test environment.

### Permanent rule

AI-Toolkit acceptance evidence must traverse the production organs being
claimed. Runtime substitution, generated provider responses, fabricated
retrievals, fabricated Journey state and source-token assertions cannot
certify physiology.

### Recovery

Productive Multi-Source Journey now executes the real Evidence Engine
against the checked-out repository, reads actual selected files,
advances the real Journey and materializes the real Working Context
before the provider boundary.

Remaining inherited contamination blocks merge authority.

## Demonstrated execution precedent — real search was invoked from a non-research Information Need

### Observed failure

The substitution-free Productive Journey acceptance called the real
cognitive coordinator with the question `fusion 02 productive bounded
cognitive journey`.

The real Need Evaluator correctly classified that wording as not
requiring repository research because it contained none of the
established repository-navigation signals. The resulting navigation
plan had `required=False`, so real search correctly returned no
retrieval.

### Classification

`INFORMATION-NEED ACTIVATION CONTRACT MISMATCH`

### Permanent rule

An acceptance that exercises real repository navigation must formulate
a Human question that explicitly requests repository, file, source,
implementation, test, audit, evidence, branch, commit, code, trace,
dependency, architecture, or another recognized research capability.

A missing retrieval must first be examined through the Information Need
and Navigation Plan. It must never be repaired by injecting fabricated
search results or by bypassing the Need Evaluator.

### Recovery

The acceptance now asks to inspect the repository while preserving the
specific Productive Bounded Cognitive Journey search terms. The real
Need Evaluator must activate research and the real Evidence Engine must
discover the repository sources.

## Demonstrated execution precedent — broad real-source query crossed an unreadable candidate

### Observed failure

The real Evidence Engine activated correctly and returned multiple
repository paths. During bounded traversal, at least one existing
candidate was classified `UNKNOWN` by the real read organ rather than
`RETRIEVED`.

The acceptance incorrectly assumed that every candidate selected by a
broad project-history query must be readable UTF-8 production evidence.

### Classification

`REAL-SOURCE ACCEPTANCE SELECTION INSTABILITY`

### Permanent rule

A physiological acceptance for a specific organ must query stable
production identities relevant to that organ. It must not use a broad
historical phrase whose ranking can include reports, execution evidence
or other changing worktree material.

`UNKNOWN` remains valid and must never be rewritten into `RETRIEVED`.

### Recovery

The Productive Journey acceptance now queries the real cognitive
coordination and service organs. Their repository files are stable,
versioned production sources and are read through the same Evidence
Engine and bounded read physiology used by the application.

## Demonstrated execution precedent — semantic engine identity violated repository-relative read contract

### Observed failure

The real Productive Journey search returned existing sources, but at
least one bounded read produced `UNKNOWN`. The source still appeared to
exist when inspected through `root / source_path`.

### Demonstrated anatomy

The Evidence Engine combines ranked filesystem results with identities
returned by the Semantic Engine. Ranked filesystem results are
repository-relative. Semantic identities could remain absolute.

The combined retrieval nevertheless declared
`source_identity_kind=repository-relative-path`.

The bounded read organ correctly rejects absolute paths, so an existing
absolute semantic source became `UNKNOWN`. In Python, joining a root to
an absolute path preserves the absolute operand, explaining why the
acceptance simultaneously observed that the source existed.

### Classification

`CROSS-ORGAN SOURCE-IDENTITY CONTRACT VIOLATION`

This supersedes the earlier incomplete classification that attributed
the failure only to broad source selection.

### Permanent rule

Every source emitted under the identity class
`repository-relative-path` must be normalized relative to the certified
repository root before it enters retrieval, Journey, provenance or
Working Context.

Absolute paths, parent traversal and paths outside the repository must
be rejected before publication by the Evidence Engine. The read organ
must remain fail-closed and must continue returning `UNKNOWN` for
invalid identities.

### Recovery

Semantic identities are now resolved against the Evidence Engine root,
validated as descendants of that root and serialized as POSIX
repository-relative paths. Outside-root identities are excluded.

## Demonstrated execution precedent — discoverable path was not certified as readable epistemic matter

### Observed failure

After semantic identities were normalized to repository-relative paths,
a real candidate still produced `UNKNOWN` even though the corresponding
path existed as a file.

### Demonstrated boundary

File existence and path validity do not prove that a candidate contains
readable epistemic matter. A file may be empty or may not be decodable
under the repository textual contract.

The Evidence Engine previously ranked and published paths before
certifying non-empty UTF-8 readability. The bounded read organ remained
fail-closed and correctly returned `UNKNOWN`.

### Classification

`DISCOVERABILITY-TO-READABILITY CONTRACT GAP`

### Permanent rule

A source advertised by the Evidence Engine as textual repository
evidence must be:

- a real file;
- inside the certified repository;
- non-empty;
- UTF-8 readable;
- represented by a repository-relative identity.

Candidates failing that contract must not enter textual retrieval.
The read organ must remain fail-closed as an independent protection.

### Recovery

Filesystem-ranked and semantic candidates are now certified through one
real readable-text boundary before publication. No content, status or
retrieval result is fabricated.

## Demonstrated execution precedent — repeated staging targeted a deletion already removed from the index

### Observed failure

All physiological and regression verifications passed:

- focused real acceptance: 2 passed;
- complete FUSION regression: 312 passed;
- repository-wide regression: 803 passed;
- CSL Level-3: all eight checks passed.

Conservation then stopped because a previous execution had already
performed `git rm` for the retired simulated acceptance. A later
recovery attempted `git add -u --` against the same now-absent path and
Git rejected the pathspec.

### Classification

`NON-IDEMPOTENT DELETION STAGING`

### Permanent rule

When an earlier interrupted execution may already have staged a
deletion, recovery must inspect the index rather than restage the absent
path. The exact staged file set is authoritative.

A verified implementation must not rerun expensive physiological
regressions solely because a later staging command was non-idempotent,
provided HEAD and all verified source artifacts remain unchanged.

### Recovery

The deletion already present in the index is preserved. Existing files
are staged explicitly, the complete staged set is compared against the
authorized set, and only then may conservation continue.

## Demonstrated execution precedent — generated Markdown contained trailing whitespace

### Observed failure

All physiological and regression verification layers were green, but
`git diff --cached --check` stopped conservation because the generated
recovery report contained trailing whitespace on a blank line.

### Classification

`GENERATED-ARTIFACT WHITESPACE HYGIENE FAILURE`

### Permanent rule

Every generated Markdown artifact and every modified Error Memory file
must be normalized line by line before staging. Each line must have
trailing whitespace removed, and the file must end with exactly one
newline.

`git diff --check` and `git diff --cached --check` must both pass before
commit.

### Recovery

The recovery report and Error Memory were normalized without changing
the verified production implementation or physiological test result.

## Demonstrated AI Partner precedent — fabricated file-byte access retracted after verification

### Observed failure

AI Partner claimed direct access to a repository test file and supplied
invented measurements, functions, source identifiers and a hash that
contradicted the authoritative GitHub blob.

### Classification

`FABRICATED FILE-BYTE ACCESS / FALSE COGNITIVE TRACE`

### Detection

Independent inspection of the exact GitHub commit demonstrated a
different blob anatomy, line count, function inventory and content.

### Recovery

AI Partner retracted the unsupported claims and acknowledged that the
content was inferred or generated without file access.

### Permanent rule

An AI contribution cannot classify file access as demonstrated without
verifiable repository identity, path identity and content evidence.
Generated analysis must never be represented as retrieved evidence.

AI Partner remains supervised until exact branch access, exact commit
access, real file retrieval, persistence and restart rediscovery are
repeatedly demonstrated.

## Demonstrated execution precedent — context reconstruction was certified from substituted organs

### Observed contamination

The context reconstruction acceptance replaced:

- `EpistemicOrganismAccess.conversation_session`;
- `EpistemicOrganismAccess.state`;
- `AIContextBuilder.build`.

It then treated generated session, Experience, organism and repository
state as evidence for real context reconstruction.

### Classification

`SUBSTITUTED CONTEXT-RECONSTRUCTION PHYSIOLOGY`

### Permanent rule

Context reconstruction acceptance must begin with a session persisted by
the real `AISessionEngine`, bound to an Experience through the real
`ConversationExperienceBridge`, populated with real raw-source records
and recovered through the real `EpistemicOrganismAccess`.

Boundedness must be demonstrated by real chronological persistence and
real truncation. Generated dictionaries cannot authorize Persistent
Experience, Provenance, organism state or Human Authority.

### Recovery

The acceptance now persists three chronological raw conversation
sources through production organs, reconstructs the latest two, verifies
real truncation, Provenance, Experience identity, AI Partner identity,
epistemic boundaries and Human Authority.

## FUSION-02 — isolated durable-session proof was insufficient

The inherited durable-session acceptance demonstrated AISessionEngine
directly but did not demonstrate that AIPlatformService, Persistent
Experience and Conversation Context shared the same durable state root.

Two tests also mutated process environment through monkeypatch. That
could characterize environment resolution, but it could not serve as
mock-free physiological acceptance for restart reconstruction.

Recovery rule:

- use an explicit state_root production contract;
- propagate it through the existing Service, Session, Experience,
  EpistemicOrganismAccess and Conversation Context organs;
- instantiate two real services with different deployment roots;
- require the second service to recover the session, Experience,
  Journey reference, raw source and bounded context from the same
  durable body;
- preserve repository identity independently from storage identity;
- do not infer takeover or persistence from an isolated session-engine
  test.

## FUSION-02 — self-referential hygiene detector false positive

The durable-root implementation passed syntax preparation, but the Bash
hygiene gate stopped before testing because the acceptance file contained
a test that listed prohibited substitution identifiers as literal text.

The external grep correctly found those literal identifiers, but they
described the prohibition rather than an imported or executed
substitution framework. This was an orchestration false positive, not a
production or physiological failure.

Recovery rule:

- do not place prohibited-token inventories inside the physiological
  acceptance file being scanned;
- keep the acceptance focused on observable real-organ behavior;
- perform substitution hygiene externally from Bash;
- inspect imports, fixtures and executable calls separately from
  explanatory strings;
- never weaken the prohibition merely to make the detector green.

## FUSION-02 — CSL Level-3 executable path must be repository-certified

After focused, FUSION and repository-wide pytest acceptance passed, the
conservation Bash invoked a fabricated root-level path named
`test_csl_level3.py`.

That file does not exist. The repository-owned Level-3 executable is:

`tests/test_csl_level3_compiler.sh`

The resulting return code was an orchestration failure, not a CSL,
compiler, UEM or production failure.

Recovery rule:

- never reconstruct a test-executable path from memory;
- certify the exact repository path before execution;
- distinguish a missing runner from a red physiological result;
- preserve already completed green suites when no source mutation
  occurred after their execution;
- run the repository-owned shell acceptance through Bash.

## FUSION-02 — report existence must follow actual control flow

A recovery Bash attempted to update the implementation report before
that report had ever been generated. Earlier runs had stopped before
their report-generation stage, so the file was correctly absent.

This was a control-flow and precondition error.

Recovery rule:

- never assume a downstream artifact exists after an earlier stop;
- certify file existence before reading;
- create a missing report from preserved demonstrated evidence;
- only update an artifact after its materialization is confirmed.

## FUSION-02 — failure/restart authority requires a real failure

The inherited E19/T15 acceptance replaced `pipeline.run` with a local
exception function. A separate test replaced session creation, session
reads, Experience binding, raw-source persistence and context
reconstruction with synthetic dictionaries and lambdas.

Those tests could exercise control-flow branches, but they could not
demonstrate organism physiology, durable interruption or restart
authority.

Recovery rule:

- trigger failure through a real production boundary;
- prefer deterministic configuration failure when external network
  execution is not the subject under acceptance;
- persist the Human raw source before the failure;
- persist an INTERRUPTED Journey without fabricating an AI answer;
- instantiate a second real Service against the same durable root;
- recover the exact unmatched Human turn and bounded context;
- ensure resume does not duplicate the Human raw source;
- preserve Human Authority and prohibit automatic epistemic promotion.

## FUSION-02 — mock removal exposed StaticProviderAdapter contract drift

The first mock-free E19/T15 run reached the real provider pipeline and
demonstrated a production contract mismatch:

`AIRequestPipeline.run()` passes `provider_settings` to every adapter,
while `StaticProviderAdapter.complete()` did not accept that argument.

The blank provider request was resolved to a registered static adapter,
so it did not produce the anticipated missing-adapter failure. The real
pipeline instead raised TypeError at the incompatible adapter contract.

Recovery rule:

- treat unexpected failures reached through real organs as production
  evidence rather than rewriting assertions around them;
- keep every registered adapter compatible with the common pipeline
  invocation contract;
- use an explicit unregistered provider identity when testing the
  missing-provider failure boundary;
- demonstrate both the successful registered-provider path and the
  interrupted unregistered-provider path;
- never replace the provider or pipeline to manufacture either result.

## FUSION-02 — generated source must have one terminal newline

The provider-contract recovery stopped before test execution because the
generated acceptance ended with an additional blank line. The source
was syntactically valid, but `git diff --check` correctly rejected the
new blank line at EOF.

Recovery rule:

- normalize generated source with `rstrip()` followed by exactly one
  newline;
- run diff hygiene before expensive regression suites;
- classify whitespace rejection as orchestration hygiene, not production
  physiology failure.

## FUSION-02 — Owner Chat requires real HTTP physiology

The inherited Owner Chat acceptance mutated the process environment
through monkeypatch and inspected private HTML rendering helpers
directly. It demonstrated fragments of authentication and markup, but
not the complete owner-operated HTTP physiology.

Recovery rule:

- configure OwnerAccessBoundary explicitly through its production token
  argument;
- start the existing RuntimeHttpServer on a real loopback socket;
- exercise real HTTP redirects, Bearer authentication, chat POST and
  session GET;
- route the chat through the real Dashboard Service, AIPlatformService,
  Pipeline and registered provider adapter;
- verify durable Human and AI raw sources;
- ensure invalid authentication fails closed;
- ensure secrets do not enter HTML, JavaScript or API responses;
- preserve Human Authority and all epistemic distinctions.

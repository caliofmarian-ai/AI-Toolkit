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

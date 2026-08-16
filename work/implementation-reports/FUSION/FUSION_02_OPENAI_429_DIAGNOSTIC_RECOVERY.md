# FUSION-02 — OpenAI HTTP 429 Diagnostic Recovery

## Human Authority

Execution continues from:

`c74fe26692d8cadfceaa84593f096baca55f1525`

on `main`.

## Demonstrated live condition

The deployed real-provider path reached OpenAI and received HTTP 429.

The previous adapter retained only the HTTP status, preventing exact
provider-side classification.

## Bounded production evolution

OpenAIProviderAdapter remains fail-closed.

For an OpenAI HTTP failure it may now retain only bounded structured
diagnostic information:

- HTTP status;
- provider error type;
- provider error code;
- OpenAI request ID when available.

The diagnostic boundary does not intentionally expose:

- OPENAI_API_KEY;
- Authorization credentials;
- AI_TOOLKIT_OWNER_TOKEN;
- Human conversation content;
- reconstructed organism context;
- arbitrary provider error prose.

No StaticProviderAdapter fallback was introduced.

## Demonstrated test-infrastructure recoveries

### PYTEST_IMPORT_PATH_NOT_ESTABLISHED

The initial resumed pytest invocation lacked the repository `lib/`
import root.

This was test-runner infrastructure, not a production defect.

Recovery: execute pytest with the repository `lib/` directory on
`PYTHONPATH`.

### STALE_PROVIDER_TEST_HELPER_REFERENCE

Two new acceptance tests referenced `_openai_adapter()`, while the
existing provider test module defines and uses `_adapter()`.

This produced NameError before exercising production.

Recovery: the two new tests were corrected to reuse the established
`_adapter()` helper.

Production was not changed to satisfy this test-infrastructure defect.

## Acceptance

The complete provider acceptance suite and bounded FUSION-02 regressions
were required to pass before conservation.

## Next live threshold

Railway deploys the resulting `main` commit.

Human Authority sends one real message through Owner AI Chat.

If OpenAI still returns HTTP 429, the sanitized diagnostic must be used
to classify the actual provider-side cause.

HTTP 429 alone is not sufficient evidence for a specific diagnosis.

FUSION-02 LIVE ACCEPTANCE remains incomplete until a real OpenAI response
and durable conversational continuity are demonstrated.

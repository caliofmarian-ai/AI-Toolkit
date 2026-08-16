# FUSION-02 — Railway Context Anatomy Diagnostic

## Purpose

Measure the real reconstructed FUSION-02 context inside Railway immediately
before AIRequestPipeline execution.

## Proven production boundary

The AI platform service builds:

`reconstructed_context = self.conversation_context.build(...)`

and then passes that exact object through:

`context_override=reconstructed_context`

to `self.pipeline.run(...)`.

The previous diagnostic assumed a keyword named `context` and therefore
failed closed before mutation.

## Existing live evidence

The Owner AI Chat request containing `hi` produced:

- human message characters: 2;
- reconstructed context characters: 295122;
- serialized request bytes: 328917;
- estimated tokens at four characters/bytes: 82230;
- conservative estimate: 109639;
- OpenAI HTTP 429;
- provider type: `tokens`;
- provider code: `rate_limit_exceeded`.

## Existing local anatomy

The local structural inspection showed:

- `repository_profile`: 272210 bytes / 82.73%;
- `runtime_status`: 42127 bytes / 12.80%.

These local measurements strongly identify likely dominant structures but do
not substitute for the real Railway session.

## Runtime diagnostic

The runtime now measures the exact `reconstructed_context` passed through
`context_override`.

For each top-level branch the diagnostic records only:

- branch name;
- serialized bytes;
- percentage;
- structural kind;
- child count.

It also records:

- total serialized bytes;
- approximate token count;
- top-level branch count.

## Privacy and security

The diagnostic does not intentionally log:

- Human message text;
- AI response text;
- reconstructed context values;
- repository values;
- complete provider payload;
- OpenAI credential;
- authorization headers.

## Behavioral boundary

No context reduction is implemented by this slice.

No model selection changes are implemented.

No StaticProviderAdapter fallback is introduced.

No Canon is modified.

## Railway acceptance

After deployment, send one short Owner AI Chat message:

`hi`

Then inspect Railway logs for:

`FUSION-02 reconstructed context anatomy:`

The resulting numerical anatomy is the evidence required before changing
FUSION-02 context physiology.

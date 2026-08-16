# FUSION-02 — OpenAI Token-Budget Diagnostic

## Authority

Starting Git commit:

`5a3d424022f3753ec99d139fabcd94341119e630`

## Purpose

Measure the size of the real serialized OpenAI request immediately before
provider transmission without logging RAW conversation content or credentials.

## Request anatomy

The diagnostic observes:

`reconstructed_context`
→ `payload`
→ `request_body`
→ `urllib.request.Request`
→ `urllib.request.urlopen`

The byte measurement therefore represents the serialized body actually passed
to the HTTP request object.

## Measurements

The runtime event named:

`OpenAI outbound request budget`

contains content-free measurements including:

- configured model;
- Human-message character count;
- reconstructed-context character count;
- serialized request byte count;
- estimated token-size measurements.

These token estimates are diagnostic approximations and are not authoritative
OpenAI billing-token counts.

## Privacy boundary

The diagnostic does not intentionally log:

- OPENAI_API_KEY;
- Authorization header;
- Human message text;
- reconstructed conversation text;
- complete provider payload.

## Recovery history

Two diagnostic-instrument defects were encountered and conserved in Error
Memory:

1. literal escaped newline characters were introduced into generated Python
   source;
2. the diagnostic referenced `logger` without defining a module logger.

The second defect caused eight provider tests to fail from one shared
`NameError`.

The recovery adds Python standard-library logging and a module logger without
changing provider semantics.

## Behavioral boundary

No Canon modification.

No context reduction.

No conversation truncation.

No StaticProviderAdapter fallback.

No Owner-security weakening.

No persistence replacement.

## Next live threshold

After Railway deploys the resulting commit:

1. Human Authority opens Owner AI Chat;
2. sends one short message;
3. Railway logs are inspected for:
   `OpenAI outbound request budget`;
4. the numerical measurements are used to determine the actual request size;
5. the OpenAI response is inspected independently.

FUSION-02 live acceptance remains incomplete until a real OpenAI response and
same-session conversation continuity are demonstrated.

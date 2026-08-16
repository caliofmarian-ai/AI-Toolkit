# FUSION-02 — Railway-Visible OpenAI Token Budget

**Generated:** 2026-08-16T19:21:18.355559+00:00

## Purpose

Expose the already-authorized, content-free OpenAI outbound request
measurements through the standard log message retained by Railway.

## Demonstrated production condition

Railway retained the event:

`OpenAI outbound request budget`

but the inspected Railway JSON did not expose the custom
`openai_request_budget` object supplied through Python `logging.extra`.

The immediately following real OpenAI request failed explicitly with:

- HTTP status: `429`
- provider type: `tokens`
- provider code: `rate_limit_exceeded`

This change does not infer the numerical cause before measurement.

## Implementation

The existing request-budget measurement remains authoritative.

The same bounded scalar measurements are now serialized into the
standard log message:

- model
- human message character count
- reconstructed context character count
- serialized request byte count
- estimated token count at four characters per token
- conservative estimated token count at three bytes per token

The structured `logging.extra` representation is retained as well.

## Confidentiality boundary

The diagnostic does not intentionally log:

- OpenAI API credentials
- Authorization headers
- human message content
- reconstructed context content
- complete provider request payload

## Semantic boundary

This change does **not**:

- reduce context
- truncate conversation history
- change the selected model
- change OpenAI credentials
- add fallback behavior
- modify Canon

## Live acceptance threshold

After Railway deploys the resulting commit, send exactly one short
Owner AI Chat message.

The Railway log must expose a line beginning:

`OpenAI outbound request budget:`

The numerical measurements from that line are required before deciding
whether FUSION-02 needs token-budget management or another correction.

## Error Memory

Updated with the demonstrated precedent that Python `logging.extra`
cannot be assumed to be operationally visible in Railway.

## Status

Implementation acceptance is test-gated by this batch.

Railway live acceptance remains unclaimed until the deployed runtime
produces the numerical diagnostic.

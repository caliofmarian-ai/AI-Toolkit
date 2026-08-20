# FUSION-02 — Durable Session State Root

## Human meaning

A conversation is part of the organism's continuing life and must not die
merely because a new software deployment replaces the application checkout.

The repository and the organism's durable state therefore have different
physical responsibilities.

## Repository root

The repository root continues to identify the deployed AI-Toolkit source and
repository anatomy.

## Durable state root

The Session engine now accepts a distinct durable state root.

Railway can provide it through:

`AI_TOOLKIT_STATE_ROOT`

The resulting session anatomy is:

`$AI_TOOLKIT_STATE_ROOT/.ai/ai_sessions`

## Conserved physiology

The same persisted Session can retain:

- Session identity;
- conversation history;
- raw sources;
- Experience identity;
- Journey reference;
- token usage and existing Session fields.

## Compatibility

Without `AI_TOOLKIT_STATE_ROOT`, local development retains the established
repository-local `.ai/ai_sessions` behavior.

## Acceptance

Automated acceptance changes the simulated deployment repository root while
keeping the durable state root constant.

The same Session is recovered with its conversation, Experience and Journey
identity intact.

## Railway requirement

Software support alone cannot make an ephemeral Railway filesystem durable.

Railway must mount persistent storage and `AI_TOOLKIT_STATE_ROOT` must point
to that mounted path.

Real redeploy acceptance must therefore be performed only after the volume
is mounted.

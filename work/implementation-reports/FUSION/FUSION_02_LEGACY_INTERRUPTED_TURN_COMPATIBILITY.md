# FUSION-02 — Legacy Interrupted Turn Compatibility

## Purpose

Repair interrupted-turn recovery for durable AI Partner sessions that
predate explicit Journey interruption metadata.

## Demonstrated production failure

The real Railway session:

- session: AI-SESSION-3BAD91C0B88C
- Experience: 3e264780-2ce0-491d-8903-41f0af66c6cb
- raw source count: 3
- final raw source actor: HUMAN
- final raw source sequence: 3
- Journey status: IN_PROGRESS
- restart_recoverable: absent

The final HUMAN raw source is durable and has no corresponding AI raw
source.

The previous detector rejected it because it required both:

- Journey status INTERRUPTED
- restart_recoverable=True

Those fields did not exist when the historical session was produced.

## Implemented physiology

Two recovery forms now exist.

### Modern explicit interruption

Recovery requires:

- final source HUMAN
- exact session ownership
- contiguous final sequence
- non-empty content
- Journey INTERRUPTED
- restart_recoverable=True

### Historical structural interruption

Recovery requires:

- final source HUMAN
- exact session ownership
- contiguous final sequence
- non-empty content
- Journey IN_PROGRESS
- restart_recoverable field absent

An explicit restart_recoverable=False remains authoritative and blocks
recovery.

## Epistemic boundary

Historical compatibility does not rewrite durable history.

It does not:

- edit the Railway session
- fabricate an INTERRUPTED Journey state
- fabricate a historical restart flag
- create Evidence
- create Knowledge
- create Canon
- add a raw source
- persist detector output

The detector remains read-only.

## Expected real continuation

Existing durable sequence:

1. HUMAN
2. AI
3. HUMAN — interrupted before corresponding AI completion

Expected continuation:

4. AI

The existing HUMAN #3 must not be duplicated.

## Validation

Targeted FUSION compatibility tests executed.

Full FUSION regression executed.

## Deployment position

No commit or push is performed by this implementation run.

The implementation must be reviewed from this report and terminal
result before certification and deployment.

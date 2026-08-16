# FUSION-02 — T1 Characterization Baseline

## Execution Identity

**Run:** RUN-01
**Phase V stage:** T1 — Characterization Baseline
**Generated:** 2026-08-16T20:46:04.120820+00:00
**Starting authority:** `25984053762c225bc93dba26a8a8108978f10a0c`

## Purpose

Characterize the current legacy cognitive physiology before
Permanent Orientation, Information Need, Epistemic Journey,
Working Context, or Context Budget Governance changes production
behavior.

T1 is characterization only.

## Demonstrated Legacy Physiology

The current implementation retains this default path:

Human request
→ AIPlatformService
→ AIRequestPipeline
→ AIContextBuilder.build()
→ RepositoryEngine.profile()
→ RepositoryProfileSerializer.to_dict(...)
→ repository_profile
→ provider adapter

The pipeline also already contains a `context_override` seam.

This is important because later stages can adapt the integration
boundary without requiring a second provider pipeline.

## Sanitized Local Measurement

| Measurement | Value |
|---|---:|
| Total serialized context | 350802 bytes |
| Estimated tokens at 4 bytes/token | 87701 |
| Estimated tokens at 3 bytes/token | 116934 |
| Repository profile | 291319 bytes |
| Repository profile share | 83.04% |
| Repository-profile engineering branch | 2 bytes |
| Engineering share of total | 0.0% |
| Top-level branch count | 14 |

### Structural contribution

| Branch | Serialized bytes | Approximate share |
|---|---:|---:|
| `repository_profile` | 291319 | 83.04% |
| `runtime_status` | 43930 | 12.52% |
| `workspace` | 9454 | 2.69% |
| `engineering_session` | 2422 | 0.69% |
| `context` | 1817 | 0.52% |
| `canonical_documents` | 741 | 0.21% |
| `repository_health` | 537 | 0.15% |
| `recent_reports` | 110 | 0.03% |
| `dependencies` | 106 | 0.03% |
| `technology_stack` | 56 | 0.02% |
| `current_epic` | 10 | 0.0% |
| `current_issue` | 10 | 0.0% |
| `current_branch` | 6 | 0.0% |
| `current_sprint` | 2 | 0.0% |

No raw Human message, raw repository content, raw context,
credential, Authorization header, or complete provider payload is
included in this report.

## Previously Demonstrated Railway Evidence

The already conserved FUSION-02 live evidence demonstrated
approximately:

- reconstructed context around 295 KB;
- engineering contribution around 98%;
- provider request estimates around 82K–110K tokens depending
  on estimator;
- OpenAI HTTP 429;
- provider type `tokens`;
- provider code `rate_limit_exceeded`.

Those measurements remain Evidence of the legacy physiology.
They are not future architectural constants.

## Characterization Acceptance

The focused T1 acceptance proves:

1. `AIContextBuilder.build()` materializes Repository Engine profile.
2. RepositoryProfileSerializer serializes that profile.
3. `repository_profile` enters the legacy context.
4. The default pipeline transports the built context to the adapter.
5. Existing `context_override` bypasses the builder.
6. A synthetic large repository profile dominates the resulting
   legacy context.
7. Characterization requires no OpenAI request.

Relevant available FUSION-02 regression files executed:
**5**

## Invariant Baseline

T1 establishes the pre-change state for:

### I-01
Knowledge Availability != Working Context

The desired distinction is not yet the default legacy physiology.

### I-08
Context Budget Does Not Delete Organism Knowledge

No organism knowledge is deleted by T1.

### I-10
Full Repository Profile Is Not Default Cognitive Payload

This invariant is intentionally NOT claimed as implemented yet.
T1 records the demonstrated legacy violation/risk that later stages
must replace.

## Mutation Boundary

Authorized:

- `tests/fusion/test_fusion_02_t1_characterization_baseline.py`
- this report
- Error Memory only if an execution/implementation error occurred

Production code modified: **NO**

CSL modified: **NO**

Canon modified: **NO**

Provider called: **NO**

Context reduced: **NO**

## T1 Acceptance Gate

T1 may be conserved only when:

- focused characterization tests pass;
- relevant available FUSION-02 regressions pass;
- production sources still parse;
- no production file is staged;
- staged mutation is allowlisted;
- `git diff --cached --check` passes;
- no obvious credential material exists;
- commit is pushed;
- local HEAD equals remote main.

## Conservation Point

T1 is a Phase-V conservation point.

Its purpose is to make later cognitive-physiology improvement
measurable against an explicit baseline rather than assumptions.

## Next Stage

After independent GitHub inspection:

**RUN-02 — T2 + T3**

- Provider Budget Introspection
- Permanent Orientation

T1 itself performs neither cutover.

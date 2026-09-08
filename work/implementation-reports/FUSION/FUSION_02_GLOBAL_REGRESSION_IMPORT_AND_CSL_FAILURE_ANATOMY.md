# FUSION-02 — Global Regression Import + CSL Failure Anatomy

## Classification

DIAGNOSIS ONLY.

No production source correction is authorized by this report.

## Repository

- Repository: `/storage/emulated/0/AI-Projects/AI-Toolkit`
- HEAD: `92086cc56b6a7f6a2c9b24092b07c9cfa65e7732`
- Remote: `https://github.com/caliofmarian-ai/AI-Toolkit.git`

## Conserved successful evidence

- Productive Bounded Cognitive Journey targeted acceptance: PASS
- FUSION regression: PASS

The newly observed failures therefore occur outside the already-green
focused FUSION-02 acceptance boundary.

## Observed global-regression failures

- `tests/epistemic/test_layered_memory.py`: RC=2
- `tests/epistemic/test_layered_memory_persistence.py`: RC=2
- `tests/epistemic/test_sedimented_memory.py`: RC=2
- `test_csl_semantic.py`: RC=2

## Current demonstrated distinction

Three failures concern import resolution for the top-level
`epistemic` package.

The CSL failure is a separate collection/import-time behavior:
`result.uem` is None when `statistics()` is accessed.

These must NOT be collapsed into one presumed root cause.

## Global FUSION Evolution Tree

```text
GLOBAL FUSION EVOLUTION
|
+-- Stage 1
|
+-- Stage 2 / FUSION-02  <-- ACTIVE
|   |
|   +-- Productive Bounded Cognitive Journey
|       |
|       +-- targeted acceptance: PASS
|       +-- FUSION regression: PASS
|       +-- global regression diagnosis: CURRENT
|
+-- Stage 3  Dashboard projection
+-- Stage 4  AI Partner project sessions
+-- Stage 5  Durable raw epistemic capture
+-- Stage 6
+-- Stage 7  Evolving project understanding
+-- Stage 8
+-- Stage 9  Living Project Image
+-- Stage 10 Epistemic genealogy/navigation
+-- Stage 11 Epic Thread
+-- Stage 12 AI Partner context reconstruction
```

## Cross-stage warning

The failing `epistemic` tests may belong to physiology shared with
later FUSION stages. Their package anatomy must therefore be recovered
before any import rewrite, relocation, or duplicate package is created.

## Evidence artifacts

- `.fusion-02-evidence/global-regression-anatomy/epistemic-anatomy.txt`
- `.fusion-02-evidence/global-regression-anatomy/failing-test-contracts.txt`
- `.fusion-02-evidence/global-regression-anatomy/test-runner-anatomy.txt`
- `.fusion-02-evidence/global-regression-anatomy/import-root-probes.txt`
- individual pytest reproduction logs under `.fusion-02-evidence/global-regression-anatomy/`

## Mutation conservation

- Production correction: NO
- Test correction: NO
- Package relocation: NO
- Duplicate package creation: NO
- Commit: NO
- Push: NO
- Railway: NO
- Reset: NO
- Restore: NO
- Stash: NO
- Force push: NO

## Required next decision

Use the demonstrated repository package/test-runner anatomy to classify
each failure as one of:

1. execution-environment/import-root error;
2. stale test contract;
3. actual production regression;
4. legacy executable script incorrectly collected as pytest;
5. another demonstrated repository-specific cause.

No correction should be selected before that classification.

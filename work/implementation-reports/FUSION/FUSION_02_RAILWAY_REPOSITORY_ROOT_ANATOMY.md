# FUSION-02 — Railway Repository Root Anatomy

## Classification

RUNTIME_REPOSITORY_ROOT_DISCOVERY_FAILURE

## Runtime acceptance evidence

The deployed AI Partner reported:

- `RUNTIME_REPOSITORY_ROOT: UNKNOWN`
- `FUSION_02_EVOLUTION_TREE.md: NOT_FOUND`
- `lib/python/ai_platform/service.py: NOT_FOUND`
- repository search was the last working stage;
- bounded read was the first failed stage.

## Git authority

Expected commit:

`c6bb238e38f1a7921bfb960cb46429619a297267`

The local authoritative checkout contains all three acceptance targets.

## Local physical anatomy

Repository root used for this audit:

`/storage/emulated/0/AI-Projects/AI-Toolkit`

- `work/fusion/FUSION_02_EVOLUTION_TREE.md`
  - absolute: `/storage/emulated/0/AI-Projects/AI-Toolkit/work/fusion/FUSION_02_EVOLUTION_TREE.md`
  - exists: `True`
- `lib/python/ai_platform/service.py`
  - absolute: `/storage/emulated/0/AI-Projects/AI-Toolkit/lib/python/ai_platform/service.py`
  - exists: `True`
- `work/implementation-reports/FUSION/FUSION_02_REPOSITORY_NATURAL_LANGUAGE_ACCESS.md`
  - absolute: `/storage/emulated/0/AI-Projects/AI-Toolkit/work/implementation-reports/FUSION/FUSION_02_REPOSITORY_NATURAL_LANGUAGE_ACCESS.md`
  - exists: `True`

## Diagnostic boundary

The demonstrated defect is no longer natural-language candidate
selection.

The files physically exist in the authoritative repository.

The failed Railway acceptance demonstrates that the deployed organism
does not possess a correctly resolved physical repository root at the
point where bounded repository reading occurs.

The next production mutation, if required, must therefore be derived
from the runtime bootstrap / repository-root construction boundary.

EvidenceEngine must not receive another speculative correction.

## Conservation

- FUSION-02 E0-E20 remain conserved.
- Human Authority remains conserved.
- Context Budget Governance remains conserved.
- Journey physiology remains conserved.
- no GitHub connector is required for local deployed-source reading.
- no production mutation was made by this diagnostic gate.

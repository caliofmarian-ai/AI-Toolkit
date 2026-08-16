# FUSION-02 — RUN-04 UEM × Knowledge Materialization Relationship Resolution

**Starting HEAD:** `336913e86234fec181bd4920345f330ecf321886`

**Mode:** Read-only architectural characterization + Error Memory conservation.

## Recovery reason

The previous RUN-04 attempt passed structural/anatomical preflight and then failed because it assumed `/tmp` was writable under Termux.

This recovery uses a demonstrated-writable Termux temporary workspace derived from `$TMPDIR` / `$PREFIX/tmp`.

The temporary-storage failure does not alter the verified repository anatomy.

## Verified UEM physiology

```text
CSL
→ CslEngine / semantic execution
→ SemanticResult
→ UemBuilder.build(semantic_results)
→ UniversalEngineeringModel
→ EngObject + EngRelationship
```

The UEM builder accepts semantic results and produces `UniversalEngineeringModel`.

## Verified Knowledge Materialization physiology

```text
CDM documents ─┐
               ├→ KnowledgeMaterializationEngine.materialize(cdm_docs, css_standards=None)
CSS standards ─┘
                     ↓
              KnowledgeObject + KnowledgeRelationship
                     ↓
              CanonicalKnowledgeGraph
                     ↓
              MaterializedKnowledge
```

Runtime verification confirms:

- `KnowledgeMaterializationEngine.materialize()` is importable.
- `materialize([], [])` returns `MaterializedKnowledge`.
- `MaterializedKnowledge.knowledge_graph` is `CanonicalKnowledgeGraph`.
- the public knowledge_materialization package does not expose a `KnowledgeMaterializer` intermediate object.

## Convergence evidence

```json
{
  "classification": "NO_CONVERGENCE_FOUND",
  "direct_convergence_candidates": [],
  "knowledge_materialization_accepts_uem": false,
  "shared_production_files": [],
  "uem_accepts_materialized_knowledge": false
}
```

## Primary verdict

**PARALLEL LEGITIMATE PHYSIOLOGIES**

## Convergence point

**NONE DEMONSTRATED**

## E1B NOT REPRESENTABLE interpretation

**WRONG ASSUMED BOUNDARY / LEGITIMATE ARCHITECTURAL SEPARATION**

RUN-03 must not treat the absence of a direct UEM ingestion contract in Knowledge Materialization as a semantic-loss finding.

## E2 consequence

**E2 NO-OP BY EVIDENCE**

## E3 consequence

**E3 REDEFINED: characterize the real CDM/CSS -> Knowledge Materialization -> Knowledge Graph boundary**

## Executable Architecture correction

REMOVE assumed UEM -> Knowledge Materialization dependency edge; treat CSL->UEM and CDM/CSS->MaterializedKnowledge as distinct existing physiologies unless a later real convergence point is demonstrated.

## Error Memory conservation

The qualifying Termux portability failure from the previous attempt remains conserved.

Preventive rule:

> Termux execution scripts must not assume that `/tmp` is writable or suitable. Temporary execution storage must use `$TMPDIR`, `$PREFIX/tmp`, or another workspace explicitly demonstrated writable before use.

This recovery does not duplicate the Error Memory event if the prior failed execution already recorded it.

## Mutation boundary

- Production modified: **NO**
- CSL modified: **NO**
- UEM modified: **NO**
- Knowledge Materialization modified: **NO**
- Canon modified: **NO**
- Authorized artifacts: existing Error Memory mutation + this RUN-04 report.

## Validation

- Python static compilation: PASS
- E1B focused regression: PASS
- Directly relevant discovered regressions: PASS

## Next authorized stage

**STOP FOR HUMAN/AUDITOR DECISION; proposed next stage is redefined E3 characterization.**

STOP after RUN-04. No E2/E3 implementation is performed by this recovery.

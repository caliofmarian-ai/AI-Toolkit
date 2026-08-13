# PCC-01 — Durable Crash Reconciliation Physiology Inspection — RUN 036

## 1. Purpose

Determine the exact restart physiology required to reconcile incomplete durable coordination operations.

This RUN performs inspection only.

It does not implement reconciliation.

## 2. Safety Contract

- software modification: NO
- test modification: NO
- behavioral test execution: NO
- git add: NO
- commit: NO
- push: NO

## 3. Authoritative Baseline

- expected: `32ab3c44d01cb86c5857b5c70f55f6720ca11f96`
- local: `32ab3c44d01cb86c5857b5c70f55f6720ca11f96`
- origin/main: `32ab3c44d01cb86c5857b5c70f55f6720ca11f96`

## 4. RUN 035 Integration State

Journal + Coordinator integration is present locally.

Durable physiological sequence:

    PREPARING
        |
        v
    Protection persistence
        |
        v
    PROTECTION_WRITTEN
        |
        v
    Experience persistence
        |
        v
    EXPERIENCE_WRITTEN
        |
        v
    pair recovery
        |
        v
    COMPLETE

## 5. Exact Durable Repository APIs

### `lib/python/experience/persistent_repository.py`

Class `JsonFileExperienceRepository`:

- `path(self)`
- `add(self, experience)`
- `get(self, experience_id)`
- `save(self, experience)`
- `contains(self, experience_id)`

### `lib/python/experience/protection_repository.py`

Class `ProtectionRepository`:

- `add(self, protection)`
- `get(self, experience_id)`
- `save(self, protection)`
- `contains(self, experience_id)`

Class `JsonFileProtectionRepository`:

- `path(self)`
- `add(self, protection)`
- `get(self, experience_id)`
- `save(self, protection)`
- `contains(self, experience_id)`

## 6. Existing Pair Recovery Physiology

```python
def recover(
        self,
        experience_id: ExperienceId,
    ) -> CoordinatedExperience:
        """Recover both durable organs and verify their relationship."""

        if not isinstance(experience_id, ExperienceId):
            raise TypeError(
                "experience_id must be an ExperienceId"
            )

        experience_exists = self._experience_repository.contains(
            experience_id
        )
        protection_exists = self._protection_repository.contains(
            experience_id
        )

        if not experience_exists and not protection_exists:
            raise PersistenceCoordinationStateError(
                "no durable Experience/Protection pair exists"
            )

        if experience_exists and not protection_exists:
            raise PersistenceCoordinationStateError(
                "partial durable pair: Protection is missing"
            )

        if protection_exists and not experience_exists:
            raise PersistenceCoordinationStateError(
                "partial durable pair: orphan Protection exists"
            )

        experience = self._experience_repository.get(experience_id)
        protection = self._protection_repository.get(experience_id)

        self._require_matching_identity(experience, protection)

        return CoordinatedExperience(
            experience=experience,
            protection=protection,
        )
```

## 7. Durable Restart State Matrix

### PREPARING

Known durable fact: the coordination operation exists, but neither repository write has yet been durably acknowledged by the journal.

Possible surviving anatomy:

- neither organ exists;
- Protection may already exist if process death occurred after its repository write but before journal advancement.

Therefore PREPARING cannot be interpreted as proof that nothing was written. Reconciliation must inspect the repositories.

### PROTECTION_WRITTEN

Known durable fact: Protection persistence completed and that boundary was acknowledged by the journal.

Possible surviving anatomy:

- Protection exists;
- Experience may not exist;
- Experience may already exist if process death occurred after its write but before journal advancement.

Therefore both repositories must be inspected.

### EXPERIENCE_WRITTEN

Known durable fact: both persistence boundaries were acknowledged.

Expected surviving anatomy:

- Protection exists;
- Experience exists.

The existing coordinator recovery physiology can verify the pair. If valid, the journal may legally advance to COMPLETE.

### COMPLETE

Both organs were persisted, pair recovery succeeded, and the durable coordination operation completed.

No crash reconciliation is required.

## 8. Safe Reconciliation Rules

Reconciliation must be evidence-driven.

It must never fabricate a missing Experience or Protection body.

For every incomplete durable record:

1. identify its ExperienceId;
2. inspect Experience Repository presence;
3. inspect Protection Repository presence;
4. compare surviving anatomy with the durable stage.

If both organs exist:

1. recover the pair through the existing coordinator;
2. verify the shared Experience identity;
3. advance the journal only through legal existing transitions;
4. finish at COMPLETE.

If only Protection exists, the missing Experience body must not be fabricated.

If only Experience exists, the missing Protection body must not be fabricated.

If neither exists, the journal remains evidence of interruption; it is not a copy of either organ.

## 9. Required Reconciliation Physiology

The Persistence Coordinator should interpret durable coordination evidence against actual surviving organs without becoming the Journal or either repository.

Required pathway:

    process starts
        |
        v
    journal.incomplete_records()
        |
        v
    inspect each durable operation
        |
        v
    inspect Experience presence
        +
    inspect Protection presence
        |
        v
    classify surviving anatomy
        |
        +-- both exist --> recover pair --> legal journal advancement --> COMPLETE
        |
        +-- missing organ --> explicit unresolved interruption

The reconciler must operate only on surviving durable evidence. It must not reconstruct missing organ bodies from assumptions.

## 10. Required Behavioral Evidence For The Next Implementation

1. PREPARING with neither organ does not become falsely complete.
2. PREPARING with both surviving organs can reconcile legally.
3. PROTECTION_WRITTEN with Protection only remains explicitly unresolved.
4. PROTECTION_WRITTEN with both organs can reconcile.
5. EXPERIENCE_WRITTEN with both organs advances to COMPLETE.
6. COMPLETE is not treated as incomplete.
7. Experience identity is preserved.
8. Protection identity relationship is preserved.
9. Missing Experience is never fabricated.
10. Missing Protection is never fabricated.
11. Journal and repositories remain distinct organs.
12. Existing normal persistence physiology remains unchanged.

Real process-death demonstration remains a later evidence step after reconciliation physiology is implemented.

## 11. Repository State

```text
 M lib/python/experience/persistence_coordinator.py
?? lib/python/experience/coordination_journal.py
?? tests/experience/test_experience_coordination_journal.py
?? work/implementation-reports/PCC-01/PCC-01_DURABLE_COORDINATION_JOURNAL_COORDINATOR_INTEGRATION_PRE_IMPLEMENTATION_INSPECTION_RUN_033.md
?? work/implementation-reports/PCC-01/PCC-01_DURABLE_COORDINATION_JOURNAL_IMPLEMENTATION_REPORT_RUN_032.md
?? work/implementation-reports/PCC-01/PCC-01_DURABLE_COORDINATION_JOURNAL_PRE_IMPLEMENTATION_INSPECTION_RUN_031.md
?? work/implementation-reports/PCC-01/PCC-01_PROTECTION_PERSISTENCE_COORDINATOR_CONSERVATION_RUN_030.md
?? work/implementation-reports/PCC-01/PCC-01_RUN020_EVIDENCE_CONSERVATION_REPORT_RUN_021.md
?? work/implementation-reports/PCC-01/PCC-01_RUN034B_COORDINATION_MODEL_RECONCILIATION_INSPECTION.md
?? work/implementation-reports/PCC-01/PCC-01_RUN034C_FAILURE_RECOVERY_AND_EXACT_INTEGRATION_ANATOMY.md
?? work/implementation-reports/PCC-01/PCC-01_RUN034D_EXACT_LOCAL_JOURNAL_ANATOMY_FOR_INTEGRATION.md
?? work/implementation-reports/PCC-01/PCC-01_RUN034_CAUSAL_ANATOMY_INSPECTION.md
?? work/implementation-reports/PCC-01/PCC-01_RUN035_DURABLE_JOURNAL_COORDINATOR_INTEGRATION.md
```

## 12. RUN 036 Conclusion

**Durable Crash Reconciliation Physiology:** INSPECTED

**Reconciliation Implementation:** NOT IMPLEMENTED

**Durable Crash Coordination:** NOT DEMONSTRATED

The next implementation must reconcile surviving durable organs from evidence and must not invent missing organ bodies.

## 13. PCC-01 Status

- Journal + Coordinator integration: BUILT LOCALLY
- Durable reconciliation physiology: INSPECTED
- Durable reconciliation implementation: NOT IMPLEMENTED
- Durable crash coordination: NOT DEMONSTRATED
- PCC-01 Implementation: NOT DEMONSTRATED
- Canonical Status: NOT CANON
- Production Status: NOT PRODUCTION-READY

## 14. Conservation

- git add: NO
- commit: NO
- push: NO

## 15. Next Required Action

IMPLEMENT DURABLE CRASH RECONCILIATION AGAINST THE EXACT PHYSIOLOGY MATERIALIZED IN THIS REPORT.

---

END OF PCC-01 RUN 036

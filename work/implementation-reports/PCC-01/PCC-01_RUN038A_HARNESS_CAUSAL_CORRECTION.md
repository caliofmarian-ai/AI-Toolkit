# PCC-01 — RUN 038A Harness Causal Correction

## Cause

RUN 038 failed before reaching the intended process-death boundary.

The failure was caused by the experimental harness assuming:

`ExperienceProtection.create()`

The existing conserved organism does not expose that construction pathway.

Therefore the failure is classified as:

**HARNESS API ASSUMPTION — NOT ORGANISM FAILURE**

## Correction

The failed RUN 038 harness was corrected by extracting the exact ExperienceProtection construction physiology from the already-conserved Protection restart harness:

`tests/experience/harness/pcc01_protection_restart_writer.py`

No new Protection constructor was added.

No production anatomy was changed to accommodate the harness.

## Contract Discipline

- accepted organism physiology remains authoritative;
- harness adapts to organism;
- organism does not adapt to mistaken harness assumptions;
- Experience != Protection;
- Persistence != authority;
- no Canon modification;
- no production claim.

## Baseline

- expected: `32ab3c44d01cb86c5857b5c70f55f6720ca11f96`
- local: `32ab3c44d01cb86c5857b5c70f55f6720ca11f96`
- origin/main: `32ab3c44d01cb86c5857b5c70f55f6720ca11f96`

## Repository State

```text
 M lib/python/experience/persistence_coordinator.py
?? lib/python/experience/coordination_journal.py
?? tests/experience/harness/pcc01_coordination_crash_reconciler.py
?? tests/experience/harness/pcc01_coordination_crash_writer.py
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
?? work/implementation-reports/PCC-01/PCC-01_RUN036_DURABLE_CRASH_RECONCILIATION_PHYSIOLOGY_INSPECTION.md
?? work/implementation-reports/PCC-01/PCC-01_RUN037_DURABLE_CRASH_RECONCILIATION_IMPLEMENTATION.md
```

## Status

- RUN 038 original demonstration: NOT DEMONSTRATED
- RUN 038 failure: RECONCILED AS HARNESS DEFECT
- corrected harness: READY
- durable crash coordination: NOT YET DEMONSTRATED BY CORRECTED HARNESS
- PCC-01 Implementation: NOT DEMONSTRATED
- Canonical Status: NOT CANON
- Production Status: NOT PRODUCTION-READY

## Next

Re-execute the corrected real Process A / Process B crash-reconciliation demonstration.

---

END OF RUN 038A

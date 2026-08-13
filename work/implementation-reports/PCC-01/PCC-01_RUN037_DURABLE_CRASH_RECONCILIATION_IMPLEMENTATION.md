# PCC-01 — Durable Crash Reconciliation Implementation — RUN 037

## 1. Purpose

Implement evidence-driven reconciliation of incomplete durable coordination operations.

## 2. Baseline

- expected: `32ab3c44d01cb86c5857b5c70f55f6720ca11f96`
- local: `32ab3c44d01cb86c5857b5c70f55f6720ca11f96`
- origin/main: `32ab3c44d01cb86c5857b5c70f55f6720ca11f96`

## 3. Implemented Physiology

The Persistence Coordinator now exposes `reconcile_incomplete()`.

Physiology:

    journal.incomplete_records()
        |
        v
    inspect surviving Experience + Protection
        |
        +-- missing organ --> remain incomplete
        |
        +-- both survive --> recover pair
                              |
                              v
                         legal journal advancement
                              |
                              v
                           COMPLETE

## 4. Safety Invariants

- Missing Experience is not fabricated.
- Missing Protection is not fabricated.
- Journal remains a distinct organ.
- Experience Repository remains distinct.
- Protection Repository remains distinct.
- Existing `recover()` physiology is reused.
- Durable transitions use the existing journal transition law.

## 5. Stage Reconciliation

- PREPARING + both organs -> PROTECTION_WRITTEN -> EXPERIENCE_WRITTEN -> COMPLETE
- PROTECTION_WRITTEN + both organs -> EXPERIENCE_WRITTEN -> COMPLETE
- EXPERIENCE_WRITTEN + both organs -> COMPLETE
- any incomplete stage + missing organ -> remains incomplete

## 6. Verification

- Python syntax: PASS
- structural reconciliation anatomy: PASS
- no organ-fabrication pathway: PASS
- behavioral test execution: NO

## 7. Exact Coordinator Diff

```diff
diff --git a/lib/python/experience/persistence_coordinator.py b/lib/python/experience/persistence_coordinator.py
index 5a8eca2..b080efe 100644
--- a/lib/python/experience/persistence_coordinator.py
+++ b/lib/python/experience/persistence_coordinator.py
@@ -2,15 +2,21 @@
 
 Experience and Protection remain independent organs.
 
+The Durable Coordination Journal is also a distinct organ.
+
 The coordinator does not become Experience.
 The coordinator does not become Protection.
+The coordinator does not become the Durable Coordination Journal.
 The coordinator does not grant authority.
 
 Its responsibility is to make the physiological relationship between
-their persistence operations explicit and inspectable.
+their persistence operations explicit, inspectable, and durably
+observable across process death.
 
 Persistence != authority.
 Storage != Experience.
+Journal != Experience.
+Journal != Protection.
 """
 
 from __future__ import annotations
@@ -19,6 +25,10 @@ from dataclasses import dataclass
 from enum import Enum
 from typing import Callable
 
+from .coordination_journal import (
+    DurableCoordinationStage,
+    JsonFileCoordinationJournal,
+)
 from .identity import ExperienceId
 from .model import Experience
 from .persistent_repository import JsonFileExperienceRepository
@@ -73,19 +83,23 @@ StageObserver = Callable[[CoordinationState], None]
 
 
 class ExperiencePersistenceCoordinator:
-    """Coordinates persistence without collapsing organ boundaries.
+    """Coordinates Experience, Protection, and durable coordination evidence.
+
+    Experience and Protection repositories remain responsible for their
+    own durable bodies.
 
-    The repositories remain responsible for their own durable bodies.
+    The Durable Coordination Journal remains responsible for durable
+    evidence of the physiological coordination operation.
 
-    This first implementation makes the physiological write order and
-    failure boundary explicit.  Durable journal persistence is NOT yet
-    claimed by this class.
+    The coordinator bridges physiological events between these distinct
+    organs without collapsing their identities or responsibilities.
     """
 
     def __init__(
         self,
         experience_repository: JsonFileExperienceRepository,
         protection_repository: JsonFileProtectionRepository,
+        coordination_journal: JsonFileCoordinationJournal | None = None,
     ) -> None:
         if not isinstance(
             experience_repository,
@@ -105,8 +119,21 @@ class ExperiencePersistenceCoordinator:
                 "JsonFileProtectionRepository"
             )
 
+        if (
+            coordination_journal is not None
+            and not isinstance(
+                coordination_journal,
+                JsonFileCoordinationJournal,
+            )
+        ):
+            raise TypeError(
+                "coordination_journal must be "
+                "JsonFileCoordinationJournal or None"
+            )
+
         self._experience_repository = experience_repository
         self._protection_repository = protection_repository
+        self._coordination_journal = coordination_journal
 
     def persist(
         self,
@@ -115,17 +142,28 @@ class ExperiencePersistenceCoordinator:
         *,
         observe_stage: StageObserver | None = None,
     ) -> CoordinatedExperience:
-        """Persist the two organs through one explicit physiological path.
+        """Persist distinct organs through one explicit physiological path.
 
         Protection is conserved before Experience so protected material
         is never intentionally persisted first as an unprotected
         Experience.
 
-        This method does NOT claim crash atomicity.
+        When a Durable Coordination Journal is supplied, each completed
+        physiological boundary is durably recorded.
+
+        This method makes interruption state durable. It does not by
+        itself claim automatic crash reconciliation.
         """
 
         self._require_matching_identity(experience, protection)
 
+        durable_record = None
+
+        if self._coordination_journal is not None:
+            durable_record = self._coordination_journal.begin(
+                experience.experience_id
+            )
+
         self._observe(
             CoordinationState(
                 experience_id=experience.experience_id,
@@ -136,6 +174,12 @@ class ExperiencePersistenceCoordinator:
 
         self._persist_protection(protection)
 
+        if durable_record is not None:
+            durable_record = self._coordination_journal.advance(
+                durable_record.coordination_operation_id,
+                DurableCoordinationStage.PROTECTION_WRITTEN,
+            )
+
         self._observe(
             CoordinationState(
                 experience_id=experience.experience_id,
@@ -146,6 +190,12 @@ class ExperiencePersistenceCoordinator:
 
         self._persist_experience(experience)
 
+        if durable_record is not None:
+            durable_record = self._coordination_journal.advance(
+                durable_record.coordination_operation_id,
+                DurableCoordinationStage.EXPERIENCE_WRITTEN,
+            )
+
         self._observe(
             CoordinationState(
                 experience_id=experience.experience_id,
@@ -156,6 +206,12 @@ class ExperiencePersistenceCoordinator:
 
         pair = self.recover(experience.experience_id)
 
+        if durable_record is not None:
+            self._coordination_journal.advance(
+                durable_record.coordination_operation_id,
+                DurableCoordinationStage.COMPLETE,
+            )
+
         self._observe(
             CoordinationState(
                 experience_id=experience.experience_id,
@@ -209,6 +265,79 @@ class ExperiencePersistenceCoordinator:
             protection=protection,
         )
 
+    def reconcile_incomplete(
+        self,
+    ) -> tuple[CoordinatedExperience, ...]:
+        """Reconcile incomplete durable operations from surviving evidence.
+
+        Reconciliation never fabricates a missing Experience or
+        Protection body.
+
+        Only operations whose Experience and Protection organs both
+        survive may be completed automatically.
+
+        Operations with missing organs remain durably incomplete.
+        """
+
+        if self._coordination_journal is None:
+            raise PersistenceCoordinationStateError(
+                "durable coordination journal is required "
+                "for crash reconciliation"
+            )
+
+        reconciled: list[CoordinatedExperience] = []
+
+        for record in self._coordination_journal.incomplete_records():
+            experience_id = record.experience_id
+
+            experience_exists = self._experience_repository.contains(
+                experience_id
+            )
+            protection_exists = self._protection_repository.contains(
+                experience_id
+            )
+
+            if not experience_exists or not protection_exists:
+                continue
+
+            pair = self.recover(experience_id)
+
+            current = record
+
+            if current.stage is DurableCoordinationStage.PREPARING:
+                current = self._coordination_journal.advance(
+                    current.coordination_operation_id,
+                    DurableCoordinationStage.PROTECTION_WRITTEN,
+                )
+
+            if (
+                current.stage
+                is DurableCoordinationStage.PROTECTION_WRITTEN
+            ):
+                current = self._coordination_journal.advance(
+                    current.coordination_operation_id,
+                    DurableCoordinationStage.EXPERIENCE_WRITTEN,
+                )
+
+            if (
+                current.stage
+                is DurableCoordinationStage.EXPERIENCE_WRITTEN
+            ):
+                current = self._coordination_journal.advance(
+                    current.coordination_operation_id,
+                    DurableCoordinationStage.COMPLETE,
+                )
+
+            if current.stage is not DurableCoordinationStage.COMPLETE:
+                raise PersistenceCoordinationStateError(
+                    "durable coordination operation did not "
+                    "reach COMPLETE"
+                )
+
+            reconciled.append(pair)
+
+        return tuple(reconciled)
+
     def _persist_protection(
         self,
         protection: ExperienceProtection,
```

## 8. Repository State

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
?? work/implementation-reports/PCC-01/PCC-01_RUN036_DURABLE_CRASH_RECONCILIATION_PHYSIOLOGY_INSPECTION.md
```

## 9. Epistemic Status

- Durable Coordination Journal: BUILT LOCALLY
- Journal + Coordinator integration: BUILT LOCALLY
- Durable crash reconciliation physiology: BUILT LOCALLY
- Real process crash/restart reconciliation: NOT YET DEMONSTRATED
- PCC-01 Implementation: NOT DEMONSTRATED
- Canonical Status: NOT CANON
- Production Status: NOT PRODUCTION-READY

## 10. Conservation

- git add: NO
- commit: NO
- push: NO

## 11. Next Required Action

Demonstrate reconciliation across a real process death/restart boundary before conservation.

---

END OF PCC-01 RUN 037

# PCC-01 — Durable Journal + Coordinator Integration — RUN 035

## Purpose

Integrate the already-built Durable Coordination Journal with the conserved Experience Persistence Coordinator.

The two organs remain distinct.

The coordinator emits durable physiological transitions through the journal.

## Safety Contract

- no approximate AST mutation
- no approximate textual insertion
- exact conserved source prerequisite
- complete deterministic coordinator replacement
- automatic rollback on failure
- no git add
- no commit
- no push

## 1. Baseline

- expected: `32ab3c44d01cb86c5857b5c70f55f6720ca11f96`
- local: `32ab3c44d01cb86c5857b5c70f55f6720ca11f96`
- origin/main: `32ab3c44d01cb86c5857b5c70f55f6720ca11f96`

## 2. Integration Implemented

The conserved coordinator now accepts an optional distinct `JsonFileCoordinationJournal` organ.

Durable physiological sequence:

```text
journal.begin(PREPARING)
        ↓
_persist_protection
        ↓
journal.advance(PROTECTION_WRITTEN)
        ↓
_persist_experience
        ↓
journal.advance(EXPERIENCE_WRITTEN)
        ↓
recover Experience + Protection
        ↓
journal.advance(COMPLETE)
```

## 3. Anatomical Separation

- Experience remains Experience.
- Protection remains Protection.
- Experience Repository remains independent.
- Protection Repository remains independent.
- Durable Coordination Journal remains independent.
- Coordinator bridges physiological events.
- Durable operation identity remains distinct from ExperienceId.

## 4. Compatibility

The journal parameter is optional.

Existing coordinator construction using only Experience and Protection repositories remains structurally supported.

## 5. Verification Performed

- authoritative Git baseline: PASS
- exact conserved coordinator prerequisite: PASS
- exact local journal API prerequisite: PASS
- deterministic complete coordinator replacement: PASS
- Python syntax: PASS
- integrated physiology structural verification: PASS

No behavioral test suite was executed by this RUN.

## 6. Exact Coordinator Diff

```diff
diff --git a/lib/python/experience/persistence_coordinator.py b/lib/python/experience/persistence_coordinator.py
index 5a8eca2..c1a0254 100644
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
```

## 7. Repository State

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

## 8. Epistemic Status

- Durable Coordination Journal: BUILT LOCALLY
- Journal + Coordinator integration: BUILT LOCALLY
- Durable interruption evidence: IMPLEMENTED LOCALLY
- Automatic crash reconciliation: NOT IMPLEMENTED
- Durable crash coordination: NOT YET DEMONSTRATED
- PCC-01 Implementation: NOT DEMONSTRATED
- Canonical Status: NOT CANON
- Production Status: NOT PRODUCTION-READY

## 9. Conservation

- git add: NO
- commit: NO
- push: NO

## 10. Next Organ

**DURABLE CRASH RECONCILIATION PHYSIOLOGY**

---

END OF PCC-01 RUN 035

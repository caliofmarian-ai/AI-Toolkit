# PCC-01 — RUN 041A — Pre-Provenance Local Recovery

## Purpose

Identify the pre-existing local modification that prevented RUN 041.

This run performs no software mutation, no staging, no commit and no push.

## Bash Executed — Complete

```bash
#!/data/data/com.termux/files/usr/bin/bash
set -uo pipefail

cd "$HOME/storage/shared/AI-Projects/AI-Toolkit" || exit 1

REPORT="work/implementation-reports/PCC-01/PCC-01_RUN041A_PRE_PROVENANCE_LOCAL_RECOVERY.md"
OUT="$PREFIX/tmp/pcc01_run041a_output.log"
SELF="$PREFIX/tmp/pcc01_recovery_041a.sh"

mkdir -p "$(dirname "$REPORT")"
: > "$OUT"

exec > >(tee "$OUT") 2>&1

echo "=========================================================="
echo "PCC-01 — RUN 041A"
echo "PRE-PROVENANCE LOCAL RECOVERY"
echo "=========================================================="

echo
echo "[1/5] Git identity"
git fetch origin main --quiet
echo "LOCAL:"
git rev-parse HEAD
echo "origin/main:"
git rev-parse origin/main

echo
echo "[2/5] Exact working tree"
git status --short

echo
echo "[3/5] Exact persistence_coordinator diff"
git diff -- lib/python/experience/persistence_coordinator.py

echo
echo "[4/5] Compare local coordinator with GitHub baseline"
echo "LOCAL SHA256:"
sha256sum lib/python/experience/persistence_coordinator.py
echo
echo "GIT HEAD SHA256:"
git show HEAD:lib/python/experience/persistence_coordinator.py | sha256sum

echo
echo "[5/5] Build autosufficient recovery evidence"

{
    echo "# PCC-01 — RUN 041A — Pre-Provenance Local Recovery"
    echo
    echo "## Purpose"
    echo
    echo "Identify the pre-existing local modification that prevented RUN 041."
    echo
    echo "This run performs no software mutation, no staging, no commit and no push."
    echo
    echo "## Bash Executed — Complete"
    echo
    echo '```bash'
    cat "$SELF"
    echo '```'
    echo
    echo "## Output — Complete"
    echo
    echo '```text'
    cat "$OUT"
    echo '```'
    echo
    echo "## Boundary"
    echo
    echo "- Software modified: NO"
    echo "- Tests executed: NO"
    echo "- git add: NO"
    echo "- commit: NO"
    echo "- push: NO"
} > "$REPORT"

echo
echo "=========================================================="
echo "RUN 041A COMPLETE"
echo "=========================================================="
echo "REPORT:"
echo "$REPORT"
echo
echo "NO software mutation"
echo "NO git add"
echo "NO commit"
echo "NO push"
echo "=========================================================="
```

## Output — Complete

```text
==========================================================
PCC-01 — RUN 041A
PRE-PROVENANCE LOCAL RECOVERY
==========================================================

[1/5] Git identity
LOCAL:
b6f9d62bfe2aad16632e4901c4302569b033d624
origin/main:
b6f9d62bfe2aad16632e4901c4302569b033d624

[2/5] Exact working tree
 M lib/python/experience/persistence_coordinator.py
?? tests/experience/harness/pcc01_coordination_crash_reconciler.py
?? tests/experience/harness/pcc01_coordination_crash_writer.py
?? work/implementation-reports/PCC-01/PCC-01_RUN034C_FAILURE_RECOVERY_AND_EXACT_INTEGRATION_ANATOMY.md
?? work/implementation-reports/PCC-01/PCC-01_RUN034D_EXACT_LOCAL_JOURNAL_ANATOMY_FOR_INTEGRATION.md
?? work/implementation-reports/PCC-01/PCC-01_RUN038A_HARNESS_CAUSAL_CORRECTION.md

[3/5] Exact persistence_coordinator diff
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

[4/5] Compare local coordinator with GitHub baseline
LOCAL SHA256:
e3e641003c99a67ee55f2b1357a9565d9616efff1370e6cc3b68f4f18460d23a  lib/python/experience/persistence_coordinator.py

GIT HEAD SHA256:
601ce0b09cf0927ebf23bb11e03eb6462ebb40b8738565c2b5fb707996bc8749  -

[5/5] Build autosufficient recovery evidence
```

## Boundary

- Software modified: NO
- Tests executed: NO
- git add: NO
- commit: NO
- push: NO

# PCC-01 — RUN 041B — Coordinator Local Reconciliation and Conservation

## Purpose

Determine whether the pre-existing local modification of
`lib/python/experience/persistence_coordinator.py` belongs to the
Durable Coordination implementation lineage already documented by
RUN 035–038B, and conserve it without discarding local tissue.

## Baseline

- LOCAL before conservation: `b6f9d62bfe2aad16632e4901c4302569b033d624`
- origin/main before conservation: `b6f9d62bfe2aad16632e4901c4302569b033d624`

## Historical Evidence Used

- `work/implementation-reports/PCC-01/PCC-01_RUN035_DURABLE_JOURNAL_COORDINATOR_INTEGRATION.md`
- `work/implementation-reports/PCC-01/PCC-01_RUN036_DURABLE_CRASH_RECONCILIATION_PHYSIOLOGY_INSPECTION.md`
- `work/implementation-reports/PCC-01/PCC-01_RUN037_DURABLE_CRASH_RECONCILIATION_IMPLEMENTATION.md`
- `work/implementation-reports/PCC-01/PCC-01_RUN038B_DURABLE_CRASH_RECONCILIATION_PROOF.md`
- `work/implementation-reports/PCC-01/PCC-01_RUN041A_PRE_PROVENANCE_LOCAL_RECOVERY.md`

## Bash Executed — Complete

```bash
#!/data/data/com.termux/files/usr/bin/bash
set -uo pipefail

export GIT_PAGER=cat
export PAGER=cat
export GH_PAGER=cat

cd "$HOME/storage/shared/AI-Projects/AI-Toolkit" || exit 1

COORD="lib/python/experience/persistence_coordinator.py"

RUN035="work/implementation-reports/PCC-01/PCC-01_RUN035_DURABLE_JOURNAL_COORDINATOR_INTEGRATION.md"
RUN036="work/implementation-reports/PCC-01/PCC-01_RUN036_DURABLE_CRASH_RECONCILIATION_PHYSIOLOGY_INSPECTION.md"
RUN037="work/implementation-reports/PCC-01/PCC-01_RUN037_DURABLE_CRASH_RECONCILIATION_IMPLEMENTATION.md"
RUN038B="work/implementation-reports/PCC-01/PCC-01_RUN038B_DURABLE_CRASH_RECONCILIATION_PROOF.md"
RUN041A="work/implementation-reports/PCC-01/PCC-01_RUN041A_PRE_PROVENANCE_LOCAL_RECOVERY.md"

REPORT="work/implementation-reports/PCC-01/PCC-01_RUN041B_COORDINATOR_LOCAL_RECONCILIATION_AND_CONSERVATION.md"

OUT="$PREFIX/tmp/pcc01_run041b_output.log"
DIFF="$PREFIX/tmp/pcc01_run041b_coordinator.diff"
SCRIPT_SELF="$PREFIX/tmp/pcc01_run041b.sh"

mkdir -p "$(dirname "$REPORT")"
: > "$OUT"
: > "$DIFF"

exec > >(tee -a "$OUT") 2>&1

fail() {
    CODE="${1:-1}"
    echo
    echo "=========================================================="
    echo "RUN 041B STOPPED SAFELY"
    echo "=========================================================="
    echo "Exit code: $CODE"
    echo "No destructive operation performed."
    echo "No commit/push performed after failure."
    exit "$CODE"
}

echo "=========================================================="
echo "PCC-01"
echo "COORDINATOR LOCAL RECONCILIATION + CONSERVATION"
echo "RUN 041B"
echo "=========================================================="

echo
echo "[1/9] Verify Git baseline"

git fetch origin main --quiet || fail $?

LOCAL="$(git rev-parse HEAD)" || fail $?
REMOTE="$(git rev-parse origin/main)" || fail $?

echo "LOCAL:       $LOCAL"
echo "origin/main: $REMOTE"

[ "$LOCAL" = "$REMOTE" ] || {
    echo "ERROR: LOCAL != origin/main"
    fail 1
}

BASE="$LOCAL"

echo "PASS: synchronized baseline"

echo
echo "[2/9] Verify required historical evidence"

for f in \
    "$RUN035" \
    "$RUN036" \
    "$RUN037" \
    "$RUN038B" \
    "$RUN041A"
do
    [ -s "$f" ] || {
        echo "ERROR: required evidence missing: $f"
        fail 1
    }

    echo "PASS: $f"
done

echo
echo "[3/9] Verify coordinator is the only tracked local mutation"

TRACKED="$(
    {
        git diff --name-only
        git diff --cached --name-only
    } | sort -u | sed '/^$/d'
)"

echo "TRACKED LOCAL DIFFERENCES:"
printf '%s\n' "$TRACKED"

[ "$TRACKED" = "$COORD" ] || {
    echo "ERROR: tracked boundary is not exactly persistence_coordinator.py"
    fail 1
}

echo "PASS: exact tracked mutation boundary"

echo
echo "[4/9] Capture exact coordinator diff"

git diff -- "$COORD" | tee "$DIFF"

[ -s "$DIFF" ] || {
    echo "ERROR: coordinator diff unexpectedly empty"
    fail 1
}

echo
echo "PASS: coordinator diff captured"

echo
echo "[5/9] Causal reconciliation against RUN 035–038B"

python - "$DIFF" "$RUN035" "$RUN036" "$RUN037" "$RUN038B" <<'PY' || fail $?
from pathlib import Path
import sys

diff_path = Path(sys.argv[1])
evidence_paths = [Path(p) for p in sys.argv[2:]]

diff = diff_path.read_text(encoding="utf-8", errors="replace")
evidence = "\n".join(
    p.read_text(encoding="utf-8", errors="replace")
    for p in evidence_paths
)

required_diff_signals = (
    "coordination_journal",
    "_coordination_journal",
)

if not all(signal in diff for signal in required_diff_signals):
    raise SystemExit(
        "FAIL: local coordinator diff does not expose "
        "Durable Coordination Journal integration"
    )

required_evidence_signals = (
    "DURABLE",
    "COORDINATION",
)

upper_evidence = evidence.upper()

if not all(signal in upper_evidence for signal in required_evidence_signals):
    raise SystemExit(
        "FAIL: historical evidence does not establish "
        "Durable Coordination context"
    )

if "DEMONSTRATED LOCALLY" not in upper_evidence:
    raise SystemExit(
        "FAIL: historical evidence does not contain "
        "the local demonstration conclusion"
    )

print(
    "PASS: local coordinator mutation belongs to the "
    "Durable Coordination implementation lineage"
)
print(
    "PASS: RUN 035–038B provide the corresponding "
    "historical implementation/demonstration context"
)
PY

echo
echo "[6/9] Verify current coordinator syntax and conserved behavioral physiology"

python -m py_compile \
    lib/python/experience/persistence_coordinator.py \
    lib/python/experience/coordination_journal.py || fail $?

python -m pytest -q \
    tests/experience/test_experience_persistence_coordinator.py \
    tests/experience/test_experience_coordination_journal.py || fail $?

echo
echo "Running complete Experience regression..."

python -m pytest -q tests/experience || fail $?

echo "PASS: coordinator + journal behavior"
echo "PASS: complete Experience regression"

echo
echo "[7/9] Generate autosufficient RUN 041B evidence"

{
    echo "# PCC-01 — RUN 041B — Coordinator Local Reconciliation and Conservation"
    echo
    echo "## Purpose"
    echo
    echo "Determine whether the pre-existing local modification of"
    echo "\`lib/python/experience/persistence_coordinator.py\` belongs to the"
    echo "Durable Coordination implementation lineage already documented by"
    echo "RUN 035–038B, and conserve it without discarding local tissue."
    echo
    echo "## Baseline"
    echo
    echo "- LOCAL before conservation: \`$BASE\`"
    echo "- origin/main before conservation: \`$REMOTE\`"
    echo
    echo "## Historical Evidence Used"
    echo
    echo "- \`$RUN035\`"
    echo "- \`$RUN036\`"
    echo "- \`$RUN037\`"
    echo "- \`$RUN038B\`"
    echo "- \`$RUN041A\`"
    echo
    echo "## Bash Executed — Complete"
    echo
    echo '```bash'
    cat "$SCRIPT_SELF"
    echo '```'
    echo
    echo "## Output — Complete"
    echo
    echo '```text'
    cat "$OUT"
    echo '```'
    echo
    echo "## Coordinator Diff — Complete"
    echo
    echo '```diff'
    cat "$DIFF"
    echo '```'
    echo
    echo "## Reconciliation Result"
    echo
    echo "- Local tracked mutation boundary: persistence coordinator only."
    echo "- Durable Coordination lineage: CONFIRMED."
    echo "- Syntax validation: PASS."
    echo "- Dedicated coordinator/journal behavior: PASS."
    echo "- Complete Experience regression: PASS."
    echo
    echo "## Conservation Status"
    echo
    echo "Pending Git conservation at the moment this section was generated."
} > "$REPORT"

echo "PASS: autosufficient RUN 041B evidence generated"

echo
echo "[8/9] Stage exact reconciliation set"

git add -- \
    "$COORD" \
    "$RUN041A" \
    "$REPORT" || fail $?

ACTUAL="$(
    git diff --cached --name-only | sort
)"

EXPECTED="$(
    printf '%s\n' \
        "$COORD" \
        "$RUN041A" \
        "$REPORT" \
    | sort
)"

if [ "$ACTUAL" != "$EXPECTED" ]; then
    echo "ERROR: staged boundary differs from exact authorized set"
    echo
    echo "ACTUAL:"
    printf '%s\n' "$ACTUAL"
    git reset --quiet
    fail 1
fi

git diff --cached --check -- "$COORD" || {
    echo "ERROR: coordinator contains Git whitespace errors"
    git reset --quiet
    fail 1
}

echo "PASS: exact conservation boundary"

echo
echo "[9/9] Commit, push, verify, finalize historical record"

git commit -m \
    "feat: conserve PCC-01 durable coordinator integration" || fail $?

IMPLEMENTATION_HEAD="$(git rev-parse HEAD)" || fail $?

git push origin main || fail $?
git fetch origin main --quiet || fail $?

REMOTE_AFTER="$(git rev-parse origin/main)" || fail $?

[ "$IMPLEMENTATION_HEAD" = "$REMOTE_AFTER" ] || {
    echo "ERROR: implementation conservation not present on origin/main"
    fail 1
}

echo "PASS: coordinator conservation synchronized"

{
    echo
    echo "## Git Conservation Result"
    echo
    echo "- Baseline HEAD: \`$BASE\`"
    echo "- Coordinator conservation HEAD: \`$IMPLEMENTATION_HEAD\`"
    echo "- origin/main: \`$REMOTE_AFTER\`"
    echo "- LOCAL == origin/main: PASS"
    echo
    echo "## Final Conclusion"
    echo
    echo "**The previously uncommitted persistence coordinator mutation was"
    echo "reconciled with the Durable Coordination lineage, behaviorally"
    echo "validated, and conserved without discarding local implementation tissue.**"
    echo
    echo "No PCC-01 CANON or PRODUCTION-READY claim is made by this run."
    echo
    echo "---"
    echo
    echo "END OF PCC-01 RUN 041B"
} >> "$REPORT"

git add -- "$REPORT" || fail $?

git commit -m \
    "docs: finalize PCC-01 RUN 041B evidence" || fail $?

FINAL_HEAD="$(git rev-parse HEAD)" || fail $?

git push origin main || fail $?
git fetch origin main --quiet || fail $?

FINAL_REMOTE="$(git rev-parse origin/main)" || fail $?

[ "$FINAL_HEAD" = "$FINAL_REMOTE" ] || {
    echo "ERROR: final RUN 041B evidence not synchronized"
    fail 1
}

echo
echo "=========================================================="
echo "RUN 041B COMPLETE"
echo "=========================================================="
echo
echo "BASE:"
echo "$BASE"
echo
echo "COORDINATOR CONSERVATION:"
echo "$IMPLEMENTATION_HEAD"
echo
echo "FINAL EVIDENCE HEAD:"
echo "$FINAL_HEAD"
echo
echo "LOCAL == origin/main:"
echo "PASS"
echo
echo "COORDINATOR LOCAL MUTATION:"
echo "RECONCILED + VALIDATED + CONSERVED"
echo
echo "NEXT:"
echo "RUN 041 Experience Provenance Integration may resume."
echo "GPT verifies GitHub directly."
echo "=========================================================="
```

## Output — Complete

```text
==========================================================
PCC-01
COORDINATOR LOCAL RECONCILIATION + CONSERVATION
RUN 041B
==========================================================

[1/9] Verify Git baseline
LOCAL:       b6f9d62bfe2aad16632e4901c4302569b033d624
origin/main: b6f9d62bfe2aad16632e4901c4302569b033d624
PASS: synchronized baseline

[2/9] Verify required historical evidence
PASS: work/implementation-reports/PCC-01/PCC-01_RUN035_DURABLE_JOURNAL_COORDINATOR_INTEGRATION.md
PASS: work/implementation-reports/PCC-01/PCC-01_RUN036_DURABLE_CRASH_RECONCILIATION_PHYSIOLOGY_INSPECTION.md
PASS: work/implementation-reports/PCC-01/PCC-01_RUN037_DURABLE_CRASH_RECONCILIATION_IMPLEMENTATION.md
PASS: work/implementation-reports/PCC-01/PCC-01_RUN038B_DURABLE_CRASH_RECONCILIATION_PROOF.md
PASS: work/implementation-reports/PCC-01/PCC-01_RUN041A_PRE_PROVENANCE_LOCAL_RECOVERY.md

[3/9] Verify coordinator is the only tracked local mutation
TRACKED LOCAL DIFFERENCES:
lib/python/experience/persistence_coordinator.py
PASS: exact tracked mutation boundary

[4/9] Capture exact coordinator diff
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

PASS: coordinator diff captured

[5/9] Causal reconciliation against RUN 035–038B
PASS: local coordinator mutation belongs to the Durable Coordination implementation lineage
PASS: RUN 035–038B provide the corresponding historical implementation/demonstration context

[6/9] Verify current coordinator syntax and conserved behavioral physiology
....................                                                     [100%]
20 passed in 0.75s

Running complete Experience regression...
........................................................................ [ 54%]
.............................................................            [100%]
133 passed in 2.90s
PASS: coordinator + journal behavior
PASS: complete Experience regression

[7/9] Generate autosufficient RUN 041B evidence
```

## Coordinator Diff — Complete

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

## Reconciliation Result

- Local tracked mutation boundary: persistence coordinator only.
- Durable Coordination lineage: CONFIRMED.
- Syntax validation: PASS.
- Dedicated coordinator/journal behavior: PASS.
- Complete Experience regression: PASS.

## Conservation Status

Pending Git conservation at the moment this section was generated.

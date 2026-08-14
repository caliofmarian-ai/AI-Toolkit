# PCC-01 — RUN 054 — Persistence Migration Implementation

## Purpose

Resolve the PCC-01 Production-Ready migration gap identified by RUN 052.

## Git authority

- Baseline: `4401d360c5cf714ee656e341282c97f725aae915`
- Local HEAD before conservation: `4401d360c5cf714ee656e341282c97f725aae915`
- origin/main before conservation: `4401d360c5cf714ee656e341282c97f725aae915`

## Evidence-derived anatomy

The inherited persistence representation was unversioned and contained exactly:

- experience_id
- created_at
- state

Recovery rejected unknown fields.

## Implemented physiology

- persistence schema version 1
- explicit schema_version on new serialization
- compatibility with the original unversioned representation
- legacy-to-current migration
- identity conservation across migration
- unsupported explicit versions rejected
- invalid version types rejected
- unknown fields remain rejected

## Regression reconciliation

The first RUN 054 execution passed 29/29 dedicated migration/persistence tests.

Complete Experience regression then found one inherited assertion expecting exactly the old three-field persistence envelope.

GitHub inspection established that the test's semantic purpose is separation of Core Experience serialization from protection state.

RUN 054A therefore advanced that assertion to admit schema_version while continuing to prohibit protection and protection_state.

## Governance result

migration: **IMPLEMENTED + DEMONSTRATED + CONSERVED**

PCC-01: **IMPLEMENTED**

PCC-01 Production-Ready: **NOT YET DECLARED**

Remaining Production-Ready gaps:

- privacy
- operational observability
- performance
- deployment behavior

PCC-01 canonical status: **NOT CANON**

## Final implementation diff

```diff
diff --git a/lib/python/experience/persistence.py b/lib/python/experience/persistence.py
index 095571f..93345b8 100644
--- a/lib/python/experience/persistence.py
+++ b/lib/python/experience/persistence.py
@@ -32,8 +32,19 @@ class ExperienceRecoveryError(ExperiencePersistenceError):
     """Raised when persisted Experience data cannot be recovered safely."""


+CURRENT_SCHEMA_VERSION = 1
+
+_LEGACY_FIELDS = frozenset(
+    {
+        "experience_id",
+        "created_at",
+        "state",
+    }
+)
+
 _REQUIRED_FIELDS = frozenset(
     {
+        "schema_version",
         "experience_id",
         "created_at",
         "state",
@@ -50,14 +61,22 @@ def serialize_experience(experience: Experience) -> dict[str, str]:
         )

     return {
+        "schema_version": CURRENT_SCHEMA_VERSION,
         "experience_id": str(experience.experience_id),
         "created_at": experience.created_at.isoformat(),
         "state": experience.state.value,
     }


-def recover_experience(data: Mapping[str, Any]) -> Experience:
-    """Recover one existing Experience without regenerating identity."""
+def migrate_experience_representation(
+    data: Mapping[str, Any],
+) -> dict[str, Any]:
+    """Normalize a supported persisted Experience representation.
+
+    The original unversioned representation is schema version 0.
+    Migration adds only persistence metadata. It must not generate,
+    replace, or reinterpret Experience identity.
+    """

     if not isinstance(data, Mapping):
         raise ExperienceRecoveryError(
@@ -66,6 +85,11 @@ def recover_experience(data: Mapping[str, Any]) -> Experience:

     fields = frozenset(data.keys())

+    if fields == _LEGACY_FIELDS:
+        migrated = dict(data)
+        migrated["schema_version"] = CURRENT_SCHEMA_VERSION
+        return migrated
+
     if fields != _REQUIRED_FIELDS:
         missing = sorted(_REQUIRED_FIELDS - fields)
         unexpected = sorted(fields - _REQUIRED_FIELDS)
@@ -75,9 +99,33 @@ def recover_experience(data: Mapping[str, Any]) -> Experience:
             f"missing={missing}, unexpected={unexpected}"
         )

-    experience_id_raw = data["experience_id"]
-    created_at_raw = data["created_at"]
-    state_raw = data["state"]
+    schema_version = data["schema_version"]
+
+    if (
+        isinstance(schema_version, bool)
+        or not isinstance(schema_version, int)
+    ):
+        raise ExperienceRecoveryError(
+            "persisted schema_version must be an integer"
+        )
+
+    if schema_version != CURRENT_SCHEMA_VERSION:
+        raise ExperienceRecoveryError(
+            "unsupported persisted Experience schema_version: "
+            f"{schema_version}"
+        )
+
+    return dict(data)
+
+
+def recover_experience(data: Mapping[str, Any]) -> Experience:
+    """Recover one existing Experience without regenerating identity."""
+
+    migrated = migrate_experience_representation(data)
+
+    experience_id_raw = migrated["experience_id"]
+    created_at_raw = migrated["created_at"]
+    state_raw = migrated["state"]

     if not isinstance(experience_id_raw, str):
         raise ExperienceRecoveryError(
diff --git a/tests/experience/test_experience_persistence.py b/tests/experience/test_experience_persistence.py
index d6a4d02..f4d4bf1 100644
--- a/tests/experience/test_experience_persistence.py
+++ b/tests/experience/test_experience_persistence.py
@@ -19,6 +19,7 @@ def test_experience_serialization_contains_only_core_fields():
     data = serialize_experience(experience)

     assert set(data) == {
+        "schema_version",
         "experience_id",
         "created_at",
         "state",
diff --git a/tests/experience/test_experience_protection_repository.py b/tests/experience/test_experience_protection_repository.py
index af092c8..1fb84dd 100644
--- a/tests/experience/test_experience_protection_repository.py
+++ b/tests/experience/test_experience_protection_repository.py
@@ -181,6 +181,7 @@ def test_core_experience_serialization_remains_independent(tmp_path):
     representation = serialize_experience(experience)

     assert set(representation) == {
+        "schema_version",
         "experience_id",
         "created_at",
         "state",
```

## RUN 054A Bash executed — complete

```bash
#!/data/data/com.termux/files/usr/bin/bash
set -uo pipefail

cd "$HOME/storage/shared/AI-Projects/AI-Toolkit" || exit 1

export GIT_PAGER=cat
export GH_PAGER=cat
export PAGER=cat
export PYTHONPATH="$PWD:$PWD/lib${PYTHONPATH:+:$PYTHONPATH}"

BASE="4401d360c5cf714ee656e341282c97f725aae915"

PERSISTENCE="lib/python/experience/persistence.py"
PRIMARY_TEST="tests/experience/test_experience_persistence.py"
MIGRATION_TEST="tests/experience/test_experience_persistence_migration.py"
PROTECTION_TEST="tests/experience/test_experience_protection_repository.py"
REPORT="work/implementation-reports/PCC-01/PCC-01_RUN054_PERSISTENCE_MIGRATION_IMPLEMENTATION.md"

SELF="$PREFIX/tmp/pcc01_run054a.sh"
OUT="$PREFIX/tmp/pcc01_run054a.output"

: > "$OUT"
exec > >(tee -a "$OUT") 2>&1

fail() {
    code="${1:-1}"

    echo
    echo "=========================================================="
    echo "RUN 054A STOPPED SAFELY"
    echo "=========================================================="
    echo "Exit code: $code"
    echo "NO commit/push after failure"
    echo "=========================================================="

    exit "$code"
}

echo "=========================================================="
echo "PCC-01 — RUN 054A"
echo "MIGRATION REGRESSION RECONCILIATION"
echo "GIT-EVIDENCE-DERIVED"
echo "=========================================================="

echo
echo "[1/7] Verify Git authority and preserved RUN 054 mutation"

git fetch origin main --quiet || fail $?

LOCAL="$(git rev-parse HEAD)"
REMOTE="$(git rev-parse origin/main)"

echo "Expected:    $BASE"
echo "LOCAL:       $LOCAL"
echo "origin/main: $REMOTE"

[ "$LOCAL" = "$BASE" ] || fail 1
[ "$REMOTE" = "$BASE" ] || fail 1

EXPECTED_PRE="$PREFIX/tmp/pcc01_run054a.expected_pre"
ACTUAL_PRE="$PREFIX/tmp/pcc01_run054a.actual_pre"

cat > "$EXPECTED_PRE" <<EOF
$PERSISTENCE
$PRIMARY_TEST
$MIGRATION_TEST
EOF

{
    git diff --name-only
    git ls-files --others --exclude-standard -- "$MIGRATION_TEST"
} | sort -u > "$ACTUAL_PRE"

sort -o "$EXPECTED_PRE" "$EXPECTED_PRE"

if ! diff -u "$EXPECTED_PRE" "$ACTUAL_PRE"; then
    echo "ERROR: local state differs from failed RUN 054 boundary"
    fail 1
fi

echo "PASS: failed RUN 054 implementation preserved exactly"

echo
echo "[2/7] Verify causal GitHub evidence"

python - "$PROTECTION_TEST" <<'PY'
from pathlib import Path
import sys

path = Path(sys.argv[1])
text = path.read_text(encoding="utf-8")

needle = '''def test_core_experience_serialization_remains_independent(tmp_path):
    from lib.python.experience.model import Experience
    from lib.python.experience.persistence import serialize_experience

    experience = Experience.create()

    representation = serialize_experience(experience)

    assert set(representation) == {
        "experience_id",
        "created_at",
        "state",
    }

    assert "protection" not in representation
    assert "protection_state" not in representation
'''

if needle not in text:
    raise SystemExit(
        "ERROR: exact GitHub-confirmed protection independence test changed"
    )

print("PASS: failing regression anatomy reproduced exactly")
print("PASS: test protects separation from protection/protection_state")
print("PASS: schema_version does not couple protection into Core Experience")
PY

[ $? -eq 0 ] || fail $?

echo
echo "[3/7] Reconcile inherited independence assertion"

python - "$PROTECTION_TEST" <<'PY'
from pathlib import Path
import sys

path = Path(sys.argv[1])
text = path.read_text(encoding="utf-8")

old = '''    assert set(representation) == {
        "experience_id",
        "created_at",
        "state",
    }

    assert "protection" not in representation
    assert "protection_state" not in representation
'''

new = '''    assert set(representation) == {
        "schema_version",
        "experience_id",
        "created_at",
        "state",
    }

    assert "protection" not in representation
    assert "protection_state" not in representation
'''

if text.count(old) != 1:
    raise SystemExit(
        "ERROR: exact inherited independence assertion not found once"
    )

text = text.replace(old, new, 1)
path.write_text(text, encoding="utf-8")

print("PASS: persistence metadata admitted")
print("PASS: protection remains excluded")
print("PASS: protection_state remains excluded")
PY

python -m py_compile "$PROTECTION_TEST" || fail $?

echo
echo "[4/7] Execute causal regression then complete Experience regression"

python -m pytest -q \
    "$PROTECTION_TEST" || fail $?

echo "PASS: protection independence regression"

echo
echo "PRESERVED FROM RUN 054:"
echo "29/29 dedicated migration + persistence tests PASS"
echo "Those successful tests are not unnecessarily repeated."

python -m pytest -q tests/experience || fail $?

echo "PASS: complete Experience regression"

echo
echo "[5/7] Verify exact final implementation boundary"

EXPECTED="$PREFIX/tmp/pcc01_run054a.expected"
ACTUAL="$PREFIX/tmp/pcc01_run054a.actual"

cat > "$EXPECTED" <<EOF
$PERSISTENCE
$PRIMARY_TEST
$PROTECTION_TEST
$MIGRATION_TEST
EOF

{
    git diff --name-only
    git ls-files --others --exclude-standard -- "$MIGRATION_TEST"
} | sort -u > "$ACTUAL"

sort -o "$EXPECTED" "$EXPECTED"

if ! diff -u "$EXPECTED" "$ACTUAL"; then
    echo "ERROR: mutation outside migration boundary"
    fail 1
fi

echo "PASS: exact mutation boundary"

echo
echo "[6/7] Generate autosufficient epic-thread"

mkdir -p "$(dirname "$REPORT")"

{
    echo "# PCC-01 — RUN 054 — Persistence Migration Implementation"
    echo
    echo "## Purpose"
    echo
    echo "Resolve the PCC-01 Production-Ready migration gap identified by RUN 052."
    echo
    echo "## Git authority"
    echo
    echo "- Baseline: \`$BASE\`"
    echo "- Local HEAD before conservation: \`$LOCAL\`"
    echo "- origin/main before conservation: \`$REMOTE\`"
    echo
    echo "## Evidence-derived anatomy"
    echo
    echo "The inherited persistence representation was unversioned and contained exactly:"
    echo
    echo "- experience_id"
    echo "- created_at"
    echo "- state"
    echo
    echo "Recovery rejected unknown fields."
    echo
    echo "## Implemented physiology"
    echo
    echo "- persistence schema version 1"
    echo "- explicit schema_version on new serialization"
    echo "- compatibility with the original unversioned representation"
    echo "- legacy-to-current migration"
    echo "- identity conservation across migration"
    echo "- unsupported explicit versions rejected"
    echo "- invalid version types rejected"
    echo "- unknown fields remain rejected"
    echo
    echo "## Regression reconciliation"
    echo
    echo "The first RUN 054 execution passed 29/29 dedicated migration/persistence tests."
    echo
    echo "Complete Experience regression then found one inherited assertion expecting exactly the old three-field persistence envelope."
    echo
    echo "GitHub inspection established that the test's semantic purpose is separation of Core Experience serialization from protection state."
    echo
    echo "RUN 054A therefore advanced that assertion to admit schema_version while continuing to prohibit protection and protection_state."
    echo
    echo "## Governance result"
    echo
    echo "migration: **IMPLEMENTED + DEMONSTRATED + CONSERVED**"
    echo
    echo "PCC-01: **IMPLEMENTED**"
    echo
    echo "PCC-01 Production-Ready: **NOT YET DECLARED**"
    echo
    echo "Remaining Production-Ready gaps:"
    echo
    echo "- privacy"
    echo "- operational observability"
    echo "- performance"
    echo "- deployment behavior"
    echo
    echo "PCC-01 canonical status: **NOT CANON**"
    echo
    echo "## Final implementation diff"
    echo
    echo '```diff'
    git diff -- \
        "$PERSISTENCE" \
        "$PRIMARY_TEST" \
        "$PROTECTION_TEST" \
        "$MIGRATION_TEST"
    echo '```'
    echo
    echo "## RUN 054A Bash executed — complete"
    echo
    echo '```bash'
    cat "$SELF"
    echo '```'
    echo
    echo "## RUN 054A terminal output — complete"
    echo
    echo '```text'
    cat "$OUT"
    echo '```'
} > "$REPORT"

[ -s "$REPORT" ] || fail 1

echo "PASS: epic-thread generated"
sha256sum "$REPORT"

echo
echo "[7/7] Conserve implementation and evidence in GitHub"

git add -- \
    "$PERSISTENCE" \
    "$PRIMARY_TEST" \
    "$PROTECTION_TEST" \
    "$MIGRATION_TEST" \
    "$REPORT" || fail $?

EXPECTED_STAGED="$PREFIX/tmp/pcc01_run054a.expected_staged"

{
    cat "$EXPECTED"
    echo "$REPORT"
} | sort > "$EXPECTED_STAGED"

git diff --cached --name-only | sort > \
    "$PREFIX/tmp/pcc01_run054a.actual_staged"

if ! diff -u \
    "$EXPECTED_STAGED" \
    "$PREFIX/tmp/pcc01_run054a.actual_staged"
then
    echo "ERROR: staging boundary violated"
    git reset --quiet
    fail 1
fi

git diff --cached --check || {
    echo "ERROR: staged integrity failure"
    git reset --quiet
    fail 1
}

git commit -m \
    "feat: add PCC-01 persistence migration" || fail $?

FINAL_HEAD="$(git rev-parse HEAD)"

git push origin main || fail $?
git fetch origin main --quiet || fail $?

FINAL_REMOTE="$(git rev-parse origin/main)"

[ "$FINAL_HEAD" = "$FINAL_REMOTE" ] || fail 1

echo
echo "=========================================================="
echo "RUN 054 COMPLETE"
echo "=========================================================="
echo
echo "FINAL HEAD:"
echo "$FINAL_HEAD"
echo
echo "LOCAL == origin/main:"
echo "PASS"
echo
echo "MIGRATION:"
echo "IMPLEMENTED + DEMONSTRATED + CONSERVED"
echo
echo "REMAINING PRODUCTION CONCERNS:"
echo "4"
echo
echo "privacy"
echo "operational observability"
echo "performance"
echo "deployment behavior"
echo
echo "PCC-01:"
echo "IMPLEMENTED"
echo
echo "PCC-01 PRODUCTION-READY:"
echo "NOT YET DECLARED"
echo
echo "PCC-01 CANONICAL STATUS:"
echo "NOT CANON"
echo
echo "EPIC-THREAD MD:"
echo "$REPORT"
echo
echo "NEXT:"
echo "GPT verifies RUN 054 directly in GitHub before RUN 055."
echo "=========================================================="
```

## RUN 054A terminal output — complete

```text
==========================================================
PCC-01 — RUN 054A
MIGRATION REGRESSION RECONCILIATION
GIT-EVIDENCE-DERIVED
==========================================================

[1/7] Verify Git authority and preserved RUN 054 mutation
Expected:    4401d360c5cf714ee656e341282c97f725aae915
LOCAL:       4401d360c5cf714ee656e341282c97f725aae915
origin/main: 4401d360c5cf714ee656e341282c97f725aae915
PASS: failed RUN 054 implementation preserved exactly

[2/7] Verify causal GitHub evidence
PASS: failing regression anatomy reproduced exactly
PASS: test protects separation from protection/protection_state
PASS: schema_version does not couple protection into Core Experience

[3/7] Reconcile inherited independence assertion
PASS: persistence metadata admitted
PASS: protection remains excluded
PASS: protection_state remains excluded

[4/7] Execute causal regression then complete Experience regression
...........                                                              [100%]
11 passed in 0.55s
PASS: protection independence regression

PRESERVED FROM RUN 054:
29/29 dedicated migration + persistence tests PASS
Those successful tests are not unnecessarily repeated.
........................................................................ [ 34%]
........................................................................ [ 68%]
.................................................................        [100%]
209 passed in 3.50s
PASS: complete Experience regression

[5/7] Verify exact final implementation boundary
PASS: exact mutation boundary

[6/7] Generate autosufficient epic-thread
```

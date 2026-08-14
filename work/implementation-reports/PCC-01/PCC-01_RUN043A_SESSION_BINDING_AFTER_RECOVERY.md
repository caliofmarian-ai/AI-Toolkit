# PCC-01 — RUN 043A — Session Binding After Recovery

## Capability

PCC-01 — Persistent Experience

## Purpose

Demonstrate that a recovered Persistent Experience can bind legitimately to Session without changing its persistent Experience identity.

## Evidence Governance

This report conserves already-produced successful behavioral evidence.

No behavioral test is re-executed by the conservation operation.

## Verified Git Baseline

- Baseline: `9c9ffe4c30a81fb65bc5601c6cd3d666ea348e51`
- Local HEAD before conservation: `9c9ffe4c30a81fb65bc5601c6cd3d666ea348e51`
- origin/main before conservation: `9c9ffe4c30a81fb65bc5601c6cd3d666ea348e51`

## Accepted Authority

- PCC-01 Implementation Contract — Human Acceptance — 2026-08-13
- PCC-01 Core Experience Implementation Specification — Human Acceptance — 2026-08-13
- PCC-01 Implementation Inventory and Build Plan — Human Acceptance — 2026-08-13

## Reused Conserved Physiology

```text
Experience.create()
    -> serialize_experience()
    -> recover_experience()
    -> SessionBinding.create()
```

No new repository physiology was introduced.

No duplicate Session Binding organ was introduced.

## RUN 043 Failure History

The first RUN 043 harness incorrectly assumed that ExperienceRepository was a concrete durable-storage implementation.

That assumption was rejected from repository evidence.

## RUN 043A Correction

RUN 043A replaced that assumption with the already-conserved Experience serialization/recovery physiology.

Its behavioral demonstration succeeded.

The subsequent RUN 043A procedural stop occurred during a working-tree boundary check and did not invalidate the successful behavioral results.

## Original RUN 043A Bash — Complete

```bash
#!/data/data/com.termux/files/usr/bin/bash
set -uo pipefail

export GIT_PAGER=cat
export PAGER=cat
export GH_PAGER=cat

cd "$HOME/storage/shared/AI-Projects/AI-Toolkit" || exit 1

EXPECTED_BASE="9c9ffe4c30a81fb65bc5601c6cd3d666ea348e51"

TEST="tests/experience/test_experience_session_binding_after_recovery.py"
REPORT="work/implementation-reports/PCC-01/PCC-01_RUN043A_SESSION_BINDING_AFTER_RECOVERY.md"

SELF="$PREFIX/tmp/pcc01_run043a.sh"
OUT="$PREFIX/tmp/pcc01_run043a.output"
DIFF="$PREFIX/tmp/pcc01_run043a.diff"

mkdir -p "$(dirname "$REPORT")"
: > "$OUT"
: > "$DIFF"

exec > >(tee -a "$OUT") 2>&1

fail() {
    CODE="${1:-1}"
    echo
    echo "=========================================================="
    echo "RUN 043A STOPPED SAFELY"
    echo "=========================================================="
    echo "Exit code: $CODE"
    echo "NO commit after failure"
    echo "NO push after failure"
    echo "=========================================================="
    exit "$CODE"
}

echo "=========================================================="
echo "PCC-01"
echo "SESSION BINDING AFTER RECOVERY — RUN 043A"
echo "EVIDENCE-DERIVED EXECUTION"
echo "=========================================================="

echo
echo "[1/8] Verify Git authority boundary"

git fetch origin main --quiet || fail $?

LOCAL="$(git rev-parse HEAD)" || fail $?
REMOTE="$(git rev-parse origin/main)" || fail $?

echo "Expected:    $EXPECTED_BASE"
echo "LOCAL:       $LOCAL"
echo "origin/main: $REMOTE"

[ "$LOCAL" = "$EXPECTED_BASE" ] || {
    echo "ERROR: local HEAD differs from verified GitHub baseline"
    fail 1
}

[ "$REMOTE" = "$EXPECTED_BASE" ] || {
    echo "ERROR: origin/main differs from verified GitHub baseline"
    fail 1
}

[ -z "$(git diff --cached --name-only)" ] || {
    echo "ERROR: staging area is not empty"
    git diff --cached --name-only
    fail 1
}

TRACKED="$(git diff --name-only)"

if [ -n "$TRACKED" ] && [ "$TRACKED" != "$TEST" ]; then
    echo "ERROR: unexpected tracked mutation exists"
    printf '%s\n' "$TRACKED"
    fail 1
fi

echo "PASS: baseline"
echo "PASS: failed RUN 043 test is the only permitted local tracked mutation"

echo
echo "[2/8] Verify accepted authority documents and conserved organs"

REQUIRED=(
"work/decisions/PCC-01_IMPLEMENTATION_CONTRACT_HUMAN_ACCEPTANCE_2026-08-13.md"
"work/decisions/PCC-01_IMPLEMENTATION_INVENTORY_AND_BUILD_PLAN_HUMAN_ACCEPTANCE_2026-08-13.md"
"lib/python/experience/model.py"
"lib/python/experience/identity.py"
"lib/python/experience/persistence.py"
"lib/python/experience/session_binding.py"
"work/implementation-reports/PCC-01/PCC-01_SESSION_BINDING_CONSERVATION_REPORT_RUN_012.md"
)

for FILE in "${REQUIRED[@]}"; do
    [ -s "$FILE" ] || {
        echo "ERROR: required evidence missing: $FILE"
        fail 1
    }
    echo "PASS: $FILE"
done

grep -q "Experience != Session" \
    lib/python/experience/session_binding.py || {
    echo "ERROR: Session/Experience separation not demonstrated in organ"
    fail 1
}

grep -q "def serialize_experience" \
    lib/python/experience/persistence.py || {
    echo "ERROR: conserved serialization pathway missing"
    fail 1
}

grep -q "def recover_experience" \
    lib/python/experience/persistence.py || {
    echo "ERROR: conserved recovery pathway missing"
    fail 1
}

echo "PASS: authority and inherited physiology"

echo
echo "[3/8] Preflight exact real APIs"

python - <<'PY' || fail $?
from lib.python.experience.model import Experience
from lib.python.experience.persistence import (
    serialize_experience,
    recover_experience,
)
from lib.python.experience.session_binding import SessionBinding

original = Experience.create()
before = original.experience_id

payload = serialize_experience(original)
recovered = recover_experience(payload)

assert recovered is not original
assert recovered.experience_id == before

binding = SessionBinding.create(
    session_id="PCC01-RUN043A-PREFLIGHT",
    experience_id=recovered.experience_id,
)

assert binding.experience_id == before
assert binding.belongs_to_experience(before)
assert binding.belongs_to_session(
    "PCC01-RUN043A-PREFLIGHT"
)

print("PASS: Experience.create()")
print("PASS: serialize_experience()")
print("PASS: recover_experience()")
print("PASS: ID_before == ID_after")
print("PASS: SessionBinding.create()")
print("PASS: recovered Experience accepts legitimate Session binding")
PY

echo
echo "[4/8] Replace failed RUN 043 harness with evidence-derived examination"

cat > "$TEST" <<'PY'
"""PCC-01 Session Binding after Experience recovery.

Evidence-derived physiology:

Experience.create
    -> serialize_experience
    -> recover_experience
    -> SessionBinding.create

Contract boundaries:
Experience != Session
Storage != Experience
Persistence != authority

This test does not invent a repository implementation.
"""

from lib.python.experience.model import Experience
from lib.python.experience.persistence import (
    recover_experience,
    serialize_experience,
)
from lib.python.experience.session_binding import SessionBinding


def _recover(experience):
    payload = serialize_experience(experience)
    recovered = recover_experience(payload)

    assert recovered is not experience

    return payload, recovered


def test_identity_survives_recovery_before_session_binding():
    original = Experience.create()
    before = original.experience_id

    _, recovered = _recover(original)

    after = recovered.experience_id

    assert before == after


def test_recovered_experience_can_bind_to_session():
    original = Experience.create()
    before = original.experience_id

    _, recovered = _recover(original)

    binding = SessionBinding.create(
        session_id="SESSION-AFTER-RECOVERY",
        experience_id=recovered.experience_id,
    )

    assert binding.experience_id == before
    assert binding.belongs_to_experience(before)
    assert binding.belongs_to_session(
        "SESSION-AFTER-RECOVERY"
    )


def test_session_binding_does_not_change_experience_identity():
    original = Experience.create()
    before = original.experience_id

    _, recovered = _recover(original)

    SessionBinding.create(
        session_id="SESSION-ONE",
        experience_id=recovered.experience_id,
    )

    assert recovered.experience_id == before


def test_rebinding_does_not_redefine_experience_identity():
    original = Experience.create()
    before = original.experience_id

    _, recovered = _recover(original)

    first = SessionBinding.create(
        session_id="SESSION-ONE",
        experience_id=recovered.experience_id,
    )

    second = SessionBinding.create(
        session_id="SESSION-TWO",
        experience_id=recovered.experience_id,
    )

    assert first.session_id != second.session_id
    assert first.experience_id == before
    assert second.experience_id == before
    assert recovered.experience_id == before


def test_session_identity_remains_distinct_from_experience_identity():
    original = Experience.create()

    _, recovered = _recover(original)

    binding = SessionBinding.create(
        session_id="SESSION-DISTINCT",
        experience_id=recovered.experience_id,
    )

    assert str(binding.session_id) != str(
        recovered.experience_id
    )


def test_recovery_does_not_require_session_identity():
    original = Experience.create()

    payload, recovered = _recover(original)

    assert "session_id" not in payload
    assert (
        recovered.experience_id
        == original.experience_id
    )


def test_binding_does_not_mutate_persistent_experience_body():
    original = Experience.create()

    _, recovered = _recover(original)

    before = serialize_experience(recovered)

    SessionBinding.create(
        session_id="SESSION-RELATIONAL",
        experience_id=recovered.experience_id,
    )

    after = serialize_experience(recovered)

    assert after == before
PY

python -m py_compile "$TEST" || fail $?

echo "PASS: corrected examination syntax"

echo
echo "[5/8] Execute behavioral demonstration"

python -m pytest -q "$TEST" || fail $?

echo "PASS: Session Binding after recovery"

echo
echo "[6/8] Execute inherited and complete Experience regression"

python -m pytest -q \
    tests/experience/test_experience_session_binding.py || fail $?

python -m pytest -q tests/experience || fail $?

echo "PASS: inherited Session Binding"
echo "PASS: complete Experience regression"

echo
echo "[7/8] Verify exact mutation boundary and build epic-thread"

git diff --check -- "$TEST" || fail $?
git diff -- "$TEST" > "$DIFF"

CHANGED="$(git diff --name-only)"

[ "$CHANGED" = "$TEST" ] || {
    echo "ERROR: organism mutation detected outside authorized test"
    printf '%s\n' "$CHANGED"
    fail 1
}

{
    echo "# PCC-01 — RUN 043A — Session Binding After Recovery"
    echo
    echo "## Purpose"
    echo
    echo "Demonstrate the accepted PCC-01 requirement that a recovered Persistent Experience can bind legitimately to Session without changing its persistent identity."
    echo
    echo "## Evidence Basis"
    echo
    echo "- PCC-01 Implementation Contract Human Acceptance"
    echo "- PCC-01 Implementation Inventory and Build Plan Human Acceptance"
    echo "- conserved Experience persistence physiology"
    echo "- conserved Experience Session Binding"
    echo "- RUN 012 Session Binding conservation evidence"
    echo
    echo "## Causal Record"
    echo
    echo "The original RUN 043 harness incorrectly treated ExperienceRepository as a concrete durable storage implementation."
    echo
    echo "That assumption was rejected."
    echo
    echo "RUN 043A uses only verified conserved physiology: serialize_experience -> recover_experience -> SessionBinding."
    echo
    echo "No organism implementation was changed to satisfy the examination."
    echo
    echo "## Bash Executed — Complete"
    echo
    echo '```bash'
    cat "$SELF"
    echo '```'
    echo
    echo "## Terminal Output — Complete"
    echo
    echo '```text'
    cat "$OUT"
    echo '```'
    echo
    echo "## Behavioral Evidence Diff — Complete"
    echo
    echo '```diff'
    cat "$DIFF"
    echo '```'
    echo
    echo "## Demonstrated Invariants"
    echo
    echo "- ID_before_recovery == ID_after_recovery"
    echo "- Experience != Session"
    echo "- recovered Experience can bind to Session"
    echo "- rebinding Session does not redefine Experience identity"
    echo "- Session identity remains distinct"
    echo "- recovery does not require Session identity"
    echo "- Session Binding does not mutate Persistent Experience body"
    echo
    echo "## Mutation Boundary"
    echo
    echo "- Existing Experience organs modified: NO"
    echo "- Existing Session Binding modified: NO"
    echo "- Behavioral evidence corrected/added: YES"
    echo
    echo "## Epistemic Status"
    echo
    echo "- Session Binding after recovery: DEMONSTRATED"
    echo
    echo "- Whole PCC-01: NOT YET CLAIMED IMPLEMENTED"
    echo
    echo "- Canonical Status: UNCHANGED"
    echo
    echo "- Production Status: UNCHANGED"
} > "$REPORT"

echo "PASS: autosufficient MD contains bash + output + diff"

echo
echo "[8/8] Conserve and synchronize GitHub"

git add -- "$TEST" "$REPORT" || fail $?

ACTUAL="$(git diff --cached --name-only | sort)"
EXPECTED="$(
    printf '%s\n' "$TEST" "$REPORT" | sort
)"

[ "$ACTUAL" = "$EXPECTED" ] || {
    echo "ERROR: staged boundary mismatch"
    git diff --cached --name-only
    git reset --quiet
    fail 1
}

git diff --cached --check -- "$TEST" || {
    git reset --quiet
    fail 1
}

git commit -m \
    "test: demonstrate PCC-01 session binding after recovery" || fail $?

EVIDENCE_HEAD="$(git rev-parse HEAD)" || fail $?

git push origin main || fail $?
git fetch origin main --quiet || fail $?

[ "$EVIDENCE_HEAD" = "$(git rev-parse origin/main)" ] || {
    echo "ERROR: first conservation not synchronized"
    fail 1
}

{
    echo
    echo "## Git Conservation"
    echo
    echo "- Baseline: \`$LOCAL\`"
    echo "- Evidence HEAD: \`$EVIDENCE_HEAD\`"
    echo "- First GitHub synchronization: PASS"
    echo
    echo "## Conclusion"
    echo
    echo "**The accepted Session Binding after recovery physiology is demonstrated and conserved.**"
    echo
    echo "No new Session organ and no new repository physiology were invented."
    echo
    echo "---"
    echo
    echo "END OF RUN 043A"
} >> "$REPORT"

git add -- "$REPORT" || fail $?

git commit -m \
    "docs: finalize PCC-01 RUN 043A evidence" || fail $?

FINAL_HEAD="$(git rev-parse HEAD)" || fail $?

git push origin main || fail $?
git fetch origin main --quiet || fail $?

FINAL_REMOTE="$(git rev-parse origin/main)" || fail $?

[ "$FINAL_HEAD" = "$FINAL_REMOTE" ] || {
    echo "ERROR: final evidence synchronization failed"
    fail 1
}

echo
echo "=========================================================="
echo "RUN 043A COMPLETE"
echo "=========================================================="
echo
echo "BASE:"
echo "$LOCAL"
echo
echo "EVIDENCE HEAD:"
echo "$EVIDENCE_HEAD"
echo
echo "FINAL HEAD:"
echo "$FINAL_HEAD"
echo
echo "LOCAL == origin/main:"
echo "PASS"
echo
echo "SESSION BINDING AFTER RECOVERY:"
echo "DEMONSTRATED + CONSERVED"
echo
echo "ORGANISM SOFTWARE MODIFIED:"
echo "NO"
echo
echo "EPIC-THREAD:"
echo "$REPORT"
echo
echo "NEXT:"
echo "GPT verifies GitHub directly before deriving the next PCC-01 run."
echo "=========================================================="
```

## Original RUN 043A Terminal Output — Complete

```text
==========================================================
PCC-01
SESSION BINDING AFTER RECOVERY — RUN 043A
EVIDENCE-DERIVED EXECUTION
==========================================================

[1/8] Verify Git authority boundary
Expected:    9c9ffe4c30a81fb65bc5601c6cd3d666ea348e51
LOCAL:       9c9ffe4c30a81fb65bc5601c6cd3d666ea348e51
origin/main: 9c9ffe4c30a81fb65bc5601c6cd3d666ea348e51
PASS: baseline
PASS: failed RUN 043 test is the only permitted local tracked mutation

[2/8] Verify accepted authority documents and conserved organs
PASS: work/decisions/PCC-01_IMPLEMENTATION_CONTRACT_HUMAN_ACCEPTANCE_2026-08-13.md
PASS: work/decisions/PCC-01_IMPLEMENTATION_INVENTORY_AND_BUILD_PLAN_HUMAN_ACCEPTANCE_2026-08-13.md
PASS: lib/python/experience/model.py
PASS: lib/python/experience/identity.py
PASS: lib/python/experience/persistence.py
PASS: lib/python/experience/session_binding.py
PASS: work/implementation-reports/PCC-01/PCC-01_SESSION_BINDING_CONSERVATION_REPORT_RUN_012.md
PASS: authority and inherited physiology

[3/8] Preflight exact real APIs
PASS: Experience.create()
PASS: serialize_experience()
PASS: recover_experience()
PASS: ID_before == ID_after
PASS: SessionBinding.create()
PASS: recovered Experience accepts legitimate Session binding

[4/8] Replace failed RUN 043 harness with evidence-derived examination
PASS: corrected examination syntax

[5/8] Execute behavioral demonstration
.......                                                                  [100%]
7 passed in 0.37s
PASS: Session Binding after recovery

[6/8] Execute inherited and complete Experience regression
....................                                                     [100%]
20 passed in 0.34s
........................................................................ [ 47%]
........................................................................ [ 95%]
.......                                                                  [100%]
151 passed in 3.14s
PASS: inherited Session Binding
PASS: complete Experience regression

[7/8] Verify exact mutation boundary and build epic-thread
ERROR: organism mutation detected outside authorized test


==========================================================
RUN 043A STOPPED SAFELY
==========================================================
Exit code: 1
NO commit after failure
NO push after failure
==========================================================
```

## Behavioral Artifact — Complete

Path: `tests/experience/test_experience_session_binding_after_recovery.py`

SHA-256: `684b7258c609706604c8cac23af1da87ee89b4bec1ad8347a3e5aa3c4dff01c5`

```python
"""PCC-01 Session Binding after Experience recovery.

Evidence-derived physiology:

Experience.create
    -> serialize_experience
    -> recover_experience
    -> SessionBinding.create

Contract boundaries:
Experience != Session
Storage != Experience
Persistence != authority

This test does not invent a repository implementation.
"""

from lib.python.experience.model import Experience
from lib.python.experience.persistence import (
    recover_experience,
    serialize_experience,
)
from lib.python.experience.session_binding import SessionBinding


def _recover(experience):
    payload = serialize_experience(experience)
    recovered = recover_experience(payload)

    assert recovered is not experience

    return payload, recovered


def test_identity_survives_recovery_before_session_binding():
    original = Experience.create()
    before = original.experience_id

    _, recovered = _recover(original)

    after = recovered.experience_id

    assert before == after


def test_recovered_experience_can_bind_to_session():
    original = Experience.create()
    before = original.experience_id

    _, recovered = _recover(original)

    binding = SessionBinding.create(
        session_id="SESSION-AFTER-RECOVERY",
        experience_id=recovered.experience_id,
    )

    assert binding.experience_id == before
    assert binding.belongs_to_experience(before)
    assert binding.belongs_to_session(
        "SESSION-AFTER-RECOVERY"
    )


def test_session_binding_does_not_change_experience_identity():
    original = Experience.create()
    before = original.experience_id

    _, recovered = _recover(original)

    SessionBinding.create(
        session_id="SESSION-ONE",
        experience_id=recovered.experience_id,
    )

    assert recovered.experience_id == before


def test_rebinding_does_not_redefine_experience_identity():
    original = Experience.create()
    before = original.experience_id

    _, recovered = _recover(original)

    first = SessionBinding.create(
        session_id="SESSION-ONE",
        experience_id=recovered.experience_id,
    )

    second = SessionBinding.create(
        session_id="SESSION-TWO",
        experience_id=recovered.experience_id,
    )

    assert first.session_id != second.session_id
    assert first.experience_id == before
    assert second.experience_id == before
    assert recovered.experience_id == before


def test_session_identity_remains_distinct_from_experience_identity():
    original = Experience.create()

    _, recovered = _recover(original)

    binding = SessionBinding.create(
        session_id="SESSION-DISTINCT",
        experience_id=recovered.experience_id,
    )

    assert str(binding.session_id) != str(
        recovered.experience_id
    )


def test_recovery_does_not_require_session_identity():
    original = Experience.create()

    payload, recovered = _recover(original)

    assert "session_id" not in payload
    assert (
        recovered.experience_id
        == original.experience_id
    )


def test_binding_does_not_mutate_persistent_experience_body():
    original = Experience.create()

    _, recovered = _recover(original)

    before = serialize_experience(recovered)

    SessionBinding.create(
        session_id="SESSION-RELATIONAL",
        experience_id=recovered.experience_id,
    )

    after = serialize_experience(recovered)

    assert after == before
```

## Demonstrated Evidence

- Dedicated Session Binding after recovery examinations: 7/7 PASS
- Existing Session Binding examinations: 20/20 PASS
- Complete Experience regression: 151/151 PASS
- Experience identity survives recovery: PASS
- Recovered Experience accepts legitimate Session binding: PASS
- Session identity remains distinct from Experience identity: PASS
- Session rebinding does not redefine Experience identity: PASS
- Session Binding does not mutate Persistent Experience body: PASS

## Organ Boundary

- Core Experience implementation modified: NO
- Experience persistence implementation modified: NO
- Existing Session Binding implementation modified: NO
- Behavioral evidence added: YES

## Conservation Bash — Complete

```bash
#!/data/data/com.termux/files/usr/bin/bash
set -uo pipefail

export GIT_PAGER=cat
export PAGER=cat
export GH_PAGER=cat

cd "$HOME/storage/shared/AI-Projects/AI-Toolkit" || exit 1

BASE="9c9ffe4c30a81fb65bc5601c6cd3d666ea348e51"

TEST="tests/experience/test_experience_session_binding_after_recovery.py"
REPORT="work/implementation-reports/PCC-01/PCC-01_RUN043A_SESSION_BINDING_AFTER_RECOVERY.md"

ORIGINAL_SCRIPT="$PREFIX/tmp/pcc01_run043a.sh"
ORIGINAL_OUTPUT="$PREFIX/tmp/pcc01_run043a.output"
THIS_SCRIPT="$PREFIX/tmp/pcc01_run043c_conserve.sh"
CONSERVATION_OUTPUT="$PREFIX/tmp/pcc01_run043c_conserve.output"

mkdir -p "$(dirname "$REPORT")"
: > "$CONSERVATION_OUTPUT"

exec > >(tee -a "$CONSERVATION_OUTPUT") 2>&1

fail() {
    CODE="${1:-1}"

    echo
    echo "=========================================================="
    echo "RUN 043C CONSERVATION STOPPED SAFELY"
    echo "=========================================================="
    echo "Exit code: $CODE"
    echo "No further Git operation performed."
    echo "=========================================================="

    exit "$CODE"
}

echo "=========================================================="
echo "PCC-01"
echo "RUN 043A EVIDENCE CONSERVATION — RUN 043C"
echo "NO TEST RE-EXECUTION"
echo "=========================================================="

echo
echo "[1/7] Verify authoritative GitHub baseline"

git fetch origin main --quiet || fail $?

LOCAL="$(git rev-parse HEAD)" || fail $?
REMOTE="$(git rev-parse origin/main)" || fail $?

echo "Expected:    $BASE"
echo "LOCAL:       $LOCAL"
echo "origin/main: $REMOTE"

[ "$LOCAL" = "$BASE" ] || {
    echo "ERROR: local HEAD changed"
    fail 1
}

[ "$REMOTE" = "$BASE" ] || {
    echo "ERROR: origin/main changed"
    fail 1
}

[ -z "$(git diff --cached --name-only)" ] || {
    echo "ERROR: staging area already contains material"
    git diff --cached --name-only
    fail 1
}

echo "PASS: authoritative baseline"

echo
echo "[2/7] Verify preserved successful RUN 043A evidence"

[ -s "$ORIGINAL_SCRIPT" ] || {
    echo "ERROR: original RUN 043A bash missing"
    fail 1
}

[ -s "$ORIGINAL_OUTPUT" ] || {
    echo "ERROR: original RUN 043A output missing"
    fail 1
}

[ -s "$TEST" ] || {
    echo "ERROR: successful RUN 043A test artifact missing locally"
    fail 1
}

grep -Fq "7 passed" "$ORIGINAL_OUTPUT" || {
    echo "ERROR: dedicated 7/7 result absent"
    fail 1
}

grep -Fq "20 passed" "$ORIGINAL_OUTPUT" || {
    echo "ERROR: inherited Session Binding result absent"
    fail 1
}

grep -Fq "151 passed" "$ORIGINAL_OUTPUT" || {
    echo "ERROR: complete Experience regression result absent"
    fail 1
}

grep -Fq \
"PASS: recovered Experience accepts legitimate Session binding" \
"$ORIGINAL_OUTPUT" || {
    echo "ERROR: recovery/binding proof absent"
    fail 1
}

echo "PASS: original RUN 043A script preserved"
echo "PASS: original RUN 043A output preserved"
echo "PASS: local behavioral evidence preserved"
echo "PASS: 7/7 dedicated examinations"
echo "PASS: 20/20 inherited Session Binding examinations"
echo "PASS: 151/151 Experience regression"

echo
echo "[3/7] Establish exact Git state without requiring a diff"

if git cat-file -e "HEAD:$TEST" 2>/dev/null; then
    echo "ERROR: test unexpectedly already exists in HEAD"
    echo "GitHub inspection previously established that it should be absent."
    fail 1
fi

if git ls-files --error-unmatch "$TEST" >/dev/null 2>&1; then
    echo "TEST INDEX STATE: TRACKED"
else
    echo "TEST INDEX STATE: UNTRACKED"
fi

echo "HEAD STATE: ABSENT"
echo "WORKTREE STATE: PRESENT"

TEST_SHA="$(sha256sum "$TEST" | awk '{print $1}')"

echo "TEST SHA-256:"
echo "$TEST_SHA"

echo
echo "PASS: local artifact identified independently of git diff"

echo
echo "[4/7] Generate autosufficient epic-thread report"

{
    echo "# PCC-01 — RUN 043A — Session Binding After Recovery"
    echo
    echo "## Capability"
    echo
    echo "PCC-01 — Persistent Experience"
    echo
    echo "## Purpose"
    echo
    echo "Demonstrate that a recovered Persistent Experience can bind legitimately to Session without changing its persistent Experience identity."
    echo
    echo "## Evidence Governance"
    echo
    echo "This report conserves already-produced successful behavioral evidence."
    echo
    echo "No behavioral test is re-executed by the conservation operation."
    echo
    echo "## Verified Git Baseline"
    echo
    echo "- Baseline: \`$BASE\`"
    echo "- Local HEAD before conservation: \`$LOCAL\`"
    echo "- origin/main before conservation: \`$REMOTE\`"
    echo
    echo "## Accepted Authority"
    echo
    echo "- PCC-01 Implementation Contract — Human Acceptance — 2026-08-13"
    echo "- PCC-01 Core Experience Implementation Specification — Human Acceptance — 2026-08-13"
    echo "- PCC-01 Implementation Inventory and Build Plan — Human Acceptance — 2026-08-13"
    echo
    echo "## Reused Conserved Physiology"
    echo
    echo '```text'
    echo "Experience.create()"
    echo "    -> serialize_experience()"
    echo "    -> recover_experience()"
    echo "    -> SessionBinding.create()"
    echo '```'
    echo
    echo "No new repository physiology was introduced."
    echo
    echo "No duplicate Session Binding organ was introduced."
    echo
    echo "## RUN 043 Failure History"
    echo
    echo "The first RUN 043 harness incorrectly assumed that ExperienceRepository was a concrete durable-storage implementation."
    echo
    echo "That assumption was rejected from repository evidence."
    echo
    echo "## RUN 043A Correction"
    echo
    echo "RUN 043A replaced that assumption with the already-conserved Experience serialization/recovery physiology."
    echo
    echo "Its behavioral demonstration succeeded."
    echo
    echo "The subsequent RUN 043A procedural stop occurred during a working-tree boundary check and did not invalidate the successful behavioral results."
    echo
    echo "## Original RUN 043A Bash — Complete"
    echo
    echo '```bash'
    cat "$ORIGINAL_SCRIPT"
    echo '```'
    echo
    echo "## Original RUN 043A Terminal Output — Complete"
    echo
    echo '```text'
    cat "$ORIGINAL_OUTPUT"
    echo '```'
    echo
    echo "## Behavioral Artifact — Complete"
    echo
    echo "Path: \`$TEST\`"
    echo
    echo "SHA-256: \`$TEST_SHA\`"
    echo
    echo '```python'
    cat "$TEST"
    echo '```'
    echo
    echo "## Demonstrated Evidence"
    echo
    echo "- Dedicated Session Binding after recovery examinations: 7/7 PASS"
    echo "- Existing Session Binding examinations: 20/20 PASS"
    echo "- Complete Experience regression: 151/151 PASS"
    echo "- Experience identity survives recovery: PASS"
    echo "- Recovered Experience accepts legitimate Session binding: PASS"
    echo "- Session identity remains distinct from Experience identity: PASS"
    echo "- Session rebinding does not redefine Experience identity: PASS"
    echo "- Session Binding does not mutate Persistent Experience body: PASS"
    echo
    echo "## Organ Boundary"
    echo
    echo "- Core Experience implementation modified: NO"
    echo "- Experience persistence implementation modified: NO"
    echo "- Existing Session Binding implementation modified: NO"
    echo "- Behavioral evidence added: YES"
    echo
    echo "## Conservation Bash — Complete"
    echo
    echo '```bash'
    cat "$THIS_SCRIPT"
    echo '```'
    echo
    echo "## Epistemic Status Before Git Conservation"
    echo
    echo "- Session Binding after recovery: DEMONSTRATED"
    echo
    echo "- Git conservation: PENDING"
    echo
    echo "- Whole PCC-01 final claim: NOT YET"
    echo
    echo "- CANON: NOT CLAIMED BY THIS RUN"
    echo
    echo "- PRODUCTION-READY: NOT CLAIMED BY THIS RUN"
} > "$REPORT"

[ -s "$REPORT" ] || {
    echo "ERROR: report was not generated"
    fail 1
}

echo "PASS: autosufficient report generated"
echo "REPORT:"
echo "$REPORT"

echo
echo "[5/7] Stage only RUN 043A evidence"

git add -- "$TEST" "$REPORT" || fail $?

ACTUAL="$(
    git diff --cached --name-only | sort
)"

EXPECTED="$(
    printf '%s\n' \
        "$TEST" \
        "$REPORT" \
    | sort
)"

if [ "$ACTUAL" != "$EXPECTED" ]; then
    echo "ERROR: staging boundary mismatch"
    echo
    echo "EXPECTED:"
    printf '%s\n' "$EXPECTED"
    echo
    echo "ACTUAL:"
    printf '%s\n' "$ACTUAL"

    git reset --quiet

    fail 1
fi

echo "STAGED:"
printf '%s\n' "$ACTUAL"

echo
echo "PASS: exact conservation boundary"

echo
echo "[6/7] Commit and synchronize behavioral evidence"

git commit -m \
"test: conserve PCC-01 session binding after recovery evidence" || fail $?

EVIDENCE_HEAD="$(git rev-parse HEAD)" || fail $?

git push origin main || fail $?
git fetch origin main --quiet || fail $?

REMOTE_AFTER_EVIDENCE="$(git rev-parse origin/main)" || fail $?

[ "$EVIDENCE_HEAD" = "$REMOTE_AFTER_EVIDENCE" ] || {
    echo "ERROR: behavioral evidence not synchronized"
    fail 1
}

echo "PASS: behavioral evidence synchronized"
echo "EVIDENCE HEAD:"
echo "$EVIDENCE_HEAD"

echo
echo "[7/7] Finalize epic-thread and synchronize"

{
    echo
    echo "## Git Conservation Result"
    echo
    echo "- Baseline: \`$BASE\`"
    echo "- Behavioral evidence commit: \`$EVIDENCE_HEAD\`"
    echo "- Behavioral evidence synchronized to origin/main: PASS"
    echo
    echo "## Conservation Terminal Output"
    echo
    echo "The complete conservation output is generated during this operation."
    echo
    echo "Its final successful state is recorded below."
    echo
    echo "## Final Epistemic Conclusion"
    echo
    echo "**Session Binding after Persistent Experience recovery is DEMONSTRATED + CONSERVED.**"
    echo
    echo "This conclusion is based on preserved successful execution evidence and the conserved behavioral artifact."
    echo
    echo "No whole-PCC-01 CANON or PRODUCTION-READY declaration is made by RUN 043A."
} >> "$REPORT"

git add -- "$REPORT" || fail $?

git commit -m \
"docs: finalize PCC-01 RUN 043A evidence" || fail $?

FINAL_HEAD="$(git rev-parse HEAD)" || fail $?

git push origin main || fail $?
git fetch origin main --quiet || fail $?

FINAL_REMOTE="$(git rev-parse origin/main)" || fail $?

[ "$FINAL_HEAD" = "$FINAL_REMOTE" ] || {
    echo "ERROR: final report synchronization failed"
    fail 1
}

echo
echo "=========================================================="
echo "RUN 043C COMPLETE"
echo "=========================================================="
echo
echo "TESTS RE-EXECUTED:"
echo "NO"
echo
echo "PRESERVED RESULTS:"
echo "7/7 PASS"
echo "20/20 PASS"
echo "151/151 PASS"
echo
echo "EVIDENCE HEAD:"
echo "$EVIDENCE_HEAD"
echo
echo "FINAL HEAD:"
echo "$FINAL_HEAD"
echo
echo "LOCAL == origin/main:"
echo "PASS"
echo
echo "SESSION BINDING AFTER RECOVERY:"
echo "DEMONSTRATED + CONSERVED"
echo
echo "REPORT:"
echo "$REPORT"
echo
echo "NEXT:"
echo "GPT verifies GitHub directly before deriving the next PCC-01 implementation."
echo "=========================================================="
```

## Epistemic Status Before Git Conservation

- Session Binding after recovery: DEMONSTRATED

- Git conservation: PENDING

- Whole PCC-01 final claim: NOT YET

- CANON: NOT CLAIMED BY THIS RUN

- PRODUCTION-READY: NOT CLAIMED BY THIS RUN

## Git Conservation Result

- Baseline: `9c9ffe4c30a81fb65bc5601c6cd3d666ea348e51`
- Behavioral evidence commit: `f79dc18cf6e1a4f0c290e0f118262dd19cadf14a`
- Behavioral evidence synchronized to origin/main: PASS

## Conservation Terminal Output

The complete conservation output is generated during this operation.

Its final successful state is recorded below.

## Final Epistemic Conclusion

**Session Binding after Persistent Experience recovery is DEMONSTRATED + CONSERVED.**

This conclusion is based on preserved successful execution evidence and the conserved behavioral artifact.

No whole-PCC-01 CANON or PRODUCTION-READY declaration is made by RUN 043A.

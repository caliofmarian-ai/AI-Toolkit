# PCC-01 — RUN 045 — Experience Forgetting Implementation

## Capability

PCC-01 — Persistent Experience

## Build Phase

Phase 10 — Forgetting

## Verified Git baseline

`6b7354be9063bea1bc0e802386f941efbee5f476`

## Evidence-derived authority

- accepted Implementation Inventory and Build Plan
- Experience Forgetting explicitly required
- forgetting must be controlled and verifiable
- forgetting must remain distinguishable from accidental loss
- retention and forgetting remain separate organs

## Anatomical boundaries

- Forgetting != Retention
- Forgetting != Protection
- Forgetting != archival
- Forgetting != accidental storage loss
- missing record != demonstrated forgetting

## Implemented tissue

- `lib/python/experience/forgetting.py`
- `lib/python/experience/forgetting_persistence.py`
- `tests/experience/test_experience_forgetting.py`
- `tests/experience/test_experience_forgetting_restart.py`

## Bash executed — complete

```bash
#!/data/data/com.termux/files/usr/bin/bash
set -uo pipefail

export GIT_PAGER=cat
export PAGER=cat
export GH_PAGER=cat

cd "$HOME/storage/shared/AI-Projects/AI-Toolkit" || exit 1

BASE="6b7354be9063bea1bc0e802386f941efbee5f476"

FORGETTING="lib/python/experience/forgetting.py"
FORGETTING_PERSISTENCE="lib/python/experience/forgetting_persistence.py"
TEST="tests/experience/test_experience_forgetting.py"
RESTART_TEST="tests/experience/test_experience_forgetting_restart.py"
REPORT="work/implementation-reports/PCC-01/PCC-01_RUN045_EXPERIENCE_FORGETTING_IMPLEMENTATION.md"

SELF="$PREFIX/tmp/pcc01_run045.sh"
OUT="$PREFIX/tmp/pcc01_run045.output"

mkdir -p "$(dirname "$REPORT")"
: > "$OUT"

exec > >(tee -a "$OUT") 2>&1

fail() {
    CODE="${1:-1}"
    echo
    echo "=========================================================="
    echo "RUN 045 STOPPED SAFELY"
    echo "=========================================================="
    echo "Exit code: $CODE"
    echo "NO commit/push after failure"
    echo "=========================================================="
    exit "$CODE"
}

echo "=========================================================="
echo "PCC-01"
echo "EXPERIENCE FORGETTING — RUN 045"
echo "EVIDENCE-DERIVED IMPLEMENTATION"
echo "=========================================================="

echo
echo "[1/10] Verify synchronized Git authority"

git fetch origin main --quiet || fail $?

LOCAL="$(git rev-parse HEAD)" || fail $?
REMOTE="$(git rev-parse origin/main)" || fail $?

echo "Expected:    $BASE"
echo "LOCAL:       $LOCAL"
echo "origin/main: $REMOTE"

[ "$LOCAL" = "$BASE" ] || fail 1
[ "$REMOTE" = "$BASE" ] || fail 1

TRACKED_DIRTY="$(
    {
        git diff --name-only
        git diff --cached --name-only
    } | sort -u
)"

if [ -n "$TRACKED_DIRTY" ]; then
    echo "ERROR: tracked/staged working tree is not clean"
    printf '%s\n' "$TRACKED_DIRTY"
    fail 1
fi

echo "PASS: tracked/staged Git authority is clean"

UNTRACKED_EXISTING="$(git ls-files --others --exclude-standard | sort)"

if [ -n "$UNTRACKED_EXISTING" ]; then
    echo
    echo "PRE-EXISTING UNTRACKED HISTORICAL ARTIFACTS:"
    printf '%s\n' "$UNTRACKED_EXISTING"
    echo
    echo "These artifacts are outside RUN 045."
    echo "They will not be deleted, modified, staged, committed, or pushed."
fi

echo "PASS: exact GitHub-verified RUN 044 baseline"

echo
echo "[2/10] Verify accepted Forgetting authority and inherited anatomy"

AUTHORITY="work/decisions/PCC-01_IMPLEMENTATION_INVENTORY_AND_BUILD_PLAN_HUMAN_ACCEPTANCE_2026-08-13.md"
PLAN="work/planning/PCC-01_IMPLEMENTATION_INVENTORY_AND_BUILD_PLAN.md"
RETENTION="lib/python/experience/retention.py"
RETENTION_PERSISTENCE="lib/python/experience/retention_persistence.py"
PROTECTION="lib/python/experience/protection.py"

for FILE in \
    "$AUTHORITY" \
    "$PLAN" \
    "$RETENTION" \
    "$RETENTION_PERSISTENCE" \
    "$PROTECTION" \
    "lib/python/experience/identity.py" \
    "lib/python/experience/model.py"
do
    [ -s "$FILE" ] || {
        echo "ERROR: required authority/anatomy missing: $FILE"
        fail 1
    }
done

grep -Fq "Experience Forgetting" "$AUTHORITY" || {
    echo "ERROR: accepted Experience Forgetting authority missing"
    fail 1
}

grep -Fq "Build Phase 10 — Forgetting" "$PLAN" || {
    echo "ERROR: Phase 10 Forgetting authority missing"
    fail 1
}

grep -Fq "Retention is not Forgetting." "$RETENTION" || {
    echo "ERROR: Retention/Forgetting boundary missing"
    fail 1
}

grep -Fq "It does not replace retention or forgetting." "$PROTECTION" || {
    echo "ERROR: Protection/Forgetting boundary missing"
    fail 1
}

echo "PASS: Forgetting explicitly authorized"
echo "PASS: Phase 10 follows Retention"
echo "PASS: Forgetting != Retention"
echo "PASS: Forgetting != Protection"

echo
echo "[3/10] Verify no duplicate Forgetting organ"

for FILE in \
    "$FORGETTING" \
    "$FORGETTING_PERSISTENCE" \
    "$TEST" \
    "$RESTART_TEST"
do
    if git cat-file -e "HEAD:$FILE" 2>/dev/null; then
        echo "ERROR: RUN 045 target already exists in Git authority:"
        echo "$FILE"
        fail 1
    fi
done

echo "PASS: no duplicate PCC-01 Forgetting organ"

echo
echo "[4/10] Build controlled Forgetting physiology"

cat > "$FORGETTING" <<'PY'
"""Controlled forgetting physiology for PCC-01 Persistent Experience.

Forgetting is an explicit, intentional and inspectable operation.

Forgetting is not accidental data loss.
Forgetting is not retention.
Forgetting is not protection.
Forgetting is not archival.
Forgetting does not rewrite Experience identity.

The organ records that an identified Experience has entered an
explicit forgetting condition under a stated reason and authorization.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum

from .identity import ExperienceId


class ExperienceForgettingError(Exception):
    """Base error for Experience forgetting violations."""


class InvalidForgettingIdentityError(ExperienceForgettingError):
    """Raised when forgetting receives an invalid Experience identity."""


class InvalidForgettingReasonError(ExperienceForgettingError):
    """Raised when forgetting lacks an explicit reason."""


class UnauthorizedForgettingError(ExperienceForgettingError):
    """Raised when forgetting is attempted without explicit authorization."""


class ForgettingState(str, Enum):
    """Observable forgetting condition."""

    PRESENT = "present"
    FORGOTTEN = "forgotten"


@dataclass(frozen=True, slots=True)
class ExperienceForgetting:
    """Forgetting state associated with one persistent Experience identity."""

    experience_id: ExperienceId
    state: ForgettingState
    reason: str | None = None
    forgotten_at: datetime | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.experience_id, ExperienceId):
            raise InvalidForgettingIdentityError(
                "experience_id must be an ExperienceId"
            )

        if self.state is ForgettingState.PRESENT:
            if self.reason is not None:
                raise InvalidForgettingReasonError(
                    "present Experience cannot carry a forgetting reason"
                )

            if self.forgotten_at is not None:
                raise ExperienceForgettingError(
                    "present Experience cannot carry forgotten_at"
                )

        if self.state is ForgettingState.FORGOTTEN:
            _require_reason(self.reason)

            if self.forgotten_at is None:
                raise ExperienceForgettingError(
                    "forgotten Experience requires forgotten_at"
                )

            if self.forgotten_at.tzinfo is None:
                raise ExperienceForgettingError(
                    "forgotten_at must be timezone-aware"
                )

    @classmethod
    def present(
        cls,
        experience_id: ExperienceId,
    ) -> "ExperienceForgetting":
        return cls(
            experience_id=experience_id,
            state=ForgettingState.PRESENT,
        )

    def forget(
        self,
        *,
        reason: str,
        authorized: bool,
        forgotten_at: datetime | None = None,
    ) -> "ExperienceForgetting":
        """Enter controlled forgetting without redefining identity."""

        if not isinstance(authorized, bool):
            raise TypeError("authorized must be bool")

        if not authorized:
            raise UnauthorizedForgettingError(
                "forgetting requires explicit authorization"
            )

        normalized_reason = _require_reason(reason)

        if forgotten_at is None:
            forgotten_at = datetime.now(timezone.utc)

        if forgotten_at.tzinfo is None:
            raise ExperienceForgettingError(
                "forgotten_at must be timezone-aware"
            )

        if self.state is ForgettingState.FORGOTTEN:
            if self.reason == normalized_reason:
                return self

            raise ExperienceForgettingError(
                "forgotten Experience cannot silently rewrite forgetting reason"
            )

        return ExperienceForgetting(
            experience_id=self.experience_id,
            state=ForgettingState.FORGOTTEN,
            reason=normalized_reason,
            forgotten_at=forgotten_at,
        )

    @property
    def is_forgotten(self) -> bool:
        return self.state is ForgettingState.FORGOTTEN


def _require_reason(value: str | None) -> str:
    if not isinstance(value, str):
        raise InvalidForgettingReasonError(
            "forgetting reason must be a non-empty string"
        )

    normalized = value.strip()

    if not normalized:
        raise InvalidForgettingReasonError(
            "forgetting reason must be a non-empty string"
        )

    return normalized
PY

cat > "$FORGETTING_PERSISTENCE" <<'PY'
"""Durable evidence of controlled PCC-01 Experience Forgetting.

This repository conserves the fact that controlled forgetting occurred.

It deliberately does not pretend that missing storage equals forgetting.
Accidental absence and explicit forgetting remain epistemically distinct.
"""

from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any

from .forgetting import ExperienceForgetting, ForgettingState
from .identity import ExperienceId


class ExperienceForgettingPersistenceError(Exception):
    """Base error for durable Forgetting persistence."""


class ExperienceForgettingNotFoundError(
    ExperienceForgettingPersistenceError
):
    """No explicit forgetting record exists for this identity."""


class ExperienceForgettingRepository:
    """Filesystem-backed durable record of forgetting physiology."""

    def __init__(self, root: str | Path) -> None:
        self._root = Path(root)

    def save(
        self,
        forgetting: ExperienceForgetting,
    ) -> None:
        if not isinstance(forgetting, ExperienceForgetting):
            raise TypeError(
                "forgetting must be an ExperienceForgetting"
            )

        self._root.mkdir(parents=True, exist_ok=True)
        target = self._path(forgetting.experience_id)

        payload = {
            "experience_id": str(forgetting.experience_id),
            "state": forgetting.state.value,
            "reason": forgetting.reason,
            "forgotten_at": (
                forgetting.forgotten_at.isoformat()
                if forgetting.forgotten_at is not None
                else None
            ),
        }

        with NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=self._root,
            prefix=".forgetting-",
            suffix=".tmp",
            delete=False,
        ) as handle:
            temporary = Path(handle.name)

            json.dump(
                payload,
                handle,
                sort_keys=True,
                separators=(",", ":"),
            )
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())

        try:
            os.replace(temporary, target)
        finally:
            if temporary.exists():
                temporary.unlink()

    def load(
        self,
        experience_id: ExperienceId,
    ) -> ExperienceForgetting:
        if not isinstance(experience_id, ExperienceId):
            raise TypeError(
                "experience_id must be an ExperienceId"
            )

        target = self._path(experience_id)

        if not target.is_file():
            raise ExperienceForgettingNotFoundError(
                f"no explicit forgetting record for Experience {experience_id}"
            )

        with target.open("r", encoding="utf-8") as handle:
            payload: dict[str, Any] = json.load(handle)

        stored_id = ExperienceId.from_string(
            payload["experience_id"]
        )

        if stored_id != experience_id:
            raise ExperienceForgettingPersistenceError(
                "stored forgetting identity does not match requested Experience"
            )

        state = ForgettingState(payload["state"])

        if state is ForgettingState.PRESENT:
            return ExperienceForgetting.present(
                stored_id
            )

        forgotten_at_raw = payload["forgotten_at"]

        if not isinstance(forgotten_at_raw, str):
            raise ExperienceForgettingPersistenceError(
                "forgotten state requires forgotten_at"
            )

        return ExperienceForgetting(
            experience_id=stored_id,
            state=ForgettingState.FORGOTTEN,
            reason=payload["reason"],
            forgotten_at=datetime.fromisoformat(
                forgotten_at_raw
            ),
        )

    def contains(
        self,
        experience_id: ExperienceId,
    ) -> bool:
        if not isinstance(experience_id, ExperienceId):
            raise TypeError(
                "experience_id must be an ExperienceId"
            )

        return self._path(experience_id).is_file()

    def _path(
        self,
        experience_id: ExperienceId,
    ) -> Path:
        return self._root / f"{experience_id}.json"
PY

echo "PASS: Forgetting organ built"
echo "PASS: durable Forgetting evidence repository built"

echo
echo "[5/10] Build behavioral examinations"

cat > "$TEST" <<'PY'
from datetime import datetime, timezone

import pytest

from lib.python.experience.forgetting import (
    ExperienceForgetting,
    ExperienceForgettingError,
    ForgettingState,
    InvalidForgettingReasonError,
    UnauthorizedForgettingError,
)
from lib.python.experience.model import Experience
from lib.python.experience.retention import ExperienceRetention


def test_new_forgetting_state_is_explicitly_present():
    experience = Experience.create()

    forgetting = ExperienceForgetting.present(
        experience.experience_id
    )

    assert forgetting.experience_id == experience.experience_id
    assert forgetting.state is ForgettingState.PRESENT
    assert forgetting.is_forgotten is False
    assert forgetting.reason is None
    assert forgetting.forgotten_at is None


def test_forgetting_requires_explicit_authorization():
    experience = Experience.create()

    forgetting = ExperienceForgetting.present(
        experience.experience_id
    )

    with pytest.raises(UnauthorizedForgettingError):
        forgetting.forget(
            reason="authorized forgetting required",
            authorized=False,
        )


def test_forgetting_requires_explicit_reason():
    experience = Experience.create()

    forgetting = ExperienceForgetting.present(
        experience.experience_id
    )

    with pytest.raises(InvalidForgettingReasonError):
        forgetting.forget(
            reason="",
            authorized=True,
        )


def test_forgetting_preserves_experience_identity():
    experience = Experience.create()
    before = experience.experience_id

    forgetting = ExperienceForgetting.present(
        before
    ).forget(
        reason="explicit owner-authorized forgetting",
        authorized=True,
    )

    assert forgetting.experience_id == before
    assert experience.experience_id == before
    assert forgetting.is_forgotten is True


def test_forgetting_time_is_explicit_and_timezone_aware():
    experience = Experience.create()

    moment = datetime(
        2026,
        8,
        14,
        13,
        0,
        tzinfo=timezone.utc,
    )

    forgetting = ExperienceForgetting.present(
        experience.experience_id
    ).forget(
        reason="controlled forgetting examination",
        authorized=True,
        forgotten_at=moment,
    )

    assert forgetting.forgotten_at == moment
    assert forgetting.forgotten_at.tzinfo is not None


def test_same_forgetting_operation_is_idempotent():
    experience = Experience.create()

    forgotten = ExperienceForgetting.present(
        experience.experience_id
    ).forget(
        reason="same forgetting rule",
        authorized=True,
    )

    repeated = forgotten.forget(
        reason="same forgetting rule",
        authorized=True,
    )

    assert repeated is forgotten


def test_forgetting_reason_cannot_be_silently_rewritten():
    experience = Experience.create()

    forgotten = ExperienceForgetting.present(
        experience.experience_id
    ).forget(
        reason="original reason",
        authorized=True,
    )

    with pytest.raises(ExperienceForgettingError):
        forgotten.forget(
            reason="replacement reason",
            authorized=True,
        )


def test_retention_and_forgetting_are_distinct_organs():
    experience = Experience.create()

    retention = ExperienceRetention.unretained(
        experience.experience_id
    ).retain(
        reason="retention examination"
    )

    forgetting = ExperienceForgetting.present(
        experience.experience_id
    )

    assert retention.experience_id == forgetting.experience_id
    assert retention.is_retained is True
    assert forgetting.is_forgotten is False
    assert type(retention) is not type(forgetting)


def test_forgetting_does_not_mutate_experience_body():
    experience = Experience.create()

    before = (
        experience.experience_id,
        experience.created_at,
        experience.state,
    )

    ExperienceForgetting.present(
        experience.experience_id
    ).forget(
        reason="external forgetting physiology",
        authorized=True,
    )

    after = (
        experience.experience_id,
        experience.created_at,
        experience.state,
    )

    assert after == before
PY

cat > "$RESTART_TEST" <<'PY'
from datetime import datetime, timezone

import pytest

from lib.python.experience.forgetting import (
    ExperienceForgetting,
    ForgettingState,
)
from lib.python.experience.forgetting_persistence import (
    ExperienceForgettingNotFoundError,
    ExperienceForgettingRepository,
)
from lib.python.experience.model import Experience


def test_explicit_forgetting_survives_repository_reconstruction(
    tmp_path,
):
    experience = Experience.create()
    experience_id = experience.experience_id

    moment = datetime(
        2026,
        8,
        14,
        13,
        30,
        tzinfo=timezone.utc,
    )

    before = ExperienceForgetting.present(
        experience_id
    ).forget(
        reason="restart-surviving forgetting",
        authorized=True,
        forgotten_at=moment,
    )

    repository_a = ExperienceForgettingRepository(
        tmp_path
    )
    repository_a.save(before)

    del repository_a

    repository_b = ExperienceForgettingRepository(
        tmp_path
    )
    after = repository_b.load(experience_id)

    assert after.experience_id == experience_id
    assert after.state is ForgettingState.FORGOTTEN
    assert after.reason == before.reason
    assert after.forgotten_at == moment
    assert repository_b.contains(experience_id)


def test_missing_record_is_not_fabricated_as_forgetting(
    tmp_path,
):
    experience = Experience.create()

    repository = ExperienceForgettingRepository(
        tmp_path
    )

    assert repository.contains(
        experience.experience_id
    ) is False

    with pytest.raises(
        ExperienceForgettingNotFoundError
    ):
        repository.load(
            experience.experience_id
        )


def test_present_state_is_distinct_from_missing_record(
    tmp_path,
):
    experience = Experience.create()

    present = ExperienceForgetting.present(
        experience.experience_id
    )

    repository = ExperienceForgettingRepository(
        tmp_path
    )
    repository.save(present)

    recovered = repository.load(
        experience.experience_id
    )

    assert recovered.state is ForgettingState.PRESENT
    assert recovered.is_forgotten is False
    assert repository.contains(
        experience.experience_id
    ) is True


def test_forgetting_recovery_preserves_identity(
    tmp_path,
):
    experience = Experience.create()
    before_id = experience.experience_id

    forgotten = ExperienceForgetting.present(
        before_id
    ).forget(
        reason="identity conservation",
        authorized=True,
    )

    repository = ExperienceForgettingRepository(
        tmp_path
    )
    repository.save(forgotten)

    recovered = repository.load(before_id)

    assert recovered.experience_id == before_id
    assert experience.experience_id == before_id
PY

python -m py_compile \
    "$FORGETTING" \
    "$FORGETTING_PERSISTENCE" \
    "$TEST" \
    "$RESTART_TEST" || fail $?

echo "PASS: syntax"

echo
echo "[6/10] Execute dedicated Forgetting physiology"

python -m pytest -q \
    "$TEST" \
    "$RESTART_TEST" || fail $?

echo "PASS: dedicated Forgetting physiology"

echo
echo "[7/10] Execute complete inherited Experience regression"

python -m pytest -q tests/experience || fail $?

echo "PASS: complete Experience regression"

echo
echo "[8/10] Verify exact mutation boundary"

git diff --check -- \
    "$FORGETTING" \
    "$FORGETTING_PERSISTENCE" \
    "$TEST" \
    "$RESTART_TEST" || fail $?

for FILE in \
    "$FORGETTING" \
    "$FORGETTING_PERSISTENCE" \
    "$TEST" \
    "$RESTART_TEST"
do
    [ -s "$FILE" ] || {
        echo "ERROR: missing RUN 045 artifact: $FILE"
        fail 1
    }
done

echo "PASS: exact RUN 045 software boundary"

echo
echo "[9/10] Generate autosufficient epic-thread MD"

{
    echo "# PCC-01 — RUN 045 — Experience Forgetting Implementation"
    echo
    echo "## Capability"
    echo
    echo "PCC-01 — Persistent Experience"
    echo
    echo "## Build Phase"
    echo
    echo "Phase 10 — Forgetting"
    echo
    echo "## Verified Git baseline"
    echo
    echo "\`$BASE\`"
    echo
    echo "## Evidence-derived authority"
    echo
    echo "- accepted Implementation Inventory and Build Plan"
    echo "- Experience Forgetting explicitly required"
    echo "- forgetting must be controlled and verifiable"
    echo "- forgetting must remain distinguishable from accidental loss"
    echo "- retention and forgetting remain separate organs"
    echo
    echo "## Anatomical boundaries"
    echo
    echo "- Forgetting != Retention"
    echo "- Forgetting != Protection"
    echo "- Forgetting != archival"
    echo "- Forgetting != accidental storage loss"
    echo "- missing record != demonstrated forgetting"
    echo
    echo "## Implemented tissue"
    echo
    echo "- \`$FORGETTING\`"
    echo "- \`$FORGETTING_PERSISTENCE\`"
    echo "- \`$TEST\`"
    echo "- \`$RESTART_TEST\`"
    echo
    echo "## Bash executed — complete"
    echo
    echo '```bash'
    cat "$SELF"
    echo '```'
    echo
    echo "## Terminal output — complete"
    echo
    echo '```text'
    cat "$OUT"
    echo '```'
    echo
    echo "## Epistemic conclusion before conservation"
    echo
    echo "- controlled Forgetting organ: BUILT LOCALLY"
    echo "- explicit authorization requirement: DEMONSTRATED"
    echo "- explicit reason requirement: DEMONSTRATED"
    echo "- identity conservation: DEMONSTRATED"
    echo "- durable forgetting evidence: DEMONSTRATED"
    echo "- missing storage != forgetting: DEMONSTRATED"
    echo "- restart recovery of forgetting state: DEMONSTRATED"
    echo "- whole PCC-01 final claim: NOT YET"
} > "$REPORT"

[ -s "$REPORT" ] || fail 1

echo "PASS: autosufficient RUN 045 MD generated"

echo
echo "[10/10] Conserve implementation + epic-thread"

git add -- \
    "$FORGETTING" \
    "$FORGETTING_PERSISTENCE" \
    "$TEST" \
    "$RESTART_TEST" \
    "$REPORT" || fail $?

ACTUAL="$(git diff --cached --name-only | sort)"

EXPECTED="$(
    printf '%s\n' \
        "$FORGETTING" \
        "$FORGETTING_PERSISTENCE" \
        "$TEST" \
        "$RESTART_TEST" \
        "$REPORT" \
    | sort
)"

if [ "$ACTUAL" != "$EXPECTED" ]; then
    echo "ERROR: staged mutation boundary mismatch"
    echo
    echo "EXPECTED:"
    printf '%s\n' "$EXPECTED"
    echo
    echo "ACTUAL:"
    printf '%s\n' "$ACTUAL"
    git reset --quiet
    fail 1
fi

git commit -m \
    "feat: implement PCC-01 experience forgetting" || fail $?

IMPLEMENTATION_HEAD="$(git rev-parse HEAD)" || fail $?

git push origin main || fail $?
git fetch origin main --quiet || fail $?

[ "$IMPLEMENTATION_HEAD" = "$(git rev-parse origin/main)" ] || fail 1

{
    echo
    echo "## Git conservation"
    echo
    echo "- Baseline: \`$BASE\`"
    echo "- Implementation commit: \`$IMPLEMENTATION_HEAD\`"
    echo "- origin/main synchronization: PASS"
    echo
    echo "## Final RUN 045 conclusion"
    echo
    echo "**Experience Forgetting: IMPLEMENTED + DEMONSTRATED + CONSERVED**"
    echo
    echo "Retention remains independently conserved."
    echo
    echo "Accidental absence is not accepted as Evidence of forgetting."
    echo
    echo "RUN 045 does not declare whole PCC-01 CANON or PRODUCTION-READY."
    echo
    echo "---"
    echo
    echo "END OF PCC-01 RUN 045"
} >> "$REPORT"

git add -- "$REPORT" || fail $?

git commit -m \
    "docs: finalize PCC-01 RUN 045 evidence" || fail $?

FINAL_HEAD="$(git rev-parse HEAD)" || fail $?

git push origin main || fail $?
git fetch origin main --quiet || fail $?

FINAL_REMOTE="$(git rev-parse origin/main)" || fail $?

[ "$FINAL_HEAD" = "$FINAL_REMOTE" ] || fail 1

echo
echo "=========================================================="
echo "RUN 045 COMPLETE"
echo "=========================================================="
echo
echo "BASE:"
echo "$BASE"
echo
echo "IMPLEMENTATION HEAD:"
echo "$IMPLEMENTATION_HEAD"
echo
echo "FINAL HEAD:"
echo "$FINAL_HEAD"
echo
echo "LOCAL == origin/main:"
echo "PASS"
echo
echo "EXPERIENCE FORGETTING:"
echo "IMPLEMENTED + DEMONSTRATED + CONSERVED"
echo
echo "EPIC-THREAD MD:"
echo "$REPORT"
echo
echo "NEXT CONTRACT PHASE:"
echo "PHASE 11 — CONFLICT AND AMBIGUITY"
echo
echo "NEXT:"
echo "GPT verifies GitHub directly before deriving RUN 046."
echo "=========================================================="
```

## Terminal output — complete

```text
==========================================================
PCC-01
EXPERIENCE FORGETTING — RUN 045
EVIDENCE-DERIVED IMPLEMENTATION
==========================================================

[1/10] Verify synchronized Git authority
Expected:    6b7354be9063bea1bc0e802386f941efbee5f476
LOCAL:       6b7354be9063bea1bc0e802386f941efbee5f476
origin/main: 6b7354be9063bea1bc0e802386f941efbee5f476
PASS: tracked/staged Git authority is clean

PRE-EXISTING UNTRACKED HISTORICAL ARTIFACTS:
tests/experience/harness/pcc01_coordination_crash_reconciler.py
tests/experience/harness/pcc01_coordination_crash_writer.py
work/implementation-reports/PCC-01/PCC-01_RUN034C_FAILURE_RECOVERY_AND_EXACT_INTEGRATION_ANATOMY.md
work/implementation-reports/PCC-01/PCC-01_RUN034D_EXACT_LOCAL_JOURNAL_ANATOMY_FOR_INTEGRATION.md
work/implementation-reports/PCC-01/PCC-01_RUN038A_HARNESS_CAUSAL_CORRECTION.md
work/implementation-reports/PCC-01/PCC-01_RUN043B_LOCAL_ARTIFACT_STATE_INSPECTION.md

These artifacts are outside RUN 045.
They will not be deleted, modified, staged, committed, or pushed.
PASS: exact GitHub-verified RUN 044 baseline

[2/10] Verify accepted Forgetting authority and inherited anatomy
PASS: Forgetting explicitly authorized
PASS: Phase 10 follows Retention
PASS: Forgetting != Retention
PASS: Forgetting != Protection

[3/10] Verify no duplicate Forgetting organ
PASS: no duplicate PCC-01 Forgetting organ

[4/10] Build controlled Forgetting physiology
PASS: Forgetting organ built
PASS: durable Forgetting evidence repository built

[5/10] Build behavioral examinations
PASS: syntax

[6/10] Execute dedicated Forgetting physiology
.............                                                            [100%]
13 passed in 0.55s
PASS: dedicated Forgetting physiology

[7/10] Execute complete inherited Experience regression
........................................................................ [ 41%]
........................................................................ [ 82%]
..............................                                           [100%]
174 passed in 3.11s
PASS: complete Experience regression

[8/10] Verify exact mutation boundary
PASS: exact RUN 045 software boundary

[9/10] Generate autosufficient epic-thread MD
```

## Epistemic conclusion before conservation

- controlled Forgetting organ: BUILT LOCALLY
- explicit authorization requirement: DEMONSTRATED
- explicit reason requirement: DEMONSTRATED
- identity conservation: DEMONSTRATED
- durable forgetting evidence: DEMONSTRATED
- missing storage != forgetting: DEMONSTRATED
- restart recovery of forgetting state: DEMONSTRATED
- whole PCC-01 final claim: NOT YET

# PCC-01 — RUN 046 — Conflict and Ambiguity

## Capability

PCC-01 — Persistent Experience

## Build Phase

Phase 11 — Conflict and ambiguity

## Verified baseline

`ea342aeca6ae6f2cb36912c04f963ad3c028b3b8`

## Contract-derived physiology

- conflict remains explicitly representable
- conflicting alternatives are preserved
- conflict representation does not silently erase a version
- ambiguity remains explicitly representable
- unknown may remain unknown
- confidence is explicit and is not truth
- Conflict != Ambiguity

## Implemented tissue

- `lib/python/experience/conflict.py`
- `lib/python/experience/ambiguity.py`
- `tests/experience/test_experience_conflict_and_ambiguity.py`

## Bash executed — complete

```bash
#!/data/data/com.termux/files/usr/bin/bash
set -uo pipefail

export GIT_PAGER=cat
export PAGER=cat
export GH_PAGER=cat

cd "$HOME/storage/shared/AI-Projects/AI-Toolkit" || exit 1

BASE="ea342aeca6ae6f2cb36912c04f963ad3c028b3b8"

CONFLICT="lib/python/experience/conflict.py"
AMBIGUITY="lib/python/experience/ambiguity.py"
TEST="tests/experience/test_experience_conflict_and_ambiguity.py"
REPORT="work/implementation-reports/PCC-01/PCC-01_RUN046_CONFLICT_AND_AMBIGUITY_IMPLEMENTATION.md"

SELF="$PREFIX/tmp/pcc01_run046.sh"
OUT="$PREFIX/tmp/pcc01_run046.output"

mkdir -p "$(dirname "$REPORT")"
: > "$OUT"

exec > >(tee -a "$OUT") 2>&1

fail() {
    CODE="${1:-1}"
    echo
    echo "=========================================================="
    echo "RUN 046 STOPPED SAFELY"
    echo "=========================================================="
    echo "Exit code: $CODE"
    echo "NO commit/push after failure"
    echo "=========================================================="
    exit "$CODE"
}

echo "=========================================================="
echo "PCC-01"
echo "CONFLICT AND AMBIGUITY — RUN 046"
echo "EVIDENCE-DERIVED IMPLEMENTATION"
echo "=========================================================="

echo
echo "[1/9] Verify GitHub-authoritative baseline"

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

echo "PASS: tracked/staged authority clean"

UNTRACKED_BEFORE="$(git ls-files --others --exclude-standard | sort)"

if [ -n "$UNTRACKED_BEFORE" ]; then
    echo
    echo "PRE-EXISTING UNTRACKED HISTORICAL ARTIFACTS:"
    printf '%s\n' "$UNTRACKED_BEFORE"
    echo
    echo "They remain outside RUN 046 conservation."
fi

echo
echo "[2/9] Verify accepted Phase 11 authority"

PLAN="work/planning/PCC-01_IMPLEMENTATION_INVENTORY_AND_BUILD_PLAN.md"
ACCEPTED="work/decisions/PCC-01_IMPLEMENTATION_INVENTORY_AND_BUILD_PLAN_HUMAN_ACCEPTANCE_2026-08-13.md"

for FILE in \
    "$PLAN" \
    "$ACCEPTED" \
    "lib/python/experience/model.py" \
    "lib/python/experience/identity.py"
do
    [ -s "$FILE" ] || {
        echo "ERROR: required evidence missing: $FILE"
        fail 1
    }
done

grep -Fq "Build Phase 11 — Conflict and ambiguity" "$PLAN" || fail 1
grep -Fq "Conflict representation" "$PLAN" || fail 1
grep -Fq "Ambiguity representation" "$PLAN" || fail 1
grep -Fq "Conflictul nu trebuie rezolvat prin ștergerea tăcută" "$PLAN" || fail 1
grep -Fq "Necunoașterea trebuie să poată rămâne necunoaștere" "$PLAN" || fail 1

echo "PASS: Phase 11 authorized"
echo "PASS: conflict must remain representable"
echo "PASS: ambiguity must remain representable"
echo "PASS: conflict must not silently erase alternatives"
echo "PASS: unknown may remain unknown"

echo
echo "[3/9] Verify no duplicate Phase 11 organs"

for FILE in "$CONFLICT" "$AMBIGUITY" "$TEST"; do
    if git cat-file -e "HEAD:$FILE" 2>/dev/null; then
        echo "ERROR: target already exists in Git authority:"
        echo "$FILE"
        fail 1
    fi
done

echo "PASS: no duplicate Phase 11 organs"

echo
echo "[4/9] Build Conflict representation"

cat > "$CONFLICT" <<'PY'
"""Conflict representation for PCC-01 Persistent Experience.

Conflict preserves incompatible claims without silently selecting,
rewriting or deleting one of them.

Representation is not resolution.
Conflict is not ambiguity.
Conflict does not redefine Experience identity.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable

from .identity import ExperienceId


class ExperienceConflictError(Exception):
    """Base error for Experience conflict representation."""


class InvalidConflictAlternativeError(ExperienceConflictError):
    """Raised when a conflict alternative is invalid."""


class ConflictState(str, Enum):
    OPEN = "open"
    RESOLVED = "resolved"


@dataclass(frozen=True, slots=True)
class ConflictAlternative:
    """One preserved alternative participating in a conflict."""

    label: str
    statement: str

    def __post_init__(self) -> None:
        if not isinstance(self.label, str) or not self.label.strip():
            raise InvalidConflictAlternativeError(
                "alternative label must be non-empty"
            )

        if not isinstance(self.statement, str) or not self.statement.strip():
            raise InvalidConflictAlternativeError(
                "alternative statement must be non-empty"
            )


@dataclass(frozen=True, slots=True)
class ExperienceConflict:
    """Explicit unresolved conflict attached to one Experience."""

    experience_id: ExperienceId
    alternatives: tuple[ConflictAlternative, ...]
    state: ConflictState = ConflictState.OPEN

    def __post_init__(self) -> None:
        if not isinstance(self.experience_id, ExperienceId):
            raise TypeError("experience_id must be an ExperienceId")

        if len(self.alternatives) < 2:
            raise ExperienceConflictError(
                "conflict requires at least two preserved alternatives"
            )

        labels = tuple(item.label.strip() for item in self.alternatives)

        if len(set(labels)) != len(labels):
            raise ExperienceConflictError(
                "conflict alternatives require distinct labels"
            )

    @classmethod
    def open(
        cls,
        *,
        experience_id: ExperienceId,
        alternatives: Iterable[ConflictAlternative],
    ) -> "ExperienceConflict":
        return cls(
            experience_id=experience_id,
            alternatives=tuple(alternatives),
            state=ConflictState.OPEN,
        )

    @property
    def is_open(self) -> bool:
        return self.state is ConflictState.OPEN

    def statements(self) -> tuple[str, ...]:
        return tuple(
            alternative.statement
            for alternative in self.alternatives
        )
PY

echo "PASS: Conflict representation built"

echo
echo "[5/9] Build Ambiguity representation"

cat > "$AMBIGUITY" <<'PY'
"""Ambiguity representation for PCC-01 Persistent Experience.

Ambiguity preserves uncertainty explicitly.

Unknown is allowed to remain unknown.
Ambiguity is not conflict.
Confidence is not truth.
Representation does not fabricate resolution.
"""

from __future__ import annotations

from dataclasses import dataclass

from .identity import ExperienceId


class ExperienceAmbiguityError(Exception):
    """Base error for Experience ambiguity representation."""


class InvalidAmbiguityDescriptionError(ExperienceAmbiguityError):
    """Raised when ambiguity lacks an explicit description."""


class InvalidConfidenceError(ExperienceAmbiguityError):
    """Raised when confidence is outside the accepted interval."""


@dataclass(frozen=True, slots=True)
class ExperienceAmbiguity:
    """Explicit unresolved uncertainty associated with an Experience."""

    experience_id: ExperienceId
    description: str
    confidence: float | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.experience_id, ExperienceId):
            raise TypeError("experience_id must be an ExperienceId")

        if (
            not isinstance(self.description, str)
            or not self.description.strip()
        ):
            raise InvalidAmbiguityDescriptionError(
                "ambiguity description must be non-empty"
            )

        if self.confidence is not None:
            if isinstance(self.confidence, bool) or not isinstance(
                self.confidence,
                (int, float),
            ):
                raise InvalidConfidenceError(
                    "confidence must be numeric or None"
                )

            if not 0.0 <= float(self.confidence) <= 1.0:
                raise InvalidConfidenceError(
                    "confidence must be between 0.0 and 1.0"
                )

    @property
    def is_unknown(self) -> bool:
        return self.confidence is None
PY

echo "PASS: Ambiguity representation built"

echo
echo "[6/9] Build contract-derived behavioral examinations"

cat > "$TEST" <<'PY'
import pytest

from lib.python.experience.ambiguity import (
    ExperienceAmbiguity,
    InvalidAmbiguityDescriptionError,
    InvalidConfidenceError,
)
from lib.python.experience.conflict import (
    ConflictAlternative,
    ConflictState,
    ExperienceConflict,
    ExperienceConflictError,
)
from lib.python.experience.model import Experience


def test_conflict_preserves_all_alternatives():
    experience = Experience.create()

    first = ConflictAlternative(
        label="observation-a",
        statement="the historical observation supports A",
    )
    second = ConflictAlternative(
        label="observation-b",
        statement="the historical observation supports B",
    )

    conflict = ExperienceConflict.open(
        experience_id=experience.experience_id,
        alternatives=(first, second),
    )

    assert conflict.state is ConflictState.OPEN
    assert conflict.is_open is True
    assert conflict.alternatives == (first, second)
    assert conflict.statements() == (
        first.statement,
        second.statement,
    )


def test_conflict_requires_multiple_preserved_alternatives():
    experience = Experience.create()

    with pytest.raises(ExperienceConflictError):
        ExperienceConflict.open(
            experience_id=experience.experience_id,
            alternatives=(
                ConflictAlternative(
                    label="only",
                    statement="only one statement",
                ),
            ),
        )


def test_conflict_does_not_change_experience_identity():
    experience = Experience.create()
    before = experience.experience_id

    conflict = ExperienceConflict.open(
        experience_id=before,
        alternatives=(
            ConflictAlternative(
                label="a",
                statement="claim A",
            ),
            ConflictAlternative(
                label="b",
                statement="claim B",
            ),
        ),
    )

    assert conflict.experience_id == before
    assert experience.experience_id == before


def test_ambiguity_can_remain_explicitly_unknown():
    experience = Experience.create()

    ambiguity = ExperienceAmbiguity(
        experience_id=experience.experience_id,
        description="available evidence does not determine the answer",
        confidence=None,
    )

    assert ambiguity.is_unknown is True
    assert ambiguity.confidence is None


def test_ambiguity_can_express_bounded_confidence_without_truth_claim():
    experience = Experience.create()

    ambiguity = ExperienceAmbiguity(
        experience_id=experience.experience_id,
        description="interpretation remains uncertain",
        confidence=0.65,
    )

    assert ambiguity.is_unknown is False
    assert ambiguity.confidence == 0.65


@pytest.mark.parametrize("confidence", [-0.01, 1.01, 2.0])
def test_invalid_confidence_is_rejected(confidence):
    experience = Experience.create()

    with pytest.raises(InvalidConfidenceError):
        ExperienceAmbiguity(
            experience_id=experience.experience_id,
            description="uncertain",
            confidence=confidence,
        )


def test_empty_ambiguity_description_is_rejected():
    experience = Experience.create()

    with pytest.raises(InvalidAmbiguityDescriptionError):
        ExperienceAmbiguity(
            experience_id=experience.experience_id,
            description="",
        )


def test_conflict_and_ambiguity_are_distinct_representations():
    experience = Experience.create()

    conflict = ExperienceConflict.open(
        experience_id=experience.experience_id,
        alternatives=(
            ConflictAlternative(
                label="a",
                statement="A",
            ),
            ConflictAlternative(
                label="b",
                statement="B",
            ),
        ),
    )

    ambiguity = ExperienceAmbiguity(
        experience_id=experience.experience_id,
        description="cannot determine which alternative is correct",
    )

    assert conflict.experience_id == ambiguity.experience_id
    assert type(conflict) is not type(ambiguity)


def test_phase_11_representation_does_not_mutate_experience():
    experience = Experience.create()

    before = (
        experience.experience_id,
        experience.created_at,
        experience.state,
    )

    ExperienceConflict.open(
        experience_id=experience.experience_id,
        alternatives=(
            ConflictAlternative(
                label="a",
                statement="A",
            ),
            ConflictAlternative(
                label="b",
                statement="B",
            ),
        ),
    )

    ExperienceAmbiguity(
        experience_id=experience.experience_id,
        description="unknown remains unknown",
    )

    after = (
        experience.experience_id,
        experience.created_at,
        experience.state,
    )

    assert after == before
PY

python -m py_compile \
    "$CONFLICT" \
    "$AMBIGUITY" \
    "$TEST" || fail $?

echo "PASS: syntax"

python -m pytest -q "$TEST" || fail $?

echo "PASS: dedicated Conflict/Ambiguity physiology"

echo
echo "[7/9] Execute complete Experience regression"

python -m pytest -q tests/experience || fail $?

echo "PASS: complete Experience regression"

echo
echo "[8/9] Generate autosufficient epic-thread MD"

git diff --check -- \
    "$CONFLICT" \
    "$AMBIGUITY" \
    "$TEST" || fail $?

{
    echo "# PCC-01 — RUN 046 — Conflict and Ambiguity"
    echo
    echo "## Capability"
    echo
    echo "PCC-01 — Persistent Experience"
    echo
    echo "## Build Phase"
    echo
    echo "Phase 11 — Conflict and ambiguity"
    echo
    echo "## Verified baseline"
    echo
    echo "\`$BASE\`"
    echo
    echo "## Contract-derived physiology"
    echo
    echo "- conflict remains explicitly representable"
    echo "- conflicting alternatives are preserved"
    echo "- conflict representation does not silently erase a version"
    echo "- ambiguity remains explicitly representable"
    echo "- unknown may remain unknown"
    echo "- confidence is explicit and is not truth"
    echo "- Conflict != Ambiguity"
    echo
    echo "## Implemented tissue"
    echo
    echo "- \`$CONFLICT\`"
    echo "- \`$AMBIGUITY\`"
    echo "- \`$TEST\`"
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
    echo "## Boundary"
    echo
    echo "RUN 046 implements representation only."
    echo
    echo "It does not fabricate automatic conflict resolution."
    echo
    echo "It does not fabricate certainty from ambiguity."
    echo
    echo "## Epistemic status before conservation"
    echo
    echo "- Conflict representation: DEMONSTRATED LOCALLY"
    echo "- Ambiguity representation: DEMONSTRATED LOCALLY"
    echo "- whole PCC-01: NOT YET CLAIMED"
} > "$REPORT"

[ -s "$REPORT" ] || fail 1

echo "PASS: autosufficient RUN 046 MD generated"

echo
echo "[9/9] Conserve exact Phase 11 evidence"

git add -- \
    "$CONFLICT" \
    "$AMBIGUITY" \
    "$TEST" \
    "$REPORT" || fail $?

ACTUAL="$(git diff --cached --name-only | sort)"

EXPECTED="$(
    printf '%s\n' \
        "$CONFLICT" \
        "$AMBIGUITY" \
        "$TEST" \
        "$REPORT" \
    | sort
)"

if [ "$ACTUAL" != "$EXPECTED" ]; then
    echo "ERROR: staged boundary mismatch"
    echo "EXPECTED:"
    printf '%s\n' "$EXPECTED"
    echo "ACTUAL:"
    printf '%s\n' "$ACTUAL"
    git reset --quiet
    fail 1
fi

git commit -m \
    "feat: implement PCC-01 conflict and ambiguity representation" || fail $?

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
    echo "## Final RUN 046 conclusion"
    echo
    echo "**Conflict and Ambiguity representation: IMPLEMENTED + DEMONSTRATED + CONSERVED**"
    echo
    echo "No automatic resolution or fabricated certainty was introduced."
    echo
    echo "RUN 046 does not declare whole PCC-01 CANON or PRODUCTION-READY."
    echo
    echo "---"
    echo
    echo "END OF PCC-01 RUN 046"
} >> "$REPORT"

git add -- "$REPORT" || fail $?

git commit -m \
    "docs: finalize PCC-01 RUN 046 evidence" || fail $?

FINAL_HEAD="$(git rev-parse HEAD)" || fail $?

git push origin main || fail $?
git fetch origin main --quiet || fail $?

FINAL_REMOTE="$(git rev-parse origin/main)" || fail $?

[ "$FINAL_HEAD" = "$FINAL_REMOTE" ] || fail 1

echo
echo "=========================================================="
echo "RUN 046 COMPLETE"
echo "=========================================================="
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
echo "CONFLICT REPRESENTATION:"
echo "IMPLEMENTED + DEMONSTRATED + CONSERVED"
echo
echo "AMBIGUITY REPRESENTATION:"
echo "IMPLEMENTED + DEMONSTRATED + CONSERVED"
echo
echo "EPIC-THREAD MD:"
echo "$REPORT"
echo
echo "NEXT CONTRACT PHASE:"
echo "PHASE 12 — EVIDENCE"
echo
echo "NEXT:"
echo "GPT verifies GitHub directly before deriving RUN 047."
echo "=========================================================="
```

## Terminal output — complete

```text
==========================================================
PCC-01
CONFLICT AND AMBIGUITY — RUN 046
EVIDENCE-DERIVED IMPLEMENTATION
==========================================================

[1/9] Verify GitHub-authoritative baseline
Expected:    ea342aeca6ae6f2cb36912c04f963ad3c028b3b8
LOCAL:       ea342aeca6ae6f2cb36912c04f963ad3c028b3b8
origin/main: ea342aeca6ae6f2cb36912c04f963ad3c028b3b8
PASS: tracked/staged authority clean

PRE-EXISTING UNTRACKED HISTORICAL ARTIFACTS:
tests/experience/harness/pcc01_coordination_crash_reconciler.py
tests/experience/harness/pcc01_coordination_crash_writer.py
work/implementation-reports/PCC-01/PCC-01_RUN034C_FAILURE_RECOVERY_AND_EXACT_INTEGRATION_ANATOMY.md
work/implementation-reports/PCC-01/PCC-01_RUN034D_EXACT_LOCAL_JOURNAL_ANATOMY_FOR_INTEGRATION.md
work/implementation-reports/PCC-01/PCC-01_RUN038A_HARNESS_CAUSAL_CORRECTION.md
work/implementation-reports/PCC-01/PCC-01_RUN043B_LOCAL_ARTIFACT_STATE_INSPECTION.md

They remain outside RUN 046 conservation.

[2/9] Verify accepted Phase 11 authority
PASS: Phase 11 authorized
PASS: conflict must remain representable
PASS: ambiguity must remain representable
PASS: conflict must not silently erase alternatives
PASS: unknown may remain unknown

[3/9] Verify no duplicate Phase 11 organs
PASS: no duplicate Phase 11 organs

[4/9] Build Conflict representation
PASS: Conflict representation built

[5/9] Build Ambiguity representation
PASS: Ambiguity representation built

[6/9] Build contract-derived behavioral examinations
PASS: syntax
...........                                                              [100%]
11 passed in 0.34s
PASS: dedicated Conflict/Ambiguity physiology

[7/9] Execute complete Experience regression
........................................................................ [ 38%]
........................................................................ [ 77%]
.........................................                                [100%]
185 passed in 3.43s
PASS: complete Experience regression

[8/9] Generate autosufficient epic-thread MD
```

## Boundary

RUN 046 implements representation only.

It does not fabricate automatic conflict resolution.

It does not fabricate certainty from ambiguity.

## Epistemic status before conservation

- Conflict representation: DEMONSTRATED LOCALLY
- Ambiguity representation: DEMONSTRATED LOCALLY
- whole PCC-01: NOT YET CLAIMED

## Git conservation

- Baseline: `ea342aeca6ae6f2cb36912c04f963ad3c028b3b8`
- Implementation commit: `aebea0ae5e655fc5a984aba3ea79fc599398542a`
- origin/main synchronization: PASS

## Final RUN 046 conclusion

**Conflict and Ambiguity representation: IMPLEMENTED + DEMONSTRATED + CONSERVED**

No automatic resolution or fabricated certainty was introduced.

RUN 046 does not declare whole PCC-01 CANON or PRODUCTION-READY.

---

END OF PCC-01 RUN 046

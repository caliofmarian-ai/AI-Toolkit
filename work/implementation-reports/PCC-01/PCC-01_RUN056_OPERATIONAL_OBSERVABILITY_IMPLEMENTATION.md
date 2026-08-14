# PCC-01 — RUN 056 — Operational Observability Implementation

## Purpose

Resolve the Production-Ready operational observability gap identified by RUN 052.

## Git authority

- Baseline: `b3ab6ef5c21e68ca19087a5e5c2c778f9008aec0`
- Local HEAD: `b3ab6ef5c21e68ca19087a5e5c2c778f9008aec0`
- origin/main: `b3ab6ef5c21e68ca19087a5e5c2c778f9008aec0`

## Evidence-derived anatomy

The existing persistence coordinator already exposes physiological coordination stages.

The existing Durable Coordination Journal already persists operation identity, Experience identity, stage, creation time, update time, and incomplete-operation state.

RUN 056 therefore does not create a parallel logging or persistence mechanism.

## Implemented physiology

- read-only PCC-01 operational observer
- machine-inspectable operational snapshot
- total operation count
- incomplete operation count
- complete operation count
- per-stage incomplete counts
- explicit healthy/unhealthy condition
- Experience-scoped durable history
- direct visibility of incomplete operations requiring attention
- observation does not mutate durable evidence
- observation does not redefine Experience identity

## Governance result

operational observability: **IMPLEMENTED + DEMONSTRATED + CONSERVED**

PCC-01: **IMPLEMENTED**

PCC-01 Production-Ready: **NOT YET DECLARED**

Remaining Production-Ready concerns:

- performance
- deployment behavior

PCC-01 canonical status: **NOT CANON**

## Implementation diff

```diff
```

## Bash executed — complete

```bash
#!/data/data/com.termux/files/usr/bin/bash
set -uo pipefail

cd "$HOME/storage/shared/AI-Projects/AI-Toolkit" || exit 1

export GIT_PAGER=cat
export GH_PAGER=cat
export PAGER=cat
export PYTHONPATH="$PWD:$PWD/lib${PYTHONPATH:+:$PYTHONPATH}"

BASE="b3ab6ef5c21e68ca19087a5e5c2c778f9008aec0"

OBS="lib/python/experience/operational_observability.py"
TEST="tests/experience/test_experience_operational_observability.py"
REPORT="work/implementation-reports/PCC-01/PCC-01_RUN056_OPERATIONAL_OBSERVABILITY_IMPLEMENTATION.md"

SELF="$PREFIX/tmp/pcc01_run056.sh"
OUT="$PREFIX/tmp/pcc01_run056.output"

: > "$OUT"
exec > >(tee -a "$OUT") 2>&1

fail() {
    code="${1:-1}"

    echo
    echo "=========================================================="
    echo "RUN 056 STOPPED SAFELY"
    echo "=========================================================="
    echo "Exit code: $code"
    echo "NO commit/push after failure"
    echo "PCC-01 remains IMPLEMENTED"
    echo "Production-Ready remains NOT DECLARED"
    echo "=========================================================="

    exit "$code"
}

echo "=========================================================="
echo "PCC-01 — RUN 056"
echo "OPERATIONAL OBSERVABILITY"
echo "EVIDENCE-DERIVED IMPLEMENTATION"
echo "=========================================================="

echo
echo "[1/9] Verify synchronized Git authority"

git fetch origin main --quiet || fail $?

LOCAL="$(git rev-parse HEAD)"
REMOTE="$(git rev-parse origin/main)"

echo "Expected:    $BASE"
echo "LOCAL:       $LOCAL"
echo "origin/main: $REMOTE"

[ "$LOCAL" = "$BASE" ] || fail 1
[ "$REMOTE" = "$BASE" ] || fail 1

[ -z "$(git diff --name-only)" ] || {
    echo "ERROR: tracked working tree not clean"
    git diff --name-only
    fail 1
}

[ -z "$(git diff --cached --name-only)" ] || {
    echo "ERROR: staging area not clean"
    git diff --cached --name-only
    fail 1
}

echo "PASS: Git authority"

echo
echo "[2/9] Verify inherited observable physiology"

python - <<'PY'
from lib.python.experience.persistence_coordinator import (
    CoordinationStage,
    CoordinationState,
    ExperiencePersistenceCoordinator,
)
from lib.python.experience.coordination_journal import (
    DurableCoordinationRecord,
    DurableCoordinationStage,
    JsonFileCoordinationJournal,
)

assert tuple(stage.value for stage in CoordinationStage) == (
    "preparing",
    "protection_written",
    "experience_written",
    "complete",
)

assert tuple(stage.value for stage in DurableCoordinationStage) == (
    "preparing",
    "protection_written",
    "experience_written",
    "complete",
)

assert hasattr(JsonFileCoordinationJournal, "records_for_experience")
assert hasattr(JsonFileCoordinationJournal, "incomplete_records")

print("PASS: coordinator exposes physiological stages")
print("PASS: durable journal exposes matching durable stages")
print("PASS: journal exposes records_for_experience")
print("PASS: journal exposes incomplete_records")
print("PASS: existing durable evidence is the observability source")
PY

[ $? -eq 0 ] || fail $?

echo
echo "[3/9] Verify no duplicate operational observability organ"

[ ! -e "$OBS" ] || {
    echo "ERROR: operational observability organ already exists"
    fail 1
}

[ ! -e "$TEST" ] || {
    echo "ERROR: operational observability test already exists"
    fail 1
}

echo "PASS: no duplicate PCC-01 operational observability organ"

echo
echo "[4/9] Build read-only operational observability organ"

cat > "$OBS" <<'PY'
"""Operational observability for PCC-01 Persistent Experience.

This organ does not become Experience, Protection, persistence, or the
Durable Coordination Journal.

It reads existing durable coordination evidence and presents a compact
operational snapshot suitable for diagnosis.

Observation != authority.
Observation != mutation.
Metrics != Experience.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from .coordination_journal import (
    DurableCoordinationRecord,
    DurableCoordinationStage,
    JsonFileCoordinationJournal,
)
from .identity import ExperienceId


class ExperienceOperationalObservabilityError(RuntimeError):
    """Base error for PCC-01 operational observation."""


@dataclass(frozen=True, slots=True)
class ExperienceOperationalSnapshot:
    """Read-only operational condition derived from durable evidence."""

    observed_at: datetime
    total_operations: int
    incomplete_operations: int
    complete_operations: int
    preparing_operations: int
    protection_written_operations: int
    experience_written_operations: int

    @property
    def healthy(self) -> bool:
        """A snapshot is healthy when no durable operation is incomplete."""

        return self.incomplete_operations == 0

    def to_dict(self) -> dict[str, object]:
        return {
            "observed_at": self.observed_at.isoformat(),
            "healthy": self.healthy,
            "total_operations": self.total_operations,
            "incomplete_operations": self.incomplete_operations,
            "complete_operations": self.complete_operations,
            "preparing_operations": self.preparing_operations,
            "protection_written_operations": (
                self.protection_written_operations
            ),
            "experience_written_operations": (
                self.experience_written_operations
            ),
        }


class ExperienceOperationalObserver:
    """Read durable PCC-01 coordination evidence without mutating it."""

    def __init__(
        self,
        coordination_journal: JsonFileCoordinationJournal,
    ) -> None:
        if not isinstance(
            coordination_journal,
            JsonFileCoordinationJournal,
        ):
            raise TypeError(
                "coordination_journal must be JsonFileCoordinationJournal"
            )

        self._coordination_journal = coordination_journal

    def snapshot(self) -> ExperienceOperationalSnapshot:
        """Describe the current durable coordination condition."""

        records = self._all_records()

        counts = {
            stage: 0
            for stage in DurableCoordinationStage
        }

        for record in records:
            counts[record.stage] += 1

        incomplete = sum(
            count
            for stage, count in counts.items()
            if stage is not DurableCoordinationStage.COMPLETE
        )

        return ExperienceOperationalSnapshot(
            observed_at=datetime.now(timezone.utc),
            total_operations=len(records),
            incomplete_operations=incomplete,
            complete_operations=counts[
                DurableCoordinationStage.COMPLETE
            ],
            preparing_operations=counts[
                DurableCoordinationStage.PREPARING
            ],
            protection_written_operations=counts[
                DurableCoordinationStage.PROTECTION_WRITTEN
            ],
            experience_written_operations=counts[
                DurableCoordinationStage.EXPERIENCE_WRITTEN
            ],
        )

    def records_for_experience(
        self,
        experience_id: ExperienceId,
    ) -> tuple[DurableCoordinationRecord, ...]:
        """Expose durable coordination history for one Experience."""

        if not isinstance(experience_id, ExperienceId):
            raise TypeError("experience_id must be ExperienceId")

        return self._coordination_journal.records_for_experience(
            experience_id
        )

    def incomplete_records(
        self,
    ) -> tuple[DurableCoordinationRecord, ...]:
        """Expose durable operations requiring operational attention."""

        return self._coordination_journal.incomplete_records()

    def _all_records(
        self,
    ) -> tuple[DurableCoordinationRecord, ...]:
        """Read journal records through its durable representation.

        The journal owns storage. This observer only derives operational
        state from the journal's persisted records.
        """

        store = self._coordination_journal._read_store()

        return tuple(
            DurableCoordinationRecord.from_dict(payload)
            for payload in store.values()
        )
PY

python -m py_compile "$OBS" || fail $?

echo "PASS: operational observability organ syntax"

echo
echo "[5/9] Build behavioral examination"

cat > "$TEST" <<'PY'
from lib.python.experience.coordination_journal import (
    DurableCoordinationStage,
    JsonFileCoordinationJournal,
)
from lib.python.experience.model import Experience
from lib.python.experience.operational_observability import (
    ExperienceOperationalObserver,
)


def _observer(tmp_path):
    journal = JsonFileCoordinationJournal(
        tmp_path / "coordination.json"
    )
    return journal, ExperienceOperationalObserver(journal)


def test_empty_journal_is_observably_healthy(tmp_path):
    _, observer = _observer(tmp_path)

    snapshot = observer.snapshot()

    assert snapshot.total_operations == 0
    assert snapshot.incomplete_operations == 0
    assert snapshot.complete_operations == 0
    assert snapshot.healthy is True


def test_preparing_operation_is_observably_incomplete(tmp_path):
    journal, observer = _observer(tmp_path)
    experience = Experience.create()

    journal.begin(experience.experience_id)

    snapshot = observer.snapshot()

    assert snapshot.total_operations == 1
    assert snapshot.incomplete_operations == 1
    assert snapshot.preparing_operations == 1
    assert snapshot.complete_operations == 0
    assert snapshot.healthy is False


def test_complete_operation_is_observably_healthy(tmp_path):
    journal, observer = _observer(tmp_path)
    experience = Experience.create()

    record = journal.begin(experience.experience_id)

    record = journal.advance(
        record.coordination_operation_id,
        DurableCoordinationStage.PROTECTION_WRITTEN,
    )
    record = journal.advance(
        record.coordination_operation_id,
        DurableCoordinationStage.EXPERIENCE_WRITTEN,
    )
    journal.advance(
        record.coordination_operation_id,
        DurableCoordinationStage.COMPLETE,
    )

    snapshot = observer.snapshot()

    assert snapshot.total_operations == 1
    assert snapshot.incomplete_operations == 0
    assert snapshot.complete_operations == 1
    assert snapshot.healthy is True


def test_snapshot_counts_each_incomplete_stage(tmp_path):
    journal, observer = _observer(tmp_path)

    preparing = journal.begin(
        Experience.create().experience_id
    )

    protection = journal.begin(
        Experience.create().experience_id
    )
    journal.advance(
        protection.coordination_operation_id,
        DurableCoordinationStage.PROTECTION_WRITTEN,
    )

    experience_written = journal.begin(
        Experience.create().experience_id
    )
    experience_written = journal.advance(
        experience_written.coordination_operation_id,
        DurableCoordinationStage.PROTECTION_WRITTEN,
    )
    journal.advance(
        experience_written.coordination_operation_id,
        DurableCoordinationStage.EXPERIENCE_WRITTEN,
    )

    snapshot = observer.snapshot()

    assert preparing is not None
    assert snapshot.total_operations == 3
    assert snapshot.incomplete_operations == 3
    assert snapshot.preparing_operations == 1
    assert snapshot.protection_written_operations == 1
    assert snapshot.experience_written_operations == 1
    assert snapshot.complete_operations == 0
    assert snapshot.healthy is False


def test_snapshot_dictionary_is_machine_inspectable(tmp_path):
    journal, observer = _observer(tmp_path)
    journal.begin(Experience.create().experience_id)

    payload = observer.snapshot().to_dict()

    assert set(payload) == {
        "observed_at",
        "healthy",
        "total_operations",
        "incomplete_operations",
        "complete_operations",
        "preparing_operations",
        "protection_written_operations",
        "experience_written_operations",
    }
    assert payload["healthy"] is False
    assert payload["total_operations"] == 1


def test_records_for_experience_are_scoped(tmp_path):
    journal, observer = _observer(tmp_path)

    target = Experience.create()
    other = Experience.create()

    target_record = journal.begin(target.experience_id)
    journal.begin(other.experience_id)

    records = observer.records_for_experience(
        target.experience_id
    )

    assert len(records) == 1
    assert (
        records[0].coordination_operation_id
        == target_record.coordination_operation_id
    )
    assert records[0].experience_id == target.experience_id


def test_incomplete_records_expose_attention_required_operations(
    tmp_path,
):
    journal, observer = _observer(tmp_path)

    incomplete = journal.begin(
        Experience.create().experience_id
    )

    complete = journal.begin(
        Experience.create().experience_id
    )
    complete = journal.advance(
        complete.coordination_operation_id,
        DurableCoordinationStage.PROTECTION_WRITTEN,
    )
    complete = journal.advance(
        complete.coordination_operation_id,
        DurableCoordinationStage.EXPERIENCE_WRITTEN,
    )
    journal.advance(
        complete.coordination_operation_id,
        DurableCoordinationStage.COMPLETE,
    )

    records = observer.incomplete_records()

    assert len(records) == 1
    assert (
        records[0].coordination_operation_id
        == incomplete.coordination_operation_id
    )


def test_observation_does_not_mutate_durable_records(tmp_path):
    journal, observer = _observer(tmp_path)

    record = journal.begin(
        Experience.create().experience_id
    )

    before = journal.get(record.coordination_operation_id)

    observer.snapshot()
    observer.records_for_experience(record.experience_id)
    observer.incomplete_records()

    after = journal.get(record.coordination_operation_id)

    assert after == before


def test_observation_does_not_change_experience_identity(tmp_path):
    journal, observer = _observer(tmp_path)

    experience = Experience.create()
    before = experience.experience_id

    journal.begin(experience.experience_id)
    observer.snapshot()

    assert experience.experience_id == before


def test_observer_requires_real_durable_coordination_journal():
    try:
        ExperienceOperationalObserver(object())
    except TypeError:
        pass
    else:
        raise AssertionError(
            "observer accepted a non-journal dependency"
        )
PY

python -m py_compile "$TEST" || fail $?

echo "PASS: behavioral examination syntax"

echo
echo "[6/9] Execute dedicated operational observability tests"

python -m pytest -q \
    "$TEST" \
    tests/experience/test_experience_coordination_journal.py \
    tests/experience/test_experience_persistence_coordinator.py || fail $?

echo "PASS: dedicated observability physiology"

echo
echo "[7/9] Execute complete Experience regression"

python -m pytest -q tests/experience || fail $?

echo "PASS: complete Experience regression"

echo
echo "[8/9] Verify mutation boundary and build autosufficient epic-thread"

EXPECTED="$PREFIX/tmp/pcc01_run056.expected"
ACTUAL="$PREFIX/tmp/pcc01_run056.actual"

cat > "$EXPECTED" <<EOF
$OBS
$TEST
EOF

{
    git diff --name-only
    git ls-files --others --exclude-standard -- "$OBS" "$TEST"
} | sort -u > "$ACTUAL"

sort -o "$EXPECTED" "$EXPECTED"

if ! diff -u "$EXPECTED" "$ACTUAL"; then
    echo "ERROR: mutation outside RUN 056 boundary"
    fail 1
fi

echo "PASS: exact mutation boundary"

mkdir -p "$(dirname "$REPORT")"

{
    echo "# PCC-01 — RUN 056 — Operational Observability Implementation"
    echo
    echo "## Purpose"
    echo
    echo "Resolve the Production-Ready operational observability gap identified by RUN 052."
    echo
    echo "## Git authority"
    echo
    echo "- Baseline: \`$BASE\`"
    echo "- Local HEAD: \`$LOCAL\`"
    echo "- origin/main: \`$REMOTE\`"
    echo
    echo "## Evidence-derived anatomy"
    echo
    echo "The existing persistence coordinator already exposes physiological coordination stages."
    echo
    echo "The existing Durable Coordination Journal already persists operation identity, Experience identity, stage, creation time, update time, and incomplete-operation state."
    echo
    echo "RUN 056 therefore does not create a parallel logging or persistence mechanism."
    echo
    echo "## Implemented physiology"
    echo
    echo "- read-only PCC-01 operational observer"
    echo "- machine-inspectable operational snapshot"
    echo "- total operation count"
    echo "- incomplete operation count"
    echo "- complete operation count"
    echo "- per-stage incomplete counts"
    echo "- explicit healthy/unhealthy condition"
    echo "- Experience-scoped durable history"
    echo "- direct visibility of incomplete operations requiring attention"
    echo "- observation does not mutate durable evidence"
    echo "- observation does not redefine Experience identity"
    echo
    echo "## Governance result"
    echo
    echo "operational observability: **IMPLEMENTED + DEMONSTRATED + CONSERVED**"
    echo
    echo "PCC-01: **IMPLEMENTED**"
    echo
    echo "PCC-01 Production-Ready: **NOT YET DECLARED**"
    echo
    echo "Remaining Production-Ready concerns:"
    echo
    echo "- performance"
    echo "- deployment behavior"
    echo
    echo "PCC-01 canonical status: **NOT CANON**"
    echo
    echo "## Implementation diff"
    echo
    echo '```diff'
    git diff -- "$OBS" "$TEST"
    echo '```'
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
} > "$REPORT"

python - "$REPORT" <<'PY'
from pathlib import Path
import sys

path = Path(sys.argv[1])
text = path.read_text(encoding="utf-8")
clean = "\n".join(
    line.rstrip(" \t")
    for line in text.splitlines()
)

if text.endswith("\n"):
    clean += "\n"

path.write_text(clean, encoding="utf-8")
PY

[ -s "$REPORT" ] || fail 1

echo "PASS: autosufficient epic-thread generated"
sha256sum "$REPORT"

echo
echo "[9/9] Conserve implementation and evidence in GitHub"

git add -- "$OBS" "$TEST" "$REPORT" || fail $?

EXPECTED_STAGED="$PREFIX/tmp/pcc01_run056.expected_staged"
ACTUAL_STAGED="$PREFIX/tmp/pcc01_run056.actual_staged"

{
    cat "$EXPECTED"
    echo "$REPORT"
} | sort > "$EXPECTED_STAGED"

git diff --cached --name-only | sort > "$ACTUAL_STAGED"

if ! diff -u "$EXPECTED_STAGED" "$ACTUAL_STAGED"; then
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
    "feat: add PCC-01 operational observability" || fail $?

FINAL_HEAD="$(git rev-parse HEAD)"

git push origin main || fail $?
git fetch origin main --quiet || fail $?

FINAL_REMOTE="$(git rev-parse origin/main)"

[ "$FINAL_HEAD" = "$FINAL_REMOTE" ] || fail 1

echo
echo "=========================================================="
echo "RUN 056 COMPLETE"
echo "=========================================================="
echo
echo "FINAL HEAD:"
echo "$FINAL_HEAD"
echo
echo "LOCAL == origin/main:"
echo "PASS"
echo
echo "OPERATIONAL OBSERVABILITY:"
echo "IMPLEMENTED + DEMONSTRATED + CONSERVED"
echo
echo "REMAINING PRODUCTION CONCERNS:"
echo "2"
echo
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
echo "GPT verifies RUN 056 directly in GitHub before deriving RUN 057."
echo "=========================================================="
```

## Terminal output — complete

```text
==========================================================
PCC-01 — RUN 056
OPERATIONAL OBSERVABILITY
EVIDENCE-DERIVED IMPLEMENTATION
==========================================================

[1/9] Verify synchronized Git authority
Expected:    b3ab6ef5c21e68ca19087a5e5c2c778f9008aec0
LOCAL:       b3ab6ef5c21e68ca19087a5e5c2c778f9008aec0
origin/main: b3ab6ef5c21e68ca19087a5e5c2c778f9008aec0
PASS: Git authority

[2/9] Verify inherited observable physiology
PASS: coordinator exposes physiological stages
PASS: durable journal exposes matching durable stages
PASS: journal exposes records_for_experience
PASS: journal exposes incomplete_records
PASS: existing durable evidence is the observability source

[3/9] Verify no duplicate operational observability organ
PASS: no duplicate PCC-01 operational observability organ

[4/9] Build read-only operational observability organ
PASS: operational observability organ syntax

[5/9] Build behavioral examination
PASS: behavioral examination syntax

[6/9] Execute dedicated operational observability tests
..............................                                           [100%]
30 passed in 0.91s
PASS: dedicated observability physiology

[7/9] Execute complete Experience regression
........................................................................ [ 31%]
........................................................................ [ 63%]
........................................................................ [ 94%]
............                                                             [100%]
228 passed in 3.67s
PASS: complete Experience regression

[8/9] Verify mutation boundary and build autosufficient epic-thread
PASS: exact mutation boundary
```

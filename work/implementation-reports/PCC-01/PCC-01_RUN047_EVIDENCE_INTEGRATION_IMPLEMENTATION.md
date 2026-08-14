# PCC-01 — RUN 047 — Evidence Integration

## Capability

PCC-01 — Persistent Experience

## Build Phase

Phase 12 — Evidence

## Git Authority

- Baseline: `efc1ecdeed5c3b47bb55fb1885d57d7b433e7f1e`
- Local HEAD before conservation: `efc1ecdeed5c3b47bb55fb1885d57d7b433e7f1e`
- origin/main before conservation: `efc1ecdeed5c3b47bb55fb1885d57d7b433e7f1e`

## Evidence-derived anatomy

- Existing organ: `lib/python/evidence_engine/engine.py`
- Existing class: `EvidenceEngine`
- Existing Evidence Engine remains authoritative
- No parallel Evidence Engine was created

## Integration physiology

```text
Experience identity
        |
        v
ExperienceEvidenceIntegrator
        |
        v
existing EvidenceEngine.find(keyword)
        |
        v
ExperienceEvidenceReference
```

## Conserved epistemic boundaries

- Experience remains Experience
- Evidence remains Evidence
- Evidence does not redefine Experience identity
- absence of Evidence remains explicit
- Evidence integration does not fabricate Evidence

## Implemented artifacts

- `lib/python/experience/evidence_integration.py`
  - SHA-256: `8fa3bbed1a5871cb8040969c356af6c14506299474017af14383e3f55d950baf`
- `tests/experience/test_experience_evidence_integration.py`
  - SHA-256: `af07beaf12bb98e17a445e2c2ace111258b6c81503f5a5cb4b9b60447043db6e`

## Demonstrated behavioral evidence

- dedicated Evidence Integration examinations: **9/9 PASS**
- complete Experience regression: **194/194 PASS**
- Experience -> Evidence integration: PASS
- inherited EvidenceEngine conservation: PASS
- Experience identity conservation: PASS
- absence of Evidence remains explicit: PASS

## RUN 047 procedural failure

Behavioral implementation did not fail.


The original RUN 047 stopped after all behavioral examinations passed because its mutation-boundary check used:

```text
git diff --name-only
```

That command does not enumerate newly-created untracked files.

Therefore the check incorrectly observed an empty ACTUAL set even though both demonstrated RUN 047 artifacts existed locally.

RUN 047A corrects only the conservation physiology by inspecting new files through:

```text
git ls-files --others --exclude-standard
```

No behavioral test is re-executed.

## Original RUN 047 Bash — Complete

```bash
#!/data/data/com.termux/files/usr/bin/bash
set -uo pipefail

export GIT_PAGER=cat
export PAGER=cat
export GH_PAGER=cat

cd "$HOME/storage/shared/AI-Projects/AI-Toolkit" || exit 1

# Repository package physiology:
# existing engines import through the top-level `python` package
# rooted at repository/lib.
export PYTHONPATH="$PWD/lib${PYTHONPATH:+:$PYTHONPATH}"

BASE="efc1ecdeed5c3b47bb55fb1885d57d7b433e7f1e"

INTEGRATION="lib/python/experience/evidence_integration.py"
TEST="tests/experience/test_experience_evidence_integration.py"
REPORT="work/implementation-reports/PCC-01/PCC-01_RUN047_EVIDENCE_INTEGRATION_IMPLEMENTATION.md"

SELF="$PREFIX/tmp/pcc01_run047.sh"
OUT="$PREFIX/tmp/pcc01_run047.output"

mkdir -p "$(dirname "$REPORT")"
: > "$OUT"

exec > >(tee -a "$OUT") 2>&1

fail() {
    CODE="${1:-1}"

    echo
    echo "=========================================================="
    echo "RUN 047 STOPPED SAFELY"
    echo "=========================================================="
    echo "Exit code: $CODE"
    echo "NO commit/push after failure"
    echo "=========================================================="

    exit "$CODE"
}

echo "=========================================================="
echo "PCC-01"
echo "EVIDENCE INTEGRATION — RUN 047"
echo "EVIDENCE-DERIVED IMPLEMENTATION"
echo "=========================================================="

echo
echo "[1/10] Verify GitHub-authoritative baseline"

git fetch origin main --quiet || fail $?

LOCAL="$(git rev-parse HEAD)" || fail $?
REMOTE="$(git rev-parse origin/main)" || fail $?

echo "Expected:    $BASE"
echo "LOCAL:       $LOCAL"
echo "origin/main: $REMOTE"

[ "$LOCAL" = "$BASE" ] || {
    echo "ERROR: local HEAD differs from verified RUN 046 authority"
    fail 1
}

[ "$REMOTE" = "$BASE" ] || {
    echo "ERROR: origin/main differs from verified RUN 046 authority"
    fail 1
}

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

echo "PASS: tracked/staged Git authority clean"

UNTRACKED_BEFORE="$(git ls-files --others --exclude-standard | sort)"

if [ -n "$UNTRACKED_BEFORE" ]; then
    echo
    echo "PRE-EXISTING UNTRACKED HISTORICAL ARTIFACTS:"
    printf '%s\n' "$UNTRACKED_BEFORE"
    echo
    echo "These remain outside RUN 047."
    echo "They will not be staged, committed, deleted, or modified."
fi

echo
echo "[2/10] Verify accepted PCC-01 authority and inherited Evidence organ"

PLAN="work/planning/PCC-01_IMPLEMENTATION_INVENTORY_AND_BUILD_PLAN.md"
ACCEPTED="work/decisions/PCC-01_IMPLEMENTATION_INVENTORY_AND_BUILD_PLAN_HUMAN_ACCEPTANCE_2026-08-13.md"
EVIDENCE_ENGINE="lib/python/evidence_engine/engine.py"
EXPERIENCE_MODEL="lib/python/experience/model.py"
EXPERIENCE_IDENTITY="lib/python/experience/identity.py"

for FILE in \
    "$PLAN" \
    "$ACCEPTED" \
    "$EVIDENCE_ENGINE" \
    "$EXPERIENCE_MODEL" \
    "$EXPERIENCE_IDENTITY"
do
    [ -s "$FILE" ] || {
        echo "ERROR: required authority/anatomy missing:"
        echo "$FILE"
        fail 1
    }
done

grep -Fq "Build Phase 12 — Evidence" "$PLAN" || {
    echo "ERROR: Phase 12 authority not found"
    fail 1
}

grep -Fq "Evidence integration" "$PLAN" || {
    echo "ERROR: Evidence integration requirement not found"
    fail 1
}

grep -Fq "class EvidenceEngine" "$EVIDENCE_ENGINE" || {
    echo "ERROR: inherited EvidenceEngine anatomy changed"
    fail 1
}

echo "PASS: Phase 12 authority"
echo "PASS: existing EvidenceEngine detected"
echo "PASS: RUN 047 will integrate; it will not create a parallel Evidence Engine"

echo
echo "[3/10] Inspect exact live APIs before mutation"

python - <<'PY' || fail $?
import inspect

from lib.python.evidence_engine.engine import EvidenceEngine
from lib.python.experience.identity import ExperienceId
from lib.python.experience.model import Experience

print("EvidenceEngine:")
print(inspect.signature(EvidenceEngine))

print("EvidenceEngine.find:")
print(inspect.signature(EvidenceEngine.find))

print("Experience.create:")
print(inspect.signature(Experience.create))

experience = Experience.create()

print("Experience ID type:")
print(type(experience.experience_id).__name__)

print("Experience ID:")
print(experience.experience_id)

assert isinstance(experience.experience_id, ExperienceId)

print("PASS: live Experience identity physiology")
print("PASS: live EvidenceEngine physiology")
PY

echo
echo "[4/10] Verify no duplicate PCC-01 Evidence integration organ"

for FILE in "$INTEGRATION" "$TEST"; do
    if git cat-file -e "HEAD:$FILE" 2>/dev/null; then
        echo "ERROR: RUN 047 target already exists in Git authority:"
        echo "$FILE"
        fail 1
    fi
done

echo "PASS: no duplicate PCC-01 Evidence integration organ"

echo
echo "[5/10] Build Experience-to-Evidence integration tissue"

cat > "$INTEGRATION" <<'PY'
"""PCC-01 Experience integration with the inherited Evidence Engine.

This module is connective tissue.

It does not create another Evidence Engine.
It does not redefine Experience.
It does not redefine ExperienceId.
It does not make Evidence become Experience.

The relationship is referential:

    Experience identity -> Evidence query -> Evidence result

Evidence may inform an Experience while remaining evidence.
Experience may refer to evidence while remaining Experience.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from lib.python.evidence_engine.engine import EvidenceEngine

from .identity import ExperienceId


class ExperienceEvidenceIntegrationError(Exception):
    """Base error for PCC-01 Evidence integration."""


class InvalidEvidenceKeywordError(ExperienceEvidenceIntegrationError):
    """Raised when an Evidence query keyword is invalid."""


@dataclass(frozen=True, slots=True)
class ExperienceEvidenceReference:
    """Evidence discovered for one conserved Experience identity."""

    experience_id: ExperienceId
    keyword: str
    evidence: Mapping[str, Any]

    def __post_init__(self) -> None:
        if not isinstance(self.experience_id, ExperienceId):
            raise TypeError("experience_id must be an ExperienceId")

        if not isinstance(self.keyword, str) or not self.keyword.strip():
            raise InvalidEvidenceKeywordError(
                "evidence keyword must be a non-empty string"
            )

        if not isinstance(self.evidence, Mapping):
            raise TypeError("evidence must be a mapping")

    @property
    def has_evidence(self) -> bool:
        """Return whether the inherited Evidence Engine found evidence."""

        for key, value in self.evidence.items():
            if key == "semantic":
                if isinstance(value, Mapping) and value:
                    return True
                continue

            if isinstance(value, (list, tuple, set)) and value:
                return True

            if isinstance(value, Mapping) and value:
                return True

        return False


class ExperienceEvidenceIntegrator:
    """Bridge Experience identity to the inherited Evidence Engine."""

    def __init__(self, evidence_engine: EvidenceEngine) -> None:
        if not isinstance(evidence_engine, EvidenceEngine):
            raise TypeError(
                "evidence_engine must be the inherited EvidenceEngine"
            )

        self._evidence_engine = evidence_engine

    def find_for_experience(
        self,
        *,
        experience_id: ExperienceId,
        keyword: str,
    ) -> ExperienceEvidenceReference:
        """Find evidence without changing Experience identity."""

        if not isinstance(experience_id, ExperienceId):
            raise TypeError("experience_id must be an ExperienceId")

        if not isinstance(keyword, str) or not keyword.strip():
            raise InvalidEvidenceKeywordError(
                "evidence keyword must be a non-empty string"
            )

        evidence = self._evidence_engine.find(keyword.strip())

        return ExperienceEvidenceReference(
            experience_id=experience_id,
            keyword=keyword.strip(),
            evidence=evidence,
        )
PY

python -m py_compile "$INTEGRATION" || fail $?

echo "PASS: Evidence integration tissue syntax"

echo
echo "[6/10] Build contract-derived behavioral examination"

cat > "$TEST" <<'PY'
from pathlib import Path

import pytest

from lib.python.evidence_engine.engine import EvidenceEngine
from lib.python.experience.evidence_integration import (
    ExperienceEvidenceIntegrator,
    ExperienceEvidenceReference,
    InvalidEvidenceKeywordError,
)
from lib.python.experience.model import Experience


def _build_repository(root: Path) -> None:
    package = root / "sample"
    package.mkdir(parents=True)

    (package / "persistent_experience_evidence.md").write_text(
        "# Persistent Experience Evidence\n",
        encoding="utf-8",
    )


def test_experience_can_reference_inherited_evidence_without_identity_change(
    tmp_path,
):
    _build_repository(tmp_path)

    experience = Experience.create()
    identity_before = experience.experience_id

    engine = EvidenceEngine(tmp_path)
    integrator = ExperienceEvidenceIntegrator(engine)

    reference = integrator.find_for_experience(
        experience_id=experience.experience_id,
        keyword="experience",
    )

    assert isinstance(reference, ExperienceEvidenceReference)
    assert reference.experience_id == identity_before
    assert experience.experience_id == identity_before


def test_evidence_remains_evidence_and_does_not_become_experience(
    tmp_path,
):
    _build_repository(tmp_path)

    experience = Experience.create()

    reference = ExperienceEvidenceIntegrator(
        EvidenceEngine(tmp_path)
    ).find_for_experience(
        experience_id=experience.experience_id,
        keyword="evidence",
    )

    assert isinstance(reference.evidence, dict)
    assert reference is not experience
    assert reference.evidence is not experience


def test_inherited_evidence_engine_is_used_directly(tmp_path):
    _build_repository(tmp_path)

    experience = Experience.create()
    engine = EvidenceEngine(tmp_path)

    direct = engine.find("evidence")

    integrated = ExperienceEvidenceIntegrator(
        engine
    ).find_for_experience(
        experience_id=experience.experience_id,
        keyword="evidence",
    )

    assert integrated.evidence == direct


def test_evidence_reference_preserves_query_provenance(tmp_path):
    _build_repository(tmp_path)

    experience = Experience.create()

    reference = ExperienceEvidenceIntegrator(
        EvidenceEngine(tmp_path)
    ).find_for_experience(
        experience_id=experience.experience_id,
        keyword="experience",
    )

    assert reference.keyword == "experience"
    assert reference.experience_id == experience.experience_id


def test_discovered_repository_evidence_is_explicit(tmp_path):
    _build_repository(tmp_path)

    experience = Experience.create()

    reference = ExperienceEvidenceIntegrator(
        EvidenceEngine(tmp_path)
    ).find_for_experience(
        experience_id=experience.experience_id,
        keyword="evidence",
    )

    assert reference.has_evidence is True
    assert (
        "sample/persistent_experience_evidence.md"
        in reference.evidence["docs"]
    )


def test_absence_of_evidence_remains_explicit(tmp_path):
    _build_repository(tmp_path)

    experience = Experience.create()

    reference = ExperienceEvidenceIntegrator(
        EvidenceEngine(tmp_path)
    ).find_for_experience(
        experience_id=experience.experience_id,
        keyword="definitely-not-present",
    )

    assert reference.has_evidence is False
    assert reference.experience_id == experience.experience_id


@pytest.mark.parametrize("keyword", ["", "   "])
def test_empty_evidence_keyword_is_rejected(tmp_path, keyword):
    experience = Experience.create()

    integrator = ExperienceEvidenceIntegrator(
        EvidenceEngine(tmp_path)
    )

    with pytest.raises(InvalidEvidenceKeywordError):
        integrator.find_for_experience(
            experience_id=experience.experience_id,
            keyword=keyword,
        )


def test_evidence_lookup_does_not_mutate_experience(tmp_path):
    _build_repository(tmp_path)

    experience = Experience.create()

    before = (
        experience.experience_id,
        experience.created_at,
        experience.state,
    )

    ExperienceEvidenceIntegrator(
        EvidenceEngine(tmp_path)
    ).find_for_experience(
        experience_id=experience.experience_id,
        keyword="evidence",
    )

    after = (
        experience.experience_id,
        experience.created_at,
        experience.state,
    )

    assert after == before
PY

python -m py_compile "$TEST" || fail $?

echo "PASS: behavioral examination syntax"

echo
echo "[7/10] Execute dedicated Phase 12 demonstration"

python -m pytest -q "$TEST" || fail $?

echo "PASS: Experience -> Evidence integration demonstrated"
echo "PASS: inherited EvidenceEngine conserved"
echo "PASS: Experience identity conserved"
echo "PASS: absence of evidence remains explicit"

echo
echo "[8/10] Execute complete Experience regression"

python -m pytest -q tests/experience || fail $?

echo "PASS: complete Experience regression"

echo
echo "[9/10] Verify mutation boundary and generate autosufficient epic-thread MD"

git diff --check -- \
    "$INTEGRATION" \
    "$TEST" || fail $?

ACTUAL_TRACKED="$(git diff --name-only | sort)"

EXPECTED_TRACKED="$(
    printf '%s\n' \
        "$INTEGRATION" \
        "$TEST" \
    | sort
)"

if [ "$ACTUAL_TRACKED" != "$EXPECTED_TRACKED" ]; then
    echo "ERROR: organism mutation outside RUN 047 boundary"
    echo
    echo "EXPECTED:"
    printf '%s\n' "$EXPECTED_TRACKED"
    echo
    echo "ACTUAL:"
    printf '%s\n' "$ACTUAL_TRACKED"
    fail 1
fi

{
    echo "# PCC-01 — RUN 047 — Evidence Integration"
    echo
    echo "## Capability"
    echo
    echo "PCC-01 — Persistent Experience"
    echo
    echo "## Build Phase"
    echo
    echo "Phase 12 — Evidence"
    echo
    echo "## Verified baseline"
    echo
    echo "\`$BASE\`"
    echo
    echo "## Evidence-derived anatomy"
    echo
    echo "- inherited Evidence organ: \`$EVIDENCE_ENGINE\`"
    echo "- inherited class: \`EvidenceEngine\`"
    echo "- inherited query physiology: \`EvidenceEngine.find(keyword)\`"
    echo "- no parallel Evidence Engine introduced"
    echo
    echo "## Implemented physiological bridge"
    echo
    echo "Experience identity -> inherited EvidenceEngine -> explicit Evidence reference"
    echo
    echo "## Conserved epistemic boundaries"
    echo
    echo "- Experience remains Experience"
    echo "- Evidence remains Evidence"
    echo "- ExperienceId remains the Experience identity"
    echo "- Evidence does not redefine Experience identity"
    echo "- absence of Evidence remains explicit"
    echo "- integration does not fabricate Evidence"
    echo
    echo "## Implemented tissue"
    echo
    echo "- \`$INTEGRATION\`"
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
    echo "## Pre-conservation status"
    echo
    echo "- Evidence Integration: DEMONSTRATED LOCALLY"
    echo "- inherited EvidenceEngine: CONSERVED"
    echo "- whole PCC-01: NOT YET CLAIMED"
} > "$REPORT"

[ -s "$REPORT" ] || {
    echo "ERROR: RUN 047 epic-thread MD missing"
    fail 1
}

echo "PASS: autosufficient RUN 047 MD generated"

echo
echo "[10/10] Conserve exact RUN 047 implementation and evidence"

git add -- \
    "$INTEGRATION" \
    "$TEST" \
    "$REPORT" || fail $?

STAGED="$(git diff --cached --name-only | sort)"

EXPECTED_STAGED="$(
    printf '%s\n' \
        "$INTEGRATION" \
        "$TEST" \
        "$REPORT" \
    | sort
)"

if [ "$STAGED" != "$EXPECTED_STAGED" ]; then
    echo "ERROR: staged boundary mismatch"
    echo
    echo "EXPECTED:"
    printf '%s\n' "$EXPECTED_STAGED"
    echo
    echo "ACTUAL:"
    printf '%s\n' "$STAGED"

    git reset --quiet

    fail 1
fi

git diff --cached --check || fail $?

git commit -m \
    "feat: integrate PCC-01 Experience with Evidence" || fail $?

IMPLEMENTATION_HEAD="$(git rev-parse HEAD)" || fail $?

git push origin main || fail $?
git fetch origin main --quiet || fail $?

REMOTE_AFTER_IMPLEMENTATION="$(git rev-parse origin/main)" || fail $?

[ "$IMPLEMENTATION_HEAD" = "$REMOTE_AFTER_IMPLEMENTATION" ] || {
    echo "ERROR: implementation commit not synchronized"
    fail 1
}

{
    echo
    echo "## Git conservation"
    echo
    echo "- Baseline: \`$BASE\`"
    echo "- Implementation commit: \`$IMPLEMENTATION_HEAD\`"
    echo "- origin/main synchronization after implementation: PASS"
    echo
    echo "## Final RUN 047 conclusion"
    echo
    echo "**Evidence Integration: IMPLEMENTED + DEMONSTRATED + CONSERVED**"
    echo
    echo "The existing EvidenceEngine remains the Evidence organ."
    echo
    echo "PCC-01 gained connective tissue rather than a duplicate Evidence system."
    echo
    echo "RUN 047 does not declare whole PCC-01 CANON or PRODUCTION-READY."
    echo
    echo "---"
    echo
    echo "END OF PCC-01 RUN 047"
} >> "$REPORT"

git add -- "$REPORT" || fail $?

git diff --cached --check || fail $?

git commit -m \
    "docs: finalize PCC-01 RUN 047 evidence" || fail $?

FINAL_HEAD="$(git rev-parse HEAD)" || fail $?

git push origin main || fail $?
git fetch origin main --quiet || fail $?

FINAL_REMOTE="$(git rev-parse origin/main)" || fail $?

[ "$FINAL_HEAD" = "$FINAL_REMOTE" ] || {
    echo "ERROR: final evidence commit not synchronized"
    fail 1
}

echo
echo "=========================================================="
echo "RUN 047 COMPLETE"
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
echo "EXISTING EVIDENCE ENGINE:"
echo "CONSERVED"
echo
echo "PCC-01 EVIDENCE INTEGRATION:"
echo "IMPLEMENTED + DEMONSTRATED + CONSERVED"
echo
echo "EPIC-THREAD MD:"
echo "$REPORT"
echo
echo "NEXT:"
echo "GPT verifies GitHub directly and derives the remaining PCC-01 acceptance work from contract evidence."
echo "=========================================================="
```

## Original RUN 047 Terminal Output — Complete

```text
==========================================================
PCC-01
EVIDENCE INTEGRATION — RUN 047
EVIDENCE-DERIVED IMPLEMENTATION
==========================================================

[1/10] Verify GitHub-authoritative baseline
Expected:    efc1ecdeed5c3b47bb55fb1885d57d7b433e7f1e
LOCAL:       efc1ecdeed5c3b47bb55fb1885d57d7b433e7f1e
origin/main: efc1ecdeed5c3b47bb55fb1885d57d7b433e7f1e
PASS: tracked/staged Git authority clean

PRE-EXISTING UNTRACKED HISTORICAL ARTIFACTS:
tests/experience/harness/pcc01_coordination_crash_reconciler.py
tests/experience/harness/pcc01_coordination_crash_writer.py
work/implementation-reports/PCC-01/PCC-01_RUN034C_FAILURE_RECOVERY_AND_EXACT_INTEGRATION_ANATOMY.md
work/implementation-reports/PCC-01/PCC-01_RUN034D_EXACT_LOCAL_JOURNAL_ANATOMY_FOR_INTEGRATION.md
work/implementation-reports/PCC-01/PCC-01_RUN038A_HARNESS_CAUSAL_CORRECTION.md
work/implementation-reports/PCC-01/PCC-01_RUN043B_LOCAL_ARTIFACT_STATE_INSPECTION.md

These remain outside RUN 047.
They will not be staged, committed, deleted, or modified.

[2/10] Verify accepted PCC-01 authority and inherited Evidence organ
PASS: Phase 12 authority
PASS: existing EvidenceEngine detected
PASS: RUN 047 will integrate; it will not create a parallel Evidence Engine

[3/10] Inspect exact live APIs before mutation
EvidenceEngine:
(repository='.')
EvidenceEngine.find:
(self, keyword)
Experience.create:
() -> "'Experience'"
Experience ID type:
ExperienceId
Experience ID:
08815b07-dfb8-474b-9e6e-3a2ffd29b44b
PASS: live Experience identity physiology
PASS: live EvidenceEngine physiology

[4/10] Verify no duplicate PCC-01 Evidence integration organ
PASS: no duplicate PCC-01 Evidence integration organ

[5/10] Build Experience-to-Evidence integration tissue
PASS: Evidence integration tissue syntax

[6/10] Build contract-derived behavioral examination
PASS: behavioral examination syntax

[7/10] Execute dedicated Phase 12 demonstration
.........                                                                [100%]
9 passed in 0.47s
PASS: Experience -> Evidence integration demonstrated
PASS: inherited EvidenceEngine conserved
PASS: Experience identity conserved
PASS: absence of evidence remains explicit

[8/10] Execute complete Experience regression
........................................................................ [ 37%]
........................................................................ [ 74%]
..................................................                       [100%]
194 passed in 3.39s
PASS: complete Experience regression

[9/10] Verify mutation boundary and generate autosufficient epic-thread MD
ERROR: organism mutation outside RUN 047 boundary

EXPECTED:
lib/python/experience/evidence_integration.py
tests/experience/test_experience_evidence_integration.py

ACTUAL:


==========================================================
RUN 047 STOPPED SAFELY
==========================================================
Exit code: 1
NO commit/push after failure
==========================================================
```

## RUN 047A Conservation Bash — Complete

```bash
#!/data/data/com.termux/files/usr/bin/bash
set -uo pipefail

export GIT_PAGER=cat
export PAGER=cat
export GH_PAGER=cat

cd "$HOME/storage/shared/AI-Projects/AI-Toolkit" || exit 1
export PYTHONPATH="$PWD/lib${PYTHONPATH:+:$PYTHONPATH}"

BASE="efc1ecdeed5c3b47bb55fb1885d57d7b433e7f1e"

INTEGRATION="lib/python/experience/evidence_integration.py"
TEST="tests/experience/test_experience_evidence_integration.py"
REPORT="work/implementation-reports/PCC-01/PCC-01_RUN047_EVIDENCE_INTEGRATION_IMPLEMENTATION.md"

ORIGINAL_SCRIPT="$PREFIX/tmp/pcc01_run047.sh"
ORIGINAL_OUTPUT="$PREFIX/tmp/pcc01_run047.output"

SELF="$PREFIX/tmp/pcc01_run047a_conserve.sh"
OUT="$PREFIX/tmp/pcc01_run047a_conserve.output"

mkdir -p "$(dirname "$REPORT")"
: > "$OUT"

exec > >(tee -a "$OUT") 2>&1

fail() {
    CODE="${1:-1}"

    echo
    echo "=========================================================="
    echo "RUN 047A STOPPED SAFELY"
    echo "=========================================================="
    echo "Exit code: $CODE"
    echo "NO tests re-executed"
    echo "NO further commit/push after failure"
    echo "=========================================================="

    exit "$CODE"
}

echo "=========================================================="
echo "PCC-01"
echo "RUN 047 EVIDENCE CONSERVATION — RUN 047A"
echo "NO TEST RE-EXECUTION"
echo "=========================================================="

echo
echo "[1/8] Verify GitHub authority"

git fetch origin main --quiet || fail $?

LOCAL="$(git rev-parse HEAD)" || fail $?
REMOTE="$(git rev-parse origin/main)" || fail $?

echo "Expected:    $BASE"
echo "LOCAL:       $LOCAL"
echo "origin/main: $REMOTE"

[ "$LOCAL" = "$BASE" ] || {
    echo "ERROR: local authority changed"
    fail 1
}

[ "$REMOTE" = "$BASE" ] || {
    echo "ERROR: GitHub authority changed"
    fail 1
}

[ -z "$(git diff --cached --name-only)" ] || {
    echo "ERROR: staging area already contains material"
    git diff --cached --name-only
    fail 1
}

[ -z "$(git diff --name-only)" ] || {
    echo "ERROR: tracked working-tree mutation exists"
    git diff --name-only
    fail 1
}

echo "PASS: baseline remains unchanged"

echo
echo "[2/8] Verify already-demonstrated RUN 047 evidence"

[ -s "$ORIGINAL_SCRIPT" ] || {
    echo "ERROR: original RUN 047 bash missing"
    fail 1
}

[ -s "$ORIGINAL_OUTPUT" ] || {
    echo "ERROR: original RUN 047 output missing"
    fail 1
}

grep -Fq "9 passed" "$ORIGINAL_OUTPUT" || {
    echo "ERROR: 9/9 dedicated result absent"
    fail 1
}

grep -Fq "194 passed" "$ORIGINAL_OUTPUT" || {
    echo "ERROR: 194/194 Experience regression result absent"
    fail 1
}

grep -Fq \
"PASS: Experience -> Evidence integration demonstrated" \
"$ORIGINAL_OUTPUT" || {
    echo "ERROR: Evidence integration demonstration absent"
    fail 1
}

grep -Fq \
"PASS: inherited EvidenceEngine conserved" \
"$ORIGINAL_OUTPUT" || {
    echo "ERROR: EvidenceEngine conservation proof absent"
    fail 1
}

grep -Fq \
"PASS: Experience identity conserved" \
"$ORIGINAL_OUTPUT" || {
    echo "ERROR: Experience identity conservation proof absent"
    fail 1
}

grep -Fq \
"PASS: absence of evidence remains explicit" \
"$ORIGINAL_OUTPUT" || {
    echo "ERROR: absence-of-evidence proof absent"
    fail 1
}

echo "PASS: dedicated Phase 12 = 9/9"
echo "PASS: complete Experience regression = 194/194"
echo "PASS: Evidence integration demonstrated"
echo "PASS: inherited EvidenceEngine conserved"
echo "PASS: Experience identity conserved"
echo "PASS: absence of Evidence remains explicit"

echo
echo "[3/8] Verify exact new artifacts using untracked-file physiology"

for FILE in "$INTEGRATION" "$TEST"; do
    [ -s "$FILE" ] || {
        echo "ERROR: demonstrated RUN 047 artifact missing:"
        echo "$FILE"
        fail 1
    }

    if git cat-file -e "HEAD:$FILE" 2>/dev/null; then
        echo "ERROR: artifact unexpectedly already exists in HEAD:"
        echo "$FILE"
        fail 1
    fi

    git ls-files --others --exclude-standard -- "$FILE" \
        | grep -Fxq "$FILE" || {
            echo "ERROR: expected RUN 047 artifact is not untracked:"
            echo "$FILE"
            fail 1
        }
done

echo "PASS: $INTEGRATION"
echo "PASS: $TEST"
echo "PASS: RUN 047 artifacts correctly classified as NEW + UNTRACKED"

echo
echo "[4/8] Verify historical untracked artifacts remain outside RUN 047"

ALL_UNTRACKED="$(git ls-files --others --exclude-standard | sort)"

echo "CURRENT UNTRACKED INVENTORY:"
printf '%s\n' "$ALL_UNTRACKED"

OTHER_UNTRACKED="$(
    printf '%s\n' "$ALL_UNTRACKED" |
    grep -Fvx "$INTEGRATION" |
    grep -Fvx "$TEST" |
    grep -Fvx "$REPORT" || true
)"

if [ -n "$OTHER_UNTRACKED" ]; then
    echo
    echo "HISTORICAL LOCAL ARTIFACTS PRESERVED OUTSIDE RUN 047:"
    printf '%s\n' "$OTHER_UNTRACKED"
fi

echo
echo "PASS: historical artifacts will not be staged or modified"

echo
echo "[5/8] Verify demonstrated source before conservation"

python -m py_compile \
    "$INTEGRATION" \
    "$TEST" || fail $?

git diff --no-index --check /dev/null "$INTEGRATION" >/dev/null 2>&1
RC1=$?

git diff --no-index --check /dev/null "$TEST" >/dev/null 2>&1
RC2=$?

# git diff --no-index returns 1 when files differ from /dev/null.
# That is expected for new files. Values >1 indicate an actual error.
[ "$RC1" -le 1 ] || {
    echo "ERROR: integration source integrity check failed"
    fail 1
}

[ "$RC2" -le 1 ] || {
    echo "ERROR: test source integrity check failed"
    fail 1
}

INTEGRATION_SHA="$(sha256sum "$INTEGRATION" | awk '{print $1}')"
TEST_SHA="$(sha256sum "$TEST" | awk '{print $1}')"

echo "INTEGRATION SHA-256:"
echo "$INTEGRATION_SHA"

echo
echo "TEST SHA-256:"
echo "$TEST_SHA"

echo
echo "PASS: demonstrated artifacts preserved byte-for-byte for conservation"

echo
echo "[6/8] Generate autosufficient epic-thread MD"

{
    echo "# PCC-01 — RUN 047 — Evidence Integration"
    echo
    echo "## Capability"
    echo
    echo "PCC-01 — Persistent Experience"
    echo
    echo "## Build Phase"
    echo
    echo "Phase 12 — Evidence"
    echo
    echo "## Git Authority"
    echo
    echo "- Baseline: \`$BASE\`"
    echo "- Local HEAD before conservation: \`$LOCAL\`"
    echo "- origin/main before conservation: \`$REMOTE\`"
    echo
    echo "## Evidence-derived anatomy"
    echo
    echo "- Existing organ: \`lib/python/evidence_engine/engine.py\`"
    echo "- Existing class: \`EvidenceEngine\`"
    echo "- Existing Evidence Engine remains authoritative"
    echo "- No parallel Evidence Engine was created"
    echo
    echo "## Integration physiology"
    echo
    echo '```text'
    echo "Experience identity"
    echo "        |"
    echo "        v"
    echo "ExperienceEvidenceIntegrator"
    echo "        |"
    echo "        v"
    echo "existing EvidenceEngine.find(keyword)"
    echo "        |"
    echo "        v"
    echo "ExperienceEvidenceReference"
    echo '```'
    echo
    echo "## Conserved epistemic boundaries"
    echo
    echo "- Experience remains Experience"
    echo "- Evidence remains Evidence"
    echo "- Evidence does not redefine Experience identity"
    echo "- absence of Evidence remains explicit"
    echo "- Evidence integration does not fabricate Evidence"
    echo
    echo "## Implemented artifacts"
    echo
    echo "- \`$INTEGRATION\`"
    echo "  - SHA-256: \`$INTEGRATION_SHA\`"
    echo "- \`$TEST\`"
    echo "  - SHA-256: \`$TEST_SHA\`"
    echo
    echo "## Demonstrated behavioral evidence"
    echo
    echo "- dedicated Evidence Integration examinations: **9/9 PASS**"
    echo "- complete Experience regression: **194/194 PASS**"
    echo "- Experience -> Evidence integration: PASS"
    echo "- inherited EvidenceEngine conservation: PASS"
    echo "- Experience identity conservation: PASS"
    echo "- absence of Evidence remains explicit: PASS"
    echo
    echo "## RUN 047 procedural failure"
    echo
    echo "Behavioral implementation did not fail."
    echo
    echo
    echo "The original RUN 047 stopped after all behavioral examinations passed because its mutation-boundary check used:"
    echo
    echo '```text'
    echo "git diff --name-only"
    echo '```'
    echo
    echo "That command does not enumerate newly-created untracked files."
    echo
    echo "Therefore the check incorrectly observed an empty ACTUAL set even though both demonstrated RUN 047 artifacts existed locally."
    echo
    echo "RUN 047A corrects only the conservation physiology by inspecting new files through:"
    echo
    echo '```text'
    echo "git ls-files --others --exclude-standard"
    echo '```'
    echo
    echo "No behavioral test is re-executed."
    echo
    echo "## Original RUN 047 Bash — Complete"
    echo
    echo '```bash'
    cat "$ORIGINAL_SCRIPT"
    echo '```'
    echo
    echo "## Original RUN 047 Terminal Output — Complete"
    echo
    echo '```text'
    cat "$ORIGINAL_OUTPUT"
    echo '```'
    echo
    echo "## RUN 047A Conservation Bash — Complete"
    echo
    echo '```bash'
    cat "$SELF"
    echo '```'
    echo
    echo "## Status before Git conservation"
    echo
    echo "- Evidence Integration: IMPLEMENTED LOCALLY"
    echo "- Evidence Integration: DEMONSTRATED"
    echo "- Evidence Integration Git conservation: PENDING"
    echo "- whole PCC-01 final acceptance: NOT YET CLAIMED"
} > "$REPORT"

[ -s "$REPORT" ] || {
    echo "ERROR: RUN 047 report generation failed"
    fail 1
}

REPORT_SHA="$(sha256sum "$REPORT" | awk '{print $1}')"

echo "PASS: autosufficient epic-thread generated"
echo "REPORT:"
echo "$REPORT"
echo "REPORT SHA-256:"
echo "$REPORT_SHA"

echo
echo "[7/8] Stage and conserve exact RUN 047 boundary"

git add -- \
    "$INTEGRATION" \
    "$TEST" \
    "$REPORT" || fail $?

STAGED="$(git diff --cached --name-only | sort)"

EXPECTED="$(
    printf '%s\n' \
        "$INTEGRATION" \
        "$TEST" \
        "$REPORT" |
    sort
)"

if [ "$STAGED" != "$EXPECTED" ]; then
    echo "ERROR: exact staging boundary violated"

    echo
    echo "EXPECTED:"
    printf '%s\n' "$EXPECTED"

    echo
    echo "ACTUAL:"
    printf '%s\n' "$STAGED"

    git reset --quiet
    fail 1
fi

git diff --cached --check || {
    echo "ERROR: staged content integrity failure"
    git reset --quiet
    fail 1
}

echo "STAGED EXACTLY:"
printf '%s\n' "$STAGED"

git commit -m \
    "feat: integrate PCC-01 Experience with Evidence" || fail $?

IMPLEMENTATION_HEAD="$(git rev-parse HEAD)" || fail $?

git push origin main || fail $?
git fetch origin main --quiet || fail $?

REMOTE_AFTER_IMPLEMENTATION="$(git rev-parse origin/main)" || fail $?

[ "$IMPLEMENTATION_HEAD" = "$REMOTE_AFTER_IMPLEMENTATION" ] || {
    echo "ERROR: implementation conservation not synchronized"
    fail 1
}

echo "PASS: implementation + demonstrated evidence synchronized"
echo "IMPLEMENTATION HEAD:"
echo "$IMPLEMENTATION_HEAD"

echo
echo "[8/8] Finalize epic-thread and synchronize"

{
    echo
    echo "## Git conservation result"
    echo
    echo "- Baseline: \`$BASE\`"
    echo "- Implementation/evidence commit: \`$IMPLEMENTATION_HEAD\`"
    echo "- origin/main synchronization: PASS"
    echo
    echo "## RUN 047A conservation output — complete"
    echo
    echo '```text'
    cat "$OUT"
    echo '```'
    echo
    echo "## Final RUN 047 conclusion"
    echo
    echo "**Evidence Integration: IMPLEMENTED + DEMONSTRATED + CONSERVED**"
    echo
    echo
    echo "The inherited EvidenceEngine remains the Evidence organ."
    echo
    echo "PCC-01 adds connective physiology only."
    echo
    echo
    echo "No duplicate Evidence Engine was introduced."
    echo
    echo "No Evidence was fabricated."
    echo
    echo "No Experience identity was rewritten."
    echo
    echo
    echo "Whole PCC-01 CANON / PRODUCTION-READY status is not declared by RUN 047."
    echo
    echo "---"
    echo
    echo "END OF PCC-01 RUN 047"
} >> "$REPORT"

git add -- "$REPORT" || fail $?

FINAL_STAGED="$(git diff --cached --name-only)"

[ "$FINAL_STAGED" = "$REPORT" ] || {
    echo "ERROR: final documentation boundary violated"
    git diff --cached --name-only
    git reset --quiet
    fail 1
}

git diff --cached --check || {
    git reset --quiet
    fail 1
}

git commit -m \
    "docs: finalize PCC-01 RUN 047 evidence" || fail $?

FINAL_HEAD="$(git rev-parse HEAD)" || fail $?

git push origin main || fail $?
git fetch origin main --quiet || fail $?

FINAL_REMOTE="$(git rev-parse origin/main)" || fail $?

[ "$FINAL_HEAD" = "$FINAL_REMOTE" ] || {
    echo "ERROR: final RUN 047 evidence not synchronized"
    fail 1
}

echo
echo "=========================================================="
echo "RUN 047A COMPLETE"
echo "=========================================================="
echo
echo "TESTS RE-EXECUTED:"
echo "NO"
echo
echo "PRESERVED EXECUTION EVIDENCE:"
echo "9/9 dedicated PASS"
echo "194/194 Experience regression PASS"
echo
echo "EXISTING EVIDENCE ENGINE:"
echo "CONSERVED"
echo
echo "PCC-01 EVIDENCE INTEGRATION:"
echo "IMPLEMENTED + DEMONSTRATED + CONSERVED"
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
echo "EPIC-THREAD MD:"
echo "$REPORT"
echo
echo "NEXT:"
echo "GPT verifies GitHub directly and derives remaining PCC-01 acceptance work from accepted contract evidence."
echo "=========================================================="
```

## Status before Git conservation

- Evidence Integration: IMPLEMENTED LOCALLY
- Evidence Integration: DEMONSTRATED
- Evidence Integration Git conservation: PENDING
- whole PCC-01 final acceptance: NOT YET CLAIMED

## Git conservation result

- Baseline: `efc1ecdeed5c3b47bb55fb1885d57d7b433e7f1e`
- Implementation/evidence commit: `7a88e04b378998b771ac9bd31c6b1da1ae483242`
- origin/main synchronization: PASS

## RUN 047A conservation output — complete

```text
==========================================================
PCC-01
RUN 047 EVIDENCE CONSERVATION — RUN 047A
NO TEST RE-EXECUTION
==========================================================

[1/8] Verify GitHub authority
Expected:    efc1ecdeed5c3b47bb55fb1885d57d7b433e7f1e
LOCAL:       efc1ecdeed5c3b47bb55fb1885d57d7b433e7f1e
origin/main: efc1ecdeed5c3b47bb55fb1885d57d7b433e7f1e
PASS: baseline remains unchanged

[2/8] Verify already-demonstrated RUN 047 evidence
PASS: dedicated Phase 12 = 9/9
PASS: complete Experience regression = 194/194
PASS: Evidence integration demonstrated
PASS: inherited EvidenceEngine conserved
PASS: Experience identity conserved
PASS: absence of Evidence remains explicit

[3/8] Verify exact new artifacts using untracked-file physiology
PASS: lib/python/experience/evidence_integration.py
PASS: tests/experience/test_experience_evidence_integration.py
PASS: RUN 047 artifacts correctly classified as NEW + UNTRACKED

[4/8] Verify historical untracked artifacts remain outside RUN 047
CURRENT UNTRACKED INVENTORY:
lib/python/experience/evidence_integration.py
tests/experience/harness/pcc01_coordination_crash_reconciler.py
tests/experience/harness/pcc01_coordination_crash_writer.py
tests/experience/test_experience_evidence_integration.py
work/implementation-reports/PCC-01/PCC-01_RUN034C_FAILURE_RECOVERY_AND_EXACT_INTEGRATION_ANATOMY.md
work/implementation-reports/PCC-01/PCC-01_RUN034D_EXACT_LOCAL_JOURNAL_ANATOMY_FOR_INTEGRATION.md
work/implementation-reports/PCC-01/PCC-01_RUN038A_HARNESS_CAUSAL_CORRECTION.md
work/implementation-reports/PCC-01/PCC-01_RUN043B_LOCAL_ARTIFACT_STATE_INSPECTION.md

HISTORICAL LOCAL ARTIFACTS PRESERVED OUTSIDE RUN 047:
tests/experience/harness/pcc01_coordination_crash_reconciler.py
tests/experience/harness/pcc01_coordination_crash_writer.py
work/implementation-reports/PCC-01/PCC-01_RUN034C_FAILURE_RECOVERY_AND_EXACT_INTEGRATION_ANATOMY.md
work/implementation-reports/PCC-01/PCC-01_RUN034D_EXACT_LOCAL_JOURNAL_ANATOMY_FOR_INTEGRATION.md
work/implementation-reports/PCC-01/PCC-01_RUN038A_HARNESS_CAUSAL_CORRECTION.md
work/implementation-reports/PCC-01/PCC-01_RUN043B_LOCAL_ARTIFACT_STATE_INSPECTION.md

PASS: historical artifacts will not be staged or modified

[5/8] Verify demonstrated source before conservation
INTEGRATION SHA-256:
8fa3bbed1a5871cb8040969c356af6c14506299474017af14383e3f55d950baf

TEST SHA-256:
af07beaf12bb98e17a445e2c2ace111258b6c81503f5a5cb4b9b60447043db6e

PASS: demonstrated artifacts preserved byte-for-byte for conservation

[6/8] Generate autosufficient epic-thread MD
PASS: autosufficient epic-thread generated
REPORT:
work/implementation-reports/PCC-01/PCC-01_RUN047_EVIDENCE_INTEGRATION_IMPLEMENTATION.md
REPORT SHA-256:
b5f295bc18066d8bd1fbae0ed2f0c946d11b96360ff8c4387219b892eaafda15

[7/8] Stage and conserve exact RUN 047 boundary
STAGED EXACTLY:
lib/python/experience/evidence_integration.py
tests/experience/test_experience_evidence_integration.py
work/implementation-reports/PCC-01/PCC-01_RUN047_EVIDENCE_INTEGRATION_IMPLEMENTATION.md
[main 7a88e04] feat: integrate PCC-01 Experience with Evidence
 3 files changed, 1708 insertions(+)
 create mode 100644 lib/python/experience/evidence_integration.py
 create mode 100644 tests/experience/test_experience_evidence_integration.py
 create mode 100644 work/implementation-reports/PCC-01/PCC-01_RUN047_EVIDENCE_INTEGRATION_IMPLEMENTATION.md
To https://github.com/caliofmarian-ai/AI-Toolkit.git
   efc1ecd..7a88e04  main -> main
PASS: implementation + demonstrated evidence synchronized
IMPLEMENTATION HEAD:
7a88e04b378998b771ac9bd31c6b1da1ae483242

[8/8] Finalize epic-thread and synchronize
```

## Final RUN 047 conclusion

**Evidence Integration: IMPLEMENTED + DEMONSTRATED + CONSERVED**


The inherited EvidenceEngine remains the Evidence organ.

PCC-01 adds connective physiology only.


No duplicate Evidence Engine was introduced.

No Evidence was fabricated.

No Experience identity was rewritten.


Whole PCC-01 CANON / PRODUCTION-READY status is not declared by RUN 047.

---

END OF PCC-01 RUN 047

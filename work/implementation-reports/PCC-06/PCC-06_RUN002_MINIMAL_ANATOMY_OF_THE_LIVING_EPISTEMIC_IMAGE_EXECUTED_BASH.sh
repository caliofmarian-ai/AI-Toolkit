#!/usr/bin/env bash
set -euo pipefail

cd ~/storage/shared/AI-Projects/AI-Toolkit || exit 1

EXPECTED_BASE="d22bde09d2b0cee4300a87d7af81f8f987f3e545"
BRANCH="pcc-06/living-project-image-run-002"
IMPLEMENTATION="lib/python/epistemic/living_project_image.py"
TEST_FILE="tests/epistemic/test_living_project_image.py"
REPORT="work/implementation-reports/PCC-06/PCC-06_RUN002_MINIMAL_ANATOMY_OF_THE_LIVING_EPISTEMIC_IMAGE.md"
EXEC_RECORD="work/implementation-reports/PCC-06/PCC-06_RUN002_MINIMAL_ANATOMY_OF_THE_LIVING_EPISTEMIC_IMAGE_EXECUTED_BASH.sh"

echo "=========================================================="
echo "PCC-06 — LIVING PROJECT IMAGE"
echo "RUN 002 — MINIMAL ANATOMY OF THE LIVING EPISTEMIC IMAGE"
echo "=========================================================="

echo
echo "[1/8] Verify Git authority and establish transformation branch"

git fetch origin main --quiet

MAIN_REMOTE="$(git rev-parse origin/main)"

echo "EXPECTED BASE: $EXPECTED_BASE"
echo "origin/main:   $MAIN_REMOTE"

test "$MAIN_REMOTE" = "$EXPECTED_BASE"

CURRENT_BRANCH="$(git branch --show-current)"
CURRENT_HEAD="$(git rev-parse HEAD)"

if [ "$CURRENT_BRANCH" = "main" ]; then
    test "$CURRENT_HEAD" = "$EXPECTED_BASE"
    test -z "$(git status --porcelain --untracked-files=all | grep -v "^?? $EXEC_RECORD$" || true)"
    git switch -c "$BRANCH"
elif [ "$CURRENT_BRANCH" = "$BRANCH" ]; then
    test "$CURRENT_HEAD" = "$EXPECTED_BASE"
else
    echo "STOP: repository is on unexpected branch: $CURRENT_BRANCH"
    exit 1
fi

echo "PASS: exact inspected Git authority"
echo "PASS: PCC-06 transformation branch established"

echo
echo "[2/8] Verify inherited anatomy before transformation"

PYTHONPATH="$PWD/lib:$PWD/lib/python${PYTHONPATH:+:$PYTHONPATH}" \
python - <<'PY'
from python.epistemic.provenance import (
    CurrentState,
    Knowledge,
    Provenance,
)
from python.epistemic.layered_memory import LayeredMemory

assert CurrentState
assert Knowledge
assert Provenance
assert LayeredMemory

print("PASS: CurrentState anatomy")
print("PASS: Knowledge anatomy")
print("PASS: Provenance anatomy")
print("PASS: Layered Memory anatomy")
PY

echo
echo "[3/8] Materialize minimal Living Project Image anatomy"

cat > "$IMPLEMENTATION" <<'PY'
"""
PCC-06 — Living Project Image.

RUN 002 — Minimal Anatomy of the Living Epistemic Image.

This module provides the smallest derived, read-only anatomy through which
the epistemic organism can represent what it demonstrably exists as now
without turning that representation into Canon, Evidence, Memory, Git,
Persistent Experience, CSL, Progressive Recall, Human Authority, or an
autonomous truth authority.

The Living Project Image is a derived epistemic surface.

It preserves semantic identity, bounded epistemic state, supporting
references, navigable provenance, uncertainty, and conflict.

It does not own the realities it represents.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


EpistemicState = Literal[
    "DEMONSTRATED",
    "UNKNOWN",
    "UNCERTAIN",
    "AMBIGUOUS",
    "CONFLICTING",
    "UNCONFIRMED",
    "NOT VERIFIED",
]

SupportKind = Literal[
    "CANON",
    "REPOSITORY",
    "IMPLEMENTATION",
    "TEST",
    "EVIDENCE",
    "KNOWLEDGE",
    "CURRENT_STATE",
    "MEMORY",
    "TRANSFORMATION",
    "PERSISTENT_EXPERIENCE",
    "WITNESS",
    "TRACE",
    "LINEAGE",
    "HISTORICAL",
    "OTHER",
]

_ALLOWED_STATES = {
    "DEMONSTRATED",
    "UNKNOWN",
    "UNCERTAIN",
    "AMBIGUOUS",
    "CONFLICTING",
    "UNCONFIRMED",
    "NOT VERIFIED",
}

_ALLOWED_SUPPORT_KINDS = {
    "CANON",
    "REPOSITORY",
    "IMPLEMENTATION",
    "TEST",
    "EVIDENCE",
    "KNOWLEDGE",
    "CURRENT_STATE",
    "MEMORY",
    "TRANSFORMATION",
    "PERSISTENT_EXPERIENCE",
    "WITNESS",
    "TRACE",
    "LINEAGE",
    "HISTORICAL",
    "OTHER",
}


class LivingProjectImageError(ValueError):
    """Raised when a Living Project Image would violate epistemic structure."""


def _text(name: str, value: str) -> str:
    if not isinstance(value, str):
        raise LivingProjectImageError(f"{name} must be text")

    value = value.strip()

    if not value:
        raise LivingProjectImageError(f"{name} must not be empty")

    return value


@dataclass(frozen=True)
class EpistemicReference:
    """
    Navigable reference toward supporting epistemic reality.

    A reference is not the referenced body and does not acquire its authority.
    """

    identifier: str
    title: str
    kind: SupportKind
    reference: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "identifier", _text("identifier", self.identifier))
        object.__setattr__(self, "title", _text("title", self.title))
        object.__setattr__(self, "reference", _text("reference", self.reference))

        if self.kind not in _ALLOWED_SUPPORT_KINDS:
            raise LivingProjectImageError(
                f"unsupported epistemic reference kind: {self.kind}"
            )

    @property
    def display_identity(self) -> str:
        return f"{self.identifier} — {self.title}"


@dataclass(frozen=True)
class LivingProjectStatement:
    """
    One derived statement on the organism's current epistemic surface.

    The statement remains distinct from every supporting epistemic body.
    """

    identifier: str
    title: str
    statement: str
    epistemic_state: EpistemicState
    supports: tuple[EpistemicReference, ...] = ()
    provenance_paths: tuple[str, ...] = ()
    uncertainty: tuple[str, ...] = ()
    conflicts: tuple[str, ...] = ()
    derived: bool = True
    authoritative: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "identifier", _text("identifier", self.identifier))
        object.__setattr__(self, "title", _text("title", self.title))
        object.__setattr__(self, "statement", _text("statement", self.statement))

        if not self.identifier.startswith("LPI-STMT-"):
            raise LivingProjectImageError(
                "Living Project Statement identity must use LPI-STMT-*"
            )

        if self.epistemic_state not in _ALLOWED_STATES:
            raise LivingProjectImageError(
                f"unsupported epistemic state: {self.epistemic_state}"
            )

        if self.derived is not True:
            raise LivingProjectImageError(
                "Living Project Statements must remain explicitly derived"
            )

        if self.authoritative is not False:
            raise LivingProjectImageError(
                "Living Project Image cannot declare itself authoritative"
            )

        if self.epistemic_state == "DEMONSTRATED" and not self.supports:
            raise LivingProjectImageError(
                "DEMONSTRATED state requires explicit supporting reality"
            )

        if self.epistemic_state == "UNCERTAIN" and not self.uncertainty:
            raise LivingProjectImageError(
                "UNCERTAIN state must preserve its uncertainty"
            )

        if self.epistemic_state == "CONFLICTING" and not self.conflicts:
            raise LivingProjectImageError(
                "CONFLICTING state must preserve visible conflict"
            )

        for path in self.provenance_paths:
            _text("provenance path", path)

        for item in self.uncertainty:
            _text("uncertainty", item)

        for item in self.conflicts:
            _text("conflict", item)

    @property
    def display_identity(self) -> str:
        return f"{self.identifier} — {self.title}"


@dataclass(frozen=True)
class LivingProjectImage:
    """
    Derived read-only current epistemic image.

    Destruction of this object destroys no authoritative project reality.
    The image can be reconstructed from the same preserved inputs.
    """

    identifier: str
    title: str
    statements: tuple[LivingProjectStatement, ...]
    derived: bool = True
    authoritative: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "identifier", _text("identifier", self.identifier))
        object.__setattr__(self, "title", _text("title", self.title))

        if not self.identifier.startswith("LPI-"):
            raise LivingProjectImageError(
                "Living Project Image identity must use LPI-*"
            )

        if self.derived is not True:
            raise LivingProjectImageError(
                "Living Project Image must remain explicitly derived"
            )

        if self.authoritative is not False:
            raise LivingProjectImageError(
                "Living Project Image cannot become an authority"
            )

        identities = tuple(item.identifier for item in self.statements)

        if len(identities) != len(set(identities)):
            raise LivingProjectImageError(
                "Living Project Image cannot contain duplicate statement identities"
            )

    @property
    def display_identity(self) -> str:
        return f"{self.identifier} — {self.title}"

    def statement(self, identifier: str) -> LivingProjectStatement:
        identifier = _text("statement identifier", identifier)

        for item in self.statements:
            if item.identifier == identifier:
                return item

        raise LivingProjectImageError(
            f"Living Project Statement not present: {identifier}"
        )

    def by_state(
        self,
        epistemic_state: EpistemicState,
    ) -> tuple[LivingProjectStatement, ...]:
        if epistemic_state not in _ALLOWED_STATES:
            raise LivingProjectImageError(
                f"unsupported epistemic state: {epistemic_state}"
            )

        return tuple(
            item
            for item in self.statements
            if item.epistemic_state == epistemic_state
        )


def form_living_project_image(
    *,
    identifier: str,
    title: str,
    statements: tuple[LivingProjectStatement, ...],
) -> LivingProjectImage:
    """
    Form a deterministic derived image from explicitly supplied representations.

    No source organ is mutated.
    No retrieval is performed.
    No missing support is invented.
    No canonical admission is performed.
    """

    if not isinstance(statements, tuple):
        raise LivingProjectImageError(
            "Living Project Image statements must be an immutable tuple"
        )

    for item in statements:
        if not isinstance(item, LivingProjectStatement):
            raise LivingProjectImageError(
                "Living Project Image accepts only LivingProjectStatement bodies"
            )

    return LivingProjectImage(
        identifier=identifier,
        title=title,
        statements=statements,
    )
PY

cat > "$TEST_FILE" <<'PY'
from dataclasses import FrozenInstanceError

import pytest

from python.epistemic.living_project_image import (
    EpistemicReference,
    LivingProjectImageError,
    LivingProjectStatement,
    form_living_project_image,
)


def reference(
    identifier="EV-000001",
    title="Repository evidence",
    kind="EVIDENCE",
    location="tests/epistemic/test_provenance.py",
):
    return EpistemicReference(
        identifier=identifier,
        title=title,
        kind=kind,
        reference=location,
    )


def demonstrated():
    return LivingProjectStatement(
        identifier="LPI-STMT-000001",
        title="Provenance capability",
        statement="The organism preserves explicit provenance.",
        epistemic_state="DEMONSTRATED",
        supports=(reference(),),
        provenance_paths=(
            "Current State → Knowledge → Verification → Evidence → Source",
        ),
    )


def test_statement_has_human_readable_identity():
    item = demonstrated()

    assert (
        item.display_identity
        == "LPI-STMT-000001 — Provenance capability"
    )


def test_reference_has_human_readable_identity():
    item = reference()

    assert item.display_identity == "EV-000001 — Repository evidence"


def test_demonstrated_statement_is_explicitly_derived_and_non_authoritative():
    item = demonstrated()

    assert item.derived is True
    assert item.authoritative is False


def test_demonstrated_state_requires_support():
    with pytest.raises(
        LivingProjectImageError,
        match="requires explicit supporting reality",
    ):
        LivingProjectStatement(
            identifier="LPI-STMT-000001",
            title="Unsupported certainty",
            statement="This must not masquerade as demonstrated.",
            epistemic_state="DEMONSTRATED",
        )


def test_unknown_is_a_legitimate_non_answer_without_fabricated_support():
    item = LivingProjectStatement(
        identifier="LPI-STMT-000002",
        title="Unknown runtime state",
        statement="The runtime condition is not known.",
        epistemic_state="UNKNOWN",
    )

    assert item.epistemic_state == "UNKNOWN"
    assert item.supports == ()
    assert item.provenance_paths == ()


def test_uncertainty_remains_visible():
    item = LivingProjectStatement(
        identifier="LPI-STMT-000003",
        title="Uncertain integration state",
        statement="Integration state remains uncertain.",
        epistemic_state="UNCERTAIN",
        supports=(reference(),),
        uncertainty=("No runtime execution has established the integration.",),
    )

    assert item.uncertainty == (
        "No runtime execution has established the integration.",
    )


def test_uncertain_state_cannot_hide_uncertainty():
    with pytest.raises(
        LivingProjectImageError,
        match="must preserve its uncertainty",
    ):
        LivingProjectStatement(
            identifier="LPI-STMT-000003",
            title="Hidden uncertainty",
            statement="Uncertainty must remain visible.",
            epistemic_state="UNCERTAIN",
        )


def test_conflict_remains_visible():
    item = LivingProjectStatement(
        identifier="LPI-STMT-000004",
        title="Conflicting project state",
        statement="Available representations conflict.",
        epistemic_state="CONFLICTING",
        supports=(
            reference(
                "EV-000001",
                "First observation",
                "EVIDENCE",
                "evidence:first",
            ),
            reference(
                "EV-000002",
                "Second observation",
                "EVIDENCE",
                "evidence:second",
            ),
        ),
        conflicts=(
            "First observation reports state A.",
            "Second observation reports state B.",
        ),
    )

    assert len(item.conflicts) == 2


def test_conflicting_state_cannot_silently_erase_conflict():
    with pytest.raises(
        LivingProjectImageError,
        match="must preserve visible conflict",
    ):
        LivingProjectStatement(
            identifier="LPI-STMT-000004",
            title="Hidden conflict",
            statement="Conflict must remain visible.",
            epistemic_state="CONFLICTING",
        )


def test_statement_is_immutable():
    item = demonstrated()

    with pytest.raises(FrozenInstanceError):
        item.statement = "Rewrite current reality."


def test_support_reference_is_immutable():
    item = reference()

    with pytest.raises(FrozenInstanceError):
        item.reference = "rewritten"


def test_image_is_derived_read_only_and_non_authoritative():
    item = demonstrated()

    image = form_living_project_image(
        identifier="LPI-000001",
        title="AI-Toolkit Living Epistemic Image",
        statements=(item,),
    )

    assert image.derived is True
    assert image.authoritative is False

    with pytest.raises(FrozenInstanceError):
        image.title = "Rewritten image"


def test_identical_inputs_reconstruct_identical_image():
    first_statement = demonstrated()
    second_statement = demonstrated()

    first = form_living_project_image(
        identifier="LPI-000001",
        title="AI-Toolkit Living Epistemic Image",
        statements=(first_statement,),
    )

    second = form_living_project_image(
        identifier="LPI-000001",
        title="AI-Toolkit Living Epistemic Image",
        statements=(second_statement,),
    )

    assert first == second


def test_image_preserves_navigation_toward_supporting_reality():
    item = demonstrated()

    image = form_living_project_image(
        identifier="LPI-000001",
        title="AI-Toolkit Living Epistemic Image",
        statements=(item,),
    )

    recovered = image.statement("LPI-STMT-000001")

    assert recovered.supports[0].reference == (
        "tests/epistemic/test_provenance.py"
    )
    assert recovered.provenance_paths == (
        "Current State → Knowledge → Verification → Evidence → Source",
    )


def test_image_can_expose_non_answer_states_without_normalizing_them():
    unknown = LivingProjectStatement(
        identifier="LPI-STMT-000010",
        title="Unknown state",
        statement="State is unknown.",
        epistemic_state="UNKNOWN",
    )

    unconfirmed = LivingProjectStatement(
        identifier="LPI-STMT-000011",
        title="Unconfirmed state",
        statement="State is not confirmed.",
        epistemic_state="UNCONFIRMED",
    )

    image = form_living_project_image(
        identifier="LPI-000001",
        title="AI-Toolkit Living Epistemic Image",
        statements=(unknown, unconfirmed),
    )

    assert image.by_state("UNKNOWN") == (unknown,)
    assert image.by_state("UNCONFIRMED") == (unconfirmed,)


def test_duplicate_statement_identity_is_rejected():
    item = demonstrated()

    with pytest.raises(
        LivingProjectImageError,
        match="duplicate statement identities",
    ):
        form_living_project_image(
            identifier="LPI-000001",
            title="AI-Toolkit Living Epistemic Image",
            statements=(item, item),
        )


def test_invalid_statement_identity_is_rejected():
    with pytest.raises(
        LivingProjectImageError,
        match=r"LPI-STMT-\*",
    ):
        LivingProjectStatement(
            identifier="STATE-000001",
            title="Wrong identity family",
            statement="Invalid identity.",
            epistemic_state="UNKNOWN",
        )


def test_image_does_not_implement_progressive_recall():
    image = form_living_project_image(
        identifier="LPI-000001",
        title="AI-Toolkit Living Epistemic Image",
        statements=(demonstrated(),),
    )

    assert not hasattr(image, "recall")
    assert not hasattr(image, "progressive_recall")
    assert not hasattr(image, "retrieve_deeper_memory")
    assert not hasattr(image, "evaluate_epistemic_sufficiency")


def test_image_does_not_claim_canonical_or_source_organ_authority():
    image = form_living_project_image(
        identifier="LPI-000001",
        title="AI-Toolkit Living Epistemic Image",
        statements=(demonstrated(),),
    )

    assert not hasattr(image, "admit_canon")
    assert not hasattr(image, "modify_canon")
    assert not hasattr(image, "write_memory")
    assert not hasattr(image, "write_evidence")
    assert not hasattr(image, "write_current_state")


def test_forming_image_does_not_mutate_source_inputs():
    item = demonstrated()
    original_supports = item.supports
    original_paths = item.provenance_paths

    form_living_project_image(
        identifier="LPI-000001",
        title="AI-Toolkit Living Epistemic Image",
        statements=(item,),
    )

    assert item.supports == original_supports
    assert item.provenance_paths == original_paths
PY

cat > "$REPORT" <<'MD'
# PCC-06 — Minimal Anatomy of the Living Epistemic Image

**Epistemic organ:** Living Project Image  
**Technical execution:** RUN 002  
**Nature:** Minimal physiological implementation  
**Canonical admission claimed:** NO

## BEFORE

The organism already possessed explicit epistemic ancestry including
Source, Observation, Evidence, Claim, Verification, Knowledge, Current State,
Sedimented Memory, and Layered Memory.

Current State already represented an explicit present-state statement derived
from registered Knowledge and preserved navigation toward its provenance.

Current State explicitly did not constitute the complete Living Project Image.

The organism therefore possessed present-state anatomy but lacked the distinct
derived surface capable of representing multiple current epistemic statements
while preserving bounded epistemic states, provenance, uncertainty, conflict,
and non-authoritative status.

## INCAPACITY

The organism could not yet form a dedicated Living Project Image that could
legitimately say:

"What does the project demonstrably exist as now?"

without conflating that representation with its supporting Canon, Evidence,
Memory, Knowledge, Current State, Git reality, CSL, or Human Authority.

## TRANSFORMATION

RUN 002 introduces the minimum Living Project Image anatomy:

- EpistemicReference;
- LivingProjectStatement;
- LivingProjectImage;
- form_living_project_image;
- explicit epistemic non-answer states;
- immutable derived representations;
- explicit support references;
- explicit provenance navigation paths;
- visible uncertainty;
- visible conflict;
- non-authoritative image semantics.

## AFTER

The organism can now form a small read-only derived epistemic surface from
explicitly supplied representations.

A statement can preserve:

- semantic identity;
- current epistemic state;
- supporting references;
- navigable provenance;
- uncertainty;
- conflict;
- derived status;
- non-authoritative status.

UNKNOWN may remain UNKNOWN without fabricated support.

DEMONSTRATED cannot exist without explicit support.

UNCERTAIN cannot hide its uncertainty.

CONFLICTING cannot hide its conflict.

## BOUNDARY

RUN 002 does not implement:

- Progressive Recall;
- epistemic sufficiency evaluation;
- deep-memory retrieval;
- automatic repository observation;
- automatic Living Project Image refresh;
- context packaging;
- AI bootstrap;
- canonical admission;
- autonomous truth authority;
- CSL migration;
- dashboard presentation.

Living Project Image remains distinct from Current State.

Current State is an epistemic source that later physiology may project into
the Living Project Image.

Connection does not mean fusion.

## EVIDENCE

Primary implementation:

`lib/python/epistemic/living_project_image.py`

Dedicated examination:

`tests/epistemic/test_living_project_image.py`

Inherited neighboring physiology remains independently examined through the
existing Provenance, Current State, Sedimented Memory, and Layered Memory
test suites.

The complete epistemic regression is executed during this RUN.

Exact terminal counts belong to the execution reality and are not fabricated
inside this report before execution.

## CANONICAL STATUS

Implementation does not canonically admit itself.

PCC-06 remains subject to Human Authority for canonical admission.

## NEXT PHYSIOLOGICAL NEED

The next legitimate need is to connect the minimal Living Project Image to
existing Current State and other eligible epistemic bodies through explicit
projection rules without allowing the image to become another independent
truth store.

That transformation must remain distinct from Progressive Recall.

Proposed next transformation:

**PCC-06 RUN 003 — Projection of Existing Epistemic State into the Living Project Image**
MD

python - <<'PY'
from pathlib import Path

for name in (
    "lib/python/epistemic/living_project_image.py",
    "tests/epistemic/test_living_project_image.py",
    "work/implementation-reports/PCC-06/PCC-06_RUN002_MINIMAL_ANATOMY_OF_THE_LIVING_EPISTEMIC_IMAGE.md",
):
    path = Path(name)
    text = path.read_text(encoding="utf-8")
    text = "\n".join(line.rstrip() for line in text.splitlines()) + "\n"
    path.write_text(text, encoding="utf-8")
PY

echo "PASS: minimal Living Project Image anatomy materialized"

echo
echo "[4/8] Static import examination"

PYTHONPATH="$PWD/lib:$PWD/lib/python${PYTHONPATH:+:$PYTHONPATH}" \
python - <<'PY'
from python.epistemic.living_project_image import (
    EpistemicReference,
    LivingProjectImage,
    LivingProjectImageError,
    LivingProjectStatement,
    form_living_project_image,
)

assert EpistemicReference
assert LivingProjectImage
assert LivingProjectImageError
assert LivingProjectStatement
assert form_living_project_image

print("PASS: EpistemicReference")
print("PASS: LivingProjectStatement")
print("PASS: LivingProjectImage")
print("PASS: form_living_project_image")
PY

echo
echo "[5/8] Dedicated PCC-06 examination"

PYTHONPATH="$PWD/lib:$PWD/lib/python${PYTHONPATH:+:$PYTHONPATH}" \
python -m pytest -q "$TEST_FILE"

echo
echo "[6/8] Neighboring inherited physiology"

PYTHONPATH="$PWD/lib:$PWD/lib/python${PYTHONPATH:+:$PYTHONPATH}" \
python -m pytest -q \
    tests/epistemic/test_provenance.py \
    tests/epistemic/test_sedimented_memory.py \
    tests/epistemic/test_layered_memory.py \
    tests/epistemic/test_layered_memory_persistence.py \
    tests/epistemic/test_layered_memory_traversal.py \
    tests/epistemic/test_layered_memory_ancestry.py

echo
echo "[7/8] Complete epistemic regression"

BEFORE_MEMORY="$(mktemp)"
AFTER_MEMORY="$(mktemp)"
NEW_MEMORY="$(mktemp)"

find work/memory -maxdepth 1 -type f -name '*.json' -print 2>/dev/null \
    | sort > "$BEFORE_MEMORY" || true

PYTHONPATH="$PWD/lib:$PWD/lib/python${PYTHONPATH:+:$PYTHONPATH}" \
python -m pytest -q tests/epistemic

find work/memory -maxdepth 1 -type f -name '*.json' -print 2>/dev/null \
    | sort > "$AFTER_MEMORY" || true

comm -13 "$BEFORE_MEMORY" "$AFTER_MEMORY" > "$NEW_MEMORY"

if [ -s "$NEW_MEMORY" ]; then
    echo
    echo "New MemoryStore products produced by regression:"
    cat "$NEW_MEMORY"

    NEW_MEMORY="$NEW_MEMORY" python - <<'PY'
import json
import os
from datetime import datetime
from pathlib import Path

manifest = Path(os.environ["NEW_MEMORY"])

for raw in manifest.read_text(encoding="utf-8").splitlines():
    if not raw.strip():
        continue

    path = Path(raw.strip())
    payload = json.loads(path.read_text(encoding="utf-8"))

    required = {
        "id",
        "title",
        "content",
        "session",
        "capability",
        "timestamp",
    }

    if set(payload) != required:
        raise SystemExit(
            f"STOP: unclassified work/memory product schema: {path}"
        )

    if payload["id"] != path.stem:
        raise SystemExit(
            f"STOP: Memory id/filename mismatch: {path}"
        )

    if payload["title"] != "First Memory":
        raise SystemExit(
            f"STOP: unexpected Memory title: {path}"
        )

    if payload["content"] != "The organism preserved an experience.":
        raise SystemExit(
            f"STOP: unexpected Memory content: {path}"
        )

    if payload["session"] != "SESSION-000001":
        raise SystemExit(
            f"STOP: unexpected Memory session: {path}"
        )

    if payload["capability"] != "CAP-0001":
        raise SystemExit(
            f"STOP: unexpected Memory capability: {path}"
        )

    stamp = datetime.fromisoformat(payload["timestamp"])

    if stamp.tzinfo is None:
        raise SystemExit(
            f"STOP: Memory timestamp lacks timezone: {path}"
        )

    print(f"PASS: classified legitimate MemoryStore test product: {path}")
PY
fi

rm -f "$BEFORE_MEMORY" "$AFTER_MEMORY" "$NEW_MEMORY"

echo
echo "[8/8] Conserve demonstrated transformation"

git diff --check

echo
echo "----- REPOSITORY REALITY BEFORE CONSERVATION -----"
git --no-pager status --short

git add \
    "$IMPLEMENTATION" \
    "$TEST_FILE" \
    "$REPORT" \
    "$EXEC_RECORD"

# Conserve only newly produced, semantically classified MemoryStore products.
git add work/memory/*.json 2>/dev/null || true

git diff --cached --check

echo
echo "----- STAGED DEMONSTRATED REALITY -----"
git --no-pager status --short

git commit -m "pcc-06: form minimal living epistemic image anatomy"

HEAD_NOW="$(git rev-parse HEAD)"

git push -u origin "$BRANCH"

git fetch origin "$BRANCH" --quiet

REMOTE="$(git rev-parse "origin/$BRANCH")"

test "$HEAD_NOW" = "$REMOTE"
test -z "$(git status --porcelain)"

echo
echo "=========================================================="
echo "PCC-06 — MINIMAL ANATOMY OF THE LIVING EPISTEMIC IMAGE"
echo "RUN 002 SUCCESS"
echo "=========================================================="
echo "BRANCH:                       $BRANCH"
echo "HEAD:                         $HEAD_NOW"
echo "LOCAL == origin/$BRANCH:     PASS"
echo "WORKTREE:                     CLEAN"
echo "LIVING PROJECT IMAGE:         FORMED"
echo "DERIVED:                      YES"
echo "READ-ONLY:                    YES"
echo "HUMAN-READABLE:               YES"
echo "PROVENANCE-PRESERVING:        YES"
echo "UNKNOWN PRESERVED:            YES"
echo "UNCERTAINTY PRESERVED:        YES"
echo "CONFLICT PRESERVED:           YES"
echo "AUTONOMOUS AUTHORITY:         NO"
echo "CANON MODIFIED:               NO"
echo "MEMORY MUTATED BY IMAGE:      NO"
echo "EVIDENCE MUTATED BY IMAGE:    NO"
echo "PROGRESSIVE RECALL:           NO"
echo "PCC-06 CANONICALLY ADMITTED:  NO"
echo "EXECUTED BASH:                CONSERVED"
echo "IMPLEMENTATION REPORT:        CONSERVED"
echo "=========================================================="

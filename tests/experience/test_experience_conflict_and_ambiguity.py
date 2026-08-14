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

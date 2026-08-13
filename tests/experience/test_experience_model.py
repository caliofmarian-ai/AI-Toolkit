from datetime import datetime, timezone

import pytest

from lib.python.experience.identity import ExperienceId
from lib.python.experience.lifecycle import ExperienceState
from lib.python.experience.model import Experience


def test_new_experience_has_identity_creation_time_and_created_state():
    experience = Experience.create()

    assert isinstance(experience.experience_id, ExperienceId)
    assert experience.created_at.tzinfo is not None
    assert experience.state is ExperienceState.CREATED


def test_experience_creation_requires_no_neighboring_epistemic_organs():
    experience = Experience.create()

    assert not hasattr(experience, "session_id")
    assert not hasattr(experience, "memory_id")
    assert not hasattr(experience, "evidence_id")


def test_reconstructed_model_preserves_explicit_identity():
    identity = ExperienceId.create()
    created_at = datetime.now(timezone.utc)

    experience = Experience(
        experience_id=identity,
        created_at=created_at,
        state=ExperienceState.CREATED,
    )

    assert experience.experience_id == identity
    assert experience.created_at == created_at


def test_naive_creation_timestamp_is_rejected():
    with pytest.raises(ValueError):
        Experience(
            experience_id=ExperienceId.create(),
            created_at=datetime.now(),
            state=ExperienceState.CREATED,
        )

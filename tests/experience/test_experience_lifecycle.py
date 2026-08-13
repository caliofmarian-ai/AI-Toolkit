import pytest

from lib.python.experience.lifecycle import (
    ExperienceLifecycleError,
    ExperienceState,
    transition,
)
from lib.python.experience.model import Experience


def test_created_experience_can_become_active_without_identity_change():
    created = Experience.create()
    active = created.activate()

    assert active.state is ExperienceState.ACTIVE
    assert active.experience_id == created.experience_id
    assert active.created_at == created.created_at


def test_active_experience_can_become_closed_without_identity_change():
    created = Experience.create()
    active = created.activate()
    closed = active.close()

    assert closed.state is ExperienceState.CLOSED
    assert closed.experience_id == created.experience_id
    assert closed.created_at == created.created_at


@pytest.mark.parametrize(
    ("current", "target"),
    [
        (ExperienceState.CREATED, ExperienceState.CREATED),
        (ExperienceState.CREATED, ExperienceState.CLOSED),
        (ExperienceState.ACTIVE, ExperienceState.CREATED),
        (ExperienceState.ACTIVE, ExperienceState.ACTIVE),
        (ExperienceState.CLOSED, ExperienceState.CREATED),
        (ExperienceState.CLOSED, ExperienceState.ACTIVE),
        (ExperienceState.CLOSED, ExperienceState.CLOSED),
    ],
)
def test_illegal_lifecycle_transitions_are_rejected(current, target):
    with pytest.raises(ExperienceLifecycleError):
        transition(current, target)


def test_created_experience_cannot_close_directly():
    with pytest.raises(ExperienceLifecycleError):
        Experience.create().close()


def test_closed_experience_cannot_be_reactivated():
    closed = Experience.create().activate().close()

    with pytest.raises(ExperienceLifecycleError):
        closed.activate()

import pytest

from lib.python.experience.lifecycle import (
    ExperienceLifecycleError,
    ExperienceState,
)
from lib.python.experience.repository import (
    ExperienceNotFoundError,
    InMemoryExperienceRepository,
)
from lib.python.experience.service import ExperienceService
from lib.python.experience.identity import ExperienceId


def make_service():
    repository = InMemoryExperienceRepository()
    return repository, ExperienceService(repository)


def test_service_creates_and_admits_experience():
    repository, service = make_service()

    experience = service.create_experience()

    assert experience.state is ExperienceState.CREATED
    assert repository.contains(experience.experience_id)
    assert service.get_experience(experience.experience_id) == experience


def test_service_activates_same_experience_identity():
    _, service = make_service()
    created = service.create_experience()

    active = service.activate_experience(created.experience_id)

    assert active.state is ExperienceState.ACTIVE
    assert active.experience_id == created.experience_id


def test_service_closes_same_experience_identity():
    _, service = make_service()
    created = service.create_experience()
    active = service.activate_experience(created.experience_id)

    closed = service.close_experience(active.experience_id)

    assert closed.state is ExperienceState.CLOSED
    assert closed.experience_id == created.experience_id


def test_service_rejects_unknown_identity():
    _, service = make_service()

    with pytest.raises(ExperienceNotFoundError):
        service.get_experience(ExperienceId.create())


def test_service_preserves_lifecycle_rules():
    _, service = make_service()
    created = service.create_experience()

    with pytest.raises(ExperienceLifecycleError):
        service.close_experience(created.experience_id)


def test_service_cannot_reactivate_closed_experience():
    _, service = make_service()
    created = service.create_experience()
    service.activate_experience(created.experience_id)
    service.close_experience(created.experience_id)

    with pytest.raises(ExperienceLifecycleError):
        service.activate_experience(created.experience_id)

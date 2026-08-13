import pytest

from lib.python.experience.identity import ExperienceId
from lib.python.experience.model import Experience
from lib.python.experience.repository import (
    ExperienceAlreadyExistsError,
    ExperienceNotFoundError,
    InMemoryExperienceRepository,
)


def test_repository_adds_and_gets_experience_by_stable_identity():
    repository = InMemoryExperienceRepository()
    experience = Experience.create()

    repository.add(experience)

    loaded = repository.get(experience.experience_id)

    assert loaded == experience
    assert loaded.experience_id == experience.experience_id


def test_repository_reports_known_identity():
    repository = InMemoryExperienceRepository()
    experience = Experience.create()

    assert repository.contains(experience.experience_id) is False

    repository.add(experience)

    assert repository.contains(experience.experience_id) is True


def test_repository_rejects_duplicate_admission():
    repository = InMemoryExperienceRepository()
    experience = Experience.create()

    repository.add(experience)

    with pytest.raises(ExperienceAlreadyExistsError):
        repository.add(experience)


def test_repository_rejects_unknown_identity_lookup():
    repository = InMemoryExperienceRepository()

    with pytest.raises(ExperienceNotFoundError):
        repository.get(ExperienceId.create())


def test_repository_saves_new_state_without_changing_identity():
    repository = InMemoryExperienceRepository()
    created = Experience.create()
    repository.add(created)

    active = created.activate()
    repository.save(active)

    loaded = repository.get(created.experience_id)

    assert loaded.state == active.state
    assert loaded.experience_id == created.experience_id


def test_repository_rejects_save_for_unknown_experience():
    repository = InMemoryExperienceRepository()
    experience = Experience.create()

    with pytest.raises(ExperienceNotFoundError):
        repository.save(experience)

import json

import pytest

from lib.python.experience.model import Experience
from lib.python.experience.persistent_repository import (
    ExperienceStoreCorruptionError,
    JsonFileExperienceRepository,
)
from lib.python.experience.repository import (
    ExperienceAlreadyExistsError,
    ExperienceNotFoundError,
)


def test_repository_persists_experience_to_file(tmp_path):
    store = tmp_path / "experience-store.json"
    repository = JsonFileExperienceRepository(store)

    experience = Experience.create()
    repository.add(experience)

    assert store.is_file()


def test_new_repository_instance_recovers_existing_experience(tmp_path):
    store = tmp_path / "experience-store.json"

    writer = JsonFileExperienceRepository(store)
    before = Experience.create().activate()
    writer.add(before)

    reader = JsonFileExperienceRepository(store)
    after = reader.get(before.experience_id)

    assert after == before
    assert after.experience_id == before.experience_id


def test_save_survives_repository_instance_replacement(tmp_path):
    store = tmp_path / "experience-store.json"

    first = JsonFileExperienceRepository(store)

    created = Experience.create()
    first.add(created)

    active = created.activate()
    first.save(active)

    second = JsonFileExperienceRepository(store)
    recovered = second.get(created.experience_id)

    assert recovered.state == active.state
    assert recovered.experience_id == created.experience_id


def test_repository_rejects_duplicate_identity(tmp_path):
    store = tmp_path / "experience-store.json"
    repository = JsonFileExperienceRepository(store)

    experience = Experience.create()
    repository.add(experience)

    with pytest.raises(ExperienceAlreadyExistsError):
        repository.add(experience)


def test_repository_rejects_unknown_save(tmp_path):
    store = tmp_path / "experience-store.json"
    repository = JsonFileExperienceRepository(store)

    with pytest.raises(ExperienceNotFoundError):
        repository.save(Experience.create())


def test_repository_contains_persisted_identity(tmp_path):
    store = tmp_path / "experience-store.json"
    repository = JsonFileExperienceRepository(store)

    experience = Experience.create()
    repository.add(experience)

    replacement_repository = JsonFileExperienceRepository(store)

    assert replacement_repository.contains(
        experience.experience_id
    )


def test_invalid_json_is_explicit_corruption(tmp_path):
    store = tmp_path / "experience-store.json"
    store.write_text("{not-json", encoding="utf-8")

    repository = JsonFileExperienceRepository(store)

    with pytest.raises(ExperienceStoreCorruptionError):
        repository.contains(Experience.create().experience_id)


def test_wrong_store_shape_is_explicit_corruption(tmp_path):
    store = tmp_path / "experience-store.json"
    store.write_text(
        json.dumps({"wrong": "shape"}),
        encoding="utf-8",
    )

    repository = JsonFileExperienceRepository(store)

    with pytest.raises(ExperienceStoreCorruptionError):
        repository.contains(Experience.create().experience_id)


def test_embedded_identity_must_match_repository_key(tmp_path):
    store = tmp_path / "experience-store.json"

    repository = JsonFileExperienceRepository(store)
    experience = Experience.create()
    repository.add(experience)

    data = json.loads(store.read_text(encoding="utf-8"))

    original_key = str(experience.experience_id)
    other = Experience.create()

    data["experiences"][original_key]["experience_id"] = str(
        other.experience_id
    )

    store.write_text(
        json.dumps(data),
        encoding="utf-8",
    )

    replacement = JsonFileExperienceRepository(store)

    with pytest.raises(ExperienceStoreCorruptionError):
        replacement.get(experience.experience_id)


def test_missing_store_is_empty_not_fabricated_experience(tmp_path):
    store = tmp_path / "missing.json"
    repository = JsonFileExperienceRepository(store)

    experience = Experience.create()

    assert repository.contains(experience.experience_id) is False

    with pytest.raises(ExperienceNotFoundError):
        repository.get(experience.experience_id)


def test_storage_does_not_supply_authority(tmp_path):
    store = tmp_path / "experience-store.json"

    repository = JsonFileExperienceRepository(store)
    experience = Experience.create()
    repository.add(experience)

    recovered = JsonFileExperienceRepository(store).get(
        experience.experience_id
    )

    assert not hasattr(recovered, "authority")
    assert not hasattr(repository, "authority")

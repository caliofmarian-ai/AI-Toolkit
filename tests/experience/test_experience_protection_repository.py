import json

import pytest

from lib.python.experience.identity import ExperienceId
from lib.python.experience.protection import (
    ExperienceProtection,
    ProtectionState,
    UnauthorizedExperienceOperationError,
)
from lib.python.experience.protection_repository import (
    JsonFileProtectionRepository,
    ProtectionAlreadyExistsError,
    ProtectionNotFoundError,
    ProtectionStoreCorruptionError,
)


def new_identity():
    return ExperienceId.create()


def test_repository_add_and_get_preserve_protection(tmp_path):
    store = tmp_path / "protection.json"
    repository = JsonFileProtectionRepository(store)

    identity = new_identity()
    before = ExperienceProtection.protected(identity)

    repository.add(before)

    after = repository.get(identity)

    assert after == before
    assert after.experience_id == identity
    assert after.state is ProtectionState.PROTECTED


def test_repository_survives_repository_instance_replacement(tmp_path):
    store = tmp_path / "protection.json"

    identity = new_identity()

    writer = JsonFileProtectionRepository(store)
    writer.add(
        ExperienceProtection.protected(identity)
    )

    reader = JsonFileProtectionRepository(store)
    recovered = reader.get(identity)

    assert recovered.experience_id == identity
    assert recovered.state is ProtectionState.PROTECTED


def test_repository_preserves_unprotected_state(tmp_path):
    store = tmp_path / "protection.json"
    identity = new_identity()

    repository = JsonFileProtectionRepository(store)
    repository.add(
        ExperienceProtection.unprotected(identity)
    )

    recovered = JsonFileProtectionRepository(store).get(identity)

    assert recovered.state is ProtectionState.UNPROTECTED


def test_repository_save_changes_protection_without_identity_change(tmp_path):
    store = tmp_path / "protection.json"
    identity = new_identity()

    repository = JsonFileProtectionRepository(store)

    initial = ExperienceProtection.unprotected(identity)
    repository.add(initial)

    protected = initial.protect()
    repository.save(protected)

    recovered = JsonFileProtectionRepository(store).get(identity)

    assert recovered.experience_id == identity
    assert recovered.state is ProtectionState.PROTECTED


def test_repository_rejects_duplicate_add(tmp_path):
    store = tmp_path / "protection.json"
    identity = new_identity()

    repository = JsonFileProtectionRepository(store)
    protection = ExperienceProtection.protected(identity)

    repository.add(protection)

    with pytest.raises(ProtectionAlreadyExistsError):
        repository.add(protection)


def test_missing_protection_is_explicit(tmp_path):
    repository = JsonFileProtectionRepository(
        tmp_path / "protection.json"
    )

    with pytest.raises(ProtectionNotFoundError):
        repository.get(new_identity())


def test_save_unknown_protection_is_rejected(tmp_path):
    repository = JsonFileProtectionRepository(
        tmp_path / "protection.json"
    )

    with pytest.raises(ProtectionNotFoundError):
        repository.save(
            ExperienceProtection.protected(new_identity())
        )


def test_corrupt_json_is_rejected(tmp_path):
    store = tmp_path / "protection.json"
    store.write_text("{not-json", encoding="utf-8")

    repository = JsonFileProtectionRepository(store)

    with pytest.raises(ProtectionStoreCorruptionError):
        repository.contains(new_identity())


def test_repository_key_identity_disagreement_is_rejected(tmp_path):
    store = tmp_path / "protection.json"

    key_identity = new_identity()
    embedded_identity = new_identity()

    store.write_text(
        json.dumps(
            {
                "format_version": 1,
                "protections": {
                    str(key_identity): {
                        "experience_id": str(embedded_identity),
                        "state": "protected",
                    }
                },
            }
        ),
        encoding="utf-8",
    )

    repository = JsonFileProtectionRepository(store)

    with pytest.raises(ProtectionStoreCorruptionError):
        repository.get(key_identity)


def test_persisted_protected_state_does_not_authorize_operation(tmp_path):
    store = tmp_path / "protection.json"
    identity = new_identity()

    repository = JsonFileProtectionRepository(store)
    repository.add(
        ExperienceProtection.protected(identity)
    )

    recovered = JsonFileProtectionRepository(store).get(identity)

    with pytest.raises(UnauthorizedExperienceOperationError):
        recovered.require_authorized(authorized=False)

    recovered.require_authorized(authorized=True)


def test_core_experience_serialization_remains_independent(tmp_path):
    from lib.python.experience.model import Experience
    from lib.python.experience.persistence import serialize_experience

    experience = Experience.create()

    representation = serialize_experience(experience)

    assert set(representation) == {
        "experience_id",
        "created_at",
        "state",
    }

    assert "protection" not in representation
    assert "protection_state" not in representation

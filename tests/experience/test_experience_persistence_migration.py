from copy import deepcopy

import pytest

from lib.python.experience.model import Experience
from lib.python.experience.persistence import (
    CURRENT_SCHEMA_VERSION,
    ExperienceRecoveryError,
    migrate_experience_representation,
    recover_experience,
    serialize_experience,
)


def _legacy_representation(experience):
    current = serialize_experience(experience)

    return {
        "experience_id": current["experience_id"],
        "created_at": current["created_at"],
        "state": current["state"],
    }


def test_new_serialization_declares_current_schema_version():
    experience = Experience.create().activate()

    data = serialize_experience(experience)

    assert data["schema_version"] == CURRENT_SCHEMA_VERSION
    assert set(data) == {
        "schema_version",
        "experience_id",
        "created_at",
        "state",
    }


def test_legacy_unversioned_representation_migrates_to_current_schema():
    experience = Experience.create().activate()
    legacy = _legacy_representation(experience)

    migrated = migrate_experience_representation(legacy)

    assert migrated["schema_version"] == CURRENT_SCHEMA_VERSION
    assert migrated["experience_id"] == str(experience.experience_id)
    assert migrated["created_at"] == experience.created_at.isoformat()
    assert migrated["state"] == experience.state.value


def test_legacy_migration_does_not_mutate_original_representation():
    experience = Experience.create()
    legacy = _legacy_representation(experience)
    original = deepcopy(legacy)

    migrate_experience_representation(legacy)

    assert legacy == original


def test_recovery_accepts_legacy_representation_and_preserves_identity():
    before = Experience.create().activate()
    legacy = _legacy_representation(before)

    after = recover_experience(legacy)

    assert after.experience_id == before.experience_id
    assert after.created_at == before.created_at
    assert after.state == before.state


def test_recovery_accepts_current_version_and_preserves_identity():
    before = Experience.create().activate().close()

    current = serialize_experience(before)
    after = recover_experience(current)

    assert after.experience_id == before.experience_id
    assert after.created_at == before.created_at
    assert after.state == before.state


@pytest.mark.parametrize(
    "schema_version",
    [
        0,
        2,
        999,
        -1,
    ],
)
def test_unknown_or_unsupported_explicit_schema_versions_are_rejected(
    schema_version,
):
    experience = Experience.create()
    data = serialize_experience(experience)
    data["schema_version"] = schema_version

    with pytest.raises(ExperienceRecoveryError):
        recover_experience(data)


@pytest.mark.parametrize(
    "schema_version",
    [
        "1",
        1.0,
        True,
        None,
    ],
)
def test_invalid_schema_version_types_are_rejected(schema_version):
    experience = Experience.create()
    data = serialize_experience(experience)
    data["schema_version"] = schema_version

    with pytest.raises(ExperienceRecoveryError):
        recover_experience(data)


def test_migration_does_not_create_new_experience_identity(monkeypatch):
    before = Experience.create().activate()
    legacy = _legacy_representation(before)

    def forbidden_create(cls):
        raise AssertionError(
            "migration/recovery must not create a replacement identity"
        )

    from lib.python.experience.identity import ExperienceId

    monkeypatch.setattr(
        ExperienceId,
        "create",
        classmethod(forbidden_create),
    )

    after = recover_experience(legacy)

    assert after.experience_id == before.experience_id


def test_extra_fields_remain_rejected_after_versioning():
    experience = Experience.create()
    data = serialize_experience(experience)
    data["invented"] = "not-authorized"

    with pytest.raises(ExperienceRecoveryError):
        recover_experience(data)

from copy import deepcopy

import pytest

from lib.python.experience.identity import ExperienceId
from lib.python.experience.lifecycle import ExperienceState
from lib.python.experience.model import Experience
from lib.python.experience.persistence import (
    ExperienceRecoveryError,
    ExperienceSerializationError,
    recover_experience,
    serialize_experience,
)


def test_experience_serialization_contains_only_core_fields():
    experience = Experience.create().activate()

    data = serialize_experience(experience)

    assert set(data) == {
        "schema_version",
        "experience_id",
        "created_at",
        "state",
    }


def test_serialization_preserves_identity_value():
    experience = Experience.create()

    data = serialize_experience(experience)

    assert data["experience_id"] == str(experience.experience_id)


def test_recovery_reconstructs_same_identity_value():
    before = Experience.create().activate()

    data = serialize_experience(before)
    after = recover_experience(data)

    assert after.experience_id == before.experience_id
    assert str(after.experience_id) == str(before.experience_id)


def test_recovery_reconstructs_identity_object_without_using_create(monkeypatch):
    before = Experience.create()
    data = serialize_experience(before)

    def forbidden_create(cls):
        raise AssertionError(
            "ExperienceId.create() must not run during recovery"
        )

    monkeypatch.setattr(
        ExperienceId,
        "create",
        classmethod(forbidden_create),
    )

    after = recover_experience(data)

    assert after.experience_id == before.experience_id


def test_recovery_preserves_created_at():
    before = Experience.create().activate()

    after = recover_experience(
        serialize_experience(before)
    )

    assert after.created_at == before.created_at


def test_recovery_preserves_lifecycle_state():
    before = Experience.create().activate().close()

    after = recover_experience(
        serialize_experience(before)
    )

    assert after.state is ExperienceState.CLOSED


def test_serialization_rejects_non_experience():
    with pytest.raises(ExperienceSerializationError):
        serialize_experience(object())


@pytest.mark.parametrize(
    "data",
    [
        {},
        {
            "experience_id": str(ExperienceId.create()),
            "created_at": "2026-08-13T12:00:00+00:00",
        },
        {
            "experience_id": str(ExperienceId.create()),
            "created_at": "2026-08-13T12:00:00+00:00",
            "state": "created",
            "extra": "not-allowed",
        },
    ],
)
def test_recovery_rejects_invalid_field_sets(data):
    with pytest.raises(ExperienceRecoveryError):
        recover_experience(data)


def test_recovery_rejects_invalid_identity():
    experience = Experience.create()
    data = serialize_experience(experience)
    data["experience_id"] = "not-a-uuid"

    with pytest.raises(ExperienceRecoveryError):
        recover_experience(data)


def test_recovery_rejects_naive_created_at():
    experience = Experience.create()
    data = serialize_experience(experience)
    data["created_at"] = "2026-08-13T12:00:00"

    with pytest.raises(ExperienceRecoveryError):
        recover_experience(data)


def test_recovery_rejects_invalid_lifecycle_state():
    experience = Experience.create()
    data = serialize_experience(experience)
    data["state"] = "invented-state"

    with pytest.raises(ExperienceRecoveryError):
        recover_experience(data)


def test_recovery_does_not_mutate_serialized_representation():
    before = Experience.create().activate()
    data = serialize_experience(before)
    original = deepcopy(data)

    recover_experience(data)

    assert data == original

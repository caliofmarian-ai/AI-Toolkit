import pytest

from lib.python.experience.identity import ExperienceId
from lib.python.experience.protection import (
    ExperienceProtection,
    ProtectionState,
)
from lib.python.experience.protection_persistence import (
    ProtectionRecoveryError,
    ProtectionSerializationError,
    recover_protection,
    serialize_protection,
)


def new_identity():
    return ExperienceId.create()


@pytest.mark.parametrize(
    "state",
    [
        ProtectionState.UNPROTECTED,
        ProtectionState.PROTECTED,
    ],
)
def test_protection_round_trip_preserves_identity_and_state(state):
    identity = new_identity()

    before = ExperienceProtection(
        experience_id=identity,
        state=state,
    )

    after = recover_protection(
        serialize_protection(before)
    )

    assert after == before
    assert after.experience_id == identity
    assert after.state is state


def test_serialized_protection_contains_only_owned_state():
    protection = ExperienceProtection.protected(new_identity())

    representation = serialize_protection(protection)

    assert set(representation) == {
        "experience_id",
        "state",
    }

    assert "authority" not in representation
    assert "authorized" not in representation
    assert "session" not in representation
    assert "memory" not in representation
    assert "evidence" not in representation


def test_serialize_rejects_non_protection_object():
    with pytest.raises(ProtectionSerializationError):
        serialize_protection(object())


def test_recovery_rejects_missing_fields():
    with pytest.raises(ProtectionRecoveryError):
        recover_protection(
            {
                "experience_id": str(new_identity()),
            }
        )


def test_recovery_rejects_unexpected_fields():
    with pytest.raises(ProtectionRecoveryError):
        recover_protection(
            {
                "experience_id": str(new_identity()),
                "state": "protected",
                "authority": True,
            }
        )


def test_recovery_rejects_invalid_identity():
    with pytest.raises(ProtectionRecoveryError):
        recover_protection(
            {
                "experience_id": "not-an-experience-id",
                "state": "protected",
            }
        )


def test_recovery_rejects_invalid_state():
    with pytest.raises(ProtectionRecoveryError):
        recover_protection(
            {
                "experience_id": str(new_identity()),
                "state": "unknown",
            }
        )


def test_recovered_protected_state_does_not_supply_authorization():
    before = ExperienceProtection.protected(new_identity())

    recovered = recover_protection(
        serialize_protection(before)
    )

    with pytest.raises(Exception):
        recovered.require_authorized(authorized=False)

    recovered.require_authorized(authorized=True)

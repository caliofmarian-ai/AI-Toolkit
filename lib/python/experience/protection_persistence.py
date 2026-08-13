"""Persistence representation for the Experience Protection organ.

Protection remains distinct from Experience.

Experience != Protection.
Storage != Experience.
Persistence != authority.

A persisted PROTECTED condition records state.
It does not grant authorization.
"""

from __future__ import annotations

from typing import Any, Mapping

from .identity import ExperienceId, ExperienceIdentityError
from .protection import ExperienceProtection, ProtectionState


class ProtectionPersistenceError(RuntimeError):
    """Base error for Protection persistence failures."""


class ProtectionSerializationError(ProtectionPersistenceError):
    """Raised when Protection cannot be serialized safely."""


class ProtectionRecoveryError(ProtectionPersistenceError):
    """Raised when persisted Protection cannot be recovered safely."""


_REQUIRED_FIELDS = frozenset(
    {
        "experience_id",
        "state",
    }
)


def serialize_protection(
    protection: ExperienceProtection,
) -> dict[str, str]:
    """Serialize exactly the persistent state owned by Protection."""

    if not isinstance(protection, ExperienceProtection):
        raise ProtectionSerializationError(
            "serialize_protection requires ExperienceProtection"
        )

    return {
        "experience_id": str(protection.experience_id),
        "state": protection.state.value,
    }


def recover_protection(
    data: Mapping[str, Any],
) -> ExperienceProtection:
    """Recover Protection without generating a new Experience identity."""

    if not isinstance(data, Mapping):
        raise ProtectionRecoveryError(
            "persisted Protection representation must be a mapping"
        )

    fields = frozenset(data.keys())

    if fields != _REQUIRED_FIELDS:
        missing = sorted(_REQUIRED_FIELDS - fields)
        unexpected = sorted(fields - _REQUIRED_FIELDS)

        raise ProtectionRecoveryError(
            "invalid persisted Protection fields; "
            f"missing={missing}, unexpected={unexpected}"
        )

    experience_id_raw = data["experience_id"]
    state_raw = data["state"]

    if not isinstance(experience_id_raw, str):
        raise ProtectionRecoveryError(
            "persisted Protection experience_id must be a string"
        )

    if not isinstance(state_raw, str):
        raise ProtectionRecoveryError(
            "persisted Protection state must be a string"
        )

    try:
        experience_id = ExperienceId.from_string(experience_id_raw)
    except ExperienceIdentityError as exc:
        raise ProtectionRecoveryError(
            "persisted Protection identity is invalid"
        ) from exc

    try:
        state = ProtectionState(state_raw)
    except ValueError as exc:
        raise ProtectionRecoveryError(
            "persisted Protection state is invalid"
        ) from exc

    return ExperienceProtection(
        experience_id=experience_id,
        state=state,
    )

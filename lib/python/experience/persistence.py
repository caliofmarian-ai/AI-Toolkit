"""Serialization boundary for PCC-01 Persistent Experience.

Serialization is a transport/storage representation of Experience.

Storage != Experience.
Persistence != authority.
Interpretation != historical fact.

Recovery must reconstruct the persisted Experience identity.
It must never generate a replacement identity.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Mapping

from .identity import ExperienceId, ExperienceIdentityError
from .lifecycle import ExperienceState
from .model import Experience


class ExperiencePersistenceError(RuntimeError):
    """Base error for Experience persistence representation failures."""


class ExperienceSerializationError(ExperiencePersistenceError):
    """Raised when an Experience cannot be serialized safely."""


class ExperienceRecoveryError(ExperiencePersistenceError):
    """Raised when persisted Experience data cannot be recovered safely."""


_REQUIRED_FIELDS = frozenset(
    {
        "experience_id",
        "created_at",
        "state",
    }
)


def serialize_experience(experience: Experience) -> dict[str, str]:
    """Serialize exactly the minimum Core Experience state."""

    if not isinstance(experience, Experience):
        raise ExperienceSerializationError(
            "serialize_experience requires an Experience"
        )

    return {
        "experience_id": str(experience.experience_id),
        "created_at": experience.created_at.isoformat(),
        "state": experience.state.value,
    }


def recover_experience(data: Mapping[str, Any]) -> Experience:
    """Recover one existing Experience without regenerating identity."""

    if not isinstance(data, Mapping):
        raise ExperienceRecoveryError(
            "persisted Experience representation must be a mapping"
        )

    fields = frozenset(data.keys())

    if fields != _REQUIRED_FIELDS:
        missing = sorted(_REQUIRED_FIELDS - fields)
        unexpected = sorted(fields - _REQUIRED_FIELDS)

        raise ExperienceRecoveryError(
            "invalid persisted Experience fields; "
            f"missing={missing}, unexpected={unexpected}"
        )

    experience_id_raw = data["experience_id"]
    created_at_raw = data["created_at"]
    state_raw = data["state"]

    if not isinstance(experience_id_raw, str):
        raise ExperienceRecoveryError(
            "persisted experience_id must be a string"
        )

    if not isinstance(created_at_raw, str):
        raise ExperienceRecoveryError(
            "persisted created_at must be a string"
        )

    if not isinstance(state_raw, str):
        raise ExperienceRecoveryError(
            "persisted state must be a string"
        )

    try:
        experience_id = ExperienceId.from_string(experience_id_raw)
    except ExperienceIdentityError as exc:
        raise ExperienceRecoveryError(
            "persisted Experience identity is invalid"
        ) from exc

    try:
        created_at = datetime.fromisoformat(created_at_raw)
    except ValueError as exc:
        raise ExperienceRecoveryError(
            "persisted created_at is invalid"
        ) from exc

    if created_at.tzinfo is None:
        raise ExperienceRecoveryError(
            "persisted created_at must be timezone-aware"
        )

    try:
        state = ExperienceState(state_raw)
    except ValueError as exc:
        raise ExperienceRecoveryError(
            "persisted Experience state is invalid"
        ) from exc

    return Experience(
        experience_id=experience_id,
        created_at=created_at,
        state=state,
    )

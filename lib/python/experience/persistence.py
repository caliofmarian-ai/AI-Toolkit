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


CURRENT_SCHEMA_VERSION = 1

_LEGACY_FIELDS = frozenset(
    {
        "experience_id",
        "created_at",
        "state",
    }
)

_REQUIRED_FIELDS = frozenset(
    {
        "schema_version",
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
        "schema_version": CURRENT_SCHEMA_VERSION,
        "experience_id": str(experience.experience_id),
        "created_at": experience.created_at.isoformat(),
        "state": experience.state.value,
    }


def migrate_experience_representation(
    data: Mapping[str, Any],
) -> dict[str, Any]:
    """Normalize a supported persisted Experience representation.

    The original unversioned representation is schema version 0.
    Migration adds only persistence metadata. It must not generate,
    replace, or reinterpret Experience identity.
    """

    if not isinstance(data, Mapping):
        raise ExperienceRecoveryError(
            "persisted Experience representation must be a mapping"
        )

    fields = frozenset(data.keys())

    if fields == _LEGACY_FIELDS:
        migrated = dict(data)
        migrated["schema_version"] = CURRENT_SCHEMA_VERSION
        return migrated

    if fields != _REQUIRED_FIELDS:
        missing = sorted(_REQUIRED_FIELDS - fields)
        unexpected = sorted(fields - _REQUIRED_FIELDS)

        raise ExperienceRecoveryError(
            "invalid persisted Experience fields; "
            f"missing={missing}, unexpected={unexpected}"
        )

    schema_version = data["schema_version"]

    if (
        isinstance(schema_version, bool)
        or not isinstance(schema_version, int)
    ):
        raise ExperienceRecoveryError(
            "persisted schema_version must be an integer"
        )

    if schema_version != CURRENT_SCHEMA_VERSION:
        raise ExperienceRecoveryError(
            "unsupported persisted Experience schema_version: "
            f"{schema_version}"
        )

    return dict(data)


def recover_experience(data: Mapping[str, Any]) -> Experience:
    """Recover one existing Experience without regenerating identity."""

    migrated = migrate_experience_representation(data)

    experience_id_raw = migrated["experience_id"]
    created_at_raw = migrated["created_at"]
    state_raw = migrated["state"]

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

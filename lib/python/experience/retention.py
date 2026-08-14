"""Retention physiology for PCC-01 Persistent Experience.

Retention is an explicit domain organ.

Retention answers whether an identified Experience is intentionally
preserved under an explicit retention rule.

Retention is not Protection.
Retention is not Forgetting.
Retention is not archival.
Retention is not accidental survival in storage.
Persistence does not itself imply retention.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum

from .identity import ExperienceId


class ExperienceRetentionError(Exception):
    """Base error for Experience retention violations."""


class InvalidRetentionIdentityError(ExperienceRetentionError):
    """Raised when retention receives an invalid Experience identity."""


class InvalidRetentionReasonError(ExperienceRetentionError):
    """Raised when an explicit retention reason is absent or invalid."""


class RetentionState(str, Enum):
    """Observable retention condition of an Experience."""

    UNRETAINED = "unretained"
    RETAINED = "retained"


@dataclass(frozen=True, slots=True)
class ExperienceRetention:
    """Explicit retention state for exactly one Experience identity.

    The Retention organ references Experience identity without owning
    or redefining it.

    A retained Experience is intentionally preserved.
    This state does not grant authority and does not mean that the
    Experience can never later enter an explicitly authorized
    forgetting physiology.
    """

    experience_id: ExperienceId
    state: RetentionState
    reason: str | None = None
    retained_at: datetime | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.experience_id, ExperienceId):
            raise InvalidRetentionIdentityError(
                "experience_id must be an ExperienceId"
            )

        if self.state is RetentionState.UNRETAINED:
            if self.reason is not None:
                raise InvalidRetentionReasonError(
                    "unretained Experience cannot carry a retention reason"
                )

            if self.retained_at is not None:
                raise ExperienceRetentionError(
                    "unretained Experience cannot carry retained_at"
                )

        if self.state is RetentionState.RETAINED:
            _require_reason(self.reason)

            if self.retained_at is None:
                raise ExperienceRetentionError(
                    "retained Experience requires retained_at"
                )

            if self.retained_at.tzinfo is None:
                raise ExperienceRetentionError(
                    "retained_at must be timezone-aware"
                )

    @classmethod
    def unretained(
        cls,
        experience_id: ExperienceId,
    ) -> "ExperienceRetention":
        return cls(
            experience_id=experience_id,
            state=RetentionState.UNRETAINED,
        )

    def retain(
        self,
        *,
        reason: str,
        retained_at: datetime | None = None,
    ) -> "ExperienceRetention":
        """Intentionally retain the same Experience identity."""

        normalized_reason = _require_reason(reason)

        if retained_at is None:
            retained_at = datetime.now(timezone.utc)

        if retained_at.tzinfo is None:
            raise ExperienceRetentionError(
                "retained_at must be timezone-aware"
            )

        if self.state is RetentionState.RETAINED:
            if self.reason == normalized_reason:
                return self

            raise ExperienceRetentionError(
                "retained Experience cannot silently replace its retention reason"
            )

        return ExperienceRetention(
            experience_id=self.experience_id,
            state=RetentionState.RETAINED,
            reason=normalized_reason,
            retained_at=retained_at,
        )

    @property
    def is_retained(self) -> bool:
        return self.state is RetentionState.RETAINED


def _require_reason(value: str | None) -> str:
    if not isinstance(value, str):
        raise InvalidRetentionReasonError(
            "retention reason must be a non-empty string"
        )

    normalized = value.strip()

    if not normalized:
        raise InvalidRetentionReasonError(
            "retention reason must be a non-empty string"
        )

    return normalized

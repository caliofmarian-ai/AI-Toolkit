"""Controlled forgetting physiology for PCC-01 Persistent Experience.

Forgetting is an explicit, intentional and inspectable operation.

Forgetting is not accidental data loss.
Forgetting is not retention.
Forgetting is not protection.
Forgetting is not archival.
Forgetting does not rewrite Experience identity.

The organ records that an identified Experience has entered an
explicit forgetting condition under a stated reason and authorization.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum

from .identity import ExperienceId


class ExperienceForgettingError(Exception):
    """Base error for Experience forgetting violations."""


class InvalidForgettingIdentityError(ExperienceForgettingError):
    """Raised when forgetting receives an invalid Experience identity."""


class InvalidForgettingReasonError(ExperienceForgettingError):
    """Raised when forgetting lacks an explicit reason."""


class UnauthorizedForgettingError(ExperienceForgettingError):
    """Raised when forgetting is attempted without explicit authorization."""


class ForgettingState(str, Enum):
    """Observable forgetting condition."""

    PRESENT = "present"
    FORGOTTEN = "forgotten"


@dataclass(frozen=True, slots=True)
class ExperienceForgetting:
    """Forgetting state associated with one persistent Experience identity."""

    experience_id: ExperienceId
    state: ForgettingState
    reason: str | None = None
    forgotten_at: datetime | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.experience_id, ExperienceId):
            raise InvalidForgettingIdentityError(
                "experience_id must be an ExperienceId"
            )

        if self.state is ForgettingState.PRESENT:
            if self.reason is not None:
                raise InvalidForgettingReasonError(
                    "present Experience cannot carry a forgetting reason"
                )

            if self.forgotten_at is not None:
                raise ExperienceForgettingError(
                    "present Experience cannot carry forgotten_at"
                )

        if self.state is ForgettingState.FORGOTTEN:
            _require_reason(self.reason)

            if self.forgotten_at is None:
                raise ExperienceForgettingError(
                    "forgotten Experience requires forgotten_at"
                )

            if self.forgotten_at.tzinfo is None:
                raise ExperienceForgettingError(
                    "forgotten_at must be timezone-aware"
                )

    @classmethod
    def present(
        cls,
        experience_id: ExperienceId,
    ) -> "ExperienceForgetting":
        return cls(
            experience_id=experience_id,
            state=ForgettingState.PRESENT,
        )

    def forget(
        self,
        *,
        reason: str,
        authorized: bool,
        forgotten_at: datetime | None = None,
    ) -> "ExperienceForgetting":
        """Enter controlled forgetting without redefining identity."""

        if not isinstance(authorized, bool):
            raise TypeError("authorized must be bool")

        if not authorized:
            raise UnauthorizedForgettingError(
                "forgetting requires explicit authorization"
            )

        normalized_reason = _require_reason(reason)

        if forgotten_at is None:
            forgotten_at = datetime.now(timezone.utc)

        if forgotten_at.tzinfo is None:
            raise ExperienceForgettingError(
                "forgotten_at must be timezone-aware"
            )

        if self.state is ForgettingState.FORGOTTEN:
            if self.reason == normalized_reason:
                return self

            raise ExperienceForgettingError(
                "forgotten Experience cannot silently rewrite forgetting reason"
            )

        return ExperienceForgetting(
            experience_id=self.experience_id,
            state=ForgettingState.FORGOTTEN,
            reason=normalized_reason,
            forgotten_at=forgotten_at,
        )

    @property
    def is_forgotten(self) -> bool:
        return self.state is ForgettingState.FORGOTTEN


def _require_reason(value: str | None) -> str:
    if not isinstance(value, str):
        raise InvalidForgettingReasonError(
            "forgetting reason must be a non-empty string"
        )

    normalized = value.strip()

    if not normalized:
        raise InvalidForgettingReasonError(
            "forgetting reason must be a non-empty string"
        )

    return normalized

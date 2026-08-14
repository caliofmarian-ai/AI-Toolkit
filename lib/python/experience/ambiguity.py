"""Ambiguity representation for PCC-01 Persistent Experience.

Ambiguity preserves uncertainty explicitly.

Unknown is allowed to remain unknown.
Ambiguity is not conflict.
Confidence is not truth.
Representation does not fabricate resolution.
"""

from __future__ import annotations

from dataclasses import dataclass

from .identity import ExperienceId


class ExperienceAmbiguityError(Exception):
    """Base error for Experience ambiguity representation."""


class InvalidAmbiguityDescriptionError(ExperienceAmbiguityError):
    """Raised when ambiguity lacks an explicit description."""


class InvalidConfidenceError(ExperienceAmbiguityError):
    """Raised when confidence is outside the accepted interval."""


@dataclass(frozen=True, slots=True)
class ExperienceAmbiguity:
    """Explicit unresolved uncertainty associated with an Experience."""

    experience_id: ExperienceId
    description: str
    confidence: float | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.experience_id, ExperienceId):
            raise TypeError("experience_id must be an ExperienceId")

        if (
            not isinstance(self.description, str)
            or not self.description.strip()
        ):
            raise InvalidAmbiguityDescriptionError(
                "ambiguity description must be non-empty"
            )

        if self.confidence is not None:
            if isinstance(self.confidence, bool) or not isinstance(
                self.confidence,
                (int, float),
            ):
                raise InvalidConfidenceError(
                    "confidence must be numeric or None"
                )

            if not 0.0 <= float(self.confidence) <= 1.0:
                raise InvalidConfidenceError(
                    "confidence must be between 0.0 and 1.0"
                )

    @property
    def is_unknown(self) -> bool:
        return self.confidence is None

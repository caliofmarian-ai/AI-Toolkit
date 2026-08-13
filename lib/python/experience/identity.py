"""Stable identity for PCC-01 Core Experience."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID, uuid4


class ExperienceIdentityError(ValueError):
    """Raised when an Experience identity is malformed."""


@dataclass(frozen=True, slots=True)
class ExperienceId:
    """Immutable identity belonging to one Experience."""

    value: str

    def __post_init__(self) -> None:
        try:
            parsed = UUID(self.value)
        except (ValueError, TypeError, AttributeError) as exc:
            raise ExperienceIdentityError(
                f"Invalid Experience identity: {self.value!r}"
            ) from exc

        canonical = str(parsed)

        if self.value != canonical:
            raise ExperienceIdentityError(
                "Experience identity must use canonical UUID representation"
            )

    @classmethod
    def create(cls) -> "ExperienceId":
        """Create a new Experience identity."""
        return cls(str(uuid4()))

    @classmethod
    def from_string(cls, value: str) -> "ExperienceId":
        """Reconstruct an existing identity without regeneration."""
        return cls(value)

    def __str__(self) -> str:
        return self.value

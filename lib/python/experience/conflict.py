"""Conflict representation for PCC-01 Persistent Experience.

Conflict preserves incompatible claims without silently selecting,
rewriting or deleting one of them.

Representation is not resolution.
Conflict is not ambiguity.
Conflict does not redefine Experience identity.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable

from .identity import ExperienceId


class ExperienceConflictError(Exception):
    """Base error for Experience conflict representation."""


class InvalidConflictAlternativeError(ExperienceConflictError):
    """Raised when a conflict alternative is invalid."""


class ConflictState(str, Enum):
    OPEN = "open"
    RESOLVED = "resolved"


@dataclass(frozen=True, slots=True)
class ConflictAlternative:
    """One preserved alternative participating in a conflict."""

    label: str
    statement: str

    def __post_init__(self) -> None:
        if not isinstance(self.label, str) or not self.label.strip():
            raise InvalidConflictAlternativeError(
                "alternative label must be non-empty"
            )

        if not isinstance(self.statement, str) or not self.statement.strip():
            raise InvalidConflictAlternativeError(
                "alternative statement must be non-empty"
            )


@dataclass(frozen=True, slots=True)
class ExperienceConflict:
    """Explicit unresolved conflict attached to one Experience."""

    experience_id: ExperienceId
    alternatives: tuple[ConflictAlternative, ...]
    state: ConflictState = ConflictState.OPEN

    def __post_init__(self) -> None:
        if not isinstance(self.experience_id, ExperienceId):
            raise TypeError("experience_id must be an ExperienceId")

        if len(self.alternatives) < 2:
            raise ExperienceConflictError(
                "conflict requires at least two preserved alternatives"
            )

        labels = tuple(item.label.strip() for item in self.alternatives)

        if len(set(labels)) != len(labels):
            raise ExperienceConflictError(
                "conflict alternatives require distinct labels"
            )

    @classmethod
    def open(
        cls,
        *,
        experience_id: ExperienceId,
        alternatives: Iterable[ConflictAlternative],
    ) -> "ExperienceConflict":
        return cls(
            experience_id=experience_id,
            alternatives=tuple(alternatives),
            state=ConflictState.OPEN,
        )

    @property
    def is_open(self) -> bool:
        return self.state is ConflictState.OPEN

    def statements(self) -> tuple[str, ...]:
        return tuple(
            alternative.statement
            for alternative in self.alternatives
        )

"""Domain anatomy of one PCC-01 Core Experience."""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime, timezone

from .identity import ExperienceId
from .lifecycle import ExperienceState, transition


@dataclass(frozen=True, slots=True)
class Experience:
    """One Core Experience domain entity.

    Experience remains distinct from Session, Memory, Evidence,
    raw dialogue, process, provider, storage, and authority.
    """

    experience_id: ExperienceId
    created_at: datetime
    state: ExperienceState

    def __post_init__(self) -> None:
        if self.created_at.tzinfo is None:
            raise ValueError("Experience created_at must be timezone-aware")

    @classmethod
    def create(cls) -> "Experience":
        """Create a new Experience in CREATED state."""
        return cls(
            experience_id=ExperienceId.create(),
            created_at=datetime.now(timezone.utc),
            state=ExperienceState.CREATED,
        )

    def activate(self) -> "Experience":
        """Transition CREATED -> ACTIVE while preserving identity."""
        return replace(
            self,
            state=transition(self.state, ExperienceState.ACTIVE),
        )

    def close(self) -> "Experience":
        """Transition ACTIVE -> CLOSED while preserving identity."""
        return replace(
            self,
            state=transition(self.state, ExperienceState.CLOSED),
        )

"""Lifecycle physiology for PCC-01 Core Experience."""

from __future__ import annotations

from enum import Enum


class ExperienceLifecycleError(ValueError):
    """Raised when an illegal Experience lifecycle transition is requested."""


class ExperienceState(str, Enum):
    """Initial Core Experience lifecycle states."""

    CREATED = "CREATED"
    ACTIVE = "ACTIVE"
    CLOSED = "CLOSED"


_ALLOWED_TRANSITIONS: dict[ExperienceState, ExperienceState] = {
    ExperienceState.CREATED: ExperienceState.ACTIVE,
    ExperienceState.ACTIVE: ExperienceState.CLOSED,
}


def transition(
    current: ExperienceState,
    target: ExperienceState,
) -> ExperienceState:
    """Validate one Core Experience lifecycle transition."""

    expected = _ALLOWED_TRANSITIONS.get(current)

    if expected is not target:
        raise ExperienceLifecycleError(
            f"Illegal Experience lifecycle transition: "
            f"{current.value} -> {target.value}"
        )

    return target

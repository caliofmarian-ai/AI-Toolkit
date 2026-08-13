"""Explicit Session-to-Experience binding for PCC-01.

This module defines relational tissue only.

It does not define Session itself and does not alter Experience.

Epistemic boundaries:

    Experience != Session
    Experience != Memory
    Experience != Evidence
    Experience != raw dialogue
    Session != process
    Session != provider
    Storage != Experience
    Interpretation != historical fact
    Persistence != authority
    Human Acceptance != Implementation
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import NewType

from .identity import ExperienceId


SessionId = NewType("SessionId", str)


class SessionBindingError(ValueError):
    """Base error for invalid Session/Experience binding operations."""


class InvalidSessionIdError(SessionBindingError):
    """Raised when a Session identity is invalid."""


class InvalidExperienceBindingError(SessionBindingError):
    """Raised when an Experience identity is invalid for binding."""


def normalize_session_id(value: str) -> SessionId:
    """Validate and normalize an external Session identity."""

    if not isinstance(value, str):
        raise InvalidSessionIdError("session_id must be a string")

    normalized = value.strip()

    if not normalized:
        raise InvalidSessionIdError("session_id must not be empty")

    return SessionId(normalized)


def validate_experience_id(value: ExperienceId) -> ExperienceId:
    """Require the established Core Experience identity type.

    Session Binding consumes ExperienceId exactly as defined by the
    Experience organ.  It does not convert Experience identity into
    Session identity or replace it with a parallel representation.
    """

    if not isinstance(value, ExperienceId):
        raise InvalidExperienceBindingError(
            "experience_id must be an ExperienceId"
        )

    return value


@dataclass(frozen=True, slots=True)
class SessionBinding:
    """Relationship between one Session identity and one Experience identity.

    The binding owns neither organ and owns neither lifecycle.
    """

    session_id: SessionId
    experience_id: ExperienceId

    @classmethod
    def create(
        cls,
        *,
        session_id: str,
        experience_id: ExperienceId,
    ) -> "SessionBinding":
        return cls(
            session_id=normalize_session_id(session_id),
            experience_id=validate_experience_id(experience_id),
        )

    def belongs_to_experience(self, experience_id: ExperienceId) -> bool:
        """Return whether this binding references the supplied Experience."""

        if not isinstance(experience_id, ExperienceId):
            return False

        return self.experience_id == experience_id

    def belongs_to_session(self, session_id: str) -> bool:
        """Return whether this binding references the supplied Session."""

        try:
            normalized = normalize_session_id(session_id)
        except InvalidSessionIdError:
            return False

        return self.session_id == normalized

"""Repository boundary for PCC-01 Core Experience."""

from __future__ import annotations

from abc import ABC, abstractmethod

from .identity import ExperienceId
from .model import Experience


class ExperienceRepositoryError(RuntimeError):
    """Base error for Experience repository operations."""


class ExperienceNotFoundError(ExperienceRepositoryError):
    """Raised when an Experience cannot be found by its identity."""


class ExperienceAlreadyExistsError(ExperienceRepositoryError):
    """Raised when creation would replace an existing Experience."""


class ExperienceRepository(ABC):
    """Storage-independent contract for Core Experience.

    The repository stores and retrieves Experience state.

    Storage is not Experience.
    Persistence is not authority.
    """

    @abstractmethod
    def add(self, experience: Experience) -> None:
        """Store a newly admitted Experience without replacement."""

    @abstractmethod
    def get(self, experience_id: ExperienceId) -> Experience:
        """Return one Experience by stable Experience identity."""

    @abstractmethod
    def save(self, experience: Experience) -> None:
        """Persist the current state of an already admitted Experience."""

    @abstractmethod
    def contains(self, experience_id: ExperienceId) -> bool:
        """Return whether this repository knows the Experience identity."""


class InMemoryExperienceRepository(ExperienceRepository):
    """Minimal repository implementation for Core behavioral tests.

    This implementation is intentionally process-local.

    It does NOT demonstrate persistence across real process death.
    """

    def __init__(self) -> None:
        self._experiences: dict[ExperienceId, Experience] = {}

    def add(self, experience: Experience) -> None:
        if experience.experience_id in self._experiences:
            raise ExperienceAlreadyExistsError(
                f"Experience already exists: {experience.experience_id}"
            )

        self._experiences[experience.experience_id] = experience

    def get(self, experience_id: ExperienceId) -> Experience:
        try:
            return self._experiences[experience_id]
        except KeyError as exc:
            raise ExperienceNotFoundError(
                f"Experience not found: {experience_id}"
            ) from exc

    def save(self, experience: Experience) -> None:
        if experience.experience_id not in self._experiences:
            raise ExperienceNotFoundError(
                f"Cannot save unknown Experience: {experience.experience_id}"
            )

        self._experiences[experience.experience_id] = experience

    def contains(self, experience_id: ExperienceId) -> bool:
        return experience_id in self._experiences

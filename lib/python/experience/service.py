"""Application physiology for PCC-01 Core Experience."""

from __future__ import annotations

from .identity import ExperienceId
from .model import Experience
from .repository import ExperienceRepository


class ExperienceService:
    """Coordinates Core Experience behavior.

    The service does not own Experience identity.
    The service does not become Session, Memory, Evidence, or authority.
    """

    def __init__(self, repository: ExperienceRepository) -> None:
        self._repository = repository

    def create_experience(self) -> Experience:
        """Create and admit a new Experience."""
        experience = Experience.create()
        self._repository.add(experience)
        return experience

    def get_experience(self, experience_id: ExperienceId) -> Experience:
        """Inspect an admitted Experience by stable identity."""
        return self._repository.get(experience_id)

    def activate_experience(
        self,
        experience_id: ExperienceId,
    ) -> Experience:
        """Activate an admitted Experience while preserving identity."""
        current = self._repository.get(experience_id)
        active = current.activate()
        self._repository.save(active)
        return active

    def close_experience(
        self,
        experience_id: ExperienceId,
    ) -> Experience:
        """Close an active Experience while preserving identity."""
        current = self._repository.get(experience_id)
        closed = current.close()
        self._repository.save(closed)
        return closed

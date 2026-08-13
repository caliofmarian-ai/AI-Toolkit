"""Coordination physiology for persistent Experience and Protection.

Experience and Protection remain independent organs.

The coordinator does not become Experience.
The coordinator does not become Protection.
The coordinator does not grant authority.

Its responsibility is to make the physiological relationship between
their persistence operations explicit and inspectable.

Persistence != authority.
Storage != Experience.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Callable

from .identity import ExperienceId
from .model import Experience
from .persistent_repository import JsonFileExperienceRepository
from .protection import ExperienceProtection
from .protection_repository import JsonFileProtectionRepository


class PersistenceCoordinationError(RuntimeError):
    """Base error for coordinated Experience persistence."""


class PersistenceCoordinationIdentityError(PersistenceCoordinationError):
    """Raised when coordinated organs do not share one ExperienceId."""


class PersistenceCoordinationStateError(PersistenceCoordinationError):
    """Raised when durable organs do not form a valid coordinated pair."""


class CoordinationStage(str, Enum):
    """Observable physiological stage of one coordination operation."""

    PREPARING = "preparing"
    PROTECTION_WRITTEN = "protection_written"
    EXPERIENCE_WRITTEN = "experience_written"
    COMPLETE = "complete"


@dataclass(frozen=True, slots=True)
class CoordinationState:
    """Observable state of one persistence coordination operation."""

    experience_id: ExperienceId
    stage: CoordinationStage


@dataclass(frozen=True, slots=True)
class CoordinatedExperience:
    """Recovered pair of distinct organs sharing one Experience identity."""

    experience: Experience
    protection: ExperienceProtection

    def __post_init__(self) -> None:
        if self.experience.experience_id != self.protection.experience_id:
            raise PersistenceCoordinationIdentityError(
                "Experience and Protection identities disagree"
            )


StageObserver = Callable[[CoordinationState], None]


class ExperiencePersistenceCoordinator:
    """Coordinates persistence without collapsing organ boundaries.

    The repositories remain responsible for their own durable bodies.

    This first implementation makes the physiological write order and
    failure boundary explicit.  Durable journal persistence is NOT yet
    claimed by this class.
    """

    def __init__(
        self,
        experience_repository: JsonFileExperienceRepository,
        protection_repository: JsonFileProtectionRepository,
    ) -> None:
        if not isinstance(
            experience_repository,
            JsonFileExperienceRepository,
        ):
            raise TypeError(
                "experience_repository must be "
                "JsonFileExperienceRepository"
            )

        if not isinstance(
            protection_repository,
            JsonFileProtectionRepository,
        ):
            raise TypeError(
                "protection_repository must be "
                "JsonFileProtectionRepository"
            )

        self._experience_repository = experience_repository
        self._protection_repository = protection_repository

    def persist(
        self,
        experience: Experience,
        protection: ExperienceProtection,
        *,
        observe_stage: StageObserver | None = None,
    ) -> CoordinatedExperience:
        """Persist the two organs through one explicit physiological path.

        Protection is conserved before Experience so protected material
        is never intentionally persisted first as an unprotected
        Experience.

        This method does NOT claim crash atomicity.
        """

        self._require_matching_identity(experience, protection)

        self._observe(
            CoordinationState(
                experience_id=experience.experience_id,
                stage=CoordinationStage.PREPARING,
            ),
            observe_stage,
        )

        self._persist_protection(protection)

        self._observe(
            CoordinationState(
                experience_id=experience.experience_id,
                stage=CoordinationStage.PROTECTION_WRITTEN,
            ),
            observe_stage,
        )

        self._persist_experience(experience)

        self._observe(
            CoordinationState(
                experience_id=experience.experience_id,
                stage=CoordinationStage.EXPERIENCE_WRITTEN,
            ),
            observe_stage,
        )

        pair = self.recover(experience.experience_id)

        self._observe(
            CoordinationState(
                experience_id=experience.experience_id,
                stage=CoordinationStage.COMPLETE,
            ),
            observe_stage,
        )

        return pair

    def recover(
        self,
        experience_id: ExperienceId,
    ) -> CoordinatedExperience:
        """Recover both durable organs and verify their relationship."""

        if not isinstance(experience_id, ExperienceId):
            raise TypeError(
                "experience_id must be an ExperienceId"
            )

        experience_exists = self._experience_repository.contains(
            experience_id
        )
        protection_exists = self._protection_repository.contains(
            experience_id
        )

        if not experience_exists and not protection_exists:
            raise PersistenceCoordinationStateError(
                "no durable Experience/Protection pair exists"
            )

        if experience_exists and not protection_exists:
            raise PersistenceCoordinationStateError(
                "partial durable pair: Protection is missing"
            )

        if protection_exists and not experience_exists:
            raise PersistenceCoordinationStateError(
                "partial durable pair: orphan Protection exists"
            )

        experience = self._experience_repository.get(experience_id)
        protection = self._protection_repository.get(experience_id)

        self._require_matching_identity(experience, protection)

        return CoordinatedExperience(
            experience=experience,
            protection=protection,
        )

    def _persist_protection(
        self,
        protection: ExperienceProtection,
    ) -> None:
        if self._protection_repository.contains(
            protection.experience_id
        ):
            self._protection_repository.save(protection)
        else:
            self._protection_repository.add(protection)

    def _persist_experience(
        self,
        experience: Experience,
    ) -> None:
        if self._experience_repository.contains(
            experience.experience_id
        ):
            self._experience_repository.save(experience)
        else:
            self._experience_repository.add(experience)

    @staticmethod
    def _require_matching_identity(
        experience: Experience,
        protection: ExperienceProtection,
    ) -> None:
        if not isinstance(experience, Experience):
            raise TypeError("experience must be an Experience")

        if not isinstance(protection, ExperienceProtection):
            raise TypeError(
                "protection must be ExperienceProtection"
            )

        if experience.experience_id != protection.experience_id:
            raise PersistenceCoordinationIdentityError(
                "Experience and Protection must share one ExperienceId"
            )

    @staticmethod
    def _observe(
        state: CoordinationState,
        observer: StageObserver | None,
    ) -> None:
        if observer is not None:
            observer(state)

"""Coordination physiology for persistent Experience and Protection.

Experience and Protection remain independent organs.

The Durable Coordination Journal is also a distinct organ.

The coordinator does not become Experience.
The coordinator does not become Protection.
The coordinator does not become the Durable Coordination Journal.
The coordinator does not grant authority.

Its responsibility is to make the physiological relationship between
their persistence operations explicit, inspectable, and durably
observable across process death.

Persistence != authority.
Storage != Experience.
Journal != Experience.
Journal != Protection.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Callable

from .coordination_journal import (
    DurableCoordinationStage,
    JsonFileCoordinationJournal,
)
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
    """Coordinates Experience, Protection, and durable coordination evidence.

    Experience and Protection repositories remain responsible for their
    own durable bodies.

    The Durable Coordination Journal remains responsible for durable
    evidence of the physiological coordination operation.

    The coordinator bridges physiological events between these distinct
    organs without collapsing their identities or responsibilities.
    """

    def __init__(
        self,
        experience_repository: JsonFileExperienceRepository,
        protection_repository: JsonFileProtectionRepository,
        coordination_journal: JsonFileCoordinationJournal | None = None,
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

        if (
            coordination_journal is not None
            and not isinstance(
                coordination_journal,
                JsonFileCoordinationJournal,
            )
        ):
            raise TypeError(
                "coordination_journal must be "
                "JsonFileCoordinationJournal or None"
            )

        self._experience_repository = experience_repository
        self._protection_repository = protection_repository
        self._coordination_journal = coordination_journal

    def persist(
        self,
        experience: Experience,
        protection: ExperienceProtection,
        *,
        observe_stage: StageObserver | None = None,
    ) -> CoordinatedExperience:
        """Persist distinct organs through one explicit physiological path.

        Protection is conserved before Experience so protected material
        is never intentionally persisted first as an unprotected
        Experience.

        When a Durable Coordination Journal is supplied, each completed
        physiological boundary is durably recorded.

        This method makes interruption state durable. It does not by
        itself claim automatic crash reconciliation.
        """

        self._require_matching_identity(experience, protection)

        durable_record = None

        if self._coordination_journal is not None:
            durable_record = self._coordination_journal.begin(
                experience.experience_id
            )

        self._observe(
            CoordinationState(
                experience_id=experience.experience_id,
                stage=CoordinationStage.PREPARING,
            ),
            observe_stage,
        )

        self._persist_protection(protection)

        if durable_record is not None:
            durable_record = self._coordination_journal.advance(
                durable_record.coordination_operation_id,
                DurableCoordinationStage.PROTECTION_WRITTEN,
            )

        self._observe(
            CoordinationState(
                experience_id=experience.experience_id,
                stage=CoordinationStage.PROTECTION_WRITTEN,
            ),
            observe_stage,
        )

        self._persist_experience(experience)

        if durable_record is not None:
            durable_record = self._coordination_journal.advance(
                durable_record.coordination_operation_id,
                DurableCoordinationStage.EXPERIENCE_WRITTEN,
            )

        self._observe(
            CoordinationState(
                experience_id=experience.experience_id,
                stage=CoordinationStage.EXPERIENCE_WRITTEN,
            ),
            observe_stage,
        )

        pair = self.recover(experience.experience_id)

        if durable_record is not None:
            self._coordination_journal.advance(
                durable_record.coordination_operation_id,
                DurableCoordinationStage.COMPLETE,
            )

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

    def reconcile_incomplete(
        self,
    ) -> tuple[CoordinatedExperience, ...]:
        """Reconcile incomplete durable operations from surviving evidence.

        Reconciliation never fabricates a missing Experience or
        Protection body.

        Only operations whose Experience and Protection organs both
        survive may be completed automatically.

        Operations with missing organs remain durably incomplete.
        """

        if self._coordination_journal is None:
            raise PersistenceCoordinationStateError(
                "durable coordination journal is required "
                "for crash reconciliation"
            )

        reconciled: list[CoordinatedExperience] = []

        for record in self._coordination_journal.incomplete_records():
            experience_id = record.experience_id

            experience_exists = self._experience_repository.contains(
                experience_id
            )
            protection_exists = self._protection_repository.contains(
                experience_id
            )

            if not experience_exists or not protection_exists:
                continue

            pair = self.recover(experience_id)

            current = record

            if current.stage is DurableCoordinationStage.PREPARING:
                current = self._coordination_journal.advance(
                    current.coordination_operation_id,
                    DurableCoordinationStage.PROTECTION_WRITTEN,
                )

            if (
                current.stage
                is DurableCoordinationStage.PROTECTION_WRITTEN
            ):
                current = self._coordination_journal.advance(
                    current.coordination_operation_id,
                    DurableCoordinationStage.EXPERIENCE_WRITTEN,
                )

            if (
                current.stage
                is DurableCoordinationStage.EXPERIENCE_WRITTEN
            ):
                current = self._coordination_journal.advance(
                    current.coordination_operation_id,
                    DurableCoordinationStage.COMPLETE,
                )

            if current.stage is not DurableCoordinationStage.COMPLETE:
                raise PersistenceCoordinationStateError(
                    "durable coordination operation did not "
                    "reach COMPLETE"
                )

            reconciled.append(pair)

        return tuple(reconciled)

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

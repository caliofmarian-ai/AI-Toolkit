"""Operational observability for PCC-01 Persistent Experience.

This organ does not become Experience, Protection, persistence, or the
Durable Coordination Journal.

It reads existing durable coordination evidence and presents a compact
operational snapshot suitable for diagnosis.

Observation != authority.
Observation != mutation.
Metrics != Experience.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from .coordination_journal import (
    DurableCoordinationRecord,
    DurableCoordinationStage,
    JsonFileCoordinationJournal,
)
from .identity import ExperienceId


class ExperienceOperationalObservabilityError(RuntimeError):
    """Base error for PCC-01 operational observation."""


@dataclass(frozen=True, slots=True)
class ExperienceOperationalSnapshot:
    """Read-only operational condition derived from durable evidence."""

    observed_at: datetime
    total_operations: int
    incomplete_operations: int
    complete_operations: int
    preparing_operations: int
    protection_written_operations: int
    experience_written_operations: int

    @property
    def healthy(self) -> bool:
        """A snapshot is healthy when no durable operation is incomplete."""

        return self.incomplete_operations == 0

    def to_dict(self) -> dict[str, object]:
        return {
            "observed_at": self.observed_at.isoformat(),
            "healthy": self.healthy,
            "total_operations": self.total_operations,
            "incomplete_operations": self.incomplete_operations,
            "complete_operations": self.complete_operations,
            "preparing_operations": self.preparing_operations,
            "protection_written_operations": (
                self.protection_written_operations
            ),
            "experience_written_operations": (
                self.experience_written_operations
            ),
        }


class ExperienceOperationalObserver:
    """Read durable PCC-01 coordination evidence without mutating it."""

    def __init__(
        self,
        coordination_journal: JsonFileCoordinationJournal,
    ) -> None:
        if not isinstance(
            coordination_journal,
            JsonFileCoordinationJournal,
        ):
            raise TypeError(
                "coordination_journal must be JsonFileCoordinationJournal"
            )

        self._coordination_journal = coordination_journal

    def snapshot(self) -> ExperienceOperationalSnapshot:
        """Describe the current durable coordination condition."""

        records = self._all_records()

        counts = {
            stage: 0
            for stage in DurableCoordinationStage
        }

        for record in records:
            counts[record.stage] += 1

        incomplete = sum(
            count
            for stage, count in counts.items()
            if stage is not DurableCoordinationStage.COMPLETE
        )

        return ExperienceOperationalSnapshot(
            observed_at=datetime.now(timezone.utc),
            total_operations=len(records),
            incomplete_operations=incomplete,
            complete_operations=counts[
                DurableCoordinationStage.COMPLETE
            ],
            preparing_operations=counts[
                DurableCoordinationStage.PREPARING
            ],
            protection_written_operations=counts[
                DurableCoordinationStage.PROTECTION_WRITTEN
            ],
            experience_written_operations=counts[
                DurableCoordinationStage.EXPERIENCE_WRITTEN
            ],
        )

    def records_for_experience(
        self,
        experience_id: ExperienceId,
    ) -> tuple[DurableCoordinationRecord, ...]:
        """Expose durable coordination history for one Experience."""

        if not isinstance(experience_id, ExperienceId):
            raise TypeError("experience_id must be ExperienceId")

        return self._coordination_journal.records_for_experience(
            experience_id
        )

    def incomplete_records(
        self,
    ) -> tuple[DurableCoordinationRecord, ...]:
        """Expose durable operations requiring operational attention."""

        return self._coordination_journal.incomplete_records()

    def _all_records(
        self,
    ) -> tuple[DurableCoordinationRecord, ...]:
        """Read journal records through its durable representation.

        The journal owns storage. This observer only derives operational
        state from the journal's persisted records.
        """

        store = self._coordination_journal._read_store()

        return tuple(
            DurableCoordinationRecord.from_dict(payload)
            for payload in store.values()
        )

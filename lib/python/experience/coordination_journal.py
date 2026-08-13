"""Durable coordination journal for PCC-01 persistence physiology."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
import json
import os
from pathlib import Path
import tempfile
from typing import Any
from uuid import UUID, uuid4

from .identity import ExperienceId


class CoordinationJournalError(RuntimeError):
    pass


class CoordinationOperationIdentityError(CoordinationJournalError):
    pass


class CoordinationJournalStateError(CoordinationJournalError):
    pass


class CoordinationJournalPersistenceError(CoordinationJournalError):
    pass


@dataclass(frozen=True, slots=True)
class CoordinationOperationId:
    value: UUID

    def __post_init__(self) -> None:
        if not isinstance(self.value, UUID):
            raise CoordinationOperationIdentityError(
                "coordination operation identity must contain a UUID"
            )

    @classmethod
    def create(cls) -> "CoordinationOperationId":
        return cls(uuid4())

    @classmethod
    def from_string(cls, raw: str) -> "CoordinationOperationId":
        if not isinstance(raw, str):
            raise CoordinationOperationIdentityError(
                "coordination operation identity must be a string"
            )

        try:
            value = UUID(raw)
        except (ValueError, AttributeError) as exc:
            raise CoordinationOperationIdentityError(
                "invalid coordination operation identity"
            ) from exc

        return cls(value)

    def __str__(self) -> str:
        return str(self.value)


class DurableCoordinationStage(str, Enum):
    PREPARING = "preparing"
    PROTECTION_WRITTEN = "protection_written"
    EXPERIENCE_WRITTEN = "experience_written"
    COMPLETE = "complete"


_ALLOWED_TRANSITIONS = {
    DurableCoordinationStage.PREPARING: {
        DurableCoordinationStage.PROTECTION_WRITTEN
    },
    DurableCoordinationStage.PROTECTION_WRITTEN: {
        DurableCoordinationStage.EXPERIENCE_WRITTEN
    },
    DurableCoordinationStage.EXPERIENCE_WRITTEN: {
        DurableCoordinationStage.COMPLETE
    },
    DurableCoordinationStage.COMPLETE: set(),
}


@dataclass(frozen=True, slots=True)
class DurableCoordinationRecord:
    coordination_operation_id: CoordinationOperationId
    experience_id: ExperienceId
    stage: DurableCoordinationStage
    created_at: datetime
    updated_at: datetime

    @classmethod
    def begin(
        cls,
        experience_id: ExperienceId,
    ) -> "DurableCoordinationRecord":
        if not isinstance(experience_id, ExperienceId):
            raise TypeError("experience_id must be ExperienceId")

        now = datetime.now(timezone.utc)

        return cls(
            coordination_operation_id=CoordinationOperationId.create(),
            experience_id=experience_id,
            stage=DurableCoordinationStage.PREPARING,
            created_at=now,
            updated_at=now,
        )

    def advance(
        self,
        target: DurableCoordinationStage,
    ) -> "DurableCoordinationRecord":
        if target not in _ALLOWED_TRANSITIONS[self.stage]:
            raise CoordinationJournalStateError(
                "illegal durable coordination transition: "
                f"{self.stage.value} -> {target.value}"
            )

        return DurableCoordinationRecord(
            coordination_operation_id=self.coordination_operation_id,
            experience_id=self.experience_id,
            stage=target,
            created_at=self.created_at,
            updated_at=datetime.now(timezone.utc),
        )

    def to_dict(self) -> dict[str, str]:
        return {
            "coordination_operation_id": str(
                self.coordination_operation_id
            ),
            "experience_id": str(self.experience_id),
            "stage": self.stage.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @classmethod
    def from_dict(
        cls,
        payload: dict[str, Any],
    ) -> "DurableCoordinationRecord":
        try:
            return cls(
                coordination_operation_id=(
                    CoordinationOperationId.from_string(
                        payload["coordination_operation_id"]
                    )
                ),
                experience_id=ExperienceId.from_string(
                    payload["experience_id"]
                ),
                stage=DurableCoordinationStage(payload["stage"]),
                created_at=datetime.fromisoformat(
                    payload["created_at"]
                ),
                updated_at=datetime.fromisoformat(
                    payload["updated_at"]
                ),
            )
        except (KeyError, ValueError, TypeError) as exc:
            raise CoordinationJournalStateError(
                "invalid durable coordination record"
            ) from exc


class JsonFileCoordinationJournal:
    SCHEMA = "pcc01-durable-coordination-journal-v1"

    def __init__(self, path: str | Path) -> None:
        self._path = Path(path)

        if self._path.exists() and self._path.is_dir():
            raise CoordinationJournalPersistenceError(
                "coordination journal path is a directory"
            )

    @property
    def path(self) -> Path:
        return self._path

    def begin(
        self,
        experience_id: ExperienceId,
    ) -> DurableCoordinationRecord:
        record = DurableCoordinationRecord.begin(experience_id)
        store = self._read_store()
        store[str(record.coordination_operation_id)] = record.to_dict()
        self._write_store(store)
        return record

    def advance(
        self,
        coordination_operation_id: CoordinationOperationId,
        target: DurableCoordinationStage,
    ) -> DurableCoordinationRecord:
        current = self.get(coordination_operation_id)
        advanced = current.advance(target)

        store = self._read_store()
        store[str(coordination_operation_id)] = advanced.to_dict()
        self._write_store(store)

        return advanced

    def get(
        self,
        coordination_operation_id: CoordinationOperationId,
    ) -> DurableCoordinationRecord:
        store = self._read_store()
        key = str(coordination_operation_id)

        if key not in store:
            raise CoordinationJournalStateError(
                "coordination operation not found"
            )

        return DurableCoordinationRecord.from_dict(store[key])

    def contains(
        self,
        coordination_operation_id: CoordinationOperationId,
    ) -> bool:
        return str(coordination_operation_id) in self._read_store()

    def records_for_experience(
        self,
        experience_id: ExperienceId,
    ) -> tuple[DurableCoordinationRecord, ...]:
        records = []

        for payload in self._read_store().values():
            if payload.get("experience_id") == str(experience_id):
                records.append(
                    DurableCoordinationRecord.from_dict(payload)
                )

        return tuple(records)

    def incomplete_records(
        self,
    ) -> tuple[DurableCoordinationRecord, ...]:
        records = []

        for payload in self._read_store().values():
            record = DurableCoordinationRecord.from_dict(payload)

            if record.stage is not DurableCoordinationStage.COMPLETE:
                records.append(record)

        return tuple(records)

    def _read_store(self) -> dict[str, dict[str, Any]]:
        if not self._path.exists():
            return {}

        try:
            document = json.loads(
                self._path.read_text(encoding="utf-8")
            )
        except (OSError, json.JSONDecodeError) as exc:
            raise CoordinationJournalPersistenceError(
                "cannot read durable coordination journal"
            ) from exc

        if document.get("schema") != self.SCHEMA:
            raise CoordinationJournalPersistenceError(
                "coordination journal schema is invalid"
            )

        records = document.get("records")

        if not isinstance(records, dict):
            raise CoordinationJournalPersistenceError(
                "coordination journal records are invalid"
            )

        return records

    def _write_store(
        self,
        records: dict[str, dict[str, Any]],
    ) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)

        document = {
            "schema": self.SCHEMA,
            "records": records,
        }

        payload = json.dumps(
            document,
            indent=2,
            sort_keys=True,
        ) + "\n"

        fd, temporary_name = tempfile.mkstemp(
            prefix=".coordination-journal-",
            suffix=".tmp",
            dir=str(self._path.parent),
        )

        temporary_path = Path(temporary_name)

        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                handle.write(payload)
                handle.flush()
                os.fsync(handle.fileno())

            os.replace(temporary_path, self._path)

        except OSError as exc:
            raise CoordinationJournalPersistenceError(
                "cannot persist durable coordination journal"
            ) from exc

        finally:
            if temporary_path.exists():
                temporary_path.unlink()

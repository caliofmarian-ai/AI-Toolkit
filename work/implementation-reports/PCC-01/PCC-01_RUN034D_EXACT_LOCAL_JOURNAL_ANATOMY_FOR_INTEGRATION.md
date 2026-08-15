# PCC-01 — Exact Local Durable Coordination Journal Anatomy — RUN 034D

## Purpose

Materialize all local Durable Coordination Journal anatomy required for the next deterministic integration step.

This report is intentionally self-contained.

No terminal output is required for subsequent GPT inspection.

## Safety Contract

- software modification: NO
- test modification: NO
- behavioral test execution: NO
- git add: NO
- commit: NO
- push: NO

## 1. Authoritative Baseline

- Expected HEAD: `32ab3c44d01cb86c5857b5c70f55f6720ca11f96`
- Local HEAD: `32ab3c44d01cb86c5857b5c70f55f6720ca11f96`
- origin/main: `32ab3c44d01cb86c5857b5c70f55f6720ca11f96`

## 2. Conserved Coordinator State

The tracked Persistence Coordinator exactly matches the conserved Git baseline.

Path:

`lib/python/experience/persistence_coordinator.py`

Conserved physiology:

`PREPARING -> _persist_protection -> PROTECTION_WRITTEN -> _persist_experience -> EXPERIENCE_WRITTEN -> recover -> COMPLETE`

## 3. Local Journal Artifacts

- Journal: `lib/python/experience/coordination_journal.py`
- Journal tests: `tests/experience/test_experience_coordination_journal.py`

## 4. Exact Structural Anatomy

### Class `CoordinationJournalError`

Bases:

- `RuntimeError`

### Class `CoordinationOperationIdentityError`

Bases:

- `CoordinationJournalError`

### Class `CoordinationJournalStateError`

Bases:

- `CoordinationJournalError`

### Class `CoordinationJournalPersistenceError`

Bases:

- `CoordinationJournalError`

### Class `CoordinationOperationId`

Methods:

- `__post_init__` — positional=['self']; kwonly=[]; positional_defaults=0
- `create` — positional=['cls']; kwonly=[]; positional_defaults=0
- `from_string` — positional=['cls', 'raw']; kwonly=[]; positional_defaults=0
- `__str__` — positional=['self']; kwonly=[]; positional_defaults=0

### Class `DurableCoordinationStage`

Bases:

- `str`
- `Enum`

### Class `DurableCoordinationRecord`

Methods:

- `begin` — positional=['cls', 'experience_id']; kwonly=[]; positional_defaults=0
- `advance` — positional=['self', 'target']; kwonly=[]; positional_defaults=0
- `to_dict` — positional=['self']; kwonly=[]; positional_defaults=0
- `from_dict` — positional=['cls', 'payload']; kwonly=[]; positional_defaults=0

### Class `JsonFileCoordinationJournal`

Methods:

- `__init__` — positional=['self', 'path']; kwonly=[]; positional_defaults=0
- `path` — positional=['self']; kwonly=[]; positional_defaults=0
- `begin` — positional=['self', 'experience_id']; kwonly=[]; positional_defaults=0
- `advance` — positional=['self', 'coordination_operation_id', 'target']; kwonly=[]; positional_defaults=0
- `get` — positional=['self', 'coordination_operation_id']; kwonly=[]; positional_defaults=0
- `contains` — positional=['self', 'coordination_operation_id']; kwonly=[]; positional_defaults=0
- `records_for_experience` — positional=['self', 'experience_id']; kwonly=[]; positional_defaults=0
- `incomplete_records` — positional=['self']; kwonly=[]; positional_defaults=0
- `_read_store` — positional=['self']; kwonly=[]; positional_defaults=0
- `_write_store` — positional=['self', 'records']; kwonly=[]; positional_defaults=0

Structural parsing: PASS

## 5. Exact Local Journal Source

The following is the exact local source present at inspection time.

```python
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
```

## 6. Exact Local Journal Behavioral Specification

The following is the exact local test source already created for this organ.

```python
from __future__ import annotations

import pytest

from lib.python.experience.coordination_journal import (
    CoordinationJournalPersistenceError,
    CoordinationJournalStateError,
    CoordinationOperationId,
    DurableCoordinationRecord,
    DurableCoordinationStage,
    JsonFileCoordinationJournal,
)
from lib.python.experience.model import Experience


def make_experience_id():
    return Experience.create().experience_id


def test_operation_identity_is_distinct_from_experience_identity():
    experience_id = make_experience_id()
    operation_id = CoordinationOperationId.create()

    assert type(operation_id) is not type(experience_id)
    assert str(operation_id) != str(experience_id)


def test_begin_creates_preparing_record():
    experience_id = make_experience_id()

    record = DurableCoordinationRecord.begin(experience_id)

    assert record.experience_id == experience_id
    assert record.stage is DurableCoordinationStage.PREPARING


def test_required_forward_physiology():
    record = DurableCoordinationRecord.begin(
        make_experience_id()
    )

    record = record.advance(
        DurableCoordinationStage.PROTECTION_WRITTEN
    )

    record = record.advance(
        DurableCoordinationStage.EXPERIENCE_WRITTEN
    )

    record = record.advance(
        DurableCoordinationStage.COMPLETE
    )

    assert record.stage is DurableCoordinationStage.COMPLETE


def test_illegal_transition_is_rejected():
    record = DurableCoordinationRecord.begin(
        make_experience_id()
    )

    with pytest.raises(CoordinationJournalStateError):
        record.advance(
            DurableCoordinationStage.EXPERIENCE_WRITTEN
        )


def test_journal_begin_is_durable(tmp_path):
    path = tmp_path / "journal.json"
    journal = JsonFileCoordinationJournal(path)

    record = journal.begin(make_experience_id())

    assert path.exists()
    assert journal.contains(record.coordination_operation_id)


def test_new_instance_recovers_same_record(tmp_path):
    path = tmp_path / "journal.json"

    writer = JsonFileCoordinationJournal(path)
    created = writer.begin(make_experience_id())

    reader = JsonFileCoordinationJournal(path)
    recovered = reader.get(created.coordination_operation_id)

    assert (
        recovered.coordination_operation_id
        == created.coordination_operation_id
    )
    assert recovered.experience_id == created.experience_id
    assert recovered.stage == created.stage


def test_stage_survives_repository_reconstruction(tmp_path):
    path = tmp_path / "journal.json"

    writer = JsonFileCoordinationJournal(path)
    created = writer.begin(make_experience_id())

    writer.advance(
        created.coordination_operation_id,
        DurableCoordinationStage.PROTECTION_WRITTEN,
    )

    reader = JsonFileCoordinationJournal(path)
    recovered = reader.get(created.coordination_operation_id)

    assert (
        recovered.stage
        is DurableCoordinationStage.PROTECTION_WRITTEN
    )


def test_complete_record_not_reported_as_incomplete(tmp_path):
    journal = JsonFileCoordinationJournal(
        tmp_path / "journal.json"
    )

    record = journal.begin(make_experience_id())

    journal.advance(
        record.coordination_operation_id,
        DurableCoordinationStage.PROTECTION_WRITTEN,
    )

    journal.advance(
        record.coordination_operation_id,
        DurableCoordinationStage.EXPERIENCE_WRITTEN,
    )

    journal.advance(
        record.coordination_operation_id,
        DurableCoordinationStage.COMPLETE,
    )

    assert journal.incomplete_records() == ()


def test_incomplete_record_is_discoverable(tmp_path):
    journal = JsonFileCoordinationJournal(
        tmp_path / "journal.json"
    )

    record = journal.begin(make_experience_id())

    incomplete = journal.incomplete_records()

    assert len(incomplete) == 1
    assert (
        incomplete[0].coordination_operation_id
        == record.coordination_operation_id
    )


def test_multiple_operations_can_reference_same_experience(tmp_path):
    journal = JsonFileCoordinationJournal(
        tmp_path / "journal.json"
    )

    experience_id = make_experience_id()

    first = journal.begin(experience_id)
    second = journal.begin(experience_id)

    records = journal.records_for_experience(experience_id)

    assert len(records) == 2
    assert first.experience_id == second.experience_id
    assert (
        first.coordination_operation_id
        != second.coordination_operation_id
    )


def test_missing_operation_fails_explicitly(tmp_path):
    journal = JsonFileCoordinationJournal(
        tmp_path / "journal.json"
    )

    with pytest.raises(
        CoordinationJournalStateError,
        match="not found",
    ):
        journal.get(CoordinationOperationId.create())


def test_invalid_json_fails_explicitly(tmp_path):
    path = tmp_path / "journal.json"
    path.write_text("{broken", encoding="utf-8")

    journal = JsonFileCoordinationJournal(path)

    with pytest.raises(CoordinationJournalPersistenceError):
        journal.incomplete_records()
```

## 7. Integration-Facing API

### Durable Stage Candidates

`DurableCoordinationStage`:

- `PREPARING`
- `PROTECTION_WRITTEN`
- `EXPERIENCE_WRITTEN`
- `COMPLETE`

### Journal Transition Methods

Class: `DurableCoordinationRecord`

#### `begin(cls, experience_id)`

```python
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
```

#### `advance(self, target)`

```python
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
```

Class: `JsonFileCoordinationJournal`

#### `begin(self, experience_id)`

```python
def begin(
        self,
        experience_id: ExperienceId,
    ) -> DurableCoordinationRecord:
        record = DurableCoordinationRecord.begin(experience_id)
        store = self._read_store()
        store[str(record.coordination_operation_id)] = record.to_dict()
        self._write_store(store)
        return record
```

#### `advance(self, coordination_operation_id, target)`

```python
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
```

#### `get(self, coordination_operation_id)`

```python
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
```

#### `records_for_experience(self, experience_id)`

```python
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
```

#### `incomplete_records(self)`

```python
def incomplete_records(
        self,
    ) -> tuple[DurableCoordinationRecord, ...]:
        records = []

        for payload in self._read_store().values():
            record = DurableCoordinationRecord.from_dict(payload)

            if record.stage is not DurableCoordinationStage.COMPLETE:
                records.append(record)

        return tuple(records)
```

Integration-facing API extraction: PASS

## 8. Repository State After Inspection

```text
?? lib/python/experience/coordination_journal.py
?? tests/experience/test_experience_coordination_journal.py
?? work/implementation-reports/PCC-01/PCC-01_DURABLE_COORDINATION_JOURNAL_COORDINATOR_INTEGRATION_PRE_IMPLEMENTATION_INSPECTION_RUN_033.md
?? work/implementation-reports/PCC-01/PCC-01_DURABLE_COORDINATION_JOURNAL_IMPLEMENTATION_REPORT_RUN_032.md
?? work/implementation-reports/PCC-01/PCC-01_DURABLE_COORDINATION_JOURNAL_PRE_IMPLEMENTATION_INSPECTION_RUN_031.md
?? work/implementation-reports/PCC-01/PCC-01_PROTECTION_PERSISTENCE_COORDINATOR_CONSERVATION_RUN_030.md
?? work/implementation-reports/PCC-01/PCC-01_RUN020_EVIDENCE_CONSERVATION_REPORT_RUN_021.md
?? work/implementation-reports/PCC-01/PCC-01_RUN034B_COORDINATION_MODEL_RECONCILIATION_INSPECTION.md
?? work/implementation-reports/PCC-01/PCC-01_RUN034C_FAILURE_RECOVERY_AND_EXACT_INTEGRATION_ANATOMY.md
?? work/implementation-reports/PCC-01/PCC-01_RUN034D_EXACT_LOCAL_JOURNAL_ANATOMY_FOR_INTEGRATION.md
?? work/implementation-reports/PCC-01/PCC-01_RUN034_CAUSAL_ANATOMY_INSPECTION.md
```

## 9. Interpretation

The Persistence Coordinator remains conserved.

The Durable Coordination Journal remains a distinct local organ.

This RUN performs no integration mutation.

The complete local journal source and its existing behavioral specification are now materialized in this report so the next implementation can be designed without terminal transcription or API guessing.

## 10. PCC-01 Status

- Durable Coordination Journal: BUILT LOCALLY
- Journal + Coordinator integration: NOT IMPLEMENTED
- Durable reconciliation after crash: NOT IMPLEMENTED
- Durable crash coordination: NOT DEMONSTRATED
- PCC-01 Implementation: NOT DEMONSTRATED
- Canonical Status: NOT CANON
- Production Status: NOT PRODUCTION-READY

## 11. Conservation

- git add: NO
- commit: NO
- push: NO

## 12. Next Required Action

GPT inspects this Markdown together with the conserved GitHub coordinator and accepted PCC-01 documents, then produces the deterministic Journal + Coordinator integration Bash.

---

END OF PCC-01 RUN 034D

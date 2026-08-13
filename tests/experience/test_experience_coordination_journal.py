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

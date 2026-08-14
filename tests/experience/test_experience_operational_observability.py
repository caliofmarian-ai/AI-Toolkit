from lib.python.experience.coordination_journal import (
    DurableCoordinationStage,
    JsonFileCoordinationJournal,
)
from lib.python.experience.model import Experience
from lib.python.experience.operational_observability import (
    ExperienceOperationalObserver,
)


def _observer(tmp_path):
    journal = JsonFileCoordinationJournal(
        tmp_path / "coordination.json"
    )
    return journal, ExperienceOperationalObserver(journal)


def test_empty_journal_is_observably_healthy(tmp_path):
    _, observer = _observer(tmp_path)

    snapshot = observer.snapshot()

    assert snapshot.total_operations == 0
    assert snapshot.incomplete_operations == 0
    assert snapshot.complete_operations == 0
    assert snapshot.healthy is True


def test_preparing_operation_is_observably_incomplete(tmp_path):
    journal, observer = _observer(tmp_path)
    experience = Experience.create()

    journal.begin(experience.experience_id)

    snapshot = observer.snapshot()

    assert snapshot.total_operations == 1
    assert snapshot.incomplete_operations == 1
    assert snapshot.preparing_operations == 1
    assert snapshot.complete_operations == 0
    assert snapshot.healthy is False


def test_complete_operation_is_observably_healthy(tmp_path):
    journal, observer = _observer(tmp_path)
    experience = Experience.create()

    record = journal.begin(experience.experience_id)

    record = journal.advance(
        record.coordination_operation_id,
        DurableCoordinationStage.PROTECTION_WRITTEN,
    )
    record = journal.advance(
        record.coordination_operation_id,
        DurableCoordinationStage.EXPERIENCE_WRITTEN,
    )
    journal.advance(
        record.coordination_operation_id,
        DurableCoordinationStage.COMPLETE,
    )

    snapshot = observer.snapshot()

    assert snapshot.total_operations == 1
    assert snapshot.incomplete_operations == 0
    assert snapshot.complete_operations == 1
    assert snapshot.healthy is True


def test_snapshot_counts_each_incomplete_stage(tmp_path):
    journal, observer = _observer(tmp_path)

    preparing = journal.begin(
        Experience.create().experience_id
    )

    protection = journal.begin(
        Experience.create().experience_id
    )
    journal.advance(
        protection.coordination_operation_id,
        DurableCoordinationStage.PROTECTION_WRITTEN,
    )

    experience_written = journal.begin(
        Experience.create().experience_id
    )
    experience_written = journal.advance(
        experience_written.coordination_operation_id,
        DurableCoordinationStage.PROTECTION_WRITTEN,
    )
    journal.advance(
        experience_written.coordination_operation_id,
        DurableCoordinationStage.EXPERIENCE_WRITTEN,
    )

    snapshot = observer.snapshot()

    assert preparing is not None
    assert snapshot.total_operations == 3
    assert snapshot.incomplete_operations == 3
    assert snapshot.preparing_operations == 1
    assert snapshot.protection_written_operations == 1
    assert snapshot.experience_written_operations == 1
    assert snapshot.complete_operations == 0
    assert snapshot.healthy is False


def test_snapshot_dictionary_is_machine_inspectable(tmp_path):
    journal, observer = _observer(tmp_path)
    journal.begin(Experience.create().experience_id)

    payload = observer.snapshot().to_dict()

    assert set(payload) == {
        "observed_at",
        "healthy",
        "total_operations",
        "incomplete_operations",
        "complete_operations",
        "preparing_operations",
        "protection_written_operations",
        "experience_written_operations",
    }
    assert payload["healthy"] is False
    assert payload["total_operations"] == 1


def test_records_for_experience_are_scoped(tmp_path):
    journal, observer = _observer(tmp_path)

    target = Experience.create()
    other = Experience.create()

    target_record = journal.begin(target.experience_id)
    journal.begin(other.experience_id)

    records = observer.records_for_experience(
        target.experience_id
    )

    assert len(records) == 1
    assert (
        records[0].coordination_operation_id
        == target_record.coordination_operation_id
    )
    assert records[0].experience_id == target.experience_id


def test_incomplete_records_expose_attention_required_operations(
    tmp_path,
):
    journal, observer = _observer(tmp_path)

    incomplete = journal.begin(
        Experience.create().experience_id
    )

    complete = journal.begin(
        Experience.create().experience_id
    )
    complete = journal.advance(
        complete.coordination_operation_id,
        DurableCoordinationStage.PROTECTION_WRITTEN,
    )
    complete = journal.advance(
        complete.coordination_operation_id,
        DurableCoordinationStage.EXPERIENCE_WRITTEN,
    )
    journal.advance(
        complete.coordination_operation_id,
        DurableCoordinationStage.COMPLETE,
    )

    records = observer.incomplete_records()

    assert len(records) == 1
    assert (
        records[0].coordination_operation_id
        == incomplete.coordination_operation_id
    )


def test_observation_does_not_mutate_durable_records(tmp_path):
    journal, observer = _observer(tmp_path)

    record = journal.begin(
        Experience.create().experience_id
    )

    before = journal.get(record.coordination_operation_id)

    observer.snapshot()
    observer.records_for_experience(record.experience_id)
    observer.incomplete_records()

    after = journal.get(record.coordination_operation_id)

    assert after == before


def test_observation_does_not_change_experience_identity(tmp_path):
    journal, observer = _observer(tmp_path)

    experience = Experience.create()
    before = experience.experience_id

    journal.begin(experience.experience_id)
    observer.snapshot()

    assert experience.experience_id == before


def test_observer_requires_real_durable_coordination_journal():
    try:
        ExperienceOperationalObserver(object())
    except TypeError:
        pass
    else:
        raise AssertionError(
            "observer accepted a non-journal dependency"
        )

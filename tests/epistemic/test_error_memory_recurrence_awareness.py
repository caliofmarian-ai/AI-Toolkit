from dataclasses import FrozenInstanceError

import pytest

from lib.python.epistemic.error_memory import (
    FailureKind,
    IntendedTransformation,
    PreTransformationRecurrenceAwareness,
    form_pre_transformation_recurrence_awareness,
    seed_demonstrated_ai_toolkit_failures_run002,
)


def make_intended(*activities: FailureKind) -> IntendedTransformation:
    return IntendedTransformation(
        identity="TRANSFORMATION-TEST-001",
        title="Demonstrated Future Transformation",
        activities=activities,
        context=("Termux", "epistemic regression"),
    )


def test_run002_memory_contains_all_four_demonstrated_precedents():
    organ = seed_demonstrated_ai_toolkit_failures_run002()

    identities = {memory.identity for memory in organ.memories}

    assert identities == {
        "ERR-0001",
        "ERR-0002",
        "ERR-0003",
        "ERR-0004",
    }


def test_import_topology_failure_preserves_historical_origin():
    organ = seed_demonstrated_ai_toolkit_failures_run002()
    memory = organ.find("ERR-0003")

    assert memory is not None
    assert memory.kind == FailureKind.EXECUTION
    assert "ERROR_MEMORY_RUN001" in memory.origin.repository_path
    assert (
        memory.origin.git_commit
        == "d8d16590911967579aeb2762a888dfcdd9ef941b"
    )
    assert "lib/python" in memory.prevention_rule


def test_metabolic_classification_failure_preserves_prevention_rule():
    organ = seed_demonstrated_ai_toolkit_failures_run002()
    memory = organ.find("ERR-0004")

    assert memory is not None
    assert memory.kind == FailureKind.EPISTEMIC
    assert "producer" in memory.prevention_rule
    assert "provenance" in memory.prevention_rule
    assert "silently" in memory.prevention_rule


def test_intended_transformation_has_human_readable_identity():
    intended = make_intended(FailureKind.EXECUTION)

    assert intended.semantic_identity == (
        "TRANSFORMATION-TEST-001 — Demonstrated Future Transformation"
    )


def test_intended_transformation_is_immutable():
    intended = make_intended(FailureKind.EXECUTION)

    with pytest.raises(FrozenInstanceError):
        intended.title = "Rewritten transformation"


def test_intended_transformation_requires_identity():
    with pytest.raises(ValueError):
        IntendedTransformation(
            identity="",
            title="Valid title",
            activities=(FailureKind.EXECUTION,),
        )


def test_intended_transformation_requires_title():
    with pytest.raises(ValueError):
        IntendedTransformation(
            identity="TRANSFORMATION-001",
            title="",
            activities=(FailureKind.EXECUTION,),
        )


def test_intended_transformation_requires_declared_activity():
    with pytest.raises(ValueError):
        IntendedTransformation(
            identity="TRANSFORMATION-001",
            title="Valid title",
            activities=(),
        )


def test_awareness_finds_execution_precedents_before_execution():
    organ = seed_demonstrated_ai_toolkit_failures_run002()
    intended = make_intended(FailureKind.EXECUTION)

    awareness = form_pre_transformation_recurrence_awareness(
        organ,
        intended,
    )

    identities = {
        warning.error_identity
        for warning in awareness.warnings
    }

    assert "ERR-0003" in identities


def test_awareness_finds_permission_precedent_for_launch_activity():
    organ = seed_demonstrated_ai_toolkit_failures_run002()
    intended = make_intended(FailureKind.PERMISSION)

    awareness = form_pre_transformation_recurrence_awareness(
        organ,
        intended,
    )

    assert [warning.error_identity for warning in awareness.warnings] == [
        "ERR-0001"
    ]


def test_awareness_finds_validation_precedent():
    organ = seed_demonstrated_ai_toolkit_failures_run002()
    intended = make_intended(FailureKind.VALIDATION)

    awareness = form_pre_transformation_recurrence_awareness(
        organ,
        intended,
    )

    assert [warning.error_identity for warning in awareness.warnings] == [
        "ERR-0002"
    ]


def test_awareness_finds_metabolic_classification_precedent():
    organ = seed_demonstrated_ai_toolkit_failures_run002()
    intended = make_intended(FailureKind.EPISTEMIC)

    awareness = form_pre_transformation_recurrence_awareness(
        organ,
        intended,
    )

    assert [warning.error_identity for warning in awareness.warnings] == [
        "ERR-0004"
    ]


def test_awareness_can_correlate_multiple_relevant_failure_kinds():
    organ = seed_demonstrated_ai_toolkit_failures_run002()
    intended = make_intended(
        FailureKind.PERMISSION,
        FailureKind.EXECUTION,
        FailureKind.VALIDATION,
        FailureKind.EPISTEMIC,
    )

    awareness = form_pre_transformation_recurrence_awareness(
        organ,
        intended,
    )

    identities = {
        warning.error_identity
        for warning in awareness.warnings
    }

    assert identities == {
        "ERR-0001",
        "ERR-0002",
        "ERR-0003",
        "ERR-0004",
    }


def test_awareness_preserves_navigable_origins():
    organ = seed_demonstrated_ai_toolkit_failures_run002()
    intended = make_intended(
        FailureKind.EXECUTION,
        FailureKind.EPISTEMIC,
    )

    awareness = form_pre_transformation_recurrence_awareness(
        organ,
        intended,
    )

    assert awareness.warnings
    for warning in awareness.warnings:
        assert warning.origin.repository_path
        assert warning.origin.run_identity
        assert warning.origin.git_commit


def test_awareness_is_derived_without_mutating_error_memory():
    organ = seed_demonstrated_ai_toolkit_failures_run002()
    before = organ.memories

    awareness = form_pre_transformation_recurrence_awareness(
        organ,
        make_intended(FailureKind.EXECUTION),
    )

    assert awareness.has_demonstrated_precedent
    assert organ.memories == before


def test_awareness_is_immutable():
    organ = seed_demonstrated_ai_toolkit_failures_run002()

    awareness = form_pre_transformation_recurrence_awareness(
        organ,
        make_intended(FailureKind.EXECUTION),
    )

    with pytest.raises(FrozenInstanceError):
        awareness.transformation_title = "Mutated"


def test_awareness_does_not_possess_execution_authority():
    organ = seed_demonstrated_ai_toolkit_failures_run002()

    awareness = form_pre_transformation_recurrence_awareness(
        organ,
        make_intended(FailureKind.EXECUTION),
    )

    assert not hasattr(awareness, "allow_execution")
    assert not hasattr(awareness, "block_execution")
    assert not hasattr(awareness, "execute")
    assert not hasattr(awareness, "canonical")


def test_awareness_does_not_become_transformation_lifecycle():
    organ = seed_demonstrated_ai_toolkit_failures_run002()

    awareness = form_pre_transformation_recurrence_awareness(
        organ,
        make_intended(FailureKind.EXECUTION),
    )

    assert isinstance(
        awareness,
        PreTransformationRecurrenceAwareness,
    )
    assert not hasattr(awareness, "advance")
    assert not hasattr(awareness, "current_stage")


def test_absence_of_matching_precedent_remains_legitimate_non_answer():
    organ = seed_demonstrated_ai_toolkit_failures_run002()

    awareness = form_pre_transformation_recurrence_awareness(
        organ,
        make_intended(FailureKind.CONTRACT),
    )

    assert awareness.warnings == ()
    assert awareness.has_demonstrated_precedent is False


def test_duplicate_activity_does_not_duplicate_warning():
    organ = seed_demonstrated_ai_toolkit_failures_run002()

    awareness = form_pre_transformation_recurrence_awareness(
        organ,
        make_intended(
            FailureKind.PERMISSION,
            FailureKind.PERMISSION,
        ),
    )

    assert [warning.error_identity for warning in awareness.warnings] == [
        "ERR-0001"
    ]

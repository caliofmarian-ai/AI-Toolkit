from dataclasses import FrozenInstanceError

import pytest

from lib.python.epistemic.error_memory import (
    FailureKind,
    IntendedTransformation,
    PreExecutionRecurrenceExamination,
    RecurrenceDisposition,
    RecurrenceExaminationStatement,
    form_pre_execution_recurrence_examination,
    form_pre_transformation_recurrence_awareness,
    seed_demonstrated_ai_toolkit_failures_run002,
)


def awareness(*activities: FailureKind):
    organ = seed_demonstrated_ai_toolkit_failures_run002()

    intended = IntendedTransformation(
        identity="TRANSFORMATION-RUN004-TEST",
        title="Future Demonstrated Transformation",
        activities=activities,
        context=("Termux", "AI-Toolkit"),
    )

    return form_pre_transformation_recurrence_awareness(
        organ,
        intended,
    )


def statement(
    identity: str,
    disposition: RecurrenceDisposition = RecurrenceDisposition.ADDRESSED,
):
    return RecurrenceExaminationStatement(
        error_identity=identity,
        disposition=disposition,
        explanation=f"Explicit examination for {identity}.",
    )


def test_unexamined_relevant_precedent_remains_unresolved():
    result = form_pre_execution_recurrence_examination(
        awareness(FailureKind.EXECUTION)
    )

    assert isinstance(result, PreExecutionRecurrenceExamination)
    assert result.has_unresolved_precedent is True
    assert [item.error_identity for item in result.unresolved] == [
        "ERR-0003"
    ]


def test_addressed_precedent_remains_visible():
    result = form_pre_execution_recurrence_examination(
        awareness(FailureKind.PERMISSION),
        (statement("ERR-0001"),),
    )

    assert result.has_unresolved_precedent is False
    assert [item.error_identity for item in result.addressed] == [
        "ERR-0001"
    ]


def test_not_applicable_is_explicit_not_silent():
    result = form_pre_execution_recurrence_examination(
        awareness(FailureKind.VALIDATION),
        (
            statement(
                "ERR-0002",
                RecurrenceDisposition.NOT_APPLICABLE,
            ),
        ),
    )

    assert result.has_unresolved_precedent is False
    assert [item.error_identity for item in result.not_applicable] == [
        "ERR-0002"
    ]
    assert result.examinations[0].explanation


def test_multiple_precedents_can_be_examined_independently():
    result = form_pre_execution_recurrence_examination(
        awareness(
            FailureKind.PERMISSION,
            FailureKind.EXECUTION,
            FailureKind.EPISTEMIC,
        ),
        (
            statement("ERR-0001"),
            statement(
                "ERR-0003",
                RecurrenceDisposition.UNRESOLVED,
            ),
            statement("ERR-0004"),
        ),
    )

    states = {
        item.error_identity: item.disposition
        for item in result.examinations
    }

    assert states == {
        "ERR-0001": RecurrenceDisposition.ADDRESSED,
        "ERR-0003": RecurrenceDisposition.UNRESOLVED,
        "ERR-0004": RecurrenceDisposition.ADDRESSED,
    }


def test_missing_statement_does_not_remove_warning():
    result = form_pre_execution_recurrence_examination(
        awareness(
            FailureKind.PERMISSION,
            FailureKind.EXECUTION,
        ),
        (statement("ERR-0001"),),
    )

    assert [item.error_identity for item in result.examinations] == [
        "ERR-0001",
        "ERR-0003",
    ]

    assert [item.error_identity for item in result.unresolved] == [
        "ERR-0003"
    ]


def test_unknown_statement_cannot_invent_error_memory():
    with pytest.raises(ValueError):
        form_pre_execution_recurrence_examination(
            awareness(FailureKind.EXECUTION),
            (statement("ERR-DOES-NOT-EXIST"),),
        )


def test_duplicate_examination_statement_is_rejected():
    with pytest.raises(ValueError):
        form_pre_execution_recurrence_examination(
            awareness(FailureKind.PERMISSION),
            (
                statement("ERR-0001"),
                statement("ERR-0001"),
            ),
        )


def test_examination_preserves_warning_provenance():
    original = awareness(FailureKind.EPISTEMIC)

    result = form_pre_execution_recurrence_examination(
        original,
        (statement("ERR-0004"),),
    )

    warning = original.warnings[0]
    examination = result.examinations[0]

    assert examination.origin == warning.origin
    assert examination.prevention_rule == warning.prevention_rule


def test_examination_does_not_mutate_awareness():
    original = awareness(FailureKind.EXECUTION)
    before = original.warnings

    form_pre_execution_recurrence_examination(
        original,
        (statement("ERR-0003"),),
    )

    assert original.warnings == before


def test_examination_is_immutable():
    result = form_pre_execution_recurrence_examination(
        awareness(FailureKind.PERMISSION),
        (statement("ERR-0001"),),
    )

    with pytest.raises(FrozenInstanceError):
        result.transformation_title = "Rewritten"


def test_examination_has_no_execution_authority():
    result = form_pre_execution_recurrence_examination(
        awareness(FailureKind.EXECUTION)
    )

    assert not hasattr(result, "execute")
    assert not hasattr(result, "allow_execution")
    assert not hasattr(result, "block_execution")
    assert not hasattr(result, "approve")
    assert not hasattr(result, "canonical")


def test_examination_does_not_become_validation_engine():
    result = form_pre_execution_recurrence_examination(
        awareness(FailureKind.VALIDATION)
    )

    assert not hasattr(result, "validate_repository")
    assert not hasattr(result, "validate_semantic")
    assert not hasattr(result, "validate_canonical")
    assert not hasattr(result, "validate_regression")


def test_absence_of_precedent_remains_legitimate_empty_examination():
    result = form_pre_execution_recurrence_examination(
        awareness(FailureKind.CONTRACT)
    )

    assert result.examinations == ()
    assert result.unresolved == ()
    assert result.has_unresolved_precedent is False


def test_statement_requires_identity():
    with pytest.raises(ValueError):
        RecurrenceExaminationStatement(
            error_identity="",
            disposition=RecurrenceDisposition.ADDRESSED,
            explanation="Examined.",
        )


def test_statement_requires_explanation():
    with pytest.raises(ValueError):
        RecurrenceExaminationStatement(
            error_identity="ERR-0001",
            disposition=RecurrenceDisposition.ADDRESSED,
            explanation=" ",
        )


def test_all_four_existing_precedents_can_be_explicitly_examined():
    result = form_pre_execution_recurrence_examination(
        awareness(
            FailureKind.PERMISSION,
            FailureKind.EXECUTION,
            FailureKind.VALIDATION,
            FailureKind.EPISTEMIC,
        ),
        (
            statement("ERR-0001"),
            statement("ERR-0002"),
            statement("ERR-0003"),
            statement("ERR-0004"),
        ),
    )

    assert {
        item.error_identity
        for item in result.examinations
    } == {
        "ERR-0001",
        "ERR-0002",
        "ERR-0003",
        "ERR-0004",
    }

    assert result.unresolved == ()

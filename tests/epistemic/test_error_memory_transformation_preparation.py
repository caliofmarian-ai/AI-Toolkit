from dataclasses import FrozenInstanceError

import pytest

from lib.python.epistemic.error_memory import (
    FailureKind,
    IntendedTransformation,
    RecurrenceDisposition,
    RecurrenceExaminationStatement,
    TransformationPreparation,
    form_pre_execution_recurrence_examination,
    form_pre_transformation_recurrence_awareness,
    prepare_intended_transformation_from_error_memory,
    prepare_transformation_with_recurrence_evidence,
    seed_demonstrated_ai_toolkit_failures_run002,
)


def transformation(*activities: FailureKind) -> IntendedTransformation:
    return IntendedTransformation(
        identity="TRANSFORMATION-RUN005-TEST",
        title="Prepared Future Transformation",
        activities=activities,
        context=("AI-Toolkit", "Termux"),
    )


def statement(
    identity: str,
    disposition: RecurrenceDisposition = RecurrenceDisposition.ADDRESSED,
) -> RecurrenceExaminationStatement:
    return RecurrenceExaminationStatement(
        error_identity=identity,
        disposition=disposition,
        explanation=f"Explicit RUN 005 examination of {identity}.",
    )


def test_preparation_carries_transformation_identity():
    organ = seed_demonstrated_ai_toolkit_failures_run002()
    intended = transformation(FailureKind.EXECUTION)

    prepared = prepare_intended_transformation_from_error_memory(
        organ,
        intended,
        (statement("ERR-0003"),),
    )

    assert isinstance(prepared, TransformationPreparation)
    assert prepared.transformation is intended
    assert prepared.semantic_identity == (
        "TRANSFORMATION-RUN005-TEST — Prepared Future Transformation"
    )


def test_preparation_carries_recurrence_evidence():
    organ = seed_demonstrated_ai_toolkit_failures_run002()
    intended = transformation(FailureKind.PERMISSION)

    prepared = prepare_intended_transformation_from_error_memory(
        organ,
        intended,
        (statement("ERR-0001"),),
    )

    assert [item.error_identity for item in prepared.recurrence_evidence] == [
        "ERR-0001"
    ]

    assert prepared.recurrence_evidence[0].prevention_rule


def test_unresolved_precedent_survives_preparation():
    organ = seed_demonstrated_ai_toolkit_failures_run002()
    intended = transformation(FailureKind.EXECUTION)

    prepared = prepare_intended_transformation_from_error_memory(
        organ,
        intended,
    )

    assert prepared.has_unresolved_recurrence_evidence is True
    assert [
        item.error_identity
        for item in prepared.unresolved_recurrence_evidence
    ] == ["ERR-0003"]


def test_addressed_precedent_remains_visible_after_preparation():
    organ = seed_demonstrated_ai_toolkit_failures_run002()
    intended = transformation(FailureKind.EXECUTION)

    prepared = prepare_intended_transformation_from_error_memory(
        organ,
        intended,
        (statement("ERR-0003"),),
    )

    assert prepared.has_unresolved_recurrence_evidence is False
    assert prepared.recurrence_evidence[0].disposition == (
        RecurrenceDisposition.ADDRESSED
    )


def test_not_applicable_precedent_remains_visible_after_preparation():
    organ = seed_demonstrated_ai_toolkit_failures_run002()
    intended = transformation(FailureKind.VALIDATION)

    prepared = prepare_intended_transformation_from_error_memory(
        organ,
        intended,
        (
            statement(
                "ERR-0002",
                RecurrenceDisposition.NOT_APPLICABLE,
            ),
        ),
    )

    assert prepared.recurrence_evidence[0].disposition == (
        RecurrenceDisposition.NOT_APPLICABLE
    )


def test_empty_recurrence_evidence_is_legitimate_without_precedent():
    organ = seed_demonstrated_ai_toolkit_failures_run002()
    intended = transformation(FailureKind.CONTRACT)

    prepared = prepare_intended_transformation_from_error_memory(
        organ,
        intended,
    )

    assert prepared.recurrence_evidence == ()
    assert prepared.unresolved_recurrence_evidence == ()
    assert prepared.has_unresolved_recurrence_evidence is False


def test_preparation_does_not_mutate_error_memory():
    organ = seed_demonstrated_ai_toolkit_failures_run002()
    before = organ.memories

    prepare_intended_transformation_from_error_memory(
        organ,
        transformation(FailureKind.PERMISSION),
        (statement("ERR-0001"),),
    )

    assert organ.memories == before


def test_preparation_does_not_mutate_transformation():
    organ = seed_demonstrated_ai_toolkit_failures_run002()
    intended = transformation(FailureKind.EXECUTION)

    before_identity = intended.identity
    before_title = intended.title
    before_activities = intended.activities
    before_context = intended.context

    prepare_intended_transformation_from_error_memory(
        organ,
        intended,
        (statement("ERR-0003"),),
    )

    assert intended.identity == before_identity
    assert intended.title == before_title
    assert intended.activities == before_activities
    assert intended.context == before_context


def test_preparation_is_immutable():
    organ = seed_demonstrated_ai_toolkit_failures_run002()

    prepared = prepare_intended_transformation_from_error_memory(
        organ,
        transformation(FailureKind.PERMISSION),
        (statement("ERR-0001"),),
    )

    with pytest.raises(FrozenInstanceError):
        prepared.transformation = transformation(FailureKind.CONTRACT)


def test_mismatched_identity_is_rejected():
    organ = seed_demonstrated_ai_toolkit_failures_run002()

    first = IntendedTransformation(
        identity="TRANSFORMATION-A",
        title="Same title",
        activities=(FailureKind.EXECUTION,),
        context=(),
    )

    second = IntendedTransformation(
        identity="TRANSFORMATION-B",
        title="Same title",
        activities=(FailureKind.EXECUTION,),
        context=(),
    )

    awareness = form_pre_transformation_recurrence_awareness(
        organ,
        first,
    )

    examination = form_pre_execution_recurrence_examination(
        awareness,
        (statement("ERR-0003"),),
    )

    with pytest.raises(ValueError):
        prepare_transformation_with_recurrence_evidence(
            second,
            examination,
        )


def test_mismatched_title_is_rejected():
    organ = seed_demonstrated_ai_toolkit_failures_run002()

    first = IntendedTransformation(
        identity="TRANSFORMATION-A",
        title="First title",
        activities=(FailureKind.EXECUTION,),
        context=(),
    )

    second = IntendedTransformation(
        identity="TRANSFORMATION-A",
        title="Second title",
        activities=(FailureKind.EXECUTION,),
        context=(),
    )

    awareness = form_pre_transformation_recurrence_awareness(
        organ,
        first,
    )

    examination = form_pre_execution_recurrence_examination(
        awareness,
        (statement("ERR-0003"),),
    )

    with pytest.raises(ValueError):
        prepare_transformation_with_recurrence_evidence(
            second,
            examination,
        )


def test_unknown_statement_cannot_enter_preparation():
    organ = seed_demonstrated_ai_toolkit_failures_run002()

    with pytest.raises(ValueError):
        prepare_intended_transformation_from_error_memory(
            organ,
            transformation(FailureKind.EXECUTION),
            (statement("ERR-NOT-OBSERVED"),),
        )


def test_preparation_has_no_execution_authority():
    organ = seed_demonstrated_ai_toolkit_failures_run002()

    prepared = prepare_intended_transformation_from_error_memory(
        organ,
        transformation(FailureKind.EXECUTION),
    )

    for forbidden in (
        "execute",
        "allow_execution",
        "block_execution",
        "approve",
        "reject",
        "authorize",
        "canonicalize",
    ):
        assert not hasattr(prepared, forbidden)


def test_preparation_does_not_duplicate_execution_validator():
    organ = seed_demonstrated_ai_toolkit_failures_run002()

    prepared = prepare_intended_transformation_from_error_memory(
        organ,
        transformation(FailureKind.VALIDATION),
    )

    for forbidden in (
        "validate_repository",
        "validate_semantic",
        "validate_canonical",
        "validate_regression",
        "validate_acceptance",
    ):
        assert not hasattr(prepared, forbidden)


def test_all_demonstrated_precedents_can_survive_into_preparation():
    organ = seed_demonstrated_ai_toolkit_failures_run002()

    intended = transformation(
        FailureKind.PERMISSION,
        FailureKind.VALIDATION,
        FailureKind.EXECUTION,
        FailureKind.EPISTEMIC,
    )

    prepared = prepare_intended_transformation_from_error_memory(
        organ,
        intended,
        (
            statement("ERR-0001"),
            statement("ERR-0002"),
            statement("ERR-0003"),
            statement("ERR-0004"),
        ),
    )

    assert {
        item.error_identity
        for item in prepared.recurrence_evidence
    } == {
        "ERR-0001",
        "ERR-0002",
        "ERR-0003",
        "ERR-0004",
    }

    assert prepared.unresolved_recurrence_evidence == ()


def test_preparation_preserves_origin_and_prevention_rule():
    organ = seed_demonstrated_ai_toolkit_failures_run002()
    intended = transformation(FailureKind.EPISTEMIC)

    awareness = form_pre_transformation_recurrence_awareness(
        organ,
        intended,
    )

    warning = awareness.warnings[0]

    prepared = prepare_intended_transformation_from_error_memory(
        organ,
        intended,
        (statement("ERR-0004"),),
    )

    evidence = prepared.recurrence_evidence[0]

    assert evidence.origin == warning.origin
    assert evidence.prevention_rule == warning.prevention_rule

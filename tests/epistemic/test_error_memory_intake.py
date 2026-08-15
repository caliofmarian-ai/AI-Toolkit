from dataclasses import FrozenInstanceError

import pytest

from lib.python.epistemic.error_memory import (
    DemonstratedFailureObservation,
    ErrorMemoryOrgan,
    FailureIntakeResult,
    FailureKind,
    FailureOrigin,
    IntendedTransformation,
    form_error_memory_from_demonstrated_failure,
    form_pre_transformation_recurrence_awareness,
    remember_demonstrated_failure,
    seed_demonstrated_ai_toolkit_failures_run002,
)


def origin() -> FailureOrigin:
    return FailureOrigin(
        repository_path=(
            "work/implementation-reports/ERROR-MEMORY/"
            "demonstrated-failure.txt"
        ),
        run_identity="ERROR MEMORY RUN 003 TEST",
        git_commit="abc123",
    )


def complete_observation(
    identity: str = "ERR-TEST-INTAKE-001",
) -> DemonstratedFailureObservation:
    return DemonstratedFailureObservation(
        identity=identity,
        title="Demonstrated Intake Failure",
        kind=FailureKind.EXECUTION,
        symptom="A demonstrated execution stopped.",
        cause="An explicit precondition was absent.",
        recovery="The explicit precondition was restored.",
        prevention_rule=(
            "Verify the explicit precondition before execution."
        ),
        origin=origin(),
        demonstrated=True,
    )


def test_failure_observation_has_human_readable_identity():
    observation = complete_observation()

    assert observation.semantic_identity == (
        "ERR-TEST-INTAKE-001 — Demonstrated Intake Failure"
    )


def test_failure_observation_is_immutable():
    observation = complete_observation()

    with pytest.raises(FrozenInstanceError):
        observation.title = "Rewritten history"


def test_complete_demonstrated_failure_forms_error_memory():
    result = form_error_memory_from_demonstrated_failure(
        complete_observation()
    )

    assert result.accepted is True
    assert result.state == "FORMED"
    assert result.memory is not None
    assert result.memory.identity == "ERR-TEST-INTAKE-001"
    assert result.memory.origin == origin()


def test_non_demonstrated_failure_does_not_form_error_memory():
    observation = DemonstratedFailureObservation(
        identity="ERR-UNCONFIRMED",
        title="Unconfirmed Failure",
        kind=FailureKind.UNKNOWN,
        symptom="A possible failure was described.",
        cause="Possible cause.",
        recovery="Possible recovery.",
        prevention_rule="Possible prevention.",
        origin=origin(),
        demonstrated=False,
    )

    result = form_error_memory_from_demonstrated_failure(
        observation
    )

    assert result.accepted is False
    assert result.state == "UNCONFIRMED"
    assert result.memory is None


@pytest.mark.parametrize(
    "missing",
    ["cause", "recovery", "prevention_rule"],
)
def test_missing_historical_dimension_is_not_invented(missing):
    values = {
        "cause": "Explicit cause.",
        "recovery": "Explicit recovery.",
        "prevention_rule": "Explicit prevention.",
    }
    values[missing] = None

    observation = DemonstratedFailureObservation(
        identity="ERR-INCOMPLETE",
        title="Incomplete Demonstrated Failure",
        kind=FailureKind.EXECUTION,
        symptom="Execution demonstrably stopped.",
        cause=values["cause"],
        recovery=values["recovery"],
        prevention_rule=values["prevention_rule"],
        origin=origin(),
        demonstrated=True,
    )

    result = form_error_memory_from_demonstrated_failure(
        observation
    )

    assert result.accepted is False
    assert result.state == "INCOMPLETE"
    assert result.memory is None
    assert missing in result.reason


def test_rejected_intake_does_not_mutate_error_memory():
    organ = seed_demonstrated_ai_toolkit_failures_run002()
    before = organ.memories

    observation = DemonstratedFailureObservation(
        identity="ERR-INCOMPLETE",
        title="Incomplete Failure",
        kind=FailureKind.EXECUTION,
        symptom="Execution stopped.",
        origin=origin(),
        demonstrated=True,
    )

    evolved, result = remember_demonstrated_failure(
        organ,
        observation,
    )

    assert result.accepted is False
    assert evolved is organ
    assert organ.memories == before


def test_accepted_intake_returns_new_organ_without_mutating_source():
    organ = seed_demonstrated_ai_toolkit_failures_run002()
    before = organ.memories

    evolved, result = remember_demonstrated_failure(
        organ,
        complete_observation(),
    )

    assert result.accepted is True
    assert organ.memories == before
    assert evolved is not organ
    assert evolved.find("ERR-TEST-INTAKE-001") is not None


def test_formed_memory_preserves_exact_explicit_fields():
    observation = complete_observation()

    result = form_error_memory_from_demonstrated_failure(
        observation
    )

    memory = result.memory

    assert memory is not None
    assert memory.title == observation.title
    assert memory.kind == observation.kind
    assert memory.symptom == observation.symptom
    assert memory.cause == observation.cause
    assert memory.recovery == observation.recovery
    assert memory.prevention_rule == observation.prevention_rule
    assert memory.origin == observation.origin


def test_intake_result_is_immutable():
    result = form_error_memory_from_demonstrated_failure(
        complete_observation()
    )

    with pytest.raises(FrozenInstanceError):
        result.state = "REWRITTEN"


def test_invalid_accepted_result_without_memory_is_rejected():
    with pytest.raises(ValueError):
        FailureIntakeResult(
            observation_identity="ERR-X",
            observation_title="Invalid accepted result",
            accepted=True,
            state="FORMED",
            reason="Invalid.",
            memory=None,
        )


def test_invalid_rejected_result_with_memory_is_rejected():
    formed = form_error_memory_from_demonstrated_failure(
        complete_observation()
    )

    assert formed.memory is not None

    with pytest.raises(ValueError):
        FailureIntakeResult(
            observation_identity="ERR-X",
            observation_title="Invalid rejected result",
            accepted=False,
            state="REJECTED",
            reason="Invalid.",
            memory=formed.memory,
        )


def test_formed_failure_becomes_available_to_existing_recurrence_reflex():
    organ = ErrorMemoryOrgan()

    evolved, result = remember_demonstrated_failure(
        organ,
        complete_observation(),
    )

    assert result.accepted is True

    intended = IntendedTransformation(
        identity="TRANSFORMATION-AFTER-INTAKE",
        title="Future Execution",
        activities=(FailureKind.EXECUTION,),
    )

    awareness = form_pre_transformation_recurrence_awareness(
        evolved,
        intended,
    )

    assert [
        warning.error_identity
        for warning in awareness.warnings
    ] == ["ERR-TEST-INTAKE-001"]


def test_intake_has_no_execution_authority():
    result = form_error_memory_from_demonstrated_failure(
        complete_observation()
    )

    assert not hasattr(result, "execute")
    assert not hasattr(result, "allow_execution")
    assert not hasattr(result, "block_execution")
    assert not hasattr(result, "canonical")


def test_observation_is_not_evidence_or_canon_by_declaration():
    observation = complete_observation()

    assert not hasattr(observation, "evidence")
    assert not hasattr(observation, "canonical")
    assert not hasattr(observation, "authority")


def test_intake_does_not_perform_arbitrary_repository_ingestion():
    observation = complete_observation()

    assert not hasattr(observation, "read_repository")
    assert not hasattr(observation, "read_stdout")
    assert not hasattr(observation, "read_conversation")
    assert not hasattr(observation, "scan")


@pytest.mark.parametrize(
    "field,value",
    [
        ("identity", ""),
        ("title", " "),
        ("symptom", ""),
    ],
)
def test_structurally_empty_observation_is_rejected(
    field,
    value,
):
    kwargs = {
        "identity": "ERR-VALID",
        "title": "Valid failure",
        "kind": FailureKind.EXECUTION,
        "symptom": "Valid symptom.",
        "origin": origin(),
        "demonstrated": True,
    }
    kwargs[field] = value

    with pytest.raises(ValueError):
        DemonstratedFailureObservation(**kwargs)


@pytest.mark.parametrize(
    "field",
    ["cause", "recovery", "prevention_rule"],
)
def test_blank_optional_interpretive_field_is_rejected(field):
    kwargs = {
        "identity": "ERR-VALID",
        "title": "Valid failure",
        "kind": FailureKind.EXECUTION,
        "symptom": "Valid symptom.",
        "origin": origin(),
        "demonstrated": True,
        field: " ",
    }

    with pytest.raises(ValueError):
        DemonstratedFailureObservation(**kwargs)

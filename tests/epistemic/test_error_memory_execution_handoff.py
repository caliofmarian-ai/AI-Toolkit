from dataclasses import FrozenInstanceError

import pytest

from lib.python.epistemic.error_memory import (
    FailureKind,
    IntendedTransformation,
    RecurrenceEvidenceHandoff,
    RecurrenceDisposition,
    RecurrenceExaminationStatement,
    form_recurrence_evidence_handoff,
    prepare_intended_transformation_from_error_memory,
    seed_demonstrated_ai_toolkit_failures_run002,
)

from lib.python.autonomous_execution_engine.models import (
    EXECUTION_VERSION,
    ExecutionContext,
)


def _transformation():
    return IntendedTransformation(
        identity="RUN006-TRANSFORMATION",
        title="RUN 006 Test Transformation",
        activities=(
            FailureKind.EXECUTION,
            FailureKind.VALIDATION,
            FailureKind.EPISTEMIC,
        ),
        context=("AI-Toolkit",),
    )


def _statement(identity):
    return RecurrenceExaminationStatement(
        error_identity=identity,
        disposition=RecurrenceDisposition.ADDRESSED,
        explanation=f"Explicitly examined {identity}.",
    )


def test_handoff_carries_exact_preparation_evidence():
    organ = seed_demonstrated_ai_toolkit_failures_run002()

    preparation = prepare_intended_transformation_from_error_memory(
        organ,
        _transformation(),
        (
            _statement("ERR-0002"),
            _statement("ERR-0003"),
            _statement("ERR-0004"),
        ),
    )

    handoff = form_recurrence_evidence_handoff(preparation)

    assert isinstance(handoff, RecurrenceEvidenceHandoff)
    assert handoff.transformation_identity == "RUN006-TRANSFORMATION"

    assert {
        item.error_identity
        for item in handoff.evidence
    } == {
        "ERR-0002",
        "ERR-0003",
        "ERR-0004",
    }

    assert handoff.unresolved == ()


def test_unresolved_precedent_survives_handoff():
    organ = seed_demonstrated_ai_toolkit_failures_run002()

    preparation = prepare_intended_transformation_from_error_memory(
        organ,
        _transformation(),
    )

    handoff = form_recurrence_evidence_handoff(preparation)

    assert handoff.has_unresolved is True
    assert {
        item.error_identity
        for item in handoff.unresolved
    } == {
        "ERR-0002",
        "ERR-0003",
        "ERR-0004",
    }


def test_handoff_is_serializable():
    organ = seed_demonstrated_ai_toolkit_failures_run002()

    preparation = prepare_intended_transformation_from_error_memory(
        organ,
        _transformation(),
    )

    body = form_recurrence_evidence_handoff(
        preparation
    ).to_dict()

    assert body["transformation_identity"] == (
        "RUN006-TRANSFORMATION"
    )
    assert body["evidence_count"] == 3
    assert body["unresolved_count"] == 3
    assert body["has_unresolved"] is True

    for item in body["evidence"]:
        assert "error_identity" in item
        assert "prevention_rule" in item
        assert "origin" in item
        assert "disposition" in item
        assert "explanation" in item

        assert set(item["origin"]) == {
            "repository_path",
            "run_identity",
            "git_commit",
        }

        assert item["origin"]["repository_path"]
        assert item["origin"]["run_identity"]

        assert "source" not in item["origin"]
        assert "reference" not in item["origin"]


def test_handoff_does_not_mutate_error_memory():
    organ = seed_demonstrated_ai_toolkit_failures_run002()
    before = organ.memories

    preparation = prepare_intended_transformation_from_error_memory(
        organ,
        _transformation(),
    )

    form_recurrence_evidence_handoff(preparation)

    assert organ.memories == before


def test_handoff_is_immutable():
    organ = seed_demonstrated_ai_toolkit_failures_run002()

    preparation = prepare_intended_transformation_from_error_memory(
        organ,
        _transformation(),
    )

    handoff = form_recurrence_evidence_handoff(preparation)

    with pytest.raises(FrozenInstanceError):
        handoff.transformation_title = "rewritten"


def test_handoff_has_no_execution_authority():
    organ = seed_demonstrated_ai_toolkit_failures_run002()

    preparation = prepare_intended_transformation_from_error_memory(
        organ,
        _transformation(),
    )

    handoff = form_recurrence_evidence_handoff(preparation)

    for forbidden in (
        "execute",
        "approve",
        "reject",
        "authorize",
        "allow_execution",
        "block_execution",
        "validate",
        "canonicalize",
    ):
        assert not hasattr(handoff, forbidden)


def test_execution_context_carries_recurrence_evidence():
    recurrence = {
        "transformation_identity": "RUN006-TRANSFORMATION",
        "evidence": [{"error_identity": "ERR-0003"}],
        "unresolved": [{"error_identity": "ERR-0003"}],
        "evidence_count": 1,
        "unresolved_count": 1,
        "has_unresolved": True,
    }

    context = ExecutionContext(
        execution_id="EXEC-RUN006",
        repository="/tmp/repo",
        workspace="/tmp",
        branch="main",
        commit="abc",
        issue="ISS-001",
        batch="BATCH-001",
        milestone="M-001",
        core="CORE-015",
        roadmap="ROADMAP",
        planning_id="PLAN-001",
        state_id="STATE-001",
        synchronization_id="SYNC-001",
        briefing_id="BRF-001",
        owner="owner",
        timestamp="2026-01-01T00:00:00+00:00",
        environment="/tmp/repo",
        policy="READ_ONLY",
        approval="APPROVED",
        confidence=1.0,
        mode="READ_ONLY",
        schema_version=EXECUTION_VERSION,
        recurrence_evidence=recurrence,
    )

    body = context.to_dict()

    assert body["recurrence_evidence"] == recurrence
    assert body["recurrence_evidence"]["has_unresolved"] is True


def test_execution_context_remains_backward_compatible():
    context = ExecutionContext(
        execution_id="EXEC-RUN006",
        repository="/tmp/repo",
        workspace="/tmp",
        branch="main",
        commit="abc",
        issue="",
        batch="",
        milestone="",
        core="CORE-015",
        roadmap="",
        planning_id="",
        state_id="",
        synchronization_id="",
        briefing_id="",
        owner="",
        timestamp="2026-01-01T00:00:00+00:00",
        environment="/tmp/repo",
        policy="READ_ONLY",
        approval="APPROVED",
        confidence=0.0,
        mode="READ_ONLY",
        schema_version=EXECUTION_VERSION,
    )

    assert context.recurrence_evidence == {}
    assert context.to_dict()["recurrence_evidence"] == {}

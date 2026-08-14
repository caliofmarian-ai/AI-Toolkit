from dataclasses import FrozenInstanceError

import pytest

from lib.python.epistemic.transformation import (
    NO_OWNER_DECISION,
    NOT_EXECUTED,
    NOT_VERIFIED,
    UNKNOWN,
    TransformationError,
    TransformationLifecycle,
)


def test_begin_preserves_existing_lifecycle_entry_point(tmp_path):
    lifecycle = TransformationLifecycle(tmp_path)

    transformation = lifecycle.begin("Preserve project evolution")

    assert transformation.status == "RUNNING"
    assert transformation.need == "Preserve project evolution"
    assert transformation.identifier == "TR-000001"
    assert (tmp_path / "TR-000001.md").is_file()


def test_transformation_exposes_exact_twelve_dimensions(tmp_path):
    transformation = TransformationLifecycle(tmp_path).begin(
        "Preserve project evolution"
    )

    assert tuple(name for name, _ in transformation.dimensions) == (
        "Need",
        "Research",
        "Hypothesis",
        "Owner Decision",
        "Implementation",
        "Execution",
        "Artifacts / Effects",
        "Evidence",
        "Verification",
        "Knowledge",
        "Evolution",
        "Next Transformation",
    )


def test_missing_knowledge_is_explicit_and_not_invented(tmp_path):
    transformation = TransformationLifecycle(tmp_path).begin(
        "Preserve project evolution"
    )

    assert transformation.research == UNKNOWN
    assert transformation.hypothesis == UNKNOWN
    assert transformation.owner_decision == NO_OWNER_DECISION
    assert transformation.execution == NOT_EXECUTED
    assert transformation.verification == NOT_VERIFIED


def test_begin_accepts_known_research_hypothesis_and_owner_decision(tmp_path):
    transformation = TransformationLifecycle(tmp_path).begin(
        "Preserve project evolution",
        research="Repository and Canon inspected.",
        hypothesis="A complete Transformation model preserves continuity.",
        owner_decision="Owner authorized PCC-02 implementation.",
    )

    assert transformation.research == "Repository and Canon inspected."
    assert (
        transformation.hypothesis
        == "A complete Transformation model preserves continuity."
    )
    assert (
        transformation.owner_decision
        == "Owner authorized PCC-02 implementation."
    )


def test_parent_transformation_uses_existing_tr_identity_family(tmp_path):
    lifecycle = TransformationLifecycle(tmp_path)

    transformation = lifecycle.begin(
        "Continue prior evolution",
        parent_transformation="TR-000042",
    )

    assert transformation.parent_transformation == "TR-000042"


def test_invalid_parent_identity_is_rejected(tmp_path):
    lifecycle = TransformationLifecycle(tmp_path)

    with pytest.raises(TransformationError):
        lifecycle.begin(
            "Continue prior evolution",
            parent_transformation="random-id",
        )


def test_identity_advances_from_existing_local_transformation_evidence(tmp_path):
    (tmp_path / "TR-000004.md").write_text("historical", encoding="utf-8")
    (tmp_path / "TR-000009.md").write_text("historical", encoding="utf-8")

    transformation = TransformationLifecycle(tmp_path).begin(
        "Continue evolution"
    )

    assert transformation.identifier == "TR-000010"


def test_complete_preserves_entry_point_and_records_supplied_epistemic_state(
    tmp_path,
):
    lifecycle = TransformationLifecycle(tmp_path)
    transformation = lifecycle.begin("Implement capability")

    completed = lifecycle.complete(
        transformation,
        implementation="Implementation applied.",
        execution="Tests executed successfully.",
        artifacts_effects="Transformation organ matured.",
        evidence="Behavioral tests passed.",
        verification="Verified against expected behavior.",
        knowledge="Existing organ can represent complete Transformation.",
        evolution="PCC-02 executable anatomy advanced.",
        next_transformation="Integrate persistent Transformation storage.",
    )

    assert completed.status == "COMPLETED"
    assert completed.ended_at is not None
    assert completed.execution == "Tests executed successfully."
    assert completed.verification == "Verified against expected behavior."

    artifact = (tmp_path / "TR-000001.md").read_text(encoding="utf-8")

    assert "## Need" in artifact
    assert "## Research" in artifact
    assert "## Hypothesis" in artifact
    assert "## Owner Decision" in artifact
    assert "## Implementation" in artifact
    assert "## Execution" in artifact
    assert "## Artifacts / Effects" in artifact
    assert "## Evidence" in artifact
    assert "## Verification" in artifact
    assert "## Knowledge" in artifact
    assert "## Evolution" in artifact
    assert "## Next Transformation" in artifact


def test_completion_does_not_falsely_claim_execution_or_verification(tmp_path):
    lifecycle = TransformationLifecycle(tmp_path)
    transformation = lifecycle.begin("Characterize unknown execution")

    completed = lifecycle.complete(transformation)

    assert completed.execution == NOT_EXECUTED
    assert completed.verification == NOT_VERIFIED
    assert completed.evidence == UNKNOWN


def test_completed_transformation_cannot_be_completed_twice(tmp_path):
    lifecycle = TransformationLifecycle(tmp_path)
    transformation = lifecycle.begin("One lifecycle")

    completed = lifecycle.complete(transformation)

    with pytest.raises(TransformationError):
        lifecycle.complete(completed)


def test_transformation_value_is_immutable(tmp_path):
    transformation = TransformationLifecycle(tmp_path).begin(
        "Preserve identity"
    )

    with pytest.raises(FrozenInstanceError):
        transformation.need = "Rewrite history"


def test_empty_need_is_rejected(tmp_path):
    lifecycle = TransformationLifecycle(tmp_path)

    with pytest.raises(TransformationError):
        lifecycle.begin("   ")


def test_running_transformation_survives_lifecycle_restart(tmp_path):
    first_lifecycle = TransformationLifecycle(tmp_path)

    original = first_lifecycle.begin(
        "Preserve Transformation across restart",
        research="Canon inspected.",
        hypothesis="Persisted evidence can reconstruct Transformation.",
        owner_decision="Owner authorized PCC-02.",
    )

    restarted_lifecycle = TransformationLifecycle(tmp_path)
    recovered = restarted_lifecycle.get(original.identifier)

    assert recovered == original
    assert recovered.status == "RUNNING"
    assert recovered.ended_at is None


def test_completed_transformation_survives_lifecycle_restart(tmp_path):
    first_lifecycle = TransformationLifecycle(tmp_path)

    running = first_lifecycle.begin(
        "Recover completed Transformation",
        parent_transformation="TR-000042",
        research="Repository inspected.",
        hypothesis="Recovery preserves all epistemic dimensions.",
        owner_decision="Owner authorized implementation.",
    )

    completed = first_lifecycle.complete(
        running,
        implementation="Existing organ extended.",
        execution="Behavioral examination executed.",
        artifacts_effects="Persistent recovery became operational.",
        evidence="Tests demonstrate restart recovery.",
        verification="Recovered value equals persisted value.",
        knowledge="Transformation can survive process restart.",
        evolution="Continuity advanced.",
        next_transformation="Continue PCC-02 maturation.",
    )

    restarted_lifecycle = TransformationLifecycle(tmp_path)
    recovered = restarted_lifecycle.get(completed.identifier)

    assert recovered == completed
    assert recovered.parent_transformation == "TR-000042"
    assert recovered.ended_at == completed.ended_at
    assert recovered.dimensions == completed.dimensions


def test_recovery_uses_stable_identity_not_filename_inference(tmp_path):
    lifecycle = TransformationLifecycle(tmp_path)

    transformation = lifecycle.begin("Protect stable identity")

    original_path = tmp_path / f"{transformation.identifier}.md"
    text = original_path.read_text(encoding="utf-8")

    original_path.write_text(
        text.replace(
            f"Transformation ID: {transformation.identifier}",
            "Transformation ID: TR-999999",
            1,
        ),
        encoding="utf-8",
    )

    with pytest.raises(
        TransformationError,
        match="identity does not match",
    ):
        lifecycle.get(transformation.identifier)


def test_missing_transformation_is_explicit(tmp_path):
    lifecycle = TransformationLifecycle(tmp_path)

    with pytest.raises(
        TransformationError,
        match="does not exist",
    ):
        lifecycle.get("TR-000404")


def test_malformed_persisted_transformation_is_not_silently_invented(tmp_path):
    path = tmp_path / "TR-000001.md"
    path.write_text(
        """# Transformation Evidence

## Identity

Transformation ID: TR-000001
Parent Transformation: NONE
Started: 2026-08-14T00:00:00+00:00
Ended: NOT ENDED
Status: RUNNING

## Need

Known need.
""",
        encoding="utf-8",
    )

    lifecycle = TransformationLifecycle(tmp_path)

    with pytest.raises(
        TransformationError,
        match="missing section",
    ):
        lifecycle.get("TR-000001")


def test_recovered_transformation_can_continue_lifecycle(tmp_path):
    first_lifecycle = TransformationLifecycle(tmp_path)

    running = first_lifecycle.begin(
        "Resume work after restart"
    )

    restarted_lifecycle = TransformationLifecycle(tmp_path)
    recovered = restarted_lifecycle.get(running.identifier)

    completed = restarted_lifecycle.complete(
        recovered,
        execution="Execution resumed after restart.",
        verification="Lifecycle continuation verified.",
    )

    assert completed.status == "COMPLETED"
    assert completed.execution == "Execution resumed after restart."

    second_restart = TransformationLifecycle(tmp_path)
    final = second_restart.get(completed.identifier)

    assert final == completed

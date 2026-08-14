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


def test_list_transformations_recovers_local_history_in_identity_order(tmp_path):
    lifecycle = TransformationLifecycle(tmp_path)

    first = lifecycle.complete(
        lifecycle.begin("First")
    )

    second = lifecycle.complete(
        lifecycle.begin(
            "Second",
            parent_transformation=first.identifier,
        )
    )

    restarted = TransformationLifecycle(tmp_path)

    assert tuple(
        transformation.identifier
        for transformation in restarted.list_transformations()
    ) == (
        first.identifier,
        second.identifier,
    )


def test_children_exposes_locally_known_direct_descendants(tmp_path):
    lifecycle = TransformationLifecycle(tmp_path)

    root = lifecycle.complete(
        lifecycle.begin("Root")
    )

    first_child = lifecycle.complete(
        lifecycle.begin(
            "First child",
            parent_transformation=root.identifier,
        )
    )

    second_child = lifecycle.begin(
        "Second child",
        parent_transformation=root.identifier,
    )

    unrelated = lifecycle.begin("Unrelated root")

    children = lifecycle.children(root.identifier)

    assert tuple(
        item.identifier for item in children
    ) == (
        first_child.identifier,
        second_child.identifier,
    )

    assert unrelated.identifier not in {
        item.identifier for item in children
    }


def test_children_can_query_valid_external_parent_identity(tmp_path):
    lifecycle = TransformationLifecycle(tmp_path)

    child = lifecycle.begin(
        "Child of externally represented Transformation",
        parent_transformation="TR-000042",
    )

    assert lifecycle.children("TR-000042") == (child,)


def test_lineage_reconstructs_locally_demonstrable_ancestry(tmp_path):
    lifecycle = TransformationLifecycle(tmp_path)

    first = lifecycle.complete(
        lifecycle.begin("Need one")
    )

    second = lifecycle.complete(
        lifecycle.begin(
            "Need two",
            parent_transformation=first.identifier,
        )
    )

    third = lifecycle.begin(
        "Need three",
        parent_transformation=second.identifier,
    )

    restarted = TransformationLifecycle(tmp_path)

    lineage = restarted.lineage(third.identifier)

    assert tuple(
        item.identifier for item in lineage
    ) == (
        first.identifier,
        second.identifier,
        third.identifier,
    )

    assert tuple(
        item.need for item in lineage
    ) == (
        "Need one",
        "Need two",
        "Need three",
    )


def test_root_lineage_contains_only_root(tmp_path):
    lifecycle = TransformationLifecycle(tmp_path)

    root = lifecycle.begin("Independent root")

    assert lifecycle.lineage(root.identifier) == (root,)


def test_external_or_missing_parent_is_preserved_but_not_invented_in_lineage(
    tmp_path,
):
    lifecycle = TransformationLifecycle(tmp_path)

    child = lifecycle.begin(
        "Continue externally known history",
        parent_transformation="TR-000042",
    )

    assert child.parent_transformation == "TR-000042"

    with pytest.raises(
        TransformationError,
        match="lineage is incomplete",
    ):
        lifecycle.lineage(child.identifier)


def test_parent_removed_after_persistence_makes_lineage_explicitly_incomplete(
    tmp_path,
):
    lifecycle = TransformationLifecycle(tmp_path)

    parent = lifecycle.complete(
        lifecycle.begin("Parent")
    )

    child = lifecycle.begin(
        "Child",
        parent_transformation=parent.identifier,
    )

    (tmp_path / f"{parent.identifier}.md").unlink()

    with pytest.raises(
        TransformationError,
        match="lineage is incomplete",
    ):
        lifecycle.lineage(child.identifier)


def test_lineage_cycle_is_rejected(tmp_path):
    lifecycle = TransformationLifecycle(tmp_path)

    first = lifecycle.complete(
        lifecycle.begin("First")
    )

    second = lifecycle.begin(
        "Second",
        parent_transformation=first.identifier,
    )

    first_path = tmp_path / f"{first.identifier}.md"
    text = first_path.read_text(encoding="utf-8")

    first_path.write_text(
        text.replace(
            "Parent Transformation: NONE",
            f"Parent Transformation: {second.identifier}",
            1,
        ),
        encoding="utf-8",
    )

    with pytest.raises(
        TransformationError,
        match="cycle",
    ):
        lifecycle.lineage(second.identifier)


def test_malformed_local_history_is_not_silently_skipped(tmp_path):
    lifecycle = TransformationLifecycle(tmp_path)

    lifecycle.begin("Valid Transformation")

    (tmp_path / "TR-000002.md").write_text(
        "# malformed",
        encoding="utf-8",
    )

    with pytest.raises(TransformationError):
        lifecycle.list_transformations()


def test_increment_003_preserves_external_parent_contract_after_restart(
    tmp_path,
):
    lifecycle = TransformationLifecycle(tmp_path)

    original = lifecycle.begin(
        "Preserve established contract",
        parent_transformation="TR-000042",
    )

    restarted = TransformationLifecycle(tmp_path)
    recovered = restarted.get(original.identifier)

    assert recovered == original
    assert recovered.parent_transformation == "TR-000042"


def test_semantic_title_reuses_existing_need(tmp_path):
    transformation = TransformationLifecycle(tmp_path).begin(
        "Prevent epistemic context loss"
    )

    assert transformation.semantic_title == (
        "Prevent epistemic context loss"
    )

    assert transformation.semantic_title == transformation.need


def test_human_identity_combines_stable_id_and_semantic_meaning(tmp_path):
    transformation = TransformationLifecycle(tmp_path).begin(
        "Preserve understandable history"
    )

    assert transformation.human_identity == (
        f"{transformation.identifier} — "
        "Preserve understandable history"
    )


def test_human_identity_survives_restart(tmp_path):
    lifecycle = TransformationLifecycle(tmp_path)

    original = lifecycle.begin(
        "Preserve semantic identity across restart"
    )

    restarted = TransformationLifecycle(tmp_path)
    recovered = restarted.get(original.identifier)

    assert recovered == original
    assert recovered.semantic_title == original.semantic_title
    assert recovered.human_identity == original.human_identity


def test_persisted_identity_contains_id_and_semantic_meaning(tmp_path):
    lifecycle = TransformationLifecycle(tmp_path)

    transformation = lifecycle.begin(
        "Make Transformation understandable to humans"
    )

    artifact = (
        tmp_path / f"{transformation.identifier}.md"
    ).read_text(encoding="utf-8")

    expected = (
        "Transformation: "
        f"{transformation.identifier} — "
        "Make Transformation understandable to humans"
    )

    assert expected in artifact


def test_dimensions_contract_remains_exactly_twelve_tuple_pairs(tmp_path):
    transformation = TransformationLifecycle(tmp_path).begin(
        "Preserve twelve-dimensional anatomy"
    )

    assert isinstance(transformation.dimensions, tuple)
    assert len(transformation.dimensions) == 12

    assert tuple(
        name for name, _ in transformation.dimensions
    ) == (
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


def test_lineage_exposes_human_identity_after_restart(tmp_path):
    lifecycle = TransformationLifecycle(tmp_path)

    parent = lifecycle.complete(
        lifecycle.begin("Recognize original need")
    )

    child = lifecycle.begin(
        "Evolve original need",
        parent_transformation=parent.identifier,
    )

    restarted = TransformationLifecycle(tmp_path)
    lineage = restarted.lineage(child.identifier)

    assert tuple(item.human_identity for item in lineage) == (
        f"{parent.identifier} — Recognize original need",
        f"{child.identifier} — Evolve original need",
    )


def test_epistemic_relation_maps_identity_meaning_and_reference(tmp_path):
    lifecycle = TransformationLifecycle(tmp_path)

    transformation = lifecycle.begin(
        "Preserve provenance without copying artifacts"
    )

    related = lifecycle.relate(
        transformation,
        relation="SUPPORTED BY",
        target_identity="EVIDENCE-LOCAL-001",
        target_title="Behavioral verification report",
        target_reference="work/reports/verification.md",
    )

    assert len(related.relations) == 1

    reference = related.relations[0]

    assert reference.relation == "SUPPORTED BY"
    assert reference.target_identity == "EVIDENCE-LOCAL-001"
    assert reference.target_title == "Behavioral verification report"
    assert reference.target_reference == "work/reports/verification.md"
    assert reference.human_identity == (
        "EVIDENCE-LOCAL-001 — Behavioral verification report"
    )


def test_relations_are_structural_not_a_thirteenth_dimension(tmp_path):
    lifecycle = TransformationLifecycle(tmp_path)

    transformation = lifecycle.begin(
        "Keep epistemic anatomy stable"
    )

    related = lifecycle.relate(
        transformation,
        relation="DERIVED FROM",
        target_identity="CANON-001",
        target_title="Canonical governing artifact",
        target_reference="canon/example.md",
    )

    assert len(related.dimensions) == 12
    assert tuple(name for name, _ in related.dimensions) == (
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


def test_relation_survives_restart(tmp_path):
    lifecycle = TransformationLifecycle(tmp_path)

    transformation = lifecycle.begin(
        "Recover explicit provenance"
    )

    related = lifecycle.relate(
        transformation,
        relation="WITNESSED BY",
        target_identity="REPORT-001",
        target_title="Execution witness",
        target_reference="work/report.md",
    )

    restarted = TransformationLifecycle(tmp_path)
    recovered = restarted.get(related.identifier)

    assert recovered == related
    assert recovered.relations == related.relations


def test_persisted_relation_is_human_readable_and_resolvable(tmp_path):
    lifecycle = TransformationLifecycle(tmp_path)

    transformation = lifecycle.begin(
        "Expose relation to human inspection"
    )

    related = lifecycle.relate(
        transformation,
        relation="AUTHORIZED BY",
        target_identity="OWNER-DECISION-001",
        target_title="Human authorization",
        target_reference="work/decision.md",
    )

    artifact = (
        tmp_path / f"{related.identifier}.md"
    ).read_text(encoding="utf-8")

    assert "## Epistemic Relations" in artifact
    assert "- Relation: AUTHORIZED BY" in artifact
    assert (
        "Target: OWNER-DECISION-001 — Human authorization"
        in artifact
    )
    assert "Reference: work/decision.md" in artifact


def test_multiple_relation_types_do_not_require_parallel_organs(tmp_path):
    lifecycle = TransformationLifecycle(tmp_path)

    transformation = lifecycle.begin(
        "Map existing epistemic neighborhood"
    )

    transformation = lifecycle.relate(
        transformation,
        relation="DERIVED FROM",
        target_identity="CANON-001",
        target_title="Governing Canon",
        target_reference="canon/governing.md",
    )

    transformation = lifecycle.relate(
        transformation,
        relation="SUPPORTED BY",
        target_identity="REPORT-001",
        target_title="Verification evidence",
        target_reference="work/report.md",
    )

    transformation = lifecycle.relate(
        transformation,
        relation="MATERIALIZED BY",
        target_identity="COMMIT-abc123",
        target_title="Repository materialization",
        target_reference="git:abc123",
    )

    assert tuple(
        relation.relation
        for relation in transformation.relations
    ) == (
        "DERIVED FROM",
        "SUPPORTED BY",
        "MATERIALIZED BY",
    )


def test_duplicate_relation_is_idempotent(tmp_path):
    lifecycle = TransformationLifecycle(tmp_path)

    transformation = lifecycle.begin(
        "Avoid duplicate epistemic edges"
    )

    first = lifecycle.relate(
        transformation,
        relation="SUPPORTED BY",
        target_identity="REPORT-001",
        target_title="One report",
        target_reference="work/report.md",
    )

    second = lifecycle.relate(
        first,
        relation="SUPPORTED BY",
        target_identity="REPORT-001",
        target_title="One report",
        target_reference="work/report.md",
    )

    assert second == first
    assert len(second.relations) == 1


def test_relation_requires_human_semantic_identity(tmp_path):
    lifecycle = TransformationLifecycle(tmp_path)

    transformation = lifecycle.begin(
        "Reject naked relation identity"
    )

    with pytest.raises(TransformationError):
        lifecycle.relate(
            transformation,
            relation="SUPPORTED BY",
            target_identity="REPORT-001",
            target_title="   ",
            target_reference="work/report.md",
        )


def test_relation_requires_resolvable_reference_text(tmp_path):
    lifecycle = TransformationLifecycle(tmp_path)

    transformation = lifecycle.begin(
        "Reject reference without location"
    )

    with pytest.raises(TransformationError):
        lifecycle.relate(
            transformation,
            relation="SUPPORTED BY",
            target_identity="REPORT-001",
            target_title="Evidence report",
            target_reference="   ",
        )


def test_relate_rejects_stale_transformation_value(tmp_path):
    lifecycle = TransformationLifecycle(tmp_path)

    original = lifecycle.begin(
        "Protect current persisted epistemic state"
    )

    matured = lifecycle.relate(
        original,
        relation="DERIVED FROM",
        target_identity="CANON-001",
        target_title="Canon",
        target_reference="canon/example.md",
    )

    assert matured != original

    with pytest.raises(
        TransformationError,
        match="does not match persisted state",
    ):
        lifecycle.relate(
            original,
            relation="SUPPORTED BY",
            target_identity="REPORT-001",
            target_title="Report",
            target_reference="work/report.md",
        )


def test_completion_preserves_structural_relations(tmp_path):
    lifecycle = TransformationLifecycle(tmp_path)

    running = lifecycle.begin(
        "Carry provenance through completion"
    )

    related = lifecycle.relate(
        running,
        relation="DERIVED FROM",
        target_identity="CANON-001",
        target_title="Governing Canon",
        target_reference="canon/governing.md",
    )

    completed = lifecycle.complete(
        related,
        execution="Executed.",
        verification="Verified.",
    )

    assert completed.relations == related.relations

    restarted = TransformationLifecycle(tmp_path)
    recovered = restarted.get(completed.identifier)

    assert recovered == completed
    assert recovered.relations == related.relations

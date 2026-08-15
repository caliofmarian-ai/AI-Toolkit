from dataclasses import FrozenInstanceError

import pytest

from python.epistemic.living_project_image import (
    EpistemicReference,
    LivingProjectImageError,
    LivingProjectStatement,
    form_living_project_image,
)


def reference(
    identifier="EV-000001",
    title="Repository evidence",
    kind="EVIDENCE",
    location="tests/epistemic/test_provenance.py",
):
    return EpistemicReference(
        identifier=identifier,
        title=title,
        kind=kind,
        reference=location,
    )


def demonstrated():
    return LivingProjectStatement(
        identifier="LPI-STMT-000001",
        title="Provenance capability",
        statement="The organism preserves explicit provenance.",
        epistemic_state="DEMONSTRATED",
        supports=(reference(),),
        provenance_paths=(
            "Current State → Knowledge → Verification → Evidence → Source",
        ),
    )


def test_statement_has_human_readable_identity():
    item = demonstrated()

    assert (
        item.display_identity
        == "LPI-STMT-000001 — Provenance capability"
    )


def test_reference_has_human_readable_identity():
    item = reference()

    assert item.display_identity == "EV-000001 — Repository evidence"


def test_demonstrated_statement_is_explicitly_derived_and_non_authoritative():
    item = demonstrated()

    assert item.derived is True
    assert item.authoritative is False


def test_demonstrated_state_requires_support():
    with pytest.raises(
        LivingProjectImageError,
        match="requires explicit supporting reality",
    ):
        LivingProjectStatement(
            identifier="LPI-STMT-000001",
            title="Unsupported certainty",
            statement="This must not masquerade as demonstrated.",
            epistemic_state="DEMONSTRATED",
        )


def test_unknown_is_a_legitimate_non_answer_without_fabricated_support():
    item = LivingProjectStatement(
        identifier="LPI-STMT-000002",
        title="Unknown runtime state",
        statement="The runtime condition is not known.",
        epistemic_state="UNKNOWN",
    )

    assert item.epistemic_state == "UNKNOWN"
    assert item.supports == ()
    assert item.provenance_paths == ()


def test_uncertainty_remains_visible():
    item = LivingProjectStatement(
        identifier="LPI-STMT-000003",
        title="Uncertain integration state",
        statement="Integration state remains uncertain.",
        epistemic_state="UNCERTAIN",
        supports=(reference(),),
        uncertainty=("No runtime execution has established the integration.",),
    )

    assert item.uncertainty == (
        "No runtime execution has established the integration.",
    )


def test_uncertain_state_cannot_hide_uncertainty():
    with pytest.raises(
        LivingProjectImageError,
        match="must preserve its uncertainty",
    ):
        LivingProjectStatement(
            identifier="LPI-STMT-000003",
            title="Hidden uncertainty",
            statement="Uncertainty must remain visible.",
            epistemic_state="UNCERTAIN",
        )


def test_conflict_remains_visible():
    item = LivingProjectStatement(
        identifier="LPI-STMT-000004",
        title="Conflicting project state",
        statement="Available representations conflict.",
        epistemic_state="CONFLICTING",
        supports=(
            reference(
                "EV-000001",
                "First observation",
                "EVIDENCE",
                "evidence:first",
            ),
            reference(
                "EV-000002",
                "Second observation",
                "EVIDENCE",
                "evidence:second",
            ),
        ),
        conflicts=(
            "First observation reports state A.",
            "Second observation reports state B.",
        ),
    )

    assert len(item.conflicts) == 2


def test_conflicting_state_cannot_silently_erase_conflict():
    with pytest.raises(
        LivingProjectImageError,
        match="must preserve visible conflict",
    ):
        LivingProjectStatement(
            identifier="LPI-STMT-000004",
            title="Hidden conflict",
            statement="Conflict must remain visible.",
            epistemic_state="CONFLICTING",
        )


def test_statement_is_immutable():
    item = demonstrated()

    with pytest.raises(FrozenInstanceError):
        item.statement = "Rewrite current reality."


def test_support_reference_is_immutable():
    item = reference()

    with pytest.raises(FrozenInstanceError):
        item.reference = "rewritten"


def test_image_is_derived_read_only_and_non_authoritative():
    item = demonstrated()

    image = form_living_project_image(
        identifier="LPI-000001",
        title="AI-Toolkit Living Epistemic Image",
        statements=(item,),
    )

    assert image.derived is True
    assert image.authoritative is False

    with pytest.raises(FrozenInstanceError):
        image.title = "Rewritten image"


def test_identical_inputs_reconstruct_identical_image():
    first_statement = demonstrated()
    second_statement = demonstrated()

    first = form_living_project_image(
        identifier="LPI-000001",
        title="AI-Toolkit Living Epistemic Image",
        statements=(first_statement,),
    )

    second = form_living_project_image(
        identifier="LPI-000001",
        title="AI-Toolkit Living Epistemic Image",
        statements=(second_statement,),
    )

    assert first == second


def test_image_preserves_navigation_toward_supporting_reality():
    item = demonstrated()

    image = form_living_project_image(
        identifier="LPI-000001",
        title="AI-Toolkit Living Epistemic Image",
        statements=(item,),
    )

    recovered = image.statement("LPI-STMT-000001")

    assert recovered.supports[0].reference == (
        "tests/epistemic/test_provenance.py"
    )
    assert recovered.provenance_paths == (
        "Current State → Knowledge → Verification → Evidence → Source",
    )


def test_image_can_expose_non_answer_states_without_normalizing_them():
    unknown = LivingProjectStatement(
        identifier="LPI-STMT-000010",
        title="Unknown state",
        statement="State is unknown.",
        epistemic_state="UNKNOWN",
    )

    unconfirmed = LivingProjectStatement(
        identifier="LPI-STMT-000011",
        title="Unconfirmed state",
        statement="State is not confirmed.",
        epistemic_state="UNCONFIRMED",
    )

    image = form_living_project_image(
        identifier="LPI-000001",
        title="AI-Toolkit Living Epistemic Image",
        statements=(unknown, unconfirmed),
    )

    assert image.by_state("UNKNOWN") == (unknown,)
    assert image.by_state("UNCONFIRMED") == (unconfirmed,)


def test_duplicate_statement_identity_is_rejected():
    item = demonstrated()

    with pytest.raises(
        LivingProjectImageError,
        match="duplicate statement identities",
    ):
        form_living_project_image(
            identifier="LPI-000001",
            title="AI-Toolkit Living Epistemic Image",
            statements=(item, item),
        )


def test_invalid_statement_identity_is_rejected():
    with pytest.raises(
        LivingProjectImageError,
        match=r"LPI-STMT-\*",
    ):
        LivingProjectStatement(
            identifier="STATE-000001",
            title="Wrong identity family",
            statement="Invalid identity.",
            epistemic_state="UNKNOWN",
        )


def test_image_does_not_implement_progressive_recall():
    image = form_living_project_image(
        identifier="LPI-000001",
        title="AI-Toolkit Living Epistemic Image",
        statements=(demonstrated(),),
    )

    assert not hasattr(image, "recall")
    assert not hasattr(image, "progressive_recall")
    assert not hasattr(image, "retrieve_deeper_memory")
    assert not hasattr(image, "evaluate_epistemic_sufficiency")


def test_image_does_not_claim_canonical_or_source_organ_authority():
    image = form_living_project_image(
        identifier="LPI-000001",
        title="AI-Toolkit Living Epistemic Image",
        statements=(demonstrated(),),
    )

    assert not hasattr(image, "admit_canon")
    assert not hasattr(image, "modify_canon")
    assert not hasattr(image, "write_memory")
    assert not hasattr(image, "write_evidence")
    assert not hasattr(image, "write_current_state")


def test_forming_image_does_not_mutate_source_inputs():
    item = demonstrated()
    original_supports = item.supports
    original_paths = item.provenance_paths

    form_living_project_image(
        identifier="LPI-000001",
        title="AI-Toolkit Living Epistemic Image",
        statements=(item,),
    )

    assert item.supports == original_supports
    assert item.provenance_paths == original_paths

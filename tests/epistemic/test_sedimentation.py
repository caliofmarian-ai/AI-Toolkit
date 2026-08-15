from dataclasses import FrozenInstanceError

import pytest

from python.epistemic.sedimentation import (
    Sedimentation,
    SedimentationAuthority,
    SedimentationTarget,
)


def make_proposal(**changes):
    values = {
        "identifier": "SED-000001",
        "title": "Durable verified learning",
        "provenance_identifier": "VER-000001",
        "statement": (
            "Verified epistemic learning may be proposed for "
            "durable preservation."
        ),
        "target": SedimentationTarget.KNOWLEDGE,
    }
    values.update(changes)
    return Sedimentation(**values)


def test_sedimentation_has_machine_and_human_identity():
    item = make_proposal()

    assert item.identifier == "SED-000001"
    assert item.human_readable_identity == (
        "SED-000001 — Durable verified learning"
    )


def test_provenance_identity_is_mandatory():
    with pytest.raises(ValueError):
        make_proposal(provenance_identifier="")


def test_semantic_statement_is_mandatory():
    with pytest.raises(ValueError):
        make_proposal(statement="")


def test_target_must_be_explicit():
    with pytest.raises(TypeError):
        make_proposal(target="KNOWLEDGE")


def test_sedimentation_is_immutable():
    item = make_proposal()

    with pytest.raises(FrozenInstanceError):
        item.statement = "replacement"


def test_new_sedimentation_has_no_automatic_authority():
    item = make_proposal()

    assert item.authority is SedimentationAuthority.PROPOSED
    assert item.requires_human_authority is True
    assert item.is_accepted is False


def test_human_authority_may_accept():
    original = make_proposal()

    accepted = original.accept_by_human_authority()

    assert original.authority is SedimentationAuthority.PROPOSED
    assert accepted.authority is SedimentationAuthority.ACCEPTED
    assert accepted.is_accepted is True
    assert accepted.provenance_identifier == original.provenance_identifier
    assert accepted.statement == original.statement


def test_human_authority_may_reject_without_erasing_history():
    original = make_proposal()

    rejected = original.reject_by_human_authority()

    assert original.authority is SedimentationAuthority.PROPOSED
    assert rejected.authority is SedimentationAuthority.REJECTED
    assert rejected.is_rejected is True
    assert rejected.provenance_identifier == original.provenance_identifier
    assert rejected.statement == original.statement


def test_authority_transition_is_not_replayable():
    accepted = make_proposal().accept_by_human_authority()

    with pytest.raises(ValueError):
        accepted.accept_by_human_authority()

    with pytest.raises(ValueError):
        accepted.reject_by_human_authority()


def test_uncertainty_can_remain_explicit():
    item = make_proposal(
        uncertainty=(
            "Available evidence does not establish canonical status."
        )
    )

    assert item.uncertainty is not None


def test_empty_uncertainty_is_not_honest_uncertainty():
    with pytest.raises(ValueError):
        make_proposal(uncertainty="   ")


def test_acceptance_does_not_create_memory_or_knowledge():
    accepted = make_proposal().accept_by_human_authority()

    assert isinstance(accepted, Sedimentation)
    assert not hasattr(accepted, "memory")
    assert not hasattr(accepted, "knowledge")


def test_memory_and_knowledge_destinations_remain_distinct():
    memory = make_proposal(
        target=SedimentationTarget.MEMORY
    )
    knowledge = make_proposal(
        target=SedimentationTarget.KNOWLEDGE
    )
    both = make_proposal(
        target=SedimentationTarget.MEMORY_AND_KNOWLEDGE
    )

    assert memory.target is SedimentationTarget.MEMORY
    assert knowledge.target is SedimentationTarget.KNOWLEDGE
    assert both.target is SedimentationTarget.MEMORY_AND_KNOWLEDGE

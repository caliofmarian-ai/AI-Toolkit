from dataclasses import replace

import pytest

from epistemic.sedimentation import (
    GovernedSedimentation,
    Learning,
    Sedimentation,
    SedimentationAuthority,
    SedimentationGovernance,
    SedimentationTarget,
)
from epistemic.sedimented_memory import (
    DownstreamKnowledgeError,
    MemoryPromotionError,
    SedimentedMemory,
    SedimentedMemoryPhysiology,
    SedimentationDelivery,
)


def make_learning() -> Learning:
    return Learning(
        identifier="LEARN-006B",
        title="Durable semantic learning",
        verification_identifier="VER-006B",
        statement=(
            "The organism learned a durable semantic conclusion."
        ),
        uncertainty=(
            "Residual uncertainty remains explicit."
        ),
    )


def make_sedimentation(
    target: SedimentationTarget,
    authority: SedimentationAuthority = (
        SedimentationAuthority.ACCEPTED
    ),
) -> Sedimentation:
    learning = make_learning()

    return Sedimentation(
        identifier="SED-006B",
        title="Sedimented semantic conclusion",
        provenance_identifier=learning.identifier,
        statement=learning.statement,
        target=target,
        authority=authority,
        uncertainty=learning.uncertainty,
    )


def make_governed(
    target: SedimentationTarget,
    authority: SedimentationAuthority = (
        SedimentationAuthority.ACCEPTED
    ),
) -> GovernedSedimentation:
    return GovernedSedimentation(
        sedimentation=make_sedimentation(
            target,
            authority,
        ),
        governance=SedimentationGovernance.ROUTINE,
        reason=None,
    )


def test_memory_target_creates_semantic_memory_only():
    governed = make_governed(
        SedimentationTarget.MEMORY
    )

    result = SedimentedMemoryPhysiology().deliver(
        governed
    )

    assert result.delivery is SedimentationDelivery.MEMORY
    assert isinstance(result.memory, SedimentedMemory)
    assert result.knowledge is None


def test_memory_preserves_sedimentation_identity():
    governed = make_governed(
        SedimentationTarget.MEMORY
    )

    result = SedimentedMemoryPhysiology().deliver(
        governed
    )

    assert (
        result.memory.sedimentation_identifier
        == governed.sedimentation.identifier
    )


def test_memory_preserves_semantic_statement():
    governed = make_governed(
        SedimentationTarget.MEMORY
    )

    result = SedimentedMemoryPhysiology().deliver(
        governed
    )

    assert (
        result.memory.meaning
        == governed.sedimentation.statement
    )


def test_memory_preserves_provenance():
    governed = make_governed(
        SedimentationTarget.MEMORY
    )

    result = SedimentedMemoryPhysiology().deliver(
        governed
    )

    assert (
        result.memory.provenance_identifier
        == governed.sedimentation.provenance_identifier
    )


def test_memory_preserves_uncertainty():
    governed = make_governed(
        SedimentationTarget.MEMORY
    )

    result = SedimentedMemoryPhysiology().deliver(
        governed
    )

    assert (
        result.memory.uncertainty
        == governed.sedimentation.uncertainty
    )


def test_memory_identity_is_distinct_from_sedimentation_identity():
    governed = make_governed(
        SedimentationTarget.MEMORY
    )

    result = SedimentedMemoryPhysiology().deliver(
        governed
    )

    assert (
        str(result.memory.memory_id)
        != governed.sedimentation.identifier
    )


def test_repeated_memory_materialization_has_distinct_memory_identity():
    governed = make_governed(
        SedimentationTarget.MEMORY
    )

    physiology = SedimentedMemoryPhysiology()

    first = physiology.deliver(governed)
    second = physiology.deliver(governed)

    assert first.memory.memory_id != second.memory.memory_id

    assert (
        first.memory.sedimentation_identifier
        == second.memory.sedimentation_identifier
    )


@pytest.mark.parametrize(
    "authority",
    (
        SedimentationAuthority.PROPOSED,
        SedimentationAuthority.REJECTED,
    ),
)
def test_unaccepted_sedimentation_cannot_be_delivered(
    authority,
):
    governed = make_governed(
        SedimentationTarget.MEMORY,
        authority,
    )

    with pytest.raises(MemoryPromotionError):
        SedimentedMemoryPhysiology().deliver(
            governed
        )


def test_accepted_authority_is_read_from_sedimentation():
    governed = make_governed(
        SedimentationTarget.MEMORY,
        SedimentationAuthority.ACCEPTED,
    )

    assert (
        governed.sedimentation.authority
        is SedimentationAuthority.ACCEPTED
    )

    result = SedimentedMemoryPhysiology().deliver(
        governed
    )

    assert result.memory is not None


def test_knowledge_target_requires_existing_knowledge_receptor():
    governed = make_governed(
        SedimentationTarget.KNOWLEDGE
    )

    with pytest.raises(DownstreamKnowledgeError):
        SedimentedMemoryPhysiology().deliver(
            governed
        )


def test_knowledge_target_does_not_create_memory():
    governed = make_governed(
        SedimentationTarget.KNOWLEDGE
    )

    sentinel = object()

    result = SedimentedMemoryPhysiology(
        knowledge_receptor=lambda item: sentinel
    ).deliver(governed)

    assert result.delivery is SedimentationDelivery.KNOWLEDGE
    assert result.memory is None
    assert result.knowledge is sentinel


def test_memory_and_knowledge_remain_distinct():
    governed = make_governed(
        SedimentationTarget.MEMORY_AND_KNOWLEDGE
    )

    sentinel = object()

    result = SedimentedMemoryPhysiology(
        knowledge_receptor=lambda item: sentinel
    ).deliver(governed)

    assert (
        result.delivery
        is SedimentationDelivery.MEMORY_AND_KNOWLEDGE
    )

    assert isinstance(
        result.memory,
        SedimentedMemory,
    )

    assert result.knowledge is sentinel
    assert result.memory is not result.knowledge


def test_delivery_does_not_mutate_original_sedimentation():
    governed = make_governed(
        SedimentationTarget.MEMORY
    )

    original = governed.sedimentation

    SedimentedMemoryPhysiology().deliver(
        governed
    )

    assert governed.sedimentation == original


def test_memory_is_not_raw_experience():
    governed = make_governed(
        SedimentationTarget.MEMORY
    )

    memory = SedimentedMemoryPhysiology().deliver(
        governed
    ).memory

    assert not hasattr(memory, "conversation")
    assert not hasattr(memory, "terminal_output")
    assert not hasattr(memory, "raw_experience")


def test_memory_does_not_claim_verification_identity():
    governed = make_governed(
        SedimentationTarget.MEMORY
    )

    memory = SedimentedMemoryPhysiology().deliver(
        governed
    ).memory

    assert not hasattr(
        memory,
        "verification_identifier",
    )


def test_governance_and_authority_remain_distinct():
    governed = make_governed(
        SedimentationTarget.MEMORY
    )

    assert (
        governed.governance
        is SedimentationGovernance.ROUTINE
    )

    assert (
        governed.sedimentation.authority
        is SedimentationAuthority.ACCEPTED
    )


def test_rejected_sedimentation_remains_preserved_as_object():
    sedimentation = make_sedimentation(
        SedimentationTarget.MEMORY,
        SedimentationAuthority.REJECTED,
    )

    governed = GovernedSedimentation(
        sedimentation=sedimentation,
        governance=SedimentationGovernance.ROUTINE,
    )

    with pytest.raises(MemoryPromotionError):
        SedimentedMemoryPhysiology().deliver(
            governed
        )

    assert (
        governed.sedimentation
        == sedimentation
    )


def test_proposed_sedimentation_remains_preserved_as_object():
    sedimentation = make_sedimentation(
        SedimentationTarget.MEMORY,
        SedimentationAuthority.PROPOSED,
    )

    governed = GovernedSedimentation(
        sedimentation=sedimentation,
        governance=SedimentationGovernance.HUMAN_AUTHORITY,
        reason=(
            "Explicit Human Authority is required before retention."
        ),
    )

    with pytest.raises(MemoryPromotionError):
        SedimentedMemoryPhysiology().deliver(
            governed
        )

    assert (
        governed.sedimentation
        == sedimentation
    )


def test_missing_knowledge_receptor_does_not_create_parallel_knowledge():
    governed = make_governed(
        SedimentationTarget.KNOWLEDGE
    )

    physiology = SedimentedMemoryPhysiology()

    with pytest.raises(DownstreamKnowledgeError):
        physiology.deliver(governed)


def test_memory_and_knowledge_target_requires_real_knowledge_receptor():
    governed = make_governed(
        SedimentationTarget.MEMORY_AND_KNOWLEDGE
    )

    with pytest.raises(DownstreamKnowledgeError):
        SedimentedMemoryPhysiology().deliver(
            governed
        )

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
        learning_id="LEARN-006A",
        verification_identifier="VER-006A",
        meaning="The organism learned a durable semantic conclusion.",
        provenance_identifier="PROV-006A",
        uncertainty="Residual uncertainty remains explicit.",
    )


def make_governed(
    target: SedimentationTarget,
    authority: SedimentationAuthority = SedimentationAuthority.ACCEPTED,
) -> GovernedSedimentation:
    learning = make_learning()

    sedimentation = Sedimentation(
        sedimentation_id="SED-006A",
        learning_identifier=learning.learning_id,
        meaning=learning.meaning,
        target=target,
        provenance_identifier=learning.provenance_identifier,
        uncertainty=learning.uncertainty,
    )

    return GovernedSedimentation(
        sedimentation=sedimentation,
        governance=SedimentationGovernance.ROUTINE,
        authority=authority,
        reason="RUN 006A physiological examination.",
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
        == governed.sedimentation.sedimentation_id
    )


def test_memory_preserves_meaning():
    governed = make_governed(
        SedimentationTarget.MEMORY
    )

    result = SedimentedMemoryPhysiology().deliver(
        governed
    )

    assert (
        result.memory.meaning
        == governed.sedimentation.meaning
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


def test_memory_has_distinct_identity():
    governed = make_governed(
        SedimentationTarget.MEMORY
    )

    physiology = SedimentedMemoryPhysiology()

    first = physiology.deliver(governed)
    second = physiology.deliver(governed)

    assert first.memory.memory_id != second.memory.memory_id


@pytest.mark.parametrize(
    "authority",
    [
        SedimentationAuthority.PROPOSED,
        SedimentationAuthority.REJECTED,
    ],
)
def test_unaccepted_sedimentation_cannot_become_memory(
    authority,
):
    governed = make_governed(
        SedimentationTarget.MEMORY,
        authority=authority,
    )

    with pytest.raises(MemoryPromotionError):
        SedimentedMemoryPhysiology().deliver(
            governed
        )


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

    physiology = SedimentedMemoryPhysiology(
        knowledge_receptor=lambda item: sentinel
    )

    result = physiology.deliver(governed)

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
    assert isinstance(result.memory, SedimentedMemory)
    assert result.knowledge is sentinel
    assert result.memory is not result.knowledge


def test_memory_does_not_mutate_sedimentation():
    governed = make_governed(
        SedimentationTarget.MEMORY
    )

    before = governed.sedimentation

    SedimentedMemoryPhysiology().deliver(
        governed
    )

    assert governed.sedimentation == before


def test_memory_is_not_raw_experience():
    governed = make_governed(
        SedimentationTarget.MEMORY
    )

    result = SedimentedMemoryPhysiology().deliver(
        governed
    )

    assert not hasattr(
        result.memory,
        "conversation",
    )
    assert not hasattr(
        result.memory,
        "terminal_output",
    )
    assert not hasattr(
        result.memory,
        "raw_experience",
    )


def test_missing_provenance_is_rejected():
    governed = make_governed(
        SedimentationTarget.MEMORY
    )

    broken = replace(
        governed,
        sedimentation=replace(
            governed.sedimentation,
            provenance_identifier="",
        ),
    )

    with pytest.raises(
        (MemoryPromotionError, ValueError)
    ):
        SedimentedMemoryPhysiology().deliver(
            broken
        )

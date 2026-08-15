import pytest

from python.epistemic.layered_memory import (
    LayeredMemory,
    LayeredMemoryRelationshipError,
    LayeredMemoryTraversal,
    MemoryEpistemicOrigin,
    layered_memory_epistemic_origin,
    traversal_epistemic_origin,
)
from python.epistemic.sedimented_memory import (
    SedimentedMemory,
    SedimentedMemoryId,
)


def memory(
    name: str,
    *,
    uncertainty: str | None = None,
) -> SedimentedMemory:
    return SedimentedMemory(
        memory_id=SedimentedMemoryId(f"MEM-{name}"),
        sedimentation_identifier=f"SED-{name}",
        meaning=f"Meaning {name}",
        provenance_identifier=f"PROV-{name}",
        uncertainty=uncertainty,
    )


def chain():
    layered = LayeredMemory()

    root, middle, deep = layered.add_chain(
        (
            memory("ROOT"),
            memory(
                "MIDDLE",
                uncertainty="historical interpretation remains bounded",
            ),
            memory("DEEP"),
        )
    )

    return layered, root, middle, deep


def test_memory_origin_preserves_memory_identity():
    layered, root, _, _ = chain()

    origin = layered_memory_epistemic_origin(
        layered,
        root.node_id,
    )

    assert origin.memory_id == root.memory.memory_id


def test_memory_origin_preserves_sedimentation_identifier():
    layered, root, _, _ = chain()

    origin = layered_memory_epistemic_origin(
        layered,
        root.node_id,
    )

    assert origin.sedimentation_identifier == "SED-ROOT"


def test_memory_origin_preserves_deeper_provenance_identifier():
    layered, root, _, _ = chain()

    origin = layered_memory_epistemic_origin(
        layered,
        root.node_id,
    )

    assert origin.provenance_identifier == "PROV-ROOT"


def test_memory_origin_exposes_route_in_epistemic_order():
    layered, root, _, _ = chain()

    origin = layered_memory_epistemic_origin(
        layered,
        root.node_id,
    )

    assert origin.route == (
        "SED-ROOT",
        "PROV-ROOT",
    )


def test_memory_origin_preserves_uncertainty():
    layered, _, middle, _ = chain()

    origin = layered_memory_epistemic_origin(
        layered,
        middle.node_id,
    )

    assert origin.uncertainty == (
        "historical interpretation remains bounded"
    )


def test_memory_origin_does_not_invent_uncertainty():
    layered, root, _, _ = chain()

    origin = layered_memory_epistemic_origin(
        layered,
        root.node_id,
    )

    assert origin.uncertainty is None


def test_traversal_can_exit_from_current_memory():
    layered, root, middle, deep = chain()

    traversal = (
        LayeredMemoryTraversal.enter(
            layered,
            root.node_id,
        )
        .enter_deeper(middle.node_id)
        .enter_deeper(deep.node_id)
    )

    origin = traversal_epistemic_origin(traversal)

    assert origin.memory_id == deep.memory.memory_id
    assert origin.route == (
        "SED-DEEP",
        "PROV-DEEP",
    )


def test_returning_through_memory_changes_origin_to_current_position():
    layered, root, middle, deep = chain()

    traversal = (
        LayeredMemoryTraversal.enter(
            layered,
            root.node_id,
        )
        .enter_deeper(middle.node_id)
        .enter_deeper(deep.node_id)
        .return_toward_surface()
    )

    origin = traversal_epistemic_origin(traversal)

    assert origin.memory_id == middle.memory.memory_id
    assert origin.route == (
        "SED-MIDDLE",
        "PROV-MIDDLE",
    )


def test_origin_lookup_does_not_mutate_layered_memory():
    layered, root, _, _ = chain()

    before = layered.nodes()

    layered_memory_epistemic_origin(
        layered,
        root.node_id,
    )

    assert layered.nodes() == before


def test_origin_lookup_does_not_resolve_or_fabricate_historical_body():
    layered, root, _, _ = chain()

    origin = layered_memory_epistemic_origin(
        layered,
        root.node_id,
    )

    assert not hasattr(origin, "experience")
    assert not hasattr(origin, "evidence")
    assert not hasattr(origin, "transformation")
    assert not hasattr(origin, "knowledge")


def test_origin_does_not_claim_authority_or_truth():
    layered, root, _, _ = chain()

    origin = layered_memory_epistemic_origin(
        layered,
        root.node_id,
    )

    assert not hasattr(origin, "authority")
    assert not hasattr(origin, "truth")
    assert not hasattr(origin, "verified")


def test_origin_rejects_empty_sedimentation_identifier():
    with pytest.raises(
        LayeredMemoryRelationshipError,
        match="Sedimentation identifier cannot be empty",
    ):
        MemoryEpistemicOrigin(
            memory_id=SedimentedMemoryId("MEM-X"),
            sedimentation_identifier=" ",
            provenance_identifier="PROV-X",
        )


def test_origin_rejects_empty_provenance_identifier():
    with pytest.raises(
        LayeredMemoryRelationshipError,
        match="Provenance identifier cannot be empty",
    ):
        MemoryEpistemicOrigin(
            memory_id=SedimentedMemoryId("MEM-X"),
            sedimentation_identifier="SED-X",
            provenance_identifier=" ",
        )


def test_origin_rejects_empty_uncertainty():
    with pytest.raises(
        LayeredMemoryRelationshipError,
        match="uncertainty cannot be empty",
    ):
        MemoryEpistemicOrigin(
            memory_id=SedimentedMemoryId("MEM-X"),
            sedimentation_identifier="SED-X",
            provenance_identifier="PROV-X",
            uncertainty=" ",
        )

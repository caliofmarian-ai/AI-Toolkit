import pytest

from epistemic.layered_memory import (
    LayeredMemory,
    LayeredMemoryIdentityError,
    LayeredMemoryNavigationError,
    LayeredMemoryNodeId,
    LayeredMemoryRelationshipError,
)
from epistemic.sedimented_memory import (
    SedimentedMemory,
    SedimentedMemoryId,
)


def memory(
    name: str,
    *,
    provenance: str | None = None,
    uncertainty: str | None = None,
) -> SedimentedMemory:
    return SedimentedMemory(
        memory_id=SedimentedMemoryId(f"MEM-{name}"),
        sedimentation_identifier=f"SED-{name}",
        meaning=f"Meaning {name}",
        provenance_identifier=provenance or f"PROV-{name}",
        uncertainty=uncertainty,
    )


def test_root_is_structural_surface():
    layered = LayeredMemory()
    root = layered.add_root(memory("ROOT"))

    assert root.depth == 0
    assert root.parent_ids == ()
    assert layered.get(root.node_id) == root


def test_child_is_one_structural_depth_deeper():
    layered = LayeredMemory()
    root = layered.add_root(memory("ROOT"))
    child = layered.add_child(root.node_id, memory("CHILD"))

    assert child.depth == 1
    assert child.parent_ids == (root.node_id,)


def test_parent_knows_child_bidirectionally():
    layered = LayeredMemory()
    root = layered.add_root(memory("ROOT"))
    child = layered.add_child(root.node_id, memory("CHILD"))

    assert layered.children(root.node_id) == (child,)
    assert layered.parents(child.node_id)[0].node_id == root.node_id


def test_can_travel_from_depth_back_to_surface():
    layered = LayeredMemory()
    root, middle, deep = layered.add_chain(
        (memory("ROOT"), memory("MID"), memory("DEEP"))
    )

    path = layered.toward_surface(deep.node_id)

    assert path.node_ids == (
        deep.node_id,
        middle.node_id,
        root.node_id,
    )


def test_can_travel_from_surface_toward_depth():
    layered = LayeredMemory()
    root, middle, deep = layered.add_chain(
        (memory("ROOT"), memory("MID"), memory("DEEP"))
    )

    descendants = layered.toward_depth(root.node_id)

    assert tuple(node.node_id for node in descendants) == (
        middle.node_id,
        deep.node_id,
    )


def test_depth_can_be_inspected_without_loading_other_depths():
    layered = LayeredMemory()
    root, middle, deep = layered.add_chain(
        (memory("ROOT"), memory("MID"), memory("DEEP"))
    )

    assert tuple(
        node.node_id for node in layered.memories_at_depth(0)
    ) == (root.node_id,)

    assert tuple(
        node.node_id for node in layered.memories_at_depth(1)
    ) == (middle.node_id,)

    assert tuple(
        node.node_id for node in layered.memories_at_depth(2)
    ) == (deep.node_id,)


def test_layer_wraps_real_sedimented_memory_without_rewriting_it():
    original = memory(
        "ORIGINAL",
        provenance="PROV-ORIGINAL",
        uncertainty="Uncertainty remains explicit.",
    )

    layered = LayeredMemory()
    node = layered.add_root(original)

    assert node.memory is original
    assert node.memory.meaning == "Meaning ORIGINAL"
    assert node.memory.uncertainty == "Uncertainty remains explicit."


def test_provenance_route_preserves_pcc04_exit_from_memory():
    layered = LayeredMemory()
    node = layered.add_root(
        memory("A", provenance="PROV-A")
    )

    assert layered.provenance_route(node.node_id) == (
        "SED-A",
        "PROV-A",
    )


def test_layered_memory_does_not_copy_raw_experience():
    layered = LayeredMemory()
    node = layered.add_root(memory("A"))

    assert not hasattr(node, "raw_experience")
    assert not hasattr(node, "conversation")
    assert not hasattr(node, "terminal_output")


def test_layered_memory_does_not_claim_evidence_identity():
    layered = LayeredMemory()
    node = layered.add_root(memory("A"))

    assert not hasattr(node, "evidence")
    assert not hasattr(node, "evidence_identifier")


def test_layered_memory_does_not_claim_csl():
    layered = LayeredMemory()
    node = layered.add_root(memory("A"))

    assert not hasattr(node, "current_state")
    assert not hasattr(node, "living_project_image")
    assert not hasattr(node, "csl")


def test_layered_memory_does_not_claim_progressive_recall():
    layered = LayeredMemory()

    assert not hasattr(layered, "progressive_recall")
    assert not hasattr(layered, "context_package")


def test_structural_depth_does_not_create_authority():
    layered = LayeredMemory()
    root, deep = layered.add_chain(
        (memory("ROOT"), memory("DEEP"))
    )

    assert not hasattr(root, "authority")
    assert not hasattr(deep, "authority")
    assert deep.depth > root.depth


def test_duplicate_node_identity_is_rejected():
    layered = LayeredMemory()
    identifier = LayeredMemoryNodeId("LMEM-fixed")

    layered.add_root(memory("A"), node_id=identifier)

    with pytest.raises(LayeredMemoryIdentityError):
        layered.add_root(memory("B"), node_id=identifier)


def test_unknown_parent_is_rejected():
    layered = LayeredMemory()

    with pytest.raises(LayeredMemoryNavigationError):
        layered.add_child(
            LayeredMemoryNodeId("LMEM-missing"),
            memory("A"),
        )


def test_empty_chain_is_rejected():
    layered = LayeredMemory()

    with pytest.raises(LayeredMemoryRelationshipError):
        layered.add_chain(())


def test_negative_depth_query_is_rejected():
    layered = LayeredMemory()

    with pytest.raises(LayeredMemoryNavigationError):
        layered.memories_at_depth(-1)


def test_memory_identity_remains_distinct_from_layer_identity():
    original = memory("A")
    layered = LayeredMemory()
    node = layered.add_root(original)

    assert str(node.node_id) != str(original.memory_id)


def test_multiple_children_preserve_navigation():
    layered = LayeredMemory()
    root = layered.add_root(memory("ROOT"))
    first = layered.add_child(root.node_id, memory("A"))
    second = layered.add_child(root.node_id, memory("B"))

    children = layered.children(root.node_id)

    assert tuple(node.node_id for node in children) == (
        first.node_id,
        second.node_id,
    )


def test_each_branch_can_navigate_back_to_same_surface():
    layered = LayeredMemory()
    root = layered.add_root(memory("ROOT"))
    first = layered.add_child(root.node_id, memory("A"))
    second = layered.add_child(root.node_id, memory("B"))

    assert layered.toward_surface(first.node_id).node_ids[-1] == root.node_id
    assert layered.toward_surface(second.node_id).node_ids[-1] == root.node_id


def test_deeper_memory_does_not_destroy_shallower_memory():
    layered = LayeredMemory()
    root, middle, deep = layered.add_chain(
        (memory("ROOT"), memory("MID"), memory("DEEP"))
    )

    assert layered.get(root.node_id).memory.meaning == "Meaning ROOT"
    assert layered.get(middle.node_id).memory.meaning == "Meaning MID"
    assert layered.get(deep.node_id).memory.meaning == "Meaning DEEP"

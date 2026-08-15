import pytest

from python.epistemic.layered_memory import (
    LayeredMemory,
    LayeredMemoryNavigationError,
    LayeredMemoryTraversal,
)
from python.epistemic.sedimented_memory import (
    SedimentedMemory,
    SedimentedMemoryId,
)


def memory(name: str) -> SedimentedMemory:
    return SedimentedMemory(
        memory_id=SedimentedMemoryId(f"MEM-{name}"),
        sedimentation_identifier=f"SED-{name}",
        meaning=f"Meaning {name}",
        provenance_identifier=f"PROV-{name}",
        uncertainty=None,
    )


def chain():
    layered = LayeredMemory()
    root, middle, deep = layered.add_chain(
        (
            memory("ROOT"),
            memory("MIDDLE"),
            memory("DEEP"),
        )
    )
    return layered, root, middle, deep


def test_traversal_enters_existing_memory():
    layered, root, _, _ = chain()

    traversal = LayeredMemoryTraversal.enter(
        layered,
        root.node_id,
    )

    assert traversal.current.node_id == root.node_id
    assert traversal.entry.node_id == root.node_id
    assert traversal.travelled_path.node_ids == (root.node_id,)


def test_traversal_exposes_deeper_options_without_selecting():
    layered, root, middle, _ = chain()

    traversal = LayeredMemoryTraversal.enter(
        layered,
        root.node_id,
    )

    assert tuple(
        node.node_id
        for node in traversal.deeper_options()
    ) == (middle.node_id,)

    assert traversal.current.node_id == root.node_id


def test_traversal_can_enter_one_layer_deeper():
    layered, root, middle, _ = chain()

    traversal = LayeredMemoryTraversal.enter(
        layered,
        root.node_id,
    ).enter_deeper(middle.node_id)

    assert traversal.current.node_id == middle.node_id
    assert traversal.travelled_path.node_ids == (
        root.node_id,
        middle.node_id,
    )


def test_traversal_can_enter_multiple_layers_deeper():
    layered, root, middle, deep = chain()

    traversal = (
        LayeredMemoryTraversal.enter(
            layered,
            root.node_id,
        )
        .enter_deeper(middle.node_id)
        .enter_deeper(deep.node_id)
    )

    assert traversal.current.node_id == deep.node_id
    assert traversal.travelled_path.node_ids == (
        root.node_id,
        middle.node_id,
        deep.node_id,
    )


def test_traversal_returns_exactly_along_travelled_route():
    layered, root, middle, deep = chain()

    deep_position = (
        LayeredMemoryTraversal.enter(
            layered,
            root.node_id,
        )
        .enter_deeper(middle.node_id)
        .enter_deeper(deep.node_id)
    )

    middle_position = deep_position.return_toward_surface()
    root_position = middle_position.return_toward_surface()

    assert middle_position.current.node_id == middle.node_id
    assert root_position.current.node_id == root.node_id
    assert root_position.can_return() is False


def test_traversal_can_return_directly_to_entry():
    layered, root, middle, deep = chain()

    traversal = (
        LayeredMemoryTraversal.enter(
            layered,
            root.node_id,
        )
        .enter_deeper(middle.node_id)
        .enter_deeper(deep.node_id)
        .return_to_entry()
    )

    assert traversal.current.node_id == root.node_id
    assert traversal.travelled_path.node_ids == (root.node_id,)


def test_traversal_can_begin_below_surface():
    layered, _, middle, deep = chain()

    traversal = (
        LayeredMemoryTraversal.enter(
            layered,
            middle.node_id,
        )
        .enter_deeper(deep.node_id)
    )

    assert traversal.entry.node_id == middle.node_id
    assert traversal.current.node_id == deep.node_id

    returned = traversal.return_to_entry()

    assert returned.current.node_id == middle.node_id


def test_traversal_refuses_non_child_jump():
    layered, root, _, deep = chain()

    traversal = LayeredMemoryTraversal.enter(
        layered,
        root.node_id,
    )

    with pytest.raises(
        LayeredMemoryNavigationError,
        match="not an immediate deeper position",
    ):
        traversal.enter_deeper(deep.node_id)


def test_traversal_refuses_return_before_it_has_travelled():
    layered, root, _, _ = chain()

    traversal = LayeredMemoryTraversal.enter(
        layered,
        root.node_id,
    )

    with pytest.raises(
        LayeredMemoryNavigationError,
        match="already at its entry position",
    ):
        traversal.return_toward_surface()


def test_traversal_preserves_current_provenance_exit():
    layered, root, middle, _ = chain()

    traversal = LayeredMemoryTraversal.enter(
        layered,
        root.node_id,
    ).enter_deeper(middle.node_id)

    assert traversal.provenance_route() == (
        "SED-MIDDLE",
        "PROV-MIDDLE",
    )


def test_traversal_does_not_mutate_layered_memory():
    layered, root, middle, deep = chain()
    before = layered.nodes()

    (
        LayeredMemoryTraversal.enter(
            layered,
            root.node_id,
        )
        .enter_deeper(middle.node_id)
        .enter_deeper(deep.node_id)
        .return_toward_surface()
        .return_to_entry()
    )

    assert layered.nodes() == before


def test_traversal_does_not_claim_progressive_recall():
    assert not hasattr(
        LayeredMemoryTraversal,
        "recall",
    )
    assert not hasattr(
        LayeredMemoryTraversal,
        "select_relevant",
    )
    assert not hasattr(
        LayeredMemoryTraversal,
        "build_context",
    )

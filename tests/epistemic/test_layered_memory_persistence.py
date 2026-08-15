import json

import pytest

from epistemic.layered_memory import (
    LayeredMemory,
    LayeredMemoryPersistenceError,
    LayeredMemoryRepository,
)
from epistemic.sedimented_memory import (
    SedimentedMemory,
    SedimentedMemoryId,
)


def memory(name, *, uncertainty=None):
    return SedimentedMemory(
        memory_id=SedimentedMemoryId(f"MEM-{name}"),
        sedimentation_identifier=f"SED-{name}",
        meaning=f"Meaning {name}",
        provenance_identifier=f"PROV-{name}",
        uncertainty=uncertainty,
    )


def organism():
    layered = LayeredMemory()
    return layered, layered.add_chain(
        (
            memory("SURFACE"),
            memory("MIDDLE"),
            memory(
                "DEEP",
                uncertainty="Uncertainty survives.",
            ),
        )
    )


def test_repository_survives_process_boundary(tmp_path):
    layered, created = organism()

    LayeredMemoryRepository(layered).save(tmp_path)

    restored = LayeredMemoryRepository.load(
        tmp_path
    ).layered_memory

    assert len(restored) == 3

    for original in created:
        recovered = restored.get(original.node_id)
        assert recovered.node_id == original.node_id
        assert recovered.memory.memory_id == original.memory.memory_id


def test_structural_depth_survives_reconstruction(tmp_path):
    layered, (surface, middle, deep) = organism()

    LayeredMemoryRepository(layered).save(tmp_path)
    restored = LayeredMemoryRepository.load(
        tmp_path
    ).layered_memory

    assert restored.get(surface.node_id).depth == 0
    assert restored.get(middle.node_id).depth == 1
    assert restored.get(deep.node_id).depth == 2


def test_navigation_back_toward_surface_survives(tmp_path):
    layered, (surface, middle, deep) = organism()

    LayeredMemoryRepository(layered).save(tmp_path)
    restored = LayeredMemoryRepository.load(
        tmp_path
    ).layered_memory

    assert restored.toward_surface(deep.node_id).node_ids == (
        deep.node_id,
        middle.node_id,
        surface.node_id,
    )


def test_navigation_toward_depth_survives(tmp_path):
    layered, (surface, middle, deep) = organism()

    LayeredMemoryRepository(layered).save(tmp_path)
    restored = LayeredMemoryRepository.load(
        tmp_path
    ).layered_memory

    assert tuple(
        node.node_id
        for node in restored.toward_depth(surface.node_id)
    ) == (
        middle.node_id,
        deep.node_id,
    )


def test_provenance_exit_survives(tmp_path):
    layered, (_, _, deep) = organism()

    LayeredMemoryRepository(layered).save(tmp_path)
    restored = LayeredMemoryRepository.load(
        tmp_path
    ).layered_memory

    assert restored.provenance_route(deep.node_id) == (
        "SED-DEEP",
        "PROV-DEEP",
    )


def test_uncertainty_survives(tmp_path):
    layered, (_, _, deep) = organism()

    LayeredMemoryRepository(layered).save(tmp_path)
    restored = LayeredMemoryRepository.load(
        tmp_path
    ).layered_memory

    assert (
        restored.get(deep.node_id).memory.uncertainty
        == "Uncertainty survives."
    )


def test_schema_is_explicit(tmp_path):
    layered, _ = organism()

    path = LayeredMemoryRepository(layered).save(tmp_path)
    payload = json.loads(path.read_text(encoding="utf-8"))

    assert payload["schema"] == "PCC-05-LAYERED-MEMORY-1"


def test_unknown_schema_fails_safely(tmp_path):
    path = tmp_path / "layered_memory.json"
    path.write_text(
        json.dumps({
            "schema": "UNKNOWN",
            "nodes": [],
        }),
        encoding="utf-8",
    )

    with pytest.raises(LayeredMemoryPersistenceError):
        LayeredMemoryRepository.load(tmp_path)


def test_corrupt_json_fails_safely(tmp_path):
    path = tmp_path / "layered_memory.json"
    path.write_text("{broken", encoding="utf-8")

    with pytest.raises(LayeredMemoryPersistenceError):
        LayeredMemoryRepository.load(tmp_path)


def test_missing_repository_reconstructs_empty_memory(tmp_path):
    restored = LayeredMemoryRepository.load(
        tmp_path
    ).layered_memory

    assert len(restored) == 0


def test_missing_parent_is_rejected(tmp_path):
    layered, _ = organism()
    path = LayeredMemoryRepository(layered).save(tmp_path)

    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["nodes"][1]["parent_ids"] = ["LMEM-MISSING"]

    path.write_text(
        json.dumps(payload),
        encoding="utf-8",
    )

    with pytest.raises(LayeredMemoryPersistenceError):
        LayeredMemoryRepository.load(tmp_path)


def test_nonreciprocal_relationship_is_rejected(tmp_path):
    layered, _ = organism()
    path = LayeredMemoryRepository(layered).save(tmp_path)

    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["nodes"][0]["child_ids"] = []

    path.write_text(
        json.dumps(payload),
        encoding="utf-8",
    )

    with pytest.raises(LayeredMemoryPersistenceError):
        LayeredMemoryRepository.load(tmp_path)


def test_invalid_depth_is_rejected(tmp_path):
    layered, _ = organism()
    path = LayeredMemoryRepository(layered).save(tmp_path)

    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["nodes"][2]["depth"] = 7

    path.write_text(
        json.dumps(payload),
        encoding="utf-8",
    )

    with pytest.raises(LayeredMemoryPersistenceError):
        LayeredMemoryRepository.load(tmp_path)


def test_memory_semantics_are_not_replaced_by_recipient(tmp_path):
    layered, (_, _, deep) = organism()

    original = layered.get(deep.node_id).memory

    LayeredMemoryRepository(layered).save(tmp_path)
    restored = LayeredMemoryRepository.load(
        tmp_path
    ).layered_memory

    recovered = restored.get(deep.node_id).memory

    assert recovered == original
    assert recovered.meaning == original.meaning
    assert recovered.provenance_identifier == original.provenance_identifier


def test_repository_does_not_claim_experience_or_evidence(tmp_path):
    layered, _ = organism()
    repository = LayeredMemoryRepository(layered)

    assert not hasattr(repository, "experience")
    assert not hasattr(repository, "evidence")
    assert not hasattr(repository, "progressive_recall")
    assert not hasattr(repository, "csl")

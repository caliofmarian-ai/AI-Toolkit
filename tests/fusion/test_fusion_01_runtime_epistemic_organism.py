from __future__ import annotations

import json

from python.dashboard.service import EngineeringDashboardService
from python.epistemic.layered_memory import LayeredMemoryRepository
from python.epistemic.provenance import Provenance
from python.epistemic.sedimentation import (
    Sedimentation,
    SedimentationAuthority,
    SedimentationRepository,
    SedimentationTarget,
)
from python.experience.persistent_repository import (
    JsonFileExperienceRepository,
)
from python.runtime.bootstrap import RuntimeBootstrap
from python.runtime.interfaces.http_server import RuntimeHttpServer
from python.runtime.organism import EpistemicOrganismAccess


def test_boundary_reuses_existing_physiology_and_serializes(tmp_path):
    boundary = EpistemicOrganismAccess(tmp_path)

    assert (
        boundary.persistent_experience_repository_class
        is JsonFileExperienceRepository
    )
    assert (
        boundary.layered_memory_repository_class
        is LayeredMemoryRepository
    )
    assert (
        boundary.sedimentation_repository_class
        is SedimentationRepository
    )
    assert boundary.provenance_class is Provenance

    state = boundary.state()
    json.dumps(state)

    assert state["boundary"]["second_runtime"] is False
    assert state["boundary"]["second_server"] is False
    assert state["boundary"]["second_dashboard"] is False
    assert (
        state["boundary"]["second_memory_architecture"]
        is False
    )

    assert (
        state["persistent_experience"]["runtime_reachable"]
        is True
    )
    assert (
        state["persistent_experience"]["storage_state"]
        == "UNKNOWN"
    )

    assert state["layered_memory"]["runtime_reachable"] is True
    assert state["sedimentation"]["runtime_reachable"] is True
    assert state["provenance"]["runtime_reachable"] is True

    assert state["human_authority"]["preserved"] is True
    assert (
        state["human_authority"]["runtime_may_mutate_canon"]
        is False
    )
    assert (
        state["migration_boundaries"]["pcc_06"]
        == "SUSPENDED_FOR_MIGRATION"
    )


def test_human_authority_is_not_bypassed(tmp_path):
    memory_root = tmp_path / "work" / "memory"
    repo = SedimentationRepository()

    proposal = Sedimentation(
        identifier="SED-FUSION-01",
        title="Authority boundary proof",
        provenance_identifier="PROV-FUSION-01",
        statement=(
            "Runtime observation must not create Human Authority."
        ),
        target=SedimentationTarget.MEMORY,
    )

    assert proposal.authority is SedimentationAuthority.PROPOSED
    assert proposal.requires_human_authority is True

    repo.register(proposal)
    repo.save(memory_root)

    boundary = EpistemicOrganismAccess(tmp_path)
    state = boundary.state()

    assert (
        state["sedimentation"]["authority_counts"]["PROPOSED"]
        == 1
    )
    assert (
        state["sedimentation"]["authority_counts"]["ACCEPTED"]
        == 0
    )

    reconstructed = SedimentationRepository.load(memory_root)
    recovered = reconstructed.get("SED-FUSION-01")

    assert recovered.authority is SedimentationAuthority.PROPOSED
    assert recovered.requires_human_authority is True


def test_restart_reconstruction_reuses_layered_memory(tmp_path):
    memory_root = tmp_path / "work" / "memory"

    first_process = LayeredMemoryRepository()
    first_process.save(memory_root)

    second_process = LayeredMemoryRepository.load(memory_root)

    assert type(second_process) is LayeredMemoryRepository
    assert second_process.layered_memory.nodes() == ()

    state = EpistemicOrganismAccess(tmp_path).state()

    assert state["layered_memory"]["state"] == "AVAILABLE"
    assert (
        state["layered_memory"]["persistent_body_exists"]
        is True
    )
    assert state["layered_memory"]["node_count"] == 0


def test_bootstrap_can_hold_single_organism_boundary():
    runtime = RuntimeBootstrap()

    assert runtime.organism is None

    runtime.organism = EpistemicOrganismAccess(
        runtime.repository_root
    )

    assert isinstance(runtime.organism, EpistemicOrganismAccess)


def test_existing_http_api_can_expose_organism_state(tmp_path):
    boundary = EpistemicOrganismAccess(tmp_path)

    server = RuntimeHttpServer(
        host="127.0.0.1",
        port=19091,
    )

    server.set_status_handler(
        lambda: {
            "runtime": {"state": "READY"},
            "organism": boundary.state(),
        }
    )

    payload = server.api.status()

    assert (
        payload["organism"]["schema"]
        == "FUSION-01-EPISTEMIC-ORGANISM-STATE-1"
    )


def test_existing_dashboard_receives_same_boundary(tmp_path):
    boundary = EpistemicOrganismAccess(tmp_path)

    dashboard = EngineeringDashboardService(
        repository_root=str(tmp_path),
        workspace_root=str(tmp_path.parent),
        organism_service=boundary,
    )

    assert dashboard.organism_service is boundary
    assert (
        dashboard.organism_service.state()["human_authority"][
            "preserved"
        ]
        is True
    )


def test_import_topology_remains_functional():
    from python.epistemic.layered_memory import (
        LayeredMemoryRepository as LayeredImport,
    )
    from python.epistemic.sedimentation import (
        SedimentationRepository as SedimentationImport,
    )

    assert LayeredImport is LayeredMemoryRepository
    assert SedimentationImport is SedimentationRepository

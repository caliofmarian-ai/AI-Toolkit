import json

from python.runtime.owner_access import OwnerAccessBoundary
from python.runtime.organism import EpistemicOrganismAccess


def test_owner_boundary_fails_closed_without_configuration():
    boundary = OwnerAccessBoundary(token="")
    decision = boundary.authenticate({})
    assert decision.authenticated is False
    assert decision.human_authority is False
    assert decision.role == "NONE"


def test_url_knowledge_is_not_authority():
    boundary = OwnerAccessBoundary(token="owner-secret")
    decision = boundary.authenticate({})
    assert decision.authenticated is False
    assert decision.reason == "OWNER_CREDENTIAL_REQUIRED"


def test_wrong_owner_credential_is_rejected():
    boundary = OwnerAccessBoundary(token="owner-secret")
    decision = boundary.authenticate(
        {"Authorization": "Bearer attacker"}
    )
    assert decision.authenticated is False
    assert decision.human_authority is False


def test_authenticated_owner_crosses_boundary():
    boundary = OwnerAccessBoundary(token="owner-secret")
    decision = boundary.authenticate(
        {"Authorization": "Bearer owner-secret"}
    )
    assert decision.authenticated is True
    assert decision.role == "OWNER"
    assert decision.human_authority is True


def test_public_state_has_no_external_privileges():
    state = OwnerAccessBoundary(token="owner-secret").public_state()
    assert state["mode"] == "PRIVATE_SINGLE_OWNER"
    assert state["public_operational_access"] is False
    assert state["multi_user"] is False
    assert state["external_repository_access"] is False
    assert state["partner_portal"] is False


def test_organism_preserves_human_authority_and_owner_posture(tmp_path):
    organism = EpistemicOrganismAccess(tmp_path)
    state = organism.state()
    json.dumps(state)

    assert state["human_authority"]["preserved"] is True
    assert state["human_authority"]["runtime_may_mutate_canon"] is False
    assert state["owner_access"]["mode"] == "PRIVATE_SINGLE_OWNER"
    assert state["owner_access"]["public_operational_access"] is False
    assert (
        state["migration_boundaries"]["pcc_06"]
        == "SUSPENDED_FOR_MIGRATION"
    )

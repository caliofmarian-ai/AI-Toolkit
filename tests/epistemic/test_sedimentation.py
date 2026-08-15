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


# ---------------------------------------------------------------------------
# PCC-04 RUN 002 — persistence + reconstruction
# ---------------------------------------------------------------------------

from python.epistemic.sedimentation import (
    SedimentationPersistenceError,
    SedimentationRepository,
)


def test_repository_preserves_sedimentation_identity():
    repository = SedimentationRepository()
    item = make_proposal()

    repository.register(item)

    assert repository.get(item.identifier) is item


def test_repository_rejects_identity_collision():
    repository = SedimentationRepository()

    repository.register(make_proposal())

    with pytest.raises(ValueError):
        repository.register(
            make_proposal(
                statement="Different meaning under same identity."
            )
        )


def test_repository_navigates_from_provenance_to_sedimentation():
    repository = SedimentationRepository()

    first = make_proposal(identifier="SED-000001")
    second = make_proposal(
        identifier="SED-000002",
        title="Second interpretation",
    )
    unrelated = make_proposal(
        identifier="SED-000003",
        provenance_identifier="VER-OTHER",
    )

    repository.register(first)
    repository.register(second)
    repository.register(unrelated)

    assert repository.by_provenance(
        "VER-000001"
    ) == (first, second)


def test_repository_does_not_infer_unknown_provenance():
    repository = SedimentationRepository()
    repository.register(make_proposal())

    assert repository.by_provenance("VER-UNKNOWN") == ()


def test_persistence_reconstructs_proposed_sedimentation(tmp_path):
    repository = SedimentationRepository()
    original = make_proposal()

    repository.register(original)
    repository.save(tmp_path)

    recovered = SedimentationRepository.load(tmp_path)
    item = recovered.get(original.identifier)

    assert item == original
    assert item.authority is SedimentationAuthority.PROPOSED
    assert item.provenance_identifier == original.provenance_identifier


def test_persistence_reconstructs_accepted_authority(tmp_path):
    repository = SedimentationRepository()
    accepted = make_proposal().accept_by_human_authority()

    repository.register(accepted)
    repository.save(tmp_path)

    recovered = SedimentationRepository.load(tmp_path)
    item = recovered.get(accepted.identifier)

    assert item == accepted
    assert item.authority is SedimentationAuthority.ACCEPTED
    assert item.is_accepted is True


def test_persistence_reconstructs_rejected_authority(tmp_path):
    repository = SedimentationRepository()
    rejected = make_proposal().reject_by_human_authority()

    repository.register(rejected)
    repository.save(tmp_path)

    recovered = SedimentationRepository.load(tmp_path)
    item = recovered.get(rejected.identifier)

    assert item == rejected
    assert item.authority is SedimentationAuthority.REJECTED
    assert item.is_rejected is True


def test_persistence_preserves_uncertainty(tmp_path):
    repository = SedimentationRepository()

    original = make_proposal(
        uncertainty="Evidence remains incomplete."
    )

    repository.register(original)
    repository.save(tmp_path)

    recovered = SedimentationRepository.load(tmp_path)

    assert (
        recovered.get(original.identifier).uncertainty
        == "Evidence remains incomplete."
    )


def test_restart_preserves_provenance_navigation(tmp_path):
    repository = SedimentationRepository()

    first = make_proposal(identifier="SED-000001")
    second = make_proposal(
        identifier="SED-000002",
        title="Second interpretation",
    )

    repository.register(first)
    repository.register(second)
    repository.save(tmp_path)

    recovered = SedimentationRepository.load(tmp_path)

    result = recovered.by_provenance("VER-000001")

    assert tuple(x.identifier for x in result) == (
        "SED-000001",
        "SED-000002",
    )


def test_missing_repository_reconstructs_as_empty(tmp_path):
    recovered = SedimentationRepository.load(tmp_path)

    assert recovered.all() == ()


def test_corrupt_persistence_is_not_silently_invented(tmp_path):
    path = tmp_path / "sedimentation.json"
    path.write_text("{broken", encoding="utf-8")

    with pytest.raises(SedimentationPersistenceError):
        SedimentationRepository.load(tmp_path)


def test_unknown_schema_is_explicitly_rejected(tmp_path):
    path = tmp_path / "sedimentation.json"
    path.write_text(
        '{"schema":"UNKNOWN","sedimentations":[]}\n',
        encoding="utf-8",
    )

    with pytest.raises(SedimentationPersistenceError):
        SedimentationRepository.load(tmp_path)


def test_repository_does_not_create_memory_or_knowledge(tmp_path):
    repository = SedimentationRepository()
    accepted = make_proposal().accept_by_human_authority()

    repository.register(accepted)
    repository.save(tmp_path)

    recovered = SedimentationRepository.load(tmp_path)

    assert recovered.get(accepted.identifier).is_accepted
    assert not hasattr(recovered, "memory")
    assert not hasattr(recovered, "knowledge")
    assert not hasattr(recovered, "current_state")
    assert not hasattr(recovered, "living_project_image")


# ---------------------------------------------------------------------------
# PCC-04 RUN 003 — Verification -> Learning -> Sedimentation
# ---------------------------------------------------------------------------

from python.epistemic.provenance import Provenance

from python.epistemic.sedimentation import (
    Learning,
    LearningSedimentationError,
    LearningSedimentationPhysiology,
)


def make_verified_learning_source():
    provenance = Provenance()

    claim = provenance.make_claim(
        "Learning source",
        "The examined condition has demonstrable meaning.",
    )

    verification = provenance.verify(
        claim,
        "Learning verification",
        state="VERIFIED",
        basis="Explicit evidence examination",
    )

    return verification


def test_learning_requires_verification():
    verification = make_verified_learning_source()

    physiology = LearningSedimentationPhysiology(
        SedimentationRepository()
    )

    learning = physiology.learn(
        verification,
        identifier="LRN-000001",
        title="Verified learning",
        statement="The verified condition produced learning.",
    )

    assert learning.verification_identifier == verification.identifier


def test_learning_is_not_memory_knowledge_or_canon():
    verification = make_verified_learning_source()

    physiology = LearningSedimentationPhysiology(
        SedimentationRepository()
    )

    learning = physiology.learn(
        verification,
        identifier="LRN-000001",
        title="Provisional learning",
        statement="This meaning remains pre-sedimentation.",
    )

    assert isinstance(learning, Learning)
    assert not hasattr(learning, "memory")
    assert not hasattr(learning, "knowledge")
    assert not hasattr(learning, "canon")


def test_learning_can_propose_sedimentation():
    verification = make_verified_learning_source()
    repository = SedimentationRepository()

    physiology = LearningSedimentationPhysiology(repository)

    learning = physiology.learn(
        verification,
        identifier="LRN-000001",
        title="Learning candidate",
        statement="Repeated verified behavior should be retained.",
    )

    sedimentation = physiology.propose_sedimentation(
        learning,
        identifier="SED-000101",
        title="Sedimentation candidate",
        target=SedimentationTarget.MEMORY,
    )

    assert sedimentation.provenance_identifier == learning.identifier
    assert sedimentation.statement == learning.statement
    assert sedimentation.authority is SedimentationAuthority.PROPOSED


def test_sedimentation_does_not_automatically_become_memory():
    verification = make_verified_learning_source()
    repository = SedimentationRepository()

    physiology = LearningSedimentationPhysiology(repository)

    learning = physiology.learn(
        verification,
        identifier="LRN-000001",
        title="Learning candidate",
        statement="Learning may deserve memory.",
    )

    sedimentation = physiology.propose_sedimentation(
        learning,
        identifier="SED-000101",
        title="Memory proposal",
        target=SedimentationTarget.MEMORY,
    )

    assert sedimentation.target is SedimentationTarget.MEMORY
    assert sedimentation.authority is SedimentationAuthority.PROPOSED

    assert not hasattr(physiology, "memory")
    assert not hasattr(physiology, "knowledge")


def test_learning_to_sedimentation_is_navigable():
    verification = make_verified_learning_source()
    repository = SedimentationRepository()

    physiology = LearningSedimentationPhysiology(repository)

    learning = physiology.learn(
        verification,
        identifier="LRN-000001",
        title="Navigable learning",
        statement="Learning retains its sedimentation descendants.",
    )

    first = physiology.propose_sedimentation(
        learning,
        identifier="SED-000101",
        title="First proposal",
        target=SedimentationTarget.MEMORY,
    )

    second = physiology.propose_sedimentation(
        learning,
        identifier="SED-000102",
        title="Second proposal",
        target=SedimentationTarget.KNOWLEDGE,
    )

    assert physiology.sedimentations_from(
        learning
    ) == (first, second)


def test_sedimentation_to_learning_is_navigable():
    verification = make_verified_learning_source()
    repository = SedimentationRepository()

    physiology = LearningSedimentationPhysiology(repository)

    learning = physiology.learn(
        verification,
        identifier="LRN-000001",
        title="Navigable learning",
        statement="Sedimentation retains its Learning origin.",
    )

    sedimentation = physiology.propose_sedimentation(
        learning,
        identifier="SED-000101",
        title="Proposal",
        target=SedimentationTarget.MEMORY,
    )

    assert physiology.learning_for(sedimentation) == learning


def test_unknown_learning_cannot_be_used_for_sedimentation():
    repository = SedimentationRepository()
    physiology = LearningSedimentationPhysiology(repository)

    foreign = Learning(
        identifier="LRN-FOREIGN",
        title="Foreign learning",
        verification_identifier="VER-FOREIGN",
        statement="This learning was never registered.",
    )

    with pytest.raises(LearningSedimentationError):
        physiology.propose_sedimentation(
            foreign,
            identifier="SED-FOREIGN",
            title="Invalid sedimentation",
            target=SedimentationTarget.MEMORY,
        )

    assert repository.all() == ()


# ---------------------------------------------------------------------------
# PCC-04 RUN 004 — Sedimentation governance + Human Attention
# ---------------------------------------------------------------------------

from python.epistemic.sedimentation import (
    GovernedSedimentation,
    SedimentationGovernance,
    SedimentationGovernor,
)


def make_governance_proposal():
    return Sedimentation(
        identifier="SED-GOV-001",
        title="Governed sedimentation",
        provenance_identifier="LRN-GOV-001",
        statement="A provisional meaning may deserve preservation.",
        target=SedimentationTarget.MEMORY,
    )


def test_routine_proposal_does_not_interrupt_human():
    proposal = make_governance_proposal()

    governed = SedimentationGovernor().routine(proposal)

    assert governed.governance is SedimentationGovernance.ROUTINE
    assert governed.requires_human_attention is False
    assert governed.may_continue_without_interruption is True

    # Proposal remains provisional.
    assert proposal.authority is SedimentationAuthority.PROPOSED


def test_routine_governance_does_not_auto_accept():
    proposal = make_governance_proposal()

    governed = SedimentationGovernor().routine(proposal)

    assert governed.sedimentation == proposal
    assert governed.sedimentation.is_accepted is False
    assert governed.sedimentation.is_rejected is False


def test_human_authority_requires_explicit_reason():
    proposal = make_governance_proposal()

    with pytest.raises(ValueError):
        GovernedSedimentation(
            sedimentation=proposal,
            governance=SedimentationGovernance.HUMAN_AUTHORITY,
        )


def test_high_impact_proposal_can_require_human_authority():
    proposal = make_governance_proposal()

    governed = SedimentationGovernor().require_human_authority(
        proposal,
        reason="Canonical approval required",
    )

    assert governed.requires_human_attention is True
    assert governed.reason == "Canonical approval required"
    assert proposal.authority is SedimentationAuthority.PROPOSED


def test_human_authority_can_accept_governed_proposal():
    proposal = make_governance_proposal()

    governed = SedimentationGovernor().require_human_authority(
        proposal,
        reason="Owner decision required",
    )

    accepted = governed.accept_by_human_authority()

    assert accepted.authority is SedimentationAuthority.ACCEPTED

    # Original history remains unchanged.
    assert proposal.authority is SedimentationAuthority.PROPOSED


def test_human_authority_can_reject_governed_proposal():
    proposal = make_governance_proposal()

    governed = SedimentationGovernor().require_human_authority(
        proposal,
        reason="Contested interpretation",
    )

    rejected = governed.reject_by_human_authority()

    assert rejected.authority is SedimentationAuthority.REJECTED

    # Original proposal remains preserved.
    assert proposal.authority is SedimentationAuthority.PROPOSED


def test_routine_governance_cannot_fake_human_authority():
    proposal = make_governance_proposal()

    governed = SedimentationGovernor().routine(proposal)

    with pytest.raises(ValueError):
        governed.accept_by_human_authority()

    with pytest.raises(ValueError):
        governed.reject_by_human_authority()


def test_governance_creates_no_memory_or_knowledge():
    proposal = make_governance_proposal()

    governed = SedimentationGovernor().routine(proposal)

    assert not hasattr(governed, "memory")
    assert not hasattr(governed, "knowledge")
    assert not hasattr(governed, "living_project_image")

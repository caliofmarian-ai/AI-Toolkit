from dataclasses import FrozenInstanceError

import pytest

from lib.python.epistemic.provenance import (
    NOT_VERIFIED,
    UNKNOWN,
    Provenance,
    ProvenanceError,
)


def test_source_preserves_origin_without_claiming_truth():
    provenance = Provenance()

    source = provenance.add_source(
        "Owner statement",
        kind="HUMAN",
        reference="conversation:owner",
    )

    assert source.identifier == "SRC-000001"
    assert source.title == "Owner statement"
    assert source.kind == "HUMAN"
    assert source.reference == "conversation:owner"
    assert source.display_identity == "SRC-000001 — Owner statement"


def test_observation_is_distinct_from_interpretation():
    provenance = Provenance()

    source = provenance.add_source(
        "Terminal execution",
        kind="EXECUTION",
        reference="terminal:run-001",
    )

    observation = provenance.observe(
        source,
        "Command exit observation",
        "Process exited with code 0.",
    )

    assert observation.source == source.identifier
    assert observation.observed == "Process exited with code 0."
    assert observation.interpretation == UNKNOWN


def test_interpretation_may_be_preserved_without_replacing_observation():
    provenance = Provenance()

    source = provenance.add_source(
        "Test run",
        kind="TEST",
        reference="pytest:run-001",
    )

    observation = provenance.observe(
        source,
        "Test result",
        "12 tests passed.",
        interpretation="The examined behavior satisfied the test suite.",
    )

    assert observation.observed == "12 tests passed."
    assert (
        observation.interpretation
        == "The examined behavior satisfied the test suite."
    )


def test_evidence_descends_from_observation():
    provenance = Provenance()

    source = provenance.add_source(
        "Git repository",
        kind="REPOSITORY",
        reference="git:HEAD",
    )

    observation = provenance.observe(
        source,
        "Commit observation",
        "Expected commit is present.",
    )

    evidence = provenance.preserve_evidence(
        observation,
        "Commit evidence",
        "git:commit:abc123",
        domain="TECHNICAL",
    )

    assert evidence.identifier == "EV-000001"
    assert evidence.observation == observation.identifier
    assert evidence.domain == "TECHNICAL"


def test_claim_is_not_automatically_verified():
    provenance = Provenance()

    claim = provenance.make_claim(
        "Persistent Experience operational",
        "Persistent Experience can recover preserved experience.",
    )

    assert claim.identifier == "CLM-000001"

    verification = provenance.verify(
        claim,
        "Persistent Experience verification",
    )

    assert verification.claim == claim.identifier
    assert verification.state == NOT_VERIFIED
    assert verification.basis == UNKNOWN


def test_supporting_evidence_relation_is_explicit():
    provenance = Provenance()

    source = provenance.add_source(
        "Behavioral test",
        kind="TEST",
        reference="pytest:test_recovery",
    )

    observation = provenance.observe(
        source,
        "Recovery result",
        "Recovered artifact matched expected state.",
    )

    evidence = provenance.preserve_evidence(
        observation,
        "Recovery test evidence",
        "pytest:test_recovery:pass",
        domain="TECHNICAL",
    )

    claim = provenance.make_claim(
        "Recovery works",
        "The preserved state can be recovered.",
    )

    relation = provenance.relate_evidence(
        evidence,
        claim,
        "SUPPORTS",
    )

    assert relation.evidence == evidence.identifier
    assert relation.claim == claim.identifier
    assert relation.role == "SUPPORTS"

    assert provenance.supporting_evidence(claim) == (evidence,)
    assert provenance.contradicting_evidence(claim) == ()


def test_contradictory_evidence_is_preserved_not_discarded():
    provenance = Provenance()

    source = provenance.add_source(
        "Runtime observation",
        kind="RUNTIME",
        reference="runtime:observation",
    )

    supporting_observation = provenance.observe(
        source,
        "Successful case",
        "Recovery succeeded for artifact A.",
    )

    contradicting_observation = provenance.observe(
        source,
        "Failed case",
        "Recovery failed for artifact B.",
    )

    supporting = provenance.preserve_evidence(
        supporting_observation,
        "Successful recovery evidence",
        "runtime:A",
        domain="TECHNICAL",
    )

    contradicting = provenance.preserve_evidence(
        contradicting_observation,
        "Failed recovery evidence",
        "runtime:B",
        domain="TECHNICAL",
    )

    claim = provenance.make_claim(
        "Recovery always succeeds",
        "Recovery succeeds for every preserved artifact.",
    )

    provenance.relate_evidence(
        supporting,
        claim,
        "SUPPORTS",
    )

    provenance.relate_evidence(
        contradicting,
        claim,
        "CONTRADICTS",
    )

    assert provenance.supporting_evidence(claim) == (supporting,)
    assert provenance.contradicting_evidence(claim) == (contradicting,)


def test_authority_evidence_remains_distinct_from_technical_evidence():
    provenance = Provenance()

    owner_source = provenance.add_source(
        "Owner authorization",
        kind="HUMAN",
        reference="conversation:authorization",
    )

    owner_observation = provenance.observe(
        owner_source,
        "Authorization observed",
        "Owner authorized PCC-03 implementation.",
    )

    authority_evidence = provenance.preserve_evidence(
        owner_observation,
        "Owner authorization evidence",
        "conversation:authorization",
        domain="AUTHORITY",
    )

    test_source = provenance.add_source(
        "Behavioral examination",
        kind="TEST",
        reference="pytest:pcc03",
    )

    test_observation = provenance.observe(
        test_source,
        "Behavior observed",
        "PCC-03 tests passed.",
    )

    technical_evidence = provenance.preserve_evidence(
        test_observation,
        "Behavioral test evidence",
        "pytest:pcc03:pass",
        domain="TECHNICAL",
    )

    assert authority_evidence.domain == "AUTHORITY"
    assert technical_evidence.domain == "TECHNICAL"
    assert authority_evidence != technical_evidence


def test_ai_source_does_not_automatically_become_evidence_or_verification():
    provenance = Provenance()

    source = provenance.add_source(
        "AI interpretation",
        kind="AI",
        reference="conversation:ai",
    )

    assert source.kind == "AI"

    claim = provenance.make_claim(
        "Capability exists",
        "The capability is operational.",
    )

    verification = provenance.verify(
        claim,
        "Capability verification",
    )

    assert verification.state == NOT_VERIFIED
    assert provenance.supporting_evidence(claim) == ()


def test_transformation_reference_is_preserved_not_reimplemented():
    provenance = Provenance()

    source = provenance.add_source(
        "Transformation artifact",
        kind="REPOSITORY",
        reference="work/transformation/TR-000001.md",
        transformation="TR-000001",
    )

    claim = provenance.make_claim(
        "Transformation produced state",
        "TR-000001 produced the observed state.",
        transformation="TR-000001",
    )

    assert source.transformation == "TR-000001"
    assert claim.transformation == "TR-000001"


def test_foreign_source_cannot_be_used_as_local_observation_parent():
    first = Provenance()
    second = Provenance()

    foreign_source = first.add_source(
        "Foreign source",
        kind="OTHER",
        reference="foreign",
    )

    with pytest.raises(ProvenanceError):
        second.observe(
            foreign_source,
            "Invalid observation",
            "Must fail.",
        )


def test_foreign_evidence_cannot_be_related_to_local_claim():
    first = Provenance()
    second = Provenance()

    source = first.add_source(
        "Source",
        kind="TEST",
        reference="test",
    )

    observation = first.observe(
        source,
        "Observation",
        "Observed.",
    )

    evidence = first.preserve_evidence(
        observation,
        "Evidence",
        "evidence",
    )

    claim = second.make_claim(
        "Claim",
        "A claim.",
    )

    with pytest.raises(ProvenanceError):
        second.relate_evidence(
            evidence,
            claim,
            "SUPPORTS",
        )


def test_epistemic_values_are_immutable():
    provenance = Provenance()

    source = provenance.add_source(
        "Immutable source",
        kind="OTHER",
        reference="source",
    )

    with pytest.raises(FrozenInstanceError):
        source.title = "Rewrite origin"


def test_empty_semantic_title_is_rejected():
    provenance = Provenance()

    with pytest.raises(ProvenanceError):
        provenance.add_source(
            "   ",
            kind="OTHER",
            reference="source",
        )


def test_human_readable_identity_is_available_for_all_primary_entities():
    provenance = Provenance()

    source = provenance.add_source(
        "Terminal",
        kind="EXECUTION",
        reference="terminal",
    )

    observation = provenance.observe(
        source,
        "Exit code",
        "Exit code was 0.",
    )

    evidence = provenance.preserve_evidence(
        observation,
        "Exit evidence",
        "terminal:exit",
    )

    claim = provenance.make_claim(
        "Execution succeeded",
        "Execution completed successfully.",
    )

    verification = provenance.verify(
        claim,
        "Execution verification",
    )

    assert source.display_identity == "SRC-000001 — Terminal"
    assert observation.display_identity == "OBS-000001 — Exit code"
    assert evidence.display_identity == "EV-000001 — Exit evidence"
    assert claim.display_identity == "CLM-000001 — Execution succeeded"
    assert (
        verification.display_identity
        == "VER-000001 — Execution verification"
    )

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


def test_provenance_survives_restart_through_single_markdown_manifestation(
    tmp_path,
):
    provenance = Provenance()

    source = provenance.add_source(
        "Repository inspection",
        kind="REPOSITORY",
        reference="git:HEAD",
        transformation="TR-000042",
    )

    observation = provenance.observe(
        source,
        "Repository state",
        "Expected implementation exists.",
        interpretation="Implementation appears structurally present.",
    )

    supporting = provenance.preserve_evidence(
        observation,
        "Repository evidence",
        "git:file:implementation.py",
        domain="TECHNICAL",
    )

    contradiction_observation = provenance.observe(
        source,
        "Runtime absence",
        "No runtime execution evidence was inspected.",
    )

    contradicting = provenance.preserve_evidence(
        contradiction_observation,
        "Missing runtime evidence",
        "runtime:UNKNOWN",
        domain="OBSERVATIONAL",
    )

    claim = provenance.make_claim(
        "Implementation is operational",
        "The implementation works in its operating environment.",
        transformation="TR-000042",
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

    provenance.verify(
        claim,
        "Operational verification",
        state=NOT_VERIFIED,
        basis=UNKNOWN,
    )

    artifact = provenance.save(tmp_path)

    assert artifact == tmp_path / "PROVENANCE.md"
    assert artifact.is_file()

    recovered = Provenance.load(tmp_path)

    assert recovered._sources == provenance._sources
    assert recovered._observations == provenance._observations
    assert recovered._evidence == provenance._evidence
    assert recovered._claims == provenance._claims
    assert recovered._verifications == provenance._verifications
    assert (
        recovered._evidence_relations
        == provenance._evidence_relations
    )


def test_persisted_manifestation_is_human_readable(tmp_path):
    provenance = Provenance()

    source = provenance.add_source(
        "Owner authorization",
        kind="HUMAN",
        reference="conversation:owner",
    )

    observation = provenance.observe(
        source,
        "Authorization",
        "Owner authorized implementation.",
    )

    evidence = provenance.preserve_evidence(
        observation,
        "Authorization evidence",
        "conversation:owner",
        domain="AUTHORITY",
    )

    claim = provenance.make_claim(
        "Implementation authorized",
        "The Owner authorized implementation.",
    )

    provenance.relate_evidence(
        evidence,
        claim,
        "SUPPORTS",
    )

    provenance.verify(
        claim,
        "Authorization verification",
        state="VERIFIED",
        basis=evidence.identifier,
    )

    artifact = provenance.save(tmp_path)
    text = artifact.read_text(encoding="utf-8")

    assert "# Epistemic Provenance" in text
    assert "SRC-000001 — Owner authorization" in text
    assert "OBS-000001 — Authorization" in text
    assert "EV-000001 — Authorization evidence" in text
    assert "CLM-000001 — Implementation authorized" in text
    assert "VER-000001 — Authorization verification" in text


def test_recovery_preserves_unknown_without_inventing_state(tmp_path):
    provenance = Provenance()

    claim = provenance.make_claim(
        "Unknown runtime condition",
        "Runtime behavior has not yet been established.",
    )

    provenance.verify(
        claim,
        "Runtime verification",
    )

    provenance.save(tmp_path)

    recovered = Provenance.load(tmp_path)

    verification = recovered._verifications["VER-000001"]

    assert verification.state == NOT_VERIFIED
    assert verification.basis == UNKNOWN


def test_recovery_preserves_supporting_and_contradicting_evidence(
    tmp_path,
):
    provenance = Provenance()

    source = provenance.add_source(
        "Runtime",
        kind="RUNTIME",
        reference="runtime",
    )

    first_observation = provenance.observe(
        source,
        "Success",
        "Case A succeeded.",
    )

    second_observation = provenance.observe(
        source,
        "Failure",
        "Case B failed.",
    )

    supporting = provenance.preserve_evidence(
        first_observation,
        "Success evidence",
        "runtime:A",
    )

    contradicting = provenance.preserve_evidence(
        second_observation,
        "Failure evidence",
        "runtime:B",
    )

    claim = provenance.make_claim(
        "Universal success",
        "Every case succeeds.",
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

    provenance.save(tmp_path)

    recovered = Provenance.load(tmp_path)
    recovered_claim = recovered._claims[claim.identifier]

    assert tuple(
        item.identifier
        for item in recovered.supporting_evidence(recovered_claim)
    ) == (supporting.identifier,)

    assert tuple(
        item.identifier
        for item in recovered.contradicting_evidence(recovered_claim)
    ) == (contradicting.identifier,)


def test_next_identity_continues_after_recovery(tmp_path):
    provenance = Provenance()

    provenance.add_source(
        "First",
        kind="OTHER",
        reference="first",
    )

    provenance.save(tmp_path)

    recovered = Provenance.load(tmp_path)

    second = recovered.add_source(
        "Second",
        kind="OTHER",
        reference="second",
    )

    assert second.identifier == "SRC-000002"


def test_missing_persisted_provenance_is_explicit(tmp_path):
    with pytest.raises(ProvenanceError):
        Provenance.load(tmp_path)


def test_corrupt_persisted_provenance_is_rejected(tmp_path):
    (tmp_path / "PROVENANCE.md").write_text(
        "# Epistemic Provenance\n\n```json\n{broken\n```\n",
        encoding="utf-8",
    )

    with pytest.raises(ProvenanceError):
        Provenance.load(tmp_path)


def test_dangling_persisted_observation_is_rejected(tmp_path):
    import json

    payload = {
        "sources": [],
        "observations": [
            {
                "identifier": "OBS-000001",
                "title": "Dangling",
                "source": "SRC-999999",
                "observed": "Impossible ancestry.",
                "interpretation": UNKNOWN,
            }
        ],
        "evidence": [],
        "claims": [],
        "verifications": [],
        "evidence_relations": [],
    }

    (tmp_path / "PROVENANCE.md").write_text(
        "# Epistemic Provenance\n\n"
        "```json\n"
        + json.dumps(payload)
        + "\n```\n",
        encoding="utf-8",
    )

    with pytest.raises(ProvenanceError):
        Provenance.load(tmp_path)


def _build_bidirectional_provenance():
    provenance = Provenance()

    source = provenance.add_source(
        "Repository and runtime inspection",
        kind="RUNTIME",
        reference="runtime:inspection",
        transformation="TR-000042",
    )

    success_observation = provenance.observe(
        source,
        "Successful execution",
        "The requested execution completed.",
        interpretation="Observed execution supports operational behavior.",
    )

    failure_observation = provenance.observe(
        source,
        "Contradicting execution",
        "A second execution failed.",
        interpretation="Observed failure contradicts universal success.",
    )

    supporting = provenance.preserve_evidence(
        success_observation,
        "Successful execution evidence",
        "runtime:success",
        domain="TECHNICAL",
    )

    contradicting = provenance.preserve_evidence(
        failure_observation,
        "Failure evidence",
        "runtime:failure",
        domain="TECHNICAL",
    )

    claim = provenance.make_claim(
        "Execution always succeeds",
        "Every execution succeeds.",
        transformation="TR-000042",
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

    verification = provenance.verify(
        claim,
        "Execution verification",
        state=NOT_VERIFIED,
        basis=contradicting.identifier,
    )

    return (
        provenance,
        source,
        success_observation,
        failure_observation,
        supporting,
        contradicting,
        claim,
        verification,
    )


def test_bidirectional_navigation_preserves_each_explicit_edge():
    (
        provenance,
        source,
        success_observation,
        failure_observation,
        supporting,
        contradicting,
        claim,
        verification,
    ) = _build_bidirectional_provenance()

    assert provenance.source_for_observation(
        success_observation
    ) == source

    assert provenance.observations_from_source(source) == (
        success_observation,
        failure_observation,
    )

    assert provenance.observation_for_evidence(
        supporting
    ) == success_observation

    assert provenance.evidence_from_observation(
        failure_observation
    ) == (contradicting,)

    assert provenance.claims_for_evidence(
        supporting
    ) == (claim,)

    assert provenance.evidence_for_claim(claim) == (
        supporting,
        contradicting,
    )

    assert provenance.verifications_for_claim(claim) == (
        verification,
    )

    assert provenance.claim_for_verification(
        verification
    ) == claim


def test_claim_navigation_keeps_contradiction_visible():
    (
        provenance,
        _source,
        _success_observation,
        _failure_observation,
        supporting,
        contradicting,
        claim,
        _verification,
    ) = _build_bidirectional_provenance()

    assert provenance.evidence_for_claim(
        claim,
        role="SUPPORTS",
    ) == (supporting,)

    assert provenance.evidence_for_claim(
        claim,
        role="CONTRADICTS",
    ) == (contradicting,)

    assert provenance.supporting_evidence(
        claim
    ) == (supporting,)

    assert provenance.contradicting_evidence(
        claim
    ) == (contradicting,)


def test_evidence_navigation_does_not_infer_unrecorded_claim_relation():
    provenance = Provenance()

    source = provenance.add_source(
        "Repository",
        kind="REPOSITORY",
        reference="git:HEAD",
    )

    observation = provenance.observe(
        source,
        "Observed file",
        "A file exists.",
    )

    evidence = provenance.preserve_evidence(
        observation,
        "File evidence",
        "git:file",
    )

    provenance.make_claim(
        "Similar words",
        "A claim exists with semantically similar wording.",
    )

    assert provenance.claims_for_evidence(evidence) == ()


def test_backward_provenance_traverses_verification_to_source():
    (
        provenance,
        source,
        success_observation,
        failure_observation,
        supporting,
        contradicting,
        claim,
        verification,
    ) = _build_bidirectional_provenance()

    assert provenance.provenance_to_source(
        verification
    ) == (
        verification,
        claim,
        (supporting, contradicting),
        (success_observation, failure_observation),
        (source,),
    )


def test_forward_provenance_traverses_source_to_verification():
    (
        provenance,
        source,
        success_observation,
        failure_observation,
        supporting,
        contradicting,
        claim,
        verification,
    ) = _build_bidirectional_provenance()

    assert provenance.provenance_from_source(
        source
    ) == (
        source,
        (success_observation, failure_observation),
        (supporting, contradicting),
        (claim,),
        (verification,),
    )


def test_bidirectional_navigation_survives_persistence_restart(
    tmp_path,
):
    (
        provenance,
        source,
        _success_observation,
        _failure_observation,
        _supporting,
        _contradicting,
        _claim,
        verification,
    ) = _build_bidirectional_provenance()

    provenance.save(tmp_path)

    recovered = Provenance.load(tmp_path)

    recovered_source = recovered._sources[source.identifier]
    recovered_verification = recovered._verifications[
        verification.identifier
    ]

    forward = recovered.provenance_from_source(
        recovered_source
    )

    backward = recovered.provenance_to_source(
        recovered_verification
    )

    assert forward[0].identifier == source.identifier
    assert forward[-1][0].identifier == verification.identifier

    assert backward[0].identifier == verification.identifier
    assert backward[-1][0].identifier == source.identifier


def test_navigation_rejects_foreign_entities():
    first = Provenance()
    second = Provenance()

    source = first.add_source(
        "First source",
        kind="OTHER",
        reference="first",
    )

    observation = first.observe(
        source,
        "First observation",
        "Observed.",
    )

    evidence = first.preserve_evidence(
        observation,
        "First evidence",
        "first:evidence",
    )

    claim = first.make_claim(
        "First claim",
        "Claim.",
    )

    first.relate_evidence(
        evidence,
        claim,
        "SUPPORTS",
    )

    verification = first.verify(
        claim,
        "First verification",
    )

    import pytest

    with pytest.raises(ProvenanceError):
        second.observations_from_source(source)

    with pytest.raises(ProvenanceError):
        second.evidence_from_observation(observation)

    with pytest.raises(ProvenanceError):
        second.claims_for_evidence(evidence)

    with pytest.raises(ProvenanceError):
        second.verifications_for_claim(claim)

    with pytest.raises(ProvenanceError):
        second.claim_for_verification(verification)


def test_invalid_navigation_role_is_rejected():
    provenance = Provenance()

    claim = provenance.make_claim(
        "Claim",
        "Statement.",
    )

    import pytest

    with pytest.raises(ProvenanceError):
        provenance.evidence_for_claim(
            claim,
            role="INFERRED",
        )

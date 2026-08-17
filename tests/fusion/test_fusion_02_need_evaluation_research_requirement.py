from __future__ import annotations

from python.ai_platform.cognitive_coordination import (
    EpistemicCognitiveCoordinator,
)


def test_repository_evidence_need_requires_bounded_read_only_research():
    coordinator = EpistemicCognitiveCoordinator()

    result = coordinator.initialize(
        "Inspect repository evidence for the current implementation",
        session_id="research-alpha",
    )

    need = result["information_need"]
    evaluation = result["need_evaluation"]
    journey = result["journey"]

    assert evaluation["schema"] == "FUSION-02-NEED-EVALUATION-1"
    assert evaluation["need_id"] == need["need_id"]
    assert evaluation["research_required"] is True
    assert evaluation["requested_capabilities"] == [
        "search",
        "resolve",
        "read",
        "inspect",
    ]
    assert evaluation["reason"] == "REPOSITORY_EVIDENCE_REQUIRED"

    assert need["research_required"] is True
    assert need["requested_capabilities"] == [
        "search",
        "resolve",
        "read",
        "inspect",
    ]

    assert journey["status"] == "UNRESOLVED"
    assert journey["step_count"] == 0
    assert journey["epistemic_gain"] is False
    assert journey["visited"] == []


def test_trivial_message_does_not_require_research():
    coordinator = EpistemicCognitiveCoordinator()

    result = coordinator.initialize(
        "hello",
        session_id="research-trivial",
    )

    evaluation = result["need_evaluation"]
    need = result["information_need"]

    assert evaluation["research_required"] is False
    assert evaluation["requested_capabilities"] == []
    assert evaluation["reason"] == "NO_EPISTEMIC_NAVIGATION_REQUIRED"
    assert evaluation["confidence"] == "HIGH"

    assert need["research_required"] is False
    assert need["requested_capabilities"] == []


def test_undemonstrated_research_requirement_remains_unknown_without_navigation():
    coordinator = EpistemicCognitiveCoordinator()

    result = coordinator.initialize(
        "Explain this idea to me",
        session_id="research-unknown",
    )

    evaluation = result["need_evaluation"]
    journey = result["journey"]

    assert evaluation["research_required"] is False
    assert evaluation["requested_capabilities"] == []
    assert evaluation["reason"] == "RESEARCH_REQUIREMENT_UNDEMONSTRATED"
    assert evaluation["confidence"] == "UNKNOWN"

    assert journey["status"] == "UNRESOLVED"
    assert journey["step_count"] == 0
    assert journey["epistemic_gain"] is False


def test_need_evaluation_does_not_claim_navigation_capabilities_not_requested():
    coordinator = EpistemicCognitiveCoordinator()

    result = coordinator.initialize(
        "Audit repository code and tests",
        session_id="research-capabilities",
    )

    requested = result["need_evaluation"]["requested_capabilities"]

    assert requested == [
        "search",
        "resolve",
        "read",
        "inspect",
    ]

    assert "traverse" not in requested
    assert "trace_provenance" not in requested
    assert "write" not in requested
    assert "modify" not in requested


def test_evaluation_is_deterministic_for_equivalent_information_need():
    coordinator = EpistemicCognitiveCoordinator()

    first = coordinator.initialize(
        "Inspect   repository   evidence",
        session_id="research-deterministic",
    )
    second = coordinator.initialize(
        "Inspect repository evidence",
        session_id="research-deterministic",
    )

    assert first["information_need"]["need_id"] == second["information_need"]["need_id"]
    assert first["need_evaluation"] == second["need_evaluation"]
    assert first["journey"]["journey_id"] == second["journey"]["journey_id"]


def test_need_evaluation_does_not_perform_retrieval():
    coordinator = EpistemicCognitiveCoordinator()

    result = coordinator.initialize(
        "Inspect repository evidence",
        session_id="research-no-retrieval",
    )

    journey = result["journey"]

    assert result["information_need"]["research_required"] is True
    assert journey["step_count"] == 0
    assert journey["visited"] == []
    assert journey["epistemic_gain"] is False
    assert journey["stopping_reason"] == ""

from __future__ import annotations

from python.ai_platform.cognitive_coordination import (
    EpistemicCognitiveCoordinator,
)


def test_information_need_is_bounded_and_does_not_retrieve():
    coordinator = EpistemicCognitiveCoordinator()

    result = coordinator.initialize(
        "  Why does Owner AI Chat receive OpenAI 429 because of tokens?  ",
        session_id="session-alpha",
    )

    need = result["information_need"]
    journey = result["journey"]

    assert need["schema"] == "FUSION-02-INFORMATION-NEED-1"
    assert need["question"] == (
        "Why does Owner AI Chat receive OpenAI 429 because of tokens?"
    )
    assert need["objective"] == "ANSWER_HUMAN_REQUEST"
    assert need["epistemic_status"] == "UNRESOLVED"

    assert need["research_required"] is False
    assert need["requested_capabilities"] == []

    assert need["constraints"] == {
        "retrieval_confers_authority": False,
        "navigation_read_only": True,
        "unknown_is_valid": True,
        "human_authority_preserved": True,
        "knowledge_availability_is_not_working_context": True,
        "full_repository_profile_default_payload": False,
    }

    assert journey["schema"] == "FUSION-02-JOURNEY-STATE-1"
    assert journey["need_id"] == need["need_id"]
    assert journey["status"] == "UNRESOLVED"
    assert journey["step_count"] == 0
    assert journey["epistemic_gain"] is False
    assert journey["visited"] == []
    assert journey["stopping_reason"] == ""


def test_trivial_human_message_does_not_imply_repository_research():
    coordinator = EpistemicCognitiveCoordinator()

    result = coordinator.initialize(
        "hi",
        session_id="session-hi",
    )

    need = result["information_need"]

    assert need["question"] == "hi"
    assert need["research_required"] is False
    assert need["requested_capabilities"] == []
    assert (
        need["constraints"]["full_repository_profile_default_payload"]
        is False
    )


def test_information_need_and_journey_identity_are_deterministic():
    coordinator = EpistemicCognitiveCoordinator()

    first = coordinator.initialize(
        "Inspect repository evidence",
        session_id="session-one",
    )
    second = coordinator.initialize(
        "Inspect   repository   evidence",
        session_id="session-one",
    )

    assert (
        first["information_need"]["need_id"]
        == second["information_need"]["need_id"]
    )
    assert (
        first["journey"]["journey_id"]
        == second["journey"]["journey_id"]
    )


def test_journey_identity_is_session_scoped():
    coordinator = EpistemicCognitiveCoordinator()

    first = coordinator.initialize(
        "Inspect repository evidence",
        session_id="session-one",
    )
    second = coordinator.initialize(
        "Inspect repository evidence",
        session_id="session-two",
    )

    assert (
        first["information_need"]["need_id"]
        == second["information_need"]["need_id"]
    )
    assert (
        first["journey"]["journey_id"]
        != second["journey"]["journey_id"]
    )


def test_empty_human_question_fails_closed():
    coordinator = EpistemicCognitiveCoordinator()

    try:
        coordinator.initialize("   ")
    except ValueError as exc:
        assert "must not be empty" in str(exc)
    else:
        raise AssertionError("Empty question must fail closed")

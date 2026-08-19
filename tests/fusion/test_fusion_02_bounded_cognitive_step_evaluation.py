from python.ai_platform.cognitive_coordination import (
    EpistemicCognitiveCoordinator,
    JourneyState,
)


def _journey(
    *,
    status="IN_PROGRESS",
    step_count=1,
    epistemic_gain=True,
    visited=("evidence:search",),
    stopping_reason="",
):
    return JourneyState(
        schema="FUSION-02-JOURNEY-1",
        journey_id="journey-e12",
        need_id="need-e12",
        status=status,
        step_count=step_count,
        epistemic_gain=epistemic_gain,
        visited=tuple(visited),
        stopping_reason=stopping_reason,
    )


def test_cognitive_step_satisfied_stops_journey():
    coordinator = EpistemicCognitiveCoordinator()

    result = coordinator.evaluate_cognitive_step(
        journey=_journey(),
        outcome="SATISFIED",
        observation_identity="read:first.txt",
        epistemic_gain=True,
    )

    assert result["outcome"] == "SATISFIED"
    assert result["continue_navigation"] is False
    assert result["authority_conferred"] is False
    assert result["human_authority_preserved"] is True

    journey = result["journey"]

    assert journey["status"] == "SATISFIED"
    assert journey["step_count"] == 2
    assert journey["epistemic_gain"] is True
    assert journey["stopping_reason"] == "SATISFIED"
    assert journey["visited"] == [
        "evidence:search",
        "read:first.txt",
    ]


def test_cognitive_step_partial_with_gain_may_continue():
    coordinator = EpistemicCognitiveCoordinator()

    result = coordinator.evaluate_cognitive_step(
        journey=_journey(),
        outcome="PARTIAL",
        observation_identity="read:first.txt",
        epistemic_gain=True,
    )

    assert result["outcome"] == "PARTIAL"
    assert result["continue_navigation"] is True

    journey = result["journey"]

    assert journey["status"] == "IN_PROGRESS"
    assert journey["step_count"] == 2
    assert journey["epistemic_gain"] is True
    assert journey["stopping_reason"] == ""


def test_cognitive_step_partial_without_gain_stops():
    coordinator = EpistemicCognitiveCoordinator()

    result = coordinator.evaluate_cognitive_step(
        journey=_journey(),
        outcome="PARTIAL",
        observation_identity="read:first.txt",
        epistemic_gain=False,
    )

    assert result["outcome"] == "NO_EPISTEMIC_GAIN"
    assert result["continue_navigation"] is False

    journey = result["journey"]

    assert journey["status"] == "NO_EPISTEMIC_GAIN"
    assert journey["step_count"] == 2
    assert journey["epistemic_gain"] is False
    assert journey["stopping_reason"] == "NO_EPISTEMIC_GAIN"


def test_cognitive_step_unknown_without_gain_stops():
    coordinator = EpistemicCognitiveCoordinator()

    result = coordinator.evaluate_cognitive_step(
        journey=_journey(),
        outcome="UNKNOWN",
        observation_identity="read:missing.txt",
        epistemic_gain=False,
    )

    assert result["outcome"] == "NO_EPISTEMIC_GAIN"
    assert result["continue_navigation"] is False
    assert result["unknown_is_valid"] is True

    journey = result["journey"]

    assert journey["status"] == "NO_EPISTEMIC_GAIN"
    assert journey["epistemic_gain"] is False
    assert journey["stopping_reason"] == "NO_EPISTEMIC_GAIN"


def test_cognitive_step_human_required_stops_without_authority():
    coordinator = EpistemicCognitiveCoordinator()

    result = coordinator.evaluate_cognitive_step(
        journey=_journey(),
        outcome="HUMAN_REQUIRED",
        observation_identity="decision:human",
        epistemic_gain=True,
    )

    assert result["continue_navigation"] is False
    assert result["authority_conferred"] is False
    assert result["human_authority_preserved"] is True

    journey = result["journey"]

    assert journey["status"] == "HUMAN_REQUIRED"
    assert journey["stopping_reason"] == "HUMAN_REQUIRED"


def test_cognitive_step_blocked_stops():
    coordinator = EpistemicCognitiveCoordinator()

    result = coordinator.evaluate_cognitive_step(
        journey=_journey(),
        outcome="BLOCKED",
        observation_identity="boundary:blocked",
        epistemic_gain=False,
    )

    assert result["continue_navigation"] is False
    assert result["journey"]["status"] == "BLOCKED"
    assert result["journey"]["stopping_reason"] == "BLOCKED"


def test_cognitive_step_forbidden_stops():
    coordinator = EpistemicCognitiveCoordinator()

    result = coordinator.evaluate_cognitive_step(
        journey=_journey(),
        outcome="FORBIDDEN",
        observation_identity="boundary:forbidden",
        epistemic_gain=False,
    )

    assert result["continue_navigation"] is False
    assert result["journey"]["status"] == "FORBIDDEN"
    assert result["journey"]["stopping_reason"] == "FORBIDDEN"


def test_cognitive_step_rejects_unknown_outcome_vocabulary():
    coordinator = EpistemicCognitiveCoordinator()

    try:
        coordinator.evaluate_cognitive_step(
            journey=_journey(),
            outcome="SEARCH_UNTIL_ANSWER",
            observation_identity="invalid",
            epistemic_gain=True,
        )
    except ValueError as exc:
        assert "unsupported cognitive outcome" in str(exc)
    else:
        raise AssertionError(
            "unsupported cognitive outcome was accepted"
        )


def test_cognitive_step_does_not_duplicate_visited_identity():
    coordinator = EpistemicCognitiveCoordinator()

    result = coordinator.evaluate_cognitive_step(
        journey=_journey(
            visited=(
                "evidence:search",
                "read:first.txt",
            )
        ),
        outcome="PARTIAL",
        observation_identity="read:first.txt",
        epistemic_gain=True,
    )

    assert result["journey"]["visited"] == [
        "evidence:search",
        "read:first.txt",
    ]


def test_cognitive_step_does_not_mutate_input_journey():
    coordinator = EpistemicCognitiveCoordinator()

    original = _journey()

    before = original.to_dict()

    coordinator.evaluate_cognitive_step(
        journey=original,
        outcome="SATISFIED",
        observation_identity="read:first.txt",
        epistemic_gain=True,
    )

    assert original.to_dict() == before

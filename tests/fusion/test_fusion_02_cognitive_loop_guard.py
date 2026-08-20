from copy import deepcopy

from python.ai_platform.cognitive_coordination import (
    EpistemicCognitiveCoordinator,
    JourneyState,
)


def _journey(
    *,
    need_id="need-e12",
    step_count=2,
    epistemic_gain=True,
    visited=(),
):
    return JourneyState(
        schema="FUSION-02-JOURNEY-STATE-1",
        journey_id="journey-e12",
        need_id=need_id,
        status="IN_PROGRESS",
        step_count=step_count,
        epistemic_gain=epistemic_gain,
        visited=tuple(visited),
        stopping_reason="",
    )


def test_guard_allows_novel_bounded_step():
    coordinator = EpistemicCognitiveCoordinator()

    result = coordinator.evaluate_cognitive_loop_guard(
        journey=_journey(
            visited=("evidence:search",)
        ),
        observation_identity="read:new.txt",
        capability="read",
        epistemic_gain=True,
    )

    assert result["continue_navigation"] is True
    assert result["stopping_reason"] == ""
    assert result["bounded"] is True
    assert result["authority_conferred"] is False
    assert result["human_authority_preserved"] is True


def test_guard_stops_repeated_need():
    coordinator = EpistemicCognitiveCoordinator()

    result = coordinator.evaluate_cognitive_loop_guard(
        journey=_journey(),
        need_id="need-e12",
        epistemic_gain=True,
    )

    assert result["repeated_need"] is True
    assert result["continue_navigation"] is False
    assert result["stopping_reason"] == "REPEATED_NEED"


def test_initial_need_is_not_repetition():
    coordinator = EpistemicCognitiveCoordinator()

    result = coordinator.evaluate_cognitive_loop_guard(
        journey=_journey(step_count=0),
        need_id="need-e12",
        epistemic_gain=True,
    )

    assert result["repeated_need"] is False
    assert result["continue_navigation"] is True


def test_guard_stops_repeated_result():
    coordinator = EpistemicCognitiveCoordinator()

    result = coordinator.evaluate_cognitive_loop_guard(
        journey=_journey(
            visited=("result:result-1",)
        ),
        result_identity="result-1",
        epistemic_gain=True,
    )

    assert result["repeated_result"] is True
    assert result["continue_navigation"] is False
    assert result["stopping_reason"] == "REPEATED_RESULT"


def test_guard_stops_repeated_identity_capability():
    coordinator = EpistemicCognitiveCoordinator()

    token = (
        "observation:source:a.py"
        "|capability:read"
    )

    result = coordinator.evaluate_cognitive_loop_guard(
        journey=_journey(
            visited=(token,)
        ),
        observation_identity="source:a.py",
        capability="read",
        epistemic_gain=True,
    )

    assert (
        result["repeated_identity_capability"]
        is True
    )
    assert result["continue_navigation"] is False
    assert (
        result["stopping_reason"]
        == "REPEATED_IDENTITY_CAPABILITY"
    )


def test_guard_stops_traversal_cycle():
    coordinator = EpistemicCognitiveCoordinator()

    result = coordinator.evaluate_cognitive_loop_guard(
        journey=_journey(
            visited=(
                "source:a.py",
                "source:b.py",
            )
        ),
        observation_identity="source:a.py",
        epistemic_gain=True,
    )

    assert result["traversal_cycle"] is True
    assert result["continue_navigation"] is False
    assert (
        result["stopping_reason"]
        == "TRAVERSAL_CYCLE"
    )


def test_guard_stops_unavailable_organ():
    coordinator = EpistemicCognitiveCoordinator()

    result = coordinator.evaluate_cognitive_loop_guard(
        journey=_journey(),
        unavailable_organ=True,
        epistemic_gain=True,
    )

    assert result["unavailable_organ"] is True
    assert result["continue_navigation"] is False
    assert (
        result["stopping_reason"]
        == "UNAVAILABLE_ORGAN"
    )


def test_guard_stops_ambiguity():
    coordinator = EpistemicCognitiveCoordinator()

    result = coordinator.evaluate_cognitive_loop_guard(
        journey=_journey(),
        ambiguous=True,
        epistemic_gain=True,
    )

    assert result["ambiguous"] is True
    assert result["continue_navigation"] is False
    assert result["stopping_reason"] == "AMBIGUITY"


def test_guard_stops_authority_boundary():
    coordinator = EpistemicCognitiveCoordinator()

    result = coordinator.evaluate_cognitive_loop_guard(
        journey=_journey(),
        authority_stop=True,
        epistemic_gain=True,
    )

    assert result["authority_stop"] is True
    assert result["continue_navigation"] is False
    assert (
        result["stopping_reason"]
        == "AUTHORITY_STOP"
    )
    assert result["authority_conferred"] is False
    assert result["human_authority_preserved"] is True


def test_guard_stops_without_epistemic_gain():
    coordinator = EpistemicCognitiveCoordinator()

    result = coordinator.evaluate_cognitive_loop_guard(
        journey=_journey(),
        epistemic_gain=False,
    )

    assert result["no_epistemic_gain"] is True
    assert result["continue_navigation"] is False
    assert (
        result["stopping_reason"]
        == "NO_EPISTEMIC_GAIN"
    )


def test_guard_does_not_mutate_journey():
    coordinator = EpistemicCognitiveCoordinator()

    journey = _journey(
        visited=("evidence:search",)
    )

    before = deepcopy(
        journey.to_dict()
    )

    coordinator.evaluate_cognitive_loop_guard(
        journey=journey,
        observation_identity="read:new.txt",
        capability="read",
        epistemic_gain=True,
    )

    assert journey.to_dict() == before


def test_guard_does_not_execute_navigation():
    coordinator = EpistemicCognitiveCoordinator()

    journey = _journey(
        step_count=7,
        visited=("evidence:search",)
    )

    result = coordinator.evaluate_cognitive_loop_guard(
        journey=journey,
        observation_identity="read:new.txt",
        capability="read",
        epistemic_gain=True,
    )

    assert result["continue_navigation"] is True
    assert journey.step_count == 7
    assert journey.visited == (
        "evidence:search",
    )


def test_guard_preserves_unknown_as_valid():
    coordinator = EpistemicCognitiveCoordinator()

    result = coordinator.evaluate_cognitive_loop_guard(
        journey=_journey(),
        unavailable_organ=True,
        epistemic_gain=False,
    )

    assert result["unknown_is_valid"] is True
    assert result["authority_conferred"] is False

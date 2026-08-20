from copy import deepcopy

import pytest

from python.ai_platform.cognitive_coordination import (
    EpistemicCognitiveCoordinator,
    JourneyState,
)


def _journey():
    return JourneyState(
        schema="FUSION-02-JOURNEY-STATE-1",
        journey_id="journey-boundary-1",
        need_id="need-boundary-1",
        status="IN_PROGRESS",
        step_count=4,
        epistemic_gain=True,
        visited=(
            "source:a.py",
            "result:result-1",
        ),
        stopping_reason="",
    )


@pytest.mark.parametrize(
    "boundary",
    (
        "BLOCKED",
        "HUMAN_REQUIRED",
        "FORBIDDEN",
    ),
)
def test_terminal_boundary_conserves_journey(
    boundary,
):
    coordinator = EpistemicCognitiveCoordinator()
    journey = _journey()

    result = coordinator.conserve_journey_boundary(
        journey=journey,
        boundary=boundary,
    )

    assert result.schema == journey.schema
    assert result.journey_id == journey.journey_id
    assert result.need_id == journey.need_id
    assert result.step_count == journey.step_count
    assert (
        result.epistemic_gain
        == journey.epistemic_gain
    )
    assert result.visited == journey.visited
    assert result.status == boundary
    assert result.stopping_reason == boundary


def test_provider_failure_conserves_journey():
    coordinator = EpistemicCognitiveCoordinator()
    journey = _journey()

    result = coordinator.conserve_journey_boundary(
        journey=journey,
        boundary="BLOCKED",
        provider_failed=True,
    )

    assert result.schema == journey.schema
    assert result.journey_id == journey.journey_id
    assert result.need_id == journey.need_id
    assert result.step_count == journey.step_count
    assert result.visited == journey.visited
    assert result.status == "PROVIDER_FAILURE"
    assert (
        result.stopping_reason
        == "PROVIDER_FAILURE"
    )


def test_explicit_reason_is_preserved():
    coordinator = EpistemicCognitiveCoordinator()
    journey = _journey()

    result = coordinator.conserve_journey_boundary(
        journey=journey,
        boundary="BLOCKED",
        stopping_reason="UNAVAILABLE_ORGAN",
    )

    assert result.status == "BLOCKED"
    assert (
        result.stopping_reason
        == "UNAVAILABLE_ORGAN"
    )


def test_conservation_does_not_mutate_input():
    coordinator = EpistemicCognitiveCoordinator()
    journey = _journey()

    before = deepcopy(
        journey.to_dict()
    )

    coordinator.conserve_journey_boundary(
        journey=journey,
        boundary="BLOCKED",
    )

    assert journey.to_dict() == before


def test_conservation_does_not_add_hops():
    coordinator = EpistemicCognitiveCoordinator()
    journey = _journey()

    result = coordinator.conserve_journey_boundary(
        journey=journey,
        boundary="HUMAN_REQUIRED",
    )

    assert result.step_count == 4
    assert result.visited == (
        "source:a.py",
        "result:result-1",
    )


def test_unsupported_boundary_is_rejected():
    coordinator = EpistemicCognitiveCoordinator()

    with pytest.raises(ValueError):
        coordinator.conserve_journey_boundary(
            journey=_journey(),
            boundary="SATISFIED",
        )


def test_provider_failure_flag_has_exact_precedence():
    coordinator = EpistemicCognitiveCoordinator()

    result = coordinator.conserve_journey_boundary(
        journey=_journey(),
        boundary="FORBIDDEN",
        provider_failed=True,
    )

    assert result.status == "PROVIDER_FAILURE"
    assert (
        result.stopping_reason
        == "PROVIDER_FAILURE"
    )


def test_conservation_is_deterministic():
    coordinator = EpistemicCognitiveCoordinator()
    journey = _journey()

    first = coordinator.conserve_journey_boundary(
        journey=journey,
        boundary="BLOCKED",
        stopping_reason="AMBIGUITY",
    )

    second = coordinator.conserve_journey_boundary(
        journey=journey,
        boundary="BLOCKED",
        stopping_reason="AMBIGUITY",
    )

    assert first.to_dict() == second.to_dict()

from pathlib import Path

from python.ai_platform.cognitive_coordination import (
    EpistemicCognitiveCoordinator,
    JourneyState,
)


def _journey(
    *,
    step_count=1,
    epistemic_gain=True,
    visited=("evidence:search",),
):
    return JourneyState(
        schema="FUSION-02-JOURNEY-STATE-1",
        journey_id="journey-productive",
        need_id="need-productive",
        status="IN_PROGRESS",
        step_count=step_count,
        epistemic_gain=epistemic_gain,
        visited=tuple(visited),
        stopping_reason="",
    )


def test_productive_journey_uses_existing_step_evaluator():
    coordinator = EpistemicCognitiveCoordinator()

    result = coordinator.evaluate_cognitive_step(
        journey=_journey(),
        outcome="PARTIAL",
        observation_identity="read:first.txt",
        epistemic_gain=True,
    )

    assert result["continue_navigation"] is True
    assert result["authority_conferred"] is False
    assert result["human_authority_preserved"] is True


def test_productive_journey_uses_existing_loop_guard():
    coordinator = EpistemicCognitiveCoordinator()

    result = coordinator.evaluate_cognitive_loop_guard(
        journey=_journey(),
        observation_identity="read:second.txt",
        capability="read",
        epistemic_gain=True,
    )

    assert result["continue_navigation"] is True
    assert result["bounded"] is True
    assert result["authority_conferred"] is False


def test_productive_journey_guard_blocks_cycle():
    coordinator = EpistemicCognitiveCoordinator()

    result = coordinator.evaluate_cognitive_loop_guard(
        journey=_journey(
            visited=(
                "evidence:search",
                "read:first.txt",
            )
        ),
        observation_identity="read:first.txt",
        capability="read",
        epistemic_gain=True,
    )

    assert result["continue_navigation"] is False
    assert result["stopping_reason"] in {
        "REPEATED_IDENTITY_CAPABILITY",
        "TRAVERSAL_CYCLE",
    }


def test_production_service_has_numeric_cognitive_bound():
    service = Path(
        "lib/python/ai_platform/service.py"
    ).read_text()

    assert "max_cognitive_steps = 8" in service
    assert "source_paths[:max_cognitive_steps]" in service


def test_production_service_does_not_create_parallel_organs():
    service = Path(
        "lib/python/ai_platform/service.py"
    ).read_text()

    forbidden = (
        "class ProductiveCognitiveCoordinator",
        "class CognitiveJourneyJournal",
        "class ProductiveWorkingContext",
        "class CognitiveMemory",
    )

    for token in forbidden:
        assert token not in service


def test_production_service_composes_multi_source_journey():
    service = Path(
        "lib/python/ai_platform/service.py"
    ).read_text()

    required = (
        "for selected_source_path in journey_source_paths:",
        "evaluate_cognitive_loop_guard(",
        "execute_read_navigation(",
        "attach_read_evidence(",
        "evaluate_cognitive_step(",
        '"read_navigations"',
        '"cognitive_loop_guards"',
        '"cognitive_step_evaluations"',
    )

    for token in required:
        assert token in service


def test_productive_journey_no_longer_selects_only_index_zero():
    service = Path(
        "lib/python/ai_platform/service.py"
    ).read_text()

    assert (
        "selected_source_path = journey_source_paths[0]"
        not in service
    )

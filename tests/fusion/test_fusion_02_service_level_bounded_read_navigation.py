from pathlib import Path

from python.ai_platform.cognitive_coordination import (
    InformationNeed,
    JourneyState,
    NavigationPlan,
)
from python.ai_platform.service import AIPlatformService


def repository_root():
    return Path(__file__).resolve().parents[2]


def restore_need(payload):
    return InformationNeed(
        schema=payload["schema"],
        need_id=payload["need_id"],
        question=payload["question"],
        objective=payload["objective"],
        epistemic_status=payload["epistemic_status"],
        research_required=payload["research_required"],
        requested_capabilities=tuple(
            payload["requested_capabilities"]
        ),
        constraints=dict(payload["constraints"]),
    )


def restore_plan(payload):
    return NavigationPlan(
        schema=payload["schema"],
        need_id=payload["need_id"],
        required=payload["required"],
        capabilities=tuple(payload["capabilities"]),
        read_only=payload["read_only"],
        authority_preserved=payload[
            "authority_preserved"
        ],
        working_context_materialized=payload[
            "working_context_materialized"
        ],
        retrieval_executed=payload[
            "retrieval_executed"
        ],
        stopping_conditions=tuple(
            payload["stopping_conditions"]
        ),
    )


def restore_journey(payload):
    return JourneyState(
        schema=payload["schema"],
        journey_id=payload["journey_id"],
        need_id=payload["need_id"],
        status=payload["status"],
        step_count=payload["step_count"],
        epistemic_gain=payload["epistemic_gain"],
        visited=tuple(payload["visited"]),
        stopping_reason=payload["stopping_reason"],
    )


def test_real_repository_productive_multi_source_physiology():
    root = repository_root()

    service = AIPlatformService(
        repository_root=str(root),
        workspace_root=str(root),
    )

    question = (
        "inspect repository cognitive coordination service"
    )

    coordination = (
        service.cognitive_coordinator.initialize(
            question,
            session_id="repository-physiology",
        )
    )

    need = restore_need(
        coordination["information_need"]
    )
    plan = restore_plan(
        coordination["navigation_plan"]
    )
    initial_journey = restore_journey(
        coordination["journey"]
    )

    search_navigation = (
        service.cognitive_coordinator
        .execute_search_navigation(
            plan=plan,
            journey=initial_journey,
            keyword=question,
            search=service.evidence_engine.find,
        )
    )

    retrieval = search_navigation["retrieval"]

    assert retrieval is not None
    assert retrieval["read_only"] is True
    assert retrieval["authority_conferred"] is False
    assert len(retrieval["source_paths"]) >= 2

    for source_path in retrieval["source_paths"]:
        candidate = Path(source_path)

        assert candidate.is_absolute() is False
        assert ".." not in candidate.parts
        assert (root / candidate).resolve().is_relative_to(
            root.resolve()
        )

    search_journey = restore_journey(
        search_navigation["journey"]
    )

    result = (
        service.activate_productive_bounded_journey(
            retrieval=retrieval,
            journey_state=search_journey,
            search_navigation=search_navigation,
        )
    )

    reads = result["read_navigations"]

    assert len(reads) >= 2
    assert len(reads) <= 8
    assert len(result["cognitive_loop_guards"]) == len(
        reads
    )
    assert len(
        result["cognitive_step_evaluations"]
    ) == len(reads)

    expected_paths = retrieval["source_paths"][
        :len(reads)
    ]

    assert [
        item["source_path"]
        for item in reads
    ] == expected_paths

    for observation in reads:
        source_path = observation["source_path"]
        source = root / source_path

        assert source.is_file()
        assert source.stat().st_size > 0
        assert source.read_text(encoding="utf-8")
        assert observation["status"] == "RETRIEVED"
        assert observation["content"] == (
            source.read_text(encoding="utf-8")
        )
        assert observation["read_only"] is True
        assert observation["bounded"] is True
        assert (
            observation["authority_conferred"]
            is False
        )

    final_journey = result["journey_state"]

    assert final_journey.step_count == (
        1 + len(reads)
    )
    assert final_journey.status == "PARTIAL"
    assert final_journey.stopping_reason in {
        "CANDIDATE_SOURCES_EXHAUSTED",
        "COGNITIVE_STEP_BOUND_REACHED",
    }

    working_context = (
        service.cognitive_coordinator
        .materialize_working_context(
            need=need,
            journey=final_journey,
            retrieval=result["retrieval"],
        )
    )

    context = working_context.to_dict()

    assert context["status"] == "MATERIALIZED"
    assert context["bounded"] is True
    assert context["authority_conferred"] is False
    assert context["human_authority_preserved"] is True

    observed = {
        item["source_path"]: item
        for item in context["evidence"]
        if "read_status" in item
    }

    for observation in reads:
        source_path = observation["source_path"]

        assert source_path in observed
        assert (
            observed[source_path]["content"]
            == observation["content"]
        )
        assert (
            observed[source_path]["read_status"]
            == "RETRIEVED"
        )


def test_real_missing_repository_source_remains_unknown():
    root = repository_root()

    service = AIPlatformService(
        repository_root=str(root),
        workspace_root=str(root),
    )

    result = (
        service.cognitive_coordinator
        .execute_read_navigation(
            "path-that-does-not-exist-anywhere.md",
            read=lambda repository, relative: (
                repository / relative
            ).read_text(encoding="utf-8"),
            repository_root=root,
        )
    )

    assert result["status"] == "UNKNOWN"
    assert result["epistemic_gain"] is False
    assert result["authority_conferred"] is False
    assert result["human_authority_preserved"] is True
    assert result["unknown_is_valid"] is True

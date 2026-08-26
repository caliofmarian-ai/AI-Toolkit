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


def real_search(service, question):
    coordination = (
        service.cognitive_coordinator.initialize(
            question,
            session_id="real-search-navigation",
        )
    )

    need = restore_need(
        coordination["information_need"]
    )
    plan = restore_plan(
        coordination["navigation_plan"]
    )
    journey = restore_journey(
        coordination["journey"]
    )

    navigation = (
        service.cognitive_coordinator
        .execute_search_navigation(
            plan=plan,
            journey=journey,
            keyword=question,
            search=service.evidence_engine.find,
        )
    )

    return need, plan, navigation


def test_real_search_materializes_real_working_context():
    root = repository_root()

    service = AIPlatformService(
        repository_root=str(root),
        workspace_root=str(root),
    )

    question = (
        "inspect repository cognitive coordination service"
    )

    need, plan, navigation = real_search(
        service,
        question,
    )

    retrieval = navigation["retrieval"]

    assert plan.required is True
    assert plan.read_only is True
    assert plan.authority_preserved is True
    assert retrieval is not None
    assert retrieval["read_only"] is True
    assert retrieval["authority_conferred"] is False
    assert retrieval[
        "working_context_materialized"
    ] is False
    assert len(retrieval["source_paths"]) >= 2

    for source_path in retrieval["source_paths"]:
        candidate = Path(source_path)

        assert candidate.is_absolute() is False
        assert ".." not in candidate.parts

        source = (root / candidate).resolve()

        assert source.is_relative_to(root.resolve())
        assert source.is_file()
        assert source.stat().st_size > 0
        assert source.read_text(encoding="utf-8")

    search_journey = restore_journey(
        navigation["journey"]
    )

    productive = (
        service.activate_productive_bounded_journey(
            retrieval=retrieval,
            journey_state=search_journey,
            search_navigation=navigation,
        )
    )

    working_context = (
        service.cognitive_coordinator
        .materialize_working_context(
            need=need,
            journey=productive["journey_state"],
            retrieval=productive["retrieval"],
        )
    )

    context = working_context.to_dict()

    assert context["status"] == "MATERIALIZED"
    assert context["bounded"] is True
    assert context["authority_conferred"] is False
    assert context["human_authority_preserved"] is True
    assert context["unknown_is_valid"] is True
    assert len(context["evidence"]) >= 2

    read_evidence = [
        item
        for item in context["evidence"]
        if item.get("read_status") == "RETRIEVED"
    ]

    assert len(read_evidence) >= 2

    for item in read_evidence:
        source = root / item["source_path"]

        assert item["content"] == source.read_text(
            encoding="utf-8"
        )
        assert item["read_only"] is True
        assert item["bounded"] is True
        assert item["authority_conferred"] is False


def test_real_non_research_need_remains_unknown():
    root = repository_root()

    service = AIPlatformService(
        repository_root=str(root),
        workspace_root=str(root),
    )

    question = "hello"

    need, plan, navigation = real_search(
        service,
        question,
    )

    assert plan.required is False
    assert navigation["retrieval"] is None

    journey = restore_journey(
        navigation["journey"]
    )

    working_context = (
        service.cognitive_coordinator
        .materialize_working_context(
            need=need,
            journey=journey,
            retrieval=None,
        )
    )

    context = working_context.to_dict()

    assert context["status"] == "UNKNOWN"
    assert context["source_paths"] == []
    assert context["evidence"] == []
    assert context["authority_conferred"] is False
    assert context["human_authority_preserved"] is True
    assert context["unknown_is_valid"] is True


def test_real_search_navigation_remains_read_only():
    root = repository_root()

    service = AIPlatformService(
        repository_root=str(root),
        workspace_root=str(root),
    )

    need, plan, navigation = real_search(
        service,
        "inspect repository evidence engine",
    )

    retrieval = navigation["retrieval"]

    assert need.research_required is True
    assert plan.required is True
    assert plan.read_only is True
    assert plan.authority_preserved is True
    assert plan.working_context_materialized is False
    assert retrieval is not None
    assert retrieval["capability"] == "search"
    assert retrieval["read_only"] is True
    assert retrieval["authority_conferred"] is False
    assert retrieval[
        "working_context_materialized"
    ] is False
    assert retrieval[
        "source_identity_kind"
    ] == "repository-relative-path"

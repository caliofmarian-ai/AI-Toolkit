from python.ai_platform.cognitive_coordination import (
    EpistemicCognitiveCoordinator,
)


def _initialized():
    coordinator = EpistemicCognitiveCoordinator()

    state = coordinator.initialize(
        "Inspect repository evidence for cognitive coordination",
        session_id="fusion02-search",
    )

    return coordinator, state


def test_first_search_navigation_executes_only_real_search_step():
    coordinator, state = _initialized()

    calls = []

    def search(keyword):
        calls.append(keyword)

        return {
            "python": [
                "lib/python/ai_platform/cognitive_coordination.py",
            ],
            "shell": [],
            "tests": [
                "tests/fusion/test_fusion_02_epistemic_navigation_plan.py",
            ],
            "docs": [],
            "semantic": {},
        }

    from python.ai_platform.cognitive_coordination import (
        JourneyState,
        NavigationPlan,
    )

    plan = NavigationPlan(
        schema=state["navigation_plan"]["schema"],
        need_id=state["navigation_plan"]["need_id"],
        required=state["navigation_plan"]["required"],
        capabilities=tuple(state["navigation_plan"]["capabilities"]),
        read_only=state["navigation_plan"]["read_only"],
        authority_preserved=state["navigation_plan"]["authority_preserved"],
        working_context_materialized=state["navigation_plan"][
            "working_context_materialized"
        ],
        retrieval_executed=state["navigation_plan"]["retrieval_executed"],
        stopping_conditions=tuple(
            state["navigation_plan"]["stopping_conditions"]
        ),
    )

    journey = JourneyState(
        schema=state["journey"]["schema"],
        journey_id=state["journey"]["journey_id"],
        need_id=state["journey"]["need_id"],
        status=state["journey"]["status"],
        step_count=state["journey"]["step_count"],
        epistemic_gain=state["journey"]["epistemic_gain"],
        visited=tuple(state["journey"]["visited"]),
        stopping_reason=state["journey"]["stopping_reason"],
    )

    result = coordinator.execute_search_navigation(
        plan=plan,
        journey=journey,
        keyword="cognitive",
        search=search,
    )

    assert calls == ["cognitive"]

    assert result["navigation_plan"]["retrieval_executed"] is True
    assert result["navigation_plan"]["working_context_materialized"] is False
    assert result["navigation_plan"]["authority_preserved"] is True

    assert result["journey"]["step_count"] == 1
    assert result["journey"]["epistemic_gain"] is True
    assert result["journey"]["status"] == "IN_PROGRESS"
    assert result["journey"]["visited"] == ["evidence:search"]

    retrieval = result["retrieval"]

    assert retrieval["capability"] == "search"
    assert retrieval["read_only"] is True
    assert retrieval["authority_conferred"] is False
    assert retrieval["working_context_materialized"] is False
    assert retrieval["source_identity_kind"] == "repository-relative-path"

    assert retrieval["source_paths"] == [
        "lib/python/ai_platform/cognitive_coordination.py",
        "tests/fusion/test_fusion_02_epistemic_navigation_plan.py",
    ]


def test_search_without_epistemic_gain_stops_legitimately():
    coordinator, state = _initialized()

    from python.ai_platform.cognitive_coordination import (
        JourneyState,
        NavigationPlan,
    )

    plan = NavigationPlan(
        schema=state["navigation_plan"]["schema"],
        need_id=state["navigation_plan"]["need_id"],
        required=True,
        capabilities=("search",),
        read_only=True,
        authority_preserved=True,
        working_context_materialized=False,
        retrieval_executed=False,
        stopping_conditions=("NO_EPISTEMIC_GAIN",),
    )

    journey = JourneyState(
        schema=state["journey"]["schema"],
        journey_id=state["journey"]["journey_id"],
        need_id=state["journey"]["need_id"],
        status="UNRESOLVED",
        step_count=0,
        epistemic_gain=False,
        visited=(),
        stopping_reason="",
    )

    result = coordinator.execute_search_navigation(
        plan=plan,
        journey=journey,
        keyword="absent-marker",
        search=lambda keyword: {
            "python": [],
            "shell": [],
            "tests": [],
            "docs": [],
            "semantic": {},
        },
    )

    assert result["navigation_plan"]["retrieval_executed"] is True
    assert result["journey"]["status"] == "NO_EPISTEMIC_GAIN"
    assert result["journey"]["epistemic_gain"] is False
    assert result["journey"]["stopping_reason"] == "NO_EPISTEMIC_GAIN"
    assert result["retrieval"]["source_paths"] == []


def test_search_is_not_executed_when_capability_not_requested():
    coordinator = EpistemicCognitiveCoordinator()

    from python.ai_platform.cognitive_coordination import (
        JourneyState,
        NavigationPlan,
    )

    plan = NavigationPlan(
        schema=coordinator.NAVIGATION_PLAN_SCHEMA,
        need_id="need-test",
        required=True,
        capabilities=("inspect",),
        read_only=True,
        authority_preserved=True,
        working_context_materialized=False,
        retrieval_executed=False,
        stopping_conditions=(),
    )

    journey = JourneyState(
        schema=coordinator.JOURNEY_SCHEMA,
        journey_id="journey-test",
        need_id="need-test",
        status="UNRESOLVED",
        step_count=0,
        epistemic_gain=False,
        visited=(),
        stopping_reason="",
    )

    called = False

    def forbidden_search(keyword):
        nonlocal called
        called = True
        raise AssertionError("search must not execute")

    result = coordinator.execute_search_navigation(
        plan=plan,
        journey=journey,
        keyword="anything",
        search=forbidden_search,
    )

    assert called is False
    assert result["retrieval"] is None
    assert result["navigation_plan"]["retrieval_executed"] is False
    assert result["journey"]["step_count"] == 0


def test_search_cannot_confer_authority_or_materialize_working_context():
    coordinator = EpistemicCognitiveCoordinator()

    from python.ai_platform.cognitive_coordination import (
        JourneyState,
        NavigationPlan,
    )

    journey = JourneyState(
        schema=coordinator.JOURNEY_SCHEMA,
        journey_id="journey-test",
        need_id="need-test",
        status="UNRESOLVED",
        step_count=0,
        epistemic_gain=False,
        visited=(),
        stopping_reason="",
    )

    bad_authority_plan = NavigationPlan(
        schema=coordinator.NAVIGATION_PLAN_SCHEMA,
        need_id="need-test",
        required=True,
        capabilities=("search",),
        read_only=True,
        authority_preserved=False,
        working_context_materialized=False,
        retrieval_executed=False,
        stopping_conditions=(),
    )

    try:
        coordinator.execute_search_navigation(
            plan=bad_authority_plan,
            journey=journey,
            keyword="x",
            search=lambda keyword: {},
        )
    except ValueError as exc:
        assert "Human authority" in str(exc)
    else:
        raise AssertionError("authority violation must fail")

    bad_context_plan = NavigationPlan(
        schema=coordinator.NAVIGATION_PLAN_SCHEMA,
        need_id="need-test",
        required=True,
        capabilities=("search",),
        read_only=True,
        authority_preserved=True,
        working_context_materialized=True,
        retrieval_executed=False,
        stopping_conditions=(),
    )

    try:
        coordinator.execute_search_navigation(
            plan=bad_context_plan,
            journey=journey,
            keyword="x",
            search=lambda keyword: {},
        )
    except ValueError as exc:
        assert "Working Context" in str(exc)
    else:
        raise AssertionError("working-context violation must fail")

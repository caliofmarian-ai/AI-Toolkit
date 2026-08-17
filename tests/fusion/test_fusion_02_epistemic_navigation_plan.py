from python.ai_platform.cognitive_coordination import (
    EpistemicCognitiveCoordinator,
)


def test_research_requirement_becomes_explicit_navigation_plan():
    coordinator = EpistemicCognitiveCoordinator()

    result = coordinator.initialize(
        "Inspect repository evidence for the implementation",
        session_id="navigation-alpha",
    )

    plan = result["navigation_plan"]

    assert plan["schema"] == "FUSION-02-NAVIGATION-PLAN-1"
    assert plan["required"] is True
    assert plan["capabilities"] == [
        "search",
        "resolve",
        "read",
        "inspect",
    ]
    assert plan["read_only"] is True
    assert plan["authority_preserved"] is True


def test_navigation_plan_does_not_execute_retrieval():
    coordinator = EpistemicCognitiveCoordinator()

    result = coordinator.initialize(
        "Audit repository evidence",
        session_id="navigation-no-retrieval",
    )

    plan = result["navigation_plan"]
    journey = result["journey"]

    assert plan["retrieval_executed"] is False
    assert plan["working_context_materialized"] is False

    assert journey["step_count"] == 0
    assert journey["visited"] == []
    assert journey["epistemic_gain"] is False


def test_navigation_plan_preserves_human_authority():
    coordinator = EpistemicCognitiveCoordinator()

    result = coordinator.initialize(
        "Inspect repository architecture",
        session_id="navigation-authority",
    )

    plan = result["navigation_plan"]
    need = result["information_need"]

    assert plan["authority_preserved"] is True
    assert plan["read_only"] is True
    assert need["constraints"]["retrieval_confers_authority"] is False
    assert need["constraints"]["human_authority_preserved"] is True


def test_navigation_plan_declares_stopping_conditions_before_navigation():
    coordinator = EpistemicCognitiveCoordinator()

    result = coordinator.initialize(
        "Inspect repository dependencies",
        session_id="navigation-stopping",
    )

    assert result["navigation_plan"]["stopping_conditions"] == [
        "NEED_SATISFIED",
        "NO_EPISTEMIC_GAIN",
        "UNKNOWN",
        "HUMAN_REQUIRED",
        "FORBIDDEN",
    ]


def test_non_research_need_has_no_navigation_capabilities():
    coordinator = EpistemicCognitiveCoordinator()

    result = coordinator.initialize(
        "hello",
        session_id="navigation-trivial",
    )

    plan = result["navigation_plan"]

    assert plan["required"] is False
    assert plan["capabilities"] == []
    assert plan["retrieval_executed"] is False
    assert plan["working_context_materialized"] is False
    assert plan["stopping_conditions"] == []


def test_navigation_plan_does_not_claim_unrequested_capabilities():
    coordinator = EpistemicCognitiveCoordinator()

    result = coordinator.initialize(
        "Audit repository code",
        session_id="navigation-bounded",
    )

    capabilities = result["navigation_plan"]["capabilities"]

    assert capabilities == [
        "search",
        "resolve",
        "read",
        "inspect",
    ]

    assert "write" not in capabilities
    assert "modify" not in capabilities
    assert "traverse" not in capabilities
    assert "trace_provenance" not in capabilities

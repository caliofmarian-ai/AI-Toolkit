from pathlib import Path

from python.ai_platform.cognitive_coordination import (
    EpistemicCognitiveCoordinator,
)


def research():
    c=EpistemicCognitiveCoordinator()

    initialized=c.initialize(
        "inspect repository implementation evidence",
        session_id="session-e17",
    )

    need_data=initialized["information_need"]
    plan_data=initialized["navigation_plan"]
    journey_data=initialized["journey"]

    need=c.formulate_need(
        need_data["question"]
    )
    evaluation=c.evaluate_need(need)

    need=type(need)(
        schema=need.schema,
        need_id=need.need_id,
        question=need.question,
        objective=need.objective,
        epistemic_status=need.epistemic_status,
        research_required=evaluation.research_required,
        requested_capabilities=evaluation.requested_capabilities,
        constraints=need.constraints,
    )

    plan=c.plan_navigation(
        need,
        evaluation,
    )

    journey=c.begin_journey(
        need,
        session_id="session-e17",
    )

    def search(keyword):
        return {
            "python": [
                "lib/python/ai_platform/pipeline.py",
                "lib/python/ai_platform/service.py",
            ],
            "shell": [],
            "tests": [
                "tests/fusion/test_fusion_02_e16_t12_default_cognitive_cutover.py",
            ],
            "docs": [],
            "semantic": {
                "lib/python/ai_platform/pipeline.py": {
                    "identity": "AIRequestPipeline",
                },
                "lib/python/ai_platform/service.py": {
                    "identity": "AIPlatformService",
                },
            },
        }

    nav=c.execute_search_navigation(
        plan=plan,
        journey=journey,
        keyword="cognitive",
        search=search,
    )

    return c, need, nav


def journey_from(c, data):
    from python.ai_platform.cognitive_coordination import JourneyState

    return JourneyState(
        schema=data["schema"],
        journey_id=data["journey_id"],
        need_id=data["need_id"],
        status=data["status"],
        step_count=data["step_count"],
        epistemic_gain=data["epistemic_gain"],
        visited=tuple(data["visited"]),
        stopping_reason=data["stopping_reason"],
    )


def test_research_need_uses_bounded_navigation():
    c, need, nav=research()

    assert need.research_required is True
    assert nav["retrieval"]["read_only"] is True
    assert nav["retrieval"]["authority_conferred"] is False
    assert nav["retrieval"]["working_context_materialized"] is False

    paths=nav["retrieval"]["source_paths"]

    assert len(paths) == 3
    assert len(paths) == len(set(paths))


def test_read_evidence_must_originate_from_retrieval():
    c, _, nav=research()

    observation=c.execute_read_navigation(
        "outside.py",
        read=lambda root, path: "outside",
        repository_root=Path("."),
    )

    try:
        c.attach_read_evidence(
            retrieval=nav["retrieval"],
            read_navigation=observation,
        )
    except ValueError as exc:
        assert "originate from retrieval" in str(exc)
    else:
        raise AssertionError(
            "foreign read evidence was accepted"
        )


def test_real_read_content_enters_bounded_working_context():
    c, need, nav=research()

    path=nav["retrieval"]["source_paths"][0]

    observation=c.execute_read_navigation(
        path,
        read=lambda root, relative: (
            "class AIRequestPipeline:\\n"
            "    pass\\n"
        ),
        repository_root=Path("."),
    )

    retrieval=c.attach_read_evidence(
        retrieval=nav["retrieval"],
        read_navigation=observation,
    )

    journey=journey_from(
        c,
        nav["journey"],
    )

    wc=c.materialize_working_context(
        need=need,
        journey=journey,
        retrieval=retrieval,
    )

    data=wc.to_dict()

    assert data["bounded"] is True
    assert data["authority_conferred"] is False
    assert data["human_authority_preserved"] is True

    evidence=[
        item
        for item in data["evidence"]
        if item["source_path"] == path
    ]

    assert len(evidence) == 1
    assert (
        evidence[0]["content"]
        == "class AIRequestPipeline:\\n    pass\\n"
    )
    assert evidence[0]["read_only"] is True
    assert evidence[0]["bounded"] is True


def test_read_evidence_has_matching_provenance():
    c, need, nav=research()

    path=nav["retrieval"]["source_paths"][0]

    observation=c.execute_read_navigation(
        path,
        read=lambda root, relative: "bounded evidence",
        repository_root=Path("."),
    )

    retrieval=c.attach_read_evidence(
        retrieval=nav["retrieval"],
        read_navigation=observation,
    )

    wc=c.materialize_working_context(
        need=need,
        journey=journey_from(
            c,
            nav["journey"],
        ),
        retrieval=retrieval,
    ).to_dict()

    evidence_paths={
        item["source_path"]
        for item in wc["evidence"]
    }

    provenance_paths={
        item["source_path"]
        for item in wc["provenance"]
    }

    assert evidence_paths == provenance_paths

    matched=[
        item
        for item in wc["provenance"]
        if item["source_path"] == path
    ]

    assert len(matched) == 1
    assert matched[0]["read_observed"] is True
    assert matched[0]["authority_conferred"] is False


def test_working_context_remains_selective():
    c, need, nav=research()

    retrieval=dict(nav["retrieval"])

    retrieval["source_paths"]=[
        f"source-{i}.py"
        for i in range(30)
    ]

    retrieval["result"]={
        "python": list(retrieval["source_paths"]),
        "shell": [],
        "tests": [],
        "docs": [],
        "semantic": {},
    }

    wc=c.materialize_working_context(
        need=need,
        journey=journey_from(
            c,
            nav["journey"],
        ),
        retrieval=retrieval,
    ).to_dict()

    assert len(wc["source_paths"]) == 8
    assert len(wc["evidence"]) == 8
    assert len(wc["provenance"]) == 8
    assert wc["bounded"] is True


def test_unknown_read_does_not_fabricate_evidence_content():
    c, need, nav=research()

    path=nav["retrieval"]["source_paths"][0]

    observation=c.execute_read_navigation(
        path,
        read=lambda root, relative: "",
        repository_root=Path("."),
    )

    assert observation["status"] == "UNKNOWN"
    assert observation["content"] == ""
    assert observation["epistemic_gain"] is False
    assert observation["authority_conferred"] is False

    retrieval=c.attach_read_evidence(
        retrieval=nav["retrieval"],
        read_navigation=observation,
    )

    wc=c.materialize_working_context(
        need=need,
        journey=journey_from(
            c,
            nav["journey"],
        ),
        retrieval=retrieval,
    ).to_dict()

    evidence=next(
        item
        for item in wc["evidence"]
        if item["source_path"] == path
    )

    assert evidence["read_status"] == "UNKNOWN"
    assert evidence["content"] == ""
    assert evidence["authority_conferred"] is False

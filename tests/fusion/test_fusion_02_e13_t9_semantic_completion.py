from python.ai_platform.cognitive_coordination import (
    EpistemicCognitiveCoordinator,
    InformationNeed,
    JourneyState,
)


def _need():
    return InformationNeed(
        schema="FUSION-02-INFORMATION-NEED-1",
        need_id="n13",
        question="Inspect relevant evidence",
        objective="ANSWER_HUMAN_REQUEST",
        epistemic_status="UNRESOLVED",
        research_required=True,
        requested_capabilities=("search", "read"),
        constraints={
            "human_authority_preserved": True,
            "retrieval_confers_authority": False,
        },
    )


def _journey():
    return JourneyState(
        schema="FUSION-02-JOURNEY-STATE-1",
        journey_id="j13",
        need_id="n13",
        status="IN_PROGRESS",
        step_count=3,
        epistemic_gain=True,
        visited=("search:a", "read:a.py", "read:b.py"),
        stopping_reason="",
    )


def test_t9_semantic_selective_context():
    c=EpistemicCognitiveCoordinator()

    retrieval={
        "capability":"read",
        "source_identity_kind":"repository-relative-path",
        "source_paths":["a.py","a.py","b.py"],
        "result":{
            "python":["a.py","b.py"],
            "semantic":{
                "a.py":{"identity":"organ.alpha"},
                "b.py":{"identity":"organ.beta"},
            },
        },
        "epistemic_class":"REPOSITORY_IMPLEMENTATION",
        "uncertainties":["runtime-unverified","runtime-unverified"],
        "relationships":[
            {
                "from":"organ.alpha",
                "relation":"depends_on",
                "to":"organ.beta",
            }
        ],
        "authority_conferred":False,
        "working_context_materialized":False,
    }

    x=c.materialize_working_context(
        need=_need(),
        journey=_journey(),
        retrieval=retrieval,
        max_sources=1,
    ).to_dict()

    assert x["source_paths"] == ["a.py"]
    assert x["semantic_identities"] == ["organ.alpha"]
    assert x["epistemic_classes"] == [
        "REPOSITORY_IMPLEMENTATION"
    ]
    assert x["uncertainties"] == ["runtime-unverified"]

    assert x["relationships"] == [
        {
            "from":"organ.alpha",
            "relation":"depends_on",
            "to":"organ.beta",
        }
    ]

    assert x["epistemic_results"] == [
        {
            "identity":"organ.alpha",
            "source_path":"a.py",
            "epistemic_class":"REPOSITORY_IMPLEMENTATION",
            "authority":"TECHNICAL_OBSERVATION",
        }
    ]

    assert x["authority_conferred"] is False
    assert x["human_authority_preserved"] is True

    assert len(x["source_paths"]) < len(
        retrieval["source_paths"]
    )

    assert "visited" not in x["journey_summary"]
    assert "b.py" not in x["source_paths"]


def test_t9_unknown_does_not_fabricate_evidence():
    c=EpistemicCognitiveCoordinator()

    x=c.materialize_working_context(
        need=_need(),
        journey=_journey(),
        retrieval=None,
    ).to_dict()

    assert x["status"] == "UNKNOWN"
    assert x["epistemic_results"] == []
    assert x["semantic_identities"] == []
    assert x["epistemic_classes"] == []
    assert x["relationships"] == []
    assert x["uncertainties"] == ["retrieval-unavailable"]
    assert x["unknown_is_valid"] is True

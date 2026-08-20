from python.ai_platform.cognitive_coordination import (
    EpistemicCognitiveCoordinator, InformationNeed, JourneyState
)

def test_t9_selective_working_context():
    c=EpistemicCognitiveCoordinator()
    need=InformationNeed(
        schema="FUSION-02-INFORMATION-NEED-1",
        need_id="n",
        question="inspect relevant evidence",
        objective="ANSWER_HUMAN_REQUEST",
        epistemic_status="UNRESOLVED",
        research_required=True,
        requested_capabilities=("search","read"),
        constraints={
            "human_authority_preserved":True,
            "retrieval_confers_authority":False,
        },
    )
    journey=JourneyState(
        schema="FUSION-02-JOURNEY-STATE-1",
        journey_id="j", need_id="n",
        status="IN_PROGRESS", step_count=2,
        epistemic_gain=True,
        visited=("search:a","read:a.py"),
        stopping_reason="",
    )
    retrieval={
        "capability":"search",
        "source_identity_kind":"repository-relative-path",
        "source_paths":["a.py","a.py","b.py"],
        "result":{"python":["a.py","b.py"]},
        "authority_conferred":False,
        "working_context_materialized":False,
    }

    x=c.materialize_working_context(
        need=need,journey=journey,retrieval=retrieval,max_sources=1
    ).to_dict()

    assert x["human_question"]=="inspect relevant evidence"
    assert x["constraints"]["human_authority_preserved"] is True
    assert x["source_paths"]==["a.py"]
    assert len(x["evidence"])==1
    assert x["provenance"][0]["source_path"]=="a.py"
    assert x["provenance"][0]["authority_conferred"] is False
    assert x["journey_summary"]["step_count"]==2
    assert "visited" not in x["journey_summary"]
    assert x["authority_conferred"] is False
    assert x["human_authority_preserved"] is True

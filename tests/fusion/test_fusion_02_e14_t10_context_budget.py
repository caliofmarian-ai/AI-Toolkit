import pytest

from python.ai_platform.cognitive_coordination import (
    ContextBudgetGovernor,
    WorkingContext,
)


def context():
    return WorkingContext(
        schema="FUSION-02-WORKING-CONTEXT-1",
        need_id="need",
        journey_id="journey",
        status="PARTIAL",
        human_question="Why does context overflow?",
        constraints={
            "human_authority_preserved": True,
            "retrieval_confers_authority": False,
        },
        source_identity_kind="repository-relative-path",
        source_paths=("a.py", "b.py"),
        evidence=(
            {
                "source_path":"a.py",
                "capability":"read",
                "result":"A"*300,
            },
            {
                "source_path":"b.py",
                "capability":"read",
                "result":"B"*300,
            },
        ),
        provenance=(
            {
                "source_path":"a.py",
                "authority_conferred":False,
            },
            {
                "source_path":"b.py",
                "authority_conferred":False,
            },
        ),
        epistemic_results=(
            {
                "identity":"a",
                "source_path":"a.py",
                "epistemic_class":"REPOSITORY_IMPLEMENTATION",
                "authority":"TECHNICAL_OBSERVATION",
            },
            {
                "identity":"b",
                "source_path":"b.py",
                "epistemic_class":"REPOSITORY_IMPLEMENTATION",
                "authority":"TECHNICAL_OBSERVATION",
            },
        ),
        semantic_identities=("a","b"),
        epistemic_classes=("REPOSITORY_IMPLEMENTATION",),
        uncertainties=("runtime-unverified",),
        relationships=(
            {
                "from":"a",
                "relation":"depends_on",
                "to":"b",
            },
        ),
        journey_summary={
            "status":"IN_PROGRESS",
            "step_count":3,
            "epistemic_gain":True,
            "stopping_reason":"",
        },
        authority_conferred=False,
        human_authority_preserved=True,
        unknown_is_valid=True,
        bounded=True,
    )


def test_budget_is_provider_capacity_minus_reserved_headroom():
    g=ContextBudgetGovernor()

    b=g.calculate_budget(
        provider_capacity=1000,
        reserved_orientation=100,
        reserved_question=50,
        reserved_instructions=100,
        reserved_answer=250,
    )

    assert b.available_context == 500


def test_unknown_provider_capacity_fails_closed():
    g=ContextBudgetGovernor()

    with pytest.raises(
        ValueError,
        match="provider capacity must be known",
    ):
        g.calculate_budget(
            provider_capacity=None,
            reserved_orientation=1,
            reserved_question=1,
            reserved_instructions=1,
            reserved_answer=1,
        )


def test_compaction_keeps_whole_evidence_and_matching_provenance():
    g=ContextBudgetGovernor()
    original=context()

    base=original.to_dict()
    base["evidence"]=[]
    base["provenance"]=[]
    base["epistemic_results"]=[]
    base["relationships"]=[]

    first=dict(base)
    first["evidence"]=[original.to_dict()["evidence"][0]]
    first["provenance"]=[original.to_dict()["provenance"][0]]
    first["epistemic_results"]=[
        original.to_dict()["epistemic_results"][0]
    ]
    first["relationships"]=original.to_dict()["relationships"]

    available=g.estimate_units(first)+5

    b=g.calculate_budget(
        provider_capacity=available+40,
        reserved_orientation=10,
        reserved_question=10,
        reserved_instructions=10,
        reserved_answer=10,
    )

    governed=g.govern(
        working_context=original,
        budget=b,
    )

    assert governed.rejected is False
    assert governed.compacted is True
    assert (
        governed.estimated_context_units
        <= b.available_context
    )

    evidence=governed.context["evidence"]
    provenance=governed.context["provenance"]
    results=governed.context["epistemic_results"]

    assert len(evidence) == 1
    assert len(provenance) == 1
    assert len(results) == 1

    path=evidence[0]["source_path"]

    assert provenance[0]["source_path"] == path
    assert results[0]["source_path"] == path

    assert evidence[0]["result"] == "A"*300


def test_hard_overflow_rejects_instead_of_corrupting_object():
    g=ContextBudgetGovernor()
    original=context()

    b=g.calculate_budget(
        provider_capacity=41,
        reserved_orientation=10,
        reserved_question=10,
        reserved_instructions=10,
        reserved_answer=10,
    )

    governed=g.govern(
        working_context=original,
        budget=b,
    )

    assert governed.rejected is True
    assert governed.context == {}
    assert governed.rejection_reason == "HARD_CONTEXT_OVERFLOW"


def test_governance_does_not_mutate_working_context():
    g=ContextBudgetGovernor()
    original=context()
    before=original.to_dict()

    b=g.calculate_budget(
        provider_capacity=1000,
        reserved_orientation=50,
        reserved_question=50,
        reserved_instructions=50,
        reserved_answer=200,
    )

    g.govern(
        working_context=original,
        budget=b,
    )

    assert original.to_dict() == before

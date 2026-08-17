from __future__ import annotations

from python.ai_platform.cognitive_coordination import (
    EpistemicCognitiveCoordinator,
)


def _initialized():
    coordinator = EpistemicCognitiveCoordinator()

    state = coordinator.initialize(
        "Inspect repository implementation evidence",
        session_id="working-context-test",
    )

    need = coordinator.formulate_need(
        "Inspect repository implementation evidence"
    )

    evaluated = coordinator.evaluate_need(need)

    need = type(need)(
        schema=need.schema,
        need_id=need.need_id,
        question=need.question,
        objective=need.objective,
        epistemic_status=need.epistemic_status,
        research_required=evaluated.research_required,
        requested_capabilities=evaluated.requested_capabilities,
        constraints=need.constraints,
    )

    journey = coordinator.begin_journey(
        need,
        session_id="working-context-test",
    )

    return coordinator, need, journey, state


def test_working_context_materializes_bounded_candidate_evidence():
    coordinator, need, journey, _ = _initialized()

    retrieval = {
        "schema": "FUSION-02-READ-ONLY-SEARCH-1",
        "capability": "search",
        "keyword": "implementation",
        "read_only": True,
        "authority_conferred": False,
        "working_context_materialized": False,
        "source_identity_kind": "repository-relative-path",
        "source_paths": [
            "lib/python/a.py",
            "lib/python/b.py",
            "tests/test_a.py",
            "docs/design.md",
        ],
        "result": {
            "python": [
                "lib/python/a.py",
                "lib/python/b.py",
            ],
            "tests": [
                "tests/test_a.py",
            ],
            "docs": [
                "docs/design.md",
            ],
            "shell": [],
            "semantic": {},
        },
    }

    context = coordinator.materialize_working_context(
        need=need,
        journey=journey,
        retrieval=retrieval,
        max_sources=2,
    )

    assert context.schema == "FUSION-02-WORKING-CONTEXT-1"
    assert context.need_id == need.need_id
    assert context.journey_id == journey.journey_id
    assert context.status == "MATERIALIZED"

    assert context.source_paths == (
        "lib/python/a.py",
        "lib/python/b.py",
    )

    assert len(context.evidence) == 2

    assert context.evidence[0]["source_path"] == "lib/python/a.py"
    assert context.evidence[0]["families"] == ["python"]

    assert context.authority_conferred is False
    assert context.human_authority_preserved is True
    assert context.unknown_is_valid is True
    assert context.bounded is True


def test_working_context_does_not_copy_raw_search_result():
    coordinator, need, journey, _ = _initialized()

    retrieval = {
        "schema": "FUSION-02-READ-ONLY-SEARCH-1",
        "capability": "search",
        "keyword": "implementation",
        "read_only": True,
        "authority_conferred": False,
        "working_context_materialized": False,
        "source_identity_kind": "repository-relative-path",
        "source_paths": [
            "lib/python/a.py",
        ],
        "result": {
            "python": [
                "lib/python/a.py",
            ],
            "tests": [],
            "docs": [],
            "shell": [],
            "semantic": {
                "large-unselected-object": {
                    "must_not": "be copied wholesale"
                }
            },
        },
    }

    context = coordinator.materialize_working_context(
        need=need,
        journey=journey,
        retrieval=retrieval,
    )

    serialized = context.to_dict()

    assert "result" not in serialized
    assert "keyword" not in serialized
    assert "large-unselected-object" not in str(serialized)

    assert serialized["source_paths"] == [
        "lib/python/a.py",
    ]


def test_working_context_preserves_unknown_without_retrieval():
    coordinator, need, journey, _ = _initialized()

    context = coordinator.materialize_working_context(
        need=need,
        journey=journey,
        retrieval=None,
    )

    assert context.status == "UNKNOWN"
    assert context.source_paths == ()
    assert context.evidence == ()
    assert context.authority_conferred is False
    assert context.human_authority_preserved is True
    assert context.unknown_is_valid is True


def test_working_context_preserves_unknown_when_search_has_no_evidence():
    coordinator, need, journey, _ = _initialized()

    retrieval = {
        "schema": "FUSION-02-READ-ONLY-SEARCH-1",
        "capability": "search",
        "keyword": "nothing",
        "read_only": True,
        "authority_conferred": False,
        "working_context_materialized": False,
        "source_identity_kind": "repository-relative-path",
        "source_paths": [],
        "result": {
            "python": [],
            "tests": [],
            "docs": [],
            "shell": [],
            "semantic": {},
        },
    }

    context = coordinator.materialize_working_context(
        need=need,
        journey=journey,
        retrieval=retrieval,
    )

    assert context.status == "UNKNOWN"
    assert context.source_paths == ()
    assert context.evidence == ()


def test_working_context_rejects_authority_promotion():
    coordinator, need, journey, _ = _initialized()

    retrieval = {
        "authority_conferred": True,
        "working_context_materialized": False,
        "source_identity_kind": "repository-relative-path",
        "source_paths": [],
        "result": {},
    }

    try:
        coordinator.materialize_working_context(
            need=need,
            journey=journey,
            retrieval=retrieval,
        )
    except ValueError as exc:
        assert "must not confer epistemic authority" in str(exc)
    else:
        raise AssertionError(
            "Working Context accepted retrieval that conferred authority"
        )


def test_working_context_rejects_non_repository_source_identity():
    coordinator, need, journey, _ = _initialized()

    retrieval = {
        "authority_conferred": False,
        "working_context_materialized": False,
        "source_identity_kind": "invented-location",
        "source_paths": [
            "lib/python/a.py",
        ],
        "result": {},
    }

    try:
        coordinator.materialize_working_context(
            need=need,
            journey=journey,
            retrieval=retrieval,
        )
    except ValueError as exc:
        assert "repository-relative source identity" in str(exc)
    else:
        raise AssertionError(
            "Working Context accepted unverified source identity"
        )


def test_working_context_rejects_already_materialized_retrieval():
    coordinator, need, journey, _ = _initialized()

    retrieval = {
        "authority_conferred": False,
        "working_context_materialized": True,
        "source_identity_kind": "repository-relative-path",
        "source_paths": [],
        "result": {},
    }

    try:
        coordinator.materialize_working_context(
            need=need,
            journey=journey,
            retrieval=retrieval,
        )
    except ValueError as exc:
        assert "exactly once" in str(exc)
    else:
        raise AssertionError(
            "Working Context accepted already materialized retrieval"
        )

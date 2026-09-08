from copy import deepcopy
from pathlib import Path

from python.ai_platform.service import AIPlatformService


def test_service_reads_bounded_candidate_sources_productively(
    monkeypatch,
    tmp_path,
):
    first = tmp_path / "first.txt"
    second = tmp_path / "second.txt"

    first.write_text(
        "FIRST-SELECTED-SOURCE",
        encoding="utf-8",
    )

    second.write_text(
        "SECOND-SELECTED-SOURCE",
        encoding="utf-8",
    )

    service = AIPlatformService(
        repository_root=str(tmp_path),
        workspace_root=str(tmp_path),
    )

    session = {
        "id": "fusion02-read-session",
        "raw_sources": [],
        "selected_provider": "provider-alpha",
        "selected_model": "model-alpha",
    }

    experience = type(
        "Experience",
        (),
        {"experience_id": "experience-read"},
    )()

    monkeypatch.setattr(
        service.settings,
        "load",
        lambda: {},
    )

    monkeypatch.setattr(
        service.prompt_library,
        "resolve",
        lambda prompt_name, fallback: fallback,
    )

    monkeypatch.setattr(
        service.sessions,
        "create",
        lambda payload: deepcopy(session),
    )

    monkeypatch.setattr(
        service.conversation_experience,
        "ensure_experience",
        lambda current_session: (
            experience,
            {},
        ),
    )

    monkeypatch.setattr(
        service.sessions,
        "bind_experience",
        lambda *args: deepcopy(session),
    )

    monkeypatch.setattr(
        service.conversation_experience,
        "raw_source",
        lambda **kwargs: {
            "actor": kwargs["actor"],
            "content": kwargs["content"],
        },
    )

    monkeypatch.setattr(
        service.sessions,
        "append_raw_source",
        lambda *args: deepcopy(session),
    )

    monkeypatch.setattr(
        service.sessions,
        "append_interaction",
        lambda *args: deepcopy(session),
    )

    monkeypatch.setattr(
        service.conversation_context,
        "build",
        lambda *args, **kwargs: {
            "schema": "LEGACY-CONTEXT-1",
            "conversation": {
                "preserved": True,
            },
        },
    )

    cognitive_state = service.cognitive_coordinator.initialize(
        "inspect selected source",
        session_id=session["id"],
    )

    monkeypatch.setattr(
        service.cognitive_coordinator,
        "initialize",
        lambda *args, **kwargs: deepcopy(
            cognitive_state
        ),
    )

    search_navigation = {
        "navigation_plan": deepcopy(
            cognitive_state["navigation_plan"]
        ),
        "journey": deepcopy(
            cognitive_state["journey"]
        ),
        "retrieval": {
            "schema": "FUSION-02-READ-ONLY-SEARCH-1",
            "capability": "search",
            "keyword": "selected source",
            "read_only": True,
            "authority_conferred": False,
            "working_context_materialized": False,
            "source_identity_kind": (
                "repository-relative-path"
            ),
            "source_paths": [
                "first.txt",
                "second.txt",
            ],
            "result": {
                "python": [],
                "tests": [],
            },
        },
    }

    monkeypatch.setattr(
        service.cognitive_coordinator,
        "execute_search_navigation",
        lambda *args, **kwargs: deepcopy(
            search_navigation
        ),
    )

    captured = {}

    def pipeline_run(
        question,
        settings,
        *,
        provider_id="",
        model="",
        context_override=None,
    ):
        captured["context"] = deepcopy(
            context_override
        )

        return {
            "answer": "answer",
            "provider": (
                provider_id or "provider-alpha"
            ),
            "model": model or "model-alpha",
            "usage": {},
        }

    monkeypatch.setattr(
        service.pipeline,
        "run",
        pipeline_run,
    )

    result = service.ask_repository(
        "inspect selected source",
        provider_id="provider-alpha",
        model="model-alpha",
    )

    serialized = repr(result)

    assert "FIRST-SELECTED-SOURCE" in serialized
    assert "SECOND-SELECTED-SOURCE" in serialized

    assert (
        result["search_navigation"]["retrieval"][
            "source_paths"
        ]
        == [
            "first.txt",
            "second.txt",
        ]
    )

    read_observation = result.get(
        "read_navigation"
    )

    if read_observation is None:
        read_observation = result.get(
            "service_read_navigation"
        )

    assert read_observation is not None
    assert read_observation["source_path"] == "first.txt"
    assert read_observation["bounded"] is True
    assert read_observation["read_only"] is True
    assert read_observation["authority_conferred"] is False

    read_navigations = result["read_navigations"]

    assert [
        item["source_path"]
        for item in read_navigations
    ] == [
        "first.txt",
        "second.txt",
    ]

    assert [
        item["status"]
        for item in read_navigations
    ] == [
        "RETRIEVED",
        "RETRIEVED",
    ]

    assert len(result["cognitive_loop_guards"]) == 2
    assert len(result["cognitive_step_evaluations"]) == 2

    assert result["journey"]["step_count"] == 3
    assert result["journey"]["status"] == "PARTIAL"

    assert (
        result["journey"]["stopping_reason"]
        == "CANDIDATE_SOURCES_EXHAUSTED"
    )

    evidence = result["working_context"]["evidence"]

    assert [
        item.get("read_status")
        for item in evidence
    ] == [
        "RETRIEVED",
        "RETRIEVED",
    ]

    assert (
        "FIRST-SELECTED-SOURCE"
        in evidence[0]["content"]
    )

    assert (
        "SECOND-SELECTED-SOURCE"
        in evidence[1]["content"]
    )

    assert (
        result["search_navigation"]["retrieval"][
            "authority_conferred"
        ]
        is False
    )


def test_service_preserves_unknown_when_selected_source_missing(
    monkeypatch,
    tmp_path,
):
    service = AIPlatformService(
        repository_root=str(tmp_path),
        workspace_root=str(tmp_path),
    )

    result = service.cognitive_coordinator.execute_read_navigation(
        "missing.txt",
        read=lambda root, path: (
            Path(root) / path
        ).read_text(encoding="utf-8"),
        repository_root=tmp_path,
    )

    assert result["status"] == "UNKNOWN"
    assert result["epistemic_gain"] is False
    assert result["authority_conferred"] is False
    assert result["human_authority_preserved"] is True
    assert result["unknown_is_valid"] is True

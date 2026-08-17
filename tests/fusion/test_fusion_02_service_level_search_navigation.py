from __future__ import annotations

from copy import deepcopy
from pathlib import Path

from python.ai_platform.service import AIPlatformService


def _prepare_service(service, monkeypatch):
    session = {
        "id": "FUSION02-SERVICE",
        "selected_provider": "provider-alpha",
        "selected_model": "model-alpha",
        "raw_sources": [],
    }

    experience = type(
        "Experience",
        (),
        {"experience_id": "FUSION02-EXPERIENCE"},
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
        service.sessions,
        "get",
        lambda session_id: deepcopy(session),
    )

    monkeypatch.setattr(
        service.conversation_experience,
        "ensure_experience",
        lambda current_session: (experience, {}),
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
        lambda session_id, source: deepcopy(session),
    )

    monkeypatch.setattr(
        service.sessions,
        "append_interaction",
        lambda *args: deepcopy(session),
    )

    return session


def test_service_search_working_context_provider_order(
    monkeypatch,
    tmp_path,
):
    service = AIPlatformService(
        repository_root=str(tmp_path),
        workspace_root=str(tmp_path),
    )

    _prepare_service(service, monkeypatch)

    events = []

    reconstructed = {
        "schema": "LEGACY-CONTEXT-1",
        "conversation": {
            "durable": True,
            "marker": "PRESERVE-ME",
        },
        "persistent_experience": {
            "preserved": True,
        },
    }

    def build_context(*args, **kwargs):
        events.append("context")
        return deepcopy(reconstructed)

    monkeypatch.setattr(
        service.conversation_context,
        "build",
        build_context,
    )

    def bounded_search(keyword):
        events.append("search")
        return {
            "docs": [],
            "python": [
                "lib/python/alpha.py",
            ],
            "shell": [],
            "tests": [
                "tests/test_alpha.py",
            ],
            "semantic": {},
            "raw_secret_marker": (
                "MUST-NOT-ENTER-WORKING-CONTEXT"
            ),
        }

    monkeypatch.setattr(
        service.evidence_engine,
        "find",
        bounded_search,
    )

    captured = {}

    def provider_run(
        prompt,
        settings,
        *,
        provider_id="",
        model="",
        context_override=None,
    ):
        events.append("provider")
        captured["context"] = deepcopy(
            context_override
        )

        return {
            "answer": "provider-answer",
            "provider": provider_id or "provider-alpha",
            "model": model or "model-alpha",
            "usage": {},
        }

    monkeypatch.setattr(
        service.pipeline,
        "run",
        provider_run,
    )

    result = service.ask_repository(
        "inspect repository implementation",
        provider_id="provider-alpha",
        model="model-alpha",
    )

    assert events == [
        "search",
        "context",
        "provider",
    ]

    provider_context = captured["context"]

    assert provider_context["schema"] == (
        "LEGACY-CONTEXT-1"
    )

    assert provider_context["conversation"] == {
        "durable": True,
        "marker": "PRESERVE-ME",
    }

    assert provider_context[
        "persistent_experience"
    ] == {
        "preserved": True,
    }

    assert "working_context" in provider_context

    working = provider_context["working_context"]

    assert working["bounded"] is True
    assert working["authority_conferred"] is False
    assert working[
        "human_authority_preserved"
    ] is True
    assert working["unknown_is_valid"] is True

    assert working["source_identity_kind"] == (
        "repository-relative-path"
    )

    assert working["source_paths"] == [
        "lib/python/alpha.py",
        "tests/test_alpha.py",
    ]

    serialized = repr(working)

    assert (
        "MUST-NOT-ENTER-WORKING-CONTEXT"
        not in serialized
    )
    assert "raw_secret_marker" not in serialized
    assert "result" not in working

    assert result["working_context"] == working
    assert result["context"] == provider_context

    assert result["search_navigation"][
        "retrieval"
    ]["capability"] == "search"


def test_service_unknown_working_context_without_research(
    monkeypatch,
    tmp_path,
):
    service = AIPlatformService(
        repository_root=str(tmp_path),
        workspace_root=str(tmp_path),
    )

    _prepare_service(service, monkeypatch)

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

    captured = {}

    def provider_run(
        prompt,
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
            "answer": "provider-answer",
            "provider": provider_id or "provider-alpha",
            "model": model or "model-alpha",
            "usage": {},
        }

    monkeypatch.setattr(
        service.pipeline,
        "run",
        provider_run,
    )

    result = service.ask_repository(
        "hello",
        provider_id="provider-alpha",
        model="model-alpha",
    )

    assert result["search_navigation"] is None

    working = result["working_context"]

    assert working["status"] == "UNKNOWN"
    assert working["source_paths"] == []
    assert working["evidence"] == []
    assert working["authority_conferred"] is False
    assert working[
        "human_authority_preserved"
    ] is True
    assert working["unknown_is_valid"] is True
    assert working["bounded"] is True

    assert captured["context"][
        "conversation"
    ] == {
        "preserved": True,
    }

    assert captured["context"][
        "working_context"
    ] == working


def test_service_search_remains_read_only(
    tmp_path,
):
    root = Path(tmp_path)

    marker = root / "controlled-evidence.md"
    marker.write_text(
        "controlled read-only evidence\n",
        encoding="utf-8",
    )

    before = marker.read_bytes()

    service = AIPlatformService(
        repository_root=str(root),
        workspace_root=str(root),
    )

    result = service.evidence_engine.find(
        "controlled-evidence"
    )

    after = marker.read_bytes()

    assert before == after
    assert "controlled-evidence.md" in result["docs"]

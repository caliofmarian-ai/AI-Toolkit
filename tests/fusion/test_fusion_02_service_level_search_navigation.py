from __future__ import annotations

from pathlib import Path

from python.ai_platform.service import AIPlatformService


def test_service_executes_bounded_search_navigation_before_provider(
    monkeypatch,
    tmp_path,
):
    service = AIPlatformService(
        repository_root=str(tmp_path),
        workspace_root=str(tmp_path),
    )

    events = []

    service.settings.load = lambda: {}

    service.prompt_library.resolve = (
        lambda prompt_name, fallback: fallback
    )

    service.conversation_experience.ensure_experience = lambda session: (
        type("Experience", (), {"experience_id": "EXP-SERVICE-SEARCH"})(),
        None,
    )

    service.conversation_experience.raw_source = (
        lambda **kwargs: {
            "actor": kwargs["actor"],
            "content": kwargs["content"],
        }
    )

    session = {
        "id": "SESSION-SERVICE-SEARCH",
        "selected_provider": "",
        "selected_model": "",
        "raw_sources": [],
    }

    service.sessions.create = lambda payload: dict(session)
    service.sessions.get = lambda session_id: dict(session)
    service.sessions.bind_experience = (
        lambda session_id, experience_id: dict(session)
    )
    service.sessions.append_raw_source = (
        lambda session_id, raw_source: dict(
            session,
            raw_sources=[
                *session.get("raw_sources", []),
                raw_source,
            ],
        )
    )
    service.sessions.append_interaction = (
        lambda session_id, question, answer, usage: dict(session)
    )

    navigation_plan = {
        "requested_capabilities": ["search"],
        "search": {
            "keyword": "cognitive_coordination",
        },
    }

    service.cognitive_coordinator.initialize = (
        lambda question, session_id: {
            "information_need": {
                "raw_source": question,
            },
            "journey": {
                "state": "INITIAL",
            },
            "navigation_plan": navigation_plan,
        }
    )

    def execute_search(plan, *, evidence_engine):
        events.append("search")
        assert plan is navigation_plan
        assert evidence_engine is service.evidence_engine
        return {
            "capability": "search",
            "status": "EXECUTED",
            "source_identity": "repository-relative-path",
            "results": {
                "docs": [],
                "python": [
                    "lib/python/ai_platform/cognitive_coordination.py",
                ],
                "shell": [],
                "tests": [],
                "semantic": {},
            },
        }

    service.cognitive_coordinator.execute_search_navigation = execute_search

    def build_context(session_id, partner_identity):
        events.append("context")
        return {
            "schema": "test-context/v1",
        }

    service.conversation_context.build = build_context

    def provider_run(
        prompt,
        settings,
        *,
        provider_id="",
        model="",
        context_override=None,
    ):
        events.append("provider")
        return {
            "answer": "provider-answer",
            "provider": "test-provider",
            "model": "test-model",
            "usage": {},
        }

    service.pipeline.run = provider_run

    result = service.ask_repository(
        "Find cognitive coordination evidence",
        session_id="SESSION-SERVICE-SEARCH",
    )

    assert events == [
        "search",
        "context",
        "provider",
    ]

    assert result["search_navigation"]["capability"] == "search"
    assert result["search_navigation"]["status"] == "EXECUTED"
    assert (
        result["search_navigation"]["source_identity"]
        == "repository-relative-path"
    )

    assert "working_context" not in result
    assert "resolved_navigation" not in result
    assert "read_navigation" not in result
    assert "inspect_navigation" not in result


def test_service_does_not_execute_search_when_plan_does_not_authorize_it(
    monkeypatch,
    tmp_path,
):
    service = AIPlatformService(
        repository_root=str(tmp_path),
        workspace_root=str(tmp_path),
    )

    service.settings.load = lambda: {}
    service.prompt_library.resolve = (
        lambda prompt_name, fallback: fallback
    )

    service.conversation_experience.ensure_experience = lambda session: (
        type("Experience", (), {"experience_id": "EXP-NO-SEARCH"})(),
        None,
    )

    service.conversation_experience.raw_source = (
        lambda **kwargs: {
            "actor": kwargs["actor"],
            "content": kwargs["content"],
        }
    )

    session = {
        "id": "SESSION-NO-SEARCH",
        "selected_provider": "",
        "selected_model": "",
        "raw_sources": [],
    }

    service.sessions.create = lambda payload: dict(session)
    service.sessions.get = lambda session_id: dict(session)
    service.sessions.bind_experience = (
        lambda session_id, experience_id: dict(session)
    )
    service.sessions.append_raw_source = (
        lambda session_id, raw_source: dict(session)
    )
    service.sessions.append_interaction = (
        lambda session_id, question, answer, usage: dict(session)
    )

    service.cognitive_coordinator.initialize = (
        lambda question, session_id: {
            "information_need": {
                "raw_source": question,
            },
            "journey": {
                "state": "INITIAL",
            },
            "navigation_plan": None,
        }
    )

    def forbidden_search(*args, **kwargs):
        raise AssertionError("search must not execute without navigation plan")

    service.cognitive_coordinator.execute_search_navigation = forbidden_search

    service.conversation_context.build = (
        lambda session_id, partner_identity: {
            "schema": "test-context/v1",
        }
    )

    service.pipeline.run = (
        lambda prompt, settings, **kwargs: {
            "answer": "provider-answer",
            "provider": "test-provider",
            "model": "test-model",
            "usage": {},
        }
    )

    result = service.ask_repository(
        "ordinary request",
        session_id="SESSION-NO-SEARCH",
    )

    assert result["search_navigation"] is None


def test_service_search_integration_does_not_mutate_repository(
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

    result = service.evidence_engine.find("controlled-evidence")

    after = marker.read_bytes()

    assert before == after
    assert "controlled-evidence.md" in result["docs"]

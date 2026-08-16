from __future__ import annotations

import os

from python.dashboard.service import EngineeringDashboardService
from python.runtime.owner_access import (
    OWNER_SESSION_COOKIE,
    OwnerAccessBoundary,
)


def test_owner_web_session_is_derived_not_raw_secret(monkeypatch):
    monkeypatch.setenv(
        "AI_TOOLKIT_OWNER_TOKEN",
        "fusion-02-test-owner-secret",
    )
    boundary = OwnerAccessBoundary()
    cookie_value = boundary.session_cookie_value()

    assert cookie_value
    assert cookie_value != "fusion-02-test-owner-secret"
    assert "fusion-02-test-owner-secret" not in cookie_value


def test_owner_cookie_authenticates_existing_boundary(monkeypatch):
    monkeypatch.setenv(
        "AI_TOOLKIT_OWNER_TOKEN",
        "fusion-02-test-owner-secret",
    )
    boundary = OwnerAccessBoundary()
    cookie = (
        f"{OWNER_SESSION_COOKIE}="
        f"{boundary.session_cookie_value()}"
    )

    decision = boundary.authenticate_request(
        {"Cookie": cookie}
    )

    assert decision.authenticated is True
    assert decision.role == "OWNER"
    assert decision.human_authority is True


def test_invalid_owner_cookie_fails_closed(monkeypatch):
    monkeypatch.setenv(
        "AI_TOOLKIT_OWNER_TOKEN",
        "fusion-02-test-owner-secret",
    )
    boundary = OwnerAccessBoundary()

    decision = boundary.authenticate_request(
        {
            "Cookie": (
                f"{OWNER_SESSION_COOKIE}=not-valid"
            )
        }
    )

    assert decision.authenticated is False
    assert decision.human_authority is False


def test_existing_bearer_contract_remains_valid(monkeypatch):
    monkeypatch.setenv(
        "AI_TOOLKIT_OWNER_TOKEN",
        "fusion-02-test-owner-secret",
    )
    boundary = OwnerAccessBoundary()

    decision = boundary.authenticate_request(
        {
            "Authorization": (
                "Bearer fusion-02-test-owner-secret"
            )
        }
    )

    assert decision.authenticated is True
    assert decision.role == "OWNER"


def test_ai_control_center_contains_real_chat_surface(tmp_path):
    service = EngineeringDashboardService(
        repository_root=str(tmp_path),
        workspace_root=str(tmp_path),
    )

    control = {
        "providers": [
            {
                "id": "openai",
                "provider_id": "openai",
                "name": "OpenAI",
                "connection": True,
                "models": ["gpt-4.1"],
            }
        ]
    }

    html = service._owner_ai_chat_panel(control)

    assert 'id="chat-form"' in html
    assert 'id="chat-question"' in html
    assert 'id="chat-session"' in html
    assert 'id="chat-provider"' in html
    assert "/api/ai/chat" in html
    assert "/api/ai/sessions" in html
    assert "AI Partner is working" in html
    assert "RAW conversation" in html
    assert "Evidence or Canon" in html


def test_chat_ui_does_not_embed_owner_secret(
    tmp_path,
    monkeypatch,
):
    secret = "MUST-NOT-APPEAR-IN-HTML"
    monkeypatch.setenv(
        "AI_TOOLKIT_OWNER_TOKEN",
        secret,
    )

    service = EngineeringDashboardService(
        repository_root=str(tmp_path),
        workspace_root=str(tmp_path),
    )

    html = service._owner_ai_chat_panel(
        {
            "providers": [
                {
                    "id": "openai",
                    "name": "OpenAI",
                    "connection": True,
                    "models": ["gpt-4.1"],
                }
            ]
        }
    )

    assert secret not in html
    assert "AI_TOOLKIT_OWNER_TOKEN" not in html


def test_chat_uses_same_origin_cookie_not_js_owner_token(
    tmp_path,
):
    service = EngineeringDashboardService(
        repository_root=str(tmp_path),
        workspace_root=str(tmp_path),
    )

    html = service._owner_ai_chat_panel(
        {
            "providers": [
                {
                    "id": "openai",
                    "name": "OpenAI",
                    "connection": True,
                    "models": ["gpt-4.1"],
                }
            ]
        }
    )

    assert 'credentials:"same-origin"' in html
    assert "Authorization" not in html
    assert "Bearer " not in html


def test_session_readback_uses_existing_ai_session_engine():
    from python.ai_platform.sessions import AISessionEngine

    assert hasattr(AISessionEngine, "list_sessions")
    assert hasattr(AISessionEngine, "get")
    assert hasattr(AISessionEngine, "conversation_sources")

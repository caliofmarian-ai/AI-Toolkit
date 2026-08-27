from __future__ import annotations

import json
import urllib.error
import urllib.request

from python.dashboard.service import (
    EngineeringDashboardService,
)
from python.runtime.interfaces.http_server import (
    RuntimeHttpServer,
)
from python.runtime.owner_access import (
    OWNER_SESSION_COOKIE,
    OwnerAccessBoundary,
)


OWNER_SECRET = "fusion-02-owner-acceptance-secret"
OWNER_DASHBOARD_COLD_START_TIMEOUT_SECONDS = 60


def _owner_boundary():
    return OwnerAccessBoundary(
        token=OWNER_SECRET,
    )


def _dashboard(tmp_path):
    return EngineeringDashboardService(
        repository_root=str(tmp_path),
        workspace_root=str(tmp_path),
    )


def _start_real_server(tmp_path):
    server = RuntimeHttpServer(
        host="127.0.0.1",
        port=0,
    )
    server.owner_access = _owner_boundary()
    server.set_dashboard_service(
        _dashboard(tmp_path)
    )
    server.start()

    assert server._server is not None

    port = server._server.server_address[1]
    base_url = f"http://127.0.0.1:{port}"

    return server, base_url


def _owner_request(
    url,
    *,
    method="GET",
    payload=None,
):
    data = None
    headers = {
        "Authorization": (
            f"Bearer {OWNER_SECRET}"
        ),
    }

    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"

    return urllib.request.Request(
        url,
        data=data,
        headers=headers,
        method=method,
    )


def test_owner_web_session_is_derived_not_raw_secret():
    boundary = _owner_boundary()
    cookie_value = boundary.session_cookie_value()

    assert cookie_value
    assert cookie_value != OWNER_SECRET
    assert OWNER_SECRET not in cookie_value


def test_owner_cookie_authenticates_existing_boundary():
    boundary = _owner_boundary()
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


def test_invalid_owner_cookie_fails_closed():
    boundary = _owner_boundary()

    decision = boundary.authenticate_request(
        {
            "Cookie": (
                f"{OWNER_SESSION_COOKIE}=not-valid"
            )
        }
    )

    assert decision.authenticated is False
    assert decision.human_authority is False


def test_existing_bearer_contract_remains_valid():
    boundary = _owner_boundary()

    decision = boundary.authenticate_request(
        {
            "Authorization": (
                f"Bearer {OWNER_SECRET}"
            )
        }
    )

    assert decision.authenticated is True
    assert decision.role == "OWNER"
    assert decision.human_authority is True


def test_ai_control_center_contains_real_chat_surface(
    tmp_path,
):
    service = _dashboard(tmp_path)

    control = service.ai_platform.control_center()
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


def test_chat_ui_contains_no_owner_secret(
    tmp_path,
):
    service = _dashboard(tmp_path)

    html = service._owner_ai_chat_panel(
        service.ai_platform.control_center()
    )

    assert OWNER_SECRET not in html
    assert "AI_TOOLKIT_OWNER_TOKEN" not in html


def test_chat_uses_same_origin_cookie_not_js_owner_token(
    tmp_path,
):
    service = _dashboard(tmp_path)

    html = service._owner_ai_chat_panel(
        service.ai_platform.control_center()
    )

    assert 'credentials:"same-origin"' in html
    assert "Authorization" not in html
    assert "Bearer " not in html


def test_unauthenticated_real_http_owner_route_redirects(
    tmp_path,
):
    server, base_url = _start_real_server(tmp_path)

    try:
        with urllib.request.urlopen(
            base_url + "/ai-control-center",
            timeout=10,
        ) as response:
            body = response.read().decode("utf-8")
            final_url = response.geturl()

        assert response.status == 200
        assert final_url.endswith("/owner/login")
        assert "AI-Toolkit Owner Access" in body
        assert OWNER_SECRET not in body
    finally:
        server.stop()


def test_authenticated_real_http_owner_chat_surface(
    tmp_path,
):
    server, base_url = _start_real_server(tmp_path)

    try:
        request = _owner_request(
            base_url + "/ai-control-center"
        )

        with urllib.request.urlopen(
            request,
            timeout=(
                OWNER_DASHBOARD_COLD_START_TIMEOUT_SECONDS
            ),
        ) as response:
            body = response.read().decode("utf-8")

        assert response.status == 200
        assert 'id="chat-form"' in body
        assert "/api/ai/chat" in body
        assert OWNER_SECRET not in body
    finally:
        server.stop()


def test_real_http_chat_persists_session_and_sources(
    tmp_path,
):
    server, base_url = _start_real_server(tmp_path)

    try:
        chat_request = _owner_request(
            base_url + "/api/ai/chat",
            method="POST",
            payload={
                "question": (
                    "inspect repository architecture"
                ),
                "provider_id": "anthropic",
                "model": "claude-sonnet-4.5",
            },
        )

        with urllib.request.urlopen(
            chat_request,
            timeout=20,
        ) as response:
            result = json.loads(
                response.read().decode("utf-8")
            )

        assert response.status == 200
        assert result["provider"] == "anthropic"
        assert result["model"] == "claude-sonnet-4.5"
        assert result["answer"]
        assert result["raw_source_count"] == 2
        assert result["epistemic_status"][
            "conversation_is_raw_source"
        ] is True
        assert result["epistemic_status"][
            "conversation_is_evidence"
        ] is False
        assert result["epistemic_status"][
            "conversation_is_canon"
        ] is False
        assert result["epistemic_status"][
            "human_authority_preserved"
        ] is True

        session_id = result["session_id"]

        session_request = _owner_request(
            base_url
            + "/api/ai/sessions/"
            + session_id
        )

        with urllib.request.urlopen(
            session_request,
            timeout=10,
        ) as response:
            payload = json.loads(
                response.read().decode("utf-8")
            )

        session = payload["session"]

        assert session["id"] == session_id
        assert len(session["raw_sources"]) == 2
        assert [
            item["actor"]
            for item in session["raw_sources"]
        ] == ["HUMAN", "AI"]
        assert session["raw_sources"][0][
            "epistemic_status"
        ]["evidence"] is False
        assert session["raw_sources"][1][
            "epistemic_status"
        ]["automatic_authority"] is False
    finally:
        server.stop()


def test_real_http_owner_authentication_fails_closed(
    tmp_path,
):
    server, base_url = _start_real_server(tmp_path)

    try:
        request = urllib.request.Request(
            base_url + "/api/ai/sessions",
            headers={
                "Authorization": (
                    "Bearer invalid-owner-credential"
                )
            },
        )

        try:
            urllib.request.urlopen(
                request,
                timeout=10,
            )
        except urllib.error.HTTPError as exc:
            status = exc.code
            payload = json.loads(
                exc.read().decode("utf-8")
            )
        else:
            raise AssertionError(
                "invalid owner credential was accepted"
            )

        assert status == 401
        assert payload["error"] == (
            "owner authentication required"
        )
        assert payload["access"]["authenticated"] is False
        assert payload["access"]["human_authority"] is False
    finally:
        server.stop()


def test_session_readback_uses_existing_ai_session_engine():
    from python.ai_platform.sessions import (
        AISessionEngine,
    )

    assert hasattr(AISessionEngine, "list_sessions")
    assert hasattr(AISessionEngine, "get")
    assert hasattr(
        AISessionEngine,
        "conversation_sources",
    )

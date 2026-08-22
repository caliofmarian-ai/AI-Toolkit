from pathlib import Path

from python.dashboard.service import EngineeringDashboardService


SERVICE_PATH = Path(
    "lib/python/dashboard/service.py"
)

HTTP_RUNTIME_PATH = Path(
    "lib/python/runtime/interfaces/http_server.py"
)

SERVICE_SOURCE = SERVICE_PATH.read_text(
    encoding="utf-8"
)

RUNTIME_SOURCE = HTTP_RUNTIME_PATH.read_text(
    encoding="utf-8"
)


def test_real_dashboard_service_symbol_is_conserved():
    assert EngineeringDashboardService is not None


def test_dashboard_service_accepts_existing_session_identity():
    assert "class EngineeringDashboardService" in SERVICE_SOURCE
    assert 'session_id: str = ""' in SERVICE_SOURCE
    assert "session_id=session_id" in SERVICE_SOURCE


def test_browser_has_durable_ai_partner_session_identity():
    assert (
        'localStorage.getItem("ai_toolkit_partner_session_id")'
        in SERVICE_SOURCE
    )
    assert (
        'localStorage.setItem("ai_toolkit_partner_session_id",sid)'
        in SERVICE_SOURCE
    )


def test_browser_transports_session_identity_to_chat_endpoint():
    assert '"/api/ai/chat"' in SERVICE_SOURCE
    assert "session_id:session.value" in SERVICE_SOURCE


def test_browser_restores_returned_session_identity():
    assert (
        "const sid=data.session_id||session.value;"
        in SERVICE_SOURCE
    )
    assert "await loadSessions(sid)" in SERVICE_SOURCE
    assert "session.value=sid" in SERVICE_SOURCE


def test_real_http_runtime_contains_chat_post_boundary():
    assert '"/api/ai/chat"' in RUNTIME_SOURCE
    assert "def do_POST" in RUNTIME_SOURCE


def test_runtime_chat_endpoint_accepts_session_identity():
    assert (
        'payload.get("session_id"'
        in RUNTIME_SOURCE
    )
    assert "session_id=session_id" in RUNTIME_SOURCE


def test_runtime_propagates_chat_to_ai_platform():
    assert (
        "dashboard_service.ai_platform.ask_repository"
        in RUNTIME_SOURCE
        or "dashboard_service.ask_repository"
        in RUNTIME_SOURCE
    )


def test_runtime_exposes_durable_session_recovery_routes():
    assert '"/api/ai/sessions"' in RUNTIME_SOURCE
    assert '"/api/ai/sessions/"' in RUNTIME_SOURCE


def test_session_engine_exposes_recovery_contract():
    from python.ai_platform.sessions import AISessionEngine

    assert hasattr(AISessionEngine, "list_sessions")
    assert hasattr(AISessionEngine, "get")
    assert hasattr(AISessionEngine, "conversation_sources")

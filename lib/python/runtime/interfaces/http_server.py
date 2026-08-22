"""
CORE-021 — Runtime HTTP Server
CANON-055 §5, CANON-056

Minimal HTTP server (stdlib only) that exposes:

    GET  /health    — liveness check
    GET  /ready     — readiness check
    GET  /metrics   — metrics snapshot
    GET  /status    — full Runtime status report
    POST /webhook/github  — GitHub webhook receiver
    POST /webhook/telegram — Telegram update receiver (fallback to polling)

Uses Python's built-in http.server so no third-party HTTP framework
is required.
"""

import json
import logging
import threading
from lib.python.runtime.interfaces.runtime_api import RuntimeApiRouter

from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import TYPE_CHECKING, Any, Callable, Dict, Optional
from urllib.parse import parse_qs, urlparse

from python.runtime.owner_access import (
    OWNER_SESSION_COOKIE,
    OwnerAccessBoundary,
)

logger = logging.getLogger(__name__)


class _RuntimeHandler(BaseHTTPRequestHandler):
    """Request handler that delegates to the RuntimeHttpServer callbacks."""

    # These are set by RuntimeHttpServer before creating instances.
    _server_ref: "RuntimeHttpServer" = None  # type: ignore[assignment]

    def log_message(self, fmt, *args):
        logger.debug("HTTP %s", fmt % args)

    def _send_json(self, data: dict, status: int = 200) -> None:
        body = json.dumps(data, indent=2).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_html(self, html: str, status: int = 200) -> None:
        body = html.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _redirect(
        self,
        location: str,
        *,
        cookie: str = "",
    ) -> None:
        self.send_response(303)
        self.send_header("Location", location)
        if cookie:
            self.send_header("Set-Cookie", cookie)
        self.send_header("Content-Length", "0")
        self.end_headers()

    def _owner_login_page(
        self,
        *,
        rejected: bool = False,
    ) -> str:
        message = (
            "<p class=\"error\">Owner credential rejected.</p>"
            if rejected
            else ""
        )
        return (
            "<!doctype html><html><head>"
            "<meta charset=\"utf-8\">"
            "<meta name=\"viewport\" "
            "content=\"width=device-width,initial-scale=1\">"
            "<title>Owner Access — AI-Toolkit</title>"
            "<style>"
            "body{font-family:Arial,sans-serif;background:#0b1020;"
            "color:#e5e7eb;display:grid;place-items:center;"
            "min-height:100vh;margin:0}"
            ".box{width:min(92vw,460px);background:#111827;"
            "border:1px solid #1f2937;border-radius:14px;"
            "padding:24px}"
            "input,button{box-sizing:border-box;width:100%;"
            "padding:12px;margin-top:10px;border-radius:8px}"
            "input{background:#0b1020;color:#fff;"
            "border:1px solid #374151}"
            "button{background:#2563eb;color:#fff;border:0;"
            "font-weight:700;cursor:pointer}"
            ".muted{color:#9ca3af}.error{color:#fca5a5}"
            "</style></head><body><main class=\"box\">"
            "<h1>AI-Toolkit Owner Access</h1>"
            "<p class=\"muted\">Private · Single Owner · "
            "Human Authority</p>"
            + message
            + "<form method=\"post\" action=\"/owner/login\">"
            "<label for=\"owner-token\">Owner credential</label>"
            "<input id=\"owner-token\" name=\"owner_token\" "
            "type=\"password\" autocomplete=\"current-password\" "
            "required autofocus>"
            "<button type=\"submit\">Enter AI-Toolkit</button>"
            "</form></main></body></html>"
        )

    def _read_body(self) -> bytes:
        length = int(self.headers.get("Content-Length", 0))
        return self.rfile.read(length) if length else b""

    def _require_owner(self) -> bool:
        srv = self.__class__._server_ref
        decision = srv.owner_access.authenticate_request(self.headers)

        if decision.authenticated:
            return True

        self._send_json(
            {
                "error": "owner authentication required",
                "access": decision.as_dict(),
            },
            401,
        )
        return False

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)
        srv = self.__class__._server_ref
        normalized_dashboard_path = srv.normalize_dashboard_path(path)
        prefer_json = query.get("format", [""])[0] == "json" or "application/json" in self.headers.get("Accept", "")
        if path == "/owner/login":
            decision = srv.owner_access.authenticate_request(
                self.headers
            )
            if decision.authenticated:
                self._redirect("/ai-control-center")
            else:
                self._send_html(self._owner_login_page())
            return

        if path == "/owner/logout":
            self._redirect(
                "/owner/login",
                cookie=(
                    f"{OWNER_SESSION_COOKIE}=; Path=/; "
                    "Max-Age=0; HttpOnly; Secure; SameSite=Strict"
                ),
            )
            return

        if path == "/api/ai/sessions":
            if not self._require_owner():
                return
            if srv.dashboard_service is None:
                self._send_json(
                    {"error": "AI dashboard service unavailable"},
                    503,
                )
                return
            sessions = (
                srv.dashboard_service.ai_platform.sessions.list_sessions()
            )
            self._send_json({"sessions": sessions})
            return

        if path.startswith("/api/ai/sessions/"):
            if not self._require_owner():
                return
            if srv.dashboard_service is None:
                self._send_json(
                    {"error": "AI dashboard service unavailable"},
                    503,
                )
                return
            session_id = path.rsplit("/", 1)[-1].strip()
            session = (
                srv.dashboard_service.ai_platform.sessions.get(
                    session_id
                )
            )
            if not session:
                self._send_json(
                    {"error": "AI session not found"},
                    404,
                )
                return
            self._send_json({"session": session})
            return

        if normalized_dashboard_path == "/" and not prefer_json and srv.dashboard_service is not None:
            self._send_html(srv.render_dashboard(path, query))

        elif normalized_dashboard_path == "/" and prefer_json:
            data = srv.api.status()
            self._send_json(data)
        elif path in ("/health", "/api/v1/health"):
            data = srv.api.health()
            self._send_json(data, 200 if data.get("healthy") else 503)
        elif path == "/api/v1/runtime":
            self._send_json(srv.api.runtime())
        elif path in ("/organism", "/api/v1/organism"):
            status = srv.api.status()
            organism = status.get("organism")

            if organism is None:
                self._send_json(
                    {
                        "state": "UNKNOWN",
                        "reason": (
                            "Organism state is not available "
                            "from RuntimeBootstrap."
                        ),
                    },
                    503,
                )
            else:
                self._send_json(organism)
        elif path == "/runtime":
            if srv.dashboard_service is not None and not prefer_json:
                self._send_html(srv.render_dashboard(path, query))
            else:
                self._send_json(srv.api.runtime())
        elif path == "/diagnostics":
            if srv.dashboard_service is not None and not prefer_json:
                self._send_html(srv.render_dashboard(path, query))
            else:
                self._send_json(srv.api.status().get("diagnostics", {}))
        elif path == "/ready":
            data = srv.handle_ready()
            status = 200 if data.get("ready") else 503
            self._send_json(data, status)
        elif path in ("/metrics", "/api/v1/metrics"):
            self._send_json(srv.api.metrics())
        elif path in ("/status", "/api/v1/status"):
            self._send_json(srv.api.status())
        elif srv.dashboard_service is not None and normalized_dashboard_path in (
            "/",
            "/projects",
            "/session",
            "/repository",
            "/ai-control-center",
            "/explorer",
            "/reports",
            "/runtime",
            "/diagnostics",
        ):
            if normalized_dashboard_path == "/ai-control-center":
                decision = srv.owner_access.authenticate_request(
                    self.headers
                )
                if not decision.authenticated:
                    self._redirect("/owner/login")
                    return
            if normalized_dashboard_path == "/repository":
                privileged_query = bool(
                    (query.get("q") or [""])[0].strip()
                    or (query.get("prompt") or [""])[0].strip()
                )
                if privileged_query and not self._require_owner():
                    return
            self._send_html(srv.render_dashboard(path, query))
        elif srv.dashboard_service is not None and path == "/api/ai/control-center":
            if not self._require_owner():
                return
            payload = srv.dashboard_payload(refresh="1" in query.get("refresh", []))
            self._send_json(payload.get("ai_control_center", {}))
        elif srv.dashboard_service is not None and path == "/api/ai/ask":
            if not self._require_owner():
                return
            question = (query.get("q") or [""])[0].strip()
            prompt_name = (query.get("prompt") or [""])[0].strip()
            if not question and not prompt_name:
                self._send_json({"error": "missing query"}, 400)
                return
            self._send_json(srv.dashboard_service.ask_repository(question=question, prompt_name=prompt_name))
        elif srv.dashboard_service is not None and path == "/api/dashboard":
            self._send_json(srv.dashboard_payload(refresh="1" in query.get("refresh", [])))
        elif srv.dashboard_service is not None and path == "/api/capabilities":
            payload = srv.dashboard_payload(refresh="1" in query.get("refresh", []))
            self._send_json(payload.get("capabilities", {}))
        elif srv.dashboard_service is not None and path.startswith("/capabilities/"):
            page = srv.render_dashboard(path, query)
            if page is None:
                self._send_json({"error": "not found"}, 404)
            else:
                self._send_html(page)
        else:
            self._send_json({"error": "not found"}, 404)

    def do_POST(self) -> None:
        path = self.path.split("?")[0]
        srv = self.__class__._server_ref
        body = self._read_body()

        if path == "/owner/login":
            try:
                form = parse_qs(
                    body.decode("utf-8"),
                    keep_blank_values=True,
                )
            except UnicodeDecodeError:
                self._send_html(
                    self._owner_login_page(rejected=True),
                    400,
                )
                return

            supplied = (
                form.get("owner_token", [""])[0].strip()
            )
            decision = srv.owner_access.authenticate(
                {"Authorization": f"Bearer {supplied}"}
            )

            if not decision.authenticated:
                self._send_html(
                    self._owner_login_page(rejected=True),
                    401,
                )
                return

            session_value = (
                srv.owner_access.session_cookie_value()
            )
            self._redirect(
                "/ai-control-center",
                cookie=(
                    f"{OWNER_SESSION_COOKIE}={session_value}; "
                    "Path=/; HttpOnly; Secure; SameSite=Strict"
                ),
            )
            return

        if path == "/webhook/github":
            sig = self.headers.get("X-Hub-Signature-256", "")
            event_type = self.headers.get("X-GitHub-Event", "unknown")
            result = srv.handle_github_webhook(event_type, sig, body)
            self._send_json(result)
        elif path == "/webhook/telegram":
            result = srv.handle_telegram_update(body)
            self._send_json(result)
        elif path == "/api/ai/chat":
            if not self._require_owner():
                return
            if srv.dashboard_service is None:
                self._send_json(
                    {"error": "AI dashboard service unavailable"},
                    503,
                )
                return
            try:
                payload = json.loads(body.decode("utf-8") or "{}")
            except (UnicodeDecodeError, json.JSONDecodeError):
                self._send_json({"error": "invalid JSON body"}, 400)
                return

            question = str(payload.get("question", "")).strip()
            session_id = str(payload.get("session_id", "")).strip()
            provider_id = str(payload.get("provider_id", "")).strip()
            model = str(payload.get("model", "")).strip()
            prompt_name = str(payload.get("prompt_name", "")).strip()
            resume_interrupted_turn = bool(
                payload.get("resume_interrupted_turn", False)
            )

            if (
                not question
                and not prompt_name
                and not resume_interrupted_turn
            ):
                self._send_json({"error": "missing question"}, 400)
                return

            try:
                result = srv.dashboard_service.ai_platform.ask_repository(
                    question=question,
                    session_id=session_id,
                    provider_id=provider_id,
                    model=model,
                    prompt_name=prompt_name,
                    resume_interrupted_turn=resume_interrupted_turn,
                )
            except ValueError as exc:
                self._send_json({"error": str(exc)}, 400)
                return
            except Exception as exc:
                logger.exception("Owner AI chat failed")
                self._send_json(
                    {
                        "error": "AI chat execution failed",
                        "detail": f"{type(exc).__name__}: {exc}",
                    },
                    500,
                )
                return

            self._send_json(result)
        else:
            self._send_json({"error": "not found"}, 404)


class RuntimeHttpServer:
    """
    Minimal HTTP server for the Runtime Server.

    All route handlers are injectable so callers can wire in the
    real Health, Metrics, and Webhook implementations.
    """

    def __init__(self, host: str = "0.0.0.0", port: int = 8080):
        self._host = host
        self._port = port
        self._server: Optional[HTTPServer] = None
        self._thread: Optional[threading.Thread] = None
        self.dashboard_service = None
        self.owner_access = OwnerAccessBoundary()

        # Default no-op handlers (replaced by bootstrap)
        self._health_handler: Callable[[], dict] = lambda: {"healthy": True}
        self._ready_handler: Callable[[], dict] = lambda: {"ready": True}
        self._runtime_handler: Callable[[], dict] = lambda: {"state": "BOOT"}
        self._metrics_handler: Callable[[], dict] = lambda: {}
        self._status_handler: Callable[[], dict] = lambda: {}
        self._github_handler: Callable[[str, str, bytes], dict] = lambda et, sig, b: {"ok": True}
        self._telegram_handler: Callable[[bytes], dict] = lambda b: {"ok": True}
        self.api = RuntimeApiRouter(
            health=self.handle_health,
            runtime=self.handle_runtime,
            status=self.handle_status,
            metrics=self.handle_metrics,
        )

    # ------------------------------------------------------------------ #
    # Handler injection
    # ------------------------------------------------------------------ #

    def set_health_handler(self, fn: Callable[[], dict]) -> None:
        self._health_handler = fn

    def set_ready_handler(self, fn: Callable[[], dict]) -> None:
        self._ready_handler = fn

    def set_runtime_handler(self, fn: Callable[[], dict]) -> None:
        self._runtime_handler = fn

    def set_metrics_handler(self, fn: Callable[[], dict]) -> None:
        self._metrics_handler = fn

    def set_status_handler(self, fn: Callable[[], dict]) -> None:
        self._status_handler = fn

    def set_github_webhook_handler(self, fn: Callable[[str, str, bytes], dict]) -> None:
        self._github_handler = fn

    def set_telegram_update_handler(self, fn: Callable[[bytes], dict]) -> None:
        self._telegram_handler = fn

    def set_dashboard_service(self, service: Any) -> None:
        self.dashboard_service = service

    # ------------------------------------------------------------------ #
    # Internal dispatch (called from _RuntimeHandler)
    # ------------------------------------------------------------------ #

    def handle_health(self) -> dict:
        try:
            return self._health_handler()
        except Exception as exc:
            logger.error("Health handler error: %s", exc)
            return {"healthy": True, "error": str(exc)}

    def handle_ready(self) -> dict:
        try:
            return self._ready_handler()
        except Exception as exc:
            logger.error("Ready handler error: %s", exc)
            return {"ready": False, "error": str(exc)}

    def handle_runtime(self) -> dict:
        try:
            return self._runtime_handler()
        except Exception as exc:
            logger.error("Runtime handler error: %s", exc)
            return {"state": "FAILED", "error": str(exc)}

    def handle_metrics(self) -> dict:
        try:
            return self._metrics_handler()
        except Exception as exc:
            return {"error": str(exc)}

    def handle_status(self) -> dict:
        try:
            return self._status_handler()
        except Exception as exc:
            return {"error": str(exc)}

    def handle_github_webhook(self, event_type: str, signature: str, body: bytes) -> dict:
        try:
            return self._github_handler(event_type, signature, body)
        except Exception as exc:
            logger.error("GitHub webhook handler error: %s", exc)
            return {"ok": False, "error": str(exc)}

    def handle_telegram_update(self, body: bytes) -> dict:
        try:
            return self._telegram_handler(body)
        except Exception as exc:
            logger.error("Telegram update handler error: %s", exc)
            return {"ok": False, "error": str(exc)}

    # ------------------------------------------------------------------ #
    # Lifecycle
    # ------------------------------------------------------------------ #

    def start(self) -> None:
        # Give the handler class a reference to this server instance
        # using a class-level attribute (one server per process).
        _RuntimeHandler._server_ref = self

        self._server = HTTPServer((self._host, self._port), _RuntimeHandler)
        self._thread = threading.Thread(
            target=self._server.serve_forever,
            name="RuntimeHttpServer",
            daemon=True,
        )
        self._thread.start()
        logger.info("RuntimeHttpServer listening on %s:%s", self._host, self._port)

    def stop(self) -> None:
        if self._server:
            self._server.shutdown()
            self._server.server_close()
        if self._thread:
            self._thread.join(timeout=5)
        logger.info("RuntimeHttpServer stopped")

    def dashboard_payload(self, *, refresh: bool = False) -> dict:
        if self.dashboard_service is None:
            return {}
        return self.dashboard_service.build(refresh=refresh)

    def render_dashboard(self, path: str, query: Dict[str, Any]) -> Optional[str]:
        if self.dashboard_service is None:
            return None
        refresh = "1" in query.get("refresh", [])
        payload = self.dashboard_service.build(refresh=refresh)
        normalized_path = self.normalize_dashboard_path(path)
        if normalized_path == "/":
            return self.dashboard_service.render_home(payload)
        if normalized_path == "/projects":
            return self.dashboard_service.render_projects(payload)
        if normalized_path == "/session":
            return self.dashboard_service.render_session(payload)
        if normalized_path == "/repository":
            question = (query.get("q") or [""])[0].strip()
            prompt_name = (query.get("prompt") or [""])[0].strip()
            return self.dashboard_service.render_repository(payload, question=question, prompt_name=prompt_name)
        if normalized_path == "/ai-control-center":
            return self.dashboard_service.render_ai_control_center(payload)
        if normalized_path == "/explorer":
            return self.dashboard_service.render_explorer(payload)
        if normalized_path == "/reports":
            return self.dashboard_service.render_reports(payload)
        if normalized_path == "/runtime":
            return self.dashboard_service.render_runtime(payload)
        if normalized_path == "/diagnostics":
            return self.dashboard_service.render_diagnostics(payload)
        if normalized_path.startswith("/capabilities/"):
            slug = normalized_path.rsplit("/", 1)[-1]
            return self.dashboard_service.render_capability(slug, payload)
        return None

    def normalize_dashboard_path(self, path: str) -> str:
        aliases = {
            "/dashboard": "/",
            "/project-manager": "/projects",
            "/engineering-session": "/session",
            "/knowledge": "/explorer",
            "/validation": "/diagnostics",
            "/settings": "/runtime",
        }
        return aliases.get(path, path)

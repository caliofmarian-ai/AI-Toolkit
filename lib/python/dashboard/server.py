from __future__ import annotations

import json
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any, Dict, Optional
from urllib.parse import parse_qs, urlparse

from .service import EngineeringDashboardService


class _DashboardRequestHandler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        return

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = self._normalize_path(parsed.path)
        query = parse_qs(parsed.query)
        server = self.server._dashboard_server  # type: ignore[attr-defined]
        if path == "/health":
            self._send_json({"ok": True, "service": "dashboard"})
            return
        if path == "/api/dashboard":
            self._send_json(server.service.build(refresh="refresh=1" in parsed.query))
            return
        if path == "/api/capabilities":
            payload = server.service.build(refresh="refresh=1" in parsed.query)
            self._send_json(payload["capabilities"])
            return
        if path == "/api/runtime":
            payload = server.service.build(refresh="refresh=1" in parsed.query)
            self._send_json(payload["runtime"])
            return
        if path == "/api/diagnostics":
            payload = server.service.build(refresh="refresh=1" in parsed.query)
            self._send_json(payload["diagnostics"])
            return
        if path == "/api/ai/control-center":
            payload = server.service.build(refresh="refresh=1" in parsed.query)
            self._send_json(payload["ai_control_center"])
            return
        if path == "/api/ai/ask":
            question = (query.get("q") or [""])[0].strip()
            prompt_name = (query.get("prompt") or [""])[0].strip()
            if not question and not prompt_name:
                self._send_json({"error": "missing query"}, status=400)
                return
            self._send_json(server.service.ask_repository(question=question, prompt_name=prompt_name))
            return
        payload = server.service.build(refresh="refresh=1" in parsed.query)
        if path == "/":
            self._send_html(server.service.render_home(payload))
            return
        if path == "/projects":
            self._send_html(server.service.render_projects(payload))
            return
        if path == "/repository":
            question = (query.get("q") or [""])[0].strip()
            prompt_name = (query.get("prompt") or [""])[0].strip()
            self._send_html(server.service.render_repository(payload, question=question, prompt_name=prompt_name))
            return
        if path == "/session":
            self._send_html(server.service.render_session(payload))
            return
        if path == "/ai-control-center":
            self._send_html(server.service.render_ai_control_center(payload))
            return
        if path == "/knowledge":
            self._send_html(server.service.render_explorer(payload))
            return
        if path == "/validation":
            self._send_html(server.service.render_diagnostics(payload))
            return
        if path == "/settings":
            self._send_html(server.service.render_runtime(payload))
            return
        if path == "/explorer":
            self._send_html(server.service.render_explorer(payload))
            return
        if path == "/reports":
            self._send_html(server.service.render_reports(payload))
            return
        if path == "/runtime":
            self._send_html(server.service.render_runtime(payload))
            return
        if path == "/diagnostics":
            self._send_html(server.service.render_diagnostics(payload))
            return
        if path.startswith("/capabilities/"):
            slug = path.rsplit("/", 1)[-1]
            page = server.service.render_capability(slug, payload)
            if page is None:
                self._send_json({"error": "not found"}, status=404)
                return
            self._send_html(page)
            return
        self._send_json({"error": "not found"}, status=404)

    def _normalize_path(self, path: str) -> str:
        aliases = {
            "/dashboard": "/",
            "/project-manager": "/projects",
            "/engineering-session": "/session",
        }
        return aliases.get(path, path)

    def _send_html(self, html: str, status: int = 200) -> None:
        body = html.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_json(self, payload: Dict[str, Any], status: int = 200) -> None:
        body = json.dumps(payload, indent=2, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


class DashboardHttpServer:
    def __init__(
        self,
        host: str = "127.0.0.1",
        port: int = 8081,
        repository_root: str = ".",
        workspace_root: Optional[str] = None,
    ) -> None:
        self.host = host
        self.port = port
        self.service = EngineeringDashboardService(
            repository_root=repository_root,
            workspace_root=workspace_root,
        )
        self._server: Optional[HTTPServer] = None
        self._thread: Optional[threading.Thread] = None

    @property
    def url(self) -> str:
        return f"http://{self.host}:{self.port}/"

    def start(self) -> None:
        self.service.build(refresh=True)
        self._server = self._build_server()
        self._thread = threading.Thread(
            target=self._server.serve_forever,
            daemon=True,
            name="EngineeringDashboardHttpServer",
        )
        self._thread.start()

    def serve_forever(self) -> None:
        self.service.build(refresh=True)
        self._server = self._build_server()
        self._server.serve_forever()

    def stop(self) -> None:
        if self._server is not None:
            self._server.shutdown()
            self._server.server_close()
        if self._thread is not None:
            self._thread.join(timeout=5)

    def _handler_class(self):
        return type(
            "EngineeringDashboardHandler",
            (_DashboardRequestHandler,),
            {},
        )

    def _build_server(self) -> HTTPServer:
        server = HTTPServer((self.host, self.port), self._handler_class())
        server._dashboard_server = self  # type: ignore[attr-defined]
        return server


def serve_dashboard(
    host: str = "127.0.0.1",
    port: int = 8081,
    repository_root: str = ".",
    workspace_root: Optional[str] = None,
    open_browser: bool = False,
) -> None:
    server = DashboardHttpServer(
        host=host,
        port=port,
        repository_root=repository_root,
        workspace_root=workspace_root,
    )
    print(f"AI-Toolkit Dashboard running at {server.url}")
    if open_browser:
        webbrowser.open(server.url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.stop()

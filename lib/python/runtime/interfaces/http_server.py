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
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import TYPE_CHECKING, Any, Callable, Dict, Optional

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

    def _read_body(self) -> bytes:
        length = int(self.headers.get("Content-Length", 0))
        return self.rfile.read(length) if length else b""

    def do_GET(self) -> None:
        path = self.path.split("?")[0]
        srv = self.__class__._server_ref
        if path == "/health":
            self._send_json(srv.handle_health())
        elif path == "/ready":
            data = srv.handle_ready()
            status = 200 if data.get("ready") else 503
            self._send_json(data, status)
        elif path == "/metrics":
            self._send_json(srv.handle_metrics())
        elif path == "/status":
            self._send_json(srv.handle_status())
        else:
            self._send_json({"error": "not found"}, 404)

    def do_POST(self) -> None:
        path = self.path.split("?")[0]
        srv = self.__class__._server_ref
        body = self._read_body()

        if path == "/webhook/github":
            sig = self.headers.get("X-Hub-Signature-256", "")
            event_type = self.headers.get("X-GitHub-Event", "unknown")
            result = srv.handle_github_webhook(event_type, sig, body)
            self._send_json(result)
        elif path == "/webhook/telegram":
            result = srv.handle_telegram_update(body)
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

        # Default no-op handlers (replaced by bootstrap)
        self._health_handler: Callable[[], dict] = lambda: {"healthy": True}
        self._ready_handler: Callable[[], dict] = lambda: {"ready": True}
        self._metrics_handler: Callable[[], dict] = lambda: {}
        self._status_handler: Callable[[], dict] = lambda: {}
        self._github_handler: Callable[[str, str, bytes], dict] = lambda et, sig, b: {"ok": True}
        self._telegram_handler: Callable[[bytes], dict] = lambda b: {"ok": True}

    # ------------------------------------------------------------------ #
    # Handler injection
    # ------------------------------------------------------------------ #

    def set_health_handler(self, fn: Callable[[], dict]) -> None:
        self._health_handler = fn

    def set_ready_handler(self, fn: Callable[[], dict]) -> None:
        self._ready_handler = fn

    def set_metrics_handler(self, fn: Callable[[], dict]) -> None:
        self._metrics_handler = fn

    def set_status_handler(self, fn: Callable[[], dict]) -> None:
        self._status_handler = fn

    def set_github_webhook_handler(self, fn: Callable[[str, str, bytes], dict]) -> None:
        self._github_handler = fn

    def set_telegram_update_handler(self, fn: Callable[[bytes], dict]) -> None:
        self._telegram_handler = fn

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
        if self._thread:
            self._thread.join(timeout=5)
        logger.info("RuntimeHttpServer stopped")

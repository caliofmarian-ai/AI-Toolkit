"""
Runtime diagnostics and persisted status snapshots.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Mapping, Optional

from lib.python.runtime.state import RuntimePublicState, RuntimeStateService


class RuntimeDiagnosticsService:
    def __init__(
        self,
        *,
        repository_root: str,
        workspace_root: str,
        state_dir: str,
        logs_dir: str,
        cli_commands: Iterable[str],
    ) -> None:
        self.repository_root = Path(repository_root).resolve()
        self.workspace_root = Path(workspace_root).resolve()
        self.state_dir = Path(state_dir)
        self.logs_dir = Path(logs_dir)
        self.cli_commands = list(cli_commands)
        self._dashboard_initialized = False
        self._dashboard_error = ""
        self._engineering_context_initialized = False
        self._engineering_context_error = ""
        self._engineering_context_summary: Dict[str, Any] = {}
        self._startup_duration_seconds = 0.0

    def mark_dashboard_initialized(self, *, initialized: bool, error: str = "") -> None:
        self._dashboard_initialized = initialized
        self._dashboard_error = error

    def mark_engineering_context_initialized(
        self,
        *,
        initialized: bool,
        error: str = "",
        summary: Optional[Mapping[str, Any]] = None,
    ) -> None:
        self._engineering_context_initialized = initialized
        self._engineering_context_error = error
        self._engineering_context_summary = dict(summary or {})

    def set_startup_duration(self, seconds: float) -> None:
        self._startup_duration_seconds = max(seconds, 0.0)

    def build_snapshot(
        self,
        *,
        config: Any,
        identity: Any,
        lifecycle: Any,
        health: Any,
        registry: Any,
        metrics: Any,
        supervisor: Any,
        runtime_state: RuntimeStateService,
    ) -> dict:
        health_summary = self._health_summary(
            config=config,
            health=health,
            runtime_state=runtime_state,
        )
        runtime_payload = {
            "runtime_id": identity.runtime_id,
            "state": runtime_state.current_state.value,
            "lifecycle_phase": identity.lifecycle_phase,
            "uptime_seconds": round(runtime_state.uptime_seconds(), 3),
            "startup_duration_seconds": round(self._startup_duration_seconds, 3),
            "port": config.http_port,
            "host": config.http_host,
            "environment": config.environment,
            "dashboard_initialized": self._dashboard_initialized,
            "engineering_context_initialized": self._engineering_context_initialized,
            "loaded_services": registry.list_services(),
            "loaded_engines": registry.list_engines(),
            "registered_cli_commands": list(self.cli_commands),
            "registered_providers": self._detect_ai_providers(),
            "current_repository": str(self.repository_root),
            "current_workspace": str(self.workspace_root),
            "current_project": self.repository_root.name,
            "current_session": self._active_session(),
            "health": health_summary,
            "runtime_configuration": config.to_dict(),
            "repository_detected": self.repository_root.exists(),
            "workspace_detected": self.workspace_root.exists(),
            "loaded_modules": self._loaded_modules(),
            "engineering_context": self._engineering_context(),
        }
        diagnostics_payload = {
            "issues": runtime_state.issues(),
            "warnings": self._warnings(runtime_payload),
            "configuration": config.to_dict(),
            "recent_startup_log": runtime_state.to_dict()["history"][-10:],
            "health_checks": {
                "checks": health_summary["checks"],
                "healthy": health_summary["healthy"],
                "ready": health_summary["ready"],
            },
            "recommendations": self._recommendations(runtime_payload),
            "future_improvements": self._future_improvements(runtime_payload),
            "dashboard_initialized": self._dashboard_initialized,
            "dashboard_error": self._dashboard_error,
            "engineering_context_initialized": self._engineering_context_initialized,
            "engineering_context_error": self._engineering_context_error,
            "engineering_context_summary": dict(self._engineering_context_summary),
            "supervisor": supervisor.summary(),
            "metrics": metrics.snapshot(),
            "lifecycle": lifecycle.to_dict(),
        }
        status_payload = {
            "service": "ai-toolkit-runtime",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "identity": identity.to_dict(),
            "state": runtime_state.to_dict(),
            "runtime": runtime_payload,
            "diagnostics": diagnostics_payload,
            "health": health_summary,
            "registry": registry.summary(),
        }
        return status_payload

    def persist(self, snapshot: Mapping[str, Any]) -> None:
        self.state_dir.mkdir(parents=True, exist_ok=True)
        (self.state_dir / "runtime_status.json").write_text(
            json.dumps(dict(snapshot), indent=2),
            encoding="utf-8",
        )
        runtime_payload = dict(snapshot.get("runtime", {}))
        diagnostics_payload = dict(snapshot.get("diagnostics", {}))
        (self.state_dir / "runtime_diagnostics.json").write_text(
            json.dumps(
                {
                    "generated_at": snapshot.get("generated_at"),
                    "runtime": runtime_payload,
                    "diagnostics": diagnostics_payload,
                    "health": snapshot.get("health", {}),
                },
                indent=2,
            ),
            encoding="utf-8",
        )

    def _health_summary(self, *, config: Any, health: Any, runtime_state: RuntimeStateService) -> dict:
        readiness = health.to_dict(health.check_readiness())
        checks = {
            "runtime_alive": True,
            "dashboard_initialized": self._dashboard_initialized,
            "engineering_context_initialized": self._engineering_context_initialized,
            "repository_loaded": self.repository_root.exists(),
            "session_initialized": bool(self._active_session()),
            "workspace_detected": self.workspace_root.exists(),
        }
        if self._dashboard_error:
            checks["dashboard_initialized"] = False
        if self._engineering_context_error:
            checks["engineering_context_initialized"] = False
        context_payload = self._engineering_context()
        checks["decision_history_loaded"] = bool(context_payload.get("decision_context"))
        checks["executive_briefing_loaded"] = bool(
            context_payload.get("executive_context", {}).get("validation", {}).get("briefing_generated", False)
        )
        healthy = all(checks.values())
        ready = healthy and readiness.get("ready", False) and runtime_state.current_state == RuntimePublicState.READY
        return {
            "healthy": healthy,
            "ready": ready,
            "state": runtime_state.current_state.value,
            "port": config.http_port,
            "checks": checks,
            "runtime_checks": readiness.get("checks", {}),
            "details": readiness.get("details", {}),
        }

    def _loaded_modules(self) -> List[str]:
        modules = [
            name
            for name in sys.modules
            if name.startswith("python.runtime")
            or name.startswith("lib.python.runtime")
            or name.startswith("python.dashboard")
            or name.startswith("lib.python.dashboard")
        ]
        return sorted(modules)

    def _detect_ai_providers(self) -> List[str]:
        providers = []
        for env_name, label in [
            ("ANTHROPIC_API_KEY", "Anthropic"),
            ("OPENAI_API_KEY", "OpenAI"),
            ("GEMINI_API_KEY", "Gemini"),
            ("GOOGLE_API_KEY", "Google"),
            ("MISTRAL_API_KEY", "Mistral"),
        ]:
            if os.environ.get(env_name):
                providers.append(label)
        return providers

    def _active_session(self) -> Dict[str, Any]:
        state = self._read_json(self.repository_root / ".ai" / "development_state" / "current_state.json") or {}
        workspace_state = state.get("workspace_state", {})
        repository_state = state.get("repository_state", {})
        sessions_dir = self.repository_root / ".ai" / "sessions"
        latest_session = None
        if sessions_dir.exists():
            matches = sorted(sessions_dir.glob("*.json"), key=lambda item: item.stat().st_mtime, reverse=True)
            if matches:
                latest_session = self._read_json(matches[0]) or {}
        return {
            "project": workspace_state.get("active_project", self.repository_root.name),
            "repository": repository_state.get("repository", self.repository_root.name),
            "branch": repository_state.get("branch", ""),
            "task": workspace_state.get("current_task", ""),
            "identifier": (latest_session or {}).get("identifier", ""),
            "status": (latest_session or {}).get("status", ""),
        }

    def _warnings(self, runtime_payload: Mapping[str, Any]) -> List[str]:
        warnings = []
        if not runtime_payload.get("registered_providers"):
            warnings.append("No AI provider credentials detected.")
        if not runtime_payload.get("loaded_engines"):
            warnings.append("No runtime engines are registered.")
        if not runtime_payload.get("dashboard_initialized"):
            warnings.append("Dashboard bootstrap is incomplete.")
        if not runtime_payload.get("engineering_context_initialized"):
            warnings.append("Engineering context bootstrap is incomplete.")
        return warnings

    def _recommendations(self, runtime_payload: Mapping[str, Any]) -> List[str]:
        recommendations = []
        if not runtime_payload.get("health", {}).get("healthy"):
            recommendations.append("Resolve failing runtime checks before deploying.")
        if not runtime_payload.get("registered_providers"):
            recommendations.append("Configure at least one AI provider for engineering workflows.")
        if not runtime_payload.get("engineering_context_initialized"):
            recommendations.append("Rebuild the engineering context before relying on runtime decisions.")
        recommendations.append("Keep the runtime entry point on the dashboard-backed server surface.")
        return recommendations

    def _future_improvements(self, runtime_payload: Mapping[str, Any]) -> List[str]:
        return [
            "Add live scheduler and job queue telemetry to the runtime page.",
            "Expose richer session controls from the dashboard.",
            "Expand diagnostics with persisted startup and shutdown traces.",
        ]

    def _read_json(self, path: Path) -> Optional[Dict[str, Any]]:
        if not path.exists():
            return None
        return json.loads(path.read_text(encoding="utf-8"))

    def _engineering_context(self) -> Dict[str, Any]:
        payload = self._read_json(self.repository_root / ".ai" / "context" / "engineering_context.json") or {}
        if payload:
            return payload
        return dict(self._engineering_context_summary)

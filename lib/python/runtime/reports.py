"""
CORE-021 — Runtime Reports
CANON-055 §5

Generates operational Runtime reports.  Reports are stored in the
canonical .ai/runtime/logs directory and can be requested via
Telegram or the HTTP interface.
"""

import json
import logging
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, Optional

logger = logging.getLogger(__name__)


class RuntimeReports:
    """
    Generates and persists operational Runtime reports.
    """

    def __init__(self, logs_dir: str = ".ai/runtime/logs"):
        self._logs_dir = Path(logs_dir)

    def generate_status_report(
        self,
        identity: Optional[Any] = None,
        lifecycle: Optional[Any] = None,
        health: Optional[Any] = None,
        metrics: Optional[Any] = None,
        registry: Optional[Any] = None,
        supervisor: Optional[Any] = None,
        scheduler: Optional[Any] = None,
        job_queue: Optional[Any] = None,
        event_loop: Optional[Any] = None,
        event_dispatcher: Optional[Any] = None,
    ) -> dict:
        """Generate a comprehensive Runtime status report."""
        report: Dict[str, Any] = {
            "report_type": "runtime_status",
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }
        if identity:
            report["identity"] = identity.to_dict()
        if lifecycle:
            report["lifecycle"] = lifecycle.to_dict()
        if health:
            result = health.check_readiness()
            report["health"] = health.to_dict(result)
        if metrics:
            report["metrics"] = metrics.snapshot()
        if registry:
            report["registry"] = registry.summary()
        if supervisor:
            report["supervisor"] = supervisor.summary()
        if scheduler:
            report["scheduler"] = scheduler.summary()
        if job_queue:
            report["job_queue"] = job_queue.summary()
        if event_loop:
            report["event_loop"] = event_loop.summary()
        if event_dispatcher:
            report["event_dispatcher"] = event_dispatcher.summary()
        return report

    def persist_report(self, report: dict, name: str = "status") -> Optional[str]:
        """Write *report* to the logs directory.  Returns the file path."""
        try:
            self._logs_dir.mkdir(parents=True, exist_ok=True)
            ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
            filename = f"runtime_{name}_{ts}.json"
            path = self._logs_dir / filename
            path.write_text(json.dumps(report, indent=2))
            return str(path)
        except Exception as exc:
            logger.warning("RuntimeReports: could not persist report: %s", exc)
            return None

    def format_text_summary(self, report: dict) -> str:
        """Return a human-readable summary of a status report."""
        lines = [
            "=== AI CTO Runtime Status ===",
            f"Generated: {report.get('generated_at', 'unknown')}",
        ]
        identity = report.get("identity", {})
        if identity:
            lines.append(f"Runtime ID:   {identity.get('runtime_id', 'unknown')}")
            lines.append(f"Version:      {identity.get('runtime_version', 'unknown')}")
            lines.append(f"Deployment:   {identity.get('deployment_id', 'unknown')}")
            lines.append(f"Phase:        {identity.get('lifecycle_phase', 'unknown')}")

        health = report.get("health", {})
        if health:
            status = "HEALTHY" if health.get("healthy") else "UNHEALTHY"
            ready = "READY" if health.get("ready") else "NOT READY"
            lines.append(f"Health:       {status} / {ready}")

        metrics = report.get("metrics", {})
        if metrics:
            counters = metrics.get("counters", {})
            for k, v in list(counters.items())[:5]:
                lines.append(f"  {k}: {v}")

        return "\n".join(lines)

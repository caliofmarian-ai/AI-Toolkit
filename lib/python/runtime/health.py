"""
CORE-021 — Runtime Health Service
CANON-055 §5 — Runtime Responsibilities

Provides liveness and readiness health checks for the Runtime Server.
Exposed via the HTTP server at /health and /ready.
"""

import logging
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict, List

logger = logging.getLogger(__name__)


@dataclass
class HealthCheckResult:
    healthy: bool
    ready: bool
    checks: Dict[str, bool]
    timestamp: str
    details: Dict[str, str]


class HealthService:
    """
    Aggregates health and readiness signals from all Runtime components.
    """

    def __init__(self):
        self._checks: Dict[str, callable] = {}
        self._startup_complete = False

    def register_check(self, name: str, check_fn: callable) -> None:
        """Register a named health check function that returns bool."""
        self._checks[name] = check_fn

    def mark_startup_complete(self) -> None:
        """Signal that the Runtime has completed startup."""
        self._startup_complete = True

    def check_liveness(self) -> HealthCheckResult:
        """
        Liveness: the Runtime process is alive.
        Returns True as long as the process is running.
        """
        now = datetime.now(timezone.utc).isoformat()
        return HealthCheckResult(
            healthy=True,
            ready=self._startup_complete,
            checks={"process": True},
            timestamp=now,
            details={"process": "alive"},
        )

    def check_readiness(self) -> HealthCheckResult:
        """
        Readiness: all registered checks pass and startup is complete.
        """
        now = datetime.now(timezone.utc).isoformat()
        results: Dict[str, bool] = {}
        details: Dict[str, str] = {}

        for name, check_fn in self._checks.items():
            try:
                ok = bool(check_fn())
                results[name] = ok
                details[name] = "ok" if ok else "fail"
            except Exception as exc:
                results[name] = False
                details[name] = str(exc)
                logger.warning("Health check %s raised: %s", name, exc)

        all_ok = all(results.values()) if results else True
        ready = all_ok and self._startup_complete

        return HealthCheckResult(
            healthy=all_ok,
            ready=ready,
            checks=results,
            timestamp=now,
            details=details,
        )

    def to_dict(self, result: HealthCheckResult) -> dict:
        return {
            "healthy": result.healthy,
            "ready": result.ready,
            "checks": result.checks,
            "timestamp": result.timestamp,
            "details": result.details,
        }

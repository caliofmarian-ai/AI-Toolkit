"""
CORE-021 — Runtime Supervisor
CANON-055 §11 — Runtime Process Model

The Supervisor continuously monitors registered Runtime Services and
Engines.  When a component signals an error the Supervisor records the
failure and notifies the Recovery Service.
"""

import logging
import threading
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class ComponentStatus:
    name: str
    healthy: bool = True
    failure_count: int = 0
    last_check: str = ""
    last_error: str = ""


class RuntimeSupervisor:
    """
    Monitors Runtime components and records their health status.
    """

    def __init__(self):
        self._statuses: Dict[str, ComponentStatus] = {}
        self._health_checks: Dict[str, Callable[[], bool]] = {}
        self._lock = threading.Lock()

    def register(self, name: str, health_check: Optional[Callable[[], bool]] = None) -> None:
        """Register a component for supervision."""
        with self._lock:
            self._statuses[name] = ComponentStatus(name=name)
            if health_check:
                self._health_checks[name] = health_check

    def record_failure(self, name: str, error: str = "") -> None:
        """Record a failure for *name*."""
        with self._lock:
            status = self._statuses.setdefault(name, ComponentStatus(name=name))
            status.healthy = False
            status.failure_count += 1
            status.last_error = error
            status.last_check = datetime.now(timezone.utc).isoformat()
        logger.error("Supervisor: component %s failed — %s", name, error)

    def record_recovery(self, name: str) -> None:
        """Record recovery of *name*."""
        with self._lock:
            if name in self._statuses:
                self._statuses[name].healthy = True
                self._statuses[name].last_check = datetime.now(timezone.utc).isoformat()
        logger.info("Supervisor: component %s recovered", name)

    def run_health_checks(self) -> Dict[str, bool]:
        """Execute all registered health checks and update statuses."""
        results: Dict[str, bool] = {}
        with self._lock:
            checks = dict(self._health_checks)
        for name, check in checks.items():
            try:
                ok = check()
                results[name] = ok
                with self._lock:
                    status = self._statuses.setdefault(name, ComponentStatus(name=name))
                    status.healthy = ok
                    status.last_check = datetime.now(timezone.utc).isoformat()
                    if not ok:
                        status.failure_count += 1
            except Exception as exc:
                results[name] = False
                self.record_failure(name, str(exc))
        return results

    def all_healthy(self) -> bool:
        """Return True if every supervised component is healthy."""
        with self._lock:
            return all(s.healthy for s in self._statuses.values())

    def summary(self) -> dict:
        with self._lock:
            return {
                "all_healthy": all(s.healthy for s in self._statuses.values()),
                "components": {
                    name: {
                        "healthy": s.healthy,
                        "failure_count": s.failure_count,
                        "last_check": s.last_check,
                        "last_error": s.last_error,
                    }
                    for name, s in self._statuses.items()
                },
            }

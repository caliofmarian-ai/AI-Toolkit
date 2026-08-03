"""
CORE-021 — Runtime Metrics
CANON-055 §5

In-memory metrics collector for the Runtime Server.
Metrics are exposed via the /metrics endpoint and included in reports.
"""

import threading
from datetime import datetime, timezone
from typing import Any, Dict


class RuntimeMetrics:
    """
    Thread-safe in-memory metrics store.

    Supports counters (increment only) and gauges (arbitrary value).
    """

    def __init__(self):
        self._counters: Dict[str, int] = {}
        self._gauges: Dict[str, Any] = {}
        self._lock = threading.Lock()
        self._start_time = datetime.now(timezone.utc).isoformat()

    # ------------------------------------------------------------------ #
    # Counters
    # ------------------------------------------------------------------ #

    def increment(self, name: str, value: int = 1) -> None:
        with self._lock:
            self._counters[name] = self._counters.get(name, 0) + value

    def counter(self, name: str) -> int:
        with self._lock:
            return self._counters.get(name, 0)

    # ------------------------------------------------------------------ #
    # Gauges
    # ------------------------------------------------------------------ #

    def set_gauge(self, name: str, value: Any) -> None:
        with self._lock:
            self._gauges[name] = value

    def gauge(self, name: str) -> Any:
        with self._lock:
            return self._gauges.get(name)

    # ------------------------------------------------------------------ #
    # Summary
    # ------------------------------------------------------------------ #

    def snapshot(self) -> dict:
        with self._lock:
            return {
                "start_time": self._start_time,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "counters": dict(self._counters),
                "gauges": dict(self._gauges),
            }

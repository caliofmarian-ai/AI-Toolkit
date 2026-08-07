"""
Runtime public state tracking for product-facing lifecycle visibility.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


class RuntimePublicState(str, Enum):
    BOOT = "BOOT"
    INITIALIZING = "INITIALIZING"
    LOADING = "LOADING"
    READY = "READY"
    SHUTTING_DOWN = "SHUTTING_DOWN"
    FAILED = "FAILED"


@dataclass
class RuntimeIssue:
    severity: str
    source: str
    message: str
    timestamp: str
    details: str = ""

    def to_dict(self) -> dict:
        return {
            "severity": self.severity,
            "source": self.source,
            "message": self.message,
            "timestamp": self.timestamp,
            "details": self.details,
        }


class RuntimeStateService:
    def __init__(self) -> None:
        now = _utc_now().isoformat()
        self._state = RuntimePublicState.BOOT
        self._started_at = now
        self._last_transition_at = now
        self._history: List[Dict[str, str]] = [
            {
                "state": RuntimePublicState.BOOT.value,
                "timestamp": now,
                "message": "Runtime process created.",
            }
        ]
        self._issues: List[RuntimeIssue] = []

    @property
    def current_state(self) -> RuntimePublicState:
        return self._state

    def transition(self, state: RuntimePublicState, message: str = "") -> None:
        now = _utc_now().isoformat()
        self._state = state
        self._last_transition_at = now
        self._history.append(
            {
                "state": state.value,
                "timestamp": now,
                "message": message,
            }
        )

    def record_issue(
        self,
        message: str,
        *,
        severity: str = "error",
        source: str = "runtime",
        details: str = "",
    ) -> None:
        self._issues.append(
            RuntimeIssue(
                severity=severity,
                source=source,
                message=message,
                timestamp=_utc_now().isoformat(),
                details=details,
            )
        )

    def uptime_seconds(self) -> float:
        return max((_utc_now() - datetime.fromisoformat(self._started_at)).total_seconds(), 0.0)

    def issues(self) -> List[dict]:
        return [issue.to_dict() for issue in self._issues]

    def to_dict(self) -> dict:
        return {
            "state": self._state.value,
            "started_at": self._started_at,
            "last_transition_at": self._last_transition_at,
            "uptime_seconds": round(self.uptime_seconds(), 3),
            "history": list(self._history),
            "issues": self.issues(),
            "error_count": sum(1 for issue in self._issues if issue.severity == "error"),
            "warning_count": sum(1 for issue in self._issues if issue.severity == "warning"),
        }

"""
CORE-021 — Runtime Recovery Service
CANON-055 §5, CANON-057

Provides automatic Recovery from unexpected failures.  When the Runtime
detects a failure it attempts recovery up to the configured maximum
number of attempts before escalating.
"""

import logging
import threading
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Callable, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class RecoveryAttempt:
    attempt_number: int
    timestamp: str
    success: bool
    error: str = ""


class RecoveryService:
    """
    Executes automatic recovery procedures.

    The Recovery Service tries to restore Runtime consistency after
    an unexpected failure.  After *max_attempts* consecutive failures
    it transitions the Runtime to MAINTENANCE mode.
    """

    def __init__(self, max_attempts: int = 3):
        self._max_attempts = max_attempts
        self._attempt_count = 0
        self._history: List[RecoveryAttempt] = []
        self._on_exhausted: Optional[Callable] = None
        self._lock = threading.Lock()

    def on_exhausted(self, callback: Callable) -> None:
        """Register a callback invoked when all recovery attempts fail."""
        self._on_exhausted = callback

    def attempt(self, recovery_fn: Callable[[], bool], error_context: str = "") -> bool:
        """
        Execute *recovery_fn*.  Returns True on success.

        Tracks the attempt and fires the exhausted callback when the
        maximum number of consecutive attempts is reached.
        """
        with self._lock:
            self._attempt_count += 1
            attempt_number = self._attempt_count

        timestamp = datetime.now(timezone.utc).isoformat()
        logger.info(
            "Recovery attempt %d/%d — %s",
            attempt_number,
            self._max_attempts,
            error_context,
        )

        try:
            success = bool(recovery_fn())
        except Exception as exc:
            success = False
            error_context = str(exc)
            logger.error("Recovery attempt %d raised: %s", attempt_number, exc)

        record = RecoveryAttempt(
            attempt_number=attempt_number,
            timestamp=timestamp,
            success=success,
            error=error_context if not success else "",
        )

        with self._lock:
            self._history.append(record)

        if success:
            logger.info("Recovery attempt %d succeeded", attempt_number)
            self.reset()
            return True

        logger.warning("Recovery attempt %d failed", attempt_number)

        if attempt_number >= self._max_attempts:
            logger.error("Recovery exhausted after %d attempts", self._max_attempts)
            if self._on_exhausted:
                self._on_exhausted()

        return False

    def reset(self) -> None:
        """Reset attempt counter after successful recovery."""
        with self._lock:
            self._attempt_count = 0

    def summary(self) -> dict:
        with self._lock:
            return {
                "max_attempts": self._max_attempts,
                "current_attempt_count": self._attempt_count,
                "history": [
                    {
                        "attempt_number": a.attempt_number,
                        "timestamp": a.timestamp,
                        "success": a.success,
                        "error": a.error,
                    }
                    for a in self._history[-10:]
                ],
            }

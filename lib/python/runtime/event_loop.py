"""
CORE-021 — Runtime Event Loop
CANON-057 — Continuous Runtime Lifecycle

The Event Loop is the heart of the continuous Runtime.  It runs
indefinitely, observing, processing, and reacting to the operational
environment.
"""

import logging
import threading
import time
from datetime import datetime, timezone
from typing import Callable, List, Optional

logger = logging.getLogger(__name__)


class EventLoop:
    """
    Continuous Runtime Loop.

    The loop runs a series of registered observers in sequence on
    each tick, then sleeps until the next tick.  Each tick corresponds
    to one Runtime loop iteration.

    Observers are lightweight callables that return quickly; heavy
    work is submitted to the Job Queue.
    """

    def __init__(self, tick_interval_seconds: int = 30):
        self._tick_interval = tick_interval_seconds
        self._observers: List[Callable] = []
        self._running = False
        self._tick_count = 0
        self._thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()

    def register_observer(self, observer: Callable) -> None:
        """Register an observer called on every loop tick."""
        self._observers.append(observer)

    def start(self) -> None:
        """Start the event loop in a background thread."""
        self._running = True
        self._stop_event.clear()
        self._thread = threading.Thread(
            target=self._loop,
            name="RuntimeEventLoop",
            daemon=True,
        )
        self._thread.start()
        logger.info("RuntimeEventLoop started (tick=%ds)", self._tick_interval)

    def stop(self) -> None:
        """Stop the event loop."""
        self._running = False
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=self._tick_interval + 5)
        logger.info("RuntimeEventLoop stopped after %d ticks", self._tick_count)

    def run_once(self) -> None:
        """Execute one tick of the event loop (used in tests)."""
        self._tick(datetime.now(timezone.utc).isoformat())

    def _loop(self) -> None:
        while self._running:
            tick_time = datetime.now(timezone.utc).isoformat()
            self._tick(tick_time)
            stopped = self._stop_event.wait(timeout=self._tick_interval)
            if stopped:
                break

    def _tick(self, tick_time: str) -> None:
        self._tick_count += 1
        logger.debug("EventLoop tick %d at %s", self._tick_count, tick_time)
        for observer in self._observers:
            try:
                observer()
            except Exception as exc:
                logger.error("EventLoop: observer %s raised: %s", repr(observer), exc)

    @property
    def tick_count(self) -> int:
        return self._tick_count

    def summary(self) -> dict:
        return {
            "running": self._running,
            "tick_count": self._tick_count,
            "tick_interval_seconds": self._tick_interval,
            "observer_count": len(self._observers),
        }

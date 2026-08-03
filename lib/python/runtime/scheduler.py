"""
CORE-021 — Runtime Scheduler Host
CANON-046 — AI CTO Scheduler Specification

The Scheduler Host manages periodic and one-shot jobs using a
background thread.  It translates scheduling rules into executable
work items placed on the Job Queue.
"""

import logging
import threading
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Callable, Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class ScheduledJob:
    job_id: str
    name: str
    callback: Callable
    interval_seconds: int
    last_run: Optional[str] = None
    run_count: int = 0
    enabled: bool = True


class SchedulerHost:
    """
    Background scheduler that executes periodic Runtime jobs.

    Jobs are registered with an interval and a callback.  The scheduler
    thread ticks every second and fires callbacks whose interval has
    elapsed.
    """

    def __init__(self, tick_interval: float = 1.0):
        self._jobs: Dict[str, ScheduledJob] = {}
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._tick_interval = tick_interval
        self._last_tick: Dict[str, float] = {}
        self._lock = threading.Lock()

    def register(self, job_id: str, name: str, callback: Callable, interval_seconds: int) -> None:
        """Register a periodic job."""
        with self._lock:
            self._jobs[job_id] = ScheduledJob(
                job_id=job_id,
                name=name,
                callback=callback,
                interval_seconds=interval_seconds,
            )
            self._last_tick[job_id] = 0.0
        logger.debug("Scheduler: registered job %s (every %ds)", name, interval_seconds)

    def unregister(self, job_id: str) -> None:
        """Remove a scheduled job."""
        with self._lock:
            self._jobs.pop(job_id, None)
            self._last_tick.pop(job_id, None)

    def start(self) -> None:
        """Start the scheduler background thread."""
        self._running = True
        self._thread = threading.Thread(
            target=self._run,
            name="RuntimeScheduler",
            daemon=True,
        )
        self._thread.start()
        logger.info("Scheduler started")

    def stop(self) -> None:
        """Stop the scheduler."""
        self._running = False
        if self._thread:
            self._thread.join(timeout=5)
        logger.info("Scheduler stopped")

    def _run(self) -> None:
        while self._running:
            now = time.monotonic()
            with self._lock:
                jobs = list(self._jobs.values())
            for job in jobs:
                if not job.enabled:
                    continue
                last = self._last_tick.get(job.job_id, 0.0)
                if now - last >= job.interval_seconds:
                    self._last_tick[job.job_id] = now
                    self._fire(job)
            time.sleep(self._tick_interval)

    def _fire(self, job: ScheduledJob) -> None:
        try:
            job.callback()
            job.run_count += 1
            job.last_run = datetime.now(timezone.utc).isoformat()
        except Exception as exc:
            logger.error("Scheduler: job %s raised: %s", job.name, exc)

    def list_jobs(self) -> List[str]:
        with self._lock:
            return sorted(self._jobs.keys())

    def summary(self) -> dict:
        with self._lock:
            return {
                "running": self._running,
                "job_count": len(self._jobs),
                "jobs": {
                    jid: {
                        "name": j.name,
                        "interval_seconds": j.interval_seconds,
                        "run_count": j.run_count,
                        "last_run": j.last_run,
                        "enabled": j.enabled,
                    }
                    for jid, j in self._jobs.items()
                },
            }

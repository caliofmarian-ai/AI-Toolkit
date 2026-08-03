"""
CORE-021 — Runtime Job Queue Host
CANON-055 §5

Thread-safe job queue that accepts callable jobs and executes them
via a pool of worker threads.
"""

import logging
import queue
import threading
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Optional
import uuid

logger = logging.getLogger(__name__)


@dataclass
class Job:
    """A unit of work submitted to the Job Queue."""

    job_id: str
    name: str
    callback: Callable
    payload: Any = None
    submitted_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    success: Optional[bool] = None
    error: str = ""


class JobQueueHost:
    """
    Thread-pool-backed job queue.

    Jobs are submitted by name and callback, queued, and executed by
    worker threads in FIFO order.
    """

    def __init__(self, worker_count: int = 2):
        self._queue: queue.Queue = queue.Queue()
        self._workers: List[threading.Thread] = []
        self._worker_count = worker_count
        self._running = False
        self._completed: List[Job] = []
        self._lock = threading.Lock()
        self._submitted_count = 0

    def start(self) -> None:
        """Start worker threads."""
        self._running = True
        for i in range(self._worker_count):
            t = threading.Thread(
                target=self._worker_loop,
                name=f"JobWorker-{i}",
                daemon=True,
            )
            t.start()
            self._workers.append(t)
        logger.info("JobQueue started with %d workers", self._worker_count)

    def stop(self) -> None:
        """Signal workers to stop and wait for them."""
        self._running = False
        for _ in self._workers:
            self._queue.put(None)  # poison pill
        for t in self._workers:
            t.join(timeout=5)
        logger.info("JobQueue stopped")

    def submit(self, name: str, callback: Callable, payload: Any = None) -> str:
        """Submit a job and return its job_id."""
        job_id = f"job-{uuid.uuid4().hex[:8]}"
        job = Job(job_id=job_id, name=name, callback=callback, payload=payload)
        with self._lock:
            self._submitted_count += 1
        self._queue.put(job)
        logger.debug("JobQueue: submitted %s (%s)", name, job_id)
        return job_id

    def _worker_loop(self) -> None:
        while self._running:
            try:
                job = self._queue.get(timeout=1)
            except queue.Empty:
                continue
            if job is None:
                break
            self._execute(job)
            self._queue.task_done()

    def _execute(self, job: Job) -> None:
        job.started_at = datetime.now(timezone.utc).isoformat()
        try:
            if job.payload is not None:
                job.callback(job.payload)
            else:
                job.callback()
            job.success = True
        except Exception as exc:
            job.success = False
            job.error = str(exc)
            logger.error("JobQueue: job %s (%s) failed: %s", job.name, job.job_id, exc)
        finally:
            job.completed_at = datetime.now(timezone.utc).isoformat()
            with self._lock:
                self._completed.append(job)

    def queue_size(self) -> int:
        return self._queue.qsize()

    def summary(self) -> dict:
        with self._lock:
            recent = self._completed[-20:]
        return {
            "running": self._running,
            "worker_count": self._worker_count,
            "queue_size": self.queue_size(),
            "submitted_count": self._submitted_count,
            "completed_count": len(self._completed),
            "recent_jobs": [
                {
                    "job_id": j.job_id,
                    "name": j.name,
                    "success": j.success,
                    "completed_at": j.completed_at,
                }
                for j in recent
            ],
        }

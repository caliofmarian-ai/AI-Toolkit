"""
CORE-021 — Runtime Graceful Shutdown
CANON-055 §5

Installs SIGTERM / SIGINT signal handlers so that the Runtime Server
shuts down cleanly when the container orchestrator (Railway) sends a
termination signal.
"""

import logging
import signal
import threading
from typing import Callable, Optional

logger = logging.getLogger(__name__)


class GracefulShutdown:
    """
    Registers OS signal handlers for SIGTERM and SIGINT.

    When a termination signal is received the *shutdown_callback* is
    invoked exactly once in the background so the signal handler itself
    can return quickly.
    """

    def __init__(self, shutdown_callback: Callable[[], None]):
        self._callback = shutdown_callback
        self._triggered = threading.Event()
        self._shutdown_thread: Optional[threading.Thread] = None

    def install(self) -> None:
        """Install signal handlers."""
        signal.signal(signal.SIGTERM, self._handle_signal)
        signal.signal(signal.SIGINT, self._handle_signal)
        logger.info("GracefulShutdown: signal handlers installed (SIGTERM, SIGINT)")

    def _handle_signal(self, signum, frame) -> None:
        if self._triggered.is_set():
            return  # Already shutting down

        sig_name = signal.Signals(signum).name
        logger.info("GracefulShutdown: received %s — initiating graceful shutdown", sig_name)
        self._triggered.set()

        # Run shutdown in a separate thread so the signal handler returns
        self._shutdown_thread = threading.Thread(
            target=self._run_shutdown,
            name="GracefulShutdown",
            daemon=False,
        )
        self._shutdown_thread.start()

    def _run_shutdown(self) -> None:
        try:
            self._callback()
        except Exception as exc:
            logger.error("GracefulShutdown: shutdown callback raised: %s", exc)

    def is_shutdown_requested(self) -> bool:
        return self._triggered.is_set()

    def wait(self) -> None:
        """Block until shutdown is triggered."""
        self._triggered.wait()

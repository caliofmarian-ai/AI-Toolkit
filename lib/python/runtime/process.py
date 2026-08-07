"""
CORE-021 — Runtime Process
CANON-055 §11 — Runtime Process Model

Entry point for the Runtime Server process.  Assembles Bootstrap,
installs graceful shutdown handling, starts the Runtime, and
blocks until shutdown is requested.
"""

import logging
import sys
import os

logger = logging.getLogger(__name__)

# Ensure lib/ is on the path when invoked directly
_script_dir = os.path.dirname(os.path.abspath(__file__))
_lib_dir = os.path.normpath(os.path.join(_script_dir, "..", ".."))
if _lib_dir not in sys.path:
    sys.path.insert(0, _lib_dir)


def main() -> int:
    """
    Runtime Server entry point.

    Returns 0 on clean shutdown, non-zero on unrecoverable error.
    """
    from lib.python.runtime.bootstrap import RuntimeBootstrap
    from lib.python.runtime.shutdown import GracefulShutdown

    # Create bootstrap (logging is configured inside bootstrap.bootstrap())
    runtime = RuntimeBootstrap()

    def do_shutdown():
        runtime.stop()

    shutdown = GracefulShutdown(shutdown_callback=do_shutdown)

    try:
        runtime.bootstrap()
        shutdown.install()
        runtime.start()

        logger.info("Runtime: entering main wait loop")
        # Block indefinitely until a shutdown signal is received
        shutdown.wait()
        logger.info("Runtime: shutdown requested — exiting")
        return 0

    except KeyboardInterrupt:
        logger.info("Runtime: KeyboardInterrupt — shutting down")
        try:
            runtime.stop()
        except Exception:
            pass
        return 0

    except Exception as exc:
        logger.critical("Runtime: unrecoverable error: %s", exc, exc_info=True)
        try:
            runtime.mark_failed(exc)
        except Exception:
            pass
        try:
            runtime.stop()
        except Exception:
            pass
        return 1


if __name__ == "__main__":
    sys.exit(main())

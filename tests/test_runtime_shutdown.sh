#!/usr/bin/env bash
# CORE-021 — Graceful Shutdown Tests
# Tests the GracefulShutdown handler.
set -e

python3 - <<'PY'
import sys, signal, time, threading
sys.path.insert(0, "lib")
import os
os.environ["JSON_LOGS"] = "false"

from lib.python.runtime.shutdown import GracefulShutdown

# --- Shutdown callback is invoked on SIGINT ---
called = []
shutdown = GracefulShutdown(shutdown_callback=lambda: called.append(True))
shutdown.install()
assert not shutdown.is_shutdown_requested()

# Send SIGINT to self
os.kill(os.getpid(), signal.SIGINT)
# Wait for async shutdown thread
time.sleep(0.3)
assert shutdown.is_shutdown_requested(), "Shutdown should be triggered"
assert len(called) == 1, f"Callback should fire once, got {len(called)}"

# --- Second signal is ignored (idempotent) ---
os.kill(os.getpid(), signal.SIGINT)
time.sleep(0.2)
assert len(called) == 1, f"Should still be 1 call after second signal, got {len(called)}"

# --- Shutdown callback exception is handled gracefully ---
def bad_callback():
    raise RuntimeError("shutdown error")

sd2 = GracefulShutdown(shutdown_callback=bad_callback)
sd2.install()
os.kill(os.getpid(), signal.SIGINT)
time.sleep(0.3)
assert sd2.is_shutdown_requested()  # Should still be marked as triggered

print("Graceful shutdown tests PASSED")
PY

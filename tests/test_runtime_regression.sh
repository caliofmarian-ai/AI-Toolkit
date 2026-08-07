#!/usr/bin/env bash
# CORE-021 — Runtime Regression Tests
# Ensures existing CLI commands are not broken by CORE-021 changes.
set -e

echo "=== REGRESSION: CLI still works ==="

echo
echo "--- inspect ---"
python3 bin/ai inspect . | python3 -c "import sys,json; d=json.load(sys.stdin); print('inspect: OK')"

echo
echo "--- Runtime package imports correctly ---"
python3 - <<'PY'
import sys
sys.path.insert(0, "lib")
# Runtime package must not interfere with existing packages
from lib.python.runtime.bootstrap import RuntimeBootstrap
from lib.python.runtime.identity import RuntimeIdentity
from lib.python.runtime.config import RuntimeConfig
from lib.python.runtime.registry import RuntimeRegistry
from lib.python.runtime.lifecycle import LifecycleManager
from lib.python.runtime.health import HealthService
from lib.python.runtime.recovery import RecoveryService
from lib.python.runtime.scheduler import SchedulerHost
from lib.python.runtime.event_loop import EventLoop
from lib.python.runtime.event_dispatcher import EventDispatcher
from lib.python.runtime.job_queue import JobQueueHost
from lib.python.runtime.metrics import RuntimeMetrics
from lib.python.runtime.reports import RuntimeReports
from lib.python.runtime.interfaces.http_server import RuntimeHttpServer
from lib.python.runtime.interfaces.github_webhook import GitHubWebhookHost
from lib.python.runtime.interfaces.telegram_gateway import TelegramGateway
from lib.python.runtime.railway import RailwayBootstrap
from lib.python.runtime.shutdown import GracefulShutdown
print("Runtime package imports: OK")
PY

echo
echo "=== REGRESSION: Runtime layout directories exist ==="
python3 - <<'PY'
import os, sys
root = os.getcwd()
required_dirs = [
    ".ai/runtime/state",
    ".ai/runtime/logs",
    ".ai/runtime/checkpoints",
    ".ai/runtime/sessions",
    ".ai/runtime/cache",
    ".ai/batches",
]
for d in required_dirs:
    path = os.path.join(root, d)
    assert os.path.isdir(path), f"Missing directory: {path}"
print("Runtime layout directories: OK")
PY

echo
echo "=== REGRESSION: Runtime HTTP endpoints stay reachable ==="
PORT=19110 PYTHONPATH=lib timeout 20s bash bin/runtime-server >/tmp/runtime-regression.log 2>&1 &
server_pid=$!
trap 'kill $server_pid >/dev/null 2>&1 || true' EXIT

python3 - <<'PY'
import json
import time
import urllib.request

base = "http://127.0.0.1:19110"
deadline = time.time() + 15
last_error = None
while time.time() < deadline:
    try:
        with urllib.request.urlopen(base + "/health", timeout=2) as response:
            payload = json.loads(response.read())
        assert payload["healthy"] is True
        with urllib.request.urlopen(base + "/status", timeout=2) as response:
            payload = json.loads(response.read())
        assert payload["runtime"]["state"] == "READY"
        print("Runtime HTTP regression: OK")
        break
    except Exception as exc:  # noqa: BLE001
        last_error = exc
        time.sleep(0.5)
else:
    raise SystemExit(f"Runtime HTTP regression failed: {last_error}")
PY

echo
echo "Regression tests PASSED"

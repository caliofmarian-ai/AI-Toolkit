#!/usr/bin/env bash
# CORE-021 — Runtime Regression Tests
# Ensures existing CLI commands are not broken by CORE-021 changes.
set -e

echo "=== REGRESSION: CLI still works ==="

echo
echo "--- inventory ---"
bash bin/ai inventory | python3 -c "import sys,json; d=json.load(sys.stdin); print('inventory: OK')"

echo
echo "--- validate ---"
bash bin/ai validate | python3 -c "import sys,json; json.load(sys.stdin); print('validate: OK')"

echo
echo "--- Runtime package imports correctly ---"
python3 - <<'PY'
import sys
sys.path.insert(0, "lib")
# Runtime package must not interfere with existing packages
from python.runtime.bootstrap import RuntimeBootstrap
from python.runtime.identity import RuntimeIdentity
from python.runtime.config import RuntimeConfig
from python.runtime.registry import RuntimeRegistry
from python.runtime.lifecycle import LifecycleManager
from python.runtime.health import HealthService
from python.runtime.recovery import RecoveryService
from python.runtime.scheduler import SchedulerHost
from python.runtime.event_loop import EventLoop
from python.runtime.event_dispatcher import EventDispatcher
from python.runtime.job_queue import JobQueueHost
from python.runtime.metrics import RuntimeMetrics
from python.runtime.reports import RuntimeReports
from python.runtime.interfaces.http_server import RuntimeHttpServer
from python.runtime.interfaces.github_webhook import GitHubWebhookHost
from python.runtime.interfaces.telegram_gateway import TelegramGateway
from python.runtime.railway import RailwayBootstrap
from python.runtime.shutdown import GracefulShutdown
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
echo "Regression tests PASSED"

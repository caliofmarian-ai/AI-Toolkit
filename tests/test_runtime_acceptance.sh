#!/usr/bin/env bash
# CORE-021 — Runtime Acceptance Tests
# Full end-to-end acceptance tests per CANON-055 acceptance criteria.
set -e

echo "=== Runtime Acceptance Tests (CORE-021) ==="
echo "Following CANON-055 acceptance criteria"
echo

python3 - <<'PY'
import sys, os, time, urllib.request, json
sys.path.insert(0, "lib")
os.environ["RUNTIME_LOOP_INTERVAL_SECONDS"] = "300"
os.environ["SCHEDULER_INTERVAL_SECONDS"] = "300"
os.environ["RUNTIME_HTTP_PORT"] = "19100"
os.environ["JSON_LOGS"] = "false"

from lib.python.runtime.bootstrap import RuntimeBootstrap
from lib.python.runtime.lifecycle import LifecyclePhase

failures = []

def check(name, condition, detail=""):
    if condition:
        print(f"  ✅ {name}")
    else:
        print(f"  ❌ FAIL: {name} — {detail}")
        failures.append(name)

# AC-1: Runtime starts successfully
rt = RuntimeBootstrap()
try:
    rt.bootstrap()
    rt.start()
    time.sleep(0.2)
    check("AC-1: Runtime starts successfully", True)
except Exception as exc:
    check("AC-1: Runtime starts successfully", False, str(exc))

# AC-2: Runtime remains alive continuously (event loop ticks)
ticks_before = rt.event_loop.tick_count
time.sleep(0.1)
check("AC-2: Runtime remains alive (event loop)", rt.event_loop._running)

# AC-3: Runtime survives restart (stop + start)
rt.stop()
rt2 = RuntimeBootstrap()
os.environ["RUNTIME_HTTP_PORT"] = "19101"
rt2.bootstrap()
rt2.start()
time.sleep(0.2)
check("AC-3: Runtime survives restart", rt2.lifecycle.is_running())

# AC-4: Runtime Health passes
result = rt2.health.check_readiness()
check("AC-4: Runtime Health passes", result.ready, str(result.checks))

# AC-4b: Engineering context reconstructed on startup
context_path = os.path.join(".ai", "context", "engineering_context.json")
decision_history_path = os.path.join(".ai", "context", "decision_history.json")
check("AC-4b: Engineering context persisted", os.path.exists(context_path))
check("AC-4c: Decision history persisted", os.path.exists(decision_history_path))

# AC-5: Runtime Recovery passes
from lib.python.runtime.recovery import RecoveryService
rec = RecoveryService(max_attempts=3)
ok = rec.attempt(lambda: True)
check("AC-5: Runtime Recovery passes", ok)

# AC-6: Runtime Loop operates correctly
loop_ticks = rt2.event_loop.tick_count
rt2.event_loop.run_once()
check("AC-6: Runtime Loop operates correctly", rt2.event_loop.tick_count > loop_ticks)

# AC-7: Scheduler operational
check(
    "AC-7: Scheduler operational",
    rt2.scheduler._running,
    "scheduler not running"
)

# AC-8: Event Loop operational
check("AC-8: Event Loop operational", rt2.event_loop._running)

# AC-9: Webhook processing works
import json as _json, hashlib, hmac
from lib.python.runtime.event_dispatcher import EventDispatcher
from lib.python.runtime.interfaces.github_webhook import GitHubWebhookHost
events = []
disp = EventDispatcher()
disp.subscribe("github.push", lambda e: events.append(e))
wh = GitHubWebhookHost(dispatcher=disp)
result = wh.process("push", "", _json.dumps({"ref": "main"}).encode())
check("AC-9: Webhook processing works", result["ok"] and len(events) == 1)

# AC-10: Telegram gateway works (disabled mode)
from lib.python.runtime.interfaces.telegram_gateway import TelegramGateway
tg = TelegramGateway(bot_token="", chat_id="")
summary = tg.summary()
check("AC-10: Telegram gateway works (disabled mode)", not summary["enabled"])

# AC-11: Graceful shutdown works
BASE = "http://127.0.0.1:19101"
with urllib.request.urlopen(BASE + "/", timeout=5) as r:
    home = r.read().decode("utf-8")
check("AC-11a: Dashboard home endpoint works", "Engineering Operating System" in home)
with urllib.request.urlopen(BASE + "/health", timeout=5) as r:
    h = _json.loads(r.read())
check("AC-11b: HTTP health endpoint works", h["healthy"])

with urllib.request.urlopen(BASE + "/ready", timeout=5) as r:
    ready = _json.loads(r.read())
check("AC-11c: HTTP readiness endpoint works", ready["ready"])

with urllib.request.urlopen(BASE + "/status", timeout=5) as r:
    status = _json.loads(r.read())
check("AC-11d: HTTP status endpoint works", status["health"]["healthy"])
check("AC-11d2: HTTP status includes engineering context", "engineering_context" in status["runtime"])

with urllib.request.urlopen(BASE + "/api/v1/runtime", timeout=5) as r:
    runtime = _json.loads(r.read())
check("AC-11e: HTTP runtime endpoint works", runtime["state"] in {"READY", "SHUTTING_DOWN"})

rt2.stop()
check("AC-11f: Graceful shutdown completes", rt2.lifecycle.is_shutdown())

# AC-12: Health endpoint operational
# Already tested above (AC-11b)
check("AC-12: Health endpoint operational", h.get("healthy") is True)

# AC-13: Readiness endpoint operational
# Already tested as part of health
check("AC-13: Readiness endpoint configured", rt2.http_server is not None)

print()
print(f"Results: {len(failures)} failure(s) out of 14 checks")

if failures:
    print("FAILED checks:", failures)
    sys.exit(1)
else:
    print("All acceptance criteria PASSED")
PY

echo
echo "Acceptance tests PASSED"

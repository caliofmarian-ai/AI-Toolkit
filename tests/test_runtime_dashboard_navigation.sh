#!/usr/bin/env bash
set -euo pipefail

cd /home/runner/work/AI-Toolkit/AI-Toolkit

python3 - <<'PY'
import json
import os
import sys
import time
from urllib.request import urlopen

sys.path.insert(0, "lib")
from lib.python.runtime.bootstrap import RuntimeBootstrap

os.environ["RUNTIME_LOOP_INTERVAL_SECONDS"] = "300"
os.environ["SCHEDULER_INTERVAL_SECONDS"] = "300"
os.environ["RUNTIME_HTTP_PORT"] = "19121"
os.environ["JSON_LOGS"] = "false"

runtime = RuntimeBootstrap()
runtime.bootstrap()
runtime.start()
base = "http://127.0.0.1:19121"
try:
    deadline = time.time() + 20
    while time.time() < deadline:
        try:
            with urlopen(base + "/health", timeout=2) as response:
                health = json.loads(response.read().decode("utf-8"))
            if health.get("healthy"):
                break
        except Exception:  # noqa: BLE001
            time.sleep(0.5)
    routes = {
        "/": "Engineering Operating System",
        "/dashboard": "Engineering Operating System",
        "/repository": "Repository",
        "/engineering-session": "Engineering Session",
        "/project-manager": "Project Manager",
        "/ai-control-center": "AI Control Center",
        "/reports": "Reports",
        "/settings": "Runtime",
    }
    for route, needle in routes.items():
        body = urlopen(base + route, timeout=5).read().decode("utf-8")
        assert needle in body, f"{route} missing {needle!r}"

    control_center = json.loads(urlopen(base + "/api/ai/control-center", timeout=5).read().decode("utf-8"))
    assert "providers" in control_center
    ask = json.loads(urlopen(base + "/api/ai/ask?q=Explain%20architecture", timeout=5).read().decode("utf-8"))
    assert "answer" in ask
    print("runtime dashboard navigation PASS")
finally:
    runtime.stop()
PY

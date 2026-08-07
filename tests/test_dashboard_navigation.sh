#!/usr/bin/env bash
set -euo pipefail

cd /home/runner/work/AI-Toolkit/AI-Toolkit

PYTHONPATH=lib python3 - <<'PY'
from urllib.request import urlopen

from python.dashboard.server import DashboardHttpServer

server = DashboardHttpServer(
    host="127.0.0.1",
    port=8101,
    repository_root=".",
    workspace_root="..",
)
server.start()
try:
    routes = {
        "/": "Engineering Operating System",
        "/projects": "Project Manager",
        "/repository": "Repository",
        "/session": "Engineering Session",
        "/ai-control-center": "AI Control Center",
        "/knowledge": "Engineering Explorer",
        "/validation": "Diagnostics",
        "/settings": "Runtime",
        "/explorer": "Engineering Explorer",
        "/runtime": "Runtime",
        "/diagnostics": "Diagnostics",
        "/reports": "Reports",
        "/capabilities/dashboard": "Capability Detail",
    }
    for route, needle in routes.items():
        body = urlopen(f"http://127.0.0.1:8101{route}").read().decode("utf-8")
        assert needle in body, f"{route} missing {needle!r}"
    api = urlopen("http://127.0.0.1:8101/api/dashboard").read().decode("utf-8")
    assert '"navigation"' in api
    runtime_api = urlopen("http://127.0.0.1:8101/api/runtime").read().decode("utf-8")
    diagnostics_api = urlopen("http://127.0.0.1:8101/api/diagnostics").read().decode("utf-8")
    control_center_api = urlopen("http://127.0.0.1:8101/api/ai/control-center").read().decode("utf-8")
    ask_ai_api = urlopen("http://127.0.0.1:8101/api/ai/ask?q=Explain%20this%20architecture.").read().decode("utf-8")
    assert '"state"' in runtime_api
    assert '"recommendations"' in diagnostics_api
    assert '"providers"' in control_center_api
    assert '"answer"' in ask_ai_api
    print("dashboard navigation PASS")
finally:
    server.stop()
PY

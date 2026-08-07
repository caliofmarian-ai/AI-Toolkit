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
        "/session": "Engineering Session",
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
    assert '"state"' in runtime_api
    assert '"recommendations"' in diagnostics_api
    print("dashboard navigation PASS")
finally:
    server.stop()
PY

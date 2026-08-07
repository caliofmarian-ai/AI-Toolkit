#!/usr/bin/env bash
set -euo pipefail

cd /home/runner/work/AI-Toolkit/AI-Toolkit

PYTHONPATH=lib python3 - <<'PY'
from python.dashboard.service import EngineeringDashboardService

service = EngineeringDashboardService(repository_root=".", workspace_root="..")
payload = service.build(refresh=True)
session = payload["session"]

assert session["current_project"] == "AI-Toolkit"
assert session["current_repository"]
assert session["current_branch"]
assert session["current_workspace"]
assert session["current_sprint"]
assert session["current_epic"]
assert session["current_engineering_task"]
assert session["current_runtime"]
assert session["current_ai_provider"]
assert session["session_history"], "expected persisted session history"
assert session["recent_activity"], "expected recent activity"
print("engineering session PASS")
PY

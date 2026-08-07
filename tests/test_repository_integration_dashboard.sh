#!/usr/bin/env bash
set -euo pipefail

cd /home/runner/work/AI-Toolkit/AI-Toolkit

PYTHONPATH=lib python3 - <<'PY'
from python.dashboard.service import EngineeringDashboardService

service = EngineeringDashboardService(repository_root=".", workspace_root="..")
payload = service.build(refresh=True)
inspection = payload["home"]["latest_repository_inspection"]
repository = payload["workspace"]["repositories"][0]

assert inspection["languages"], "expected language distribution from repository engine"
assert inspection["tech_stack"], "expected technology stack from repository engine"
assert repository["name"] == "AI-Toolkit"
assert repository["implementation_progress"].endswith("%")
print("dashboard repository integration PASS")
PY

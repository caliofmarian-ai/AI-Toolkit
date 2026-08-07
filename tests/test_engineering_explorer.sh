#!/usr/bin/env bash
set -euo pipefail

cd /home/runner/work/AI-Toolkit/AI-Toolkit

PYTHONPATH=lib python3 - <<'PY'
from python.dashboard.service import EngineeringDashboardService

service = EngineeringDashboardService(repository_root=".", workspace_root="..")
payload = service.build(refresh=True)
capabilities = {item["slug"]: item for item in payload["capabilities"]["items"]}
assert "engineering_context" in payload

for slug in ["dashboard", "project-manager", "engineering-session", "engineering-explorer", "repository-engine"]:
    assert slug in capabilities, f"missing capability {slug}"

dashboard = capabilities["dashboard"]
assert dashboard["implementation_percentage"] > 0
assert dashboard["status"] in {"Planned", "In Progress", "Implemented", "Validated", "Operational", "Blocked"}
assert dashboard["why"]["problem"]
assert dashboard["unlock_conditions"]
print("engineering explorer PASS")
PY

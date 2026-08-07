#!/usr/bin/env bash
set -euo pipefail

cd /home/runner/work/AI-Toolkit/AI-Toolkit

PYTHONPATH=lib python3 - <<'PY'
from python.dashboard.service import EngineeringDashboardService

service = EngineeringDashboardService(repository_root=".", workspace_root="..")
payload = service.build(refresh=True)
cards = {card["label"]: card["value"] for card in payload["home"]["summary_cards"]}

required = {
    "Current Project",
    "Current Repository",
    "Current Branch",
    "Current Sprint",
    "Current Epic",
    "Current Issue",
    "Current Engineering Task",
    "Current AI Provider",
    "Current Runtime Status",
    "Repository Health",
    "Repository Statistics",
    "Latest Repository Inspection",
}

missing = sorted(required - set(cards))
assert not missing, f"missing home cards: {missing}"
assert payload["home"]["recent_reports"], "expected recent reports"
assert payload["home"]["repository_statistics"]["total_files"] > 0
assert payload["home"]["latest_repository_inspection"]["tech_stack"], "expected tech stack"
print("dashboard home PASS")
PY

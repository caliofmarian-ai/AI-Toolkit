#!/data/data/com.termux/files/usr/bin/bash
set -e

python3 - <<'PY'
import sys

sys.path.insert(0,"lib")

from python.agent_runtime.registry import build_runtime
from python.agent_runtime.models import AgentContext

runtime = build_runtime()

result = runtime.execute(
    "develop",
    AgentContext(repository=".")
)

roadmap = result.data["roadmap"]

print()
print("Roadmap status:", roadmap["status"])
print("Estimated hours:", roadmap["estimated_hours"])
print()

for phase in roadmap["phases"]:
    print(phase["name"])
    for item in phase["items"]:
        print(" -", item)

print()
print("Autonomous Planner PASS")
PY

grep -A40 "## Roadmap" .ai/audit/development_report.md

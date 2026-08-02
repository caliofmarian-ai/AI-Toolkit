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

state = result.data["execution_state"]

print()

print("Coordinator:", state["status"])

for phase in state["phases"]:
    print(
        phase["name"],
        "->",
        phase["status"]
    )

print()

print("Execution Coordinator PASS")
PY

test -f .ai/execution_state.json

grep -A20 "Execution State" .ai/audit/development_report.md

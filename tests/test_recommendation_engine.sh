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

print()

for item in result.data["recommendations_generated"]:
    print(item["priority"], "-", item["title"])

print()

print("Recommendation Engine PASS")
PY

grep -A20 "## Next Actions" .ai/audit/development_report.md

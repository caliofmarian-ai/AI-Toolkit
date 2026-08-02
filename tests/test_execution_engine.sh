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

for item in result.data["execution"]:
    print(item["batch"], "->", item["status"])

print()
print("Execution Engine PASS")
PY

test -f .ai/batches/BATCH-001/execution.log
test -f .ai/batches/BATCH-002/execution.log

echo
echo "Execution logs created."

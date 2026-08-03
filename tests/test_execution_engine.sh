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

generated = result.data["generated_batches"]
execution = result.data["execution"]

assert len(execution) == len(generated), (
    f"Execution count {len(execution)} != generated count {len(generated)}"
)

for item in execution:
    print(item["batch"], "->", item["status"])

print()
print("Execution Engine PASS")
PY

echo
echo "Execution results match generated batches."

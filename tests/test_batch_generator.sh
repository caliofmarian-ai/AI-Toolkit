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

for batch in result.data["generated_batches"]:
    print(batch["identifier"], batch["title"], "-", batch["priority"])

print()
print("Batch Generator PASS")
PY

grep -A20 "## Generated Batches" .ai/audit/development_report.md

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

for folder in result.data["materialized_batches"]:
    print(folder)

print()

print("GitHub Materialization PASS")
PY

test -f .ai/batches/BATCH-001/issue.md
test -f .ai/batches/BATCH-001/checklist.md
test -f .ai/batches/BATCH-001/pull_request.md
test -f .ai/batches/BATCH-001/implementation_plan.md
test -f .ai/batches/BATCH-001/metadata.json

echo
echo "Artifacts generated successfully."

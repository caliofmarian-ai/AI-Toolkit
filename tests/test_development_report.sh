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

assert result.success

print()
print("Development report generated.")
print()
print("Development Report PASS")
PY

test -f .ai/audit/development_report.md
head -20 .ai/audit/development_report.md

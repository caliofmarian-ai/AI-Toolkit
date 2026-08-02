#!/data/data/com.termux/files/usr/bin/bash
set -e

python3 - <<'PY'
import sys

sys.path.insert(0,"lib")

from python.agent_runtime.registry import build_runtime
from python.agent_runtime.models import AgentContext

runtime = build_runtime()

runtime.execute(
    "develop",
    AgentContext(repository=".")
)

print()
print("Profiler PASS")
PY

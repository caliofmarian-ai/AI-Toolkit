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

review = result.data["review"]

print()

print("Status :", review["status"])
print("Score  :", review["score"])

print()

for line in review["summary"]:
    print("-", line)

print()

print("Review Agent PASS")
PY

grep -A15 "## Review" .ai/audit/development_report.md

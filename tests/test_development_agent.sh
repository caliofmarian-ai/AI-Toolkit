#!/data/data/com.termux/files/usr/bin/bash
set -e

python3 - <<'PY'
import sys

sys.path.insert(0,"lib")

from python.agent_runtime.registry import build_runtime
from python.agent_runtime.models import AgentContext

runtime = build_runtime()

print("Registered agents:")
print(runtime.list_agents())

result = runtime.execute(
    "develop",
    AgentContext(repository=".")
)

assert result.success

print()
print(result.messages[0])
print()

print("Repository files:",
      result.data["repository"]["files"])

print("Dependencies:",
      result.data["dependencies"]["dependencies"])

print("Validation:",
      result.data["validation"]["passed"])

print("Planning tasks:",
      len(result.data["planning"].tasks))

print("Canonical docs:",
      len(result.data["canonical"]["canonical_documents"]))

print("Semantic files:",
      len(result.data["semantic"]))

print("Knowledge graph nodes:",
      len(result.data["knowledge_graph"]["nodes"]))

print()
print("Development Agent PASS")
PY

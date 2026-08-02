#!/data/data/com.termux/files/usr/bin/bash
set -e

python3 - <<'PY'
import sys

sys.path.insert(0,"lib")

from python.agent_runtime.runtime import AgentRuntime
from python.agent_runtime.models import AgentContext

from python.agents.repository_inspector_agent import RepositoryInspectorAgent

runtime = AgentRuntime()

runtime.register(
    RepositoryInspectorAgent.NAME,
    RepositoryInspectorAgent()
)

print("Registered Agents:")
print(runtime.list_agents())

result = runtime.execute(
    "inspect",
    AgentContext(repository=".")
)

assert result.success

print()
print(result.messages[0])
print(result.data["repository_health"])

print()
print("Agent Runtime PASS")
PY

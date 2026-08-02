#!/data/data/com.termux/files/usr/bin/bash
set -e

python3 - <<'PY'
import sys
from pathlib import Path

sys.path.insert(0, "lib")

from python.agent_runtime.registry import build_runtime
from python.agent_runtime.models import AgentContext

runtime = build_runtime()

print("=== REGISTERED AGENTS ===")
print(runtime.list_agents())

assert "inspect" in runtime.list_agents()
assert "develop" in runtime.list_agents()

print()
print("=== EXECUTE DEVELOPMENT AGENT ===")

result = runtime.execute(
    "develop",
    AgentContext(repository=".")
)

assert result.success

print(result.messages[0])

print()
print("=== VERIFY REPORTS ===")

assert Path(".ai/audit/development_report.md").exists()
assert Path(".ai/audit/repository_report.md").exists()

print("Reports OK")

print()
print("=== VERIFY BATCHES ===")

batches = result.data["generated_batches"]

assert len(batches) > 0

print("Generated:", len(batches))

print()
print("=== VERIFY MATERIALIZATION ===")

for folder in result.data["materialized_batches"]:
    p = Path(folder)

    assert (p / "metadata.json").exists()
    assert (p / "issue.md").exists()
    assert (p / "implementation_plan.md").exists()
    assert (p / "pull_request.md").exists()

print("Materialization OK")

print()
print("=== VERIFY EXECUTION ===")

execution = result.data["execution"]

assert len(execution) == len(batches)

for item in execution:
    assert item["status"] == "COMPLETED"

print("Execution OK")

print()
print("=== VERIFY KNOWLEDGE GRAPH ===")

assert len(result.data["knowledge_graph"]["nodes"]) > 0
assert len(result.data["knowledge_graph"]["edges"]) > 0

print("Knowledge Graph OK")

print()
print("=== VERIFY SEMANTIC MODEL ===")

assert len(result.data["semantic"]) > 0

print("Semantic Engine OK")

print()
print("===================================")
print("END-TO-END INTEGRATION TEST PASS")
print("===================================")
PY

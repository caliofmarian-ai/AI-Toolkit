#!/data/data/com.termux/files/usr/bin/bash
set -e

python3 - <<'PY'
import sys
from pathlib import Path

sys.path.insert(0, "lib")

from python.workspace_orchestrator.engine import WorkspaceOrchestrator

workspace = str(Path(".").resolve().parent)

results = WorkspaceOrchestrator().execute(workspace)

print()
print("Repositories processed:", len(results))
print()

for item in results:

    print(item["repository"], "->", item["status"])

    if item["status"] == "SUCCESS":
        print(" Score:", item["report_score"])
        print(" Health:", item["health"])
        print(" Batches:", item["batches"])
    else:
        print(" Error:", item["error"])

    print()

assert len(results) > 0

print("Workspace Orchestrator PASS")
PY

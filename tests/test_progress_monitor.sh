#!/data/data/com.termux/files/usr/bin/bash
set -e

python3 - <<'PY'
import sys
from pathlib import Path

sys.path.insert(0,"lib")

from python.workspace_orchestrator.engine import WorkspaceOrchestrator

workspace = str(Path(".").resolve().parent)

results = WorkspaceOrchestrator().execute(workspace)

print()

print("SUMMARY")
print("-------")

for item in results:

    if item["status"] == "SUCCESS":
        print(
            f'{item["repository"]}: '
            f'{item["elapsed"]:.2f}s'
        )
    else:
        print(
            f'{item["repository"]}: FAILED'
        )

print()
print("Progress Monitor PASS")
PY

#!/data/data/com.termux/files/usr/bin/bash
set -e

python3 - <<'PY'
import sys

sys.path.insert(0,"lib")

from pathlib import Path
from python.workspace_manager.engine import WorkspaceManager

repos = WorkspaceManager().discover(
    str(Path(".").resolve().parent)
)

print()

print("Repositories discovered:", len(repos))
print()

for repo in repos:
    print("-", repo["name"])

print()
print("Workspace Manager PASS")
PY

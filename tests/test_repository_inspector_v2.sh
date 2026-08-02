#!/data/data/com.termux/files/usr/bin/bash
set -e

python3 - <<'PY'
import sys

sys.path.insert(0,"lib")

from python.repository_inspector_v2.engine import RepositoryInspectorV2

agent = RepositoryInspectorV2(".")

report = agent.export(
    ".ai/audit/repository_inspector_v2.json"
)

print()
print("Repository Health :", report["repository_health"])
print("Files             :", report["repository"]["files"])
print("Dependencies      :", report["dependencies"]["dependencies"])
print("Validation Passed :", report["validation"]["passed"])
print("Planning Tasks    :", len(report["plan"]["tasks"]))
print()
print("Repository Inspector v2 PASS")
PY

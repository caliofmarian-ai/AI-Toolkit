#!/data/data/com.termux/files/usr/bin/bash
set -e

python3 - <<'PY'
import sys

sys.path.insert(0,"lib")

from python.repository_inspector_v2.engine import RepositoryInspectorV2

report = RepositoryInspectorV2(".").inspect()

print()
print("Repository Score :", report["repository_score"])
print("Findings         :", len(report["findings"]))
print("Recommendations  :", len(report["recommendations"]))
print()
print("Repository Analysis PASS")
PY

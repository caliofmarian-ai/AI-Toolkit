#!/data/data/com.termux/files/usr/bin/bash
set -e

python3 - <<'PY'
import sys

sys.path.insert(0,"lib")

from python.repository_inspector_v2.engine import RepositoryInspectorV2

RepositoryInspectorV2(".").export(
    ".ai/audit/repository_inspector_v2.json"
)

print("Markdown report generated.")
PY

test -f .ai/audit/repository_report.md

echo
echo "Markdown Report PASS"

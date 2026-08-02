#!/data/data/com.termux/files/usr/bin/bash
set -e

python3 - <<'PY'
import sys

sys.path.insert(0,"lib")

from python.semantic_engine.engine import SemanticEngine

report = SemanticEngine(".").analyze()

print()

print("Python files analysed:", len(report))

classes = 0
functions = 0

for item in report.values():
    classes += len(item["classes"])
    functions += len(item["functions"])

print("Classes :", classes)
print("Functions:", functions)

print()

print("Semantic Engine PASS")
PY

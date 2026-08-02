#!/data/data/com.termux/files/usr/bin/bash
set -e

python3 - <<'PY'
import sys

sys.path.insert(0,"lib")

from python.planning_engine.engine import PlanningEngine
from python.planning_engine.exporter import PlanningExporter

engine = PlanningEngine(".")

plan = engine.build_plan()

assert len(plan.tasks) == 3

PlanningExporter.export(
    plan,
    ".ai/audit/execution_plan.json"
)

print("Plan:", plan.identifier)

for task in plan.tasks:
    print("-", task.identifier, task.title)

print()
print("Planning Engine PASS")
PY

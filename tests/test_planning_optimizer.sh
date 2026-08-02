#!/data/data/com.termux/files/usr/bin/bash
set -e

python3 - <<'PY'
import sys

sys.path.insert(0,"lib")

from python.planning_optimizer.engine import PlanningOptimizer

result = PlanningOptimizer().scan(".")

print()
print("Planning Optimizer")
print("------------------")
print("Files:", result["count"])
print("Elapsed: %.2fs" % result["elapsed"])
print()
print("Planning Optimizer PASS")
PY

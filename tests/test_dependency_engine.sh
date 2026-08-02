#!/data/data/com.termux/files/usr/bin/bash
set -e

python3 - <<'PY'
import sys

sys.path.insert(0,"lib/python/dependency_engine")

from engine import DependencyEngine
from exporter import DependencyExporter

engine = DependencyEngine(".")

dependencies = engine.discover()

stats = engine.statistics()

assert stats["dependencies"] > 0

DependencyExporter.export(
    dependencies,
    ".ai/audit/dependency_graph.json"
)

print(stats)

print("Dependency Engine PASS")
PY

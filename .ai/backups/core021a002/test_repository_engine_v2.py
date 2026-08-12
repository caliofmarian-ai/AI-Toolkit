#!/data/data/com.termux/files/usr/bin/bash
set -e

python3 - <<'PY'
import sys

sys.path.insert(0,"lib/python/repository_engine")

from engine import RepositoryEngine
from exporter import RepositoryExporter

engine = RepositoryEngine(".")

inventory = engine.discover()

stats = engine.statistics()

assert stats["items"] > 0
assert stats["files"] > 0

RepositoryExporter.export(
    inventory,
    ".ai/audit/repository_inventory_v2.json"
)

print(stats)

print("Repository Engine PASS")
PY

#!/data/data/com.termux/files/usr/bin/bash
set -e

python3 - <<'PY'
import sys

sys.path.insert(0,"lib/python/validation_engine")

from engine import ValidationEngine
from exporter import ValidationExporter

engine = ValidationEngine(".")

results = engine.validate()

stats = engine.statistics()

assert stats["checks"] > 0

ValidationExporter.export(
    results,
    ".ai/audit/validation_report.json"
)

print(stats)

print("Validation Engine PASS")
PY

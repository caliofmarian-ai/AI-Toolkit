#!/data/data/com.termux/files/usr/bin/bash
set -e

python3 - <<'PY'
import sys

sys.path.insert(0,"lib")

from python.validation_engine.engine import ValidationEngine
from python.validation_engine.exporter import ValidationExporter

engine = ValidationEngine(".")

results = engine.validate()

stats = engine.statistics()

assert stats["checks"] > 0
assert all(r.identifier.startswith("ATK-VAL-") for r in results)

ValidationExporter.export(
    results,
    ".ai/audit/validation_report.json"
)

print(stats)

print("Validation Engine PASS")
PY

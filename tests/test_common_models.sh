#!/data/data/com.termux/files/usr/bin/bash
set -e

python3 - <<'PY'
import sys

sys.path.insert(0,"lib")

from python.common.models import Batch

batch = Batch(
    identifier="BATCH-001",
    title="Example",
    priority="HIGH",
    reason="Validation",
    estimated_hours=2,
)

assert batch.status == "READY"

print(batch)

print()

print("Common Models PASS")
PY

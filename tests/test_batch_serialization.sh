#!/data/data/com.termux/files/usr/bin/bash
set -e

python3 - <<'PY'
import sys

sys.path.insert(0,"lib")

from python.common.models import Batch

batch = Batch(
    identifier="BATCH-001",
    title="Serialization",
    priority="HIGH",
    reason="Test",
    estimated_hours=5,
)

data = batch.to_dict()

clone = Batch.from_dict(data)

assert clone.identifier == batch.identifier
assert clone.title == batch.title
assert clone.priority == batch.priority
assert clone.reason == batch.reason

print()
print("Serialization PASS")
PY

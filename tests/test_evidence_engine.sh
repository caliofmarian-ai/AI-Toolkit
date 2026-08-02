#!/data/data/com.termux/files/usr/bin/bash
set -e

python3 - <<'PY'
import sys

sys.path.insert(0,"lib")

from python.canonical_audit.engine import CanonicalAuditEngine

audit = CanonicalAuditEngine(".").audit()

print()

for name, evidence in audit["evidence"].items():

    print(name)

    total = (
        len(evidence["python"]) +
        len(evidence["shell"]) +
        len(evidence["tests"]) +
        len(evidence["docs"])
    )

    print("Evidence:", total)

print()

print("Evidence Engine PASS")
PY

#!/data/data/com.termux/files/usr/bin/bash
set -e

python3 - <<'PY'
import sys

sys.path.insert(0,"lib")

from python.canonical_audit.engine import CanonicalAuditEngine

audit = CanonicalAuditEngine(".").audit()

print()
print("Canonical Docs :", len(audit["canonical_documents"]))
print("Python Modules :", len(audit["python_modules"]))
print("Missing Modules:", len(audit["missing_modules"]))

if audit["missing_modules"]:
    print()
    print("Examples:")
    for item in audit["missing_modules"][:10]:
        print("-", item)

print()
print("Canonical Audit PASS")
PY

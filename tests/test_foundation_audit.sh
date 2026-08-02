#!/data/data/com.termux/files/usr/bin/bash
set -e

python3 lib/python/foundation_audit.py

test -f .ai/audit/foundation_audit_001.json

echo
echo "Foundation Audit PASS"

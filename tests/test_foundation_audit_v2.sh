#!/data/data/com.termux/files/usr/bin/bash
set -e

python3 lib/python/foundation_audit/main.py

test -f .ai/audit/foundation_audit_002.json

echo
echo "Foundation Audit v2 PASS"

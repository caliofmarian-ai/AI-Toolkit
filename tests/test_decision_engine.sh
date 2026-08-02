#!/data/data/com.termux/files/usr/bin/bash
set -e

python3 lib/python/decision_engine.py

test -f .ai/memory/decision.json

echo
echo "========== DECISION =========="

cat .ai/memory/decision.json

echo
echo "Decision Engine PASS"

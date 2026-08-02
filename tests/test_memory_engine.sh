#!/data/data/com.termux/files/usr/bin/bash
set -e

python3 lib/python/memory_engine.py .

test -f .ai/memory/history.json
test -f .ai/memory/index.json

echo
echo "========== INDEX =========="
cat .ai/memory/index.json

echo
echo "Memory Engine PASS"

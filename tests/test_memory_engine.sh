#!/data/data/com.termux/files/usr/bin/bash
set -e

python3 lib/python/memory_engine.py .

test -f .ai/memory/history.json

echo
echo "Memory Engine PASS"

#!/data/data/com.termux/files/usr/bin/bash
set -e

python3 lib/python/repository_inventory.py

test -f .ai/audit/repository_inventory.json

echo
echo "Repository Inventory PASS"

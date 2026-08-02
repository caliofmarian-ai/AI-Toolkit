#!/data/data/com.termux/files/usr/bin/bash
set -e

echo
echo "=== INVENTORY ==="
bash bin/ai inventory

echo
echo "=== DEPENDENCIES ==="
bash bin/ai dependencies

echo
echo "=== VALIDATE ==="
bash bin/ai validate

echo
echo "=== PLAN ==="
bash bin/ai plan

echo
echo "CLI PASS"

#!/data/data/com.termux/files/usr/bin/bash
set -e

echo
echo "=== INVENTORY ==="
bin/ai inventory

echo
echo "=== DEPENDENCIES ==="
bin/ai dependencies

echo
echo "=== VALIDATE ==="
bin/ai validate

echo
echo "=== PLAN ==="
bin/ai plan

echo
echo "CLI PASS"

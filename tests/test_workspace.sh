#!/data/data/com.termux/files/usr/bin/bash
set -e

ROOT="${1:-.}"

echo "========== Workspace Test =========="

bash lib/workspace_engine.sh "$ROOT"

echo
echo "PASS"

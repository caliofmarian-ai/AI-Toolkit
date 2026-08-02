#!/data/data/com.termux/files/usr/bin/bash
set -e

ROOT="${1:-.}"

echo "========== Workspace Validation =========="

bash lib/workspace_engine.sh "$ROOT"

echo
echo "All workspace checks passed."

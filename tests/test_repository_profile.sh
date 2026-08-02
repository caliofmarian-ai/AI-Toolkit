#!/data/data/com.termux/files/usr/bin/bash
set -e

ROOT="${1:-.}"

echo "========== Repository Intelligence Test =========="

bash lib/repository_profile_engine.sh "$ROOT"

echo
echo "PASS"

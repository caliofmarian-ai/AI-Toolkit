#!/data/data/com.termux/files/usr/bin/bash

set -e

ACTION="${1:-help}"
ISSUE="${2:-}"
ROOT="$(pwd)"

case "$ACTION" in

start)

if [ -z "$ISSUE" ]; then
    echo "Usage:"
    echo "ai issue start <number>"
    exit 1
fi

echo
echo "======================================"
echo " AI ISSUE WORKFLOW"
echo "======================================"

echo
echo "[1/7] Reading GitHub Issue..."
echo
gh issue view "$ISSUE"

echo
echo "[2/7] Git status"
git status

echo
echo "[3/7] Current branch"
git branch --show-current

echo
echo "[4/7] Repository summary"
bash "$(dirname "$0")/repository_summary.sh" "$ROOT"

echo
echo "[5/7] Generate context"
bash "$(dirname "$0")/context_engine.sh" "$ROOT"

echo
echo "[6/7] Prepare work session"
bash "$(dirname "$0")/work_engine.sh" "$ROOT"

echo
echo "[7/7] Ready"

echo
echo "======================================"
echo " READY TO IMPLEMENT ISSUE #$ISSUE"
echo "======================================"

;;

*)

echo "Usage:"
echo
echo "ai issue start <number>"

;;

esac

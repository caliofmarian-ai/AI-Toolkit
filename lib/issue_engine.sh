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
echo "[1/6] Git status"
git status

echo
echo "[2/6] Current branch"
git branch --show-current

echo
echo "[3/6] Repository inspection"
bash "$(dirname "$0")/repository_summary.sh" "$ROOT"

echo
echo "[4/6] Generate context"
bash "$(dirname "$0")/context_engine.sh" "$ROOT"

echo
echo "[5/6] Prepare work session"
bash "$(dirname "$0")/work_engine.sh" "$ROOT"

echo
echo "[6/6] Issue"

echo "Issue: #$ISSUE"

echo
echo "======================================"
echo " READY TO START ISSUE #$ISSUE"
echo "======================================"

;;

*)

echo
echo "Usage"

echo
echo "ai issue start <number>"

;;

esac


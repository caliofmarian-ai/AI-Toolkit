#!/data/data/com.termux/files/usr/bin/bash
set -e

python3 lib/python/autonomous_workflow_engine.py

test -f .ai/memory/workflow.json

echo
echo "========== WORKFLOW =========="
cat .ai/memory/workflow.json

echo
echo "Autonomous Workflow PASS"

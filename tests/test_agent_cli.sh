#!/data/data/com.termux/files/usr/bin/bash
set -e

echo
echo "===== AGENT LIST ====="

python3 - <<'PY'
import sys

sys.path.insert(0,"lib")

from python.agent_runtime.registry import build_runtime

runtime = build_runtime()

print(runtime.list_agents())
PY

echo
echo "===== AGENT EXECUTION ====="

bash bin/ai inspect

echo
echo "AGENT CLI PASS"

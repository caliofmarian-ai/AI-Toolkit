#!/data/data/com.termux/files/usr/bin/bash
set -e

python3 lib/python/knowledge_graph_engine.py

test -f .ai/memory/knowledge_graph.json

echo
echo "========== GRAPH =========="
python3 - <<'PY'
import json
with open(".ai/memory/knowledge_graph.json") as f:
    g=json.load(f)
print("Nodes :",len(g["nodes"]))
print("Edges :",len(g["edges"]))
PY

echo
echo "Knowledge Graph PASS"

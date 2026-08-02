#!/data/data/com.termux/files/usr/bin/bash
set -e

python3 - <<'PY'
import sys

sys.path.insert(0,"lib")

from python.knowledge_graph_v2.engine import KnowledgeGraphEngine

engine = KnowledgeGraphEngine(".")

graph = engine.export(
    ".ai/audit/knowledge_graph_v2.json"
)

print()

print("Nodes :", len(graph["nodes"]))
print("Edges :", len(graph["edges"]))

print()

print("Knowledge Graph PASS")
PY

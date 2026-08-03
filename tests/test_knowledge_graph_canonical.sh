#!/data/data/com.termux/files/usr/bin/bash
set -e

python3 - <<'PY'
import sys
sys.path.insert(0, "lib")

from python.canonical_repository import CanonicalRepository
from python.knowledge_graph import CanonicalKnowledgeGraph, CanonicalKnowledgeGraphBuilder
from pathlib import Path

repo = CanonicalRepository.load_from_directory(Path("docs/canonical"))
builder = CanonicalKnowledgeGraphBuilder()
graph = builder.build(repo)

assert graph.node_count() > 0
assert graph.edge_count() > 0

data = graph.to_dict()
assert "nodes" in data
assert "edges" in data

graph2 = CanonicalKnowledgeGraph.from_dict(data)
assert graph2.node_count() == graph.node_count()

print(f"Graph: {graph.node_count()} nodes, {graph.edge_count()} edges")
print("Knowledge Graph (Canonical) PASS")
PY

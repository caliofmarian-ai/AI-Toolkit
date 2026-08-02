#!/usr/bin/env python3

import json
from pathlib import Path

ROOT = Path(".").resolve()

GRAPH = {
    "repository": ROOT.name,
    "nodes": [],
    "edges": []
}

def add_node(node_type, name, path):
    GRAPH["nodes"].append({
        "type": node_type,
        "name": name,
        "path": str(path.relative_to(ROOT))
    })

def connect(source, target, relation):
    GRAPH["edges"].append({
        "from": source,
        "to": target,
        "relation": relation
    })

for f in sorted((ROOT / "docs" / "canonical").glob("*.md")):
    add_node("canonical", f.stem, f)

for f in sorted((ROOT / "lib").glob("*engine*")):
    add_node("engine", f.stem, f)

for f in sorted((ROOT / "tests").glob("*")):
    if f.is_file():
        add_node("test", f.stem, f)

for f in sorted((ROOT / ".ai" / "memory").glob("*")):
    if f.is_file():
        add_node("memory", f.stem, f)

for node in GRAPH["nodes"]:
    connect(ROOT.name, node["name"], "contains")

OUT = ROOT / ".ai" / "memory" / "knowledge_graph.json"

OUT.write_text(
    json.dumps(GRAPH, indent=2),
    encoding="utf-8"
)

print("==================================")
print("Knowledge Graph Engine")
print("==================================")
print()
print("Nodes :", len(GRAPH["nodes"]))
print("Edges :", len(GRAPH["edges"]))
print()
print("Saved:")
print(OUT)

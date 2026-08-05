# DEPRECATED: This module is frozen for compatibility only.
# See docs/implementation/MODULE_CLASSIFICATION.md — Disposition: DEPRECATE
# Do not add features. Use the canonical module packages instead.

#!/usr/bin/env python3

import json
from pathlib import Path

ROOT = Path(".").resolve()

MEMORY = ROOT / ".ai" / "memory"
CONTEXT = ROOT / ".ai" / "context"

INDEX = MEMORY / "index.json"
GRAPH = MEMORY / "knowledge_graph.json"
PROFILE = CONTEXT / "repository_profile.json"

decision = {
    "status": "ready",
    "recommendations": [],
    "metrics": {}
}

if PROFILE.exists():
    profile = json.loads(PROFILE.read_text(encoding="utf-8"))

    engines = profile.get("statistics", {}).get("engines", 0)
    tests = profile.get("statistics", {}).get("tests", 0)

    decision["metrics"]["engines"] = engines
    decision["metrics"]["tests"] = tests

    if tests < engines:
        decision["recommendations"].append(
            "Increase automated test coverage."
        )

if GRAPH.exists():
    graph = json.loads(GRAPH.read_text(encoding="utf-8"))

    decision["metrics"]["graph_nodes"] = len(graph["nodes"])
    decision["metrics"]["graph_edges"] = len(graph["edges"])

if INDEX.exists():
    idx = json.loads(INDEX.read_text(encoding="utf-8"))

    decision["metrics"]["memory_events"] = idx["events"]

decision["recommendations"].append(
    "Continue with IMP-004 Phase 2."
)

OUT = MEMORY / "decision.json"

OUT.write_text(
    json.dumps(decision, indent=2),
    encoding="utf-8"
)

print("==================================")
print("Decision Engine")
print("==================================")
print()

for k, v in decision["metrics"].items():
    print(f"{k}: {v}")

print()

print("Recommendations")

for r in decision["recommendations"]:
    print("-", r)

print()
print("Saved:", OUT)

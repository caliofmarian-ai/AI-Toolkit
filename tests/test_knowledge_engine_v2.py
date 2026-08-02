#!/data/data/com.termux/files/usr/bin/bash
set -e

python3 - <<'PY'
import sys

sys.path.insert(0,"lib/python/knowledge_engine")

from engine import KnowledgeEngine

engine = KnowledgeEngine()

engine.register(
    "ENGINE-001",
    "Knowledge Engine",
    "Engine"
)

assert len(engine.entities()) == 1

engine.export(".ai/audit/knowledge_database.json")

print("Knowledge Engine PASS")
PY

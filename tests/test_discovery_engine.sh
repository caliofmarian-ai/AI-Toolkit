#!/data/data/com.termux/files/usr/bin/bash
set -e

python3 - <<'PY'
import sys

sys.path.insert(0,"lib")

from python.discovery_engine.engine import DiscoveryEngine

engine = DiscoveryEngine(".")

docs = engine.discover_canonical_documents()

print()
print("Canonical documents discovered:", len(docs))
print()

for name, path in sorted(docs.items())[:20]:
    print("-", path)

print()
print("Discovery Engine PASS")
PY

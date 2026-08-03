#!/data/data/com.termux/files/usr/bin/bash
set -e

python3 - <<'PY'
import sys
sys.path.insert(0, "lib")

from python.canonical_repository import CanonicalRepository
from pathlib import Path

repo = CanonicalRepository.load_from_directory(Path("docs/canonical"))

assert len(repo.all_documents()) >= 10
assert repo.get_by_id("CANON-001") is not None
dep_graph = repo.dependency_graph()
assert isinstance(dep_graph, dict)

stats = repo.statistics()
assert "total_documents" in stats

print(f"Repository: {stats['total_documents']} documents")
print("Canonical Repository PASS")
PY

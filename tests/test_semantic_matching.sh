#!/data/data/com.termux/files/usr/bin/bash
set -e

python3 - <<'PY'
import sys
sys.path.insert(0, "lib")

from python.canonical_repository import CanonicalRepository
from python.semantic_matching import SemanticMatcher
from pathlib import Path

repo = CanonicalRepository.load_from_directory(Path("docs/canonical"))
matcher = SemanticMatcher(".")

matches = matcher.match_all(repo)

assert isinstance(matches, dict)
assert len(matches) > 0

total_matches = sum(len(m) for m in matches.values())
print(f"Total matches: {total_matches}")
print(f"Documents with matches: {sum(1 for m in matches.values() if m)}")
print("Semantic Matching PASS")
PY

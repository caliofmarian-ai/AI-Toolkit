#!/data/data/com.termux/files/usr/bin/bash
set -e

python3 - <<'PY'
import sys
sys.path.insert(0, "lib")

from python.canonical_repository import CanonicalRepository
from python.semantic_matching import SemanticMatcher
from python.coverage_engine import CoverageEngine
from pathlib import Path

repo = CanonicalRepository.load_from_directory(Path("docs/canonical"))
matcher = SemanticMatcher(".")
matches = matcher.match_all(repo)

engine = CoverageEngine(".")
metrics = engine.compute(repo, matches)

assert len(metrics) > 0
for m in metrics:
    assert 0.0 <= m.score <= 1.0, f"Invalid score for {m.category}: {m.score}"

summary = engine.summary(metrics)
assert "overall" in summary

print(f"Coverage categories: {len(metrics)}")
for m in metrics:
    print(f"  {m.category}: {m.score:.0%}")
print("Coverage Engine PASS")
PY

#!/data/data/com.termux/files/usr/bin/bash
set -e

python3 - <<'PY'
import sys
sys.path.insert(0, "lib")

from python.canonical_repository import CanonicalRepository
from python.semantic_matching import SemanticMatcher
from python.coverage_engine import CoverageEngine
from python.compliance_engine import ComplianceEngine
from pathlib import Path

repo = CanonicalRepository.load_from_directory(Path("docs/canonical"))
matcher = SemanticMatcher(".")
matches = matcher.match_all(repo)

coverage_engine = CoverageEngine(".")
coverage = coverage_engine.compute(repo, matches)

compliance_engine = ComplianceEngine(".")
metrics = compliance_engine.evaluate(repo, matches, coverage)

assert len(metrics) > 0
score = compliance_engine.overall_score(metrics)
assert 0.0 <= score <= 1.0

print(f"Compliance categories: {len(metrics)}")
print(f"Overall score: {score:.0%}")
print("Compliance Engine PASS")
PY

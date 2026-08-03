#!/data/data/com.termux/files/usr/bin/bash
set -e

python3 - <<'PY'
import sys
sys.path.insert(0, "lib")

from python.canonical_repository import CanonicalRepository
from python.semantic_matching import SemanticMatcher
from python.coverage_engine import CoverageEngine
from python.drift_engine import DriftEngine
from pathlib import Path

repo = CanonicalRepository.load_from_directory(Path("docs/canonical"))
matcher = SemanticMatcher(".")
matches = matcher.match_all(repo)

coverage_engine = CoverageEngine(".")
coverage = coverage_engine.compute(repo, matches)

engine = DriftEngine(".")
findings = engine.detect(repo, matches, coverage)

assert isinstance(findings, list)
dist = engine.severity_distribution(findings)
assert isinstance(dist, dict)

plan = engine.remediation_plan(findings)
assert isinstance(plan, list)

print(f"Drift findings: {len(findings)}")
print(f"Severity distribution: {dist}")
print("Drift Engine PASS")
PY

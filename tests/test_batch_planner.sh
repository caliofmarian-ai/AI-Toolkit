#!/data/data/com.termux/files/usr/bin/bash
set -e

python3 - <<'PY'
import sys
sys.path.insert(0, "lib")

from python.canonical_repository import CanonicalRepository
from python.semantic_matching import SemanticMatcher
from python.coverage_engine import CoverageEngine
from python.drift_engine import DriftEngine
from python.batch_planner import BatchPlanner
from pathlib import Path

repo = CanonicalRepository.load_from_directory(Path("docs/canonical"))
matcher = SemanticMatcher(".")
matches = matcher.match_all(repo)

coverage_engine = CoverageEngine(".")
coverage = coverage_engine.compute(repo, matches)

drift_engine = DriftEngine(".")
findings = drift_engine.detect(repo, matches, coverage)

planner = BatchPlanner()
batches = planner.generate(repo, findings, coverage)

assert isinstance(batches, list)
for batch in batches:
    assert batch.id
    assert batch.priority is not None

roadmap = planner.roadmap(batches)
assert "immediate" in roadmap

print(f"Generated {len(batches)} batches")
print("Batch Planner PASS")
PY

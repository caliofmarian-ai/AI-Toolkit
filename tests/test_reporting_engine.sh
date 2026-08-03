#!/data/data/com.termux/files/usr/bin/bash
set -e

python3 - <<'PY'
import sys
sys.path.insert(0, "lib")

from python.canonical_repository import CanonicalRepository
from python.knowledge_graph import CanonicalKnowledgeGraphBuilder
from python.semantic_matching import SemanticMatcher
from python.coverage_engine import CoverageEngine
from python.compliance_engine import ComplianceEngine
from python.drift_engine import DriftEngine
from python.batch_planner import BatchPlanner
from python.reporting_engine import ReportingEngine
from pathlib import Path

repo = CanonicalRepository.load_from_directory(Path("docs/canonical"))
builder = CanonicalKnowledgeGraphBuilder()
graph = builder.build(repo)

matcher = SemanticMatcher(".")
matches = matcher.match_all(repo)

coverage_engine = CoverageEngine(".")
coverage = coverage_engine.compute(repo, matches)

compliance_engine = ComplianceEngine(".")
compliance = compliance_engine.evaluate(repo, matches, coverage)

drift_engine = DriftEngine(".")
findings = drift_engine.detect(repo, matches, coverage)

planner = BatchPlanner()
batches = planner.generate(repo, findings, coverage)

reporter = ReportingEngine()
reports = reporter.generate(repo, graph, matches, coverage, compliance, findings, batches)

assert "markdown" in reports
assert "json" in reports
assert "executive" in reports["markdown"]

print("Executive report length:", len(reports["markdown"]["executive"]))
print("Reporting Engine PASS")
PY

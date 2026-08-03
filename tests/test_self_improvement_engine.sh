#!/data/data/com.termux/files/usr/bin/bash
set -e

python3 - <<'PY'
import sys
import json
import tempfile
import os
from pathlib import Path

sys.path.insert(0, "lib")

# ---------------------------------------------------------------------------
# 1. Import all public API
# ---------------------------------------------------------------------------

from python.self_improvement_engine import (
    SelfImprovementEngine,
    ImprovementCoordinator,
    OptimizationPlanner,
    EvolutionPlanner,
    TechnicalDebtAnalyzer,
    PerformanceAnalyzer,
    CapabilityAnalyzer,
    IssueGenerator,
    BatchGenerator,
    CoreProposalEngine,
    RoadmapEvolutionEngine,
    ImprovementPersistence,
    ImprovementReportGenerator,
    IMPROVEMENT_VERSION,
    PRIORITY_CRITICAL,
    PRIORITY_HIGH,
    PRIORITY_MEDIUM,
    PRIORITY_LOW,
    EFFORT_LOW,
    EFFORT_MEDIUM,
    EFFORT_HIGH,
    TechnicalDebt,
    PerformanceMetric,
    CapabilityGap,
    ProposedIssue,
    ProposedBatch,
    CoreProposal,
    RoadmapUpdate,
    OptimizationPlan,
)

print("1. Imports OK")

# ---------------------------------------------------------------------------
# 2. Constants
# ---------------------------------------------------------------------------

assert IMPROVEMENT_VERSION == "1.0.0"
assert PRIORITY_HIGH == "high"
assert EFFORT_MEDIUM == "medium"
print("2. Constants OK")

# ---------------------------------------------------------------------------
# 3. TechnicalDebt model
# ---------------------------------------------------------------------------

debt = TechnicalDebt(
    debt_id="DEBT-001",
    category="legacy_module",
    component="lib/python/old_engine.py",
    description="Legacy top-level module",
    severity="low",
    estimated_effort="low",
    evidence={"file": "old_engine.py"},
    recommendation="Replace with dedicated package",
)
d = debt.to_dict()
assert d["debt_id"] == "DEBT-001"
assert d["category"] == "legacy_module"
assert d["severity"] == "low"
print("3. TechnicalDebt model OK")

# ---------------------------------------------------------------------------
# 4. PerformanceMetric model
# ---------------------------------------------------------------------------

metric = PerformanceMetric(
    metric_id="PERF-001",
    name="execution_duration_ms",
    value=1500.0,
    unit="ms",
    baseline=5000.0,
    trend="stable",
    evidence={"source": "CORE-015"},
)
d = metric.to_dict()
assert d["metric_id"] == "PERF-001"
assert d["value"] == 1500.0
assert d["trend"] == "stable"
print("4. PerformanceMetric model OK")

# ---------------------------------------------------------------------------
# 5. CapabilityGap model
# ---------------------------------------------------------------------------

gap = CapabilityGap(
    gap_id="GAP-CLI-EXECUTE",
    category="missing_cli_command",
    description="CLI command `ai execute` is not registered",
    priority=PRIORITY_HIGH,
    evidence={"source": "cli/main.py"},
)
d = gap.to_dict()
assert d["gap_id"] == "GAP-CLI-EXECUTE"
assert d["priority"] == PRIORITY_HIGH
print("5. CapabilityGap model OK")

# ---------------------------------------------------------------------------
# 6. ProposedIssue model
# ---------------------------------------------------------------------------

issue = ProposedIssue(
    issue_id="ISS-001",
    title="Fix legacy module",
    description="Remove legacy module",
    objective="Eliminate legacy code",
    motivation="Reduce technical debt",
    dependencies=[],
    acceptance_criteria=["Module removed", "Tests pass"],
    priority=PRIORITY_MEDIUM,
    estimated_effort=EFFORT_LOW,
    estimated_risk="low",
    affected_components=["lib/python/old.py"],
    canonical_references=[],
    evidence={"debt_id": "DEBT-001"},
    implementation_strategy="Remove the module",
    validation_strategy="Run test suite",
)
d = issue.to_dict()
assert d["issue_id"] == "ISS-001"
assert d["priority"] == PRIORITY_MEDIUM
assert isinstance(d["acceptance_criteria"], list)
print("6. ProposedIssue model OK")

# ---------------------------------------------------------------------------
# 7. ProposedBatch model
# ---------------------------------------------------------------------------

batch = ProposedBatch(
    batch_id="BATCH-IMP-001",
    title="Technical Debt Batch",
    objectives=["Fix legacy modules"],
    issue_ids=["ISS-001"],
    dependencies=[],
    execution_order=["ISS-001"],
    acceptance_criteria=["All issues resolved"],
    regression_strategy="Run full test suite",
    validation_strategy="Run ai evaluate",
    owner_approval_required=True,
    evidence={"priority": "medium"},
)
d = batch.to_dict()
assert d["batch_id"] == "BATCH-IMP-001"
assert d["owner_approval_required"] is True
print("7. ProposedBatch model OK")

# ---------------------------------------------------------------------------
# 8. TechnicalDebtAnalyzer — against AI Toolkit
# ---------------------------------------------------------------------------

analyzer = TechnicalDebtAnalyzer(".")
debt_items = analyzer.analyze()
assert isinstance(debt_items, list)
# Should detect at least some legacy modules
for item in debt_items:
    assert isinstance(item, TechnicalDebt)
    assert item.debt_id.startswith("DEBT-")
    assert item.severity in ("low", "medium", "high", "critical")
print(f"8. TechnicalDebtAnalyzer OK ({len(debt_items)} items detected)")

# ---------------------------------------------------------------------------
# 9. PerformanceAnalyzer
# ---------------------------------------------------------------------------

perf_analyzer = PerformanceAnalyzer(".")
metrics = perf_analyzer.analyze()
assert isinstance(metrics, list)
for m in metrics:
    assert isinstance(m, PerformanceMetric)
print(f"9. PerformanceAnalyzer OK ({len(metrics)} metrics)")

# ---------------------------------------------------------------------------
# 10. CapabilityAnalyzer — against AI Toolkit
# ---------------------------------------------------------------------------

cap_analyzer = CapabilityAnalyzer(".")
gaps = cap_analyzer.analyze()
assert isinstance(gaps, list)
for g in gaps:
    assert isinstance(g, CapabilityGap)
    assert g.gap_id.startswith("GAP-")
print(f"10. CapabilityAnalyzer OK ({len(gaps)} gaps detected)")

# ---------------------------------------------------------------------------
# 11. IssueGenerator
# ---------------------------------------------------------------------------

gen = IssueGenerator()

debt_issues = gen.generate_from_debt(debt_items[:3])
assert isinstance(debt_issues, list)
for issue in debt_issues:
    assert isinstance(issue, ProposedIssue)
    assert issue.issue_id.startswith("ISS-")
    assert issue.priority in (PRIORITY_CRITICAL, PRIORITY_HIGH, PRIORITY_MEDIUM, PRIORITY_LOW)

gap_issues = gen.generate_from_gaps(gaps)
assert isinstance(gap_issues, list)
for issue in gap_issues:
    assert isinstance(issue, ProposedIssue)
print("11. IssueGenerator OK")

# ---------------------------------------------------------------------------
# 12. BatchGenerator
# ---------------------------------------------------------------------------

batch_gen = BatchGenerator()
all_issues = debt_issues + gap_issues

batches = batch_gen.generate(all_issues)
assert isinstance(batches, list)
for b in batches:
    assert isinstance(b, ProposedBatch)
    assert b.owner_approval_required is True
    assert b.batch_id.startswith("BATCH-IMP-")

# Empty input
empty_batches = batch_gen.generate([])
assert empty_batches == []
print("12. BatchGenerator OK")

# ---------------------------------------------------------------------------
# 13. CoreProposalEngine
# ---------------------------------------------------------------------------

core_engine = CoreProposalEngine()

# Should not propose when score is high
no_proposals = core_engine.generate([], evaluation_score=0.9)
assert no_proposals == []

# Should not duplicate existing COREs
for_existing = core_engine.generate([
    CapabilityGap("GAP-X", "missing_package", "missing test", PRIORITY_HIGH, {})
], evaluation_score=0.5)
assert isinstance(for_existing, list)
print("13. CoreProposalEngine OK")

# ---------------------------------------------------------------------------
# 14. RoadmapEvolutionEngine
# ---------------------------------------------------------------------------

roadmap_engine = RoadmapEvolutionEngine()

updates = roadmap_engine.generate_updates(
    capability_gaps=[CapabilityGap("GAP-X", "missing", "desc", PRIORITY_HIGH, {})],
    technical_debt=[TechnicalDebt("D1", "legacy", "comp", "desc", "high", "low", {}, "fix")],
    evaluation_score=0.5,
)
assert isinstance(updates, list)
for u in updates:
    assert u.owner_approval_required is True
    assert u.update_id.startswith("RU-")

# No updates when everything is fine
empty_updates = roadmap_engine.generate_updates([], [], 0.9)
assert isinstance(empty_updates, list)
print("14. RoadmapEvolutionEngine OK")

# ---------------------------------------------------------------------------
# 15. OptimizationPlan model
# ---------------------------------------------------------------------------

plan = OptimizationPlan(
    plan_id="IMP-001",
    generated_at="2026-01-01T00:00:00+00:00",
    repository="/tmp/repo",
    schema_version=IMPROVEMENT_VERSION,
    technical_debt_items=[debt],
    performance_metrics=[metric],
    capability_gaps=[gap],
    proposed_issues=debt_issues[:1],
    proposed_batches=batches[:1] if batches else [],
    summary="Test plan",
)
d = plan.to_dict()
assert d["plan_id"] == "IMP-001"
assert d["schema_version"] == IMPROVEMENT_VERSION
assert d["technical_debt_count"] == 1
assert d["performance_metric_count"] == 1
assert d["capability_gap_count"] == 1
assert d["proposed_issue_count"] == 1
assert isinstance(d["technical_debt"], list)
assert isinstance(d["performance_metrics"], list)
print("15. OptimizationPlan model OK")

# ---------------------------------------------------------------------------
# 16. ImprovementReportGenerator
# ---------------------------------------------------------------------------

report_gen = ImprovementReportGenerator()
markdown = report_gen.render(plan)
assert "# AI CTO Self Improvement Report" in markdown
assert "IMP-001" in markdown
assert "Technical Debt" in markdown
assert "Capability Gaps" in markdown
assert "Proposed Issues" in markdown

with tempfile.TemporaryDirectory() as tmpdir:
    out = Path(tmpdir) / "AI_CTO_SELF_IMPROVEMENT.md"
    report_gen.generate(plan, out)
    assert out.exists()
    assert "IMP-001" in out.read_text()
print("16. ImprovementReportGenerator OK")

# ---------------------------------------------------------------------------
# 17. ImprovementPersistence
# ---------------------------------------------------------------------------

with tempfile.TemporaryDirectory() as tmpdir:
    persistence = ImprovementPersistence(tmpdir)
    assert not persistence.exists()

    paths = persistence.save(plan, markdown=markdown)
    assert persistence.exists()

    expected_keys = (
        "improvements", "technical_debt", "performance",
        "optimization_plan", "proposed_issues", "proposed_batches",
        "proposed_cores", "roadmap_updates", "capability_analysis",
        "history", "snapshot",
    )
    for key in expected_keys:
        assert Path(paths[key]).exists(), f"{key} artifact missing"
    assert Path(paths["markdown"]).exists()

    loaded = persistence.load_improvements()
    assert loaded["plan_id"] == "IMP-001"
    assert loaded["schema_version"] == IMPROVEMENT_VERSION

    # Second save appends to history
    persistence.save(plan)
    loaded2 = persistence.load_improvements()
    assert isinstance(loaded2, dict)

print("17. ImprovementPersistence OK")

# ---------------------------------------------------------------------------
# 18. SelfImprovementEngine — integration test against AI Toolkit
# ---------------------------------------------------------------------------

engine = SelfImprovementEngine(
    repository=".",
    persist=True,
    refresh_integrations=False,
)
result = engine.improve()

assert "optimization_plan" in result
assert "plan_dict" in result
assert "markdown" in result
assert "paths" in result

d = result["plan_dict"]
assert d["schema_version"] == IMPROVEMENT_VERSION
assert d["plan_id"].startswith("IMP-")
assert isinstance(d["technical_debt"], list)
assert isinstance(d["performance_metrics"], list)
assert isinstance(d["capability_gaps"], list)
assert isinstance(d["proposed_issues"], list)
assert isinstance(d["proposed_batches"], list)
assert d["technical_debt_count"] >= 0
assert d["capability_gap_count"] >= 0

paths = result["paths"]
expected_keys = (
    "improvements", "technical_debt", "performance",
    "optimization_plan", "proposed_issues", "proposed_batches",
    "proposed_cores", "roadmap_updates", "capability_analysis",
    "history", "snapshot",
)
for key in expected_keys:
    assert Path(paths[key]).exists(), f"{key} artifact missing in integration test"
assert Path(paths["markdown"]).exists()

print("18. SelfImprovementEngine integration test OK")

# ---------------------------------------------------------------------------
# 19. Determinism
# ---------------------------------------------------------------------------

result2 = engine.improve()
d2 = result2["plan_dict"]
assert d2["schema_version"] == d["schema_version"]
assert d2["technical_debt_count"] == d["technical_debt_count"]
assert d2["capability_gap_count"] == d["capability_gap_count"]
print("19. Determinism OK")

# ---------------------------------------------------------------------------
# 20. EvolutionPlanner
# ---------------------------------------------------------------------------

evolver = EvolutionPlanner(".")

recs = evolver.plan_evolution({"overall_score": 0.4, "overall_gate": "FAILED",
                                "regression_findings": [{"severity": "high"}],
                                "architecture_findings": [{"severity": "high"}]})
assert isinstance(recs, list)
assert len(recs) > 0

good_recs = evolver.plan_evolution({"overall_score": 0.9, "overall_gate": "PASS",
                                     "regression_findings": [],
                                     "architecture_findings": []})
assert isinstance(good_recs, list)
print("20. EvolutionPlanner OK")

# ---------------------------------------------------------------------------
# 21. CLI smoke test — ai improve
# ---------------------------------------------------------------------------

import subprocess

proc = subprocess.run(
    ["bash", "bin/ai", "improve"],
    capture_output=True,
    text=True,
    cwd=".",
)
assert proc.returncode == 0, f"ai improve failed: {proc.stderr}"
assert "Plan ID" in proc.stdout

proc_json = subprocess.run(
    ["bash", "bin/ai", "improve", "--json"],
    capture_output=True,
    text=True,
    cwd=".",
)
assert proc_json.returncode == 0, f"ai improve --json failed: {proc_json.stderr}"
payload = json.loads(proc_json.stdout)
assert "plan_id" in payload
assert "schema_version" in payload
assert "technical_debt" in payload

for flag in ("--technical-debt", "--performance", "--roadmap"):
    p = subprocess.run(
        ["bash", "bin/ai", "improve", flag],
        capture_output=True,
        text=True,
        cwd=".",
    )
    assert p.returncode == 0, f"ai improve {flag} failed: {p.stderr}"

print("21. CLI smoke test OK")

print()
print("========================================")
print(" Self Improvement Engine PASS")
print("========================================")
PY

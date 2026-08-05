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

from python.self_evaluation_engine import (
    SelfEvaluationEngine,
    EvaluationCoordinator,
    CanonicalComplianceAnalyzer,
    ArchitectureComplianceAnalyzer,
    RepositoryComplianceAnalyzer,
    RegressionAnalyzer,
    CoverageAnalyzer,
    EvidenceAnalyzer,
    ImprovementAnalyzer,
    QualityScorer,
    ConfidenceScorer,
    EvaluationPersistence,
    EvaluationReportGenerator,
    EVALUATION_VERSION,
    GATE_PASS,
    GATE_WARNING,
    GATE_FAILED,
    GATE_BLOCKED,
    GATE_MANUAL_REVIEW,
    QUALITY_GATES,
    ALL_DIMENSIONS,
    DIMENSION_CANONICAL_COMPLIANCE,
    DIMENSION_OVERALL,
    DIMENSION_TESTING_QUALITY,
    DIMENSION_CONFIDENCE,
    EvaluationContext,
    QualityScore,
    RegressionFinding,
    ArchitectureFinding,
    EvaluationResult,
)

print("1. Imports OK")

# ---------------------------------------------------------------------------
# 2. Constants
# ---------------------------------------------------------------------------

assert EVALUATION_VERSION == "1.0.0"
assert GATE_PASS in QUALITY_GATES
assert GATE_FAILED in QUALITY_GATES
assert DIMENSION_OVERALL in ALL_DIMENSIONS
assert len(ALL_DIMENSIONS) == 11
print("2. Constants OK")

# ---------------------------------------------------------------------------
# 3. QualityScore model
# ---------------------------------------------------------------------------

score = QualityScore(
    dimension=DIMENSION_CANONICAL_COMPLIANCE,
    score=0.85,
    gate=GATE_PASS,
    evidence=["CORE-007: 0 deviations"],
    findings=[],
    recommendation="No action required.",
)
d = score.to_dict()
assert d["dimension"] == DIMENSION_CANONICAL_COMPLIANCE
assert d["score"] == 0.85
assert d["gate"] == GATE_PASS
assert isinstance(d["evidence"], list)
assert isinstance(d["findings"], list)
print("3. QualityScore model OK")

# ---------------------------------------------------------------------------
# 4. RegressionFinding model
# ---------------------------------------------------------------------------

finding = RegressionFinding(
    severity="high",
    component="planning",
    finding="Missing planning keys",
    impact="Incomplete planning output",
    affected_modules=["autonomous_planning_engine"],
    confidence=0.9,
    recommendation="Re-run ai plan",
    evidence={"missing": ["planning_id"]},
)
d = finding.to_dict()
assert d["severity"] == "high"
assert d["component"] == "planning"
assert d["confidence"] == 0.9
print("4. RegressionFinding model OK")

# ---------------------------------------------------------------------------
# 5. ArchitectureFinding model
# ---------------------------------------------------------------------------

arch = ArchitectureFinding(
    category="architecture_risk",
    component="some_module",
    description="Circular dependency detected",
    severity="high",
    evidence={"source": "CORE-008B"},
)
d = arch.to_dict()
assert d["category"] == "architecture_risk"
assert d["severity"] == "high"
print("5. ArchitectureFinding model OK")

# ---------------------------------------------------------------------------
# 6. QualityScorer
# ---------------------------------------------------------------------------

scorer = QualityScorer()

scores = [
    QualityScore("canonical_compliance", 0.9, GATE_PASS, [], [], ""),
    QualityScore("architecture_quality", 0.8, GATE_PASS, [], [], ""),
    QualityScore("repository_health", 0.7, GATE_WARNING, [], [], ""),
    QualityScore("execution_quality", 0.6, GATE_WARNING, [], [], ""),
    QualityScore("planning_quality", 0.85, GATE_PASS, [], [], ""),
    QualityScore("maintainability", 0.75, GATE_PASS, [], [], ""),
    QualityScore("documentation_quality", 0.5, GATE_WARNING, [], [], ""),
    QualityScore("testing_quality", 0.6, GATE_WARNING, [], [], ""),
    QualityScore("confidence", 0.8, GATE_PASS, [], [], ""),
    QualityScore("workspace_quality", 0.7, GATE_PASS, [], [], ""),
]
overall = scorer.score_overall(scores)
assert overall.dimension == DIMENSION_OVERALL
assert 0 <= overall.score <= 1.0
assert overall.gate in QUALITY_GATES

# Empty scores
empty_overall = scorer.score_overall([])
assert empty_overall.score == 0.0
assert empty_overall.gate == GATE_FAILED
print("6. QualityScorer OK")

# ---------------------------------------------------------------------------
# 7. ConfidenceScorer
# ---------------------------------------------------------------------------

conf_scorer = ConfidenceScorer()

# All available
full = conf_scorer.score(True, True, True, True, True)
assert full.score == 1.0
assert full.gate == GATE_PASS

# None available
empty = conf_scorer.score(False, False, False, False, False)
assert empty.score == 0.0
assert empty.gate == GATE_FAILED

# Partial
partial = conf_scorer.score(True, True, False, False, True)
assert partial.score == 0.6
assert partial.gate == GATE_WARNING
print("7. ConfidenceScorer OK")

# ---------------------------------------------------------------------------
# 8. RegressionAnalyzer
# ---------------------------------------------------------------------------

analyzer = RegressionAnalyzer(".")
reg_score, findings = analyzer.analyze(
    planning_data={"planning_id": "PLAN-001", "schema_version": "1.0.0", "execution_queue": {}},
    context_data={"repository": "AI-Toolkit", "current_branch": "main"},
    execution_data={},
)
# All required keys present — should PASS
assert reg_score.gate == GATE_PASS
assert len(findings) == 0

# Missing planning keys
reg_score2, findings2 = analyzer.analyze(
    planning_data={},
    context_data={},
    execution_data={},
)
assert reg_score2.gate != GATE_PASS
assert len(findings2) > 0
print("8. RegressionAnalyzer OK")

# ---------------------------------------------------------------------------
# 9. CoverageAnalyzer
# ---------------------------------------------------------------------------

cov_analyzer = CoverageAnalyzer(".")
cov_score = cov_analyzer.analyze()
assert cov_score.dimension == DIMENSION_TESTING_QUALITY
assert 0 <= cov_score.score <= 1.0
assert cov_score.gate in QUALITY_GATES
print("9. CoverageAnalyzer OK")

# ---------------------------------------------------------------------------
# 10. EvidenceAnalyzer
# ---------------------------------------------------------------------------

ev_analyzer = EvidenceAnalyzer()

good_evidence = ev_analyzer.analyze({"evidence": {"evidence_count": 15}})
assert good_evidence.score >= 0.7

no_evidence = ev_analyzer.analyze({})
assert no_evidence.score < 0.7
print("10. EvidenceAnalyzer OK")

# ---------------------------------------------------------------------------
# 11. ImprovementAnalyzer
# ---------------------------------------------------------------------------

imp_analyzer = ImprovementAnalyzer()
failed_scores = [QualityScore("canonical_compliance", 0.3, GATE_FAILED, [], [], "Fix this")]
recs = imp_analyzer.analyze(failed_scores, [], [])
assert len(recs) > 0
assert "critical" in recs[0].lower() or "canonical_compliance" in recs[0].lower()
print("11. ImprovementAnalyzer OK")

# ---------------------------------------------------------------------------
# 12. EvaluationResult model
# ---------------------------------------------------------------------------

eval_ctx = EvaluationContext(
    evaluation_id="EVAL-001",
    repository="/tmp/repo",
    workspace="/tmp",
    generated_at="2026-01-01T00:00:00+00:00",
    schema_version=EVALUATION_VERSION,
    planning_id="PLAN-001",
    execution_id="EXEC-001",
    briefing_id="BRF-001",
    synchronization_id="SYNC-001",
)
eval_result = EvaluationResult(
    evaluation_id="EVAL-001",
    generated_at="2026-01-01T00:00:00+00:00",
    repository="/tmp/repo",
    schema_version=EVALUATION_VERSION,
    context=eval_ctx,
    overall_gate=GATE_PASS,
    overall_score=0.85,
    overall_confidence=0.9,
    summary="Test evaluation",
)
d = eval_result.to_dict()
assert d["evaluation_id"] == "EVAL-001"
assert d["schema_version"] == EVALUATION_VERSION
assert d["overall_gate"] == GATE_PASS
assert d["overall_score"] == 0.85
assert isinstance(d["quality_scores"], list)
assert isinstance(d["regression_findings"], list)
assert isinstance(d["architecture_findings"], list)
print("12. EvaluationResult model OK")

# ---------------------------------------------------------------------------
# 13. EvaluationReportGenerator
# ---------------------------------------------------------------------------

gen = EvaluationReportGenerator()
markdown = gen.render(eval_result)
assert "# AI CTO Self Evaluation Report" in markdown
assert "EVAL-001" in markdown
assert "Quality Scores" in markdown
assert "Regressions" in markdown
assert "Recommendations" in markdown

with tempfile.TemporaryDirectory() as tmpdir:
    out = Path(tmpdir) / "AI_CTO_SELF_EVALUATION.md"
    gen.generate(eval_result, out)
    assert out.exists()
    assert "EVAL-001" in out.read_text()
print("13. EvaluationReportGenerator OK")

# ---------------------------------------------------------------------------
# 14. EvaluationPersistence
# ---------------------------------------------------------------------------

with tempfile.TemporaryDirectory() as tmpdir:
    persistence = EvaluationPersistence(tmpdir)
    assert not persistence.exists()

    paths = persistence.save(eval_result, markdown=markdown)
    assert persistence.exists()

    for key in ("evaluation", "quality", "confidence", "compliance", "architecture",
                "coverage", "regressions", "evidence", "history", "snapshot"):
        assert Path(paths[key]).exists(), f"{key} artifact missing"

    assert Path(paths["markdown"]).exists()

    loaded = persistence.load_evaluation()
    assert loaded["evaluation_id"] == "EVAL-001"
    assert loaded["schema_version"] == EVALUATION_VERSION

    history = persistence.load_evaluation()
    assert isinstance(history, dict)

print("14. EvaluationPersistence OK")

# ---------------------------------------------------------------------------
# 15. SelfEvaluationEngine — integration test against AI Toolkit
# ---------------------------------------------------------------------------

engine = SelfEvaluationEngine(
    repository=".",
    persist=True,
    refresh_integrations=False,
)
result = engine.evaluate()

assert "evaluation_result" in result
assert "evaluation_dict" in result
assert "markdown" in result
assert "paths" in result

d = result["evaluation_dict"]
assert d["schema_version"] == EVALUATION_VERSION
assert d["evaluation_id"].startswith("ATK-EVAL-")
assert 0 <= d["overall_score"] <= 1.0
assert d["overall_gate"] in QUALITY_GATES
assert isinstance(d["quality_scores"], list)
assert len(d["quality_scores"]) >= 7
assert isinstance(d["regression_findings"], list)
assert isinstance(d["architecture_findings"], list)
assert isinstance(d["recommendations"], list)

paths = result["paths"]
for key in ("evaluation", "quality", "confidence", "compliance",
            "architecture", "coverage", "regressions", "evidence",
            "history", "snapshot"):
    assert Path(paths[key]).exists(), f"{key} artifact missing in integration test"
assert Path(paths["markdown"]).exists()
print("15. SelfEvaluationEngine integration test OK")

# ---------------------------------------------------------------------------
# 16. Determinism
# ---------------------------------------------------------------------------

result2 = engine.evaluate()
d2 = result2["evaluation_dict"]
assert d2["schema_version"] == d["schema_version"]
# Overall score should be stable across identical runs
assert abs(d2["overall_score"] - d["overall_score"]) < 0.01
assert d2["overall_gate"] == d["overall_gate"]
print("16. Determinism OK")

# ---------------------------------------------------------------------------
# 17. CLI smoke test — ai evaluate
# ---------------------------------------------------------------------------

import subprocess

proc = subprocess.run(
    ["python3", "-m", "lib.python.cli.main", "evaluate"],
    capture_output=True,
    text=True,
    cwd=".",
)
assert proc.returncode == 0, f"ai evaluate exited {proc.returncode}: {proc.stderr}"
assert "Evaluation ID" in proc.stdout

proc_json = subprocess.run(
    ["python3", "-m", "lib.python.cli.main", "evaluate", "--json"],
    capture_output=True,
    text=True,
    cwd=".",
)
assert proc_json.returncode == 0, f"ai evaluate --json failed: {proc_json.stderr}"
payload = json.loads(proc_json.stdout)
assert "evaluation_id" in payload
assert "schema_version" in payload
assert "overall_score" in payload

# Quality flag
proc_quality = subprocess.run(
    ["python3", "-m", "lib.python.cli.main", "evaluate", "--quality"],
    capture_output=True,
    text=True,
    cwd=".",
)
assert proc_quality.returncode == 0

# Regressions flag
proc_reg = subprocess.run(
    ["python3", "-m", "lib.python.cli.main", "evaluate", "--regressions"],
    capture_output=True,
    text=True,
    cwd=".",
)
assert proc_reg.returncode == 0
print("17. CLI smoke test OK")

print()
print("========================================")
print(" Self Evaluation Engine PASS")
print("========================================")
PY

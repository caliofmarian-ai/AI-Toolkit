#!/data/data/com.termux/files/usr/bin/bash
set -e

python3 - <<'PY'
import json
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any, Dict, List, Mapping

sys.path.insert(0, "lib")

from python.executive_briefing_engine import (
    ExecutiveBriefingEngine,
    ExecutiveBriefingGenerator,
    ExecutiveRecommendationEngine,
    ExecutivePriorityEngine,
    ExecutiveRiskAnalyzer,
    ExecutiveDecisionTracker,
    ExecutiveInsightGenerator,
    ExecutiveBriefingPersistence,
    ExecutiveBriefing,
    ExecutiveRecommendation,
    ExecutiveRisk,
    ExecutivePriorityItem,
    ExecutiveDecision,
    OwnerDashboard,
    BRIEFING_VERSION,
)
from python.executive_briefing_engine.models import (
    PRIORITY_CRITICAL,
    PRIORITY_HIGH,
    PRIORITY_MEDIUM,
    PRIORITY_LOW,
    PRIORITY_BLOCKED,
    PRIORITY_COMPLETED,
    PRIORITY_WAITING,
    SEVERITY_CRITICAL,
    SEVERITY_HIGH,
    SEVERITY_MEDIUM,
    SEVERITY_LOW,
    RISK_ARCHITECTURE,
    RISK_CANONICAL_DRIFT,
    RISK_MISSING_COMPONENTS,
)


# ---------------------------------------------------------------------------
# Test fixtures
# ---------------------------------------------------------------------------

def _make_snapshot(overrides: Dict[str, Any] = None) -> Dict[str, Any]:
    """Return a minimal but realistic development state snapshot."""
    base = {
        "generated_at": "2026-01-01T00:00:00Z",
        "schema_version": "1.0.0",
        "current_context": {
            "current_branch": "feature/core-010",
            "current_issue": "CORE-010",
            "current_pull_request": "PR-42",
            "current_batch": "BATCH-007",
            "current_milestone": "MILESTONE-03",
            "current_epic": "EPIC-AI-CTO",
            "current_recommendation": "BATCH-007",
        },
        "state": {
            "identifier": "STATE-001",
            "schema_version": "1.0.0",
            "workspace_state": {
                "active_workspace": "AI-Toolkit",
                "current_task": "CORE-010",
                "blocked_tasks": ["TASK-X", "TASK-Y"],
                "completed_tasks": ["CORE-001", "CORE-002"],
                "current_batch": "BATCH-007",
                "current_milestone": "MILESTONE-03",
            },
            "repository_state": {
                "repository": "/repo",
                "branch": "feature/core-010",
                "open_pull_requests": ["PR-42", "PR-41", "PR-40", "PR-39"],
                "tags": [],
            },
            "execution_state": {
                "current_executor": "ai-cto",
                "running_jobs": [],
                "completed_jobs": ["JOB-001"],
                "failed_jobs": [],
                "execution_history": [],
            },
            "planning_state": {
                "current_roadmap": "EPIC-AI-CTO",
                "recommended_batch": "BATCH-007",
            },
            "review_state": {
                "open_prs": ["PR-42", "PR-41", "PR-40", "PR-39"],
                "pending_reviews": [],
            },
            "owner_state": {},
            "telegram_state": {},
            "snapshot_metadata": {"sequence_number": 5, "identifier": "SNAP-000005"},
            "integrity_report": {"failed_checks": []},
        },
        "integrity": {
            "state_sha256": "abc123",
            "snapshot_history": [],
        },
        "integrations": {
            "repository_intelligence": {
                "repository_root": "/repo",
                "statistics": {"files": 150, "directories": 30, "repository_name": "AI-Toolkit"},
            },
            "canonical_intelligence": {
                "available": True,
                "canonical_documents": 10,
                "overall_coverage": 85.0,
                "overall_compliance": 90.0,
                "drift_findings": 2,
                "batches": 3,
            },
            "semantic_repository_intelligence": {
                "schema_version": "1.0.0",
                "captured_at": "2026-01-01T00:00:00Z",
                "analysis": {
                    "import_graph": {"node_count": 50, "edge_count": 120},
                    "architecture_graph": {
                        "node_count": 30,
                        "edge_count": 60,
                        "hotspots": ["lib/python/engine.py", "lib/python/models.py"],
                        "extension_points": ["lib/python/base.py"],
                        "risks": [],
                    },
                    "complexity": {"total_files": 150},
                    "recommendation_count": 2,
                    "top_recommendation": {
                        "id": "SR-001",
                        "title": "Decompose large modules",
                        "priority": "medium",
                    },
                    "next_core": "CORE-011",
                },
            },
            "ai_cto_scanner": {
                "report_exists": True,
                "scores": {"overall": 92},
                "workspace": {"total_files": 150, "total_directories": 30},
                "detection": {},
            },
            "executable_repository_intelligence": {
                "provider": "runtime_execution_state",
                "running_jobs": 0,
                "completed_jobs": 5,
                "failed_jobs": 0,
            },
        },
        "recent_events": [],
    }
    if overrides:
        _deep_merge(base, overrides)
    return base


def _make_degraded_snapshot() -> Dict[str, Any]:
    """Snapshot with critical issues for negative-path testing."""
    return _make_snapshot({
        "integrations": {
            "canonical_intelligence": {
                "overall_coverage": 40.0,
                "overall_compliance": 60.0,
                "drift_findings": 8,
                "batches": 12,
            },
            "semantic_repository_intelligence": {
                "analysis": {
                    "architecture_graph": {
                        "node_count": 30,
                        "edge_count": 60,
                        "hotspots": [f"module_{i}.py" for i in range(10)],
                        "extension_points": [],
                        "risks": ["Circular dependency in core", "Orphan module detected"],
                    },
                    "complexity": {"total_files": 350},
                },
            },
            "executable_repository_intelligence": {
                "failed_jobs": 3,
            },
        },
        "state": {
            "workspace_state": {
                "blocked_tasks": ["TASK-A", "TASK-B", "TASK-C", "TASK-D"],
            },
            "integrity_report": {
                "failed_checks": ["hash_mismatch", "schema_invalid"],
            },
        },
    })


def _deep_merge(base: dict, overrides: dict):
    for key, value in overrides.items():
        if key in base and isinstance(base[key], dict) and isinstance(value, dict):
            _deep_merge(base[key], value)
        else:
            base[key] = value


class FakeDevelopmentStateEngine:
    """Stub that returns a controlled snapshot for unit testing."""

    def __init__(self, snapshot_override=None, repository_root="."):
        self.repository_root = repository_root
        self._snapshot = snapshot_override or _make_snapshot()
        self.manager = _FakeManager(self._snapshot)

    def LoadCurrentState(self, create_if_missing=False):
        return _FakeState()


class _FakeState:
    identifier = "STATE-001"


class _FakeManager:
    def __init__(self, snapshot):
        self._snapshot = snapshot

    def GenerateExecutiveSnapshot(self, state, refresh_integrations=False):
        return _FakeSnapshot(self._snapshot)


class _FakeSnapshot:
    def __init__(self, data):
        self._data = data

    def to_dict(self):
        return self._data


# ---------------------------------------------------------------------------
# Model tests
# ---------------------------------------------------------------------------

class ModelTests(unittest.TestCase):

    def test_executive_recommendation_roundtrip(self):
        rec = ExecutiveRecommendation(
            id="REC-001",
            title="Fix canonical drift",
            description="Resolve 3 drift findings.",
            priority=PRIORITY_HIGH,
            impact="Restores specification alignment.",
            confidence=0.95,
            required_effort="medium",
            dependencies=("DEP-A",),
            affected_components=("engine.py",),
            reasoning="Evidence shows drift.",
            evidence=("drift_findings=3",),
        )
        d = rec.to_dict()
        self.assertEqual(d["id"], "REC-001")
        self.assertEqual(d["priority"], PRIORITY_HIGH)
        self.assertEqual(d["confidence"], 0.95)
        self.assertIsInstance(d["dependencies"], list)
        self.assertIsInstance(d["affected_components"], list)

        restored = ExecutiveRecommendation.from_dict(d)
        self.assertEqual(restored.id, rec.id)
        self.assertEqual(restored.priority, rec.priority)
        self.assertEqual(restored.confidence, rec.confidence)

    def test_executive_risk_roundtrip(self):
        risk = ExecutiveRisk(
            id="RISK-001",
            category=RISK_CANONICAL_DRIFT,
            severity=SEVERITY_HIGH,
            title="Canonical drift detected",
            description="8 drift findings.",
            evidence=("drift=8",),
            affected_components=(),
            remediation="Resolve drift.",
        )
        d = risk.to_dict()
        self.assertEqual(d["category"], RISK_CANONICAL_DRIFT)
        restored = ExecutiveRisk.from_dict(d)
        self.assertEqual(restored.severity, SEVERITY_HIGH)

    def test_executive_priority_item_roundtrip(self):
        item = ExecutivePriorityItem(
            id="PRI-001",
            title="Fix blocked task",
            classification=PRIORITY_BLOCKED,
            category="task",
            rationale="Task is blocked.",
        )
        d = item.to_dict()
        self.assertEqual(d["classification"], PRIORITY_BLOCKED)
        restored = ExecutivePriorityItem.from_dict(d)
        self.assertEqual(restored.id, "PRI-001")

    def test_executive_decision_roundtrip(self):
        dec = ExecutiveDecision(
            id="DEC-001",
            title="Merge PR queue",
            description="Decide merge order.",
            options=("FIFO", "Critical first"),
            recommended_option="Critical first",
            impact="Reduces integration debt.",
            urgency=PRIORITY_MEDIUM,
            context="4 PRs open.",
        )
        d = dec.to_dict()
        self.assertIsInstance(d["options"], list)
        restored = ExecutiveDecision.from_dict(d)
        self.assertEqual(restored.recommended_option, "Critical first")

    def test_owner_dashboard_roundtrip(self):
        dash = OwnerDashboard(
            overall_health="warning",
            repository_readiness="development-ready",
            current_progress="3/10 items completed (30%)",
            open_risks=5,
            recommended_actions=("Fix drift", "Review PRs"),
            blocked_items=("TASK-X",),
        )
        d = dash.to_dict()
        self.assertEqual(d["overall_health"], "warning")
        self.assertIsInstance(d["recommended_actions"], list)
        restored = OwnerDashboard.from_dict(d)
        self.assertEqual(restored.open_risks, 5)

    def test_executive_briefing_roundtrip(self):
        dash = OwnerDashboard(
            overall_health="healthy",
            repository_readiness="production-ready",
            current_progress="all complete",
            open_risks=0,
            recommended_actions=(),
            blocked_items=(),
        )
        briefing = ExecutiveBriefing(
            briefing_id="BRIEF-ABC",
            generated_at="2026-01-01T00:00:00Z",
            schema_version=BRIEFING_VERSION,
            repository="/repo",
            executive_summary="All healthy.",
            current_branch="main",
            current_issue="",
            current_pull_request="",
            current_batch="",
            current_milestone="",
            current_epic="",
            current_recommendation="",
            architecture_health="healthy",
            canonical_health="healthy",
            development_health="healthy",
            repository_health="healthy",
            runtime_health="healthy",
            recommendations=(),
            critical_risks=(),
            all_risks=(),
            pending_decisions=(),
            priorities=(),
            suggested_next_core="CORE-011",
            suggested_next_batch="",
            suggested_next_pr="",
            estimated_completion="within current milestone",
            owner_dashboard=dash,
        )
        d = briefing.to_dict()
        self.assertEqual(d["briefing_id"], "BRIEF-ABC")
        self.assertIsInstance(d["recommendations"], list)
        self.assertIsInstance(d["all_risks"], list)
        self.assertIsInstance(d["priorities"], list)
        self.assertIsInstance(d["pending_decisions"], list)

        restored = ExecutiveBriefing.from_dict(d)
        self.assertEqual(restored.briefing_id, "BRIEF-ABC")
        self.assertEqual(restored.schema_version, BRIEFING_VERSION)


# ---------------------------------------------------------------------------
# Risk Analyzer tests
# ---------------------------------------------------------------------------

class RiskAnalyzerTests(unittest.TestCase):

    def test_healthy_snapshot_produces_minimal_risks(self):
        analyzer = ExecutiveRiskAnalyzer()
        risks = analyzer.analyze(_make_snapshot())
        # Healthy snapshot: some minor risks may be generated, but no critical ones
        critical = [r for r in risks if r.severity == SEVERITY_CRITICAL]
        self.assertEqual(critical, [], f"Unexpected critical risks: {critical}")

    def test_degraded_snapshot_produces_critical_risks(self):
        analyzer = ExecutiveRiskAnalyzer()
        risks = analyzer.analyze(_make_degraded_snapshot())
        critical_or_high = [r for r in risks if r.severity in (SEVERITY_CRITICAL, SEVERITY_HIGH)]
        self.assertTrue(
            len(critical_or_high) >= 2,
            f"Expected ≥2 critical/high risks, got: {[(r.severity, r.title) for r in critical_or_high]}"
        )

    def test_canonical_drift_risk_detected(self):
        analyzer = ExecutiveRiskAnalyzer()
        snapshot = _make_snapshot({"integrations": {"canonical_intelligence": {"drift_findings": 8, "overall_coverage": 85.0}}})
        risks = analyzer.analyze(snapshot)
        drift_risks = [r for r in risks if r.category == RISK_CANONICAL_DRIFT]
        self.assertTrue(len(drift_risks) >= 1, "Expected canonical drift risk")
        self.assertEqual(drift_risks[0].severity, SEVERITY_CRITICAL)

    def test_low_coverage_risk_detected(self):
        analyzer = ExecutiveRiskAnalyzer()
        snapshot = _make_snapshot({"integrations": {"canonical_intelligence": {"overall_coverage": 35.0, "drift_findings": 0}}})
        risks = analyzer.analyze(snapshot)
        drift_risks = [r for r in risks if r.category == RISK_CANONICAL_DRIFT]
        self.assertTrue(len(drift_risks) >= 1, "Expected low coverage risk")

    def test_architecture_risk_from_hotspots(self):
        analyzer = ExecutiveRiskAnalyzer()
        snapshot = _make_snapshot({
            "integrations": {
                "semantic_repository_intelligence": {
                    "analysis": {
                        "architecture_graph": {
                            "node_count": 40,
                            "hotspots": [f"h{i}.py" for i in range(6)],
                            "risks": [],
                        }
                    }
                }
            }
        })
        risks = analyzer.analyze(snapshot)
        arch_risks = [r for r in risks if r.category == RISK_ARCHITECTURE]
        self.assertTrue(len(arch_risks) >= 1, "Expected architecture hotspot risk")

    def test_risks_are_sorted_by_severity(self):
        analyzer = ExecutiveRiskAnalyzer()
        risks = analyzer.analyze(_make_degraded_snapshot())
        severities = [r.severity for r in risks]
        order = [ExecutiveRiskAnalyzer._SEVERITY_ORDER.get(s, 9) for s in severities]
        self.assertEqual(order, sorted(order), "Risks should be sorted by severity")

    def test_risk_ids_are_unique(self):
        analyzer = ExecutiveRiskAnalyzer()
        risks = analyzer.analyze(_make_degraded_snapshot())
        ids = [r.id for r in risks]
        self.assertEqual(len(ids), len(set(ids)), "Risk IDs must be unique")


# ---------------------------------------------------------------------------
# Recommendation Engine tests
# ---------------------------------------------------------------------------

class RecommendationEngineTests(unittest.TestCase):

    def test_healthy_snapshot_produces_recommendations(self):
        engine = ExecutiveRecommendationEngine()
        risks = ExecutiveRiskAnalyzer().analyze(_make_snapshot())
        recs = engine.generate(_make_snapshot(), risks)
        self.assertIsInstance(recs, list)
        self.assertTrue(len(recs) >= 1)

    def test_degraded_snapshot_has_high_priority_recommendations(self):
        snapshot = _make_degraded_snapshot()
        risks = ExecutiveRiskAnalyzer().analyze(snapshot)
        recs = ExecutiveRecommendationEngine().generate(snapshot, risks)
        high_or_critical = [r for r in recs if r.priority in (PRIORITY_CRITICAL, PRIORITY_HIGH)]
        self.assertTrue(
            len(high_or_critical) >= 2,
            f"Expected ≥2 high/critical recommendations, got {len(high_or_critical)}"
        )

    def test_all_recommendations_have_evidence(self):
        snapshot = _make_snapshot()
        risks = ExecutiveRiskAnalyzer().analyze(snapshot)
        recs = ExecutiveRecommendationEngine().generate(snapshot, risks)
        for rec in recs:
            self.assertTrue(len(rec.evidence) >= 1, f"{rec.id} has no evidence")

    def test_all_recommendations_have_reasoning(self):
        snapshot = _make_snapshot()
        risks = ExecutiveRiskAnalyzer().analyze(snapshot)
        recs = ExecutiveRecommendationEngine().generate(snapshot, risks)
        for rec in recs:
            self.assertTrue(rec.reasoning.strip(), f"{rec.id} has empty reasoning")

    def test_recommendations_sorted_by_priority(self):
        snapshot = _make_degraded_snapshot()
        risks = ExecutiveRiskAnalyzer().analyze(snapshot)
        recs = ExecutiveRecommendationEngine().generate(snapshot, risks)
        from python.executive_briefing_engine.recommendation_engine import _PRIORITY_ORDER
        orders = [_PRIORITY_ORDER.get(r.priority, 9) for r in recs]
        self.assertEqual(orders, sorted(orders), "Recommendations must be sorted by priority")

    def test_recommendation_ids_are_unique(self):
        snapshot = _make_snapshot()
        risks = ExecutiveRiskAnalyzer().analyze(snapshot)
        recs = ExecutiveRecommendationEngine().generate(snapshot, risks)
        ids = [r.id for r in recs]
        self.assertEqual(len(ids), len(set(ids)))

    def test_canonical_drift_triggers_recommendation(self):
        snapshot = _make_snapshot({"integrations": {"canonical_intelligence": {"drift_findings": 3}}})
        risks = ExecutiveRiskAnalyzer().analyze(snapshot)
        recs = ExecutiveRecommendationEngine().generate(snapshot, risks)
        drift_recs = [r for r in recs if "drift" in r.title.lower()]
        self.assertTrue(len(drift_recs) >= 1, "Expected canonical drift recommendation")


# ---------------------------------------------------------------------------
# Priority Engine tests
# ---------------------------------------------------------------------------

class PriorityEngineTests(unittest.TestCase):

    def test_blocked_tasks_classified(self):
        engine = ExecutivePriorityEngine()
        items = engine.classify(_make_snapshot())
        blocked = [i for i in items if i.classification == PRIORITY_BLOCKED]
        self.assertEqual(len(blocked), 2, "Expected 2 blocked items (TASK-X, TASK-Y)")

    def test_critical_coverage_classified(self):
        snapshot = _make_snapshot({"integrations": {"canonical_intelligence": {"overall_coverage": 40.0, "drift_findings": 8}}})
        items = ExecutivePriorityEngine().classify(snapshot)
        critical = [i for i in items if i.classification == PRIORITY_CRITICAL]
        self.assertTrue(len(critical) >= 1, "Expected critical classification for low coverage")

    def test_completed_tasks_classified(self):
        items = ExecutivePriorityEngine().classify(_make_snapshot())
        completed = [i for i in items if i.classification == PRIORITY_COMPLETED]
        self.assertTrue(len(completed) >= 2, "Expected completed items from completed_tasks")

    def test_items_sorted_by_classification(self):
        items = ExecutivePriorityEngine().classify(_make_snapshot())
        from python.executive_briefing_engine.priority_engine import ExecutivePriorityEngine as PE
        order_map = PE._CLASSIFICATION_ORDER
        orders = [order_map.get(i.classification, 9) for i in items]
        self.assertEqual(orders, sorted(orders))

    def test_priority_ids_are_unique(self):
        items = ExecutivePriorityEngine().classify(_make_snapshot())
        ids = [i.id for i in items]
        self.assertEqual(len(ids), len(set(ids)))


# ---------------------------------------------------------------------------
# Decision Tracker tests
# ---------------------------------------------------------------------------

class DecisionTrackerTests(unittest.TestCase):

    def test_blocked_tasks_produce_decision(self):
        decisions = ExecutiveDecisionTracker().extract(_make_snapshot())
        blocked_decs = [d for d in decisions if "blocked" in d.title.lower()]
        self.assertTrue(len(blocked_decs) >= 1, "Expected blocked task decision")

    def test_all_decisions_have_options(self):
        decisions = ExecutiveDecisionTracker().extract(_make_degraded_snapshot())
        for dec in decisions:
            self.assertTrue(len(dec.options) >= 2, f"{dec.id} needs ≥2 options")

    def test_all_decisions_have_recommended_option(self):
        decisions = ExecutiveDecisionTracker().extract(_make_snapshot())
        for dec in decisions:
            self.assertTrue(dec.recommended_option.strip(), f"{dec.id} missing recommended_option")

    def test_canonical_quality_gate_decision_for_degraded(self):
        decisions = ExecutiveDecisionTracker().extract(_make_degraded_snapshot())
        gate_decs = [d for d in decisions if "quality gate" in d.title.lower() or "canonical" in d.title.lower()]
        self.assertTrue(len(gate_decs) >= 1, "Expected canonical quality gate decision")

    def test_decision_ids_are_unique(self):
        decisions = ExecutiveDecisionTracker().extract(_make_snapshot())
        ids = [d.id for d in decisions]
        self.assertEqual(len(ids), len(set(ids)))


# ---------------------------------------------------------------------------
# Insight Generator tests
# ---------------------------------------------------------------------------

class InsightGeneratorTests(unittest.TestCase):

    def test_architecture_health_healthy(self):
        gen = ExecutiveInsightGenerator()
        result = gen.architecture_health(_make_snapshot())
        self.assertIn(result, ("healthy", "warning", "degraded", "unknown"))

    def test_canonical_health_degraded(self):
        gen = ExecutiveInsightGenerator()
        snapshot = _make_snapshot({"integrations": {"canonical_intelligence": {"overall_coverage": 30.0, "drift_findings": 12}}})
        self.assertEqual(gen.canonical_health(snapshot), "critical")

    def test_development_health_with_failed_jobs(self):
        gen = ExecutiveInsightGenerator()
        snapshot = _make_snapshot({"state": {"execution_state": {"failed_jobs": ["JOB-1"]}}})
        self.assertEqual(gen.development_health(snapshot), "degraded")

    def test_repository_health_with_integrity_failure(self):
        gen = ExecutiveInsightGenerator()
        snapshot = _make_snapshot({"state": {"integrity_report": {"failed_checks": ["mismatch"]}}})
        self.assertEqual(gen.repository_health(snapshot), "degraded")

    def test_executive_summary_generated(self):
        gen = ExecutiveInsightGenerator()
        summary = gen.executive_summary(
            _make_snapshot(), "healthy", "healthy", "healthy", "healthy", "healthy", 0, 1
        )
        self.assertTrue(summary.strip())
        self.assertTrue(len(summary) > 20)

    def test_suggested_next_core_from_semantic(self):
        gen = ExecutiveInsightGenerator()
        result = gen.suggested_next_core(_make_snapshot())
        self.assertEqual(result, "CORE-011")

    def test_estimated_completion_derived(self):
        gen = ExecutiveInsightGenerator()
        result = gen.estimated_completion(_make_snapshot())
        self.assertTrue(result.strip())


# ---------------------------------------------------------------------------
# Generator tests
# ---------------------------------------------------------------------------

class GeneratorTests(unittest.TestCase):

    def _make_briefing(self) -> ExecutiveBriefing:
        dash = OwnerDashboard(
            overall_health="healthy",
            repository_readiness="production-ready",
            current_progress="5/10 complete",
            open_risks=2,
            recommended_actions=("Fix drift",),
            blocked_items=(),
        )
        return ExecutiveBriefing(
            briefing_id="BRIEF-TEST",
            generated_at="2026-01-01T00:00:00Z",
            schema_version=BRIEFING_VERSION,
            repository="/repo",
            executive_summary="Repository is healthy.",
            current_branch="main",
            current_issue="CORE-010",
            current_pull_request="PR-42",
            current_batch="BATCH-007",
            current_milestone="M3",
            current_epic="EPIC-AI",
            current_recommendation="BATCH-007",
            architecture_health="healthy",
            canonical_health="healthy",
            development_health="healthy",
            repository_health="healthy",
            runtime_health="healthy",
            recommendations=(
                ExecutiveRecommendation(
                    id="REC-001", title="Fix drift", description="3 drift findings.",
                    priority=PRIORITY_HIGH, impact="High", confidence=0.9,
                    required_effort="medium", dependencies=(), affected_components=(),
                    reasoning="Drift detected.", evidence=("drift=3",),
                ),
            ),
            critical_risks=(),
            all_risks=(
                ExecutiveRisk(
                    id="RISK-001", category=RISK_CANONICAL_DRIFT, severity=SEVERITY_MEDIUM,
                    title="Minor drift", description="2 drift findings.",
                    evidence=("drift=2",), affected_components=(), remediation="Resolve drift.",
                ),
            ),
            pending_decisions=(
                ExecutiveDecision(
                    id="DEC-001", title="Merge queue", description="Decide order.",
                    options=("FIFO", "Priority"), recommended_option="Priority",
                    impact="Reduces debt.", urgency=PRIORITY_MEDIUM, context="4 PRs.",
                ),
            ),
            priorities=(
                ExecutivePriorityItem(
                    id="PRI-001", title="Batch execution", classification=PRIORITY_HIGH,
                    category="batch_execution", rationale="Active batch.",
                ),
            ),
            suggested_next_core="CORE-011",
            suggested_next_batch="BATCH-008",
            suggested_next_pr="PR-43",
            estimated_completion="within current milestone",
            owner_dashboard=dash,
        )

    def test_render_produces_markdown(self):
        gen = ExecutiveBriefingGenerator()
        md = gen.render(self._make_briefing())
        self.assertIn("# AI CTO Executive Briefing", md)
        self.assertIn("BRIEF-TEST", md)
        self.assertIn("Owner Dashboard", md)
        self.assertIn("Executive Summary", md)
        self.assertIn("Current Workspace Status", md)
        self.assertIn("Health Overview", md)
        self.assertIn("Recommendations", md)
        self.assertIn("Risks", md)
        self.assertIn("Priorities", md)
        self.assertIn("Pending Decisions", md)
        self.assertIn("Suggested Next Steps", md)
        self.assertIn("CORE-011", md)

    def test_generate_writes_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "AI_CTO_EXECUTIVE_BRIEFING.md"
            gen = ExecutiveBriefingGenerator()
            content = gen.generate(self._make_briefing(), path)
            self.assertTrue(path.exists())
            self.assertEqual(path.read_text(encoding="utf-8"), content)
            self.assertIn("# AI CTO Executive Briefing", content)

    def test_render_is_deterministic(self):
        gen = ExecutiveBriefingGenerator()
        briefing = self._make_briefing()
        md1 = gen.render(briefing)
        md2 = gen.render(briefing)
        self.assertEqual(md1, md2)


# ---------------------------------------------------------------------------
# Persistence tests
# ---------------------------------------------------------------------------

class PersistenceTests(unittest.TestCase):

    def _make_briefing(self) -> ExecutiveBriefing:
        dash = OwnerDashboard(
            overall_health="healthy", repository_readiness="production-ready",
            current_progress="all good", open_risks=0, recommended_actions=(), blocked_items=(),
        )
        return ExecutiveBriefing(
            briefing_id="BRIEF-PERSIST", generated_at="2026-01-01T00:00:00Z",
            schema_version=BRIEFING_VERSION, repository="/repo",
            executive_summary="Healthy.", current_branch="main",
            current_issue="", current_pull_request="", current_batch="",
            current_milestone="", current_epic="", current_recommendation="",
            architecture_health="healthy", canonical_health="healthy",
            development_health="healthy", repository_health="healthy", runtime_health="healthy",
            recommendations=(), critical_risks=(), all_risks=(),
            pending_decisions=(), priorities=(), suggested_next_core="",
            suggested_next_batch="", suggested_next_pr="", estimated_completion="",
            owner_dashboard=dash,
        )

    def test_save_creates_all_artifacts(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            persistence = ExecutiveBriefingPersistence(tmpdir)
            paths = persistence.save(self._make_briefing())
            expected_keys = {"briefing", "recommendations", "priorities", "risks", "owner_actions"}
            self.assertEqual(set(paths.keys()), expected_keys)
            for key, path in paths.items():
                self.assertTrue(Path(path).exists(), f"{key} not persisted at {path}")

    def test_saved_json_is_valid(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            persistence = ExecutiveBriefingPersistence(tmpdir)
            paths = persistence.save(self._make_briefing())
            for key, path in paths.items():
                with open(path, encoding="utf-8") as f:
                    data = json.load(f)
                self.assertIsInstance(data, dict, f"{key} not a JSON object")

    def test_load_briefing(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            persistence = ExecutiveBriefingPersistence(tmpdir)
            briefing = self._make_briefing()
            persistence.save(briefing)
            loaded = persistence.load_briefing()
            self.assertEqual(loaded["briefing_id"], "BRIEF-PERSIST")

    def test_exists_false_before_save(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            persistence = ExecutiveBriefingPersistence(tmpdir)
            self.assertFalse(persistence.exists())

    def test_exists_true_after_save(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            persistence = ExecutiveBriefingPersistence(tmpdir)
            persistence.save(self._make_briefing())
            self.assertTrue(persistence.exists())

    def test_save_is_deterministic(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            persistence = ExecutiveBriefingPersistence(tmpdir)
            briefing = self._make_briefing()
            persistence.save(briefing)
            content1 = (Path(tmpdir) / ".ai" / "executive" / "briefing.json").read_text()
            persistence.save(briefing)
            content2 = (Path(tmpdir) / ".ai" / "executive" / "briefing.json").read_text()
            self.assertEqual(content1, content2)


# ---------------------------------------------------------------------------
# Engine integration tests (with fake state engine)
# ---------------------------------------------------------------------------

class EngineIntegrationTests(unittest.TestCase):

    def _make_engine(self, snapshot=None) -> ExecutiveBriefingEngine:
        snap = snapshot or _make_snapshot()

        class _FakeEngine(FakeDevelopmentStateEngine):
            def __init__(self_inner, repository_root="."):
                super().__init__(snap, repository_root)

        with tempfile.TemporaryDirectory() as tmpdir:
            engine = ExecutiveBriefingEngine(
                repository=tmpdir,
                output_dir=tmpdir,
                persist=False,
                state_engine_class=_FakeEngine,
            )
            return engine, tmpdir, _FakeEngine

    def test_generate_returns_briefing(self):
        snap = _make_snapshot()

        class _FakeEngine(FakeDevelopmentStateEngine):
            def __init__(self_inner, repository_root="."):
                super().__init__(snap, repository_root)

        with tempfile.TemporaryDirectory() as tmpdir:
            engine = ExecutiveBriefingEngine(
                repository=tmpdir,
                output_dir=tmpdir,
                persist=False,
                state_engine_class=_FakeEngine,
            )
            result = engine.generate()

        self.assertIn("briefing", result)
        self.assertIn("markdown", result)
        briefing = result["briefing"]
        self.assertIsInstance(briefing, ExecutiveBriefing)
        self.assertTrue(briefing.briefing_id.startswith("BRIEF-"))

    def test_generate_produces_markdown(self):
        snap = _make_snapshot()

        class _FakeEngine(FakeDevelopmentStateEngine):
            def __init__(self_inner, repository_root="."):
                super().__init__(snap, repository_root)

        with tempfile.TemporaryDirectory() as tmpdir:
            engine = ExecutiveBriefingEngine(
                repository=tmpdir,
                output_dir=tmpdir,
                persist=False,
                state_engine_class=_FakeEngine,
            )
            result = engine.generate()

        md = result["markdown"]
        self.assertIn("# AI CTO Executive Briefing", md)
        self.assertIn("Owner Dashboard", md)

    def test_generate_with_persist(self):
        snap = _make_snapshot()

        class _FakeEngine(FakeDevelopmentStateEngine):
            def __init__(self_inner, repository_root="."):
                super().__init__(snap, repository_root)

        with tempfile.TemporaryDirectory() as tmpdir:
            engine = ExecutiveBriefingEngine(
                repository=tmpdir,
                output_dir=tmpdir,
                persist=True,
                state_engine_class=_FakeEngine,
            )
            result = engine.generate()
            paths = result["paths"]
            for key in ("briefing", "recommendations", "priorities", "risks", "owner_actions", "markdown"):
                self.assertIn(key, paths, f"Missing path for {key}")
                self.assertTrue(Path(paths[key]).exists(), f"File not found: {paths[key]}")

    def test_briefing_id_is_stable_for_same_snapshot(self):
        snap = _make_snapshot()

        class _FakeEngine(FakeDevelopmentStateEngine):
            def __init__(self_inner, repository_root="."):
                super().__init__(snap, repository_root)

        with tempfile.TemporaryDirectory() as tmpdir:
            engine = ExecutiveBriefingEngine(
                repository=tmpdir,
                output_dir=tmpdir,
                persist=False,
                state_engine_class=_FakeEngine,
            )
            r1 = engine.generate()
            r2 = engine.generate()

        self.assertEqual(r1["briefing"].briefing_id, r2["briefing"].briefing_id)

    def test_degraded_snapshot_raises_risks_in_briefing(self):
        snap = _make_degraded_snapshot()

        class _FakeEngine(FakeDevelopmentStateEngine):
            def __init__(self_inner, repository_root="."):
                super().__init__(snap, repository_root)

        with tempfile.TemporaryDirectory() as tmpdir:
            engine = ExecutiveBriefingEngine(
                repository=tmpdir,
                output_dir=tmpdir,
                persist=False,
                state_engine_class=_FakeEngine,
            )
            result = engine.generate()

        briefing = result["briefing"]
        self.assertTrue(len(briefing.all_risks) >= 3, "Expected risks from degraded snapshot")
        self.assertNotIn(briefing.architecture_health, ("healthy",))

    def test_briefing_owner_dashboard_populated(self):
        snap = _make_snapshot()

        class _FakeEngine(FakeDevelopmentStateEngine):
            def __init__(self_inner, repository_root="."):
                super().__init__(snap, repository_root)

        with tempfile.TemporaryDirectory() as tmpdir:
            engine = ExecutiveBriefingEngine(
                repository=tmpdir,
                output_dir=tmpdir,
                persist=False,
                state_engine_class=_FakeEngine,
            )
            result = engine.generate()

        dash = result["briefing"].owner_dashboard
        self.assertTrue(dash.overall_health in ("healthy", "warning", "degraded", "critical"))
        self.assertTrue(dash.repository_readiness.strip())
        self.assertIsInstance(dash.open_risks, int)


# ---------------------------------------------------------------------------
# AI Toolkit integration test (real repository, no refresh)
# ---------------------------------------------------------------------------

class AIToolkitIntegrationTest(unittest.TestCase):
    """
    Validates the engine against the AI Toolkit repository itself.

    Uses the real DevelopmentStateEngine but does NOT refresh integrations,
    so no external analysis is re-run.
    """

    def test_generate_against_ai_toolkit(self):
        import os
        repo_root = os.path.abspath(".")
        engine = ExecutiveBriefingEngine(
            repository=repo_root,
            output_dir=repo_root,
            persist=False,
            refresh_integrations=False,
        )
        result = engine.generate()

        briefing = result["briefing"]
        self.assertIsInstance(briefing, ExecutiveBriefing)
        self.assertTrue(briefing.briefing_id.startswith("BRIEF-"))
        self.assertTrue(briefing.generated_at.endswith("Z"))
        self.assertEqual(briefing.schema_version, BRIEFING_VERSION)
        self.assertTrue(result["markdown"].strip())
        self.assertIn("# AI CTO Executive Briefing", result["markdown"])


# ---------------------------------------------------------------------------
# __all__ / public surface tests
# ---------------------------------------------------------------------------

class PublicSurfaceTests(unittest.TestCase):

    def test_all_public_classes_importable(self):
        from python.executive_briefing_engine import (
            ExecutiveBriefingEngine,
            ExecutiveBriefingGenerator,
            ExecutiveRecommendationEngine,
            ExecutivePriorityEngine,
            ExecutiveRiskAnalyzer,
            ExecutiveDecisionTracker,
            ExecutiveInsightGenerator,
            ExecutiveBriefingPersistence,
        )
        for cls in (
            ExecutiveBriefingEngine,
            ExecutiveBriefingGenerator,
            ExecutiveRecommendationEngine,
            ExecutivePriorityEngine,
            ExecutiveRiskAnalyzer,
            ExecutiveDecisionTracker,
            ExecutiveInsightGenerator,
            ExecutiveBriefingPersistence,
        ):
            self.assertTrue(callable(cls), f"{cls.__name__} is not callable")

    def test_briefing_version_constant(self):
        self.assertEqual(BRIEFING_VERSION, "1.0.0")


if __name__ == "__main__":
    unittest.main()
PY

echo "All executive briefing engine tests passed."

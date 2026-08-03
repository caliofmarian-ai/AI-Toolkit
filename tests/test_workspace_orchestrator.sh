#!/data/data/com.termux/files/usr/bin/bash
set -e

python3 - <<'PY'
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, "lib")

from python.workspace_orchestrator import (
    WorkspaceOrchestrator,
    WorkspaceRepository,
    WorkspaceDependencyEdge,
    WorkspaceRelationship,
    WorkspaceHealth,
    WorkspaceRecommendation,
    WorkspaceRisk,
    WorkspacePriority,
    WorkspaceScanResult,
    WorkspaceStatistics,
    WorkspaceRegistry,
    RepositoryRegistry,
    WorkspacePersistence,
    WorkspaceDiscoveryEngine,
    WorkspaceScanner,
    WorkspaceDependencyGraph,
    WorkspaceRelationshipAnalyzer,
    WorkspaceHealthEngine,
    WorkspacePriorityEngine,
    WorkspaceRiskAnalyzer,
    WorkspaceRecommendationEngine,
    WorkspaceExecutiveDashboard,
    WorkspaceReportGenerator,
    WorkspaceStateManager,
    WORKSPACE_SCHEMA_VERSION,
    HEALTH_HEALTHY,
    HEALTH_DEGRADED,
    HEALTH_CRITICAL,
    HEALTH_UNKNOWN,
    RISK_CRITICAL,
    RISK_HIGH,
    RISK_MEDIUM,
    RISK_LOW,
    STATUS_ACTIVE,
    STATUS_BLOCKED,
    STATUS_COMPLIANT,
    STATUS_PARTIAL,
    STATUS_MISSING,
)
from python.workspace_orchestrator.models import (
    REPO_TYPE_TOOL,
    REPO_TYPE_UNKNOWN,
    REPO_CATEGORY_AI,
    REPO_CATEGORY_UNKNOWN,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

def _make_repo(name="test-repo", **kwargs):
    defaults = dict(
        display_name=name,
        description=f"Description for {name}",
        repository_root=f"/tmp/{name}",
        repository_type=REPO_TYPE_TOOL,
        repository_category=REPO_CATEGORY_AI,
        repository_health=HEALTH_HEALTHY,
        readiness=85.0,
        canonical_status=STATUS_COMPLIANT,
        semantic_status=STATUS_COMPLIANT,
        runtime_status=HEALTH_HEALTHY,
        development_status=STATUS_ACTIVE,
        owner_status=STATUS_ACTIVE,
        risk_status=RISK_LOW,
        priority=5,
    )
    defaults.update(kwargs)
    return WorkspaceRepository(name=name, **defaults)


def _make_healthy_result(workspace_root="/tmp/ws"):
    r1 = _make_repo("repo-a", readiness=90.0, priority=2)
    r2 = _make_repo("repo-b", readiness=70.0, priority=4,
                    repository_health=HEALTH_DEGRADED,
                    canonical_status=STATUS_PARTIAL)
    health = WorkspaceHealth(
        overall_health=HEALTH_HEALTHY,
        repository_health=HEALTH_HEALTHY,
        architecture_health=HEALTH_HEALTHY,
        canonical_health=HEALTH_DEGRADED,
        development_health=HEALTH_HEALTHY,
        runtime_health=HEALTH_HEALTHY,
        executive_health=HEALTH_HEALTHY,
        owner_health=HEALTH_HEALTHY,
        healthy_count=1,
        degraded_count=1,
        critical_count=0,
        unknown_count=0,
        total_repositories=2,
        overall_readiness=80.0,
        average_priority=3.0,
    )
    return WorkspaceScanResult(
        workspace_id="WS-TEST01",
        workspace_root=workspace_root,
        generated_at="2026-01-01T00:00:00+00:00",
        schema_version=WORKSPACE_SCHEMA_VERSION,
        repositories=[r1, r2],
        dependencies=[],
        relationships=[],
        health=health,
        priorities=[
            WorkspacePriority(
                rank=1, repository="repo-a", reason="Test.",
                expected_impact="High.", confidence=0.9,
                required_effort="low", blocking_dependencies=(),
            ),
        ],
        recommendations=[
            WorkspaceRecommendation(
                id="WREC-001", title="Test rec", description="desc",
                priority=RISK_MEDIUM, impact="good", confidence=0.8,
                required_effort="medium", target_repository="repo-a",
            ),
        ],
        risks=[
            WorkspaceRisk(
                id="WRISK-001", category="health", severity=RISK_LOW,
                title="Low risk", description="Minor issue.",
                affected_repositories=("repo-b",), remediation="Fix it.",
            ),
        ],
        total_repositories=2,
        scanned_repositories=2,
        failed_repositories=0,
    )


# ---------------------------------------------------------------------------
# Tests — Models
# ---------------------------------------------------------------------------

class WorkspaceRepositoryModelTest(unittest.TestCase):

    def test_to_dict_round_trip(self):
        repo = _make_repo("my-repo", readiness=75.5, priority=3)
        d = repo.to_dict()
        assert d["name"] == "my-repo"
        assert d["readiness"] == 75.5
        assert d["priority"] == 3
        assert d["schema_version"] == WORKSPACE_SCHEMA_VERSION

        restored = WorkspaceRepository.from_dict(d)
        assert restored.name == repo.name
        assert restored.readiness == repo.readiness
        assert restored.priority == repo.priority

    def test_dependencies_are_tuples(self):
        repo = _make_repo("r", dependencies=("dep-a", "dep-b"))
        assert isinstance(repo.dependencies, tuple)
        d = repo.to_dict()
        assert isinstance(d["dependencies"], list)
        r2 = WorkspaceRepository.from_dict(d)
        assert r2.dependencies == ("dep-a", "dep-b")

    def test_tags_serialization(self):
        repo = _make_repo("r", tags=("ai", "core"))
        d = repo.to_dict()
        r2 = WorkspaceRepository.from_dict(d)
        assert r2.tags == ("ai", "core")


class WorkspaceDependencyEdgeModelTest(unittest.TestCase):

    def test_round_trip(self):
        edge = WorkspaceDependencyEdge(
            source="repo-a", target="repo-b",
            dependency_type="declared", confidence=0.9,
            evidence=("explicit dep",),
        )
        d = edge.to_dict()
        r = WorkspaceDependencyEdge.from_dict(d)
        assert r.source == "repo-a"
        assert r.target == "repo-b"
        assert r.confidence == 0.9
        assert r.evidence == ("explicit dep",)


class WorkspaceRelationshipModelTest(unittest.TestCase):

    def test_round_trip(self):
        rel = WorkspaceRelationship(
            repo_a="a", repo_b="b",
            relationship_type="sibling", strength=0.75,
            shared_components=("ai", "backend"),
        )
        d = rel.to_dict()
        r = WorkspaceRelationship.from_dict(d)
        assert r.repo_a == "a"
        assert r.strength == 0.75
        assert r.shared_components == ("ai", "backend")


class WorkspaceHealthModelTest(unittest.TestCase):

    def test_round_trip(self):
        h = WorkspaceHealth(
            overall_health=HEALTH_HEALTHY,
            repository_health=HEALTH_HEALTHY,
            architecture_health=HEALTH_DEGRADED,
            canonical_health=HEALTH_CRITICAL,
            development_health=HEALTH_HEALTHY,
            runtime_health=HEALTH_UNKNOWN,
            executive_health=HEALTH_HEALTHY,
            owner_health=HEALTH_HEALTHY,
            healthy_count=3,
            degraded_count=1,
            critical_count=0,
            unknown_count=1,
            total_repositories=5,
            overall_readiness=75.0,
            average_priority=4.0,
        )
        d = h.to_dict()
        r = WorkspaceHealth.from_dict(d)
        assert r.overall_health == HEALTH_HEALTHY
        assert r.canonical_health == HEALTH_CRITICAL
        assert r.total_repositories == 5
        assert r.overall_readiness == 75.0


class WorkspaceScanResultModelTest(unittest.TestCase):

    def test_round_trip(self):
        result = _make_healthy_result()
        d = result.to_dict()
        r = WorkspaceScanResult.from_dict(d)
        assert r.workspace_id == result.workspace_id
        assert r.total_repositories == result.total_repositories
        assert len(r.repositories) == 2
        assert len(r.priorities) == 1
        assert len(r.recommendations) == 1
        assert len(r.risks) == 1

    def test_statistics_round_trip(self):
        stats = WorkspaceStatistics(
            total_repositories=5,
            healthy_repositories=3,
            degraded_repositories=1,
            critical_repositories=0,
            unknown_repositories=1,
            blocked_repositories=0,
            active_repositories=4,
            total_dependencies=7,
            total_relationships=3,
            total_risks=2,
            critical_risks=0,
            total_recommendations=4,
            overall_readiness=78.5,
            scan_duration=1.23,
        )
        d = stats.to_dict()
        r = WorkspaceStatistics.from_dict(d)
        assert r.total_repositories == 5
        assert r.overall_readiness == 78.5
        assert r.scan_duration == 1.23


# ---------------------------------------------------------------------------
# Tests — Registry
# ---------------------------------------------------------------------------

class RepositoryRegistryTest(unittest.TestCase):

    def test_register_and_lookup(self):
        reg = RepositoryRegistry()
        repo = _make_repo("alpha")
        reg.register(repo)
        assert reg.contains("alpha")
        assert reg.get("alpha") is repo
        assert len(reg) == 1

    def test_remove(self):
        reg = RepositoryRegistry()
        reg.register(_make_repo("a"))
        reg.register(_make_repo("b"))
        removed = reg.remove("a")
        assert removed.name == "a"
        assert not reg.contains("a")
        assert reg.contains("b")

    def test_rename(self):
        reg = RepositoryRegistry()
        reg.register(_make_repo("old"))
        assert reg.rename("old", "new")
        assert not reg.contains("old")
        assert reg.contains("new")

    def test_relocate(self):
        reg = RepositoryRegistry()
        reg.register(_make_repo("r", repository_root="/tmp/r"))
        assert reg.relocate("r", "/new/path")
        assert reg.get("r").repository_root == "/new/path"

    def test_serialisation(self):
        reg = RepositoryRegistry()
        reg.register(_make_repo("a", readiness=80.0))
        reg.register(_make_repo("b", readiness=60.0))
        items = reg.to_list()
        assert len(items) == 2
        restored = RepositoryRegistry.from_list(items)
        assert restored.contains("a")
        assert restored.contains("b")

    def test_sort_by_priority(self):
        reg = RepositoryRegistry()
        reg.register(_make_repo("z", priority=5))
        reg.register(_make_repo("a", priority=1))
        reg.register(_make_repo("m", priority=3))
        names = [r.name for r in reg.all()]
        assert names == ["a", "m", "z"]


class WorkspaceRegistryTest(unittest.TestCase):

    def test_register_and_lookup(self):
        wr = WorkspaceRegistry()
        wr.register("WS-001", "/tmp/workspace")
        assert "WS-001" in wr.workspace_ids()
        assert wr.get_root("WS-001") is not None

    def test_remove(self):
        wr = WorkspaceRegistry()
        wr.register("WS-A", "/tmp/a")
        assert wr.remove("WS-A")
        assert len(wr) == 0

    def test_serialisation(self):
        wr = WorkspaceRegistry()
        wr.register("WS-X", "/tmp/x")
        d = wr.to_dict()
        restored = WorkspaceRegistry.from_dict(d)
        assert "WS-X" in restored.workspace_ids()


# ---------------------------------------------------------------------------
# Tests — Persistence
# ---------------------------------------------------------------------------

class WorkspacePersistenceTest(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.persistence = WorkspacePersistence(self.tmp)

    def test_save_and_load_repositories(self):
        result = _make_healthy_result(self.tmp)
        stats = WorkspaceStatistics(
            total_repositories=2,
            healthy_repositories=1,
            degraded_repositories=1,
            critical_repositories=0,
            unknown_repositories=0,
            blocked_repositories=0,
            active_repositories=2,
            total_dependencies=0,
            total_relationships=0,
            total_risks=1,
            critical_risks=0,
            total_recommendations=1,
            overall_readiness=80.0,
            scan_duration=0.5,
        )
        paths = self.persistence.save(result, stats)
        assert "workspace" in paths
        assert "repositories" in paths
        assert "health" in paths
        assert "statistics" in paths
        assert "history" in paths

        repos = self.persistence.load_repositories()
        assert len(repos) == 2
        names = {r.name for r in repos}
        assert "repo-a" in names
        assert "repo-b" in names

    def test_load_health(self):
        result = _make_healthy_result(self.tmp)
        stats = WorkspaceStatistics(
            total_repositories=2, healthy_repositories=1, degraded_repositories=1,
            critical_repositories=0, unknown_repositories=0, blocked_repositories=0,
            active_repositories=2, total_dependencies=0, total_relationships=0,
            total_risks=1, critical_risks=0, total_recommendations=1,
            overall_readiness=80.0, scan_duration=0.1,
        )
        self.persistence.save(result, stats)
        health = self.persistence.load_health()
        assert health is not None
        assert health.overall_health == HEALTH_HEALTHY
        assert health.total_repositories == 2

    def test_load_priorities(self):
        result = _make_healthy_result(self.tmp)
        stats = WorkspaceStatistics(
            total_repositories=2, healthy_repositories=1, degraded_repositories=1,
            critical_repositories=0, unknown_repositories=0, blocked_repositories=0,
            active_repositories=2, total_dependencies=0, total_relationships=0,
            total_risks=1, critical_risks=0, total_recommendations=1,
            overall_readiness=80.0, scan_duration=0.1,
        )
        self.persistence.save(result, stats)
        priorities = self.persistence.load_priorities()
        assert len(priorities) == 1
        assert priorities[0].repository == "repo-a"

    def test_history_grows(self):
        result = _make_healthy_result(self.tmp)
        stats = WorkspaceStatistics(
            total_repositories=2, healthy_repositories=1, degraded_repositories=1,
            critical_repositories=0, unknown_repositories=0, blocked_repositories=0,
            active_repositories=2, total_dependencies=0, total_relationships=0,
            total_risks=1, critical_risks=0, total_recommendations=1,
            overall_readiness=80.0, scan_duration=0.1,
        )
        self.persistence.save(result, stats)
        self.persistence.save(result, stats)
        history = self.persistence.load_history()
        assert len(history) == 2

    def test_exists_false_before_save(self):
        tmp2 = tempfile.mkdtemp()
        p = WorkspacePersistence(tmp2)
        assert not p.exists()

    def test_exists_true_after_save(self):
        result = _make_healthy_result(self.tmp)
        stats = WorkspaceStatistics(
            total_repositories=2, healthy_repositories=1, degraded_repositories=1,
            critical_repositories=0, unknown_repositories=0, blocked_repositories=0,
            active_repositories=2, total_dependencies=0, total_relationships=0,
            total_risks=1, critical_risks=0, total_recommendations=1,
            overall_readiness=80.0, scan_duration=0.1,
        )
        self.persistence.save(result, stats)
        assert self.persistence.exists()

    def test_atomic_write(self):
        """Verify the tmp-then-rename write produces valid JSON."""
        result = _make_healthy_result(self.tmp)
        stats = WorkspaceStatistics(
            total_repositories=2, healthy_repositories=1, degraded_repositories=1,
            critical_repositories=0, unknown_repositories=0, blocked_repositories=0,
            active_repositories=2, total_dependencies=0, total_relationships=0,
            total_risks=1, critical_risks=0, total_recommendations=1,
            overall_readiness=80.0, scan_duration=0.1,
        )
        self.persistence.save(result, stats)
        workspace_file = Path(self.tmp) / ".ai" / "workspace" / "workspace.json"
        assert workspace_file.exists()
        with open(str(workspace_file)) as fh:
            data = json.load(fh)
        assert data["workspace_id"] == "WS-TEST01"


# ---------------------------------------------------------------------------
# Tests — Discovery Engine
# ---------------------------------------------------------------------------

class WorkspaceDiscoveryEngineTest(unittest.TestCase):

    def test_discovers_git_repos(self):
        import os
        with tempfile.TemporaryDirectory() as tmp:
            # Create a fake git repo
            repo_a = Path(tmp) / "repo-a"
            repo_a.mkdir()
            (repo_a / ".git").mkdir()

            engine = WorkspaceDiscoveryEngine(tmp)
            repos = engine.discover()
            assert len(repos) == 1
            assert repos[0]["name"] == "repo-a"
            assert repos[0]["path"] == str(repo_a)

    def test_skips_non_git_directories(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "not-a-repo").mkdir()
            engine = WorkspaceDiscoveryEngine(tmp)
            repos = engine.discover()
            assert repos == []

    def test_empty_workspace(self):
        with tempfile.TemporaryDirectory() as tmp:
            engine = WorkspaceDiscoveryEngine(tmp)
            repos = engine.discover()
            assert repos == []

    def test_nested_discovery(self):
        with tempfile.TemporaryDirectory() as tmp:
            nested = Path(tmp) / "org" / "project"
            nested.mkdir(parents=True)
            (nested / ".git").mkdir()
            engine = WorkspaceDiscoveryEngine(tmp)
            repos = engine.discover_nested(max_depth=2)
            assert len(repos) == 1
            assert repos[0]["name"] == "project"


# ---------------------------------------------------------------------------
# Tests — Dependency Graph
# ---------------------------------------------------------------------------

class WorkspaceDependencyGraphTest(unittest.TestCase):

    def test_declared_dependencies(self):
        r1 = _make_repo("a", dependencies=("b",))
        r2 = _make_repo("b")
        graph = WorkspaceDependencyGraph([r1, r2])
        edges = graph.build()
        declared = [e for e in edges if e.dependency_type == "declared"]
        assert len(declared) == 1
        assert declared[0].source == "a"
        assert declared[0].target == "b"

    def test_no_self_dependency(self):
        r = _make_repo("a", dependencies=("a",))
        graph = WorkspaceDependencyGraph([r])
        edges = graph.build()
        # declared dep to 'a' from 'a' is only included if 'a' is in the repo list
        # since a depends on a and a is in the map, it will be included
        for e in edges:
            assert e.source != e.target or e.dependency_type != "declared"

    def test_cycle_detection_simple(self):
        r1 = _make_repo("a", dependencies=("b",))
        r2 = _make_repo("b", dependencies=("a",))
        graph = WorkspaceDependencyGraph([r1, r2])
        edges = graph.build()
        cycles = graph.detect_cycles(edges)
        assert len(cycles) >= 1

    def test_cycle_detection_no_cycle(self):
        r1 = _make_repo("a", dependencies=("b",))
        r2 = _make_repo("b")
        graph = WorkspaceDependencyGraph([r1, r2])
        edges = graph.build()
        cycles = graph.detect_cycles(edges)
        assert cycles == []

    def test_empty_repositories(self):
        graph = WorkspaceDependencyGraph([])
        edges = graph.build()
        assert edges == []


class WorkspaceRelationshipAnalyzerTest(unittest.TestCase):

    def test_sibling_detection(self):
        r1 = _make_repo("a", repository_category=REPO_CATEGORY_AI)
        r2 = _make_repo("b", repository_category=REPO_CATEGORY_AI)
        analyzer = WorkspaceRelationshipAnalyzer([r1, r2])
        rels = analyzer.analyze()
        siblings = [r for r in rels if r.relationship_type == "sibling"]
        assert len(siblings) >= 1

    def test_different_categories_no_sibling(self):
        r1 = _make_repo("a", repository_category=REPO_CATEGORY_AI)
        r2 = _make_repo("b", repository_category=REPO_CATEGORY_UNKNOWN)
        analyzer = WorkspaceRelationshipAnalyzer([r1, r2])
        rels = analyzer.analyze()
        siblings = [r for r in rels if r.relationship_type == "sibling"]
        assert len(siblings) == 0

    def test_deduplication(self):
        """Same pair should appear only once per relationship type."""
        r1 = _make_repo("a", repository_category=REPO_CATEGORY_AI)
        r2 = _make_repo("b", repository_category=REPO_CATEGORY_AI)
        analyzer = WorkspaceRelationshipAnalyzer([r1, r2])
        rels = analyzer.analyze()
        keys = [(r.repo_a, r.repo_b, r.relationship_type) for r in rels]
        assert len(keys) == len(set(keys))


# ---------------------------------------------------------------------------
# Tests — Intelligence Layer
# ---------------------------------------------------------------------------

class WorkspaceHealthEngineTest(unittest.TestCase):

    def test_all_healthy(self):
        repos = [
            _make_repo("a", repository_health=HEALTH_HEALTHY, readiness=90.0),
            _make_repo("b", repository_health=HEALTH_HEALTHY, readiness=85.0),
        ]
        engine = WorkspaceHealthEngine()
        health = engine.compute(repos)
        assert health.overall_health == HEALTH_HEALTHY
        assert health.healthy_count == 2
        assert health.total_repositories == 2

    def test_critical_repository_downgrades_workspace(self):
        repos = [
            _make_repo("a", repository_health=HEALTH_HEALTHY, readiness=90.0),
            _make_repo("b", repository_health=HEALTH_CRITICAL, readiness=20.0),
        ]
        engine = WorkspaceHealthEngine()
        health = engine.compute(repos)
        assert health.critical_count == 1

    def test_empty_workspace(self):
        engine = WorkspaceHealthEngine()
        health = engine.compute([])
        assert health.overall_health == HEALTH_UNKNOWN
        assert health.total_repositories == 0

    def test_readiness_average(self):
        repos = [
            _make_repo("a", readiness=80.0),
            _make_repo("b", readiness=60.0),
        ]
        engine = WorkspaceHealthEngine()
        health = engine.compute(repos)
        assert abs(health.overall_readiness - 70.0) < 0.01


class WorkspacePriorityEngineTest(unittest.TestCase):

    def test_ranking_order(self):
        repos = [
            _make_repo("a", risk_status=RISK_LOW, repository_health=HEALTH_HEALTHY, readiness=90.0, priority=5),
            _make_repo("b", risk_status=RISK_CRITICAL, repository_health=HEALTH_CRITICAL, readiness=30.0, priority=1),
        ]
        engine = WorkspacePriorityEngine()
        priorities = engine.rank(repos, [])
        assert len(priorities) == 2
        assert priorities[0].repository == "b"   # critical first
        assert priorities[1].repository == "a"

    def test_reason_and_impact_populated(self):
        repos = [
            _make_repo("x", repository_health=HEALTH_DEGRADED, risk_status=RISK_HIGH),
        ]
        engine = WorkspacePriorityEngine()
        priorities = engine.rank(repos, [])
        assert len(priorities) == 1
        assert priorities[0].reason != ""
        assert priorities[0].expected_impact != ""

    def test_blocking_dependencies_populated(self):
        repos = [_make_repo("a"), _make_repo("b")]
        deps = [WorkspaceDependencyEdge(
            source="x", target="a", dependency_type="declared", confidence=1.0
        )]
        engine = WorkspacePriorityEngine()
        priorities = engine.rank(repos, deps)
        a_priority = next(p for p in priorities if p.repository == "a")
        assert "x" in a_priority.blocking_dependencies

    def test_empty_returns_empty(self):
        engine = WorkspacePriorityEngine()
        assert engine.rank([], []) == []


class WorkspaceRiskAnalyzerTest(unittest.TestCase):

    def test_critical_health_creates_risk(self):
        repos = [
            _make_repo("bad", repository_health=HEALTH_CRITICAL, readiness=25.0),
        ]
        analyzer = WorkspaceRiskAnalyzer()
        risks = analyzer.analyze(repos, [], [])
        critical = [r for r in risks if r.severity == RISK_CRITICAL]
        assert len(critical) >= 1

    def test_canonical_missing_creates_risk(self):
        repos = [_make_repo("r", canonical_status=STATUS_MISSING)]
        analyzer = WorkspaceRiskAnalyzer()
        risks = analyzer.analyze(repos, [], [])
        high = [r for r in risks if r.severity == RISK_HIGH and "canonical" in r.category.lower()]
        assert len(high) >= 1

    def test_cycle_creates_risk(self):
        repos = [_make_repo("a"), _make_repo("b")]
        cycles = [["a", "b"]]
        analyzer = WorkspaceRiskAnalyzer()
        risks = analyzer.analyze(repos, [], cycles)
        cycle_risks = [r for r in risks if "cycle" in r.title.lower()]
        assert len(cycle_risks) >= 1

    def test_sorted_critical_first(self):
        repos = [
            _make_repo("a", canonical_status=STATUS_MISSING, repository_health=HEALTH_CRITICAL, readiness=20.0),
        ]
        analyzer = WorkspaceRiskAnalyzer()
        risks = analyzer.analyze(repos, [], [])
        if len(risks) >= 2:
            order = {RISK_CRITICAL: 0, RISK_HIGH: 1, RISK_MEDIUM: 2, RISK_LOW: 3}
            for i in range(len(risks) - 1):
                assert order.get(risks[i].severity, 9) <= order.get(risks[i+1].severity, 9)

    def test_empty_repositories(self):
        analyzer = WorkspaceRiskAnalyzer()
        risks = analyzer.analyze([], [], [])
        assert isinstance(risks, list)


class WorkspaceRecommendationEngineTest(unittest.TestCase):

    def _make_health(self, overall=HEALTH_HEALTHY, readiness=80.0):
        return WorkspaceHealth(
            overall_health=overall,
            repository_health=overall,
            architecture_health=overall,
            canonical_health=overall,
            development_health=overall,
            runtime_health=overall,
            executive_health=overall,
            owner_health=overall,
            healthy_count=1,
            total_repositories=1,
            overall_readiness=readiness,
        )

    def test_always_produces_at_least_one(self):
        engine = WorkspaceRecommendationEngine()
        repos = [_make_repo("a")]
        health = self._make_health()
        risks = []
        priorities = [WorkspacePriority(
            rank=1, repository="a", reason="test", expected_impact="good",
            confidence=0.9, required_effort="low", blocking_dependencies=(),
        )]
        recs = engine.generate(repos, health, risks, priorities)
        assert len(recs) >= 1

    def test_critical_risk_creates_critical_recommendation(self):
        engine = WorkspaceRecommendationEngine()
        repos = [_make_repo("a")]
        health = self._make_health(HEALTH_CRITICAL, 30.0)
        risks = [WorkspaceRisk(
            id="WRISK-001", category="health", severity=RISK_CRITICAL,
            title="Critical", description="Very bad.",
            affected_repositories=("a",), remediation="Fix ASAP.",
        )]
        priorities = []
        recs = engine.generate(repos, health, risks, priorities)
        critical = [r for r in recs if r.priority == RISK_CRITICAL]
        assert len(critical) >= 1

    def test_recommendations_sorted(self):
        engine = WorkspaceRecommendationEngine()
        repos = [_make_repo("a", canonical_status=STATUS_MISSING)]
        health = self._make_health()
        risks = []
        priorities = []
        recs = engine.generate(repos, health, risks, priorities)
        order = {RISK_CRITICAL: 0, RISK_HIGH: 1, RISK_MEDIUM: 2, RISK_LOW: 3}
        for i in range(len(recs) - 1):
            assert order.get(recs[i].priority, 9) <= order.get(recs[i+1].priority, 9)


# ---------------------------------------------------------------------------
# Tests — Dashboard
# ---------------------------------------------------------------------------

class WorkspaceExecutiveDashboardTest(unittest.TestCase):

    def test_build_returns_all_keys(self):
        result = _make_healthy_result()
        stats = WorkspaceStatistics(
            total_repositories=2, healthy_repositories=1, degraded_repositories=1,
            critical_repositories=0, unknown_repositories=0, blocked_repositories=0,
            active_repositories=2, total_dependencies=0, total_relationships=0,
            total_risks=1, critical_risks=0, total_recommendations=1,
            overall_readiness=80.0, scan_duration=0.5,
        )
        engine = WorkspaceExecutiveDashboard()
        d = engine.build(result, stats)
        required_keys = [
            "executive_summary", "workspace_summary", "health",
            "current_priorities", "current_risks", "current_recommendations",
            "suggested_next_repository", "estimated_overall_progress",
        ]
        for key in required_keys:
            assert key in d, f"Missing key: {key}"

    def test_suggested_next_repository(self):
        result = _make_healthy_result()
        stats = WorkspaceStatistics(
            total_repositories=2, healthy_repositories=1, degraded_repositories=1,
            critical_repositories=0, unknown_repositories=0, blocked_repositories=0,
            active_repositories=2, total_dependencies=0, total_relationships=0,
            total_risks=1, critical_risks=0, total_recommendations=1,
            overall_readiness=80.0, scan_duration=0.5,
        )
        engine = WorkspaceExecutiveDashboard()
        d = engine.build(result, stats)
        assert d["suggested_next_repository"] == "repo-a"


class WorkspaceReportGeneratorTest(unittest.TestCase):

    def _build_dashboard(self):
        result = _make_healthy_result()
        stats = WorkspaceStatistics(
            total_repositories=2, healthy_repositories=1, degraded_repositories=1,
            critical_repositories=0, unknown_repositories=0, blocked_repositories=0,
            active_repositories=2, total_dependencies=0, total_relationships=0,
            total_risks=1, critical_risks=0, total_recommendations=1,
            overall_readiness=80.0, scan_duration=0.5,
        )
        return WorkspaceExecutiveDashboard().build(result, stats)

    def test_generates_markdown(self):
        gen = WorkspaceReportGenerator()
        d = self._build_dashboard()
        md = gen.generate(d)
        assert md.startswith("# AI CTO Workspace Dashboard")
        assert "## Executive Summary" in md
        assert "## Workspace Summary" in md
        assert "## Workspace Health" in md
        assert "## Current Priorities" in md
        assert "## Suggested Next Actions" in md

    def test_markdown_contains_repository_names(self):
        gen = WorkspaceReportGenerator()
        d = self._build_dashboard()
        md = gen.generate(d)
        assert "repo-a" in md

    def test_write_to_disk(self):
        with tempfile.TemporaryDirectory() as tmp:
            gen = WorkspaceReportGenerator()
            d = self._build_dashboard()
            md = gen.generate(d)
            path = gen.write(md, tmp)
            assert Path(path).exists()
            assert Path(path).name == "AI_CTO_WORKSPACE_DASHBOARD.md"
            content = Path(path).read_text()
            assert "# AI CTO Workspace Dashboard" in content


# ---------------------------------------------------------------------------
# Tests — State Manager
# ---------------------------------------------------------------------------

class WorkspaceStateManagerTest(unittest.TestCase):

    def test_load_from_empty_dir(self):
        with tempfile.TemporaryDirectory() as tmp:
            manager = WorkspaceStateManager(tmp)
            manager.load()
            assert manager.repository_count() == 0

    def test_register_and_retrieve(self):
        with tempfile.TemporaryDirectory() as tmp:
            manager = WorkspaceStateManager(tmp)
            repo = _make_repo("r1")
            manager.register_repository(repo)
            assert manager.repository_count() == 1
            repos = manager.current_repositories()
            assert repos[0].name == "r1"

    def test_remove_repository(self):
        with tempfile.TemporaryDirectory() as tmp:
            manager = WorkspaceStateManager(tmp)
            manager.register_repository(_make_repo("x"))
            removed = manager.remove_repository("x")
            assert removed is not None
            assert manager.repository_count() == 0

    def test_workspace_id_deterministic(self):
        with tempfile.TemporaryDirectory() as tmp:
            m1 = WorkspaceStateManager(tmp)
            m2 = WorkspaceStateManager(tmp)
            assert m1.ensure_workspace_id() == m2.ensure_workspace_id()


# ---------------------------------------------------------------------------
# Tests — Full Orchestrator Integration
# ---------------------------------------------------------------------------

class WorkspaceOrchestratorIntegrationTest(unittest.TestCase):

    def test_scan_parent_directory(self):
        """Scan the parent of the current repo — discovers AI-Toolkit."""
        workspace = str(Path(".").resolve().parent)
        with tempfile.TemporaryDirectory() as tmp:
            orchestrator = WorkspaceOrchestrator(
                workspace_root=workspace,
                output_dir=tmp,
                persist=False,
            )
            result = orchestrator.scan()
            assert result.total_repositories >= 1
            names = [r.name for r in result.repositories]
            assert "AI-Toolkit" in names

    def test_scan_with_persistence(self):
        """Scan and verify all 11 artifact files are created."""
        workspace = str(Path(".").resolve().parent)
        with tempfile.TemporaryDirectory() as tmp:
            orchestrator = WorkspaceOrchestrator(
                workspace_root=workspace,
                output_dir=tmp,
                persist=True,
            )
            result = orchestrator.scan()

            ai_dir = Path(workspace) / ".ai" / "workspace"
            expected_files = [
                "workspace.json", "repositories.json", "dependencies.json",
                "relationships.json", "health.json", "priorities.json",
                "recommendations.json", "risks.json", "statistics.json",
                "history.json", "dashboard.json",
            ]
            for fname in expected_files:
                assert (ai_dir / fname).exists(), f"Missing: {fname}"

            dashboard_md = Path(tmp) / "AI_CTO_WORKSPACE_DASHBOARD.md"
            assert dashboard_md.exists()

    def test_scan_produces_valid_health(self):
        workspace = str(Path(".").resolve().parent)
        with tempfile.TemporaryDirectory() as tmp:
            o = WorkspaceOrchestrator(workspace_root=workspace, output_dir=tmp, persist=False)
            result = o.scan()
            assert result.health.total_repositories == result.total_repositories
            assert result.health.overall_health in (
                HEALTH_HEALTHY, HEALTH_DEGRADED, HEALTH_CRITICAL, HEALTH_UNKNOWN
            )

    def test_scan_produces_valid_recommendations(self):
        workspace = str(Path(".").resolve().parent)
        with tempfile.TemporaryDirectory() as tmp:
            o = WorkspaceOrchestrator(workspace_root=workspace, output_dir=tmp, persist=False)
            result = o.scan()
            for rec in result.recommendations:
                assert rec.id.startswith("WREC-")
                assert rec.title
                assert rec.priority in (RISK_CRITICAL, RISK_HIGH, RISK_MEDIUM, RISK_LOW)
                assert 0.0 <= rec.confidence <= 1.0

    def test_scan_produces_valid_priorities(self):
        workspace = str(Path(".").resolve().parent)
        with tempfile.TemporaryDirectory() as tmp:
            o = WorkspaceOrchestrator(workspace_root=workspace, output_dir=tmp, persist=False)
            result = o.scan()
            for i, p in enumerate(result.priorities, start=1):
                assert p.rank == i
                assert p.repository
                assert p.confidence > 0.0

    def test_register_single_repository(self):
        workspace = str(Path(".").resolve().parent)
        with tempfile.TemporaryDirectory() as tmp:
            o = WorkspaceOrchestrator(workspace_root=workspace, output_dir=tmp, persist=True)
            repo = o.register_repository(str(Path(".").resolve()))
            assert repo.name == "AI-Toolkit"
            assert repo.repository_root
            assert repo.last_scan != ""

    def test_dashboard_after_scan(self):
        workspace = str(Path(".").resolve().parent)
        with tempfile.TemporaryDirectory() as tmp:
            o = WorkspaceOrchestrator(workspace_root=workspace, output_dir=tmp, persist=True)
            o.scan()
            # Now reload and generate dashboard
            o2 = WorkspaceOrchestrator(workspace_root=workspace, output_dir=tmp, persist=False)
            d = o2.dashboard()
            assert "markdown" in d
            assert "# AI CTO Workspace Dashboard" in d["markdown"]
            assert "dashboard_dict" in d

    def test_backward_compat_execute(self):
        """execute() method should still work as before."""
        workspace = str(Path(".").resolve().parent)
        o = WorkspaceOrchestrator(workspace_root=workspace)
        results = o.execute(workspace)
        assert len(results) >= 1
        for r in results:
            assert "repository" in r
            assert "status" in r
            assert r["status"] in ("SUCCESS", "FAILED")

    def test_scan_result_serializable(self):
        workspace = str(Path(".").resolve().parent)
        with tempfile.TemporaryDirectory() as tmp:
            o = WorkspaceOrchestrator(workspace_root=workspace, output_dir=tmp, persist=False)
            result = o.scan()
            d = result.to_dict()
            # Must be fully serialisable
            serialized = json.dumps(d)
            assert len(serialized) > 100


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main(verbosity=2)

loader = unittest.TestLoader()
suite = unittest.TestSuite()

for test_class in [
    WorkspaceRepositoryModelTest,
    WorkspaceDependencyEdgeModelTest,
    WorkspaceRelationshipModelTest,
    WorkspaceHealthModelTest,
    WorkspaceScanResultModelTest,
    RepositoryRegistryTest,
    WorkspaceRegistryTest,
    WorkspacePersistenceTest,
    WorkspaceDiscoveryEngineTest,
    WorkspaceDependencyGraphTest,
    WorkspaceRelationshipAnalyzerTest,
    WorkspaceHealthEngineTest,
    WorkspacePriorityEngineTest,
    WorkspaceRiskAnalyzerTest,
    WorkspaceRecommendationEngineTest,
    WorkspaceExecutiveDashboardTest,
    WorkspaceReportGeneratorTest,
    WorkspaceStateManagerTest,
    WorkspaceOrchestratorIntegrationTest,
]:
    suite.addTests(loader.loadTestsFromTestCase(test_class))

runner = unittest.TextTestRunner(verbosity=2)
result = runner.run(suite)

print()
print(f"Tests run:   {result.testsRun}")
print(f"Failures:    {len(result.failures)}")
print(f"Errors:      {len(result.errors)}")
print()

if result.failures or result.errors:
    print("WORKSPACE ORCHESTRATOR TESTS FAILED")
    sys.exit(1)
else:
    print("Workspace Orchestrator PASS")
PY

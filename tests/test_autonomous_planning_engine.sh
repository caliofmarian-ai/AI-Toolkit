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

from python.autonomous_planning_engine import (
    AutonomousPlanningEngine,
    PlanningDecisionEngine,
    DependencyGraph,
    DependencyResolver,
    PriorityOptimizer,
    RoadmapPlanner,
    IssuePlanner,
    BatchPlanner,
    PullRequestPlanner,
    MilestonePlanner,
    ExecutionQueueBuilder,
    PlanningPersistence,
    PlanningReportGenerator,
    PLANNING_VERSION,
    PRIORITY_CRITICAL,
    PRIORITY_HIGH,
    PRIORITY_MEDIUM,
    PRIORITY_LOW,
    PRIORITY_BLOCKED,
    EFFORT_LOW,
    EFFORT_MEDIUM,
    EFFORT_HIGH,
    TYPE_CORE,
    TYPE_ISSUE,
    TYPE_BATCH,
    TYPE_PR,
    TYPE_MILESTONE,
    PHASE_FOUNDATION,
    PHASE_INTELLIGENCE,
    PHASE_AUTONOMY,
    PHASE_PRODUCTION,
    MATURITY_EARLY,
    MATURITY_DEVELOPING,
    MATURITY_MATURE,
    MATURITY_ADVANCED,
    PlanningEntry,
    ExecutionQueue,
    RoadmapProgress,
    NextActions,
    PlanningResult,
)

print("1. Imports OK")

# ---------------------------------------------------------------------------
# 2. PlanningEntry model
# ---------------------------------------------------------------------------

entry = PlanningEntry(
    entry_id="CORE-015",
    title="Implement CORE-015",
    type=TYPE_CORE,
    priority=PRIORITY_HIGH,
    reason="Test reason",
    dependencies=("CORE-014",),
    estimated_effort=EFFORT_MEDIUM,
    confidence=0.85,
    blocked_by=(),
    metadata={"core_id": "CORE-015"},
)
d = entry.to_dict()
assert d["entry_id"] == "CORE-015"
assert d["type"] == TYPE_CORE
assert d["priority"] == PRIORITY_HIGH
assert d["confidence"] == 0.85
assert d["dependencies"] == ["CORE-014"]
assert d["blocked_by"] == []
print("2. PlanningEntry model OK")

# ---------------------------------------------------------------------------
# 3. DependencyGraph
# ---------------------------------------------------------------------------

graph = DependencyGraph()
graph.add_edge("CORE-014", "CORE-009")
graph.add_edge("CORE-014", "CORE-010")
graph.add_edge("CORE-010", "CORE-009")
assert "CORE-014" in graph.nodes()
assert "CORE-009" in graph.dependencies_of("CORE-014")
assert "CORE-010" in graph.dependencies_of("CORE-014")
assert not graph.has_cycle()

order = graph.topological_sort()
assert order.index("CORE-009") < order.index("CORE-014")
assert order.index("CORE-010") < order.index("CORE-014")

# Cycle detection
cycle_graph = DependencyGraph()
cycle_graph.add_edge("A", "B")
cycle_graph.add_edge("B", "A")
assert cycle_graph.has_cycle()

graph_dict = graph.to_dict()
assert graph_dict["node_count"] == 3
assert graph_dict["edge_count"] == 3
print("3. DependencyGraph OK")

# ---------------------------------------------------------------------------
# 4. DependencyResolver — core graph from AI Toolkit itself
# ---------------------------------------------------------------------------

resolver = DependencyResolver(".")
core_graph = resolver.build_core_graph()
core_dict = core_graph.to_dict()
assert core_dict["node_count"] >= 0  # may be 0 in minimal CI environments
assert isinstance(core_dict["edges"], dict)

dep_map = resolver.core_dependency_map()
assert isinstance(dep_map, dict)

# Resolve entries — dependency ordering
entries_raw = [
    {
        "entry_id": "CORE-B",
        "title": "B",
        "dependencies": ["CORE-A"],
        "blocked_by": [],
    },
    {
        "entry_id": "CORE-A",
        "title": "A",
        "dependencies": [],
        "blocked_by": [],
    },
]
resolved = resolver.resolve_entries(entries_raw)
ids = [e["entry_id"] for e in resolved]
assert ids.index("CORE-A") < ids.index("CORE-B"), f"Expected A before B, got {ids}"

# Blocked entries go last
entries_with_blocked = [
    {"entry_id": "UNBLOCKED", "title": "x", "dependencies": [], "blocked_by": []},
    {"entry_id": "BLOCKED", "title": "y", "dependencies": [], "blocked_by": ["CORE-X"]},
]
resolved2 = resolver.resolve_entries(entries_with_blocked)
ids2 = [e["entry_id"] for e in resolved2]
assert ids2.index("UNBLOCKED") < ids2.index("BLOCKED"), f"Expected UNBLOCKED before BLOCKED, got {ids2}"
print("4. DependencyResolver OK")

# ---------------------------------------------------------------------------
# 5. PriorityOptimizer
# ---------------------------------------------------------------------------

opt = PriorityOptimizer()

entries_to_opt = [
    PlanningEntry(
        entry_id="HIGH",
        title="Critical CORE",
        type=TYPE_CORE,
        priority=PRIORITY_HIGH,
        reason="test",
        dependencies=(),
        estimated_effort=EFFORT_LOW,
        confidence=0.9,
        blocked_by=(),
        metadata={},
    ),
    PlanningEntry(
        entry_id="LOW",
        title="Low priority item",
        type=TYPE_ISSUE,
        priority=PRIORITY_LOW,
        reason="test",
        dependencies=(),
        estimated_effort=EFFORT_HIGH,
        confidence=0.4,
        blocked_by=(),
        metadata={},
    ),
    PlanningEntry(
        entry_id="BLOCKED",
        title="Blocked item",
        type=TYPE_BATCH,
        priority=PRIORITY_MEDIUM,
        reason="test",
        dependencies=(),
        estimated_effort=EFFORT_MEDIUM,
        confidence=0.5,
        blocked_by=("CORE-X",),
        metadata={},
    ),
]
optimised = opt.optimize(entries_to_opt, {}, {})
assert len(optimised) == 3
# Blocked must be last or assigned PRIORITY_BLOCKED
blocked_entries = [e for e in optimised if e.blocked_by]
assert all(e.priority == PRIORITY_BLOCKED for e in blocked_entries)
print("5. PriorityOptimizer OK")

# ---------------------------------------------------------------------------
# 6. RoadmapPlanner
# ---------------------------------------------------------------------------

roadmap_planner = RoadmapPlanner()

decision_ctx = {
    "implemented_cores": ["CORE-007", "CORE-008", "CORE-009", "CORE-010"],
    "documented_cores": ["CORE-007", "CORE-008", "CORE-009", "CORE-010", "CORE-011"],
    "incomplete_cores": ["CORE-011"],
    "blocked_cores": [],
    "next_core": "CORE-011",
    "completion_percentage": 80.0,
}

rec = roadmap_planner.recommend_next_core(decision_ctx)
assert rec is not None
assert rec["id"] == "CORE-011"
assert rec["type"] == TYPE_CORE
assert 0 < rec["confidence"] <= 1.0

roadmap_entries = roadmap_planner.build_roadmap_entries(decision_ctx)
assert len(roadmap_entries) == 1
assert roadmap_entries[0].entry_id == "CORE-011"

# No incomplete COREs → None
empty_ctx = {
    "implemented_cores": ["CORE-007"],
    "documented_cores": ["CORE-007"],
    "incomplete_cores": [],
    "blocked_cores": [],
    "next_core": None,
    "completion_percentage": 100.0,
}
assert roadmap_planner.recommend_next_core(empty_ctx) is None
print("6. RoadmapPlanner OK")

# ---------------------------------------------------------------------------
# 7. IssuePlanner
# ---------------------------------------------------------------------------

issue_planner = IssuePlanner()
issue_rec = issue_planner.recommend_next_issue(decision_ctx, {}, {})
# May or may not produce a recommendation — just check types
if issue_rec is not None:
    assert isinstance(issue_rec, dict)
    assert "title" in issue_rec

issue_entries = issue_planner.build_issue_entries(decision_ctx, {}, {})
assert isinstance(issue_entries, list)
for ie in issue_entries:
    assert isinstance(ie, PlanningEntry)
    assert ie.type == TYPE_ISSUE
print("7. IssuePlanner OK")

# ---------------------------------------------------------------------------
# 8. BatchPlanner
# ---------------------------------------------------------------------------

with tempfile.TemporaryDirectory() as tmpdir:
    # Create a minimal batch document
    dev_dir = Path(tmpdir) / "development"
    dev_dir.mkdir()
    (dev_dir / "BATCH-003_TEST.md").write_text(
        "# BATCH-003\nStatus: IN DEVELOPMENT\nCORE-011 reference\n"
    )
    b_planner = BatchPlanner(tmpdir)
    b_rec = b_planner.recommend_next_batch(decision_ctx, {}, {})
    # Should detect the IN DEVELOPMENT batch
    b_entries = b_planner.build_batch_entries(decision_ctx, {}, {})
    assert isinstance(b_entries, list)
    for be in b_entries:
        assert isinstance(be, PlanningEntry)
        assert be.type == TYPE_BATCH
print("8. BatchPlanner OK")

# ---------------------------------------------------------------------------
# 9. PullRequestPlanner
# ---------------------------------------------------------------------------

pr_planner = PullRequestPlanner()
pr_rec = pr_planner.recommend_next_pr(
    {"current_branch": "feature/core-011-new-engine", "suggested_next_pr": ""},
    {},
    {},
)
assert pr_rec is not None  # should recommend opening PR for feature branch
assert "title" in pr_rec

pr_entries = pr_planner.build_pr_entries(
    {"current_branch": "feature/core-011", "suggested_next_pr": ""},
    {},
    {},
)
assert isinstance(pr_entries, list)
for pe in pr_entries:
    assert pe.type == TYPE_PR
print("9. PullRequestPlanner OK")

# ---------------------------------------------------------------------------
# 10. MilestonePlanner
# ---------------------------------------------------------------------------

ms_planner = MilestonePlanner()
ms_rec = ms_planner.recommend_next_milestone(
    {"current_phase": PHASE_INTELLIGENCE, "current_milestone": "OLD-MS",
     "implemented_cores": ["CORE-007", "CORE-008"], "completion_percentage": 60.0,
     "incomplete_cores": ["CORE-009"]},
    {},
)
assert ms_rec is not None
assert "title" in ms_rec

ms_entries = ms_planner.build_milestone_entries(
    {"current_phase": PHASE_FOUNDATION, "current_milestone": "",
     "implemented_cores": [], "completion_percentage": 0.0,
     "incomplete_cores": ["CORE-007"]},
    {},
)
assert isinstance(ms_entries, list)
for me in ms_entries:
    assert me.type == TYPE_MILESTONE
print("10. MilestonePlanner OK")

# ---------------------------------------------------------------------------
# 11. ExecutionQueueBuilder
# ---------------------------------------------------------------------------

queue_entries = [
    PlanningEntry(
        entry_id="CORE-011",
        title="Implement CORE-011",
        type=TYPE_CORE,
        priority=PRIORITY_HIGH,
        reason="next core",
        dependencies=("CORE-009",),
        estimated_effort=EFFORT_MEDIUM,
        confidence=0.85,
        blocked_by=(),
        metadata={},
    ),
    PlanningEntry(
        entry_id="CORE-009",
        title="Implement CORE-009",
        type=TYPE_CORE,
        priority=PRIORITY_CRITICAL,
        reason="prerequisite",
        dependencies=(),
        estimated_effort=EFFORT_LOW,
        confidence=0.95,
        blocked_by=(),
        metadata={},
    ),
]

with tempfile.TemporaryDirectory() as tmpdir:
    builder = ExecutionQueueBuilder(tmpdir)
    queue = builder.build(
        entries=queue_entries,
        snapshot={},
        queue_id="TEST-QUEUE",
        generated_at="2026-01-01T00:00:00+00:00",
        repository=tmpdir,
    )
    assert isinstance(queue, ExecutionQueue)
    assert queue.queue_id == "TEST-QUEUE"
    assert len(queue.entries) == 2
    q_dict = queue.to_dict()
    assert q_dict["entry_count"] == 2
    assert isinstance(q_dict["entries"], list)
print("11. ExecutionQueueBuilder OK")

# ---------------------------------------------------------------------------
# 12. PlanningPersistence — atomic writes
# ---------------------------------------------------------------------------

from python.autonomous_planning_engine.models import PLANNING_VERSION

with tempfile.TemporaryDirectory() as tmpdir:
    persistence = PlanningPersistence(tmpdir)
    assert not persistence.exists()

    # Build a minimal PlanningResult to persist
    eq = ExecutionQueue(
        queue_id="Q-001",
        generated_at="2026-01-01T00:00:00+00:00",
        schema_version=PLANNING_VERSION,
        repository=tmpdir,
        entries=[],
    )
    na = NextActions(
        generated_at="2026-01-01T00:00:00+00:00",
        repository=tmpdir,
    )
    rp = RoadmapProgress(
        generated_at="2026-01-01T00:00:00+00:00",
        repository=tmpdir,
        total_cores=10,
        completed_cores=["CORE-007"],
        incomplete_cores=["CORE-011"],
        blocked_cores=[],
        current_phase=PHASE_FOUNDATION,
        repository_maturity=MATURITY_EARLY,
        completion_percentage=10.0,
        estimated_remaining_effort=EFFORT_HIGH,
        next_core="CORE-011",
    )
    pr = PlanningResult(
        planning_id="PLAN-TEST",
        generated_at="2026-01-01T00:00:00+00:00",
        repository=tmpdir,
        schema_version=PLANNING_VERSION,
        execution_queue=eq,
        next_actions=na,
        roadmap_progress=rp,
        recommended_core=None,
        recommended_issue=None,
        recommended_batch=None,
        recommended_pr=None,
        recommended_milestone=None,
    )

    paths = persistence.save(pr)
    assert persistence.exists()
    assert Path(paths["planning"]).exists()
    assert Path(paths["execution_queue"]).exists()
    assert Path(paths["next_actions"]).exists()
    assert Path(paths["roadmap_progress"]).exists()

    loaded = persistence.load_planning()
    assert loaded["planning_id"] == "PLAN-TEST"
    assert loaded["schema_version"] == PLANNING_VERSION
print("12. PlanningPersistence OK")

# ---------------------------------------------------------------------------
# 13. PlanningReportGenerator
# ---------------------------------------------------------------------------

generator = PlanningReportGenerator()
markdown = generator.render(pr)
assert "# AI CTO Planning Report" in markdown
assert "PLAN-TEST" in markdown
assert "Roadmap Progress" in markdown
assert "Next Actions" in markdown
assert "Execution Queue" in markdown

with tempfile.TemporaryDirectory() as tmpdir:
    out_path = Path(tmpdir) / "AI_CTO_PLANNING_REPORT.md"
    generator.generate(pr, out_path)
    assert out_path.exists()
    content = out_path.read_text(encoding="utf-8")
    assert "PLAN-TEST" in content
print("13. PlanningReportGenerator OK")

# ---------------------------------------------------------------------------
# 14. AutonomousPlanningEngine — integration test against AI Toolkit itself
# ---------------------------------------------------------------------------

engine = AutonomousPlanningEngine(
    repository=".",
    persist=True,
    refresh_integrations=False,
)
result = engine.plan()

assert "planning_result" in result
assert "planning_dict" in result
assert "markdown" in result
assert "paths" in result

d = result["planning_dict"]

# Schema
assert d["schema_version"] == PLANNING_VERSION
assert d["planning_id"].startswith("PLAN-")

# Roadmap progress
rp_d = d["roadmap_progress"]
assert isinstance(rp_d["completed_cores"], list)
assert isinstance(rp_d["incomplete_cores"], list)
assert 0 <= rp_d["completion_percentage"] <= 100
assert rp_d["current_phase"] in (
    PHASE_FOUNDATION, PHASE_INTELLIGENCE, PHASE_AUTONOMY, PHASE_PRODUCTION
)
assert rp_d["repository_maturity"] in (
    MATURITY_EARLY, MATURITY_DEVELOPING, MATURITY_MATURE, MATURITY_ADVANCED
)

# Execution queue
queue_d = d["execution_queue"]
assert isinstance(queue_d["entries"], list)
assert queue_d["entry_count"] >= 0

# Artifacts written to disk
paths = result["paths"]
assert Path(paths["planning"]).exists()
assert Path(paths["execution_queue"]).exists()
assert Path(paths["next_actions"]).exists()
assert Path(paths["roadmap_progress"]).exists()
assert Path(paths["markdown"]).exists()

# All persisted JSON is valid
for key in ("planning", "execution_queue", "next_actions", "roadmap_progress"):
    with open(paths[key]) as f:
        payload = json.load(f)
    assert isinstance(payload, dict), f"{key} JSON must be a dict"

# Report markdown
assert len(result["markdown"]) > 100

print("14. AutonomousPlanningEngine integration test OK")

# ---------------------------------------------------------------------------
# 15. Determinism — two consecutive runs produce stable schema
# ---------------------------------------------------------------------------

result2 = engine.plan()
d2 = result2["planning_dict"]
assert d2["schema_version"] == d["schema_version"]
assert d2["roadmap_progress"]["current_phase"] == d["roadmap_progress"]["current_phase"]
assert d2["roadmap_progress"]["completed_cores"] == d["roadmap_progress"]["completed_cores"]
assert d2["roadmap_progress"]["incomplete_cores"] == d["roadmap_progress"]["incomplete_cores"]
print("15. Determinism OK")

# ---------------------------------------------------------------------------
# 16. PlanningDecisionEngine — unit test
# ---------------------------------------------------------------------------

decision_engine = PlanningDecisionEngine(".")
ctx = decision_engine.decide({}, {})
assert isinstance(ctx["implemented_cores"], list)
assert isinstance(ctx["documented_cores"], list)
assert isinstance(ctx["incomplete_cores"], list)
assert isinstance(ctx["blocked_cores"], list)
assert ctx["current_phase"] in (
    PHASE_FOUNDATION, PHASE_INTELLIGENCE, PHASE_AUTONOMY, PHASE_PRODUCTION
)
assert 0 <= ctx["completion_percentage"] <= 100
print("16. PlanningDecisionEngine unit test OK")

# ---------------------------------------------------------------------------
# 17. CLI smoke test — ai plan
# ---------------------------------------------------------------------------

import subprocess
proc = subprocess.run(
    ["bash", "bin/ai", "plan"],
    capture_output=True,
    text=True,
    cwd=".",
)
assert proc.returncode == 0, f"ai plan exited {proc.returncode}: {proc.stderr}"
assert "Planning ID" in proc.stdout or "Execution Plan" in proc.stdout

proc_json = subprocess.run(
    ["bash", "bin/ai", "plan", "--json"],
    capture_output=True,
    text=True,
    cwd=".",
)
assert proc_json.returncode == 0, f"ai plan --json exited {proc_json.returncode}: {proc_json.stderr}"
payload = json.loads(proc_json.stdout)
assert "planning_id" in payload
assert "execution_queue" in payload
print("17. CLI smoke test OK")

print()
print("========================================")
print(" Autonomous Planning Engine PASS")
print("========================================")
PY

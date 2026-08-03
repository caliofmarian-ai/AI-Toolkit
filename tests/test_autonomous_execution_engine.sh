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

from python.autonomous_execution_engine import (
    AutonomousExecutionEngine,
    ExecutionCoordinator,
    ExecutionQueue,
    ExecutionScheduler,
    ArtifactManager,
    ExecutionEvidenceCollector,
    ExecutionSnapshot,
    ExecutionLogger,
    ExecutionReporter,
    ExecutionPersistence,
    ExecutionPolicy,
    ExecutionPermissions,
    ExecutionApproval,
    ExecutionValidator,
    ExecutionRollbackPlanner,
    ExecutionReportGenerator,
    EXECUTION_VERSION,
    EXECUTION_MODES,
    MODE_READ_ONLY,
    MODE_PLAN_ONLY,
    MODE_VALIDATION_ONLY,
    MODE_SIMULATION,
    MODE_DRY_RUN,
    MODE_OWNER_APPROVED,
    MODE_FULL_ACCEPTANCE,
    APPROVAL_UNKNOWN,
    APPROVAL_WAITING_OWNER,
    APPROVAL_APPROVED,
    APPROVAL_DENIED,
    APPROVAL_REVOKED,
    APPROVAL_EXPIRED,
    APPROVAL_STATES,
    VALIDATION_PASS,
    VALIDATION_WARNING,
    VALIDATION_FAIL,
    VALIDATION_SKIPPED,
    PIPELINE_STAGES,
    ExecutionContext,
    ExecutionStageResult,
    ValidationResult,
    ExecutionMetrics,
    ExecutionResult,
    ExecutionHistoryEntry,
    ExecutionHistory,
)

print("1. Imports OK")

# ---------------------------------------------------------------------------
# 2. Model constants
# ---------------------------------------------------------------------------

assert EXECUTION_VERSION == "1.0.0"
assert MODE_READ_ONLY in EXECUTION_MODES
assert MODE_FULL_ACCEPTANCE in EXECUTION_MODES
assert APPROVAL_APPROVED in APPROVAL_STATES
assert APPROVAL_DENIED in APPROVAL_STATES
assert len(PIPELINE_STAGES) == 15
print("2. Constants OK")

# ---------------------------------------------------------------------------
# 3. ExecutionPolicy — safe modes
# ---------------------------------------------------------------------------

for mode in (MODE_READ_ONLY, MODE_PLAN_ONLY, MODE_VALIDATION_ONLY, MODE_SIMULATION, MODE_DRY_RUN):
    policy = ExecutionPolicy(mode=mode)
    assert policy.is_safe_mode(), f"{mode} should be a safe mode"
    assert not policy.requires_approval(), f"{mode} should not require approval"
    assert not policy.permits_operation("force_push"), f"{mode} should deny force_push"

for mode in (MODE_OWNER_APPROVED, MODE_FULL_ACCEPTANCE):
    policy = ExecutionPolicy(mode=mode)
    assert not policy.is_safe_mode(), f"{mode} should not be safe"
    assert policy.requires_approval(), f"{mode} should require approval"
    assert policy.permits_operation("force_push"), f"{mode} should permit force_push"

assert ExecutionPolicy(mode="UNKNOWN_MODE").mode == MODE_READ_ONLY
print("3. ExecutionPolicy OK")

# ---------------------------------------------------------------------------
# 4. ExecutionPermissions
# ---------------------------------------------------------------------------

permissions = ExecutionPermissions()

# Safe mode — always passes
safe_result = permissions.check(ExecutionPolicy(MODE_READ_ONLY), APPROVAL_UNKNOWN)
assert safe_result.status == VALIDATION_PASS

# Owner approved mode + approved state — passes
approved_result = permissions.check(ExecutionPolicy(MODE_OWNER_APPROVED), APPROVAL_APPROVED)
assert approved_result.status == VALIDATION_PASS

# Owner approved mode + waiting state — fails
denied_result = permissions.check(ExecutionPolicy(MODE_OWNER_APPROVED), APPROVAL_WAITING_OWNER)
assert denied_result.status == VALIDATION_FAIL
assert len(denied_result.findings) > 0
print("4. ExecutionPermissions OK")

# ---------------------------------------------------------------------------
# 5. ExecutionApproval
# ---------------------------------------------------------------------------

approval_resolver = ExecutionApproval()

# Safe modes always return APPROVED
for mode in (MODE_READ_ONLY, MODE_SIMULATION, MODE_DRY_RUN):
    result = approval_resolver.resolve({}, {}, mode)
    assert result == APPROVAL_APPROVED, f"Expected APPROVED for {mode}, got {result}"

# State override
result = approval_resolver.resolve({"approval_state": "APPROVED"}, {}, MODE_OWNER_APPROVED)
assert result == APPROVAL_APPROVED

result = approval_resolver.resolve({"approval_state": "DENIED"}, {}, MODE_OWNER_APPROVED)
assert result == APPROVAL_DENIED
print("5. ExecutionApproval OK")

# ---------------------------------------------------------------------------
# 6. ExecutionEvidenceCollector
# ---------------------------------------------------------------------------

collector = ExecutionEvidenceCollector()
collector.record("CORE-013", "context", {"branch": "main"})
collector.record("CORE-009", "state", {"issue": "ISS-001"})
evidence = collector.collect()
assert evidence["evidence_count"] == 2
assert len(evidence["items"]) == 2

collector.reset()
assert collector.collect()["evidence_count"] == 0
print("6. ExecutionEvidenceCollector OK")

# ---------------------------------------------------------------------------
# 7. ExecutionSnapshot
# ---------------------------------------------------------------------------

snap = ExecutionSnapshot.capture(
    execution_id="EXEC-001",
    context={"mode": "READ_ONLY"},
    planning_queue={"entries": []},
    development_state={"issue": "ISS-001"},
    briefing={"briefing_id": "BRF-001"},
    live_context={"branch": "main"},
    schema_version=EXECUTION_VERSION,
)
assert snap["snapshot_id"].startswith("SNAP-")
assert snap["execution_id"] == "EXEC-001"
assert snap["schema_version"] == EXECUTION_VERSION
print("7. ExecutionSnapshot OK")

# ---------------------------------------------------------------------------
# 8. ExecutionLogger
# ---------------------------------------------------------------------------

logger = ExecutionLogger()
logger.info("test_stage", "Test message", {"key": "value"})
logger.warning("test_stage", "Warning message")
logger.error("test_stage", "Error message")
entries = logger.entries()
assert len(entries) == 3
assert entries[0]["level"] == "INFO"
assert entries[1]["level"] == "WARNING"
assert entries[2]["level"] == "ERROR"

log_dict = logger.to_dict()
assert log_dict["entry_count"] == 3
print("8. ExecutionLogger OK")

# ---------------------------------------------------------------------------
# 9. ExecutionScheduler
# ---------------------------------------------------------------------------

scheduler = ExecutionScheduler()

# No entries
assert scheduler.next_executable({}, {}) is None
assert scheduler.next_executable({"entries": []}, {}) is None

# Blocked entries only
result = scheduler.next_executable(
    {"entries": [{"entry_id": "X", "blocked_by": ["Y"], "priority": "high"}]},
    {},
)
assert result is None

# Priority ordering
queue = {
    "entries": [
        {"entry_id": "LOW", "blocked_by": [], "priority": "low"},
        {"entry_id": "HIGH", "blocked_by": [], "priority": "high"},
        {"entry_id": "CRIT", "blocked_by": [], "priority": "critical"},
    ]
}
next_entry = scheduler.next_executable(queue, {})
assert next_entry["entry_id"] == "CRIT"
print("9. ExecutionScheduler OK")

# ---------------------------------------------------------------------------
# 10. ExecutionRollbackPlanner
# ---------------------------------------------------------------------------

planner = ExecutionRollbackPlanner()
plan = planner.plan(
    execution_id="EXEC-001",
    context={"branch": "main", "commit": "abc123", "batch": "BATCH-001"},
    stage_results=[
        {"stage": "execute_approved_step", "status": "PASS"},
        {"stage": "update_state", "status": "PASS"},
        {"stage": "load_context", "status": "PASS"},
    ],
)
assert plan["execution_id"] == "EXEC-001"
assert plan["owner_approval_required"] is True
assert plan["step_count"] >= 2
print("10. ExecutionRollbackPlanner OK")

# ---------------------------------------------------------------------------
# 11. ExecutionReportGenerator
# ---------------------------------------------------------------------------

from python.autonomous_execution_engine.models import (
    ExecutionResult, ExecutionContext, ExecutionMetrics
)

ctx = ExecutionContext(
    execution_id="EXEC-001",
    repository="/tmp/repo",
    workspace="/tmp",
    branch="main",
    commit="abc",
    issue="ISS-001",
    batch="BATCH-001",
    milestone="MS-001",
    core="CORE-015",
    roadmap="ROADMAP-001",
    planning_id="PLAN-001",
    state_id="STATE-001",
    synchronization_id="SYNC-001",
    briefing_id="BRF-001",
    owner="owner",
    timestamp="2026-01-01T00:00:00+00:00",
    environment="/tmp/repo",
    policy="READ_ONLY",
    approval="APPROVED",
    confidence=0.75,
    mode="READ_ONLY",
    schema_version=EXECUTION_VERSION,
)
metrics = ExecutionMetrics(
    execution_id="EXEC-001",
    generated_at="2026-01-01T00:00:00+00:00",
    total_duration_ms=500.0,
    stage_durations={},
    validation_scores={},
    evidence_count=5,
    artifact_count=3,
    error_count=0,
    warning_count=1,
    confidence=0.75,
    schema_version=EXECUTION_VERSION,
)
exec_result = ExecutionResult(
    execution_id="EXEC-001",
    generated_at="2026-01-01T00:00:00+00:00",
    repository="/tmp/repo",
    mode="READ_ONLY",
    approval="APPROVED",
    status="COMPLETED",
    schema_version=EXECUTION_VERSION,
    context=ctx,
    metrics=metrics,
    summary="Test summary",
)

gen = ExecutionReportGenerator()
markdown = gen.render(exec_result)
assert "# AI CTO Execution Report" in markdown
assert "EXEC-001" in markdown
assert "Confidence" in markdown
assert "Pipeline Stages" in markdown
print("11. ExecutionReportGenerator OK")

# ---------------------------------------------------------------------------
# 12. ExecutionPersistence — atomic writes
# ---------------------------------------------------------------------------

with tempfile.TemporaryDirectory() as tmpdir:
    persistence = ExecutionPersistence(tmpdir)
    assert not persistence.exists()

    paths = persistence.save(
        exec_result,
        log_entries=[{"level": "INFO", "message": "test"}],
        report_dict={"execution_id": "EXEC-001"},
        markdown=markdown,
    )

    assert persistence.exists()
    assert Path(paths["execution"]).exists()
    assert Path(paths["execution_context"]).exists()
    assert Path(paths["execution_metrics"]).exists()
    assert Path(paths["execution_log"]).exists()
    assert Path(paths["markdown"]).exists()

    loaded = persistence.load_execution()
    assert loaded["execution_id"] == "EXEC-001"
    assert loaded["schema_version"] == EXECUTION_VERSION

    history = persistence.load_history()
    assert history["entry_count"] == 1

    # Second save appends to history
    persistence.save(exec_result, report_dict={}, markdown="")
    history2 = persistence.load_history()
    assert history2["entry_count"] == 2

print("12. ExecutionPersistence OK")

# ---------------------------------------------------------------------------
# 13. ExecutionValidator compatibility regression checks
# ---------------------------------------------------------------------------

validator = ExecutionValidator(".")
repo_v = validator.validate_repository()
assert repo_v.status != VALIDATION_SKIPPED, repo_v.findings

canon_v = validator.validate_canonical()
assert canon_v.status != VALIDATION_SKIPPED, canon_v.findings

reg_v = validator.validate_regression(
    {
        "planning_queue": {
            "queue_id": "PLAN-001",
            "schema_version": "1.0.0",
            "entries": [],
        }
    }
)
assert reg_v.status == VALIDATION_PASS, reg_v.findings
print("13. ExecutionValidator compatibility OK")

# ---------------------------------------------------------------------------
# 14. AutonomousExecutionEngine — integration test against AI Toolkit
# ---------------------------------------------------------------------------

engine = AutonomousExecutionEngine(
    repository=".",
    mode=MODE_READ_ONLY,
    persist=True,
    refresh_integrations=False,
)
result = engine.execute()

assert "execution_result" in result
assert "execution_dict" in result
assert "markdown" in result
assert "paths" in result

d = result["execution_dict"]
assert d["schema_version"] == EXECUTION_VERSION
assert d["execution_id"].startswith("EXEC-")
assert d["mode"] == MODE_READ_ONLY
assert d["approval"] in APPROVAL_STATES
assert len(d["stage_results"]) == len(PIPELINE_STAGES)
assert isinstance(d["validation_results"], list)
assert len(d["validation_results"]) >= 5

paths = result["paths"]
assert Path(paths["execution"]).exists()
assert Path(paths["execution_context"]).exists()
assert Path(paths["execution_metrics"]).exists()
assert Path(paths["execution_log"]).exists()
assert Path(paths["execution_history"]).exists()
assert Path(paths["markdown"]).exists()

# All JSON is valid
for key in ("execution", "execution_context", "execution_metrics"):
    with open(paths[key]) as f:
        payload = json.load(f)
    assert isinstance(payload, dict), f"{key} must be a dict"

assert len(result["markdown"]) > 100
print("14. AutonomousExecutionEngine integration test OK")

# ---------------------------------------------------------------------------
# 15. Simulation mode
# ---------------------------------------------------------------------------

sim_engine = AutonomousExecutionEngine(
    repository=".",
    mode=MODE_SIMULATION,
    persist=False,
)
sim_result = sim_engine.execute()
assert sim_result["execution_dict"]["mode"] == MODE_SIMULATION
assert sim_result["execution_dict"]["approval"] == APPROVAL_APPROVED  # safe mode
print("15. SIMULATION mode OK")

# ---------------------------------------------------------------------------
# 16. Determinism — two consecutive runs produce stable schema
# ---------------------------------------------------------------------------

result2 = engine.execute()
d2 = result2["execution_dict"]
assert d2["schema_version"] == d["schema_version"]
assert d2["mode"] == d["mode"]
assert len(d2["stage_results"]) == len(d["stage_results"])
print("16. Determinism OK")

# ---------------------------------------------------------------------------
# 17. CLI smoke test — ai execute
# ---------------------------------------------------------------------------

import subprocess

proc = subprocess.run(
    ["bash", "bin/ai", "execute"],
    capture_output=True,
    text=True,
    cwd=".",
)
assert proc.returncode == 0, f"ai execute exited {proc.returncode}: {proc.stderr}"
assert "Execution ID" in proc.stdout

proc_json = subprocess.run(
    ["bash", "bin/ai", "execute", "--json"],
    capture_output=True,
    text=True,
    cwd=".",
)
assert proc_json.returncode == 0, f"ai execute --json exited {proc_json.returncode}: {proc_json.stderr}"
payload = json.loads(proc_json.stdout)
assert "execution_id" in payload
assert "schema_version" in payload
print("17. CLI smoke test OK")

# ---------------------------------------------------------------------------
# 18. CLI simulate and dry-run modes
# ---------------------------------------------------------------------------

for flag in ("--simulate", "--dry-run", "--validate"):
    p = subprocess.run(
        ["bash", "bin/ai", "execute", flag],
        capture_output=True,
        text=True,
        cwd=".",
    )
    assert p.returncode == 0, f"ai execute {flag} failed: {p.stderr}"
print("18. CLI flags OK")

print()
print("========================================")
print(" Autonomous Execution Engine PASS")
print("========================================")
PY

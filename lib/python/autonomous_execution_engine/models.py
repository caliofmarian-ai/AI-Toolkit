"""
Autonomous Execution Engine — Canonical Models
CORE-015A

All execution artifacts are deterministic, serialisable, and versioned.
No execution decisions are hardcoded — every field is derived from
existing CORE engine intelligence.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

EXECUTION_VERSION = "1.0.0"

# ---------------------------------------------------------------------------
# Execution Mode constants
# ---------------------------------------------------------------------------

MODE_READ_ONLY = "READ_ONLY"
MODE_PLAN_ONLY = "PLAN_ONLY"
MODE_VALIDATION_ONLY = "VALIDATION_ONLY"
MODE_SIMULATION = "SIMULATION"
MODE_DRY_RUN = "DRY_RUN"
MODE_OWNER_APPROVED = "OWNER_APPROVED"
MODE_FULL_ACCEPTANCE = "FULL_ACCEPTANCE"

EXECUTION_MODES = (
    MODE_READ_ONLY,
    MODE_PLAN_ONLY,
    MODE_VALIDATION_ONLY,
    MODE_SIMULATION,
    MODE_DRY_RUN,
    MODE_OWNER_APPROVED,
    MODE_FULL_ACCEPTANCE,
)

# ---------------------------------------------------------------------------
# Approval State constants
# ---------------------------------------------------------------------------

APPROVAL_UNKNOWN = "UNKNOWN"
APPROVAL_WAITING_OWNER = "WAITING_OWNER"
APPROVAL_APPROVED = "APPROVED"
APPROVAL_DENIED = "DENIED"
APPROVAL_REVOKED = "REVOKED"
APPROVAL_EXPIRED = "EXPIRED"

APPROVAL_STATES = (
    APPROVAL_UNKNOWN,
    APPROVAL_WAITING_OWNER,
    APPROVAL_APPROVED,
    APPROVAL_DENIED,
    APPROVAL_REVOKED,
    APPROVAL_EXPIRED,
)

# ---------------------------------------------------------------------------
# Validation Result constants
# ---------------------------------------------------------------------------

VALIDATION_PASS = "PASS"
VALIDATION_WARNING = "WARNING"
VALIDATION_FAIL = "FAIL"
VALIDATION_SKIPPED = "SKIPPED"

# ---------------------------------------------------------------------------
# Pipeline Stage constants
# ---------------------------------------------------------------------------

STAGE_LOAD_CONTEXT = "load_context"
STAGE_LOAD_STATE = "load_development_state"
STAGE_LOAD_BRIEFING = "load_executive_briefing"
STAGE_LOAD_QUEUE = "load_planning_queue"
STAGE_VALIDATE_DEPENDENCIES = "validate_dependencies"
STAGE_VALIDATE_POLICIES = "validate_policies"
STAGE_VALIDATE_APPROVALS = "validate_approvals"
STAGE_PREPARE_CONTEXT = "prepare_execution_context"
STAGE_EXECUTE_STEP = "execute_approved_step"
STAGE_COLLECT_EVIDENCE = "collect_evidence"
STAGE_RUN_VALIDATION = "run_validation"
STAGE_UPDATE_STATE = "update_state"
STAGE_GENERATE_REPORTS = "generate_reports"
STAGE_PERSIST_ARTIFACTS = "persist_artifacts"
STAGE_RETURN_SUMMARY = "return_deterministic_summary"

PIPELINE_STAGES = (
    STAGE_LOAD_CONTEXT,
    STAGE_LOAD_STATE,
    STAGE_LOAD_BRIEFING,
    STAGE_LOAD_QUEUE,
    STAGE_VALIDATE_DEPENDENCIES,
    STAGE_VALIDATE_POLICIES,
    STAGE_VALIDATE_APPROVALS,
    STAGE_PREPARE_CONTEXT,
    STAGE_EXECUTE_STEP,
    STAGE_COLLECT_EVIDENCE,
    STAGE_RUN_VALIDATION,
    STAGE_UPDATE_STATE,
    STAGE_GENERATE_REPORTS,
    STAGE_PERSIST_ARTIFACTS,
    STAGE_RETURN_SUMMARY,
)


# ---------------------------------------------------------------------------
# ExecutionContext
# ---------------------------------------------------------------------------

@dataclass
class ExecutionContext:
    """Records every dimension of a single execution run."""

    execution_id: str
    repository: str
    workspace: str
    branch: str
    commit: str
    issue: str
    batch: str
    milestone: str
    core: str
    roadmap: str
    planning_id: str
    state_id: str
    synchronization_id: str
    briefing_id: str
    owner: str
    timestamp: str
    environment: str
    policy: str
    approval: str
    confidence: float
    mode: str
    schema_version: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "execution_id": self.execution_id,
            "repository": self.repository,
            "workspace": self.workspace,
            "branch": self.branch,
            "commit": self.commit,
            "issue": self.issue,
            "batch": self.batch,
            "milestone": self.milestone,
            "core": self.core,
            "roadmap": self.roadmap,
            "planning_id": self.planning_id,
            "state_id": self.state_id,
            "synchronization_id": self.synchronization_id,
            "briefing_id": self.briefing_id,
            "owner": self.owner,
            "timestamp": self.timestamp,
            "environment": self.environment,
            "policy": self.policy,
            "approval": self.approval,
            "confidence": self.confidence,
            "mode": self.mode,
            "schema_version": self.schema_version,
        }


# ---------------------------------------------------------------------------
# ExecutionStageResult
# ---------------------------------------------------------------------------

@dataclass
class ExecutionStageResult:
    """Outcome of a single pipeline stage."""

    stage: str
    status: str
    duration_ms: float
    evidence: Dict[str, Any]
    errors: List[str]
    warnings: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "stage": self.stage,
            "status": self.status,
            "duration_ms": self.duration_ms,
            "evidence": self.evidence,
            "errors": self.errors,
            "warnings": self.warnings,
        }


# ---------------------------------------------------------------------------
# ValidationResult
# ---------------------------------------------------------------------------

@dataclass
class ValidationResult:
    """Result of a single validation check."""

    validator: str
    status: str
    score: float
    findings: List[str]
    evidence: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "validator": self.validator,
            "status": self.status,
            "score": self.score,
            "findings": self.findings,
            "evidence": self.evidence,
        }


# ---------------------------------------------------------------------------
# ExecutionMetrics
# ---------------------------------------------------------------------------

@dataclass
class ExecutionMetrics:
    """Performance and quality metrics for a single execution."""

    execution_id: str
    generated_at: str
    total_duration_ms: float
    stage_durations: Dict[str, float]
    validation_scores: Dict[str, float]
    evidence_count: int
    artifact_count: int
    error_count: int
    warning_count: int
    confidence: float
    schema_version: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "execution_id": self.execution_id,
            "generated_at": self.generated_at,
            "total_duration_ms": self.total_duration_ms,
            "stage_durations": self.stage_durations,
            "validation_scores": self.validation_scores,
            "evidence_count": self.evidence_count,
            "artifact_count": self.artifact_count,
            "error_count": self.error_count,
            "warning_count": self.warning_count,
            "confidence": self.confidence,
            "schema_version": self.schema_version,
        }


# ---------------------------------------------------------------------------
# ExecutionSnapshot
# ---------------------------------------------------------------------------

@dataclass
class ExecutionSnapshot:
    """Frozen snapshot of execution state for reproducibility."""

    snapshot_id: str
    execution_id: str
    captured_at: str
    context: Dict[str, Any]
    planning_queue: Dict[str, Any]
    development_state: Dict[str, Any]
    briefing: Dict[str, Any]
    live_context: Dict[str, Any]
    schema_version: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "snapshot_id": self.snapshot_id,
            "execution_id": self.execution_id,
            "captured_at": self.captured_at,
            "context": self.context,
            "planning_queue": self.planning_queue,
            "development_state": self.development_state,
            "briefing": self.briefing,
            "live_context": self.live_context,
            "schema_version": self.schema_version,
        }


# ---------------------------------------------------------------------------
# ExecutionResult
# ---------------------------------------------------------------------------

@dataclass
class ExecutionResult:
    """Deterministic summary of a complete execution run."""

    execution_id: str
    generated_at: str
    repository: str
    mode: str
    approval: str
    status: str
    schema_version: str
    context: Optional[ExecutionContext] = None
    stage_results: List[ExecutionStageResult] = field(default_factory=list)
    validation_results: List[ValidationResult] = field(default_factory=list)
    metrics: Optional[ExecutionMetrics] = None
    snapshot: Optional[ExecutionSnapshot] = None
    evidence: Dict[str, Any] = field(default_factory=dict)
    artifacts: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    next_actions: List[str] = field(default_factory=list)
    summary: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "execution_id": self.execution_id,
            "generated_at": self.generated_at,
            "repository": self.repository,
            "mode": self.mode,
            "approval": self.approval,
            "status": self.status,
            "schema_version": self.schema_version,
            "context": self.context.to_dict() if self.context else {},
            "stage_results": [s.to_dict() for s in self.stage_results],
            "validation_results": [v.to_dict() for v in self.validation_results],
            "metrics": self.metrics.to_dict() if self.metrics else {},
            "snapshot": self.snapshot.to_dict() if self.snapshot else {},
            "evidence": self.evidence,
            "artifacts": self.artifacts,
            "errors": self.errors,
            "warnings": self.warnings,
            "next_actions": self.next_actions,
            "summary": self.summary,
        }


# ---------------------------------------------------------------------------
# ExecutionHistoryEntry
# ---------------------------------------------------------------------------

@dataclass
class ExecutionHistoryEntry:
    """A single row in the execution history log."""

    execution_id: str
    timestamp: str
    repository: str
    mode: str
    approval: str
    status: str
    duration_ms: float
    confidence: float
    summary: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "execution_id": self.execution_id,
            "timestamp": self.timestamp,
            "repository": self.repository,
            "mode": self.mode,
            "approval": self.approval,
            "status": self.status,
            "duration_ms": self.duration_ms,
            "confidence": self.confidence,
            "summary": self.summary,
        }


# ---------------------------------------------------------------------------
# ExecutionHistory
# ---------------------------------------------------------------------------

@dataclass
class ExecutionHistory:
    """Complete ordered history of execution runs for one repository."""

    repository: str
    generated_at: str
    schema_version: str
    entries: List[ExecutionHistoryEntry] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "repository": self.repository,
            "generated_at": self.generated_at,
            "schema_version": self.schema_version,
            "entry_count": len(self.entries),
            "entries": [e.to_dict() for e in self.entries],
        }

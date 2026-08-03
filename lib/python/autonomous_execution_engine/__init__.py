"""
Autonomous Execution Engine — CORE-015

The AI CTO execution layer.

Transforms approved planning into controlled, observable and reproducible
execution without duplicating any existing CORE intelligence.

Public API::

    from python.autonomous_execution_engine import AutonomousExecutionEngine

    engine = AutonomousExecutionEngine(repository="/path/to/repo")
    result = engine.execute()
"""

from .engine import (
    ArtifactManager,
    AutonomousExecutionEngine,
    ExecutionCoordinator,
    ExecutionQueue,
    ExecutionScheduler,
)
from .evidence import ExecutionEvidenceCollector, ExecutionSnapshot
from .logger import ExecutionLogger, ExecutionReporter
from .models import (
    APPROVAL_APPROVED,
    APPROVAL_DENIED,
    APPROVAL_EXPIRED,
    APPROVAL_REVOKED,
    APPROVAL_STATES,
    APPROVAL_UNKNOWN,
    APPROVAL_WAITING_OWNER,
    EXECUTION_VERSION,
    EXECUTION_MODES,
    MODE_DRY_RUN,
    MODE_FULL_ACCEPTANCE,
    MODE_OWNER_APPROVED,
    MODE_PLAN_ONLY,
    MODE_READ_ONLY,
    MODE_SIMULATION,
    MODE_VALIDATION_ONLY,
    PIPELINE_STAGES,
    STAGE_COLLECT_EVIDENCE,
    STAGE_EXECUTE_STEP,
    STAGE_GENERATE_REPORTS,
    STAGE_LOAD_BRIEFING,
    STAGE_LOAD_CONTEXT,
    STAGE_LOAD_QUEUE,
    STAGE_LOAD_STATE,
    STAGE_PERSIST_ARTIFACTS,
    STAGE_PREPARE_CONTEXT,
    STAGE_RETURN_SUMMARY,
    STAGE_RUN_VALIDATION,
    STAGE_UPDATE_STATE,
    STAGE_VALIDATE_APPROVALS,
    STAGE_VALIDATE_DEPENDENCIES,
    STAGE_VALIDATE_POLICIES,
    VALIDATION_FAIL,
    VALIDATION_PASS,
    VALIDATION_SKIPPED,
    VALIDATION_WARNING,
    ExecutionContext,
    ExecutionHistory,
    ExecutionHistoryEntry,
    ExecutionMetrics,
    ExecutionResult,
    ExecutionSnapshot as ExecutionSnapshotModel,
    ExecutionStageResult,
    ValidationResult,
)
from .persistence import ExecutionPersistence
from .policy import ExecutionApproval, ExecutionPermissions, ExecutionPolicy
from .report import ExecutionReportGenerator
from .rollback import ExecutionRollbackPlanner
from .validator import ExecutionValidator

__all__ = [
    # Main engine
    "AutonomousExecutionEngine",
    # Sub-engines
    "ExecutionCoordinator",
    "ExecutionQueue",
    "ExecutionScheduler",
    "ArtifactManager",
    "ExecutionEvidenceCollector",
    "ExecutionSnapshot",
    "ExecutionLogger",
    "ExecutionReporter",
    "ExecutionPersistence",
    "ExecutionPolicy",
    "ExecutionPermissions",
    "ExecutionApproval",
    "ExecutionValidator",
    "ExecutionRollbackPlanner",
    "ExecutionReportGenerator",
    # Mode constants
    "EXECUTION_VERSION",
    "EXECUTION_MODES",
    "MODE_READ_ONLY",
    "MODE_PLAN_ONLY",
    "MODE_VALIDATION_ONLY",
    "MODE_SIMULATION",
    "MODE_DRY_RUN",
    "MODE_OWNER_APPROVED",
    "MODE_FULL_ACCEPTANCE",
    # Approval constants
    "APPROVAL_UNKNOWN",
    "APPROVAL_WAITING_OWNER",
    "APPROVAL_APPROVED",
    "APPROVAL_DENIED",
    "APPROVAL_REVOKED",
    "APPROVAL_EXPIRED",
    "APPROVAL_STATES",
    # Validation constants
    "VALIDATION_PASS",
    "VALIDATION_WARNING",
    "VALIDATION_FAIL",
    "VALIDATION_SKIPPED",
    # Pipeline stage constants
    "PIPELINE_STAGES",
    "STAGE_LOAD_CONTEXT",
    "STAGE_LOAD_STATE",
    "STAGE_LOAD_BRIEFING",
    "STAGE_LOAD_QUEUE",
    "STAGE_VALIDATE_DEPENDENCIES",
    "STAGE_VALIDATE_POLICIES",
    "STAGE_VALIDATE_APPROVALS",
    "STAGE_PREPARE_CONTEXT",
    "STAGE_EXECUTE_STEP",
    "STAGE_COLLECT_EVIDENCE",
    "STAGE_RUN_VALIDATION",
    "STAGE_UPDATE_STATE",
    "STAGE_GENERATE_REPORTS",
    "STAGE_PERSIST_ARTIFACTS",
    "STAGE_RETURN_SUMMARY",
    # Models
    "ExecutionContext",
    "ExecutionStageResult",
    "ValidationResult",
    "ExecutionMetrics",
    "ExecutionSnapshotModel",
    "ExecutionResult",
    "ExecutionHistoryEntry",
    "ExecutionHistory",
]

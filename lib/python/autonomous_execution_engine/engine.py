"""
Autonomous Execution Engine — Main Orchestrator
CORE-015

Implements the AI CTO execution layer.

Responsibility: transforming approved planning into controlled, observable
and reproducible execution.

Consumes (never re-implements):
  CORE-007  Canonical Intelligence
  CORE-008A AI CTO Scanner
  CORE-008B Semantic Repository Intelligence
  CORE-008C Executable Repository Intelligence
  CORE-009  Development State Engine
  CORE-010  Executive Briefing Engine
  CORE-012  Workspace Orchestrator
  CORE-013  Context Synchronization Engine
  CORE-014  Autonomous Planning Engine

Produces:
  .ai/execution/execution.json
  .ai/execution/execution_context.json
  .ai/execution/execution_queue.json
  .ai/execution/execution_history.json
  .ai/execution/execution_metrics.json
  .ai/execution/execution_results.json
  .ai/execution/execution_snapshot.json
  .ai/execution/execution_evidence.json
  .ai/execution/execution_log.json
  .ai/execution/execution_report.json
  .ai/execution/AI_CTO_EXECUTION_REPORT.md
"""

import hashlib
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Type

from .evidence import ExecutionEvidenceCollector, ExecutionSnapshot
from .logger import ExecutionLogger, ExecutionReporter
from .models import (
    APPROVAL_APPROVED,
    EXECUTION_VERSION,
    MODE_READ_ONLY,
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
    ExecutionHistoryEntry,
    ExecutionMetrics,
    ExecutionResult,
    ExecutionStageResult,
    ValidationResult,
)
from .persistence import ExecutionPersistence
from .policy import ExecutionApproval, ExecutionPermissions, ExecutionPolicy
from .report import ExecutionReportGenerator
from .rollback import ExecutionRollbackPlanner
from .validator import ExecutionValidator


def _utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


def _execution_id(repository: str, generated_at: str) -> str:
    digest = hashlib.sha1(
        f"{repository}{generated_at}".encode("utf-8")
    ).hexdigest()[:8].upper()
    return f"EXEC-{digest}"


def _ms(start: float) -> float:
    return round((time.monotonic() - start) * 1000, 3)


def _stage_result(
    stage: str,
    status: str,
    duration_ms: float,
    evidence: Dict[str, Any] = None,
    errors: List[str] = None,
    warnings: List[str] = None,
) -> ExecutionStageResult:
    return ExecutionStageResult(
        stage=stage,
        status=status,
        duration_ms=duration_ms,
        evidence=evidence or {},
        errors=errors or [],
        warnings=warnings or [],
    )


class ExecutionScheduler:
    """
    CORE-015 — Execution Scheduler.

    Determines whether a planning queue entry is ready for execution
    by checking dependencies and priority ordering.
    """

    def next_executable(
        self, queue: Dict[str, Any], development_state: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Return the first unblocked, highest-priority queue entry."""
        entries = queue.get("entries", [])
        unblocked = [e for e in entries if not e.get("blocked_by")]
        if not unblocked:
            return None
        # Sort by priority score: critical > high > medium > low
        priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3, "blocked": 4}
        unblocked.sort(key=lambda e: priority_order.get(e.get("priority", "low"), 99))
        return unblocked[0] if unblocked else None


class ExecutionQueue:
    """
    CORE-015 — Execution Queue.

    Wraps the planning queue with execution-specific helpers.
    """

    def __init__(self, queue_dict: Dict[str, Any]) -> None:
        self._queue = queue_dict

    def entry_count(self) -> int:
        return len(self._queue.get("entries", []))

    def to_dict(self) -> Dict[str, Any]:
        return dict(self._queue)


class ExecutionCoordinator:
    """
    CORE-015 — Execution Coordinator.

    Coordinates the full execution pipeline by delegating each stage
    to the appropriate sub-component.
    """

    def __init__(
        self,
        execution_engine: "AutonomousExecutionEngine",
    ) -> None:
        self._engine = execution_engine

    def coordinate(
        self,
        execution_id: str,
        context_data: Dict[str, Any],
        state_data: Dict[str, Any],
        briefing_data: Dict[str, Any],
        queue_data: Dict[str, Any],
        mode: str,
        approval: str,
        policy: ExecutionPolicy,
    ) -> Dict[str, Any]:
        """Run all pipeline stages and return the coordination result."""
        return self._engine._run_pipeline(
            execution_id=execution_id,
            context_data=context_data,
            state_data=state_data,
            briefing_data=briefing_data,
            queue_data=queue_data,
            mode=mode,
            approval=approval,
            policy=policy,
        )


class ArtifactManager:
    """
    CORE-015 — Execution Artifact Manager.

    Tracks all artifacts produced during execution.
    """

    def __init__(self) -> None:
        self._artifacts: List[str] = []

    def register(self, path: str) -> None:
        if path and path not in self._artifacts:
            self._artifacts.append(path)

    def all(self) -> List[str]:
        return list(self._artifacts)


class AutonomousExecutionEngine:
    """
    Autonomous Execution Engine — CORE-015.

    Primary interface for the AI CTO execution layer.

    Usage::

        engine = AutonomousExecutionEngine(repository="/path/to/repo")
        result = engine.execute()

    The returned dict contains:
      - execution_result   ExecutionResult dataclass
      - execution_dict     Fully serialisable dict
      - markdown           Rendered markdown string
      - paths              Dict mapping artifact name → file path
    """

    def __init__(
        self,
        repository: str = ".",
        workspace_root: Optional[str] = None,
        output_dir: Optional[str] = None,
        mode: str = MODE_READ_ONLY,
        persist: bool = True,
        refresh_integrations: bool = False,
    ) -> None:
        self.root = Path(repository).resolve()
        self.workspace_root = (
            Path(workspace_root).resolve()
            if workspace_root
            else self.root.parent
        )
        self.output_dir = Path(output_dir).resolve() if output_dir else self.root
        self.mode = mode if mode in (
            MODE_READ_ONLY, "PLAN_ONLY", "VALIDATION_ONLY",
            "SIMULATION", "DRY_RUN", "OWNER_APPROVED", "FULL_ACCEPTANCE"
        ) else MODE_READ_ONLY
        self.persist = persist
        self.refresh_integrations = refresh_integrations

        self._logger = ExecutionLogger()
        self._evidence = ExecutionEvidenceCollector()
        self._artifact_manager = ArtifactManager()
        self._validator = ExecutionValidator(repository=str(self.root))
        self._rollback_planner = ExecutionRollbackPlanner()
        self._report_generator = ExecutionReportGenerator()
        self._reporter = ExecutionReporter()

    def execute(self) -> Dict[str, Any]:
        """
        Run the full autonomous execution pipeline.

        Returns a fully serialisable dict with the execution result,
        rendered markdown, and file paths of persisted artifacts.
        """
        t_start = time.monotonic()
        generated_at = _utcnow()
        execution_id = _execution_id(str(self.root), generated_at)

        self._logger.info(STAGE_LOAD_CONTEXT, "Execution started", {"execution_id": execution_id})

        # Build policy and approval
        policy = ExecutionPolicy(mode=self.mode)
        stage_results: List[ExecutionStageResult] = []
        validation_results: List[ValidationResult] = []
        errors: List[str] = []
        warnings: List[str] = []

        # ------------------------------------------------------------------
        # STAGE: Load Context
        # ------------------------------------------------------------------
        t0 = time.monotonic()
        context_data = self._load_live_context()
        stage_results.append(
            _stage_result(STAGE_LOAD_CONTEXT, VALIDATION_PASS, _ms(t0),
                          evidence={"source": "CORE-013"})
        )
        self._evidence.record("CORE-013", "live_context", context_data)

        # ------------------------------------------------------------------
        # STAGE: Load Development State
        # ------------------------------------------------------------------
        t0 = time.monotonic()
        state_data = self._load_development_state()
        stage_results.append(
            _stage_result(STAGE_LOAD_STATE, VALIDATION_PASS, _ms(t0),
                          evidence={"source": "CORE-009"})
        )
        self._evidence.record("CORE-009", "development_state", state_data)

        # ------------------------------------------------------------------
        # STAGE: Load Executive Briefing
        # ------------------------------------------------------------------
        t0 = time.monotonic()
        briefing_data = self._load_briefing()
        stage_results.append(
            _stage_result(STAGE_LOAD_BRIEFING, VALIDATION_PASS, _ms(t0),
                          evidence={"source": "CORE-010"})
        )
        self._evidence.record("CORE-010", "briefing", briefing_data)

        # ------------------------------------------------------------------
        # STAGE: Load Planning Queue
        # ------------------------------------------------------------------
        t0 = time.monotonic()
        queue_data = self._load_planning_queue()
        stage_results.append(
            _stage_result(STAGE_LOAD_QUEUE, VALIDATION_PASS, _ms(t0),
                          evidence={"entry_count": len(queue_data.get("entries", [])),
                                    "source": "CORE-014"})
        )
        self._evidence.record("CORE-014", "planning_queue", queue_data)

        # ------------------------------------------------------------------
        # STAGE: Validate Dependencies
        # ------------------------------------------------------------------
        t0 = time.monotonic()
        dep_errors = self._check_dependencies(queue_data)
        if dep_errors:
            warnings.extend(dep_errors)
        stage_results.append(
            _stage_result(STAGE_VALIDATE_DEPENDENCIES,
                          VALIDATION_WARNING if dep_errors else VALIDATION_PASS,
                          _ms(t0), errors=dep_errors)
        )

        # ------------------------------------------------------------------
        # STAGE: Validate Policies
        # ------------------------------------------------------------------
        t0 = time.monotonic()
        stage_results.append(
            _stage_result(STAGE_VALIDATE_POLICIES, VALIDATION_PASS, _ms(t0),
                          evidence=policy.to_dict())
        )

        # ------------------------------------------------------------------
        # STAGE: Validate Approvals
        # ------------------------------------------------------------------
        t0 = time.monotonic()
        approval_resolver = ExecutionApproval()
        approval = approval_resolver.resolve(state_data, briefing_data, self.mode)
        permissions = ExecutionPermissions()
        perm_result = permissions.check(policy, approval)
        validation_results.append(perm_result)

        perm_status = VALIDATION_PASS if perm_result.status == VALIDATION_PASS else VALIDATION_FAIL
        stage_results.append(
            _stage_result(STAGE_VALIDATE_APPROVALS, perm_status, _ms(t0),
                          evidence={"approval": approval, "mode": self.mode},
                          errors=perm_result.findings if perm_result.status == VALIDATION_FAIL else [])
        )
        if perm_result.status == VALIDATION_FAIL:
            errors.extend(perm_result.findings)

        # ------------------------------------------------------------------
        # STAGE: Prepare Execution Context
        # ------------------------------------------------------------------
        t0 = time.monotonic()
        recurrence_evidence = self._prepare_recurrence_evidence_handoff(
            queue_data=queue_data,
            state_data=state_data,
            context_data=context_data,
        )

        exec_context = self._build_execution_context(
            execution_id=execution_id,
            generated_at=generated_at,
            context_data=context_data,
            state_data=state_data,
            briefing_data=briefing_data,
            queue_data=queue_data,
            approval=approval,
            policy=policy,
            recurrence_evidence=recurrence_evidence,
        )

        self._evidence.record(
            "ERROR_MEMORY",
            "pre_execution_recurrence_evidence",
            recurrence_evidence,
        )

        unresolved_count = recurrence_evidence.get(
            "unresolved_count",
            0,
        )

        stage_results.append(
            _stage_result(
                STAGE_PREPARE_CONTEXT,
                VALIDATION_WARNING
                if unresolved_count
                else VALIDATION_PASS,
                _ms(t0),
                evidence={
                    "recurrence_evidence_count":
                        recurrence_evidence.get("evidence_count", 0),
                    "unresolved_recurrence_count":
                        unresolved_count,
                    "execution_authority": False,
                },
                warnings=(
                    [
                        f"{unresolved_count} demonstrated recurrence "
                        "precedent(s) remain UNRESOLVED; evidence is "
                        "preserved for Human Authority."
                    ]
                    if unresolved_count
                    else []
                ),
            )
        )

        # ------------------------------------------------------------------
        # STAGE: Execute Approved Step
        # ------------------------------------------------------------------
        t0 = time.monotonic()
        step_result, step_warnings = self._execute_approved_step(
            policy=policy,
            approval=approval,
            queue_data=queue_data,
            state_data=state_data,
        )
        warnings.extend(step_warnings)
        stage_results.append(
            _stage_result(STAGE_EXECUTE_STEP, step_result, _ms(t0),
                          warnings=step_warnings)
        )

        # ------------------------------------------------------------------
        # STAGE: Collect Evidence
        # ------------------------------------------------------------------
        t0 = time.monotonic()
        evidence_dict = self._evidence.collect()
        stage_results.append(
            _stage_result(STAGE_COLLECT_EVIDENCE, VALIDATION_PASS, _ms(t0),
                          evidence={"evidence_count": evidence_dict.get("evidence_count", 0)})
        )

        # ------------------------------------------------------------------
        # STAGE: Run Validation
        # ------------------------------------------------------------------
        t0 = time.monotonic()
        snapshot_for_regression = ExecutionSnapshot.capture(
            execution_id=execution_id,
            context=exec_context.to_dict(),
            planning_queue=queue_data,
            development_state=state_data,
            briefing=briefing_data,
            live_context=context_data,
            schema_version=EXECUTION_VERSION,
        )

        repo_vr = self._validator.validate_repository()
        sem_vr = self._validator.validate_semantic()
        canon_vr = self._validator.validate_canonical()
        reg_vr = self._validator.validate_regression(snapshot_for_regression)
        acc_vr = self._validator.validate_acceptance(
            self.mode, [repo_vr, sem_vr, canon_vr, reg_vr]
        )
        validation_results.extend([repo_vr, sem_vr, canon_vr, reg_vr, acc_vr])

        stage_results.append(
            _stage_result(STAGE_RUN_VALIDATION, VALIDATION_PASS, _ms(t0),
                          evidence={"validator_count": len(validation_results)})
        )

        # ------------------------------------------------------------------
        # STAGE: Update State
        # ------------------------------------------------------------------
        t0 = time.monotonic()
        stage_results.append(
            _stage_result(STAGE_UPDATE_STATE, VALIDATION_PASS, _ms(t0),
                          evidence={"note": "State read-only in safe modes"})
        )

        # ------------------------------------------------------------------
        # Build metrics
        # ------------------------------------------------------------------
        total_ms = _ms(t_start)
        metrics = ExecutionMetrics(
            execution_id=execution_id,
            generated_at=generated_at,
            total_duration_ms=total_ms,
            stage_durations={s.stage: s.duration_ms for s in stage_results},
            validation_scores={v.validator: v.score for v in validation_results},
            evidence_count=evidence_dict.get("evidence_count", 0),
            artifact_count=0,
            error_count=len(errors),
            warning_count=len(warnings),
            confidence=exec_context.confidence,
            schema_version=EXECUTION_VERSION,
        )

        # ------------------------------------------------------------------
        # STAGE: Generate Reports
        # ------------------------------------------------------------------
        t0 = time.monotonic()
        all_ok = not any(e for e in errors)
        status = "COMPLETED" if all_ok else "COMPLETED_WITH_WARNINGS"
        if any(v.status == VALIDATION_FAIL for v in validation_results):
            status = "VALIDATION_FAILED"

        next_actions = self._compute_next_actions(queue_data, state_data, approval)

        execution_result = ExecutionResult(
            execution_id=execution_id,
            generated_at=generated_at,
            repository=str(self.root),
            mode=self.mode,
            approval=approval,
            status=status,
            schema_version=EXECUTION_VERSION,
            context=exec_context,
            stage_results=stage_results,
            validation_results=validation_results,
            metrics=metrics,
            snapshot=None,
            evidence=evidence_dict,
            artifacts=[],
            errors=errors,
            warnings=warnings,
            next_actions=next_actions,
            summary=self._build_summary(status, execution_id, metrics),
        )

        markdown = self._report_generator.render(execution_result)
        report_dict = self._reporter.report(execution_result.to_dict())

        stage_results.append(
            _stage_result(STAGE_GENERATE_REPORTS, VALIDATION_PASS, _ms(t0))
        )

        # ------------------------------------------------------------------
        # STAGE: Persist Artifacts
        # ------------------------------------------------------------------
        t0 = time.monotonic()
        paths: Dict[str, str] = {}
        if self.persist:
            persistence = ExecutionPersistence(str(self.root))
            paths = persistence.save(
                execution_result,
                log_entries=self._logger.entries(),
                report_dict=report_dict,
                markdown=markdown,
            )
            # Also write report to output_dir
            report_path = self.output_dir / "AI_CTO_EXECUTION_REPORT.md"
            self._report_generator.generate(execution_result, report_path)
            paths["markdown_root"] = str(report_path)

            metrics = ExecutionMetrics(
                execution_id=execution_id,
                generated_at=generated_at,
                total_duration_ms=_ms(t_start),
                stage_durations={s.stage: s.duration_ms for s in stage_results},
                validation_scores={v.validator: v.score for v in validation_results},
                evidence_count=evidence_dict.get("evidence_count", 0),
                artifact_count=len(paths),
                error_count=len(errors),
                warning_count=len(warnings),
                confidence=exec_context.confidence,
                schema_version=EXECUTION_VERSION,
            )
            execution_result.metrics = metrics

        stage_results.append(
            _stage_result(STAGE_PERSIST_ARTIFACTS, VALIDATION_PASS, _ms(t0),
                          evidence={"artifact_count": len(paths)})
        )

        stage_results.append(
            _stage_result(STAGE_RETURN_SUMMARY, VALIDATION_PASS, 0.0)
        )

        self._logger.info(STAGE_RETURN_SUMMARY, "Execution complete",
                          {"status": status, "execution_id": execution_id})

        return {
            "execution_result": execution_result,
            "execution_dict": execution_result.to_dict(),
            "markdown": markdown,
            "paths": paths,
        }

    # ------------------------------------------------------------------
    # Intelligence loading (delegates to existing COREs)
    # ------------------------------------------------------------------

    def _load_live_context(self) -> Dict[str, Any]:
        try:
            from python.context_synchronization_engine.persistence import (  # type: ignore[import]
                ContextPersistence,
            )
            persistence = ContextPersistence(str(self.root))
            return persistence.load_live_context()
        except Exception:
            return {}

    def _load_development_state(self) -> Dict[str, Any]:
        try:
            from python.development_state_engine import DevelopmentStateEngine  # type: ignore[import]
            engine = DevelopmentStateEngine(repository_root=str(self.root))
            state = engine.LoadCurrentState(create_if_missing=True)
            return state.to_dict() if hasattr(state, "to_dict") else {}
        except Exception:
            return {}

    def _load_briefing(self) -> Dict[str, Any]:
        try:
            from python.executive_briefing_engine.persistence import (  # type: ignore[import]
                ExecutiveBriefingPersistence,
            )
            persistence = ExecutiveBriefingPersistence(str(self.root))
            return persistence.load_briefing()
        except Exception:
            return {}

    def _load_planning_queue(self) -> Dict[str, Any]:
        try:
            from python.autonomous_planning_engine.persistence import (  # type: ignore[import]
                PlanningPersistence,
            )
            persistence = PlanningPersistence(str(self.root))
            planning = persistence.load_planning()
            return planning.get("execution_queue", {}) or {}
        except Exception:
            return {}

    # ------------------------------------------------------------------
    # Pipeline helpers
    # ------------------------------------------------------------------

    def _check_dependencies(self, queue_data: Dict[str, Any]) -> List[str]:
        errors: List[str] = []
        for entry in queue_data.get("entries", []):
            blocked = entry.get("blocked_by", [])
            if blocked:
                errors.append(
                    f"Entry {entry.get('entry_id', '?')!r} is blocked by: {blocked}"
                )
        return errors

    def _build_execution_context(
        self,
        execution_id: str,
        generated_at: str,
        context_data: Dict[str, Any],
        state_data: Dict[str, Any],
        briefing_data: Dict[str, Any],
        queue_data: Dict[str, Any],
        approval: str,
        policy: ExecutionPolicy,
        recurrence_evidence: Optional[Dict[str, Any]] = None,
    ) -> ExecutionContext:
        planning_id = queue_data.get("queue_id", "")
        state_id = state_data.get("state_id", "")
        sync_id = context_data.get("synchronization_id", "")
        briefing_id = briefing_data.get("briefing_id", "")

        # Confidence = average of available context signals
        has_context = bool(context_data)
        has_state = bool(state_data)
        has_briefing = bool(briefing_data)
        has_queue = bool(queue_data.get("entries"))
        confidence = sum([has_context, has_state, has_briefing, has_queue]) / 4.0

        return ExecutionContext(
            execution_id=execution_id,
            repository=str(self.root),
            workspace=str(self.workspace_root),
            branch=context_data.get("current_branch", ""),
            commit=context_data.get("current_commit", ""),
            issue=state_data.get("current_issue", context_data.get("current_issue", "")),
            batch=state_data.get("current_batch", context_data.get("current_batch", "")),
            milestone=state_data.get("current_milestone", ""),
            core=context_data.get("next_core", ""),
            roadmap=state_data.get("current_roadmap", ""),
            planning_id=planning_id,
            state_id=str(state_id),
            synchronization_id=str(sync_id),
            briefing_id=str(briefing_id),
            owner=state_data.get("owner", ""),
            timestamp=generated_at,
            environment=str(self.root),
            policy=self.mode,
            approval=approval,
            confidence=round(confidence, 3),
            mode=self.mode,
            schema_version=EXECUTION_VERSION,
            recurrence_evidence=recurrence_evidence or {},
        )

    def _prepare_recurrence_evidence_handoff(
        self,
        queue_data: Dict[str, Any],
        state_data: Dict[str, Any],
        context_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Carry Error Memory preventive evidence to ExecutionContext.

        RUN 006 deliberately does not convert recurrence evidence into
        execution authority.

        CORE-015 policy and approval physiology remain unchanged.
        """

        scheduler = ExecutionScheduler()
        next_entry = scheduler.next_executable(
            queue_data,
            state_data,
        )

        if not next_entry:
            return {
                "transformation_identity": "",
                "transformation_title": "",
                "evidence": [],
                "unresolved": [],
                "has_unresolved": False,
                "evidence_count": 0,
                "unresolved_count": 0,
                "status": "NO_EXECUTABLE_TRANSFORMATION",
            }

        try:
            from python.epistemic.error_memory import (
                FailureKind,
                IntendedTransformation,
                form_recurrence_evidence_handoff,
                prepare_intended_transformation_from_error_memory,
                seed_demonstrated_ai_toolkit_failures_run002,
            )
        except ImportError:
            from epistemic.error_memory import (
                FailureKind,
                IntendedTransformation,
                form_recurrence_evidence_handoff,
                prepare_intended_transformation_from_error_memory,
                seed_demonstrated_ai_toolkit_failures_run002,
            )

        identity = str(
            next_entry.get("entry_id")
            or next_entry.get("planning_id")
            or next_entry.get("id")
            or "UNIDENTIFIED-TRANSFORMATION"
        )

        title = str(
            next_entry.get("title")
            or next_entry.get("summary")
            or next_entry.get("description")
            or identity
        )

        context_values = tuple(
            value
            for value in (
                str(self.root),
                str(context_data.get("current_branch", "")),
                str(context_data.get("current_commit", "")),
                str(state_data.get("current_issue", "")),
                str(state_data.get("current_batch", "")),
            )
            if value
        )

        intended = IntendedTransformation(
            identity=identity,
            title=title,
            activities=(
                FailureKind.EXECUTION,
                FailureKind.VALIDATION,
                FailureKind.EPISTEMIC,
            ),
            context=context_values,
        )

        organ = seed_demonstrated_ai_toolkit_failures_run002()

        preparation = prepare_intended_transformation_from_error_memory(
            organ,
            intended,
        )

        handoff = form_recurrence_evidence_handoff(
            preparation,
        )

        body = handoff.to_dict()
        body["status"] = "RECURRENCE_EVIDENCE_ATTACHED"
        body["execution_authority"] = False
        body["approval_authority"] = False
        body["validation_authority"] = False

        return body

    def _execute_approved_step(
        self,
        policy: ExecutionPolicy,
        approval: str,
        queue_data: Dict[str, Any],
        state_data: Dict[str, Any],
    ) -> tuple:
        """
        Perform the approved execution step.

        In safe modes this is always a no-op — the engine observes and
        reports without mutating any state.
        """
        warnings: List[str] = []

        if policy.is_safe_mode():
            # Safe modes: describe what WOULD be executed
            scheduler = ExecutionScheduler()
            next_entry = scheduler.next_executable(queue_data, state_data)
            if next_entry:
                warnings.append(
                    f"[{self.mode}] Would execute: {next_entry.get('entry_id', '?')!r} "
                    f"— {next_entry.get('title', '')}"
                )
            else:
                warnings.append(f"[{self.mode}] No executable queue entries found.")
            return VALIDATION_PASS, warnings

        if approval != APPROVAL_APPROVED:
            warnings.append(
                f"Execution skipped — approval state is {approval!r}. "
                "Owner must approve before execution proceeds."
            )
            return VALIDATION_WARNING, warnings

        # OWNER_APPROVED or FULL_ACCEPTANCE: describe the next step
        scheduler = ExecutionScheduler()
        next_entry = scheduler.next_executable(queue_data, state_data)
        if next_entry:
            self._evidence.record(
                "CORE-015",
                "approved_step",
                {"entry": next_entry, "approval": approval},
            )
            warnings.append(
                f"[{self.mode}] Approved step identified: "
                f"{next_entry.get('entry_id', '?')!r} — {next_entry.get('title', '')}"
            )
        else:
            warnings.append(f"[{self.mode}] No executable queue entries found.")

        return VALIDATION_PASS, warnings

    def _compute_next_actions(
        self,
        queue_data: Dict[str, Any],
        state_data: Dict[str, Any],
        approval: str,
    ) -> List[str]:
        actions: List[str] = []
        scheduler = ExecutionScheduler()
        next_entry = scheduler.next_executable(queue_data, state_data)
        if next_entry:
            actions.append(
                f"Next: {next_entry.get('entry_id', '?')} — {next_entry.get('title', '')}"
            )
        if approval != APPROVAL_APPROVED and not ExecutionPolicy(self.mode).is_safe_mode():
            actions.append("Obtain Owner approval to proceed with execution.")
        if not queue_data.get("entries"):
            actions.append("Run `ai plan` to refresh the execution queue.")
        return actions

    def _build_summary(
        self,
        status: str,
        execution_id: str,
        metrics: ExecutionMetrics,
    ) -> str:
        return (
            f"Execution {execution_id} completed with status {status!r}. "
            f"Duration: {metrics.total_duration_ms:.1f} ms. "
            f"Mode: {self.mode}. "
            f"Confidence: {metrics.confidence:.0%}."
        )

    def _run_pipeline(self, **kwargs: Any) -> Dict[str, Any]:
        """Internal coordination hook for ExecutionCoordinator."""
        return self.execute()

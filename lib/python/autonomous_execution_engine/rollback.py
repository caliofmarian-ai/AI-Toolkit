"""
Autonomous Execution Engine — Rollback Planner
CORE-015F

Produces a deterministic rollback plan for every execution step
without performing any destructive operations autonomously.
"""

from typing import Any, Dict, List, Mapping


class ExecutionRollbackPlanner:
    """
    CORE-015F — Execution Rollback Planner.

    Analyses the execution context and produces a rollback plan.
    The planner NEVER executes rollback — it only describes how.
    Owner approval is always required before any rollback is attempted.
    """

    def plan(
        self,
        execution_id: str,
        context: Mapping[str, Any],
        stage_results: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Produce a rollback plan for the given execution.

        Returns a deterministic dict describing rollback steps
        ordered from last executed stage backwards.
        """
        steps: List[Dict[str, Any]] = []

        # Walk stages in reverse — only stages that completed need rollback
        completed = [
            s for s in stage_results if s.get("status") in ("PASS", "WARNING")
        ]
        for stage in reversed(completed):
            step = self._rollback_step(stage, context)
            if step:
                steps.append(step)

        return {
            "execution_id": execution_id,
            "rollback_required": bool(steps),
            "owner_approval_required": True,
            "step_count": len(steps),
            "steps": steps,
            "notes": (
                "Rollback must be approved by the Owner before execution. "
                "The AI CTO will NEVER perform rollback autonomously."
            ),
        }

    # ------------------------------------------------------------------

    def _rollback_step(
        self,
        stage: Dict[str, Any],
        context: Mapping[str, Any],
    ) -> Dict[str, Any]:
        """Produce a single rollback step description."""
        stage_name = stage.get("stage", "")
        branch = context.get("branch", "")
        commit = context.get("commit", "")
        batch = context.get("batch", "")

        if stage_name == "execute_approved_step":
            return {
                "stage": stage_name,
                "action": "restore_development_state",
                "description": (
                    f"Restore development state to batch={batch!r}, "
                    f"branch={branch!r}, commit={commit!r}"
                ),
                "owner_action_required": True,
            }
        if stage_name == "update_state":
            return {
                "stage": stage_name,
                "action": "revert_state_update",
                "description": "Revert development state update to previous values.",
                "owner_action_required": True,
            }
        # Other stages are read-only — no rollback needed
        return {}

"""
Autonomous Execution Engine — Execution Policy, Permissions and Approval
CORE-015B

Enforces safety contracts before any execution step is performed.
"""

from typing import Any, Dict, List, Mapping

from .models import (
    APPROVAL_APPROVED,
    APPROVAL_DENIED,
    APPROVAL_EXPIRED,
    APPROVAL_REVOKED,
    APPROVAL_UNKNOWN,
    APPROVAL_WAITING_OWNER,
    MODE_DRY_RUN,
    MODE_FULL_ACCEPTANCE,
    MODE_OWNER_APPROVED,
    MODE_PLAN_ONLY,
    MODE_READ_ONLY,
    MODE_SIMULATION,
    MODE_VALIDATION_ONLY,
    VALIDATION_FAIL,
    VALIDATION_PASS,
    VALIDATION_WARNING,
    ValidationResult,
)

# ---------------------------------------------------------------------------
# Protected operations — execution MUST never perform these without approval
# ---------------------------------------------------------------------------

_PROTECTED_OPERATIONS = frozenset(
    {
        "force_push",
        "delete_branch",
        "merge_pull_request",
        "rewrite_git_history",
        "destructive_command",
        "modify_external_repository",
    }
)

# Modes that require explicit owner approval for protected operations
_APPROVAL_REQUIRED_MODES = frozenset(
    {
        MODE_OWNER_APPROVED,
        MODE_FULL_ACCEPTANCE,
    }
)

# Modes that never execute real mutations
_SAFE_MODES = frozenset(
    {
        MODE_READ_ONLY,
        MODE_PLAN_ONLY,
        MODE_VALIDATION_ONLY,
        MODE_SIMULATION,
        MODE_DRY_RUN,
    }
)


class ExecutionPolicy:
    """
    CORE-015B — Execution Policy.

    Determines which operations are permitted for a given execution mode.
    """

    def __init__(self, mode: str = MODE_READ_ONLY) -> None:
        if mode not in (
            MODE_READ_ONLY,
            MODE_PLAN_ONLY,
            MODE_VALIDATION_ONLY,
            MODE_SIMULATION,
            MODE_DRY_RUN,
            MODE_OWNER_APPROVED,
            MODE_FULL_ACCEPTANCE,
        ):
            mode = MODE_READ_ONLY
        self.mode = mode

    def is_safe_mode(self) -> bool:
        """Return True if the mode never performs real mutations."""
        return self.mode in _SAFE_MODES

    def requires_approval(self) -> bool:
        """Return True if the mode requires explicit owner approval."""
        return self.mode in _APPROVAL_REQUIRED_MODES

    def permits_operation(self, operation: str) -> bool:
        """Return True if the operation is permitted in the current mode."""
        if operation in _PROTECTED_OPERATIONS:
            return self.mode in _APPROVAL_REQUIRED_MODES
        return True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "mode": self.mode,
            "is_safe_mode": self.is_safe_mode(),
            "requires_approval": self.requires_approval(),
            "protected_operations": sorted(_PROTECTED_OPERATIONS),
        }


class ExecutionPermissions:
    """
    CORE-015B — Execution Permissions.

    Validates that the current context has the necessary permissions
    to perform an execution step.
    """

    def check(self, policy: ExecutionPolicy, approval: str) -> ValidationResult:
        """
        Check that policy + approval permit execution.

        Returns PASS if execution may proceed, FAIL otherwise.
        """
        errors: List[str] = []

        if policy.requires_approval():
            if approval not in (APPROVAL_APPROVED,):
                errors.append(
                    f"Execution mode {policy.mode!r} requires APPROVED state "
                    f"but approval is {approval!r}"
                )

        if errors:
            return ValidationResult(
                validator="ExecutionPermissions",
                status=VALIDATION_FAIL,
                score=0.0,
                findings=errors,
                evidence={"mode": policy.mode, "approval": approval},
            )

        return ValidationResult(
            validator="ExecutionPermissions",
            status=VALIDATION_PASS,
            score=1.0,
            findings=[],
            evidence={"mode": policy.mode, "approval": approval},
        )


class ExecutionApproval:
    """
    CORE-015B — Execution Approval.

    Determines the current approval state from development state and
    briefing context.
    """

    def resolve(
        self,
        development_state: Mapping[str, Any],
        briefing: Mapping[str, Any],
        mode: str,
    ) -> str:
        """
        Derive the current approval state.

        Safe modes are always treated as APPROVED for read-only operations.
        Protected modes require an explicit approval signal.
        """
        if mode in _SAFE_MODES:
            return APPROVAL_APPROVED

        # Check development state for an explicit approval signal
        state_approval = str(development_state.get("approval_state", "")).upper().strip()
        if state_approval in {
            APPROVAL_APPROVED,
            APPROVAL_DENIED,
            APPROVAL_REVOKED,
            APPROVAL_EXPIRED,
        }:
            return state_approval

        # Check briefing for pending owner decisions
        owner_decisions = briefing.get("owner_dashboard", {}).get(
            "recommended_actions", []
        )
        if owner_decisions:
            return APPROVAL_WAITING_OWNER

        return APPROVAL_UNKNOWN

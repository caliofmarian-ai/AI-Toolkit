"""
CSL Safety and Governance Kernel — Canonical Specification Language v1.0.0

Implements the mandatory governance components:
- Permission Engine
- Risk Engine
- Approval Engine
- Audit Engine
- Emergency Stop

CSL Reference: Volume VII (Safety and Governance), RFC-0005 (Safety and Governance Kernel)
CORE: CORE-023-009
"""

from __future__ import annotations

import datetime
import logging
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Permission Model (Volume VII Chapter 5)
# ---------------------------------------------------------------------------

class PermissionCategory(str, Enum):
    READ = "READ"
    WRITE = "WRITE"
    EXECUTE = "EXECUTE"
    GENERATE = "GENERATE"
    APPROVE = "APPROVE"
    AUDIT = "AUDIT"
    GOVERN = "GOVERN"
    EMERGENCY = "EMERGENCY"


@dataclass(frozen=True)
class Permission:
    """A single explicit permission grant."""

    category: PermissionCategory
    scope: str  # resource or action scope
    granted_by: str = "system"
    reason: str = ""


# ---------------------------------------------------------------------------
# Risk Model (Volume VII Chapter 7)
# ---------------------------------------------------------------------------

class RiskLevel(str, Enum):
    NONE = "NONE"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


# Risk levels that require explicit human approval
_APPROVAL_REQUIRED_LEVELS = {RiskLevel.HIGH, RiskLevel.CRITICAL}


@dataclass(frozen=True)
class RiskClassification:
    """Risk classification for an engineering action."""

    action: str
    level: RiskLevel
    requires_approval: bool
    reason: str = ""

    @classmethod
    def classify(cls, action: str, level: RiskLevel) -> "RiskClassification":
        return cls(
            action=action,
            level=level,
            requires_approval=level in _APPROVAL_REQUIRED_LEVELS,
            reason=f"Action '{action}' classified as {level.value} risk",
        )


# ---------------------------------------------------------------------------
# Approval Model (Volume VII Chapter 8)
# ---------------------------------------------------------------------------

class ApprovalStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    AUTO_APPROVED = "AUTO_APPROVED"


@dataclass
class ApprovalRecord:
    """Record of an approval decision."""

    approval_id: str
    action: str
    risk_level: RiskLevel
    status: ApprovalStatus
    approved_by: str = ""
    reason: str = ""
    timestamp: str = field(default_factory=lambda: datetime.datetime.utcnow().isoformat())


# ---------------------------------------------------------------------------
# Audit Record (Volume VII Chapter 10)
# ---------------------------------------------------------------------------

@dataclass
class AuditRecord:
    """Immutable audit record for a governance event."""

    record_id: str
    action: str
    risk_level: RiskLevel
    approval_id: str
    actor: str
    outcome: str  # PERMITTED | DENIED | STOPPED
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.datetime.utcnow().isoformat())


# ---------------------------------------------------------------------------
# Permission Engine
# ---------------------------------------------------------------------------

class PermissionEngine:
    """
    Evaluates whether an actor has permission to execute an action.

    Permissions shall be explicit (Volume VII Chapter 5).
    """

    def __init__(self) -> None:
        self._grants: List[Permission] = []

    def grant(self, permission: Permission) -> None:
        self._grants.append(permission)

    def check(self, category: PermissionCategory, scope: str) -> bool:
        """Return True if the category is permitted for the scope."""
        for grant in self._grants:
            if grant.category == category and (grant.scope == scope or grant.scope == "*"):
                return True
        return False

    def require(self, category: PermissionCategory, scope: str) -> None:
        """Raise PermissionDeniedError if permission is not granted."""
        if not self.check(category, scope):
            raise PermissionDeniedError(f"Permission denied: {category.value} on '{scope}'")


class PermissionDeniedError(Exception):
    """Raised when a required permission is not granted."""


# ---------------------------------------------------------------------------
# Risk Engine
# ---------------------------------------------------------------------------

class RiskEngine:
    """
    Classifies the risk level of engineering actions.

    Risk classification determines approval requirements (Volume VII Chapter 7).
    """

    _DEFAULT_CLASSIFICATIONS: Dict[str, RiskLevel] = {
        "read": RiskLevel.NONE,
        "validate": RiskLevel.LOW,
        "compile": RiskLevel.LOW,
        "generate": RiskLevel.LOW,
        "write": RiskLevel.MEDIUM,
        "deploy": RiskLevel.HIGH,
        "delete": RiskLevel.HIGH,
        "modify_canonical": RiskLevel.CRITICAL,
        "emergency_stop": RiskLevel.CRITICAL,
    }

    def __init__(self) -> None:
        self._classifications = dict(self._DEFAULT_CLASSIFICATIONS)

    def register(self, action: str, level: RiskLevel) -> None:
        self._classifications[action.lower()] = level

    def classify(self, action: str) -> RiskClassification:
        level = self._classifications.get(action.lower(), RiskLevel.MEDIUM)
        return RiskClassification.classify(action, level)


# ---------------------------------------------------------------------------
# Approval Engine
# ---------------------------------------------------------------------------

class ApprovalEngine:
    """
    Manages approval decisions for high-risk actions.

    Approval shall be explicit (Volume VII Chapter 8).
    """

    def __init__(self) -> None:
        self._records: List[ApprovalRecord] = []

    def request(self, action: str, risk_level: RiskLevel,
                auto_approve_below: RiskLevel = RiskLevel.MEDIUM) -> ApprovalRecord:
        """
        Request approval for an action.

        Actions below auto_approve_below are auto-approved.
        High/critical risk actions remain PENDING until explicitly approved.
        """
        approval_id = str(uuid.uuid4())
        level_order = list(RiskLevel)
        auto_approve = level_order.index(risk_level) <= level_order.index(auto_approve_below)

        if auto_approve:
            record = ApprovalRecord(
                approval_id=approval_id,
                action=action,
                risk_level=risk_level,
                status=ApprovalStatus.AUTO_APPROVED,
                approved_by="system",
                reason=f"Risk level {risk_level.value} is within auto-approval threshold",
            )
        else:
            record = ApprovalRecord(
                approval_id=approval_id,
                action=action,
                risk_level=risk_level,
                status=ApprovalStatus.PENDING,
                reason=f"Risk level {risk_level.value} requires explicit human approval",
            )

        self._records.append(record)
        return record

    def approve(self, approval_id: str, approved_by: str, reason: str = "") -> ApprovalRecord:
        """Grant explicit approval."""
        for record in self._records:
            if record.approval_id == approval_id:
                record.status = ApprovalStatus.APPROVED
                record.approved_by = approved_by
                record.reason = reason
                return record
        raise KeyError(f"Approval record '{approval_id}' not found")

    def reject(self, approval_id: str, reason: str = "") -> ApprovalRecord:
        """Reject an approval request."""
        for record in self._records:
            if record.approval_id == approval_id:
                record.status = ApprovalStatus.REJECTED
                record.reason = reason
                return record
        raise KeyError(f"Approval record '{approval_id}' not found")

    def is_approved(self, approval_id: str) -> bool:
        for record in self._records:
            if record.approval_id == approval_id:
                return record.status in (ApprovalStatus.APPROVED, ApprovalStatus.AUTO_APPROVED)
        return False

    def all_records(self) -> List[ApprovalRecord]:
        return list(self._records)


# ---------------------------------------------------------------------------
# Audit Engine
# ---------------------------------------------------------------------------

class AuditEngine:
    """
    Records immutable audit logs for all governance events.

    Audit records shall include Risk Level (Volume VII Chapter 10).
    """

    def __init__(self) -> None:
        self._records: List[AuditRecord] = []

    def record(self, action: str, risk_level: RiskLevel, approval_id: str,
               actor: str, outcome: str, metadata: Optional[Dict[str, Any]] = None) -> AuditRecord:
        record = AuditRecord(
            record_id=str(uuid.uuid4()),
            action=action,
            risk_level=risk_level,
            approval_id=approval_id,
            actor=actor,
            outcome=outcome,
            metadata=metadata or {},
        )
        self._records.append(record)
        logger.info(
            "GovernanceKernel audit: action=%s risk=%s outcome=%s actor=%s",
            action, risk_level.value, outcome, actor,
        )
        return record

    def all_records(self) -> List[AuditRecord]:
        return list(self._records)

    def records_for_action(self, action: str) -> List[AuditRecord]:
        return [r for r in self._records if r.action == action]


# ---------------------------------------------------------------------------
# Emergency Stop (Volume VII Chapter 4)
# ---------------------------------------------------------------------------

class EmergencyStop:
    """
    Emergency Stop mechanism.

    When activated, all governed actions are immediately halted.
    Human authority is mandatory to resume (Volume VII Chapter 3).
    """

    def __init__(self) -> None:
        self._active = False
        self._reason = ""
        self._activated_by = ""
        self._activated_at = ""

    def activate(self, reason: str, activated_by: str = "system") -> None:
        self._active = True
        self._reason = reason
        self._activated_by = activated_by
        self._activated_at = datetime.datetime.utcnow().isoformat()
        logger.critical(
            "GovernanceKernel EMERGENCY STOP activated: reason=%s by=%s",
            reason, activated_by,
        )

    def deactivate(self, authorized_by: str) -> None:
        self._active = False
        logger.info(
            "GovernanceKernel EMERGENCY STOP deactivated by=%s", authorized_by
        )

    @property
    def is_active(self) -> bool:
        return self._active

    @property
    def reason(self) -> str:
        return self._reason

    def check(self) -> None:
        """Raise EmergencyStopError if emergency stop is active."""
        if self._active:
            raise EmergencyStopError(
                f"Emergency stop is active: {self._reason} (activated_by={self._activated_by})"
            )


class EmergencyStopError(Exception):
    """Raised when an action is attempted while emergency stop is active."""


# ---------------------------------------------------------------------------
# Governance Kernel — unified entry point
# ---------------------------------------------------------------------------

class GovernanceKernel:
    """
    The CSL Safety and Governance Kernel.

    Single mandatory entry point for all governed engineering actions.

    Components:
    - Permission Engine
    - Risk Engine
    - Approval Engine
    - Audit Engine
    - Emergency Stop

    Usage:
        kernel = GovernanceKernel()
        kernel.permissions.grant(Permission(PermissionCategory.EXECUTE, "compile"))
        approval = kernel.authorize("compile", actor="ci-runner")
        # approval.status == AUTO_APPROVED for low-risk actions
    """

    def __init__(self) -> None:
        self.permissions = PermissionEngine()
        self.risk = RiskEngine()
        self.approvals = ApprovalEngine()
        self.audit = AuditEngine()
        self.emergency_stop = EmergencyStop()

    def authorize(self, action: str, actor: str = "system",
                  metadata: Optional[Dict[str, Any]] = None) -> ApprovalRecord:
        """
        Authorize an engineering action through the full governance pipeline.

        1. Check emergency stop
        2. Classify risk
        3. Request approval
        4. Audit the outcome
        """
        # 1. Emergency stop check
        self.emergency_stop.check()

        # 2. Risk classification
        risk = self.risk.classify(action)

        # 3. Approval
        approval = self.approvals.request(action, risk.level)

        # 4. Audit
        outcome = "PERMITTED" if approval.status in (
            ApprovalStatus.APPROVED, ApprovalStatus.AUTO_APPROVED
        ) else "PENDING_APPROVAL"

        self.audit.record(
            action=action,
            risk_level=risk.level,
            approval_id=approval.approval_id,
            actor=actor,
            outcome=outcome,
            metadata=metadata or {},
        )

        if approval.status == ApprovalStatus.PENDING:
            raise ApprovalRequiredError(
                f"Action '{action}' (risk={risk.level.value}) requires explicit human approval. "
                f"Approval ID: {approval.approval_id}"
            )

        return approval

    def deny(self, action: str, actor: str = "system", reason: str = "") -> None:
        """Record a denied action in the audit log."""
        risk = self.risk.classify(action)
        self.audit.record(
            action=action,
            risk_level=risk.level,
            approval_id="",
            actor=actor,
            outcome="DENIED",
            metadata={"reason": reason},
        )


class ApprovalRequiredError(Exception):
    """Raised when a high-risk action requires explicit approval before execution."""

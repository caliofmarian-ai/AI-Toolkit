from __future__ import annotations

from typing import Any, Dict, Iterable, List, Optional, Union

from python.engineering_workspace.capabilities import Capability
from python.engineering_workspace.capabilities_manager import CapabilitiesManager

from .chat_models import PermissionOp, PermissionPolicy


class PermissionManager:
    """Evaluate runtime permissions against explicit allow rules."""

    def __init__(self, policy: Optional[PermissionPolicy] = None) -> None:
        self.policy = policy or PermissionPolicy(id="default", rules={})
        self.capabilities = CapabilitiesManager()

    def set_policy(self, policy: PermissionPolicy) -> None:
        self.policy = policy

    def grant(self, subject: str, operation: Union[str, PermissionOp], *, capability: Optional[str] = None) -> None:
        op_value = operation.value if isinstance(operation, PermissionOp) else str(operation)
        existing = self.policy.rules.setdefault(subject, [])
        if op_value not in {item.value for item in existing}:
            existing.append(PermissionOp(op_value))
        if capability:
            self.capabilities.add_capability(capability)

    def is_allowed(
        self,
        user: Optional[str] = None,
        op: Union[str, PermissionOp, Capability] = PermissionOp.SEND_MESSAGE,
        *,
        session: Optional[str] = None,
        provider: Optional[str] = None,
    ) -> bool:
        if isinstance(op, Capability):
            candidate = op.value
        elif isinstance(op, PermissionOp):
            candidate = op.value
        else:
            candidate = str(op)

        keys: List[str] = ["*"]
        if user:
            keys.extend([str(user), f"user:{user}"])
        if session:
            keys.extend([str(session), f"session:{session}"])
        if provider:
            keys.extend([str(provider), f"provider:{provider}"])

        for key in keys:
            allowed = self.policy.rules.get(key, [])
            if any(item.value == candidate for item in allowed):
                return True
        return False

    def as_dict(self) -> Dict[str, Any]:
        return self.policy.to_dict()

    @classmethod
    def from_dict(cls, payload: Dict[str, Any]) -> "PermissionManager":
        return cls(PermissionPolicy.from_dict(payload))

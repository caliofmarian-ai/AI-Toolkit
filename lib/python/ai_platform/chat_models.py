from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, Iterable, List, Optional


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _ensure_id(prefix: str, value: Optional[str]) -> str:
    if value and str(value).strip():
        return str(value).strip()
    import uuid

    return f"{prefix}-{uuid.uuid4().hex[:12]}"


@dataclass
class ChatSession:
    id: str
    created_at: datetime = field(default_factory=_utc_now)
    owner: str = "owner"
    active_thread_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    provider_id: Optional[str] = None
    permission_policy_id: Optional[str] = None

    def __post_init__(self) -> None:
        self.id = _ensure_id("chat-session", self.id)

    @classmethod
    def from_dict(cls, payload: Dict[str, Any]) -> "ChatSession":
        created_at = payload.get("created_at")
        if isinstance(created_at, str):
            try:
                created_at = datetime.fromisoformat(created_at)
            except ValueError:
                created_at = _utc_now()
        elif created_at is None:
            created_at = _utc_now()
        return cls(
            id=str(payload.get("id") or ""),
            created_at=created_at,
            owner=str(payload.get("owner") or "owner"),
            active_thread_id=payload.get("active_thread_id"),
            metadata=dict(payload.get("metadata") or {}),
            provider_id=payload.get("provider_id"),
            permission_policy_id=payload.get("permission_policy_id"),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat(),
            "owner": self.owner,
            "active_thread_id": self.active_thread_id,
            "metadata": dict(self.metadata),
            "provider_id": self.provider_id,
            "permission_policy_id": self.permission_policy_id,
        }


@dataclass
class ChatThread:
    id: str
    session_id: str
    created_at: datetime = field(default_factory=_utc_now)
    messages: List[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.id = _ensure_id("chat-thread", self.id)

    @classmethod
    def from_dict(cls, payload: Dict[str, Any]) -> "ChatThread":
        created_at = payload.get("created_at")
        if isinstance(created_at, str):
            try:
                created_at = datetime.fromisoformat(created_at)
            except ValueError:
                created_at = _utc_now()
        elif created_at is None:
            created_at = _utc_now()
        return cls(
            id=str(payload.get("id") or ""),
            session_id=str(payload.get("session_id") or ""),
            created_at=created_at,
            messages=[str(item) for item in list(payload.get("messages") or [])],
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "session_id": self.session_id,
            "created_at": self.created_at.isoformat(),
            "messages": list(self.messages),
        }


@dataclass
class ChatMessage:
    id: str
    thread_id: str
    author: str
    created_at: datetime = field(default_factory=_utc_now)
    content: str = ""
    attachments: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.id = _ensure_id("chat-message", self.id)

    @classmethod
    def from_dict(cls, payload: Dict[str, Any]) -> "ChatMessage":
        created_at = payload.get("created_at")
        if isinstance(created_at, str):
            try:
                created_at = datetime.fromisoformat(created_at)
            except ValueError:
                created_at = _utc_now()
        elif created_at is None:
            created_at = _utc_now()
        return cls(
            id=str(payload.get("id") or ""),
            thread_id=str(payload.get("thread_id") or ""),
            author=str(payload.get("author") or "user"),
            created_at=created_at,
            content=str(payload.get("content") or ""),
            attachments=[str(item) for item in list(payload.get("attachments") or [])],
            metadata=dict(payload.get("metadata") or {}),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "thread_id": self.thread_id,
            "author": self.author,
            "created_at": self.created_at.isoformat(),
            "content": self.content,
            "attachments": list(self.attachments),
            "metadata": dict(self.metadata),
        }


@dataclass
class ChatAttachment:
    id: str
    session_id: str
    original_name: str
    mime_type: str
    size: int
    sha256: str
    storage_path: str
    ocr_text: Optional[str] = None
    preview_url: Optional[str] = None
    linked_thread_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.id = _ensure_id("chat-attachment", self.id)
        self.size = int(self.size)

    @classmethod
    def from_dict(cls, payload: Dict[str, Any]) -> "ChatAttachment":
        return cls(
            id=str(payload.get("id") or ""),
            session_id=str(payload.get("session_id") or ""),
            original_name=str(payload.get("original_name") or "unnamed"),
            mime_type=str(payload.get("mime_type") or "application/octet-stream"),
            size=int(payload.get("size") or 0),
            sha256=str(payload.get("sha256") or ""),
            storage_path=str(payload.get("storage_path") or ""),
            ocr_text=payload.get("ocr_text"),
            preview_url=payload.get("preview_url"),
            linked_thread_id=payload.get("linked_thread_id"),
            metadata=dict(payload.get("metadata") or {}),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "session_id": self.session_id,
            "original_name": self.original_name,
            "mime_type": self.mime_type,
            "size": self.size,
            "sha256": self.sha256,
            "storage_path": self.storage_path,
            "ocr_text": self.ocr_text,
            "preview_url": self.preview_url,
            "linked_thread_id": self.linked_thread_id,
            "metadata": dict(self.metadata),
        }


class PermissionOp(str, Enum):
    SEND_MESSAGE = "send_message"
    ATTACH_FILE = "attach_file"
    USE_PROVIDER = "use_provider"
    UPLOAD_ARCHIVE = "upload_archive"
    EXECUTE_TOOL = "execute_tool"


@dataclass
class PermissionPolicy:
    id: str
    rules: Dict[str, List[PermissionOp]] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.id = _ensure_id("permission-policy", self.id)

    @classmethod
    def from_dict(cls, payload: Dict[str, Any]) -> "PermissionPolicy":
        rules: Dict[str, List[PermissionOp]] = {}
        for key, value in dict(payload.get("rules") or {}).items():
            rules[str(key)] = [
                PermissionOp(item) if isinstance(item, PermissionOp) else PermissionOp(str(item))
                for item in list(value or [])
            ]
        return cls(id=str(payload.get("id") or ""), rules=rules)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "rules": {
                key: [item.value for item in value]
                for key, value in self.rules.items()
            },
        }


class ProviderConnectionState(str, Enum):
    CONNECTED = "connected"
    FAILED = "failed"
    INACTIVE = "inactive"


@dataclass
class ProviderConnection:
    id: str
    display_name: str
    state: ProviderConnectionState
    model_list: List[str] = field(default_factory=list)
    capability_subset: List[str] = field(default_factory=list)
    route_policy: Dict[str, Any] = field(default_factory=dict)
    fallback_provider: Optional[str] = None
    health: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.id = _ensure_id("provider", self.id)
        if isinstance(self.state, str):
            self.state = ProviderConnectionState(self.state)

    @classmethod
    def from_dict(cls, payload: Dict[str, Any]) -> "ProviderConnection":
        state_value = payload.get("state")
        if isinstance(state_value, str):
            state = ProviderConnectionState(state_value)
        else:
            state = state_value or ProviderConnectionState.INACTIVE
        return cls(
            id=str(payload.get("id") or ""),
            display_name=str(payload.get("display_name") or ""),
            state=state,
            model_list=[str(item) for item in list(payload.get("model_list") or [])],
            capability_subset=[str(item) for item in list(payload.get("capability_subset") or [])],
            route_policy=dict(payload.get("route_policy") or {}),
            fallback_provider=payload.get("fallback_provider"),
            health=dict(payload.get("health") or {}),
            metadata=dict(payload.get("metadata") or {}),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "display_name": self.display_name,
            "state": self.state.value,
            "model_list": list(self.model_list),
            "capability_subset": list(self.capability_subset),
            "route_policy": dict(self.route_policy),
            "fallback_provider": self.fallback_provider,
            "health": dict(self.health),
            "metadata": dict(self.metadata),
        }


@dataclass
class ContextSnapshot:
    session_id: str
    timestamp: datetime = field(default_factory=_utc_now)
    repo: str = ""
    branch: str = ""
    issue: Optional[str] = None
    sprint: Optional[str] = None
    workspace: Optional[str] = None
    provider_id: Optional[str] = None
    model_id: Optional[str] = None
    semantic_context: Dict[str, Any] = field(default_factory=dict)
    attachments: List[str] = field(default_factory=list)
    history: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, payload: Dict[str, Any]) -> "ContextSnapshot":
        timestamp = payload.get("timestamp")
        if isinstance(timestamp, str):
            try:
                timestamp = datetime.fromisoformat(timestamp)
            except ValueError:
                timestamp = _utc_now()
        elif timestamp is None:
            timestamp = _utc_now()
        return cls(
            session_id=str(payload.get("session_id") or ""),
            timestamp=timestamp,
            repo=str(payload.get("repo") or ""),
            branch=str(payload.get("branch") or ""),
            issue=payload.get("issue"),
            sprint=payload.get("sprint"),
            workspace=payload.get("workspace"),
            provider_id=payload.get("provider_id"),
            model_id=payload.get("model_id"),
            semantic_context=dict(payload.get("semantic_context") or {}),
            attachments=[str(item) for item in list(payload.get("attachments") or [])],
            history=[str(item) for item in list(payload.get("history") or [])],
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "session_id": self.session_id,
            "timestamp": self.timestamp.isoformat(),
            "repo": self.repo,
            "branch": self.branch,
            "issue": self.issue,
            "sprint": self.sprint,
            "workspace": self.workspace,
            "provider_id": self.provider_id,
            "model_id": self.model_id,
            "semantic_context": dict(self.semantic_context),
            "attachments": list(self.attachments),
            "history": list(self.history),
        }

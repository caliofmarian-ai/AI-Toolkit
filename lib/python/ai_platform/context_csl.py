from __future__ import annotations

from typing import Any, Dict, Iterable, List, Mapping, Optional, Union

from .chat_models import ChatSession, ContextSnapshot


class ContextCSLExporter:
    """Build a minimal reproducible context snapshot for session bootstrap."""

    def __init__(self) -> None:
        self._session_store: Dict[str, Dict[str, Any]] = {}

    def register_session(self, session: Union[ChatSession, Mapping[str, Any]]) -> ChatSession:
        payload = session.to_dict() if isinstance(session, ChatSession) else dict(session)
        model = ChatSession.from_dict(payload)
        self._session_store[model.id] = model.to_dict()
        return model

    def context_snapshot(
        self,
        session: Union[ChatSession, Mapping[str, Any]],
        *,
        semantic_context: Optional[Mapping[str, Any]] = None,
        message_history: Optional[Iterable[str]] = None,
        attachments: Optional[Iterable[str]] = None,
    ) -> ContextSnapshot:
        resolved = session.to_dict() if isinstance(session, ChatSession) else dict(session)
        session_model = ChatSession.from_dict(resolved)
        metadata = dict(session_model.metadata or {})
        snapshot = ContextSnapshot(
            session_id=session_model.id,
            repo=str(metadata.get("repo") or metadata.get("repository") or ""),
            branch=str(metadata.get("branch") or ""),
            issue=metadata.get("issue"),
            sprint=metadata.get("sprint"),
            workspace=metadata.get("workspace"),
            provider_id=session_model.provider_id,
            model_id=str(metadata.get("model_id") or "" ) or None,
            semantic_context=dict(semantic_context or metadata.get("semantic_context") or {}),
            attachments=[str(item) for item in list(attachments or metadata.get("attachments") or [])],
            history=[str(item) for item in list(message_history or metadata.get("history") or [])],
        )
        return snapshot

    def export_csl(self, session: Union[ChatSession, Mapping[str, Any]], **kwargs: Any) -> Dict[str, Any]:
        snapshot = self.context_snapshot(session, **kwargs)
        return {
            "kind": "csl_context_snapshot",
            "session_id": snapshot.session_id,
            "timestamp": snapshot.timestamp.isoformat(),
            "repo": snapshot.repo,
            "branch": snapshot.branch,
            "issue": snapshot.issue,
            "sprint": snapshot.sprint,
            "workspace": snapshot.workspace,
            "provider_id": snapshot.provider_id,
            "model_id": snapshot.model_id,
            "semantic_context": dict(snapshot.semantic_context),
            "attachments": list(snapshot.attachments),
            "history": list(snapshot.history),
        }

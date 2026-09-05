#!/usr/bin/env python3

from __future__ import annotations

import tempfile
from pathlib import Path

from python.ai_platform.attachments import AttachmentStore
from python.ai_platform.chat_models import ChatSession, ChatThread, ChatMessage, PermissionOp, ProviderConnection, ProviderConnectionState
from python.ai_platform.context_csl import ContextCSLExporter
from python.ai_platform.permissions import PermissionManager
from python.ai_platform.provider_registry import ProviderRegistry


def main() -> None:
    session = ChatSession(
        id="session-1",
        owner="owner",
        metadata={
            "repo": "AI-Toolkit",
            "branch": "main",
            "issue": "CORE-021",
            "sprint": "S1",
            "workspace": "/workspace",
            "semantic_context": {"domain": "runtime"},
            "history": ["m1"],
            "attachments": ["attachment-1"],
        },
        provider_id="local-provider",
    )
    payload = session.to_dict()
    restored = ChatSession.from_dict(payload)
    assert restored.id == session.id
    assert restored.to_dict() == payload

    thread = ChatThread(id="thread-1", session_id=session.id, messages=["m1", "m2"])
    message = ChatMessage(id="m1", thread_id=thread.id, author="user", content="hello", metadata={"type": "question"})
    assert message.to_dict()["content"] == "hello"

    registry = ProviderRegistry()
    provider = ProviderConnection(
        id="local-provider",
        display_name="Local Provider",
        state=ProviderConnectionState.CONNECTED,
        model_list=["gpt-4o-mini"],
        capability_subset=["ai.chat", "ai.analyze"],
        route_policy={"default": "local-provider"},
        fallback_provider="local-provider",
        health={"latency_ms": 33, "connection": True},
    )
    registry.register_provider(provider)
    assert registry.get_provider("local-provider").id == "local-provider"

    with tempfile.TemporaryDirectory() as tmp:
        store = AttachmentStore(repository_root=tmp)
        attachment = store.add_attachment(
            session_id=session.id,
            original_name="sample.txt",
            content="hello world",
            mime_type="text/plain",
            linked_thread_id=thread.id,
            metadata={"kind": "sample"},
        )
        assert attachment.size == len("hello world")
        assert attachment.sha256
        deduped = store.add_attachment(
            session_id=session.id,
            original_name="sample.txt",
            content="hello world",
            mime_type="text/plain",
            linked_thread_id=thread.id,
        )
        assert deduped.sha256 == attachment.sha256

    permission_manager = PermissionManager()
    permission_manager.grant("owner", PermissionOp.SEND_MESSAGE)
    permission_manager.grant("session:session-1", PermissionOp.ATTACH_FILE)
    assert permission_manager.is_allowed("owner", PermissionOp.SEND_MESSAGE)
    assert permission_manager.is_allowed("owner", PermissionOp.SEND_MESSAGE, session="session-1")
    assert not permission_manager.is_allowed("guest", PermissionOp.SEND_MESSAGE)

    exporter = ContextCSLExporter()
    snapshot = exporter.context_snapshot(
        session,
        semantic_context={"domain": "runtime"},
        message_history=["m1", "m2"],
        attachments=["attachment-1"],
    )
    exported = exporter.export_csl(
        session,
        semantic_context={"domain": "runtime"},
        message_history=["m1", "m2"],
        attachments=["attachment-1"],
    )
    assert snapshot.session_id == session.id
    assert exported["session_id"] == session.id
    assert exported["semantic_context"]["domain"] == "runtime"

    print("ai_platform backend foundation OK")


if __name__ == "__main__":
    main()

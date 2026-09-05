#!/usr/bin/env python3
"""Focused regression tests for the chat orchestration extension layer.

Covers what the foundation smoke test does not exercise in depth:
    * full session/thread/message CRUD lifecycle through AIPlatformService
    * persistence survives across a fresh AIPlatformService instance
      (i.e. the .ai/chat JSON store is the durable source of truth)
    * chat sessions stay synced into the canonical AISessionEngine store
      instead of creating a parallel session stack
    * permission grant/deny enforcement via PermissionManager
    * context export (CSL) reflects session metadata end to end
"""

from __future__ import annotations

import tempfile

from python.ai_platform.chat_models import (
    ChatAttachment,
    ChatMessage,
    ChatSession,
    ChatThread,
    ContextSnapshot,
    PermissionOp,
    PermissionPolicy,
    ProviderConnection,
    ProviderConnectionState,
)
from python.ai_platform.permissions import PermissionManager
from python.ai_platform.service import AIPlatformService


def _configure_chat_access(service: AIPlatformService, session_id: str) -> None:
    service.chat_provider_registry.register_provider(
        {
            "id": "local-provider",
            "display_name": "Local Provider",
            "state": ProviderConnectionState.CONNECTED.value,
        }
    )
    service.permission_manager.grant("owner", PermissionOp.USE_PROVIDER)
    service.permission_manager.grant("owner", PermissionOp.SEND_MESSAGE)
    service.permission_manager.grant("owner", PermissionOp.ATTACH_FILE)


def test_serialization_round_trips() -> None:
    session = ChatSession(
        id="round-trip-session",
        owner="owner",
        metadata={"repo": "AI-Toolkit", "branch": "main"},
        provider_id="local-provider",
    )
    assert ChatSession.from_dict(session.to_dict()).to_dict() == session.to_dict()

    thread = ChatThread(id="round-trip-thread", session_id=session.id, messages=["m1"])
    assert ChatThread.from_dict(thread.to_dict()).to_dict() == thread.to_dict()

    message = ChatMessage(id="round-trip-message", thread_id=thread.id, author="user", content="hi")
    assert ChatMessage.from_dict(message.to_dict()).to_dict() == message.to_dict()

    attachment = ChatAttachment(
        id="round-trip-attachment",
        session_id=session.id,
        original_name="a.txt",
        mime_type="text/plain",
        size=5,
        sha256="deadbeef",
        storage_path="/tmp/a.txt",
    )
    assert ChatAttachment.from_dict(attachment.to_dict()).to_dict() == attachment.to_dict()

    policy = PermissionPolicy(id="policy-1", rules={"owner": [PermissionOp.SEND_MESSAGE]})
    assert PermissionPolicy.from_dict(policy.to_dict()).to_dict() == policy.to_dict()

    provider = ProviderConnection(
        id="prov-1",
        display_name="Provider",
        state=ProviderConnectionState.CONNECTED,
    )
    assert ProviderConnection.from_dict(provider.to_dict()).to_dict() == provider.to_dict()

    snapshot = ContextSnapshot(session_id=session.id, repo="AI-Toolkit", branch="main")
    assert ContextSnapshot.from_dict(snapshot.to_dict()).to_dict() == snapshot.to_dict()

    print("serialization round trips OK")


def test_chat_crud_lifecycle_and_persistence() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        service = AIPlatformService(tmp)
        _configure_chat_access(service, "chat-session-lifecycle")

        session = service.create_chat_session(
            {
                "id": "chat-session-lifecycle",
                "owner": "owner",
                "metadata": {"repo": "AI-Toolkit", "branch": "main"},
                "provider_id": "local-provider",
            }
        )
        assert session["id"] == "chat-session-lifecycle"
        assert session["active_thread_id"]

        thread = service.create_chat_thread(session["id"], payload={"messages": []})
        assert thread["session_id"] == session["id"]

        message = service.create_chat_message(
            thread_id=thread["id"],
            author="user",
            content="hello",
            metadata={"type": "question"},
        )
        assert message["thread_id"] == thread["id"]
        assert service.get_chat_thread(thread["id"])["messages"] == [message["id"]]

        updated_message = service.update_chat_message(message["id"], changes={"content": "updated"})
        assert updated_message["content"] == "updated"

        updated_thread = service.update_chat_thread(thread["id"], changes={"messages": [message["id"], "extra"]})
        assert updated_thread["messages"] == [message["id"], "extra"]

        updated_session = service.update_chat_session(
            session["id"], changes={"metadata": {"branch": "feature/chat"}}
        )
        assert updated_session["metadata"]["branch"] == "feature/chat"
        # Prior metadata keys are preserved (merge, not replace).
        assert updated_session["metadata"]["repo"] == "AI-Toolkit"

        assert any(item["id"] == session["id"] for item in service.list_chat_sessions())
        assert any(item["id"] == thread["id"] for item in service.list_chat_threads(session["id"]))
        assert any(item["id"] == message["id"] for item in service.list_chat_messages(thread["id"]))

        # A fresh service instance pointed at the same repository root must see
        # the same durable state: the .ai/chat store, not an in-memory stack.
        reloaded = AIPlatformService(tmp)
        reloaded_session = reloaded.get_chat_session(session["id"])
        assert reloaded_session is not None
        assert reloaded_session["metadata"]["branch"] == "feature/chat"
        reloaded_message = reloaded.get_chat_message(message["id"])
        assert reloaded_message is not None
        assert reloaded_message["content"] == "updated"

        assert service.delete_chat_message(message["id"]) is True
        assert service.get_chat_message(message["id"]) is None
        assert service.delete_chat_message("does-not-exist") is False

        assert service.delete_chat_thread(thread["id"]) is True
        assert service.get_chat_thread(thread["id"]) is None

        assert service.delete_chat_session(session["id"]) is True
        assert service.get_chat_session(session["id"]) is None
        assert service.delete_chat_session(session["id"]) is False

    print("chat CRUD lifecycle and persistence OK")


def test_chat_session_syncs_into_ai_session_engine() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        service = AIPlatformService(tmp)
        _configure_chat_access(service, "chat-session-sync")
        session = service.create_chat_session(
            {
                "id": "chat-session-sync",
                "owner": "owner",
                "metadata": {
                    "repo": "AI-Toolkit",
                    "branch": "feature/sync",
                    "issue": "CORE-099",
                },
                "provider_id": "local-provider",
            }
        )

        # The canonical AISessionEngine must own the durable session record;
        # no parallel session stack is created for the chat layer.
        engine_session = service.sessions.get(session["id"])
        assert engine_session
        assert engine_session["id"] == session["id"]
        assert engine_session["branch"] == "feature/sync"
        assert engine_session["issue"] == "CORE-099"
        assert engine_session["selected_provider"] == "local-provider"
        assert engine_session["engineering_context"]["chat_session_id"] == session["id"]

        # Updates to the chat session must re-sync the same engine record
        # (same id), not create a second one.
        service.update_chat_session(session["id"], changes={"metadata": {"branch": "feature/sync-2"}})
        resynced = service.sessions.get(session["id"])
        assert resynced["branch"] == "feature/sync-2"
        assert len(service.sessions.list_sessions()) == 1

    print("chat session AISessionEngine sync OK")


def test_permission_grant_and_deny() -> None:
    manager = PermissionManager()
    manager.grant("owner", PermissionOp.SEND_MESSAGE)
    manager.grant("session:chat-session-1", PermissionOp.ATTACH_FILE)

    assert manager.is_allowed("owner", PermissionOp.SEND_MESSAGE) is True
    assert manager.is_allowed("owner", PermissionOp.SEND_MESSAGE, session="chat-session-1") is True
    assert manager.is_allowed("owner", PermissionOp.ATTACH_FILE) is False
    assert manager.is_allowed("owner", PermissionOp.ATTACH_FILE, session="chat-session-1") is True
    assert manager.is_allowed("guest", PermissionOp.SEND_MESSAGE) is False
    assert manager.is_allowed(None, PermissionOp.SEND_MESSAGE) is False

    with tempfile.TemporaryDirectory() as tmp:
        service = AIPlatformService(tmp)
        service.permission_manager.grant("owner", PermissionOp.SEND_MESSAGE.value)
        assert service.check_permission(user="owner", operation=PermissionOp.SEND_MESSAGE.value) is True
        assert service.check_permission(user="guest", operation=PermissionOp.SEND_MESSAGE.value) is False

    print("permission grant/deny OK")


def test_context_export_reflects_session_metadata() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        service = AIPlatformService(tmp)
        _configure_chat_access(service, "chat-session-context")
        session = service.create_chat_session(
            {
                "id": "chat-session-context",
                "owner": "owner",
                "metadata": {
                    "repo": "AI-Toolkit",
                    "branch": "main",
                    "issue": "CORE-021",
                    "sprint": "S1",
                    "workspace": "/workspace",
                    "semantic_context": {"domain": "runtime"},
                    "history": ["m1"],
                    "attachments": ["attachment-1"],
                },
                "provider_id": "local-provider",
            }
        )

        exported = service.export_session_context(session)
        assert exported["session_id"] == session["id"]
        assert exported["repo"] == "AI-Toolkit"
        assert exported["branch"] == "main"
        assert exported["issue"] == "CORE-021"
        assert exported["sprint"] == "S1"
        assert exported["workspace"] == "/workspace"
        assert exported["provider_id"] == "local-provider"
        assert exported["semantic_context"]["domain"] == "runtime"
        assert exported["attachments"] == ["attachment-1"]
        assert exported["history"] == ["m1"]
        assert exported["kind"] == "csl_context_snapshot"

    print("context export reflects session metadata OK")


def test_chat_crud_enforces_provider_and_permissions() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        service = AIPlatformService(tmp)
        try:
            service.create_chat_session(
                {"id": "untrusted", "owner": "owner", "provider_id": "unknown"}
            )
        except ValueError as exc:
            assert "unknown chat provider" in str(exc)
        else:
            raise AssertionError("unknown provider was accepted")

        _configure_chat_access(service, "secured")
        session = service.create_chat_session(
            {"id": "secured", "owner": "owner", "provider_id": "local-provider"}
        )
        thread = service.get_chat_thread(session["active_thread_id"])
        assert thread is not None

        service.permission_manager = PermissionManager()
        try:
            service.create_chat_message(
                thread_id=thread["id"], author="owner", content="blocked"
            )
        except PermissionError:
            pass
        else:
            raise AssertionError("message permission was not enforced")

        try:
            service.add_attachment(
                session_id=session["id"],
                original_name="blocked.txt",
                content="blocked",
            )
        except PermissionError:
            pass
        else:
            raise AssertionError("attachment permission was not enforced")

    print("chat CRUD provider and permission enforcement OK")


def main() -> None:
    test_serialization_round_trips()
    test_chat_crud_lifecycle_and_persistence()
    test_chat_session_syncs_into_ai_session_engine()
    test_permission_grant_and_deny()
    test_context_export_reflects_session_metadata()
    test_chat_crud_enforces_provider_and_permissions()
    print("ai chat CRUD/permissions/context export tests OK")


if __name__ == "__main__":
    main()

from __future__ import annotations

import json
from pathlib import Path

import pytest

from python.ai_platform.context_builder import AIContextBuilder
from python.ai_platform.conversation_context import (
    ConversationContextReconstructor,
)
from python.ai_platform.service import AIPlatformService
from python.runtime.organism import EpistemicOrganismAccess


def test_context_reconstructor_reuses_existing_anatomy():
    assert ConversationContextReconstructor.__dict__.get(
        "base_context_builder", None
    ) is None

    source = Path(
        "lib/python/ai_platform/conversation_context.py"
    ).read_text(encoding="utf-8")

    assert "AIContextBuilder" in source
    assert "EpistemicOrganismAccess" in source
    assert "AISessionEngine(" not in source


def test_context_is_bounded_serializable_and_inspectable(
    tmp_path,
    monkeypatch,
):
    reconstructor = ConversationContextReconstructor(
        tmp_path,
        max_raw_sources=2,
        max_source_chars=256,
    )

    recovered = {
        "session_id": "session-1",
        "project": "AI-Toolkit",
        "repository": "AI-Toolkit",
        "experience": {
            "experience_id": "EXP-1",
            "state": "ACTIVE",
            "recovered": True,
        },
        "raw_sources": [
            {
                "event_id": "RAW-1",
                "actor": "HUMAN",
                "sequence": 1,
                "timestamp": "2026-08-16T00:00:00+00:00",
                "content": "first",
                "source": {"identifier": "RAW-1"},
                "epistemic_status": {
                    "raw_source": True,
                    "evidence": False,
                    "canon": False,
                },
            },
            {
                "event_id": "RAW-2",
                "actor": "AI",
                "sequence": 2,
                "timestamp": "2026-08-16T00:00:01+00:00",
                "content": "second",
                "provider": "test-provider",
                "model": "test-model",
                "source": {"identifier": "RAW-2"},
                "epistemic_status": {
                    "raw_source": True,
                    "evidence": False,
                    "canon": False,
                },
            },
            {
                "event_id": "RAW-3",
                "actor": "HUMAN",
                "sequence": 3,
                "timestamp": "2026-08-16T00:00:02+00:00",
                "content": "third",
                "source": {"identifier": "RAW-3"},
                "epistemic_status": {
                    "raw_source": True,
                    "evidence": False,
                    "canon": False,
                },
            },
        ],
    }

    monkeypatch.setattr(
        reconstructor.organism,
        "conversation_session",
        lambda session_id: recovered,
    )
    monkeypatch.setattr(
        reconstructor.organism,
        "state",
        lambda: {
            "schema": "organism",
            "layered_memory": {"state": "AVAILABLE"},
            "persistent_experience": {"runtime_reachable": True},
            "provenance": {"runtime_reachable": True},
            "error_memory": {"state": "AVAILABLE_AS_EVIDENCE"},
            "human_authority": {"preserved": True},
            "migration_boundaries": {
                "pcc_06": "SUSPENDED_FOR_MIGRATION"
            },
        },
    )
    monkeypatch.setattr(
        reconstructor.base_context_builder,
        "build",
        lambda: {
            "repository_profile": {"name": "AI-Toolkit"},
            "repository_health": {},
            "current_branch": "fusion/test",
            "current_sprint": "",
            "current_epic": "",
            "current_issue": "",
            "runtime_status": {},
            "workspace": {"workspace": "/workspace"},
        },
    )

    context = reconstructor.build("session-1")

    assert context["schema"] == "FUSION-02-CONVERSATION-CONTEXT-1"
    assert len(context["conversation"]["sources"]) == 2
    assert [
        item["sequence"]
        for item in context["conversation"]["sources"]
    ] == [2, 3]

    assert context["persistent_experience"]["experience_id"] == "EXP-1"
    assert context["provenance"]["sources"][0]["event_id"] == "RAW-2"

    boundaries = context["epistemic_boundaries"]
    assert boundaries["raw_conversation_is_evidence"] is False
    assert boundaries["raw_conversation_is_canon"] is False
    assert boundaries["ai_statement_is_evidence"] is False
    assert boundaries["automatic_sedimentation"] is False
    assert boundaries["human_authority_preserved"] is True

    json.dumps(context)


def test_pipeline_can_receive_reconstructed_context():
    source = Path("lib/python/ai_platform/pipeline.py").read_text(
        encoding="utf-8"
    )
    assert "context_override" in source
    assert "dict(context_override)" in source


def test_service_reconstructs_after_human_raw_source_before_provider():
    source = Path("lib/python/ai_platform/service.py").read_text(
        encoding="utf-8"
    )

    human = source.index(
        "human_source = self.conversation_experience.raw_source"
    )
    persist = source.index(
        "self.sessions.append_raw_source",
        human,
    )
    reconstruct = source.index(
        "reconstructed_context = self.conversation_context.build",
        persist,
    )
    provider = source.index(
        "result = self.pipeline.run",
        reconstruct,
    )

    assert human < persist < reconstruct < provider


def test_error_memory_precedents_are_evidence_not_canon():
    organism_source = Path(
        "lib/python/runtime/organism.py"
    ).read_text(encoding="utf-8")

    assert "FUSION_02_TERMUX_EXECUTION_ERROR_MEMORY.md" in organism_source
    assert '"evidence_is_canon": False' in organism_source
    assert '"automatic_sedimentation": False' in organism_source


def test_repository_query_privileged_bypass_is_closed():
    source = Path(
        "lib/python/runtime/interfaces/http_server.py"
    ).read_text(encoding="utf-8")

    assert 'normalized_dashboard_path == "/repository"' in source
    assert "privileged_query" in source
    assert "if privileged_query and not self._require_owner()" in source


def test_authenticated_owner_chat_route_exists():
    source = Path(
        "lib/python/runtime/interfaces/http_server.py"
    ).read_text(encoding="utf-8")

    marker = 'elif path == "/api/ai/chat":'
    index = source.index(marker)
    tail = source[index:index + 1800]

    assert "if not self._require_owner()" in tail
    assert "ask_repository(" in tail
    assert "session_id=session_id" in tail


def test_organism_still_preserves_human_authority():
    source = Path("lib/python/runtime/organism.py").read_text(
        encoding="utf-8"
    )

    assert "human_authority" in source
    assert "SUSPENDED_FOR_MIGRATION" in source


def test_no_parallel_memory_or_session_system_created():
    created = Path("lib/python/ai_platform/conversation_context.py")
    source = created.read_text(encoding="utf-8")

    assert "class AISessionEngine" not in source
    assert "class Experience" not in source
    assert "class Provenance" not in source
    assert "class LayeredMemoryRepository" not in source


def test_fusion02_context_anatomy_exposes_only_structure():
    from python.ai_platform.service import (
        _fusion02_context_anatomy,
    )

    human_secret = (
        "HUMAN RAW CONTENT MUST NOT LEAK"
    )

    repository_secret = (
        "REPOSITORY VALUE MUST NOT LEAK"
    )

    context = {
        "conversation": {
            "sources": [
                {
                    "actor": "HUMAN",
                    "content": human_secret,
                }
            ]
        },
        "repository_profile": {
            "private": repository_secret,
        },
    }

    anatomy = (
        _fusion02_context_anatomy(
            context
        )
    )

    assert (
        anatomy[
            "total_serialized_bytes"
        ]
        > 0
    )

    assert (
        anatomy["branch_count"]
        == 2
    )

    assert (
        "conversation"
        in anatomy["branches"]
    )

    assert (
        "repository_profile"
        in anatomy["branches"]
    )

    serialized = repr(anatomy)

    assert human_secret not in serialized
    assert repository_secret not in serialized


def test_fusion02_context_anatomy_preserves_branch_identity():
    from python.ai_platform.service import (
        _fusion02_context_anatomy,
    )

    context = {
        "repository_profile": {
            "payload": "x" * 10000,
        },
        "runtime_status": {
            "payload": "y" * 1000,
        },
        "conversation": {
            "sources": [],
        },
    }

    anatomy = (
        _fusion02_context_anatomy(
            context
        )
    )

    repository_bytes = (
        anatomy["branches"][
            "repository_profile"
        ]["bytes"]
    )

    runtime_bytes = (
        anatomy["branches"][
            "runtime_status"
        ]["bytes"]
    )

    assert (
        repository_bytes
        > runtime_bytes
    )

    assert (
        anatomy[
            "estimated_tokens_at_4_bytes"
        ]
        > 0
    )

    for branch in (
        anatomy["branches"].values()
    ):
        assert set(branch) == {
            "bytes",
            "percent",
            "kind",
            "children",
        }

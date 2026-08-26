from __future__ import annotations

import json
from pathlib import Path


from python.ai_platform.context_builder import AIContextBuilder
from python.ai_platform.conversation_context import (
    ConversationContextReconstructor,
)
from python.ai_platform.service import AIPlatformService


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
):
    service = AIPlatformService(
        repository_root=str(tmp_path),
        workspace_root=str(tmp_path),
    )

    session = service.sessions.create(
        {
            "id": "FUSION02-REAL-CONTEXT-SESSION",
            "project": "AI-Toolkit",
            "repository": "AI-Toolkit",
            "selected_provider": "provider-alpha",
            "selected_model": "model-alpha",
        }
    )

    experience, binding = (
        service.conversation_experience
        .ensure_experience(session)
    )

    assert binding.session_id == session["id"]
    assert (
        str(binding.experience_id)
        == str(experience.experience_id)
    )

    session = service.sessions.bind_experience(
        session["id"],
        str(experience.experience_id),
    )

    raw_inputs = (
        (
            "HUMAN",
            "first",
            "",
            "",
        ),
        (
            "AI",
            "second",
            "provider-alpha",
            "model-alpha",
        ),
        (
            "HUMAN",
            "third-" + ("x" * 400),
            "",
            "",
        ),
    )

    for sequence, (
        actor,
        content,
        provider,
        model,
    ) in enumerate(raw_inputs, start=1):
        source_item = (
            service.conversation_experience.raw_source(
                session=session,
                experience=experience,
                actor=actor,
                content=content,
                sequence=sequence,
                provider=provider,
                model=model,
            )
        )

        session = service.sessions.append_raw_source(
            session["id"],
            source_item,
        )

    persisted = service.sessions.get(session["id"])

    assert persisted["experience_id"] == str(
        experience.experience_id
    )
    assert len(persisted["raw_sources"]) == 3

    reconstructor = ConversationContextReconstructor(
        tmp_path,
        tmp_path,
        max_raw_sources=2,
        max_source_chars=256,
    )

    context = reconstructor.build(
        session["id"]
    )

    assert context["schema"] == (
        "FUSION-02-CONVERSATION-CONTEXT-1"
    )
    assert context["bounded"] == {
        "max_raw_sources": 2,
        "max_source_chars": 256,
        "raw_sources_included": 2,
    }

    sources = context["conversation"]["sources"]

    assert len(sources) == 2
    assert [
        item["sequence"]
        for item in sources
    ] == [2, 3]
    assert [
        item["actor"]
        for item in sources
    ] == ["AI", "HUMAN"]

    assert sources[0]["content"] == "second"
    assert sources[0]["content_truncated"] is False

    assert len(sources[1]["content"]) == 256
    assert sources[1]["content_truncated"] is True
    assert sources[1]["original_content_chars"] > 256

    assert context[
        "persistent_experience"
    ]["experience_id"] == str(
        experience.experience_id
    )

    assert context["active_session"]["session_id"] == (
        session["id"]
    )

    assert context["ai_partner"] == {
        "provider": "provider-alpha",
        "model": "model-alpha",
    }

    provenance = context["provenance"]["sources"]

    assert [
        item["sequence"]
        for item in provenance
    ] == [2, 3]
    assert provenance[0]["event_id"] == (
        sources[0]["event_id"]
    )
    assert provenance[1]["event_id"] == (
        sources[1]["event_id"]
    )

    for item in provenance:
        status = item["epistemic_status"]

        assert status["raw_source"] is True
        assert status["evidence"] is False
        assert status["canon"] is False
        assert status["automatic_authority"] is False

    boundaries = context["epistemic_boundaries"]

    assert boundaries[
        "raw_conversation_is_evidence"
    ] is False
    assert boundaries[
        "raw_conversation_is_canon"
    ] is False
    assert boundaries[
        "ai_statement_is_evidence"
    ] is False
    assert boundaries[
        "automatic_sedimentation"
    ] is False
    assert boundaries[
        "human_authority_preserved"
    ] is True

    assert context["organism"][
        "human_authority"
    ]["preserved"] is True

    serialized = json.dumps(
        context,
        sort_keys=True,
    )

    assert "first" not in serialized
    assert "second" in serialized
    assert len(serialized) > 0

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

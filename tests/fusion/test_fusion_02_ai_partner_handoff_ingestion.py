from __future__ import annotations

import hashlib
from pathlib import Path

from python.ai_platform.conversation_context import (
    ConversationContextReconstructor,
)
from python.ai_platform.service import AIPlatformService
from python.ai_platform.sessions import AISessionEngine


def _write_handoff(root: Path, content: str = "handoff evidence") -> Path:
    path = (
        root
        / "work"
        / "implementation-reports"
        / "FUSION"
        / "FUSION_02_CHATGPT_AI_PARTNER_HANDOFF_001.md"
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


def test_bind_experience_attaches_handoff_reference_to_existing_session(
    tmp_path,
):
    handoff = _write_handoff(
        tmp_path,
        "Human authority governs. AI material is evidence input.",
    )

    sessions = AISessionEngine(str(tmp_path))
    sessions.create({"id": "session-handoff"})

    attached = sessions.bind_experience(
        "session-handoff",
        "EXP-HANDOFF",
    )

    sources = attached["engineering_context"]["handoff_sources"]
    assert len(sources) == 1
    assert sources[0]["path"] == str(handoff.relative_to(tmp_path))
    assert sources[0]["classification"] == (
        "PROVENANCE_BEARING_HANDOFF_EVIDENCE"
    )
    assert sources[0]["source_semantics"] == "EVIDENCE_INPUT_NOT_AUTHORITY"
    assert sources[0]["human_authority_preserved"] is True
    assert sources[0]["automatic_canon_promotion"] is False
    assert sources[0]["automatic_memory_promotion"] is False
    assert "Human authority governs" not in repr(sources)


def test_reconstructor_materializes_attached_handoff_with_integrity(
    tmp_path,
    monkeypatch,
):
    content = (
        "# Handoff\n\n"
        "Human final authority: Marian.\n"
        "AI proposals remain proposals until accepted.\n"
    )
    handoff = _write_handoff(tmp_path, content)
    digest = hashlib.sha256(content.encode("utf-8")).hexdigest()

    reconstructor = ConversationContextReconstructor(tmp_path)

    recovered = {
        "session_id": "session-handoff",
        "project": "AI-Toolkit",
        "repository": "AI-Toolkit",
        "experience": {
            "experience_id": "EXP-HANDOFF",
            "state": "ACTIVE",
            "recovered": True,
        },
        "raw_sources": [],
        "engineering_context": {
            "handoff_sources": [
                {
                    "path": str(handoff.relative_to(tmp_path)),
                    "content_sha256": digest,
                    "classification": (
                        "PROVENANCE_BEARING_HANDOFF_EVIDENCE"
                    ),
                    "source_semantics": "EVIDENCE_INPUT_NOT_AUTHORITY",
                    "human_authority_preserved": True,
                }
            ]
        },
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
            "layered_memory": {},
            "persistent_experience": {},
            "provenance": {},
            "error_memory": {},
            "human_authority": {"preserved": True},
            "migration_boundaries": {},
        },
    )
    monkeypatch.setattr(
        reconstructor.base_context_builder,
        "build",
        lambda: {
            "repository_profile": {},
            "repository_health": {},
            "current_branch": "main",
            "current_sprint": "",
            "current_epic": "FUSION-02",
            "current_issue": "",
            "runtime_status": {},
            "workspace": {"workspace": "/workspace"},
        },
    )

    context = reconstructor.build("session-handoff")
    source = context["handoff"]["sources"][0]

    assert source["content"] == content
    assert source["integrity_verified"] is True
    assert context["handoff"]["source_count"] == 1
    assert context["handoff"]["epistemic_status"]["evidence_input"] is True
    assert context["handoff"]["epistemic_status"]["canon"] is False
    assert context["handoff"]["epistemic_status"]["layered_memory"] is False
    assert context["handoff"]["epistemic_status"]["automatic_authority"] is False
    assert context["epistemic_boundaries"]["handoff_context_grants_authority"] is False
    assert context["epistemic_boundaries"]["human_authority_preserved"] is True


def test_reconstructor_refuses_unverified_handoff_content(
    tmp_path,
    monkeypatch,
):
    handoff = _write_handoff(tmp_path, "changed content")
    reconstructor = ConversationContextReconstructor(tmp_path)

    recovered = {
        "session_id": "session-handoff",
        "project": "AI-Toolkit",
        "repository": "AI-Toolkit",
        "experience": {},
        "raw_sources": [],
        "engineering_context": {
            "handoff_sources": [
                {
                    "path": str(handoff.relative_to(tmp_path)),
                    "content_sha256": "0" * 64,
                }
            ]
        },
    }

    monkeypatch.setattr(
        reconstructor.organism,
        "conversation_session",
        lambda session_id: recovered,
    )
    monkeypatch.setattr(
        reconstructor.organism,
        "state",
        lambda: {"schema": "organism"},
    )
    monkeypatch.setattr(
        reconstructor.base_context_builder,
        "build",
        lambda: {
            "repository_profile": {},
            "repository_health": {},
            "current_branch": "main",
            "runtime_status": {},
            "workspace": {},
        },
    )

    source = reconstructor.build("session-handoff")["handoff"]["sources"][0]
    assert source["integrity_verified"] is False
    assert source["integrity_error"] == "CONTENT_SHA256_MISMATCH"
    assert source["content"] == ""


def test_service_delivers_verified_handoff_to_provider_boundary(
    tmp_path,
    monkeypatch,
):
    marker = "HANDOFF-PROVIDER-BOUNDARY-MARKER"
    content = (
        "# AI Partner handoff\n\n"
        "Human final authority is preserved.\n"
        f"{marker}\n"
    )
    _write_handoff(tmp_path, content)

    service = AIPlatformService(
        repository_root=str(tmp_path),
        workspace_root=str(tmp_path),
    )

    # Keep repository/runtime projection deterministic while preserving the
    # real durable session -> Experience -> handoff -> reconstructor path.
    monkeypatch.setattr(
        service.conversation_context.base_context_builder,
        "build",
        lambda: {
            "repository_profile": {},
            "repository_health": {},
            "current_branch": "main",
            "current_sprint": "",
            "current_epic": "FUSION-02",
            "current_issue": "",
            "runtime_status": {},
            "workspace": {"workspace": str(tmp_path)},
        },
    )
    monkeypatch.setattr(
        service.conversation_context.organism,
        "state",
        lambda: {
            "schema": "organism",
            "layered_memory": {},
            "persistent_experience": {},
            "provenance": {},
            "error_memory": {},
            "human_authority": {"preserved": True},
            "migration_boundaries": {},
        },
    )

    captured = {}

    def provider_boundary(
        question,
        settings,
        *,
        provider_id="",
        model="",
        context_override=None,
    ):
        captured["context"] = context_override
        return {
            "answer": "acknowledged",
            "provider": provider_id or "test-provider",
            "model": model or "test-model",
            "usage": {},
        }

    monkeypatch.setattr(service.pipeline, "run", provider_boundary)

    result = service.ask_repository(
        "acknowledge the inherited handoff",
        provider_id="test-provider",
        model="test-model",
    )

    provider_context = captured["context"]
    handoff = provider_context["handoff"]

    assert result["answer"] == "acknowledged"
    assert handoff["source_count"] == 1
    assert marker in handoff["sources"][0]["content"]
    assert handoff["sources"][0]["integrity_verified"] is True
    assert handoff["epistemic_status"]["canon"] is False
    assert handoff["epistemic_status"]["layered_memory"] is False
    assert handoff["epistemic_status"]["automatic_authority"] is False
    assert (
        provider_context["epistemic_boundaries"][
            "handoff_context_grants_authority"
        ]
        is False
    )
    assert (
        provider_context["epistemic_boundaries"][
            "human_authority_preserved"
        ]
        is True
    )

    sessions = service.sessions.list_sessions()
    assert len(sessions) == 1
    references = sessions[0]["engineering_context"]["handoff_sources"]
    assert marker not in repr(references)
    assert references[0]["content_sha256"] == hashlib.sha256(
        content.encode("utf-8")
    ).hexdigest()


def test_existing_service_sequence_attaches_before_context_reconstruction():
    source = Path("lib/python/ai_platform/service.py").read_text(encoding="utf-8")

    bind = source.index("self.sessions.bind_experience")
    reconstruct = source.index("self.conversation_context.build", bind)

    assert bind < reconstruct


def test_handoff_ingestion_creates_no_parallel_memory_or_session_anatomy():
    sessions_source = Path("lib/python/ai_platform/sessions.py").read_text(
        encoding="utf-8"
    )
    context_source = Path(
        "lib/python/ai_platform/conversation_context.py"
    ).read_text(encoding="utf-8")

    forbidden = (
        "class HandoffMemory",
        "class HandoffSession",
        "class HandoffRepository",
        "class AIPartnerMemory",
    )

    for token in forbidden:
        assert token not in sessions_source
        assert token not in context_source

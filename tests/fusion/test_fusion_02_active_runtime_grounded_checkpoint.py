import hashlib
import json
import os
from contextlib import contextmanager

import pytest

from python.ai_platform.service import AIPlatformService
from python.dashboard.service import EngineeringDashboardService
from python.runtime.identity import RuntimeIdentity


REPOSITORY = "caliofmarian-ai/AI-Toolkit"
BRANCH = "fusion-02/mock-free-physiology-recovery"
COMMIT = "a" * 40
SOURCE_PATH = "work/runtime-grounding.txt"
SENTINEL = (
    "FUSION02_RUNTIME_GROUNDING_SENTINEL="
    "ACTIVE-PREVIEW-BYTES-VERIFIED"
)


@contextmanager
def scoped_environment(values):
    previous = {
        key: os.environ.get(key)
        for key in values
    }

    try:
        for key, value in values.items():
            os.environ[key] = value
        yield
    finally:
        for key, value in previous.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value


def railway_environment():
    return {
        "RAILWAY_ENVIRONMENT": "fusion02-grounded-preview",
        "RAILWAY_ENVIRONMENT_ID": "environment-preview",
        "RAILWAY_PROJECT_ID": "project-ai-toolkit",
        "RAILWAY_SERVICE_ID": "service-ai-toolkit",
        "RAILWAY_DEPLOYMENT_ID": "deployment-preview",
        "RAILWAY_GIT_REPO_OWNER": "caliofmarian-ai",
        "RAILWAY_GIT_REPO_NAME": "AI-Toolkit",
        "RAILWAY_GIT_BRANCH": BRANCH,
        "RAILWAY_GIT_COMMIT_SHA": COMMIT,
    }


def complete_retrieval():
    content = SENTINEL + "\n"
    raw = content.encode("utf-8")
    blob_header = f"blob {len(raw)}\0".encode("ascii")
    blob_sha = hashlib.sha1(blob_header + raw).hexdigest()
    content_sha256 = hashlib.sha256(raw).hexdigest()
    observation = {
        "source_path": SOURCE_PATH,
        "status": "RETRIEVED",
        "content": content,
        "repository_identity": REPOSITORY,
        "requested_branch": BRANCH,
        "requested_commit": COMMIT,
        "resolved_commit": COMMIT,
        "branch_head_commit": COMMIT,
        "blob_sha": blob_sha,
        "byte_count": len(raw),
        "character_count": len(content),
        "content_sha256": content_sha256,
        "blob_sha_verified": True,
        "complete_file": True,
        "content_complete": True,
    }

    return {
        "checkpoint_identity": {
            "repository": REPOSITORY,
            "requested_branch": BRANCH,
            "requested_commit": COMMIT,
            "resolved_commit": COMMIT,
            "branch_head_commit": COMMIT,
            "branch_head_matches_commit": True,
            "requested_path_count": 1,
            "retrieved_path_count": 1,
            "complete_files": True,
            "status": "RETRIEVED",
            "read_only": True,
            "authority_conferred": False,
            "human_authority_preserved": True,
        },
        "read_observations": [observation],
    }


def working_context(retrieval):
    observation = retrieval["read_observations"][0]

    return {
        "evidence": [
            {
                key: observation[key]
                for key in (
                    "source_path",
                    "blob_sha",
                    "byte_count",
                    "character_count",
                    "content_sha256",
                    "blob_sha_verified",
                    "content_complete",
                )
            }
        ]
    }


def pipeline_result(*, semantic_model_execution):
    return {
        "full_file_reading": {
            "schema": "FUSION-02-COMPLETE-FILE-READING-1",
            "mode": "SINGLE_CONTEXT_COMPLETE",
            "file_count": 1,
            "files_delivered": 1,
            "all_segments_delivered": True,
            "raw_content_truncated": False,
        },
        "provider_execution": {
            "schema": "FUSION-02-PROVIDER-EXECUTION-1",
            "provider": (
                "openai"
                if semantic_model_execution
                else "anthropic"
            ),
            "model": (
                "gpt-4.1"
                if semantic_model_execution
                else "claude-sonnet-4.5"
            ),
            "adapter": (
                "OpenAIProviderAdapter"
                if semantic_model_execution
                else "StaticProviderAdapter"
            ),
            "execution_kind": (
                "EXTERNAL_HTTPS"
                if semantic_model_execution
                else "STATIC_DETERMINISTIC"
            ),
            "external_network_execution": semantic_model_execution,
            "semantic_model_execution": semantic_model_execution,
        },
    }


def test_provider_execution_kind_distinguishes_static_and_external(
    tmp_path,
):
    service = AIPlatformService(str(tmp_path))
    static_adapter = service.registry.adapter("anthropic")
    external_adapter = service.registry.adapter("openai")

    assert static_adapter.execution_kind == "STATIC_DETERMINISTIC"
    assert static_adapter.external_network_execution is False
    assert static_adapter.semantic_model_execution is False
    assert external_adapter.execution_kind == "EXTERNAL_HTTPS"
    assert external_adapter.external_network_execution is True
    assert external_adapter.semantic_model_execution is True


def test_active_runtime_identity_comes_from_server_environment():
    with scoped_environment(railway_environment()):
        service_identity = (
            AIPlatformService.runtime_deployment_identity()
        )
        runtime_identity = RuntimeIdentity.create().to_dict()

    assert service_identity["status"] == "DEMONSTRATED"
    assert service_identity["identity_complete"] is True
    assert service_identity["repository"] == REPOSITORY
    assert service_identity["git_branch"] == BRANCH
    assert service_identity["git_commit"] == COMMIT
    assert runtime_identity["git_branch"] == BRANCH
    assert runtime_identity["git_commit"] == COMMIT


def test_checkpoint_integrity_rejects_any_incomplete_file():
    retrieval = complete_retrieval()

    assert AIPlatformService.checkpoint_integrity_issues(
        retrieval
    ) == []

    retrieval["read_observations"][0]["content_complete"] = False

    assert (
        "checkpoint-observation-1-content-incomplete"
        in AIPlatformService.checkpoint_integrity_issues(retrieval)
    )


def test_system_attestation_proves_transport_not_narrative_truth():
    retrieval = complete_retrieval()

    with scoped_environment(railway_environment()):
        attestation = AIPlatformService.access_attestation(
            retrieval=retrieval,
            working_context=working_context(retrieval),
            pipeline_result=pipeline_result(
                semantic_model_execution=True
            ),
        )

    assert attestation["status"] == "DEMONSTRATED"
    assert attestation["verification"] == {
        "checkpoint_complete": True,
        "checkpoint_integrity_issues": [],
        "file_manifests_verified": True,
        "provider_delivery_complete": True,
        "runtime_matches_checkpoint": True,
        "external_semantic_execution": True,
    }
    assert attestation["file_manifests"][0][
        "source_path"
    ] == SOURCE_PATH
    assert "content" not in attestation["file_manifests"][0]
    assert attestation["provider_narrative"] == {
        "epistemic_status": "RAW_SOURCE_NOT_EVIDENCE",
        "factual_grounding": "NOT_DEMONSTRATED",
        "self_report_is_attestation": False,
    }
    assert attestation["authority_conferred"] is False
    assert attestation["human_authority_preserved"] is True


def test_access_attestation_persists_with_ai_raw_source(tmp_path):
    service = AIPlatformService(str(tmp_path))
    session = service.sessions.create(
        {
            "project": "AI-Toolkit",
            "repository": REPOSITORY,
        }
    )
    experience, _binding = (
        service.conversation_experience.ensure_experience(session)
    )
    session = service.sessions.bind_experience(
        session["id"],
        str(experience.experience_id),
    )
    human = service.conversation_experience.raw_source(
        session=session,
        experience=experience,
        actor="HUMAN",
        content="Inspect the exact checkpoint",
        sequence=1,
    )
    session = service.sessions.append_raw_source(
        session["id"],
        human,
    )
    retrieval = complete_retrieval()

    with scoped_environment(railway_environment()):
        attestation = service.access_attestation(
            retrieval=retrieval,
            working_context=working_context(retrieval),
            pipeline_result=pipeline_result(
                semantic_model_execution=True
            ),
        )

    ai_source = service.conversation_experience.raw_source(
        session=session,
        experience=experience,
        actor="AI",
        content="Provider narrative remains a raw source.",
        sequence=2,
        provider="openai",
        model="gpt-4.1",
        access_attestation=attestation,
    )
    service.sessions.append_raw_source(
        session["id"],
        ai_source,
    )
    recovered = service.sessions.get(session["id"])

    assert recovered["raw_sources"][1][
        "access_attestation"
    ] == attestation
    assert recovered["raw_sources"][1][
        "source_semantics"
    ] == "RAW_SOURCE_NOT_EVIDENCE"
    json.dumps(recovered)


def test_owner_ui_separates_system_attestation_from_model_text(
    tmp_path,
):
    with scoped_environment(
        {"ANTHROPIC_API_KEY": "static-display-only"}
    ):
        dashboard = EngineeringDashboardService(
            repository_root=str(tmp_path),
            workspace_root=str(tmp_path),
        )
        html = dashboard._owner_ai_chat_panel(
            dashboard.ai_platform.control_center()
        )

    assert "SYSTEM-GENERATED ACCESS ATTESTATION" in html
    assert "NOT MODEL TEXT" in html
    assert "x.access_attestation" in html
    assert "JSON.stringify(value,null,2)" in html
    assert "chat-attestation" in html
    assert "STATIC_DETERMINISTIC" in html


@pytest.mark.skipif(
    os.environ.get("AI_TOOLKIT_LIVE_GITHUB_CHECKPOINT") != "1",
    reason="separate live public GitHub acceptance",
)
def test_partial_live_checkpoint_fails_closed_before_ai_source(
    tmp_path,
):
    question = f"""Inspect this exact repository checkpoint.

Repository: `caliofmarian-ai/AI-Toolkit`
Branch: `{BRANCH}`
Commit: `d0b3d694cbb08ba5982e4ce8a3f746b7a40f7134`
Source: `work/implementation-reports/FUSION/FUSION_02_AI_PARTNER_HANDOFF_012.md`
Source: `work/implementation-reports/FUSION`
"""
    service = AIPlatformService(
        repository_root=str(tmp_path),
        workspace_root=str(tmp_path),
    )

    with pytest.raises(
        ValueError,
        match="repository checkpoint access is incomplete",
    ):
        service.ask_repository(
            question,
            provider_id="anthropic",
            model="claude-sonnet-4.5",
        )

    sessions = service.sessions.list_sessions()

    assert len(sessions) == 1
    assert [
        item["actor"]
        for item in sessions[0]["raw_sources"]
    ] == ["HUMAN"]
    assert sessions[0]["journey_reference"][
        "status"
    ] == "INTERRUPTED"
    assert sessions[0]["journey_reference"][
        "stopping_reason"
    ].startswith("checkpoint-failure:")


# The live preview verifier reads this exact complete file and must recover
# the sentinel without receiving its value in the Human question.
RUNTIME_GROUNDING_SENTINEL = SENTINEL

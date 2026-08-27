import hashlib
import os
import re

import pytest

from python.ai_platform.cognitive_coordination import WorkingContext
from python.ai_platform.service import AIPlatformService
from python.evidence_engine.engine import EvidenceEngine


REPOSITORY = "caliofmarian-ai/AI-Toolkit"
BRANCH = "fusion-02/mock-free-physiology-recovery"
COMMIT = "9540326d655162dbbe6e0b3d0fd22d3cf54418f3"
HANDOFF = (
    "work/implementation-reports/FUSION/"
    "FUSION_02_AI_PARTNER_HANDOFF_011.md"
)
LARGE_FILE = (
    "work/implementation-reports/FUSION/"
    "FUSION_02_TERMUX_EXECUTION_ERROR_MEMORY.md"
)
DIRECTORY = "work/implementation-reports/FUSION"


def checkpoint_question(*paths):
    requested_paths = "\n".join(
        f"Source: `{path}`"
        for path in paths
    )

    return f"""Inspect this exact repository checkpoint.

Repository: `{REPOSITORY}`
Branch: `{BRANCH}`
Commit: `{COMMIT}`
{requested_paths}
"""


def complete_working_context(content):
    encoded = content.encode("utf-8")
    content_sha256 = hashlib.sha256(encoded).hexdigest()

    return WorkingContext(
        schema="FUSION-02-WORKING-CONTEXT-1",
        need_id="need-complete-file",
        journey_id="journey-complete-file",
        status="MATERIALIZED",
        human_question="Read the complete file",
        constraints={
            "human_authority_preserved": True,
            "retrieval_confers_authority": False,
        },
        source_identity_kind="repository-relative-path",
        source_paths=("work/complete-file.md",),
        evidence=(
            {
                "source_path": "work/complete-file.md",
                "source_identity_kind": "repository-relative-path",
                "families": ["docs"],
                "read_status": "RETRIEVED",
                "content": content,
                "repository_identity": REPOSITORY,
                "requested_commit": COMMIT,
                "resolved_commit": COMMIT,
                "blob_sha": "1" * 40,
                "byte_count": len(encoded),
                "character_count": len(content),
                "content_sha256": content_sha256,
                "blob_sha_verified": True,
                "complete_file": True,
                "content_complete": True,
                "read_only": True,
                "bounded": True,
                "authority_conferred": False,
            },
        ),
        provenance=(
            {
                "source_path": "work/complete-file.md",
                "source_identity_kind": "repository-relative-path",
                "retrieval_capability": "read-checkpoint",
                "repository_identity": REPOSITORY,
                "requested_commit": COMMIT,
                "resolved_commit": COMMIT,
                "blob_sha": "1" * 40,
                "byte_count": len(encoded),
                "character_count": len(content),
                "content_sha256": content_sha256,
                "blob_sha_verified": True,
                "complete_file": True,
                "content_complete": True,
                "authority_conferred": False,
            },
        ),
        epistemic_results=(
            {
                "identity": "work/complete-file.md",
                "source_path": "work/complete-file.md",
                "epistemic_class": "COMMITTED_REPOSITORY_EVIDENCE",
                "authority": "TECHNICAL_OBSERVATION",
            },
        ),
        semantic_identities=(),
        epistemic_classes=("COMMITTED_REPOSITORY_EVIDENCE",),
        uncertainties=(),
        relationships=(),
        journey_summary={
            "status": "PARTIAL",
            "step_count": 1,
            "epistemic_gain": True,
            "stopping_reason": "COMPLETE_FILE_AVAILABLE",
        },
        authority_conferred=False,
        human_authority_preserved=True,
        unknown_is_valid=True,
        bounded=True,
    )


def test_explicit_checkpoint_coordinates_are_parsed_without_guessing():
    request = EvidenceEngine._checkpoint_request(
        checkpoint_question(HANDOFF, LARGE_FILE)
    )

    assert request == {
        "repository": REPOSITORY,
        "branch": BRANCH,
        "commit": COMMIT,
        "paths": [HANDOFF, LARGE_FILE],
    }

    assert EvidenceEngine._checkpoint_request(
        "inspect some repository"
    ) is None

    traversal = checkpoint_question("work/../outside.md")

    assert EvidenceEngine._checkpoint_request(traversal) is None


def test_complete_text_segmentation_is_lossless_and_unlimited_by_file_size():
    content = ("anatomy-αβγ\n" * 5_000) + "FINAL-BYTE"
    segments = EvidenceEngine._lossless_text_segments(content)

    assert len(content) > 16_000
    assert len(segments) > 1
    assert "".join(item["content"] for item in segments) == content
    assert segments[0]["character_start"] == 0
    assert segments[-1]["character_end"] == len(content)
    assert segments[-1]["byte_end"] == len(content.encode("utf-8"))
    assert [item["segment_index"] for item in segments] == list(
        range(1, len(segments) + 1)
    )


def test_checkpoint_status_distinguishes_complete_partial_and_unavailable():
    assert EvidenceEngine._checkpoint_status(
        [{"status": "RETRIEVED"}, {"status": "RETRIEVED"}]
    ) == "RETRIEVED"
    assert EvidenceEngine._checkpoint_status(
        [{"status": "RETRIEVED"}, {"status": "UNKNOWN"}]
    ) == "PARTIAL"
    assert EvidenceEngine._checkpoint_status(
        [{"status": "UNKNOWN"}]
    ) == "NOT_AVAILABLE"


def test_pipeline_delivers_every_segment_when_one_context_cannot_hold_file(
    tmp_path,
):
    content = ("complete-file-physiology\n" * 6_000) + "FINAL-BYTE"
    working_context = complete_working_context(content)
    service = AIPlatformService(str(tmp_path))

    result = service.pipeline.run(
        "Inspect the entire file",
        service.settings.load(),
        provider_id="ollama",
        model="llama3.1",
        working_context=working_context,
    )

    reading = result["full_file_reading"]
    expected_sha256 = hashlib.sha256(
        content.encode("utf-8")
    ).hexdigest()

    assert reading["mode"] == "SEQUENTIAL_COMPLETE"
    assert reading["segment_count"] > 1
    assert reading["segments_delivered"] == reading["segment_count"]
    assert reading["all_segments_delivered"] is True
    assert reading["raw_content_truncated"] is False
    assert reading["delivered_by_path"] == {
        "work/complete-file.md": reading["segment_count"]
    }
    assert reading["delivered_content_sha256_by_path"] == {
        "work/complete-file.md": expected_sha256
    }
    assert reading["provider_calls"] > reading["segment_count"]
    assert reading["authority_conferred"] is False
    assert reading["human_authority_preserved"] is True


@pytest.mark.skipif(
    os.environ.get("AI_TOOLKIT_LIVE_GITHUB_CHECKPOINT") != "1",
    reason="separate live public GitHub acceptance",
)
def test_complete_file_transport_reaches_registered_static_adapter(
    tmp_path,
):
    service = AIPlatformService(
        repository_root=str(tmp_path),
        workspace_root=str(tmp_path),
    )

    result = service.ask_repository(
        checkpoint_question(HANDOFF, LARGE_FILE),
        provider_id="anthropic",
        model="claude-sonnet-4.5",
    )

    checkpoint = result["repository_checkpoint"]

    assert checkpoint["repository"] == REPOSITORY
    assert checkpoint["requested_branch"] == BRANCH
    assert checkpoint["requested_commit"] == COMMIT
    assert checkpoint["resolved_commit"] == COMMIT
    assert re.fullmatch(
        r"[0-9a-f]{40}",
        checkpoint["branch_head_commit"],
    )
    assert checkpoint["branch_head_matches_commit"] is (
        checkpoint["branch_head_commit"] == COMMIT
    )
    assert checkpoint["requested_path_count"] == 2
    assert checkpoint["retrieved_path_count"] == 2
    assert checkpoint["complete_files"] is True
    assert checkpoint["status"] == "RETRIEVED"

    evidence_by_path = {
        item["source_path"]: item
        for item in result["working_context"]["evidence"]
    }
    large = evidence_by_path[LARGE_FILE]

    assert large["content_complete"] is True
    assert large["complete_file"] is True
    assert large["blob_sha_verified"] is True
    assert large["character_count"] > 16_000
    assert len(large["content"]) == large["character_count"]
    assert large["content"].endswith(
        "never transform retrieved evidence into Canon or Human Authority.\n"
    )
    assert hashlib.sha256(
        large["content"].encode("utf-8")
    ).hexdigest() == large["content_sha256"]

    reading = result["full_file_reading"]
    assert reading["mode"] == "SINGLE_CONTEXT_COMPLETE"
    assert reading["all_segments_delivered"] is True
    assert reading["raw_content_truncated"] is False
    assert reading["files_delivered"] == 2
    assert reading["delivered_content_sha256_by_path"][LARGE_FILE] == (
        large["content_sha256"]
    )
    assert result["provider_execution"] == {
        "schema": "FUSION-02-PROVIDER-EXECUTION-1",
        "provider": "anthropic",
        "model": "claude-sonnet-4.5",
        "adapter": "StaticProviderAdapter",
        "execution_kind": "STATIC_DETERMINISTIC",
        "external_network_execution": False,
        "semantic_model_execution": False,
    }
    assert result["access_attestation"][
        "verification"
    ]["external_semantic_execution"] is False


@pytest.mark.skipif(
    os.environ.get("AI_TOOLKIT_LIVE_GITHUB_CHECKPOINT") != "1",
    reason="separate live public GitHub acceptance",
)
def test_directory_is_rejected_and_mixed_paths_are_partial():
    result = EvidenceEngine(".").find_github_checkpoint(
        checkpoint_question(HANDOFF, DIRECTORY)
    )

    assert result["checkpoint_identity"]["status"] == "PARTIAL"
    assert result["checkpoint_identity"]["requested_path_count"] == 2
    assert result["checkpoint_identity"]["retrieved_path_count"] == 1
    assert result["source_paths"] == [HANDOFF]

    directory_observation = next(
        item
        for item in result["read_observations"]
        if item["source_path"] == DIRECTORY
    )

    assert directory_observation["status"] == "UNKNOWN"
    assert directory_observation["complete_file"] is False
    assert directory_observation["content_complete"] is False
    assert "requested-path-is-not-a-file" in directory_observation[
        "uncertainty"
    ]

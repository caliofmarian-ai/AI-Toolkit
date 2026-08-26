import os

import pytest

from python.ai_platform.service import AIPlatformService
from python.evidence_engine.engine import EvidenceEngine


REPOSITORY = "caliofmarian-ai/AI-Toolkit"
BRANCH = "fusion-02/mock-free-physiology-recovery"
COMMIT = "4baa82b3fb5446f75a72039684e2a2a601d92340"
HANDOFF = (
    "work/implementation-reports/FUSION/"
    "FUSION_02_AI_PARTNER_HANDOFF_010.md"
)


def checkpoint_question():
    return f"""Inspect this exact repository checkpoint.

Repository: `{REPOSITORY}`
Branch: `{BRANCH}`
Commit: `{COMMIT}`
Handoff: `{HANDOFF}`
"""


def test_explicit_checkpoint_coordinates_are_parsed_without_guessing():
    request = EvidenceEngine._checkpoint_request(
        checkpoint_question()
    )

    assert request == {
        "repository": REPOSITORY,
        "branch": BRANCH,
        "commit": COMMIT,
        "paths": [HANDOFF],
    }

    assert EvidenceEngine._checkpoint_request(
        "inspect some repository"
    ) is None

    traversal = checkpoint_question().replace(
        HANDOFF,
        "work/../outside.md",
    )

    assert EvidenceEngine._checkpoint_request(
        traversal
    ) is None


@pytest.mark.skipif(
    os.environ.get(
        "AI_TOOLKIT_LIVE_GITHUB_CHECKPOINT"
    ) != "1",
    reason="separate live public GitHub acceptance",
)
def test_ai_partner_receives_exact_live_github_checkpoint(tmp_path):
    service = AIPlatformService(
        repository_root=str(tmp_path),
        workspace_root=str(tmp_path),
    )

    result = service.ask_repository(
        checkpoint_question(),
        provider_id="anthropic",
        model="claude-sonnet-4.5",
    )

    checkpoint = result["repository_checkpoint"]

    assert checkpoint["repository"] == REPOSITORY
    assert checkpoint["requested_branch"] == BRANCH
    assert checkpoint["requested_commit"] == COMMIT
    assert checkpoint["resolved_commit"] == COMMIT
    assert checkpoint["branch_head_commit"] == COMMIT
    assert checkpoint["branch_head_matches_commit"] is True
    assert checkpoint["status"] == "RETRIEVED"
    assert checkpoint["read_only"] is True
    assert checkpoint["authority_conferred"] is False
    assert checkpoint["human_authority_preserved"] is True

    working = result["working_context"]

    assert working["source_paths"] == [HANDOFF]
    assert working["authority_conferred"] is False
    assert working["human_authority_preserved"] is True
    assert len(working["evidence"]) == 1

    evidence = working["evidence"][0]

    assert evidence["source_path"] == HANDOFF
    assert evidence["read_status"] == "RETRIEVED"
    assert evidence["repository_identity"] == REPOSITORY
    assert evidence["requested_branch"] == BRANCH
    assert evidence["requested_commit"] == COMMIT
    assert evidence["resolved_commit"] == COMMIT
    assert evidence["blob_sha"]
    assert evidence["byte_count"] > 0
    assert evidence["content_complete"] is True
    assert "FUSION-02 AI Partner Handoff 010" in evidence["content"]
    assert "Human Authority: Marian Caliof" in evidence["content"]

    provenance = working["provenance"][0]

    assert provenance["repository_identity"] == REPOSITORY
    assert provenance["requested_commit"] == COMMIT
    assert provenance["resolved_commit"] == COMMIT
    assert provenance["blob_sha"] == evidence["blob_sha"]
    assert provenance["byte_count"] == evidence["byte_count"]

    assert result["raw_source_count"] == 2
    assert result["epistemic_status"][
        "retrieval_confers_authority"
    ] is False
    assert result["epistemic_status"][
        "human_authority_preserved"
    ] is True

from __future__ import annotations

import ast
import json
import subprocess
from pathlib import Path

from python.ai_platform.context_builder import (
    AIContextBuilder,
)
from python.ai_platform.service import (
    AIPlatformService,
)


def repository_root():
    return Path(__file__).resolve().parents[2]


def serialized_size(value):
    return len(
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    )


def current_git_branch(root):
    return subprocess.run(
        [
            "git",
            "branch",
            "--show-current",
        ],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def test_real_permanent_orientation_is_bounded():
    root = repository_root()

    orientation = AIContextBuilder(
        repository_root=str(root),
        workspace_root=str(root.parent),
    ).build_permanent_orientation()

    assert orientation["schema"] == (
        "ai-toolkit/permanent-epistemic-orientation/v1"
    )
    assert orientation["organism"] == "AI-Toolkit"
    assert orientation["project"] == root.name
    assert orientation["current_branch"] == (
        current_git_branch(root)
    )

    assert "repository_profile" not in orientation
    assert "repository_health" not in orientation
    assert "technology_stack" not in orientation
    assert "dependencies" not in orientation
    assert "workspace" not in orientation
    assert "recent_reports" not in orientation
    assert "canonical_documents" not in orientation

    assert orientation["human_authority"] == {
        "authority": "human",
        "ai_may_promote_authority": False,
    }

    constraints = orientation["constraints"]

    assert constraints[
        "knowledge_availability_is_not_working_context"
    ] is True
    assert constraints[
        "retrieval_confers_authority"
    ] is False
    assert constraints[
        "semantic_identity_is_physical_location"
    ] is False
    assert constraints["navigation_read_only"] is True
    assert constraints["unknown_is_valid"] is True
    assert constraints[
        "full_repository_profile_default_payload"
    ] is False

    runtime = orientation["runtime_status"]

    assert set(runtime) == {
        "available",
        "state",
        "field_count",
        "fields",
        "fields_truncated",
        "values_materialized",
    }
    assert runtime["values_materialized"] is False
    assert len(runtime["fields"]) <= 32
    assert serialized_size(runtime) < 4096
    assert serialized_size(orientation) < 8192


def test_real_orientation_declares_existing_organs():
    root = repository_root()

    orientation = AIContextBuilder(
        repository_root=str(root),
        workspace_root=str(root.parent),
    ).build_permanent_orientation()

    assert orientation["available_organs"] == [
        "csl_uem",
        "canon",
        "knowledge_graph",
        "repository",
        "provenance",
        "layered_memory",
        "persistent_experience",
    ]

    assert orientation["navigation_capabilities"] == [
        "search",
        "resolve",
        "read",
        "inspect",
        "traverse",
        "trace_provenance",
    ]


def test_real_orientation_is_deterministic_and_read_only():
    root = repository_root()

    before = subprocess.run(
        ["git", "status", "--short"],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    ).stdout

    builder = AIContextBuilder(
        repository_root=str(root),
        workspace_root=str(root.parent),
    )

    first = builder.build_permanent_orientation()
    second = builder.build_permanent_orientation()

    after = subprocess.run(
        ["git", "status", "--short"],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    ).stdout

    assert first == second
    assert after == before


def test_orientation_organ_does_not_profile_repository():
    source_path = (
        repository_root()
        / "lib"
        / "python"
        / "ai_platform"
        / "context_builder.py"
    )

    tree = ast.parse(
        source_path.read_text(encoding="utf-8")
    )

    target = None

    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            if node.name != "AIContextBuilder":
                continue

            for item in node.body:
                if (
                    isinstance(item, ast.FunctionDef)
                    and item.name
                    == "build_permanent_orientation"
                ):
                    target = item
                    break

    assert target is not None

    names = {
        node.id
        for node in ast.walk(target)
        if isinstance(node, ast.Name)
    }

    attributes = {
        node.attr
        for node in ast.walk(target)
        if isinstance(node, ast.Attribute)
    }

    assert "RepositoryEngine" not in names
    assert "RepositoryProfileSerializer" not in names
    assert "profile" not in attributes


def test_real_ai_partner_receives_permanent_orientation(
    tmp_path,
):
    root = repository_root()
    durable = tmp_path / "durable-ai-partner"

    service = AIPlatformService(
        repository_root=str(root),
        workspace_root=str(root.parent),
        state_root=str(durable),
    )

    result = service.ask_repository(
        "inspect permanent epistemic orientation",
        provider_id="anthropic",
        model="claude-sonnet-4.5",
    )

    context = result["context"]
    orientation = context["permanent_orientation"]

    assert orientation["schema"] == (
        "ai-toolkit/permanent-epistemic-orientation/v1"
    )
    assert orientation["organism"] == "AI-Toolkit"
    assert orientation["project"] == root.name
    assert orientation["current_branch"] == (
        current_git_branch(root)
    )

    assert "working_context" in context
    assert "conversation" in context
    assert "repository_profile" not in orientation

    assert orientation["human_authority"][
        "authority"
    ] == "human"
    assert orientation["human_authority"][
        "ai_may_promote_authority"
    ] is False

    assert result["epistemic_status"][
        "retrieval_confers_authority"
    ] is False
    assert result["epistemic_status"][
        "human_authority_preserved"
    ] is True


def test_legacy_context_remains_real_and_available():
    root = repository_root()

    context = AIContextBuilder(
        repository_root=str(root),
        workspace_root=str(root.parent),
    ).build()

    assert "repository_profile" in context
    assert isinstance(
        context["repository_profile"],
        dict,
    )
    assert "repository_health" in context
    assert "workspace" in context

def test_runtime_orientation_never_exposes_nested_values():
    payload = {
        "runtime": {
            "state": "ACTIVE",
            "provider_secret": "MUST-NOT-LEAK",
            "nested": {
                "conversation": "MUST-NOT-LEAK",
            },
            "large_body": "x" * 100000,
        }
    }

    bounded = AIContextBuilder._bounded_runtime_orientation(
        payload
    )

    serialized = json.dumps(
        bounded,
        sort_keys=True,
    )

    assert bounded["available"] is True
    assert bounded["state"] == "ACTIVE"
    assert bounded["field_count"] == 4
    assert bounded["values_materialized"] is False
    assert "provider_secret" in bounded["fields"]
    assert "nested" in bounded["fields"]
    assert "MUST-NOT-LEAK" not in serialized
    assert ("x" * 100) not in serialized
    assert serialized_size(bounded) < 4096

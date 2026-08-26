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
    _fusion02_context_anatomy,
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
            default=str,
        ).encode("utf-8")
    )


def repository_status(root):
    return subprocess.run(
        ["git", "status", "--short"],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    ).stdout


def test_t1_real_builder_materializes_repository_profile():
    root = repository_root()

    context = AIContextBuilder(
        repository_root=str(root),
        workspace_root=str(root.parent),
    ).build()

    profile = context["repository_profile"]

    assert isinstance(profile, dict)
    assert profile
    assert "repository_health" in context
    assert "technology_stack" in context
    assert "dependencies" in context
    assert "workspace" in context

    assert context["repository_health"] == (
        profile.get("health_summary", {})
    )
    assert context["technology_stack"] == (
        profile.get("tech_stack", [])
    )
    assert context["dependencies"] == (
        profile.get("dependencies", {})
    )


def test_t1_real_pipeline_default_path_transports_profile():
    root = repository_root()

    service = AIPlatformService(
        repository_root=str(root),
        workspace_root=str(root.parent),
    )

    result = service.pipeline.run(
        question="characterize the real repository",
        settings=service.settings.load(),
        provider_id="anthropic",
        model="claude-sonnet-4.5",
    )

    context = result["context"]

    assert result["provider"] == "anthropic"
    assert result["model"] == "claude-sonnet-4.5"
    assert result["answer"]
    assert "repository_profile" in context
    assert context["repository_profile"]
    assert "repository_health" in context
    assert "technology_stack" in context
    assert "dependencies" in context


def test_t1_real_context_override_remains_authoritative():
    root = repository_root()

    service = AIPlatformService(
        repository_root=str(root),
        workspace_root=str(root.parent),
    )

    override = {
        "schema": "t1-real-override/v1",
        "bounded": True,
        "human_authority_preserved": True,
        "authority_conferred": False,
    }

    result = service.pipeline.run(
        question="use bounded context",
        settings=service.settings.load(),
        provider_id="anthropic",
        model="claude-sonnet-4.5",
        context_override=override,
    )

    assert result["context"] == override
    assert result["answer"]


def test_t1_real_context_anatomy_is_measurable():
    root = repository_root()

    context = AIContextBuilder(
        repository_root=str(root),
        workspace_root=str(root.parent),
    ).build()

    anatomy = _fusion02_context_anatomy(
        context
    )

    assert anatomy["total_serialized_bytes"] == (
        serialized_size(context)
    )
    assert anatomy["branch_count"] == len(context)
    assert anatomy[
        "estimated_tokens_at_4_bytes"
    ] > 0

    repository_profile = anatomy["branches"][
        "repository_profile"
    ]

    assert repository_profile["bytes"] > 0
    assert repository_profile["kind"] == "object"
    assert 0 < repository_profile["percent"] <= 100

    for branch in anatomy["branches"].values():
        assert set(branch) == {
            "bytes",
            "percent",
            "kind",
            "children",
        }


def test_t1_real_characterization_is_read_only():
    root = repository_root()
    before = repository_status(root)

    builder = AIContextBuilder(
        repository_root=str(root),
        workspace_root=str(root.parent),
    )

    first = builder.build()
    second = builder.build()

    after = repository_status(root)

    assert first["repository_profile"] == (
        second["repository_profile"]
    )
    assert after == before


def test_t1_production_characterization_contract_is_connected():
    root = repository_root()

    context_path = (
        root
        / "lib"
        / "python"
        / "ai_platform"
        / "context_builder.py"
    )
    pipeline_path = (
        root
        / "lib"
        / "python"
        / "ai_platform"
        / "pipeline.py"
    )

    context_tree = ast.parse(
        context_path.read_text(encoding="utf-8")
    )
    pipeline_tree = ast.parse(
        pipeline_path.read_text(encoding="utf-8")
    )

    context_calls = {
        node.func.attr
        for node in ast.walk(context_tree)
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
        )
    }

    pipeline_calls = {
        node.func.attr
        for node in ast.walk(pipeline_tree)
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
        )
    }

    assert "profile" in context_calls
    assert "build" in pipeline_calls
    assert "complete" in pipeline_calls

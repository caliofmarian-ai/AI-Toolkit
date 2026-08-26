from __future__ import annotations

import ast
import os
import subprocess
import sys
from pathlib import Path

import pytest

from python.ai_platform.adapters import (
    OpenAIProviderAdapter,
    ProviderCredentialError,
    ProviderExecutionError,
    ProviderResponseError,
    builtin_adapters,
)


def repository_root():
    return Path(__file__).resolve().parents[2]


def production_openai_adapter():
    adapters = [
        adapter
        for adapter in builtin_adapters()
        if (
            isinstance(
                adapter,
                OpenAIProviderAdapter,
            )
            and adapter.provider_id == "openai"
        )
    ]

    assert len(adapters) == 1
    return adapters[0]


def test_exact_production_openai_adapter_is_registered():
    adapter = production_openai_adapter()

    assert adapter.provider_id == "openai"
    assert adapter.descriptor.name == "OpenAI"
    assert adapter.descriptor.env_vars == [
        "OPENAI_API_KEY"
    ]
    assert adapter.descriptor.models
    assert adapter.descriptor.models[0][
        "id"
    ] == "gpt-4.1"
    assert adapter.DEFAULT_BASE_URL == (
        "https://api.openai.com/v1"
    )
    assert adapter.DEFAULT_TIMEOUT_SECONDS > 0


def test_missing_credential_fails_closed_in_real_process():
    root = repository_root()
    environment = dict(os.environ)

    environment.pop(
        "OPENAI_API_KEY",
        None,
    )

    code = """
from python.ai_platform.adapters import (
    OpenAIProviderAdapter,
    ProviderCredentialError,
    builtin_adapters,
)

adapter = next(
    item
    for item in builtin_adapters()
    if (
        isinstance(item, OpenAIProviderAdapter)
        and item.provider_id == "openai"
    )
)

try:
    adapter.complete(
        question="credential boundary",
        context={
            "schema": "credential-boundary/v1",
        },
        model="gpt-4.1",
        provider_settings={},
    )
except ProviderCredentialError:
    raise SystemExit(0)

raise SystemExit(
    "credential-free request did not fail closed"
)
"""

    result = subprocess.run(
        [sys.executable, "-c", code],
        cwd=root,
        env=environment,
        capture_output=True,
        text=True,
        timeout=20,
    )

    assert result.returncode == 0
    assert "credential-free request" not in (
        result.stderr
    )


def test_production_request_boundary_uses_real_https():
    root = repository_root()

    adapter_path = (
        root
        / "lib"
        / "python"
        / "ai_platform"
        / "adapters.py"
    )

    tree = ast.parse(
        adapter_path.read_text(encoding="utf-8")
    )

    calls = {
        node.func.attr
        for node in ast.walk(tree)
        if (
            isinstance(node, ast.Call)
            and isinstance(
                node.func,
                ast.Attribute,
            )
        )
    }

    assert "Request" in calls
    assert "urlopen" in calls
    assert "read" in calls
    assert "decode" in calls
    assert "loads" in calls


def test_provider_failure_types_are_explicit():
    assert issubclass(
        ProviderCredentialError,
        ProviderExecutionError,
    )
    assert issubclass(
        ProviderResponseError,
        ProviderExecutionError,
    )


def test_request_budget_diagnostic_is_content_free():
    diagnostic = (
        OpenAIProviderAdapter
        ._openai_request_budget_diagnostic(
            question="human-sensitive-content",
            reconstructed_context=(
                "context-sensitive-content"
            ),
            request_body=(
                b'{"sensitive":"payload-content"}'
            ),
            model="gpt-4.1",
        )
    )

    rendered = repr(diagnostic)

    assert diagnostic["model"] == "gpt-4.1"
    assert diagnostic[
        "human_message_characters"
    ] == len("human-sensitive-content")
    assert diagnostic[
        "reconstructed_context_characters"
    ] == len("context-sensitive-content")
    assert diagnostic[
        "serialized_request_bytes"
    ] > 0
    assert diagnostic[
        "estimated_tokens_at_4_chars"
    ] > 0
    assert diagnostic[
        "conservative_estimated_tokens_at_3_bytes"
    ] > 0

    assert "human-sensitive-content" not in rendered
    assert "context-sensitive-content" not in rendered
    assert "payload-content" not in rendered
    assert "OPENAI_API_KEY" not in rendered
    assert "Authorization" not in rendered


def test_response_extraction_fails_closed_without_text():
    with pytest.raises(
        ProviderResponseError,
        match="no output",
    ):
        OpenAIProviderAdapter._extract_answer(
            {}
        )

    with pytest.raises(
        ProviderResponseError,
        match="no textual answer",
    ):
        OpenAIProviderAdapter._extract_answer(
            {
                "output": [],
            }
        )


def test_external_success_requires_separate_live_evidence():
    root = repository_root()

    live_evidence = (
        root
        / "work"
        / "implementation-reports"
        / "FUSION"
        / "FUSION_02_OPENAI_PROVIDER_LIVE_EVIDENCE.json"
    )

    if not live_evidence.exists():
        pytest.skip(
            "real credentialed external acceptance "
            "has not been executed"
        )

    import json

    evidence = json.loads(
        live_evidence.read_text(encoding="utf-8")
    )

    assert evidence["status"] == "PASS"
    assert evidence["provider"] == "openai"
    assert evidence[
        "external_network_executed"
    ] is True
    assert evidence[
        "real_production_adapter"
    ] is True
    assert evidence[
        "credential_persisted"
    ] is False
    assert evidence[
        "answer_persisted"
    ] is False
    assert evidence[
        "human_authority_preserved"
    ] is True

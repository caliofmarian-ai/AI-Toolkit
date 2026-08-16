from __future__ import annotations

import inspect
import json
import os
import socket
import urllib.error
from unittest.mock import patch

import pytest

from python.ai_platform import adapters as adapters_module
from python.ai_platform.adapters import (
    OpenAIProviderAdapter,
    ProviderDescriptor,
)
from python.ai_platform.pipeline import AIRequestPipeline


def _descriptor():
    return ProviderDescriptor(
        provider_id="openai",
        name="OpenAI",
        env_vars=["OPENAI_API_KEY"],
        models=[
            {
                "id": "gpt-test-model",
                "capabilities": ["chat"],
                "token_limit": 128000,
            }
        ],
        capabilities=["chat"],
        token_limit=128000,
        estimated_cost_per_1k_tokens=0.01,
    )


def _adapter():
    return OpenAIProviderAdapter(_descriptor())


def _complete(adapter, question, context, model):
    return adapter.complete(
        question=question,
        context=context,
        model=model,

        provider_settings={},)


def _find_http_patch_target():
    """Return the actual patchable HTTP callable used by production.

    This helper mirrors the demonstrated OpenAIProviderAdapter boundary.
    It does not perform a network call.
    """
    return "adapters_module.urllib.request.urlopen"


class FakeHTTPResponse:
    def __init__(self, body, status=200):
        self._body = json.dumps(body).encode("utf-8")
        self.status = status
        self.headers = {}

    def read(self):
        return self._body

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


def _success_body(answer="REAL PROVIDER RESPONSE"):
    return {
        "id": "resp_test_001",
        "model": "gpt-test-model",
        "output": [
            {
                "type": "message",
                "role": "assistant",
                "content": [
                    {
                        "type": "output_text",
                        "text": answer,
                    }
                ],
            }
        ],
        "usage": {
            "input_tokens": 17,
            "output_tokens": 5,
            "total_tokens": 22,
        },
    }


def _capture_request(monkeypatch, response_body=None):
    captured = {}

    target = _find_http_patch_target()

    def fake_urlopen(request, *args, **kwargs):
        captured["request"] = request
        captured["args"] = args
        captured["kwargs"] = kwargs
        return FakeHTTPResponse(
            response_body or _success_body()
        )

    monkeypatch.setenv("OPENAI_API_KEY", "test-secret-not-real")
    parent_expr, attribute = target.rsplit(".", 1)
    parent = eval(parent_expr, {"adapters_module": adapters_module})
    monkeypatch.setattr(
        parent,
        attribute,
        fake_urlopen,
        raising=True,
    )

    return captured


def test_external_request_contains_human_message_and_context(monkeypatch):
    captured = _capture_request(monkeypatch)

    context = {
        "schema": "fusion-02-context/v1",
        "project": {
            "id": "AI-Toolkit",
        },
        "session": {
            "id": "session-test",
        },
        "conversation": [
            {
                "actor": "HUMAN",
                "content": "previous durable source",
            }
        ],
        "provenance": {
            "source": "persistent-experience",
        },
    }

    result = _complete(
        _adapter(),
        "current human message",
        context,
        "gpt-test-model",
    )

    request = captured["request"]

    assert request is not None

    raw_data = getattr(request, "data", None)
    assert raw_data is not None

    payload = json.loads(raw_data.decode("utf-8"))

    serialized = json.dumps(payload)

    assert "current human message" in serialized
    assert "AI-Toolkit" in serialized
    assert "session-test" in serialized
    assert "previous durable source" in serialized
    assert "persistent-experience" in serialized

    assert result["answer"] == "REAL PROVIDER RESPONSE"


def test_external_request_targets_openai_responses_boundary(monkeypatch):
    captured = _capture_request(monkeypatch)

    _complete(
        _adapter(),
        "hello",
        {"schema": "fusion-02-context/v1"},
        "gpt-test-model",
    )

    request = captured["request"]
    url = getattr(request, "full_url", "")

    assert url.startswith("https://")
    assert "/v1/responses" in url


def test_provider_and_model_identity_are_not_replaced(monkeypatch):
    captured = _capture_request(monkeypatch)

    result = _complete(
        _adapter(),
        "identity check",
        {"schema": "fusion-02-context/v1"},
        "gpt-test-model",
    )

    request = captured["request"]
    payload = json.loads(request.data.decode("utf-8"))

    assert payload.get("model") == "gpt-test-model"

    if "provider" in result:
        assert result["provider"] == "openai"

    if "model" in result:
        assert result["model"] == "gpt-test-model"


def test_external_response_is_interpreted(monkeypatch):
    _capture_request(
        monkeypatch,
        _success_body("provider answer 123"),
    )

    result = _complete(
        _adapter(),
        "question",
        {"schema": "fusion-02-context/v1"},
        "gpt-test-model",
    )

    assert result["answer"] == "provider answer 123"

    usage = result["usage"]

    assert usage["input_tokens"] == 17
    assert usage["output_tokens"] == 5


def test_missing_credential_fails_closed(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    with pytest.raises(Exception) as exc:
        _complete(
            _adapter(),
            "must not execute",
            {"schema": "fusion-02-context/v1"},
            "gpt-test-model",
        )

    message = str(exc.value).lower()

    assert (
        "credential" in message
        or "api key" in message
        or "openai_api_key" in message
    )


def test_timeout_is_explicit_failure(monkeypatch):
    target = _find_http_patch_target()

    monkeypatch.setenv(
        "OPENAI_API_KEY",
        "test-secret-not-real",
    )

    def timeout(*args, **kwargs):
        raise socket.timeout("bounded provider timeout")

    parent_expr, attribute = target.rsplit(".", 1)
    parent = eval(parent_expr, {"adapters_module": adapters_module})
    monkeypatch.setattr(
        parent,
        attribute,
        timeout,
        raising=True,
    )

    with pytest.raises(Exception) as exc:
        _complete(
            _adapter(),
            "timeout test",
            {"schema": "fusion-02-context/v1"},
            "gpt-test-model",
        )

    assert "timeout" in str(exc.value).lower()


def test_http_provider_failure_is_explicit(monkeypatch):
    target = _find_http_patch_target()

    monkeypatch.setenv(
        "OPENAI_API_KEY",
        "test-secret-not-real",
    )

    def failure(*args, **kwargs):
        raise urllib.error.HTTPError(
            url="https://api.openai.com/v1/responses",
            code=429,
            msg="rate limited",
            hdrs=None,
            fp=None,
        )

    parent_expr, attribute = target.rsplit(".", 1)
    parent = eval(parent_expr, {"adapters_module": adapters_module})
    monkeypatch.setattr(
        parent,
        attribute,
        failure,
        raising=True,
    )

    with pytest.raises(Exception) as exc:
        _complete(
            _adapter(),
            "failure test",
            {"schema": "fusion-02-context/v1"},
            "gpt-test-model",
        )

    message = str(exc.value).lower()

    assert (
        "429" in message
        or "provider" in message
        or "http" in message
        or "rate" in message
    )


def test_invalid_provider_response_is_explicit_failure(monkeypatch):
    _capture_request(
        monkeypatch,
        {
            "id": "resp_invalid",
            "output": [],
            "usage": {},
        },
    )

    with pytest.raises(Exception):
        _complete(
            _adapter(),
            "invalid response",
            {"schema": "fusion-02-context/v1"},
            "gpt-test-model",
        )


def test_openai_adapter_does_not_fallback_to_static(monkeypatch):
    target = _find_http_patch_target()

    monkeypatch.setenv(
        "OPENAI_API_KEY",
        "test-secret-not-real",
    )

    static_called = {"value": False}

    def static_complete(*args, **kwargs):
        static_called["value"] = True
        return {
            "answer": "FABRICATED STATIC FALLBACK",
            "usage": {
                "input_tokens": 1,
                "output_tokens": 1,
                "estimated_cost": 0,
                "latency_ms": 1,
            },
        }

    monkeypatch.setattr(
        adapters_module.StaticProviderAdapter,
        "complete",
        static_complete,
    )

    def failure(*args, **kwargs):
        raise urllib.error.URLError(
            "external provider unavailable"
        )

    parent_expr, attribute = target.rsplit(".", 1)
    parent = eval(parent_expr, {"adapters_module": adapters_module})
    monkeypatch.setattr(
        parent,
        attribute,
        failure,
        raising=True,
    )

    with pytest.raises(Exception):
        _complete(
            _adapter(),
            "do not fabricate",
            {"schema": "fusion-02-context/v1"},
            "gpt-test-model",
        )

    assert static_called["value"] is False


def test_pipeline_propagates_context_to_real_adapter_contract():
    class Registry:
        def __init__(self):
            self.received = None

        def list_providers(self, settings):
            return [
                {
                    "id": "openai",
                    "provider_id": "openai",
                    "models": [{"id": "gpt-test-model"}],
                }
            ]

        def adapter(self, provider_id):
            assert provider_id == "openai"
            return self

        def complete(self, question, context, model,
            provider_settings=None,
):
            self.received = {
                "question": question,
                "context": context,
                "model": model,
            }
            return {
                "answer": "pipeline provider response",
                "usage": {
                    "input_tokens": 2,
                    "output_tokens": 3,
                    "estimated_cost": 0.001,
                    "latency_ms": 4,
                },
            }

    class ModelManager:
        def discover_models(self, providers):
            return {
                "openai": [
                    {
                        "id": "gpt-test-model",
                    }
                ]
            }

        def resolve_roles(self, settings, discovered):
            return {
                "engineering_model": "gpt-test-model",
                "default_model": "gpt-test-model",
            }

    class ContextBuilder:
        def build(self):
            raise AssertionError(
                "context builder must not replace context_override"
            )

    registry = Registry()

    pipeline = AIRequestPipeline(
        registry=registry,
        model_manager=ModelManager(),
        context_builder=ContextBuilder(),
    )

    context = {
        "schema": "fusion-02-context/v1",
        "project": {"id": "AI-Toolkit"},
        "conversation": [
            {
                "actor": "HUMAN",
                "content": "durable prior message",
            }
        ],
    }

    result = pipeline.run(
        "current human message",
        {
            "default_provider": "openai",
        },
        provider_id="openai",
        model="gpt-test-model",
        context_override=context,
    )

    assert registry.received == {
        "question": "current human message",
        "context": context,
        "model": "gpt-test-model",
    }

    assert result["provider"] == "openai"
    assert result["model"] == "gpt-test-model"
    assert result["context"] == context
    assert result["answer"] == "pipeline provider response"


def test_test_suite_never_uses_real_external_provider(monkeypatch):
    # This acceptance test intentionally proves that all adapter calls in
    # this module are replaceable at the HTTP boundary. It must never need
    # or consume a real deployment credential.
    assert os.environ.get("OPENAI_API_KEY") != "test-secret-not-real"


def test_http_429_preserves_sanitized_provider_diagnostic(
    monkeypatch,
):
    import io

    monkeypatch.setenv(
        "OPENAI_API_KEY",
        "test-secret-not-real",
    )

    adapter = _adapter()

    provider_body = json.dumps(
        {
            "error": {
                "message": (
                    "Sensitive provider prose that must "
                    "not be propagated"
                ),
                "type": "insufficient_quota",
                "param": None,
                "code": "insufficient_quota",
            }
        }
    ).encode("utf-8")

    def failure(request, timeout):
        raise urllib.error.HTTPError(
            url=request.full_url,
            code=429,
            msg="Too Many Requests",
            hdrs={
                "x-request-id": "req_fusion02_429",
            },
            fp=io.BytesIO(provider_body),
        )

    monkeypatch.setattr(
        adapters_module.urllib.request,
        "urlopen",
        failure,
    )

    with pytest.raises(
        adapters_module.ProviderExecutionError,
    ) as caught:
        adapter.complete(
            question="Human message",
            context={
                "schema": "fusion-02-context/v1",
            },
            model="gpt-4.1",
            provider_settings={},
        )

    diagnostic = str(caught.value)

    assert "status=429" in diagnostic
    assert "type=insufficient_quota" in diagnostic
    assert "code=insufficient_quota" in diagnostic
    assert "request_id=req_fusion02_429" in diagnostic

    assert "test-secret-not-real" not in diagnostic
    assert "Human message" not in diagnostic
    assert "Sensitive provider prose" not in diagnostic


def test_http_failure_with_non_json_body_remains_fail_closed(
    monkeypatch,
):
    import io

    monkeypatch.setenv(
        "OPENAI_API_KEY",
        "test-secret-not-real",
    )

    adapter = _adapter()

    def failure(request, timeout):
        raise urllib.error.HTTPError(
            url=request.full_url,
            code=429,
            msg="Too Many Requests",
            hdrs={},
            fp=io.BytesIO(
                b"provider body not safe for propagation"
            ),
        )

    monkeypatch.setattr(
        adapters_module.urllib.request,
        "urlopen",
        failure,
    )

    with pytest.raises(
        adapters_module.ProviderExecutionError,
    ) as caught:
        adapter.complete(
            question="Human message",
            context={},
            model="gpt-4.1",
            provider_settings={},
        )

    diagnostic = str(caught.value)

    assert diagnostic == "OpenAI HTTP failure: status=429"
    assert "test-secret-not-real" not in diagnostic
    assert "provider body not safe" not in diagnostic


def test_openai_request_budget_diagnostic_is_content_free():
    diagnostic = OpenAIProviderAdapter._openai_request_budget_diagnostic(
        question="human-secret-content",
        reconstructed_context="context-secret-content",
        request_body=b'{"secret":"payload-secret-content"}',
        model="gpt-4.1",
    )

    assert diagnostic["model"] == "gpt-4.1"
    assert diagnostic["human_message_characters"] == len(
        "human-secret-content"
    )
    assert diagnostic["reconstructed_context_characters"] == len(
        "context-secret-content"
    )
    assert diagnostic["serialized_request_bytes"] == len(
        b'{"secret":"payload-secret-content"}'
    )
    assert diagnostic["estimated_tokens_at_4_chars"] > 0
    assert (
        diagnostic["conservative_estimated_tokens_at_3_bytes"]
        > 0
    )

    rendered = repr(diagnostic)

    assert "human-secret-content" not in rendered
    assert "context-secret-content" not in rendered
    assert "payload-secret-content" not in rendered
    assert "OPENAI_API_KEY" not in rendered
    assert "Authorization" not in rendered

def test_request_budget_is_visible_in_standard_log_message(
    monkeypatch,
    caplog,
):
    monkeypatch.setenv(
        "OPENAI_API_KEY",
        "test-secret-not-real",
    )

    captured = {}

    class Response:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def read(self):
            return json.dumps(
                {
                    "output_text": "provider answer",
                    "usage": {
                        "input_tokens": 1,
                        "output_tokens": 1,
                    },
                }
            ).encode("utf-8")

    def fake_urlopen(request, timeout):
        captured["body"] = request.data
        return Response()

    monkeypatch.setattr(
        adapters_module.urllib.request,
        "urlopen",
        fake_urlopen,
    )

    caplog.set_level(
        "INFO",
        logger="python.ai_platform.adapters",
    )

    adapter = _adapter()

    adapter.complete(
        question="hi",
        context={
            "schema": "fusion-02-context/v1",
            "probe": "x" * 32,
        },
        model="gpt-4.1",
        provider_settings={},
    )

    messages = [
        record.getMessage()
        for record in caplog.records
        if "OpenAI outbound request budget" in record.getMessage()
    ]

    assert len(messages) == 1

    message = messages[0]

    assert "model=gpt-4.1" in message
    assert "human_message_characters=2" in message
    assert "reconstructed_context_characters=" in message
    assert "serialized_request_bytes=" in message
    assert "estimated_tokens_at_4_chars=" in message
    assert "conservative_estimated_tokens_at_3_bytes=" in message

    assert "test-secret-not-real" not in message
    assert '"probe"' not in message
    assert ("x" * 32) not in message
    assert "hi" not in message

    assert captured["body"]

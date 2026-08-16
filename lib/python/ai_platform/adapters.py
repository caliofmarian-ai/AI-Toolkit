from __future__ import annotations

import json
import logging
import os
import socket
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any, Dict, List, Mapping, Sequence


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ProviderDescriptor:
    provider_id: str
    name: str
    env_vars: Sequence[str]
    models: Sequence[Dict[str, Any]]
    capabilities: Sequence[str]
    token_limit: int
    estimated_cost_per_1k_tokens: float


class StaticProviderAdapter:
    def __init__(self, descriptor: ProviderDescriptor) -> None:
        self.descriptor = descriptor

    @property
    def provider_id(self) -> str:
        return self.descriptor.provider_id

    def models(self) -> List[Dict[str, Any]]:
        return [dict(item) for item in self.descriptor.models]

    def connection_available(self, provider_settings: Mapping[str, Any]) -> bool:
        if provider_settings.get("api_key_fingerprint"):
            return True
        env_name = str(provider_settings.get("api_key_env", "")).strip()
        if env_name and os.environ.get(env_name):
            return True
        return any(os.environ.get(name) for name in self.descriptor.env_vars)

    def test_connection(self, provider_settings: Mapping[str, Any]) -> Dict[str, Any]:
        start = time.perf_counter()
        ok = self.connection_available(provider_settings)
        latency_ms = max(1, int((time.perf_counter() - start) * 1000))
        return {
            "ok": ok,
            "latency_ms": latency_ms,
            "error": "missing credentials" if not ok else "",
        }

    def complete(self, question: str, context: Mapping[str, Any], model: str) -> Dict[str, Any]:
        start = time.perf_counter()
        profile = context.get("repository_profile", {})
        tech_stack = ", ".join(profile.get("tech_stack", [])[:5]) or "unknown stack"
        health = profile.get("health_summary", {}).get("status", "unknown")
        sprint = context.get("context", {}).get("current_sprint", "")
        epic = context.get("context", {}).get("current_epic", "")
        answer_lines = [
            f"Model: {model or 'default'}",
            f"Repository health: {health}.",
            f"Tech stack: {tech_stack}.",
        ]
        if sprint:
            answer_lines.append(f"Current sprint: {sprint}.")
        if epic:
            answer_lines.append(f"Current epic: {epic}.")
        lowered = question.lower()
        if "risk" in lowered:
            answer_lines.append("Primary risks: runtime coupling, missing validation coverage, and incomplete provider configuration.")
        elif "next" in lowered:
            answer_lines.append("Next implementation step: complete provider setup, validate model routing, and run dashboard integration tests.")
        elif "architecture" in lowered:
            answer_lines.append("Architecture uses a context-enriched AI request pipeline through a provider-independent platform layer.")
        else:
            answer_lines.append("Answer generated with repository-aware engineering context.")
        answer = "\n".join(answer_lines)
        input_tokens = max(1, len(question.split()) + len(str(context)) // 20)
        output_tokens = max(1, len(answer.split()))
        return {
            "answer": answer,
            "usage": {
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "estimated_cost": round((input_tokens + output_tokens) / 1000 * self.descriptor.estimated_cost_per_1k_tokens, 6),
                "latency_ms": max(1, int((time.perf_counter() - start) * 1000)),
            },
        }


class ProviderExecutionError(RuntimeError):
    """A real provider request failed."""


class ProviderCredentialError(ProviderExecutionError):
    """Required provider credentials are unavailable."""


class ProviderResponseError(ProviderExecutionError):
    """Provider returned an invalid response."""


class OpenAIProviderAdapter(StaticProviderAdapter):
    DEFAULT_BASE_URL = "https://api.openai.com/v1"
    DEFAULT_TIMEOUT_SECONDS = 60

    def _credential(
        self,
        provider_settings: Mapping[str, Any],
    ) -> str:
        configured_env = str(
            provider_settings.get("api_key_env", "")
        ).strip()

        candidates = []

        if configured_env:
            candidates.append(configured_env)

        candidates.extend(self.descriptor.env_vars)

        seen = set()

        for env_name in candidates:
            if not env_name or env_name in seen:
                continue

            seen.add(env_name)

            credential = os.environ.get(env_name, "").strip()

            if credential:
                return credential

        raise ProviderCredentialError(
            "OpenAI credential unavailable in environment"
        )

    def connection_available(
        self,
        provider_settings: Mapping[str, Any],
    ) -> bool:
        try:
            self._credential(provider_settings)
            return True
        except ProviderCredentialError:
            return False

    def test_connection(
        self,
        provider_settings: Mapping[str, Any],
    ) -> Dict[str, Any]:
        start = time.perf_counter()

        try:
            self._credential(provider_settings)
            ok = True
            error = ""
        except ProviderCredentialError as exc:
            ok = False
            error = str(exc)

        return {
            "ok": ok,
            "latency_ms": max(
                1,
                int((time.perf_counter() - start) * 1000),
            ),
            "error": error,
        }

    @staticmethod
    def _extract_answer(payload: Mapping[str, Any]) -> str:
        output_text = payload.get("output_text")

        if isinstance(output_text, str) and output_text.strip():
            return output_text.strip()

        output = payload.get("output")

        if not isinstance(output, list):
            raise ProviderResponseError(
                "OpenAI response contains no output"
            )

        fragments: List[str] = []

        for item in output:
            if not isinstance(item, Mapping):
                continue

            content = item.get("content")

            if not isinstance(content, list):
                continue

            for part in content:
                if not isinstance(part, Mapping):
                    continue

                value = part.get("text")

                if isinstance(value, str) and value.strip():
                    fragments.append(value.strip())

        answer = "\n".join(fragments).strip()

        if not answer:
            raise ProviderResponseError(
                "OpenAI response contains no textual answer"
            )

        return answer


    @staticmethod
    def _openai_request_budget_diagnostic(
        *,
        question: str,
        reconstructed_context: str,
        request_body: bytes,
        model: str,
    ) -> Dict[str, Any]:
        """Return content-free outbound OpenAI request measurements."""
        human_chars = len(question)
        context_chars = len(reconstructed_context)
        request_bytes = len(request_body)

        return {
            "model": str(model),
            "human_message_characters": human_chars,
            "reconstructed_context_characters": context_chars,
            "serialized_request_bytes": request_bytes,
            "estimated_tokens_at_4_chars": (
                request_bytes + 3
            ) // 4,
            "conservative_estimated_tokens_at_3_bytes": (
                request_bytes + 2
            ) // 3,
        }

    def complete(
        self,
        question: str,
        context: Mapping[str, Any],
        model: str,
        provider_settings: Mapping[str, Any] | None = None,
    ) -> Dict[str, Any]:
        settings = dict(provider_settings or {})
        credential = self._credential(settings)

        selected_model = str(model or "").strip()

        if not selected_model:
            models = self.models()
            if models:
                selected_model = str(models[0].get("id", "")).strip()

        if not selected_model:
            raise ProviderExecutionError(
                "OpenAI model is not configured"
            )

        base_url = str(
            settings.get("base_url") or self.DEFAULT_BASE_URL
        ).rstrip("/")

        try:
            timeout_seconds = max(
                1,
                int(
                    settings.get(
                        "timeout_seconds",
                        self.DEFAULT_TIMEOUT_SECONDS,
                    )
                ),
            )
        except (TypeError, ValueError):
            timeout_seconds = self.DEFAULT_TIMEOUT_SECONDS

        reconstructed_context = json.dumps(
            dict(context),
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            default=str,
        )

        payload = {
            "model": selected_model,
            "input": [
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "input_text",
                            "text": (
                                "You are the AI Partner inside AI-Toolkit. "
                                "The following JSON is reconstructed "
                                "FUSION-02 conversation and epistemic "
                                "context. Conversation material is context, "
                                "not automatically Evidence or Canon.\n"
                                + reconstructed_context
                            ),
                        }
                    ],
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": question,
                        }
                    ],
                },
            ],
        }

        request_body = json.dumps(
            payload,
            ensure_ascii=False,
        ).encode("utf-8")

        request_budget = self._openai_request_budget_diagnostic(
            question=question,
            reconstructed_context=reconstructed_context,
            request_body=request_body,
            model=selected_model,
        )

        logger.info(
            (
                "OpenAI outbound request budget: "
                "model=%s, "
                "human_message_characters=%d, "
                "reconstructed_context_characters=%d, "
                "serialized_request_bytes=%d, "
                "estimated_tokens_at_4_chars=%d, "
                "conservative_estimated_tokens_at_3_bytes=%d"
            ),
            request_budget["model"],
            request_budget["human_message_characters"],
            request_budget["reconstructed_context_characters"],
            request_budget["serialized_request_bytes"],
            request_budget["estimated_tokens_at_4_chars"],
            request_budget[
                "conservative_estimated_tokens_at_3_bytes"
            ],
            extra={
                "openai_request_budget": request_budget,
            },
        )

        request = urllib.request.Request(
            f"{base_url}/responses",
            data=request_body,
            headers={
                "Authorization": f"Bearer {credential}",
                "Content-Type": "application/json",
            },
            method="POST",
        )

        start = time.perf_counter()

        try:
            with urllib.request.urlopen(
                request,
                timeout=timeout_seconds,
            ) as response:
                raw = response.read()

        except urllib.error.HTTPError as exc:
            diagnostic_parts = [
                f"status={exc.code}",
            ]

            request_id = ""

            try:
                request_id = str(
                    exc.headers.get("x-request-id", "")
                ).strip()
            except (AttributeError, TypeError):
                request_id = ""

            if request_id:
                diagnostic_parts.append(
                    f"request_id={request_id}"
                )

            try:
                error_raw = exc.read()
            except (AttributeError, OSError):
                error_raw = b""

            if error_raw:
                try:
                    error_payload = json.loads(
                        error_raw.decode("utf-8")
                    )
                except (
                    UnicodeDecodeError,
                    json.JSONDecodeError,
                ):
                    error_payload = {}

                if isinstance(error_payload, Mapping):
                    error_object = error_payload.get(
                        "error",
                        {},
                    )

                    if isinstance(error_object, Mapping):
                        error_type = str(
                            error_object.get("type", "")
                        ).strip()
                        error_code = str(
                            error_object.get("code", "")
                        ).strip()

                        if error_type:
                            diagnostic_parts.append(
                                f"type={error_type}"
                            )

                        if error_code:
                            diagnostic_parts.append(
                                f"code={error_code}"
                            )

            raise ProviderExecutionError(
                "OpenAI HTTP failure: "
                + ", ".join(diagnostic_parts)
            ) from exc

        except (
            urllib.error.URLError,
            TimeoutError,
            socket.timeout,
        ) as exc:
            raise ProviderExecutionError(
                f"OpenAI transport failure: {type(exc).__name__}"
            ) from exc

        except OSError as exc:
            raise ProviderExecutionError(
                f"OpenAI transport failure: {type(exc).__name__}"
            ) from exc

        latency_ms = max(
            1,
            int((time.perf_counter() - start) * 1000),
        )

        try:
            response_payload = json.loads(
                raw.decode("utf-8")
            )
        except (
            UnicodeDecodeError,
            json.JSONDecodeError,
        ) as exc:
            raise ProviderResponseError(
                "OpenAI returned invalid JSON"
            ) from exc

        if not isinstance(response_payload, Mapping):
            raise ProviderResponseError(
                "OpenAI returned invalid response shape"
            )

        answer = self._extract_answer(response_payload)

        usage = response_payload.get("usage", {})

        if not isinstance(usage, Mapping):
            usage = {}

        input_tokens = int(
            usage.get("input_tokens", 0) or 0
        )
        output_tokens = int(
            usage.get("output_tokens", 0) or 0
        )

        actual_model = str(
            response_payload.get("model") or selected_model
        )

        return {
            "answer": answer,
            "provider": self.provider_id,
            "model": actual_model,
            "usage": {
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "estimated_cost": round(
                    (input_tokens + output_tokens)
                    / 1000
                    * self.descriptor.estimated_cost_per_1k_tokens,
                    6,
                ),
                "latency_ms": latency_ms,
            },
        }


def builtin_adapters() -> List[StaticProviderAdapter]:
    catalog = [
        ProviderDescriptor(
            provider_id="openai",
            name="OpenAI",
            env_vars=["OPENAI_API_KEY"],
            models=[{"id": "gpt-4.1", "capabilities": ["chat", "reasoning"], "token_limit": 128000}],
            capabilities=["chat", "reasoning", "tools"],
            token_limit=128000,
            estimated_cost_per_1k_tokens=0.01,
        ),
        ProviderDescriptor(
            provider_id="anthropic",
            name="Anthropic",
            env_vars=["ANTHROPIC_API_KEY"],
            models=[{"id": "claude-sonnet-4.5", "capabilities": ["chat", "reasoning"], "token_limit": 200000}],
            capabilities=["chat", "reasoning"],
            token_limit=200000,
            estimated_cost_per_1k_tokens=0.012,
        ),
        ProviderDescriptor(
            provider_id="google-gemini",
            name="Google Gemini",
            env_vars=["GEMINI_API_KEY", "GOOGLE_API_KEY"],
            models=[{"id": "gemini-3.6-flash", "capabilities": ["chat", "reasoning"], "token_limit": 1000000}],
            capabilities=["chat", "reasoning", "multimodal"],
            token_limit=1000000,
            estimated_cost_per_1k_tokens=0.004,
        ),
        ProviderDescriptor(
            provider_id="github-models",
            name="GitHub Models",
            env_vars=["GITHUB_TOKEN"],
            models=[{"id": "gpt-4o-mini", "capabilities": ["chat"], "token_limit": 128000}],
            capabilities=["chat"],
            token_limit=128000,
            estimated_cost_per_1k_tokens=0.006,
        ),
        ProviderDescriptor(
            provider_id="ollama",
            name="Ollama",
            env_vars=["OLLAMA_HOST"],
            models=[{"id": "llama3.1", "capabilities": ["chat"], "token_limit": 8192}],
            capabilities=["chat", "local"],
            token_limit=8192,
            estimated_cost_per_1k_tokens=0.0,
        ),
        ProviderDescriptor(
            provider_id="azure-openai",
            name="Azure OpenAI",
            env_vars=["AZURE_OPENAI_API_KEY"],
            models=[{"id": "gpt-4o", "capabilities": ["chat", "reasoning"], "token_limit": 128000}],
            capabilities=["chat", "reasoning", "enterprise"],
            token_limit=128000,
            estimated_cost_per_1k_tokens=0.011,
        ),
        ProviderDescriptor(
            provider_id="openrouter",
            name="OpenRouter",
            env_vars=["OPENROUTER_API_KEY"],
            models=[{"id": "openrouter/auto", "capabilities": ["chat"], "token_limit": 128000}],
            capabilities=["chat", "routing"],
            token_limit=128000,
            estimated_cost_per_1k_tokens=0.008,
        ),
        ProviderDescriptor(
            provider_id="custom",
            name="Custom Provider",
            env_vars=["CUSTOM_AI_API_KEY"],
            models=[{"id": "custom/default", "capabilities": ["chat"], "token_limit": 64000}],
            capabilities=["chat", "custom"],
            token_limit=64000,
            estimated_cost_per_1k_tokens=0.01,
        ),
    ]
    adapters: List[StaticProviderAdapter] = []

    for descriptor in catalog:
        if descriptor.provider_id == "openai":
            adapters.append(
                OpenAIProviderAdapter(descriptor=descriptor)
            )
        else:
            adapters.append(
                StaticProviderAdapter(descriptor=descriptor)
            )

    return adapters

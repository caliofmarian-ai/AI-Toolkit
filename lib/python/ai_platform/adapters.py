from __future__ import annotations

import os
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Mapping, Sequence


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
    return [StaticProviderAdapter(descriptor=item) for item in catalog]

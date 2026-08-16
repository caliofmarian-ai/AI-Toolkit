from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, Mapping

from .context_builder import AIContextBuilder
from .model_manager import ModelManager
from .registry import ProviderRegistry


class AIRequestPipeline:
    def __init__(
        self,
        *,
        registry: ProviderRegistry,
        model_manager: ModelManager,
        context_builder: AIContextBuilder,
    ) -> None:
        self.registry = registry
        self.model_manager = model_manager
        self.context_builder = context_builder

    def run(
        self,
        question: str,
        settings: Mapping[str, Any],
        *,
        provider_id: str = "",
        model: str = "",
        context_override: Mapping[str, Any] | None = None,
    ) -> Dict[str, Any]:
        providers = self.registry.list_providers(settings)
        discovered = self.model_manager.discover_models(providers)
        roles = self.model_manager.resolve_roles(settings, discovered)
        fallback_provider = sorted(discovered.keys())[0] if discovered else ""
        selected_provider = provider_id or settings.get("default_provider") or fallback_provider
        selected_model = model or roles.get("engineering_model") or roles.get("default_model", "")
        adapter = self.registry.adapter(str(selected_provider))
        if adapter is None:
            raise ValueError(f"no adapter found for provider: {selected_provider!r}")

        context = (
            dict(context_override)
            if context_override is not None
            else self.context_builder.build()
        )
        completion = adapter.complete(
            question=question,
            context=context,
            model=selected_model,
        )
        usage = {
            "provider": selected_provider,
            "model": selected_model,
            "input_tokens": completion["usage"]["input_tokens"],
            "output_tokens": completion["usage"]["output_tokens"],
            "estimated_cost": completion["usage"]["estimated_cost"],
            "latency_ms": completion["usage"]["latency_ms"],
            "success": True,
            "error": "",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        return {
            "question": question,
            "answer": completion["answer"],
            "provider": selected_provider,
            "model": selected_model,
            "context": context,
            "usage": usage,
        }

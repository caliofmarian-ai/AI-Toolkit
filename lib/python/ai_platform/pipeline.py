from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, Mapping

from .context_builder import AIContextBuilder
from .cognitive_coordination import (
    ContextBudgetGovernor,
    WorkingContext,
)
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
        self._shadow_working_context: WorkingContext | None = None
        self._last_shadow_comparison: Dict[str, Any] | None = None
        self._default_cognitive_working_context: WorkingContext | None = None

    def use_cognitive_working_context(
        self,
        working_context: WorkingContext | None,
    ) -> None:
        self._default_cognitive_working_context = working_context
        self._shadow_working_context = None
        self._last_shadow_comparison = None

    def observe_working_context(
        self,
        working_context: WorkingContext | None,
    ) -> None:
        self._shadow_working_context = working_context
        self._last_shadow_comparison = None

    def consume_shadow_comparison(
        self,
    ) -> Dict[str, Any] | None:
        comparison = self._last_shadow_comparison
        self._last_shadow_comparison = None
        return (
            dict(comparison)
            if comparison is not None
            else None
        )

    def run(
        self,
        question: str,
        settings: Mapping[str, Any],
        *,
        provider_id: str = "",
        model: str = "",
        context_override: Mapping[str, Any] | None = None,
        working_context: WorkingContext | None = None,
        reserved_orientation: int = 256,
        reserved_question: int = 256,
        reserved_instructions: int = 512,
        reserved_answer: int = 1024,
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

        if (
            working_context is not None
            and context_override is not None
        ):
            raise ValueError(
                "working_context and context_override are mutually exclusive"
            )

        context_governance = None
        shadow_comparison = None

        default_cognitive_working_context = (
            self._default_cognitive_working_context
        )
        self._default_cognitive_working_context = None

        if (
            working_context is not None
            and default_cognitive_working_context is not None
        ):
            raise ValueError(
                "explicit and default cognitive working contexts "
                "cannot coexist"
            )

        effective_working_context = (
            working_context
            if working_context is not None
            else default_cognitive_working_context
        )

        if effective_working_context is not None:
            provider_capacity = self.registry.model_token_limit(
                str(selected_provider),
                str(selected_model),
            )

            governor = ContextBudgetGovernor()

            budget = governor.calculate_budget(
                provider_capacity=provider_capacity,
                reserved_orientation=reserved_orientation,
                reserved_question=reserved_question,
                reserved_instructions=reserved_instructions,
                reserved_answer=reserved_answer,
            )

            governed = governor.govern(
                working_context=effective_working_context,
                budget=budget,
            )

            if governed.rejected:
                raise ValueError(
                    "working context exceeds provider-safe budget: "
                    + governed.rejection_reason
                )

            context = dict(governed.context)
            context_governance = {
                "provider_capacity": budget.provider_capacity,
                "available_context": budget.available_context,
                "estimated_context_units": (
                    governed.estimated_context_units
                ),
                "compacted": governed.compacted,
                "rejected": governed.rejected,
            }
        else:
            context = (
                dict(context_override)
                if context_override is not None
                else self.context_builder.build()
            )

        shadow_working_context = self._shadow_working_context
        self._shadow_working_context = None

        if shadow_working_context is not None:
            provider_capacity = self.registry.model_token_limit(
                str(selected_provider),
                str(selected_model),
            )

            shadow_governor = ContextBudgetGovernor()

            shadow_budget = shadow_governor.calculate_budget(
                provider_capacity=provider_capacity,
                reserved_orientation=reserved_orientation,
                reserved_question=reserved_question,
                reserved_instructions=reserved_instructions,
                reserved_answer=reserved_answer,
            )

            shadow_governed = shadow_governor.govern(
                working_context=shadow_working_context,
                budget=shadow_budget,
            )

            shadow_comparison = {
                "mode": "SHADOW",
                "provider_payload_source": "LEGACY",
                "shadow_payload_sent_to_provider": False,
                "provider_capacity": shadow_budget.provider_capacity,
                "available_context": shadow_budget.available_context,
                "legacy_estimated_context_units": (
                    shadow_governor.estimate_units(context)
                ),
                "cognitive_estimated_context_units": (
                    shadow_governed.estimated_context_units
                ),
                "cognitive_compacted": shadow_governed.compacted,
                "cognitive_rejected": shadow_governed.rejected,
                "cognitive_rejection_reason": (
                    shadow_governed.rejection_reason
                ),
                "cognitive_source_count": len(
                    shadow_governed.context.get(
                        "source_paths",
                        [],
                    )
                ),
                "cognitive_epistemic_result_count": len(
                    shadow_governed.context.get(
                        "epistemic_results",
                        [],
                    )
                ),
                "cognitive_provenance_count": len(
                    shadow_governed.context.get(
                        "provenance",
                        [],
                    )
                ),
                "authority_conferred": (
                    shadow_governed.context.get(
                        "authority_conferred",
                        False,
                    )
                ),
                "human_authority_preserved": (
                    shadow_governed.context.get(
                        "human_authority_preserved",
                        True,
                    )
                ),
            }

        self._last_shadow_comparison = shadow_comparison

        provider_settings = dict(
            settings.get("providers", {})
        ).get(str(selected_provider), {})

        completion = adapter.complete(
            question=question,
            context=context,
            model=selected_model,
            provider_settings=provider_settings,
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
            "context_governance": context_governance,
            "shadow_comparison": shadow_comparison,
            "usage": usage,
        }

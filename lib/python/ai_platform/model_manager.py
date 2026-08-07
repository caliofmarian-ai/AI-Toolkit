from __future__ import annotations

from typing import Any, Dict, List, Mapping

from .settings import DEFAULT_MODEL_ROLES


class ModelManager:
    def discover_models(self, providers: List[Mapping[str, Any]]) -> Dict[str, List[str]]:
        discovered: Dict[str, List[str]] = {}
        for provider in providers:
            discovered[str(provider["id"])] = list(provider.get("models", []))
        return discovered

    def resolve_roles(self, settings: Mapping[str, Any], discovered: Mapping[str, List[str]]) -> Dict[str, str]:
        configured = {**DEFAULT_MODEL_ROLES, **dict(settings.get("model_configuration", {}))}
        flat_models = {model for models in discovered.values() for model in models}
        resolved = {}
        first_model = sorted(flat_models)[0] if flat_models else ""
        for role in DEFAULT_MODEL_ROLES:
            candidate = str(configured.get(role, ""))
            resolved[role] = candidate if candidate in flat_models else first_model
        return resolved

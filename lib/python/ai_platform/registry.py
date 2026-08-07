from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Mapping, Optional

from .adapters import StaticProviderAdapter


class ProviderRegistry:
    def __init__(self) -> None:
        self._adapters: Dict[str, StaticProviderAdapter] = {}
        self._health: Dict[str, Dict[str, Any]] = {}

    def register(self, adapter: StaticProviderAdapter) -> None:
        self._adapters[adapter.provider_id] = adapter

    def adapter(self, provider_id: str) -> Optional[StaticProviderAdapter]:
        return self._adapters.get(provider_id)

    def provider_ids(self) -> List[str]:
        return sorted(self._adapters.keys())

    def test_connection(self, provider_id: str, provider_settings: Mapping[str, Any]) -> Dict[str, Any]:
        adapter = self._adapters.get(provider_id)
        if adapter is None:
            raise ValueError(f"provider '{provider_id}' is not registered")
        result = adapter.test_connection(provider_settings)
        now = datetime.now(timezone.utc).isoformat()
        health = self._health.setdefault(provider_id, {})
        health.update(
            {
                "last_response_time_ms": result["latency_ms"],
                "health_status": "healthy" if result["ok"] else "degraded",
                "connection": bool(result["ok"]),
            }
        )
        if result["ok"]:
            health["last_success"] = now
            health["errors"] = []
            health["last_failure"] = ""
        else:
            health["last_failure"] = now
            health["errors"] = [result.get("error", "connection test failed")]
        return {
            "provider": provider_id,
            "status": "connected" if result["ok"] else "disconnected",
            "connection": bool(result["ok"]),
            "last_success": health.get("last_success", ""),
            "last_failure": health.get("last_failure", ""),
            "last_response_time": result["latency_ms"],
            "health_status": health.get("health_status", "unknown"),
            "errors": health.get("errors", []),
        }

    def list_providers(self, settings: Mapping[str, Any]) -> List[Dict[str, Any]]:
        provider_settings = dict(settings.get("providers", {}))
        providers = []
        for provider_id in self.provider_ids():
            adapter = self._adapters[provider_id]
            configured = dict(provider_settings.get(provider_id, {}))
            health = dict(self._health.get(provider_id, {}))
            models = adapter.models()
            providers.append(
                {
                    "id": provider_id,
                    "name": adapter.descriptor.name,
                    "status": "configured" if adapter.connection_available(configured) else "not_configured",
                    "connection": bool(health.get("connection", adapter.connection_available(configured))),
                    "models": [item["id"] for item in models],
                    "latency": health.get("last_response_time_ms", 0),
                    "capabilities": list(adapter.descriptor.capabilities),
                    "token_limits": {item["id"]: item.get("token_limit", adapter.descriptor.token_limit) for item in models},
                    "estimated_cost": adapter.descriptor.estimated_cost_per_1k_tokens,
                    "health": health.get("health_status", "unknown"),
                    "errors": health.get("errors", []),
                    "last_success": health.get("last_success", ""),
                    "last_failure": health.get("last_failure", ""),
                    "last_response_time": health.get("last_response_time_ms", 0),
                }
            )
        return providers

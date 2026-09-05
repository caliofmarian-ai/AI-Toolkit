from __future__ import annotations

from typing import Dict, Iterable, List, Mapping, Optional, Union

from .chat_models import ProviderConnection, ProviderConnectionState


class ProviderRegistry:
    """Normalize provider state and capabilities behind a serializable contract."""

    def __init__(self) -> None:
        self.providers: Dict[str, ProviderConnection] = {}

    def register_provider(self, provider_conn: Union[ProviderConnection, Mapping[str, object]]) -> ProviderConnection:
        connection = provider_conn if isinstance(provider_conn, ProviderConnection) else ProviderConnection.from_dict(dict(provider_conn))
        self.providers[connection.id] = connection
        return connection

    def get_provider(self, provider_id: str) -> Optional[ProviderConnection]:
        return self.providers.get(provider_id)

    def all_providers(self) -> List[ProviderConnection]:
        return list(self.providers.values())

    def register_many(self, providers: Iterable[Union[ProviderConnection, Mapping[str, object]]]) -> List[ProviderConnection]:
        registered: List[ProviderConnection] = []
        for provider in providers:
            registered.append(self.register_provider(provider))
        return registered

    def normalize_health(self, provider_id: str, *, last_success: Optional[str] = None, last_failure: Optional[str] = None, latency_ms: int = 0, connection: bool = False) -> ProviderConnection:
        provider = self.providers.get(provider_id)
        if provider is None:
            raise KeyError(f"Unknown provider: {provider_id}")
        provider.health = {
            "last_success": last_success or provider.health.get("last_success", ""),
            "last_failure": last_failure or provider.health.get("last_failure", ""),
            "latency_ms": int(latency_ms),
            "connection": bool(connection),
            "status": "connected" if connection else "disconnected",
        }
        provider.state = ProviderConnectionState.CONNECTED if connection else ProviderConnectionState.INACTIVE
        self.providers[provider_id] = provider
        return provider

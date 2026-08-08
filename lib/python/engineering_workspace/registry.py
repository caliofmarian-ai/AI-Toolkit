"""
CANON-081 Engineering Workspace

CORE-022 Engineering Workspace Kernel

Workspace Registry Orchestrator

The Engineering Workspace Registry does NOT replace existing registries.
It provides a unified discovery layer over Runtime, Agent, Provider,
and Workspace services.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass(slots=True)
class RegistryEntry:
    """
    Generic registry entry describing a connected subsystem.
    """

    name: str
    component: Any
    metadata: Dict[str, Any] = field(default_factory=dict)


class EngineeringWorkspaceRegistry:
    """
    Top-level Registry Orchestrator.

    This registry keeps references to authoritative registries already
    implemented by the platform. It intentionally avoids duplicating
    RuntimeRegistry, ProviderRegistry or AgentRuntime.
    """

    def __init__(self) -> None:
        self._registries: Dict[str, RegistryEntry] = {}
        self._services: Dict[str, RegistryEntry] = {}

    # ---------------------------------------------------------
    # Registry registration
    # ---------------------------------------------------------

    def register_registry(
        self,
        name: str,
        registry: Any,
        **metadata: Any,
    ) -> None:
        self._registries[name] = RegistryEntry(
            name=name,
            component=registry,
            metadata=dict(metadata),
        )

    def registry(self, name: str) -> Optional[Any]:
        entry = self._registries.get(name)
        return None if entry is None else entry.component

    def registries(self) -> Dict[str, Any]:
        return {
            name: entry.component
            for name, entry in self._registries.items()
        }

    # ---------------------------------------------------------
    # Service registration
    # ---------------------------------------------------------

    def register_service(
        self,
        name: str,
        service: Any,
        **metadata: Any,
    ) -> None:
        self._services[name] = RegistryEntry(
            name=name,
            component=service,
            metadata=dict(metadata),
        )

    def service(self, name: str) -> Optional[Any]:
        entry = self._services.get(name)
        return None if entry is None else entry.component

    def services(self) -> Dict[str, Any]:
        return {
            name: entry.component
            for name, entry in self._services.items()
        }

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def summary(self) -> Dict[str, Any]:
        return {
            "registry_count": len(self._registries),
            "service_count": len(self._services),
            "registries": sorted(self._registries.keys()),
            "services": sorted(self._services.keys()),
        }

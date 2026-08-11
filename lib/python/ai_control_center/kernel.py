"""
AI Control Center

Engineering Kernel

Lightweight orchestration kernel.

The kernel DOES NOT replace existing registries.
It coordinates them.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass(slots=True)
class KernelContext:
    """
    Shared runtime context.
    """

    values: Dict[str, Any] = field(default_factory=dict)


class EngineeringKernel:

    def __init__(self):

        self._context = KernelContext()

        self._services: Dict[str, Any] = {}

        self._providers: Dict[str, Any] = {}

    @property
    def context(self) -> KernelContext:
        return self._context

    #
    # Services
    #

    def register_service(self, name: str, service: Any) -> None:

        self._services[name] = service

    def service(self, name: str):

        return self._services.get(name)

    def services(self):

        return dict(self._services)

    #
    # Providers
    #

    def register_provider(self, name: str, provider: Any) -> None:

        self._providers[name] = provider

    def provider(self, name: str):

        return self._providers.get(name)

    def providers(self):

        return dict(self._providers)

    #
    # Diagnostics
    #

    def summary(self):

        return {

            "service_count": len(self._services),

            "provider_count": len(self._providers),

            "services": sorted(self._services.keys()),

            "providers": sorted(self._providers.keys()),

        }

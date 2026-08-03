"""
CORE-021 — Runtime Registry
CANON-055 §11

The Registry maintains the canonical catalogue of all registered
Runtime Services and Engines.  Services and Engines must be registered
before they may execute.
"""

from typing import Any, Dict, List, Optional


class RuntimeRegistry:
    """
    Central registry for Runtime Services and Engines.

    Supports registration, discovery, and status reporting.
    """

    def __init__(self):
        self._services: Dict[str, Any] = {}
        self._engines: Dict[str, Any] = {}

    # ------------------------------------------------------------------ #
    # Services
    # ------------------------------------------------------------------ #

    def register_service(self, name: str, service: Any) -> None:
        """Register a Runtime Service."""
        self._services[name] = service

    def get_service(self, name: str) -> Optional[Any]:
        """Return the service registered under *name*, or None."""
        return self._services.get(name)

    def list_services(self) -> List[str]:
        """Return the sorted list of registered service names."""
        return sorted(self._services.keys())

    # ------------------------------------------------------------------ #
    # Engines
    # ------------------------------------------------------------------ #

    def register_engine(self, name: str, engine: Any) -> None:
        """Register a Runtime Engine."""
        self._engines[name] = engine

    def get_engine(self, name: str) -> Optional[Any]:
        """Return the engine registered under *name*, or None."""
        return self._engines.get(name)

    def list_engines(self) -> List[str]:
        """Return the sorted list of registered engine names."""
        return sorted(self._engines.keys())

    # ------------------------------------------------------------------ #
    # Summary
    # ------------------------------------------------------------------ #

    def summary(self) -> dict:
        return {
            "services": self.list_services(),
            "engines": self.list_engines(),
            "service_count": len(self._services),
            "engine_count": len(self._engines),
        }

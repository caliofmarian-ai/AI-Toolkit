"""Runtime capability management for the engineering workspace.

This module provides a lightweight registry that augments the canonical
`Capability` enum with runtime-only entries without mutating the base enum.
"""

from __future__ import annotations

from typing import Iterable, Optional, Set

from .capabilities import Capability


class CapabilitiesManager:
    """Manage canonical and runtime-defined workspace capabilities.

    The canonical capability list remains the source of truth for the base
    engineering workspace model. This manager adds a separate runtime registry
    for custom capabilities so orchestration logic can evolve without editing the
    static enum definition.
    """

    def __init__(self, custom_capabilities: Optional[Iterable[str]] = None) -> None:
        self._custom_capabilities: Set[str] = set()
        if custom_capabilities is not None:
            for capability in custom_capabilities:
                self.add_capability(capability)

    @staticmethod
    def _normalize_capability(cap: str) -> str:
        """Normalize a capability value and reject empty or null input."""
        if cap is None:
            raise ValueError("capability cannot be None")

        if isinstance(cap, Capability):
            value = cap.value
        else:
            value = str(cap).strip()

        if not value:
            raise ValueError("capability cannot be empty")

        return value

    def list_capabilities(self) -> list[str]:
        """Return the canonical and runtime-added capabilities as a sorted list."""
        capabilities = {item.value for item in Capability}
        capabilities.update(self._custom_capabilities)
        return sorted(capabilities)

    def add_capability(self, cap: str) -> None:
        """Add a runtime-defined capability without modifying the enum definition."""
        normalized = self._normalize_capability(cap)
        self._custom_capabilities.add(normalized)

    def remove_capability(self, cap: str) -> None:
        """Remove a runtime-defined capability if it was added dynamically."""
        normalized = self._normalize_capability(cap)
        self._custom_capabilities.discard(normalized)

    def has_capability(self, cap: str) -> bool:
        """Return True when the capability exists in the enum or custom registry."""
        normalized = self._normalize_capability(cap)
        if normalized in {item.value for item in Capability}:
            return True
        return normalized in self._custom_capabilities

    def reset(self) -> None:
        """Discard all runtime-only capabilities and keep only the base enum set."""
        self._custom_capabilities.clear()

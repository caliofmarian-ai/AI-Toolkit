"""
CANON-081 Engineering Workspace

CORE-022 Engineering Workspace Kernel

Engineering Service Contract

Defines the canonical lifecycle for every Engineering Workspace service.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict


class EngineeringService(ABC):
    """
    Base class for every Engineering Workspace service.
    """

    @property
    @abstractmethod
    def service_id(self) -> str:
        ...

    @property
    @abstractmethod
    def service_name(self) -> str:
        ...

    @property
    @abstractmethod
    def service_version(self) -> str:
        ...

    @abstractmethod
    def initialize(self) -> None:
        """
        Initialize the service.
        """
        ...

    @abstractmethod
    def shutdown(self) -> None:
        """
        Shutdown the service.
        """
        ...

    @abstractmethod
    def health(self) -> Dict[str, Any]:
        """
        Return current health information.
        """
        ...

    @abstractmethod
    def diagnostics(self) -> Dict[str, Any]:
        """
        Return diagnostic information.
        """
        ...

    @abstractmethod
    def capabilities(self) -> Dict[str, bool]:
        """
        Return supported capabilities.
        """
        ...

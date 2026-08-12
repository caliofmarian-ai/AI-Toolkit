"""
CANON-081 Engineering Workspace

CORE-022 Engineering Workspace Kernel

Engineering Workspace Interface

This module defines the canonical interface exposed by the
Engineering Workspace. It intentionally contains no implementation.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class EngineeringWorkspace(ABC):
    """
    Canonical Engineering Workspace interface.

    Every implementation of the Engineering Workspace shall expose
    the same high-level engineering services regardless of the
    underlying provider implementation.
    """

    # ---------------------------------------------------------
    # Core
    # ---------------------------------------------------------

    @abstractmethod
    def identity(self) -> Any:
        ...

    @abstractmethod
    def state(self) -> Any:
        ...

    @abstractmethod
    def health(self) -> Any:
        ...

    @abstractmethod
    def registry(self) -> Any:
        ...

    @abstractmethod
    def capabilities(self) -> Any:
        ...

    # ---------------------------------------------------------
    # Engineering Domains
    # ---------------------------------------------------------

    @abstractmethod
    def repository(self) -> Any:
        ...

    @abstractmethod
    def runtime(self) -> Any:
        ...

    @abstractmethod
    def context(self) -> Any:
        ...

    @abstractmethod
    def knowledge(self) -> Any:
        ...

    @abstractmethod
    def diagnostics(self) -> Any:
        ...

    # ---------------------------------------------------------
    # AI Platform
    # ---------------------------------------------------------

    @abstractmethod
    def ai_platform(self) -> Any:
        ...

    @abstractmethod
    def agent_runtime(self) -> Any:
        ...

    # ---------------------------------------------------------
    # Providers
    # ---------------------------------------------------------

    @abstractmethod
    def filesystem(self) -> Any:
        ...

    @abstractmethod
    def terminal(self) -> Any:
        ...

    @abstractmethod
    def github(self) -> Any:
        ...

    @abstractmethod
    def railway(self) -> Any:
        ...

    # ---------------------------------------------------------
    # Session
    # ---------------------------------------------------------

    @abstractmethod
    def session(self) -> Any:
        ...

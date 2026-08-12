"""
AI Control Center

Provider Foundation
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict


class Provider(ABC):

    @property
    @abstractmethod
    def provider_id(self) -> str:
        ...

    @property
    @abstractmethod
    def provider_name(self) -> str:
        ...

    @abstractmethod
    def available(self) -> bool:
        ...

    @abstractmethod
    def summary(self) -> Dict[str, Any]:
        ...

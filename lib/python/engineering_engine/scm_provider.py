from __future__ import annotations

from abc import ABC, abstractmethod

from lib.python.engineering_engine.github_publish_engine import (
    PublishOperation,
)


class SCMProvider(ABC):

    @abstractmethod
    def publish(
        self,
        operation: PublishOperation,
        *,
        plan_only: bool = True,
    ) -> str:
        raise NotImplementedError

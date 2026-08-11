"""
AI Control Center

Application Bootstrap
"""

from __future__ import annotations

from pathlib import Path

from ai_control_center.kernel import EngineeringKernel
from ai_control_center.providers import LocalRepositoryProvider


class AIControlCenter:

    def __init__(self, repository: str | Path):

        self.kernel = EngineeringKernel()

        self.repository_provider = LocalRepositoryProvider(repository)

        self.kernel.register_provider(
            self.repository_provider.provider_id,
            self.repository_provider,
        )

    def summary(self):

        return {

            "kernel": self.kernel.summary(),

            "repository": self.repository_provider.summary(),

        }

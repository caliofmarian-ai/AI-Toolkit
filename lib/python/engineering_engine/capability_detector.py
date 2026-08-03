from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class CapabilityResult:
    name: str
    implemented: bool
    evidence: str


class CapabilityDetector:

    def __init__(self, root: Path):
        self.root = root

    def _exists(self, relative_path: str) -> bool:
        return (self.root / relative_path).exists()

    def detect(self) -> list[CapabilityResult]:

        capabilities = [
            (
                "Runtime REST API",
                "lib/python/runtime/interfaces/runtime_api.py",
            ),
            (
                "OpenAPI Specification",
                "docs/openapi/runtime-api-v1.yaml",
            ),
            (
                "API Authentication",
                "lib/python/runtime/interfaces/api_auth.py",
            ),
            (
                "GraphQL Preparation",
                "lib/python/runtime/interfaces/graphql",
            ),
            (
                "MCP Preparation",
                "lib/python/runtime/interfaces/mcp",
            ),
        ]

        results = []

        for name, target in capabilities:

            exists = self._exists(target)

            results.append(
                CapabilityResult(
                    name=name,
                    implemented=exists,
                    evidence=target if exists else f"{target} not found",
                )
            )

        return results

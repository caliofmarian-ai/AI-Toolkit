from __future__ import annotations

from pathlib import Path


class CanonicalReferenceDetector:

    def __init__(self, root: Path):
        self.root = root

    def detect(self) -> list[str]:

        refs = []

        candidates = [
            "docs/openapi/runtime-api-v1.yaml",
            "docs/graphql",
            "docs/mcp",
            "implementation-packages",
            "engineering-rules",
        ]

        for candidate in candidates:

            if (self.root / candidate).exists():
                refs.append(candidate)

        return sorted(refs)

from __future__ import annotations


class AcceptanceDetector:

    def detect(self) -> list[str]:

        return [
            "Repository builds successfully",
            "Validation Engine passes",
            "Review Engine passes",
            "Planning synchronized with repository",
            "Canonical compliance preserved",
        ]

from __future__ import annotations

from pathlib import Path


class DeliverableDetector:

    def __init__(self, root: Path):
        self.root = root

    def detect(self) -> list[str]:

        deliverables = []

        candidates = [
            ("Repository Audit", "repository-audit.md"),
            ("Gap Analysis", "gap-analysis.md"),
            ("Planning Report", "planning-report.md"),
            ("Implementation Package", "IP-CORE-023.md"),
            ("Validation Report", "validation-report.md"),
            ("Review Summary", "review-summary.md"),
        ]

        package_root = self.root / "implementation-packages"

        for _, core_dir in [(None, d) for d in package_root.iterdir() if d.is_dir()]:

            for name, filename in candidates:

                if (core_dir / filename).exists():
                    deliverables.append(name)

        return sorted(set(deliverables))

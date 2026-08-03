from __future__ import annotations

from pathlib import Path

from lib.python.engineering_engine.canonical_reference_detector import CanonicalReferenceDetector
from lib.python.engineering_engine.models import (
    EngineeringBatch,
    ImplementationPackageModel,
)


class PackageBuilder:

    def __init__(self, root: Path):
        self.root = root

    def build(
        self,
        core: str,
        title: str,
        batches: list[EngineeringBatch],
    ) -> ImplementationPackageModel:

        detector = CanonicalReferenceDetector(self.root)

        canonical_references = detector.detect()

        objectives = []

        if batches:
            objectives = [batch.objective for batch in batches]
        else:
            objectives = [
                "Repository verification",
                "Canonical compliance",
                "Engineering validation",
            ]

        deliverables = [
            "Repository Audit",
            "Gap Analysis",
            "Planning Report",
            "Implementation Package",
            "Validation Report",
        ]

        acceptance = [
            "Repository builds successfully",
            "Validation passes",
            "Planning is synchronized with repository",
            "Canonical compliance preserved",
        ]

        scope = [
            batch.title for batch in batches
        ] if batches else [
            "Engineering Platform",
        ]

        return ImplementationPackageModel(
            core=core,
            title=title,
            canonical_references=canonical_references,
            objectives=objectives,
            scope=scope,
            deliverables=deliverables,
            acceptance_criteria=acceptance,
            batches=batches,
        )

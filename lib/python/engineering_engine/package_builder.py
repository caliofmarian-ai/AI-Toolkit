from __future__ import annotations

from pathlib import Path

from lib.python.engineering_engine.canonical_reference_detector import CanonicalReferenceDetector
from lib.python.engineering_engine.scope_detector import ScopeDetector
from lib.python.engineering_engine.deliverable_detector import DeliverableDetector
from lib.python.engineering_engine.acceptance_detector import AcceptanceDetector
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

        scope_detector = ScopeDetector(self.root)

        scope = scope_detector.detect()

        deliverable_detector = DeliverableDetector(self.root)

        deliverables = deliverable_detector.detect()

        if not deliverables:
            deliverables = [
            "Repository Audit",
            "Gap Analysis",
            "Planning Report",
            "Implementation Package",
            "Validation Report",
        ]

        acceptance_detector = AcceptanceDetector()

        acceptance = acceptance_detector.detect()

        if not acceptance:
            acceptance = [
            "Repository builds successfully",
            "Validation passes",
            "Planning is synchronized with repository",
            "Canonical compliance preserved",
        ]

        return ImplementationPackageModel(
            core=core,
            title=title,
            canonical_references=canonical_references,
            objectives=objectives,
            scope=scope if scope else ['Engineering Platform'],
            deliverables=deliverables,
            acceptance_criteria=acceptance,
            batches=batches,
        )

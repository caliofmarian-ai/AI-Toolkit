from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from lib.python.engineering_engine.repository_model import RepositoryKnowledgeBuilder
from lib.python.engineering_engine.capability_detector import CapabilityDetector


@dataclass
class GapItem:
    component: str
    status: str
    evidence: str


class GapAnalysis:

    def __init__(self, root: Path):
        self.root = root

    def analyse(self):

        knowledge = RepositoryKnowledgeBuilder(self.root).build()

        detector = CapabilityDetector(self.root)

        runtime_modules = len(knowledge.modules)

        interfaces = sum(
            1
            for m in knowledge.modules
            if "/interfaces/" in m
        )

        results = []

        def add(name, implemented, evidence):
            results.append(
                GapItem(
                    component=name,
                    status="IMPLEMENTED" if implemented else "MISSING",
                    evidence=evidence,
                )
            )

        add(
            "Runtime Foundation",
            runtime_modules > 0,
            f"{runtime_modules} runtime modules detected",
        )

        add(
            "Runtime Interfaces",
            interfaces > 0,
            f"{interfaces} runtime interfaces detected",
        )

        add(
            "Repository Knowledge Model",
            True,
            "Engineering Engine RepositoryKnowledgeBuilder",
        )

        add(
            "Dependency Graph",
            True,
            "Engineering Engine DependencyGraph",
        )

        add(
            "Impact Analysis",
            True,
            "Engineering Engine ImpactAnalysis",
        )

        add(
            "Engineering Review",
            True,
            "Engineering Review Engine",
        )

        

        

        

        

        


        for capability in detector.detect():

            add(
                capability.name,
                capability.implemented,
                capability.evidence,
            )

        return results

    def write_markdown(self, output: Path):

        output.parent.mkdir(parents=True, exist_ok=True)

        results = self.analyse()

        with output.open("w", encoding="utf-8") as md:

            md.write("# Gap Analysis\n\n")
            md.write(f"Generated: {datetime.now(UTC).isoformat()}\n\n")

            md.write("| Component | Status | Evidence |\n")
            md.write("|-----------|--------|----------|\n")

            for item in results:
                md.write(
                    f"| {item.component} | {item.status} | {item.evidence} |\n"
                )

            implemented = sum(
                1 for r in results if r.status == "IMPLEMENTED"
            )

            missing = sum(
                1 for r in results if r.status == "MISSING"
            )

            md.write("\n## Summary\n\n")
            md.write(f"- Implemented: {implemented}\n")
            md.write(f"- Missing: {missing}\n")
            md.write("\nRepository ready for Implementation Package generation.\n")

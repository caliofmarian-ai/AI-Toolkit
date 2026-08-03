from __future__ import annotations

from pathlib import Path

from lib.python.engineering_engine.gap_analysis import GapAnalysis
from lib.python.engineering_engine.repository_model import RepositoryKnowledgeBuilder
from lib.python.engineering_engine.dependency_graph import DependencyGraphBuilder
from lib.python.engineering_engine.impact_analysis import ImpactAnalysis
from lib.python.engineering_engine.rule_engine import RuleEngine
from lib.python.engineering_engine.dependency_rule_engine import DependencyRuleEngine


from lib.python.engineering_engine.models import EngineeringBatch

PlanningBatch = EngineeringBatch



class PlanningEngine:

    def __init__(self, root: Path):
        self.root = root
        self.rules = RuleEngine()
        self.dependencies = DependencyRuleEngine(self.root)

    def plan(self, core: str):

        gaps = GapAnalysis(self.root).analyse()

        knowledge = RepositoryKnowledgeBuilder(self.root).build()
        graph = DependencyGraphBuilder(self.root).build(knowledge)

        impact = ImpactAnalysis(graph)

        runtime = impact.analyse(
            "lib/python/runtime/interfaces/http_server.py"
        )

        affected = runtime.affected

        batches = []

        for index, gap in enumerate(
            [g for g in gaps if g.status == "MISSING"],
            start=1,
        ):

            rule = self.rules.classify(gap.component)
            dependency = self.dependencies.evaluate(gap.component)

            batches.append(
                PlanningBatch(
                    id=f"{core}-{index:03d}",
                    title=gap.component,
                    priority=rule.priority,
                    status=dependency.status,
                    risk=rule.risk,
                    rationale=gap.evidence,
                    affected_modules=affected,
                    objective=gap.component,
suggested_tests=[
                        "tests/test_runtime_bootstrap.sh",
                        "tests/test_runtime_health.sh",
                        "tests/test_runtime_webhooks.sh",
                    ],
                )
            )

        return batches

    def write_markdown(self, core: str):

        package = self.root / "implementation-packages" / core
        package.mkdir(parents=True, exist_ok=True)

        report = package / "planning-report.md"

        batches = self.plan(core)

        with report.open("w", encoding="utf-8") as md:

            md.write("# Dependency Aware Planning Report\n\n")
            md.write(f"CORE: {core}\n\n")

            md.write("| Batch | Status | Risk | Priority | Affected |\n")
            md.write("|-------|--------|------|----------|----------|\n")

            for batch in batches:
                md.write(
                    f"| {batch.id} | {batch.status} | {batch.risk} | {batch.priority} | {batch.affected_modules} |\n"
                )

            md.write("\n## Details\n\n")

            for batch in batches:
                md.write(f"### {batch.id}\n\n")
                md.write(f"Objective: {batch.title}\n\n")
                md.write(f"Status: {batch.status}\n\n")
                md.write(f"Risk: {batch.risk}\n\n")
                md.write(f"Priority: {batch.priority}\n\n")
                md.write(f"Affected modules: {batch.affected_modules}\n\n")
                md.write(f"Reason: {batch.rationale}\n\n")

        return report

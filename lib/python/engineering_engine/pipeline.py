from __future__ import annotations

from pathlib import Path

from lib.python.engineering_engine.repository_audit import RepositoryAudit
from lib.python.engineering_engine.gap_analysis import GapAnalysis
from lib.python.engineering_engine.planning_engine import PlanningEngine
from lib.python.engineering_engine.review_engine import ReviewEngine
from lib.python.engineering_engine.validation_engine import ValidationEngine
from lib.python.engineering_engine.ip_generator import (
    ImplementationPackageGenerator,
)


class EngineeringPipeline:

    def __init__(self, root: Path):
        self.root = root

    def run(self, core: str):

        package = self.root / "implementation-packages" / core
        package.mkdir(parents=True, exist_ok=True)

        RepositoryAudit(self.root).write_markdown(
            package / "repository-audit.md"
        )

        GapAnalysis(self.root).write_markdown(
            package / "gap-analysis.md"
        )

        PlanningEngine(self.root).write_markdown(core)

        model = PlanningEngine(self.root).build_package_model(core)

        ImplementationPackageGenerator(self.root).generate(model)

        ValidationEngine(self.root).validate(core)

        review = ReviewEngine(self.root).review(
            "lib/python/runtime/interfaces/http_server.py"
        )

        with (package / "review-summary.md").open(
            "w",
            encoding="utf-8",
        ) as md:

            md.write("# Engineering Review Summary\n\n")
            md.write(f"Risk: {review.risk}\n\n")

            md.write("## Affected Modules\n\n")

            for module in review.affected_modules:
                md.write(f"- {module}\n")

            md.write("\n## Suggested Tests\n\n")

            if review.affected_tests:
                for test in review.affected_tests:
                    md.write(f"- {test}\n")
            else:
                md.write("- None detected\n")

        return package

from pathlib import Path

class AuditResult:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.max_score = 0
        self.warnings = []

class Check:

    name = "Unnamed Check"

    def run(self, root):
        raise NotImplementedError


class DirectoryStructureCheck(Check):

    name = "Directory Structure"

    REQUIRED = [
        "bin",
        "lib",
        "development",
        "docs",
        "tests",
        ".ai"
    ]

    def run(self, root):

        result = AuditResult(self.name)

        for folder in self.REQUIRED:
            result.max_score += 10

            if (root / folder).exists():
                result.score += 10
            else:
                result.warnings.append(
                    f"Missing directory: {folder}"
                )

        return result


class EngineInventoryCheck(Check):

    name = "Engine Inventory"

    def run(self, root):

        result = AuditResult(self.name)

        engines = list((root / "lib").rglob("*engine*"))

        result.max_score = 20

        if len(engines) >= 10:
            result.score = 20
        elif len(engines) >= 5:
            result.score = 10
        else:
            result.score = 0
            result.warnings.append("Too few engines detected.")

        return result


class CanonicalDocumentsCheck(Check):

    name = "Canonical Documents"

    def run(self, root):

        result = AuditResult(self.name)

        docs = list((root / "docs/canonical").glob("*.md"))

        result.max_score = 20

        if len(docs) >= 10:
            result.score = 20
        else:
            result.score = 10
            result.warnings.append(
                "Canonical document count is low."
            )

        return result

class EngineTestCoverageCheck(Check):

    name = "Engine Test Coverage"

    def run(self, root):

        result = AuditResult(self.name)
        result.max_score = 20

        lib = root / "lib"
        tests = root / "tests"

        if not lib.exists():
            result.warnings.append("lib directory missing")
            return result

        engines = []

        for f in lib.rglob("*engine*.sh"):
            engines.append(f.stem)

        for f in lib.rglob("*engine*.py"):
            engines.append(f.stem)

        matched = 0

        for engine in engines:

            found = False

            for test in tests.rglob("*"):

                if engine.lower() in test.name.lower():
                    found = True
                    break

            if found:
                matched += 1
            else:
                result.warnings.append(
                    f"No test found for {engine}"
                )

        if engines:
            result.score = round(
                matched / len(engines) * result.max_score
            )

        return result


class CLIIntegrationCheck(Check):

    name = "CLI Integration"

    def run(self, root):

        result = AuditResult(self.name)
        result.max_score = 20

        launcher = root / "bin" / "ai"

        if not launcher.exists():
            result.warnings.append("bin/ai missing")
            return result

        text = launcher.read_text(encoding="utf-8")

        keywords = [
            "inspect",
            "context",
            "work",
            "git",
            "github",
            "issue"
        ]

        count = 0

        for keyword in keywords:

            if keyword in text:
                count += 1
            else:
                result.warnings.append(
                    f"CLI missing command: {keyword}"
                )

        result.score = round(
            count / len(keywords) * result.max_score
        )

        return result


class DevelopmentBatchCheck(Check):

    name = "Development Batch"

    def run(self, root):

        result = AuditResult(self.name)
        result.max_score = 20

        development = root / "development"

        if not development.exists():
            result.warnings.append(
                "development directory missing"
            )
            return result

        batches = list(
            development.glob("BATCH-*.md")
        )

        if len(batches) >= 2:
            result.score = 20
        elif len(batches) == 1:
            result.score = 10
            result.warnings.append(
                "Only one development batch found."
            )
        else:
            result.warnings.append(
                "No development batches found."
            )

        return result


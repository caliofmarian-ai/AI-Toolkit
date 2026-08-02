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

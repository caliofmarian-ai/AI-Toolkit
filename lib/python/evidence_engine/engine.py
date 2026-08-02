from pathlib import Path
from python.semantic_engine.engine import SemanticEngine


class EvidenceEngine:

    def __init__(self, repository="."):

        self.root = Path(repository).resolve()

    def find(self, keyword):

        keyword = keyword.lower()

        semantic = SemanticEngine(self.root).analyze()

        evidence = {
            "python": [],
            "shell": [],
            "tests": [],
            "docs": [],
        }

        for file in self.root.rglob("*"):

            if not file.is_file():
                continue

            if ".git" in file.parts:
                continue

            name = file.name.lower()

            if keyword not in name:
                continue

            rel = str(file.relative_to(self.root))

            if file.suffix == ".py":
                evidence["python"].append(rel)

            elif file.suffix == ".sh":
                evidence["shell"].append(rel)

            elif "test" in name:
                evidence["tests"].append(rel)

            elif file.suffix == ".md":
                evidence["docs"].append(rel)

        evidence["semantic"] = {}

        for filename, data in semantic.items():

            score = []

            for cls in data["classes"]:
                if keyword in cls.lower():
                    score.append(("class", cls))

            for fn in data["functions"]:
                if keyword in fn.lower():
                    score.append(("function", fn))

            for imp in data["imports"]:
                if keyword in imp.lower():
                    score.append(("import", imp))

            if score:
                evidence["semantic"][filename] = score

        return evidence

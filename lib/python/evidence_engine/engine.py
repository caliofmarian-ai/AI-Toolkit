from pathlib import Path


class EvidenceEngine:

    def __init__(self, repository="."):

        self.root = Path(repository).resolve()

    def find(self, keyword):

        keyword = keyword.lower()

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

        return evidence

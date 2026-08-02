from pathlib import Path
from python.evidence_engine.engine import EvidenceEngine

class CanonicalAuditEngine:

    def __init__(self, repository="."):

        self.root = Path(repository).resolve()

    def audit(self):

        report = {
            "canonical_documents": [],
            "python_modules": [],
            "missing_modules": [],
        }

        for doc in self.root.rglob("*SPEC*.md"):
            if ".git" not in doc.parts:
                report["canonical_documents"].append(doc.stem)

        for module in self.root.rglob("*.py"):
            if ".git" not in module.parts:
                report["python_modules"].append(module.stem)

        module_names = set(report["python_modules"])

        evidence_engine = EvidenceEngine(self.root)

        report["evidence"] = {}


        for doc in report["canonical_documents"]:

            base = (
                doc.replace("_SPEC", "")
                   .replace("_v1.0.0", "")
                   .replace("_v2.0.0", "")
                   .lower()
            )

            found = False

            for module in module_names:
                if base in module.lower():
                    found = True
                    break

            if found:
                report["evidence"][doc] = evidence_engine.find(base)
            else:
                report["missing_modules"].append(doc)

        return report

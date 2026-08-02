from pathlib import Path
from python.evidence_engine.engine import EvidenceEngine

class CanonicalAuditEngine:

    def __init__(self, repository=".", workspace_index=None):

        self.root = Path(repository).resolve()
        self._workspace_index = workspace_index

    def _get_index(self):
        if self._workspace_index is not None:
            return self._workspace_index
        from python.workspace_index import WorkspaceIndexBuilder
        return WorkspaceIndexBuilder(self.root).build()

    def audit(self):

        index = self._get_index()

        report = {
            "canonical_documents": [],
            "python_modules": [],
            "missing_modules": [],
        }

        for doc in index.markdown_files():
            if "SPEC" in doc.name:
                report["canonical_documents"].append(Path(doc.name).stem)

        for module in index.python_files():
            report["python_modules"].append(Path(module.name).stem)

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

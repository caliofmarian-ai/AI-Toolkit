from pathlib import Path


class DiscoveryEngine:

    PATTERNS = [
        "*SPEC*.md",
        "*MAP*.md",
        "*ARCHITECTURE*.md",
        "*INVARIANT*.md",
        "*CANON*.md",
    ]

    def __init__(self, root="."):

        self.root = Path(root).resolve()

    def discover_canonical_documents(self):

        documents = {}

        for pattern in self.PATTERNS:

            for file in self.root.rglob(pattern):

                if ".git" in file.parts:
                    continue

                documents[file.stem] = str(
                    file.relative_to(self.root)
                )

        return dict(sorted(documents.items()))

    def statistics(self):

        docs = self.discover_canonical_documents()

        return {
            "canonical_documents": len(docs)
        }

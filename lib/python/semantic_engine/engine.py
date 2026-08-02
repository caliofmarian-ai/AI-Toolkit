"""
Semantic Engine
"""
import ast
from pathlib import Path


class SemanticEngine:

    def __init__(self, repository=".", workspace_index=None):

        self.root = Path(repository).resolve()
        self._workspace_index = workspace_index

    def _get_index(self):
        if self._workspace_index is not None:
            return self._workspace_index
        from python.workspace_index import WorkspaceIndexBuilder
        return WorkspaceIndexBuilder(self.root).build()

    def analyze(self):

        index = self._get_index()

        report = {}

        for wf in index.python_files():

            file = Path(index.repository_root) / wf.path

            try:
                tree = ast.parse(
                    file.read_text(encoding="utf-8")
                )
            except Exception:
                continue

            symbols = {
                "classes": [],
                "functions": [],
                "imports": [],
            }

            for node in ast.walk(tree):

                if isinstance(node, ast.ClassDef):
                    symbols["classes"].append(node.name)

                elif isinstance(node, ast.FunctionDef):
                    symbols["functions"].append(node.name)

                elif isinstance(node, ast.Import):
                    for item in node.names:
                        symbols["imports"].append(item.name)

                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        symbols["imports"].append(node.module)

            report[wf.path] = symbols

        return report

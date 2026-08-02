import ast
from pathlib import Path


class SemanticEngine:

    def __init__(self, repository="."):

        self.root = Path(repository).resolve()

    def analyze(self):

        report = {}

        for file in self.root.rglob("*.py"):

            if ".git" in file.parts:
                continue

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

            report[str(file.relative_to(self.root))] = symbols

        return report

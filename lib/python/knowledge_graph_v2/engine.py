import ast
import json
from pathlib import Path


class KnowledgeGraphEngine:

    def __init__(self, repository="."):

        self.root = Path(repository).resolve()

    def build(self):

        graph = {
            "nodes": [],
            "edges": [],
        }

        known = set()

        for file in self.root.rglob("*.py"):

            if ".git" in file.parts:
                continue

            node = str(file.relative_to(self.root))

            if node not in known:
                known.add(node)
                graph["nodes"].append(node)

            try:
                tree = ast.parse(
                    file.read_text(encoding="utf-8")
                )
            except Exception:
                continue

            for item in ast.walk(tree):

                if isinstance(item, ast.Import):

                    for mod in item.names:

                        graph["edges"].append({
                            "from": node,
                            "to": mod.name,
                            "type": "import"
                        })

                elif isinstance(item, ast.ImportFrom):

                    if item.module:

                        graph["edges"].append({
                            "from": node,
                            "to": item.module,
                            "type": "from_import"
                        })

        return graph

    def export(self, filename):

        graph = self.build()

        path = Path(filename)
        path.parent.mkdir(parents=True, exist_ok=True)

        path.write_text(
            json.dumps(graph, indent=2),
            encoding="utf-8"
        )

        return graph

import ast
import json
from pathlib import Path


class KnowledgeGraphEngine:

    def __init__(self, repository=".", workspace_index=None):

        self.root = Path(repository).resolve()
        self._workspace_index = workspace_index

    def _get_index(self):
        if self._workspace_index is not None:
            return self._workspace_index
        from python.workspace_index import WorkspaceIndexBuilder
        return WorkspaceIndexBuilder(self.root).build()

    def build(self):

        index = self._get_index()

        graph = {
            "nodes": [],
            "edges": [],
        }

        known = set()

        for wf in index.python_files():

            node = wf.path

            if node not in known:
                known.add(node)
                graph["nodes"].append(node)

            file = Path(index.repository_root) / wf.path

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

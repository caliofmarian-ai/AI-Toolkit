import json
import re
from pathlib import Path

from python.semantic_repository_intelligence.import_graph import ImportGraphBuilder

from .models import DependencyMap


class DependencyDiscovery:

    def discover(self, root: Path, file_analyses) -> DependencyMap:
        manifests = {
            "requirements.txt": self._requirements(root / "requirements.txt"),
            "package.json": self._package_json(root / "package.json"),
            "go.mod": self._go_mod(root / "go.mod"),
            "Gemfile": self._gemfile(root / "Gemfile"),
        }

        manifests = {
            key: value for key, value in manifests.items() if value
        }

        graph = ImportGraphBuilder().build(file_analyses, root)
        unresolved_imports = sum(1 for edge in graph.edges if edge.resolved is None)

        return DependencyMap(
            manifests=manifests,
            internal_import_edges=len(graph.edges),
            internal_import_nodes=len(graph.nodes),
            unresolved_imports=unresolved_imports,
        )

    def _requirements(self, path: Path):
        if not path.exists():
            return []
        dependencies = []
        for raw in path.read_text(encoding="utf-8", errors="ignore").splitlines():
            line = raw.strip()
            if not line or line.startswith("#") or line.startswith("-"):
                continue
            dependencies.append(line)
        return dependencies

    def _package_json(self, path: Path):
        if not path.exists():
            return []
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return []
        dependencies = []
        for section in ("dependencies", "devDependencies", "peerDependencies", "optionalDependencies"):
            for name, version in (data.get(section) or {}).items():
                dependencies.append(f"{name}@{version}")
        return sorted(set(dependencies))

    def _go_mod(self, path: Path):
        if not path.exists():
            return []
        content = path.read_text(encoding="utf-8", errors="ignore")
        dependencies = []
        in_require_block = False
        for raw in content.splitlines():
            line = raw.strip()
            if line.startswith("require ("):
                in_require_block = True
                continue
            if in_require_block and line == ")":
                in_require_block = False
                continue
            if line.startswith("require "):
                entry = line[len("require "):].strip()
                if entry:
                    dependencies.append(entry)
                continue
            if in_require_block and line and not line.startswith("//"):
                dependencies.append(line)
        return dependencies

    def _gemfile(self, path: Path):
        if not path.exists():
            return []
        dependencies = []
        regex = re.compile(r"""^\s*gem\s+['"]([^'"]+)['"](?:\s*,\s*['"]([^'"]+)['"])?""")
        for raw in path.read_text(encoding="utf-8", errors="ignore").splitlines():
            match = regex.match(raw)
            if not match:
                continue
            name = match.group(1)
            version = match.group(2)
            dependencies.append(f"{name} {version}".strip() if version else name)
        return dependencies

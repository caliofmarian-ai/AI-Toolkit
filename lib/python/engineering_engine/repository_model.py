from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import ast

from lib.python.engineering_engine.repository_scanner import RepositoryScanner


@dataclass
class PythonModule:

    path: str

    imports: list[str] = field(default_factory=list)

    classes: list[str] = field(default_factory=list)

    functions: list[str] = field(default_factory=list)


@dataclass
class RepositoryKnowledge:

    modules: dict[str, PythonModule] = field(default_factory=dict)


class RepositoryKnowledgeBuilder:

    def __init__(self, root: Path):

        self.root = root

        self.scanner = RepositoryScanner(root)

    def build(self):

        scan = self.scanner.scan()

        knowledge = RepositoryKnowledge()

        files = (
            scan.runtime_modules
            + scan.runtime_interfaces
            + scan.engineering_modules
        )

        for rel in files:

            path = self.root / rel

            try:

                tree = ast.parse(path.read_text(encoding="utf-8"))

            except Exception:

                continue

            module = PythonModule(path=rel)

            for node in ast.walk(tree):

                if isinstance(node, ast.Import):

                    for alias in node.names:

                        module.imports.append(alias.name)

                elif isinstance(node, ast.ImportFrom):

                    module.imports.append(
                        node.module or ""
                    )

                elif isinstance(node, ast.ClassDef):

                    module.classes.append(node.name)

                elif isinstance(node, ast.FunctionDef):

                    module.functions.append(node.name)

            knowledge.modules[rel] = module

        return knowledge

"""
Semantic Repository Intelligence — Relationship Resolver
CORE-008B

Resolves symbolic references (import strings, qualified names) to actual
file paths within the repository.  Exported as a standalone class so that
other engines (CallGraphBuilder, ArchitectureGraphBuilder, etc.) can reuse it.
"""

import os
from pathlib import Path
from typing import Dict, Optional, Set

from .models import FileAnalysis


class RelationshipResolver:
    """
    Resolves symbolic Python import strings to relative file paths inside the
    repository and provides module-to-file lookup utilities for other graph
    builders.
    """

    def __init__(
        self,
        root: Path,
        file_analyses: Dict[str, FileAnalysis],
    ):
        self.root = root
        self._analyses = file_analyses
        self._python_paths: Set[str] = {
            p for p, fa in file_analyses.items() if fa.language == "python"
        }
        # Build module→path mapping for quick lookup
        self._module_map: Dict[str, str] = self._build_module_map()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def resolve_import(
        self, source_path: str, module: str, level: int = 0
    ) -> Optional[str]:
        """
        Resolve *module* as imported from *source_path* (with *level* for
        relative imports) to a relative repository file path.

        Returns the resolved path or None if the module is external.
        """
        module_rel = module.replace(".", "/")

        if level > 0:
            source_dir = os.path.dirname(source_path)
            for _ in range(level - 1):
                source_dir = os.path.dirname(source_dir)
            candidates = [
                _norm(os.path.join(source_dir, module_rel + ".py")),
                _norm(os.path.join(source_dir, module_rel, "__init__.py")),
            ]
        else:
            candidates = [
                _norm(module_rel + ".py"),
                _norm(os.path.join(module_rel, "__init__.py")),
            ]
            # Also check the module map for installed-like imports
            if module in self._module_map:
                return self._module_map[module]

        for cand in candidates:
            if cand in self._python_paths:
                return cand
            # Allow prefix match (e.g. lib/python/foo.py matches foo)
            for path in self._python_paths:
                if _norm(path).endswith("/" + cand):
                    return path

        return None

    def resolve_symbol(self, qualified_name: str) -> Optional[str]:
        """
        Attempt to resolve a dotted qualified name (e.g.
        ``python.ai_cto_scanner.engine.AICTOScannerEngine``) to a file path.
        """
        parts = qualified_name.split(".")
        # Try progressively shorter module prefixes
        for i in range(len(parts), 0, -1):
            module = ".".join(parts[:i])
            result = self.resolve_import("", module, 0)
            if result:
                return result
        return None

    def file_to_module(self, file_path: str) -> str:
        """Convert a relative file path to a dotted module name."""
        path = _norm(file_path)
        if path.endswith("/__init__.py"):
            path = path[: -len("/__init__.py")]
        elif path.endswith(".py"):
            path = path[:-3]
        return path.replace("/", ".")

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _build_module_map(self) -> Dict[str, str]:
        """
        Build a mapping from dotted module name → relative file path for all
        Python files in the workspace.
        """
        module_map: Dict[str, str] = {}
        for path in sorted(self._python_paths):
            module = self.file_to_module(path)
            module_map[module] = path
            # Also map the last component so ``import engine`` resolves to
            # ``python/foo/engine.py``.
            last = module.split(".")[-1]
            if last not in module_map:
                module_map[last] = path
        return module_map


def _norm(path: str) -> str:
    """Normalise path separators to forward slashes and strip leading ./"""
    p = path.replace("\\", "/")
    while p.startswith("./"):
        p = p[2:]
    return p

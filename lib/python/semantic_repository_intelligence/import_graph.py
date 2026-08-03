"""
Semantic Repository Intelligence — Import Graph Builder
CORE-008B

Builds a directed graph of module imports, resolves symbolic imports to file
paths within the repository, detects circular dependencies, identifies critical
(highly-imported) and orphan (never-imported) modules.
"""

import os
from collections import defaultdict, deque
from pathlib import Path
from typing import Dict, List, Optional, Set

from .models import FileAnalysis, ImportEdge, ImportGraphResult


class RelationshipResolver:
    """
    Resolves symbolic Python import strings to relative file paths within the
    repository.  Non-Python / external imports are returned as-is with
    resolved=None.
    """

    def __init__(self, root: Path, all_python_paths: Set[str]):
        self.root = root
        self._python_paths = all_python_paths  # set of relative paths like "lib/python/foo/bar.py"

    def resolve(self, source_path: str, module: str, level: int) -> Optional[str]:
        """
        Attempt to resolve *module* to a relative file path.

        Returns the relative path if found, else None.
        """
        # Build candidate paths from the symbolic module name
        module_rel = module.replace(".", "/")

        # Handle relative imports (level > 0)
        if level > 0:
            source_dir = os.path.dirname(source_path)
            for _ in range(level - 1):
                source_dir = os.path.dirname(source_dir)
            candidates = [
                os.path.join(source_dir, module_rel + ".py"),
                os.path.join(source_dir, module_rel, "__init__.py"),
            ]
        else:
            candidates = [
                module_rel + ".py",
                os.path.join(module_rel, "__init__.py"),
            ]

        # Normalise separators for platform independence
        for cand in candidates:
            cand = cand.replace("\\", "/")
            if cand in self._python_paths:
                return cand
            # Try with various repo-root prefixes (e.g. "lib/python/foo.py")
            for path in self._python_paths:
                if path.replace("\\", "/").endswith("/" + cand):
                    return path

        return None


class ImportGraphBuilder:
    """
    Builds an ImportGraph from the file-level FileAnalysis results produced by
    ASTAnalyzer.
    """

    # Number of top modules by in-degree to classify as "critical"
    CRITICAL_TOP_N = 10
    # Minimum in-degree to be considered critical
    CRITICAL_MIN_DEGREE = 3

    def build(
        self,
        file_analyses: Dict[str, FileAnalysis],
        root: Path,
    ) -> ImportGraphResult:
        """
        Build the import graph from the given file analyses.

        Parameters
        ----------
        file_analyses:
            dict mapping relative path → FileAnalysis (as returned by ASTAnalyzer)
        root:
            absolute path to the repository root
        """
        python_paths: Set[str] = {
            p for p, fa in file_analyses.items() if fa.language == "python"
        }
        resolver = RelationshipResolver(root, python_paths)

        nodes: List[str] = sorted(python_paths)
        edges: List[ImportEdge] = []
        in_degree: Dict[str, int] = defaultdict(int)

        for path, analysis in sorted(file_analyses.items()):
            if analysis.language != "python":
                continue
            for imp in analysis.imports:
                resolved = resolver.resolve(path, imp.module, imp.level)
                confidence = 1.0 if resolved else 0.5
                edge = ImportEdge(
                    source=path,
                    target=imp.module,
                    resolved=resolved,
                    confidence=confidence,
                )
                edges.append(edge)
                if resolved:
                    in_degree[resolved] += 1

        # Build adjacency for cycle detection
        adj: Dict[str, List[str]] = defaultdict(list)
        for edge in edges:
            if edge.resolved:
                adj[edge.source].append(edge.resolved)

        circular = self._find_cycles(nodes, adj)

        # Critical modules: top-N by in-degree (with minimum threshold)
        sorted_by_degree = sorted(
            in_degree.items(), key=lambda kv: kv[1], reverse=True
        )
        critical = [
            p for p, deg in sorted_by_degree
            if deg >= self.CRITICAL_MIN_DEGREE
        ][:self.CRITICAL_TOP_N]

        # Orphan modules: Python files that no other Python file imports
        imported_targets: Set[str] = {e.resolved for e in edges if e.resolved}
        orphan = sorted(p for p in python_paths if p not in imported_targets)

        return ImportGraphResult(
            nodes=nodes,
            edges=edges,
            circular_dependencies=circular,
            critical_modules=critical,
            orphan_modules=orphan,
            in_degree=dict(in_degree),
        )

    # ------------------------------------------------------------------
    # Cycle detection (iterative DFS)
    # ------------------------------------------------------------------

    def _find_cycles(
        self,
        nodes: List[str],
        adj: Dict[str, List[str]],
    ) -> List[List[str]]:
        """
        Return a list of cycles found in the directed graph using an iterative
        DFS with a path stack.  Each cycle is expressed as the minimal list of
        nodes that form the loop.

        Limits to 20 unique cycles to avoid combinatorial explosion on large
        monorepos.
        """
        visited: Set[str] = set()
        cycles: List[List[str]] = []
        MAX_CYCLES = 20

        for start in sorted(nodes):
            if start in visited or len(cycles) >= MAX_CYCLES:
                break
            stack = [(start, [start], {start})]
            while stack and len(cycles) < MAX_CYCLES:
                node, path, path_set = stack.pop()
                for neighbour in sorted(adj.get(node, [])):
                    if neighbour in path_set:
                        # Found a cycle — extract the loop portion
                        idx = path.index(neighbour)
                        cycle = path[idx:]
                        # Deduplicate: check for rotation equivalence
                        if not self._is_duplicate_cycle(cycle, cycles):
                            cycles.append(cycle)
                    elif neighbour not in visited:
                        stack.append((neighbour, path + [neighbour], path_set | {neighbour}))
            visited.add(start)

        return cycles

    def _is_duplicate_cycle(
        self, cycle: List[str], existing: List[List[str]]
    ) -> bool:
        """Return True if *cycle* is a rotation of any cycle in *existing*."""
        key = frozenset(cycle)
        for ex in existing:
            if frozenset(ex) == key:
                return True
        return False

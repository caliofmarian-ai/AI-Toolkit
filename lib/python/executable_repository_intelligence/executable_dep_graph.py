"""
Executable Repository Intelligence — Executable Dependency Graph Builder
CORE-008C

Builds a dependency graph that contains ONLY executable files.

Excludes:
  - Markdown / documentation files
  - Generated reports
  - Canonical specification documents
  - Temporary files
  - Build artifacts
"""

from pathlib import Path
from typing import Dict, List, Set

from .models import (
    ExecutableDependencyEdge,
    ExecutableDependencyGraph,
    FileClassification,
)


# Categories excluded from the executable dependency graph
_EXCLUDED_CATEGORIES = frozenset([
    "Documentation",
    "Generated Artifact",
    "Reports",
    "Canonical Specification",
    "Temporary",
    "Deprecated",
    "Assets",
])

# Categories that are executable
_EXECUTABLE_CATEGORIES = frozenset([
    "Executable Code",
    "Runtime Entry Point",
    "Bootstrap",
    "Public API",
    "Internal API",
    "Plugin API",
    "Extension Point",
    "Scripts",
])


class ExecutableDependencyGraphBuilder:
    """
    Builds a dependency graph restricted to executable files.

    Reuses CORE-008B import graph data (resolved paths) without re-parsing.
    """

    def build(
        self,
        file_classifications: List[FileClassification],
        file_analyses: Dict,           # path → FileAnalysis (CORE-008B)
        import_graph_result,           # ImportGraphResult (CORE-008B)
        root: Path,
    ) -> ExecutableDependencyGraph:
        """Build and return the ExecutableDependencyGraph."""

        # Determine which files are executable nodes and which are excluded
        exec_nodes: Set[str] = set()
        excluded: List[str] = []
        exclusion_reasons: Dict[str, str] = {}

        cat_map = {fc.path: fc for fc in file_classifications}

        for fc in file_classifications:
            if fc.category in _EXCLUDED_CATEGORIES:
                excluded.append(fc.path)
                exclusion_reasons[fc.path] = "Category: %s" % fc.category
            elif fc.is_executable or fc.category in _EXECUTABLE_CATEGORIES:
                exec_nodes.add(fc.path)
            else:
                # Non-executable, non-documentation files (e.g. Config, Env)
                excluded.append(fc.path)
                exclusion_reasons[fc.path] = "Non-executable: %s" % fc.category

        # Build edges from the CORE-008B import graph edges
        edges: List[ExecutableDependencyEdge] = []
        seen_edges: Set[tuple] = set()

        # Walk CORE-008B import edges
        import_edges = getattr(import_graph_result, "edges", [])
        for edge in import_edges:
            source = edge.source
            target = edge.resolved  # only follow resolved (internal) edges
            if not target:
                continue
            if source in exec_nodes and target in exec_nodes:
                key = (source, target)
                if key not in seen_edges:
                    seen_edges.add(key)
                    edges.append(ExecutableDependencyEdge(
                        source=source,
                        target=target,
                        kind="import",
                    ))

        # Sort for determinism
        edges.sort(key=lambda e: (e.source, e.target))
        excluded_sorted = sorted(set(excluded))

        return ExecutableDependencyGraph(
            nodes=sorted(exec_nodes),
            edges=edges,
            excluded=excluded_sorted,
            exclusion_reasons=exclusion_reasons,
        )

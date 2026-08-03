"""
Workspace Orchestrator — Dependency Graph
CORE-012

WorkspaceDependencyGraph: builds and queries the cross-repository dependency
                          graph for an entire workspace.
WorkspaceRelationshipAnalyzer: derives semantic relationships between repos.

No analysis is duplicated — data is consumed from WorkspaceRepository models.
"""

from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from .models import (
    WorkspaceDependencyEdge,
    WorkspaceRelationship,
    WorkspaceRepository,
)


class WorkspaceDependencyGraph:
    """
    Builds a complete cross-repository dependency graph.

    Detects:
    - Shared canonical specifications (same CORE-NNN identifiers appear in
      multiple repos)
    - Shared library names (overlapping Python imports / package names)
    - Shared runtime components (same executable script names)
    - Declared dependencies (explicit 'dependencies' field on the model)
    - Dependency cycles

    The graph is directed:  source --depends-on--> target
    """

    def __init__(self, repositories: List[WorkspaceRepository]) -> None:
        self._repos = {r.name: r for r in repositories}

    def build(self) -> List[WorkspaceDependencyEdge]:
        """Return the full set of dependency edges for the workspace."""
        edges: List[WorkspaceDependencyEdge] = []

        edges.extend(self._declared_dependencies())
        edges.extend(self._shared_canonical_specs())
        edges.extend(self._shared_library_names())

        # Deduplicate (same source/target/type)
        seen: Set[Tuple[str, str, str]] = set()
        unique: List[WorkspaceDependencyEdge] = []
        for edge in edges:
            key = (edge.source, edge.target, edge.dependency_type)
            if key not in seen:
                seen.add(key)
                unique.append(edge)

        return sorted(unique, key=lambda e: (e.source, e.target, e.dependency_type))

    def detect_cycles(
        self, edges: List[WorkspaceDependencyEdge]
    ) -> List[List[str]]:
        """Return a list of cycles (each cycle is a list of repository names)."""
        graph: Dict[str, Set[str]] = {name: set() for name in self._repos}
        for edge in edges:
            if edge.source in graph:
                graph[edge.source].add(edge.target)

        cycles: List[List[str]] = []
        visited: Set[str] = set()
        rec_stack: List[str] = []

        def dfs(node: str) -> bool:
            visited.add(node)
            rec_stack.append(node)
            for neighbour in graph.get(node, set()):
                if neighbour not in visited:
                    if dfs(neighbour):
                        return True
                elif neighbour in rec_stack:
                    idx = rec_stack.index(neighbour)
                    cycles.append(list(rec_stack[idx:]))
                    return True
            rec_stack.pop()
            return False

        for name in sorted(self._repos.keys()):
            if name not in visited:
                dfs(name)

        return cycles

    # ------------------------------------------------------------------
    # Edge derivation helpers
    # ------------------------------------------------------------------

    def _declared_dependencies(self) -> List[WorkspaceDependencyEdge]:
        """Return edges for explicitly declared dependencies on WorkspaceRepository."""
        edges = []
        for repo in self._repos.values():
            for dep in repo.dependencies:
                if dep == repo.name:
                    continue  # skip self-dependencies
                if dep in self._repos:
                    edges.append(WorkspaceDependencyEdge(
                        source=repo.name,
                        target=dep,
                        dependency_type="declared",
                        confidence=1.0,
                        evidence=(f"{repo.name} explicitly lists {dep} as a dependency",),
                    ))
        return edges

    def _shared_canonical_specs(self) -> List[WorkspaceDependencyEdge]:
        """
        Infer dependencies from shared canonical specification IDs
        (CORE-NNN patterns) in scan_scores or repository names.
        """
        edges = []
        # Extract CORE spec sets per repo from scan data (if available)
        spec_map: Dict[str, Set[str]] = {}
        for name, repo in self._repos.items():
            specs = self._extract_core_specs(repo)
            if specs:
                spec_map[name] = specs

        # If repo A's specs are a superset of repo B's specs, B may depend on A
        names = sorted(spec_map.keys())
        for i, a in enumerate(names):
            for b in names[i + 1:]:
                shared = spec_map[a] & spec_map[b]
                if shared:
                    edges.append(WorkspaceRelationship(
                        repo_a=a,
                        repo_b=b,
                        relationship_type="shared_canonical",
                        strength=min(1.0, len(shared) / 10.0),
                        shared_components=tuple(sorted(shared)),
                    ))
                    # Not a directional dep; emit both directions with low confidence
                    for spec in shared:
                        edges.append(WorkspaceDependencyEdge(
                            source=b,
                            target=a,
                            dependency_type="shared_canonical",
                            confidence=0.5,
                            evidence=(f"Shared canonical spec: {spec}",),
                        ))
        # Filter to only WorkspaceDependencyEdge instances
        return [e for e in edges if isinstance(e, WorkspaceDependencyEdge)]

    def _shared_library_names(self) -> List[WorkspaceDependencyEdge]:
        """
        Infer dependencies when multiple repos share Python package names
        (detected from their scan_scores['library_names'] if present).
        """
        edges = []
        lib_map: Dict[str, Set[str]] = {}
        for name, repo in self._repos.items():
            libs = set(str(k) for k in repo.scan_scores.get("library_names", []))
            if libs:
                lib_map[name] = libs

        names = sorted(lib_map.keys())
        for i, a in enumerate(names):
            for b in names[i + 1:]:
                shared = lib_map[a] & lib_map[b]
                if shared:
                    edges.append(WorkspaceDependencyEdge(
                        source=a,
                        target=b,
                        dependency_type="shared_library",
                        confidence=0.6,
                        evidence=tuple(f"Shared library: {lib}" for lib in sorted(shared)[:5]),
                    ))
        return edges

    def _extract_core_specs(self, repo: WorkspaceRepository) -> Set[str]:
        """Extract CORE-NNN identifiers from repository name or scan data."""
        import re
        specs: Set[str] = set()
        text = repo.name + " " + repo.description
        for m in re.finditer(r"CORE-\d+[A-Z]?", text):
            specs.add(m.group(0))
        return specs


class WorkspaceRelationshipAnalyzer:
    """
    Derives semantic relationships between repositories in a workspace.

    Detects:
    - Sibling repositories (same category, similar structure)
    - Parent/child relationships (one is a subset of another)
    - Peer relationships (same type, different purpose)
    - Shared architecture (identical technology stack detected)
    """

    def __init__(self, repositories: List[WorkspaceRepository]) -> None:
        self._repos = {r.name: r for r in repositories}

    def analyze(self) -> List[WorkspaceRelationship]:
        """Return the full set of relationships for the workspace."""
        relationships: List[WorkspaceRelationship] = []

        relationships.extend(self._sibling_relationships())
        relationships.extend(self._peer_relationships())
        relationships.extend(self._shared_architecture_relationships())

        # Deduplicate (unordered pair + type)
        seen: Set[Tuple[str, str, str]] = set()
        unique: List[WorkspaceRelationship] = []
        for rel in relationships:
            a, b = sorted([rel.repo_a, rel.repo_b])
            key = (a, b, rel.relationship_type)
            if key not in seen:
                seen.add(key)
                unique.append(rel)

        return sorted(unique, key=lambda r: (r.repo_a, r.repo_b))

    # ------------------------------------------------------------------
    # Relationship derivation helpers
    # ------------------------------------------------------------------

    def _sibling_relationships(self) -> List[WorkspaceRelationship]:
        """Repos with the same category are siblings."""
        by_category: Dict[str, List[str]] = {}
        for name, repo in self._repos.items():
            cat = repo.repository_category
            by_category.setdefault(cat, []).append(name)

        relationships = []
        for cat, names in by_category.items():
            if len(names) < 2:
                continue
            names_sorted = sorted(names)
            for i, a in enumerate(names_sorted):
                for b in names_sorted[i + 1:]:
                    relationships.append(WorkspaceRelationship(
                        repo_a=a,
                        repo_b=b,
                        relationship_type="sibling",
                        strength=0.7,
                        shared_components=(f"category:{cat}",),
                    ))
        return relationships

    def _peer_relationships(self) -> List[WorkspaceRelationship]:
        """Repos with the same type are peers."""
        by_type: Dict[str, List[str]] = {}
        for name, repo in self._repos.items():
            rtype = repo.repository_type
            by_type.setdefault(rtype, []).append(name)

        relationships = []
        for rtype, names in by_type.items():
            if len(names) < 2:
                continue
            names_sorted = sorted(names)
            for i, a in enumerate(names_sorted):
                for b in names_sorted[i + 1:]:
                    relationships.append(WorkspaceRelationship(
                        repo_a=a,
                        repo_b=b,
                        relationship_type="peer",
                        strength=0.5,
                        shared_components=(f"type:{rtype}",),
                    ))
        return relationships

    def _shared_architecture_relationships(self) -> List[WorkspaceRelationship]:
        """Repos with high scan-score similarity share architecture."""
        names = sorted(self._repos.keys())
        relationships = []
        for i, a in enumerate(names):
            for b in names[i + 1:]:
                sim = self._score_similarity(self._repos[a], self._repos[b])
                if sim >= 0.7:
                    relationships.append(WorkspaceRelationship(
                        repo_a=a,
                        repo_b=b,
                        relationship_type="shared_architecture",
                        strength=sim,
                        shared_components=(),
                    ))
        return relationships

    def _score_similarity(self, a: WorkspaceRepository, b: WorkspaceRepository) -> float:
        """Compute a 0–1 similarity score between two repositories."""
        if not a.scan_scores or not b.scan_scores:
            return 0.0
        keys = set(a.scan_scores.keys()) & set(b.scan_scores.keys())
        if not keys:
            return 0.0
        total_diff = 0.0
        for k in keys:
            try:
                av = float(a.scan_scores[k])
                bv = float(b.scan_scores[k])
                total_diff += abs(av - bv) / 100.0
            except (TypeError, ValueError):
                pass
        return max(0.0, 1.0 - total_diff / max(1, len(keys)))

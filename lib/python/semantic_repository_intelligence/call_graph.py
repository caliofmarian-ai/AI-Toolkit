"""
Semantic Repository Intelligence — Call Graph Builder
CORE-008B

Builds a call graph from AST-level FileAnalysis results, identifies entry
points and traces the most significant execution chains.
"""

from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Set

from .models import CallEdge, CallGraphResult, FileAnalysis, FunctionSymbol

# How deep we trace execution chains
_MAX_CHAIN_DEPTH = 8
# Maximum number of execution chains to return
_MAX_CHAINS = 20


class CallGraphBuilder:
    """
    Builds a call graph from the FileAnalysis results produced by ASTAnalyzer.

    For Python files, the AST analyzer records the names of functions/methods
    called within each function body.  This builder links those names back to
    their definition sites to produce directed edges.

    For non-Python files (TypeScript, etc.) the call graph is partial because
    we rely on regex-based analysis only.
    """

    def build(
        self,
        file_analyses: Dict[str, FileAnalysis],
        root: Path,
    ) -> CallGraphResult:
        # Step 1: build a name → (file, FunctionSymbol) lookup for all functions
        func_index: Dict[str, List[tuple]] = defaultdict(list)
        for path, analysis in sorted(file_analyses.items()):
            for func in analysis.functions:
                func_index[func.name].append((path, func))

        # Step 2: build call edges
        edges: List[CallEdge] = []
        for path, analysis in sorted(file_analyses.items()):
            for func in analysis.functions:
                for callee in func.calls:
                    # Only record edges to known internal functions
                    if callee in func_index:
                        edges.append(CallEdge(
                            caller_file=path,
                            caller_func=func.name,
                            callee=callee,
                            line=func.line,
                        ))

        # Step 3: identify entry points
        entry_points = self._find_entry_points(file_analyses, func_index)

        # Step 4: trace execution chains from each entry point
        adj: Dict[str, Set[str]] = defaultdict(set)
        for edge in edges:
            adj[edge.caller_func].add(edge.callee)

        chains = self._trace_chains(entry_points, adj)

        return CallGraphResult(
            edges=edges,
            entry_points=sorted(entry_points),
            execution_chains=chains,
        )

    # ------------------------------------------------------------------
    # Entry point detection
    # ------------------------------------------------------------------

    def _find_entry_points(
        self,
        file_analyses: Dict[str, FileAnalysis],
        func_index: Dict[str, List[tuple]],
    ) -> List[str]:
        """
        Identify entry-point references as ``<file>::<func>`` strings.

        An entry point is:
        - a function named main / run / start / execute
        - a function decorated with common entry-point decorators
        - a ``__main__`` sentinel in a file
        """
        ENTRY_NAMES = frozenset(["main", "run", "start", "execute", "startup"])
        ENTRY_DECORATORS = frozenset([
            "app.route", "router.get", "router.post", "dp.message",
            "router.message", "click.command", "cli.command",
        ])

        result: List[str] = []
        for path, analysis in sorted(file_analyses.items()):
            if "__main__" in analysis.entry_points:
                result.append("%s::__main__" % path)
            for func in analysis.functions:
                if func.name in ENTRY_NAMES:
                    result.append("%s::%s" % (path, func.name))
                elif any(d in ENTRY_DECORATORS for d in func.decorators):
                    result.append("%s::%s" % (path, func.name))
        return result

    # ------------------------------------------------------------------
    # Chain tracing (iterative DFS)
    # ------------------------------------------------------------------

    def _trace_chains(
        self,
        entry_points: List[str],
        adj: Dict[str, Set[str]],
    ) -> List[List[str]]:
        """Trace execution chains from each entry point, avoiding infinite loops."""
        chains: List[List[str]] = []

        for ep in entry_points[:_MAX_CHAINS]:
            # Extract the function name from the "file::func" reference
            func_name = ep.split("::")[-1]
            chain = self._dfs_chain(func_name, adj, set(), _MAX_CHAIN_DEPTH)
            if len(chain) > 1:
                chains.append(chain)
            if len(chains) >= _MAX_CHAINS:
                break

        return chains

    def _dfs_chain(
        self,
        func: str,
        adj: Dict[str, Set[str]],
        visited: Set[str],
        depth: int,
    ) -> List[str]:
        """Return the longest chain reachable from *func* via DFS."""
        if depth == 0 or func in visited:
            return [func]
        visited = visited | {func}
        best = [func]
        for callee in sorted(adj.get(func, [])):
            chain = [func] + self._dfs_chain(callee, adj, visited, depth - 1)
            if len(chain) > len(best):
                best = chain
        return best

"""
Semantic Repository Intelligence Engine — CORE-008B

Orchestrates the full semantic analysis pipeline:

  ASTAnalyzer
    → ImportGraphBuilder
    → CallGraphBuilder
    → DependencyGraphBuilder
    → ArchitectureGraphBuilder
    → InjectionPointAnalyzer
    → RelationshipResolver
    → ConfidenceEngine
    → SemanticRecommendationEngine
    → SemanticPersistence

Integrates with CORE-007 (WorkspaceIndex) and CORE-008A (AICTOScannerEngine).
"""

from pathlib import Path
from typing import Any, Dict, Optional

from .ast_analyzer import ASTAnalyzer
from .import_graph import ImportGraphBuilder
from .call_graph import CallGraphBuilder
from .dependency_graph import DependencyGraphBuilder
from .architecture_graph import ArchitectureGraphBuilder
from .injection_point_analyzer import InjectionPointAnalyzer
from .relationship_resolver import RelationshipResolver
from .confidence_engine import ConfidenceEngine
from .recommendation_engine import SemanticRecommendationEngine
from .persistence import SemanticPersistence
from .models import RepositoryComplexity


# Suggested next CORE implementation based on heuristics
_NEXT_CORE_SUGGESTIONS = [
    ("CORE-009", "Development State Engine",
     "Persist full development state for cross-session reasoning."),
    ("CORE-010", "Project Memory Engine",
     "Build persistent project memory from semantic snapshots."),
    ("CORE-011", "Executive Briefing Engine",
     "Generate daily AI CTO executive briefings from semantic knowledge."),
    ("CORE-012", "AI CTO Telegram Workspace",
     "Expose AI CTO intelligence through the Telegram control plane."),
]


class SemanticRepositoryEngine:
    """
    Semantic Repository Intelligence Engine.

    Understands software architecture instead of merely locating files.
    Discovers relationships between components and generates explainable,
    evidence-based recommendations.

    Usage::

        engine = SemanticRepositoryEngine(repository="/path/to/repo")
        result = engine.analyze()

    The *result* dict is fully serialisable to JSON and is suitable for
    embedding in the AI CTO integration report.
    """

    def __init__(
        self,
        repository: str = ".",
        workspace_index=None,
        persist: bool = True,
    ):
        self.root = Path(repository).resolve()
        self._workspace_index = workspace_index
        self._persist = persist

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def analyze(self) -> Dict[str, Any]:
        """
        Run the full semantic analysis pipeline.

        Returns a comprehensive dict with all graph results, recommendations,
        findings, and complexity metrics.  Output is deterministic — identical
        repositories produce identical results.
        """
        # Phase 1 — AST analysis
        ast_analyzer = ASTAnalyzer(self.root, workspace_index=self._workspace_index)
        file_analyses = ast_analyzer.analyze()

        # Phase 2 — Relationship resolution (needed by multiple builders)
        resolver = RelationshipResolver(self.root, file_analyses)

        # Phase 3 — Import graph
        import_builder = ImportGraphBuilder()
        import_graph = import_builder.build(file_analyses, self.root)

        # Phase 4 — Call graph
        call_builder = CallGraphBuilder()
        call_graph = call_builder.build(file_analyses, self.root)

        # Phase 5 — Dependency graph
        dep_builder = DependencyGraphBuilder()
        dep_graph = dep_builder.build(file_analyses, self.root)

        # Phase 6 — Architecture graph
        arch_builder = ArchitectureGraphBuilder()
        arch_graph = arch_builder.build(file_analyses, import_graph, self.root)

        # Phase 7 — Injection point analysis
        inj_analyzer = InjectionPointAnalyzer()
        injection_points = inj_analyzer.analyze(file_analyses, self.root)

        # Phase 8 — Semantic recommendations and findings
        rec_engine = SemanticRecommendationEngine()
        recommendations = rec_engine.generate(
            import_graph=import_graph,
            call_graph=call_graph,
            dependency_graph=dep_graph,
            architecture_graph=arch_graph,
            injection_points=injection_points,
        )
        findings = rec_engine.generate_findings(
            import_graph=import_graph,
            architecture_graph=arch_graph,
            injection_points=injection_points,
        )

        # Phase 9 — Complexity metrics
        complexity = self._compute_complexity(file_analyses)

        # Phase 10 — Suggest next CORE implementation
        next_core = self._suggest_next_core(arch_graph, import_graph, injection_points)

        result = {
            "repository": str(self.root),
            "file_count": len(file_analyses),
            "ast_analysis": {
                path: fa.to_dict()
                for path, fa in sorted(file_analyses.items())
            },
            "import_graph": import_graph.to_dict(),
            "call_graph": call_graph.to_dict(),
            "dependency_graph": dep_graph.to_dict(),
            "architecture_graph": arch_graph.to_dict(),
            "injection_points": [ip.to_dict() for ip in injection_points],
            "recommendations": [r.to_dict() for r in recommendations],
            "semantic_findings": [f.to_dict() for f in findings],
            "complexity": complexity.to_dict(),
            "next_core": next_core,
        }

        # Phase 11 — Persist semantic knowledge
        if self._persist:
            try:
                persistence = SemanticPersistence(self.root)
                persistence.save(result)
            except (OSError, IOError):
                pass

        return result

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _compute_complexity(self, file_analyses) -> RepositoryComplexity:
        """Aggregate complexity metrics across all file analyses."""
        total_functions = 0
        total_classes = 0
        total_imports = 0
        max_imports = 0
        max_functions = 0
        lang_dist: Dict[str, int] = {}

        for path, fa in file_analyses.items():
            lang_dist[fa.language] = lang_dist.get(fa.language, 0) + 1
            total_functions += len(fa.functions)
            total_classes += len(fa.classes)
            total_imports += len(fa.imports)
            if len(fa.imports) > max_imports:
                max_imports = len(fa.imports)
            if len(fa.functions) > max_functions:
                max_functions = len(fa.functions)

        n = max(1, len(file_analyses))
        total_symbols = total_functions + total_classes

        # Cyclomatic complexity estimate: rough heuristic based on branch count
        # (1 + avg branches per function) where branches are estimated as
        # 0.3 * avg number of calls per function
        avg_calls = sum(
            len(func.calls)
            for fa in file_analyses.values()
            for func in fa.functions
        ) / max(1, total_functions)
        cyclomatic = round(1.0 + avg_calls * 0.3, 2)

        return RepositoryComplexity(
            total_files=n,
            total_symbols=total_symbols,
            total_imports=total_imports,
            total_functions=total_functions,
            total_classes=total_classes,
            avg_imports_per_module=total_imports / n,
            avg_functions_per_file=total_functions / n,
            max_imports_in_module=max_imports,
            max_functions_in_file=max_functions,
            cyclomatic_complexity_estimate=cyclomatic,
            language_distribution=dict(sorted(lang_dist.items())),
        )

    def _suggest_next_core(self, arch_graph, import_graph, injection_points) -> str:
        """
        Suggest the most appropriate next CORE implementation based on the
        current analysis state.
        """
        # If there are many injection points, a state engine is the right next step
        if len(injection_points) > 10:
            core_id, core_name, rationale = _NEXT_CORE_SUGGESTIONS[0]
        # If the architecture graph is complex (many nodes), memory is needed
        elif arch_graph.node_count >= 8:
            core_id, core_name, rationale = _NEXT_CORE_SUGGESTIONS[1]
        # Otherwise suggest the briefing engine
        else:
            core_id, core_name, rationale = _NEXT_CORE_SUGGESTIONS[2]

        return "%s — %s: %s" % (core_id, core_name, rationale)

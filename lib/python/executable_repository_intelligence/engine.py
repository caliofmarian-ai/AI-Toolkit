"""
Executable Repository Intelligence Engine — CORE-008C

Orchestrates the full executable analysis pipeline on top of CORE-008B:

  SemanticRepositoryEngine (CORE-008B)
    → FileClassifier
    → RuntimeMapBuilder
    → ExecutableDependencyGraphBuilder
    → InjectionSafetyClassifier
    → ZoneClassifier
    → ExecutableRecommendationEngine
    → ExecutablePersistence
    → ExecutionModelReportGenerator

The engine is the authoritative repository execution model for all future
CORE modules.  It NEVER re-implements CORE-008B logic — it REUSES the
SemanticRepositoryEngine output.
"""

import sys
from collections import Counter
from pathlib import Path
from typing import Any, Dict, Optional

from python.semantic_repository_intelligence import SemanticRepositoryEngine
from python.semantic_repository_intelligence.ast_analyzer import ASTAnalyzer
from python.semantic_repository_intelligence.import_graph import ImportGraphBuilder

from .file_classifier import FileClassifier
from .runtime_map import RuntimeMapBuilder
from .executable_dep_graph import ExecutableDependencyGraphBuilder
from .injection_safety import InjectionSafetyClassifier
from .zone_classifier import ZoneClassifier
from .recommendations import ExecutableRecommendationEngine
from .persistence import ExecutablePersistence
from .report import ExecutionModelReportGenerator
from .models import ExecutableRepositoryResult


class ExecutableRepositoryEngine:
    """
    Executable Repository Intelligence Engine.

    Determines which files participate in runtime execution and which are
    informational only.  Produces a deterministic, JSON-serialisable result.

    Usage::

        engine = ExecutableRepositoryEngine(repository="/path/to/repo")
        result = engine.analyze()

    The *result* dict is suitable for embedding in the AI CTO integration
    report and for persisting to .ai/runtime_repository_model.json.
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
        Run the full executable intelligence pipeline.

        Calls CORE-008B SemanticRepositoryEngine first, then builds the
        executable layer on top.  Returns a fully serialisable dict.
        """
        # Phase 1 — CORE-008B semantic analysis (reuse, do not duplicate)
        semantic_engine = SemanticRepositoryEngine(
            repository=str(self.root),
            workspace_index=self._workspace_index,
            persist=False,   # We persist our own outputs below
        )
        semantic_result = semantic_engine.analyze()

        # Phase 1b — Obtain live FileAnalysis objects and ImportGraphResult by
        # reusing CORE-008B components directly (AST + import resolution).
        # This avoids duplicating any semantic logic.
        ast_analyzer = ASTAnalyzer(self.root, workspace_index=self._workspace_index)
        file_analyses = ast_analyzer.analyze()

        import_builder = ImportGraphBuilder()
        import_graph_result = import_builder.build(file_analyses, self.root)

        # Reconstruct InjectionPoint-like objects from semantic result
        injection_points = self._deserialize_injection_points(
            semantic_result.get("injection_points", [])
        )

        # Phase 2 — File classification
        classifier = FileClassifier()
        file_classifications = classifier.classify_all(file_analyses, self.root)

        # Phase 3 — Runtime map
        runtime_builder = RuntimeMapBuilder()
        runtime_map = runtime_builder.build(file_classifications, file_analyses, self.root)

        # Phase 4 — Executable dependency graph
        dep_builder = ExecutableDependencyGraphBuilder()
        dep_graph = dep_builder.build(
            file_classifications, file_analyses, import_graph_result, self.root
        )

        # Phase 5 — Injection safety
        safety_classifier = InjectionSafetyClassifier()
        injection_safety = safety_classifier.classify(
            injection_points, file_classifications, self.root
        )

        # Phase 6 — Zone classification
        zone_classifier = ZoneClassifier()
        zones = zone_classifier.classify(file_classifications, self.root)

        # Phase 7 — Recommendations
        rec_engine = ExecutableRecommendationEngine()
        recommendations = rec_engine.generate(
            file_classifications, runtime_map, dep_graph, zones, injection_safety
        )

        # Phase 8 — Assemble result
        executable_count = sum(1 for fc in file_classifications if fc.is_executable)
        non_executable_count = len(file_classifications) - executable_count

        category_dist: Dict[str, int] = Counter(fc.category for fc in file_classifications)
        zone_dist: Dict[str, int] = Counter(z.zone for z in zones)
        safety_dist: Dict[str, int] = Counter(r.safety for r in injection_safety)

        result_obj = ExecutableRepositoryResult(
            repository=str(self.root),
            file_classifications=file_classifications,
            runtime_map=runtime_map,
            executable_dependency_graph=dep_graph,
            injection_safety=injection_safety,
            zones=zones,
            recommendations=recommendations,
            executable_file_count=executable_count,
            non_executable_file_count=non_executable_count,
            category_distribution=dict(sorted(category_dist.items())),
            zone_distribution=dict(sorted(zone_dist.items())),
            safety_distribution=dict(sorted(safety_dist.items())),
        )

        result = result_obj.to_dict()

        # Phase 9 — Persist outputs
        if self._persist:
            try:
                persistence = ExecutablePersistence(self.root)
                runtime_model_path = persistence.save_runtime_model(result)
                exec_map_path = persistence.save_executable_map(result)
                print("[CORE-008C] Written: %s" % runtime_model_path, file=sys.stderr)
                print("[CORE-008C] Written: %s" % exec_map_path, file=sys.stderr)
            except Exception as exc:
                print("[CORE-008C] WARNING: Persistence failed: %s" % exc, file=sys.stderr)

            # Phase 10 — Generate AI_CTO_EXECUTION_MODEL.md
            try:
                report_gen = ExecutionModelReportGenerator()
                report_path = self.root / "AI_CTO_EXECUTION_MODEL.md"
                report_gen.generate(result, report_path)
                print("[CORE-008C] Written: %s" % report_path, file=sys.stderr)
            except Exception as exc:
                print("[CORE-008C] WARNING: Report generation failed: %s" % exc, file=sys.stderr)

        return result

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _deserialize_injection_points(self, ip_dicts):
        """
        Reconstruct lightweight InjectionPoint-like objects from serialised dicts.
        """
        class _IP:
            __slots__ = ("name", "type", "file", "line", "pattern", "confidence", "evidence")

            def __init__(self, d):
                self.name = d.get("name", "")
                self.type = d.get("type", "")
                self.file = d.get("file", "")
                self.line = d.get("line", 0)
                self.pattern = d.get("pattern", "")
                self.confidence = d.get("confidence", 0.5)
                self.evidence = d.get("evidence", [])

        return [_IP(d) for d in ip_dicts]


"""
Executable Repository Intelligence — Recommendation Engine
CORE-008C

Generates evidence-based, executable-specific recommendations.
Does NOT duplicate CORE-008B semantic recommendations.
"""

from typing import List

from .models import (
    ExecutableDependencyGraph,
    ExecutableRecommendation,
    FileClassification,
    RepositoryRuntimeMap,
    RepositoryZone,
    InjectionSafetyRecord,
)


class ExecutableRecommendationEngine:
    """
    Generates executable-layer recommendations from the full analysis.
    """

    def generate(
        self,
        file_classifications: List[FileClassification],
        runtime_map: RepositoryRuntimeMap,
        dep_graph: ExecutableDependencyGraph,
        zones: List[RepositoryZone],
        injection_safety: List[InjectionSafetyRecord],
    ) -> List[ExecutableRecommendation]:
        recs: List[ExecutableRecommendation] = []

        recs.extend(self._doc_in_runtime(zones))
        recs.extend(self._entry_point_isolation(runtime_map, file_classifications))
        recs.extend(self._unsafe_injection_points(injection_safety))
        recs.extend(self._generated_in_runtime(zones))
        recs.extend(self._missing_entry_point(runtime_map))
        recs.extend(self._high_coupling(dep_graph, file_classifications))

        # Assign stable sequential IDs
        for i, rec in enumerate(recs, start=1):
            rec.id = "EXEC-REC-%03d" % i

        return recs

    # ------------------------------------------------------------------
    # Rule generators
    # ------------------------------------------------------------------

    def _doc_in_runtime(
        self, zones: List[RepositoryZone]
    ) -> List[ExecutableRecommendation]:
        """Detect documentation files in Runtime zones."""
        doc_in_runtime = [
            z for z in zones
            if z.zone == "Runtime" and any("Documentation" in e for e in z.evidence)
        ]
        if not doc_in_runtime:
            return []
        affected = [z.path for z in doc_in_runtime[:5]]
        return [ExecutableRecommendation(
            id="",
            title="Move documentation out of runtime directories",
            description=(
                "Documentation files found in runtime zones: %s. "
                "Separate documentation into a dedicated /docs directory to keep "
                "the runtime surface clean and reduce deployment artifact size."
                % ", ".join(affected)
            ),
            category="isolation",
            priority="medium",
            confidence=0.85,
            evidence=["Zones with documentation in runtime: %d" % len(doc_in_runtime)],
            affected_files=affected,
        )]

    def _entry_point_isolation(
        self,
        runtime_map: RepositoryRuntimeMap,
        file_classifications: List[FileClassification],
    ) -> List[ExecutableRecommendation]:
        """Detect multiple entry points that could be consolidated."""
        entry_points = [
            fc for fc in file_classifications
            if fc.category == "Runtime Entry Point"
        ]
        if len(entry_points) <= 1:
            return []
        return [ExecutableRecommendation(
            id="",
            title="Improve entry-point isolation",
            description=(
                "%d runtime entry points detected (%s). "
                "Consider consolidating into a single well-defined entry point "
                "or clearly separating concerns between entry points."
                % (
                    len(entry_points),
                    ", ".join(fc.path for fc in entry_points[:3]),
                )
            ),
            category="entry_point",
            priority="medium",
            confidence=0.80,
            evidence=[
                "Entry points: %s" % ", ".join(fc.path for fc in entry_points)
            ],
            affected_files=[fc.path for fc in entry_points],
        )]

    def _unsafe_injection_points(
        self, injection_safety: List[InjectionSafetyRecord]
    ) -> List[ExecutableRecommendation]:
        """Flag injection points classified as UNSAFE."""
        unsafe = [r for r in injection_safety if r.safety == "UNSAFE"]
        if not unsafe:
            return []
        affected = sorted(set(r.file for r in unsafe))
        return [ExecutableRecommendation(
            id="",
            title="Eliminate unsafe injection points",
            description=(
                "%d UNSAFE injection points detected in: %s. "
                "These use dynamic code execution (eval, exec, subprocess, etc.) "
                "which allows arbitrary code injection. Replace with safe, "
                "statically-typed alternatives."
                % (len(unsafe), ", ".join(affected[:3]))
            ),
            category="isolation",
            priority="critical",
            confidence=0.90,
            evidence=["%s — %s" % (r.name, r.rationale) for r in unsafe[:5]],
            affected_files=affected,
        )]

    def _generated_in_runtime(
        self, zones: List[RepositoryZone]
    ) -> List[ExecutableRecommendation]:
        """Detect generated artifacts mixed into runtime zones."""
        gen_in_runtime = [
            z for z in zones
            if z.zone == "Runtime" and any("Generated" in e for e in z.evidence)
        ]
        if not gen_in_runtime:
            return []
        affected = [z.path for z in gen_in_runtime[:5]]
        return [ExecutableRecommendation(
            id="",
            title="Separate generated artifacts from runtime code",
            description=(
                "Generated artifacts found in runtime zones: %s. "
                "Move generated files (reports, compiled outputs, caches) to a "
                "dedicated directory (e.g. /build, /dist, /.ai) and add them to "
                ".gitignore."
                % ", ".join(affected)
            ),
            category="generation",
            priority="low",
            confidence=0.75,
            evidence=["Zones with generated artifacts in runtime: %d" % len(gen_in_runtime)],
            affected_files=affected,
        )]

    def _missing_entry_point(
        self, runtime_map: RepositoryRuntimeMap
    ) -> List[ExecutableRecommendation]:
        """Recommend adding a clear main entry point if none is found."""
        if runtime_map.main_entry_point:
            return []
        return [ExecutableRecommendation(
            id="",
            title="Define a clear main runtime entry point",
            description=(
                "No unambiguous main entry point was detected. "
                "Add a main.py / __main__.py or clearly document the primary "
                "execution entry point to make the runtime topology explicit."
            ),
            category="entry_point",
            priority="high",
            confidence=0.80,
            evidence=["No file matched entry-point patterns"],
            affected_files=[],
        )]

    def _high_coupling(
        self,
        dep_graph: ExecutableDependencyGraph,
        file_classifications: List[FileClassification],
    ) -> List[ExecutableRecommendation]:
        """Identify executable files with very high in-degree (heavily depended upon)."""
        from collections import Counter
        in_degree: Counter = Counter()
        for edge in dep_graph.edges:
            in_degree[edge.target] += 1

        threshold = 5
        hotspots = [
            (path, count)
            for path, count in in_degree.most_common(10)
            if count >= threshold
        ]
        if not hotspots:
            return []

        affected = [p for p, _ in hotspots]
        return [ExecutableRecommendation(
            id="",
            title="Reduce coupling in high-dependency executable modules",
            description=(
                "%d executable module(s) have high in-degree (≥%d dependents): %s. "
                "Consider splitting these into smaller, more focused modules to "
                "reduce coupling and improve testability."
                % (len(hotspots), threshold, ", ".join(affected[:3]))
            ),
            category="coupling",
            priority="medium",
            confidence=0.80,
            evidence=[
                "%s: %d dependents" % (p, c) for p, c in hotspots[:5]
            ],
            affected_files=affected,
        )]

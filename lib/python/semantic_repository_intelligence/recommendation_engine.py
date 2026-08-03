"""
Semantic Repository Intelligence — Semantic Recommendation Engine
CORE-008B

Generates evidence-based, prioritised recommendations from the semantic
analysis results.  Every recommendation carries:

  - Confidence score
  - Supporting evidence
  - Affected modules
  - Estimated implementation effort, architectural impact, and technical risk
  - Recommended implementation order
"""

from typing import Dict, List, Optional

from .confidence_engine import ConfidenceEngine
from .models import (
    ArchitectureGraphResult,
    CallGraphResult,
    DependencyGraphResult,
    ImportGraphResult,
    InjectionPoint,
    SemanticFinding,
    SemanticRecommendation,
)


class SemanticRecommendationEngine:
    """
    Generates semantic recommendations from all graph analysis results.
    """

    def __init__(self):
        self._confidence = ConfidenceEngine()

    def generate(
        self,
        import_graph: ImportGraphResult,
        call_graph: CallGraphResult,
        dependency_graph: DependencyGraphResult,
        architecture_graph: ArchitectureGraphResult,
        injection_points: List[InjectionPoint],
        next_core: Optional[str] = None,
    ) -> List[SemanticRecommendation]:
        """Generate the full list of recommendations sorted by priority and order."""
        recs: List[SemanticRecommendation] = []

        recs.extend(self._circular_dependency_recs(import_graph))
        recs.extend(self._orphan_module_recs(import_graph))
        recs.extend(self._hotspot_recs(import_graph, architecture_graph))
        recs.extend(self._architecture_risk_recs(architecture_graph))
        recs.extend(self._extension_point_recs(architecture_graph, injection_points))
        recs.extend(self._dependency_recs(dependency_graph))
        recs.extend(self._entry_point_recs(call_graph))

        # Assign stable implementation order (sort by priority, then confidence desc)
        priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        recs.sort(
            key=lambda r: (priority_order.get(r.priority, 9), -r.confidence)
        )
        for idx, rec in enumerate(recs, 1):
            rec.implementation_order = idx

        return recs

    # ------------------------------------------------------------------
    # Recommendation generators
    # ------------------------------------------------------------------

    def _circular_dependency_recs(
        self, import_graph: ImportGraphResult
    ) -> List[SemanticRecommendation]:
        recs = []
        for idx, cycle in enumerate(import_graph.circular_dependencies[:5], 1):
            cycle_str = " → ".join(cycle + [cycle[0]])
            recs.append(SemanticRecommendation(
                id="REC-CIRC-%03d" % idx,
                title="Break circular dependency: %s" % " ↔ ".join(cycle[:2]),
                description=(
                    "Circular import detected: %s. "
                    "Circular imports prevent Python modules from being imported cleanly "
                    "and introduce hidden coupling. Introduce an interface layer or move "
                    "shared symbols to a dedicated utilities module."
                    % cycle_str
                ),
                category="dependency",
                priority="high",
                confidence=self._confidence.score(0.95, [cycle_str], cross_reference_count=len(cycle), evidence_tier="ast"),
                evidence=[cycle_str],
                affected_modules=cycle,
                estimated_effort="medium",
                estimated_impact="high",
                estimated_risk="medium",
                implementation_order=0,
            ))
        return recs

    def _orphan_module_recs(
        self, import_graph: ImportGraphResult
    ) -> List[SemanticRecommendation]:
        orphans = import_graph.orphan_modules
        if len(orphans) <= 2:
            return []
        sample = sorted(orphans)[:5]
        return [SemanticRecommendation(
            id="REC-ORPH-001",
            title="Investigate %d orphan modules" % len(orphans),
            description=(
                "%d Python modules are never imported by any other module in the repository. "
                "They may be dead code, standalone scripts, or missing integration links. "
                "Review and either integrate or remove them."
                % len(orphans)
            ),
            category="architecture",
            priority="medium",
            confidence=self._confidence.score(0.75, sample, cross_reference_count=len(orphans), evidence_tier="ast"),
            evidence=["Orphan modules: %s" % ", ".join(sample)],
            affected_modules=sample,
            estimated_effort="small",
            estimated_impact="medium",
            estimated_risk="low",
            implementation_order=0,
        )]

    def _hotspot_recs(
        self,
        import_graph: ImportGraphResult,
        architecture_graph: ArchitectureGraphResult,
    ) -> List[SemanticRecommendation]:
        recs = []
        for idx, hotspot in enumerate(architecture_graph.hotspots[:3], 1):
            in_deg = import_graph.in_degree.get(hotspot, 0)
            recs.append(SemanticRecommendation(
                id="REC-HOT-%03d" % idx,
                title="Reduce coupling on hotspot: %s" % hotspot,
                description=(
                    "%s is imported by %d other modules, making it an architectural hotspot. "
                    "Consider splitting this module or extracting an interface to reduce coupling."
                    % (hotspot, in_deg)
                ),
                category="architecture",
                priority="medium",
                confidence=self._confidence.score(0.80, [hotspot], cross_reference_count=in_deg, evidence_tier="ast"),
                evidence=["in-degree: %d" % in_deg],
                affected_modules=[hotspot],
                estimated_effort="large",
                estimated_impact="high",
                estimated_risk="medium",
                implementation_order=0,
            ))
        return recs

    def _architecture_risk_recs(
        self, architecture_graph: ArchitectureGraphResult
    ) -> List[SemanticRecommendation]:
        recs = []
        for idx, risk in enumerate(architecture_graph.risks, 1):
            priority = {"critical": "critical", "high": "high", "medium": "medium"}.get(
                risk.severity, "low"
            )
            recs.append(SemanticRecommendation(
                id="REC-RISK-%03d" % idx,
                title="Address architecture risk: %s" % risk.title,
                description=risk.description,
                category="architecture",
                priority=priority,
                confidence=risk.confidence,
                evidence=risk.evidence,
                affected_modules=risk.affected_modules[:5],
                estimated_effort="medium",
                estimated_impact="high",
                estimated_risk="medium",
                implementation_order=0,
            ))
        return recs

    def _extension_point_recs(
        self,
        architecture_graph: ArchitectureGraphResult,
        injection_points: List[InjectionPoint],
    ) -> List[SemanticRecommendation]:
        recs = []
        ep_count = len(architecture_graph.extension_points)
        ip_count = len(injection_points)
        if ep_count < 3 and ip_count < 5:
            recs.append(SemanticRecommendation(
                id="REC-EXT-001",
                title="Define formal extension points",
                description=(
                    "The repository has only %d identified extension points and %d injection points. "
                    "Introducing formal plugin interfaces, event buses, or middleware hooks will "
                    "improve extensibility for future CORE implementations."
                    % (ep_count, ip_count)
                ),
                category="extension",
                priority="medium",
                confidence=self._confidence.score(0.65, architecture_graph.extension_points, evidence_tier="heuristic"),
                evidence=["Extension points: %d" % ep_count, "Injection points: %d" % ip_count],
                affected_modules=architecture_graph.extension_points[:5],
                estimated_effort="medium",
                estimated_impact="high",
                estimated_risk="low",
                implementation_order=0,
            ))
        return recs

    def _dependency_recs(
        self, dependency_graph: DependencyGraphResult
    ) -> List[SemanticRecommendation]:
        recs = []
        if dependency_graph.dependency_count == 0:
            recs.append(SemanticRecommendation(
                id="REC-DEP-001",
                title="No manifest-declared external dependencies found",
                description=(
                    "No requirements.txt, package.json, or similar manifest file was found. "
                    "Ensure all external dependencies are declared to enable reproducible builds "
                    "and dependency vulnerability scanning."
                ),
                category="dependency",
                priority="medium",
                confidence=0.80,
                evidence=["No manifest files detected"],
                affected_modules=[],
                estimated_effort="small",
                estimated_impact="medium",
                estimated_risk="high",
                implementation_order=0,
            ))
        elif dependency_graph.dependency_count > 50:
            recs.append(SemanticRecommendation(
                id="REC-DEP-002",
                title="Large dependency footprint (%d packages)" % dependency_graph.dependency_count,
                description=(
                    "The repository declares %d external dependencies. "
                    "Consider auditing for unused or transitive dependencies to reduce supply-chain risk."
                    % dependency_graph.dependency_count
                ),
                category="dependency",
                priority="low",
                confidence=0.70,
                evidence=["%d external dependencies" % dependency_graph.dependency_count],
                affected_modules=[],
                estimated_effort="small",
                estimated_impact="medium",
                estimated_risk="medium",
                implementation_order=0,
            ))
        return recs

    def _entry_point_recs(
        self, call_graph: CallGraphResult
    ) -> List[SemanticRecommendation]:
        if not call_graph.entry_points:
            return [SemanticRecommendation(
                id="REC-EP-001",
                title="No clear entry points detected",
                description=(
                    "The call graph analysis found no identifiable entry points (main functions, "
                    "CLI handlers, or __main__ sentinels). Adding a clear application entry point "
                    "improves discoverability and AI CTO context awareness."
                ),
                category="architecture",
                priority="low",
                confidence=0.65,
                evidence=["No entry points found in call graph"],
                affected_modules=[],
                estimated_effort="trivial",
                estimated_impact="medium",
                estimated_risk="low",
                implementation_order=0,
            )]
        return []

    # ------------------------------------------------------------------
    # Semantic findings (observations without recommendations)
    # ------------------------------------------------------------------

    def generate_findings(
        self,
        import_graph: ImportGraphResult,
        architecture_graph: ArchitectureGraphResult,
        injection_points: List[InjectionPoint],
    ) -> List[SemanticFinding]:
        findings: List[SemanticFinding] = []
        fid = [0]

        def next_id():
            fid[0] += 1
            return "FIND-%04d" % fid[0]

        # Critical module observation
        for mod in import_graph.critical_modules[:5]:
            findings.append(SemanticFinding(
                id=next_id(),
                category="dependency",
                title="Critical module: %s" % mod,
                description="This module has a high in-degree and is central to the repository architecture.",
                severity="info",
                evidence=["in-degree: %d" % import_graph.in_degree.get(mod, 0)],
                affected_modules=[mod],
                confidence=0.90,
            ))

        # Injection point observations
        ip_types: Dict[str, int] = {}
        for ip in injection_points:
            ip_types[ip.type] = ip_types.get(ip.type, 0) + 1
        for ip_type, count in sorted(ip_types.items()):
            findings.append(SemanticFinding(
                id=next_id(),
                category="pattern",
                title="%d %s patterns detected" % (count, ip_type),
                description="The repository uses %d %s extension patterns." % (count, ip_type),
                severity="info",
                evidence=["%d instances" % count],
                affected_modules=[],
                confidence=0.80,
            ))

        # Architecture layer summary
        for node in architecture_graph.nodes:
            if node.in_degree >= 2 or node.out_degree >= 2:
                findings.append(SemanticFinding(
                    id=next_id(),
                    category="structure",
                    title="Layer '%s' has significant connectivity" % node.name,
                    description=(
                        "Layer '%s' has in-degree %d and out-degree %d, "
                        "indicating it plays a central role in the architecture."
                        % (node.name, node.in_degree, node.out_degree)
                    ),
                    severity="info",
                    evidence=["in-degree: %d, out-degree: %d" % (node.in_degree, node.out_degree)],
                    affected_modules=node.modules[:5],
                    confidence=0.85,
                ))

        return findings

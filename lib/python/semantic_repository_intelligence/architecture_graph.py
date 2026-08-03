"""
Semantic Repository Intelligence — Architecture Graph Builder
CORE-008B

Categorises repository modules into architectural layers, builds a directed
dependency graph between layers, and identifies hotspots, risks, and potential
extension points.
"""

import re
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Set, Tuple

from .models import (
    ArchitectureEdge,
    ArchitectureGraphResult,
    ArchitectureNode,
    ArchitectureRisk,
    FileAnalysis,
    ImportGraphResult,
)


# ---------------------------------------------------------------------------
# Layer classification rules
# ---------------------------------------------------------------------------

# Each rule is (layer_name, [(pattern_type, value), ...])
# pattern_type is one of: "path_contains", "filename_contains", "import_has"
_LAYER_RULES: List[Tuple[str, List[Tuple[str, str]]]] = [
    ("CLI", [
        ("path_contains", "/cli/"),
        ("filename_contains", "cli"),
        ("path_contains", "/bin/"),
    ]),
    ("Agent Runtime", [
        ("path_contains", "agent_runtime"),
        ("path_contains", "/agents/"),
        ("filename_contains", "_agent"),
    ]),
    ("Canonical Intelligence", [
        ("path_contains", "canonical"),
        ("path_contains", "knowledge_graph"),
        ("filename_contains", "canonical"),
    ]),
    ("Semantic Analysis", [
        ("path_contains", "semantic"),
        ("filename_contains", "semantic"),
    ]),
    ("Workspace", [
        ("path_contains", "workspace"),
        ("filename_contains", "workspace"),
    ]),
    ("Scanning / Detection", [
        ("path_contains", "ai_cto_scanner"),
        ("path_contains", "repository_inspector"),
        ("path_contains", "discovery_engine"),
        ("filename_contains", "scanner"),
        ("filename_contains", "detector"),
    ]),
    ("Planning", [
        ("path_contains", "planning"),
        ("path_contains", "batch_planner"),
        ("path_contains", "batch_generator"),
        ("filename_contains", "planner"),
    ]),
    ("Reporting", [
        ("path_contains", "reporting"),
        ("filename_contains", "report"),
    ]),
    ("Compliance / Coverage / Drift", [
        ("path_contains", "compliance_engine"),
        ("path_contains", "coverage_engine"),
        ("path_contains", "drift_engine"),
    ]),
    ("Memory / State", [
        ("path_contains", "memory"),
        ("path_contains", "session"),
        ("filename_contains", "memory"),
        ("filename_contains", "state"),
    ]),
    ("Validation", [
        ("path_contains", "validation"),
        ("filename_contains", "validation"),
    ]),
    ("Testing", [
        ("path_contains", "/tests/"),
        ("filename_contains", "test_"),
    ]),
    ("Configuration / Profiles", [
        ("path_contains", "project_profile"),
        ("filename_contains", "config"),
        ("filename_contains", "settings"),
    ]),
    ("Core / Common", [
        ("path_contains", "common"),
        ("path_contains", "canonical_entities"),
        ("filename_contains", "models"),
        ("filename_contains", "base"),
    ]),
]

_UNCATEGORISED = "Uncategorised"


def _classify_path(path: str) -> str:
    norm = path.replace("\\", "/").lower()
    filename = Path(path).name.lower()
    for layer_name, rules in _LAYER_RULES:
        for rule_type, value in rules:
            if rule_type == "path_contains" and value.lower() in norm:
                return layer_name
            if rule_type == "filename_contains" and value.lower() in filename:
                return layer_name
    return _UNCATEGORISED


# ---------------------------------------------------------------------------
# ArchitectureGraphBuilder
# ---------------------------------------------------------------------------

class ArchitectureGraphBuilder:
    """
    Builds an ArchitectureGraph by:

    1. Classifying every Python file into a named architectural layer.
    2. Using the import graph to build directed layer-to-layer dependency edges.
    3. Computing coupling metrics.
    4. Identifying risks and extension points.
    """

    # Minimum import-edge count to classify a module as a hotspot
    _HOTSPOT_THRESHOLD = 5

    def build(
        self,
        file_analyses: Dict[str, FileAnalysis],
        import_graph: ImportGraphResult,
        root: Path,
    ) -> ArchitectureGraphResult:
        # Step 1: classify each file into a layer
        layer_modules: Dict[str, List[str]] = defaultdict(list)
        for path, analysis in sorted(file_analyses.items()):
            if analysis.language != "python":
                continue
            layer = _classify_path(path)
            layer_modules[layer].append(path)

        # Step 2: build module → layer mapping
        module_to_layer: Dict[str, str] = {}
        for layer, modules in layer_modules.items():
            for m in modules:
                module_to_layer[m] = layer

        # Step 3: build layer-to-layer edges
        layer_edge_counts: Dict[Tuple[str, str], int] = defaultdict(int)
        for edge in import_graph.edges:
            if edge.resolved:
                src_layer = module_to_layer.get(edge.source, _UNCATEGORISED)
                tgt_layer = module_to_layer.get(edge.resolved, _UNCATEGORISED)
                if src_layer != tgt_layer:
                    layer_edge_counts[(src_layer, tgt_layer)] += 1

        # Compute in-degree / out-degree per layer for ArchitectureNode
        layer_in_degree: Dict[str, int] = defaultdict(int)
        layer_out_degree: Dict[str, int] = defaultdict(int)
        for (src, tgt), cnt in layer_edge_counts.items():
            layer_out_degree[src] += cnt
            layer_in_degree[tgt] += cnt

        all_layers = sorted(set(layer_modules.keys()))
        nodes: List[ArchitectureNode] = []
        for layer in all_layers:
            modules = sorted(layer_modules[layer])
            node = ArchitectureNode(
                id=layer.lower().replace(" ", "_").replace("/", "_"),
                name=layer,
                layer=layer,
                modules=modules,
                in_degree=layer_in_degree.get(layer, 0),
                out_degree=layer_out_degree.get(layer, 0),
            )
            nodes.append(node)

        # Step 4: build ArchitectureEdges
        max_strength = max(layer_edge_counts.values(), default=1)
        edges: List[ArchitectureEdge] = []
        for (src, tgt), cnt in sorted(layer_edge_counts.items()):
            edges.append(ArchitectureEdge(
                source=src,
                target=tgt,
                relationship="imports",
                strength=min(1.0, cnt / max_strength),
            ))

        # Step 5: hotspot modules (high import in-degree)
        in_degree_map = import_graph.in_degree
        hotspots = sorted(
            [m for m, deg in in_degree_map.items() if deg >= self._HOTSPOT_THRESHOLD],
            key=lambda m: in_degree_map[m],
            reverse=True,
        )[:15]

        # Step 6: high-coupling modules (many imports + many importers)
        module_import_count: Dict[str, int] = defaultdict(int)
        for edge in import_graph.edges:
            module_import_count[edge.source] += 1
        high_coupling = sorted(
            [m for m, cnt in module_import_count.items() if cnt >= self._HOTSPOT_THRESHOLD],
            key=lambda m: module_import_count[m],
            reverse=True,
        )[:15]

        # Step 7: low cohesion layers (very diverse file sets)
        low_cohesion = [
            layer for layer, modules in layer_modules.items()
            if len(modules) > 20 or layer == _UNCATEGORISED
        ]

        # Step 8: extension points from nodes with high in-degree
        extension_points = [
            n.name for n in nodes
            if n.in_degree >= 3
        ][:10]

        # Step 9: architecture risks
        risks = self._identify_risks(
            import_graph=import_graph,
            layer_modules=layer_modules,
            hotspots=hotspots,
            high_coupling=high_coupling,
        )

        return ArchitectureGraphResult(
            nodes=nodes,
            edges=edges,
            hotspots=hotspots,
            risks=risks,
            high_coupling_modules=high_coupling,
            low_cohesion_layers=sorted(low_cohesion),
            extension_points=extension_points,
        )

    # ------------------------------------------------------------------
    # Risk identification
    # ------------------------------------------------------------------

    def _identify_risks(
        self,
        import_graph: ImportGraphResult,
        layer_modules: Dict[str, List[str]],
        hotspots: List[str],
        high_coupling: List[str],
    ) -> List[ArchitectureRisk]:
        risks: List[ArchitectureRisk] = []
        rid = 0

        def next_id():
            nonlocal rid
            rid += 1
            return "ARCH-RISK-%03d" % rid

        # Circular dependencies
        for cycle in import_graph.circular_dependencies[:5]:
            risks.append(ArchitectureRisk(
                id=next_id(),
                title="Circular dependency detected",
                description="Modules %s form a circular import chain." % " → ".join(cycle + [cycle[0]]),
                severity="high",
                affected_modules=cycle,
                evidence=["Import cycle: %s" % " → ".join(cycle + [cycle[0]])],
                confidence=0.95,
            ))

        # Hotspot / god module risks
        for m in hotspots[:3]:
            risks.append(ArchitectureRisk(
                id=next_id(),
                title="Architectural hotspot",
                description="%s is imported by many modules, creating a high-coupling hub." % m,
                severity="medium",
                affected_modules=[m],
                evidence=["in-degree: %d" % import_graph.in_degree.get(m, 0)],
                confidence=0.85,
            ))

        # Large uncategorised layer
        uncategorised = layer_modules.get(_UNCATEGORISED, [])
        if len(uncategorised) > 5:
            risks.append(ArchitectureRisk(
                id=next_id(),
                title="Unclassified modules",
                description="%d modules could not be assigned to a known architectural layer." % len(uncategorised),
                severity="low",
                affected_modules=sorted(uncategorised)[:10],
                evidence=["Layer classification: Uncategorised"],
                confidence=0.70,
            ))

        # High coupling
        if len(high_coupling) > 5:
            risks.append(ArchitectureRisk(
                id=next_id(),
                title="High coupling detected",
                description="%d modules have an excessive number of outbound imports." % len(high_coupling),
                severity="medium",
                affected_modules=sorted(high_coupling)[:10],
                evidence=["Outbound import count exceeds threshold"],
                confidence=0.80,
            ))

        return risks

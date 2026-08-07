"""
Knowledge Materialization Engine

Transforms canonical documents (CSS, CDM, CSL standards) into executable
knowledge: Knowledge Objects, Knowledge Relationships, Knowledge Graph,
Canonical Entity Graph, Dependency Graph, Reasoning Graph, Traceability Graph.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

from python.canonical_entities import (
    CanonicalEdge,
    CanonicalNode,
    EdgeType,
    NodeType,
)
from python.knowledge_graph.graph import CanonicalKnowledgeGraph


@dataclass
class KnowledgeObject:
    """A materialized knowledge unit derived from a canonical document or section."""

    id: str
    kind: str           # document | section | standard | dependency
    name: str
    source: str
    version: str
    status: str
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "kind": self.kind,
            "name": self.name,
            "source": self.source,
            "version": self.version,
            "status": self.status,
            "metadata": self.metadata,
        }


@dataclass
class KnowledgeRelationship:
    """A materialized relationship between two knowledge objects."""

    source_id: str
    target_id: str
    relation: str
    confidence: float = 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source_id": self.source_id,
            "target_id": self.target_id,
            "relation": self.relation,
            "confidence": self.confidence,
        }


@dataclass
class MaterializedKnowledge:
    """
    The full materialized knowledge state produced by the engine.

    Includes:
      - knowledge_objects: flat list of all entities
      - knowledge_relationships: flat list of all edges
      - knowledge_graph: navigable canonical graph
      - dependency_graph: adjacency dict {id: [deps]}
      - traceability_graph: adjacency dict {id: [traces]}
    """

    knowledge_objects: List[KnowledgeObject] = field(default_factory=list)
    knowledge_relationships: List[KnowledgeRelationship] = field(default_factory=list)
    knowledge_graph: Optional[CanonicalKnowledgeGraph] = None
    dependency_graph: Dict[str, List[str]] = field(default_factory=dict)
    traceability_graph: Dict[str, List[str]] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        graph_dict = self.knowledge_graph.to_dict() if self.knowledge_graph else {}
        return {
            "knowledge_objects": [o.to_dict() for o in self.knowledge_objects],
            "knowledge_relationships": [r.to_dict() for r in self.knowledge_relationships],
            "knowledge_graph": graph_dict,
            "dependency_graph": self.dependency_graph,
            "traceability_graph": self.traceability_graph,
            "statistics": {
                "objects": len(self.knowledge_objects),
                "relationships": len(self.knowledge_relationships),
                "graph_nodes": self.knowledge_graph.node_count() if self.knowledge_graph else 0,
                "graph_edges": self.knowledge_graph.edge_count() if self.knowledge_graph else 0,
            },
        }

    def export(self, path: str) -> None:
        """Persist materialized knowledge to a JSON file."""
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(self.to_dict(), fh, indent=2)


class KnowledgeMaterializationEngine:
    """
    Materializes canonical documents into executable knowledge.

    Accepts output from CDM Engine and CSS Engine.
    Produces a unified MaterializedKnowledge object containing the
    full Knowledge Graph, Dependency Graph, and Traceability Graph.
    """

    def materialize(self, cdm_docs: list, css_standards: list = None) -> MaterializedKnowledge:
        """
        Materialize knowledge from CDM documents and optional CSS standards.

        Parameters
        ----------
        cdm_docs : list[CdmDocumentObject]
            Documents materialized by the CDM Engine.
        css_standards : list[CSSStandardRecord], optional
            Standards loaded by the CSS Engine.
        """
        if css_standards is None:
            css_standards = []

        objects: List[KnowledgeObject] = []
        relationships: List[KnowledgeRelationship] = []
        graph = CanonicalKnowledgeGraph()
        dep_graph: Dict[str, List[str]] = {}
        trace_graph: Dict[str, List[str]] = {}

        # Materialize CDM documents
        known_ids = set()
        for doc in cdm_docs:
            obj = KnowledgeObject(
                id=doc.identifier,
                kind="document",
                name=doc.title or doc.identifier,
                source=doc.path,
                version=doc.version,
                status=doc.status,
                metadata={
                    "classification": doc.classification,
                    "owner": doc.owner,
                    "standard_family": doc.standard_family,
                    "section_count": len(doc.sections),
                    "dependency_count": len(doc.dependencies),
                    "traceability_count": len(doc.traceability),
                },
            )
            objects.append(obj)
            known_ids.add(doc.identifier)

            graph.add_node(CanonicalNode(
                id=doc.identifier,
                node_type=NodeType.DOCUMENT,
                name=doc.title or doc.identifier,
                source_document=doc.path,
                version=doc.version,
                metadata={"status": doc.status},
                provenance=doc.path,
            ))

            # Sections as sub-nodes
            for i, section in enumerate(doc.sections):
                section_id = f"{doc.identifier}::S{i}"
                graph.add_node(CanonicalNode(
                    id=section_id,
                    node_type=NodeType.SECTION,
                    name=section.title,
                    source_document=doc.path,
                    version=doc.version,
                    metadata={"level": section.level},
                    provenance=doc.identifier,
                ))
                graph.add_edge(CanonicalEdge(
                    source_id=doc.identifier,
                    target_id=section_id,
                    edge_type=EdgeType.CONTAINS,
                    confidence=1.0,
                    metadata={},
                ))

            dep_graph[doc.identifier] = list(doc.dependencies)

            # Traceability graph
            trace_targets = [t.target for t in doc.traceability]
            trace_graph[doc.identifier] = trace_targets

        # Materialize CSS standards
        for std in css_standards:
            std_id = std.identifier
            if std_id in known_ids:
                continue
            obj = KnowledgeObject(
                id=std_id,
                kind="standard",
                name=std.title or std_id,
                source=std.path,
                version=std.version,
                status=std.status,
                metadata={
                    "standard_family": std.standard_family,
                    "classification": std.classification,
                    "owner": std.owner,
                },
            )
            objects.append(obj)
            known_ids.add(std_id)

            graph.add_node(CanonicalNode(
                id=std_id,
                node_type=NodeType.DOCUMENT,
                name=std.title or std_id,
                source_document=std.path,
                version=std.version,
                metadata={"status": std.status},
                provenance=std.path,
            ))
            dep_graph[std_id] = list(std.dependencies)

        # Build dependency edges in the graph
        for source_id, deps in dep_graph.items():
            for dep_id in deps:
                if graph.get_node(dep_id) is None:
                    graph.add_node(CanonicalNode(
                        id=dep_id,
                        node_type=NodeType.DOCUMENT,
                        name=dep_id,
                        source_document="",
                        version="",
                        metadata={"placeholder": True},
                        provenance=source_id,
                    ))
                graph.add_edge(CanonicalEdge(
                    source_id=source_id,
                    target_id=dep_id,
                    edge_type=EdgeType.DEPENDS_ON,
                    confidence=1.0,
                    metadata={},
                ))
                relationships.append(KnowledgeRelationship(
                    source_id=source_id,
                    target_id=dep_id,
                    relation="DEPENDS_ON",
                ))

        # Build traceability edges
        for source_id, traces in trace_graph.items():
            for target_id in traces:
                if graph.get_node(target_id) is None:
                    graph.add_node(CanonicalNode(
                        id=target_id,
                        node_type=NodeType.DOCUMENT,
                        name=target_id,
                        source_document="",
                        version="",
                        metadata={"placeholder": True},
                        provenance=source_id,
                    ))
                graph.add_edge(CanonicalEdge(
                    source_id=source_id,
                    target_id=target_id,
                    edge_type=EdgeType.REFERENCES,
                    confidence=1.0,
                    metadata={"relation": "TRACES"},
                ))
                relationships.append(KnowledgeRelationship(
                    source_id=source_id,
                    target_id=target_id,
                    relation="TRACES",
                ))

        return MaterializedKnowledge(
            knowledge_objects=objects,
            knowledge_relationships=relationships,
            knowledge_graph=graph,
            dependency_graph=dep_graph,
            traceability_graph=trace_graph,
        )

    def materialize_from_standards_root(self, standards_root: str) -> MaterializedKnowledge:
        """
        Convenience method: load all standards from a directory tree and materialize.

        Automatically uses CDM Engine and CSS Engine to load documents.
        """
        from python.cdm_engine import CdmEngine
        from python.css_engine import CSSEngine

        cdm = CdmEngine()
        css = CSSEngine()

        root = Path(standards_root)
        cdm_docs = []
        css_records = []

        for md in sorted(root.rglob("*.md")):
            try:
                cdm_docs.append(cdm.load(str(md)))
            except Exception:
                pass
            try:
                css_records.append(css.load(str(md)))
            except Exception:
                pass

        return self.materialize(cdm_docs, css_records)

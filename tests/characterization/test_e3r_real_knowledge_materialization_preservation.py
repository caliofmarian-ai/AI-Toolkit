from pathlib import Path

from python.cdm_engine import CdmEngine
from python.css_engine import CSSEngine
from python.knowledge_materialization import KnowledgeMaterializationEngine


def _write(path: Path, text: str) -> str:
    path.write_text(text, encoding="utf-8")
    return str(path)


def _node(graph, node_id):
    node = graph.get_node(node_id)
    assert node is not None, node_id
    return node


def test_e3r_real_knowledge_materialization_preservation(tmp_path):
    cdm_source = """# E3R Controlled CDM Title

Version: 9.8.7
Status: Active
Classification: E3R-CDM-CLASSIFICATION-ALPHA
Identifier: E3RCDM-900
Owner: E3R-CDM-OWNER-BETA
Standard Family: E3R-CDM-FAMILY-GAMMA
Custom Semantic Marker: E3R-CDM-CUSTOM-METADATA-DELTA

## E3R Section One
E3R section content value OMEGA.
DEPENDS-ON: EDEP-901
TRACE: ETRACE-902

## E3R Section Two
Second controlled section.
"""

    css_source = """# E3R Controlled CSS Title

Version: 7.6.5
Status: Normative
Classification: E3R-CSS-CLASSIFICATION-ALPHA
Standard Family: E3R-CSS-FAMILY-GAMMA
Identifier: E3RCSS-910
Owner: E3R-CSS-OWNER-BETA

## Purpose
The standard must preserve its legitimate semantic contract.

## Scope
Controlled E3-R CSS scope.

## Objectives
Reference CDM-999 and CSS-998.
"""

    cdm_path = _write(tmp_path / "E3RCDM-900.md", cdm_source)
    css_path = _write(tmp_path / "E3RCSS-910.md", css_source)

    cdm_engine = CdmEngine()
    css_engine = CSSEngine()

    doc = cdm_engine.load(cdm_path)
    std = css_engine.load(css_path)

    assert doc.identifier == "E3RCDM-900"
    assert doc.title == "E3R Controlled CDM Title"
    assert doc.version == "9.8.7"
    assert doc.status == "Active"
    assert doc.classification == "E3R-CDM-CLASSIFICATION-ALPHA"
    assert doc.owner == "E3R-CDM-OWNER-BETA"
    assert doc.standard_family == "E3R-CDM-FAMILY-GAMMA"
    assert doc.metadata["Custom Semantic Marker"] == "E3R-CDM-CUSTOM-METADATA-DELTA"
    assert doc.provenance == cdm_path

    assert [section.title for section in doc.sections] == [
        "E3R Section One",
        "E3R Section Two",
    ]

    assert "EDEP-901" in doc.dependencies
    assert "ETRACE-902" in doc.dependencies

    traceability = {
        (link.relation, link.target)
        for link in doc.traceability
    }

    assert ("DEPENDS-ON", "EDEP-901") in traceability
    assert ("TRACE", "ETRACE-902") in traceability

    assert std.identifier == "E3RCSS-910"
    assert std.title == "E3R Controlled CSS Title"
    assert std.version == "7.6.5"
    assert std.status == "Normative"
    assert std.classification == "E3R-CSS-CLASSIFICATION-ALPHA"
    assert std.owner == "E3R-CSS-OWNER-BETA"
    assert std.standard_family == "E3R-CSS-FAMILY-GAMMA"
    assert std.sections == ["Purpose", "Scope", "Objectives"]
    assert "CDM-999" in std.dependencies
    assert "CSS-998" in std.dependencies

    materialized = KnowledgeMaterializationEngine().materialize(
        [doc],
        [std],
    )

    objects = {
        obj.id: obj
        for obj in materialized.knowledge_objects
    }

    assert "E3RCDM-900" in objects
    assert "E3RCSS-910" in objects

    cdm_obj = objects["E3RCDM-900"]
    css_obj = objects["E3RCSS-910"]

    assert cdm_obj.kind == "document"
    assert cdm_obj.name == "E3R Controlled CDM Title"
    assert cdm_obj.source == cdm_path
    assert cdm_obj.version == "9.8.7"
    assert cdm_obj.status == "Active"
    assert cdm_obj.metadata["classification"] == "E3R-CDM-CLASSIFICATION-ALPHA"
    assert cdm_obj.metadata["owner"] == "E3R-CDM-OWNER-BETA"
    assert cdm_obj.metadata["standard_family"] == "E3R-CDM-FAMILY-GAMMA"
    assert cdm_obj.metadata["section_count"] == 2

    assert css_obj.kind == "standard"
    assert css_obj.name == "E3R Controlled CSS Title"
    assert css_obj.source == css_path
    assert css_obj.version == "7.6.5"
    assert css_obj.status == "Normative"
    assert css_obj.metadata["classification"] == "E3R-CSS-CLASSIFICATION-ALPHA"
    assert css_obj.metadata["owner"] == "E3R-CSS-OWNER-BETA"
    assert css_obj.metadata["standard_family"] == "E3R-CSS-FAMILY-GAMMA"

    graph = materialized.knowledge_graph

    cdm_node = _node(graph, "E3RCDM-900")
    css_node = _node(graph, "E3RCSS-910")

    assert cdm_node.name == "E3R Controlled CDM Title"
    assert cdm_node.source_document == cdm_path
    assert cdm_node.version == "9.8.7"
    assert cdm_node.metadata["status"] == "Active"
    assert cdm_node.provenance == cdm_path

    assert css_node.name == "E3R Controlled CSS Title"
    assert css_node.source_document == css_path
    assert css_node.version == "7.6.5"
    assert css_node.metadata["status"] == "Normative"
    assert css_node.provenance == css_path

    section_0 = _node(graph, "E3RCDM-900::S0")
    section_1 = _node(graph, "E3RCDM-900::S1")

    assert section_0.name == "E3R Section One"
    assert section_1.name == "E3R Section Two"
    assert section_0.source_document == cdm_path
    assert section_0.version == "9.8.7"
    assert section_0.provenance == "E3RCDM-900"

    contains_targets = {
        edge.target_id
        for edge in graph.get_edges_from("E3RCDM-900")
        if edge.edge_type.value == "CONTAINS"
    }

    assert "E3RCDM-900::S0" in contains_targets
    assert "E3RCDM-900::S1" in contains_targets

    assert "EDEP-901" in materialized.dependency_graph["E3RCDM-900"]
    assert "CDM-999" in materialized.dependency_graph["E3RCSS-910"]
    assert "CSS-998" in materialized.dependency_graph["E3RCSS-910"]

    assert "EDEP-901" in materialized.traceability_graph["E3RCDM-900"]
    assert "ETRACE-902" in materialized.traceability_graph["E3RCDM-900"]

    relationships = {
        (rel.source_id, rel.target_id, rel.relation)
        for rel in materialized.knowledge_relationships
    }

    assert ("E3RCDM-900", "EDEP-901", "DEPENDS_ON") in relationships
    assert ("E3RCDM-900", "ETRACE-902", "DEPENDS_ON") in relationships
    assert ("E3RCDM-900", "EDEP-901", "TRACES") in relationships
    assert ("E3RCDM-900", "ETRACE-902", "TRACES") in relationships
    assert ("E3RCSS-910", "CDM-999", "DEPENDS_ON") in relationships
    assert ("E3RCSS-910", "CSS-998", "DEPENDS_ON") in relationships

    dep_edges = [
        edge
        for edge in graph.get_edges_from("E3RCDM-900")
        if edge.target_id == "EDEP-901"
        and edge.edge_type.value == "DEPENDS_ON"
    ]

    assert dep_edges

    trace_edges = [
        edge
        for edge in graph.get_edges_from("E3RCDM-900")
        if edge.target_id == "ETRACE-902"
        and edge.edge_type.value == "REFERENCES"
    ]

    assert trace_edges
    assert trace_edges[0].metadata["relation"] == "TRACES"

    unresolved_dep = _node(graph, "EDEP-901")
    unresolved_trace = _node(graph, "ETRACE-902")
    unresolved_css = _node(graph, "CDM-999")

    for placeholder in (
        unresolved_dep,
        unresolved_trace,
        unresolved_css,
    ):
        assert placeholder.metadata["placeholder"] is True
        assert placeholder.source_document == ""
        assert placeholder.version == ""

    assert unresolved_dep.provenance == "E3RCDM-900"
    assert unresolved_trace.provenance == "E3RCDM-900"
    assert unresolved_css.provenance == "E3RCSS-910"

    serialized = materialized.to_dict()

    serialized_objects = {
        obj["id"]: obj
        for obj in serialized["knowledge_objects"]
    }

    assert serialized_objects["E3RCDM-900"]["source"] == cdm_path
    assert serialized_objects["E3RCDM-900"]["version"] == "9.8.7"
    assert serialized_objects["E3RCDM-900"]["status"] == "Active"
    assert (
        serialized_objects["E3RCDM-900"]["metadata"]["owner"]
        == "E3R-CDM-OWNER-BETA"
    )

    serialized_nodes = {
        node["id"]: node
        for node in serialized["knowledge_graph"]["nodes"]
    }

    assert serialized_nodes["E3RCDM-900"]["provenance"] == cdm_path
    assert serialized_nodes["EDEP-901"]["metadata"]["placeholder"] is True

    assert "Custom Semantic Marker" not in cdm_obj.metadata
    assert "provenance" not in cdm_obj.metadata
    assert "content" not in section_0.metadata

    css_section_nodes = [
        node
        for node in graph._nodes.values()
        if node.provenance == "E3RCSS-910"
        and node.node_type.value == "SECTION"
    ]

    assert css_section_nodes == []

    relationship_type = type(
        materialized.knowledge_relationships[0]
    )

    controlled_relationship = relationship_type(
        source_id="E3R-REL-SOURCE",
        target_id="E3R-REL-TARGET",
        relation="E3R-RELATION",
        confidence=0.4321,
        metadata={
            "semantic_marker":
            "E3R-REL-METADATA-CONTROLLED"
        },
    )

    assert (
        controlled_relationship.metadata["semantic_marker"]
        == "E3R-REL-METADATA-CONTROLLED"
    )

    controlled_dict = controlled_relationship.to_dict()

    assert controlled_dict["confidence"] == 0.4321
    assert "metadata" not in controlled_dict

    serialized_trace_edges = [
        edge
        for edge in serialized["knowledge_graph"]["edges"]
        if edge["source_id"] == "E3RCDM-900"
        and edge["target_id"] == "ETRACE-902"
        and edge["edge_type"] == "REFERENCES"
    ]

    assert serialized_trace_edges
    assert (
        serialized_trace_edges[0]["metadata"]["relation"]
        == "TRACES"
    )

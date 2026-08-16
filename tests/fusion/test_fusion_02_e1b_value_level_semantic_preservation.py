"""
FUSION-02 RUN-03 / E1B.

Value-level characterization of the real semantic path.

No production repair is authorized here.
"""

from __future__ import annotations

import inspect

from python.csl_engine import CslEngine
from python.canonical_entities import UemBuilder
from python.knowledge_materialization import KnowledgeMaterializationEngine


CSL = """\
Project:
    Identifier: E1B-PROJECT-ALPHA-731
    Title: "E1B Distinctive Project 731"
    Version: 7.3.1
    Status: Approved
    Classification: "E1B-EPISTEMIC-CLASS-731"
    Authority: "E1B-HUMAN-AUTHORITY-731"
    Provenance: "E1B-PROVENANCE-731"
    LifecycleMarker: "E1B-LIFECYCLE-731"

Capability:
    Identifier: E1B-CAPABILITY-BETA-731
    Name: "E1B Distinctive Capability 731"
    Version: 7.3.2
    Status: Maintained
    Authority: "E1B-AUTHORITY-BETA-731"
    Provenance: "E1B-PROVENANCE-BETA-731"
    EpistemicClass: "E1B-EVIDENCE-731"
    LifecycleMarker: "E1B-LIFECYCLE-BETA-731"

Requirement:
    Identifier: E1B-REQUIREMENT-GAMMA-731
    Name: "E1B Distinctive Requirement 731"
    Version: 7.3.3
    Status: Approved
    Authority: "E1B-AUTHORITY-GAMMA-731"
    Provenance: "E1B-PROVENANCE-GAMMA-731"
    EpistemicClass: "E1B-CANON-731"

Relationship:
    E1B-CAPABILITY-BETA-731 implements E1B-REQUIREMENT-GAMMA-731
    Authority: "E1B-RELATION-AUTHORITY-731"
    Provenance: "E1B-RELATION-PROVENANCE-731"

Relationship:
    E1B-PROJECT-ALPHA-731 contains E1B-CAPABILITY-BETA-731
"""


def execution():
    result = CslEngine().execute(
        CSL,
        source_name="E1B_CONTROLLED_TRACE.csl",
    )
    assert result.valid, [
        (d.code, d.message)
        for d in result.diagnostics
    ]
    assert result.ast is not None
    assert result.semantic is not None
    return result


def entity_by_id(semantic, identifier):
    return next(
        e for e in semantic.entities
        if e["identifier"] == identifier
    )


def relation(semantic, source, relation_type, target):
    return next(
        r for r in semantic.relationships
        if r["source"] == source
        and r["relation_type"] == relation_type
        and r["target"] == target
    )


def test_real_csl_ast_semantic_pipeline_executes():
    result = execution()

    assert (
        result.ast.header_value("Identifier")
        == "E1B-PROJECT-ALPHA-731"
    )
    assert (
        result.ast.header_value("Classification")
        == "E1B-EPISTEMIC-CLASS-731"
    )


def test_identity_values_survive_ast_to_semantic():
    result = execution()
    semantic = result.semantic

    assert semantic.doc_id == "E1B-PROJECT-ALPHA-731"

    ids = {
        entity["identifier"]
        for entity in semantic.entities
    }

    assert "E1B-PROJECT-ALPHA-731" in ids
    assert "E1B-CAPABILITY-BETA-731" in ids
    assert "E1B-REQUIREMENT-GAMMA-731" in ids


def test_authority_provenance_epistemic_and_lifecycle_values_survive_semantic():
    result = execution()
    semantic = result.semantic

    project = entity_by_id(
        semantic,
        "E1B-PROJECT-ALPHA-731",
    )
    capability = entity_by_id(
        semantic,
        "E1B-CAPABILITY-BETA-731",
    )
    requirement = entity_by_id(
        semantic,
        "E1B-REQUIREMENT-GAMMA-731",
    )

    assert (
        project["properties"]["Authority"]
        == "E1B-HUMAN-AUTHORITY-731"
    )
    assert (
        project["properties"]["Provenance"]
        == "E1B-PROVENANCE-731"
    )
    assert (
        project["properties"]["LifecycleMarker"]
        == "E1B-LIFECYCLE-731"
    )
    assert (
        semantic.classification
        == "E1B-EPISTEMIC-CLASS-731"
    )

    assert (
        capability["properties"]["Authority"]
        == "E1B-AUTHORITY-BETA-731"
    )
    assert (
        capability["properties"]["Provenance"]
        == "E1B-PROVENANCE-BETA-731"
    )
    assert (
        capability["properties"]["EpistemicClass"]
        == "E1B-EVIDENCE-731"
    )
    assert (
        capability["properties"]["LifecycleMarker"]
        == "E1B-LIFECYCLE-BETA-731"
    )
    assert capability["version"] == "7.3.2"
    assert capability["status"] == "Maintained"

    assert (
        requirement["properties"]["Authority"]
        == "E1B-AUTHORITY-GAMMA-731"
    )
    assert (
        requirement["properties"]["Provenance"]
        == "E1B-PROVENANCE-GAMMA-731"
    )
    assert (
        requirement["properties"]["EpistemicClass"]
        == "E1B-CANON-731"
    )


def test_relationship_values_survive_semantic_boundary():
    semantic = execution().semantic

    rel = relation(
        semantic,
        "E1B-CAPABILITY-BETA-731",
        "implements",
        "E1B-REQUIREMENT-GAMMA-731",
    )

    assert (
        rel["attributes"]["Authority"]
        == "E1B-RELATION-AUTHORITY-731"
    )
    assert (
        rel["attributes"]["Provenance"]
        == "E1B-RELATION-PROVENANCE-731"
    )


def test_values_survive_real_uem_builder():
    semantic = execution().semantic
    uem = UemBuilder().build([semantic])

    capability = uem.get_object(
        "E1B-CAPABILITY-BETA-731"
    )
    requirement = uem.get_object(
        "E1B-REQUIREMENT-GAMMA-731"
    )

    assert capability is not None
    assert requirement is not None

    assert capability.version == "7.3.2"
    assert capability.status == "Maintained"

    assert (
        capability.properties["Authority"]
        == "E1B-AUTHORITY-BETA-731"
    )
    assert (
        capability.properties["Provenance"]
        == "E1B-PROVENANCE-BETA-731"
    )
    assert (
        capability.properties["EpistemicClass"]
        == "E1B-EVIDENCE-731"
    )
    assert (
        capability.properties["LifecycleMarker"]
        == "E1B-LIFECYCLE-BETA-731"
    )

    assert (
        requirement.properties["Authority"]
        == "E1B-AUTHORITY-GAMMA-731"
    )
    assert (
        requirement.properties["Provenance"]
        == "E1B-PROVENANCE-GAMMA-731"
    )
    assert (
        requirement.properties["EpistemicClass"]
        == "E1B-CANON-731"
    )


def test_relationship_survives_real_uem_builder():
    semantic = execution().semantic
    uem = UemBuilder().build([semantic])

    matches = [
        rel
        for rel in uem.all_relationships()
        if rel.source_id
        == "E1B-CAPABILITY-BETA-731"
        and rel.target_id
        == "E1B-REQUIREMENT-GAMMA-731"
        and rel.relation_type.value == "IMPLEMENTS"
    ]

    assert len(matches) == 1

    rel = matches[0]

    assert (
        rel.metadata["Authority"]
        == "E1B-RELATION-AUTHORITY-731"
    )
    assert (
        rel.metadata["Provenance"]
        == "E1B-RELATION-PROVENANCE-731"
    )


def test_materialization_boundary_has_no_uem_ingestion_contract():
    signature = inspect.signature(
        KnowledgeMaterializationEngine.materialize
    )

    parameters = list(signature.parameters)

    assert parameters == [
        "self",
        "cdm_docs",
        "css_standards",
    ]

    assert "uem" not in parameters
    assert "semantic_results" not in parameters


def test_no_test_adapter_is_used_to_bridge_uem_to_materialization():
    source = inspect.getsource(
        KnowledgeMaterializationEngine.materialize
    )

    assert "cdm_docs" in source
    assert "UemBuilder" not in source
    assert "UniversalEngineeringModel" not in source

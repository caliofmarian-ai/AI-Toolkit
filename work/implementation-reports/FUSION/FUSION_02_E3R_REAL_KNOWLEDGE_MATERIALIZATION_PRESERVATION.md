# FUSION-02 — E3-R Real Knowledge Materialization Preservation Characterization

## STARTING AUTHORITY

cabdc271f3c39992706f8f308c01945f9f6e5473

## ACTUAL INPUT PHYSIOLOGY

CDM source → CdmEngine → CdmDocumentObject

CSS source → CSSEngine → CSSStandardRecord

## ACTUAL MATERIALIZATION PHYSIOLOGY

CdmDocumentObject / CSSStandardRecord → KnowledgeMaterializationEngine.materialize() → KnowledgeObject / KnowledgeRelationship → CanonicalKnowledgeGraph → MaterializedKnowledge → dependency_graph / traceability_graph

## IMPORT CONTRACT FINDING

CdmTraceabilityLink exists in python.cdm_engine.engine but is not exported by python.cdm_engine.

E3-R therefore characterizes traceability through the public CdmEngine result contract rather than depending on the internal concrete type.

## CDM SEMANTIC CONTRACT

PRESERVED

## CSS SEMANTIC CONTRACT

PRESERVED

## VALUE-LEVEL PRESERVATION MATRIX

| Semantic family | Result |
| --- | --- |
| CDM core identity/title/version/status/source/classification/owner/family | PRESERVED |
| CSS core identity/title/version/status/source/classification/owner/family | PRESERVED |
| Dependency relationship | TRANSFORMED WITH SEMANTIC PRESERVATION |
| Traceability relationship | TRANSFORMED WITH SEMANTIC PRESERVATION |
| Dependency graph | PRESERVED |
| Traceability graph | PRESERVED |
| Canonical dependency edge | TRANSFORMED WITH SEMANTIC PRESERVATION |
| Canonical traceability edge | TRANSFORMED WITH SEMANTIC PRESERVATION |
| Placeholder semantics | PRESERVED |
| Graph identity/provenance | PRESERVED |
| Sections | TRANSFORMED WITH SEMANTIC PRESERVATION |
| Containment | TRANSFORMED WITH SEMANTIC PRESERVATION |

## KNOWLEDGE OBJECT FINDINGS

Core characterized CDM and CSS document/standard semantics survive into KnowledgeObject.

Arbitrary source metadata is selectively projected rather than copied wholesale.

## KNOWLEDGE RELATIONSHIP FINDINGS

Dependencies become KnowledgeRelationship relation=DEPENDS_ON.

Traceability targets become KnowledgeRelationship relation=TRACES.

KnowledgeRelationship.to_dict() does not serialize the runtime metadata field. This is recorded as an observed serialization characteristic, not automatically promoted to a defect without an authoritative preservation requirement.

## CANONICAL KNOWLEDGE GRAPH FINDINGS

Document and standard identities are represented as canonical nodes.

Sections are transformed into section nodes connected through CONTAINS.

Dependencies are transformed into DEPENDS_ON edges.

Traceability is transformed into REFERENCES edges carrying relation=TRACES metadata.

## DEPENDENCY GRAPH FINDINGS

PRESERVED

## TRACEABILITY GRAPH FINDINGS

PRESERVED

## PROVENANCE FINDINGS

PRESERVED

Unresolved dependency/traceability target placeholders retain source identity as provenance.

## TRANSFORMATIONS

- sections → CanonicalNode SECTION + CONTAINS edge
- dependencies → dependency_graph + KnowledgeRelationship DEPENDS_ON + CanonicalEdge DEPENDS_ON
- traceability → traceability_graph + KnowledgeRelationship TRACES + CanonicalEdge REFERENCES with relation metadata
- unresolved targets → placeholder CanonicalNode

## DROPPED SEMANTICS

Arbitrary CDM metadata is not copied wholesale into KnowledgeObject.metadata.

KnowledgeRelationship.to_dict() omits runtime metadata.

Neither observation is declared a contract-violating semantic loss without separate authoritative evidence that the omitted data must survive those exact boundaries.

## NOT-REPRESENTABLE SEMANTICS

UEM semantics are intentionally outside this characterization boundary according to the conserved RUN-04 verdict.

## REAL DEFECTS

NONE DEMONSTRATED by the characterized production physiology.

## NON-DEFECT TRANSFORMATIONS

Different structural representations preserving the characterized semantic meaning are classified as transformations rather than semantic losses.

## PRIMARY VERDICT

E3-R TRANSFORMATION WITHOUT LOSS

## EXECUTABLE ARCHITECTURE CONSEQUENCE

NO CORRECTION REQUIRED to the RUN-04 architectural boundary on current evidence.

Metadata serialization requirements remain a separate contract question and must not be converted into a repair without authoritative evidence.

## UEM RELATIONSHIP

UNCHANGED — CSL → SemanticResult → UemBuilder → UniversalEngineeringModel and CDM/CSS → KnowledgeMaterializationEngine → MaterializedKnowledge remain distinct demonstrated physiologies.

No convergence was constructed.

## TESTS

Import-path verification: PASS.
Traceability runtime-contract preflight: PASS.
Controlled fixture preflight: PASS.
Focused E3-R characterization: PASS.
Directly relevant regressions: PASS.

## MUTATION BOUNDARY

Production: NO.
CSL: NO.
UEM: NO.
CDM implementation: NO.
CSS implementation: NO.
Knowledge Materialization implementation: NO.
Knowledge Graph implementation: NO.
Canon: NO.

## ERROR MEMORY IMPACT

The recovery confirms the preventive rule that package-level exports must be verified explicitly. Concrete implementation type existence does not prove package-level importability.

Where concrete class identity is unnecessary, characterization should use the demonstrated public runtime contract.

## NEXT AUTHORIZED STAGE

STOP FOR HUMAN/AUDITOR DECISION.

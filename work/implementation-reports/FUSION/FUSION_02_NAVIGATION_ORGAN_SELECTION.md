# FUSION-02 — Navigation Organ Selection

## Starting Authority

8c1fd1bbaa3115262a2a137019ff6652d5ece157

## Characterization Type

EXECUTABLE CHARACTERIZATION ONLY

No production navigation mutation was authorized or performed.

## Conserved Cognitive Physiology

Human Raw Source
→ Information Need
→ Need Evaluation
→ Navigation Plan
→ Initial Journey State

Retrieval remains unimplemented.

Working Context remains unimplemented.

Journey traversal has not started.

## Objective

Determine which existing production organs can legitimately serve the planned read-only NavigationPlan capabilities without inventing convenience APIs.

## Verified Candidate Imports

### python.repository_engine.engine.RepositoryEngine

- import: PASS
- constructor: (root='.', workspace_index=None)
- public methods:
  - discover(self)
  - profile(self)
  - statistics(self)

### python.engineering_engine.semantic_query_engine.SemanticQueryEngine

- import: PASS
- constructor: (repository: 'SemanticRepository')
- public methods:
  - find_by_type(self, entity_type: 'EntityType') -> 'list[SemanticEntity]'
  - find_entity(self, name: 'str') -> 'SemanticEntity | None'
  - outgoing_relationships(self, source: 'str') -> 'list[SemanticRelationship]'

### python.evidence_engine.engine.EvidenceEngine

- import: PASS
- constructor: (repository='.')
- public methods:
  - find(self, keyword)

### python.repository_inspector_v2.engine.RepositoryInspectorV2

- import: PASS
- constructor: (root='.', workspace_index=None)
- public methods:
  - export(self, filename)
  - inspect(self)

### python.semantic_repository_intelligence.relationship_resolver.RelationshipResolver

- import: PASS
- constructor: (root: pathlib.Path, file_analyses: Dict[str, python.semantic_repository_intelligence.models.FileAnalysis])
- public methods:
  - file_to_module(self, file_path: str) -> str
  - resolve_import(self, source_path: str, module: str, level: int = 0) -> Optional[str]
  - resolve_symbol(self, qualified_name: str) -> Optional[str]

### python.epistemic.transformation.TransformationLifecycle

- import: PASS
- constructor: (root: 'Path | None' = None)
- public methods:
  - begin(self, need: 'str', *, parent_transformation: 'str | None' = None, research: 'str' = 'UNKNOWN', hypothesis: 'str' = 'UNKNOWN', owner_decision: 'str' = 'NO OWNER DECISION RECORDED') -> 'Transformation'
  - children(self, identifier: 'str') -> 'tuple[Transformation, ...]'
  - complete(self, transformation: 'Transformation', *, implementation: 'str' = 'UNKNOWN', execution: 'str' = 'NOT EXECUTED', artifacts_effects: 'str' = 'UNKNOWN', evidence: 'str' = 'UNKNOWN', verification: 'str' = 'NOT VERIFIED', knowledge: 'str' = 'UNKNOWN', evolution: 'str' = 'UNKNOWN', next_transformation: 'str' = 'UNKNOWN') -> 'Transformation'
  - get(self, identifier: 'str') -> 'Transformation'
  - inspect(self, identifier: 'str') -> 'dict[str, object]'
  - lineage(self, identifier: 'str') -> 'tuple[Transformation, ...]'
  - list_transformations(self) -> 'tuple[Transformation, ...]'
  - relate(self, transformation: 'Transformation', *, relation: 'str', target_identity: 'str', target_title: 'str', target_reference: 'str') -> 'Transformation'
  - resolve_reference(self, reference: 'EpistemicReference') -> 'Path | None'

### python.epistemic.provenance.Provenance

- import: PASS
- constructor: () -> 'None'
- public methods:
  - add_source(self, title: 'str', *, kind: 'SourceKind', reference: 'str', transformation: 'str | None' = None) -> 'Source'
  - claim_for_verification(self, verification: 'Verification') -> 'Claim'
  - claims_for_evidence(self, evidence: 'Evidence', *, role: 'EvidenceRole | None' = None) -> 'tuple[Claim, ...]'
  - contradicting_evidence(self, claim: 'Claim') -> 'tuple[Evidence, ...]'
  - current_states_for_knowledge(self, knowledge: 'Knowledge') -> 'tuple[CurrentState, ...]'
  - establish_current_state(self, knowledge: 'Knowledge', title: 'str', statement: 'str', *, authority: 'str', temporal_status: 'str' = 'CURRENT') -> 'CurrentState'
  - evidence_for_claim(self, claim: 'Claim', *, role: 'EvidenceRole | None' = None) -> 'tuple[Evidence, ...]'
  - evidence_from_observation(self, observation: 'Observation') -> 'tuple[Evidence, ...]'
  - knowledge_for_current_state(self, current_state: 'CurrentState') -> 'Knowledge'
  - knowledge_for_verification(self, verification: 'Verification') -> 'tuple[Knowledge, ...]'
  - load(root: 'Path') -> "'Provenance'"
  - make_claim(self, title: 'str', statement: 'str', *, transformation: 'str | None' = None) -> 'Claim'
  - observation_for_evidence(self, evidence: 'Evidence') -> 'Observation'
  - observations_from_source(self, source: 'Source') -> 'tuple[Observation, ...]'
  - observe(self, source: 'Source', title: 'str', observed: 'str', *, interpretation: 'str' = 'UNKNOWN') -> 'Observation'
  - preserve_evidence(self, observation: 'Observation', title: 'str', reference: 'str', *, domain: 'EvidenceDomain' = 'OTHER') -> 'Evidence'
  - promote_knowledge(self, verification: 'Verification', title: 'str', statement: 'str', *, authority: 'str') -> 'Knowledge'
  - provenance_from_source(self, source: 'Source') -> 'tuple[Source, tuple[Observation, ...], tuple[Evidence, ...], tuple[Claim, ...], tuple[Verification, ...]]'
  - provenance_from_source_to_current_state(self, source: 'Source') -> 'tuple[Source, tuple[Observation, ...], tuple[Evidence, ...], tuple[Claim, ...], tuple[Verification, ...], tuple[Knowledge, ...], tuple[CurrentState, ...]]'
  - provenance_from_source_to_knowledge(self, source: 'Source') -> 'tuple[Source, tuple[Observation, ...], tuple[Evidence, ...], tuple[Claim, ...], tuple[Verification, ...], tuple[Knowledge, ...]]'
  - provenance_to_source(self, verification: 'Verification') -> 'tuple[Verification, Claim, tuple[Evidence, ...], tuple[Observation, ...], tuple[Source, ...]]'
  - provenance_to_source_from_current_state(self, current_state: 'CurrentState') -> 'tuple[CurrentState, Knowledge, Verification, Claim, tuple[Evidence, ...], tuple[Observation, ...], tuple[Source, ...]]'
  - provenance_to_source_from_knowledge(self, knowledge: 'Knowledge') -> 'tuple[Knowledge, Verification, Claim, tuple[Evidence, ...], tuple[Observation, ...], tuple[Source, ...]]'
  - relate_evidence(self, evidence: 'Evidence', claim: 'Claim', role: 'EvidenceRole') -> 'EvidenceRelation'
  - save(self, root: 'Path') -> 'Path'
  - source_for_observation(self, observation: 'Observation') -> 'Source'
  - supporting_evidence(self, claim: 'Claim') -> 'tuple[Evidence, ...]'
  - verification_for_knowledge(self, knowledge: 'Knowledge') -> 'Verification'
  - verifications_for_claim(self, claim: 'Claim') -> 'tuple[Verification, ...]'
  - verify(self, claim: 'Claim', title: 'str', *, state: 'str' = 'NOT VERIFIED', basis: 'str' = 'UNKNOWN') -> 'Verification'

### python.epistemic.layered_memory.LayeredMemory

- import: PASS
- constructor: () -> 'None'
- public methods:
  - add_chain(self, memories: 'Iterable[SedimentedMemory]') -> 'tuple[LayeredMemoryNode, ...]'
  - add_child(self, parent_id: 'LayeredMemoryNodeId', memory: 'SedimentedMemory', *, node_id: 'LayeredMemoryNodeId | None' = None) -> 'LayeredMemoryNode'
  - add_root(self, memory: 'SedimentedMemory', *, node_id: 'LayeredMemoryNodeId | None' = None) -> 'LayeredMemoryNode'
  - children(self, node_id: 'LayeredMemoryNodeId') -> 'tuple[LayeredMemoryNode, ...]'
  - get(self, node_id: 'LayeredMemoryNodeId') -> 'LayeredMemoryNode'
  - memories_at_depth(self, depth: 'int') -> 'tuple[LayeredMemoryNode, ...]'
  - nodes(self) -> 'tuple[LayeredMemoryNode, ...]'
  - parents(self, node_id: 'LayeredMemoryNodeId') -> 'tuple[LayeredMemoryNode, ...]'
  - provenance_route(self, node_id: 'LayeredMemoryNodeId') -> 'tuple[str, str]'
  - toward_depth(self, node_id: 'LayeredMemoryNodeId') -> 'tuple[LayeredMemoryNode, ...]'
  - toward_surface(self, node_id: 'LayeredMemoryNodeId') -> 'LayeredMemoryPath'

## Safe Runtime Characterization

### python.repository_engine.engine.RepositoryEngine

- instantiated: True
- constructor strategy: {'kwargs': {}}

### python.engineering_engine.semantic_query_engine.SemanticQueryEngine

- instantiated: False
- constructor strategy: NOT INSTANTIATED — REQUIRED DEPENDENCIES: repository

### python.evidence_engine.engine.EvidenceEngine

- instantiated: True
- constructor strategy: {'kwargs': {}}
- candidate method: find(keyword)

### python.repository_inspector_v2.engine.RepositoryInspectorV2

- instantiated: True
- constructor strategy: {'kwargs': {}}
- candidate method: inspect()

## Capability Candidate Matrix

### SEARCH

- python.engineering_engine.semantic_query_engine.SemanticQueryEngine via find_by_type, find_entity
- python.evidence_engine.engine.EvidenceEngine via find

### RESOLVE

- python.semantic_repository_intelligence.relationship_resolver.RelationshipResolver via resolve_import, resolve_symbol
- python.epistemic.transformation.TransformationLifecycle via resolve_reference

### READ

- python.epistemic.transformation.TransformationLifecycle via get
- python.epistemic.provenance.Provenance via load
- python.epistemic.layered_memory.LayeredMemory via get

### INSPECT

- python.repository_inspector_v2.engine.RepositoryInspectorV2 via inspect
- python.epistemic.transformation.TransformationLifecycle via inspect

## Executable Observations

RepositoryEngine instantiated successfully under its demonstrated constructor contract, but no planned navigation method was established by this characterization.

SemanticQueryEngine was not instantiated because its demonstrated constructor requires a repository dependency. No guessed repository adapter was created.

EvidenceEngine instantiated successfully and exposes find(keyword), but that method was not executed because its input/output and provenance contract must be characterized before navigation authorization.

RepositoryInspectorV2 instantiated successfully and exposes inspect(), but that method was not executed because its read-only result contract must first be demonstrated.

## Selection Rule

A lexical match, import success, constructor success, or method-name match does not by itself authorize an organ for cognitive navigation.

The first retrieval mutation may use only an organ whose constructor, input contract, output contract, read-only behavior, semantic role, and provenance behavior have been demonstrated.

## Search

CANDIDATES DISCOVERED; EXECUTION CONTRACT NOT YET AUTHORIZED.

## Resolve

CANDIDATES DISCOVERED; EXECUTION CONTRACT NOT YET AUTHORIZED.

## Read

CANDIDATES DISCOVERED; EXECUTION CONTRACT NOT YET AUTHORIZED.

## Inspect

CANDIDATES DISCOVERED; EXECUTION CONTRACT NOT YET AUTHORIZED.

## Read-Only Requirement

MANDATORY.

No selected navigation operation may mutate repository content, Canon, CSL, UEM, Knowledge Materialization, Knowledge Graph, or Human-authored state.

## Provenance Requirement

MANDATORY FOR RETRIEVED EVIDENCE.

A retrieved item must remain attributable to its real source. An organ that returns useful information without sufficient source identity cannot alone complete the future Working Context physiology.

## Human Authority

PRESERVED.

Navigation and retrieval may expose evidence but may not promote retrieved information into authority merely because it was found.

## Permanent Orientation

PRESERVED.

## Navigation Plan

PRESERVED.

## Retrieval

NOT IMPLEMENTED.

## Working Context

NOT IMPLEMENTED.

## Journey Traversal

NOT STARTED.

## Production Mutation

NONE.

## Characterization Verdict

NO NAVIGATION ORGAN IS YET AUTHORIZED SOLELY BY THIS RUN.

The repository contains real candidate organs, but their exact read-only execution, result, and provenance contracts must be characterized before the first retrieval mutation.

## Next Exact Boundary

Characterize executable read-only behavior of the smallest viable candidate set, beginning with EvidenceEngine.find(keyword) and RepositoryInspectorV2.inspect(), while separately determining the real repository dependency required by SemanticQueryEngine.

Do not implement retrieval during that characterization.

## Next Authorized Stage

DIRECT GITHUB AUDIT OF THIS CONSERVED ORGAN-SELECTION REPORT.

THEN AUTHORIZE THE SMALLEST REAL READ-ONLY NAVIGATION EXECUTION BOUNDARY.

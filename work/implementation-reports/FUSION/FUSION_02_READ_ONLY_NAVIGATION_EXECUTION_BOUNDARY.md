# FUSION-02 — Read-Only Navigation Execution Boundary

## Starting Authority

271948d42423795120b91bda3222e445b368bf10

## Characterization Type

CHARACTERIZATION ONLY

No production mutation was authorized or performed.

## Conserved Cognitive Physiology

Human Raw Source
→ Information Need
→ Need Evaluation
→ Navigation Plan
→ Initial Journey State

Retrieval remains unimplemented.

Working Context remains unimplemented.

## Objective

Identify the real existing repository organs capable of supporting the planned read-only capabilities:

- search
- resolve
- read
- inspect

without inventing convenience APIs or constructing adapters.

## Discovered Python Anatomy

### lib/python/agents/repository_inspector_agent.py

- class: RepositoryInspectorAgent

### lib/python/ai_control_center/panels/repository/panel.py

- class: RepositoryPanel
- relevant methods: git_repository

### lib/python/ai_control_center/providers/local_repository.py

- class: LocalRepositoryProvider

### lib/python/ai_cto_scanner/report.py

- class: AICTOReportGenerator
- relevant methods: _readiness_scores, _semantic_architecture_graph, _semantic_findings, _repository_complexity

### lib/python/ai_cto_scanner/scoring.py

- class: ReadinessScorer
- relevant methods: _compute_development_readiness

### lib/python/ai_platform/context_builder.py

- class: AIContextBuilder
- relevant methods: _read_json

### lib/python/ai_platform/model_manager.py

- class: ModelManager
- relevant methods: resolve_roles

### lib/python/ai_platform/prompt_library.py

- class: PromptLibrary
- relevant methods: resolve

### lib/python/ai_platform/service.py

- class: AIPlatformService
- relevant methods: ask_repository

### lib/python/ai_platform/sessions.py

- class: AISessionEngine
- relevant methods: _read

### lib/python/autonomous_execution_engine/persistence.py

- class: ExecutionPersistence
- relevant methods: _read

### lib/python/autonomous_execution_engine/policy.py

- class: ExecutionApproval
- relevant methods: resolve

### lib/python/autonomous_execution_engine/validator.py

- class: ExecutionValidator
- relevant methods: validate_repository

### lib/python/autonomous_planning_engine/batch_planner.py

- class: BatchPlanner
- relevant methods: _find_in_development_batches

### lib/python/autonomous_planning_engine/decision_engine.py

- class: PlanningDecisionEngine
- relevant methods: _repository_health

### lib/python/autonomous_planning_engine/dependency_resolver.py

- class: DependencyGraph
- class: DependencyResolver
- relevant methods: build_core_graph, build_batch_graph, resolve_entries

### lib/python/autonomous_planning_engine/persistence.py

- class: PlanningPersistence
- relevant methods: _read

### lib/python/batch_planner/planner.py

- class: BatchPlanner
- relevant methods: _resolve_dependencies

### lib/python/canonical_entities/models.py

- class: DriftFinding

### lib/python/canonical_parser/lexer.py

- class: CslLexer
- relevant methods: _read_string, _read_word

### lib/python/canonical_repository/repository.py

- class: CanonicalRepository
- relevant methods: dependency_graph

### lib/python/cdm_engine/engine.py

- class: CdmTraceabilityLink

### lib/python/context_synchronization_engine/engine.py

- class: ContextResolver
- relevant methods: resolve, _resolve_next_core
- class: ContextValidator
- relevant methods: _field_finding

### lib/python/context_synchronization_engine/models.py

- class: SynchronizationFinding

### lib/python/dashboard/service.py

- class: EngineeringDashboardService
- relevant methods: render_repository, _load_repository_profile, ask_repository, _resolve_related_paths, _repository_usage, _read_json, _inspection_panel, _repository_table

### lib/python/development_state_engine/models.py

- class: RepositoryState

### lib/python/development_state_engine/repository.py

- class: DevelopmentStateRepository
- relevant methods: _read_json, _safe_read_integrity, _resolve_snapshot_path

### lib/python/development_state_engine/runtime.py

- class: DevelopmentStateEventBus
- relevant methods: _read_json
- class: DevelopmentStateManager
- relevant methods: _normalize_repository_state, _repository_intelligence, _semantic_repository_intelligence, _executable_repository_intelligence

### lib/python/drift_engine/engine.py

- class: DriftEngine
- relevant methods: _finding, _orphan_implementation_findings

### lib/python/engineering_engine/dependency_graph.py

- class: DependencyGraph
- class: DependencyGraphBuilder

### lib/python/engineering_engine/github_repository_resolver.py

- class: GitHubRepository
- class: GitHubRepositoryResolver
- relevant methods: resolve

### lib/python/engineering_engine/import_resolver.py

- class: ImportResolver
- relevant methods: resolve

### lib/python/engineering_engine/knowledge_graph.py

- class: KnowledgeGraph
- class: KnowledgeGraphBuilder

### lib/python/engineering_engine/repository_audit.py

- class: RepositoryAudit

### lib/python/engineering_engine/repository_model.py

- class: RepositoryKnowledge
- class: RepositoryKnowledgeBuilder

### lib/python/engineering_engine/repository_scanner.py

- class: RepositoryModel
- class: RepositoryScanner

### lib/python/engineering_engine/semantic_entities.py

- class: SemanticRepository

### lib/python/engineering_engine/semantic_query_engine.py

- class: SemanticQueryEngine
- relevant methods: find_by_type, find_entity

### lib/python/engineering_engine/semantic_repository_builder.py

- class: SemanticRepositoryBuilder

### lib/python/engineering_workspace/workspace.py

- class: EngineeringWorkspace
- relevant methods: repository, knowledge

### lib/python/epistemic/layered_memory.py

- class: LayeredMemoryNode
- relevant methods: provenance_identifier
- class: LayeredMemory
- relevant methods: provenance_route
- class: LayeredMemoryRepository
- class: LayeredMemoryTraversal
- relevant methods: provenance_route

### lib/python/epistemic/provenance.py

- class: ProvenanceError
- class: Knowledge
- class: KnowledgePromotionError
- class: Provenance
- relevant methods: promote_knowledge, knowledge_for_verification, verification_for_knowledge, provenance_to_source_from_knowledge, current_states_for_knowledge, knowledge_for_current_state, provenance_to_source_from_current_state, provenance_from_source_to_current_state, provenance_to_source, provenance_from_source, provenance_from_source_to_knowledge, _require_registered_knowledge
- function: _knowledge_identifier
- function: _require_knowledge_text
- function: promote_verified_knowledge

### lib/python/epistemic/sedimentation.py

- class: Sedimentation
- relevant methods: human_readable_identity
- class: SedimentationRepository
- relevant methods: by_provenance

### lib/python/epistemic/sedimented_memory.py

- class: DownstreamKnowledgeError
- class: SedimentedMemoryPhysiology
- relevant methods: _provenance_identifier, _to_knowledge

### lib/python/epistemic/transformation.py

- class: TransformationLifecycle
- relevant methods: resolve_reference, inspect

### lib/python/evidence_engine/engine.py

- class: EvidenceEngine
- relevant methods: find

### lib/python/executable_repository_intelligence/engine.py

- class: ExecutableRepositoryEngine

### lib/python/executable_repository_intelligence/executable_dep_graph.py

- class: ExecutableDependencyGraphBuilder

### lib/python/executable_repository_intelligence/models.py

- class: RepositoryRuntimeMap
- class: ExecutableDependencyGraph
- class: RepositoryZone
- class: ExecutableRepositoryResult

### lib/python/executable_repository_intelligence/report.py

- class: ExecutionModelReportGenerator
- relevant methods: _executable_dependency_graph

### lib/python/executable_repository_intelligence/runtime_map.py

- class: RuntimeMapBuilder
- relevant methods: _find_main_entry, _find_bootstrap
- function: _read_text

### lib/python/executive_briefing_engine/insight_generator.py

- class: ExecutiveInsightGenerator
- relevant methods: repository_health

### lib/python/executive_briefing_engine/persistence.py

- class: ExecutiveBriefingPersistence
- relevant methods: _read

### lib/python/executive_briefing_engine/recommendation_engine.py

- class: ExecutiveRecommendationEngine
- relevant methods: _healthy_repository_recommendation

### lib/python/executive_briefing_engine/risk_analyzer.py

- class: ExecutiveRiskAnalyzer
- relevant methods: _repository_integrity_risks

### lib/python/experience/coordination_journal.py

- class: JsonFileCoordinationJournal
- relevant methods: _read_store

### lib/python/experience/deployment.py

- function: prepare_experience_repository

### lib/python/experience/evidence_integration.py

- class: ExperienceEvidenceIntegrator
- relevant methods: find_for_experience

### lib/python/experience/forgetting_persistence.py

- class: ExperienceForgettingRepository

### lib/python/experience/performance.py

- function: characterize_persistent_repository

### lib/python/experience/persistent_repository.py

- class: PersistentExperienceRepositoryError
- class: JsonFileExperienceRepository
- relevant methods: _read_store

### lib/python/experience/protection_repository.py

- class: ProtectionRepositoryError
- class: ProtectionAlreadyExistsError
- class: ProtectionRepository
- class: JsonFileProtectionRepository
- relevant methods: _read_store

### lib/python/experience/provenance_integration.py

- class: ExperienceProvenanceError
- class: ExperienceProvenance

### lib/python/experience/repository.py

- class: ExperienceRepositoryError
- class: ExperienceAlreadyExistsError
- class: ExperienceRepository
- class: InMemoryExperienceRepository

### lib/python/experience/retention_persistence.py

- class: ExperienceRetentionRepository

### lib/python/knowledge_engine/database.py

- class: KnowledgeDatabase

### lib/python/knowledge_engine/engine.py

- class: KnowledgeEngine

### lib/python/knowledge_graph/builder.py

- class: CanonicalKnowledgeGraphBuilder

### lib/python/knowledge_graph/graph.py

- class: CanonicalKnowledgeGraph

### lib/python/knowledge_graph_v2/engine.py

- class: KnowledgeGraphEngine

### lib/python/knowledge_materialization/engine.py

- class: KnowledgeObject
- class: KnowledgeRelationship
- class: MaterializedKnowledge
- class: KnowledgeMaterializationEngine

### lib/python/project_profiles/trading_signals.py

- class: TradingSignalsProfile
- relevant methods: inspect

### lib/python/repository_engine/classifier.py

- class: RepositoryFileClassifier

### lib/python/repository_engine/cli.py

- function: inspect

### lib/python/repository_engine/engine.py

- class: RepositoryEngine

### lib/python/repository_engine/exporter.py

- class: RepositoryExporter

### lib/python/repository_engine/models.py

- class: RepositoryItem
- class: RepositoryMetrics
- class: RepositoryProfile

### lib/python/repository_engine/serializer.py

- class: RepositoryProfileSerializer

### lib/python/repository_inspector_v2/analyzer.py

- class: RepositoryAnalyzer

### lib/python/repository_inspector_v2/engine.py

- class: RepositoryInspectorV2
- relevant methods: inspect

### lib/python/rule_engine/rules/repository_size_rule.py

- class: RepositorySizeRule

### lib/python/runtime/diagnostics.py

- class: RuntimeDiagnosticsService
- relevant methods: _read_json

### lib/python/runtime/health.py

- class: HealthService
- relevant methods: check_readiness

### lib/python/runtime/interfaces/http_server.py

- class: _RuntimeHandler
- relevant methods: _read_body
- class: RuntimeHttpServer
- relevant methods: set_ready_handler, handle_ready

### lib/python/runtime/interfaces/telegram_gateway.py

- class: TelegramGateway
- relevant methods: _command_map_lookup

### lib/python/runtime/lifecycle.py

- class: LifecycleManager
- relevant methods: is_ready

### lib/python/runtime/organism.py

- class: EpistemicOrganismAccess
- relevant methods: _provenance_state

### lib/python/self_evaluation_engine/analyzers.py

- class: RepositoryComplianceAnalyzer

### lib/python/self_evaluation_engine/models.py

- class: RegressionFinding
- class: ArchitectureFinding

### lib/python/self_evaluation_engine/persistence.py

- class: EvaluationPersistence
- relevant methods: _read

### lib/python/self_improvement_engine/persistence.py

- class: ImprovementPersistence
- relevant methods: _read

### lib/python/semantic_matching/matcher.py

- class: SemanticMatcher
- relevant methods: _read_file

### lib/python/semantic_repository_intelligence/architecture_graph.py

- class: ArchitectureGraphBuilder

### lib/python/semantic_repository_intelligence/ast_analyzer.py

- class: ASTAnalyzer
- relevant methods: _find_analyzer

### lib/python/semantic_repository_intelligence/call_graph.py

- class: CallGraphBuilder
- relevant methods: _find_entry_points, _trace_chains

### lib/python/semantic_repository_intelligence/dependency_graph.py

- class: DependencyGraphBuilder

### lib/python/semantic_repository_intelligence/engine.py

- class: SemanticRepositoryEngine

### lib/python/semantic_repository_intelligence/import_graph.py

- class: RelationshipResolver
- relevant methods: resolve
- class: ImportGraphBuilder
- relevant methods: _find_cycles

### lib/python/semantic_repository_intelligence/models.py

- class: ImportGraphResult
- class: CallGraphResult
- class: DependencyGraphResult
- class: ArchitectureGraphResult
- class: SemanticFinding
- class: RepositoryComplexity

### lib/python/semantic_repository_intelligence/recommendation_engine.py

- class: SemanticRecommendationEngine
- relevant methods: generate_findings

### lib/python/semantic_repository_intelligence/relationship_resolver.py

- class: RelationshipResolver
- relevant methods: resolve_import, resolve_symbol

### lib/python/validation_engine/csl_validator.py

- class: ValidationFinding

### lib/python/workspace_index/incremental.py

- class: RepositorySnapshot

### lib/python/workspace_index/models.py

- class: WorkspaceIndex
- relevant methods: repository_name, repository_root

### lib/python/workspace_index/policy.py

- class: RepositoryPolicy

### lib/python/workspace_orchestrator/dependency_graph.py

- class: WorkspaceDependencyGraph

### lib/python/workspace_orchestrator/engine.py

- class: WorkspaceOrchestrator
- relevant methods: register_repository

### lib/python/workspace_orchestrator/intelligence.py

- class: WorkspaceRiskAnalyzer
- relevant methods: _blocked_repository_risks, _low_readiness_risks, _isolated_repository_risks
- class: WorkspaceRecommendationEngine
- relevant methods: _next_repository_recommendation

### lib/python/workspace_orchestrator/models.py

- class: WorkspaceRepository

### lib/python/workspace_orchestrator/persistence.py

- class: WorkspacePersistence
- relevant methods: _read_json

### lib/python/workspace_orchestrator/registry.py

- class: RepositoryRegistry

### lib/python/workspace_orchestrator/scanner.py

- class: WorkspaceScanner
- relevant methods: scan_repository, _map_to_repository

### lib/python/workspace_orchestrator/state_manager.py

- class: WorkspaceStateManager
- relevant methods: register_repository, remove_repository, rename_repository, relocate_repository, update_repository, repository_count

## Verified Import / Signature Characterization

### python.agents.repository_inspector_agent

- import: PASS
- class RepositoryInspectorAgent: module_export=True
  signature: ()

### python.ai_control_center.panels.repository.panel

- import: PASS
- class RepositoryPanel: module_export=True
  signature: (root: 'Path') -> None
  method git_repositoryUNAVAILABLE

### python.ai_control_center.providers.local_repository

- import: FAILED
- error: ModuleNotFoundError: No module named 'repository_engine'

### python.ai_cto_scanner.report

- import: PASS
- class AICTOReportGenerator: module_export=True
  signature: ()
  method _readiness_scores(self, r)
  method _semantic_architecture_graph(self, semantic)
  method _semantic_findings(self, semantic)
  method _repository_complexity(self, semantic)

### python.ai_cto_scanner.scoring

- import: PASS
- class ReadinessScorer: module_export=True
  signature: ()
  method _compute_development_readiness(self, detection_results, canonical_stats)

### python.ai_platform.context_builder

- import: PASS
- class AIContextBuilder: module_export=True
  signature: (repository_root: 'str' = '.', workspace_root: 'str | None' = None) -> 'None'
  method _read_json(self, path: 'Path') -> 'Dict[str, Any]'

### python.ai_platform.model_manager

- import: PASS
- class ModelManager: module_export=True
  signature: ()
  method resolve_roles(self, settings: 'Mapping[str, Any]', discovered: 'Mapping[str, List[str]]') -> 'Dict[str, str]'

### python.ai_platform.prompt_library

- import: PASS
- class PromptLibrary: module_export=True
  signature: ()
  method resolve(self, name: 'str', fallback: 'str' = '') -> 'str'

### python.ai_platform.service

- import: PASS
- class AIPlatformService: module_export=True
  signature: (repository_root: 'str' = '.', workspace_root: 'Optional[str]' = None) -> 'None'
  method ask_repository(self, question: 'str', *, session_id: 'str' = '', provider_id: 'str' = '', model: 'str' = '', prompt_name: 'str' = '') -> 'Dict[str, Any]'

### python.ai_platform.sessions

- import: PASS
- class AISessionEngine: module_export=True
  signature: (repository_root: 'str' = '.') -> 'None'
  method _read(self, path: 'Path') -> 'Dict[str, Any]'

### python.autonomous_execution_engine.persistence

- import: PASS
- class ExecutionPersistence: module_export=True
  signature: (repository_root: str = '.') -> None
  method _read(self, filename: str) -> Dict[str, Any]

### python.autonomous_execution_engine.policy

- import: PASS
- class ExecutionApproval: module_export=True
  signature: ()
  method resolve(self, development_state: Mapping[str, Any], briefing: Mapping[str, Any], mode: str) -> str

### python.autonomous_execution_engine.validator

- import: PASS
- class ExecutionValidator: module_export=True
  signature: (repository: str = '.') -> None
  method validate_repository(self) -> python.autonomous_execution_engine.models.ValidationResult

### python.autonomous_planning_engine.batch_planner

- import: PASS
- class BatchPlanner: module_export=True
  signature: (repository_root: str = '.') -> None
  method _find_in_development_batches(self) -> Dict[str, pathlib.Path]

### python.autonomous_planning_engine.decision_engine

- import: PASS
- class PlanningDecisionEngine: module_export=True
  signature: (repository_root: str = '.') -> None
  method _repository_health(snapshot: Mapping[str, Any]) -> str

### python.autonomous_planning_engine.dependency_resolver

- import: PASS
- class DependencyGraph: module_export=True
  signature: () -> None
- class DependencyResolver: module_export=True
  signature: (repository_root: str = '.') -> None
  method build_core_graph(self) -> python.autonomous_planning_engine.dependency_resolver.DependencyGraph
  method build_batch_graph(self) -> python.autonomous_planning_engine.dependency_resolver.DependencyGraph
  method resolve_entries(self, entries: Iterable[Mapping[str, Any]]) -> List[Mapping[str, Any]]

### python.autonomous_planning_engine.persistence

- import: PASS
- class PlanningPersistence: module_export=True
  signature: (repository_root: str = '.') -> None
  method _read(self, filename: str) -> Dict[str, Any]

### python.batch_planner.planner

- import: PASS
- class BatchPlanner: module_export=True
  signature: ()
  method _resolve_dependencies(self, canonical_repo, doc_id)

### python.canonical_entities.models

- import: PASS
- class DriftFinding: module_export=True
  signature: (id: str, category: str, severity: python.canonical_entities.models.DriftSeverity, canonical_ref: str, implementation_ref: str, description: str, evidence: List[str] = <factory>, recommendation: str = '', confidence: float = 0.0, detected_at: str = '') -> None

### python.canonical_parser.lexer

- import: PASS
- class CslLexer: module_export=True
  signature: (source: 'str', source_name: 'str' = '')
  method _read_string(self, content: 'str', start: 'int')
  method _read_word(self, content: 'str', start: 'int')

### python.canonical_repository.repository

- import: PASS
- class CanonicalRepository: module_export=True
  signature: ()
  method dependency_graph(self)

### python.cdm_engine.engine

- import: PASS
- class CdmTraceabilityLink: module_export=True
  signature: (relation: 'str', target: 'str', source_context: 'str' = '') -> None

### python.context_synchronization_engine.engine

- import: PASS
- class ContextResolver: module_export=True
  signature: (repository_root: str = '.')
  method resolve(self, git_context: Mapping[str, Any], github_context: Mapping[str, Any], development_context: Mapping[str, Any], workspace_context: Mapping[str, Any], cache: Mapping[str, Any]) -> Dict[str, Any]
  method _resolve_next_core(self, *, active_core: str, current_recommendation: str, planning_next_core: str, semantic_next_core: str, previous: str) -> Tuple[str, str, str]
- class ContextValidator: module_export=True
  signature: ()
  method _field_finding(self, category: str, field: str, before: Any, after: Any, corrected_fields: List[str]) -> List[python.context_synchronization_engine.models.SynchronizationFinding]

### python.context_synchronization_engine.models

- import: PASS
- class SynchronizationFinding: module_export=True
  signature: (category: str, severity: str, message: str, evidence: Tuple[str, ...] = (), corrected: bool = False) -> None

### python.dashboard.service

- import: PASS
- class EngineeringDashboardService: module_export=True
  signature: (repository_root: 'str' = '.', workspace_root: 'Optional[str]' = None, cache_ttl_seconds: 'float' = 5.0, organism_service: 'Optional[Any]' = None) -> 'None'
  method render_repository(self, payload: 'Optional[Dict[str, Any]]' = None, *, question: 'str' = '', prompt_name: 'str' = '') -> 'str'
  method _load_repository_profile(self) -> 'Dict[str, Any]'
  method ask_repository(self, question: 'str', prompt_name: 'str' = '') -> 'Dict[str, Any]'
  method _resolve_related_paths(self, relative_paths: 'Iterable[str]') -> 'List[Path]'
  method _repository_usage(self, definition: 'CapabilityDefinition', workspace: 'Mapping[str, Any]') -> 'List[str]'
  method _read_json(self, path: 'Optional[Path]') -> 'Optional[Dict[str, Any]]'
  method _inspection_panel(self, inspection: 'Mapping[str, Any]') -> 'str'
  method _repository_table(self, items: 'Iterable[Mapping[str, Any]]') -> 'str'

### python.development_state_engine.models

- import: PASS
- class RepositoryState: module_export=True
  signature: (identifier: str, repository: str, branch: str, head_commit: str, open_pull_requests: Tuple[str, ...] = (), latest_merge: str = '', tags: Tuple[str, ...] = (), release: str = '', repository_health: str = 'UNKNOWN', schema_version: str = '1.0.0') -> None

### python.development_state_engine.repository

- import: PASS
- class DevelopmentStateRepository: module_export=True
  signature: (repository_root: Union[str, pathlib.Path] = '.')
  method _read_json(self, path: pathlib.Path) -> Dict[str, Any]
  method _safe_read_integrity(self) -> Dict[str, Any]
  method _resolve_snapshot_path(self, snapshot_reference: str) -> pathlib.Path

### python.development_state_engine.runtime

- import: PASS
- class DevelopmentStateEventBus: module_export=True
  signature: (repository_root: Union[str, pathlib.Path] = '.')
  method _read_json(self, path: pathlib.Path) -> Dict[str, Any]
- class DevelopmentStateManager: module_export=True
  signature: (repository_root: Union[str, pathlib.Path] = '.', repository: Optional[python.development_state_engine.repository.DevelopmentStateRepository] = None, event_bus: Optional[python.development_state_engine.runtime.DevelopmentStateEventBus] = None, repository_engine_class=<class 'python.repository_engine.engine.RepositoryEngine'>, canonical_engine_class=<class 'python.canonical_intelligence.engine.CanonicalIntelligenceEngine'>, semantic_engine_class=<class 'python.semantic_repository_intelligence.engine.SemanticRepositoryEngine'>, ai_cto_scanner_class=<class 'python.ai_cto_scanner.engine.AICTOScannerEngine'>, executable_intelligence_provider=None)
  method _normalize_repository_state(self, state: python.development_state_engine.models.RepositoryState) -> python.development_state_engine.models.RepositoryState
  method _repository_intelligence(self) -> Dict[str, Any]
  method _semantic_repository_intelligence(self, refresh: bool) -> Dict[str, Any]
  method _executable_repository_intelligence(self, state: python.development_state_engine.models.DevelopmentState, refresh: bool) -> Dict[str, Any]

### python.drift_engine.engine

- import: PASS
- class DriftEngine: module_export=True
  signature: (repository='.', workspace_index=None)
  method _finding(self, finding_id, category, severity, canonical_ref, implementation_ref, description, evidence, recommendation, confidence, detected_at)
  method _orphan_implementation_findings(self, index, matches, timestamp)

### python.engineering_engine.dependency_graph

- import: PASS
- class DependencyGraph: module_export=True
  signature: (graph: 'dict[str, set[str]]' = <factory>) -> None
- class DependencyGraphBuilder: module_export=True
  signature: (root: 'Path')

### python.engineering_engine.github_repository_resolver

- import: PASS
- class GitHubRepository: module_export=True
  signature: (owner: 'str', repo: 'str') -> None
- class GitHubRepositoryResolver: module_export=True
  signature: ()
  method resolve(self) -> 'GitHubRepository'

### python.engineering_engine.import_resolver

- import: PASS
- class ImportResolver: module_export=True
  signature: (repository_root: 'Path')
  method resolve(self, imported: 'str') -> 'str | None'

### python.engineering_engine.knowledge_graph

- import: PASS
- class KnowledgeGraph: module_export=True
  signature: (modules: 'set[str]' = <factory>, interfaces: 'set[str]' = <factory>, classes: 'set[str]' = <factory>, functions: 'set[str]' = <factory>, imports: 'set[str]' = <factory>) -> None
- class KnowledgeGraphBuilder: module_export=True
  signature: ()

### python.engineering_engine.repository_audit

- import: PASS
- class RepositoryAudit: module_export=True
  signature: (repository_root: 'Path')

### python.engineering_engine.repository_model

- import: PASS
- class RepositoryKnowledge: module_export=True
  signature: (modules: 'dict[str, PythonModule]' = <factory>) -> None
- class RepositoryKnowledgeBuilder: module_export=True
  signature: (root: 'Path')

### python.engineering_engine.repository_scanner

- import: PASS
- class RepositoryModel: module_export=True
  signature: (runtime_modules: 'list[str]' = <factory>, runtime_interfaces: 'list[str]' = <factory>, engineering_modules: 'list[str]' = <factory>, tests: 'list[str]' = <factory>, entrypoints: 'list[str]' = <factory>, canonical_documents: 'list[str]' = <factory>) -> None
- class RepositoryScanner: module_export=True
  signature: (root: 'Path')

### python.engineering_engine.semantic_entities

- import: PASS
- class SemanticRepository: module_export=True
  signature: (entities: 'list[SemanticEntity]' = <factory>, relationships: 'list[SemanticRelationship]' = <factory>) -> None

### python.engineering_engine.semantic_query_engine

- import: PASS
- class SemanticQueryEngine: module_export=True
  signature: (repository: 'SemanticRepository')
  method find_by_type(self, entity_type: 'EntityType') -> 'list[SemanticEntity]'
  method find_entity(self, name: 'str') -> 'SemanticEntity | None'

### python.engineering_engine.semantic_repository_builder

- import: PASS
- class SemanticRepositoryBuilder: module_export=True
  signature: (root: 'Path')

### python.engineering_workspace.workspace

- import: PASS
- class EngineeringWorkspace: module_export=True
  signature: ()
  method repository(self) -> 'Any'
  method knowledge(self) -> 'Any'

### python.epistemic.layered_memory

- import: PASS
- class LayeredMemoryNode: module_export=True
  signature: (node_id: 'LayeredMemoryNodeId', memory: 'SedimentedMemory', depth: 'int', parent_ids: 'tuple[LayeredMemoryNodeId, ...]' = (), child_ids: 'tuple[LayeredMemoryNodeId, ...]' = ()) -> None
  method provenance_identifierUNAVAILABLE
- class LayeredMemory: module_export=True
  signature: () -> 'None'
  method provenance_route(self, node_id: 'LayeredMemoryNodeId') -> 'tuple[str, str]'
- class LayeredMemoryRepository: module_export=True
  signature: (layered_memory: 'LayeredMemory | None' = None) -> 'None'
- class LayeredMemoryTraversal: module_export=True
  signature: (layered_memory: 'LayeredMemory', trail: 'tuple[LayeredMemoryNodeId, ...]') -> None
  method provenance_route(self) -> 'tuple[str, str]'

### python.epistemic.provenance

- import: PASS
- class ProvenanceError: module_export=True
- class Knowledge: module_export=True
  signature: (identifier: 'str', title: 'str', statement: 'str', verification_identifier: 'str', authority: 'str', status: 'str' = 'ESTABLISHED') -> None
- class KnowledgePromotionError: module_export=True
- class Provenance: module_export=True
  signature: () -> 'None'
  method promote_knowledge(self, verification: 'Verification', title: 'str', statement: 'str', *, authority: 'str') -> 'Knowledge'
  method knowledge_for_verification(self, verification: 'Verification') -> 'tuple[Knowledge, ...]'
  method verification_for_knowledge(self, knowledge: 'Knowledge') -> 'Verification'
  method provenance_to_source_from_knowledge(self, knowledge: 'Knowledge') -> 'tuple[Knowledge, Verification, Claim, tuple[Evidence, ...], tuple[Observation, ...], tuple[Source, ...]]'
  method current_states_for_knowledge(self, knowledge: 'Knowledge') -> 'tuple[CurrentState, ...]'
  method knowledge_for_current_state(self, current_state: 'CurrentState') -> 'Knowledge'
  method provenance_to_source_from_current_state(self, current_state: 'CurrentState') -> 'tuple[CurrentState, Knowledge, Verification, Claim, tuple[Evidence, ...], tuple[Observation, ...], tuple[Source, ...]]'
  method provenance_from_source_to_current_state(self, source: 'Source') -> 'tuple[Source, tuple[Observation, ...], tuple[Evidence, ...], tuple[Claim, ...], tuple[Verification, ...], tuple[Knowledge, ...], tuple[CurrentState, ...]]'
  method provenance_to_source(self, verification: 'Verification') -> 'tuple[Verification, Claim, tuple[Evidence, ...], tuple[Observation, ...], tuple[Source, ...]]'
  method provenance_from_source(self, source: 'Source') -> 'tuple[Source, tuple[Observation, ...], tuple[Evidence, ...], tuple[Claim, ...], tuple[Verification, ...]]'
  method provenance_from_source_to_knowledge(self, source: 'Source') -> 'tuple[Source, tuple[Observation, ...], tuple[Evidence, ...], tuple[Claim, ...], tuple[Verification, ...], tuple[Knowledge, ...]]'
  method _require_registered_knowledge(self, knowledge: 'Knowledge') -> 'None'
- function _knowledge_identifier(number: 'int') -> 'str'
- function _require_knowledge_text(name: 'str', value: 'str') -> 'str'
- function promote_verified_knowledge(verification: 'Verification', *, identifier: 'str', title: 'str', statement: 'str', authority: 'str') -> 'Knowledge'

### python.epistemic.sedimentation

- import: PASS
- class Sedimentation: module_export=True
  signature: (identifier: 'str', title: 'str', provenance_identifier: 'str', statement: 'str', target: 'SedimentationTarget', authority: 'SedimentationAuthority' = <SedimentationAuthority.PROPOSED: 'PROPOSED'>, uncertainty: 'str | None' = None) -> None
  method human_readable_identityUNAVAILABLE
- class SedimentationRepository: module_export=True
  signature: () -> 'None'
  method by_provenance(self, provenance_identifier: 'str') -> 'tuple[Sedimentation, ...]'

### python.epistemic.sedimented_memory

- import: PASS
- class DownstreamKnowledgeError: module_export=True
- class SedimentedMemoryPhysiology: module_export=True
  signature: (knowledge_receptor: 'KnowledgeReceptor | None' = None) -> 'None'
  method _provenance_identifier(governed: 'GovernedSedimentation') -> 'str'
  method _to_knowledge(self, governed: 'GovernedSedimentation') -> 'object'

### python.epistemic.transformation

- import: PASS
- class TransformationLifecycle: module_export=True
  signature: (root: 'Path | None' = None)
  method resolve_reference(self, reference: 'EpistemicReference') -> 'Path | None'
  method inspect(self, identifier: 'str') -> 'dict[str, object]'

### python.evidence_engine.engine

- import: PASS
- class EvidenceEngine: module_export=True
  signature: (repository='.')
  method find(self, keyword)

### python.executable_repository_intelligence.engine

- import: PASS
- class ExecutableRepositoryEngine: module_export=True
  signature: (repository: str = '.', workspace_index=None, persist: bool = True)

### python.executable_repository_intelligence.executable_dep_graph

- import: PASS
- class ExecutableDependencyGraphBuilder: module_export=True
  signature: ()

### python.executable_repository_intelligence.models

- import: PASS
- class RepositoryRuntimeMap: module_export=True
  signature: (main_entry_point: Optional[str], execution_chain: List[str], bootstrap_sequence: List[str], runtime_components: List[python.executable_repository_intelligence.models.RuntimeComponent], initialization_order: List[str], scheduler_entry: Optional[str], background_workers: List[str], telegram_runtime: List[str], owner_runtime: List[str], admin_runtime: List[str], persistence_runtime: List[str], shutdown_hooks: List[str], restart_hooks: List[str], resume_hooks: List[str]) -> None
- class ExecutableDependencyGraph: module_export=True
  signature: (nodes: List[str], edges: List[python.executable_repository_intelligence.models.ExecutableDependencyEdge], excluded: List[str], exclusion_reasons: Dict[str, str]) -> None
- class RepositoryZone: module_export=True
  signature: (path: str, zone: str, file_count: int, evidence: List[str]) -> None
- class ExecutableRepositoryResult: module_export=True
  signature: (repository: str, file_classifications: List[python.executable_repository_intelligence.models.FileClassification], runtime_map: python.executable_repository_intelligence.models.RepositoryRuntimeMap, executable_dependency_graph: python.executable_repository_intelligence.models.ExecutableDependencyGraph, injection_safety: List[python.executable_repository_intelligence.models.InjectionSafetyRecord], zones: List[python.executable_repository_intelligence.models.RepositoryZone], recommendations: List[python.executable_repository_intelligence.models.ExecutableRecommendation], executable_file_count: int, non_executable_file_count: int, category_distribution: Dict[str, int], zone_distribution: Dict[str, int], safety_distribution: Dict[str, int]) -> None

### python.executable_repository_intelligence.report

- import: PASS
- class ExecutionModelReportGenerator: module_export=True
  signature: ()
  method _executable_dependency_graph(self, r: Dict[str, Any]) -> str

### python.executable_repository_intelligence.runtime_map

- import: PASS
- class RuntimeMapBuilder: module_export=True
  signature: ()
  method _find_main_entry(self, file_analyses: Dict, exec_files: Set[str]) -> Optional[str]
  method _find_bootstrap(self, file_classifications: List[python.executable_repository_intelligence.models.FileClassification], file_analyses: Dict, root: pathlib.Path) -> List[str]
- function _read_text(root: pathlib.Path, path_str: str) -> str

### python.executive_briefing_engine.insight_generator

- import: PASS
- class ExecutiveInsightGenerator: module_export=True
  signature: ()
  method repository_health(self, snapshot: Mapping[str, Any]) -> str

### python.executive_briefing_engine.persistence

- import: PASS
- class ExecutiveBriefingPersistence: module_export=True
  signature: (repository_root: str = '.')
  method _read(self, path: pathlib.Path) -> Dict[str, Any]

### python.executive_briefing_engine.recommendation_engine

- import: PASS
- class ExecutiveRecommendationEngine: module_export=True
  signature: ()
  method _healthy_repository_recommendation(self, next_id) -> python.executive_briefing_engine.models.ExecutiveRecommendation

### python.executive_briefing_engine.risk_analyzer

- import: PASS
- class ExecutiveRiskAnalyzer: module_export=True
  signature: ()
  method _repository_integrity_risks(self, next_id, integrity: Mapping[str, Any], state: Mapping[str, Any]) -> List[python.executive_briefing_engine.models.ExecutiveRisk]

### python.experience.coordination_journal

- import: PASS
- class JsonFileCoordinationJournal: module_export=True
  signature: (path: 'str | Path') -> 'None'
  method _read_store(self) -> 'dict[str, dict[str, Any]]'

### python.experience.deployment

- import: PASS
- function prepare_experience_repository(*, environment: 'dict[str, str] | None' = None, repository_root: 'str | Path | None' = None) -> 'JsonFileExperienceRepository'

### python.experience.evidence_integration

- import: PASS
- class ExperienceEvidenceIntegrator: module_export=True
  signature: (evidence_engine: 'EvidenceEngine') -> 'None'
  method find_for_experience(self, *, experience_id: 'ExperienceId', keyword: 'str') -> 'ExperienceEvidenceReference'

### python.experience.forgetting_persistence

- import: PASS
- class ExperienceForgettingRepository: module_export=True
  signature: (root: 'str | Path') -> 'None'

### python.experience.performance

- import: PASS
- function characterize_persistent_repository(path: 'str | Path', *, experience_count: 'int') -> 'ExperiencePerformanceSample'

### python.experience.persistent_repository

- import: PASS
- class PersistentExperienceRepositoryError: module_export=True
- class JsonFileExperienceRepository: module_export=True
  signature: (path: 'str | Path') -> 'None'
  method _read_store(self) -> 'dict[str, Any]'

### python.experience.protection_repository

- import: PASS
- class ProtectionRepositoryError: module_export=True
- class ProtectionAlreadyExistsError: module_export=True
- class ProtectionRepository: module_export=True
  signature: ()
- class JsonFileProtectionRepository: module_export=True
  signature: (path: 'str | Path') -> 'None'
  method _read_store(self) -> 'dict[str, Any]'

### python.experience.provenance_integration

- import: PASS
- class ExperienceProvenanceError: module_export=True
- class ExperienceProvenance: module_export=True
  signature: (experience_id: 'ExperienceId', provenance: 'str', mechanism: 'str', observed_at: 'datetime', session_context: 'str | None' = None, derived_from: 'tuple[str, ...]' = (), historical_fact: 'str | None' = None, interpretation: 'str | None' = None) -> None

### python.experience.repository

- import: PASS
- class ExperienceRepositoryError: module_export=True
- class ExperienceAlreadyExistsError: module_export=True
- class ExperienceRepository: module_export=True
  signature: ()
- class InMemoryExperienceRepository: module_export=True
  signature: () -> 'None'

### python.experience.retention_persistence

- import: PASS
- class ExperienceRetentionRepository: module_export=True
  signature: (root: 'str | Path') -> 'None'

### python.knowledge_engine.database

- import: PASS
- class KnowledgeDatabase: module_export=True
  signature: ()

### python.knowledge_engine.engine

- import: PASS
- class KnowledgeEngine: module_export=True
  signature: ()

### python.knowledge_graph.builder

- import: PASS
- class CanonicalKnowledgeGraphBuilder: module_export=True
  signature: ()

### python.knowledge_graph.graph

- import: PASS
- class CanonicalKnowledgeGraph: module_export=True
  signature: ()

### python.knowledge_graph_v2.engine

- import: PASS
- class KnowledgeGraphEngine: module_export=True
  signature: (repository='.', workspace_index=None)

### python.knowledge_materialization.engine

- import: PASS
- class KnowledgeObject: module_export=True
  signature: (id: 'str', kind: 'str', name: 'str', source: 'str', version: 'str', status: 'str', metadata: 'Dict[str, Any]' = <factory>) -> None
- class KnowledgeRelationship: module_export=True
  signature: (source_id: 'str', target_id: 'str', relation: 'str', confidence: 'float' = 1.0, metadata: 'Dict[str, Any]' = <factory>) -> None
- class MaterializedKnowledge: module_export=True
  signature: (knowledge_objects: 'List[KnowledgeObject]' = <factory>, knowledge_relationships: 'List[KnowledgeRelationship]' = <factory>, knowledge_graph: 'Optional[CanonicalKnowledgeGraph]' = None, dependency_graph: 'Dict[str, List[str]]' = <factory>, traceability_graph: 'Dict[str, List[str]]' = <factory>) -> None
- class KnowledgeMaterializationEngine: module_export=True
  signature: ()

### python.project_profiles.trading_signals

- import: PASS
- class TradingSignalsProfile: module_export=True
  signature: ()
  method inspect(self, repository)

### python.repository_engine.classifier

- import: PASS
- class RepositoryFileClassifier: module_export=True
  signature: ()

### python.repository_engine.cli

- import: PASS
- function inspect(path='.')

### python.repository_engine.engine

- import: PASS
- class RepositoryEngine: module_export=True
  signature: (root='.', workspace_index=None)

### python.repository_engine.exporter

- import: PASS
- class RepositoryExporter: module_export=True
  signature: ()

### python.repository_engine.models

- import: PASS
- class RepositoryItem: module_export=True
  signature: (path: str, name: str, item_type: str, size: int) -> None
- class RepositoryMetrics: module_export=True
  signature: (total_files: int, total_directories: int, language_distribution: Dict[str, int], file_class_distribution: Dict[str, int], test_file_count: int, documentation_file_count: int, entry_point_count: int, documentation_coverage_ratio: float, test_coverage_ratio: float) -> None
- class RepositoryProfile: module_export=True
  signature: (path: str, name: str, metrics: python.repository_engine.models.RepositoryMetrics, classified_files: List[python.repository_engine.models.ClassifiedFile], tech_stack: List[str], entry_points: List[str], dependencies: python.repository_engine.models.DependencyMap, health_summary: Dict[str, Any]) -> None

### python.repository_engine.serializer

- import: PASS
- class RepositoryProfileSerializer: module_export=True
  signature: ()

### python.repository_inspector_v2.analyzer

- import: PASS
- class RepositoryAnalyzer: module_export=True
  signature: ()

### python.repository_inspector_v2.engine

- import: PASS
- class RepositoryInspectorV2: module_export=True
  signature: (root='.', workspace_index=None)
  method inspect(self)

### python.rule_engine.rules.repository_size_rule

- import: PASS
- class RepositorySizeRule: module_export=True
  signature: ()

### python.runtime.diagnostics

- import: PASS
- class RuntimeDiagnosticsService: module_export=True
  signature: (*, repository_root: 'str', workspace_root: 'str', state_dir: 'str', logs_dir: 'str', cli_commands: 'Iterable[str]') -> 'None'
  method _read_json(self, path: 'Path') -> 'Optional[Dict[str, Any]]'

### python.runtime.health

- import: PASS
- class HealthService: module_export=True
  signature: ()
  method check_readiness(self) -> python.runtime.health.HealthCheckResult

### python.runtime.interfaces.http_server

- import: PASS
- class _RuntimeHandler: module_export=True
  signature: (request, client_address, server)
  method _read_body(self) -> bytes
- class RuntimeHttpServer: module_export=True
  signature: (host: str = '0.0.0.0', port: int = 8080)
  method set_ready_handler(self, fn: Callable[[], dict]) -> None
  method handle_ready(self) -> dict

### python.runtime.interfaces.telegram_gateway

- import: PASS
- class TelegramGateway: module_export=True
  signature: (bot_token: str = '', chat_id: str = '', event_dispatcher: Optional[Any] = None)
  method _command_map_lookup(self, command: str) -> Optional[str]

### python.runtime.lifecycle

- import: PASS
- class LifecycleManager: module_export=True
  signature: ()
  method is_ready(self) -> bool

### python.runtime.organism

- import: PASS
- class EpistemicOrganismAccess: module_export=True
  signature: (repository_root: 'str | Path' = '.') -> 'None'
  method _provenance_state(self) -> 'dict[str, Any]'

### python.self_evaluation_engine.analyzers

- import: PASS
- class RepositoryComplianceAnalyzer: module_export=True
  signature: (repository: str = '.') -> None

### python.self_evaluation_engine.models

- import: PASS
- class RegressionFinding: module_export=True
  signature: (severity: str, component: str, finding: str, impact: str, affected_modules: List[str], confidence: float, recommendation: str, evidence: Dict[str, Any]) -> None
- class ArchitectureFinding: module_export=True
  signature: (category: str, component: str, description: str, severity: str, evidence: Dict[str, Any]) -> None

### python.self_evaluation_engine.persistence

- import: PASS
- class EvaluationPersistence: module_export=True
  signature: (repository_root: str = '.') -> None
  method _read(self, filename: str) -> Dict[str, Any]

### python.self_improvement_engine.persistence

- import: PASS
- class ImprovementPersistence: module_export=True
  signature: (repository_root: str = '.') -> None
  method _read(self, filename: str) -> Dict[str, Any]

### python.semantic_matching.matcher

- import: PASS
- class SemanticMatcher: module_export=True
  signature: (repository='.', workspace_index=None)
  method _read_file(self, relative_path)

### python.semantic_repository_intelligence.architecture_graph

- import: PASS
- class ArchitectureGraphBuilder: module_export=True
  signature: ()

### python.semantic_repository_intelligence.ast_analyzer

- import: PASS
- class ASTAnalyzer: module_export=True
  signature: (root, workspace_index=None)
  method _find_analyzer(self, extension: str) -> Optional[python.semantic_repository_intelligence.ast_analyzer.LanguageAnalyzer]

### python.semantic_repository_intelligence.call_graph

- import: PASS
- class CallGraphBuilder: module_export=True
  signature: ()
  method _find_entry_points(self, file_analyses: Dict[str, python.semantic_repository_intelligence.models.FileAnalysis], func_index: Dict[str, List[tuple]]) -> List[str]
  method _trace_chains(self, entry_points: List[str], adj: Dict[str, Set[str]]) -> List[List[str]]

### python.semantic_repository_intelligence.dependency_graph

- import: PASS
- class DependencyGraphBuilder: module_export=True
  signature: ()

### python.semantic_repository_intelligence.engine

- import: PASS
- class SemanticRepositoryEngine: module_export=True
  signature: (repository: str = '.', workspace_index=None, persist: bool = True)

### python.semantic_repository_intelligence.import_graph

- import: PASS
- class RelationshipResolver: module_export=True
  signature: (root: pathlib.Path, all_python_paths: Set[str])
  method resolve(self, source_path: str, module: str, level: int) -> Optional[str]
- class ImportGraphBuilder: module_export=True
  signature: ()
  method _find_cycles(self, nodes: List[str], adj: Dict[str, List[str]]) -> List[List[str]]

### python.semantic_repository_intelligence.models

- import: PASS
- class ImportGraphResult: module_export=True
  signature: (nodes: List[str], edges: List[python.semantic_repository_intelligence.models.ImportEdge], circular_dependencies: List[List[str]], critical_modules: List[str], orphan_modules: List[str], in_degree: Dict[str, int]) -> None
- class CallGraphResult: module_export=True
  signature: (edges: List[python.semantic_repository_intelligence.models.CallEdge], entry_points: List[str], execution_chains: List[List[str]]) -> None
- class DependencyGraphResult: module_export=True
  signature: (external_dependencies: List[python.semantic_repository_intelligence.models.ExternalDependency], internal_modules: List[str], dependency_count: int) -> None
- class ArchitectureGraphResult: module_export=True
  signature: (nodes: List[python.semantic_repository_intelligence.models.ArchitectureNode], edges: List[python.semantic_repository_intelligence.models.ArchitectureEdge], hotspots: List[str], risks: List[python.semantic_repository_intelligence.models.ArchitectureRisk], high_coupling_modules: List[str], low_cohesion_layers: List[str], extension_points: List[str]) -> None
- class SemanticFinding: module_export=True
  signature: (id: str, category: str, title: str, description: str, severity: str, evidence: List[str], affected_modules: List[str], confidence: float) -> None
- class RepositoryComplexity: module_export=True
  signature: (total_files: int, total_symbols: int, total_imports: int, total_functions: int, total_classes: int, avg_imports_per_module: float, avg_functions_per_file: float, max_imports_in_module: int, max_functions_in_file: int, cyclomatic_complexity_estimate: float, language_distribution: Dict[str, int]) -> None

### python.semantic_repository_intelligence.recommendation_engine

- import: PASS
- class SemanticRecommendationEngine: module_export=True
  signature: ()
  method generate_findings(self, import_graph: python.semantic_repository_intelligence.models.ImportGraphResult, architecture_graph: python.semantic_repository_intelligence.models.ArchitectureGraphResult, injection_points: List[python.semantic_repository_intelligence.models.InjectionPoint]) -> List[python.semantic_repository_intelligence.models.SemanticFinding]

### python.semantic_repository_intelligence.relationship_resolver

- import: PASS
- class RelationshipResolver: module_export=True
  signature: (root: pathlib.Path, file_analyses: Dict[str, python.semantic_repository_intelligence.models.FileAnalysis])
  method resolve_import(self, source_path: str, module: str, level: int = 0) -> Optional[str]
  method resolve_symbol(self, qualified_name: str) -> Optional[str]

### python.validation_engine.csl_validator

- import: PASS
- class ValidationFinding: module_export=True
  signature: (category: 'ValidationCategory', severity: 'str', code: 'str', message: 'str', source_ref: 'str' = '', passed: 'bool' = True) -> None

### python.workspace_index.incremental

- import: PASS
- class RepositorySnapshot: module_export=True
  signature: (version: int, repository_root: str, repository_name: str, created_at: float, files: Tuple[python.workspace_index.incremental.FileSnapshot, ...]) -> None

### python.workspace_index.models

- import: PASS
- class WorkspaceIndex: module_export=True
  signature: (repository_name, repository_root, files, directories, ignored_files, ignored_dirs, statistics, created_at)
  method repository_nameUNAVAILABLE
  method repository_rootUNAVAILABLE

### python.workspace_index.policy

- import: PASS
- class RepositoryPolicy: module_export=True
  signature: (exclude_dirs=None, extra_exclude_dirs=None, exclude_extensions=None, extra_exclude_extensions=None)

### python.workspace_orchestrator.dependency_graph

- import: PASS
- class WorkspaceDependencyGraph: module_export=True
  signature: (repositories: List[python.workspace_orchestrator.models.WorkspaceRepository]) -> None

### python.workspace_orchestrator.engine

- import: PASS
- class WorkspaceOrchestrator: module_export=True
  signature: (workspace_root: str = '.', output_dir: Optional[str] = None, persist: bool = True) -> None
  method register_repository(self, repository_path: str) -> python.workspace_orchestrator.models.WorkspaceRepository

### python.workspace_orchestrator.intelligence

- import: PASS
- class WorkspaceRiskAnalyzer: module_export=True
  signature: ()
  method _blocked_repository_risks(self, next_id, repositories: List[python.workspace_orchestrator.models.WorkspaceRepository]) -> List[python.workspace_orchestrator.models.WorkspaceRisk]
  method _low_readiness_risks(self, next_id, repositories: List[python.workspace_orchestrator.models.WorkspaceRepository]) -> List[python.workspace_orchestrator.models.WorkspaceRisk]
  method _isolated_repository_risks(self, next_id, repositories: List[python.workspace_orchestrator.models.WorkspaceRepository], dependencies: List[python.workspace_orchestrator.models.WorkspaceDependencyEdge]) -> List[python.workspace_orchestrator.models.WorkspaceRisk]
- class WorkspaceRecommendationEngine: module_export=True
  signature: ()
  method _next_repository_recommendation(self, next_id, priorities: List[python.workspace_orchestrator.models.WorkspacePriority]) -> List[python.workspace_orchestrator.models.WorkspaceRecommendation]

### python.workspace_orchestrator.models

- import: PASS
- class WorkspaceRepository: module_export=True
  signature: (name: str, display_name: str, description: str, repository_root: str, repository_type: str = 'unknown', repository_category: str = 'unknown', default_branch: str = 'main', current_branch: str = '', current_issue: str = '', current_pull_request: str = '', current_batch: str = '', current_milestone: str = '', current_epic: str = '', current_recommendation: str = '', development_state: str = 'unknown', executive_briefing_id: str = '', repository_health: str = 'unknown', readiness: float = 0.0, canonical_status: str = 'unknown', semantic_status: str = 'unknown', runtime_status: str = 'unknown', development_status: str = 'unknown', owner_status: str = 'unknown', risk_status: str = 'low', priority: int = 5, dependencies: Tuple[str, ...] = <factory>, dependents: Tuple[str, ...] = <factory>, tags: Tuple[str, ...] = <factory>, last_scan: str = '', last_refresh: str = '', last_briefing: str = '', last_validation: str = '', scan_scores: Dict[str, Any] = <factory>, schema_version: str = '1.0.0') -> None

### python.workspace_orchestrator.persistence

- import: PASS
- class WorkspacePersistence: module_export=True
  signature: (workspace_root: str = '.')
  method _read_json(self, filename: str) -> Optional[Any]

### python.workspace_orchestrator.registry

- import: PASS
- class RepositoryRegistry: module_export=True
  signature: () -> None

### python.workspace_orchestrator.scanner

- import: PASS
- class WorkspaceScanner: module_export=True
  signature: () -> None
  method scan_repository(self, name: str, root: str) -> python.workspace_orchestrator.models.WorkspaceRepository
  method _map_to_repository(self, name: str, root: str, git_info: Dict[str, str], scan_data: Dict[str, Any], scan_error: Optional[str]) -> python.workspace_orchestrator.models.WorkspaceRepository

### python.workspace_orchestrator.state_manager

- import: PASS
- class WorkspaceStateManager: module_export=True
  signature: (workspace_root: str = '.') -> None
  method register_repository(self, repo: python.workspace_orchestrator.models.WorkspaceRepository) -> None
  method remove_repository(self, name: str) -> Optional[python.workspace_orchestrator.models.WorkspaceRepository]
  method rename_repository(self, old_name: str, new_name: str) -> bool
  method relocate_repository(self, name: str, new_root: str) -> bool
  method update_repository(self, repo: python.workspace_orchestrator.models.WorkspaceRepository) -> None
  method repository_count(self) -> int

## Source-Level Capability Evidence

### search

- lib/python/ai_cto_scanner/detectors.py:132 — if re.search(pat, text, re.IGNORECASE | re.MULTILINE):
- lib/python/ai_platform/cognitive_coordination.py:169 — "search",
- lib/python/ai_platform/context_builder.py:63 — "search",
- lib/python/autonomous_planning_engine/batch_planner.py:32 — m = _BATCH_RE.search(batch_id)
- lib/python/autonomous_planning_engine/batch_planner.py:42 — m = _STATUS_RE.search(content)
- lib/python/autonomous_planning_engine/batch_planner.py:159 — m = _BATCH_RE.search(md_file.stem)
- lib/python/autonomous_planning_engine/decision_engine.py:102 — search_dirs = [
- lib/python/autonomous_planning_engine/decision_engine.py:106 — search_files = list(self.root.glob("README*"))
- lib/python/autonomous_planning_engine/decision_engine.py:108 — for d in search_dirs:
- lib/python/autonomous_planning_engine/decision_engine.py:119 — for f in search_files:
- lib/python/autonomous_planning_engine/dependency_resolver.py:40 — match = _CORE_RE.search(source[:2000])
- lib/python/canonical_parser/parser.py:62 — ref = self._DOC_REF_RE.search(filename)
- lib/python/context_synchronization_engine/engine.py:135 — match = re.search(r"(CORE[-_]?\d{3}[A-Z]?)", branch or "", flags=re.IGNORECASE)
- lib/python/context_synchronization_engine/engine.py:146 — match = re.search(r"(?:issue|task|pr)[-_]?(\d+)", branch or "", flags=re.IGNORECASE)
- lib/python/context_synchronization_engine/engine.py:150 — match = re.search(r"(BATCH[-_]?\d{3})", branch or "", flags=re.IGNORECASE)
- lib/python/context_synchronization_engine/engine.py:209 — match = re.search(r"[:/]([^/:]+)/([^/]+?)(?:\.git)?$", remote_url)
- lib/python/context_synchronization_engine/engine.py:600 — match = re.search(r"(CORE-\d{3}[A-Z]?)", text or "", flags=re.IGNORECASE)
- lib/python/dashboard/service.py:138 — future_roadmap="Add search, graph navigation, and richer cross-linking between reports, files, and decisions.",
- lib/python/executable_repository_intelligence/file_classifier.py:297 — elif kind == "path_re" and re.search(value, path_str):
- lib/python/executable_repository_intelligence/runtime_map.py:70 — if p.search(text):
- lib/python/semantic_repository_intelligence/dependency_graph.py:61 — m = _SETUP_INSTALL_RE.search(text)
- lib/python/workspace_orchestrator/dashboard.py:139 — m = re.search(r"CORE-\d+[A-Z]?", text)

### resolve

- lib/python/ai_control_center/panels/repository/panel.py:22 — return cls(Path(path).resolve())
- lib/python/ai_control_center/providers/local_repository.py:23 — self._root = Path(root).resolve()
- lib/python/ai_cto_scanner/engine.py:55 — self.root = Path(repository).resolve()
- lib/python/ai_cto_scanner/engine.py:56 — self.output_dir = Path(output_dir).resolve() if output_dir else Path(".").resolve()
- lib/python/ai_platform/cognitive_coordination.py:170 — "resolve",
- lib/python/ai_platform/context_builder.py:18 — self.repository_root = Path(repository_root).resolve()
- lib/python/ai_platform/context_builder.py:19 — self.workspace_root = Path(workspace_root).resolve() if workspace_root else self.repository_root.parent
- lib/python/ai_platform/context_builder.py:64 — "resolve",
- lib/python/ai_platform/conversation_context.py:41 — self.repository_root = Path(repository_root).resolve()
- lib/python/ai_platform/conversation_context.py:43 — Path(workspace_root).resolve()
- lib/python/ai_platform/conversation_experience.py:44 — self.repository_root = Path(repository_root).resolve()
- lib/python/ai_platform/model_manager.py:15 — def resolve_roles(self, settings: Mapping[str, Any], discovered: Mapping[str, List[str]]) -> Dict[str, str]:
- lib/python/ai_platform/pipeline.py:34 — roles = self.model_manager.resolve_roles(settings, discovered)
- lib/python/ai_platform/prompt_library.py:41 — def resolve(self, name: str, fallback: str = "") -> str:
- lib/python/ai_platform/service.py:203 — prompt = self.prompt_library.resolve(
- lib/python/ai_platform/service.py:390 — role_models = self.model_manager.resolve_roles(settings, discovered)
- lib/python/ai_platform/sessions.py:12 — self.root = Path(repository_root).resolve()
- lib/python/ai_platform/settings.py:24 — self.root = Path(repository_root).resolve()
- lib/python/autonomous_execution_engine/engine.py:235 — self.root = Path(repository).resolve()
- lib/python/autonomous_execution_engine/engine.py:237 — Path(workspace_root).resolve()
- lib/python/autonomous_execution_engine/engine.py:241 — self.output_dir = Path(output_dir).resolve() if output_dir else self.root
- lib/python/autonomous_execution_engine/engine.py:349 — approval = approval_resolver.resolve(state_data, briefing_data, self.mode)
- lib/python/autonomous_execution_engine/persistence.py:39 — self.repository_root = Path(repository_root).resolve()
- lib/python/autonomous_execution_engine/policy.py:157 — def resolve(
- lib/python/autonomous_planning_engine/batch_planner.py:54 — self.root = Path(repository_root).resolve()
- lib/python/autonomous_planning_engine/decision_engine.py:145 — self.root = Path(repository_root).resolve()
- lib/python/autonomous_planning_engine/dependency_resolver.py:188 — self.root = Path(repository_root).resolve()
- lib/python/autonomous_planning_engine/dependency_resolver.py:246 — def resolve_entries(
- lib/python/autonomous_planning_engine/engine.py:100 — self.root = Path(repository).resolve()
- lib/python/autonomous_planning_engine/engine.py:102 — Path(workspace_root).resolve()
- lib/python/autonomous_planning_engine/engine.py:106 — self.output_dir = Path(output_dir).resolve() if output_dir else self.root
- lib/python/autonomous_planning_engine/execution_queue.py:21 — Dependencies are respected via DependencyResolver.resolve_entries().
- lib/python/autonomous_planning_engine/execution_queue.py:96 — # Resolve dependency order
- lib/python/autonomous_planning_engine/execution_queue.py:98 — resolved_dicts = self._resolver.resolve_entries(entry_dicts)
- lib/python/autonomous_planning_engine/persistence.py:37 — self.repository_root = Path(repository_root).resolve()
- lib/python/autonomous_workflow_engine.py:11 — ROOT = Path(".").resolve()
- lib/python/canonical_audit/engine.py:8 — self.root = Path(repository).resolve()
- lib/python/canonical_intelligence/engine.py:18 — self.root = Path(repository).resolve()
- lib/python/cli/engineering.py:7 — ROOT = Path(__file__).resolve().parents[3]
- lib/python/cli/main.py:721 — print(f"  Context JSON:   {paths.get('live_context', str(Path(repository).resolve() / '.ai' / 'context' / 'live_context.json'))}")
- lib/python/cli/main.py:722 — print(f"  Report:         {paths.get('markdown', str(Path(repository).resolve() / '.ai' / 'context' / 'AI_CTO_CONTEXT_REPORT.md'))}")
- lib/python/compliance_engine/engine.py:10 — self.root = Path(repository).resolve()
- lib/python/context_synchronization_engine/engine.py:97 — self.root = Path(repository_root).resolve()
- lib/python/context_synchronization_engine/engine.py:202 — self.root = Path(repository_root).resolve()
- lib/python/context_synchronization_engine/engine.py:226 — self.root = Path(repository_root).resolve()
- lib/python/context_synchronization_engine/engine.py:351 — self.root = Path(repository_root).resolve()
- lib/python/context_synchronization_engine/engine.py:352 — self.workspace_root = Path(workspace_root).resolve() if workspace_root else self.root.parent
- lib/python/context_synchronization_engine/engine.py:383 — self.root = Path(repository_root).resolve()
- lib/python/context_synchronization_engine/engine.py:385 — def resolve(
- lib/python/context_synchronization_engine/engine.py:734 — self.root = Path(repository_root).resolve()
- lib/python/context_synchronization_engine/engine.py:735 — self.workspace_root = Path(workspace_root).resolve() if workspace_root else self.root.parent
- lib/python/context_synchronization_engine/engine.py:744 — live_context = resolver.resolve(
- lib/python/context_synchronization_engine/engine.py:764 — live_context = resolver.resolve(
- lib/python/context_synchronization_engine/engine.py:1573 — self.repository = str(Path(repository).resolve())
- lib/python/context_synchronization_engine/engine.py:1574 — self.workspace_root = str(Path(workspace_root).resolve()) if workspace_root else str(Path(repository).resolve().parent)
- lib/python/context_synchronization_engine/persistence.py:10 — self.repository_root = Path(repository_root).resolve()
- lib/python/coverage_engine/engine.py:10 — self.root = Path(repository).resolve()
- lib/python/css_engine/engine.py:119 — self._root = Path(standards_root).resolve() if standards_root else None
- lib/python/dashboard/service.py:328 — self.repository_root = Path(repository_root).resolve()
- lib/python/dashboard/service.py:330 — Path(workspace_root).resolve()
- lib/python/dashboard/service.py:680 — Path(repo.repository_root).resolve() == self.repository_root
- lib/python/decision_engine.py:10 — ROOT = Path(".").resolve()
- lib/python/dependency_engine/engine.py:11 — self.root = Path(root).resolve()
- lib/python/development_state_engine/repository.py:24 — self.repository_root = Path(repository_root).resolve()
- lib/python/development_state_engine/repository.py:108 — export_path = (self.repository_root / export_path).resolve()
- lib/python/development_state_engine/repository.py:117 — source = (self.repository_root / source).resolve()
- lib/python/development_state_engine/runtime.py:81 — self.repository_root = Path(repository_root).resolve()
- lib/python/development_state_engine/runtime.py:224 — self.repository_root = Path(repository_root).resolve()
- lib/python/development_state_engine/runtime.py:640 — self.repository_root = Path(repository_root).resolve()
- lib/python/discovery_engine/engine.py:16 — self.root = Path(root).resolve()
- lib/python/drift_engine/engine.py:11 — self.root = Path(repository).resolve()
- lib/python/engineering_engine/dependency_graph.py:30 — resolved = self.resolver.resolve(imported)
- lib/python/engineering_engine/github_cli_client.py:13 — repository = GitHubRepositoryResolver().resolve()
- lib/python/engineering_engine/github_cli_state_provider.py:19 — repository = GitHubRepositoryResolver().resolve()
- lib/python/engineering_engine/github_issue_state_provider.py:25 — repository = GitHubRepositoryResolver().resolve()
- lib/python/engineering_engine/github_real_client.py:15 — repo = GitHubRepositoryResolver().resolve()
- lib/python/engineering_engine/github_repository_resolver.py:15 — def resolve(self) -> GitHubRepository:
- lib/python/engineering_engine/import_resolver.py:21 — def resolve(self, imported: str) -> str | None:
- lib/python/epistemic/transformation.py:597 — def resolve_reference(
- lib/python/epistemic/transformation.py:602 — Resolve a repository-relative manifestation when one exists locally.
- lib/python/epistemic/transformation.py:661 — resolved = self.resolve_reference(reference)
- lib/python/evidence_engine/engine.py:9 — self.root = Path(repository).resolve()
- lib/python/executable_repository_intelligence/engine.py:63 — self.root = Path(repository).resolve()
- lib/python/executive_briefing_engine/decision_tracker.py:66 — title="Resolve or de-prioritize blocked tasks",
- lib/python/executive_briefing_engine/engine.py:79 — self.root = Path(repository).resolve()
- lib/python/executive_briefing_engine/engine.py:80 — self.output_dir = Path(output_dir).resolve() if output_dir else self.root
- lib/python/executive_briefing_engine/persistence.py:33 — self.repository_root = Path(repository_root).resolve()
- lib/python/executive_briefing_engine/priority_engine.py:112 — title=f"Resolve {drift} canonical drift findings",
- lib/python/executive_briefing_engine/priority_engine.py:168 — title=f"Resolve current issue: {current_issue}",
- lib/python/executive_briefing_engine/recommendation_engine.py:109 — title="Resolve canonical drift findings",
- lib/python/executive_briefing_engine/recommendation_engine.py:213 — title=f"Resolve architecture risks ({len(arch_risks)} detected)",
- lib/python/executive_briefing_engine/risk_analyzer.py:88 — remediation="Review architecture graph and resolve identified structural issues.",
- lib/python/executive_briefing_engine/risk_analyzer.py:133 — remediation="Run canonical intelligence pipeline and resolve all drift findings.",
- lib/python/executive_briefing_engine/risk_analyzer.py:218 — remediation="Resolve broken dependencies to prevent runtime failures.",
- lib/python/executive_briefing_engine/risk_analyzer.py:246 — remediation="Investigate and resolve all integrity failures before proceeding.",
- lib/python/executive_briefing_engine/risk_analyzer.py:285 — remediation="Investigate failed execution jobs and resolve root causes.",
- lib/python/experience/deployment.py:35 — """Resolve the durable Experience store for this deployment.
- lib/python/foundation_audit/main.py:15 — ROOT = Path(".").resolve()
- lib/python/foundation_audit.py:10 — ROOT = Path(".").resolve()
- lib/python/knowledge_graph_engine.py:10 — ROOT = Path(".").resolve()

### read

- lib/python/ai_cto_scanner/detectors.py:128 — text = (Path(root) / wf.path).read_text(encoding="utf-8", errors="ignore")
- lib/python/ai_platform/adapters.py:377 — raw = response.read()
- lib/python/ai_platform/adapters.py:399 — error_raw = exc.read()
- lib/python/ai_platform/cognitive_coordination.py:47 — read_only: bool
- lib/python/ai_platform/cognitive_coordination.py:171 — "read",
- lib/python/ai_platform/cognitive_coordination.py:203 — read_only=True,
- lib/python/ai_platform/context_builder.py:22 — """Build bounded read-only orientation without repository profiling.
- lib/python/ai_platform/context_builder.py:65 — "read",
- lib/python/ai_platform/context_builder.py:142 — return json.loads(path.read_text(encoding="utf-8"))
- lib/python/ai_platform/sessions.py:46 — session = self._read(path)
- lib/python/ai_platform/sessions.py:53 — return self._read(path)
- lib/python/ai_platform/sessions.py:128 — def _read(self, path: Path) -> Dict[str, Any]:
- lib/python/ai_platform/sessions.py:132 — return json.loads(path.read_text(encoding="utf-8"))
- lib/python/ai_platform/settings.py:32 — payload = json.loads(self.path.read_text(encoding="utf-8"))
- lib/python/autonomous_execution_engine/engine.py:441 — evidence={"note": "State read-only in safe modes"})
- lib/python/autonomous_execution_engine/models.py:19 — MODE_READ_ONLY = "READ_ONLY"
- lib/python/autonomous_execution_engine/persistence.py:126 — return self._read("execution.json")
- lib/python/autonomous_execution_engine/persistence.py:130 — return self._read("execution_history.json")
- lib/python/autonomous_execution_engine/persistence.py:141 — history = self._read("execution_history.json")
- lib/python/autonomous_execution_engine/persistence.py:187 — def _read(self, filename: str) -> Dict[str, Any]:
- lib/python/autonomous_execution_engine/persistence.py:192 — return json.loads(path.read_text(encoding="utf-8"))
- lib/python/autonomous_execution_engine/policy.py:166 — Safe modes are always treated as APPROVED for read-only operations.
- lib/python/autonomous_execution_engine/rollback.py:86 — # Other stages are read-only — no rollback needed
- lib/python/autonomous_planning_engine/batch_planner.py:39 — content = md_file.read_text(encoding="utf-8", errors="replace")
- lib/python/autonomous_planning_engine/decision_engine.py:76 — head = py_file.read_text(encoding="utf-8", errors="replace")[:3000]
- lib/python/autonomous_planning_engine/decision_engine.py:113 — content = f.read_text(encoding="utf-8", errors="replace")
- lib/python/autonomous_planning_engine/decision_engine.py:121 — content = f.read_text(encoding="utf-8", errors="replace")
- lib/python/autonomous_planning_engine/dependency_resolver.py:37 — source = py_file.read_text(encoding="utf-8", errors="replace")
- lib/python/autonomous_planning_engine/dependency_resolver.py:69 — source = py_file.read_text(encoding="utf-8", errors="replace")
- lib/python/autonomous_planning_engine/dependency_resolver.py:236 — content = md_file.read_text(encoding="utf-8", errors="replace")
- lib/python/autonomous_planning_engine/persistence.py:87 — return self._read("planning.json")
- lib/python/autonomous_planning_engine/persistence.py:118 — def _read(self, filename: str) -> Dict[str, Any]:
- lib/python/autonomous_planning_engine/persistence.py:123 — return json.loads(path.read_text(encoding="utf-8"))
- lib/python/autonomous_workflow_engine.py:25 — decision = json.loads(decision_file.read_text())
- lib/python/canonical_parser/parser.py:16 — text = path.read_text(encoding="utf-8")
- lib/python/cdm_engine/engine.py:160 — text = p.read_text(encoding="utf-8")
- lib/python/cli/main.py:744 — mode = "READ_ONLY"
- lib/python/context_synchronization_engine/engine.py:305 — lines = path.read_text(encoding="utf-8").splitlines()
- lib/python/context_synchronization_engine/engine.py:344 — return json.loads(path.read_text(encoding="utf-8"))
- lib/python/context_synchronization_engine/engine.py:376 — return json.loads(path.read_text(encoding="utf-8"))
- lib/python/context_synchronization_engine/engine.py:1464 — return json.loads(path.read_text(encoding="utf-8"))
- lib/python/context_synchronization_engine/persistence.py:28 — return json.loads(path.read_text(encoding="utf-8"))
- lib/python/csl_engine/engine.py:190 — text = Path(path).read_text(encoding="utf-8")
- lib/python/css_engine/engine.py:129 — text = p.read_text(encoding="utf-8")
- lib/python/dashboard/service.py:192 — "Leverage existing runtime artifacts and keep the dashboard read-oriented for the MVP.",
- lib/python/dashboard/service.py:1205 — return json.loads(path.read_text(encoding="utf-8"))
- lib/python/decision_engine.py:26 — profile = json.loads(PROFILE.read_text(encoding="utf-8"))
- lib/python/decision_engine.py:40 — graph = json.loads(GRAPH.read_text(encoding="utf-8"))
- lib/python/decision_engine.py:46 — idx = json.loads(INDEX.read_text(encoding="utf-8"))
- lib/python/development_state_engine/repository.py:171 — return json.loads(path.read_text(encoding="utf-8"))
- lib/python/development_state_engine/runtime.py:186 — return json.loads(path.read_text(encoding="utf-8"))
- lib/python/development_state_engine/runtime.py:582 — payload = json.loads(self.repository.integrity_path.read_text(encoding="utf-8"))
- lib/python/development_validator/parser.py:7 — self.text = self.path.read_text(encoding="utf-8")
- lib/python/development_validator.py:27 — text = path.read_text(encoding="utf-8")
- lib/python/engineering_engine/compiler.py:50 — text = csl_file.read_text(encoding='utf-8')
- lib/python/engineering_engine/dependency_rule_engine.py:31 — for line in path.read_text(encoding="utf-8").splitlines():
- lib/python/engineering_engine/github_transaction_log.py:31 — path.read_text(encoding="utf-8")
- lib/python/engineering_engine/project_importer.py:26 — source.read_text(encoding="utf-8")
- lib/python/engineering_engine/repository_model.py:54 — tree = ast.parse(path.read_text(encoding="utf-8"))
- lib/python/engineering_workspace/capabilities.py:18 — READ_REPOSITORY = "repository.read"
- lib/python/engineering_workspace/capabilities.py:25 — READ_FILES = "filesystem.read"
- lib/python/engineering_workspace/capabilities.py:43 — GITHUB_READ = "github.read"
- lib/python/engineering_workspace/capabilities.py:51 — RAILWAY_READ = "railway.read"
- lib/python/engineering_workspace/capabilities.py:58 — RUNTIME_READ = "runtime.read"
- lib/python/engineering_workspace/capabilities.py:64 — KNOWLEDGE_READ = "knowledge.read"
- lib/python/engineering_workspace/capabilities.py:70 — CANONICAL_READ = "canonical.read"
- lib/python/epistemic/layered_memory.py:466 — path.read_text(encoding="utf-8")
- lib/python/epistemic/memory/store.py:76 — return Memory(**json.loads(file.read_text()))
- lib/python/epistemic/memory/store.py:87 — Memory(**json.loads(file.read_text()))
- lib/python/epistemic/provenance.py:1251 — text = path.read_text(encoding="utf-8")
- lib/python/epistemic/sedimentation.py:159 — """Durable Sedimentation representation could not be preserved or read."""
- lib/python/epistemic/sedimentation.py:276 — path.read_text(encoding="utf-8")
- lib/python/epistemic/transformation.py:468 — path.read_text(encoding="utf-8")
- lib/python/executable_repository_intelligence/injection_safety.py:10 — READ_ONLY          — Hook only reads state, does not mutate
- lib/python/executable_repository_intelligence/injection_safety.py:35 — # Evidence keywords suggesting read-only behaviour
- lib/python/executable_repository_intelligence/injection_safety.py:37 — "read_only", "readonly", "read only", "observe", "monitor", "listen",
- lib/python/executable_repository_intelligence/injection_safety.py:99 — # Check for read-only patterns
- lib/python/executable_repository_intelligence/injection_safety.py:105 — safety="READ_ONLY",
- lib/python/executable_repository_intelligence/models.py:56 — "READ_ONLY",
- lib/python/executable_repository_intelligence/runtime_map.py:63 — return (root / path_str).read_text(encoding="utf-8", errors="ignore")
- lib/python/executive_briefing_engine/engine.py:139 — synchronized = json.loads(path.read_text(encoding="utf-8"))
- lib/python/executive_briefing_engine/persistence.py:89 — return self._read(path)
- lib/python/executive_briefing_engine/persistence.py:119 — def _read(self, path: Path) -> Dict[str, Any]:
- lib/python/executive_briefing_engine/persistence.py:121 — return json.loads(path.read_text(encoding="utf-8"))
- lib/python/experience/coordination_journal.py:265 — self._path.read_text(encoding="utf-8")
- lib/python/experience/coordination_journal.py:269 — "cannot read durable coordination journal"
- lib/python/experience/operational_observability.py:33 — """Read-only operational condition derived from durable evidence."""
- lib/python/experience/operational_observability.py:67 — """Read durable PCC-01 coordination evidence without mutating it."""
- lib/python/experience/operational_observability.py:143 — """Read journal records through its durable representation.
- lib/python/experience/persistent_repository.py:137 — raw = self._path.read_text(encoding="utf-8")
- lib/python/experience/persistent_repository.py:140 — f"cannot read Experience store: {self._path}"
- lib/python/experience/protection_repository.py:159 — raw = self._path.read_text(encoding="utf-8")
- lib/python/experience/protection_repository.py:162 — f"cannot read Protection store: {self._path}"
- lib/python/foundation_audit/checks.py:159 — text = launcher.read_text(encoding="utf-8")
- lib/python/knowledge_graph_v2/engine.py:42 — file.read_text(encoding="utf-8")
- lib/python/memory_engine.py:25 — history = json.loads(HISTORY.read_text(encoding="utf-8"))
- lib/python/repository_engine/deps.py:38 — for raw in path.read_text(encoding="utf-8", errors="ignore").splitlines():
- lib/python/repository_engine/deps.py:49 — data = json.loads(path.read_text(encoding="utf-8"))
- lib/python/repository_engine/deps.py:61 — content = path.read_text(encoding="utf-8", errors="ignore")
- lib/python/repository_engine/deps.py:86 — for raw in path.read_text(encoding="utf-8", errors="ignore").splitlines():

### inspect

- lib/python/agents/ai_cto_scanner_agent.py:5 — Registered under the "inspect" name in the agent runtime.
- lib/python/agents/ai_cto_scanner_agent.py:22 — NAME = "inspect"
- lib/python/agents/development_agent.py:99 — lambda: RepositoryInspectorV2(repository, workspace_index=workspace_index).inspect(),
- lib/python/agents/repository_inspector_agent.py:9 — NAME = "inspect"
- lib/python/agents/repository_inspector_agent.py:15 — report = engine.inspect()
- lib/python/ai_cto_scanner/report.py:453 — "> *Reuse the 'ai inspect <path>' command to refresh this report after changes.*",
- lib/python/ai_platform/cognitive_coordination.py:172 — "inspect",
- lib/python/ai_platform/context_builder.py:66 — "inspect",
- lib/python/cli/main.py:177 — inspect_parser = sub.add_parser(
- lib/python/cli/main.py:178 — "inspect",
- lib/python/cli/main.py:181 — inspect_parser.add_argument(
- lib/python/cli/main.py:185 — help="Path to the repository to inspect (default: current directory)",
- lib/python/cli/main.py:187 — inspect_parser.add_argument(
- lib/python/cli/main.py:193 — inspect_parser.add_argument(
- lib/python/cli/main.py:199 — inspect_parser.add_argument(
- lib/python/cli/main.py:205 — inspect_parser.add_argument(
- lib/python/cli/main.py:524 — elif args.command == "inspect":
- lib/python/cli/main.py:572 — cmd_agent("inspect", repository=args.path, output_dir=args.output)
- lib/python/dashboard/service.py:153 — purpose="Inspect repositories and provide foundational engineering intelligence.",
- lib/python/dashboard/service.py:160 — related_tests=["tests/test_repository_engine_inspect.sh", "tests/test_repository_profile.sh"],
- lib/python/dashboard/service.py:161 — cli_commands=["python3 -m python.cli.main inspect .", "bin/ai inspect ."],
- lib/python/dashboard/service.py:651 — inspection = self._latest_json(self.repository_root / ".ai" / "reports", "inspect-*.json")
- lib/python/dashboard/service.py:789 — ("Repository Inspection", self._latest_json_path(self.repository_root / ".ai" / "reports", "inspect-*.json")),
- lib/python/engineering_workspace/capabilities.py:20 — INSPECT_REPOSITORY = "repository.inspect"
- lib/python/epistemic/transformation.py:635 — def inspect(
- lib/python/experience/service.py:27 — """Inspect an admitted Experience by stable identity."""
- lib/python/foundation_audit/checks.py:162 — "inspect",
- lib/python/planning_engine/engine.py:29 — title=f"Inspect {stats['files']} files",
- lib/python/project_profiles/trading_signals.py:18 — def inspect(self, repository):
- lib/python/repository_engine/cli.py:9 — def inspect(path="."):
- lib/python/repository_engine/cli.py:18 — report_path = output_dir / f"inspect-{stamp}.md"
- lib/python/repository_engine/cli.py:21 — profile_path = output_dir / f"inspect-{stamp}.json"
- lib/python/repository_engine/report.py:21 — lines.append("# Repository Inspect Report")
- lib/python/repository_inspector_v2/engine.py:21 — def inspect(self):
- lib/python/repository_inspector_v2/engine.py:58 — report = self.inspect()
- lib/python/repository_inventory.py:60 — "inspect",
- lib/python/runtime/bootstrap.py:247 — "bin/ai inspect .",
- lib/python/self_improvement_engine/analyzers.py:225 — "inventory", "dependencies", "validate", "inspect",
- lib/python/workspace_orchestrator/intelligence.py:439 — remediation="Run 'ai inspect --execution-model' on each repository and implement missing components.",
- lib/python/workspace_orchestrator/intelligence.py:573 — "Run 'ai inspect' on each and implement the recommended CORE specs."

### provenance

- lib/python/ai_platform/context_builder.py:58 — "provenance",
- lib/python/ai_platform/conversation_context.py:9 — - Provenance system;
- lib/python/ai_platform/conversation_context.py:197 — "provenance": {
- lib/python/ai_platform/conversation_context.py:225 — "provenance": organism_state.get("provenance", {}),
- lib/python/ai_platform/conversation_experience.py:9 — - another Provenance system;
- lib/python/ai_platform/conversation_experience.py:33 — from python.epistemic.provenance import Source
- lib/python/canonical_entities/models.py:106 — provenance: str = ""
- lib/python/cdm_engine/engine.py:15 — - provenance preservation
- lib/python/cdm_engine/engine.py:90 — provenance: str = ""
- lib/python/cdm_engine/engine.py:117 — "provenance": self.provenance,
- lib/python/cdm_engine/engine.py:232 — provenance=path,
- lib/python/context_synchronization_engine/engine.py:936 — provenance={
- lib/python/context_synchronization_engine/engine.py:976 — provenance={
- lib/python/context_synchronization_engine/engine.py:1008 — provenance={
- lib/python/context_synchronization_engine/engine.py:1037 — provenance={
- lib/python/context_synchronization_engine/engine.py:1067 — provenance=live_context.get("sources", {}),
- lib/python/context_synchronization_engine/engine.py:1099 — provenance={
- lib/python/context_synchronization_engine/engine.py:1144 — provenance={
- lib/python/context_synchronization_engine/engine.py:1178 — provenance={
- lib/python/context_synchronization_engine/engine.py:1215 — provenance={
- lib/python/context_synchronization_engine/engine.py:1245 — provenance={
- lib/python/context_synchronization_engine/engine.py:1417 — provenance: Mapping[str, Any],
- lib/python/context_synchronization_engine/engine.py:1428 — provenance=dict(self._sorted_mapping(provenance)),
- lib/python/context_synchronization_engine/models.py:108 — provenance: Optional[Dict[str, Any]] = None
- lib/python/context_synchronization_engine/models.py:122 — "provenance": _normalize_mapping(self.provenance or {}),
- lib/python/context_synchronization_engine/models.py:136 — provenance=dict(_normalize_mapping(data.get("provenance", {}))),
- lib/python/epistemic/layered_memory.py:11 — relationships and the existing SedimentedMemory provenance reference
- lib/python/epistemic/layered_memory.py:73 — They do not imply authority, truth, chronology, or provenance.
- lib/python/epistemic/layered_memory.py:75 — Provenance remains owned by the wrapped SedimentedMemory and by the
- lib/python/epistemic/layered_memory.py:123 — """Expose, but do not replace, PCC-04 provenance navigation."""
- lib/python/epistemic/layered_memory.py:311 — The second is the provenance identity already preserved by PCC-04.
- lib/python/epistemic/layered_memory.py:784 — It exposes only identifiers already preserved by Memory provenance.
- lib/python/epistemic/layered_memory.py:813 — "Provenance identifier must be textual."
- lib/python/epistemic/layered_memory.py:818 — "Provenance identifier cannot be empty."
- lib/python/epistemic/provenance.py:2 — PCC-03 — Provenance + Lineage.
- lib/python/epistemic/provenance.py:4 — This module implements the first executable anatomy of epistemic provenance.
- lib/python/epistemic/provenance.py:49 — """Raised when an invalid provenance relationship is requested."""
- lib/python/epistemic/provenance.py:208 — It is an explicit epistemic promotion whose provenance remains navigable
- lib/python/epistemic/provenance.py:209 — back through the Verification and the already-preserved provenance chain.
- lib/python/epistemic/provenance.py:253 — Existing provenance remains authoritative for the history leading to the
- lib/python/epistemic/provenance.py:324 — class Provenance:
- lib/python/epistemic/provenance.py:326 — In-memory executable provenance anatomy.
- lib/python/epistemic/provenance.py:527 — resulting Knowledge a stable identity inside this Provenance organ.
- lib/python/epistemic/provenance.py:589 — the inherited PCC-03 provenance anatomy supplies the remaining path.
- lib/python/epistemic/provenance.py:689 — Explain Current State backward through its explicit provenance.
- lib/python/epistemic/provenance.py:729 — Traverse explicit provenance from Source through Current State.
- lib/python/epistemic/provenance.py:980 — Traverse explicit PCC-03 provenance from Source through Knowledge.
- lib/python/epistemic/provenance.py:1033 — Persist this Provenance anatomy as one human-inspectable Markdown
- lib/python/epistemic/provenance.py:1044 — path = root / "PROVENANCE.md"
- lib/python/epistemic/provenance.py:1133 — "# Epistemic Provenance",
- lib/python/epistemic/provenance.py:1236 — def load(cls, root: Path) -> "Provenance":
- lib/python/epistemic/provenance.py:1238 — Recover persisted Provenance without inventing missing information.
- lib/python/epistemic/provenance.py:1244 — path = Path(root) / "PROVENANCE.md"
- lib/python/epistemic/provenance.py:1248 — f"Persisted Provenance does not exist: {path}"
- lib/python/epistemic/provenance.py:1258 — "Persisted Provenance missing machine-recoverable block"
- lib/python/epistemic/provenance.py:1265 — "Persisted Provenance has unterminated representation"
- lib/python/epistemic/provenance.py:1274 — "Persisted Provenance representation is malformed"
- lib/python/epistemic/provenance.py:1290 — "Persisted Provenance schema is incomplete or unknown"
- lib/python/epistemic/provenance.py:1293 — provenance = cls()
- lib/python/epistemic/provenance.py:1310 — provenance._sources,
- lib/python/epistemic/provenance.py:1318 — if item.source not in provenance._sources:
- lib/python/epistemic/provenance.py:1325 — provenance._observations,
- lib/python/epistemic/provenance.py:1333 — if item.observation not in provenance._observations:
- lib/python/epistemic/provenance.py:1340 — provenance._evidence,
- lib/python/epistemic/provenance.py:1348 — provenance._claims,
- lib/python/epistemic/provenance.py:1356 — if item.claim not in provenance._claims:
- lib/python/epistemic/provenance.py:1363 — provenance._verifications,
- lib/python/epistemic/provenance.py:1373 — not in provenance._verifications
- lib/python/epistemic/provenance.py:1381 — provenance._knowledge,
- lib/python/epistemic/provenance.py:1391 — not in provenance._knowledge
- lib/python/epistemic/provenance.py:1399 — provenance._current_states,
- lib/python/epistemic/provenance.py:1407 — if relation.evidence not in provenance._evidence:
- lib/python/epistemic/provenance.py:1413 — if relation.claim not in provenance._claims:
- lib/python/epistemic/provenance.py:1419 — if relation in provenance._evidence_relations:
- lib/python/epistemic/provenance.py:1424 — provenance._evidence_relations.append(relation)
- lib/python/epistemic/provenance.py:1428 — "Persisted Provenance entity is malformed"
- lib/python/epistemic/provenance.py:1431 — return provenance
- lib/python/epistemic/provenance.py:1466 — "Verification is not registered in this Provenance"
- lib/python/epistemic/sedimentation.py:7 — This organ does not own Experience, Transformation, Provenance, Memory,
- lib/python/epistemic/sedimentation.py:136 — Rejection preserves the proposal and its provenance rather than
- lib/python/epistemic/sedimentation.py:168 — It is not a Memory Store, Knowledge Engine, Provenance organ, Current State
- lib/python/epistemic/sedimentation.py:412 — from python.epistemic.provenance import Verification
- lib/python/epistemic/sedimented_memory.py:214 — "Sedimentation must preserve provenance before Memory."
- lib/python/experience/provenance_integration.py:1 — """Experience Provenance Integration for PCC-01.
- lib/python/experience/provenance_integration.py:3 — This organ connects Persistent Experience with provenance semantics already
- lib/python/experience/provenance_integration.py:6 — It does not replace Knowledge Graph provenance.
- lib/python/experience/provenance_integration.py:12 — Inherited provenance vocabulary:
- lib/python/experience/provenance_integration.py:13 — provenance
- lib/python/experience/provenance_integration.py:27 — """Raised when Experience provenance violates its physiology."""
- lib/python/experience/provenance_integration.py:51 — provenance: str
- lib/python/experience/provenance_integration.py:70 — "provenance",
- lib/python/experience/provenance_integration.py:72 — "provenance",
- lib/python/experience/provenance_integration.py:73 — self.provenance,
- lib/python/experience/provenance_integration.py:156 — provenance: str,
- lib/python/experience/provenance_integration.py:163 — """Observe provenance without mutating Core Experience."""
- lib/python/experience/provenance_integration.py:167 — provenance=provenance,
- lib/python/experience/provenance_integration.py:185 — "provenance": self.provenance,
- lib/python/experience/provenance_integration.py:209 — """Restore provenance while preserving Experience identity."""
- lib/python/experience/provenance_integration.py:238 — provenance=payload[
- lib/python/experience/provenance_integration.py:239 — "provenance"

### knowledge_graph

- lib/python/agents/development_agent.py:21 — from python.knowledge_graph_v2.engine import KnowledgeGraphEngine
- lib/python/agents/development_agent.py:112 — report["knowledge_graph"] = profiler.run(
- lib/python/agents/development_agent.py:113 — "KnowledgeGraph",
- lib/python/agents/development_agent.py:114 — lambda: KnowledgeGraphEngine(repository, workspace_index=workspace_index).build(),
- lib/python/agents/development_report.py:21 — report.append(f"Knowledge graph nodes: {len(result['knowledge_graph']['nodes'])}")
- lib/python/ai_cto_scanner/engine.py:18 — from python.knowledge_graph import CanonicalKnowledgeGraphBuilder
- lib/python/ai_cto_scanner/engine.py:148 — graph = CanonicalKnowledgeGraphBuilder().build(canonical_repo)
- lib/python/ai_cto_scanner/report.py:100 — "**Knowledge graph nodes:** %d" % canonical.get("graph_nodes", 0),
- lib/python/ai_platform/context_builder.py:56 — "knowledge_graph",
- lib/python/autonomous_workflow_engine.py:41 — "engine": "Knowledge Graph",
- lib/python/canonical_intelligence/engine.py:9 — from python.knowledge_graph import CanonicalKnowledgeGraphBuilder
- lib/python/canonical_intelligence/engine.py:32 — graph = CanonicalKnowledgeGraphBuilder().build(canonical_repo)
- lib/python/context_synchronization_engine/engine.py:1159 — "knowledge_graph": self._load_json(self.root / ".ai" / "knowledge" / "graph.json"),
- lib/python/dashboard/service.py:263 — next_milestone="CDM Engine feeding the Knowledge Graph automatically.",
- lib/python/dashboard/service.py:298 — description="Materializes CDM documents and CSS standards into Knowledge Objects, Knowledge Relationships, a Knowledge Graph, a Dependency Graph, and a Traceability Graph.",
- lib/python/dashboard/service.py:299 — architecture="Consumes CDM Engine and CSS Engine outputs and builds a CanonicalKnowledgeGraph with full node and edge materialization.",
- lib/python/dashboard/service.py:301 — outputs=["MaterializedKnowledge with knowledge_graph, dependency_graph, traceability_graph"],
- lib/python/dashboard/service.py:302 — dependencies=["cdm-engine", "css-engine", "knowledge_graph", "canonical_entities"],
- lib/python/dashboard/service.py:303 — related_paths=["lib/python/knowledge_materialization", "lib/python/knowledge_graph"],
- lib/python/dashboard/service.py:309 — next_milestone="Repository Intelligence consuming the Knowledge Graph instead of file scanning.",
- lib/python/dashboard/service.py:310 — engineering_decisions=["Build on existing CanonicalKnowledgeGraph rather than introduce a new graph library."],
- lib/python/decision_engine.py:16 — GRAPH = MEMORY / "knowledge_graph.json"
- lib/python/engineering_engine/knowledge_graph.py:11 — class KnowledgeGraph:
- lib/python/engineering_engine/knowledge_graph.py:24 — class KnowledgeGraphBuilder:
- lib/python/engineering_engine/knowledge_graph.py:29 — ) -> KnowledgeGraph:
- lib/python/engineering_engine/knowledge_graph.py:31 — graph = KnowledgeGraph()
- lib/python/engineering_engine/package_builder.py:13 — from lib.python.engineering_engine.knowledge_graph import (
- lib/python/engineering_engine/package_builder.py:14 — KnowledgeGraphBuilder,
- lib/python/engineering_engine/package_builder.py:52 — graph = KnowledgeGraphBuilder().build(knowledge)
- lib/python/engineering_engine/planning_engine.py:34 — ('Add AST, semantic analysis, and UEM', 'CRITICAL', 'HIGH', 'Introduce first-class AST, semantic analyzer, and Universal Engineering Model subsystems.', ['lib/python/canonical_entities', 'lib/python/knowledge_graph', 'lib/python/knowledge_graph_v2', 'lib/python/canonical_intelligence']),
- lib/python/engineering_engine/repository_audit.py:103 — "path": "lib/python/{knowledge_graph,knowledge_graph_v2,canonical_intelligence,semantic_matching}",
- lib/python/engineering_engine/repository_audit.py:212 — md.write('- Compiler/intelligence layer: canonical_*, engineering_engine, planning_engine, validation_engine, knowledge_graph*\n')
- lib/python/engineering_engine/review_engine.py:8 — from lib.python.engineering_engine.knowledge_graph import (
- lib/python/engineering_engine/review_engine.py:9 — KnowledgeGraphBuilder,
- lib/python/engineering_engine/review_engine.py:33 — knowledge_graph = KnowledgeGraphBuilder().build(knowledge)
- lib/python/engineering_engine/review_engine.py:37 — # KnowledgeGraph is created here so future migrations can
- lib/python/engineering_engine/review_engine.py:42 — _ = knowledge_graph
- lib/python/engineering_engine/scope_detector.py:3 — from lib.python.engineering_engine.knowledge_graph import (
- lib/python/engineering_engine/scope_detector.py:4 — KnowledgeGraph,
- lib/python/engineering_engine/scope_detector.py:15 — graph: KnowledgeGraph,
- lib/python/engineering_engine/semantic_extractor.py:3 — from lib.python.engineering_engine.knowledge_graph import KnowledgeGraph
- lib/python/engineering_engine/semantic_extractor.py:15 — graph: KnowledgeGraph,
- lib/python/engineering_engine/semantic_repository_builder.py:8 — from lib.python.engineering_engine.knowledge_graph import (
- lib/python/engineering_engine/semantic_repository_builder.py:9 — KnowledgeGraphBuilder,
- lib/python/engineering_engine/semantic_repository_builder.py:31 — graph = KnowledgeGraphBuilder().build(knowledge)
- lib/python/experience/provenance_integration.py:6 — It does not replace Knowledge Graph provenance.
- lib/python/knowledge_graph/__init__.py:1 — from .builder import CanonicalKnowledgeGraphBuilder
- lib/python/knowledge_graph/__init__.py:2 — from .graph import CanonicalKnowledgeGraph
- lib/python/knowledge_graph/__init__.py:4 — __all__ = ["CanonicalKnowledgeGraph", "CanonicalKnowledgeGraphBuilder"]
- lib/python/knowledge_graph/builder.py:4 — from python.knowledge_graph.graph import CanonicalKnowledgeGraph
- lib/python/knowledge_graph/builder.py:7 — class CanonicalKnowledgeGraphBuilder:
- lib/python/knowledge_graph/builder.py:8 — """Build canonical knowledge graph from a CanonicalRepository."""
- lib/python/knowledge_graph/builder.py:18 — graph = CanonicalKnowledgeGraph()
- lib/python/knowledge_graph/graph.py:4 — class CanonicalKnowledgeGraph:
- lib/python/knowledge_graph_engine.py:49 — OUT = ROOT / ".ai" / "memory" / "knowledge_graph.json"
- lib/python/knowledge_graph_engine.py:57 — print("Knowledge Graph Engine")
- lib/python/knowledge_graph_v2/__init__.py:2 — Knowledge Graph Engine v2
- lib/python/knowledge_graph_v2/engine.py:6 — class KnowledgeGraphEngine:
- lib/python/knowledge_materialization/engine.py:5 — knowledge: Knowledge Objects, Knowledge Relationships, Knowledge Graph,
- lib/python/knowledge_materialization/engine.py:22 — from python.knowledge_graph.graph import CanonicalKnowledgeGraph
- lib/python/knowledge_materialization/engine.py:76 — - knowledge_graph: navigable canonical graph
- lib/python/knowledge_materialization/engine.py:83 — knowledge_graph: Optional[CanonicalKnowledgeGraph] = None
- lib/python/knowledge_materialization/engine.py:88 — graph_dict = self.knowledge_graph.to_dict() if self.knowledge_graph else {}
- lib/python/knowledge_materialization/engine.py:92 — "knowledge_graph": graph_dict,
- lib/python/knowledge_materialization/engine.py:98 — "graph_nodes": self.knowledge_graph.node_count() if self.knowledge_graph else 0,
- lib/python/knowledge_materialization/engine.py:99 — "graph_edges": self.knowledge_graph.edge_count() if self.knowledge_graph else 0,
- lib/python/knowledge_materialization/engine.py:116 — full Knowledge Graph, Dependency Graph, and Traceability Graph.
- lib/python/knowledge_materialization/engine.py:135 — graph = CanonicalKnowledgeGraph()
- lib/python/knowledge_materialization/engine.py:284 — knowledge_graph=graph,
- lib/python/recommendation_engine/engine.py:25 — if len(report["knowledge_graph"]["edges"]) < 100:
- lib/python/recommendation_engine/engine.py:29 — "reason": "Knowledge graph is still small.",
- lib/python/self_improvement_engine/analyzers.py:70 — "knowledge_graph_engine",
- lib/python/semantic_repository_intelligence/architecture_graph.py:44 — ("path_contains", "knowledge_graph"),

### repository_engine

- lib/python/agents/development_agent.py:14 — from python.repository_engine.engine import RepositoryEngine
- lib/python/agents/development_agent.py:78 — "RepositoryEngine",
- lib/python/agents/development_agent.py:79 — lambda: RepositoryEngine(repository, workspace_index=workspace_index).statistics(),
- lib/python/ai_control_center/providers/local_repository.py:6 — Canonical adapter over RepositoryEngine.
- lib/python/ai_control_center/providers/local_repository.py:14 — from repository_engine import RepositoryEngine
- lib/python/ai_control_center/providers/local_repository.py:25 — self._engine = RepositoryEngine(str(self._root))
- lib/python/ai_cto_scanner/engine.py:21 — from python.semantic_repository_intelligence import SemanticRepositoryEngine
- lib/python/ai_cto_scanner/engine.py:121 — semantic_engine = SemanticRepositoryEngine(
- lib/python/ai_platform/context_builder.py:12 — from python.repository_engine.engine import RepositoryEngine
- lib/python/ai_platform/context_builder.py:13 — from python.repository_engine.serializer import RepositoryProfileSerializer
- lib/python/ai_platform/context_builder.py:102 — profile = RepositoryProfileSerializer.to_dict(RepositoryEngine(self.repository_root).profile())
- lib/python/autonomous_execution_engine/validator.py:66 — SemanticRepositoryEngine,
- lib/python/autonomous_execution_engine/validator.py:68 — engine = SemanticRepositoryEngine(repository=self.repository, persist=False)
- lib/python/cli/main.py:19 — from python.repository_engine.engine import RepositoryEngine
- lib/python/cli/main.py:28 — RepositoryEngine(".").statistics(),
- lib/python/cli/main.py:528 — from python.executable_repository_intelligence import ExecutableRepositoryEngine
- lib/python/cli/main.py:530 — engine = ExecutableRepositoryEngine(repository=args.path, persist=persist)
- lib/python/cli/main.py:551 — from python.semantic_repository_intelligence import SemanticRepositoryEngine
- lib/python/cli/main.py:552 — engine = SemanticRepositoryEngine(repository=args.path, persist=False)
- lib/python/context_synchronization_engine/engine.py:930 — loader="GitContextProvider + RepositoryEngine",
- lib/python/dashboard/service.py:15 — from python.repository_engine.engine import RepositoryEngine
- lib/python/dashboard/service.py:16 — from python.repository_engine.serializer import RepositoryProfileSerializer
- lib/python/dashboard/service.py:134 — related_paths=["lib/python/dashboard", "lib/python/repository_engine", "lib/python/workspace_orchestrator"],
- lib/python/dashboard/service.py:155 — architecture="Uses RepositoryEngine plus existing inspection artifacts instead of duplicating scan logic.",
- lib/python/dashboard/service.py:159 — related_paths=["lib/python/repository_engine", ".ai/reports"],
- lib/python/dashboard/service.py:160 — related_tests=["tests/test_repository_engine_inspect.sh", "tests/test_repository_profile.sh"],
- lib/python/dashboard/service.py:170 — why_architecture="RepositoryEngine already computes the required profile and health information.",
- lib/python/dashboard/service.py:653 — profile = RepositoryEngine(self.repository_root).profile()
- lib/python/development_state_engine/runtime.py:18 — from python.repository_engine.engine import RepositoryEngine
- lib/python/development_state_engine/runtime.py:19 — from python.semantic_repository_intelligence import SemanticPersistence, SemanticRepositoryEngine
- lib/python/development_state_engine/runtime.py:218 — repository_engine_class=RepositoryEngine,
- lib/python/development_state_engine/runtime.py:220 — semantic_engine_class=SemanticRepositoryEngine,
- lib/python/development_state_engine/runtime.py:227 — self.repository_engine_class = repository_engine_class
- lib/python/development_state_engine/runtime.py:457 — engine = self.repository_engine_class(root=str(self.repository_root))
- lib/python/engineering_engine/repository_audit.py:119 — "path": "lib/python/{semantic_repository_intelligence,executable_repository_intelligence,repository_engine,repository_inspector_v2}",
- lib/python/executable_repository_intelligence/__init__.py:7 — Builds on top of CORE-008B (SemanticRepositoryEngine) without duplication.
- lib/python/executable_repository_intelligence/__init__.py:11 — from python.executable_repository_intelligence import ExecutableRepositoryEngine
- lib/python/executable_repository_intelligence/__init__.py:12 — result = ExecutableRepositoryEngine(repository="/path").analyze()
- lib/python/executable_repository_intelligence/__init__.py:15 — from .engine import ExecutableRepositoryEngine
- lib/python/executable_repository_intelligence/__init__.py:26 — "ExecutableRepositoryEngine",
- lib/python/executable_repository_intelligence/engine.py:6 — SemanticRepositoryEngine (CORE-008B)
- lib/python/executable_repository_intelligence/engine.py:18 — SemanticRepositoryEngine output.
- lib/python/executable_repository_intelligence/engine.py:26 — from python.semantic_repository_intelligence import SemanticRepositoryEngine
- lib/python/executable_repository_intelligence/engine.py:41 — class ExecutableRepositoryEngine:
- lib/python/executable_repository_intelligence/engine.py:50 — engine = ExecutableRepositoryEngine(repository="/path/to/repo")
- lib/python/executable_repository_intelligence/engine.py:75 — Calls CORE-008B SemanticRepositoryEngine first, then builds the
- lib/python/executable_repository_intelligence/engine.py:79 — semantic_engine = SemanticRepositoryEngine(
- lib/python/executable_repository_intelligence/models.py:283 — """Full result produced by the ExecutableRepositoryEngine."""
- lib/python/planning_engine/engine.py:5 — from python.repository_engine.engine import RepositoryEngine
- lib/python/planning_engine/engine.py:14 — self.repository = RepositoryEngine(root, workspace_index=workspace_index)
- lib/python/repository_engine/__init__.py:6 — from .engine import RepositoryEngine
- lib/python/repository_engine/__init__.py:10 — "RepositoryEngine",
- lib/python/repository_engine/cli.py:4 — from .engine import RepositoryEngine
- lib/python/repository_engine/cli.py:11 — profile = RepositoryEngine(root).profile()
- lib/python/repository_engine/engine.py:13 — class RepositoryEngine:
- lib/python/repository_inspector_v2/engine.py:6 — from python.repository_engine.engine import RepositoryEngine
- lib/python/repository_inspector_v2/engine.py:16 — self.repository = RepositoryEngine(root, workspace_index=workspace_index)
- lib/python/runtime/bootstrap.py:269 — "repository": "python.repository_engine.engine:RepositoryEngine",
- lib/python/self_evaluation_engine/analyzers.py:102 — SemanticRepositoryEngine,
- lib/python/self_evaluation_engine/analyzers.py:104 — engine = SemanticRepositoryEngine(repository=self.repository, persist=False)
- lib/python/semantic_repository_intelligence/__init__.py:9 — from python.semantic_repository_intelligence import SemanticRepositoryEngine
- lib/python/semantic_repository_intelligence/__init__.py:10 — result = SemanticRepositoryEngine(repository="/path").analyze()
- lib/python/semantic_repository_intelligence/__init__.py:13 — from .engine import SemanticRepositoryEngine
- lib/python/semantic_repository_intelligence/__init__.py:26 — "SemanticRepositoryEngine",
- lib/python/semantic_repository_intelligence/engine.py:49 — class SemanticRepositoryEngine:
- lib/python/semantic_repository_intelligence/engine.py:59 — engine = SemanticRepositoryEngine(repository="/path/to/repo")

## Architectural Questions To Resolve From Evidence

1. Which existing organ legitimately owns repository search?

2. Which existing organ resolves a semantic result to a concrete repository object?

3. Which existing organ performs bounded read access?

4. Which existing organ exposes structural inspection without mutation?

5. What provenance is emitted by each real operation?

6. Which operations are already read-only by contract?

7. Which capability names in NavigationPlan correspond to real existing APIs?

8. Which planned capability has no legitimate implementation organ yet?

## Safety Boundary

This characterization does not authorize:

- repository retrieval implementation;
- Working Context materialization;
- Journey traversal mutation;
- production adapters;
- guessed convenience APIs;
- CSL mutation;
- UEM mutation;
- Canon mutation.

## Navigation Plan Status

PRESERVED.

## Retrieval Status

NOT IMPLEMENTED.

## Working Context Status

NOT IMPLEMENTED.

## Journey Traversal Status

NOT STARTED.

## Human Authority

PRESERVED.

## Next Authorized Stage

DIRECT AUDIT OF THIS CHARACTERIZATION.

Only after the real search / resolve / read / inspect contracts are identified may the exact first read-only navigation production mutation be authorized.

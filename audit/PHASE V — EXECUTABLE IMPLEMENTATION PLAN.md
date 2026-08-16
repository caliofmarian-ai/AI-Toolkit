PHASE V — EXECUTABLE IMPLEMENTATION PLAN

A. Repository Authority & Baseline

Phase V is grounded in the inspected caliofmarian-ai/AI-Toolkit anatomy on the FUSION-01 continuation line, including the runtime organism boundary commit 629876db0a1207c79b75996e53e9c4fddb89093d (fusion: connect runtime to epistemic organism). That commit attaches EpistemicOrganismAccess to RuntimeBootstrap and explicitly preserves it as a controlled access boundary rather than a second organism.

The implementation baseline that matters for Phase V is:

AIPlatformService
 ├── AIContextBuilder
 ├── AISessionEngine
 ├── ProviderRegistry
 ├── ModelManager
 └── AIRequestPipeline
        ↓
 AIContextBuilder.build()
        ↓
 repository/engineering context materialization
        ↓
 ProviderAdapter.complete(question, context, model)

AIPlatformService.ask_repository() currently invokes the pipeline before session persistence. For a new session it then copies repository_profile and the complete returned context into session storage.

AISessionEngine persists JSON under .ai/ai_sessions and currently owns conversation history, prompt history, token usage, repository_profile, and engineering_context.

ProviderRegistry already exposes provider/model capabilities and per-model token_limits; therefore provider-budget discovery does not require a new provider registry.

The builtin provider anatomy currently uses StaticProviderAdapter. Its complete() consumes question + context + model, reads repository_profile, and synthesizes an answer locally. This is important characterization evidence: implementation must not confuse this test/static physiology with successful invocation of a real provider.

The 295 KB / 82K–110K / OpenAI 429 measurements remain baseline Evidence, not future constants.


---

B. Existing Implementation Anatomy

The implementation plan is anchored to these existing bodies.

Anatomy	Existing responsibility	Phase V disposition

lib/python/ai_platform/service.py / AIPlatformService	composition + request/session façade	ADAPT late
lib/python/ai_platform/pipeline.py / AIRequestPipeline	context → provider request	primary integration seam
lib/python/ai_platform/context_builder.py / AIContextBuilder	pre-request engineering/repository snapshot	characterize, then separate responsibility
lib/python/ai_platform/adapters.py	provider descriptors/adapters	budget + provider-boundary adaptation
lib/python/ai_platform/registry.py	provider registration/capabilities	REUSE
lib/python/ai_platform/sessions.py	persistent AI sessions	ADAPT at T14
lib/python/runtime/organism.py / EpistemicOrganismAccess	read-oriented FUSION runtime boundary	REUSE; do not turn into coordinator
CSL lexer/parser/analyzer/UEM	semantic identity/orientation	REUSE
CanonicalRepository	Canon resolution	REUSE
Knowledge materialization/graph	structural epistemic representation	REUSE
RepositoryEngine	repository perception/profile	REUSE selectively
RepositoryProfileSerializer	repository profile serialization	REUSE only when explicitly needed
PCC Provenance	provenance physiology	REUSE
LayeredMemory / repository	memory traversal	REUSE
JsonFileExperienceRepository	Persistent Experience	REUSE
Sedimentation	authority boundary	REUSE


FUSION already exposes Persistent Experience, Layered Memory, Sedimentation and Provenance as runtime-reachable physiology while explicitly refusing to invent missing persistence contracts.

This is important: Phase V introduces coordination contracts around existing organs, not replacements inside them.


---

C. Error Memory Constraints

The FUSION implementation history demonstrates several failure classes that become engineering constraints.

The inspected FUSION commit shows that runtime reconstruction had to be placed behind a bounded thread/wait because ContextSynchronizationEngine.synchronize() could stall bootstrap. It also introduced reuse of already reconstructed engineering context to prevent duplicate synchronous reconstruction inside the dashboard.

EpistemicOrganismAccess itself explicitly identifies the PCC-04 import-topology recovery report as demonstrated Error Memory evidence and refuses to fabricate a dedicated ErrorMemory service merely because such evidence exists.

Therefore the implementation must prevent recurrence of:

1. import topology failures — every stage gets static import/compile validation before tests;


2. duplicate expensive reconstruction — one request may not reconstruct the same large context through multiple paths;


3. unbounded synchronization/bootstrap waits — cognitive retrieval cannot become a new indefinite runtime blocker;


4. fragmented Termux mutations — Bash must be self-contained and fail closed;


5. partial Python surgery producing syntax/indentation errors — mutation is followed immediately by compile/static validation;


6. successful tests masking wrong integration anatomy — each stage gets structural acceptance assertions, not merely green generic tests;


7. failure evidence being confused with Error Memory authority — a failure report is Evidence until the existing Error Memory contract legitimately accepts it;


8. silent provider substitution — a real provider failure cannot be presented as success from StaticProviderAdapter.



Future Bash rule:

execution error
    ↓
preserve repository state
    ↓
generate implementation/error report
    ↓
record Error Memory only if existing Error Memory contract qualifies it
    ↓
no automatic promotion to Canon / Experience / authority


---

D. Invariant Enforcement Matrix

Invariant	Current enforcement	Missing	Introduced/proven	Test stage

I-01 Knowledge ≠ Working Context	implicit	provider path conflates them	T3/T9	T9
I-02 Retrieval ≠ Authority	FUSION/Sedimentation	cross-organ transport	T4	T4/T6
I-03 Identity ≠ Location	resolver anatomy implicit	federation contract	T5	T5
I-04 Provider mediated	partial pipeline mediation	capability bypass prevention	T6/T11	T11
I-05 Navigation read-only	FUSION explicitly read-oriented	all cognitive capabilities	T6	T6
I-06 Provenance survives	PCC	cross-organ envelope	T4	T4/T13
I-07 UNKNOWN valid	FUSION explicitly uses UNKNOWN	cognitive loop	T5/T8	T8
I-08 Budget doesn't delete knowledge	absent	complete	T10	T10
I-09 Human Authority preserved	FUSION/Sedimentation	loop enforcement	T6/T8	T15
I-10 Full profile not default	currently violated conceptually	complete	T12	T12
I-11 Class survives transport	implicit PCC semantics	envelope enforcement	T4	T4


FUSION already explicitly exposes human_authority.preserved=True, prevents automatic acceptance/rejection, and declares runtime mutation restrictions.


---

E. T1 Characterization Baseline

1. PURPOSE. Freeze the current physiology before changing it. No new cognitive capability; T1 creates executable evidence describing exactly what the current request does.

2. CURRENT ANATOMY. Inspect service.py::AIPlatformService.ask_repository, pipeline.py::AIRequestPipeline.run, context_builder.py::AIContextBuilder.build, provider adapter complete, session creation/persistence, RepositoryEngine/profile serializer path and existing AI-platform tests.

3. REUSE. Existing request pipeline, context builder, RepositoryEngine, serializer, provider registry and sessions unchanged.

4. CONNECT. None in production.

5. ADAPT. None in production.

6. NEW. Characterization test/report instrumentation only where existing tests cannot expose serialized-size/contribution measurements. No production abstraction.

7. FILE IMPACT. Inspect all AI-platform files above plus relevant repository-engine tests. Modify only existing test anatomy and, if necessary, test fixtures/helpers. Create a Phase-V/T1 implementation report. Explicitly do not modify CSL, Canon, runtime organism, Knowledge Graph, Memory, Provenance or production request behavior.

8. CONTRACT CHANGE. None. Current behavior becomes measured and asserted.

9. INVARIANTS. Establish evidence for I-01 and I-10 violations/risk; verify I-09 remains intact.

10. TEST PLAN. Extend the closest existing AI-platform/context tests to capture: context keys, serialized byte size, repository_profile presence, contribution sizes, adapter input and session snapshot behavior. Add focused characterization test only if no existing file legitimately owns this.

11. ACCEPTANCE GATE. Reproducible measurement proves where full profile enters the request, how much each major context branch contributes, what adapter receives, and what session persists.

12. FAILURE GATE. STOP if current repository behavior differs materially from Phase IV assumptions, if the 429 path cannot be located, or if tests cannot distinguish context construction from provider serialization.

13. ROLLBACK/CONSERVATION. Production unchanged. Only test/report commit is conserved.

14. ERROR MEMORY. Prevent import/syntax/measurement ambiguity. Any newly demonstrated pipeline failure gets preserved in report before qualification for Error Memory.

15. REPORT. work/implementation-reports/.../PHASE_V_T1_CHARACTERIZATION_BASELINE.md under the repository's established implementation-report hierarchy, with HEAD, branch, measurements, test commands, diffs, failures and acceptance verdict.


---

F. T2 Provider Budget Introspection

1. PURPOSE. Make provider/model capacity queryable before payload materialization.

2. CURRENT ANATOMY. ProviderDescriptor.token_limit, model dictionaries in builtin_adapters(), ProviderRegistry.list_providers(), ModelManager, pipeline model selection. The registry already returns per-model token limits.

3. REUSE. ProviderDescriptor, ProviderRegistry, ModelManager.

4. CONNECT. Selected provider/model → existing limit metadata.

5. ADAPT. Pipeline/model-selection interface only if current selection cannot expose resolved provider capacity before context serialization.

6. NEW. Only a minimal provider-budget view/value contract if no existing return structure can express resolved capacity plus reserved portions. No second registry.

7. FILE IMPACT. Inspect/possibly adapt ai_platform/registry.py, model_manager.py, pipeline.py; extend their existing tests. Do not modify adapters' provider catalog semantics unless characterization proves metadata inconsistency.

8. CONTRACT CHANGE. Before: provider capacity is descriptive metadata. After: selected provider/model capacity is available as request-governance input.

9. INVARIANTS. I-08.

10. TEST PLAN. Existing registry/model tests must prove exact model-specific limit selection and UNKNOWN/fail-closed behavior for missing limits.

11. ACCEPTANCE GATE. Pipeline can obtain provider/model capacity without constructing RepositoryProfile.

12. FAILURE GATE. Missing/ambiguous model capacity cannot silently assume an unlimited budget.

13. CONSERVATION. Existing provider configuration remains compatible.

14. ERROR MEMORY. Record provider-metadata contradictions if discovered.

15. REPORT. T2 report with provider/model matrix, resolved limits and regression results.


---

G. T3 Permanent Orientation

1. PURPOSE. Give AI a bounded semantic map before research.

2. CURRENT ANATOMY. CSL lexer/parser/analyzer/UEM, active project/runtime/session information, FUSION authority state.

3. REUSE. CSL/UEM semantic structures; FUSION Human Authority state; active workspace/session identities.

4. CONNECT. Existing semantic identity/authority metadata → orientation materialization.

5. ADAPT. AI context responsibility: orientation must become separately callable from legacy context building.

6. NEW. Minimal Permanent Orientation representation/assembler only because no inspected current object represents the cross-domain, bounded provider-facing orientation.

7. FILE IMPACT. Inspect CSL/UEM implementation and existing tests before naming any new production file. Adapt AI context layer only after exact ownership is established. Do not modify CSL grammar or Canon.

8. CONTRACT CHANGE. Before: context builder provides knowledge snapshot. After: a distinct bounded orientation can be produced without repository-wide materialization.

9. INVARIANTS. I-01, I-03, I-09, I-10.

10. TEST PLAN. CSL/UEM tests remain regression-only; AI context tests prove orientation contains identities/classes/capabilities/authority but not organ contents.

11. ACCEPTANCE GATE. Orientation creation does not invoke full RepositoryEngine.profile and size remains independent of repository corpus size within the fixture.

12. FAILURE GATE. STOP if orientation requires embedding Canon/Memory/repository bodies.

13. CONSERVATION. Legacy context path remains untouched for provider requests.

14. ERROR MEMORY. Prevent duplicate context reconstruction and semantic/path conflation.

15. REPORT. T3 orientation fields, provenance of each field, byte measurement and proof of excluded bulk data.


---

H. T4 Epistemic Result Envelope

1. PURPOSE. Permit heterogeneous organ results to cross coordination boundaries without losing identity/class/provenance/authority.

2. CURRENT ANATOMY. PCC Provenance, UEM semantic results, Canon identities, Repository observations, LayeredMemory nodes, Experience identities.

3. REUSE. All native result objects remain owners of semantics.

4. CONNECT. Native result → transport envelope.

5. ADAPT. None of the organs should be rewritten.

6. NEW. Minimal transversal result envelope is justified: no single existing object legitimately represents all organ classes without converting their semantics.

7. FILE IMPACT. Inspect PCC/UEM/Evidence contracts first; new file location must follow whichever existing epistemic contract package owns cross-organ types. No speculative parallel models hierarchy. No CSL/Canon modification.

8. CONTRACT CHANGE. Retrieval gains a common transport boundary but does not gain authority.

9. INVARIANTS. I-02, I-06, I-07, I-09, I-11.

10. TEST PLAN. Round-trip examples for Canon, Observation/Evidence, Memory and Experience; class and authority must remain identical.

11. ACCEPTANCE GATE. Four heterogeneous organ results survive transport with identity/source/provenance/class intact.

12. FAILURE GATE. Any implicit promotion (MEMORY→EVIDENCE, etc.) stops stage.

13. CONSERVATION. Native organ objects unchanged.

14. ERROR MEMORY. New class: epistemic transport/classification loss.

15. REPORT. Mapping of every tested native object into envelope and back/reference semantics.


---

I. T5 Federated Resolution

1. PURPOSE. Resolve semantic identity through the organ that already owns it.

2. CURRENT ANATOMY. CanonicalRepository, UEM, KnowledgeGraph, RepositoryEngine, LayeredMemory IDs, Experience IDs, Provenance identities.

3. REUSE. Local resolvers.

4. CONNECT. Domain discrimination → delegated resolver.

5. ADAPT. Existing resolver adapters only if necessary to expose bounded common outcomes.

6. NEW. Minimal federation coordinator; justified because no existing organ should own routing between all other organs.

7. FILE IMPACT. Inspect exact resolver method signatures before selecting production location. Do not create mega-index/storage.

8. CONTRACT CHANGE. semantic identity can yield RESOLVED/UNRESOLVED/AMBIGUOUS/FORBIDDEN and native-compatible stale semantics.

9. INVARIANTS. I-02, I-03, I-07, I-11.

10. TEST PLAN. At least CSL/UEM, Canon, Repository, Memory and Experience resolution paths plus ambiguity/unresolved.

11. ACCEPTANCE GATE. No physical path required by caller; correct native resolver demonstrably invoked.

12. FAILURE GATE. Fabricated resolution or fallback to filesystem guessing.

13. CONSERVATION. Existing resolvers remain independently usable.

14. ERROR MEMORY. Record resolver ambiguity/stale-manifestation defects.

15. REPORT. Resolver routing matrix and exact outcomes.


---

J. T6 Read-only Capability Mediation

1. PURPOSE. Introduce controlled epistemic actions: SEARCH, RESOLVE, READ, INSPECT, TRAVERSE, TRACE_PROVENANCE.

2. CURRENT ANATOMY. Federated resolution from T5; organ-specific read/traversal APIs; FUSION read boundary.

3. REUSE. Native search/read/traversal/provenance operations.

4. CONNECT. Capability request → permission/domain → native operation.

5. ADAPT. FUSION may expose/connect reachability but must not become a god router.

6. NEW. Minimal capability request/mediation contract.

7. FILE IMPACT. Cognitive coordination package location is determined from repository anatomy at T5. runtime/organism.py should preferably remain unchanged unless a missing reachability hook is proven.

8. CONTRACT CHANGE. Model may request semantic operations but never arbitrary filesystem/runtime operations.

9. INVARIANTS. I-02, I-04, I-05, I-06, I-09.

10. TEST PLAN. Every capability read-only; forbidden mutation attempts fail closed.

11. ACCEPTANCE GATE. Capability layer cannot mutate Canon, repository, Sedimentation, runtime config or Experience.

12. FAILURE GATE. Any write path reachable through navigation.

13. CONSERVATION. FUSION's current read-only authority boundary preserved.

14. ERROR MEMORY. Record capability-boundary escapes.

15. REPORT. Capability/organ/permission matrix and mutation-negative tests.


---

K. T7 Information Need + Journey State

1. PURPOSE. Represent task-driven epistemic demand and durable research progression.

2. CURRENT ANATOMY. Sessions provide persistence precedent; Persistent Experience provides durable experience but is semantically wrong for journeys.

3. REUSE. IDs/persistence conventions where legitimate.

4. CONNECT. Question/orientation → Need; results → Journey hops.

5. ADAPT. None to sessions yet.

6. NEW. Information Need and Journey State contracts are genuinely absent and cannot be absorbed into Conversation, Experience or Memory without collapsing epistemic classes.

7. FILE IMPACT. New location selected beside cognitive coordination contracts, not under Experience/Memory. Tests there. Sessions untouched until T14.

8. CONTRACT CHANGE. Research becomes explicit/auditable rather than implicit provider reasoning.

9. INVARIANTS. I-01, I-02, I-07, I-11.

10. TEST PLAN. Need lifecycle, parent/next need, hop recording, stop reason, serialization/reconstruction.

11. ACCEPTANCE GATE. Journey can represent a deterministic multi-hop fixture independently of provider.

12. FAILURE GATE. Journey persistence changes authority/classification.

13. CONSERVATION. Conversation/Experience/Memory remain separate.

14. ERROR MEMORY. Journey-corruption/persistence-loss class.

15. REPORT. Journey schema, lifecycle examples, persistence proof.


---

L. T8 Cognitive Loop

1. PURPOSE. Make iterative research possible.

2. CURRENT ANATOMY. T3 orientation, T5 resolution, T6 capabilities, T7 Need/Journey.

3. REUSE. All previous contracts and organ traversal.

4. CONNECT. Provider reasoning proposes next need/capability; organism validates/executes.

5. ADAPT. Pipeline only later; T8 should initially be independently executable/testable.

6. NEW. Minimal cognitive coordinator is justified because movement between organs is absent.

7. FILE IMPACT. Cognitive coordination package + focused tests only; no legacy pipeline cutover.

8. CONTRACT CHANGE. Need evaluation yields exact terminal states:

SATISFIED, PARTIAL, UNKNOWN, BLOCKED, HUMAN_REQUIRED, FORBIDDEN, NO_EPISTEMIC_GAIN.

9. INVARIANTS. I-02–I-07, I-09, I-11.

10. TEST PLAN. Repeated need, repeated result, repeated (identity, capability), traversal cycle, unavailable organ, ambiguity, authority stop, no gain.

11. ACCEPTANCE GATE. No test fixture can traverse indefinitely; UNKNOWN is reachable without fabrication.

12. FAILURE GATE. Unbounded autonomous traversal or model bypass.

13. CONSERVATION. Journey state persists on blocked/provider-failure boundaries.

14. ERROR MEMORY. Infinite-loop/repeated-retrieval/authority-bypass errors.

15. REPORT. State-transition coverage and every terminal-condition proof.


---

M. T9 Working Context Assembly

1. PURPOSE. Materialize temporary consciousness from selected Journey evidence.

2. CURRENT ANATOMY. AIContextBuilder currently constructs pre-research snapshot; T7/T8 provide journey/results.

3. REUSE. Existing serialization helpers where semantically safe.

4. CONNECT. Selected result envelopes → Working Context.

5. ADAPT. AIContextBuilder responsibility must now be split; exact implementation shape determined by T1 characterization rather than class name.

6. NEW. Working Context representation/assembler because Journey and legacy context are not equivalent.

7. FILE IMPACT. ai_platform/context_builder.py plus cognitive-context contracts/tests. RepositoryEngine unchanged.

8. CONTRACT CHANGE. Working Context becomes output of research, not prerequisite for research.

9. INVARIANTS. I-01, I-02, I-06, I-08, I-10, I-11.

10. TEST PLAN. Selection, deduplication, provenance references, contradictions, Human constraints, journey-summary exclusion of full journey.

11. ACCEPTANCE GATE. Working Context is strictly smaller/selective in representative fixture while preserving necessary evidence.

12. FAILURE GATE. Assembly triggers repository-wide materialization.

13. CONSERVATION. Journey remains reconstructible independently.

14. ERROR MEMORY. Provenance-loss/context-contamination class.

15. REPORT. Journey-vs-Working-Context comparison.


---

N. T10 Context Budget Governance

1. PURPOSE. Guarantee provider-safe materialization without reducing organism knowledge.

2. CURRENT ANATOMY. Provider token limits already exist; T9 provides materializable context.

3. REUSE. ProviderRegistry/model metadata.

4. CONNECT. provider/model capacity → Working Context materializer.

5. ADAPT. Provider boundary/pipeline must accept governed payload.

6. NEW. Minimal budget policy because token limit metadata alone cannot allocate headroom among orientation/question/instructions/answer/context.

7. FILE IMPACT. AI-platform budget/context layer + tests; no organ storage changes.

8. CONTRACT CHANGE. Serialization is refused/compacted before provider if unsafe.

9. INVARIANTS. I-01, I-08, I-10.

10. TEST PLAN. Dedup, replacement, reference preservation, provider differences, hard overflow rejection.

11. ACCEPTANCE GATE. serialized request <= safe calculated budget for every supported test model.

12. FAILURE GATE. Unknown capacity cannot silently become unlimited; evidence cannot simply be truncated mid-object.

13. CONSERVATION. Full Journey/knowledge untouched.

14. ERROR MEMORY. Budget-estimator mismatch and provenance-breaking compaction.

15. REPORT. Before/after byte/token estimates and budget calculation.


---

O. T11 Shadow Pipeline Integration

1. PURPOSE. Integrate new physiology without changing provider behavior.

2. CURRENT ANATOMY. AIRequestPipeline.run() is the integration seam; service owns it.

3. REUSE. Legacy builder and provider path remain authoritative during shadow.

4. CONNECT. Pipeline invokes new journey/working-context path in observation mode.

5. ADAPT. AIRequestPipeline, service wiring.

6. NEW. Shadow comparison record only if Journey audit cannot represent comparison cleanly.

7. FILE IMPACT. pipeline.py, service.py, related tests; context builder only if required. Sessions must not double-write epistemic state.

8. CONTRACT CHANGE. Provider still receives legacy payload; new payload is computed and compared but not silently substituted.

9. INVARIANTS. All, especially I-04/I-10.

10. TEST PLAN. Compare serialized size, classes, provenance, authority, sufficiency, retrieval path, duplicates, repository-profile contribution and predicted budget.

11. ACCEPTANCE GATE. Shadow output exists with zero provider-behavior change and zero duplicate authority/persistence mutation.

12. FAILURE GATE. Shadow path changes answer/provider selection or writes duplicate epistemic state.

13. CONSERVATION. Legacy path remains immediately usable.

14. ERROR MEMORY. Shadow divergence/new-path side effects.

15. REPORT. Side-by-side legacy/new comparison for controlled prompts.


---

P. T12 "hi" Cutover

1. PURPOSE. First production proof that trivial conversation no longer loads repository-wide cognition.

2. CURRENT ANATOMY. T11 shadow comparison identifies safe new path.

3. REUSE. Orientation, Working Context, budget, existing provider selection.

4. CONNECT. trivial request → no research need → bounded payload.

5. ADAPT. Pipeline cutover selection.

6. NEW. None expected.

7. FILE IMPACT. Primarily pipeline.py and focused tests. RepositoryEngine must not be modified to fake success.

8. CONTRACT CHANGE. "hi" uses new cognitive payload.

9. INVARIANTS. I-01, I-04, I-08, I-10.

10. TEST PLAN. Spy/assert that full RepositoryEngine.profile()/serializer is not invoked for trivial request.

11. ACCEPTANCE GATE. Full profile absent both from materialization and serialized provider payload.

12. FAILURE GATE. Any hidden legacy context fallback recreates full profile.

13. CONSERVATION. Feature/cutover path must permit safe rollback to shadow/legacy without data loss.

14. ERROR MEMORY. Accidental eager-profile regression.

15. REPORT. "hi" trace, invoked components, context size and provider budget.


---

Q. T13 429 Research Cutover

1. PURPOSE. Demonstrate real selective multi-hop cognition.

2. CURRENT ANATOMY. AIPlatformService → pipeline → context builder → RepositoryEngine/profile serializer → provider evidence path.

3. REUSE. Existing semantic/resolution/repository/provenance organs.

4. CONNECT. Information needs traverse those organs selectively.

5. ADAPT. Pipeline chooses research path for substantive diagnostic question.

6. NEW. None beyond prior stages.

7. FILE IMPACT. Pipeline/coordinator tests and fixtures containing real 429 evidence. Repository/Provenance systems remain native.

8. CONTRACT CHANGE. Explanation is produced from retrieved causal evidence, not giant preloaded snapshot.

9. INVARIANTS. All eleven.

10. TEST PLAN. Required multi-hop route, provenance/class preservation, insufficient-evidence UNKNOWN, no static fallback, bounded payload.

11. ACCEPTANCE GATE. Demonstrated causal chain with evidence-selected Working Context below provider-safe budget.

12. FAILURE GATE. Answer claims 429 cause without Evidence or silently substitutes synthetic provider.

13. CONSERVATION. Journey survives provider failure.

14. ERROR MEMORY. False causal closure / evidence insufficiency masked as certainty.

15. REPORT. Complete audited 429 journey: needs, organs, resolver, evidence identity, provenance, stop reason, payload size.


---

R. T14 Session Integration

1. PURPOSE. Connect Conversation to Journey without turning session storage into Memory.

2. CURRENT ANATOMY. AISessionEngine persists session JSON containing repository and engineering snapshots plus conversation/token usage.

3. REUSE. Session identity, timestamps, conversation and token usage.

4. CONNECT. Session → Journey ID/status/reference.

5. ADAPT. Session schema/persistence to stop requiring giant context snapshots for new cognitive requests.

6. NEW. Journey persistence store only if T7 demonstrates no existing neutral persistence contract can own it. It must not be LayeredMemory or Experience masquerading under another name.

7. FILE IMPACT. sessions.py, service session creation, Journey persistence module/tests. Existing session compatibility must be inspected.

8. CONTRACT CHANGE. Session references research; it does not contain/reclassify research knowledge.

9. INVARIANTS. I-01, I-02, I-08, I-11.

10. TEST PLAN. Old session load, new session write, Journey reference, restart reconstruction, no automatic Experience creation.

11. ACCEPTANCE GATE. Conversation ≠ Journey ≠ Working Context is observable in persisted representation.

12. FAILURE GATE. Migration loses existing sessions or duplicates Memory.

13. CONSERVATION. Existing session files remain readable.

14. ERROR MEMORY. Persistence migration/restart corruption.

15. REPORT. Before/after session schema and restart evidence.


---

S. T15 Failure/Restart Validation

1. PURPOSE. Prove physiology remains epistemically honest under failure.

2. CURRENT ANATOMY. Runtime FUSION boundary, Journey persistence, provider pipeline, resolver/capabilities.

3. REUSE. Runtime recovery/state conventions and existing UNKNOWN semantics.

4. CONNECT. Failure events → Journey state.

5. ADAPT. Error propagation where current components swallow/replace errors.

6. NEW. None expected.

7. FILE IMPACT. Primarily tests; production fixes only for demonstrated gaps.

8. CONTRACT CHANGE. Failures preserve Journey and return explicit epistemic status.

9. INVARIANTS. I-02, I-04–I-09, I-11.

10. TEST PLAN. resolver failure, unavailable organ, stale/ambiguous identity, missing/contradictory Evidence, cycle, budget exhaustion, provider failure/429, runtime restart, Human Authority.

11. ACCEPTANCE GATE. Every Phase IV failure physiology has deterministic outcome.

12. FAILURE GATE. Silent fallback, lost Journey, authority promotion, infinite retry.

13. CONSERVATION. Last valid Journey checkpoint survives.

14. ERROR MEMORY. Every newly demonstrated implementation defect gets report preservation and qualification under Error Memory rules.

15. REPORT. Failure matrix with observed status/recovery/persistence.


---

T. T16 Legacy Context Retirement

1. PURPOSE. Remove giant snapshot from default cognition after replacement is proven.

2. CURRENT ANATOMY. Legacy AIContextBuilder/pipeline path remains through T15.

3. REUSE. RepositoryEngine/profile serializer remain explicit capabilities.

4. CONNECT. Full profile becomes opt-in research/diagnostic capability.

5. ADAPT. Context builder and pipeline default behavior.

6. NEW. None.

7. FILE IMPACT. context_builder.py, pipeline.py, service/session remnants and tests. Do not delete RepositoryEngine/ProfileSerializer.

8. CONTRACT CHANGE.

Before:

request → full preconstructed engineering context

After:

request → orientation → need-driven research → bounded working context

9. INVARIANTS. I-01, I-08, I-10 chiefly; all regressions checked.

10. TEST PLAN. Full AI-platform regression plus explicit full-profile capability test.

11. ACCEPTANCE GATE. No default Owner AI Chat path constructs full RepositoryProfile, while explicit repository diagnostics still can.

12. FAILURE GATE. Any legitimate repository capability becomes inaccessible.

13. CONSERVATION. Full-profile machinery remains available outside default cognitive payload.

14. ERROR MEMORY. Legacy dependency discovered after retirement.

15. REPORT. Final legacy-call graph, retained explicit uses, context reduction evidence and full regression verdict.


---

U. Cross-Stage Dependency Graph

T1 Characterization
 │
 ├─→ T2 Provider Budget
 │
 └─→ T3 Orientation
       ↓
T4 Result Envelope
       ↓
T5 Federated Resolution
       ↓
T6 Capability Mediation
       ↓
T7 Need + Journey
       ↓
T8 Cognitive Loop
       ↓
T9 Working Context
       ↓
T10 Budget Governance
       ↓
T11 Shadow Integration
       ↓
T12 "hi" Cutover
       ↓
T13 429 Cutover
       ↓
T14 Session Integration
       ↓
T15 Failure/Restart
       ↓
T16 Legacy Retirement

There are deliberate conservation points at T1, T6, T11, T13 and T15. No stage after those points should proceed without its acceptance report.


---

V. Test & Acceptance Matrix

The minimum end-state suite must prove five layers:

Layer	Critical proof

Anatomy	current context path characterized
Epistemics	identity/class/provenance/authority survive
Navigation	multi-hop + termination + UNKNOWN
Context	selective + bounded + provider-aware
Runtime	persistence/restart/provider failure


Two golden acceptance scenarios remain mandatory.

Golden A — hi:

profile_calls == 0
repository-wide retrieval == false
Working Context bounded
provider budget satisfied

Golden B — 429 diagnostic:

multi_hop == true
selective_retrieval == true
provenance_preserved == true
authority_preserved == true
journey_auditable == true
payload_budget_safe == true
synthetic_fallback == false
UNKNOWN_if_insufficient == true

Existing tests are extended before creating new files. New test modules are justified only for genuinely new cognitive contracts that have no legitimate existing test owner.


---

W. File Mutation Matrix

The mutation strategy is intentionally narrow.

Existing file/body	Earliest mutation

lib/python/ai_platform/registry.py	T2 only if necessary
lib/python/ai_platform/model_manager.py	T2
lib/python/ai_platform/context_builder.py	T3/T9
lib/python/ai_platform/pipeline.py	T2 minimally; major T11
lib/python/ai_platform/service.py	T11
lib/python/ai_platform/sessions.py	T14
lib/python/ai_platform/adapters.py	only if provider contract evidence requires it
lib/python/runtime/organism.py	preferably NO CHANGE
CSL lexer/parser/analyzer	NO CHANGE
Canon	NO CHANGE
Knowledge Graph	NO REWRITE
RepositoryEngine	NO REWRITE
LayeredMemory	NO REWRITE
Persistent Experience	NO REWRITE
PCC Provenance	NO REWRITE


Exact filenames for genuinely new cognitive contracts are intentionally not invented in Phase V until the first implementation stage inspects the package topology and chooses the existing architectural owner. That is compliance with the user's prohibition against assuming paths, not an unresolved architectural question.


---

X. Bash Execution Contract

Every T-stage implementation Bash is contractually required to operate from:

~/storage/shared/AI-Projects/AI-Toolkit

and perform, in order:

1. enter exact repository;


2. set -euo pipefail;


3. fetch remote;


4. capture branch/HEAD/status;


5. verify expected branch;


6. prove expected continuation SHA;


7. fail closed on divergence;


8. preserve unrelated work rather than clean/reset it;


9. inspect every target before mutation;


10. establish authorized-file allowlist;


11. perform only stage-authorized mutations;


12. run Python/static/import/syntax validation immediately;


13. run focused tests;


14. run relevant regressions;


15. run stage acceptance measurements;


16. on implementation/execution error, conserve a Markdown failure report and apply existing Error Memory qualification rules;


17. normalize generated Markdown/text integrity where applicable;


18. git diff --check;


19. scan authorized diff for credentials/secrets;


20. prove changed paths ⊆ authorized mutation set;


21. stage only authorized files;


22. commit conserved successful work;


23. push normally;


24. never reset;


25. never force-push;


26. never silently clean unrelated work;


27. fetch remote again;


28. prove local HEAD == remote target HEAD;


29. print commit SHA;


30. print report path;


31. never mutate Canon absent separate Human authorization.



No Bash may treat “tests passed” as sufficient if its stage-specific acceptance gate failed.


---

Y. Commit/Report Conservation Contract

Each T-stage produces one independently auditable conserved unit whenever successful:

T-stage
  ├── authorized implementation/test changes
  ├── implementation report
  ├── focused acceptance evidence
  └── one pushed Git commit

The report must contain:

stage
timestamp
starting branch
starting SHA
remote continuation SHA
repository status before mutation

files inspected
authorized mutation boundary
files actually changed

architectural contract
reuse/connect/adapt/new decisions

static validation
focused tests
regression tests
acceptance measurements

invariants exercised
Error Memory checks
new errors discovered

git diff --check
secret scan
mutation-boundary verification

final status
commit SHA
remote SHA verification
next permitted stage

A failed execution that cannot legitimately commit production/test changes must still conserve its report locally whenever filesystem integrity permits. A later recovery Bash must inspect that report before attempting another mutation.

The implementation reports therefore become the physiological execution history, while GitHub becomes the remotely auditable conserved state.

They do not automatically become Canon, Memory or Persistent Experience.


---

Z. Final Implementation Readiness Verdict

READY FOR T1 IMPLEMENTATION

The repository anatomy is understood precisely enough to implement T1 without architectural improvisation.

This verdict is deliberately limited to T1. Later stages have planned new contracts whose exact file placement should be decided only when their stage is reached and the immediately relevant package topology is inspected.

Exact T1 mutation boundary

T1 is a characterization-only implementation.

Authorized mutations:

existing AI-platform/request-context tests;

existing test helpers/fixtures only where required for measurement;

one T1 Markdown implementation report.


Production files including:

AIPlatformService, AIRequestPipeline, AIContextBuilder, adapters, RepositoryEngine, CSL, Canon, Knowledge Graph, PCC, Memory, Experience and FUSION must remain behaviorally and textually unchanged in T1.

Exact T1 tests

T1 must characterize and assert:

AIPlatformService → AIRequestPipeline path;

AIContextBuilder.build() invocation;

RepositoryProfile presence and contribution;

serialized context byte size;

engineering-context contribution;

provider adapter input;

estimated provider-input baseline;

session persistence of repository_profile;

session persistence of engineering_context;

trivial "hi" behavior under the current legacy physiology;

no accidental authority mutation during characterization.


The existing service/session anatomy confirms that the session currently receives those large snapshots, so this measurement is directly grounded in current code.

Exact T1 acceptance gate

T1 passes only when the report can answer quantitatively:

Where is context constructed?
What invokes RepositoryEngine.profile()?
What enters the provider boundary?
What is serialized size?
What proportion comes from repository_profile?
What proportion comes from engineering context?
What does "hi" materialize today?
What gets persisted into AISessionEngine?
Where exactly can the later cutover occur?

No answer may be inferred from Phase IV alone; each must be produced from executable characterization.

Exact T1 report

PHASE_V_T1_CHARACTERIZATION_BASELINE.md

inside the established Phase-V/PCC-style implementation-report hierarchy selected after inspecting the current work/implementation-reports layout.

Exact expected commit boundary

The T1 commit must contain:

characterization tests
+ test-only measurement support if required
+ PHASE_V_T1_CHARACTERIZATION_BASELINE.md

and zero production-behavior modifications.

Only after that commit is pushed and local HEAD is proven identical to the remote target HEAD is T2 authorized to begin.

This sequencing is what makes the next development deterministic: T1 does not attempt to solve the 429. It first turns the existing 429-producing cognitive anatomy into executable, versioned Evidence against which every subsequent physiological change can be measured.

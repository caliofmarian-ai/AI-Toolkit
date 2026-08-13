# PCC-01 — PROTECTION PRE-IMPLEMENTATION INSPECTION — RUN 013

**Stage:** Protection

**Execution date:** 2026-08-13

**Expected baseline:** `3e5f63ad101e080cf765f4a54383c3246d3866fb`

**Purpose:** Investigate the existing organism before constructing PCC-01 Protection.

**Software modification:** NONE

**Git conservation:** NONE

**Epistemic rule:** term occurrence does not demonstrate behavioral compatibility.

---

## 1. Authoritative Baseline

```text
Expected:    3e5f63ad101e080cf765f4a54383c3246d3866fb
LOCAL:       3e5f63ad101e080cf765f4a54383c3246d3866fb
origin/main: 3e5f63ad101e080cf765f4a54383c3246d3866fb
PASS: LOCAL == origin/main == expected baseline
```

## 2. Inspection Working Tree Boundary

```text
?? work/implementation-reports/PCC-01/PCC-01_PROTECTION_PRE_IMPLEMENTATION_INSPECTION_RUN_013.md

PASS: only RUN 013 report is outside the conserved repository
```

## 3. Accepted PCC-01 Sources Available For Inspection

```text
work/specifications/PCC-01_CORE_EXPERIENCE_IMPLEMENTATION_SPECIFICATION.md
  SHA-256: b16f2b7312bb6182c224135d840178c81dfd138a0c5df30bb8a260714ccdc486
  Bytes:   36215
  Lines:   1608
work/contracts/PCC-01_IMPLEMENTATION_CONTRACT_2026-08-13.md
  SHA-256: b191d5946875074014df7e5acbc8c86a4cc22101fd0f74ad3496170d6d240211
  Bytes:   77434
  Lines:   3467
work/planning/PCC-01_IMPLEMENTATION_INVENTORY_AND_BUILD_PLAN.md
  SHA-256: 4220024727e84c20ecedd835b8e61443050d14ce199522ab068a658a2ad10d78
  Bytes:   54108
  Lines:   2867
work/inspection/PCC-01_CORE_EXPERIENCE_PRE_IMPLEMENTATION_INSPECTION_2026-08-13.md
  SHA-256: 0cc903aff01558622faa6a93782954d9458342c398a7c175fc3ebd8f5f289aa3
  Bytes:   435872
  Lines:   9855
```

## 4. Protection References — Accepted Core Experience Specification


The following material is extracted from the accepted specification.

Occurrence alone is not interpreted as implementation.

```text
7:**Human Authority:** Owner  
31:It defines the software contract that must be accepted by the Human Authority before implementation begins.
53:Persistence is not authority.
68:- Experience Identity represents its persistent identity;
82:2. Experience Identity;
106:9. Persistence != authority
113:## 6. Central Identity Invariant
153:| Experience Identity | CONSTRUIM NOU |
158:Neighboring infrastructure is not automatically replaced.
182:`lib/python/experience/identity.py`
192:No Session, Memory, Evidence, retention, forgetting or protection implementation belongs inside these modules merely for convenience.
204:`tests/experience/test_experience_identity.py`
227:- possess exactly one Experience identity;
230:- remain independent from Session identity;
231:- remain independent from Memory identity;
232:- remain independent from Evidence identity;
239:The model MUST NOT declare authority.
253:Additional fields MUST NOT silently introduce Session, Memory, Evidence, Provenance, authority, retention or protection semantics before their respective phases.
264:- be immutable after creation;
279:## 14. Identity Creation
281:A new Experience receives a new identity only during explicit creation.
283:Loading an existing Experience MUST NOT generate a replacement identity.
285:Recovery of an existing Experience MUST NOT generate a replacement identity.
287:Deserialization MUST preserve the stored Experience identity.
291:## 15. Identity Uniqueness
303:## 16. Identity Stability
319:## 17. Identity Immutability
321:The public domain contract MUST NOT permit arbitrary mutation of `experience_id`.
323:An Experience whose identity changes becomes a different Experience and MUST NOT be silently treated as continuity of the original.
349:Future phases MAY extend lifecycle semantics for retention, archival, forgetting, conflict or protection.
359:the Experience has been admitted into the Core Experience domain and possesses a valid identity but has not yet entered active operation.
366:- authority;
384:- canonical authority.
397:- deleted;
500:Saving MUST NOT silently create a new Experience identity.
508:1. reconstruct the corresponding Experience with the same identity and state; or
515:## 31. Repository Identity Invariant
523:This proves repository identity preservation.
537:The representation MUST preserve enough information to reconstruct the Core Experience without generating a new identity.
560:A filename is not an Experience identity.
564:A serialized record is not authority.
611:1. generate exactly one new Experience identity;
629:4. preserve Experience identity;
642:4. preserve Experience identity;
678:`Experience Identity`
706:Experience MUST NOT inherit Memory identity.
730:Core Experience MUST be designed so provenance can later be associated without rewriting Experience identity semantics.
758:## 49. Authority Boundary
760:Persistence does not grant authority.
770:Authority remains governed separately.
772:Human Authority remains with the Owner where Human Acceptance is required.
778:Experience identity MUST NOT be derived from process identity.
782:The Experience identity must remain capable of surviving that death through later persistence/recovery phases.
788:Experience identity MUST NOT be derived from an AI provider.
796:## 52. Protection Against Concept Collapse
800:- Experience subclasses Session merely to reuse identity;
805:- storage location is treated as Experience identity;
819:`ExperienceIdentityError`
831:- malformed identity;
844:That would destroy identity continuity.
854:3. Experience ID is immutable through normal domain operations;
857:6. Session identity is not required;
858:7. Memory identity is not required;
859:8. Evidence identity is not required.
863:## 56. Identity Invariants
865:Identity MUST maintain:
867:1. creation generates a valid identity;
869:3. load does not regenerate identity;
870:4. lifecycle transitions do not modify identity;
871:5. serialization round-trip preserves identity;
872:6. repository round-trip preserves identity.
885:6. lifecycle does not imply authority.
893:1. save/load identity preservation;
896:4. no identity regeneration on load;
897:5. no silent replacement of an existing Experience with another identity;
906:1. one creation request produces one new Experience identity;
907:2. activation preserves identity;
908:3. closure preserves identity;
909:4. retrieval preserves identity;
919:It MUST NOT be silently replaced on load.
1010:## 67. Core Test — Identity Uniqueness
1020:## 68. Core Test — Identity Immutability
1022:Attempt prohibited identity mutation through the supported public API.
1113:- it has a valid identity;
1125:Assert identity preservation and ACTIVE state.
1135:Assert identity preservation and CLOSED state.
1147:This protects the first three epistemic boundaries structurally and behaviorally.
1151:## 79. Core Test — Storage Is Not Identity
1153:Where a file-backed repository is used, test behavior MUST demonstrate that Experience identity is read from domain data and is not inferred solely from an arbitrary runtime object identity.
1157:That naming convention does not redefine identity semantics.
1178:- Identity;
1192:- identity uniqueness;
1193:- identity stability through Core operations;
1203:## 83. Core Acceptance Criterion — Identity
1261:## 88. Explicitly Out of Scope — Protection
1263:Experience Protection is NOT implemented in this milestone.
1265:Protection belongs after the Core organ exists and before the complete persistence/recovery acceptance loop.
1283:Delete does not automatically mean epistemic forgetting.
1328:Any future canonization requires an explicit Human Authority gate.
1348:3. Experience Identity;
1367:5. protection;
1385:It MUST NOT silently invent architectural authority.
1405:Existing organs remain valid unless explicitly superseded through accepted architectural authority.
1407:Core Experience MUST integrate with the organism rather than replace neighboring organs merely because PCC-01 is newer.
1448:## 104. Human Authority Rule
1450:The Human Authority for this gate is:
1454:Only the Human Authority may accept or reject this implementation specification.
1483:2. verify its structural integrity;
1513:No later artifact may retroactively convert an earlier research artifact into Canon without explicit authority.
1521:- stable identity;
1561:These statuses may change only through their respective future evidence and authority gates.
1573:**Experience Identity**
1593:Persistence into authority.
```

## 5. Protection References — Contract And Accepted Build Plan


### Source: `work/contracts/PCC-01_IMPLEMENTATION_CONTRACT_2026-08-13.md`

```text
6:Human Authority: Owner
95:**Persistence != authority**
113:5. protectorul experienței;
761:- invalid/corrupt.
788:- corrupt -> accepted prin simpla ignorare a corupției;
790:- protected -> exported fără autorizație.
807:- invalid identity;
810:- unauthorized;
811:- corrupted persistent body;
980:# 72. Un singur adevăr pentru Session identity
982:Trebuie stabilită o fiziologie unică pentru Session identity.
1203:Human Authority rămâne distinctă de mecanismele automate.
1409:**candidate -> Experience -> identity -> protection -> persistence -> Session binding -> process death -> process restart -> recovery -> inspection -> retention/forgetting behavior**
1432:- protection;
1685:Dacă procesul de guvernanță PCC-01 cere acceptare umană finală, numai Human Authority poate acorda acea acceptare.
1783:- REPLACE;
1827:Protection, retention, archive și forgetting trebuie integrate în ciclul de viață.
2142:- identity;
2145:- Session identity;
2150:- protection;
2155:- corruption;
2211:- demonstrația protection;
2377:6. protection metadata;
2498:- protection;
2533:**Identity**
2535:**Protection**
2569:**provider conversation id -> Session identity -> permanent truth**
2581:**Memory summary -> overwrite Experience**
2799:8. confunda persistence cu authority;
2823:**Identity**
2826:**Protection**
2871:Identity este continuitatea prin care organismul știe că vorbește despre aceeași experiență.
2873:Protection seamănă cu barierele și mecanismele de protecție.
3031:- Experience identity;
3032:- Session identity;
3038:- protection;
3098:- privacy/protection;
3226:**Human Authority**
3251:**Persistence != authority**
3333:Necesită decizia Human Authority.
3337:# 286. Întrebarea pentru Human Authority
3400:- Human Authority.
```

### Source: `work/planning/PCC-01_IMPLEMENTATION_INVENTORY_AND_BUILD_PLAN.md`

```text
6:Human Authority: Owner  
193:# 12. Frontiera Authority
199:**Persistence != authority**
255:- identity;
259:- protection state;
306:candidate -> Experience -> identified -> protected -> persisted -> bound -> recoverable
352:# 23. Experience protection
358:Protection trebuie să fie o stare observabilă, nu doar o presupunere.
393:- load by identity;
477:Experience identity
481:Session identity.
613:- identity;
620:- protection;
630:Evidence poate conține referința la Experience identity.
801:- deleted;
818:# 65. Protection policy
864:Nu acceptăm silent corruption.
874:# 70. Duplicate identity
876:Dacă aceeași identity este revendicată incompatibil de două corpuri, operația trebuie refuzată sau conflictul reprezentat explicit.
882:Load pentru identity inexistentă trebuie să producă rezultat explicit.
888:# 72. Corrupted persistence
902:# 74. Unauthorized access
1028:# 89. Historical immutability
1055:- identity;
1057:- protection;
1095:# 96. Experience Identity
1097:Identity este mecanism transversal.
1191:# 107. Build Phase 2 — Identity
1193:Construim mecanismul de identity.
1237:# 113. Build Phase 8 — Protection
1251:Construim forgetting și diferența față de archive/delete.
1303:# 123. Test — identity uniqueness
1305:Două Experience distincte nu trebuie să primească accidental aceeași identity.
1309:# 124. Test — identity stability
1311:Serializarea și reload-ul nu trebuie să schimbe identity.
1357:Experience identity != Session identity.
1373:# 134. Test — protection
1409:# 140. Test — corruption
1415:# 141. Test — unauthorized access
1421:# 142. Test — duplicate identity
1423:Conflictul de identity trebuie detectat.
1427:# 143. Test — missing identity
1469:**candidate -> Experience -> identity -> protection -> persistence -> Session binding -> process death -> process restart -> recovery -> inspection -> retention/forgetting behavior**
1481:- identity înainte de restart;
1486:- identity după restart;
1508:# 153. Evidence integrity
1527:- identity este stabilă;
1593:**Experience Identity**
1605:**Experience Protection**
1709:# 170. Interdicția persistence-as-authority
1713:**Persistence != authority**
1770:# 178. Invariantul de protection
1791:- identity;
1808:- identity invariant.
1827:**PCC-01 PROVENANCE AND PROTECTION**
1862:- identity;
1949:- identity;
1952:- corruption;
1953:- protection;
2032:Identity  
2036:Protection  
2068:**same persistent Experience identity across real process restart**
2157:4. Experience Identity;
2166:13. protection;
2267:# 227. Forgetting authority
2305:# 233. Mutation semantics
2311:# 234. Direct storage mutation
2550:| Experience Identity | CONSTRUIM NOU | identitate persistentă |
2582:| Persistence / authority | Persistence != authority |
2592:| Core Built | model + identity + lifecycle + service + repository |
2594:| Restart Demonstrated | proces nou recuperează aceeași identity |
2609:- identity există;
2614:- save/load păstrează identity.
2626:- identity este aceeași;
2743:+ Protection  
```

## 6. Prior Pre-Implementation Inspection — Protection-Relevant Observations

```text
9:Human Authority: Owner
50:7. what identity and lifecycle tissue already exists;
82:- **Persistence != authority**
85:The restart identity invariant remains:
311:### Source Plan Section 107 — Build Phase 2 — Identity
315:Construim mecanismul de identity.
381:### Source Plan Section 113 — Build Phase 8 — Protection
405:Construim forgetting și diferența față de archive/delete.
437:**candidate -> Experience -> identity -> protection -> persistence -> Session binding -> process death -> process restart -> recovery -> inspection -> retention/forgetting behavior**
460:- identity este stabilă;
479:**Experience Identity**
491:**Experience Protection**
514:- identity;
589:Identity  
593:Protection  
636:4. Experience Identity;
645:13. protection;
685:| Experience Identity | CONSTRUIM NOU | identitate persistentă |
721:| Persistence / authority | Persistence != authority |
735:| Core Built | model + identity + lifecycle + service + repository |
737:| Restart Demonstrated | proces nou recuperează aceeași identity |
773:+ Protection  
1137:.ai/development_state/integrity.json
1560:lib/python/runtime/identity.py
2103:lib/python/ai_cto_scanner/scoring.py:78:         # Context Integrity Readiness (subset of Project Memory)
2104:lib/python/ai_cto_scanner/scoring.py:79:         integrity_components = self._filter_components(memory, ["Context Integrity", "Snapshot Engine", "Context Persistence"])
2117:lib/python/epistemic/memory/model.py:4: A Memory is immutable.
2154:lib/python/workspace_index/models.py:42:     Canonical immutable in-memory representation of a repository.
3641:lib/python/development_state_engine/runtime.py:260:         self.repository.VerifyIntegrity()
3648:lib/python/development_state_engine/runtime.py:576:         if not self.repository.integrity_path.exists():
3649:lib/python/development_state_engine/runtime.py:582:         payload = json.loads(self.repository.integrity_path.read_text(encoding="utf-8"))
3794:lib/python/executive_briefing_engine/risk_analyzer.py:224:     # Repository Integrity Risks
3795:lib/python/executive_briefing_engine/risk_analyzer.py:240:                 title=f"Repository integrity failures ({len(failed_checks)})",
3796:lib/python/executive_briefing_engine/risk_analyzer.py:242:                     f"{len(failed_checks)} integrity checks failed for this repository."
3858:lib/python/runtime/interfaces/github_webhook.py:10:     discussion, repository, create, delete, ping
3990:lib/python/semantic_repository_intelligence/persistence.py:25:     - The repository identity and analysis timestamp
4007:lib/python/workspace_index/builder.py:39:         Traverse the repository exactly once and return an immutable
4019:lib/python/workspace_index/models.py:4: Immutable data model for the canonical repository representation.
4020:lib/python/workspace_index/models.py:12:     """Immutable representation of a single repository file."""
4021:lib/python/workspace_index/models.py:22:     """Immutable representation of a single repository directory."""
4022:lib/python/workspace_index/models.py:42:     Canonical immutable in-memory representation of a repository.
4023:lib/python/workspace_index/models.py:77:     # Repository identity
4026:lib/python/workspace_index/policy.py:4: Single authority for repository inclusion and exclusion rules.
4027:lib/python/workspace_index/policy.py:13:     Centralised authority for repository path filtering.
4097:lib/python/workspace_orchestrator/registry.py:32:         """Register or replace a repository entry."""
4101:lib/python/workspace_orchestrator/registry.py:65:         """Update an existing repository (full replacement by name)."""
4456:lib/python/ai_cto_scanner/scoring.py:79:         integrity_components = self._filter_components(memory, ["Context Integrity", "Snapshot Engine", "Context Persistence"])
4659:### Term: `identity`
4662:.ai/reports/inspect-20260807.json:4503:       "path": "lib/python/runtime/identity.py",
4663:.ai/runtime/logs/runtime_periodic_20260803_125834.json:4:   "identity": {
4664:.ai/runtime/logs/runtime_periodic_20260803_125835.json:4:   "identity": {
4665:.ai/runtime/logs/runtime_periodic_20260803_130455.json:4:   "identity": {
4666:.ai/runtime/logs/runtime_periodic_20260803_130456.json:4:   "identity": {
4667:artifacts/engineering-project.json:782:         "title": "Review lib/python/runtime/identity.py",
4668:artifacts/engineering-project.json:783:         "body": "# Review lib/python/runtime/identity.py\n\n## Priority\nMEDIUM\n\n## Objective\nSemantic review of module.\n\n## Affected Modules\n- lib/python/runtime/identity.py\n\n## Implementation Checklist\n- [ ] Analyse current implementation\n- [ ] Implement required changes\n- [ ] Execute validation\n- [ ] Perform engineering review\n\n## Acceptance Criteria\n- [ ] Implementation completed\n- [ ] Validation passes\n- [ ] No regression introduced\n- [ ] Documentation updated",
4669:lib/python/ai_cto_scanner/report.py:277:             ("OwnerControl", "Owner Readiness", "Implement owner identity and permission layer"),
4670:lib/python/engineering_workspace/models.py:113:     identity: WorkspaceIdentity
4671:lib/python/engineering_workspace/workspace.py:32:     def identity(self) -> Any:
4672:lib/python/runtime/bootstrap.py:13:     5. Initialize Runtime Identity
4673:lib/python/runtime/bootstrap.py:33: from lib.python.runtime.identity import RuntimeIdentity
4674:lib/python/runtime/bootstrap.py:67:         self.identity: Optional[RuntimeIdentity] = None
4675:lib/python/runtime/bootstrap.py:129:         # Step 6 — Runtime Identity
4676:lib/python/runtime/bootstrap.py:174:         self.identity.lifecycle_phase = LifecyclePhase.READY.value
4677:lib/python/runtime/bootstrap.py:180:         logger.info("Bootstrap: Runtime READY — %s", self.identity.runtime_id)
4678:lib/python/runtime/bootstrap.py:219:         self.identity = RuntimeIdentity.create()
4679:lib/python/runtime/bootstrap.py:221:             "Bootstrap: Runtime identity created — id=%s version=%s",
4680:lib/python/runtime/bootstrap.py:222:             self.identity.runtime_id,
4681:lib/python/runtime/bootstrap.py:223:             self.identity.runtime_version,
4682:lib/python/runtime/bootstrap.py:252:         self.metrics.set_gauge("runtime_id", self.identity.runtime_id)
4683:lib/python/runtime/bootstrap.py:253:         self.metrics.set_gauge("runtime_version", self.identity.runtime_version)
4684:lib/python/runtime/bootstrap.py:506:         self.identity.lifecycle_phase = LifecyclePhase.RUNNING.value
4685:lib/python/runtime/bootstrap.py:524:         self.identity.lifecycle_phase = LifecyclePhase.SHUTDOWN.value
4686:lib/python/runtime/bootstrap.py:578:             identity=self.identity,
4687:lib/python/runtime/bootstrap.py:592:             identity=self.identity,
4688:lib/python/runtime/bootstrap.py:608:             identity=self.identity,
4689:lib/python/runtime/bootstrap.py:634:             "runtime_id": self.identity.runtime_id,
4690:lib/python/runtime/bootstrap.py:635:             "lifecycle_phase": self.identity.lifecycle_phase,
4691:lib/python/runtime/bootstrap.py:650:             identity=self.identity,
4692:lib/python/runtime/diagnostics.py:61:         identity: Any,
4693:lib/python/runtime/diagnostics.py:75:             "runtime_id": identity.runtime_id,
4694:lib/python/runtime/diagnostics.py:77:             "lifecycle_phase": identity.lifecycle_phase,
4695:lib/python/runtime/diagnostics.py:124:             "identity": identity.to_dict(),
4696:lib/python/runtime/identity.py:2: CORE-021 — Runtime Identity
4697:lib/python/runtime/identity.py:3: CANON-055 §8 — Runtime Identity
4698:lib/python/runtime/identity.py:17:     """Immutable identity for a Runtime instance."""
4699:lib/python/runtime/identity.py:32:         """Create a new Runtime Identity from the environment."""
4700:lib/python/runtime/railway.py:7: - Logs deployment identity
4701:lib/python/runtime/railway.py:66:     """Log Railway deployment identity at startup."""
4702:lib/python/runtime/reports.py:30:         identity: Optional[Any] = None,
4703:lib/python/runtime/reports.py:46:         if identity:
4704:lib/python/runtime/reports.py:47:             report["identity"] = identity.to_dict()
4705:lib/python/runtime/reports.py:88:         identity = report.get("identity", {})
4706:lib/python/runtime/reports.py:89:         if identity:
4707:lib/python/runtime/reports.py:90:             lines.append(f"Runtime ID:   {identity.get('runtime_id', 'unknown')}")
4708:lib/python/runtime/reports.py:91:             lines.append(f"Version:      {identity.get('runtime_version', 'unknown')}")
4709:lib/python/runtime/reports.py:92:             lines.append(f"Deployment:   {identity.get('deployment_id', 'unknown')}")
4710:lib/python/runtime/reports.py:93:             lines.append(f"Phase:        {identity.get('lifecycle_phase', 'unknown')}")
4711:lib/python/semantic_repository_intelligence/persistence.py:25:     - The repository identity and analysis timestamp
4712:lib/python/workspace_index/models.py:77:     # Repository identity
4713:lib/python/workspace_orchestrator/models.py:70:     Combines identity, tracking state, intelligence outputs, and cross-repo
4714:lib/python/workspace_orchestrator/models.py:74:     # Identity
4715:lib/python/workspace_orchestrator/persistence.py:7:   workspace.json          workspace identity and metadata
4716:tests/test_runtime_bootstrap.sh:21: assert rt.identity is not None, "identity must be set"
4717:tests/test_runtime_bootstrap.sh:51: # --- Identity has required fields ---
4718:tests/test_runtime_bootstrap.sh:52: identity_dict = rt.identity.to_dict()
4719:tests/test_runtime_bootstrap.sh:54:     assert identity_dict[field], f"Missing identity field: {field}"
4720:tests/test_runtime_regression.sh:19: from lib.python.runtime.identity import RuntimeIdentity
4821:### Term: `protection`
6090:- `IntegrityReport`
7191:- `WorkspaceIdentity`
8139:- `lib.python.runtime.identity`
8231:### `lib/python/runtime/identity.py`
8235:- `RuntimeIdentity`
8391:- `log_railway_identity`
9414:- identity: 24
9432:- identity: 2
9455:- identity: 1
9601:- identity: 11
9705:- identity: 5
9785:- identity: 1
9804:- identity: 1
```

## 7. Existing Software Tissue — Protection / Authority / Integrity Search


Search scope: Python software and tests.

```text
lib/python/autonomous_workflow_engine.py:1:# DEPRECATED: This module is frozen for compatibility only.
lib/python/decision_engine.py:1:# DEPRECATED: This module is frozen for compatibility only.
lib/python/development_validator.py:1:# DEPRECATED: This module is frozen for compatibility only.
lib/python/foundation_audit.py:1:# DEPRECATED: This module is frozen for compatibility only.
lib/python/knowledge_graph_engine.py:1:# DEPRECATED: This module is frozen for compatibility only.
lib/python/memory_engine.py:1:# DEPRECATED: This module is frozen for compatibility only.
lib/python/repository_inventory.py:1:# DEPRECATED: This module is frozen for compatibility only.
lib/python/workspace_index/__init__.py:9:from .policy import RepositoryPolicy
lib/python/workspace_index/__init__.py:28:    "RepositoryPolicy",
lib/python/workspace_index/builder.py:4:Sole authority for filesystem traversal.
lib/python/workspace_index/builder.py:15:from .policy import RepositoryPolicy
lib/python/workspace_index/builder.py:20:    Performs exactly one filesystem traversal and produces an immutable
lib/python/workspace_index/builder.py:25:    builder = WorkspaceIndexBuilder(root=".", policy=RepositoryPolicy())
lib/python/workspace_index/builder.py:29:    def __init__(self, root=".", policy=None):
lib/python/workspace_index/builder.py:31:        self.policy = policy if policy is not None else RepositoryPolicy()
lib/python/workspace_index/builder.py:39:        Traverse the repository exactly once and return an immutable
lib/python/workspace_index/builder.py:59:                if self.policy.is_excluded_dir(d) or self.policy.should_prune(current_parts + (d,)):
lib/python/workspace_index/builder.py:85:                if self.policy.is_excluded_file(filename, ext):
lib/python/workspace_index/incremental.py:9:    RepositoryPolicy
lib/python/workspace_index/incremental.py:17:    WorkspaceIndex  (immutable, unchanged public interface)
lib/python/workspace_index/incremental.py:32:from .policy import RepositoryPolicy
lib/python/workspace_index/incremental.py:36:# A version mismatch forces a full rebuild and replaces the stale cache.
lib/python/workspace_index/incremental.py:50:@dataclass(frozen=True)
lib/python/workspace_index/incremental.py:59:@dataclass(frozen=True)
lib/python/workspace_index/incremental.py:110:@dataclass(frozen=True)
lib/python/workspace_index/incremental.py:120:    removed: Tuple[str, ...]             # relative paths of deleted files
lib/python/workspace_index/incremental.py:154:@dataclass(frozen=True)
lib/python/workspace_index/incremental.py:190:    Contains the immutable WorkspaceIndex alongside incremental metrics.
lib/python/workspace_index/incremental.py:297:    result = IncrementalWorkspaceIndex(root=".", policy=policy).build()
lib/python/workspace_index/incremental.py:298:    index  = result.index   # standard immutable WorkspaceIndex
lib/python/workspace_index/incremental.py:306:    def __init__(self, root=".", policy=None, cache_dir=None):
lib/python/workspace_index/incremental.py:308:        self.policy = policy if policy is not None else RepositoryPolicy()
lib/python/workspace_index/incremental.py:320:        Return an immutable WorkspaceIndex, using cached data wherever possible.
lib/python/workspace_index/incremental.py:381:        index = WorkspaceIndexBuilder(self.root, policy=self.policy).build()
lib/python/workspace_index/incremental.py:504:        Applies the same RepositoryPolicy pruning as WorkspaceIndexBuilder so
lib/python/workspace_index/incremental.py:537:                    self.policy.is_excluded_dir(d)
lib/python/workspace_index/incremental.py:538:                    or self.policy.should_prune(candidate_parts)
lib/python/workspace_index/incremental.py:548:                if self.policy.is_excluded_file(filename, ext):
lib/python/workspace_index/models.py:4:Immutable data model for the canonical repository representation.
lib/python/workspace_index/models.py:10:@dataclass(frozen=True)
lib/python/workspace_index/models.py:12:    """Immutable representation of a single repository file."""
lib/python/workspace_index/models.py:20:@dataclass(frozen=True)
lib/python/workspace_index/models.py:22:    """Immutable representation of a single repository directory."""
lib/python/workspace_index/models.py:28:@dataclass(frozen=True)
lib/python/workspace_index/models.py:42:    Canonical immutable in-memory representation of a repository.
lib/python/workspace_index/models.py:45:    Read-only after construction — mutation raises AttributeError.
lib/python/workspace_index/models.py:67:        object.__setattr__(self, "_locked", True)
lib/python/workspace_index/models.py:70:        if getattr(self, "_locked", False):
lib/python/workspace_index/models.py:72:                "WorkspaceIndex is immutable and cannot be modified after construction."
lib/python/workspace_index/models.py:146:            if "canonical" in f.path.replace("\\", "/")
lib/python/workspace_index/policy.py:2:Repository Policy
lib/python/workspace_index/policy.py:4:Single authority for repository inclusion and exclusion rules.
lib/python/workspace_index/policy.py:7:All filtering is delegated to RepositoryPolicy.
lib/python/workspace_index/policy.py:11:class RepositoryPolicy:
lib/python/workspace_index/policy.py:13:    Centralised authority for repository path filtering.
lib/python/workspace_index/policy.py:20:    DEFAULT_EXCLUDE_DIRS = frozenset([
lib/python/workspace_index/policy.py:43:    DEFAULT_EXCLUDE_EXTENSIONS = frozenset([
lib/python/workspace_index/policy.py:60:            Full replacement for the default directory exclusion set.
lib/python/workspace_index/policy.py:65:            Full replacement for the default extension exclusion set.
lib/python/workspace_index/policy.py:70:            frozenset(exclude_dirs)
lib/python/workspace_index/policy.py:74:        self._exclude_dirs = base_dirs | frozenset(extra_exclude_dirs or [])
lib/python/workspace_index/policy.py:77:            frozenset(exclude_extensions)
lib/python/workspace_index/policy.py:81:        self._exclude_extensions = base_ext | frozenset(extra_exclude_extensions or [])
lib/python/repository_engine/engine.py:129:            ("pnpm-lock.yaml", "pnpm"),
lib/python/repository_engine/engine.py:130:            ("yarn.lock", "Yarn"),
lib/python/repository_engine/deps.py:63:        in_require_block = False
lib/python/repository_engine/deps.py:67:                in_require_block = True
lib/python/repository_engine/deps.py:69:            if in_require_block and line == ")":
lib/python/repository_engine/deps.py:70:                in_require_block = False
lib/python/repository_engine/deps.py:77:            if in_require_block and line and not line.startswith("//"):
lib/python/validation_engine/engine.py:30:                    identifier=f"VAL-{path.replace('/','_').upper()}",
lib/python/batch_planner/planner.py:28:            fallback_ref = "lib/python/%s/" % self._slugify(doc.title.replace("Specification", ""))
lib/python/cli/main.py:351:    help="Run in SIMULATION mode (no mutations)",
lib/python/cli/main.py:744:        mode = "READ_ONLY"
lib/python/agents/development_agent.py:10:    RepositoryPolicy,
lib/python/agents/development_agent.py:50:        policy = RepositoryPolicy()
lib/python/agents/development_agent.py:54:            lambda: IncrementalWorkspaceIndex(repository, policy=policy).build(),
lib/python/agents/development_agent.py:74:        # Phase 2 — All engines consume the same immutable WorkspaceIndex
lib/python/rule_engine/__init__.py:7:    Permission,
lib/python/rule_engine/__init__.py:8:    PermissionCategory,
lib/python/rule_engine/__init__.py:9:    PermissionEngine,
lib/python/rule_engine/__init__.py:10:    PermissionDeniedError,
lib/python/rule_engine/__init__.py:27:    "Permission",
lib/python/rule_engine/__init__.py:28:    "PermissionCategory",
lib/python/rule_engine/__init__.py:29:    "PermissionEngine",
lib/python/rule_engine/__init__.py:30:    "PermissionDeniedError",
lib/python/rule_engine/governance_kernel.py:5:- Permission Engine
lib/python/rule_engine/governance_kernel.py:28:# Permission Model (Volume VII Chapter 5)
lib/python/rule_engine/governance_kernel.py:31:class PermissionCategory(str, Enum):
lib/python/rule_engine/governance_kernel.py:42:@dataclass(frozen=True)
lib/python/rule_engine/governance_kernel.py:43:class Permission:
lib/python/rule_engine/governance_kernel.py:44:    """A single explicit permission grant."""
lib/python/rule_engine/governance_kernel.py:46:    category: PermissionCategory
lib/python/rule_engine/governance_kernel.py:68:@dataclass(frozen=True)
lib/python/rule_engine/governance_kernel.py:117:    """Immutable audit record for a governance event."""
lib/python/rule_engine/governance_kernel.py:130:# Permission Engine
lib/python/rule_engine/governance_kernel.py:133:class PermissionEngine:
lib/python/rule_engine/governance_kernel.py:135:    Evaluates whether an actor has permission to execute an action.
lib/python/rule_engine/governance_kernel.py:137:    Permissions shall be explicit (Volume VII Chapter 5).
lib/python/rule_engine/governance_kernel.py:141:        self._grants: List[Permission] = []
lib/python/rule_engine/governance_kernel.py:143:    def grant(self, permission: Permission) -> None:
lib/python/rule_engine/governance_kernel.py:144:        self._grants.append(permission)
lib/python/rule_engine/governance_kernel.py:146:    def check(self, category: PermissionCategory, scope: str) -> bool:
lib/python/rule_engine/governance_kernel.py:153:    def require(self, category: PermissionCategory, scope: str) -> None:
lib/python/rule_engine/governance_kernel.py:154:        """Raise PermissionDeniedError if permission is not granted."""
lib/python/rule_engine/governance_kernel.py:156:            raise PermissionDeniedError(f"Permission denied: {category.value} on '{scope}'")
lib/python/rule_engine/governance_kernel.py:159:class PermissionDeniedError(Exception):
lib/python/rule_engine/governance_kernel.py:160:    """Raised when a required permission is not granted."""
lib/python/rule_engine/governance_kernel.py:181:        "delete": RiskLevel.HIGH,
lib/python/rule_engine/governance_kernel.py:279:    Records immutable audit logs for all governance events.
lib/python/rule_engine/governance_kernel.py:321:    Human authority is mandatory to resume (Volume VII Chapter 3).
lib/python/rule_engine/governance_kernel.py:377:    - Permission Engine
lib/python/rule_engine/governance_kernel.py:385:        kernel.permissions.grant(Permission(PermissionCategory.EXECUTE, "compile"))
lib/python/rule_engine/governance_kernel.py:391:        self.permissions = PermissionEngine()
lib/python/canonical_audit/engine.py:43:                doc.replace("_SPEC", "")
lib/python/canonical_audit/engine.py:44:                   .replace("_v1.0.0", "")
lib/python/canonical_audit/engine.py:45:                   .replace("_v2.0.0", "")
lib/python/knowledge_graph_v2/__init__.py:4:DEPRECATED: This module is frozen for compatibility only.
lib/python/workspace_orchestrator/__init__.py:44:    STATUS_BLOCKED,
lib/python/workspace_orchestrator/__init__.py:100:    "STATUS_BLOCKED",
lib/python/workspace_orchestrator/engine.py:204:            blocked_repositories=sum(1 for r in scanned_repos if r.development_state == "blocked"),
lib/python/workspace_orchestrator/engine.py:277:                    blocked_repositories=0,
lib/python/workspace_orchestrator/engine.py:317:            blocked_repositories=sum(
lib/python/workspace_orchestrator/engine.py:318:                1 for r in repositories if r.development_state == "blocked"
lib/python/workspace_orchestrator/engine.py:413:                blocked_repositories=0,
lib/python/workspace_orchestrator/dashboard.py:49:        blocked_repos = [r for r in repositories if r.development_state == "blocked"]
lib/python/workspace_orchestrator/dashboard.py:80:            "blocked_work": [r.to_dict() for r in blocked_repos],
lib/python/workspace_orchestrator/dashboard.py:194:            label = dim.replace("_", " ").title()
lib/python/workspace_orchestrator/dashboard.py:242:                if p.get("blocking_dependencies"):
lib/python/workspace_orchestrator/dashboard.py:243:                    _add(f"- Blocking Dependencies: {', '.join(p['blocking_dependencies'])}")
lib/python/workspace_orchestrator/dashboard.py:287:        # Blocked Work
lib/python/workspace_orchestrator/dashboard.py:288:        blocked = dashboard.get("blocked_work", [])
lib/python/workspace_orchestrator/dashboard.py:289:        if blocked:
lib/python/workspace_orchestrator/dashboard.py:290:            _add("## Blocked Work")
lib/python/workspace_orchestrator/dashboard.py:292:            for repo in blocked:
lib/python/workspace_orchestrator/intelligence.py:22:    STATUS_BLOCKED,
lib/python/workspace_orchestrator/intelligence.py:142:        blocked = sum(1 for r in repositories if r.development_state == STATUS_BLOCKED)
lib/python/workspace_orchestrator/intelligence.py:144:        if blocked / max(1, total) > 0.3:
lib/python/workspace_orchestrator/intelligence.py:166:        blocked = sum(1 for r in repositories if r.owner_status == STATUS_BLOCKED)
lib/python/workspace_orchestrator/intelligence.py:168:        if blocked / max(1, total) > 0.3:
lib/python/workspace_orchestrator/intelligence.py:206:        # Build dependency lookup: which repos block others
lib/python/workspace_orchestrator/intelligence.py:207:        blocking: Dict[str, List[str]] = {}
lib/python/workspace_orchestrator/intelligence.py:209:            blocking.setdefault(edge.target, []).append(edge.source)
lib/python/workspace_orchestrator/intelligence.py:238:            blocking_deps = blocking.get(repo.name, [])
lib/python/workspace_orchestrator/intelligence.py:251:                blocking_dependencies=tuple(blocking_deps),
lib/python/workspace_orchestrator/intelligence.py:277:        if repo.development_state == STATUS_BLOCKED:
lib/python/workspace_orchestrator/intelligence.py:278:            parts.append("development is blocked")
lib/python/workspace_orchestrator/intelligence.py:285:            return "Restoring this repository will unblock dependent work and reduce overall risk."
lib/python/workspace_orchestrator/intelligence.py:323:        risks.extend(self._blocked_repository_risks(next_id, repositories))
lib/python/workspace_orchestrator/intelligence.py:389:    def _blocked_repository_risks(
lib/python/workspace_orchestrator/intelligence.py:392:        blocked = [r for r in repositories if r.development_state == STATUS_BLOCKED]
lib/python/workspace_orchestrator/intelligence.py:393:        if not blocked:
lib/python/workspace_orchestrator/intelligence.py:399:            title="Blocked repository development",
lib/python/workspace_orchestrator/intelligence.py:400:            description=f"{len(blocked)} repositories have blocked development state.",
lib/python/workspace_orchestrator/intelligence.py:401:            affected_repositories=tuple(r.name for r in blocked),
lib/python/workspace_orchestrator/intelligence.py:402:            remediation="Identify and resolve blocking dependencies. Review current issues and PRs.",
lib/python/workspace_orchestrator/intelligence.py:403:            evidence=tuple(f"{r.name}: development_state=blocked" for r in blocked),
lib/python/workspace_orchestrator/intelligence.py:535:            dependencies=top.blocking_dependencies,
lib/python/workspace_orchestrator/intelligence.py:576:            impact="Canonical compliance unlocks the full AI CTO intelligence layer.",
lib/python/workspace_orchestrator/models.py:44:STATUS_BLOCKED = "blocked"
lib/python/workspace_orchestrator/models.py:213:@dataclass(frozen=True)
lib/python/workspace_orchestrator/models.py:248:@dataclass(frozen=True)
lib/python/workspace_orchestrator/models.py:283:@dataclass(frozen=True)
lib/python/workspace_orchestrator/models.py:350:@dataclass(frozen=True)
lib/python/workspace_orchestrator/models.py:403:@dataclass(frozen=True)
lib/python/workspace_orchestrator/models.py:447:@dataclass(frozen=True)
lib/python/workspace_orchestrator/models.py:457:    blocking_dependencies: Tuple[str, ...]
lib/python/workspace_orchestrator/models.py:472:            "blocking_dependencies": list(self.blocking_dependencies),
lib/python/workspace_orchestrator/models.py:489:            blocking_dependencies=tuple(data.get("blocking_dependencies", [])),
lib/python/workspace_orchestrator/models.py:589:@dataclass(frozen=True)
lib/python/workspace_orchestrator/models.py:598:    blocked_repositories: int
lib/python/workspace_orchestrator/models.py:615:            "blocked_repositories": self.blocked_repositories,
lib/python/workspace_orchestrator/models.py:634:            blocked_repositories=int(data.get("blocked_repositories", 0)),
lib/python/workspace_orchestrator/persistence.py:73:            delete=False,
lib/python/workspace_orchestrator/persistence.py:78:        os.replace(tmp_path, str(target))
lib/python/workspace_orchestrator/persistence.py:329:            a.replace(".json", ""): str(self.base_dir / a)
lib/python/workspace_orchestrator/registry.py:19:    Provides lookup by name and root path.  All mutations are tracked for
lib/python/workspace_orchestrator/registry.py:28:    # Mutation
lib/python/workspace_orchestrator/registry.py:32:        """Register or replace a repository entry."""
lib/python/workspace_orchestrator/registry.py:65:        """Update an existing repository (full replacement by name)."""
lib/python/workspace_orchestrator/scanner.py:42:    STATUS_BLOCKED,
lib/python/workspace_orchestrator/scanner.py:100:            except PermissionError:
lib/python/workspace_orchestrator/scanner.py:180:                    info["default_branch"] = ref.replace("refs/remotes/origin/", "")
lib/python/workspace_orchestrator/scanner.py:265:            owner_status = STATUS_BLOCKED
lib/python/workspace_orchestrator/scanner.py:413:        if any("blocked" in str(c).lower() for c in state_comps):
lib/python/workspace_orchestrator/scanner.py:414:            return STATUS_BLOCKED
lib/python/workspace_orchestrator/state_manager.py:27:    - Provide a live RepositoryRegistry for mutation during a scan
lib/python/workspace_orchestrator/state_manager.py:28:    - Flush state atomically after each mutation
lib/python/repository_profile.py:1:# DEPRECATED: This module is frozen for compatibility only.
lib/python/repository_profile.py:63:if exists("pnpm-lock.yaml"):
lib/python/canonical_entities/models.py:96:@dataclass(frozen=True)
lib/python/canonical_entities/models.py:109:@dataclass(frozen=True)
lib/python/canonical_entities/models.py:120:@dataclass(frozen=True)
lib/python/canonical_entities/models.py:131:@dataclass(frozen=True)
lib/python/canonical_entities/models.py:149:@dataclass(frozen=True)
lib/python/canonical_entities/models.py:161:@dataclass(frozen=True)
lib/python/canonical_entities/models.py:174:@dataclass(frozen=True)
lib/python/canonical_entities/models.py:184:@dataclass(frozen=True)
lib/python/canonical_entities/models.py:200:@dataclass(frozen=True)
lib/python/canonical_entities/uem.py:15:    POLICY = 'POLICY'
lib/python/canonical_entities/uem.py:57:    PROTECTED = 'PROTECTED'
lib/python/canonical_entities/uem.py:77:@dataclass(frozen=True)
lib/python/canonical_parser/parser.py:190:        status = raw_status.strip().lower().replace("-", " ")
lib/python/canonical_parser/csl_parser.py:52:        if not self._consume(TokenType.INDENT, 'CSL-0103', f'Missing indented block for {entity_type}'):
lib/python/canonical_parser/csl_parser.py:73:        if not self._consume(TokenType.INDENT, 'CSL-0103', 'Missing indented block for Relationship'):
lib/python/canonical_parser/csl_parser.py:87:        self._consume(TokenType.DEDENT, 'CSL-0103', 'Missing dedent for Relationship block')
lib/python/canonical_parser/diagnostics.py:38:@dataclass(frozen=True)
lib/python/canonical_parser/lexer.py:40:RESERVED_KEYWORDS = frozenset([
lib/python/canonical_parser/lexer.py:42:    "Policy", "Rule", "Risk", "Issue", "Epic", "Milestone", "Task", "Component",
lib/python/canonical_parser/lexer.py:49:@dataclass(frozen=True)
lib/python/canonical_parser/lexer.py:59:@dataclass(frozen=True)
lib/python/canonical_parser/semantic_analyzer.py:11:@dataclass(frozen=True)
lib/python/coverage_engine/engine.py:39:        metrics.append(self._keyword_metric("Configuration", index, ["config", "configuration", "settings", "policy"]))
lib/python/coverage_engine/engine.py:41:        metrics.append(self._keyword_metric("Security", index, ["security", "auth", "secret", "permission"]))
lib/python/coverage_engine/engine.py:84:                    discovered.append(lowered.replace(" layer", ""))
lib/python/drift_engine/engine.py:25:        timestamp = datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
lib/python/drift_engine/engine.py:179:                    id="orphan-implementation-%s" % wf.name.replace(".", "-").lower(),
lib/python/semantic_matching/matcher.py:179:        aliases.append(doc.id.lower().replace("-", "_"))
lib/python/ai_cto_scanner/detectors.py:82:        file_paths = [wf.path.replace("\\", "/") for wf in all_files]
lib/python/ai_cto_scanner/detectors.py:90:        return self.__class__.__name__.replace("Detector", "")
lib/python/ai_cto_scanner/detectors.py:100:            path_lower = wf.path.replace("\\", "/").lower()
lib/python/ai_cto_scanner/detectors.py:126:                path_lower = wf.path.replace("\\", "/").lower()
lib/python/ai_cto_scanner/detectors.py:249:        ("Permissions", [
lib/python/ai_cto_scanner/detectors.py:250:            r"\bpermissions?\b",
lib/python/ai_cto_scanner/detectors.py:251:            r"check_permission",
lib/python/ai_cto_scanner/detectors.py:252:            r"has_permission",
lib/python/ai_cto_scanner/detectors.py:253:            r"PERMISSIONS\b",
lib/python/ai_cto_scanner/detectors.py:524:        ("Context Integrity", [
lib/python/ai_cto_scanner/detectors.py:525:            r"context_integrity",
lib/python/ai_cto_scanner/detectors.py:526:            r"ContextIntegrity",
lib/python/ai_cto_scanner/detectors.py:527:            r"integrity_check",
lib/python/ai_cto_scanner/report.py:188:                "Extend owner permission layer with AI CTO approval gates",
lib/python/ai_cto_scanner/report.py:192:                "Add AI CTO configuration block to existing config file",
lib/python/ai_cto_scanner/report.py:277:            ("OwnerControl", "Owner Readiness", "Implement owner identity and permission layer"),
lib/python/ai_cto_scanner/report.py:383:            "- [ ] Enable context integrity monitoring",
lib/python/ai_cto_scanner/scoring.py:21:        "ContextIntegrity": 0.6,
lib/python/ai_cto_scanner/scoring.py:78:        # Context Integrity Readiness (subset of Project Memory)
lib/python/ai_cto_scanner/scoring.py:79:        integrity_components = self._filter_components(memory, ["Context Integrity", "Snapshot Engine", "Context Persistence"])
lib/python/ai_cto_scanner/scoring.py:80:        scores["Context Integrity Readiness"] = min(100, int((integrity_components / 3) * 100))
lib/python/semantic_repository_intelligence/architecture_graph.py:108:    norm = path.replace("\\", "/").lower()
lib/python/semantic_repository_intelligence/architecture_graph.py:177:                id=layer.lower().replace(" ", "_").replace("/", "_"),
lib/python/semantic_repository_intelligence/call_graph.py:91:        ENTRY_NAMES = frozenset(["main", "run", "start", "execute", "startup"])
lib/python/semantic_repository_intelligence/call_graph.py:92:        ENTRY_DECORATORS = frozenset([
lib/python/semantic_repository_intelligence/dependency_graph.py:101:        block = data.get(key, {})
lib/python/semantic_repository_intelligence/dependency_graph.py:102:        if isinstance(block, dict):
lib/python/semantic_repository_intelligence/dependency_graph.py:103:            for name, version in sorted(block.items()):
lib/python/semantic_repository_intelligence/import_graph.py:36:        module_rel = module.replace(".", "/")
lib/python/semantic_repository_intelligence/import_graph.py:55:            cand = cand.replace("\\", "/")
lib/python/semantic_repository_intelligence/import_graph.py:60:                if path.replace("\\", "/").endswith("/" + cand):
lib/python/semantic_repository_intelligence/import_graph.py:192:        key = frozenset(cycle)
lib/python/semantic_repository_intelligence/import_graph.py:194:            if frozenset(ex) == key:
lib/python/semantic_repository_intelligence/injection_point_analyzer.py:37:     re.compile(r"@(?:app|bp|router)\.(?:route|get|post|put|delete|patch)\b"),
lib/python/semantic_repository_intelligence/injection_point_analyzer.py:98:     re.compile(r"@(?:Injectable|Component|Pipe|Guard|Interceptor|Controller)\b"),
lib/python/semantic_repository_intelligence/relationship_resolver.py:50:        module_rel = module.replace(".", "/")
lib/python/semantic_repository_intelligence/relationship_resolver.py:100:        return path.replace("/", ".")
lib/python/semantic_repository_intelligence/relationship_resolver.py:125:    p = path.replace("\\", "/")
lib/python/executable_repository_intelligence/executable_dep_graph.py:26:_EXCLUDED_CATEGORIES = frozenset([
lib/python/executable_repository_intelligence/executable_dep_graph.py:37:_EXECUTABLE_CATEGORIES = frozenset([
lib/python/executable_repository_intelligence/file_classifier.py:53:    ("Generated Artifact", "Lock file", False, 0.90, [
lib/python/executable_repository_intelligence/file_classifier.py:54:        ("filename", "package-lock.json"),
lib/python/executable_repository_intelligence/file_classifier.py:55:        ("filename", "yarn.lock"),
lib/python/executable_repository_intelligence/file_classifier.py:56:        ("filename", "poetry.lock"),
lib/python/executable_repository_intelligence/file_classifier.py:57:        ("filename", "Pipfile.lock"),
lib/python/executable_repository_intelligence/file_classifier.py:58:        ("filename", "Cargo.lock"),
lib/python/executable_repository_intelligence/injection_safety.py:10:  READ_ONLY          — Hook only reads state, does not mutate
lib/python/executable_repository_intelligence/injection_safety.py:20:# Injection types that are inherently safe (no mutation, structural only)
lib/python/executable_repository_intelligence/injection_safety.py:21:_SAFE_TYPES = frozenset(["plugin_interface", "service_boundary"])
lib/python/executable_repository_intelligence/injection_safety.py:24:_COND_TYPES = frozenset(["decorator", "middleware", "hook", "di_container"])
lib/python/executable_repository_intelligence/injection_safety.py:27:_RISKY_TYPES = frozenset(["event_bus"])
lib/python/executable_repository_intelligence/injection_safety.py:35:# Evidence keywords suggesting read-only behaviour
lib/python/executable_repository_intelligence/injection_safety.py:36:_READONLY_KEYWORDS = [
lib/python/executable_repository_intelligence/injection_safety.py:37:    "read_only", "readonly", "read only", "observe", "monitor", "listen",
lib/python/executable_repository_intelligence/injection_safety.py:99:        # Check for read-only patterns
lib/python/executable_repository_intelligence/injection_safety.py:100:        if any(kw in evidence_text for kw in _READONLY_KEYWORDS):
lib/python/executable_repository_intelligence/injection_safety.py:105:                safety="READ_ONLY",
lib/python/executable_repository_intelligence/injection_safety.py:106:                rationale="Hook only observes/reads state; no mutation detected.",
lib/python/executable_repository_intelligence/models.py:56:    "READ_ONLY",
lib/python/executable_repository_intelligence/recommendations.py:127:                "which allows arbitrary code injection. Replace with safe, "
lib/python/development_state_engine/__init__.py:18:    IntegrityReport,
lib/python/development_state_engine/__init__.py:39:    "IntegrityReport",
lib/python/development_state_engine/models.py:37:@dataclass(frozen=True)
lib/python/development_state_engine/models.py:46:    blocked_tasks: Tuple[str, ...] = ()
lib/python/development_state_engine/models.py:53:        object.__setattr__(self, "blocked_tasks", _coerce_tuple_of_strings(self.blocked_tasks))
lib/python/development_state_engine/models.py:65:        _validate_tuple_of_strings("blocked_tasks", self.blocked_tasks)
lib/python/development_state_engine/models.py:78:            "blocked_tasks": list(self.blocked_tasks),
lib/python/development_state_engine/models.py:94:            blocked_tasks=tuple(data.get("blocked_tasks", ())),
lib/python/development_state_engine/models.py:100:@dataclass(frozen=True)
lib/python/development_state_engine/models.py:157:@dataclass(frozen=True)
lib/python/development_state_engine/models.py:217:@dataclass(frozen=True)
lib/python/development_state_engine/models.py:275:@dataclass(frozen=True)
lib/python/development_state_engine/models.py:327:@dataclass(frozen=True)
lib/python/development_state_engine/models.py:378:@dataclass(frozen=True)
lib/python/development_state_engine/models.py:428:@dataclass(frozen=True)
lib/python/development_state_engine/models.py:476:@dataclass(frozen=True)
lib/python/development_state_engine/models.py:477:class IntegrityReport:
lib/python/development_state_engine/models.py:479:    repository_integrity: float
lib/python/development_state_engine/models.py:480:    canonical_integrity: float
lib/python/development_state_engine/models.py:481:    memory_integrity: float
lib/python/development_state_engine/models.py:482:    execution_integrity: float
lib/python/development_state_engine/models.py:483:    planning_integrity: float
lib/python/development_state_engine/models.py:484:    resume_integrity: float
lib/python/development_state_engine/models.py:485:    overall_context_integrity_score: float
lib/python/development_state_engine/models.py:494:        _require_percentage("repository_integrity", self.repository_integrity)
lib/python/development_state_engine/models.py:495:        _require_percentage("canonical_integrity", self.canonical_integrity)
lib/python/development_state_engine/models.py:496:        _require_percentage("memory_integrity", self.memory_integrity)
lib/python/development_state_engine/models.py:497:        _require_percentage("execution_integrity", self.execution_integrity)
lib/python/development_state_engine/models.py:498:        _require_percentage("planning_integrity", self.planning_integrity)
lib/python/development_state_engine/models.py:499:        _require_percentage("resume_integrity", self.resume_integrity)
lib/python/development_state_engine/models.py:500:        _require_percentage("overall_context_integrity_score", self.overall_context_integrity_score)
lib/python/development_state_engine/models.py:506:            "repository_integrity": float(self.repository_integrity),
lib/python/development_state_engine/models.py:507:            "canonical_integrity": float(self.canonical_integrity),
lib/python/development_state_engine/models.py:508:            "memory_integrity": float(self.memory_integrity),
lib/python/development_state_engine/models.py:509:            "execution_integrity": float(self.execution_integrity),
lib/python/development_state_engine/models.py:510:            "planning_integrity": float(self.planning_integrity),
lib/python/development_state_engine/models.py:511:            "resume_integrity": float(self.resume_integrity),
lib/python/development_state_engine/models.py:512:            "overall_context_integrity_score": float(self.overall_context_integrity_score),
lib/python/development_state_engine/models.py:516:    def from_dict(cls, data: Mapping[str, Any]) -> "IntegrityReport":
lib/python/development_state_engine/models.py:520:            repository_integrity=float(data["repository_integrity"]),
lib/python/development_state_engine/models.py:521:            canonical_integrity=float(data["canonical_integrity"]),
lib/python/development_state_engine/models.py:522:            memory_integrity=float(data["memory_integrity"]),
lib/python/development_state_engine/models.py:523:            execution_integrity=float(data["execution_integrity"]),
lib/python/development_state_engine/models.py:524:            planning_integrity=float(data["planning_integrity"]),
lib/python/development_state_engine/models.py:525:            resume_integrity=float(data["resume_integrity"]),
lib/python/development_state_engine/models.py:526:            overall_context_integrity_score=float(data["overall_context_integrity_score"]),
lib/python/development_state_engine/models.py:530:@dataclass(frozen=True)
lib/python/development_state_engine/models.py:541:    integrity_report: IntegrityReport
lib/python/development_state_engine/models.py:567:        if not isinstance(self.integrity_report, IntegrityReport):
lib/python/development_state_engine/models.py:568:            raise ValueError("integrity_report must be IntegrityReport")
lib/python/development_state_engine/models.py:578:        self.integrity_report.validate()
lib/python/development_state_engine/models.py:592:            "integrity_report": self.integrity_report.to_dict(),
lib/python/development_state_engine/models.py:608:            integrity_report=IntegrityReport.from_dict(data["integrity_report"]),
lib/python/development_state_engine/repository.py:28:        self.integrity_path = self.base_dir / "integrity.json"
lib/python/development_state_engine/repository.py:35:        """Load current state with integrity verification and migration."""
lib/python/development_state_engine/repository.py:42:        self.VerifyIntegrity(payload)
lib/python/development_state_engine/repository.py:55:        current_integrity = self._safe_read_integrity()
lib/python/development_state_engine/repository.py:56:        history = current_integrity.get("snapshot_history", [])
lib/python/development_state_engine/repository.py:57:        self._write_integrity(payload, history)
lib/python/development_state_engine/repository.py:62:        """Create immutable snapshot from current state and track history."""
lib/python/development_state_engine/repository.py:77:        integrity = self._safe_read_integrity()
lib/python/development_state_engine/repository.py:78:        history: List[Dict[str, Any]] = list(integrity.get("snapshot_history", []))
lib/python/development_state_engine/repository.py:89:        self._write_integrity(payload, history)
lib/python/development_state_engine/repository.py:124:    def VerifyIntegrity(self, payload: Optional[Mapping[str, Any]] = None) -> bool:
lib/python/development_state_engine/repository.py:125:        """Verify current state hash against integrity metadata."""
lib/python/development_state_engine/repository.py:131:        integrity = self._read_json(self.integrity_path)
lib/python/development_state_engine/repository.py:132:        expected = integrity.get("state_sha256")
lib/python/development_state_engine/repository.py:134:            raise ValueError("Integrity file missing state hash")
lib/python/development_state_engine/repository.py:138:            raise ValueError("Integrity verification failed for development state")
lib/python/development_state_engine/repository.py:164:            os.replace(tmp_path, path)
lib/python/development_state_engine/repository.py:175:    def _safe_read_integrity(self) -> Dict[str, Any]:
lib/python/development_state_engine/repository.py:176:        if not self.integrity_path.exists():
lib/python/development_state_engine/repository.py:178:        return self._read_json(self.integrity_path)
lib/python/development_state_engine/repository.py:180:    def _write_integrity(self, payload: Mapping[str, Any], snapshot_history: List[Dict[str, Any]]):
lib/python/development_state_engine/repository.py:181:        integrity_payload = {
lib/python/development_state_engine/repository.py:186:        self._atomic_write_text(self.integrity_path, self._serialize(integrity_payload))
lib/python/development_state_engine/repository.py:206:        integrity = self._safe_read_integrity()
lib/python/development_state_engine/repository.py:207:        history = integrity.get("snapshot_history", [])
lib/python/development_state_engine/repository.py:238:            "integrity_report",
lib/python/development_state_engine/runtime.py:11:from dataclasses import dataclass, replace
lib/python/development_state_engine/runtime.py:25:    IntegrityReport,
lib/python/development_state_engine/runtime.py:53:@dataclass(frozen=True)
lib/python/development_state_engine/runtime.py:58:    integrity: Dict[str, Any]
lib/python/development_state_engine/runtime.py:69:            "integrity": self.integrity,
lib/python/development_state_engine/runtime.py:199:            os.replace(tmp_path, path)
lib/python/development_state_engine/runtime.py:260:        self.repository.VerifyIntegrity()
lib/python/development_state_engine/runtime.py:263:        integrity = self._load_integrity_document()
lib/python/development_state_engine/runtime.py:271:            "state_sha256": integrity.get("state_sha256", ""),
lib/python/development_state_engine/runtime.py:318:                "integrity_report": state.integrity_report.to_dict(),
lib/python/development_state_engine/runtime.py:320:            integrity=self._load_integrity_document(),
lib/python/development_state_engine/runtime.py:366:        snapshot = replace(
lib/python/development_state_engine/runtime.py:375:        normalized = replace(
lib/python/development_state_engine/runtime.py:390:        return replace(
lib/python/development_state_engine/runtime.py:393:            blocked_tasks=self._dedupe_strings(state.blocked_tasks),
lib/python/development_state_engine/runtime.py:397:        return replace(
lib/python/development_state_engine/runtime.py:404:        return replace(
lib/python/development_state_engine/runtime.py:415:        return replace(
lib/python/development_state_engine/runtime.py:422:        return replace(
lib/python/development_state_engine/runtime.py:431:        return replace(
lib/python/development_state_engine/runtime.py:441:        return replace(
lib/python/development_state_engine/runtime.py:575:    def _load_integrity_document(self) -> Dict[str, Any]:
lib/python/development_state_engine/runtime.py:576:        if not self.repository.integrity_path.exists():
lib/python/development_state_engine/runtime.py:582:        payload = json.loads(self.repository.integrity_path.read_text(encoding="utf-8"))
lib/python/development_state_engine/runtime.py:607:            os.replace(tmp_path, path)
lib/python/development_state_engine/runtime.py:736:        updated = replace(
lib/python/development_state_engine/runtime.py:738:            workspace_state=replace(state.workspace_state, **workspace_updates) if workspace_updates else state.workspace_state,
lib/python/development_state_engine/runtime.py:739:            repository_state=replace(state.repository_state, **repository_updates) if repository_updates else state.repository_state,
lib/python/development_state_engine/runtime.py:740:            execution_state=replace(state.execution_state, **execution_updates) if execution_updates else state.execution_state,
lib/python/development_state_engine/runtime.py:741:            planning_state=replace(state.planning_state, **planning_updates) if planning_updates else state.planning_state,
lib/python/development_state_engine/runtime.py:742:            review_state=replace(state.review_state, **review_updates) if review_updates else state.review_state,
lib/python/development_state_engine/runtime.py:743:            owner_state=replace(state.owner_state, **owner_updates) if owner_updates else state.owner_state,
lib/python/development_state_engine/runtime.py:744:            telegram_state=replace(state.telegram_state, **telegram_updates) if telegram_updates else state.telegram_state,
lib/python/development_state_engine/runtime.py:789:        updated = replace(
lib/python/development_state_engine/runtime.py:791:            execution_state=replace(
lib/python/development_state_engine/runtime.py:820:        updated = replace(
lib/python/development_state_engine/runtime.py:822:            owner_state=replace(
lib/python/development_state_engine/runtime.py:826:            planning_state=replace(
lib/python/development_state_engine/runtime.py:855:        updated = replace(
lib/python/development_state_engine/runtime.py:857:            workspace_state=replace(
lib/python/development_state_engine/runtime.py:864:            planning_state=replace(
lib/python/development_state_engine/runtime.py:892:        updated = replace(
lib/python/development_state_engine/runtime.py:894:            review_state=replace(
lib/python/development_state_engine/runtime.py:916:        updated = replace(
lib/python/development_state_engine/runtime.py:918:            repository_state=replace(
lib/python/development_state_engine/runtime.py:958:        updated = replace(
lib/python/development_state_engine/runtime.py:960:            repository_state=replace(state.repository_state, open_pull_requests=tuple(open_pull_requests)),
lib/python/development_state_engine/runtime.py:961:            review_state=replace(state.review_state, open_prs=tuple(open_prs), pending_reviews=tuple(pending)),
lib/python/development_state_engine/runtime.py:983:        updated = replace(
lib/python/development_state_engine/runtime.py:985:            workspace_state=replace(
lib/python/development_state_engine/runtime.py:1007:        updated = replace(
lib/python/development_state_engine/runtime.py:1009:            workspace_state=replace(state.workspace_state, current_batch=batch_id),
lib/python/development_state_engine/runtime.py:1010:            planning_state=replace(
lib/python/development_state_engine/runtime.py:1050:                blocked_tasks=(),
lib/python/development_state_engine/runtime.py:1119:            integrity_report=IntegrityReport(
lib/python/development_state_engine/runtime.py:1121:                repository_integrity=100.0,
lib/python/development_state_engine/runtime.py:1122:                canonical_integrity=100.0,
lib/python/development_state_engine/runtime.py:1123:                memory_integrity=100.0,
lib/python/development_state_engine/runtime.py:1124:                execution_integrity=100.0,
lib/python/development_state_engine/runtime.py:1125:                planning_integrity=100.0,
lib/python/development_state_engine/runtime.py:1126:                resume_integrity=100.0,
lib/python/development_state_engine/runtime.py:1127:                overall_context_integrity_score=100.0,
lib/python/executive_briefing_engine/decision_tracker.py:25:    - Development state blocking conditions
lib/python/executive_briefing_engine/decision_tracker.py:44:        decisions.extend(self._blocked_task_decisions(next_id, state))
lib/python/executive_briefing_engine/decision_tracker.py:52:    # Blocked task decisions
lib/python/executive_briefing_engine/decision_tracker.py:55:    def _blocked_task_decisions(
lib/python/executive_briefing_engine/decision_tracker.py:60:        blocked_tasks = workspace.get("blocked_tasks", [])
lib/python/executive_briefing_engine/decision_tracker.py:62:        if isinstance(blocked_tasks, list) and blocked_tasks:
lib/python/executive_briefing_engine/decision_tracker.py:63:            task_list = ", ".join(str(t) for t in blocked_tasks[:3])
lib/python/executive_briefing_engine/decision_tracker.py:66:                title="Resolve or de-prioritize blocked tasks",
lib/python/executive_briefing_engine/decision_tracker.py:68:                    f"{len(blocked_tasks)} tasks are blocked: {task_list}. "
lib/python/executive_briefing_engine/decision_tracker.py:69:                    "The owner must decide whether to unblock, reassign, or de-prioritize them."
lib/python/executive_briefing_engine/decision_tracker.py:72:                    "Unblock by resolving dependency or constraint",
lib/python/executive_briefing_engine/decision_tracker.py:77:                recommended_option="Unblock by resolving dependency or constraint",
lib/python/executive_briefing_engine/decision_tracker.py:78:                impact="Restores development velocity and unblocks downstream work.",
lib/python/executive_briefing_engine/decision_tracker.py:81:                    f"Blocked tasks: {blocked_tasks[:5]}"
lib/python/executive_briefing_engine/engine.py:307:        from .models import PRIORITY_COMPLETED, PRIORITY_BLOCKED
lib/python/executive_briefing_engine/engine.py:309:        blocked_count = sum(1 for p in priorities if p.classification == PRIORITY_BLOCKED)
lib/python/executive_briefing_engine/engine.py:326:        # Blocked items
lib/python/executive_briefing_engine/engine.py:327:        from .models import PRIORITY_BLOCKED
lib/python/executive_briefing_engine/engine.py:328:        blocked_items = tuple(
lib/python/executive_briefing_engine/engine.py:329:            p.title for p in priorities if p.classification == PRIORITY_BLOCKED
lib/python/executive_briefing_engine/engine.py:338:            blocked_items=blocked_items,
lib/python/executive_briefing_engine/engine.py:345:    _EMPTY_SENTINELS = frozenset({"", "UNSPECIFIED", "None", "null", "N/A"})
lib/python/executive_briefing_engine/generator.py:95:        if d.blocked_items:
lib/python/executive_briefing_engine/generator.py:97:            lines.append("**Blocked Items:**")
lib/python/executive_briefing_engine/generator.py:98:            for item in d.blocked_items:
lib/python/executive_briefing_engine/insight_generator.py:72:        blocked_tasks = workspace.get("blocked_tasks", [])
lib/python/executive_briefing_engine/insight_generator.py:76:        n_blocked = len(blocked_tasks) if isinstance(blocked_tasks, list) else 0
lib/python/executive_briefing_engine/insight_generator.py:82:        if n_blocked > 3:
lib/python/executive_briefing_engine/insight_generator.py:84:        if n_blocked > 0:
lib/python/executive_briefing_engine/insight_generator.py:92:        integrity = snapshot.get("integrity", {})
lib/python/executive_briefing_engine/insight_generator.py:94:        integrity_report = state.get("integrity_report", {})
lib/python/executive_briefing_engine/insight_generator.py:95:        failed_checks = integrity_report.get("failed_checks", [])
lib/python/executive_briefing_engine/insight_generator.py:107:        if not integrity.get("state_sha256"):
lib/python/executive_briefing_engine/models.py:19:PRIORITY_BLOCKED = "blocked"
lib/python/executive_briefing_engine/models.py:32:RISK_REPOSITORY_INTEGRITY = "repository_integrity"
lib/python/executive_briefing_engine/models.py:41:@dataclass(frozen=True)
lib/python/executive_briefing_engine/models.py:93:@dataclass(frozen=True)
lib/python/executive_briefing_engine/models.py:136:@dataclass(frozen=True)
lib/python/executive_briefing_engine/models.py:170:@dataclass(frozen=True)
lib/python/executive_briefing_engine/models.py:213:@dataclass(frozen=True)
lib/python/executive_briefing_engine/models.py:222:    blocked_items: Tuple[str, ...]
lib/python/executive_briefing_engine/models.py:231:            "blocked_items": list(self.blocked_items),
lib/python/executive_briefing_engine/models.py:242:            blocked_items=tuple(data.get("blocked_items", [])),
lib/python/executive_briefing_engine/models.py:250:@dataclass(frozen=True)
lib/python/executive_briefing_engine/persistence.py:114:            os.replace(tmp_path, path)
lib/python/executive_briefing_engine/priority_engine.py:6:priority levels: Critical, High, Medium, Low, Blocked, Waiting, Completed.
lib/python/executive_briefing_engine/priority_engine.py:12:    PRIORITY_BLOCKED,
lib/python/executive_briefing_engine/priority_engine.py:22:_EMPTY_SENTINELS = frozenset({"", "UNSPECIFIED", "None", "null", "N/A"})
lib/python/executive_briefing_engine/priority_engine.py:34:    - Development state: current tasks, blocked tasks, completed tasks
lib/python/executive_briefing_engine/priority_engine.py:53:        items.extend(self._classify_blocked_items(next_id, state))
lib/python/executive_briefing_engine/priority_engine.py:63:    # Blocked items
lib/python/executive_briefing_engine/priority_engine.py:66:    def _classify_blocked_items(
lib/python/executive_briefing_engine/priority_engine.py:71:        blocked_tasks = workspace.get("blocked_tasks", [])
lib/python/executive_briefing_engine/priority_engine.py:73:        if isinstance(blocked_tasks, list):
lib/python/executive_briefing_engine/priority_engine.py:74:            for task in blocked_tasks:
lib/python/executive_briefing_engine/priority_engine.py:78:                    classification=PRIORITY_BLOCKED,
lib/python/executive_briefing_engine/priority_engine.py:80:                    rationale="Task is in the blocked_tasks list and requires unblocking.",
lib/python/executive_briefing_engine/priority_engine.py:90:                    classification=PRIORITY_BLOCKED,
lib/python/executive_briefing_engine/priority_engine.py:92:                    rationale="Execution job has failed and blocks downstream work.",
lib/python/executive_briefing_engine/priority_engine.py:282:        PRIORITY_BLOCKED: 1,
lib/python/executive_briefing_engine/recommendation_engine.py:32:_EMPTY_SENTINELS = frozenset({"", "UNSPECIFIED", "None", "null", "N/A"})
lib/python/executive_briefing_engine/recommendation_engine.py:55:    - Development state (blocked tasks, open PRs)
lib/python/executive_briefing_engine/recommendation_engine.py:284:        blocked_tasks = workspace.get("blocked_tasks", [])
lib/python/executive_briefing_engine/recommendation_engine.py:285:        if isinstance(blocked_tasks, list) and blocked_tasks:
lib/python/executive_briefing_engine/recommendation_engine.py:288:                title=f"Unblock stalled work items ({len(blocked_tasks)} blocked)",
lib/python/executive_briefing_engine/recommendation_engine.py:290:                    f"{len(blocked_tasks)} tasks are currently blocked and require attention."
lib/python/executive_briefing_engine/recommendation_engine.py:293:                impact="Restores development velocity by clearing blockers.",
lib/python/executive_briefing_engine/recommendation_engine.py:297:                affected_components=tuple(blocked_tasks[:3]),
lib/python/executive_briefing_engine/recommendation_engine.py:299:                    "Blocked tasks directly reduce throughput.  "
lib/python/executive_briefing_engine/recommendation_engine.py:300:                    "Each unresolved blocker stalls downstream work."
lib/python/executive_briefing_engine/recommendation_engine.py:302:                evidence=tuple(blocked_tasks[:3]),
lib/python/executive_briefing_engine/risk_analyzer.py:19:    RISK_REPOSITORY_INTEGRITY,
lib/python/executive_briefing_engine/risk_analyzer.py:35:    integrity reports, and executable intelligence.  Never re-runs analysis.
lib/python/executive_briefing_engine/risk_analyzer.py:49:        integrity = snapshot.get("integrity", {})
lib/python/executive_briefing_engine/risk_analyzer.py:55:        risks.extend(self._repository_integrity_risks(next_id, integrity, state))
lib/python/executive_briefing_engine/risk_analyzer.py:224:    # Repository Integrity Risks
lib/python/executive_briefing_engine/risk_analyzer.py:227:    def _repository_integrity_risks(
lib/python/executive_briefing_engine/risk_analyzer.py:228:        self, next_id, integrity: Mapping[str, Any], state: Mapping[str, Any]
lib/python/executive_briefing_engine/risk_analyzer.py:231:        state_sha = integrity.get("state_sha256", "")
lib/python/executive_briefing_engine/risk_analyzer.py:233:        integrity_report = state.get("integrity_report", {})
lib/python/executive_briefing_engine/risk_analyzer.py:234:        failed_checks = integrity_report.get("failed_checks", [])
lib/python/executive_briefing_engine/risk_analyzer.py:238:                category=RISK_REPOSITORY_INTEGRITY,
lib/python/executive_briefing_engine/risk_analyzer.py:240:                title=f"Repository integrity failures ({len(failed_checks)})",
lib/python/executive_briefing_engine/risk_analyzer.py:242:                    f"{len(failed_checks)} integrity checks failed for this repository."
lib/python/executive_briefing_engine/risk_analyzer.py:246:                remediation="Investigate and resolve all integrity failures before proceeding.",
lib/python/executive_briefing_engine/risk_analyzer.py:252:                category=RISK_REPOSITORY_INTEGRITY,
lib/python/executive_briefing_engine/risk_analyzer.py:254:                title="No integrity hash recorded",
lib/python/executive_briefing_engine/risk_analyzer.py:255:                description="The development state has not been integrity-hashed yet.",
lib/python/executive_briefing_engine/risk_analyzer.py:258:                remediation="Save development state to generate integrity hash.",
lib/python/context_synchronization_engine/engine.py:4:from dataclasses import replace
lib/python/context_synchronization_engine/engine.py:20:_EMPTY_SENTINELS = frozenset({"", "UNSPECIFIED", "None", "null", "N/A"})
lib/python/context_synchronization_engine/engine.py:42:    "open_blockers",
lib/python/context_synchronization_engine/engine.py:138:        value = match.group(1).replace("_", "-").upper()
lib/python/context_synchronization_engine/engine.py:140:            value = value.replace("CORE", "CORE-")
lib/python/context_synchronization_engine/engine.py:153:        value = match.group(1).replace("_", "-").upper()
lib/python/context_synchronization_engine/engine.py:155:            value = value.replace("BATCH", "BATCH-")
lib/python/context_synchronization_engine/engine.py:265:            "open_blockers": _compact_list(workspace_state.get("blocked_tasks", ())),
lib/python/context_synchronization_engine/engine.py:277:        normalized = sorted(value.replace("Z", "+00:00") for value in timestamps if value)
lib/python/context_synchronization_engine/engine.py:480:            "open_blockers": development_context.get("open_blockers", []),
lib/python/context_synchronization_engine/engine.py:532:        normalized = sorted(value.replace("Z", "+00:00") for value in timestamps if value)
lib/python/context_synchronization_engine/engine.py:718:            lines.append(f"- **{key.replace('_', ' ').title()}**: {rendered}")
lib/python/context_synchronization_engine/engine.py:844:        workspace_state = replace(
lib/python/context_synchronization_engine/engine.py:852:            blocked_tasks=tuple(_compact_list(live_context.get("open_blockers", []) or state.workspace_state.blocked_tasks)),
lib/python/context_synchronization_engine/engine.py:854:        repository_state = replace(
lib/python/context_synchronization_engine/engine.py:864:        planning_state = replace(
lib/python/context_synchronization_engine/engine.py:871:        review_state = replace(
lib/python/context_synchronization_engine/engine.py:877:        updated = replace(
lib/python/context_synchronization_engine/engine.py:1228:                "open_tasks": executive.get("owner_dashboard", {}).get("blocked_items", []),
lib/python/context_synchronization_engine/engine.py:1348:                        "authority": details.get("authority", "Owner"),
lib/python/context_synchronization_engine/engine.py:1379:                        "authority": "AI CTO Runtime",
lib/python/context_synchronization_engine/engine.py:1526:            "open_blockers": live_context.get("open_blockers", []),
lib/python/context_synchronization_engine/models.py:24:@dataclass(frozen=True)
lib/python/context_synchronization_engine/models.py:52:@dataclass(frozen=True)
lib/python/context_synchronization_engine/models.py:101:@dataclass(frozen=True)
lib/python/context_synchronization_engine/models.py:144:@dataclass(frozen=True)
lib/python/context_synchronization_engine/persistence.py:46:            os.replace(tmp_path, path)
lib/python/autonomous_planning_engine/__init__.py:35:    PRIORITY_BLOCKED,
lib/python/autonomous_planning_engine/__init__.py:82:    "PRIORITY_BLOCKED",
lib/python/autonomous_planning_engine/batch_planner.py:22:_EMPTY = frozenset({"", "UNSPECIFIED", "None", "null", "N/A"})
lib/python/autonomous_planning_engine/batch_planner.py:39:        content = md_file.read_text(encoding="utf-8", errors="replace")
lib/python/autonomous_planning_engine/batch_planner.py:87:                    blocked_by=(),
lib/python/autonomous_planning_engine/decision_engine.py:11:  - Blocked work                  (from DevelopmentStateEngine blocked_tasks)
lib/python/autonomous_planning_engine/decision_engine.py:34:_EMPTY = frozenset({"", "UNSPECIFIED", "None", "null", "N/A"})
lib/python/autonomous_planning_engine/decision_engine.py:76:                    head = py_file.read_text(encoding="utf-8", errors="replace")[:3000]
lib/python/autonomous_planning_engine/decision_engine.py:113:                            content = f.read_text(encoding="utf-8", errors="replace")
lib/python/autonomous_planning_engine/decision_engine.py:121:                content = f.read_text(encoding="utf-8", errors="replace")
lib/python/autonomous_planning_engine/decision_engine.py:170:        blocked = self._blocked_cores(snapshot)
lib/python/autonomous_planning_engine/decision_engine.py:171:        next_core = self._next_core(implemented, all_known, blocked)
lib/python/autonomous_planning_engine/decision_engine.py:180:            "blocked_cores": blocked,
lib/python/autonomous_planning_engine/decision_engine.py:186:            "blocked_tasks": self._blocked_tasks(snapshot),
lib/python/autonomous_planning_engine/decision_engine.py:204:        blocked: List[str],
lib/python/autonomous_planning_engine/decision_engine.py:206:        """Return the lowest-numbered undone, unblocked documented CORE."""
lib/python/autonomous_planning_engine/decision_engine.py:208:        blocked_set = set(blocked)
lib/python/autonomous_planning_engine/decision_engine.py:210:            if core not in impl_set and core not in blocked_set:
lib/python/autonomous_planning_engine/decision_engine.py:247:    def _blocked_cores(snapshot: Mapping[str, Any]) -> List[str]:
lib/python/autonomous_planning_engine/decision_engine.py:249:        blocked = state.get("workspace_state", {}).get("blocked_tasks", [])
lib/python/autonomous_planning_engine/decision_engine.py:250:        return [t for t in (blocked or []) if _CORE_RE.match(str(t))]
lib/python/autonomous_planning_engine/decision_engine.py:253:    def _blocked_tasks(snapshot: Mapping[str, Any]) -> List[str]:
lib/python/autonomous_planning_engine/decision_engine.py:255:        return list(state.get("workspace_state", {}).get("blocked_tasks", []) or [])
lib/python/autonomous_planning_engine/dependency_resolver.py:10:  - Development state blocked_tasks / priority_queue
lib/python/autonomous_planning_engine/dependency_resolver.py:19:from typing import Any, Dict, FrozenSet, Iterable, List, Mapping, Optional, Set, Tuple
lib/python/autonomous_planning_engine/dependency_resolver.py:37:            source = py_file.read_text(encoding="utf-8", errors="replace")
lib/python/autonomous_planning_engine/dependency_resolver.py:69:        source = py_file.read_text(encoding="utf-8", errors="replace")
lib/python/autonomous_planning_engine/dependency_resolver.py:110:    def dependencies_of(self, node: str) -> FrozenSet[str]:
lib/python/autonomous_planning_engine/dependency_resolver.py:111:        return frozenset(self._edges.get(node, set()))
lib/python/autonomous_planning_engine/dependency_resolver.py:113:    def nodes(self) -> FrozenSet[str]:
lib/python/autonomous_planning_engine/dependency_resolver.py:114:        return frozenset(self._nodes)
lib/python/autonomous_planning_engine/dependency_resolver.py:184:    - Development state: blocked_tasks, priority_queue
lib/python/autonomous_planning_engine/dependency_resolver.py:236:                content = md_file.read_text(encoding="utf-8", errors="replace")
lib/python/autonomous_planning_engine/dependency_resolver.py:251:        their dependents.  Entries that are blocked are placed last.
lib/python/autonomous_planning_engine/dependency_resolver.py:254:        ``dependencies`` (list of entry_id strings) and ``blocked_by``
lib/python/autonomous_planning_engine/dependency_resolver.py:286:        # Move blocked entries to the end
lib/python/autonomous_planning_engine/dependency_resolver.py:287:        unblocked = [e for e in result if not e.get("blocked_by")]
lib/python/autonomous_planning_engine/dependency_resolver.py:288:        blocked = [e for e in result if e.get("blocked_by")]
lib/python/autonomous_planning_engine/dependency_resolver.py:289:        return unblocked + blocked
lib/python/autonomous_planning_engine/engine.py:274:        blocked = decision_ctx.get("blocked_cores", [])
lib/python/autonomous_planning_engine/engine.py:296:            blocked_cores=list(blocked),
lib/python/autonomous_planning_engine/execution_queue.py:15:  - blocked_by
lib/python/autonomous_planning_engine/execution_queue.py:18:  1. Unblocked entries sorted by priority score (Critical → High → Medium → Low)
lib/python/autonomous_planning_engine/execution_queue.py:19:  2. Blocked entries appended at the end
lib/python/autonomous_planning_engine/execution_queue.py:29:    PRIORITY_BLOCKED,
lib/python/autonomous_planning_engine/execution_queue.py:44:    PRIORITY_BLOCKED: 4,
lib/python/autonomous_planning_engine/execution_queue.py:75:            unsorted, may contain blocked items).
lib/python/autonomous_planning_engine/execution_queue.py:110:        # Stable sort: blocked last, then by priority rank, then by entry_id
lib/python/autonomous_planning_engine/execution_queue.py:113:                1 if e.blocked_by else 0,
lib/python/autonomous_planning_engine/issue_planner.py:23:_EMPTY = frozenset({"", "UNSPECIFIED", "None", "null", "N/A"})
lib/python/autonomous_planning_engine/issue_planner.py:72:                    blocked_by=(),
lib/python/autonomous_planning_engine/milestone_planner.py:34:_EMPTY = frozenset({"", "UNSPECIFIED", "None", "null", "N/A"})
lib/python/autonomous_planning_engine/milestone_planner.py:76:                    blocked_by=(),
lib/python/autonomous_planning_engine/models.py:5:All planning artifacts are deterministic, serialisable, and frozen.
lib/python/autonomous_planning_engine/models.py:23:PRIORITY_BLOCKED = "blocked"
lib/python/autonomous_planning_engine/models.py:63:@dataclass(frozen=True)
lib/python/autonomous_planning_engine/models.py:75:    blocked_by: Tuple[str, ...]
lib/python/autonomous_planning_engine/models.py:80:        object.__setattr__(self, "blocked_by", tuple(self.blocked_by))
lib/python/autonomous_planning_engine/models.py:92:            "blocked_by": list(self.blocked_by),
lib/python/autonomous_planning_engine/models.py:135:    blocked_cores: List[str]
lib/python/autonomous_planning_engine/models.py:149:            "blocked_cores": self.blocked_cores,
lib/python/autonomous_planning_engine/persistence.py:113:            os.replace(tmp_path, path)
lib/python/autonomous_planning_engine/pr_planner.py:18:_EMPTY = frozenset({"", "UNSPECIFIED", "None", "null", "N/A"})
lib/python/autonomous_planning_engine/pr_planner.py:60:                    blocked_by=(),
lib/python/autonomous_planning_engine/priority_optimizer.py:26:    PRIORITY_BLOCKED,
lib/python/autonomous_planning_engine/priority_optimizer.py:39:    PRIORITY_BLOCKED: 4,
lib/python/autonomous_planning_engine/priority_optimizer.py:48:_EMPTY = frozenset({"", "UNSPECIFIED", "None", "null", "N/A"})
lib/python/autonomous_planning_engine/priority_optimizer.py:62:    - Stable sort order (blocked items always last)
lib/python/autonomous_planning_engine/priority_optimizer.py:109:                # Replace only the priority field — all other fields unchanged
lib/python/autonomous_planning_engine/priority_optimizer.py:111:                entry = dataclasses.replace(entry, priority=new_priority)
lib/python/autonomous_planning_engine/priority_optimizer.py:130:        # Blocked entries always get the minimum score
lib/python/autonomous_planning_engine/priority_optimizer.py:131:        if entry.blocked_by:
lib/python/autonomous_planning_engine/priority_optimizer.py:155:        """Higher score for entries that unblock more dependent work."""
lib/python/autonomous_planning_engine/priority_optimizer.py:206:        blocked = state.get("workspace_state", {}).get("blocked_tasks", [])
lib/python/autonomous_planning_engine/priority_optimizer.py:207:        if not blocked:
lib/python/autonomous_planning_engine/priority_optimizer.py:208:            blocked = []
lib/python/autonomous_planning_engine/priority_optimizer.py:209:        if entry.entry_id in blocked or entry.title in blocked:
lib/python/autonomous_planning_engine/priority_optimizer.py:258:        if entry.blocked_by:
lib/python/autonomous_planning_engine/priority_optimizer.py:259:            return PRIORITY_BLOCKED
lib/python/autonomous_planning_engine/report.py:22:    blocked = entry.get("blocked_by", [])
lib/python/autonomous_planning_engine/report.py:23:    blocked_str = f" ⚠ BLOCKED by: {', '.join(str(b) for b in blocked)}" if blocked else ""
lib/python/autonomous_planning_engine/report.py:29:        f"(`{entry.get('type', '')}`){blocked_str}\n"
lib/python/autonomous_planning_engine/report.py:89:        blocked = rp.get("blocked_cores", [])
lib/python/autonomous_planning_engine/report.py:95:        if blocked:
lib/python/autonomous_planning_engine/report.py:96:            lines.append(f"**Blocked COREs ({len(blocked)}):**\n")
lib/python/autonomous_planning_engine/report.py:97:            lines.append(_fmt_list(blocked))
lib/python/autonomous_planning_engine/roadmap_planner.py:67:        blocked = decision_context.get("blocked_cores", [])
lib/python/autonomous_planning_engine/roadmap_planner.py:75:        confidence = 0.95 if next_core not in blocked else 0.4
lib/python/autonomous_planning_engine/roadmap_planner.py:91:            "blocked": next_core in blocked,
lib/python/autonomous_planning_engine/roadmap_planner.py:103:        blocked = set(decision_context.get("blocked_cores", []))
lib/python/autonomous_planning_engine/roadmap_planner.py:110:            is_blocked = core_id in blocked
lib/python/autonomous_planning_engine/roadmap_planner.py:118:                    priority="blocked" if is_blocked else "high",
lib/python/autonomous_planning_engine/roadmap_planner.py:124:                    confidence=0.4 if is_blocked else 0.85,
lib/python/autonomous_planning_engine/roadmap_planner.py:125:                    blocked_by=tuple([core_id]) if is_blocked else (),
lib/python/autonomous_execution_engine/__init__.py:40:    MODE_READ_ONLY,
lib/python/autonomous_execution_engine/__init__.py:73:from .policy import ExecutionApproval, ExecutionPermissions, ExecutionPolicy
lib/python/autonomous_execution_engine/__init__.py:91:    "ExecutionPolicy",
lib/python/autonomous_execution_engine/__init__.py:92:    "ExecutionPermissions",
lib/python/autonomous_execution_engine/__init__.py:100:    "MODE_READ_ONLY",
lib/python/autonomous_execution_engine/engine.py:46:    MODE_READ_ONLY,
lib/python/autonomous_execution_engine/engine.py:74:from .policy import ExecutionApproval, ExecutionPermissions, ExecutionPolicy
lib/python/autonomous_execution_engine/engine.py:124:        """Return the first unblocked, highest-priority queue entry."""
lib/python/autonomous_execution_engine/engine.py:126:        unblocked = [e for e in entries if not e.get("blocked_by")]
lib/python/autonomous_execution_engine/engine.py:127:        if not unblocked:
lib/python/autonomous_execution_engine/engine.py:130:        priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3, "blocked": 4}
lib/python/autonomous_execution_engine/engine.py:131:        unblocked.sort(key=lambda e: priority_order.get(e.get("priority", "low"), 99))
lib/python/autonomous_execution_engine/engine.py:132:        return unblocked[0] if unblocked else None
lib/python/autonomous_execution_engine/engine.py:175:        policy: ExecutionPolicy,
lib/python/autonomous_execution_engine/engine.py:186:            policy=policy,
lib/python/autonomous_execution_engine/engine.py:231:        mode: str = MODE_READ_ONLY,
lib/python/autonomous_execution_engine/engine.py:243:            MODE_READ_ONLY, "PLAN_ONLY", "VALIDATION_ONLY",
lib/python/autonomous_execution_engine/engine.py:245:        ) else MODE_READ_ONLY
lib/python/autonomous_execution_engine/engine.py:270:        # Build policy and approval
lib/python/autonomous_execution_engine/engine.py:271:        policy = ExecutionPolicy(mode=self.mode)
lib/python/autonomous_execution_engine/engine.py:341:                          evidence=policy.to_dict())
lib/python/autonomous_execution_engine/engine.py:350:        permissions = ExecutionPermissions()
lib/python/autonomous_execution_engine/engine.py:351:        perm_result = permissions.check(policy, approval)
lib/python/autonomous_execution_engine/engine.py:375:            policy=policy,
lib/python/autonomous_execution_engine/engine.py:386:            policy=policy,
lib/python/autonomous_execution_engine/engine.py:441:                          evidence={"note": "State read-only in safe modes"})
lib/python/autonomous_execution_engine/engine.py:604:            blocked = entry.get("blocked_by", [])
lib/python/autonomous_execution_engine/engine.py:605:            if blocked:
lib/python/autonomous_execution_engine/engine.py:607:                    f"Entry {entry.get('entry_id', '?')!r} is blocked by: {blocked}"
lib/python/autonomous_execution_engine/engine.py:620:        policy: ExecutionPolicy,
lib/python/autonomous_execution_engine/engine.py:652:            policy=self.mode,
lib/python/autonomous_execution_engine/engine.py:661:        policy: ExecutionPolicy,
lib/python/autonomous_execution_engine/engine.py:674:        if policy.is_safe_mode():
lib/python/autonomous_execution_engine/engine.py:725:        if approval != APPROVAL_APPROVED and not ExecutionPolicy(self.mode).is_safe_mode():
lib/python/autonomous_execution_engine/evidence.py:57:    Captures a frozen, reproducible snapshot of the execution context.
lib/python/autonomous_execution_engine/models.py:19:MODE_READ_ONLY = "READ_ONLY"
lib/python/autonomous_execution_engine/models.py:28:    MODE_READ_ONLY,
lib/python/autonomous_execution_engine/models.py:130:    policy: str
lib/python/autonomous_execution_engine/models.py:155:            "policy": self.policy,
lib/python/autonomous_execution_engine/models.py:255:    """Frozen snapshot of execution state for reproducibility."""
lib/python/autonomous_execution_engine/persistence.py:182:            os.replace(tmp_path, path)
lib/python/autonomous_execution_engine/policy.py:2:Autonomous Execution Engine — Execution Policy, Permissions and Approval
lib/python/autonomous_execution_engine/policy.py:21:    MODE_READ_ONLY,
lib/python/autonomous_execution_engine/policy.py:31:# Protected operations — execution MUST never perform these without approval
lib/python/autonomous_execution_engine/policy.py:34:_PROTECTED_OPERATIONS = frozenset(
lib/python/autonomous_execution_engine/policy.py:37:        "delete_branch",
lib/python/autonomous_execution_engine/policy.py:45:# Modes that require explicit owner approval for protected operations
lib/python/autonomous_execution_engine/policy.py:46:_APPROVAL_REQUIRED_MODES = frozenset(
lib/python/autonomous_execution_engine/policy.py:53:# Modes that never execute real mutations
lib/python/autonomous_execution_engine/policy.py:54:_SAFE_MODES = frozenset(
lib/python/autonomous_execution_engine/policy.py:56:        MODE_READ_ONLY,
lib/python/autonomous_execution_engine/policy.py:65:class ExecutionPolicy:
lib/python/autonomous_execution_engine/policy.py:67:    CORE-015B — Execution Policy.
lib/python/autonomous_execution_engine/policy.py:72:    def __init__(self, mode: str = MODE_READ_ONLY) -> None:
lib/python/autonomous_execution_engine/policy.py:74:            MODE_READ_ONLY,
lib/python/autonomous_execution_engine/policy.py:82:            mode = MODE_READ_ONLY
lib/python/autonomous_execution_engine/policy.py:86:        """Return True if the mode never performs real mutations."""
lib/python/autonomous_execution_engine/policy.py:95:        if operation in _PROTECTED_OPERATIONS:
lib/python/autonomous_execution_engine/policy.py:104:            "protected_operations": sorted(_PROTECTED_OPERATIONS),
lib/python/autonomous_execution_engine/policy.py:108:class ExecutionPermissions:
lib/python/autonomous_execution_engine/policy.py:110:    CORE-015B — Execution Permissions.
lib/python/autonomous_execution_engine/policy.py:112:    Validates that the current context has the necessary permissions
lib/python/autonomous_execution_engine/policy.py:116:    def check(self, policy: ExecutionPolicy, approval: str) -> ValidationResult:
lib/python/autonomous_execution_engine/policy.py:118:        Check that policy + approval permit execution.
lib/python/autonomous_execution_engine/policy.py:124:        if policy.requires_approval():
lib/python/autonomous_execution_engine/policy.py:127:                    f"Execution mode {policy.mode!r} requires APPROVED state "
lib/python/autonomous_execution_engine/policy.py:133:                validator="ExecutionPermissions",
lib/python/autonomous_execution_engine/policy.py:137:                evidence={"mode": policy.mode, "approval": approval},
lib/python/autonomous_execution_engine/policy.py:141:            validator="ExecutionPermissions",
lib/python/autonomous_execution_engine/policy.py:145:            evidence={"mode": policy.mode, "approval": approval},
lib/python/autonomous_execution_engine/policy.py:166:        Safe modes are always treated as APPROVED for read-only operations.
lib/python/autonomous_execution_engine/policy.py:167:        Protected modes require an explicit approval signal.
lib/python/autonomous_execution_engine/rollback.py:86:        # Other stages are read-only — no rollback needed
lib/python/self_evaluation_engine/__init__.py:41:    GATE_BLOCKED,
lib/python/self_evaluation_engine/__init__.py:82:    "GATE_BLOCKED",
lib/python/self_evaluation_engine/models.py:20:GATE_BLOCKED = "BLOCKED"
lib/python/self_evaluation_engine/models.py:23:QUALITY_GATES = (GATE_PASS, GATE_WARNING, GATE_FAILED, GATE_BLOCKED, GATE_MANUAL_REVIEW)
lib/python/self_evaluation_engine/persistence.py:211:            os.replace(tmp_path, path)
lib/python/self_improvement_engine/analyzers.py:94:                            f"Evaluate whether {py_file.name!r} can be replaced by "
lib/python/self_improvement_engine/analyzers.py:279:                        gap_id=f"GAP-PKG-{pkg.upper().replace('-', '_')}",
lib/python/self_improvement_engine/generators.py:225:                    canonical_impact="Extends AI CTO with test automation authority.",
lib/python/self_improvement_engine/persistence.py:213:            os.replace(tmp_path, path)
lib/python/runtime/event_dispatcher.py:51:        self._lock = threading.Lock()
lib/python/runtime/event_dispatcher.py:55:        with self._lock:
lib/python/runtime/event_dispatcher.py:64:        with self._lock:
lib/python/runtime/event_dispatcher.py:87:        with self._lock:
lib/python/runtime/identity.py:6:immutable during Runtime execution.
lib/python/runtime/identity.py:17:    """Immutable identity for a Runtime instance."""
lib/python/runtime/interfaces/github_webhook.py:10:    discussion, repository, create, delete, ping
lib/python/runtime/interfaces/github_webhook.py:36:    "delete": "github.delete",
lib/python/runtime/interfaces/http_server.py:163:        # Default no-op handlers (replaced by bootstrap)
lib/python/runtime/job_queue.py:49:        self._lock = threading.Lock()
lib/python/runtime/job_queue.py:78:        with self._lock:
lib/python/runtime/job_queue.py:109:            with self._lock:
lib/python/runtime/job_queue.py:116:        with self._lock:
lib/python/runtime/metrics.py:24:        self._lock = threading.Lock()
lib/python/runtime/metrics.py:32:        with self._lock:
lib/python/runtime/metrics.py:36:        with self._lock:
lib/python/runtime/metrics.py:44:        with self._lock:
lib/python/runtime/metrics.py:48:        with self._lock:
lib/python/runtime/metrics.py:56:        with self._lock:
lib/python/runtime/process.py:7:blocks until shutdown is requested.
lib/python/runtime/process.py:46:        # Block indefinitely until a shutdown signal is received
lib/python/runtime/recovery.py:42:        self._lock = threading.Lock()
lib/python/runtime/recovery.py:55:        with self._lock:
lib/python/runtime/recovery.py:81:        with self._lock:
lib/python/runtime/recovery.py:100:        with self._lock:
lib/python/runtime/recovery.py:104:        with self._lock:
lib/python/runtime/scheduler.py:46:        self._lock = threading.Lock()
lib/python/runtime/scheduler.py:50:        with self._lock:
lib/python/runtime/scheduler.py:62:        with self._lock:
lib/python/runtime/scheduler.py:87:            with self._lock:
lib/python/runtime/scheduler.py:107:        with self._lock:
lib/python/runtime/scheduler.py:111:        with self._lock:
lib/python/runtime/shutdown.py:64:        """Block until shutdown is triggered."""
lib/python/runtime/supervisor.py:36:        self._lock = threading.Lock()
lib/python/runtime/supervisor.py:40:        with self._lock:
lib/python/runtime/supervisor.py:47:        with self._lock:
lib/python/runtime/supervisor.py:57:        with self._lock:
lib/python/runtime/supervisor.py:66:        with self._lock:
lib/python/runtime/supervisor.py:72:                with self._lock:
lib/python/runtime/supervisor.py:85:        with self._lock:
lib/python/runtime/supervisor.py:89:        with self._lock:
lib/python/engineering_engine/repository_audit.py:18:    must_be_replaced: bool
lib/python/engineering_engine/repository_audit.py:46:            "must_be_replaced": False,
lib/python/engineering_engine/repository_audit.py:62:            "must_be_replaced": False,
lib/python/engineering_engine/repository_audit.py:78:            "must_be_replaced": False,
lib/python/engineering_engine/repository_audit.py:94:            "must_be_replaced": False,
lib/python/engineering_engine/repository_audit.py:110:            "must_be_replaced": True,
lib/python/engineering_engine/repository_audit.py:126:            "must_be_replaced": False,
lib/python/engineering_engine/repository_audit.py:137:            "purpose": "higher-order automation, orchestration, and policy/rule evaluation",
lib/python/engineering_engine/repository_audit.py:142:            "must_be_replaced": False,
lib/python/engineering_engine/repository_audit.py:143:            "missing_interfaces": ["governance kernel hooks", "approval/risk/permission contracts", "audit/emergency-stop integration"],
lib/python/engineering_engine/repository_audit.py:144:            "missing_tests": ["approval chain tests", "policy enforcement tests", "emergency stop tests"],
lib/python/engineering_engine/repository_audit.py:158:            "must_be_replaced": True,
lib/python/engineering_engine/repository_audit.py:227:                md.write(f'- Must be replaced: {"yes" if module.must_be_replaced else "no"}\n')
lib/python/engineering_engine/gap_analysis.py:32:            GapItem('Safety and Governance Kernel', 'MISSING', 'Rule/policy components exist without a single mandatory permission/risk/approval/audit/emergency-stop kernel'),
lib/python/engineering_engine/planning_engine.py:31:            ('Inventory and classify modules', 'HIGH', 'MEDIUM', 'Classify every existing module into keep/refactor/replace/deprecate and freeze legacy modules as compatibility-only.', ['lib/python', 'lib/*.sh', 'bin']),
lib/python/engineering_engine/planning_engine.py:33:            ('Build canonical source loader and parser boundary', 'CRITICAL', 'HIGH', 'Replace the markdown-section parser approach with a real CSL lexical/syntax parsing boundary and diagnostics contract.', ['lib/python/canonical_parser', 'lib/python/canonical_entities']),
lib/python/engineering_engine/planning_engine.py:38:            ('Implement governance kernel', 'CRITICAL', 'HIGH', 'Promote rule/policy pieces into mandatory permission, risk, approval, audit, authorization, and emergency-stop services.', ['lib/python/rule_engine', 'lib/python/autonomous_execution_engine', 'lib/python/runtime']),
lib/python/engineering_engine/rule_engine.py:6:@dataclass(frozen=True)
lib/python/engineering_engine/rule_engine.py:17:        PlanningRule("REST API", "BLOCKED", "HIGH", "HIGH"),
lib/python/engineering_engine/dependency_rule_engine.py:54:            status = "BLOCKED"
lib/python/engineering_engine/relationship_extractor.py:22:            source = module_path.replace("/", ".").removesuffix(".py")
lib/python/ai_platform/adapters.py:9:@dataclass(frozen=True)
lib/python/dashboard/service.py:21:@dataclass(frozen=True)
lib/python/dashboard/service.py:229:        description="Loads canonical standard documents and validates them for metadata completeness, version format, required sections, normative language, and cross-reference integrity.",
lib/python/dashboard/service.py:505:                f"<td>{escape(', '.join(capability.get('blocking_dependencies') or []) or 'None')}</td>"
lib/python/dashboard/service.py:509:            "<table><thead><tr><th>Capability</th><th>Status</th><th>Progress</th><th>Target Epic</th><th>Blocking Dependencies</th></tr></thead>"
lib/python/dashboard/service.py:598:                    ("Unlock Conditions", "; ".join(capability["unlock_conditions"]) or "None"),
lib/python/dashboard/service.py:599:                    ("Blocking Dependencies", ", ".join(capability["blocking_dependencies"]) or "None"),
lib/python/dashboard/service.py:977:                    "unlock_conditions": self._unlock_conditions(definition, resolved_paths, resolved_tests),
lib/python/dashboard/service.py:978:                    "blocking_dependencies": [],
lib/python/dashboard/service.py:995:            blocking = [
lib/python/dashboard/service.py:1000:            item["blocking_dependencies"] = blocking
lib/python/dashboard/service.py:1001:            if item["status"] == "Planned" and blocking:
lib/python/dashboard/service.py:1002:                item["status"] = "Blocked"
lib/python/dashboard/service.py:1006:        blocked = sum(1 for item in items if item["status"] == "Blocked")
lib/python/dashboard/service.py:1016:                {"label": "Blocked", "value": str(blocked)},
lib/python/dashboard/service.py:1130:    def _unlock_conditions(
lib/python/dashboard/service.py:1220:            "nav a{display:block;padding:8px 0;}"
lib/python/dashboard/service.py:1330:                f"<td>{escape(str(key).replace('_', ' ').title())}</td>"
lib/python/cdm_engine/engine.py:31:_LIFECYCLE_STATES = frozenset(["Draft", "Normative", "Active", "Deprecated", "Superseded", "Archived"])
lib/python/cdm_engine/engine.py:300:            value = doc.metadata.get(field_name, "") or getattr(doc, field_name.lower().replace(" ", "_"), "")
lib/python/css_engine/engine.py:31:_VALID_STATUSES = frozenset(["Draft", "Normative", "Deprecated", "Superseded", "Archived", "Active"])
lib/python/css_engine/engine.py:250:            value = getattr(record, field_name.lower().replace(" ", "_"), "") or ""
lib/python/engineering_workspace/capabilities.py:28:    DELETE_FILES = "filesystem.delete"
lib/python/engineering_workspace/registry.py:8:The Engineering Workspace Registry does NOT replace existing registries.
lib/python/ai_control_center/kernel.py:8:The kernel DOES NOT replace existing registries.
lib/python/epistemic/capability.py:58:            description="The organism can verify its own structural integrity.",
lib/python/epistemic/memory/model.py:4:A Memory is immutable.
lib/python/epistemic/memory/model.py:12:@dataclass(frozen=True)
lib/python/experience/identity.py:13:@dataclass(frozen=True, slots=True)
lib/python/experience/identity.py:15:    """Immutable identity belonging to one Experience."""
lib/python/experience/model.py:5:from dataclasses import dataclass, replace
lib/python/experience/model.py:12:@dataclass(frozen=True, slots=True)
lib/python/experience/model.py:17:    raw dialogue, process, provider, storage, and authority.
lib/python/experience/model.py:39:        return replace(
lib/python/experience/model.py:46:        return replace(
lib/python/experience/repository.py:20:    """Raised when creation would replace an existing Experience."""
lib/python/experience/repository.py:29:    Persistence is not authority.
lib/python/experience/repository.py:34:        """Store a newly admitted Experience without replacement."""
lib/python/experience/service.py:14:    The service does not become Session, Memory, Evidence, or authority.
lib/python/experience/session_binding.py:17:    Persistence != authority
lib/python/experience/session_binding.py:63:    Session identity or replace it with a parallel representation.
lib/python/experience/session_binding.py:74:@dataclass(frozen=True, slots=True)
tests/experience/test_experience_identity.py:25:def test_experience_identity_is_immutable():
tests/experience/test_experience_identity.py:28:    with pytest.raises(dataclasses.FrozenInstanceError):
tests/experience/test_experience_core.py:57:        "authority",
tests/experience/test_experience_session_binding.py:44:def test_binding_does_not_replace_experience():
tests/experience/test_experience_session_binding.py:96:def test_raw_string_cannot_replace_experience_identity():
tests/experience/test_experience_session_binding.py:104:def test_none_cannot_replace_experience_identity():
```

## 8. Candidate Existing Organs


These are candidates for behavioral inspection, not automatically reusable tissue.

```text
lib/python/agents/repository_inspector_agent.py
lib/python/ai_control_center/providers/local_repository.py
lib/python/autonomous_execution_engine/policy.py
lib/python/canonical_repository/repository.py
lib/python/development_state_engine/repository.py
lib/python/engineering_engine/github_repository_resolver.py
lib/python/engineering_engine/repository_audit.py
lib/python/engineering_engine/repository_model.py
lib/python/engineering_engine/repository_scanner.py
lib/python/engineering_engine/semantic_repository_builder.py
lib/python/engineering_engine/validation_engine.py
lib/python/engineering_engine/validation_plan_engine.py
lib/python/engineering_workspace/permissions.py
lib/python/engineering_workspace/providers/local_repository_provider.py
lib/python/engineering_workspace/repository.py
lib/python/experience/identity.py
lib/python/experience/repository.py
lib/python/repository_hygiene_audit.py
lib/python/repository_inventory.py
lib/python/repository_profile.py
lib/python/rule_engine/rules/repository_size_rule.py
lib/python/rule_engine/rules/validation_rule.py
lib/python/runtime/identity.py
lib/python/session_runtime/storage.py
lib/python/workspace_index/policy.py
```

## 9. Protection-Relevant Python Anatomy Index

```text
lib/python/agents/repository_inspector_agent.py
  7: class RepositoryInspectorAgent
lib/python/ai_control_center/panels/repository/panel.py
  16: class RepositoryPanel
  33: function git_repository
lib/python/ai_control_center/providers/local_repository.py
  19: class LocalRepositoryProvider
lib/python/ai_cto_scanner/report.py
  686: function _repository_complexity
lib/python/ai_platform/service.py
  69: function ask_repository
lib/python/autonomous_execution_engine/policy.py
  65: class ExecutionPolicy
  108: class ExecutionPermissions
lib/python/autonomous_execution_engine/validator.py
  32: function validate_repository
  62: function validate_semantic
  88: function validate_canonical
  114: function validate_regression
  154: function validate_acceptance
lib/python/autonomous_planning_engine/decision_engine.py
  247: function _blocked_cores
  253: function _blocked_tasks
  312: function _repository_health
lib/python/canonical_repository/repository.py
  6: class CanonicalRepository
lib/python/cdm_engine/engine.py
  294: function validate
  322: function validate_all
lib/python/cli/engineering.py
  38: function engineering_validate
lib/python/cli/main.py
  41: function cmd_validate
lib/python/context_synchronization_engine/engine.py
  614: function validate
lib/python/csl_engine/engine.py
  235: function validate
lib/python/css_engine/engine.py
  152: function validate
  167: function validate_all
  248: function _validate_metadata
  259: function _validate_version
  268: function _validate_status
  277: function _validate_required_sections
  288: function _validate_normative_language
  299: function _validate_cross_references
  309: function _validate_dependencies
lib/python/dashboard/service.py
  418: function render_repository
  632: function _load_repository_profile
  918: function ask_repository
  1130: function _unlock_conditions
  1147: function _repository_usage
  1346: function _repository_table
lib/python/development_state_engine/models.py
  22: function _validate_tuple_of_strings
  56: function validate
  101: class RepositoryState
  118: function validate
  178: function validate
  234: function validate
  293: function validate
  345: function validate
  394: function validate
  442: function validate
  477: class IntegrityReport
  491: function validate
  547: function validate
lib/python/development_state_engine/repository.py
  17: class DevelopmentStateRepository
  124: function VerifyIntegrity
  175: function _safe_read_integrity
  180: function _write_integrity
lib/python/development_state_engine/runtime.py
  396: function _normalize_repository_state
  456: function _repository_intelligence
  479: function _semantic_repository_intelligence
  528: function _executable_repository_intelligence
  575: function _load_integrity_document
lib/python/development_validator.py
  20: function validate
lib/python/engineering_engine/github_repository_resolver.py
  8: class GitHubRepository
  13: class GitHubRepositoryResolver
lib/python/engineering_engine/repository_audit.py
  34: class RepositoryAudit
lib/python/engineering_engine/repository_model.py
  23: class RepositoryKnowledge
  28: class RepositoryKnowledgeBuilder
lib/python/engineering_engine/repository_scanner.py
  8: class RepositoryModel
  23: class RepositoryScanner
lib/python/engineering_engine/semantic_entities.py
  45: class SemanticRepository
lib/python/engineering_engine/semantic_repository_builder.py
  22: class SemanticRepositoryBuilder
lib/python/engineering_engine/validation_engine.py
  30: function validate
lib/python/engineering_workspace/models.py
  45: class WorkspaceIdentity
lib/python/engineering_workspace/workspace.py
  32: function identity
  56: function repository
lib/python/executable_repository_intelligence/engine.py
  41: class ExecutableRepositoryEngine
lib/python/executable_repository_intelligence/models.py
  109: class RepositoryRuntimeMap
  230: class RepositoryZone
  282: class ExecutableRepositoryResult
lib/python/executive_briefing_engine/decision_tracker.py
  55: function _blocked_task_decisions
lib/python/executive_briefing_engine/insight_generator.py
  90: function repository_health
lib/python/executive_briefing_engine/priority_engine.py
  66: function _classify_blocked_items
lib/python/executive_briefing_engine/recommendation_engine.py
  473: function _healthy_repository_recommendation
lib/python/executive_briefing_engine/risk_analyzer.py
  227: function _repository_integrity_risks
lib/python/experience/identity.py
  9: class ExperienceIdentityError
lib/python/experience/repository.py
  11: class ExperienceRepositoryError
  23: class ExperienceRepository
  49: class InMemoryExperienceRepository
lib/python/experience/session_binding.py
  58: function validate_experience_id
lib/python/repository_engine/classifier.py
  33: class RepositoryFileClassifier
lib/python/repository_engine/engine.py
  13: class RepositoryEngine
lib/python/repository_engine/exporter.py
  5: class RepositoryExporter
lib/python/repository_engine/models.py
  5: class RepositoryItem
  17: class RepositoryMetrics
  65: class RepositoryProfile
lib/python/repository_engine/serializer.py
  5: class RepositoryProfileSerializer
lib/python/repository_inspector_v2/analyzer.py
  1: class RepositoryAnalyzer
lib/python/repository_inspector_v2/engine.py
  12: class RepositoryInspectorV2
lib/python/rule_engine/governance_kernel.py
  31: class PermissionCategory
  43: class Permission
  133: class PermissionEngine
  159: class PermissionDeniedError
  397: function authorize
lib/python/rule_engine/rules/repository_size_rule.py
  4: class RepositorySizeRule
lib/python/runtime/bootstrap.py
  203: function _step_validate_environment
  218: function _step_create_identity
  666: function _invalidate_runtime_snapshot
lib/python/runtime/config.py
  74: function validate
lib/python/runtime/identity.py
  16: class RuntimeIdentity
lib/python/runtime/interfaces/api_auth.py
  12: function authorized
lib/python/runtime/railway.py
  65: function log_railway_identity
lib/python/runtime/secrets.py
  53: function validate
lib/python/self_evaluation_engine/analyzers.py
  141: class RepositoryComplianceAnalyzer
lib/python/semantic_repository_intelligence/engine.py
  49: class SemanticRepositoryEngine
lib/python/semantic_repository_intelligence/models.py
  436: class RepositoryComplexity
lib/python/session_runtime/storage.py
  4: class SessionStorage
lib/python/validation_engine/csl_validator.py
  56: function validate_text
  74: function validate_file
  77: function validate_uem
  86: function _validate_lexical
  96: function _validate_syntax
  102: function _validate_semantic
  110: function _validate_relationships
  121: function _validate_constraints
  126: function _validate_dependencies
  129: function _validate_governance
  134: function _validate_safety
lib/python/validation_engine/engine.py
  12: function validate
lib/python/workspace_index/incremental.py
  60: class RepositorySnapshot
  367: function invalidate_cache
lib/python/workspace_index/models.py
  81: function repository_name
  85: function repository_root
lib/python/workspace_index/policy.py
  11: class RepositoryPolicy
lib/python/workspace_orchestrator/engine.py
  358: function register_repository
lib/python/workspace_orchestrator/intelligence.py
  389: function _blocked_repository_risks
  443: function _isolated_repository_risks
  516: function _next_repository_recommendation
lib/python/workspace_orchestrator/models.py
  66: class WorkspaceRepository
lib/python/workspace_orchestrator/registry.py
  15: class RepositoryRegistry
lib/python/workspace_orchestrator/scanner.py
  116: function scan_repository
  186: function _map_to_repository
lib/python/workspace_orchestrator/state_manager.py
  76: function register_repository
  81: function remove_repository
  86: function rename_repository
  91: function relocate_repository
  96: function update_repository
  123: function repository_count
tests/experience/test_experience_core.py
  6: function test_complete_core_lifecycle_preserves_one_experience_identity
  30: function test_repository_is_storage_boundary_not_experience_identity
tests/experience/test_experience_identity.py
  18: function test_existing_identity_can_be_reconstructed_without_regeneration
  25: function test_experience_identity_is_immutable
  32: function test_malformed_identity_is_rejected
tests/experience/test_experience_lifecycle.py
  11: function test_created_experience_can_become_active_without_identity_change
  20: function test_active_experience_can_become_closed_without_identity_change
tests/experience/test_experience_model.py
  10: function test_new_experience_has_identity_creation_time_and_created_state
  26: function test_reconstructed_model_preserves_explicit_identity
tests/experience/test_experience_repository.py
  12: function test_repository_adds_and_gets_experience_by_stable_identity
  24: function test_repository_reports_known_identity
  35: function test_repository_rejects_duplicate_admission
  45: function test_repository_rejects_unknown_identity_lookup
  52: function test_repository_saves_new_state_without_changing_identity
  66: function test_repository_rejects_save_for_unknown_experience
tests/experience/test_experience_service.py
  30: function test_service_activates_same_experience_identity
  40: function test_service_closes_same_experience_identity
  51: function test_service_rejects_unknown_identity
tests/experience/test_experience_session_binding.py
  14: function test_experience_create_returns_established_experience_identity
  32: function test_session_identity_is_not_experience_identity
  44: function test_binding_does_not_replace_experience
  56: function test_binding_preserves_exact_experience_identity
  81: function test_empty_session_identity_is_rejected
  91: function test_non_string_session_identity_is_rejected
  96: function test_raw_string_cannot_replace_experience_identity
  104: function test_none_cannot_replace_experience_identity
  112: function test_validate_experience_id_preserves_identity_object
```

## 10. Current Core Experience Organ


This is the organ Protection must surround without collapsing its neighboring organs.


### `lib/python/experience/identity.py`

```python
"""Stable identity for PCC-01 Core Experience."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID, uuid4


class ExperienceIdentityError(ValueError):
    """Raised when an Experience identity is malformed."""


@dataclass(frozen=True, slots=True)
class ExperienceId:
    """Immutable identity belonging to one Experience."""

    value: str

    def __post_init__(self) -> None:
        try:
            parsed = UUID(self.value)
        except (ValueError, TypeError, AttributeError) as exc:
            raise ExperienceIdentityError(
                f"Invalid Experience identity: {self.value!r}"
            ) from exc

        canonical = str(parsed)

        if self.value != canonical:
            raise ExperienceIdentityError(
                "Experience identity must use canonical UUID representation"
            )

    @classmethod
    def create(cls) -> "ExperienceId":
        """Create a new Experience identity."""
        return cls(str(uuid4()))

    @classmethod
    def from_string(cls, value: str) -> "ExperienceId":
        """Reconstruct an existing identity without regeneration."""
        return cls(value)

    def __str__(self) -> str:
        return self.value
```

### `lib/python/experience/model.py`

```python
"""Domain anatomy of one PCC-01 Core Experience."""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime, timezone

from .identity import ExperienceId
from .lifecycle import ExperienceState, transition


@dataclass(frozen=True, slots=True)
class Experience:
    """One Core Experience domain entity.

    Experience remains distinct from Session, Memory, Evidence,
    raw dialogue, process, provider, storage, and authority.
    """

    experience_id: ExperienceId
    created_at: datetime
    state: ExperienceState

    def __post_init__(self) -> None:
        if self.created_at.tzinfo is None:
            raise ValueError("Experience created_at must be timezone-aware")

    @classmethod
    def create(cls) -> "Experience":
        """Create a new Experience in CREATED state."""
        return cls(
            experience_id=ExperienceId.create(),
            created_at=datetime.now(timezone.utc),
            state=ExperienceState.CREATED,
        )

    def activate(self) -> "Experience":
        """Transition CREATED -> ACTIVE while preserving identity."""
        return replace(
            self,
            state=transition(self.state, ExperienceState.ACTIVE),
        )

    def close(self) -> "Experience":
        """Transition ACTIVE -> CLOSED while preserving identity."""
        return replace(
            self,
            state=transition(self.state, ExperienceState.CLOSED),
        )
```

### `lib/python/experience/lifecycle.py`

```python
"""Lifecycle physiology for PCC-01 Core Experience."""

from __future__ import annotations

from enum import Enum


class ExperienceLifecycleError(ValueError):
    """Raised when an illegal Experience lifecycle transition is requested."""


class ExperienceState(str, Enum):
    """Initial Core Experience lifecycle states."""

    CREATED = "CREATED"
    ACTIVE = "ACTIVE"
    CLOSED = "CLOSED"


_ALLOWED_TRANSITIONS: dict[ExperienceState, ExperienceState] = {
    ExperienceState.CREATED: ExperienceState.ACTIVE,
    ExperienceState.ACTIVE: ExperienceState.CLOSED,
}


def transition(
    current: ExperienceState,
    target: ExperienceState,
) -> ExperienceState:
    """Validate one Core Experience lifecycle transition."""

    expected = _ALLOWED_TRANSITIONS.get(current)

    if expected is not target:
        raise ExperienceLifecycleError(
            f"Illegal Experience lifecycle transition: "
            f"{current.value} -> {target.value}"
        )

    return target
```

### `lib/python/experience/repository.py`

```python
"""Repository boundary for PCC-01 Core Experience."""

from __future__ import annotations

from abc import ABC, abstractmethod

from .identity import ExperienceId
from .model import Experience


class ExperienceRepositoryError(RuntimeError):
    """Base error for Experience repository operations."""


class ExperienceNotFoundError(ExperienceRepositoryError):
    """Raised when an Experience cannot be found by its identity."""


class ExperienceAlreadyExistsError(ExperienceRepositoryError):
    """Raised when creation would replace an existing Experience."""


class ExperienceRepository(ABC):
    """Storage-independent contract for Core Experience.

    The repository stores and retrieves Experience state.

    Storage is not Experience.
    Persistence is not authority.
    """

    @abstractmethod
    def add(self, experience: Experience) -> None:
        """Store a newly admitted Experience without replacement."""

    @abstractmethod
    def get(self, experience_id: ExperienceId) -> Experience:
        """Return one Experience by stable Experience identity."""

    @abstractmethod
    def save(self, experience: Experience) -> None:
        """Persist the current state of an already admitted Experience."""

    @abstractmethod
    def contains(self, experience_id: ExperienceId) -> bool:
        """Return whether this repository knows the Experience identity."""


class InMemoryExperienceRepository(ExperienceRepository):
    """Minimal repository implementation for Core behavioral tests.

    This implementation is intentionally process-local.

    It does NOT demonstrate persistence across real process death.
    """

    def __init__(self) -> None:
        self._experiences: dict[ExperienceId, Experience] = {}

    def add(self, experience: Experience) -> None:
        if experience.experience_id in self._experiences:
            raise ExperienceAlreadyExistsError(
                f"Experience already exists: {experience.experience_id}"
            )

        self._experiences[experience.experience_id] = experience

    def get(self, experience_id: ExperienceId) -> Experience:
        try:
            return self._experiences[experience_id]
        except KeyError as exc:
            raise ExperienceNotFoundError(
                f"Experience not found: {experience_id}"
            ) from exc

    def save(self, experience: Experience) -> None:
        if experience.experience_id not in self._experiences:
            raise ExperienceNotFoundError(
                f"Cannot save unknown Experience: {experience.experience_id}"
            )

        self._experiences[experience.experience_id] = experience

    def contains(self, experience_id: ExperienceId) -> bool:
        return experience_id in self._experiences
```

### `lib/python/experience/service.py`

```python
"""Application physiology for PCC-01 Core Experience."""

from __future__ import annotations

from .identity import ExperienceId
from .model import Experience
from .repository import ExperienceRepository


class ExperienceService:
    """Coordinates Core Experience behavior.

    The service does not own Experience identity.
    The service does not become Session, Memory, Evidence, or authority.
    """

    def __init__(self, repository: ExperienceRepository) -> None:
        self._repository = repository

    def create_experience(self) -> Experience:
        """Create and admit a new Experience."""
        experience = Experience.create()
        self._repository.add(experience)
        return experience

    def get_experience(self, experience_id: ExperienceId) -> Experience:
        """Inspect an admitted Experience by stable identity."""
        return self._repository.get(experience_id)

    def activate_experience(
        self,
        experience_id: ExperienceId,
    ) -> Experience:
        """Activate an admitted Experience while preserving identity."""
        current = self._repository.get(experience_id)
        active = current.activate()
        self._repository.save(active)
        return active

    def close_experience(
        self,
        experience_id: ExperienceId,
    ) -> Experience:
        """Close an active Experience while preserving identity."""
        current = self._repository.get(experience_id)
        closed = current.close()
        self._repository.save(closed)
        return closed
```

### `lib/python/experience/session_binding.py`

```python
"""Explicit Session-to-Experience binding for PCC-01.

This module defines relational tissue only.

It does not define Session itself and does not alter Experience.

Epistemic boundaries:

    Experience != Session
    Experience != Memory
    Experience != Evidence
    Experience != raw dialogue
    Session != process
    Session != provider
    Storage != Experience
    Interpretation != historical fact
    Persistence != authority
    Human Acceptance != Implementation
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import NewType

from .identity import ExperienceId


SessionId = NewType("SessionId", str)


class SessionBindingError(ValueError):
    """Base error for invalid Session/Experience binding operations."""


class InvalidSessionIdError(SessionBindingError):
    """Raised when a Session identity is invalid."""


class InvalidExperienceBindingError(SessionBindingError):
    """Raised when an Experience identity is invalid for binding."""


def normalize_session_id(value: str) -> SessionId:
    """Validate and normalize an external Session identity."""

    if not isinstance(value, str):
        raise InvalidSessionIdError("session_id must be a string")

    normalized = value.strip()

    if not normalized:
        raise InvalidSessionIdError("session_id must not be empty")

    return SessionId(normalized)


def validate_experience_id(value: ExperienceId) -> ExperienceId:
    """Require the established Core Experience identity type.

    Session Binding consumes ExperienceId exactly as defined by the
    Experience organ.  It does not convert Experience identity into
    Session identity or replace it with a parallel representation.
    """

    if not isinstance(value, ExperienceId):
        raise InvalidExperienceBindingError(
            "experience_id must be an ExperienceId"
        )

    return value


@dataclass(frozen=True, slots=True)
class SessionBinding:
    """Relationship between one Session identity and one Experience identity.

    The binding owns neither organ and owns neither lifecycle.
    """

    session_id: SessionId
    experience_id: ExperienceId

    @classmethod
    def create(
        cls,
        *,
        session_id: str,
        experience_id: ExperienceId,
    ) -> "SessionBinding":
        return cls(
            session_id=normalize_session_id(session_id),
            experience_id=validate_experience_id(experience_id),
        )

    def belongs_to_experience(self, experience_id: ExperienceId) -> bool:
        """Return whether this binding references the supplied Experience."""

        if not isinstance(experience_id, ExperienceId):
            return False

        return self.experience_id == experience_id

    def belongs_to_session(self, session_id: str) -> bool:
        """Return whether this binding references the supplied Session."""

        try:
            normalized = normalize_session_id(session_id)
        except InvalidSessionIdError:
            return False

        return self.session_id == normalized
```

## 11. Current Core Experience Behavioral Baseline

```text
......................................................                   [100%]
54 passed in 0.41s
PASS: existing Core Experience behavior remains healthy
```

## 12. Protection Construction Questions


RUN 013 deliberately does NOT answer these questions by assumption.

The report provides evidence for GPT/Human inspection of:

1. Which existing tissue, if any, qualifies as **MOȘTENIM**?
2. Which existing tissue requires **ADAPTĂM**?
3. Which Protection tissue must be **CONSTRUIM NOU**?
4. Which superficially similar tissue must be **NU FOLOSIM**?
5. What exactly is being protected: Experience identity, lifecycle legality, repository behavior, or another boundary?
6. Which mutations are legitimate physiological development and which are prohibited injury/corruption?
7. Where must authority be checked without making persistence equal authority?
8. Which protection rules belong now and which belong to later Retention / Forgetting / Evidence phases?
9. How will Protection preserve Session != Experience?
10. Which behaviors require explicit tests before conservation?

## 13. Mandatory Epistemic Boundaries


- Experience != Session
- Experience != Memory
- Experience != Evidence
- Experience != raw dialogue
- Session != process
- Session != provider
- Storage != Experience
- Interpretation != historical fact
- Persistence != authority
- Human Acceptance != Implementation

## 14. Central Identity Invariant


`ID_before_restart == ID_after_restart`

RUN 013 does not demonstrate this invariant.

No real process death or process restart occurs in this inspection.

## 15. PCC-01 Epistemic Status


**Implementation Status:** NOT DEMONSTRATED

**Canonical Status:** NOT CANON

**Production Status:** NOT PRODUCTION-READY

## 16. Mutation Boundary


RUN 013 created or modified only:

- `work/implementation-reports/PCC-01/PCC-01_PROTECTION_PRE_IMPLEMENTATION_INSPECTION_RUN_013.md`

It did not modify software.

It did not modify tests.

It did not modify accepted specifications.

It did not modify Canon.

## 17. Final Repository State

```text
?? work/implementation-reports/PCC-01/PCC-01_PROTECTION_PRE_IMPLEMENTATION_INSPECTION_RUN_013.md

PASS: RUN 013 is the only working-tree artifact
```

## 18. Report Integrity

```text
Bytes before final marker: 134252
Lines before final marker: 2049
```

## 19. Final Result


**RUN 013: PASS**

**Protection software constructed:** NO

**Repository software modified:** NO

**NEXT REQUIRED ACTION:** GPT inspection and classification of Protection tissue before implementation.

---

END OF PCC-01 PROTECTION PRE-IMPLEMENTATION INSPECTION — RUN 013

# PCC-01 — CORE EXPERIENCE IMPLEMENTATION SPECIFICATION

**Capability:** PCC-01 — Persistent Experience  
**Milestone:** PCC-01 CORE EXPERIENCE  
**Document Type:** Pre-Implementation Software Specification  
**Date:** 2026-08-13  
**Human Authority:** Owner  
**Implementation Status:** NOT DEMONSTRATED  
**Canonical Status:** NOT CANON  
**Production Status:** NOT PRODUCTION-READY  
**Human Acceptance:** REQUIRED BEFORE IMPLEMENTATION

---

## 1. Purpose

This document specifies the first executable organ of PCC-01 — Persistent Experience.

The milestone defined here is:

**PCC-01 CORE EXPERIENCE**

It establishes the minimum software anatomy required for an Experience to exist as a first-class domain entity inside AI-Toolkit.

This specification does not claim that PCC-01 is implemented.

It does not claim that Persistent Experience has been demonstrated.

It does not modify Canon.

It defines the software contract that must be accepted by the Human Authority before implementation begins.

---

## 2. Epistemic Position

PCC-01 currently remains:

**Implementation Status: NOT DEMONSTRATED**

**Canonical Status: NOT CANON**

**Production Status: NOT PRODUCTION-READY**

The existence of this specification does not change those states.

Specification is not implementation.

Implementation is not behavioral proof.

Passing unit tests is not production readiness.

Persistence is not authority.

Human Acceptance is not Implementation.

---

## 3. Organism Analogy

AI-Toolkit is software.

The organism terminology used by this project is an architectural and explanatory model.

For PCC-01:

- Experience Model represents the anatomy of an Experience;
- Experience Identity represents its persistent identity;
- Experience Lifecycle represents its physiological state transitions;
- Experience Repository represents controlled conservation and retrieval;
- Experience Service coordinates the Core Experience organ.

These analogies do not assert biological properties of software.

---

## 4. Core Experience Scope

The Core Experience milestone contains exactly these conceptual components:

1. Experience Model;
2. Experience Identity;
3. Experience Lifecycle;
4. Experience Repository;
5. Experience Service;
6. Core Experience tests.

This milestone establishes the organ.

It does not yet establish the complete physiology of Persistent Experience.

---

## 5. Mandatory Epistemic Boundaries

Implementation MUST preserve all ten PCC-01 boundaries:

1. Experience != Session
2. Experience != Memory
3. Experience != Evidence
4. Experience != raw dialogue
5. Session != process
6. Session != provider
7. Storage != Experience
8. Interpretation != historical fact
9. Persistence != authority
10. Human Acceptance != Implementation

No implementation convenience may collapse these boundaries.

---

## 6. Central Identity Invariant

The final PCC-01 capability must demonstrate:

**ID_before_restart == ID_after_restart**

Core Experience MUST be designed so that this invariant can later be demonstrated across real process death and process restart.

This specification does NOT claim that the invariant has already been demonstrated.

Core unit tests MUST NOT be presented as proof of real restart continuity.

---

## 7. Core Architectural Principle

Core Experience is a new domain organ.

It MUST NOT be implemented as:

- a renamed Session;
- a renamed Memory record;
- a renamed Evidence artifact;
- a raw dialogue transcript;
- a storage path;
- a process identifier;
- a provider identifier.

Existing neighboring organs may later be integrated through explicit boundaries and adapters.

---

## 8. Construction Classification

For this milestone:

| Component | Classification |
|---|---|
| Experience Core | CONSTRUIM NOU |
| Experience Model | CONSTRUIM NOU |
| Experience Identity | CONSTRUIM NOU |
| Experience Lifecycle | CONSTRUIM NOU |
| Experience Repository | CONSTRUIM NOU |
| Experience Service | CONSTRUIM NOU |

Neighboring infrastructure is not automatically replaced.

Reuse before duplication.

Inherit before replacing.

Integrate; do not collapse.

---

## 9. Proposed Software Package

The Core Experience organ SHOULD be isolated as its own Python package.

Target package:

`lib/python/experience/`

Initial package anatomy:

`lib/python/experience/__init__.py`

`lib/python/experience/model.py`

`lib/python/experience/identity.py`

`lib/python/experience/lifecycle.py`

`lib/python/experience/repository.py`

`lib/python/experience/service.py`

`lib/python/experience/errors.py`

No Session, Memory, Evidence, retention, forgetting or protection implementation belongs inside these modules merely for convenience.

---

## 10. Test Package

Core behavioral tests SHOULD live independently from implementation code.

Initial test anatomy:

`tests/experience/test_experience_model.py`

`tests/experience/test_experience_identity.py`

`tests/experience/test_experience_lifecycle.py`

`tests/experience/test_experience_repository.py`

`tests/experience/test_experience_service.py`

`tests/experience/test_experience_boundaries.py`

These are Core Experience tests.

They are not yet PCC-01 final acceptance Evidence.

---

## 11. Experience Model Responsibility

Experience Model defines what an Experience is at the software-domain level.

It MUST:

- represent one Experience;
- possess exactly one Experience identity;
- possess an explicit lifecycle state;
- contain minimum creation metadata;
- remain independent from Session identity;
- remain independent from Memory identity;
- remain independent from Evidence identity;
- remain serializable without becoming equivalent to its serialized representation.

The model MUST NOT perform repository I/O.

The model MUST NOT own process lifecycle.

The model MUST NOT declare authority.

---

## 12. Minimum Experience Data

The initial Experience representation MUST contain at least:

- `experience_id`;
- `created_at`;
- `state`.

The implementation MAY contain additional internal versioning metadata where required for safe serialization.

Additional fields MUST NOT silently introduce Session, Memory, Evidence, Provenance, authority, retention or protection semantics before their respective phases.

---

## 13. Experience ID

`experience_id` is the stable identifier of one Experience.

It MUST:

- be created once;
- be immutable after creation;
- be serializable;
- survive repository save/load;
- remain identical after reconstruction from persisted representation;
- be independent from Session identifiers;
- be independent from process identifiers;
- be independent from provider identifiers;
- be independent from storage filenames.

The ID identifies the Experience.

The ID is not the Experience itself.

---

## 14. Identity Creation

A new Experience receives a new identity only during explicit creation.

Loading an existing Experience MUST NOT generate a replacement identity.

Recovery of an existing Experience MUST NOT generate a replacement identity.

Deserialization MUST preserve the stored Experience identity.

---

## 15. Identity Uniqueness

Two independently created Experiences MUST receive distinct identities.

Therefore:

`Experience_A.experience_id != Experience_B.experience_id`

unless both objects are explicitly representations of the same persisted Experience.

---

## 16. Identity Stability

For one Experience:

`ID_at_creation == ID_after_save_load`

must hold at the repository boundary.

Later PCC-01 phases must extend this behavioral proof to:

`ID_before_restart == ID_after_restart`

across real process death.

---

## 17. Identity Immutability

The public domain contract MUST NOT permit arbitrary mutation of `experience_id`.

An Experience whose identity changes becomes a different Experience and MUST NOT be silently treated as continuity of the original.

---

## 18. Experience Lifecycle Responsibility

Experience Lifecycle defines the allowed physiological states of Core Experience.

Lifecycle logic MUST be explicit.

Lifecycle behavior MUST NOT be inferred from file existence, directory placement or process state.

---

## 19. Initial Lifecycle States

Core Experience MUST initially define at least:

**CREATED**

**ACTIVE**

**CLOSED**

These states belong to the Core Experience milestone.

Future phases MAY extend lifecycle semantics for retention, archival, forgetting, conflict or protection.

Those future semantics MUST NOT be fabricated in this milestone.

---

## 20. CREATED State

`CREATED` means:

the Experience has been admitted into the Core Experience domain and possesses a valid identity but has not yet entered active operation.

Creation does not imply:

- persistence;
- Session binding;
- Evidence;
- authority;
- Canon;
- production readiness.

---

## 21. ACTIVE State

`ACTIVE` means:

the Experience is currently permitted to participate in later Experience operations.

ACTIVE does not mean:

- current process;
- current Session;
- provider connection;
- human approval;
- canonical authority.

---

## 22. CLOSED State

`CLOSED` means:

the Core Experience lifecycle has been explicitly closed.

CLOSED does not mean:

- forgotten;
- deleted;
- archived;
- invalid;
- rejected;
- non-existent.

Retention and forgetting semantics belong to later phases.

---

## 23. Initial Lifecycle Transitions

The initial legal transition graph is:

`CREATED -> ACTIVE`

`ACTIVE -> CLOSED`

No other transition is legal unless explicitly introduced by an accepted later specification.

---

## 24. Illegal Lifecycle Transitions

At minimum, Core Experience MUST reject:

`CREATED -> CLOSED`

`ACTIVE -> CREATED`

`CLOSED -> ACTIVE`

`CLOSED -> CREATED`

and self-transitions unless explicitly required by later accepted behavior.

Illegal transitions MUST produce explicit domain errors.

They MUST NOT silently succeed.

---

## 25. Lifecycle Determinism

Given:

- the current valid lifecycle state;
- the requested transition;

the lifecycle component MUST deterministically either:

1. return/produce the valid next state; or
2. reject the transition with an explicit lifecycle error.

---

## 26. Lifecycle Independence

Experience lifecycle MUST NOT be determined by:

- whether a Session exists;
- whether a process is alive;
- whether a provider is connected;
- whether a storage file exists;
- whether Evidence exists.

Those are separate concerns.

---

## 27. Experience Repository Responsibility

Experience Repository defines the conservation boundary for Core Experience.

It provides domain-oriented save/load behavior.

Repository is not Experience.

Storage is not Experience.

---

## 28. Repository Contract

The Core Experience Repository MUST provide behavior equivalent to:

- save an Experience;
- load an Experience by Experience ID;
- determine whether an Experience exists by Experience ID.

The exact Python method names may follow repository conventions discovered in the existing codebase, provided these semantics remain unchanged.

---

## 29. Repository Save Semantics

Saving MUST preserve:

- Experience ID;
- creation metadata;
- lifecycle state;
- supported serialization version metadata.

Saving MUST NOT silently create a new Experience identity.

---

## 30. Repository Load Semantics

Loading by Experience ID MUST either:

1. reconstruct the corresponding Experience with the same identity and state; or
2. return/raise an explicit not-found domain result/error.

Loading MUST NOT fabricate an Experience when none exists.

---

## 31. Repository Identity Invariant

For an Experience `E`:

`E.experience_id == repository.load(E.experience_id).experience_id`

MUST hold after successful save/load.

This proves repository identity preservation.

It does NOT yet prove real process restart continuity.

---

## 32. Repository Serialization Boundary

Serialization is a representation of Experience.

Serialization is not Experience.

The repository MAY serialize the model into a deterministic structured representation.

The representation MUST preserve enough information to reconstruct the Core Experience without generating a new identity.

---

## 33. Serialization Requirements

Core serialization MUST preserve at least:

- schema/version marker where required;
- `experience_id`;
- `created_at`;
- lifecycle `state`.

Serialization MUST NOT embed arbitrary runtime objects.

Serialization MUST NOT depend on live process memory for reconstruction.

---

## 34. Storage Boundary

The physical storage mechanism is an implementation detail behind Experience Repository.

A filename is not an Experience identity.

A directory is not an Experience.

A serialized record is not authority.

The repository abstraction MUST prevent higher-level services from depending unnecessarily on storage layout.

---

## 35. Repository Implementation Strategy

The first Core Experience repository SHOULD use the simplest deterministic storage strategy compatible with the repository's existing architecture.

Before implementation, existing repository/storage infrastructure MUST be reused where behaviorally compatible.

Compatibility MUST be demonstrated from behavior and contracts.

It MUST NOT be inferred from filenames alone.

If existing infrastructure cannot satisfy the Experience Repository contract without collapsing epistemic boundaries, a dedicated repository implementation MUST be used.

---

## 36. Experience Service Responsibility

Experience Service coordinates Core Experience use cases.

It is the physiological coordinator of the first Experience organ.

It MUST NOT absorb the responsibilities of all future PCC-01 organs.

---

## 37. Service Core Operations

The Core Experience Service MUST provide behavior equivalent to:

- create Experience;
- activate Experience;
- close Experience;
- get/load Experience.

Exact method names may follow repository conventions if semantics remain explicit.

---

## 38. Service Creation Semantics

Creating an Experience through the service MUST:

1. generate exactly one new Experience identity;
2. create the Experience in `CREATED` state;
3. assign creation metadata;
4. return the new Experience.

Whether creation immediately persists the Experience MUST be explicit in implementation and tests.

It MUST NOT happen ambiguously.

---

## 39. Service Activation Semantics

Activation MUST:

1. obtain the target Experience;
2. validate that its current state permits activation;
3. transition `CREATED -> ACTIVE`;
4. preserve Experience identity;
5. persist the resulting state when repository-backed operation is used;
6. return the resulting Experience.

---

## 40. Service Closure Semantics

Closure MUST:

1. obtain the target Experience;
2. validate that its current state permits closure;
3. transition `ACTIVE -> CLOSED`;
4. preserve Experience identity;
5. persist the resulting state when repository-backed operation is used;
6. return the resulting Experience.

---

## 41. Service Retrieval Semantics

Retrieval MUST load an existing Experience through the repository boundary.

Retrieval MUST NOT create a new Experience as a fallback for missing data.

Missing Experience and new Experience are different conditions.

---

## 42. Dependency Direction

Core dependencies SHOULD flow conceptually as:

`Experience Service`
↓
`Experience Repository`
↓
`serialization/storage`

and:

`Experience Service`
↓
`Experience Lifecycle`

with:

`Experience Model`
+
`Experience Identity`

forming the central domain anatomy.

Infrastructure MUST depend on domain contracts rather than forcing storage semantics into the domain model where practical.

---

## 43. Session Boundary

Session is explicitly outside Core Experience.

Core Experience MUST NOT require a Session to exist.

An Experience MUST be constructible and testable independently of Session.

Later Session Binding MUST associate identities without collapsing them.

Future relation:

`Experience ID != Session ID`

---

## 44. Memory Boundary

Memory is explicitly outside Core Experience.

Experience MUST NOT inherit Memory identity.

Experience MUST NOT become a Memory record merely because it can persist.

Memory integration belongs to a later phase.

---

## 45. Evidence Boundary

Evidence is explicitly outside Core Experience.

Core unit tests may produce test results.

Those results are not automatically PCC-01 acceptance Evidence.

Evidence integration is a later explicit phase.

---

## 46. Provenance Boundary

Provenance integration is outside this Core milestone.

Core Experience MUST be designed so provenance can later be associated without rewriting Experience identity semantics.

No provenance fact may be fabricated merely to populate a field.

---

## 47. Raw Dialogue Boundary

Raw dialogue is not Experience.

Core Experience MUST NOT define an Experience as an unprocessed conversation transcript.

Later candidate/admission logic may derive or associate Experience information from dialogue.

That future transformation must remain explicit and traceable.

---

## 48. Interpretation Boundary

Interpretation is not historical fact.

Core Experience MUST NOT silently convert interpretations into factual historical attributes.

Future provenance/conflict/ambiguity layers must represent this distinction explicitly.

---

## 49. Authority Boundary

Persistence does not grant authority.

An Experience being stored does not make its content:

- Canon;
- accepted;
- correct;
- verified;
- authoritative.

Authority remains governed separately.

Human Authority remains with the Owner where Human Acceptance is required.

---

## 50. Process Boundary

Experience identity MUST NOT be derived from process identity.

A process may die.

The Experience identity must remain capable of surviving that death through later persistence/recovery phases.

---

## 51. Provider Boundary

Experience identity MUST NOT be derived from an AI provider.

Changing provider must not logically create a different Experience solely because the provider changed.

Provider integration is outside Core Experience.

---

## 52. Protection Against Concept Collapse

Implementation review MUST reject any design where:

- Experience subclasses Session merely to reuse identity;
- Experience aliases Memory;
- Experience aliases Evidence;
- Experience ID equals process ID;
- Experience ID equals Session ID by definition;
- storage location is treated as Experience identity;
- persisted data is treated as authoritative because it persisted;
- dialogue is stored and called Experience without explicit admission semantics.

---

## 53. Error Model

Core Experience MUST define explicit domain errors.

At minimum:

`ExperienceError`

`ExperienceIdentityError`

`ExperienceLifecycleError`

`ExperienceNotFoundError`

`ExperienceRepositoryError`

Errors SHOULD preserve the distinction between:

- invalid domain state;
- missing Experience;
- malformed identity;
- persistence/repository failure.

---

## 54. Error Non-Fabrication Rule

Errors MUST NOT be hidden by fabricating substitute Experiences.

For example:

a failed load MUST NOT create a new Experience with a new UUID and return it as if recovery succeeded.

That would destroy identity continuity.

---

## 55. Experience Model Invariants

The model MUST maintain:

1. Experience ID exists;
2. Experience ID is valid;
3. Experience ID is immutable through normal domain operations;
4. creation time exists;
5. lifecycle state is valid;
6. Session identity is not required;
7. Memory identity is not required;
8. Evidence identity is not required.

---

## 56. Identity Invariants

Identity MUST maintain:

1. creation generates a valid identity;
2. independent creations generate distinct identities;
3. load does not regenerate identity;
4. lifecycle transitions do not modify identity;
5. serialization round-trip preserves identity;
6. repository round-trip preserves identity.

---

## 57. Lifecycle Invariants

Lifecycle MUST maintain:

1. every Experience has exactly one current Core lifecycle state;
2. transitions are explicit;
3. illegal transitions fail explicitly;
4. transitions preserve Experience ID;
5. lifecycle does not depend on process liveness;
6. lifecycle does not imply authority.

---

## 58. Repository Invariants

Repository MUST maintain:

1. save/load identity preservation;
2. save/load lifecycle preservation;
3. explicit not-found behavior;
4. no identity regeneration on load;
5. no silent replacement of an existing Experience with another identity;
6. storage representation remains behind repository boundary.

---

## 59. Service Invariants

Service MUST maintain:

1. one creation request produces one new Experience identity;
2. activation preserves identity;
3. closure preserves identity;
4. retrieval preserves identity;
5. illegal lifecycle operations are rejected;
6. missing Experience is not silently recreated.

---

## 60. Timestamp Semantics

`created_at` MUST represent Experience creation time.

It MUST NOT be silently replaced on load.

It MUST NOT become process-start time.

It MUST NOT become Session-start time unless those events happen to coincide and remain separately represented.

A deterministic timezone-aware representation SHOULD be used.

---

## 61. Serialization Versioning

If persisted Core Experience records require a schema marker, that marker MUST be explicit.

Future schema evolution MUST NOT silently reinterpret incompatible historical records.

Unsupported representations SHOULD fail explicitly until a migration contract exists.

---

## 62. Creation Versus Recovery

Creation and recovery are distinct operations.

Creation:

`nothing -> new Experience + new Experience ID`

Recovery:

`persisted existing Experience -> reconstructed same Experience + same Experience ID`

Recovery MUST NEVER silently execute creation semantics.

---

## 63. Loading Versus Recovery

Core Repository load is a prerequisite for later recovery behavior.

A successful load proves that a persisted representation can reconstruct the domain object.

It does not alone prove recovery across real process death.

Real restart recovery belongs to a subsequent PCC-01 phase.

---

## 64. Core Persistence Boundary

The Repository milestone introduces enough persistence behavior to test deterministic save/load.

This is not yet the complete PCC-01 persistence/recovery demonstration.

The later restart harness MUST start a genuinely new process and recover the Experience from durable state.

---

## 65. Future Restart Harness Requirement

A later PCC-01 phase MUST provide a harness that:

1. creates an Experience;
2. records its Experience ID;
3. persists it;
4. terminates the originating process;
5. starts a new process;
6. loads/recover the Experience;
7. obtains the recovered Experience ID;
8. compares both IDs.

Acceptance condition:

`ID_before_restart == ID_after_restart`

No in-memory object from the first process may be used to satisfy the comparison.

---

## 66. Core Test — Model Creation

Test MUST demonstrate that a valid Experience can be created with:

- Experience ID;
- creation timestamp;
- `CREATED` state.

The test MUST demonstrate no Session is required.

---

## 67. Core Test — Identity Uniqueness

Create two independent Experiences.

Assert:

`experience_a.experience_id != experience_b.experience_id`

---

## 68. Core Test — Identity Immutability

Attempt prohibited identity mutation through the supported public API.

The domain contract MUST prevent or explicitly reject it.

---

## 69. Core Test — Lifecycle Activation

Create Experience.

Transition:

`CREATED -> ACTIVE`

Assert:

- state becomes ACTIVE;
- Experience ID remains unchanged.

---

## 70. Core Test — Lifecycle Closure

Create and activate Experience.

Transition:

`ACTIVE -> CLOSED`

Assert:

- state becomes CLOSED;
- Experience ID remains unchanged.

---

## 71. Core Test — Illegal Lifecycle Transitions

Tests MUST cover all initial prohibited transitions.

Each MUST fail explicitly with the expected domain error.

---

## 72. Core Test — Serialization Round Trip

Serialize and reconstruct an Experience.

Assert preservation of:

- Experience ID;
- creation timestamp;
- lifecycle state.

This test MUST NOT be described as process-restart Evidence.

---

## 73. Core Test — Repository Save/Load

Create Experience.

Save.

Load using Experience ID.

Assert:

`created.experience_id == loaded.experience_id`

and equivalent supported Core state.

---

## 74. Core Test — Repository Not Found

Request an unknown valid Experience ID.

Assert explicit not-found behavior.

Assert that no substitute Experience is created.

---

## 75. Core Test — Service Creation

Call Core Experience Service creation.

Assert:

- exactly one Experience is returned;
- it has a valid identity;
- it begins in CREATED;
- retrieval semantics behave according to the selected persistence contract.

---

## 76. Core Test — Service Activation

Through Experience Service:

create -> activate.

Assert identity preservation and ACTIVE state.

---

## 77. Core Test — Service Closure

Through Experience Service:

create -> activate -> close.

Assert identity preservation and CLOSED state.

---

## 78. Core Test — Boundary Independence

Tests MUST demonstrate that Core Experience can operate without importing or constructing:

- Session runtime objects;
- Memory records;
- Evidence records.

This protects the first three epistemic boundaries structurally and behaviorally.

---

## 79. Core Test — Storage Is Not Identity

Where a file-backed repository is used, test behavior MUST demonstrate that Experience identity is read from domain data and is not inferred solely from an arbitrary runtime object identity.

Storage naming may use Experience ID for deterministic addressing.

That naming convention does not redefine identity semantics.

---

## 80. Core Test — Missing Data Does Not Become New Experience

Attempt to retrieve a non-existing Experience.

Assert:

- explicit failure/not-found;
- no newly generated Experience ID;
- no persisted substitute record.

---

## 81. Core Acceptance Criterion — Anatomy

Core Experience passes the anatomy criterion when all five required components exist with explicit responsibilities:

- Model;
- Identity;
- Lifecycle;
- Repository;
- Service.

Existence alone is insufficient for PCC-01 final implementation status.

---

## 82. Core Acceptance Criterion — Behavior

Core Experience passes its behavioral milestone when tests demonstrate:

- creation;
- identity uniqueness;
- identity stability through Core operations;
- legal lifecycle transitions;
- rejection of illegal transitions;
- repository save/load;
- service coordination;
- explicit not-found behavior;
- preservation of required boundaries.

---

## 83. Core Acceptance Criterion — Identity

The Core milestone MUST demonstrate:

`ID_at_creation == ID_after_repository_round_trip`

This is necessary but not sufficient for final PCC-01.

Final PCC-01 still requires:

`ID_before_restart == ID_after_restart`

across real process death.

---

## 84. Core Acceptance Criterion — Boundary Preservation

No Core implementation may require conceptual equivalence between Experience and:

- Session;
- Memory;
- Evidence;
- raw dialogue;
- storage.

If tests pass only by collapsing one of these concepts, the milestone fails.

---

## 85. Core Acceptance Criterion — Existing Organ Compatibility

Before reusing existing repository/storage components, implementation review MUST establish behavioral compatibility.

The criterion is:

**test behavior; do not infer from filenames**

Existing code with a suitable name but incompatible semantics MUST NOT be treated as compatible.

---

## 86. Explicitly Out of Scope — Session Binding

Session Binding is NOT implemented in this milestone.

A later phase will associate Experience and Session while preserving distinct identities.

---

## 87. Explicitly Out of Scope — Provenance

Provenance integration is NOT implemented in this milestone.

No artificial provenance values may be invented to make Core Experience appear complete.

---

## 88. Explicitly Out of Scope — Protection

Experience Protection is NOT implemented in this milestone.

Protection belongs after the Core organ exists and before the complete persistence/recovery acceptance loop.

---

## 89. Explicitly Out of Scope — Retention

Retention behavior is NOT implemented in this milestone.

CLOSED does not mean archived.

---

## 90. Explicitly Out of Scope — Forgetting

Forgetting behavior is NOT implemented in this milestone.

CLOSED does not mean forgotten.

Delete does not automatically mean epistemic forgetting.

Those distinctions require later explicit specification.

---

## 91. Explicitly Out of Scope — Conflict and Ambiguity

Conflict and ambiguity representation are NOT implemented in this milestone.

Future phases MUST represent uncertainty rather than fabricate certainty.

---

## 92. Explicitly Out of Scope — Evidence Integration

Evidence integration is NOT implemented in this milestone.

Test output is not automatically acceptance Evidence.

Evidence must later be deliberately materialized and inspected.

---

## 93. Explicitly Out of Scope — Human Acceptance of Implementation

Human Acceptance of this specification authorizes only the defined implementation work.

It does NOT mean:

- implementation exists;
- tests pass;
- Evidence exists;
- PCC-01 is IMPLEMENTED;
- PCC-01 is production-ready;
- PCC-01 is Canon.

---

## 94. Explicitly Out of Scope — Canonization

This specification does not modify Canon.

PCC-01 remains NOT CANON.

Any future canonization requires an explicit Human Authority gate.

---

## 95. Explicitly Out of Scope — Production Readiness

No result from the Core milestone alone may produce:

`Production Status: PRODUCTION-READY`

Production readiness requires later integration, behavioral Evidence and explicit evaluation.

---

## 96. Implementation Order

After Human Acceptance of this specification, implementation MUST proceed in this order:

1. establish Core Experience package;
2. Experience Model;
3. Experience Identity;
4. Experience Lifecycle;
5. Experience Repository;
6. Experience Service;
7. Core tests;
8. inspect results.

Only after Core Experience is demonstrated may subsequent PCC-01 phases proceed according to the accepted build plan.

---

## 97. Subsequent PCC-01 Order

After Core Experience:

1. restart harness;
2. recovery test;
3. Session Binding;
4. provenance integration;
5. protection;
6. retention;
7. forgetting;
8. conflict/ambiguity;
9. Evidence integration;
10. acceptance run;
11. Human Evaluation.

This specification does not authorize skipping directly to those stages.

---

## 98. No Architectural Guessing Rule

Implementation MUST follow this specification and the accepted PCC-01 contract/build plan.

Where the repository exposes a genuine unresolved compatibility question, implementation MUST stop at that boundary and inspect behavior.

It MUST NOT silently invent architectural authority.

---

## 99. Reuse Rule

Before creating infrastructure already present elsewhere in AI-Toolkit:

1. inspect existing behavior;
2. compare its contract with this specification;
3. reuse if behaviorally compatible;
4. adapt through a boundary if partially compatible;
5. construct new tissue only when necessary.

**reuse before duplication**

---

## 100. Inheritance Rule

Existing organs remain valid unless explicitly superseded through accepted architectural authority.

Core Experience MUST integrate with the organism rather than replace neighboring organs merely because PCC-01 is newer.

**inherit before replacing**

---

## 101. Integration Rule

The goal is not to merge all epistemic concepts into one universal object.

The goal is coordinated physiology between distinct organs.

**integrate; do not collapse**

---

## 102. Behavioral Evidence Rule

Names, directories, class names and comments do not prove behavior.

Implementation decisions involving existing components MUST be supported by executable behavior, contracts or direct code inspection.

**test behavior; do not infer from filenames**

---

## 103. Uncertainty Rule

If existing repository behavior is ambiguous:

- mark the ambiguity;
- inspect it;
- test it;
- resolve it explicitly.

Do not fabricate certainty merely to continue implementation.

**represent uncertainty; do not fabricate certainty**

---

## 104. Human Authority Rule

The Human Authority for this gate is:

**Owner**

Only the Human Authority may accept or reject this implementation specification.

GPT may propose, inspect, implement after authorization and produce Evidence.

GPT may not self-declare Human Acceptance.

---

## 105. Specification Acceptance Gate

Before software implementation begins, the Owner must explicitly decide whether this document is accepted.

Required decision:

**PCC-01 CORE EXPERIENCE IMPLEMENTATION SPECIFICATION ACCEPTED**

or

**PCC-01 CORE EXPERIENCE IMPLEMENTATION SPECIFICATION REJECTED**

No implementation begins before this gate is resolved.

---

## 106. Post-Acceptance Conservation

If accepted:

1. normalize the specification deterministically if required;
2. verify its structural integrity;
3. calculate SHA-256;
4. create a Human Acceptance record;
5. verify the Human Acceptance record;
6. conserve specification and acceptance according to the established Git workflow;
7. confirm local HEAD and `origin/main` synchronization.

Only after conservation may Core Experience software construction begin.

---

## 107. Traceability Chain

The implementation must remain traceable through:

Research  
-> Reconciliation  
-> Human Acceptance  
-> Implementation Contract  
-> Human Acceptance  
-> Inventory and Build Plan  
-> Human Acceptance  
-> Pre-Implementation Inspection  
-> Core Experience Implementation Specification  
-> Human Acceptance  
-> Software  
-> Tests  
-> Evidence  
-> Human Decision

No later artifact may retroactively convert an earlier research artifact into Canon without explicit authority.

---

## 108. Core Milestone Success Statement

The Core Experience milestone succeeds only when executable behavior demonstrates that AI-Toolkit possesses a distinct Experience domain organ with:

- stable identity;
- explicit lifecycle;
- deterministic conservation/retrieval;
- coordinated service behavior;
- preserved epistemic boundaries.

This success does NOT yet mean PCC-01 Persistent Experience is fully implemented.

---

## 109. PCC-01 Final Success Constraint

The final capability cannot succeed merely because:

- an Experience class exists;
- a UUID exists;
- a file exists;
- save/load works;
- unit tests pass.

Persistent Experience ultimately requires the organism to preserve an identifiable Experience across genuine process death and process restart without confusing it with Session, Memory or Evidence.

Required final invariant:

**ID_before_restart == ID_after_restart**

That demonstration remains future work.

---

## 110. Current Status After This Specification

Even if this specification is Human Accepted, the capability status remains:

**Implementation Status: NOT DEMONSTRATED**

**Canonical Status: NOT CANON**

**Production Status: NOT PRODUCTION-READY**

These statuses may change only through their respective future evidence and authority gates.

---

## 111. Final Declaration

This document specifies the first software organ required by PCC-01.

It defines:

**Experience Model**

**Experience Identity**

**Experience Lifecycle**

**Experience Repository**

**Experience Service**

It deliberately does not collapse:

Experience into Session.

Experience into Memory.

Experience into Evidence.

Experience into raw dialogue.

Storage into Experience.

Persistence into authority.

Human Acceptance into Implementation.

It preserves the future requirement:

**ID_before_restart == ID_after_restart**

without pretending that the invariant has already been demonstrated.

**PCC-01 CORE EXPERIENCE IMPLEMENTATION SPECIFICATION COMPLETE — HUMAN DECISION REQUIRED**

**NEXT GATE: HUMAN ACCEPTANCE OF PCC-01 CORE EXPERIENCE IMPLEMENTATION SPECIFICATION**

---

END OF PCC-01 — CORE EXPERIENCE IMPLEMENTATION SPECIFICATION
PHASE X — SEMANTIC IDENTITY, MANIFESTATION & CROSS-ORGAN RESOLUTION AUDIT

A. Research Question

Phase IX established that UEM can legitimately become a semantic convergence plane, but not a universal source of truth.

Phase X asks the next necessary question:

> Can AI-Toolkit currently distinguish one semantic entity from its multiple manifestations across CSL, Canon, repository, runtime, Evidence, Memory and Experience — and can it resolve between them without inventing a second universal registry?



The repository-grounded verdict is:

PARTIALLY — LOCAL IDENTITY AND LOCAL RESOLUTION EXIST, BUT CROSS-ORGAN IDENTITY DOES NOT.

AI-Toolkit already has several legitimate identity systems. The missing anatomy is not identity itself and not another mega-registry.

The missing anatomy is a safe way to say:

these manifestations refer to the same semantic entity

while preserving:

their different origins
their different authority
their different time/state
their different physical manifestations


---

B. The Existing Identity Systems

The organism does not currently have one identity system.

It has several.

Canon

CanonicalRepository indexes canonical documents by:

doc.id
filename

and exposes:

get_by_id()
get_by_filename()
get_by_dependency()
dependents_of()

This is already a legitimate semantic resolver for Canon.

UEM

UEM indexes EngObject by:

obj_id

and relationships by source/target IDs. Its current builder derives those identities primarily from CSL SemanticResult.

Canonical Knowledge Graph

The graph uses:

CanonicalNode.id

plus graph edges between those IDs and provenance/source-document metadata.

Repository Engine

Repository anatomy is physically identified primarily by:

path
name

RepositoryItem, ClassifiedFile and RepositoryProfile are path-oriented structures.

Therefore repository identity is currently manifestation identity, not semantic identity.

This distinction is critical.


---

C. Semantic Identity vs Manifestation Identity

We can now define the distinction from actual repository anatomy.

Suppose the concept is:

AIRequestPipeline

Its semantic identity answers:

> What is this thing?



A repository manifestation might answer:

lib/python/ai_platform/...

A canonical manifestation might answer:

document/section describing AIRequestPipeline

A CSL manifestation may answer:

EngObject(obj_id="AIRequestPipeline")

Runtime may eventually answer:

live service/component instance

These are not interchangeable identities.

The correct anatomy is:

SEMANTIC IDENTITY
             AIRequestPipeline
                    │
       ┌────────────┼────────────┐
       ▼            ▼            ▼
     CSL          CANON      REPOSITORY
manifestation   manifestation manifestation

Phase X confirms this model is necessary.


---

D. Canon Already Demonstrates Why Semantic Identity Must Be Independent of Path

CanonicalRepository explicitly supports both:

get_by_id(doc_id)

and:

get_by_filename(filename)

That means its architecture already recognizes two concepts:

Canonical identity
      ≠
filename

A document can therefore conceptually preserve its canonical ID even if its filename changes.

This is an existing precedent for Phase IV invariant I-03:

> Semantic Identity ≠ Physical Location.



We do not need to invent that principle from nothing.

Part of the organism already implements it.


---

E. Repository Engine Does the Opposite — Correctly

Repository Engine's objects are deliberately physical:

RepositoryItem.path
ClassifiedFile.path
RepositoryProfile.path

This is not a defect.

Repository Engine answers:

> What physically exists in this repository?



It should not be forced to answer:

> What eternal semantic entity does this file represent?



Therefore:

RepositoryEngine must remain a manifestation/perception organ.

Trying to add universal semantic identity directly into every repository object would violate its clean responsibility.

Resolution should happen above it.


---

F. UEM Currently Conflates Identity and Manifestation

This is the most important Phase X finding.

Current UEM stores:

EngObject
    obj_id
    source_document
    source_ref
    ast_ref

Conceptually that object is trying to carry both:

WHAT
+
WHERE IT CAME FROM

For CSL-only ingestion this works reasonably well.

For cross-organ convergence it fails.

If:

obj_id = AIRequestPipeline

is used for:

CSL declaration;

canonical definition;

Python class;

runtime component;


then only one object can occupy that dictionary key.

Phase IX already identified last-writer-wins collision.

Phase X can now diagnose the underlying cause:

> UEM lacks a first-class distinction between Semantic Entity and Manifestation.




---

G. We Must Not Solve This With Composite IDs Alone

A tempting solution would be:

csl:AIRequestPipeline
canon:AIRequestPipeline
repository:AIRequestPipeline
runtime:AIRequestPipeline

That prevents collisions.

But it creates another problem:

the organism no longer inherently knows that all four concern:

AIRequestPipeline

We would merely replace:

collision

with:

semantic fragmentation

Therefore two levels are necessary:

semantic_identity
       │
       ├── manifestation_identity A
       ├── manifestation_identity B
       └── manifestation_identity C

This is a genuine missing semantic distinction.


---

H. Existing Resolvers Are Local and Should Stay Local

CanonicalRepository already resolves Canon IDs.

UEM resolves its own objects.

CanonicalKnowledgeGraph resolves graph nodes.

RepositoryEngine can inspect physical repository structures.

Other Phase II–V audits established local resolution/traversal in Memory, Persistent Experience and PCC/FUSION.

The correct future physiology is therefore not:

MegaResolver
   knows every file
   knows every Canon object
   knows every Memory object
   knows every Experience

Instead:

Semantic Identity
       ↓
Resolution Coordination
       ↓
determine domain / manifestation requested
       ↓
delegate
       ├── CanonicalRepository
       ├── UEM
       ├── RepositoryEngine
       ├── KnowledgeGraph
       ├── Memory resolver
       ├── Experience repository
       └── Provenance

This directly validates Phase III's federated-resolution hypothesis.


---

I. Cross-Organ Resolution Is Currently Missing

The inspected CanonicalRepository knows nothing about UEM.

Repository Engine's models know nothing about canonical IDs or UEM identities.

UEM's package itself contains only:

__init__.py
models.py
uem.py

There is no independent cross-organ resolver inside canonical_entities.

And the Phase VIII audit established that KnowledgeMaterialization follows a separate CDM/CSS path.

Therefore:

CROSS-ORGAN RESOLUTION IS NOT CURRENTLY IMPLEMENTED AS A UNIFIED PHYSIOLOGY.

This is no longer hypothetical.


---

J. But We Already Have the Seeds of Resolution

Several existing concepts can be reused.

source_document

Can connect a manifestation to its semantic/document origin.

source_ref

Can identify the current source manifestation.

ast_ref

Intended to preserve some source-semantic connection, though currently underpowered.

Canonical doc.id

Provides stable semantic document identity independent of filename.

Graph source_document

Connects graph structures back to canonical documents.

So we are not missing every connective tissue.

We are missing a consistent cross-organ interpretation of that tissue.


---

K. Manifestation Requires Domain

A manifestation cannot be safely identified merely by path.

It needs at least a domain concept.

Conceptually:

Manifestation

semantic_identity:
    AIRequestPipeline

domain:
    repository

local_identity:
    lib/python/.../pipeline.py::AIRequestPipeline

versus:

Manifestation

semantic_identity:
    AIRequestPipeline

domain:
    canon

local_identity:
    CAN-... / section ...

The domain is important because it tells federated resolution which existing organ owns resolution.

This avoids a mega-index.


---

L. Resolution Must Be Directional

Resolution is not simply:

ID → object

We need at least two different questions.

Semantic → manifestations

AIRequestPipeline
      ↓
Where does it manifest?

Potential result:

CSL
Canon
Repository
Runtime
Evidence

Manifestation → semantic identity

lib/python/.../pipeline.py
      ↓
What semantic entity does this manifest?

These operations have different uncertainty.

The first may return many results.

The second may return:

RESOLVED
AMBIGUOUS
UNRESOLVED

A future contract must not pretend every physical file maps uniquely to one semantic entity.


---

M. Resolution Must Preserve UNKNOWN

Example:

Repository contains:

some_new_component.py

but neither CSL nor Canon knows it.

Correct result:

repository manifestation exists
semantic identity = UNKNOWN / UNRESOLVED

Not:

invent semantic identity from filename

This directly preserves Phase IV invariant I-07.

Likewise if two semantic identities could legitimately map to the same implementation structure:

AMBIGUOUS

must remain valid.


---

N. Identity Confidence Must Not Become Authority

Resolution may use evidence such as:

matching identifier
matching class name
canonical reference
explicit mapping
source reference
relationship topology

But a high-confidence identity match does not mean the retrieved content is Canon.

Example:

repository class
   ↓ 99% resolution confidence
AIRequestPipeline

still means:

epistemic_class = repository observation

not:

CANON

Therefore:

resolution confidence
       ≠
epistemic authority

This should become a hard future invariant.


---

O. Temporal Manifestation

Phase VI raised the question:

> If PCC-01 changes implementation, is it still PCC-01?



Phase X now provides the answer model.

Yes, potentially:

semantic identity
      PCC-01
         │
         ├── manifestation M1
         │      valid T1–T2
         │
         ├── manifestation M2
         │      valid T2–T3
         │
         └── manifestation M3
                CURRENT

Current UEM has:

version
status

but no explicit manifestation lifecycle/time semantics.

Repository Engine similarly models the current repository snapshot, not semantic continuity.

Finding X-01 — CRITICAL

Current semantic models do not fully represent manifestation succession/currentness.

This connects directly to the earlier Temporal & Current-Truth research.


---

P. Physical Location Must Be Replaceable

Suppose:

lib/python/a.py

moves to:

lib/python/platform/a.py

A healthy system should produce:

semantic identity unchanged
manifestation location changed

not:

old semantic entity deleted
new semantic entity created

unless evidence shows that the semantic entity actually changed.

This is exactly why RepositoryEngine cannot be the semantic identity authority.

Its path-centric anatomy is correct for perception, but insufficient for continuity.


---

Q. Multi-Project Identity

Phase VI identified another risk.

Suppose both AI-Toolkit and another project contain:

RepositoryEngine

A globally unqualified identity is insufficient.

We need conceptual scope:

AI-Toolkit::RepositoryEngine

versus:

OtherProject::RepositoryEngine

Current CanonicalRepository is instantiated per loaded document set and therefore obtains scope implicitly from the repository instance.

Current UEM object dictionary has no explicit project/organism namespace in its identity model.

Finding X-02 — HIGH

UEM identity is insufficiently namespaced for future multi-organism convergence.

This must be solved before AI-Toolkit acts as engineering organism over multiple projects.


---

R. Cross-Organ Mapping Must Be Sparse

We should not require every object to have manifestations everywhere.

For example:

semantic identity: Human Authority

may have:

CSL manifestation ✓
Canon manifestation ✓
repository manifestation ✗

Likewise:

temporary runtime socket

may have:

runtime manifestation ✓
Canon ✗
CSL ✗
Memory ✗

That is healthy.

Therefore the model must support:

zero or more manifestations per domain

and never infer that absence from one domain means nonexistence globally.


---

S. Orphan Detection Now Becomes Precisely Definable

Phase VI introduced semantic/materialization orphans.

We can now formalize them conceptually.

Semantic orphan

semantic identity
      ↓
no current manifestations resolvable

Manifestation orphan

repository/runtime manifestation
      ↓
no semantic identity resolvable

Historical orphan

historical manifestation
      ↓
semantic identity still exists
but continuity link missing

Cross-organ orphan

Canon identity
      ↓
expected repository manifestation
      ↓
none found

But this last one is not automatically an error.

It could represent:

planned
deprecated
documentation-only
not-yet-implemented

Authority and lifecycle status must be consulted before classification.


---

T. Resolution Cannot Infer Expected Manifestations Without Semantics

This is subtle but important.

If Canon says:

Requirement R

we cannot automatically demand:

Python file R.py

Semantic type and relationship determine what manifestations are expected.

Thus CSL/UEM's semantic map has an important role:

semantic type
+
relationships
+
status
        ↓
expected manifestation semantics

This makes the future reconciliation auditor much smarter than simple filename matching.


---

U. Current Resolution Capability Matrix

Organ	Local identity	Physical identity	Semantic resolution	Cross-organ resolution

CSL/SemanticResult	YES	source_path	YES/PARTIAL	NO
UEM	YES	source refs	YES local	NO
CanonicalRepository	YES	filename	YES	NO
Canonical KG	YES	source_document	YES local	NO
RepositoryEngine	path-centric	YES	limited	NO
KG V2	path/module	YES	structural	NO
PCC/Provenance	domain-specific	source/provenance	PARTIAL	domain-specific
Memory	domain-specific IDs	repository-specific	local	NO demonstrated
Experience	ExperienceId	persistence manifestation	local	NO demonstrated


The organism has many resolvers but no federation contract.

That exactly confirms Phase III.


---

V. The Minimal Missing Anatomy

We can now answer whether we need a new universal registry.

NO.

We need something much smaller.

Conceptually:

Semantic Identity Association

Its job is only to know or derive:

semantic identity
     ↕
manifestation reference(s)
     ↕
owning organ

It must not contain the knowledge itself.

Then federated resolution becomes:

semantic identity
      ↓
association
      ↓
organ + local identity
      ↓
existing organ resolver
      ↓
actual manifestation

This is a routing/association function, not another knowledge database.


---

W. But Even the Association Must Not Become Authoritative Truth Automatically

How is an association established?

Possible origins:

explicit CSL reference
explicit Canon mapping
derived parser relationship
repository observation
Human-approved mapping
runtime observation
historical reconciliation

These have different epistemic strengths.

Therefore association itself needs provenance.

Example:

AIRequestPipeline
   ↕
repository class X

association_source:
explicit CSL mapping

confidence:
1.0

versus:

association_source:
name heuristic

confidence:
0.62

The second cannot silently become canonical identity.


---

X. Resolution State Model

Phase IV proposed states including:

UNRESOLVED
AMBIGUOUS
FORBIDDEN
STALE

Phase X validates these strongly.

A minimum resolution outcome needs conceptual states:

RESOLVED
UNRESOLVED
AMBIGUOUS
STALE
FORBIDDEN
UNAVAILABLE

Potentially:

HISTORICAL_ONLY

may also be useful, but we should not canonize it yet.

Most importantly:

UNRESOLVED

is not an exception that must always be eliminated.

It is epistemic information.


---

Y. Phase X Identity Invariants

The research now supports the following future invariants:

X-I01 — Semantic Identity ≠ Manifestation Identity

X-I02 — Manifestation Identity Is Organ-Scoped

X-I03 — Physical Location Is Not Semantic Authority

X-I04 — Resolution Confidence ≠ Epistemic Authority

X-I05 — One Semantic Entity May Have Zero, One, or Many Manifestations

X-I06 — One Manifestation May Be Ambiguous Until Evidence Resolves It

X-I07 — Resolution Must Preserve Provenance

X-I08 — Cross-Organ Resolution Must Delegate to Organ-Local Resolvers

X-I09 — UEM Must Not Own Organ Knowledge

X-I10 — Manifestation Replacement Must Not Automatically Create a New Semantic Identity

X-I11 — UNKNOWN/UNRESOLVED Is Valid

X-I12 — Resolution Must Not Promote Observation to Canon

These align with, rather than duplicate, the Phase IV invariants.


---

Z. Phase X Final Verdict

The research produces a decisive result.

AI-Toolkit ALREADY HAS LOCAL IDENTITY AND LOCAL RESOLUTION ANATOMY.

Examples include the explicit separation in CanonicalRepository between canonical doc.id and filename, and Repository Engine's deliberately physical path-based identity.

WHAT IS MISSING IS CROSS-ORGAN SEMANTIC ASSOCIATION AND FEDERATED RESOLUTION.

But that does not justify a mega-registry.

The correct anatomy emerging from the repository is:

SEMANTIC IDENTITY
                        │
                        │
             manifestation associations
                        │
       ┌────────────────┼────────────────┐
       ▼                ▼                ▼
      CSL              CANON         REPOSITORY
       │                │                │
 local resolver    local resolver    local perception
       │                │                │
       └────────────────┼────────────────┘
                        │
                        ▼
              resolved manifestation
                        │
                        ▼
             Epistemic Result Envelope

UEM can provide the semantic identity space and orientation map.

Existing organs retain their own resolution and authority.

A thin federated coordination layer determines which organ should resolve a requested manifestation.

This confirms another important point about CSL:

> CSL does not need to know filesystem locations in order to orient the AI.



It needs to preserve semantic identity and relationships. Resolution can determine the current manifestation later.

That means the original CSL-map hypothesis continues to survive increasingly strict repository inspection.

The next unresolved research frontier

Phase X exposes the next fundamental problem: even if identity and manifestations can be associated, the organism still needs to determine which manifestation represents the present, which is historical, which has been superseded, and what happens when Canon, repository, runtime and Memory disagree.

So the next task should be:

Phase XI — Current Truth, Temporal Manifestation & Semantic Reconciliation Audit

This should connect the six temporal principles we previously accepted-but-did-not-canonize with the concrete identity anatomy discovered here and determine how AI-Toolkit can answer not merely:

> “What manifestations exist?”



but:

> “What is true now, according to which authority, what was true before, and why did it change?”

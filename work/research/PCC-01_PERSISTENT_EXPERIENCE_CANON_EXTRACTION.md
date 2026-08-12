# PCC-01 — Persistent Experience Canon Extraction and Traceability

Version: 0.1.0

Status: Working Extraction — Human Acceptance Required

Classification: Production Canon Extraction / Epistemic Continuity

Parent Contract: `PRODUCTION_CANON_CONTRACT.md`

Production Capability: `PCC-01 — Persistent Experience`

Human Authority: Owner

---

# 1. Purpose

This document extracts, reconciles, and makes traceable the requirements
for:

**PCC-01 — Persistent Experience**

Its purpose is not to invent a new architecture.

Its purpose is to determine, from preserved research, observed
experience, repository evidence, existing implementation, and human
decisions, what Persistent Experience must mean before production
implementation begins.

This document separates:

- preserved source material;
- observed implementation;
- research conclusions;
- production requirements;
- unresolved questions;
- prohibited interpretations;
- acceptance evidence;
- acceptance tests.

No requirement becomes production Canon merely because it appears in
research, code, an audit, or this working extraction.

Human acceptance remains required.

---

# 2. The Problem Being Solved

AI-Toolkit currently preserves important parts of its existence, but it
does not yet reliably preserve the complete experience through which
its evolution occurs.

A project may preserve:

- code;
- commits;
- documents;
- terminal output;
- tests;
- generated Evidence;
- current state.

Yet still lose the lived path that produced them.

That lost path may contain:

- the human need;
- the original human idea;
- the way the idea was expressed;
- questions;
- uncertainty;
- disagreement;
- corrections;
- AI proposals;
- rejected proposals;
- Bash proposed by an AI;
- Bash actually executed by the human;
- terminal output;
- failures;
- observations;
- interpretations;
- intermediate discoveries;
- decisions;
- resulting artifacts;
- reflections.

If only the final artifact survives, the project knows what exists but
may no longer know adequately how or why it came to exist.

Persistent Experience exists to prevent that epistemic loss.

---

# 3. Human Meaning

Persistent Experience is the organism's preserved lived experience.

It is not merely a log.

It is not merely terminal history.

It is not merely conversation history.

It is not merely a Session.

It is not merely a Transformation.

It is not merely Evidence.

It is not merely a Witness.

It is not Memory.

It is not CSL.

Persistent Experience preserves the relevant raw experience from which
those later structures may be understood, evidenced, organized,
derived, or sedimented.

In human terms:

> Session tells us during what continuous interval the organism lived
> and worked.

> Persistent Experience preserves what was actually lived during that
> interval.

> Transformation explains the meaningful change that occurred.

> Evidence supports claims about what happened.

> Witness provides a compact testimony of the transformation.

> Memory preserves what should remain learned.

> CSL / Living Project Image expresses the best current image of the
> organism.

These structures may cooperate.

They must not be collapsed into one another merely because their
information overlaps.

---

# 4. Source Classes Used by This Extraction

The extraction distinguishes source classes because existence,
historical importance, and canonical authority are not the same thing.

## 4.1 Preserved Research

Research material records concepts, reasoning, proposed models,
discoveries, and human–AI investigation.

Research is epistemically valuable.

Research does not automatically become production Canon.

---

## 4.2 Preserved Experience

Existing Persistent Experience artifacts demonstrate that the project
has already experimented with preserving lived execution.

They provide historical and empirical evidence.

Their existence does not prove that the complete target physiology has
been implemented.

---

## 4.3 Repository Implementation

Executable code demonstrates what the repository currently contains.

Code presence does not by itself establish:

- canonical correctness;
- operational completeness;
- production readiness;
- architectural authority.

---

## 4.4 Audit Evidence

Audits describe what could be observed at a particular repository
state.

An audit is Evidence.

An audit does not acquire authority to redefine Canon.

---

## 4.5 Human Decisions

Explicit human decisions establish authority where the project reserves
such authority to the human owner.

Human decisions must remain traceable to their context rather than
being rewritten later as if they originated from the implementation.

---

# 5. Primary Source Basis

The principal preserved source identified for the birth of Persistent
Experience is:

`work/research/EP-0001_Birth_of_Persistent_Experience_20260809T223848Z.md`

The preserved research establishes the problem that execution alone is
insufficient.

The system must preserve the context through which execution became
meaningful.

The research identifies the need to preserve, together where
applicable:

- research context;
- dialogue;
- Bash;
- terminal execution;
- resulting experience.

The research also establishes that Persistent Experience emerged
because project continuity could not depend upon the human manually
reconstructing the past for a later AI collaborator.

Authority classification:

**CONFIRMED AS SOURCE BASIS**

Production interpretation:

**SUBJECT TO THIS EXTRACTION AND HUMAN ACCEPTANCE**

---

# 6. Existing Persistent Experience Evidence

Repository evidence identifies existing artifacts under:

`work/persistent-experience/`

including:

- active Experience artifacts;
- terminal Evidence;
- an Experience index.

Observed examples include:

`work/persistent-experience/active/EXP-20260809T225030Z.md`

`work/persistent-experience/active/EXP-20260809T225309Z.md`

`work/persistent-experience/evidence/EXP-20260809T225309Z.terminal.log`

`work/persistent-experience/index/INDEX.md`

These artifacts demonstrate that Persistent Experience has already
existed as an experimental repository concept.

They also demonstrate an important limitation:

the preserved Experience artifacts do not yet establish complete
automatic preservation of all relevant lived experience.

Some expected material remained to be completed from the surrounding
research conversation or execution context.

Therefore:

**Persistent Experience concept exists: CONFIRMED**

**Persistent Experience experimental artifacts exist: CONFIRMED**

**Terminal experience preservation has been demonstrated: CONFIRMED**

**Complete automatic lived-experience capture: NOT DEMONSTRATED**

**Production-complete Persistent Experience: NOT DEMONSTRATED**

---

# 7. Existing Runtime Reconciliation

The runtime inspection at repository HEAD:

`079e9e762f543d611ce265f74cda4c7b9c340210`

identified several related organs.

They must be reconciled with Persistent Experience rather than silently
redefined.

---

## 7.1 Epistemic Session

Source:

`lib/python/epistemic/session.py`

Observed responsibility:

A Session groups a continuous sequence of events into a transformation
journey.

It records:

- identifier;
- purpose;
- start time;
- status.

Session open and close events are appended to Chronicle.

Production interpretation:

Session represents the bounded interval or episode of work.

It does not currently preserve the complete lived content of that
episode.

Classification:

**EXISTING RELATED ORGAN**

**NOT EQUIVALENT TO PERSISTENT EXPERIENCE**

---

## 7.2 Session Runtime

Sources:

`lib/python/session_runtime/models.py`

`lib/python/session_runtime/runtime.py`

`lib/python/session_runtime/storage.py`

Observed responsibility:

The runtime Session contains:

- identifier;
- repository;
- status;
- completed steps;
- metadata.

It can be created, checkpointed, saved, and loaded through JSON
persistence.

Production interpretation:

This is operational session-state persistence.

It may later participate in Persistent Experience coordination.

It is not itself evidence of complete Experience capture.

Classification:

**EXISTING RELATED ORGAN**

**POTENTIAL INTEGRATION POINT**

**NOT EQUIVALENT TO PERSISTENT EXPERIENCE**

---

## 7.3 Transformation

Source:

`lib/python/epistemic/transformation.py`

Observed responsibility:

The current executable Transformation lifecycle preserves:

- an identifier;
- need;
- start time;
- status;
- completion time.

It writes a Transformation Evidence artifact.

Production interpretation:

This implementation represents an early executable transformation
lifecycle.

It does not currently embody the complete research model of meaningful
project evolution.

It must not be treated as a substitute for Persistent Experience.

Classification:

**EXISTING RELATED ORGAN**

**PARTIAL TRANSFORMATION IMPLEMENTATION**

**NOT EQUIVALENT TO PERSISTENT EXPERIENCE**

---

## 7.4 Witness

Source:

`lib/python/epistemic/witness.py`

Observed responsibility:

Witness accepts:

- need;
- dialogue;
- implementation;
- execution;
- result;
- knowledge.

It writes a Witness artifact.

This is important because the current Witness already recognizes that a
meaningful transformation can involve dialogue, implementation,
execution, result, and knowledge.

However, these values are supplied to Witness.

Witness does not itself demonstrate automatic capture of the original
experience from which those values came.

Production interpretation:

Witness is a compact testimony or derived representation.

Witness may reference Persistent Experience.

Witness must not replace the preserved original Experience.

Classification:

**EXISTING RELATED ORGAN**

**DERIVED TESTIMONY**

**NOT EQUIVALENT TO PERSISTENT EXPERIENCE**

---

# 8. Core Production Definition

Subject to human acceptance, PCC-01 defines Persistent Experience as:

> The project-owned preservation of epistemically significant lived
> project experience in a form that retains sufficient original
> context, sequence, provenance, and execution reality to allow later
> humans and AI collaborators to understand what occurred without
> depending upon manual reconstruction by the original participant.

Persistent Experience must preserve reality before later
interpretation, compression, sedimentation, or contextual packaging can
replace access to that reality.

---

# 9. Capture Before Interpretation

Classification:

**PROPOSED CONFIRMED PRODUCTION REQUIREMENT**

Persistent Experience shall preserve epistemically significant raw
experience before that experience is replaced by:

- summaries;
- Witnesses;
- Memories;
- CSL representations;
- context packages;
- conclusions;
- derived interpretations.

Interpretation may occur.

Compression may occur.

Sedimentation may occur.

Derived views may occur.

The original preserved Experience must remain independently reachable.

The system shall not require the later derived representation to serve
as the only surviving account of the original event.

---

# 10. Original Experience Preservation

Classification:

**PROPOSED CONFIRMED PRODUCTION REQUIREMENT**

Once epistemically significant Experience has been accepted into
persistent preservation, later processing shall not silently rewrite
the original experience to conform to:

- a later conclusion;
- current architecture;
- current terminology;
- successful implementation;
- revised Canon;
- an AI-generated summary;
- a cleaner historical narrative.

A failed command remains a failed command.

A rejected proposal remains a rejected proposal.

A contradiction remains historically visible even after resolution.

A human correction remains attributable to the human.

An AI proposal remains attributable to the AI.

Historical reality must not be rewritten merely because the organism
later knows more.

Corrections and later interpretations shall be represented through
additional traceable structures.

---

# 11. Human ↔ AI Dialogue Preservation

Classification:

**PROPOSED CONFIRMED PRODUCTION REQUIREMENT**

Where Human↔AI dialogue materially contributes to project evolution,
Persistent Experience shall be capable of preserving the relevant
dialogue.

The preserved representation must retain enough structure to
distinguish:

- human contribution;
- AI contribution;
- sequence;
- relevant temporal context;
- relationship to the active Session or Transformation where known.

The system must preserve human intellectual initiative.

If the human originates an idea, requirement, correction, analogy,
objection, or decision, later AI reformulation must not erase that
origin.

Likewise, AI-generated proposals must not later be represented as human
decisions merely because the human subsequently accepted or implemented
them.

---

# 12. Proposed Bash and Executed Bash Are Different Facts

Classification:

**PROPOSED CONFIRMED PRODUCTION REQUIREMENT**

Persistent Experience shall distinguish between:

**Bash proposed or generated**

and

**Bash actually executed**

These are not epistemically equivalent.

A command may be:

- proposed but never executed;
- copied incompletely;
- edited by the human;
- executed later;
- executed more than once;
- executed in a different repository state;
- executed after environmental changes;
- rejected;
- interrupted;
- partially executed.

Therefore the system shall not infer execution merely from the presence
of a proposed command.

Execution must be supported by execution Evidence.

---

# 13. Terminal Execution Preservation

Classification:

**PROPOSED CONFIRMED PRODUCTION REQUIREMENT**

For epistemically significant terminal execution, Persistent Experience
shall be capable of preserving, where technically observable and
applicable:

- the executed command or command stream;
- stdout;
- stderr;
- exit status;
- execution time;
- execution order;
- working directory;
- relevant repository identity;
- relevant repository state;
- relationship to the active Experience;
- relationship to the active Session where known.

Failures are part of Experience.

An implementation shall not preserve only successful execution.

A command returning non-zero may be more epistemically important than a
successful command because it can explain subsequent reasoning,
correction, or transformation.

---

# 14. Observation and Reflection

Classification:

**PROPOSED CONFIRMED PRODUCTION REQUIREMENT**

Persistent Experience shall support preservation of observations and
reflections when they materially contribute to understanding what was
experienced.

Observation and reflection must remain distinguishable from raw
execution Evidence.

For example:

Terminal reality:

`command failed with exit code 1`

Observation:

`the generated script stopped during repository discovery`

Reflection:

`the current capture mechanism is fragile when large scripts are copied
through the conversation interface`

These are related facts but not the same epistemic object.

The system must not silently transform interpretation into raw Evidence.

---

# 15. Resulting Artifact Association

Classification:

**PROPOSED CONFIRMED PRODUCTION REQUIREMENT**

Persistent Experience shall be able to associate resulting artifacts
with the experience that produced or materially changed them.

Examples may include:

- source files;
- research documents;
- audit reports;
- Evidence;
- tests;
- commits;
- configuration changes;
- generated CSL;
- Witnesses;
- Transformations.

Association does not imply that the Experience owns the artifact's
canonical authority.

It establishes navigable provenance.

---

# 16. Execution Context

Classification:

**PROPOSED CONFIRMED PRODUCTION REQUIREMENT**

Persistent Experience shall preserve sufficient execution context to
make important execution intelligible later.

Context may include, where applicable:

- repository;
- branch;
- commit;
- working tree state;
- working directory;
- runtime environment;
- timestamp;
- command sequence;
- Session identity;
- Transformation identity;
- relevant tool or actor.

Not every possible environmental variable must be captured.

Capture depth must be sufficient to preserve epistemic meaning and
support appropriate reproducibility.

The exact minimum technical execution-context schema remains an
implementation design decision constrained by this requirement.

---

# 17. Provenance

Classification:

**PROPOSED CONFIRMED PRODUCTION REQUIREMENT**

Every epistemically significant Experience component shall preserve
sufficient provenance to answer, where applicable:

- who contributed it;
- what produced it;
- when it occurred;
- in which Experience it occurred;
- in which Session it occurred;
- to which Transformation it relates;
- what Evidence supports it;
- what artifact resulted from it;
- whether it is original or derived.

Provenance shall not be reconstructed later from assumption when it was
available at capture time.

---

# 18. Human-Readable Identity

Classification:

**PROPOSED CONFIRMED PRODUCTION REQUIREMENT**

Persistent Experience shall obey the Human-Readable Identity Principle.

Every epistemically significant Experience entity intended for human
inspection shall possess:

- a stable machine-addressable identifier;
- a concise human-readable semantic title.

Human-facing representations shall normally present both together.

Example:

`EXP-0042 — First Captured Terminal Run`

rather than:

`EXP-0042`

alone.

Identifiers establish identity.

Titles communicate meaning.

---

# 19. No Naked Identifier

Classification:

**PROPOSED CONFIRMED PRODUCTION REQUIREMENT**

Where a semantic title is known, human-facing Persistent Experience
representations shall not require the human to resolve an opaque
identifier merely to understand what an entity means.

Machine-oriented derived representations may use compact identifiers
where doing so materially reduces context volume.

Such compact representations remain derived views.

They shall not destroy the human-readable identity of the underlying
entity.

---

# 20. Navigability

Classification:

**PROPOSED CONFIRMED PRODUCTION REQUIREMENT**

Persistent Experience must be navigable.

A human or AI inspecting an Experience should be able to travel toward
related epistemic artifacts when those relationships are known.

Relevant navigable relationships may include:

- Session;
- Transformation;
- Evidence;
- Witness;
- Memory;
- CSL representation;
- resulting artifact;
- preceding Experience;
- following Experience;
- source dialogue;
- terminal transcript.

Human-readable CSL or Markdown views should use navigable references
where the representation technology permits them.

A reference must not falsely imply that a target exists.

Broken or unresolved relationships must remain explicit.

---

# 21. Capture Once, Reference Many

Classification:

**PROPOSED CONFIRMED PRODUCTION REQUIREMENT**

Large raw Experience should not need to be duplicated into every later
epistemic structure.

The preferred relationship is:

Capture once.

Preserve integrity.

Assign identity.

Reference many times.

Transformation, Witness, Memory, CSL, context packages, and audits may
reference the preserved Experience or selected parts of it.

Derived representations may contain excerpts or summaries where useful.

They must retain a path to the preserved source when that source
remains available.

---

# 22. Project-Owned Continuity

Classification:

**PROPOSED CONFIRMED PRODUCTION REQUIREMENT**

Persistent Experience belongs to the project continuity system.

It must not exist only inside the memory or conversation history of a
particular external AI provider.

The external AI collaborator may change.

The project must retain its Experience.

Provider-native conversation history may be used as an input when
available.

It must not be the sole continuity mechanism.

---

# 23. Human Preservation Burden

Classification:

**PROPOSED CONFIRMED PRODUCTION REQUIREMENT**

The target production physiology shall progressively reduce the need
for the human to manually preserve epistemically significant project
experience.

The human should not normally be required to:

- reconstruct previous conversations;
- rewrite historical context;
- manually paste large terminal transcripts;
- remember which Bash produced which result;
- create enormous handover prompts for replacement AI collaborators.

Manual preservation may remain available as:

- fallback;
- correction;
- import mechanism;
- recovery mechanism;
- explicit human contribution.

It must not remain the intended normal operating mechanism for mature
Persistent Experience.

---

# 24. Evidence-Bounded Representation

Classification:

**PROPOSED CONFIRMED PRODUCTION REQUIREMENT**

Persistent Experience shall not claim to have captured information that
was not actually observable or preserved.

If dialogue cannot be accessed automatically, the system shall not
claim that the complete dialogue was captured.

If stderr was unavailable, it shall not invent stderr.

If the executed command cannot be distinguished from a proposed
command, the uncertainty shall remain explicit.

If an Experience is incomplete, it shall be represented as incomplete.

Honest incompleteness is preferable to fabricated continuity.

---

# 25. Relationship to Session

Classification:

**PROPOSED CONFIRMED PRODUCTION REQUIREMENT**

Session and Persistent Experience shall remain distinct.

Session answers primarily:

**During what bounded episode did the organism work, and for what
purpose?**

Persistent Experience answers primarily:

**What epistemically significant reality was lived during that
episode?**

One Session may contain multiple Experience components.

An Experience should be able to reference its Session when known.

The implementation must not require duplication of the complete
Experience into the Session object.

---

# 26. Relationship to Transformation

Classification:

**PROPOSED CONFIRMED PRODUCTION REQUIREMENT**

Persistent Experience and Transformation shall remain distinct.

Experience preserves what was lived.

Transformation organizes meaningful evolution.

A Transformation may be reconstructed or understood through one or
more Experience sources.

A Transformation must not rewrite those sources.

Persistent Experience may exist even when no Transformation has yet
been formally recognized.

This is important because interpretation may occur after experience.

---

# 27. Relationship to Evidence

Classification:

**PROPOSED CONFIRMED PRODUCTION REQUIREMENT**

Evidence and Persistent Experience shall remain distinct.

Evidence supports claims.

Experience preserves lived context.

A terminal transcript may simultaneously function as Experience
material and Evidence, but its epistemic roles must remain
distinguishable.

The system shall not assume that every Experience component proves a
claim.

Nor shall it assume that Evidence alone preserves the complete
experience through which the claim became meaningful.

---

# 28. Relationship to Witness

Classification:

**PROPOSED CONFIRMED PRODUCTION REQUIREMENT**

Witness is a compact testimony of a Transformation or significant
event.

Persistent Experience is the deeper preserved reality from which a
Witness may derive or to which it may point.

Witness must not become the only surviving representation of the
Experience merely because it is smaller or easier to consume.

Where possible, Witness should retain navigable provenance toward the
Experience it summarizes.

---

# 29. Relationship to Memory

Classification:

**PROPOSED CONFIRMED PRODUCTION REQUIREMENT**

Persistent Experience and Memory shall remain distinct.

Experience preserves what was lived.

Memory preserves what the organism has sedimented as durable knowledge.

Memory may be derived from Experience.

The Experience must not be destroyed merely because Memory has been
created.

Later correction of Memory must remain capable of travelling back
toward the Experience and Evidence from which the Memory arose.

---

# 30. Relationship to CSL / Living Project Image

Classification:

**PROPOSED CONFIRMED PRODUCTION REQUIREMENT**

Persistent Experience is not the Living Project Image.

CSL expresses the best evidence-bounded current image of the project.

Persistent Experience preserves historical lived reality.

CSL may reference Experience when history or provenance is relevant.

CSL may use compact derived representations.

It must not require raw Experience to be duplicated wholesale into the
current image.

---

# 31. Security and Sensitive Material

Classification:

**RECONCILIATION REQUIRED**

Raw Experience may contain:

- credentials;
- tokens;
- personal information;
- private conversations;
- secrets;
- environment values;
- external provider data;
- sensitive repository information.

Therefore Capture Before Interpretation cannot safely mean:

**persist every observable byte without governance.**

Production implementation requires a controlled policy for:

- secret detection;
- redaction;
- exclusion;
- access control;
- retention;
- deletion where legitimately required;
- provenance of redaction;
- preservation of the fact that redaction occurred.

Security filtering must not silently falsify history.

For example, a secret value may need to become:

`[REDACTED — SECRET]`

while preserving that a redaction occurred.

The exact security and privacy contract requires further reconciliation
before unrestricted automatic capture can be considered production
ready.

---

# 32. Capture Boundary

Classification:

**RECONCILIATION REQUIRED**

Not every character produced during project activity is necessarily
epistemically significant.

Unbounded capture can create:

- excessive storage;
- noise;
- duplicated material;
- sensitive-data risk;
- retrieval degradation;
- unusable context.

Therefore the production system requires a governed capture boundary.

The boundary must satisfy both:

**do not lose meaningful experience**

and

**do not indiscriminately preserve irrelevant or dangerous material**

The exact automatic selection policy remains unresolved.

Until resolved, implementations must prefer explicit completeness
status over pretending that selective capture is complete capture.

---

# 33. Immutability and Correction

Classification:

**RECONCILIATION REQUIRED**

The research direction strongly requires preservation of original
experience.

However, production must reconcile this with legitimate requirements
such as:

- secret removal;
- privacy correction;
- corrupt artifact repair;
- legal deletion requirements;
- accidental binary or excessive-data capture.

Therefore "original preservation" should not yet be interpreted as
absolute physical immutability under every circumstance.

The required semantic rule is stronger and already clear:

**history must not be silently rewritten.**

Where alteration is legitimate, the system should preserve appropriate
traceability of:

- what changed;
- why;
- under whose authority;
- when;
- what relationship remains to the previous state where legally and
  technically permissible.

The exact retention/deletion mechanics require further production
design.

---

# 34. Automatic Capture

Classification:

**CONFIRMED TARGET / IMPLEMENTATION NOT YET DEMONSTRATED**

The long-term purpose of Persistent Experience requires automatic or
system-assisted capture.

Current repository evidence does not demonstrate complete automatic
capture of:

Human ↔ AI dialogue
+
proposed Bash
+
executed Bash
+
stdout
+
stderr
+
exit status
+
observations
+
resulting artifacts
+
execution context

as one governed Experience continuum.

Therefore the current implementation must not be described as
production-complete Persistent Experience.

---

# 35. Current Implementation Status

At the audited repository state:

`079e9e762f543d611ce265f74cda4c7b9c340210`

the following assessment applies.

## CONFIRMED PRESENT

- experimental Persistent Experience artifacts;
- Experience index;
- preserved terminal transcript Evidence;
- Epistemic Session implementation;
- Session Runtime persistence;
- early Transformation lifecycle;
- Witness generation;
- Chronicle-related Session recording.

## PARTIALLY PRESENT

- terminal experience preservation;
- execution-context preservation;
- relationships among epistemic structures;
- transformation evidence;
- session persistence.

## NOT DEMONSTRATED AS COMPLETE

- automatic Human↔AI dialogue capture;
- automatic proposed-Bash capture;
- reliable distinction between proposed and executed Bash throughout
  the Experience lifecycle;
- automatic stdout/stderr/exit-status association with the same
  Experience;
- complete Experience provenance;
- automatic Experience ↔ Session linkage;
- automatic Experience ↔ Transformation linkage;
- automatic Experience ↔ Witness linkage;
- human-readable semantic titles for every Experience;
- navigable Experience relationships;
- governed capture boundary;
- security/redaction policy;
- production acceptance tests;
- production-ready end-to-end Persistent Experience.

Therefore:

**Current PCC-01 production status: NOT YET REALIZED**

This status is evidence-bounded.

It does not claim historical non-existence of capabilities for which
current evidence is unavailable.

---

# 36. Prohibited Behaviour

A PCC-01 implementation shall not:

- treat conversation history held only by an external AI provider as
  project-owned Persistent Experience;
- infer that proposed Bash was executed without execution Evidence;
- erase failed execution because a later execution succeeded;
- rewrite original human contributions as AI contributions;
- rewrite AI proposals as human decisions;
- replace original Experience with a summary;
- replace original Experience with Witness;
- replace original Experience with Memory;
- replace original Experience with CSL;
- collapse Session, Experience, Transformation, Evidence, Witness, and
  Memory into one epistemic object merely for implementation
  convenience;
- claim complete capture when capture was partial;
- invent missing stdout, stderr, timestamps, actors, commands, or
  provenance;
- create hidden epistemic authority;
- silently promote derived interpretation into original Experience;
- silently delete contradictions;
- silently sanitize history in order to make later architecture appear
  inevitable;
- expose secrets merely to satisfy a naive interpretation of raw
  preservation;
- silently redact material without preserving appropriate redaction
  provenance;
- require opaque identifiers alone in normal human-facing
  representations when semantic titles are known.

---

# 37. Human Authority

Human authority applies across PCC-01.

The human owner retains authority to:

- accept or reject the PCC-01 production definition;
- establish capture-policy boundaries;
- determine legitimate exclusions;
- correct attribution;
- challenge AI interpretation;
- classify Experience significance;
- approve security/redaction policy;
- resolve canonical contradictions;
- reject derived summaries;
- require deeper provenance;
- invalidate falsely claimed completeness;
- authorize production readiness.

AI may:

- capture;
- organize;
- correlate;
- index;
- propose titles;
- identify relationships;
- derive summaries;
- detect potential secrets;
- propose sedimentation;
- propose Transformations;
- propose Memory.

These operations do not grant the AI independent canonical authority.

No hidden authority layer may exist behind the human-facing governance
model.

---

# 38. Required Provenance

A production Persistent Experience representation shall be capable of
preserving or resolving, where applicable:

## Identity

- Experience identifier;
- semantic title.

## Time

- creation/capture time;
- event time where different;
- sequence.

## Actor

- human;
- AI;
- terminal/runtime;
- repository/system;
- other known source.

## Context

- repository;
- branch;
- commit;
- working directory;
- Session;
- Transformation where known.

## Content Origin

- dialogue;
- proposed instruction;
- executed instruction;
- terminal output;
- observation;
- reflection;
- generated artifact;
- external source.

## Relationships

- Evidence;
- Witness;
- Memory;
- CSL;
- preceding/following Experience;
- resulting artifacts.

## Integrity

- integrity information appropriate to the preserved artifact where
  useful;
- completeness status;
- redaction status;
- derivation status.

Unknown provenance shall be represented as unknown rather than invented.

---

# 39. Minimum Human-Readable Experience Model

The exact serialization format remains an implementation decision.

However, a human-facing Experience should be capable of communicating
at least:

**Identity**

`EXP-xxxx — Semantic Title`

**Purpose / Context**

Why this Experience matters and where it occurred.

**Participants**

Who or what contributed.

**Sequence**

What happened and in what order.

**Dialogue**

Relevant Human↔AI exchange where captured.

**Proposed Actions**

What was suggested.

**Executed Actions**

What actually ran.

**Execution Reality**

stdout, stderr, exit status, and relevant environment context.

**Observations**

What was observed.

**Results**

What resulted.

**Artifacts**

What was created or changed.

**Relationships**

Session, Transformation, Evidence, Witness, Memory, CSL, lineage.

**Completeness**

What was captured and what was not.

**Provenance**

Where each significant component came from.

This is a semantic requirement.

It does not mandate a single monolithic file.

---

# 40. Storage Architecture Constraint

Classification:

**PRODUCTION CONSTRAINT — IMPLEMENTATION DESIGN OPEN**

Persistent Experience may be physically represented through:

- one manifest plus referenced artifacts;
- event records;
- append-only streams;
- content-addressed objects;
- Markdown human views;
- structured machine representations;
- combinations of these.

The Canon Extraction does not yet select the final storage technology.

However, any selected implementation must preserve:

- project ownership;
- provenance;
- navigability;
- human readability;
- machine addressability;
- original Experience preservation;
- evidence-bounded completeness;
- derivability;
- separation of epistemic roles.

Implementation convenience shall not redefine these requirements.

---

# 41. Acceptance Evidence

PCC-01 cannot be considered realized merely because a class named
`PersistentExperience` exists.

Acceptance requires observable end-to-end Evidence.

At minimum, a controlled acceptance run must demonstrate a meaningful
work episode containing:

1. a human-originated need or instruction;
2. an AI contribution;
3. a Bash proposal;
4. actual terminal execution;
5. stdout;
6. stderr or explicit evidence that none occurred;
7. exit status;
8. an observation or result;
9. a resulting artifact or explicit no-artifact result;
10. Session association where a Session is active;
11. provenance for the captured components;
12. a human-readable Experience identity;
13. preserved sequence;
14. explicit completeness status.

The acceptance Evidence must allow an independent reviewer to determine
which information was actually captured rather than reconstructed after
the fact.

---

# 42. Acceptance Tests

Before PCC-01 may be represented as production-ready, tests must cover
at least the following behaviours.

## AT-01 — Experience Creation

A new Experience can be created with:

- stable identifier;
- semantic title;
- timestamp;
- project/repository context.

---

## AT-02 — Human and AI Attribution

Human and AI contributions remain distinguishable after persistence and
reload.

---

## AT-03 — Proposed vs Executed Bash

A proposed command is not marked executed until execution Evidence
exists.

---

## AT-04 — Successful Execution Capture

Executed command, stdout, exit status, and relevant context are
associated with the Experience.

---

## AT-05 — Failed Execution Capture

A failed command and non-zero exit status remain preserved and
navigable.

Failure must not abort Experience preservation itself.

---

## AT-06 — stderr Preservation

stderr is preserved when present.

Absence of stderr is represented without fabrication.

---

## AT-07 — Ordering

Multiple Experience events retain their meaningful sequence.

---

## AT-08 — Session Relationship

An Experience created during an active Session can resolve its Session
relationship without duplicating the entire Experience into Session.

---

## AT-09 — Transformation Relationship

A Transformation can reference relevant Experience without rewriting
the Experience.

---

## AT-10 — Witness Relationship

A Witness can reference or derive from Experience while the original
Experience remains available.

---

## AT-11 — Original Preservation

Creating a summary, Witness, Memory, or other derived representation
does not overwrite the original Experience.

---

## AT-12 — Human-Readable Identity

Human-facing output presents identifier and semantic title together
where the title is known.

---

## AT-13 — Navigability

Known relationships resolve to existing artifacts or are explicitly
reported as unresolved.

---

## AT-14 — Incomplete Capture Honesty

If a source cannot be captured, the Experience records incompleteness
rather than claiming full capture.

---

## AT-15 — Sensitive Material Handling

Sensitive material handling follows the approved security policy and
does not silently falsify the historical record.

This test cannot be considered final until the security policy is
reconciled.

---

## AT-16 — Persistence and Reload

An Experience can survive process termination and be reconstructed from
project-owned persistence without relying on the original AI
conversation session.

---

## AT-17 — Provider Independence

The preserved Experience remains usable when the external AI
collaborator changes.

---

## AT-18 — Evidence-Bounded Status

The system cannot represent PCC-01 as complete merely because some
capture components succeeded.

Completeness must correspond to observable captured components.

---

# 43. Acceptance Scenario

A minimum production acceptance scenario should reproduce the type of
work that originally exposed the continuity problem.

Example:

A human asks an AI to investigate a project problem.

The AI proposes a Bash command.

The human executes the command in Termux.

The command produces output.

The output exposes a failure.

The human reports or observes the failure.

The AI changes its interpretation.

A corrected action follows.

A repository artifact results.

Persistent Experience should allow a later independent AI collaborator
to navigate that episode and determine:

- what the human wanted;
- what the AI proposed;
- what was actually executed;
- what failed;
- what output existed;
- what the human observed;
- how reasoning changed;
- what action followed;
- what artifact resulted;
- which parts were captured directly;
- which parts were later interpretation.

The later AI should not require the original human to rewrite that
history manually.

---

# 44. Current Production Gap

The principal PCC-01 gap is not the complete absence of persistence.

The repository already contains multiple forms of persistence.

The gap is the absence of a demonstrated governed continuum connecting:

Human Experience
↓
AI Contribution
↓
Proposed Action
↓
Actual Execution
↓
Execution Reality
↓
Observation
↓
Result
↓
Artifacts
↓
Provenance
↓
Later Transformation / Witness / Memory / CSL

while preserving the original Experience and keeping the epistemic
roles distinct.

This is the production gap PCC-01 must close.

---

# 45. Implementation Boundary for an AI Coding Agent

An implementation agent may be instructed to implement PCC-01 only
after the human accepts the production requirements and unresolved
boundaries are explicitly identified.

The agent may:

- inspect existing Session, Chronicle, Transformation, Witness, and
  runtime components;
- reuse compatible implementation;
- add Experience models and persistence;
- add capture mechanisms;
- add provenance;
- add relationships;
- add human-readable views;
- add tests;
- produce acceptance Evidence.

The agent shall not:

- redefine Persistent Experience;
- collapse epistemic organs;
- invent Canon;
- silently resolve security/governance questions;
- declare unresolved requirements implemented;
- delete experimental historical artifacts merely because a newer
  implementation exists;
- replace human-readable semantics with opaque identifiers;
- claim automatic dialogue capture where provider access does not
  support it;
- fabricate continuity across unavailable sources.

---

# 46. Reconciliation Required Before Full Production

The following remain explicitly unresolved and shall not be silently
decided by an implementation agent:

## R-01 — Dialogue Acquisition

How does AI-Toolkit obtain Human↔AI dialogue from different AI
collaboration environments?

Possible mechanisms require technical investigation.

No assumption is made here that every provider exposes complete
conversation history.

---

## R-02 — Capture Boundary

What constitutes sufficient epistemic significance for automatic
capture?

The system requires a balance between continuity and uncontrolled data
accumulation.

---

## R-03 — Security / Secrets / Privacy

What material must be excluded, redacted, protected, retained, or
deleted?

This requires an explicit production policy.

---

## R-04 — Retention

How long is raw Experience retained?

Can Experience move through archival depth while remaining navigable?

This should later reconcile with Layered Memory without prematurely
turning Experience into Memory.

---

## R-05 — Physical Storage Model

The semantic contract is clearer than the final storage implementation.

The final architecture must be selected through implementation design
and evidence, not assumption.

---

## R-06 — Automatic Session Binding

The relationship between the two current Session implementations and
future Persistent Experience requires controlled reconciliation.

The implementation must not arbitrarily choose one as canonical merely
because it is easier to modify.

---

# 47. Human Acceptance Decisions Requested

Before this extraction becomes normative for PCC-01, the human owner
should explicitly decide whether to accept the following principles:

1. Persistent Experience is the preserved lived experience of the
   epistemic organism.

2. Session, Persistent Experience, Transformation, Evidence, Witness,
   Memory, and CSL remain distinct epistemic roles.

3. Raw Experience is preserved before later interpretation replaces
   access to it.

4. Human and AI contributions retain attribution.

5. Proposed Bash and executed Bash are distinct facts.

6. Failed execution is preserved.

7. Original Experience is not silently rewritten by later conclusions.

8. Derived structures reference Experience rather than destroying it.

9. Human-facing Experience uses both stable identifier and semantic
   title.

10. Persistent Experience belongs to the project rather than a
    particular AI provider.

11. The mature system should reduce manual preservation burden toward
    automatic or system-assisted capture.

12. Incomplete capture must be represented honestly.

13. Security and privacy constraints may legitimately limit raw capture
    but may not silently falsify history.

14. Human authority remains above all AI-derived representations.

15. Current implementation must remain classified as incomplete until
    end-to-end acceptance Evidence exists.

---

# 48. Proposed Authority Classification

Subject to explicit human acceptance:

## CONFIRMED

- Persistent Experience is required.
- Persistent Experience preserves lived project experience.
- original Experience must remain reachable after derivation;
- human initiative and AI contribution require provenance;
- proposed and executed actions must be distinguishable;
- terminal reality includes failures;
- Experience must be project-owned;
- incomplete capture must not be represented as complete;
- human-readable epistemic identity applies;
- no hidden AI authority is permitted;
- current repository state does not demonstrate production-complete
  PCC-01.

## RECONCILIATION REQUIRED

- automatic dialogue acquisition;
- exact capture boundary;
- secret/privacy policy;
- retention policy;
- physical storage architecture;
- reconciliation of existing Session implementations;
- exact provider integration mechanisms.

## RESEARCH ONLY UNTIL LATER PCC WORK

- detailed sedimentation physiology;
- final Layered Memory mechanics;
- final Progressive Recall algorithms;
- final Automatic Context Package algorithms;
- final AI Bootstrap protocol;
- final Zero-Prompt Continuity mechanism.

These later concepts constrain direction but shall not be implemented
inside PCC-01 merely because they depend upon Experience.

---

# 49. Production Gate for PCC-01

PCC-01 may advance toward production only through:

SOURCE BASIS PRESERVED
↓
REQUIREMENTS EXTRACTED
↓
HUMAN ACCEPTANCE
↓
UNRESOLVED BOUNDARIES EXPLICIT
↓
IMPLEMENTATION DESIGN
↓
CONTROLLED IMPLEMENTATION
↓
AUTOMATED TESTS
↓
REAL CAPTURE SCENARIO
↓
EVIDENCE PRESERVED
↓
INDEPENDENT VERIFICATION
↓
HUMAN PRODUCTION ACCEPTANCE

No implementation agent may skip this gate by reporting task success.

---

# 50. Relationship to the Larger Continuity Path

PCC-01 is the first production capability in the continuity path:

Persistent Experience
↓
Transformation
↓
Provenance + Lineage
↓
Sedimentation
↓
Layered Memory
↓
CSL / Living Project Image
↓
Progressive Recall
↓
Automatic Context Package
↓
AI Bootstrap / Context Handshake
↓
Zero-Prompt Continuity

PCC-01 must provide trustworthy experiential ground for later stages.

It must not attempt to implement all later stages prematurely.

If Persistent Experience is unreliable, every later layer risks
building increasingly sophisticated representations of incomplete or
incorrect history.

Therefore PCC-01 establishes the first production rule of continuity:

**The organism must first preserve what it lived before it can safely
decide what that experience means.**

---

# 51. Current Frontier

The immediate frontier after human review of this extraction is:

1. verify this document was saved without corruption;
2. review the proposed requirements and classifications;
3. obtain explicit human acceptance or corrections;
4. preserve the accepted PCC-01 extraction;
5. materialize the accepted requirements into
   `PRODUCTION_CANON_CONTRACT.md`;
6. reconcile the unresolved PCC-01 boundaries sufficiently for the
   first implementation increment;
7. construct one controlled implementation task;
8. implement against the accepted contract;
9. run automated acceptance tests;
10. perform a real Human↔AI↔Termux Experience capture;
11. preserve Evidence;
12. independently audit the result.

Only then may PCC-01 production status be reconsidered.

---

# 52. Working-Draft Warning

This document is a controlled extraction, not yet final normative
Canon.

Its purpose is to make the proposed PCC-01 contract visible enough for
human inspection before implementation.

The human owner may:

- accept;
- reject;
- correct;
- narrow;
- expand;
- request additional Evidence;
- return any requirement to research.

No implementation agent may interpret the existence of this document as
permission to treat unresolved sections as decided.

Human acceptance is the next authority event.
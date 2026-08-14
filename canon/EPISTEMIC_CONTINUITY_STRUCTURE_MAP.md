# Epistemic Continuity Structure Map

Version: 0.1.0

Status: CANON

Classification: Canonical Epistemic Continuity Structure Map

## Purpose

This document explains the role of the principal structures used to preserve
the continuity, history, evidence, knowledge, and current state of the
AI-Toolkit Epistemic Organism.

Its purpose is to allow a human or AI encountering the repository for the
first time to understand what each structure represents and why it exists.

This document is an authoritative Canonical Structure Map of the
AI-Toolkit Epistemic Organism. Its canonical authority derives from
explicit Human Authority.

---

## Structure Map

| Structure | Role | What It Preserves |
|---|---|---|
| Session | Continuous interval of work | Beginning, end, purpose, and transformations produced during the session |
| Transformation | Primary unit of evolution | Need → Research → Decision → Implementation → Result |
| Persistent Experience | Raw lived experience | Conversation, Bash, terminal execution, observations, and reflection |
| Evidence | Proof of what actually occurred | Outputs, tests, files, Git state, runtime observations, and other verifiable evidence |
| Witness | Witness of a transformation | Compact persistent proof that a transformation occurred and what resulted from it |
| Trace | Current position in the evolutionary process | Latest transformation and observed state |
| Lineage | Genealogy of evolution | Relationships between successive transformations and their historical ancestry |
| Memory | Sedimented knowledge | Knowledge that the organism must preserve beyond the session in which it was acquired |
| CSL / Living Project Image | Current demonstrable truth | The current epistemic representation of what the project demonstrably is |

---

## Fundamental Distinction

These structures are related, but they are not synonyms.

### Session

A Session represents a continuous period of work.

It answers:

**During what continuous working context did these transformations occur?**

A Session may contain multiple Transformations.

---

### Transformation

A Transformation is the primary unit of project evolution.

It answers:

**What changed, why did it change, how was the change performed, and what was
the result?**

A Transformation connects:

Need → Research → Decision → Implementation → Execution → Result → Knowledge

---

### Persistent Experience

Persistent Experience preserves the raw experience from which knowledge and
transformations emerge.

It may contain:

- relevant Human ↔ AI conversation;
- exact Bash commands;
- terminal stdout;
- terminal stderr;
- exit codes;
- observations;
- reflections;
- execution context.

It answers:

**What was actually experienced during this work?**

Persistent Experience is not the final interpretation of the experience.

---

### Evidence

Evidence preserves verifiable proof.

Examples include:

- terminal output;
- test results;
- repository files;
- Git commits;
- Git diffs;
- branch state;
- runtime observations;
- validation results.

It answers:

**What proves that this claim or transformation actually occurred?**

---

### Witness

A Witness is the compact persistent witness of a Transformation.

It answers:

**What persistent artifact certifies that this transformation occurred and
records its observed result?**

A Witness does not replace the complete Evidence.

---

### Trace

Trace records the organism's current position in its evolutionary process.

It answers:

**Where are we now?**

It should identify the latest relevant transformation and state without
attempting to reproduce the entire historical chain.

---

### Lineage

Lineage preserves the genealogy of the organism's evolution.

It answers:

**How did the current state descend from previous states and transformations?**

Lineage connects the present to its historical ancestry.

---

### Memory

Memory preserves sedimented knowledge.

It answers:

**What did the organism learn that must survive beyond the conversation or
session in which it was discovered?**

Memory is not intended to duplicate every raw conversation or terminal log.

Raw experience remains Evidence/Persistent Experience.

Memory preserves the knowledge derived from that experience.

---

### CSL / Living Project Image

CSL / Living Project Image represents the current demonstrable truth about
the project.

It answers:

**What does the project demonstrably exist as now?**

It should represent the current state derived from accepted transformations
and available evidence.

It is not the historical transcript.

History explains how the project reached its current state.

The Living Project Image represents what that state currently is.

---

## Relationship Between the Structures

The intended research model is:

Session
    ↓
Persistent Experience
    ↓
Transformation
    ↓
Evidence
    ↓
Witness
    ↓
Lineage
    ↓
Memory
    ↓
CSL / Living Project Image
    ↓
Next Transformation

This sequence must not be interpreted as meaning that each structure contains
the next structure.

It represents their functional relationship within epistemic continuity.

---

## Core Continuity Principle

The current truth must never require the destruction of its history.

The history must explain how the current truth came to exist.

Therefore:

- Persistent Experience preserves what was experienced.
- Transformation preserves what changed.
- Evidence preserves what can be demonstrated.
- Witness preserves that the transformation occurred.
- Lineage preserves how transformations are historically connected.
- Memory preserves what was learned.
- Trace identifies where the organism currently is.
- CSL / Living Project Image represents the current demonstrable state.
- Session groups the continuous work during which these processes occurred.

Together these structures are intended to prevent loss of project context
when the human or AI agent changes, a conversation ends, or development
continues in another environment.

---

## Research Status

This structure map records the current understanding reached during the
Epistemic Continuity research.

The relationships, identifiers, storage contracts, lifecycle rules, and
automation mechanisms remain subject to further research and reconciliation
before canonicalization.

---

## Transformation Completeness Model

A Transformation is considered epistemically complete only when it can answer
the following twelve questions.

These questions define the minimum research model for reconstructing why a
transformation exists, what produced it, what actually occurred, what was
learned, and how the project continues from it.

### 1. Why? — Need

What real need made this Transformation necessary?

---

### 2. What did we research? — Research

What conversations, observations, documents, hypotheses, alternatives, and
existing evidence were examined?

---

### 3. What did we believe before execution? — Hypothesis

What result was expected?

What assumption or proposition was intended to be demonstrated, tested, or
falsified?

---

### 4. What did the human authority decide? — Owner Decision

What did the designated human authority explicitly accept, reject, modify, or
authorize?

AI assistance does not replace the Owner Decision.

---

### 5. What did we intend to change? — Implementation

What transformation was proposed?

This may include Bash, source code, documents, configuration, repository
operations, or other implementation actions.

---

### 6. What was actually executed? — Execution

What commands or actions were actually executed?

Proposed execution and actual execution must not be treated as equivalent.

---

### 7. What actually changed? — Artifacts / Effects

What files, source code, states, commits, configurations, structures, or other
artifacts were actually created, modified, removed, or otherwise affected?

Intended effects and observed effects must remain distinguishable.

---

### 8. What evidence do we have? — Evidence

What verifiable evidence supports the claims about the Transformation?

Evidence may include:

- terminal stdout;
- terminal stderr;
- exit codes;
- test results;
- file contents;
- hashes;
- Git state;
- commits;
- diffs;
- runtime observations;
- validation results;
- other reproducible observations.

---

### 9. Did it work? — Verification

Did the Transformation produce the intended result?

The result may be:

- verified;
- partially verified;
- failed;
- not verified;
- unknown.

Verification must be based on Evidence rather than assumption.

---

### 10. What did we learn? — Knowledge

What new reliable knowledge resulted from the Transformation?

Knowledge must remain distinguishable from hypothesis, assumption, and
unverified interpretation.

---

### 11. How did the organism or project evolve? — Evolution

What new capability, structure, understanding, state, or verified condition
exists after the Transformation?

Evolution may also record regression, loss, or failure when the project did
not improve.

---

### 12. Where does the story continue? — Epic Thread / Next Transformation

From which previous Transformation does this Transformation descend?

How does it contribute to the continuous history of the project?

What unresolved question, need, contradiction, or next Transformation
naturally follows?

---

## Unknown-State Rule

A Transformation must never invent an answer merely to satisfy the
completeness model.

When reliable information is unavailable, the state must be represented
explicitly.

Examples include:

- `UNKNOWN`
- `NOT APPLICABLE`
- `NOT EXECUTED`
- `NOT VERIFIED`
- `NO OWNER DECISION RECORDED`

Absence of knowledge must not be represented as knowledge.

---

## Automation Principle

The twelve-question model does not imply that the human must manually complete
twelve forms for every Transformation.

The Epistemic Organism should eventually derive and preserve as much of this
information as possible from:

- Human ↔ AI conversation;
- research artifacts;
- Bash commands;
- terminal execution;
- Git history and repository state;
- tests;
- runtime observations;
- Evidence;
- CSL / Living Project Image state.

Human authority remains responsible for decisions requiring human approval
and for accepting, rejecting, or correcting the resulting interpretation.

---

## Research Status

This Transformation Completeness Model is part of the authoritative
Epistemic Continuity Canon. Its twelve-question completeness model and
Unknown-State Rule govern Transformation implementation unless explicitly
evolved through Human Authority.

---

# Identity and Relations Research Model

Version: 0.1.0

Status: CANON

Classification: Epistemic Continuity — Identity and Relations

## Purpose

This section defines the current research model for the identity,
human-readable meaning, representation, relations, and navigability of
epistemically significant entities within AI-Toolkit.

The objective is to ensure that the project remains simultaneously:

- precisely identifiable by machines;
- understandable by humans;
- traceable across its evolution;
- navigable during audit;
- capable of producing compact derived representations for AI;
- resistant to context loss.

These principles are authoritative components of the Epistemic Continuity Canon.

---

## 1. Human-Readable Identity Principle

Every epistemically significant entity shall possess both:

1. a stable machine-addressable identifier; and
2. a concise human-readable semantic title.

Human-facing representations shall present both together.

An identifier establishes identity.

A title communicates meaning.

A human shall not be required to resolve opaque identifiers across repository
artifacts merely to understand the project's history, state, decisions,
evidence, or evolution.

### Example

Avoid presenting only:

`TR-0042`

Prefer:

`TR-0042 — Preserve Terminal Experience`

The identifier provides stable identity.

The semantic title provides immediate human understanding.

---

## 2. No Naked Identifier Principle

In any human-facing representation, an epistemic identifier shall not be
presented alone when its semantic title is known.

Human-facing representations should therefore prefer:

`NEED-0031 — Prevent Context Loss`

`DECISION-0019 — Adopt Persistent Experience`

`EXP-0042 — First Captured Terminal Run`

`EV-0103 — Terminal Capture Proof`

`WT-0042 — Terminal Experience Witness`

`MEM-0021 — Execution Context Knowledge`

`STATE-0011 — Persistent Execution Enabled`

instead of presenting only:

`NEED-0031`

`DECISION-0019`

`EXP-0042`

`EV-0103`

`WT-0042`

`MEM-0021`

`STATE-0011`

The project must not require a human to memorize or manually decode its
internal identifiers in order to understand it.

---

## 3. Semantic Identity Rule

A human-readable title is not merely decorative metadata.

It is the semantic component of the entity's human-readable identity.

An epistemic entity may therefore conceptually contain:

### Stable ID

`TR-0042`

### Human Title

`Preserve Terminal Experience`

### Human Display Identity

`TR-0042 — Preserve Terminal Experience`

The Stable ID should remain persistent even if the Human Title is later
improved.

This allows references and relations to remain stable while human-readable
language can evolve under controlled governance.

---

## 4. Human Semantic Priority

Repository structures intended for human understanding should communicate
meaning before requiring technical decoding.

For humans, the semantic title leads understanding.

For machines, the stable identifier guarantees identity.

Therefore:

**The identifier tells the organism which entity it is.**

**The title tells the human what that entity means.**

Both are necessary.

---

## 5. Representation Derivation Principle

Canonical epistemic identity and meaning shall remain independent of any
particular representation.

Human-readable and machine-optimized representations may be derived from the
same canonical knowledge.

Derived representations may reduce redundancy or omit human-readable semantic
titles when identity resolution remains deterministic.

No derived representation may become an independent source of canonical
truth.

### Human-oriented representation

A human-facing representation may show:

`TR-0042 — Preserve Terminal Experience`

`SUPPORTED BY → EV-0103 — Terminal Capture Proof`

`PRODUCES → STATE-0011 — Persistent Execution Enabled`

### Machine-oriented derived representation

An AI-oriented derivative may represent the same knowledge more compactly:

`TR-0042 -> EV-0103 -> STATE-0011`

The compact representation exists for efficiency.

It does not replace the canonical source.

It must remain derivable and resolvable back to the same epistemic entities.

---

## 6. Representation Layers

The current research model therefore distinguishes between:

### Canonical Knowledge

The authoritative identity, meaning, relations, and state.

### Human Representation

Optimized for:

- comprehension;
- semantic clarity;
- navigation;
- explanation;
- audit.

It may contain:

- stable identifiers;
- semantic titles;
- descriptions;
- contextual explanations;
- navigable links.

### AI-Derived Representation

Optimized for:

- reduced information volume;
- reduced token consumption;
- deterministic processing;
- graph traversal;
- machine reasoning;
- efficient context reconstruction.

It may use compact identifiers and relations when their semantic resolution
remains deterministic.

The AI-derived representation remains subordinate to and regenerable from the
authoritative canonical knowledge.

---

## 7. Explicit Relations Principle

Epistemically significant relations must be explicit.

A relation must not be considered established merely because two artifacts:

- have similar names;
- exist in the same directory;
- were created near the same time;
- appear semantically related;
- are inferred to be related by an AI.

For example, a Transformation may explicitly declare relations such as:

`CAUSED BY`

`AUTHORIZED BY`

`SUPPORTED BY`

`WITNESSED BY`

`DERIVED FROM`

`PREVIOUS`

`NEXT`

`PART OF`

`CONTINUES`

`PRODUCED`

`MATERIALIZED BY`

The exact canonical relation vocabulary remains subject to further research.

---

## 8. Human-Readable Relations

Human-facing relation views should preserve semantic identity.

Instead of:

`TR-0042 → EV-0103 → WT-0042 → STATE-0011`

prefer:

`TR-0042 — Preserve Terminal Experience`

`SUPPORTED BY → EV-0103 — Terminal Capture Proof`

`WITNESSED BY → WT-0042 — Terminal Experience Witness`

`PRODUCES → STATE-0011 — Persistent Execution Enabled`

This allows a human to understand the basic epistemic structure without
opening every referenced artifact.

---

## 9. Epistemic Navigability Principle

Every human-visible reference to an epistemically significant entity should,
whenever a resolvable manifestation exists, permit direct navigation to that
entity or to its supporting artifact.

Navigation shall be derived from persistent identity and explicit relations
rather than making epistemic identity dependent upon a filesystem path or
hyperlink.

A human auditor should be able to move from a claim to its:

- Need;
- research;
- Owner Decision;
- Transformation;
- Persistent Experience;
- Evidence;
- Witness;
- implementation;
- Git materialization;
- resulting state;
- Memory;
- historical ancestry;

without manually searching the repository.

---

## 10. Identity Is Not Location

An epistemic entity does not exist merely because a file exists at a
particular path.

The entity possesses an identity.

A file, CSL representation, Git commit, database record, graph node, or other
artifact may be a manifestation or representation of that entity.

Conceptually:

Epistemic Entity
    |
    +-- Identity
    +-- Semantic Meaning
    +-- Properties
    +-- Relations
    +-- Manifestations
            |
            +-- Markdown
            +-- CSL
            +-- Git
            +-- Evidence
            +-- Runtime Representation
            +-- Derived AI Representation

Therefore, moving a file must not automatically destroy the epistemic identity
of the entity it represents.

---

## 11. Navigable Audit Trail

The Living Project Image should eventually allow a human to travel through
the epistemic history of the project.

For example:

`STATE-0011 — Persistent Execution Enabled`

may navigate to:

`TR-0042 — Preserve Terminal Experience`

which may navigate to:

`DECISION-0019 — Adopt Persistent Experience`

which may navigate to:

`EV-0103 — Terminal Capture Proof`

which may navigate to:

- terminal output;
- tests;
- Git diff;
- commit;
- runtime observation.

The same graph should permit historical navigation toward previous states and
Transformations.

The objective is not merely to store history.

The objective is to make history explorable.

---

## 12. Epic Thread as Human-Readable Evolution

The Epic Thread should not be presented to humans merely as a sequence of
opaque identifiers.

A human-readable Epic Thread may appear conceptually as:

`Prevent Context Loss [NEED-0031]`

↓  

`Adopt Persistent Experience [DECISION-0019]`

↓  

`Define Persistent Experience [TR-0040]`

↓  

`Capture Execution Context [TR-0041]`

↓  

`Preserve Terminal Experience [TR-0042]`

↓  

`Persistent Execution Enabled [STATE-0011]`

This allows the evolution of the project to be understood as a meaningful
story rather than a sequence of database-like identifiers.

---

## 13. Identity and EXIST

The Identity and Relations model supports the emerging EXIST research.

For an epistemically significant entity, the organism should eventually be
able to answer:

- What exists?
- What is its stable identity?
- What does it mean?
- Where is it manifested?
- Why does it exist?
- What produced it?
- What preceded it?
- What does it relate to?
- What evidence supports it?
- Who authorized it when human authorization was required?
- What state resulted from it?
- How can a human inspect it?
- How can an AI resolve it deterministically?
- How can its historical ancestry be reconstructed?

Existence and relationship must not depend solely upon AI inference.

---

## 14. Core Identity and Relations Research Statement

Every epistemically significant entity must possess a persistent identity.

Every epistemically significant relationship must be explicit, traceable, and
verifiable.

Identity establishes what exists.

Relations establish how existing things are connected.

Neither existence nor relationship may be inferred merely from filename,
proximity, naming similarity, or AI assumption.

Human-readable representations must additionally communicate semantic meaning
without requiring humans to decode opaque identifiers.

---

## Research Status

The Identity and Relations model records the current accepted direction of
the Epistemic Continuity research.

The identifier schemes, relation vocabulary, resolution mechanisms, CSL
syntax, link generation, storage contracts, and canonical governance rules
remain subject to further research and reconciliation before
canonicalization.

---

# 0.5 — Epistemic Provenance

Version: 0.1.0

Status: CANON

Classification: Epistemic Continuity — Provenance

## Purpose

This section defines the current research model for determining how the
Epistemic Organism knows that something is true.

The objective is not merely to preserve information.

The objective is to preserve the path by which information can become
observation, evidence, verified knowledge, memory, and ultimately part of the
Living Project Image.

The organism must be capable of answering:

- What do we know?
- How do we know it?
- Where did the information originate?
- What was actually observed?
- What evidence supports the conclusion?
- What evidence contradicts it?
- Was it verified?
- When was it verified?
- Is it still current?
- Who authorized a decision when human authority was required?
- What Transformation produced the current state?
- Can a human travel back to the original evidence?

These principles are authoritative components of the Epistemic Continuity Canon.

---

## 0.5.1 — Provenance Anatomy

The current research model distinguishes between:

SOURCE
    ↓
OBSERVATION
    ↓
EVIDENCE
    ↓
CLAIM
    ↓
VERIFICATION
    ↓
KNOWLEDGE
    ↓
CURRENT STATE / LIVING PROJECT IMAGE

These are not synonyms.

Each has a distinct epistemic role.

### Source

A Source identifies where information originated.

Possible sources include:

- Human ↔ AI conversation;
- Owner statement;
- canonical document;
- repository;
- executed action;
- observed running system;
- test;
- external service;
- research material;
- preserved historical artifact.

A Source does not automatically prove a conclusion.

A statement existing in a conversation proves that the statement occurred.

It does not automatically prove that the statement is true.

### Observation

An Observation records what was actually perceived or established from a
Source.

Observation must remain distinguishable from interpretation.

For example:

Human meaning:

"The requested action completed successfully."

Deeper technical evidence may contain implementation-specific details about
how this was observed.

The human does not need to understand those technical details merely to
understand what happened.

### Evidence

Evidence is preserved material capable of supporting or contradicting a
specific Claim.

Evidence should not exist as an unexplained accumulation of logs, files, or
outputs.

Where practical, the organism should know:

- what the Evidence represents;
- where it originated;
- what was observed;
- which Claim it supports;
- which Claim it contradicts;
- when it was produced;
- how it can be inspected.

### Claim

A Claim is an explicit statement about reality.

A Claim does not become true merely because:

- a human wrote it;
- an AI generated it;
- a document contains it;
- implementation appears to support it;
- another Claim resembles it.

A Claim requires appropriate provenance and Evidence.

### Verification

Verification evaluates whether the available Evidence is sufficient and
relevant to establish the Claim.

Evidence must be evaluated relative to the Claim it is intended to support.

Evidence proving that something was designed does not necessarily prove that
it works.

Evidence proving that something works under controlled testing does not
necessarily prove that it works in its real operating environment.

### Knowledge

Knowledge is what the organism may responsibly retain as established or
otherwise epistemically characterized understanding after evaluating the
available Evidence.

Knowledge must preserve the path back to the Claims, Evidence, Observations,
Sources, and Transformations from which it originated.

### Current State

The Current State represents the best-supported understanding of the
organism's present condition.

Current State is not equivalent to all historical Knowledge.

Something may have been true previously without remaining established as true
now.

---

## 0.5.2 — Bidirectional Provenance

Provenance must be traversable in both directions.

### From current truth toward evidence

A human may begin with:

"Persistent Experience is operational."

and travel toward:

Current State
    ↓
Knowledge
    ↓
Verification
    ↓
Claim
    ↓
Evidence
    ↓
Observation
    ↓
Source

This answers:

"Why does the organism believe this?"

### From evidence toward current meaning

A human or AI may begin with an original artifact and travel toward:

Source
    ↓
Observation
    ↓
Evidence
    ↓
Claim
    ↓
Verification
    ↓
Knowledge
    ↓
Affected Current State

This answers:

"What does this evidence actually establish?"

---

## 0.5.3 — Authority Evidence and Technical Evidence

Human authorization and technical truth are different epistemic matters.

If the Owner approves a direction, preserved conversation or another
authoritative record may establish:

"The Owner approved this direction."

It does not automatically establish:

"The resulting implementation works correctly."

Therefore:

**Authority Evidence is not equivalent to Technical Evidence.**

Human authority establishes authorized intent and governance decisions.

Appropriate technical Evidence establishes claims about actual technical
behavior.

Both may be necessary for a Transformation.

---

## 0.5.4 — AI Is Not Automatic Evidence

An AI statement is not Evidence merely because it was generated by an AI.

If an AI states:

"This capability exists."

the organism should be able to establish what was actually inspected or
observed.

Conceptually:

AI Interpretation
       ↓
Inspected Source
       ↓
Observation
       ↓
Evidence
       ↓
Claim

The authority of a conclusion derives from its supporting Evidence rather
than from the identity of the AI or human who formulated it.

---

## 0.5.5 — Contradictory Evidence

Evidence that contradicts a Claim must not be silently discarded.

The organism must be capable of representing:

CLAIM
    │
    ├── SUPPORTING EVIDENCE
    │
    └── CONTRADICTING EVIDENCE
             ↓
        VERIFICATION
             ↓
     CURRENT EPISTEMIC STATE

Contradiction is information.

It must remain visible until it is understood or resolved.

---

## 0.5.6 — Evidence Strength Is Claim-Relative

Not all Evidence has equal value for every Claim.

The strength and relevance of Evidence must be evaluated relative to the
specific Claim.

A document may be excellent Evidence that:

"The Owner defined Requirement X."

The same document may be insufficient Evidence that:

"Requirement X is operational in the real system."

Therefore:

**Evidence strength is relative to the Claim it is intended to support.**

A universal evidence hierarchy shall not be assumed without further research.

---

## 0.5.7 — Human Comprehension Principle

The primary description of an epistemic entity, state, relation, capability,
event, Claim, or result shall express its meaning in language understandable
to a non-software-specialist human.

Technical terminology may exist in engineering views and derived
representations.

Technical terminology shall not be required merely to understand:

- what the organism knows;
- what happened;
- why it happened;
- what resulted;
- whether something succeeded;
- what remains unknown;
- why a conclusion can be trusted.

The governing idea is:

**The human sees the meaning.**

**The auditor sees why it can be trusted.**

**The engineer sees how it is implemented.**

**The AI may consume an optimized representation.**

**All must observe the same underlying reality.**

---

## 0.5.8 — Multiple Views of the Same Reality

The same epistemic reality may have different representations.

### Human View

Answers:

"What does this mean?"

Example:

"The organism preserved what happened during the action."

### Audit View

Answers:

"Why can this be trusted?"

Example:

"The action completed successfully, its result was preserved, and the
supporting evidence is available."

### Engineering View

Answers:

"How was this technically implemented and observed?"

This view may contain implementation-specific terminology, files, execution
details, technical outputs, hashes, identifiers, and other engineering
information.

### AI-Derived View

Answers:

"What is the most efficient deterministic representation required for machine
processing?"

It may contain compact identifiers and relationships.

These views must not create separate truths.

They are different representations of the same underlying epistemic reality.

---

## 0.5.9 — Explicit Epistemic State

The Living Project Image must not force every question into only TRUE or
FALSE.

The organism must be capable of distinguishing conditions such as:

- VERIFIED;
- SUPPORTED;
- PARTIALLY SUPPORTED;
- UNKNOWN;
- CONTRADICTED;
- OUTDATED;
- REFUTED.

This vocabulary remains a research candidate and is not yet canonical.

The important principle is that the organism must represent the actual state
of its knowledge rather than pretending to possess certainty.

---

## 0.5.10 — No Arbitrary Confidence

The organism should not manufacture apparently precise confidence values
without a rigorous basis.

For example:

"Confidence: 87%"

must not be produced merely because an AI estimates that number intuitively.

Epistemic state should remain explainable.

The organism must be able to answer:

"Why is this considered Verified, Supported, Unknown, Contradicted, or
Outdated?"

---

## 0.5.11 — Epistemic Boundary Principle

The organism shall preserve the boundary between:

- what is known;
- what is supported but not fully established;
- what is contradicted;
- what is outdated;
- what has been refuted;
- what remains unknown.

Absence of knowledge shall not be silently replaced by inference.

A valid result may therefore be:

"We do not currently know."

This is not a failure of the organism.

It is an accurate representation of the boundary of its knowledge.

The organism must know not only what it knows, but also where its knowledge
ends.

---

## 0.5.12 — Temporal Truth Principle

Truth within an evolving project has a temporal dimension.

A capability may have been verified previously and later changed.

Historical Evidence must not be destroyed merely because the current state
has changed.

The organism must distinguish between:

"It was verified as true at that time."

and:

"We currently possess sufficient Evidence to establish that it remains true."

Historical truth and current truth are therefore related but distinct.

---

## 0.5.13 — Living Project Image Does Not Erase History

The Living Project Image represents the best-supported current reality.

It does not replace historical Lineage.

Conceptually:

CURRENT PROJECT IMAGE
        │
        ▼
Previous State
        │
        ▼
Transformation
        │
        ▼
Previous State
        │
        ▼
Transformation
        │
        ▼
Earlier State

The project may evolve or involute.

If a capability once existed and later disappeared, the Living Project Image
should represent its current absence while Lineage preserves:

- that it existed;
- when it existed;
- what changed;
- why it changed;
- what Transformation changed it;
- what Evidence supports that history;
- what authority approved the change where required.

---

## 0.5.14 — Human-Navigable Provenance

Human-facing representations should expose meaning before technical detail.

A human may see:

### Persistent Experience — Operational

**What this means**

The organism can preserve important experience from its work and recover it
later.

**Why we believe this**

The behavior was observed and supporting Evidence is available.

**Current knowledge**

VERIFIED

**Explore**

- Why was this created?
- What Evidence supports it?
- What changed?
- Who approved it?
- How does it work technically?
- Show its history.

The human should be able to descend into deeper layers only when desired or
required.

---

## 0.5.15 — Transformation and Provenance

Transformation is not merely a modification.

A Transformation is an explainable transition through which project reality
moves from one state to another.

Conceptually:

STATE A
    │
    │ Need
    │ Research
    │ Decision
    │ Action
    │ Evidence
    │ Verification
    ▼
TRANSFORMATION
    │
    ▼
STATE B

Transformation provides a major temporal and causal backbone for project
history.

It must connect what was needed, understood, decided, performed, observed,
verified, learned, and changed.

---

## 0.5.16 — Provenance Principle

Every epistemically significant Claim must permit reconstruction of where it
came from and what Evidence supports or contradicts it.

---

## 0.5.17 — Observation–Interpretation Separation Principle

What was actually observed must remain distinguishable from what was inferred
or interpreted from the Observation.

---

## 0.5.18 — Claim-Relative Evidence Principle

Evidence strength and relevance must be evaluated relative to the specific
Claim it supports or contradicts.

---

## 0.5.19 — Authority–Technical Evidence Separation Principle

Evidence that a human authority approved a decision does not by itself
demonstrate that the resulting technical Claim is true.

---

## 0.5.20 — Contradictory Evidence Preservation Principle

Evidence contradicting a Claim must not be silently discarded, hidden, or
overridden merely because supporting Evidence also exists.

---

## 0.5.21 — Temporal Truth Principle

A verified state may cease to be current without ceasing to be historically
true.

Historical truth must remain preserved while the Living Project Image
represents the best-supported current state.

---

## 0.5.22 — Provenance and EXIST

Provenance provides part of the mechanism through which EXIST may eventually
be enforced.

When the organism presents something as existing or true, it should
eventually be capable of answering:

- What is it?
- What does it mean?
- What is its identity?
- What Claim is being made?
- What was observed?
- What Evidence supports it?
- What Evidence contradicts it?
- Was it verified?
- When was it verified?
- Is that verification still current?
- What produced it?
- What preceded it?
- Who authorized it where authority was required?
- Where can the original Evidence be inspected?

Thus:

**The organism should not merely state reality.**

**It should preserve the path that gives it the right to make the statement.**

---

# 0.6 — Layered Epistemic Memory

Version: 0.1.0

Status: CANON

Classification: Epistemic Continuity — Memory

## Purpose

This section defines the current research model for how AI-Toolkit may
preserve very large amounts of experience without requiring all preserved
information to remain continuously present in active AI context.

The organism must be capable of preserving years of evolution while recalling
only the knowledge relevant to the current purpose.

The central idea is:

**Preservation does not mean permanent cognitive loading.**

The organism may preserve very large amounts of experience while bringing
only relevant knowledge into active context.

---

## 0.6.1 — Memory Depth

The current research model distinguishes progressively different levels of
epistemic depth.

Conceptually:

CURRENT PURPOSE
      │
      ▼
ACTIVE CONTEXT
      ↕
LIVING PROJECT IMAGE
      ↕
ESTABLISHED KNOWLEDGE
      ↕
SEMANTIC MEMORY
      ↕
EPISODIC MEMORY
      ↕
TRANSFORMATIONS
      ↕
PERSISTENT EXPERIENCE
      ↕
EVIDENCE
      ↕
ORIGINAL SOURCES

These levels must not be interpreted prematurely as mandatory software
directories.

They represent epistemic roles.

---

## 0.6.2 — Meaning Increases Upward, Detail Increases Downward

As information moves upward through memory:

- informational volume should generally decrease;
- semantic concentration should increase;
- current relevance should increase;
- orientation should become easier.

As a human or AI moves downward:

- historical context increases;
- detail increases;
- original experience becomes accessible;
- Evidence becomes directly inspectable.

Therefore:

**The higher we travel through memory, the greater the concentration of
meaning and the smaller the information volume.**

**The deeper we travel, the greater the contextual detail until we reach the
original experience and Evidence.**

---

## 0.6.3 — Not Everything Experienced Becomes Memory

The organism may experience much more than it needs to retain as active or
semantic Memory.

A research session may contain:

- important discoveries;
- accepted principles;
- rejected ideas;
- operational confirmations;
- temporary questions;
- repeated explanations;
- execution details;
- incidental conversation.

All relevant original experience may remain preserved.

Not all of it must become higher-level Memory.

Conceptually:

EXPERIENCE
    ↓
What happened?
    ↓
What is significant?
    ↓
What was learned?
    ↓
What should be remembered?
    ↓
What changes the current image?

---

## 0.6.4 — Epistemic Sedimentation

Epistemic Sedimentation is the process through which preserved experience is
interpreted, related to existing knowledge, and transformed in a controlled
manner into Memory and Knowledge.

Conceptually:

ORIGINAL EXPERIENCE
        │
        ├─────────────────────┐
        ▼                     │
INTERPRETATION                │
        ↓                     │
MEMORY                        │
        ↓                     │
KNOWLEDGE                     │
                              ▼
                    ORIGINAL EXPERIENCE
                    REMAINS PRESERVED

Sedimentation must not rewrite original experience.

If a later discovery shows that an earlier interpretation was wrong, the
organism must remain capable of returning to the original experience.

---

## 0.6.5 — Non-Duplicative Memory Principle

Higher memory levels should preserve meaning, relationships, and learned
knowledge rather than unnecessarily duplicating lower-level experience.

For example, a long research conversation may produce a concise semantic
Memory.

The concise Memory should preserve its relationship to the research from
which it originated.

Therefore:

**Memory should preserve what was learned, not simply copy everything that
was experienced.**

---

## 0.6.6 — Preservation and Promotion Are Different

Preserving experience and promoting an interpretation into higher Memory are
different operations.

The organism should not depend entirely upon an AI deciding:

"This is important."

and:

"This is not important."

Relevant original experience should remain preserved independently of later
sedimentation.

An AI may identify possible significance and propose higher-level Memory.

Fundamental conclusions, Owner Decisions, Canonical changes, architectural
principles, and other governed knowledge must remain subject to the
appropriate human and canonical authority.

---

## 0.6.7 — Memory Stability Levels

The research currently distinguishes several possible memory roles.

### Working Memory

Information required for the current activity.

Example:

"We are currently researching layered epistemic memory."

### Episodic Memory

What happened during a particular experience.

Example:

"During Epistemic Continuity research, the Owner identified uncontrolled
memory growth as a future problem."

### Semantic Memory

Meaning sedimented from experience.

Example:

"Preservation does not require permanent cognitive loading."

### Established Knowledge

Understanding that has been sufficiently supported and accepted for the
relevant epistemic purpose.

Example:

"The project must carry its own continuity."

### Canonical Knowledge

Knowledge that has passed through the required canonical governance process
and possesses canonical authority.

These categories are research concepts.

They are not yet finalized as canonical storage structures.

---

## 0.6.8 — Living Project Image and Active Context

The Living Project Image is not the entirety of the organism's Memory.

It represents a condensed image of the best-supported

# 0.7 — Epistemic Continuity Chain

Status: CANON

Classification: Epistemic Continuity Research

Purpose: Define how project experience becomes a continuous, explainable, verifiable, navigable, and transferable history of project evolution.

This section builds upon the previously established research concerning Persistent Experience, Transformation, Evidence, Witness, Trace, Lineage, Memory, Provenance, Layered Epistemic Memory, Progressive Recall, and the future CSL Living Project Image.

The central problem addressed here is not merely how information is stored.

The problem is how the project preserves the meaning of its own evolution.

A project must be able to explain:

- what was needed;
- what was observed;
- what was researched;
- what was proposed;
- what was decided;
- what was rejected;
- what action was taken;
- what actually happened;
- what evidence was produced;
- what was verified;
- what was learned;
- what changed;
- what remains unresolved;
- and how the present state emerged from previous states.

The objective is continuity that belongs to the project rather than to the temporary memory of any external AI agent, conversation, terminal session, or human recollection.

---

## 0.7.1 — Anatomy of a Complete Experience

A complete experience is not merely a conversation.

It is not merely a Bash command.

It is not merely terminal output.

It is not merely a commit.

It is not merely the artifact that eventually results.

All of these may be parts of an experience.

A complete epistemic experience is the explainable history of how the project moved from one meaningful condition to another.

Conceptually:

HUMAN NEED
    ↓
CONVERSATION / RESEARCH
    ↓
UNDERSTANDING
    ↓
DECISION
    ↓
TRANSFORMATION
    ↓
ACTION
    ↓
EXPERIENCE
    ↓
OBSERVATION
    ↓
EVIDENCE
    ↓
VERIFICATION
    ↓
LEARNING
    ↓
MEMORY
    ↓
KNOWLEDGE
    ↓
LIVING PROJECT IMAGE

The chain must not be interpreted as a mandatory rigid sequence.

Its purpose is to expose the meaningful relationships through which project reality evolves.

Example:

NEED

"The project must not lose its context when an AI conversation reaches its context limit."

    ↓

RESEARCH

How can project continuity become independent of the temporary AI session?

    ↓

UNDERSTANDING

The memory required for continuity must belong to the project rather than exclusively to the external AI agent.

    ↓

DIRECTION

Persistent Experience
Epistemic Provenance
Layered Memory
Progressive Recall
Context Packages
Living Project Image

    ↓

ACTION

Research findings are preserved inside the project.

    ↓

RESULT

The project possesses part of the knowledge required to explain its own epistemic evolution.

    ↓

EVIDENCE

Research artifacts
repository history
captured experience
verification records

    ↓

MEMORY

The organism can preserve what it learned.

    ↓

LIVING PROJECT IMAGE

The best-supported representation of current project reality evolves.

The complete experience therefore preserves meaning, not merely events.

---

## 0.7.2 — Transformation as the Semantic Envelope of Change

Transformation is the principal semantic unit through which project evolution is understood.

A Transformation should explain:

What reality existed before?

Why was change necessary?

What need, observation, contradiction, opportunity, or question initiated the change?

What research occurred?

What alternatives were considered?

What decision was made?

What action was actually performed?

What happened during execution?

What evidence was produced?

What was verified?

What was learned?

What reality exists afterward?

Conceptually:

TRANSFORMATION

BEFORE
What was true before the transformation?

NEED / TRIGGER
Why did change become necessary?

RESEARCH
What did we attempt to understand?

DECISION
What was accepted, rejected, deferred, or left unresolved?

ACTION
What was actually done?

EXPERIENCE
What happened while the action was performed?

EVIDENCE
What observations or artifacts support the result?

VERIFICATION
What was checked?

LEARNING
What did the organism learn?

AFTER
What can now be demonstrated to be true?

A Transformation is therefore not merely a change record.

It is an explainable bridge between two project realities.

---

## 0.7.3 — Reality Must Not Be Forced Into a Fictional Workflow

Not every Transformation begins with a clearly articulated need.

Real project evolution is irregular.

Sometimes the first event is an observation:

OBSERVATION

"Something is not working."

    ↓

INVESTIGATION

    ↓

DISCOVERED NEED

    ↓

RESEARCH

    ↓

DECISION

    ↓

ACTION

In another case:

IDEA
    ↓
RESEARCH
    ↓
NEW NEED DISCOVERED

In another:

ACTION
    ↓
UNEXPECTED RESULT
    ↓
NEW RESEARCH
    ↓
NEW TRANSFORMATION

The continuity model must therefore describe the actual process rather than forcing the actual process into an artificial template.

This follows directly from Reality First.

A Transformation may contain absent, unresolved, unknown, deferred, or inapplicable stages when that is what actually occurred.

The organism must preserve the truth of the process rather than manufacture completeness.

---

## 0.7.4 — Conversation Is Experience, Not Automatically Canonical Truth

Human ↔ AI conversation is a critical source of project experience.

It may contain:

- needs;
- questions;
- observations;
- ideas;
- hypotheses;
- alternatives;
- research;
- explanations;
- proposals;
- preferences;
- decisions;
- approvals;
- rejections;
- corrections;
- uncertainty;
- unresolved questions;
- reflections;
- discoveries.

These elements are epistemically valuable because they may explain why the project evolved.

However, conversation is not automatically Canon.

A proposal made during research may later be rejected.

A hypothesis may later be falsified.

A temporary preference may later change.

An AI interpretation may be wrong.

A human may reconsider an earlier decision.

Therefore:

CONVERSATION
    ↓
PERSISTENT EXPERIENCE
    ↓
INTERPRETATION
    ↓
CLASSIFICATION
    ↓
DECISIONS / FINDINGS / QUESTIONS / HYPOTHESES
    ↓
VERIFICATION WHERE APPLICABLE
    ↓
MEMORY
    ↓
KNOWLEDGE
    ↓
CURRENT PROJECT REALITY

The conversation preserves the evolution of thought.

The Living Project Image must preserve the best-supported current understanding.

The two must remain connected without being confused.

---

## 0.7.5 — Preservation of Idea Evolution

The project should preserve not only final decisions but the meaningful genealogy through which important ideas developed.

Example:

PROBLEM

AI conversation loses context.

    ↓

INITIAL IDEA

Preserve conversations.

    ↓

REALIZATION

Raw preservation will accumulate very large amounts of information.

    ↓

NEW QUESTION

How can the organism preserve experience without loading all historical information into every working context?

    ↓

HUMAN ANALOGY

Human beings do not consciously recall every experience simultaneously.

    ↓

RESEARCH

Layered Epistemic Memory.

    ↓

FINDING

Progressive Recall.

    ↓

FINDING

Context Packages.

    ↓

CURRENT DIRECTION

The project carries the continuity required by humans and future AI agents.

This is the genealogy of an idea.

It allows future humans and AI systems to answer not only:

"What was decided?"

but also:

"Why did this idea appear?"

"What problem was it intended to solve?"

"What alternatives existed?"

"What changed our understanding?"

"Which previous concept produced this one?"

"What evidence or experience caused the transition?"

This genealogy is part of the epic thread of the project.

---

## 0.7.6 — Granularity Without Human Cognitive Overload

The system must not require a human to navigate thousands or millions of meaningless granular records merely to understand project evolution.

It would be possible to preserve every message as:

MSG-000001
MSG-000002
MSG-000003
...
MSG-900000

but such a representation would be hostile to human understanding.

Raw experience may preserve individual messages when required for evidence and reconstruction.

The semantic continuity layer should instead expose meaningful moments.

Example:

RESEARCH EPISODE — Layered Epistemic Memory

Meaningful moments:

- Owner identifies uncontrolled memory growth.
- Human-memory analogy is introduced.
- Layered memory model is proposed.
- Owner accepts the research direction.
- Progressive Recall is derived.
- Context Independence is established.

The human can understand the episode immediately.

If stronger verification is required, the human or AI can travel downward toward the original experience.

Therefore:

preserve granular evidence;

present meaningful structure.

Granularity must remain available without becoming the primary human interface.

---

## 0.7.7 — Bash Is an Action, Not the Transformation

A Bash script is not itself the meaning of a project transformation.

It is a technical representation of an action, or a collection of actions.

For example, the human-level meaning may be:

"The second research audit was preserved inside the project."

The action may be described as:

"Install the downloaded research audit into the project's preserved audit history."

The verification may state:

- source identified;
- destination verified;
- existing material protected;
- copied artifact verified;
- resulting repository state inspected.

Only at the deeper engineering or evidence level is it necessary to expose commands such as:

cp
sha256sum
git status

The human should not need to understand these technical commands merely to understand what happened to the project.

Technical detail remains available for audit, engineering, reproduction, and evidence.

Meaning remains primary in human-facing representations.

---

## 0.7.8 — Terminal Output Is Observed Experience

Terminal output is an important form of observed experience and evidence.

However, raw output may contain thousands of lines.

The Living Project Image must not become a copy of terminal history.

The organism should be capable of preserving the original output while sedimenting its meaning.

For example, raw terminal output may demonstrate that synchronization occurred.

The human-facing meaning may be:

"The synchronization completed successfully and the local project matched the authoritative repository state."

If an auditor asks:

"How do we know?"

the system should be capable of navigating to the original terminal evidence.

This establishes a distinction between:

MEANING

and

RAW EVIDENCE

Both are valuable.

They serve different cognitive purposes.

---

## 0.7.9 — Git Is a Powerful Witness, but Not the Whole Story

Version history can demonstrate important facts about project evolution.

It may establish:

- what artifacts changed;
- when a recorded change occurred;
- what version resulted;
- what content was added;
- what content was removed;
- which structural state followed another.

But version history does not necessarily explain why the change occurred.

Conversation, research, owner decisions, and project needs may contain the reason.

Transformation joins these worlds.

HUMAN / AI EXPERIENCE
        │
        │ WHY?
        ▼
   TRANSFORMATION
        ▲
        │ WHAT ACTUALLY CHANGED?
        │
   VERSION HISTORY

Neither should be mistaken for the other.

Together they provide stronger continuity.

---

## 0.7.10 — Witness as Compact Verification of Transformation

Witness should not duplicate all Evidence.

A Witness is the compact record that a meaningful transformation occurred and indicates where its supporting traces can be verified.

Example:

WT-0042 — Research Memory Preservation

Transformation:
Preserve Epistemic Memory Research

Observed Result:
The research artifact became part of the preserved project history.

Evidence:
- preserved research artifact;
- repository state;
- version history;
- verification record.

Outcome:
SUCCESS

The human can inspect the compact Witness.

An auditor can travel from Witness to Evidence.

A deeper investigation can travel from Evidence to original Experience.

Witness therefore provides cognitive compression without severing provenance.

---

## 0.7.11 — Session Is Not Transformation

Session and Transformation represent different dimensions of project continuity.

A Session represents a continuous interval of work.

A Transformation represents a meaningful line of project evolution.

One Session may contain multiple Transformations:

SESSION

├── Transformation A
├── Research Episode
├── Transformation B
├── Unresolved Question
└── Transformation C

A single Transformation may also cross multiple Sessions:

SESSION 1
    └── Research
          │
SESSION 2
    └── Decision
          │
SESSION 3
    └── Implementation
          │
SESSION 4
    └── Verification

Therefore:

Session represents temporal continuity of work.

Transformation represents semantic continuity of change.

The two must be linked but must never be treated as equivalent.

---

## 0.7.12 — Transformations Have Genealogy

A Transformation may produce the need for other Transformations.

Example:

TR — Prevent Context Loss
    │
    ├── TR — Preserve Persistent Experience
    │
    ├── TR — Establish Epistemic Provenance
    │
    ├── TR — Establish Layered Memory
    │
    └── TR — Generate AI Context Packages

The project therefore develops a transformation lineage.

A future human or AI should be able to understand:

- which Transformation produced another;
- which problem generated a Transformation;
- which previous finding made it necessary;
- which decision authorized it;
- what project state preceded it;
- what project state followed it.

Transformations should therefore form an intelligible genealogy rather than an unstructured chronological list.

Human-facing representations must obey the Human-Readable Identity Principle.

For example:

TR-0042 — Establish Layered Memory

is preferable to:

TR-0042

A stable identifier establishes identity.

A concise semantic title communicates meaning.

---

## 0.7.13 — Continuity Must Cross AI Boundaries

The major test of epistemic continuity is whether project work can continue when the external AI agent changes.

A new AI agent should not need personal memory of the previous conversation.

The project itself should be capable of communicating the context required for continuation.

Conceptually, a future context package may contain:

PROJECT IDENTITY

AI-Toolkit

CURRENT PURPOSE

Build project-owned epistemic continuity.

CURRENT RESEARCH

Epistemic Continuity.

ESTABLISHED DIRECTION

- Persistent Experience
- Transformation
- Provenance
- Layered Memory
- Progressive Recall
- Context Independence

OWNER-ACCEPTED RESEARCH PRINCIPLES

- Human-readable identities
- No naked identifiers
- Human comprehension first
- Navigable provenance
- Project-owned continuity

CURRENT FRONTIER

The current research question or transformation frontier.

RECENT EVOLUTION

The recent meaningful changes that produced the current frontier.

DEEPER CONTEXT

Resolvable paths toward:

- research documents;
- relevant Transformations;
- original Experience;
- Evidence;
- decisions;
- historical states.

The new AI does not need to remember the previous conversation.

The project explains what it is, what has happened, what is currently understood, and where deeper evidence can be found.

This is the foundation of AI-independent project continuity.

---

## 0.7.14 — Progressive Context Expansion

A Context Package must not become an epistemic prison.

A new AI or human may discover that the initial context is insufficient.

For example:

"To evaluate this decision I need to understand why the Owner rejected Alternative X."

The organism should permit progressive travel:

CONTEXT PACKAGE
    ↓
RELEVANT DECISION
    ↓
RESEARCH EPISODE
    ↓
CONVERSATION EXPERIENCE
    ↓
ORIGINAL OWNER STATEMENT

This is Progressive Recall applied to project continuity.

The system should provide the minimum useful context first and deeper context when required.

The organism therefore behaves more like navigable memory than a gigantic prompt.

---

## 0.7.15 — Continuity Preservation Should Be Predominantly Automatic

The human should not be required to manually write a historical report after every working session.

If project continuity depends on the human repeatedly reconstructing:

"What did we discuss?"

"What did we decide?"

"What command did I run?"

"What happened?"

"Why did we do it?"

then the continuity problem has merely been transferred from the AI to the human.

The target physiology is:

HUMAN + AI WORK NORMALLY
        ↓
ORGANISM OBSERVES
        ↓
ORGANISM PRESERVES EXPERIENCE
        ↓
ORGANISM IDENTIFIES POSSIBLE TRANSFORMATIONS
        ↓
ORGANISM CONNECTS EVIDENCE
        ↓
ORGANISM PROPOSES SEDIMENTATION
        ↓
HUMAN AUTHORITY WHERE REQUIRED
        ↓
MEMORY / KNOWLEDGE
        ↓
LIVING PROJECT IMAGE

Human intervention should primarily provide authority, judgment, clarification, and governance.

Mechanical preservation should increasingly belong to the organism.

---

## 0.7.16 — Automation Must Not Invent Meaning

Automatic capture does not grant automatic authority.

An AI may incorrectly infer:

"This was the Owner's decision."

when the human was only exploring a possibility.

The continuity system must therefore distinguish categories such as:

QUESTION

IDEA

HYPOTHESIS

PROPOSAL

OWNER PREFERENCE

OWNER DECISION

RESEARCH FINDING

VERIFIED FINDING

CANONICAL DECISION

These categories must not be silently collapsed into one another.

A statement such as:

"Yes, perhaps that would be useful."

must not automatically become:

OWNER DECISION — Mandatory Architecture

Epistemic classification and human authority must remain distinct.

---

## 0.7.17 — Explicit Uncertainty in Human Intent

The organism must be capable of admitting uncertainty about what the human meant.

Suppose a human says:

"Okay, do that."

but several proposals are active in the immediate context.

The organism must not fabricate the object of approval.

It should be capable of representing:

DECISION ATTRIBUTION UNCERTAIN

and, where the ambiguity materially affects project reality:

HUMAN CLARIFICATION REQUIRED

This applies the Epistemic Boundary Principle directly to Human ↔ AI interaction.

Unknown intent must remain unknown until sufficiently established.

---

## 0.7.18 — Capture Before Interpretation Principle

An important principle follows from the previous sections.

### Capture Before Interpretation Principle

Epistemically significant original Experience should be preserved before, or independently of, its later interpretation, condensation, classification, or sedimentation.

The reason is fundamental:

interpretation can be wrong.

If the interpretation later proves incorrect, the organism must be able to return to the original experience.

In human language:

First preserve what happened.

Then determine what it means.

The derived interpretation must never erase the original evidence from which it was produced.

---

## 0.7.19 — Semantic Continuity Principle

### Semantic Continuity Principle

Project continuity shall preserve not only chronological events but the meaningful relationships through which needs, research, decisions, actions, evidence, learning, and state changes produced one another.

A chronological log may say:

10:02 — message
10:05 — command
10:07 — output
10:15 — commit

Semantic continuity asks:

WHY?

    ↓

WHAT DID WE LEARN?

    ↓

WHAT DID WE DECIDE?

    ↓

WHAT DID WE DO?

    ↓

WHAT HAPPENED?

    ↓

WHAT PROVES IT?

    ↓

WHAT CHANGED?

Chronology is necessary.

Chronology alone is insufficient.

Semantic relationships transform history into continuity.

---

## 0.7.20 — Session-Independent Continuity Principle

### Session-Independent Continuity Principle

No Transformation shall depend for its intelligibility upon the continued availability of the AI session in which part of that Transformation occurred.

A Transformation may begin in one AI conversation and continue through several later sessions or different AI agents.

Its semantic identity must survive those boundaries.

The project, not the external conversation, must own the continuity.

---

## 0.7.21 — Human Preservation Burden Principle

### Human Preservation Burden Principle

The human shall not be required to manually reconstruct project history that the organism could have captured from the work as it occurred.

In human terms:

The human should build the project.

The human should not become the secretary of the project's memory.

Human authority remains essential.

Mechanical memory work should increasingly belong to the organism.

---

## 0.7.22 — Continuity Physiology

The research developed so far can be represented as:

HUMAN PURPOSE
    ↓
NEED
    ↓
RESEARCH
    ↓
DECISION
    ↓
TRANSFORMATION
    ↓
ACTION
    ↓
EXPERIENCE
    ↓
OBSERVATION
    ↓
EVIDENCE
    ↓
WITNESS
    ↓
VERIFICATION
    ↓
LEARNING
    ↓
MEMORY
    ↓
KNOWLEDGE
    ↓
LIVING PROJECT IMAGE
    ↓
CURRENT PURPOSE
    ↓
CONTEXT PACKAGE
    ↓
HUMAN + NEXT AI

The cycle then continues.

The result is no longer a sequence of disconnected AI conversations.

It is an epistemic organism capable of accumulating experience and carrying its own continuity across working sessions.

## 0.7.23 — Automatic Experience Capture Boundary

The organism must determine what should be captured automatically from lived project work.

The objective is not simply:

"Store everything."

Nor is the objective:

"Store only what an AI currently considers important."

Both extremes are dangerous.

Capturing everything indiscriminately can produce an enormous accumulation of duplicated, low-value, or reconstructible information.

Capturing only what appears important at the moment risks destroying information whose significance becomes visible only later.

The correct objective is:

Preserve sufficient original experience to allow faithful reconstruction of project evolution while avoiding unnecessary duplication and uncontrolled accumulation.

This requires an explicit distinction between:

CAPTURE

and

RETENTION.

Conceptually:

LIVED REALITY
    ↓
CAPTURE
    ↓
CLASSIFICATION
    ↓
EPISTEMIC RELEVANCE
    ↓
PRESERVE / CONDENSE / REFERENCE / DISCARD

However, DISCARD must be treated conservatively.

The organism must not casually destroy information merely because an AI agent currently believes that information is unimportant.

Future significance cannot always be predicted from present context.

---

## 0.7.24 — Four Conceptual Information Classes

For continuity research, captured information can initially be understood through four conceptual classes.

These classes are a research model and are not yet a finalized canonical taxonomy.

### A — Experience of Record

Experience of Record directly describes meaningful project evolution.

Examples include:

- human requirements;
- important observations;
- owner decisions;
- approvals;
- rejections;
- corrections;
- research conclusions;
- changes of direction;
- executed actions;
- significant action results;
- important failures;
- verification results;
- evidence;
- project modifications;
- meaningful before/after states.

This information forms part of the organism's historical experience.

It should normally remain preservable and traceable.

### B — Supporting Experience

Supporting Experience contributes to understanding or reconstructing an epistemically significant event but may not need to become long-term semantic Memory.

Examples may include:

- intermediate explanations;
- exploratory discussion;
- alternatives considered;
- detailed technical observations;
- intermediate outputs;
- supporting reasoning context.

Supporting Experience may become important when a decision, interpretation, or Transformation is later challenged.

It therefore should remain reachable where required by provenance.

### C — Reconstructible Detail

Some information can be regenerated or retrieved from an authoritative preserved source without copying it repeatedly into epistemic memory.

For example:

EVIDENCE
    ↓
REFERENCE
    ↓
ORIGINAL ARTIFACT

is preferable to:

EVIDENCE
    ↓
COPY
COPY
COPY
COPY

when all copies would represent the same underlying information.

The organism should prefer identity and reference over unnecessary duplication.

### D — Epistemic Noise

Some captured information may contribute no meaningful new information to identity, continuity, evidence, understanding, or project evolution.

For example:

the same unchanged state printed repeatedly hundreds of times.

However, classification as Epistemic Noise must be conservative.

Noise should be demonstrable rather than assumed.

The system must avoid using "noise reduction" as justification for destroying potentially important history.

---

## 0.7.25 — Human ↔ AI Conversation Capture

Human ↔ AI conversation is one of the most important continuity sources because it often contains something that implementation artifacts and version history cannot independently provide:

INTENT.

Conversation may explain:

- why work began;
- what the human actually wanted;
- what problem was perceived;
- which alternatives were considered;
- what was misunderstood;
- what was corrected;
- what was rejected;
- what was accepted;
- what remained unresolved;
- why the project changed direction.

The organism should therefore be capable of identifying meaningful conversational categories such as:

NEED

QUESTION

OBSERVATION

IDEA

HYPOTHESIS

RESEARCH FINDING

PROPOSAL

OWNER PREFERENCE

OWNER DECISION

REJECTION

CORRECTION

UNRESOLVED QUESTION

These classifications must remain connected to the original experience.

For example, Memory may eventually contain:

OWNER DECISION — Adopt Layered Epistemic Memory

but provenance should permit navigation toward:

- the research episode;
- the relevant conversation;
- the original owner statement;
- the surrounding context.

Semantic sedimentation must not destroy the path back to lived experience.

---

## 0.7.26 — Not Every Human Agreement Is an Owner Decision

Natural conversation contains expressions such as:

"yes"

"okay"

"continue"

"I agree"

"that sounds good"

"let us investigate that"

These statements do not necessarily possess the same epistemic or governance meaning.

For example:

"Continue researching this approach."

does not mean:

"This approach is now approved Canon."

Likewise:

"This seems useful."

does not necessarily mean:

"This is now an architectural requirement."

The organism must therefore preserve the scope of human authorization.

Conceptually:

OWNER STATEMENT
    ↓
WHAT WAS THE STATEMENT RESPONDING TO?
    ↓
WHAT EXACTLY WAS ACCEPTED?
    ↓
WHAT WAS THE AUTHORITY LEVEL?
    ↓
Research acceptance?
Working direction?
Engineering decision?
Canonical approval?
Permission to continue?

The meaning of human approval must remain bounded by demonstrable context.

---

## 0.7.27 — Authority Scope Principle

### Authority Scope Principle

A human statement of agreement or authorization shall be interpreted only within the scope demonstrably supported by its conversational and governance context.

In human terms:

A "yes" cannot authorize more than the human actually said yes to.

This principle protects the project against authority inflation.

Acceptance of a research direction does not automatically constitute canonical approval.

Acceptance of an implementation experiment does not automatically modify project architecture.

Permission to continue does not automatically approve every proposition previously discussed.

Where authority scope is uncertain, the uncertainty must remain explicit.

---

## 0.7.28 — Capture of Executed Actions

When an action is executed through a technical environment such as Termux, the organism should eventually be capable of preserving at least three human-understandable dimensions:

INTENTION

What were we trying to accomplish?

ACTION

What was actually done?

OUTCOME

What happened?

For example:

INTENTION

Bring the latest authoritative project state onto the phone.

ACTION

Synchronize the local project with its authoritative repository.

OUTCOME

Synchronization succeeded and both copies represented the same project version.

This human-facing description preserves meaning.

Technical details remain available at deeper levels for engineering and audit.

The organism should not require a human to understand command-line syntax merely to understand project history.

---

## 0.7.29 — Linking Technical Execution to the Conversation That Produced It

A major continuity problem exists when work is fragmented between different environments.

A typical present-day workflow may be:

HUMAN
    ↓
expresses a need in conversation

AI
    ↓
proposes an action

HUMAN
    ↓
copies the proposed Bash

TERMUX
    ↓
executes the action

TERMINAL
    ↓
produces output

HUMAN
    ↓
copies output back into conversation

AI / HUMAN
    ↓
interprets the result

These are not seven unrelated historical events.

They are parts of one meaningful experience.

The organism should eventually be capable of reconstructing:

HUMAN NEED
    ↓
AI RECOMMENDATION
    ↓
PROPOSED ACTION
    ↓
HUMAN EXECUTION
    ↓
OBSERVED RESULT
    ↓
INTERPRETATION
    ↓
VERIFICATION
    ↓
PROJECT CHANGE

This relationship is essential for preserving causality and meaning.

---

## 0.7.30 — Action Identity

Epistemically significant actions should possess stable identity.

Human-facing representations must obey the Human-Readable Identity Principle.

Instead of:

ACT-0182

the human should see:

ACT-0182 — Synchronize Phone With Authoritative Project

The identifier establishes stable machine-addressable identity.

The title communicates meaning.

An Action can then be related to its parent Transformation.

For example:

TR-0042 — Establish Project-Owned Continuity
    │
    └── ACT-0182 — Synchronize Phone With Authoritative Project

Deeper representations may expose the exact technical execution.

The human-facing representation should first expose the purpose and meaning of the action.

---

## 0.7.31 — Outcome Classification

The completion of an action does not automatically demonstrate achievement of the intended result.

The organism must distinguish conditions such as:

ACTION COMPLETED

ACTION FAILED

ACTION PARTIALLY COMPLETED

OUTCOME UNKNOWN

OUTCOME CONTRADICTED

A technical process may terminate successfully while failing to produce the intended project outcome.

Therefore:

EXECUTION SUCCESS

is not equivalent to:

GOAL SUCCESS.

The intended reality must be compared with the observed reality.

---

## 0.7.32 — Intention–Outcome Separation Principle

### Intention–Outcome Separation Principle

The successful completion of an action shall not by itself establish that the intended project outcome was achieved.

The complete relationship is:

INTENTION
    ↓
ACTION
    ↓
OBSERVED RESULT
    ↓
DOES THE RESULT SATISFY THE INTENTION?
    ↓
VERIFICATION

This protects the organism from confusing technical completion with actual success.

The project must establish what changed in reality.

---

## 0.7.33 — Version History as Evidence of Structural Change

In human-facing epistemic language, version history should not be reduced to opaque technical terminology such as commit identifiers, branch names, or hashes.

These details remain important for engineering and verification.

But their human meaning is broader:

version history provides verifiable traces of changes to the body of the project.

When a Transformation modifies the organism, the continuity model should be able to answer:

What changed in the organism?

Where is the evidence of that change?

What existed before?

What exists afterward?

Which preserved technical record demonstrates the transition?

Technical version-control information therefore becomes a deeper evidence layer rather than the primary language through which the human must understand the project.

---

## 0.7.34 — Before and After State

For significant Transformations, the organism should preserve enough information to establish:

BEFORE

What could be demonstrated to be true before the Transformation?

and:

AFTER

What can be demonstrated to be true after the Transformation?

Conceptually:

STATE 41
    ↓
TRANSFORMATION A
    ↓
STATE 42
    ↓
TRANSFORMATION B
    ↓
STATE 43

This produces the evolutionary thread of the organism.

Without BEFORE, the result may be visible but the meaning of the change is weakened.

Without AFTER, the intended action may be known but the actual resulting reality remains uncertain.

---

## 0.7.35 — State Change Instead of Unnecessary Full Duplication

Preserving Before and After does not imply creating a complete duplicate of the entire project after every action.

That would create uncontrolled information growth.

The organism should distinguish between:

FULL STATE

and:

STATE CHANGE.

Where possible:

STATE 42
+
TRANSFORMATION B
+
DEMONSTRATED CHANGE
=
STATE 43

The historical state may be reconstructible through lineage and authoritative preserved artifacts.

The continuity system should prefer meaningful change records and resolvable history over unnecessary duplication.

---

## 0.7.36 — Failure Is Experience

Failure is not disposable history.

A project that remembers only successful actions cannot learn correctly from its own evolution.

The organism should preserve meaningful failed experience.

For example:

We attempted Approach X.

It failed under Condition Y.

Evidence demonstrated Failure Z.

The reason was investigated.

Approach X was abandoned, corrected, or superseded.

Approach Q replaced it.

This allows a future human or AI to discover:

"We have already investigated this path."

Without such memory, every new AI agent may unknowingly repeat old mistakes.

---

## 0.7.37 — Negative Knowledge

Failure, falsification, rejection, and demonstrated absence can produce a valuable form of knowledge:

Negative Knowledge.

Negative Knowledge describes what is known not to work, not to exist, not to satisfy a requirement, or not to be sufficiently supported under known conditions.

Conceptually:

CLAIM / APPROACH
    ↓
TEST / EXPERIENCE
    ↓
REFUTATION / FAILURE
    ↓
CONDITIONS
    ↓
NEGATIVE KNOWLEDGE

The correct representation is not:

"X is bad."

It should preserve conditions and provenance.

For example:

"Approach X failed under conditions Y because evidence Z demonstrated the following limitation."

Negative Knowledge remains revisable if conditions or evidence change.

It is knowledge, not dogma.

---

## 0.7.38 — Repetition Avoidance Principle

### Repetition Avoidance Principle

The organism should use preserved negative knowledge and prior experience to avoid unknowingly repeating previously investigated failures, rejected paths, or disproven assumptions.

In human terms:

The organism should not repeat the same mistake merely because the current AI agent was not present when the mistake was first made.

This principle directly addresses epistemic dementia.

Prior failure should become available experience.

Prior rejection should remain explainable.

Prior falsification should remain traceable.

A future attempt may still be legitimate if conditions have changed, but it should not occur in ignorance of relevant prior experience.

---

## 0.7.39 — Automatic Capture Does Not Mean Automatic Canonization

The organism may increasingly automate:

capture;

classification;

relationship discovery;

provenance construction;

evidence association;

memory proposals;

contradiction detection.

However, automation must not silently promote every captured interpretation into Canon.

The following should not automatically become canonical truth:

- every AI conclusion;
- every assumption;
- every intermediate result;
- every temporary preference;
- every apparently successful implementation;
- every conversational interpretation;
- every generated summary;
- every inferred relationship.

The conceptual progression is:

CAPTURE
    ↓
CLASSIFY
    ↓
RELATE
    ↓
VERIFY
    ↓
SEDIMENT
    ↓
GOVERN WHERE REQUIRED

Capture can become highly automatic.

Canonical authority must remain governed.

---

## 0.7.40 — Capture Once, Reference Many Principle

### Capture Once, Reference Many Principle

An original epistemically significant artifact should, where practical, be preserved once and referenced from the multiple Claims, Transformations, Memories, or Views that depend upon it rather than unnecessarily duplicated.

Conceptually:

                 ORIGINAL EXPERIENCE
                  /       |       \
                 /        |        \
                ↓         ↓         ↓
           DECISION     MEMORY   TRANSFORMATION

The system should not create three independent copies of the same experience merely because three epistemic structures depend upon it.

One preserved experience may support many relationships.

This principle reduces unnecessary memory growth while preserving provenance.

---

## 0.7.41 — Content Identity

The organism should eventually be capable of recognizing when multiple observed artifacts represent the same underlying content.

For example, the same research document may exist:

- in a phone Download directory;
- inside the repository;
- in a backup;
- in an exported archive.

These locations do not necessarily represent four independent epistemic artifacts.

Conceptually:

CONTENT IDENTITY
    ↓
ONE KNOWN ARTIFACT
    ↓
LOCATION A
LOCATION B
LOCATION C
LOCATION D

The exact engineering mechanism is not decided at this research stage.

Possible technical mechanisms must be evaluated later.

The epistemic requirement is more important:

Multiplicity of copies must not be confused with multiplicity of independent knowledge or evidence.

---

## 0.7.42 — Evidence Independence Principle

### Evidence Independence Principle

Multiple copies or representations derived from the same underlying Source shall not be misrepresented as independent Evidence.

If five files all derive from one original artifact, the organism must not claim:

"Five independent pieces of evidence exist."

It may instead establish:

"One underlying evidentiary source is preserved through five known representations or locations."

This distinction is critical for trustworthy audit.

Evidence strength must not be artificially inflated by duplication.

---

## 0.7.43 — Automatic Capture Boundary

The research now supports an initial division of responsibility.

### The organism should automatically capture, where technically possible:

- relevant Human ↔ AI experience;
- action intention;
- executed actions;
- observed outcomes;
- significant failures;
- meaningful project changes;
- verification results;
- evidence references;
- temporal relationships;
- known causal relationships;
- before/after conditions;
- session identity;
- related Transformation identity;
- provenance;
- unresolved uncertainty;
- contradictions discovered during observation.

### The organism may automatically propose:

- what may have been learned;
- what appears epistemically important;
- what may deserve sedimentation;
- which Claims may result;
- which contradictions exist;
- which Memory may require updating;
- which part of the Living Project Image may be stale;
- which relationships appear to exist;
- which prior experiences may be relevant.

### Human authority remains necessary for matters such as:

- the human's actual intention where interpretation is uncertain;
- owner decisions;
- contested high-impact interpretations;
- canonical approvals;
- fundamental identity changes;
- governance decisions;
- destructive or materially risky decisions where authorization is required.

This separation allows strong automation without surrendering epistemic authority.

---

## 0.7.44 — The Organism Must Not Become Bureaucracy

There is a serious usability risk.

If the organism asks after every message:

"Was that a decision?"

"Should I save this?"

"Was that important?"

"Is this canonical?"

"Should this become Memory?"

then continuity preservation becomes an obstacle to actual work.

The organism should normally operate through:

WORK
    ↓
CAPTURE
    ↓
PROVISIONAL CLASSIFICATION
    ↓
CONTINUE WORKING

Human intervention should be requested primarily when there is a meaningful reason.

Examples include:

AMBIGUOUS HIGH-IMPACT DECISION

CANONICAL APPROVAL REQUIRED

CONTRADICTION REQUIRING HUMAN AUTHORITY

DESTRUCTIVE OR MATERIAL ACTION

FUNDAMENTAL IDENTITY CHANGE

UNRESOLVED INTENT WITH MATERIAL CONSEQUENCES

The continuity system must serve work rather than interrupt it continuously.

---

## 0.7.45 — Human Attention Principle

### Human Attention Principle

The organism shall conserve human attention by requesting explicit intervention primarily when human authority, unresolved ambiguity, material risk, or governance requires it.

Routine preservation and traceability should not become a continuous clerical burden upon the human.

In human terms:

The memory of the organism must work for the human.

The human must not work for the memory.

---

## 0.7.46 — Integrated Continuity Cycle

The continuity physiology developed in this research can now be represented more completely:

                         HUMAN
                           │
                         NEED
                           │
                           ▼
                    HUMAN ↔ AI WORK
                           │
              ┌────────────┴────────────┐
              │                         │
              ▼                         ▼
          EXPERIENCE                 INTENTION
              │                         │
              └────────────┬────────────┘
                           ▼
                    TRANSFORMATION
                           │
                         ACTION
                           │
                      OBSERVATION
                           │
                        OUTCOME
                           │
                       EVIDENCE
                           │
                        WITNESS
                           │
                     VERIFICATION
                           │
                        LEARNING
                           │
                     SEDIMENTATION
                           │
                         MEMORY
                           │
                       KNOWLEDGE
                           │
                           ▼
                  LIVING PROJECT IMAGE
                           │
                           ▼
                     FUTURE PURPOSE
                           │
                    PROGRESSIVE RECALL
                           │
                           ▼
                     CONTEXT PACKAGE
                           │
                           ▼
                    HUMAN + NEXT AI

This cycle can repeat across:

- conversations;
- AI agents;
- devices;
- working environments;
- repository states;
- implementation generations;
- research generations;
- long periods of project evolution.

Continuity therefore becomes a property of the project rather than a property of one working session.

---

## 0.7.47 — Central Continuity Conclusion

The continuity system must preserve the meaning of project evolution, not merely its data exhaust.

The organism must remember not only:

what happened,

but also, where evidence permits:

why it happened;

what need produced it;

what was researched;

what alternatives existed;

what was decided;

what action occurred;

what result was observed;

what evidence supports that result;

what was learned;

what changed;

what remains uncertain;

and how the current reality emerged from previous reality.

This is the difference between historical storage and epistemic continuity.

---

## 0.7.48 — Project-Owned Continuity

The project must progressively become capable of carrying the context required for its own continuation.

This context must not depend exclusively upon:

- the memory of the current human;
- the context window of the current AI;
- one ChatGPT conversation;
- one external AI provider;
- one terminal session;
- one device;
- one temporary derived representation.

The project should preserve enough identity, experience, provenance, memory, knowledge, transformation history, current state, and unresolved frontier to orient another authorized human or AI.

This establishes:

PROJECT-OWNED CONTINUITY

rather than:

AGENT-OWNED CONTINUITY.

---

## 0.7.49 — Continuity and the Epistemic Organism

Within the Epistemic Organism analogy, continuity is not a single organ.

It is an organism-wide physiological property.

Persistent Experience preserves lived experience.

Evidence preserves observable support.

Witness provides compact testimony of transformation.

Trace provides current positional continuity.

Lineage preserves genealogy.

Memory preserves what should remain recallable.

Knowledge preserves sedimented understanding.

Transformation preserves meaningful evolution.

Progressive Recall allows travel through memory according to need.

The Living Project Image exposes the best-supported present understanding.

CSL provides the future common language through which these relationships can become intelligible to humans and resolvable by machines.

Continuity emerges from their cooperation.

---

## 0.7.50 — Continuity Must Preserve Both Meaning and Proof

A continuity system that preserves only meaning risks becoming an unverified story.

A continuity system that preserves only raw evidence risks becoming incomprehensible.

Therefore the organism requires both.

HUMAN-UNDERSTANDABLE MEANING
            ↕
NAVIGABLE PROVENANCE
            ↕
ORIGINAL EXPERIENCE / EVIDENCE

The human should be able to understand the project without reading every technical artifact.

The auditor should be able to descend toward evidence.

The AI should be able to resolve identities and relationships.

All should remain connected to the same project reality.

---

## 0.7.51 — Continuity Must Preserve Unresolved Reality

Not every research episode ends with a decision.

Not every action produces a known result.

Not every contradiction is immediately resolved.

Not every question has an answer.

Therefore continuity must preserve states such as:

UNKNOWN

UNRESOLVED

DEFERRED

CONTRADICTED

PARTIALLY VERIFIED

UNDER RESEARCH

AWAITING HUMAN AUTHORITY

The organism must not manufacture closure merely to make its history appear complete.

An unresolved question is itself part of the real project state.

---

## 0.7.52 — Continuity Across Evolution and Involution

Project history does not always represent progress.

A project may:

- gain a capability;
- lose a capability;
- replace a working approach with a weaker one;
- introduce a contradiction;
- regress;
- remove an organ;
- restore an earlier state;
- abandon a research direction;
- supersede a decision.

The continuity system must therefore preserve both evolution and involution.

The Living Project Image must represent what is true now.

Lineage must preserve how that state was reached.

History must not be rewritten to imply continuous improvement when reality demonstrates otherwise.

---

## 0.7.53 — Continuity Is Not the Same as Immutability

Preserving history does not mean that every interpretation remains permanently valid.

Knowledge may be corrected.

Decisions may be superseded.

Hypotheses may be falsified.

Implementations may disappear.

Canon may evolve through governance.

The continuity requirement is:

do not silently erase how the project arrived at its current state.

A superseded decision may cease to govern the present while remaining part of project history.

A falsified hypothesis may cease to be believed while remaining part of research lineage.

A removed capability may cease to exist while its previous existence remains historically demonstrable.

This allows the organism to change without losing its biography.

---

## 0.7.54 — Historical Truth and Current Truth

The continuity system must distinguish:

CURRENT TRUTH

from:

HISTORICAL TRUTH.

For example:

CURRENT TRUTH

Capability X does not currently exist.

HISTORICAL TRUTH

Capability X existed in a previous verified project state.

Both statements may be simultaneously true.

Likewise:

CURRENT DECISION

Approach B is authoritative.

HISTORICAL DECISION

Approach A was previously accepted and later superseded.

The organism must not destroy historical truth when current truth changes.

---

## 0.7.55 — Epistemic Biography

The accumulated continuity of meaningful project transformations forms what can be understood as the epistemic biography of the organism.

This biography includes:

- origin;
- needs;
- discoveries;
- decisions;
- mistakes;
- failures;
- corrections;
- successful transformations;
- rejected directions;
- acquired capabilities;
- lost capabilities;
- changing understanding;
- canonical evolution;
- unresolved questions;
- current condition.

The biography is not a decorative history.

It provides explanatory context for present reality.

A mature project should increasingly be capable of answering:

Who am I?

Why do I exist?

What have I experienced?

What have I learned?

What did I try that failed?

Why am I structured this way?

What changed me?

What do I currently know?

What do I not know?

What am I currently becoming?

---

## 0.7.56 — Continuity Research Outcome

The current research supports the following working conclusion:

Epistemic continuity is the project-owned capability to preserve and navigate the meaningful, evidence-connected evolution of project reality across time, sessions, tools, devices, humans, and AI agents without requiring any single external agent to remember the complete history.

Its purpose is not infinite accumulation.

Its purpose is persistent intelligibility.

The project should be capable of carrying forward enough of its identity, experience, decisions, evidence, memory, knowledge, lineage, and current frontier that work can continue without epistemic amnesia.

This continuity is a prerequisite for the future Living Project Image.

The Living Project Image, in turn, must represent the best-supported current reality produced by this continuous history.

---

## 0.7.57 — Research Principles Established or Strengthened in Section 0.7

The following principles are established or strengthened as research conclusions within this section:

### Capture Before Interpretation Principle

Preserve epistemically significant original Experience before, or independently of, later interpretation and condensation.

### Semantic Continuity Principle

Preserve meaningful causal and epistemic relationships, not chronology alone.

### Session-Independent Continuity Principle

A Transformation must remain intelligible independently of the AI session in which it occurred.

### Human Preservation Burden Principle

The human should not manually reconstruct history that the organism could have captured during work.

### Authority Scope Principle

Human authorization must not be interpreted beyond the scope demonstrably supported by context.

### Intention–Outcome Separation Principle

Successful execution does not by itself demonstrate achievement of intended reality.

### Repetition Avoidance Principle

Relevant prior failures, rejected paths, and disproven assumptions should remain available to prevent accidental repetition.

### Capture Once, Reference Many Principle

Preserve an original epistemic artifact once where practical and reference it from the structures that depend upon it.

### Evidence Independence Principle

Multiple copies derived from one source must not be represented as independent evidence.

### Human Attention Principle

Routine continuity preservation should minimize unnecessary human interruption and clerical burden.

These principles remain part of the current research model until formally reconciled and promoted through the appropriate governance process.

---

## 0.7.58 — Boundary Toward the Living Project Image

Section 0.7 establishes how meaningful project evolution can remain continuous.

The next problem is different.

If the organism possesses:

- Experience;
- Transformations;
- Evidence;
- Witnesses;
- Trace;
- Lineage;
- Memory;
- Knowledge;
- Provenance;

how does it represent:

WHAT IS TRUE ABOUT THE PROJECT NOW?

That representation must not merely repeat history.

It must synthesize the best-supported present condition while preserving navigable paths toward history and evidence.

It must distinguish:

what should exist;

what can be demonstrated to exist;

what is absent;

what is unknown;

what is contradictory;

what is stale;

what is under research;

what changed;

and what remains unresolved.

This leads directly to:

# 0.8 — Living Project Image Physiology

Status: CANON

Classification: Living Project Image and CSL Research

Purpose: Define the physiological role, epistemic boundaries, human comprehension requirements, and continuity behavior of the Living Project Image before defining the cognitive grammar and technical syntax of CSL.

This section begins from the continuity model established in Section 0.7.

The project may preserve:

- Experience;
- Sessions;
- Transformations;
- Evidence;
- Witnesses;
- Trace;
- Lineage;
- Memory;
- Knowledge;
- Provenance;
- decisions;
- uncertainty;
- contradictions;
- historical states.

However, possession of these structures does not automatically provide a human or AI with an intelligible understanding of the project as it exists now.

A project can possess a perfect archive and still be difficult to understand.

A project can preserve every conversation and still lose the meaning of its current state.

A project can contain correct Canon and correct implementation while requiring days of investigation to determine how they relate.

Therefore continuity requires a present-facing epistemic representation.

That representation is the Living Project Image.

---

## 0.8.1 — The Missing Layer Between Memory and Current Understanding

The continuity physiology developed so far can be represented as:

EXPERIENCE
    ↓
PROVENANCE
    ↓
TRANSFORMATIONS
    ↓
LAYERED MEMORY
    ↓
KNOWLEDGE
    ↓
        ?
    ↓
CURRENT PROJECT UNDERSTANDING

The missing layer cannot simply be another summary.

A summary may:

- omit important contradictions;
- silently resolve uncertainty;
- become stale;
- lose provenance;
- reflect one AI agent's interpretation;
- hide differences between intended and observed reality.

The missing layer must instead preserve an explicit relationship between current understanding and the reality that supports it.

This leads to:

LIVING PROJECT IMAGE

The Living Project Image is not merely a document.

It is the continuously maintainable epistemic representation of the project as it can currently be demonstrated to exist.

---

## 0.8.2 — Working Definition of the Living Project Image

### Living Project Image

The Living Project Image is the continuously maintainable, human-understandable, machine-resolvable representation of the best-supported current reality of a project, preserving explicit paths toward its Canon, implementation, history, memory, Transformations, uncertainty, contradictions, and Evidence.

In simpler human language:

The Living Project Image is the project's best-supported picture of itself now.

It must answer:

What is this project?

Why does it exist?

What should exist?

What actually exists?

What can it currently do?

What can it not yet do?

What has changed?

What is uncertain?

What is contradictory?

What is missing?

What is currently being researched?

How did the project reach this state?

Where is the evidence?

How can I inspect the deeper history?

---

## 0.8.3 — The Living Project Image Is Not a Conventional Project Summary

A conventional project summary may say:

"AI-Toolkit is an engineering platform for building and maintaining software projects."

That may be useful.

It is not sufficient.

The Living Project Image must represent the project at a much deeper epistemic level.

For example, it should eventually be capable of exposing:

IDENTITY

What organism is this?

PURPOSE

Why does it exist?

CANON

What is authorized or required to be true?

ANATOMY

What organs, tissues, systems, and artifacts constitute the organism?

PHYSIOLOGY

What can the organism actually do?

CURRENT CONDITION

What condition is each meaningful part currently in?

MEMORY

What has the organism retained?

KNOWLEDGE

What does it currently know?

TRANSFORMATIONS

How did the current reality emerge?

UNCERTAINTY

What cannot currently be established?

CONTRADICTIONS

Where do claims, evidence, Canon, or observed reality disagree?

GAPS

What should exist but cannot currently be demonstrated?

PROVENANCE

How can each important statement be verified?

The Living Project Image therefore provides orientation rather than merely description.

---

## 0.8.4 — The Project Reality Triangle

The research originally expressed an important intuition as:

CODE + CANON = PROJECT IMAGE

This remains valuable but requires refinement.

Code alone is not the complete realized project.

A real project may include:

- source code;
- configuration;
- data structures;
- documentation;
- deployment state;
- runtime behavior;
- repository state;
- integrations;
- external dependencies;
- generated artifacts;
- operational capabilities;
- preserved knowledge;
- research;
- evidence.

Likewise, Canon does not describe everything that can currently be observed.

A more complete conceptual relationship is:

                PROJECT REALITY
                     │
       ┌─────────────┼─────────────┐
       │             │             │
       ▼             ▼             ▼
     CANON       REALIZATION    EXPERIENCE
       │             │             │
       └─────────────┼─────────────┘
                     │
                  EVIDENCE
                     │
                     ▼
             LIVING PROJECT IMAGE

CANON describes authorized expectations and governing truth.

REALIZATION describes what has actually been built or instantiated.

EXPERIENCE explains how the project reached the current condition.

EVIDENCE establishes what can actually be supported.

The Living Project Image brings these dimensions into one intelligible present-facing representation.

---

## 0.8.5 — Expected Reality and Observed Reality

One of the most important functions of the Living Project Image is to distinguish:

WHAT SHOULD EXIST

from:

WHAT CAN BE DEMONSTRATED TO EXIST.

Conceptually:

CANON
    │
    ▼
EXPECTED REALITY

and:

OBSERVATION
    │
    ▼
EVIDENCE
    │
    ▼
OBSERVED REALITY

These two realities must then be compared.

EXPECTED REALITY
        ↕
OBSERVED REALITY

This comparison exposes conformity and divergence.

The organism must never assume that something exists merely because Canon says that it should exist.

Likewise, the existence of something in implementation does not automatically establish that it is canonically authorized.

---

## 0.8.6 — Example: Requirement Versus Demonstrated Reality

Suppose the project establishes the requirement:

"The organism must preserve its own experience."

The Living Project Image should not merely repeat that statement.

It should be capable of representing something conceptually equivalent to:

REQUIREMENT

Preserve project experience.

EXPECTED REALITY

The organism preserves relevant lived project experience across working sessions.

OBSERVED REALITY

Partial preservation currently exists.

EPISTEMIC CONDITION

PARTIALLY SUPPORTED

KNOWN GAP

Automatic Human ↔ AI conversation preservation has not yet been demonstrated.

HISTORY

The requirement emerged from the need to prevent project context loss across AI sessions.

EVIDENCE

Resolvable references toward the existing preservation mechanisms and research artifacts.

The human can therefore understand immediately:

what we want;

what exists;

what does not exist;

what we know;

and why we believe it.

---

## 0.8.7 — EXIST Applied to the Living Project Image

The Theory of Canonical Existence becomes central here.

The Living Project Image must not confuse:

EXPECTED

with:

EXISTING.

An entity may be required by Canon and still fail the test of demonstrated existence.

An entity may also exist operationally without being represented correctly in Canon.

Therefore the Living Project Image must eventually support epistemic conditions such as:

DEMONSTRATED TO EXIST

EXPECTED BUT NOT DEMONSTRATED

PREVIOUSLY DEMONSTRATED, CURRENTLY ABSENT

EXISTENCE UNKNOWN

EXISTENCE CONTRADICTED

PARTIALLY DEMONSTRATED

UNDER INVESTIGATION

The exact future vocabulary remains to be designed.

The research requirement is already clear:

existence must be demonstrated rather than assumed.

---

## 0.8.8 — Absence Is Part of the Image

A truthful image of the project must represent not only presence but absence.

For example:

EXPECTED

Automatic conversation preservation.

OBSERVED

No sufficient evidence currently demonstrates automatic preservation.

RESULT

EXPECTED BUT NOT DEMONSTRATED.

This negative condition is part of project reality.

The Living Project Image must therefore expose:

what exists;

what does not exist;

what may exist but has not been verified;

what previously existed;

what has disappeared;

what cannot currently be established.

An image that contains only positive existence claims is incomplete.

---

## 0.8.9 — Unknown Is Not Absent

The organism must also distinguish:

ABSENT

from:

UNKNOWN.

Suppose the organism has not inspected a subsystem after a major change.

It would be epistemically incorrect to state:

"The capability does not exist."

The correct state may be:

"Current existence has not been established after the recent Transformation."

Likewise, the organism must not state:

"The capability exists."

unless evidence supports that conclusion.

This distinction is essential.

ABSENT means sufficient evidence supports absence under the applicable existence criteria.

UNKNOWN means the available evidence is insufficient to establish either existence or absence.

The Living Project Image must preserve this boundary.

---

## 0.8.10 — Contradiction Is Part of Current Reality

The Living Project Image must not silently eliminate contradictions.

Suppose:

CANON says X.

A current implementation artifact indicates Y.

An older document says Z.

Runtime evidence indicates X only partially functions.

The organism must not simply choose one statement and hide the disagreement.

The image should expose:

CONTRADICTION DETECTED

and provide navigable relationships toward the conflicting sources.

A contradiction is itself a fact about the current epistemic condition of the project.

The contradiction may later be resolved.

Until then, the Living Project Image must preserve it.

---

## 0.8.11 — Staleness Is an Epistemic Condition

Information can once have been correct and later become stale.

For example:

A capability was verified as operational.

A later Transformation modifies the relevant organ.

The previous verification may no longer be sufficient to establish the current state.

The Living Project Image must therefore be capable of representing:

PREVIOUSLY VERIFIED

but:

CURRENT VERIFICATION STALE.

This avoids a dangerous failure mode:

historically true information being presented as currently verified truth.

The project must know not only what was verified, but whether that verification remains applicable to current reality.

---

## 0.8.12 — Living Does Not Mean Constantly Rewritten Without Control

The word "Living" must not imply uncontrolled automatic rewriting.

The image is living because it can evolve as project reality evolves.

But epistemic authority must remain governed.

Suppose Canon states:

CAPABILITY X MUST EXIST.

Observation later demonstrates:

CAPABILITY X CANNOT CURRENTLY BE FOUND.

The organism must not solve the contradiction by silently changing Canon to:

CAPABILITY X DOES NOT NEED TO EXIST.

Instead:

CANON

X must exist.

OBSERVED REALITY

X cannot currently be demonstrated.

CURRENT CONDITION

NON-CONFORMING / UNKNOWN,
depending upon available evidence.

ACTION

Investigation, correction, or governance may be required.

The Living Project Image reflects divergence.

It does not erase divergence.

---

## 0.8.13 — Canon and Living Project Image Have Different Physiological Roles

A fundamental distinction emerges.

### Canon

Canon defines what is authorized, required, constrained, or normatively true within the governed project.

### Living Project Image

The Living Project Image represents what the project can currently demonstrate about its actual present reality.

The relationship is:

CANON
    │
    │ expected
    ▼
REALITY COMPARISON
    ▲
    │ observed
    │
LIVING PROJECT IMAGE

The comparison between them produces conformity information.

Therefore:

Canon is not the Living Project Image.

The Living Project Image is not Canon.

Neither should replace the other.

---

## 0.8.14 — The Living Project Image Is Not a New Competing Canon

This distinction must be protected strongly.

If the Living Project Image becomes an independently maintained second source of truth, the project will eventually develop epistemic divergence.

For example:

CANON A

and:

LIVING IMAGE B

could silently evolve into incompatible realities.

The Living Project Image must therefore remain evidence-connected and derivable from authoritative project reality.

It should not become a manually maintained parallel architecture.

Where human interpretation is necessary, provenance and authority must remain explicit.

---

## 0.8.15 — One Reality, Multiple Representations

Different consumers require different representations.

A human project owner may require:

plain language;

semantic titles;

visual grouping;

explanations;

navigation.

An engineer may require:

implementation detail;

file locations;

technical relationships;

execution evidence.

An auditor may require:

claims;

sources;

provenance;

verification;

contradictions.

An AI may require:

compact identifiers;

structured relations;

machine-resolvable states;

minimal context.

These views should not become separate truths.

Conceptually:

                    PROJECT REALITY
                          │
            ┌─────────────┼─────────────┐
            ▼             ▼             ▼
          HUMAN         AUDITOR       ENGINEER
           VIEW           VIEW          VIEW
              \             │             /
               \            │            /
                └───────────┼───────────┘
                            ▼
                       AI DERIVED VIEW

All representations must remain connected to the same underlying project reality.

---

## 0.8.16 — Single Reality, Multiple Views Principle

### Single Reality, Multiple Views Principle

AI-Toolkit shall maintain one epistemic project reality from which human, audit, engineering, and AI-optimized representations may be derived.

No derived representation shall become an independent competing source of project truth.

In human language:

One project.

One reality being tracked.

Multiple ways to see it.

This principle is especially important for future compact AI representations.

The AI may receive a highly compressed derived representation.

That representation must remain traceable to the same reality visible to the human.

---

## 0.8.17 — The Living Project Image Is a Cognitive Map

The Living Project Image should not become a giant storage container.

It should function as a cognitive map.

A map does not contain every physical object in the territory.

It allows the traveler to understand:

where they are;

what surrounds them;

what important structures exist;

how those structures relate;

where uncertainty or danger exists;

how to travel toward deeper detail.

Likewise, the Living Project Image should expose the meaningful structure of project reality and provide paths toward deeper information.

Conceptually:

LIVING PROJECT IMAGE
        │
        ├── current meaning
        ├── identities
        ├── relationships
        ├── epistemic conditions
        ├── contradictions
        ├── uncertainty
        └── navigable references
                │
                ▼
          PROJECT MEMORY
                │
                ▼
       ORIGINAL EXPERIENCE
                │
                ▼
             EVIDENCE

This allows high-level comprehension without destroying depth.

---

## 0.8.18 — CSL as the Expression of the Living Project Image

The research direction now connects directly to CSL.

CSL is not merely intended to describe isolated specifications.

Its deeper role is emerging as the common epistemic language through which project reality can become:

human-readable;

machine-resolvable;

traceable;

navigable;

auditable;

deterministic;

and continuity-preserving.

The Living Project Image may therefore be expressed through CSL.

This does not yet define the final syntax of CSL.

It defines the role CSL must eventually satisfy.

Conceptually:

PROJECT REALITY
        ↓
EPISTEMIC INTERPRETATION
        ↓
LIVING PROJECT IMAGE
        ↓
EXPRESSED THROUGH CSL
        ↓
┌─────────────┬──────────────┬─────────────┐
│             │              │             │
HUMAN      ENGINEER       AUDITOR          AI
VIEW          VIEW           VIEW        COMPACT VIEW

CSL becomes the common semantic bridge between these views.

---

## 0.8.19 — CSL Is Not Merely a Serialization Format

If CSL were only another way to serialize structured information, the project could simply use JSON, YAML, XML, or another existing format.

The research objective is different.

CSL must communicate epistemic meaning.

It must allow the reader to recognize concepts such as:

Need;

Research;

Decision;

Transformation;

Evidence;

Memory;

Knowledge;

Unknown;

Contradiction;

Current State;

Canon;

and the relationships between them.

Therefore CSL requires more than technical syntax.

It requires a cognitive grammar.

Before designing punctuation, delimiters, parsers, schemas, or file extensions, the research must determine:

What kinds of things exist in the CSL cognitive world?

How does a human recognize them?

How are they related?

How is authority communicated?

How is uncertainty communicated?

How is provenance communicated?

How does the human travel from meaning toward proof?

These questions belong to the research frontier that follows Section 0.8.

---

## 0.8.20 — CSL Must Preserve Human Comprehension

The project exists to help humans develop and maintain their projects with AI support.

Therefore the human cannot become a secondary consumer of the project's own knowledge.

A technically perfect machine representation that requires specialized software-engineering knowledge merely to understand project history would fail an important objective.

Human-facing CSL must allow a non-specialist project owner to understand concepts such as:

"What happened?"

"Why?"

"What did we decide?"

"What exists now?"

"What failed?"

"What remains unknown?"

"What should happen next?"

without first learning the internal implementation mechanisms of AI-Toolkit.

Technical precision remains necessary.

But technical precision must not require unnecessary technical opacity.

---

## 0.8.21 — Human Meaning Before Technical Mechanism

Consider the technical statement:

"Terminal Capture persists stdout."

An engineer may understand it immediately.

A non-specialist human may not.

The human-facing meaning is closer to:

"The organism preserves what the execution environment reported after an action."

The deeper technical layer may then explain:

- terminal capture;
- standard output;
- storage mechanism;
- file path;
- encoding;
- process identifiers.

This creates levels of explanation.

HUMAN MEANING
    ↓
ENGINEERING EXPLANATION
    ↓
TECHNICAL MECHANISM
    ↓
RAW EVIDENCE

The human should be able to stop at the level sufficient for the task.

The engineer or auditor should be able to continue deeper.

---

## 0.8.22 — Human Comprehension Principle

### Human Comprehension Principle

Human-facing epistemic representations shall communicate project meaning in language understandable without unnecessary dependence on internal software terminology.

Technical terminology may remain available at deeper engineering and audit levels where precision requires it.

This does not mean technical concepts must be hidden.

It means the project should explain what those concepts mean for the organism.

For example:

TECHNICAL TERM

Event Bus

HUMAN / ORGANISM MEANING

The circulation pathway through which events travel between organs.

The technical identity remains available.

The human obtains a mental model.

---

## 0.8.23 — The Epistemic Organism as a Human Cognitive Bridge

The Epistemic Organism analogy provides a valuable bridge between complex software architecture and human understanding.

For example:

Canon can be understood as DNA.

Knowledge Engine can be understood as Brain.

Reasoning Engine can be understood as Prefrontal Cortex.

Knowledge Repository can be understood as Memory.

Repository Scanner can be understood as Eyes.

Input Connectors can be understood as Ears or senses.

CSL can be understood as Language.

Traceability Network can be understood as Nervous System.

Governance Engine can be understood as Heart or governance-maintaining physiology.

Validation Engine can be understood as Immune System.

Audit Engine can be understood as Adaptive Immune System.

Canonical Models can be understood as Skeleton.

Execution Engine can be understood as Muscles.

Merge Engine can be understood as Hands.

Executive Briefing Engine can be understood as Mouth.

API Layer can be understood as Skin or external interface.

Event Bus can be understood as Blood Flow.

Workflow Engine can be understood as Metabolism.

Canonical Artifacts can be understood as Cells.

Modules can be understood as Tissues.

Engines can be understood as Organs.

Capability Domains can be understood as Organ Systems.

The analogy does not change the fact that AI-Toolkit is implemented as software.

Its purpose is to provide a coherent human mental model of what the software does.

---

## 0.8.24 — Anatomical Language Must Preserve Technical Resolvability

The organism analogy must not destroy engineering precision.

A human may see:

MEMORY

while an engineer or AI must still be capable of resolving:

which repository structure;

which engine;

which artifact;

which interface;

which implementation;

which evidence.

Therefore human anatomical meaning and technical identity should remain connected.

Conceptually:

HUMAN MEANING

Memory

        ↕ resolvable relationship

EPISTEMIC ORGAN

Knowledge Repository

        ↕ resolvable relationship

TECHNICAL REALIZATION

specific implementation artifacts

The human mental model and the engineering reality must not become disconnected vocabularies.

---

## 0.8.25 — The Living Project Image Should Explain the Organism to a Newcomer

A newcomer should not need to inspect hundreds or thousands of project files merely to understand what AI-Toolkit is.

The Living Project Image should eventually provide an entry point similar to:

AI-TOOLKIT

Identity:
Epistemic Engineering Organism.

Purpose:
Help a human develop, understand, validate, maintain, and evolve projects with AI assistance while preserving project-owned continuity and canonical authority.

Current Condition:
[demonstrated state]

Major Organ Systems:
[human-readable anatomy]

Current Capabilities:
[demonstrated capabilities]

Developing Capabilities:
[partially established capabilities]

Known Gaps:
[expected but missing or unverified capabilities]

Current Research:
[active research frontier]

Recent Evolution:
[meaningful recent Transformations]

Uncertainty:
[current unknowns]

Contradictions:
[current unresolved contradictions]

Evidence:
[navigable provenance]

From this orientation, the newcomer can travel deeper only where needed.

---

## 0.8.26 — Human-Readable Identity Is Essential to the Living Image

The Living Project Image may eventually contain hundreds or thousands of epistemic entities.

Opaque identifiers alone would make the image unusable for humans.

Therefore the previously established Human-Readable Identity Principle becomes mandatory for human-facing Living Project Image representations.

Instead of:

TR-0042

the human should see:

TR-0042 — Establish Layered Memory

Instead of:

NEED-0031

the human should see:

NEED-0031 — Prevent Context Loss

Instead of:

EV-0103

the human should see:

EV-0103 — Terminal Capture Proof

Instead of:

MEM-0021

the human should see:

MEM-0021 — Execution Context Knowledge

The identifier answers:

"Which exact entity is this?"

The title answers:

"What does it mean?"

Both are necessary.

---

## 0.8.27 — Human-Readable Identity Principle

### Human-Readable Identity Principle

Every epistemically significant entity shall possess both a stable machine-addressable identifier and a concise human-readable semantic title.

Human-facing representations shall present both together.

An identifier establishes identity.

A title communicates meaning.

A human shall not be required to resolve opaque identifiers across repository artifacts merely to understand the project's history, state, decisions, Evidence, or evolution.

This principle applies broadly to entities such as:

Needs;

Research episodes;

Decisions;

Transformations;

Actions;

Evidence;

Witnesses;

Memory;

Knowledge;

States;

Contradictions;

Gaps;

and other epistemically significant structures.

---

## 0.8.28 — No Naked Identifier Principle

### No Naked Identifier Principle

In any representation intended for human comprehension, an epistemic identifier shall not be presented alone when its semantic title is known.

Therefore:

TR-0042

is insufficient when:

TR-0042 — Establish Layered Memory

is available.

Machine-optimized derived representations may use compact identifiers where appropriate.

The restriction applies to human-facing representations.

This allows AI-optimized views to remain compact without imposing machine-oriented cognitive burdens upon humans.

---

## 0.8.29 — Human and AI Representations Can Differ in Density

The human may require:

TR-0042 — Establish Layered Memory

with explanatory context.

An AI working on a tightly bounded task may require only:

TR-0042

plus machine-resolvable relationships.

This is acceptable if both resolve to the same underlying epistemic entity.

Conceptually:

                    SAME ENTITY
                        │
              ┌─────────┴─────────┐
              ▼                   ▼
          HUMAN VIEW            AI VIEW

TR-0042 — Establish       TR-0042
Layered Memory

Human representation optimizes comprehension.

AI representation may optimize context efficiency.

Neither creates a new truth.

---
## 0.8.30 — Navigability as a Fundamental Human Requirement

Reading the Living Project Image should not be a dead-end experience.

When the human encounters an important statement, the human should be able to ask:

What does this mean?

Why does this exist?

Who or what established it?

What Transformation produced it?

What Evidence supports it?

What did the Canon require?

What existed before?

What exists now?

What original experience led to this conclusion?

What contradictions exist?

What changed afterward?

The Living Project Image must therefore support epistemic travel.

---

## 0.8.31 — Navigable Provenance

Consider:

TR-0042 — Establish Layered Memory

A human-facing representation should eventually permit navigation conceptually similar to:

TR-0042 — Establish Layered Memory
    │
    ├── Why did this Transformation exist?
    │       ↓
    │   NEED-0031 — Prevent Context Loss
    │
    ├── What research produced it?
    │       ↓
    │   relevant research episode
    │
    ├── What was decided?
    │       ↓
    │   relevant Decision
    │
    ├── What happened?
    │       ↓
    │   Experience / Action
    │
    ├── What proves it?
    │       ↓
    │   Evidence
    │
    ├── What did the organism learn?
    │       ↓
    │   Memory / Knowledge
    │
    └── What is true now?
            ↓
        Current State

This is not merely hyperlink convenience.

It is an epistemic audit capability.

---

## 0.8.32 — Superior Audit Through Navigability

A human auditor should not be forced to trust a CSL statement because it looks authoritative.

The auditor should be able to travel from:

CLAIM

toward:

SOURCE

EVIDENCE

TRANSFORMATION

ORIGINAL EXPERIENCE

CANONICAL AUTHORITY

where applicable.

The stronger the claim, the more important the ability to inspect its provenance.

CSL should therefore eventually support navigable references toward the artifacts that justify its assertions.

This allows a human to move from:

"What does the project say?"

to:

"Why should I believe it?"

and then to:

"Show me the underlying evidence."

---

## 0.8.33 — CSL as Map Rather Than Warehouse

This produces an important architectural conclusion.

CSL should not attempt to physically contain every piece of raw project information.

If CSL copied:

every conversation;

every terminal output;

every implementation file;

every test result;

every audit;

every historical state;

then the Living Project Image would become enormous and cognitively unusable.

Instead:

CSL / LIVING PROJECT IMAGE
        │
        ├── meaning
        ├── identity
        ├── relationship
        ├── current epistemic condition
        ├── authority
        └── resolvable references
                │
                ▼
        DEEPER PROJECT MEMORY
                │
                ▼
        ORIGINAL EXPERIENCE
                │
                ▼
             EVIDENCE

CSL becomes the meaningful navigable map of reality.

It does not need to duplicate the entire territory.

---

## 0.8.34 — Navigable Reality Principle

### Navigable Reality Principle

A human-facing epistemic representation should permit travel from high-level meaning toward the deeper authoritative artifacts, history, Experience, and Evidence required to understand or verify that meaning.

The human should not be required to know repository geography in advance.

The project should provide the path.

This principle transforms provenance from a backend property into a usable human capability.

---

## 0.8.35 — The Living Project Image Must Remain Cognitively Manageable

As AI-Toolkit evolves, it may accumulate enormous amounts of information.

The Living Project Image cannot present all of that information simultaneously.

The human brain requires orientation, grouping, hierarchy, and progressive detail.

Therefore the Living Project Image must cooperate with Layered Epistemic Memory and Progressive Recall.

Conceptually:

ORIENTATION
    ↓
CURRENT PROJECT IMAGE
    ↓
RELEVANT DOMAIN
    ↓
RELEVANT ORGAN
    ↓
RELEVANT TRANSFORMATION
    ↓
RELEVANT MEMORY
    ↓
ORIGINAL EXPERIENCE
    ↓
RAW EVIDENCE

The human travels deeper only when necessary.

This resembles human memory:

we do not consciously load our complete biography into working thought every time we make a decision.

We recall what is relevant.

---

## 0.8.36 — Living Image as the Entrance to Layered Memory

The Living Project Image may therefore become the principal entrance into the organism's memory.

Instead of asking:

"Which file contains the thing I need?"

the human may begin with:

"What do I want to understand?"

For example:

Why does layered memory exist?

The organism can travel:

CURRENT IMAGE
    ↓
MEMORY SYSTEM
    ↓
LAYERED MEMORY
    ↓
TRANSFORMATION
    ↓
RESEARCH
    ↓
ORIGINAL EXPERIENCE

Or:

Does automatic conversation capture exist?

The organism can travel:

CURRENT IMAGE
    ↓
CONTINUITY PHYSIOLOGY
    ↓
CAPABILITY
    ↓
CURRENT CONDITION
    ↓
EVIDENCE
    ↓
KNOWN GAP

The project becomes navigable by meaning rather than only by filesystem location.

---

## 0.8.37 — The Living Project Image as the Epic Thread

The original research described CSL as the project's "epic thread."

This idea can now be expressed more rigorously.

The epic thread is not a giant chronological transcript.

It is continuity of meaning.

Conceptually:

IDENTITY
    ↓
PURPOSE
    ↓
NEEDS
    ↓
RESEARCH
    ↓
DECISIONS
    ↓
TRANSFORMATIONS
    ↓
CURRENT REALITY
    ↓
FUTURE DIRECTION

Every meaningful point can remain connected downward toward history and Evidence.

The thread should therefore prevent the project from silently:

wandering;

duplicating previous work;

forgetting decisions;

repeating disproven approaches;

confusing old truth with current truth;

confusing intention with reality;

confusing assertion with Evidence;

losing why something exists;

losing what the human wanted.

This is the deeper meaning of CSL as the project's epic thread.

---

## 0.8.38 — A Living Image Can Represent Evolution and Involution

The Living Project Image must not assume that every project change represents improvement.

Suppose:

STATE 1

Capability X works.

TRANSFORMATION

A major restructuring occurs.

STATE 2

Capability X no longer works.

The image must change accordingly.

It must not preserve:

Capability X — Operational

merely because that was previously true.

The image should represent current reality:

Capability X — Previously demonstrated, currently not demonstrated or currently failed.

The historical state remains available through Lineage.

Thus the image can represent:

evolution;

regression;

loss;

recovery;

replacement;

abandonment;

restoration.

"Living" means responsive to reality, not optimistic.

---

## 0.8.39 — The Image Must Detect Divergence

A critical future physiological capability follows.

The organism should compare expected reality with observed reality.

Conceptually:

EXPECTED REALITY
        │
        ├─────────────────┐
        │                 │
        ▼                 ▼
      CANON          OBSERVED REALITY
                          │
                          ▼
                       COMPARE
                          │
                ┌─────────┴─────────┐
                ▼                   ▼
              MATCH             DIVERGENCE

Possible divergence may include:

required capability missing;

unauthorized capability present;

implementation contradicting Canon;

documentation contradicting implementation;

stale verification;

runtime contradicting repository assumptions;

two canonical statements conflicting;

current state differing from remembered state.

The exact future detection mechanisms remain an implementation research problem.

The epistemic requirement is already established.

## 0.8.40 — Divergence Must Not Be Silently Repaired in the Image

When divergence is detected, the organism must not simply edit the representation until the contradiction disappears.

For example:

CANON

X must exist.

OBSERVED REALITY

X does not currently appear to exist.

Incorrect response:

Rewrite the image as though X exists.

Also incorrect:

Rewrite Canon automatically so that X no longer needs to exist.

Correct epistemic response:

Expose the divergence.

The project may then require:

investigation;

implementation repair;

verification;

governance;

or Canon evolution.

The image reports reality.

It does not manufacture harmony.

---

## 0.8.41 — Living Project Image Integrity Principle

### Living Project Image Integrity Principle

The Living Project Image shall represent the best-supported current project reality and shall expose uncertainty, contradiction, absence, staleness, regression, and divergence rather than silently filling those conditions with assumptions.

This is one of the strongest applications of Reality First and EXIST within the continuity model.

A truthful incomplete image is superior to a complete fictional image.

---

## 0.8.42 — Temporal Depth

Although the Living Project Image is present-facing, it must remain connected to temporal depth.

A human may ask:

"What did the project look like before this Transformation?"

"Did this capability exist six months ago?"

"When did this contradiction appear?"

"Why did this organ change?"

"Which decision produced the current architecture?"

Lineage and Transformation history should allow the organism to reconstruct or navigate toward historical project states.

Conceptually:

LIVING IMAGE — NOW
        ↑
TRANSFORMATION
        ↑
PROJECT STATE — T-1
        ↑
TRANSFORMATION
        ↑
PROJECT STATE — T-2
        ↑
TRANSFORMATION
        ↑
PROJECT STATE — T-3

The current image therefore sits at the living frontier of an epistemic biography.

---

## 0.8.43 — Historical Reconstruction Without Full Historical Duplication

Temporal depth does not require preserving a complete duplicate Living Project Image after every minor event.

Historical understanding may be reconstructed from:

known state;

Transformations;

Lineage;

preserved artifacts;

version history;

Evidence;

historical Memory.

The exact reconstruction mechanism is not yet defined.

The research principle is:

preserve enough lineage and evidence to reconstruct meaningful historical truth without unnecessary full duplication.

This continues the memory-efficiency principles established earlier.

---

## 0.8.44 — The Living Image Must Be Able to Say "I Do Not Know"

One of the most important properties of an epistemically healthy organism is the ability to expose ignorance.

A project image that always appears complete encourages false confidence.

The Living Project Image must be able to represent statements such as:

"Current condition unknown."

"Not verified after the latest Transformation."

"Evidence insufficient."

"Two sources disagree."

"Owner intention unresolved."

"Existence not demonstrated."

"Historical information incomplete."

"Current implementation status under investigation."

These are not failures of the Living Project Image.

They are evidence of epistemic honesty.

---

## 0.8.45 — Epistemic Fog

A useful research metaphor is Epistemic Fog.

Some areas of the project may be well established:

HIGH CONFIDENCE
CLEAR PROVENANCE
CURRENT VERIFICATION

Other areas may contain:

STALE KNOWLEDGE

UNKNOWN STATE

CONTRADICTORY EVIDENCE

UNVERIFIED EXISTENCE

INCOMPLETE HISTORY

Rather than hiding this difference, the Living Project Image should eventually make it visible.

The human should be able to recognize:

where the organism sees clearly;

where the organism has partial visibility;

where the organism does not currently know.

This may become an important part of future CSL visual semantics.

---

## 0.8.46 — Transition Toward Human-Facing CSL

At this point, the Living Project Image has a physiological role:

represent the best-supported current project reality;

connect present meaning to historical continuity;

compare expected and observed reality;

expose uncertainty and contradiction;

provide navigable provenance;

support multiple derived views;

preserve human comprehension.

The next problem is representational.

How should a human actually read this image?

If the image contains:

Needs;

Decisions;

Transformations;

Evidence;

Memory;

Knowledge;

Contradictions;

Unknowns;

Canonical statements;

Organs;

States;

Relationships;

then a newcomer requires a way to recognize what each of these means.

This leads to the human learning problem of CSL.

The language must not merely be parseable.

It must become cognitively learnable. 

## 0.8.47 — CSL Must Teach the Human How to Read It

A new requirement emerged directly from the human comprehension objective.

A person encountering a CSL document for the first time should not be required to study a separate technical manual before beginning to understand the document.

The document should help teach its own reading conventions.

This does not mean that every CSL document must reproduce the entire CSL specification.

It means that a human-facing CSL representation should provide enough immediate guidance for an unfamiliar person to understand the fundamental semantic categories used in that representation.

The objective is:

OPEN CSL
    ↓
SEE READING GUIDE
    ↓
UNDERSTAND BASIC SEMANTIC CATEGORIES
    ↓
BEGIN READING PROJECT REALITY
    ↓
REPEATED EXPOSURE
    ↓
INCREASING FAMILIARITY
    ↓
NATURAL CSL LITERACY

CSL should become easier to read through use.

---

## 0.8.48 — CSL Self-Teaching Legend

A human-facing CSL document should be capable of presenting a standardized reading legend.

The legend does not primarily describe the specific project.

It describes the language through which the project is being represented.

Conceptually:

CSL — READING GUIDE

NEED

A Need describes something required by the human, project, or organism.

RESEARCH

Research represents structured investigation intended to improve understanding.

DECISION

A Decision records an accepted choice within a defined authority scope.

TRANSFORMATION

A Transformation describes a meaningful change from one project reality to another.

ACTION

An Action records something that was actually done.

EXPERIENCE

Experience preserves what occurred while the project was being worked on.

EVIDENCE

Evidence provides observable support for a Claim, state, event, or conclusion.

WITNESS

A Witness provides a compact verification that a meaningful event or Transformation occurred.

MEMORY

Memory preserves something the organism must remain capable of recalling.

KNOWLEDGE

Knowledge represents sedimented understanding supported at the applicable epistemic level.

UNKNOWN

Unknown indicates that the organism cannot currently establish the truth of the relevant matter.

CONTRADICTION

Contradiction indicates that two or more relevant representations, Claims, expectations, or pieces of Evidence cannot currently be reconciled.

CURRENT STATE

Current State describes the best-supported present condition.

CANON

Canon represents the human-governed authoritative engineering truth of the project.

The exact future terminology and definitions remain subject to CSL research and governance.

The important requirement is already visible:

the reader should not have to guess what the language means.

---

## 0.8.49 — The Legend Describes CSL, Not the Project

A critical distinction must be maintained.

The CSL legend answers:

"What does this type of thing mean in CSL?"

The Living Project Image answers:

"What is true about this particular project?"

These must not be mixed.

For example:

LEGEND

TRANSFORMATION

A meaningful change from one project reality to another.

PROJECT CONTENT

TR-0042 — Establish Layered Memory

The first teaches the language.

The second uses the language.

This separation allows CSL literacy to transfer between projects.

Once a human learns what Transformation means in AI-Toolkit, the same semantic concept should remain recognizable when AI-Toolkit is used to understand another project.

---

## 0.8.50 — Stable Meaning Across Projects

If CSL is intended to become a common language between:

humans;

AI systems;

Canon;

project implementation;

memory;

research;

audit;

and project evolution,

then fundamental CSL terms cannot arbitrarily change meaning from one project to another.

For example:

EVIDENCE

must not mean one thing in AI-Toolkit and a fundamentally different thing in Trading Signals Platform.

Likewise:

TRANSFORMATION

MEMORY

DECISION

UNKNOWN

CONTRADICTION

should retain stable semantic identities.

Project-specific content may differ.

The language should remain stable.

This creates transferable CSL literacy.

---

## 0.8.51 — Standardized Legend

The legend should therefore be derived from the CSL language definition rather than manually reinvented inside every project.

Conceptually:

CSL LANGUAGE
    │
    ├── semantic vocabulary
    ├── meaning
    ├── relationships
    ├── reading conventions
    ├── visual conventions
    └── standard legend
             │
             ▼
     HUMAN-FACING CSL
             │
             ├── AI-Toolkit
             ├── Trading Project
             ├── DROPi
             └── Future Projects

A future renderer or CSL-aware application may generate the appropriate legend automatically.

The technical mechanism is not yet decided.

The semantic requirement is:

one language should teach one stable conceptual system.

---

## 0.8.52 — Portable Understanding

A human-facing CSL artifact should remain understandable when separated from the environment in which it was originally produced.

For example, a person may receive a CSL representation through:

a repository;

an exported document;

an audit package;

a future dashboard;

a local file;

a preserved archive.

The person should still be able to determine:

what language is being used;

what the principal semantic categories mean;

what project is represented;

how to begin reading it.

This suggests a future distinction between representations optimized for portability and representations optimized for compactness.

---

## 0.8.53 — Human Portable CSL and Compact CSL

The research suggests at least two possible representation profiles.

### Human Portable CSL

Optimized for independent human comprehension.

It may contain:

- language identity;
- CSL version;
- reading legend;
- human-readable titles;
- explanatory labels;
- visual semantics where available;
- navigable provenance;
- sufficient orientation to understand the artifact independently.

### Compact CSL

Optimized for efficient machine use or expert workflows.

It may reduce:

- repeated explanations;
- legend content;
- descriptive labels;
- redundant human guidance.

It may rely more heavily on:

- stable identifiers;
- machine-resolvable relations;
- references;
- compact semantic notation.

These profiles must not represent different project realities.

They are different views of the same epistemic content.

The exact profiles remain a future design problem.

---

## 0.8.54 — Self-Teaching Representation Principle

### Self-Teaching Representation Principle

A human-facing CSL representation should provide sufficient language guidance for a person unfamiliar with CSL to begin interpreting its meaning without requiring prior specialist training.

The objective is not to teach the complete language inside every document.

The objective is to remove the initial barrier to comprehension.

A newcomer should be able to begin.

Repeated use should deepen understanding.

---

## 0.8.55 — CSL Should Become Familiar Through Exposure

A human language becomes easier to understand through repeated exposure to stable patterns.

The same principle can be deliberately used in CSL.

If:

Need always means Need;

Evidence always means Evidence;

Transformation always means Transformation;

Memory always means Memory;

Contradiction always communicates contradiction;

and their visual and semantic identities remain stable,

then the human begins to recognize meaning before consciously analyzing every element.

This reduces cognitive effort over time.

CSL literacy should therefore be designed to emerge progressively through normal project use.

---

## 0.8.56 — Progressive Familiarity Principle

### Progressive Familiarity Principle

Repeated exposure to human-facing CSL should progressively reduce the cognitive effort required to interpret it.

Stable terminology, stable semantic identities, stable visual conventions, and an embedded reading legend should allow CSL literacy to develop naturally through use.

In human terms:

CSL should be learnable by reading CSL.

The user should not need to become a software engineer before the language becomes useful.

---

## 0.8.57 — Visual Semantics

The human proposal introduced an additional cognitive mechanism:

stable color identity.

The purpose of color is not decoration.

The purpose is semantic recognition.

If a semantic category possesses a stable visual identity, the human brain may begin to recognize the category before reading every word.

For example, a future human interface may allow a person to visually distinguish:

Memory;

Evidence;

Transformation;

Decision;

Unknown;

Contradiction;

Canon;

Current State.

The exact colors are not yet selected.

The research question is broader:

Can stable visual semantics reduce the cognitive cost of navigating complex epistemic structures?

The current research direction says yes, provided visual semantics remain supplementary rather than authoritative.

---

## 0.8.58 — Color as a Cognitive Accelerator

Color may operate as a secondary recognition channel.

Conceptually:

TEXTUAL IDENTITY
+
SEMANTIC TITLE
+
VISUAL IDENTITY
=
FASTER HUMAN RECOGNITION

For example, after repeated use, a human may recognize:

"This belongs to Memory."

before consciously reading the full heading.

This resembles visual recognition in many human environments.

The objective is not merely beauty.

The objective is cognitive orientation.

---

## 0.8.59 — Visual Identity Must Be Stable

If Memory is represented by one visual identity today and an unrelated identity tomorrow, the cognitive learning benefit disappears.

Likewise, if the same color means:

Memory in one project;

Decision in another project;

Evidence in a third project,

the language becomes visually ambiguous.

Therefore visual semantics, where used, should belong to CSL rather than individual project preference.

Conceptually:

CSL SEMANTIC CATEGORY
        ↓
STABLE VISUAL IDENTITY
        ↓
ALL HUMAN-FACING CSL VIEWS

This allows visual familiarity to transfer between projects.

---

## 0.8.60 — Do Not Assign Final Colors Prematurely

The current research should not yet define:

Memory = blue;

Evidence = green;

Contradiction = red;

or any other final palette.

Such choices require later investigation of:

- accessibility;
- contrast;
- color-vision differences;
- light and dark interfaces;
- monochrome rendering;
- terminal compatibility;
- printing;
- cultural interpretation;
- cognitive distinction;
- visual overload.

The research requirement is:

stable semantic visual identity.

The specific palette is a later design decision.

---

## 0.8.61 — Meaning Must Survive Without Color

A fundamental accessibility requirement follows.

The Living Project Image may be consumed through:

plain text;

a terminal;

a screen reader;

a monochrome display;

printed material;

an environment that strips styling;

a future parser that ignores presentation.

Therefore no epistemic meaning may depend exclusively on color.

Incorrect:

RED

with no textual indication that the entity represents a contradiction.

Correct:

CONTRADICTION — Canon and Observed Reality Disagree

with an additional stable visual identity when the rendering environment supports it.

Color strengthens recognition.

Text establishes explicit meaning.

---

## 0.8.62 — Semantic Redundancy Principle

### Semantic Redundancy Principle

No epistemic meaning shall depend exclusively upon color or another visual property.

Visual identity shall reinforce explicit semantic identity rather than replace it.

This protects:

accessibility;

portability;

machine interpretation;

plain-text readability;

long-term preservation.

The semantic structure must remain complete when styling is removed.

---

## 0.8.63 — Visual Semantic Families

Assigning a completely unrelated color to every epistemic entity type could create visual overload.

The human may eventually encounter dozens of semantic categories.

Therefore the research suggests grouping related concepts into visual semantic families.

Conceptually:

EVOLUTION FAMILY

- Need
- Research
- Decision
- Transformation
- Action

TRUTH AND VERIFICATION FAMILY

- Claim
- Evidence
- Verification
- Witness

MEMORY FAMILY

- Experience
- Memory
- Knowledge
- Historical State

EPISTEMIC CONDITION FAMILY

- Known
- Unknown
- Contradiction
- Stale
- Unverified
- Absent

GOVERNANCE FAMILY

- Canon
- Authority
- Approval
- Supersession

ANATOMY FAMILY

- Organism
- Organ System
- Organ
- Tissue
- Artifact

These families are research candidates, not a finalized taxonomy.

The important insight is hierarchical visual cognition.

The human may first recognize:

"This belongs to Memory."

and then determine:

"This is Persistent Experience rather than sedimented Knowledge."

---

## 0.8.64 — Hierarchical Visual Recognition

The visual system should eventually support more than flat category recognition.

Conceptually:

FAMILY
    ↓
CATEGORY
    ↓
SPECIFIC ENTITY

For example:

MEMORY FAMILY
    ↓
MEMORY
    ↓
MEM-0021 — Execution Context Knowledge

or:

EVOLUTION FAMILY
    ↓
TRANSFORMATION
    ↓
TR-0042 — Establish Layered Memory

This gives the human several levels of orientation simultaneously.

The design should reduce cognitive burden rather than add visual complexity.

---

## 0.8.65 — Visual Semantics Principle

### Visual Semantics Principle

Epistemically meaningful categories may possess stable visual identities that improve recognition and navigation for humans, provided that no meaning depends exclusively upon visual styling and the underlying representation remains semantically complete without it.

Visual semantics belong to human cognition.

Semantic identity remains authoritative.

---

## 0.8.66 — CSL Must Work Without Styling and Improve With Styling

The target relationship can be stated clearly:

PLAIN CSL

must remain understandable.

RENDERED CSL

should become faster and easier for humans to interpret.

Therefore:

SEMANTIC COMPLETENESS
    ↓
PLAIN REPRESENTATION

plus:

VISUAL SEMANTICS
    ↓
COGNITIVE ACCELERATION

The styled representation improves experience.

It does not create additional truth.

---

## 0.8.67 — Representation Versus Meaning

This distinction protects CSL from becoming dependent upon one application.

Suppose a future AI-Toolkit dashboard renders:

Transformation with one visual treatment;

Evidence with another;

Memory with another.

The `.csl` semantic representation must remain valid even if that dashboard disappears.

Another renderer should be capable of reconstructing equivalent meaning.

Therefore:

CSL SEMANTICS

must be separable from:

CSL PRESENTATION.

This is important for long-term continuity.

---

## 0.8.68 — No Renderer May Become the Source of Truth

A future CSL editor, dashboard, mobile application, web interface, or AI viewer may provide a rich presentation.

None should become the authoritative project reality merely because humans find it convenient.

The authoritative epistemic content must remain independently preservable and resolvable.

The renderer is an organ of perception.

It is not the truth itself.

Conceptually:

PROJECT REALITY
    ↓
CSL SEMANTIC REPRESENTATION
    ↓
RENDERER
    ↓
HUMAN PERCEPTION

If the renderer disappears, project meaning must remain recoverable.

---

## 0.8.69 — Human-Readable Identity Plus Visual Identity

The research now combines several principles.

A human-facing entity may eventually appear conceptually as:

[VISUAL IDENTITY: TRANSFORMATION]

TR-0042 — Establish Layered Memory

The human receives:

VISUAL FAMILY

"What kind of thing is this?"

SEMANTIC CATEGORY

"This is a Transformation."

STABLE IDENTIFIER

"Which exact Transformation is it?"

HUMAN TITLE

"What does this Transformation mean?"

This multi-channel identity is much more cognitively useful than:

TR-0042

alone.

---

## 0.8.70 — Semantic Titles Must Remain Concise

Human-readable titles lose their value if they become miniature paragraphs.

For example:

TR-0042 — Establish Layered Memory

creates a quick mental image.

A title such as:

TR-0042 — Establish a New Multi-Level Hierarchical Persistent Epistemic Memory Architecture for Context-Preserving Artificial Intelligence Continuity Across Project Sessions

may contain more detail but destroys rapid recognition.

The title should communicate the entity's core meaning.

Detailed explanation belongs inside the entity.

This supports scanning and navigation.

---

## 0.8.71 — Semantic Title as Cognitive Handle

A concise title functions as a cognitive handle.

The identifier gives exact identity.

The title gives the human something memorable.

For example:

NEED-0031 — Prevent Context Loss

DECISION-0019 — Adopt Persistent Experience

EXP-0042 — First Captured Terminal Run

EV-0103 — Terminal Capture Proof

WT-0042 — Terminal Experience Witness

MEM-0021 — Execution Context Knowledge

STATE-0011 — Persistent Execution Enabled

These identities allow the human to build a mental map.

Without titles, the project becomes a field of codes.

With titles, the codes remain precise while the project becomes readable.

---

## 0.8.72 — Semantic Relationships Should Also Be Human-Readable

Entities are not the only structures requiring human comprehension.

Relationships must also communicate meaning.

Instead of exposing only machine relationships such as:

REL-0041

the human should see relationships conceptually equivalent to:

PRODUCED BY

SUPPORTED BY

SUPERSEDES

CONTRADICTS

DERIVED FROM

REQUIRES

IMPLEMENTED BY

VERIFIED BY

PART OF

PRECEDED BY

FOLLOWED BY

CURRENT VERSION OF

The exact future CSL relationship vocabulary remains to be researched.

The requirement is:

relationships should communicate their meaning directly.

---

## 0.8.73 — The Human Should Be Able to Read the Project as a Story of Reality

A well-formed Living Project Image should permit a human to follow relationships naturally.

For example:

NEED-0031 — Prevent Context Loss

LED TO

RES-0012 — Project-Owned Continuity Research

WHICH PRODUCED

DECISION-0019 — Adopt Persistent Experience

WHICH ENABLED

TR-0042 — Establish Layered Memory

WHICH CONTRIBUTED TO

MEM-0021 — Execution Context Knowledge

SUPPORTED BY

EV-0103 — Terminal Capture Proof

The human does not need to decode a database graph.

The project tells an intelligible story while preserving formal identities.

---

## 0.8.74 — Human Narrative Must Not Invent Causality

Readable relationships create another risk.

The system may be tempted to tell a smooth story even when causality has not been demonstrated.

For example:

A happened before B.

That does not automatically mean:

A caused B.

Therefore CSL must distinguish relationships such as:

PRECEDED

from:

CAUSED

or:

LED TO

when evidence differs.

Human readability must not weaken epistemic rigor.

A beautiful story that invents causality is worse than an incomplete but truthful representation.

---

## 0.8.75 — Relationship Evidence

Important semantic relationships may themselves require Evidence.

For example:

CLAIM

Decision A caused Transformation B.

The system should be capable of answering:

How do we know?

Possible support may include:

- explicit owner instruction;
- Transformation record;
- conversation context;
- implementation history;
- decision reference.

Therefore relationships are not always merely structural links.

Some relationships are epistemic Claims.

They must remain verifiable.

---

## 0.8.76 — Navigability and Human Semantic Titles Reinforce Each Other

Consider an audit path.

The human sees:

TR-0042 — Establish Layered Memory

and selects:

SUPPORTED BY

The next representation may show:

EV-0103 — Terminal Capture Proof

The human can immediately understand the destination before opening it.

If only opaque identifiers were displayed:

TR-0042
    ↓
EV-0103

the audit path would technically exist but remain cognitively expensive.

Therefore:

navigation;

human-readable identity;

semantic relationships;

visual identity;

provenance

must cooperate.

---

## 0.8.77 — CSL Should Support Epistemic Travel, Not Merely Hyperlinks

A hyperlink says:

"Go to this location."

Epistemic navigation should say:

"Why would you go there?"

For example:

SUPPORTED BY
    → EV-0103 — Terminal Capture Proof

DERIVED FROM
    → EXP-0042 — First Captured Terminal Run

AUTHORIZED BY
    → DECISION-0019 — Adopt Persistent Experience

SUPERSEDES
    → DECISION-0012 — Earlier Memory Approach

The relationship itself gives meaning to the journey.

Thus navigability becomes semantic rather than merely positional.

---

## 0.8.78 — The Project Should Be Navigable by Question

A mature Living Project Image may eventually allow the human to approach the project through natural epistemic questions.

For example:

WHAT IS THIS?

    → Identity

WHY DOES IT EXIST?

    → Purpose / Need / Origin

WHAT SHOULD EXIST?

    → Canon

WHAT ACTUALLY EXISTS?

    → Current Reality

HOW DO WE KNOW?

    → Evidence / Verification

HOW DID WE GET HERE?

    → Transformations / Lineage

WHAT FAILED?

    → Negative Knowledge

WHAT DO WE NOT KNOW?

    → Unknown / Epistemic Fog

WHAT CHANGED?

    → Transformation / State Difference

WHO AUTHORIZED THIS?

    → Authority / Decision

WHAT SHOULD WE DO NEXT?

    → Current Purpose / Gap / Frontier

This may become one of the most human-friendly ways to explore CSL.

---

## 0.8.79 — CSL Literacy Should Not Require Memorizing Repository Geography

A person should not need to remember:

work/research/...

work/evidence/...

lib/python/...

some deeply nested directory...

in order to understand project reality.

Filesystem location remains important for technical resolution.

It should not be the primary human memory mechanism.

The human should remember:

Layered Memory

rather than:

the exact path where one representation of Layered Memory happens to be stored.

The organism should resolve meaning toward location.

---

## 0.8.80 — Semantic Addressing

This suggests a research direction:

semantic addressing.

A human concept may have:

stable identity;

human-readable title;

semantic type;

relationships;

one or more physical representations.

For example:

TR-0042 — Establish Layered Memory

may resolve toward:

- a Transformation record;
- relevant research;
- Evidence;
- repository changes;
- Memory;
- historical state.

The human begins from meaning.

The organism resolves toward physical reality.

The exact mechanism remains a future implementation question.

---

## 0.8.81 — Physical Location and Epistemic Identity Are Different

A file can move.

A directory can be renamed.

A repository may be reorganized.

If epistemic identity depends entirely on physical path, project meaning becomes fragile.

Therefore:

PHYSICAL LOCATION

and:

EPISTEMIC IDENTITY

must not be treated as identical concepts.

The organism should be capable of preserving identity while updating location.

This is especially important for long-lived projects.

---

## 0.8.82 — Living Image as Orientation Layer

The Living Project Image can now be understood as the organism's primary orientation layer.

It should allow a human or AI to answer:

WHERE AM I?

WHAT IS THIS?

WHAT IS CURRENTLY TRUE?

WHAT IS UNCERTAIN?

WHAT IS WRONG?

WHAT CHANGED?

WHY?

WHERE IS THE EVIDENCE?

WHERE CAN I GO DEEPER?

This orientation layer sits above detailed memory without replacing it.

---

## 0.8.83 — A Possible Future Human Experience

Imagine opening the Living Project Image after a year of project development.

The first view may conceptually present:

AI-TOOLKIT — LIVING PROJECT IMAGE

CSL READING GUIDE

New to CSL?
The legend explains the semantic categories and visual identities used below.

IDENTITY

AI-Toolkit — Epistemic Engineering Organism

PURPOSE

Preserve human-directed engineering continuity across AI-assisted project development.

CURRENT CONDITION

Operational capabilities exist alongside capabilities under active research and development.

MEMORY

Persistent Experience — Operational / verified according to current evidence.

Layered Memory — Research direction established; implementation condition separately represented.

Progressive Recall — Defined in research; implementation condition separately represented.

CURRENT TRANSFORMATION

Establish Project-Owned Continuity.

KNOWN GAP

Automatic preservation of Human ↔ AI research is not yet demonstrated.

CONTRADICTION

An older representation describes a capability differently from the current research model.

UNKNOWN

The current condition of a specific organ has not been verified after a recent Transformation.

NEXT PURPOSE

Establish automatic continuity capture and Living Project Image generation.

Each statement can then expose:

WHY?

HISTORY

EVIDENCE

CANON

IMPLEMENTATION

CURRENT STATE

RELATED TRANSFORMATIONS

The human does not begin by searching 1,300 files.

The organism explains itself.

---

## 0.8.84 — The Living Project Image Must Distinguish Research From Reality

The example above exposes another critical requirement.

A concept may exist in research without existing in implementation.

For example:

Layered Memory may be:

RESEARCH-ESTABLISHED

but:

NOT YET IMPLEMENTED.

The Living Project Image must not collapse those states.

Likewise:

a proposed organ;

a canonical requirement;

a prototype;

a verified operational capability

are not equivalent.

The image must communicate the epistemic and realization status of each.

This prevents research language from being mistaken for existing capability.

---

## 0.8.85 — Concept Existence and Implementation Existence

EXIST may therefore require several dimensions.

For example:

Does the concept exist in research?

Does the requirement exist in Canon?

Does a design exist?

Does an implementation exist?

Has the implementation been verified?

Is it currently operational?

These are different existence questions.

A concept can exist without implementation.

An implementation can exist without canonical authorization.

A capability can have existed historically but not currently.

The Living Project Image must eventually represent these distinctions explicitly.

---

## 0.8.86 — Avoiding False Capability Inflation

AI-generated project descriptions frequently make statements such as:

"The system supports X."

when the repository merely contains:

a design document;

an unfinished class;

a placeholder;

an old test;

a planned roadmap item.

The Living Project Image must resist this.

A capability should be represented according to demonstrated reality.

Possible future conditions may include concepts such as:

PROPOSED

RESEARCHED

CANONICALLY REQUIRED

DESIGNED

PARTIALLY REALIZED

REALIZED

VERIFIED

OPERATIONAL

REGRESSED

RETIRED

ABSENT

UNKNOWN

The final state model remains future research.

The important requirement is:

do not confuse mention with existence.

---

## 0.8.87 — Mention Does Not Establish Existence

A term appearing in a document does not establish that the corresponding entity or capability exists in the relevant sense.

Likewise:

a filename does not establish operational capability;

a class name does not establish functioning behavior;

a roadmap item does not establish implementation;

an old test does not establish current operation;

a conversation does not establish Canon.

This principle is a direct consequence of EXIST.

The Living Project Image must determine which kind of existence is actually supported.

---

## 0.8.88 — Current Truth Must Be Evidence-Bounded

The Living Project Image should only claim as current truth what available evidence supports at the required epistemic level.

If the evidence supports:

"Research exists."

the image must not inflate that into:

"Capability exists."

If the evidence supports:

"Implementation artifact exists."

the image must not automatically inflate that into:

"Capability is operational."

If the evidence supports:

"Capability passed verification before Transformation X."

the image must not automatically claim:

"Capability is currently verified after Transformation X."

This creates an evidence-bounded image.

---

## 0.8.89 — Evidence-Bounded Representation Principle

### Evidence-Bounded Representation Principle

The Living Project Image shall not represent an entity, capability, relationship, state, or conclusion at a stronger epistemic level than the available Evidence supports.

In human terms:

The image must not claim more than it can prove.

This is fundamental to preserving trust.

---

## 0.8.90 — Living Image Confidence Must Be Explainable

If the organism communicates confidence, that confidence should not be a mysterious number.

For example:

CONFIDENCE: 0.83

is of limited human value without explanation.

The human should be able to understand why confidence is high or low.

Possible explanatory factors may include:

current verification;

source quality;

independent evidence;

contradiction;

staleness;

incomplete observation;

historical consistency.

The exact confidence model remains future research.

The requirement is:

confidence must remain explainable and evidence-connected.

---

## 0.8.91 — Visual Semantics May Represent Epistemic Condition

The earlier color proposal may eventually help expose epistemic condition as well as semantic category.

However, this requires careful design.

The human may need to distinguish simultaneously:

WHAT TYPE OF THING IS THIS?

and:

WHAT CONDITION IS IT IN?

For example:

Transformation = semantic category.

Contradicted = epistemic condition.

If both use color independently, visual conflict may occur.

Therefore the future visual grammar may require separate visual channels such as:

family color;

icon;

border;

marker;

label;

shape;

textual status.

No design is selected yet.

The important research finding is:

semantic type and epistemic condition are separate dimensions.

The visual grammar must not confuse them.

---

## 0.8.92 — Category Is Not Condition

Examples:

MEMORY

is a category.

STALE

is a condition.

EVIDENCE

is a category.

CONTRADICTED

may describe the condition of a Claim supported or challenged by Evidence.

CAPABILITY

is a category.

UNVERIFIED

is a condition.

TRANSFORMATION

is a category.

FAILED

may describe its outcome.

This distinction will be essential in CSL Cognitive Grammar.

---

## 0.8.93 — Anatomy Is Not Epistemic Status

Likewise:

Organ;

Tissue;

Organ System;

Artifact

describe structural identity.

They do not by themselves say whether the structure:

exists;

works;

is healthy;

is verified;

is canonical;

is experimental;

is stale;

is contradicted.

The Living Project Image must therefore represent multiple dimensions without collapsing them.

For example:

ORGAN

Memory

REALIZATION CONDITION

Partially realized

EPISTEMIC CONDITION

Partially verified

CANONICAL CONDITION

Research-defined, not yet canonically finalized

HISTORY

Derived from continuity research

EVIDENCE

[references]

This is much more truthful than a simple:

Memory — Exists.

---

## 0.8.94 — Multidimensional Project Reality

The research now suggests that an epistemic entity may require several independent dimensions.

Potential dimensions include:

IDENTITY

What exact thing is this?

SEMANTIC TYPE

What kind of thing is it?

MEANING

What does it mean?

AUTHORITY

Who or what governs it?

EXISTENCE

In what sense does it exist?

REALIZATION

Has it been built or instantiated?

OPERATIONAL CONDITION

Does it currently function?

EPISTEMIC CONDITION

How strongly is its state known?

TEMPORAL CONDITION

Is the information current, historical, stale, superseded?

PROVENANCE

Where does the knowledge come from?

RELATIONSHIPS

How does it connect to other entities?

These dimensions should not be prematurely flattened into one status field.

---

## 0.8.95 — Human View Must Hide Complexity Without Destroying It

A human does not necessarily want to see ten dimensions for every entity at all times.

The Living Project Image should therefore support progressive disclosure.

Initial view:

Layered Memory — Partially Established

Deeper view:

Research:
Established.

Canonical requirement:
Not yet finalized.

Implementation:
Partial.

Verification:
Incomplete.

Current confidence:
Explainable from listed Evidence.

History:
Available.

Evidence:
Available.

The complexity remains.

The human sees it when necessary.

This is another application of Progressive Recall to representation.

---

## 0.8.96 — Cognitive Compression Without Epistemic Loss

The Living Project Image must compress complexity for human cognition without deleting the paths required to recover deeper truth.

This can be represented as:

DEEP PROJECT REALITY
        ↓
COGNITIVE COMPRESSION
        ↓
HUMAN-UNDERSTANDABLE IMAGE
        ↓
NAVIGABLE EXPANSION
        ↓
DEEP PROJECT REALITY

Compression is acceptable.

Irrecoverable distortion is not.

---

## 0.8.97 — Cognitive Compression Principle

### Cognitive Compression Principle

Human-facing project representations may compress epistemic complexity for comprehension, provided that the compression does not misrepresent the supported reality and preserves resolvable paths toward the deeper information required for verification or understanding.

This principle may become fundamental to CSL rendering.

---

## 0.8.98 — The Living Project Image Should Change When Reality Changes

A static project map will eventually become false.

The Living Project Image must therefore possess a maintenance physiology.

Conceptually:

PROJECT CHANGE
    ↓
OBSERVATION
    ↓
RELEVANT EVIDENCE CHANGES
    ↓
AFFECTED EPISTEMIC ENTITIES IDENTIFIED
    ↓
CURRENT UNDERSTANDING RE-EVALUATED
    ↓
LIVING PROJECT IMAGE UPDATED

This does not imply rewriting Canon.

It means the current representation must respond to observed project change.

---

## 0.8.99 — Change Propagation

A Transformation may affect more than one visible statement.

For example:

A Memory organ changes.

This may affect:

implementation state;

verification state;

capability state;

related Evidence;

current project condition;

known gaps;

Living Project Image summaries.

The future system should therefore understand dependencies between epistemic statements.

A change in underlying reality should identify which derived representations may have become stale.

This is one reason explicit relationships are essential.

---
## 0.8.100 — Staleness Propagation

Suppose:

Evidence E verified Capability C.

Transformation T modifies the organ upon which C depends.

The organism should consider whether:

Evidence E remains sufficient for the current version of C.

If not, C may transition conceptually from:

VERIFIED

to:

VERIFICATION STALE

until new Evidence is produced.

This is more trustworthy than carrying old verification forward indefinitely.

The exact invalidation rules remain future research.

---

## 0.8.101 — The Living Image Must Not Become a Manually Maintained Dashboard

If every project change requires a human to manually update:

current capability lists;

status pages;

memory descriptions;

gap registers;

project summaries;

then divergence will eventually occur.

The Living Project Image should increasingly be derived from evidence-connected project structures.

Humans may approve or correct high-impact interpretations.

But routine synchronization should become physiological behavior of the organism.

The image should be alive because the organism maintains it, not because a human repeatedly rewrites a status report.

---

## 0.8.102 — Derived but Verifiable

This creates an important balance.

The Living Project Image may be largely derived.

But derived does not mean untrustworthy if:

the derivation is explainable;

sources are traceable;

Evidence is accessible;

uncertainty is explicit;

human authority is preserved;

the image can be regenerated.

This resembles the earlier rule:

internal representations may be derived from Canon and project reality.

Derived structures should remain regenerable rather than becoming secret independent truth.

---

## 0.8.103 — Regenerability

A mature Living Project Image should ideally be reconstructible from preserved authoritative project reality.

If the rendered image is deleted, the organism should be capable of rebuilding it from:

Canon;

epistemic identities;

current implementation observations;

Memory;

Transformations;

Evidence;

Provenance;

Lineage;

governed decisions.

The exact reconstruction architecture remains future engineering work.

The research requirement is:

loss of a derived view must not equal loss of project truth.

---

## 0.8.104 — Regenerable View Principle

### Regenerable View Principle

Derived human, audit, engineering, and AI views of the Living Project Image should, where practical, remain regenerable from preserved authoritative epistemic sources rather than becoming irreplaceable independent stores of project truth.

This strengthens the Single Reality, Multiple Views Principle.

---

## 0.8.105 — The Living Image and AI Context

The Living Project Image may become one of the principal sources from which future AI Context Packages are generated.

Instead of giving a new AI:

the complete repository;

the complete conversation archive;

every historical Transformation;

all raw Evidence;

the entire Memory;

the organism can provide:

relevant current image;

relevant recent evolution;

relevant Canon;

relevant Memory;

relevant unresolved frontier;

references for deeper retrieval.

This directly supports context efficiency.

---

## 0.8.106 — AI Should Receive Context According to Purpose

A new AI working on:

Trading Signals Platform deployment

does not necessarily require every detail of:

AI-Toolkit's historical CSL color research.

Likewise, an AI researching CSL does not require all raw runtime logs from an unrelated project.

The Living Project Image and Layered Memory should allow context to be selected according to purpose.

PURPOSE
    ↓
RELEVANT CURRENT IMAGE
    ↓
RELEVANT MEMORY
    ↓
RELEVANT HISTORY
    ↓
RELEVANT EVIDENCE
    ↓
AI CONTEXT PACKAGE

This is Progressive Recall applied to AI collaboration.

---

## 0.8.107 — Context Efficiency Must Not Become Context Distortion

Compression and relevance selection create a risk.

The organism may omit context that changes the meaning of what remains.

Therefore context generation must preserve:

material contradictions;

relevant uncertainty;

authority boundaries;

important rejected alternatives;

applicable Negative Knowledge;

critical provenance;

current gaps.

A shorter context is useful only if it remains epistemically faithful.

---

## 0.8.108 — Context Fidelity Principle

### Context Fidelity Principle

A derived context representation may omit information that is not relevant to its declared purpose, but it shall not omit material context in a manner that changes the supported meaning, authority, uncertainty, or epistemic condition of the information presented.

This principle will be important for future AI Context Packages.

---

## 0.8.109 — The Living Project Image and Project Handover

The original continuity problem involved transferring work from one AI session to another.

The Living Project Image changes the nature of handover.

Instead of manually writing:

"Here is everything we discussed..."

the project may eventually provide:

WHO I AM

WHAT I AM TRYING TO ACHIEVE

WHAT IS TRUE NOW

WHAT HAS RECENTLY CHANGED

WHAT HAS BEEN DECIDED

WHAT IS STILL UNDER RESEARCH

WHAT IS UNKNOWN

WHAT HAS FAILED BEFORE

WHAT EVIDENCE MATTERS

WHAT THE CURRENT HUMAN WANTS

WHERE THE CURRENT FRONTIER IS

HOW TO TRAVEL DEEPER

This is a project-generated handover rather than a conversation-generated handover.

---

## 0.8.110 — From Conversation Continuity to Organism Continuity

The initial problem was:

"How do we continue when this conversation reaches its maximum context?"

The deeper solution is not:

"Make a better conversation summary."

It is:

"Make the project capable of carrying its own epistemic continuity."

This is a fundamental transition.

OLD MODEL

AI remembers project.

NEW MODEL

Project remembers itself and informs AI.

The AI remains extremely useful.

But continuity no longer depends entirely upon that AI instance.

---

## 0.8.111 — Living Project Image as Anti-Dementia Physiology

The earlier research used the term "epistemic dementia" to describe repeated loss of project understanding when context disappears or new AI agents begin without sufficient history.

The Living Project Image contributes to the solution by preserving:

identity;

current truth;

history;

meaning;

relationships;

uncertainty;

negative knowledge;

current frontier.

Persistent Experience preserves lived history.

Layered Memory controls accumulated knowledge.

Progressive Recall retrieves relevant depth.

The Living Project Image provides present orientation.

Together they create continuity physiology.

---

## 0.8.112 — CSL Is Becoming the Language of Organism Self-Knowledge

The role of CSL can now be expressed more strongly.

CSL is not merely a specification language through which humans tell software what to build.

It is emerging as the language through which the epistemic organism can express:

what it is;

what it should be;

what it currently is;

what it knows;

what it remembers;

what changed;

what it cannot establish;

what contradicts;

what evidence exists;

what the human decided;

what remains to be done.

This does not yet define final CSL.

It establishes the research objective that CSL must satisfy.

---

## 0.8.113 — CSL as Human–AI–Project Common Language

The project contains several participants and realities:

HUMAN

provides purpose, judgment, creativity, authority, and lived intention.

AI

assists research, reasoning, interpretation, engineering, verification, and navigation.

CANON

preserves governed engineering truth.

IMPLEMENTATION

realizes project behavior.

MEMORY

preserves project experience and learned understanding.

EVIDENCE

supports what can be believed.

CSL must become the common semantic bridge among them.

Conceptually:

                    HUMAN
                      │
                      │
                      ▼
                     CSL
                 ↙    ↓    ↘
              CANON   AI   LIVING IMAGE
                │      │       │
                └──────┼───────┘
                       ▼
                 PROJECT REALITY

This is why CSL cannot be designed merely as a parser syntax.

It carries epistemic responsibility.

---

## 0.8.114 — The Human Must Remain Able to Correct the Image

The Living Project Image may contain derived interpretations.

AI may help maintain them.

Automated observation may update them.

But the human must remain able to challenge statements such as:

"That is not what I meant."

"That decision was only exploratory."

"That capability is not actually complete."

"That relationship is wrong."

"That title misrepresents the idea."

"That research direction was rejected."

Such corrections become new epistemic events and may require re-evaluation of dependent representations.

The organism must support correction rather than defend its previous interpretation.

---

## 0.8.115 — Correction Must Preserve History

If a Living Project Image statement is corrected, the system should not necessarily erase the fact that the incorrect interpretation previously existed.

For significant cases, continuity may need to preserve:

PREVIOUS INTERPRETATION

why it was produced;

CORRECTION

what changed our understanding;

CURRENT INTERPRETATION

what is now supported.

This prevents silent historical rewriting.

It also allows the organism to learn from interpretive error.

---

## 0.8.116 — The Image Is a Claim About Reality

A profound consequence follows.

Every meaningful statement in the Living Project Image is effectively a Claim about project reality.

For example:

"Persistent Experience is operational."

is a Claim.

"Layered Memory is only research-defined."

is a Claim.

"Capability X is absent."

is a Claim.

"Decision Y governs this organ."

is a Claim.

Therefore the Living Project Image itself must remain subject to:

Evidence;

Traceability;

Falsifiability;

Correction;

Governance where applicable.

The image cannot sit outside the epistemic rules of the organism.

---

## 0.8.117 — Self-Auditable Image

Because Living Project Image statements are Claims, the image should eventually be auditable.

The organism may ask of itself:

Which current statements lack Evidence?

Which statements depend on stale Evidence?

Which relationships are inferred rather than explicit?

Which claims contradict Canon?

Which capabilities have not been recently verified?

Which human decisions have ambiguous authority scope?

Which current states depend upon superseded information?

This turns the Living Project Image into an auditable epistemic structure rather than a decorative project overview.

---

## 0.8.118 — The Image Must Expose Its Own Weaknesses

A trustworthy organism should not only expose project weaknesses.

It should expose weaknesses in its own understanding of the project.

For example:

CURRENT IMAGE COVERAGE

82% of known critical organs currently verified.

UNVERIFIED AREA

Execution physiology changed after latest Transformation.

PROVENANCE GAP

One historical Decision lacks preserved original conversation context.

CONTRADICTION

Two research artifacts use incompatible terminology.

UNKNOWN

Current Railway realization not recently observed.

The exact future metrics are not decided.

The principle is:

the image must not pretend to know more about itself than it knows.

---

## 0.8.119 — Self-Inspection

The Living Project Image may therefore become one of the structures through which AI-Toolkit inspects itself.

This connects directly to the broader project requirement that AI-Toolkit should improve its ability to:

build;

maintain;

audit;

validate;

understand;

and evolve

AI-Toolkit itself while helping external projects.

The organism can compare:

WHAT I BELIEVE I AM

with:

WHAT MY CANON REQUIRES

and:

WHAT MY EVIDENCE DEMONSTRATES.

That comparison is a form of epistemic self-inspection.

---

## 0.8.120 — Self-Inspection Is Not Self-Authority

The organism may inspect itself.

It may identify contradictions.

It may propose corrections.

It may discover that Canon no longer matches implementation.

It may detect that its Living Project Image is stale.

It may recommend governance action.

But self-inspection does not grant unlimited self-authority.

Human authority and Canonical Governance remain applicable.

The organism can diagnose itself without unilaterally redefining what it is supposed to be.

---

## 0.8.121 — Living Project Image Integrity Depends on Provenance

Without provenance, the image becomes an AI-generated story.

With provenance, the image can become an auditable representation.

For every significant statement, the system should eventually be able to answer:

WHY IS THIS HERE?

WHAT SUPPORTS IT?

WHEN WAS IT LAST VERIFIED?

WHAT CHANGED SINCE THEN?

WHAT AUTHORITY APPLIES?

WHAT WOULD FALSIFY IT?

WHERE IS THE ORIGINAL EVIDENCE?

This is the foundation of trustworthy self-knowledge.

---

## 0.8.122 — Living Project Image Integrity Depends on Temporal Awareness

Current truth is temporal.

A statement may be true at time T1 and false at time T2.

Therefore the image should eventually understand temporal applicability.

For example:

STATE-0011 — Persistent Execution Enabled

VALID FROM:
Transformation X

LAST VERIFIED:
Verification Y

AFFECTED BY:
Transformation Z

CURRENT CONDITION:
Requires re-verification

The exact CSL syntax is not defined.

The research requirement is:

current truth must be aware of relevant change.

---

## 0.8.123 — Current Does Not Mean Latest File Timestamp

The newest modified file is not automatically the best representation of current truth.

A file may be:

recently copied;

recently reformatted;

generated from stale information;

modified without changing meaning.

Likewise, an older Canon may remain authoritative.

Therefore "current" must be determined epistemically, not merely chronologically.

Relevant factors may include:

authority;

supersession;

applicable Transformation;

Evidence;

verification;

lineage;

governance.

Timestamp is evidence.

Timestamp is not truth by itself.

---
## 0.8.124 — The Living Project Image Must Preserve Authority Status

Different statements may possess different authority.

For example:

OWNER IDEA

RESEARCH HYPOTHESIS

OWNER-ACCEPTED RESEARCH DIRECTION

ENGINEERING DECISION

CANONICAL REQUIREMENT

OBSERVED IMPLEMENTATION STATE

VERIFIED OPERATIONAL STATE

These are not interchangeable.

The Living Project Image must allow the human to understand not only:

"What does this say?"

but:

"What authority does this statement possess?"

This will be an important requirement for CSL Cognitive Grammar.

---

## 0.8.125 — Authority Must Be Visible Without Becoming Bureaucratic

If every line requires a large governance block, CSL becomes difficult to read.

The future grammar therefore needs cognitive compression.

For example, authority may be represented through:

stable labels;

visual markers;

semantic grouping;

inherited context;

expandable detail.

The human should be able to recognize authority quickly and inspect the deeper governance trail when necessary.

The exact representation remains future work.

---

## 0.8.126 — The Living Project Image Must Preserve Owner Meaning

Because AI-Toolkit exists to help the human develop personal projects, preserving human meaning is particularly important.

A technically correct implementation may still fail if it no longer reflects what the human intended.

Therefore the image should preserve links between:

OWNER PURPOSE

OWNER NEED

OWNER DECISION

ENGINEERING REALIZATION

CURRENT OUTCOME

This makes it possible to ask:

"Did the project merely build something?"

or:

"Did the project build what the human actually intended?"

This is a higher-order form of validation.

---

## 0.8.127 — Purpose Alignment

The organism should eventually be capable of detecting divergence not only from Canon but from active human purpose.

For example:

OWNER PURPOSE

Reduce dependency on external AI context.

IMPLEMENTATION DIRECTION

Creates a new subsystem requiring manual context reconstruction after every session.

The implementation may technically function.

But it contradicts the original purpose.

The Living Project Image should preserve enough purpose lineage to make such divergence visible.

---

## 0.8.128 — Purpose Is Part of Project Reality

Purpose is not merely introductory documentation.

It influences:

which Needs matter;

which Transformations are desirable;

which outcomes count as success;

which compromises are acceptable;

which future direction is coherent.

Therefore purpose belongs in the Living Project Image.

A project that remembers implementation but forgets purpose may continue moving while no longer knowing why.

---

## 0.8.129 — The Living Project Image Must Support Future Decision-Making

The image is not only retrospective.

It should help answer:

What should we work on next?

This answer should not come from arbitrary AI preference.

It should emerge from:

current purpose;

Canon;

known gaps;

contradictions;

failed verification;

active research;

dependencies;

owner priorities;

current capability state.

Thus future direction remains connected to present reality.

---

## 0.8.130 — Current Frontier

The Living Project Image should identify the current frontier.

The frontier is the meaningful boundary between:

what has already been established

and:

what is currently being investigated, built, corrected, or decided.

For the present research, the frontier is moving toward:

CSL Cognitive Grammar.

The project has established a working understanding of:

continuity;

memory;

provenance;

Living Project Image physiology;

human-readable identity;

self-teaching CSL;

visual semantics;

navigability.

It has not yet established the complete cognitive grammar through which these concepts should be expressed.

That is the next research problem.

---

## 0.8.131 — Living Project Image as Present-Facing Biography

The project possesses an epistemic biography through its preserved Transformations and history.

The Living Project Image is the present-facing expression of that biography.

Biography answers:

HOW DID I BECOME THIS?

Living Image answers:

WHAT AM I NOW?

Lineage connects them.

Purpose answers:

WHAT AM I TRYING TO BECOME?

Together:

PAST
    ↓
BIOGRAPHY
    ↓
PRESENT
    ↓
LIVING PROJECT IMAGE
    ↓
PURPOSE
    ↓
FUTURE

This creates temporal continuity of identity.

---

## 0.8.132 — The Image Must Not Freeze Identity

Project identity may itself evolve.

For example, AI-Toolkit began with earlier generations and capabilities.

The Epistemic Organism model represents an evolving research direction.

The Living Project Image must be able to distinguish:

historical identity;

current identity;

experimental future identity.

It must not rewrite older generations as though they had always possessed the current conceptual model.

Historical truth must remain historically accurate.

---

## 0.8.133 — Generational Awareness

A mature project may contain multiple generations simultaneously.

For example:

OLDER OPERATIONAL GENERATION

may contain usable capabilities.

RESEARCH GENERATION

may contain a more advanced conceptual architecture not yet production-ready.

The Living Project Image must not confuse:

newer research

with:

more operational capability.

Likewise, an older generation must not automatically be treated as irrelevant merely because newer research exists.

The image should represent:

what each generation is;

what it can do;

what it cannot do;

how generations relate;

which parts are authoritative for which purpose.

---

## 0.8.134 — Evolution Without Erasing Usable Capability

The project may need to enter practical use before the newest Epistemic Organism research is fully implemented.

The Living Project Image should therefore help identify:

usable existing capabilities;

research-only future capabilities;

migration paths;

compatibility;

gaps;

risks.

This prevents research ambition from unnecessarily blocking practical production.

It also prevents production urgency from destroying the deeper research direction.

Both realities can coexist explicitly.

---

## 0.8.135 — The Living Image Can Support Migration

When the organism evolves from an older architecture toward a newer epistemic architecture, the Living Project Image may eventually expose:

CURRENT ORGAN

existing operational implementation;

TARGET ORGAN

new epistemic physiology;

MIGRATION STATE

not started / partial / verified / complete;

PRESERVED CAPABILITY

what must continue working;

NEW CAPABILITY

what the new generation adds;

EVIDENCE

what demonstrates migration success.

This may become important for AI-Toolkit's own evolution.

---

## 0.8.136 — The Living Image Must Represent What Is Usable Now

A human trying to use AI-Toolkit on another project needs a practical answer:

"What can I use today?"

The image should eventually distinguish:

AVAILABLE NOW

PARTIALLY AVAILABLE

REQUIRES MANUAL WORK

UNDER DEVELOPMENT

RESEARCH ONLY

PLANNED

UNKNOWN

This is more useful than a roadmap that mixes all generations and ideas into one capability list.

The human can then decide whether to use an existing organ now or wait for a newer one.

---

## 0.8.137 — Practical Truth and Research Truth Must Coexist

A research conclusion may say:

"The future continuity physiology should work this way."

Operational truth may say:

"The current implementation does not yet work this way."

Both belong in the project image.

The image must not collapse:

TARGET REALITY

and:

CURRENT REALITY.

The difference between them is precisely what creates meaningful development work.

---

## 0.8.138 — Gap as a First-Class Epistemic Entity

A Gap is not merely an absence in a checklist.

A meaningful Gap connects:

EXPECTED REALITY

to:

OBSERVED REALITY.

For example:

GAP — Automatic Human ↔ AI Experience Capture

EXPECTED

Project-owned continuity should automatically preserve relevant conversation experience.

OBSERVED

Current workflow requires manual preservation.

WHY IT MATTERS

Context can still be lost when the external AI session disappears.

EVIDENCE

Current workflow observation.

RELATED PURPOSE

Prevent epistemic dementia.

RELATED RESEARCH

Epistemic Continuity.

A Gap therefore has meaning, provenance, and consequence.

---

## 0.8.139 — Contradiction and Gap Are Different

A Gap means:

something expected is missing, incomplete, or not demonstrated.

A Contradiction means:

two or more relevant statements, observations, or expectations conflict.

Example Gap:

Canon requires X.
X is absent.

Example Contradiction:

Document A says X exists.
Runtime Evidence says X does not function.

The Living Project Image should distinguish these conditions.

They may require different responses.

---

## 0.8.140 — Unknown, Gap, Contradiction, and Failure Are Different

These categories must not be collapsed.

UNKNOWN

We do not currently know whether X exists.

GAP

X is expected but cannot currently be demonstrated as satisfying the expectation.

CONTRADICTION

Relevant sources disagree about X.

FAILURE

An attempted action or capability did not produce the required outcome under observed conditions.

These distinctions are essential for honest project understanding.

They will need representation in CSL Cognitive Grammar.

---

## 0.8.141 — The Living Image Is an Epistemic Instrument

The Living Project Image should therefore be understood not merely as documentation but as an epistemic instrument.

It helps the organism and human:

observe;

orient;

compare;

question;

navigate;

verify;

remember;

detect divergence;

identify uncertainty;

understand change;

continue work.

It is part of the physiology through which the project becomes understandable to itself and to its collaborators.

---

## 0.8.142 — CSL Must Preserve Meaning Before Optimizing Tokens

AI context efficiency matters.

Compact derived representations will be valuable.

However, the canonical or human-facing semantic model must not be impoverished merely to save tokens.

The correct sequence is:

DEFINE TRUE MEANING
    ↓
PRESERVE TRUE MEANING
    ↓
CREATE COMPACT DERIVED REPRESENTATION
    ↓
VERIFY SEMANTIC EQUIVALENCE

not:

REMOVE MEANING
    ↓
CALL THE RESULT EFFICIENT.

Token optimization belongs to derived AI views.

Human and canonical meaning must remain sufficiently rich.

---

## 0.8.143 — Compact AI Views Can Use Opaque Identifiers

The No Naked Identifier Principle applies to human-facing representations.

A compact AI context may legitimately contain structures such as:

TR-0042
MEM-0021
EV-0103

if the AI can resolve those identities correctly and the compression is useful.

This allows:

HUMAN VIEW

TR-0042 — Establish Layered Memory

AI COMPACT VIEW

TR-0042

Both refer to the same entity.

Thus human cognition and machine efficiency do not need to compete.

---

## 0.8.144 — Compression Must Be Reversible by Resolution

If an AI receives:

TR-0042

it should be possible, when necessary, to resolve that identifier back toward:

semantic title;

meaning;

relationships;

history;

Evidence;

authority;

current condition.

Compactness must not create an epistemic dead end.

This is another form of navigability.

---

## 0.8.145 — The Living Image Should Support Different Depths of Reading

A human may read at several depths.

### Depth 1 — Orientation

What is the project?

What is its current condition?

What matters now?

### Depth 2 — Understanding

Why does this organ or capability exist?

How does it relate to the project?

### Depth 3 — Evolution

How did it reach this condition?

Which Transformations matter?

### Depth 4 — Verification

What Evidence supports the statement?

### Depth 5 — Forensic Reconstruction

Show original Experience, technical execution, historical artifacts, and detailed provenance.

The same project reality supports all five depths.

The human chooses how far to travel.

---

## 0.8.146 — Progressive Reading

This creates a human analogue of Progressive Recall.

The system does not overwhelm the reader with maximum detail immediately.

It provides:

ORIENTATION
    ↓
MEANING
    ↓
CONTEXT
    ↓
PROVENANCE
    ↓
FORENSIC DEPTH

as required.

The project becomes readable by layers.

This may become a central characteristic of human-facing CSL.

---

## 0.8.147 — Progressive Reading Principle

### Progressive Reading Principle

Human-facing CSL should permit a reader to begin with concise project meaning and progressively reveal deeper context, history, technical detail, and Evidence according to need without requiring all available complexity to be consumed at once.

This principle connects CSL directly to Layered Epistemic Memory.

---

## 0.8.148 — CSL Reading Legend Should Support Progressive Reading

The CSL legend itself may eventually have levels.

A newcomer may initially need:

Need;

Decision;

Transformation;

Evidence;

Memory;

Unknown;

Contradiction.

An advanced auditor may need:

authority classes;

relationship semantics;

existence states;

temporal applicability;

provenance markers.

Therefore the reading guide may itself support progressive depth.

Again, the exact implementation is not yet decided.

The principle is:

teach enough to begin;

allow deeper language understanding when required.

---

## 0.8.149 — The Legend Must Be Version-Aware

CSL may evolve through controlled governance.

Therefore a future `.csl` representation should identify which CSL language version it uses.

A legend must correspond to that version.

Otherwise a future reader could apply newer meanings to an older artifact incorrectly.

Conceptually:

CSL LANGUAGE VERSION

1.x

READING GUIDE

derived from CSL 1.x semantics.

PROJECT CONTENT

interpreted under CSL 1.x.

This preserves long-term readability.

---

## 0.8.150 — CSL Evolution Must Preserve Historical Interpretability

If CSL changes in the future, old project history must not become unreadable.

Possible future strategies may include:

versioned parsers;

migration tools;

historical language definitions;

compatibility renderers.

The implementation is not yet chosen.

The epistemic requirement is:

the project must remain capable of understanding its own historical CSL representations.

Otherwise language evolution itself would create epistemic dementia.

---

## 0.8.151 — The Legend Is Part of Human Accessibility, Not Canonical Project Content

The standard CSL reading guide may appear inside a human-facing representation without becoming part of the represented project's own Canon.

This distinction matters.

For example:

CSL READING GUIDE

describes the language.

PROJECT CANON

describes the governed project.

The two may appear in one rendered artifact.

They belong to different semantic layers.

A parser, auditor, or human must be able to distinguish them.

---

## 0.8.152 — Visual Legend

If visual semantics are used, the reading guide should explain them.

Conceptually:

VISUAL READING GUIDE

[visual identity A] — Evolution family

[visual identity B] — Memory family

[visual identity C] — Evidence / Verification family

[visual marker] — Unknown

[visual marker] — Contradiction

[visual marker] — Stale

The exact appearance is future design work.

The important requirement is:

visual semantics must be discoverable rather than mysterious.

---

## 0.8.153 — Human Memory Benefits From Consistency

The user's observation about color reveals a broader cognitive principle.

Humans learn repeated stable associations.

If every encounter with CSL reinforces the same:

terms;

visual families;

relationship names;

identity structure;

navigation patterns;

then the language gradually moves from conscious decoding toward recognition.

This can make large epistemic projects more manageable.

The language becomes part of the human's mental model of the project.

---

## 0.8.154 — CSL Should Reduce the Distance Between Human Thought and Project Structure

The human begins with ideas such as:

"I do not want the project to forget what happened."

The engineering system may internally require:

capture;

storage;

provenance;

identifiers;

relations;

indexes;

renderers;

validation.

CSL should preserve the human meaning while allowing technical resolution.

Conceptually:

HUMAN IDEA

"The project should remember its experience."

        ↓

CSL MEANING

NEED — Preserve Project Experience

        ↓

EPISTEMIC STRUCTURE

related Memory / Transformation / Evidence

        ↓

ENGINEERING REALIZATION

technical implementation

The human can travel downward.

The engineer can travel upward.

The AI can operate across both.

---

## 0.8.155 — CSL as Bidirectional Translation Layer

This suggests CSL may eventually function bidirectionally.

HUMAN → PROJECT

Human expresses purpose, Need, Decision, correction.

CSL helps formalize that meaning.

PROJECT → HUMAN

The organism expresses current state, Evidence, Memory, contradiction, and history.

CSL helps make that meaning intelligible.

Therefore CSL is not merely an input specification language.

It is also an output language of project self-description.

This is a major expansion of its original role.

---

## 0.8.156 — CSL and Implementation Must Remain Connected

If CSL describes:

Capability X — Operational

while implementation reality contradicts it, the language has failed to remain alive.

Therefore future CSL physiology requires connections between semantic statements and observable implementation reality.

The exact mechanism may involve:

scanning;

validation;

tests;

runtime observation;

repository analysis;

Evidence generation.

Those are engineering mechanisms.

The epistemic requirement is:

CSL statements about realized project reality must remain evidence-connected.

---

## 0.8.157 — CSL Is Not the Implementation

CSL should describe and connect to implementation.

It should not pretend to be implementation.

Likewise, implementation does not replace CSL.

Implementation answers:

WHAT IS PHYSICALLY REALIZED?

CSL answers:

WHAT DOES THIS MEAN WITHIN PROJECT REALITY?

HOW DOES IT RELATE TO PURPOSE, CANON, HISTORY, EVIDENCE, AND CURRENT STATE?

This distinction allows code and Canon to become parts of one coherent project image without becoming the same thing.

---

## 0.8.158 — Toward the Complete Project Image

The original intuition:

CODE + CANON = PROJECT IMAGE

can now be expanded conceptually:

CANON
+
REALIZATION
+
CURRENT OBSERVATION
+
EXPERIENCE
+
MEMORY
+
KNOWLEDGE
+
TRANSFORMATIONS
+
EVIDENCE
+
PROVENANCE
+
UNCERTAINTY
+
CONTRADICTIONS
+
PURPOSE
=
LIVING PROJECT IMAGE

This is not a mathematical equation.

It expresses the dimensions that contribute to the complete epistemic picture.

CSL is the candidate language through which that picture becomes intelligible and navigable.

---

## 0.8.159 — The Living Project Image Is Never Absolutely Complete

A critical epistemic limitation must be acknowledged.

No project image can guarantee absolute knowledge of every relevant aspect of reality.

Observation may be incomplete.

Evidence may be missing.

External systems may change.

Historical context may already have been lost.

Human intention may be ambiguous.

Therefore "complete project image" must not mean:

omniscient project image.

It means:

the most complete image justified by currently available and appropriately evaluated evidence.

Unknown areas must remain visible.

---

## 0.8.160 — Completeness Must Be Evidence-Bounded

A project may have:

complete coverage of one organ;

partial coverage of another;

unknown state in a third.

The Living Project Image should therefore understand completeness relative to:

scope;

evidence;

time;

purpose.

The image should never claim absolute completeness merely because all expected fields contain values.

A filled form can still contain false knowledge.

Epistemic completeness is not syntactic completeness.

---

## 0.8.161 — Honest Completeness Principle

### Honest Completeness Principle

The Living Project Image shall prefer explicit incompleteness over unsupported completion.

Unknown, unresolved, stale, absent, and contradictory conditions shall remain representable rather than being replaced with assumptions merely to produce a visually complete image.

This is essential to Reality First.

---

## 0.8.162 — The Living Project Image Must Be Falsifiable

If the image says:

"Capability X is operational."

there must be some possible observation that could demonstrate that statement is no longer true.

If no observation could ever challenge the image, it becomes dogma rather than knowledge.

Therefore important current-state Claims should remain falsifiable where applicable.

This connects Living Project Image physiology to the Canonical Research Axioms.

---

## 0.8.163 — The Image Must Support Correction Loops

Conceptually:

CURRENT IMAGE CLAIM
    ↓
NEW OBSERVATION
    ↓
CONFLICT?
    │
    ├── NO → confidence may remain or strengthen
    │
    └── YES
          ↓
      INVESTIGATE
          ↓
      VERIFY
          ↓
      CORRECT CURRENT IMAGE
          ↓
      PRESERVE HISTORY

This is how the image remains alive without becoming unstable.

---

## 0.8.164 — Correction Is Evolution of Knowledge

When stronger Evidence changes the image, this is not necessarily a failure.

It may represent successful epistemic correction.

The organism learns.

For example:

OLD UNDERSTANDING

Capability X is operational.

NEW EVIDENCE

Capability X fails under condition Y.

NEW UNDERSTANDING

Capability X is operational only under conditions excluding Y.

The image becomes more accurate.

History preserves the evolution.

---
## 0.8.165 — The Living Image Should Support Human Trust Through Inspection

Trust should not require blind faith in AI-Toolkit.

A human should increasingly be able to inspect:

what the organism believes;

why it believes it;

what Evidence exists;

what remains uncertain;

what changed;

what authority applies.

The system earns trust through inspectability.

This is especially important because AI participates in interpretation.

---

## 0.8.166 — Explainability Must Be Native

Explainability should not be an emergency feature added only after something goes wrong.

The Living Project Image should be structured so that important statements naturally possess:

meaning;

source;

relationships;

Evidence;

history;

authority;

epistemic condition.

Then explanation becomes a normal traversal of project structure.

The system does not need to invent an explanation after the fact.

It follows existing provenance.

---

## 0.8.167 — The Living Project Image Is Not Merely for AI-Toolkit

Although this research is being conducted inside AI-Toolkit, the objective is broader.

AI-Toolkit should eventually help external projects produce their own Living Project Images.

For example:

Trading Signals Platform

could possess a Living Project Image describing:

purpose;

trading capabilities;

data sources;

strategies;

risk controls;

current deployment;

known failures;

verification;

operational gaps;

recent Transformations.

DROPi could possess a different project image.

The semantic language remains CSL.

Project-specific reality changes.

This is another reason stable CSL semantics matter.

---

## 0.8.168 — AI-Toolkit Must First Learn on Itself

AI-Toolkit is an appropriate first subject because the organism can test its own epistemic mechanisms on its own development.

It can attempt to preserve:

its own research;

its own Transformations;

its own Evidence;

its own Memory;

its own Living Project Image.

Weaknesses discovered through self-application can then improve the mechanisms before they are relied upon heavily for external projects.

This creates a self-improving engineering loop without granting uncontrolled self-authority.

---

## 0.8.169 — Self-Application Loop

Conceptually:

AI-TOOLKIT RESEARCH
        ↓
NEW EPISTEMIC CAPABILITY
        ↓
APPLY CAPABILITY TO AI-TOOLKIT
        ↓
OBSERVE WEAKNESSES
        ↓
EVIDENCE
        ↓
RESEARCH / CORRECTION
        ↓
IMPROVED CAPABILITY
        ↓
REAPPLY

The organism becomes a test subject for its own epistemic physiology.

This is consistent with the requirement that every implementation should improve AI-Toolkit's ability to build, maintain, audit, validate, and evolve itself.

---

## 0.8.170 — Research Must Not Block Useful Production Indefinitely

Self-improvement can become an endless research loop if not bounded by practical purpose.

The human also needs AI-Toolkit to help with real projects.

Therefore the Living Project Image should eventually make visible:

WHAT IS USABLE NOW?

WHAT REQUIRES MANUAL SUPPORT?

WHAT IS RESEARCH ONLY?

WHAT IS SAFE TO APPLY TO AN EXTERNAL PROJECT?

WHAT IS NOT READY?

This allows practical use to begin without falsely claiming that the full Epistemic Organism already exists.

---

## 0.8.171 — Production and Research Can Proceed in Parallel

The project does not necessarily need to choose between:

finish all epistemic research first;

or:

abandon research and use only the old system.

A Living Project Image can help support a third path:

USE VERIFIED EXISTING CAPABILITY

while:

CONTINUING RESEARCH

and:

MIGRATING CAPABILITY WHEN READY.

This requires accurate generational and capability state representation.

The project must know which organism functions are mature enough to use.

---

## 0.8.172 — The Living Project Image Can Become the Migration Map

When AI-Toolkit begins supporting the Trading project, the image may help answer:

Which current AI-Toolkit capabilities are already operational?

Which require manual Termux support?

Which depend on older generations?

Which newer epistemic functions can be introduced safely?

Which capabilities are research-only?

What must be preserved during migration?

This makes the Living Project Image useful not only epistemically but operationally.

---

## 0.8.173 — Living Project Image Physiology Summary

The research now supports the following physiological model.

The Living Project Image:

represents the best-supported current project reality;

distinguishes expected reality from observed reality;

distinguishes Canon from current realization;

represents existence, absence, unknown, contradiction, and staleness;

remains connected to project history;

preserves navigable provenance;

supports human, engineering, audit, and AI views;

uses human-readable identities;

supports progressive reading;

may use stable visual semantics;

must remain meaningful without visual styling;

teaches humans how to begin reading CSL;

supports context generation;

supports project handover;

supports self-inspection;

supports correction;

supports historical reconstruction;

supports generational awareness;

supports practical capability discovery;

and remains bounded by Evidence and human authority.

It is not:

a static status report;

a manually maintained dashboard;

a replacement for Canon;

a replacement for implementation;

a replacement for Memory;

a replacement for Evidence;

an AI-generated narrative detached from proof.

It is the present-facing epistemic map through which those realities become understandable together.

---

## 0.8.174 — Principles Established or Strengthened in Section 0.8

The following principles are established or strengthened as research conclusions within this section.

### Single Reality, Multiple Views Principle

One epistemic project reality may produce multiple human, engineering, audit, and AI representations without creating competing truths.

### Human Comprehension Principle

Human-facing epistemic representations should communicate project meaning without unnecessary dependence on internal software terminology.

### Human-Readable Identity Principle

Every epistemically significant entity should possess stable machine identity and concise human-readable semantic identity.

### No Naked Identifier Principle

Human-facing representations should not expose an identifier alone when its semantic title is known.

### Navigable Reality Principle

Humans should be able to travel from high-level meaning toward deeper history, authority, implementation, and Evidence.

### Self-Teaching Representation Principle

Human-facing CSL should provide sufficient language guidance for an unfamiliar person to begin reading it.

### Progressive Familiarity Principle

Repeated exposure to stable CSL semantics and visual conventions should progressively reduce cognitive effort.

### Semantic Redundancy Principle

No epistemic meaning should depend exclusively upon color or another visual property.

### Visual Semantics Principle

Stable visual identities may improve human recognition provided semantic meaning remains explicit and presentation-independent.

### Evidence-Bounded Representation Principle

The Living Project Image must not claim a stronger epistemic state than available Evidence supports.

### Cognitive Compression Principle

Human representations may compress complexity while preserving faithful meaning and navigable access to deeper truth.

### Regenerable View Principle

Derived views should remain regenerable from preserved authoritative epistemic sources where practical.

### Context Fidelity Principle

Context compression must not remove material information in a manner that changes meaning, authority, uncertainty, or epistemic condition.

### Progressive Reading Principle

Human-facing CSL should allow movement from orientation toward deeper context, provenance, and forensic Evidence according to need.

### Honest Completeness Principle

Explicit incompleteness is preferable to unsupported completion.

These remain research conclusions until reconciled and promoted through the appropriate governance process.

---

## 0.8.175 — Research Boundary: What Has Not Yet Been Decided

Section 0.8 does not establish the final technical design of CSL.

The following remain unresolved:

- final CSL syntax;
- final file structure;
- exact `.csl` serialization;
- parser architecture;
- editor architecture;
- renderer architecture;
- exact semantic colors;
- exact icons or visual markers;
- final semantic taxonomy;
- final relationship vocabulary;
- final existence-state model;
- final authority-state model;
- final confidence model;
- exact link representation;
- exact semantic addressing mechanism;
- exact historical reconstruction mechanism;
- exact Living Project Image generation mechanism;
- exact invalidation and staleness rules;
- exact relationship between existing CSL generations and the future model.

These must not be invented merely to make the research appear complete.

They form part of the next research frontier.

---

## 0.8.176 — Research Boundary: What Is Now Strongly Established

Although implementation details remain open, the research has established a strong direction.

CSL must be:

human-readable;

machine-resolvable;

self-teaching at the human-facing level;

semantically stable;

evidence-connected;

navigable;

authority-aware;

uncertainty-aware;

historically interpretable;

capable of supporting visual semantics;

independent of visual styling for meaning;

capable of compact derived AI representations;

and suitable for expressing the Living Project Image.

The Living Project Image must represent:

Canon;

current realized reality;

Experience;

Memory;

Knowledge;

Transformations;

Evidence;

uncertainty;

contradictions;

gaps;

purpose;

history;

and current direction

without collapsing these dimensions into one another.

---

## 0.8.177 — Central Living Project Image Conclusion

The Living Project Image is not simply a description of the project.

It is the project's evidence-bounded, navigable, present-facing self-representation.

It should allow a human or AI to understand:

what the project is;

why it exists;

what it should be;

what it actually is;

what it knows;

what it remembers;

what it cannot establish;

where it contradicts itself;

how it arrived here;

and where the Evidence is.

The image must evolve when reality evolves.

It must preserve history without presenting history as current truth.

It must preserve uncertainty without filling gaps through assumption.

It must remain connected to Canon without becoming Canon.

It must remain connected to implementation without becoming implementation.

It must remain connected to Memory without becoming the complete archive.

It is the map through which the organism understands and communicates its current reality.

---

## 0.8.178 — Central CSL Conclusion

The research also supports a stronger understanding of CSL.

CSL is not merely a language for writing specifications.

CSL is the candidate common epistemic language through which:

the human expresses meaning;

AI interprets and assists;

Canon expresses governed truth;

the organism expresses current reality;

Memory remains navigable;

Transformations preserve evolution;

Evidence remains reachable;

and derived machine representations remain resolvable.

Human-facing CSL should teach itself progressively.

A newcomer should be able to open a CSL representation, read its legend, recognize its semantic categories, understand human-readable identities, follow meaningful relationships, and travel toward deeper Evidence.

Over time, stable terminology and visual semantics should make CSL increasingly natural to read.

In this sense:

CSL is not merely a format.

It is intended to become the readable language of the epistemic organism.

---

## 0.8.179 — Transition to CSL Cognitive Grammar

The physiological role of the Living Project Image is now sufficiently developed to expose the next research problem.

Before defining how a `.csl` file is technically written, the project must determine the cognitive grammar of the language.

The next questions are:

What are the fundamental semantic families of CSL?

What kinds of epistemic entities must a human recognize?

Which concepts describe project evolution?

Which describe truth and Evidence?

Which describe Memory?

Which describe anatomy?

Which describe authority?

Which describe epistemic condition?

Which describe temporal state?

Which describe existence?

Which relationships are fundamental?

How should category, state, authority, and Evidence remain distinguishable?

What should a human be able to understand before seeing any technical syntax?

How should the standardized CSL legend explain these concepts?

How can the same grammar support both human-rich and AI-compact representations?

Only after these questions are answered should final syntax be designed.

This leads directly to:

# 0.9 — CSL Cognitive Grammar
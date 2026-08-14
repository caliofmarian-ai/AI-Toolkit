# PCC-03 — Provenance + Lineage

## RUN 003 — Bidirectional Provenance Navigation

Status: IMPLEMENTED — NOT CANON

Canonical Basis:

- `canon/EPISTEMIC_CONTINUITY_STRUCTURE_MAP.md`
- Canon SHA-256: `ba855d8d0196fa007a7e5e55eaac3da453538030ae6f3337f801aad127203d36`
- PCC-03 RUN 001 — Provenance Anatomy
- PCC-03 RUN 002 — Persistent Provenance Identity + Recovery
- PCC-02 — authoritative Transformation temporal/causal lineage

---

## 1. Why? — Need

RUN 001 established the provenance anatomy.

RUN 002 allowed that anatomy to survive process restart.

The organism still required explicit traversal through those relationships.

Stored provenance that cannot be followed in both directions does not yet
satisfy the Canonical Bidirectional Provenance principle.

---

## 2. What did we research? — Research

The governing Canon states:

Provenance must be traversable in both directions.

The Canon additionally requires relationships to be explicit, traceable, and
verifiable and prohibits deriving epistemic relationships merely from filename,
proximity, naming similarity, or AI assumption.

The existing implementation was inspected before mutation.

It already possessed:

- Source;
- Observation;
- Evidence;
- Claim;
- Verification;
- explicit EvidenceRelation;
- supporting Evidence navigation;
- contradicting Evidence navigation;
- persistence;
- reconstruction.

Therefore no new graph or lineage organ was required.

---

## 3. What did we believe before execution? — Hypothesis

The existing Provenance organ can become bidirectionally navigable by exposing
the relations it already owns, without creating another graph, persistence
authority, or inferred relationship system.

---

## 4. What did the human authority decide? — Owner Decision

The Owner explicitly authorized continuation after audit, with the requirement
that Canon and existing code be inspected first and that no errors, duplicate
organs, or contradictory implementations be introduced.

---

## 5. What did we intend to change? — Implementation

Mature the existing `Provenance` organ with navigation for:

Source
↔ Observation
↔ Evidence
↔ Claim
↔ Verification

Add whole-path traversal:

Verification
→ Claim
→ Evidence
→ Observation
→ Source

and:

Source
→ Observation
→ Evidence
→ Claim
→ Verification

Do not implement Knowledge.

Do not implement Current State.

Do not duplicate PCC-02 Transformation lineage.

Do not create ProvenanceGraph or LineageGraph.

---

## 6. What was actually executed? — Execution

The run:

1. verified exact Git authority;
2. verified governing Canon;
3. verified RUN 001 and RUN 002 anatomy;
4. verified the mutation boundary;
5. matured the existing Provenance organ;
6. extended behavioral examination;
7. executed dedicated PCC-03 tests;
8. executed inherited epistemic and Experience regression;
9. examined the epistemic package for duplicate/premature organs;
10. conserved this Epic Thread;
11. admitted only the exact intended mutation to Git.

---

## 7. What actually changed? — Artifacts / Effects

Modified:

- `lib/python/epistemic/provenance.py`
- `tests/epistemic/test_provenance.py`

Created:

- `work/implementation-reports/PCC-03/PCC-03_RUN003_BIDIRECTIONAL_PROVENANCE_NAVIGATION_EPIC_THREAD.md`

New navigation includes:

- Observation → Source;
- Source → Observations;
- Evidence → Observation;
- Observation → Evidence;
- Evidence → Claims;
- Claim → Evidence;
- Claim → Verifications;
- Verification → Claim;
- complete backward provenance traversal;
- complete forward provenance traversal through the currently implemented
  PCC-03 anatomy.

---

## 8. What evidence do we have? — Evidence

The run requires passing evidence for:

- every explicit edge in both directions;
- contradiction visibility;
- absence of inferred Evidence→Claim relations;
- forward whole-path traversal;
- backward whole-path traversal;
- traversal after persistence/recovery;
- rejection of foreign/unregistered entities;
- rejection of invalid relation roles;
- inherited PCC-03 behavior;
- inherited epistemic and Experience behavior;
- absence of duplicate graph organs.

---

## 9. Did it work? — Verification

Successful completion establishes bidirectional traversal across the executable
PCC-03 anatomy currently implemented.

It does NOT establish Knowledge or Current State.

Those concepts remain explicit later boundaries.

Navigation follows explicit relations only.

No relationship is created merely because two entities appear related.

---

## 10. What did we learn? — Knowledge

Bidirectional provenance does not require a second graph when the underlying
epistemic relationships already exist explicitly.

The correct evolution is to make those existing relations navigable.

Contradiction remains part of provenance and therefore remains visible during
navigation.

Persistence and navigation must agree: a provenance path that exists before
restart must remain navigable after reconstruction.

---

## 11. How did the organism or project evolve? — Evolution

Before RUN 003:

the organism could preserve provenance but navigation was partial.

After RUN 003:

the organism can travel explicitly:

Source
→ Observation
→ Evidence
→ Claim
→ Verification

and backward:

Verification
→ Claim
→ Evidence
→ Observation
→ Source.

This makes the currently implemented provenance history explorable without
creating another epistemic authority.

---

## 12. Where does the story continue? — Epic Thread / Next Transformation

PCC-03 RUN 001
→ Provenance Anatomy

PCC-03 RUN 002
→ Persistent Provenance Identity + Recovery

PCC-03 RUN 003
→ Bidirectional Provenance Navigation

The next boundary is NOT declared blindly.

After this commit GPT must inspect:

- the resulting Git state;
- this Epic Thread;
- governing Canon;
- remaining PCC-03 provenance requirements;
- existing epistemic organs.

Only then may RUN 004 be derived.

PCC-03:

IMPLEMENTATION IN PROGRESS

Production-ready:

NO

Canonical:

NO

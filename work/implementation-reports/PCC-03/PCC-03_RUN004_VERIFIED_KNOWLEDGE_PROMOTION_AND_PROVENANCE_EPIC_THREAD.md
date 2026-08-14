# PCC-03 — Provenance + Lineage

## RUN 004 — Verified Knowledge Promotion + Provenance

Status: IMPLEMENTED — NOT CANON

Canonical Basis:

- `canon/EPISTEMIC_CONTINUITY_STRUCTURE_MAP.md`
- Canon SHA-256: `ba855d8d0196fa007a7e5e55eaac3da453538030ae6f3337f801aad127203d36`
- PCC-03 RUN 001 — Provenance Anatomy
- PCC-03 RUN 002 — Persistent Provenance Identity + Recovery
- PCC-03 RUN 003 — Bidirectional Provenance Navigation

---

## 1. Why? — Need

The organism could preserve and navigate:

Source
→ Observation
→ Evidence
→ Claim
→ Verification

but the governing epistemic anatomy continues from Verification toward
Knowledge.

Verification and Knowledge must remain distinct.

Evidence must not silently become Knowledge.

---

## 2. What did we research? — Research

Before implementation the repository was inspected for existing Knowledge and
Memory organs.

Existing structures include:

- `lib/python/knowledge_engine/engine.py`
- `lib/python/knowledge_engine/models.py`
- `lib/python/knowledge_materialization/engine.py`
- `lib/python/epistemic/memory.py`
- `lib/python/epistemic/memory/model.py`
- `lib/python/epistemic/memory/store.py`

Those organs already have separate responsibilities.

RUN 004 therefore did not create another Knowledge Engine, Knowledge Graph,
Memory Store, Evidence Engine, Verification Engine, provenance graph, or
lineage organ.

---

## 3. What did we believe? — Hypothesis

The smallest safe maturation was an explicit epistemic promotion boundary:

Verification
→ Knowledge

while retaining the preceding PCC-03 provenance anatomy as the historical
authority.

---

## 4. What did Human Authority decide? — Owner Decision

Human Authority explicitly authorized continuation under Canon with strict
requirements:

- inspect Canon first;
- inspect existing code first;
- do not create duplicates;
- do not invent epistemic state;
- preserve the complete Epic Thread for every run.

---

## 5. What did we implement? — Implementation

RUN 004 adds a bounded immutable `Knowledge` value and an explicit
`promote_verified_knowledge(...)` boundary.

Knowledge preserves:

- stable `KN-*` identity;
- human-readable title;
- explicit semantic statement;
- originating Verification identity;
- explicit authority;
- explicit established status.

Promotion requires an actual Verification object.

Promotion requires explicit semantic information.

Promotion requires explicit authority.

---

## 6. What happened during execution? — Execution

The first RUN 004 examination exposed a test-harness defect before commit:

the newly appended tests referenced `Verification` and `Evidence` without
importing them into the test module.

The implementation itself had compiled.

The safety boundary worked:

- tests failed;
- execution stopped;
- no commit occurred;
- no push occurred;
- Git authority remained at the pre-RUN004 commit.

The repair then inspected the exact inherited Verification dataclass:

- identifier
- title
- claim
- state
- basis

The test harness was repaired to import the real inherited classes explicitly.

The reflective constructor guess was removed.

The repaired examination then executed the dedicated PCC-03 suite and inherited
epistemic/Experience regression.

---

## 7. What changed? — Artifacts / Effects

Modified:

- `lib/python/epistemic/provenance.py`
- `tests/epistemic/test_provenance.py`

Created:

- `work/implementation-reports/PCC-03/PCC-03_RUN004_VERIFIED_KNOWLEDGE_PROMOTION_AND_PROVENANCE_EPIC_THREAD.md`

No existing Knowledge or Memory organ was modified.

---

## 8. What evidence do we have? — Evidence

The run examines that:

- non-Verification objects cannot be promoted;
- authority cannot be absent;
- semantic statement cannot be absent;
- Knowledge has its own identity;
- originating Verification identity remains explicit;
- Knowledge remains immutable;
- Knowledge remains distinct from Evidence;
- Knowledge remains distinct from Verification;
- Current State is not claimed;
- Living Project Image is not claimed;
- Memory is not claimed;
- inherited epistemic behavior remains intact.

The failed first examination is also preserved as causal evidence in this Epic
Thread rather than erased from project history.

---

## 9. Did it work? — Verification

Successful completion means:

Verification → Knowledge is executable as an explicit governed promotion.

It does not mean every Verification automatically becomes Knowledge.

It does not mean AI may promote information autonomously.

It does not establish Current State or Living Project Image.

---

## 10. What did we learn? — Knowledge

The implementation boundary and the test boundary are both part of epistemic
integrity.

A correct conceptual implementation is not sufficient when the examination
harness itself does not reference the inherited anatomy correctly.

The failed examination therefore became useful evidence and was preserved
rather than hidden.

---

## 11. How did the organism evolve? — Evolution

Before RUN 004:

Source
→ Observation
→ Evidence
→ Claim
→ Verification

After RUN 004:

Source
→ Observation
→ Evidence
→ Claim
→ Verification
→ Knowledge

Knowledge remains explicitly linked to its originating Verification.

Existing Knowledge Engines and Memory organs remain separate.

---

## 12. Where does the story continue? — Epic Thread / Next Transformation

RUN 001
→ Provenance Anatomy

RUN 002
→ Persistent Provenance Identity + Recovery

RUN 003
→ Bidirectional Provenance Navigation

RUN 004
→ Verified Knowledge Promotion + Provenance

The exact RUN 005 boundary is NOT declared from assumption.

GPT must inspect:

- the committed RUN 004 implementation;
- this Epic Thread;
- governing Canon;
- existing Knowledge/Memory organs;
- remaining PCC-03 requirements.

Only then may RUN 005 be derived.

PCC-03:

IMPLEMENTATION IN PROGRESS

Production-ready:

NO

Canonical:

NO

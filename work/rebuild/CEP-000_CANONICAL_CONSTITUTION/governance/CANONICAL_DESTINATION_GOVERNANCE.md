# CANONICAL DESTINATION GOVERNANCE

## Purpose

This document defines the boundary of the authoritative canonical destination.

The authoritative repository destination is:

`canon/`

The existence of this directory does not itself create Canon.

---

# 1. Canonical Boundary

`canon/` is reserved for artifacts that have completed legitimate Canonical Admission.

Research, candidates, implementation reports, test output, AI drafts, temporary artifacts, and unaccepted proposals must remain outside the authoritative canonical body.

---

# 2. Presence Does Not Equal Authority

A file does not become CANON merely because it exists under `canon/`.

Canonical Authority requires:

- an admitted canonical identity;
- successful admission evidence;
- explicit Human Authority;
- and a traceable resulting CANON state.

An unauthorized file found under `canon/` is a boundary violation, not Canon.

---

# 3. Required Canonical Artifact Metadata

Every admitted canonical artifact must make traceable, directly or through an associated canonical manifest:

- Canonical ID;
- Canonical title;
- Canonical state;
- Human Authority;
- admission evidence;
- source candidate;
- admission Git identity;
- and version/history relationship when applicable.

---

# 4. Admission Evidence Boundary

Admission evidence is not automatically Canon.

Implementation reports and admission reports remain evidence of governance.

They must not be confused with the canonical artifact they justify.

The canonical artifact must remain distinguishable from its evidence.

---

# 5. Mutation Protection

Existing CANON must not be silently overwritten.

A proposed change to existing Canon must enter governed review and produce a new admission decision.

Historical canonical states must remain traceable.

---

# 6. Unauthorized Mutation

The following do not grant Canonical Authority:

- manual copying;
- automated copying;
- file creation;
- Git staging;
- Git commit;
- Git merge;
- deployment;
- test success;
- AI generation.

When such an action places non-admitted material in `canon/`, the organism must treat the condition as a governance violation.

---

# 7. Bootstrap State

At materialization of this destination, no canonical candidate has yet completed formal Canonical Admission under the new mechanism.

Therefore the initial `canon/` destination contains governance information only and must not be interpreted as containing admitted Canon.

CEP-000 remains an ACCEPTED CANDIDATE until its separate admission proceeding succeeds and Human Authority explicitly admits it.

PCC-01 remains IMPLEMENTED + PRODUCTION-READY + NOT CANON until its separate admission proceeding succeeds.

---

# END OF CANONICAL DESTINATION GOVERNANCE

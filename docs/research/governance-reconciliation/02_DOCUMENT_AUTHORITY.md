# 02 — Document Authority

Version: 1.0.0-draft

Status: Draft — Pending Human Review and Approval

Classification: Canonical Research Document

Package: docs/research/governance-reconciliation/

---

## 1. Purpose

This document defines the authority level, normative status and classification
of every governance document, derived from repository evidence.

---

## 2. Highest Authority Document

**Verified Fact:** `governance/PROJECT_CONSTITUTION.md` is the highest authority
governance document. This is established by its own text in Article I:
> "This Constitution is the highest governance document of the AI-Toolkit project.
> No canonical specification may contradict this document.
> In case of conflict, this Constitution prevails."

**Verified Fact:** The same document, Article II, establishes that canonical
specifications are authoritative over source code:
> "Canonical specifications constitute the authoritative definition of the system.
> Source code is an implementation of canonical specifications.
> Documentation is not descriptive; it is normative."

---

## 3. Normative Documents

**Architectural Conclusion:** Based on repository evidence, the following documents
are Normative (they define rules, constraints or obligations that must be followed):

| Document | Normative Scope | Evidence |
|----------|----------------|---------|
| PROJECT_CONSTITUTION.md | All canonical specifications | Explicit self-declaration, Article I |
| GOVERNANCE_MODEL.md | All governance activity | "establishes... framework for engineering decision making" |
| ENGINEERING_PRINCIPLES.md | All engineering artifacts | "mandatory and apply regardless of programming language" |
| ARCHITECTURE_PRINCIPLES.md | All architectural work | "governing every canonical model, standard, platform" |
| DECISION_PROCESS.md | All engineering decisions | "No engineering decision shall bypass this lifecycle" |
| STANDARDIZATION_PROCESS.md | All canonical standards | "applies to every canonical standard" |
| QUALITY_POLICY.md | Quality standards | Intent is normative (file is currently empty) |
| SECURITY_POLICY.md | Security standards | Intent is normative (file is currently empty) |
| RELEASE_POLICY.md | Release process | Intent is normative (file is currently empty) |

**Note on empty normative documents:** The empty policy documents (QUALITY_POLICY,
SECURITY_POLICY, RELEASE_POLICY) are classified as normative by intent and architectural
position, but are currently inoperative because they contain no content.

---

## 4. Informative Documents

**Architectural Conclusion:** The following documents are Informative (they explain,
motivate or describe, but do not impose rules):

| Document | Informative Scope | Evidence |
|----------|------------------|---------|
| PROJECT_MANIFESTO.md | Motivation and rationale | Explains "Why AI-Toolkit Exists" |
| PROJECT_PHILOSOPHY.md | Engineering worldview | Describes beliefs, not rules |
| PROJECT_IDENTITY.md | Project description | Describes what AI-Toolkit is |

**Engineering Inference:** The boundary between normative and informative is not
explicitly defined by any governance document. This classification is derived by
analyzing document content and purpose. A human authority should confirm this
classification when authoring PROJECT_GLOSSARY.md.

---

## 5. Planning Documents (Neither Normative nor Informative)

**Architectural Conclusion:** The following documents are Planning Documents —
they define scope, objectives, trajectory and context. They are canonical artifacts
but neither normative nor informative in the standard sense:

| Document | Planning Scope | Status |
|----------|---------------|--------|
| PROJECT_VALUES.md | Value system | Empty |
| PROJECT_OBJECTIVES.md | Measurable objectives | Empty |
| PROJECT_SCOPE.md | Scope boundaries | Empty |
| PROJECT_SUCCESS_CRITERIA.md | Success definition | Empty |
| LONG_TERM_VISION.md | Multi-year vision | Empty |
| PROJECT_ROADMAP.md | Execution roadmap | Empty |
| PROJECT_LIFECYCLE.md | Project lifecycle stages | Empty |
| PROJECT_STAKEHOLDERS.md | Stakeholder definitions | Empty |
| PROJECT_RISK_MODEL.md | Risk framework | Empty |
| ECOSYSTEM_PRINCIPLES.md | Ecosystem-level principles | Empty |

---

## 6. Reference Documents

| Document | Reference Scope | Status |
|----------|----------------|--------|
| PROJECT_GLOSSARY.md | Canonical terminology | Empty |

**Engineering Inference:** PROJECT_GLOSSARY.md, once authored, will function as a
normative reference document. It defines terminology that governs interpretation of
all other governance documents.

---

## 7. Complete Authority Classification Table

| Document | Authority Tier | Type | Has Content |
|----------|---------------|------|-------------|
| PROJECT_CONSTITUTION.md | 1 (Highest) | Normative | Yes |
| PROJECT_IDENTITY.md | 2 | Informative | Yes |
| PROJECT_MANIFESTO.md | 2 | Informative | Yes |
| PROJECT_PHILOSOPHY.md | 2 | Informative | Yes |
| GOVERNANCE_MODEL.md | 3 | Normative | Yes |
| DECISION_PROCESS.md | 3 | Normative | Yes |
| STANDARDIZATION_PROCESS.md | 3 | Normative | Yes |
| ENGINEERING_PRINCIPLES.md | 4 | Normative | Yes |
| ARCHITECTURE_PRINCIPLES.md | 4 | Normative | Yes |
| ECOSYSTEM_PRINCIPLES.md | 4 | Normative | **Empty** |
| QUALITY_POLICY.md | 5 | Normative | **Empty** |
| SECURITY_POLICY.md | 5 | Normative | **Empty** |
| RELEASE_POLICY.md | 5 | Normative | **Empty** |
| PROJECT_VALUES.md | 6 | Planning | **Empty** |
| PROJECT_OBJECTIVES.md | 6 | Planning | **Empty** |
| PROJECT_SCOPE.md | 6 | Planning | **Empty** |
| PROJECT_SUCCESS_CRITERIA.md | 6 | Planning | **Empty** |
| LONG_TERM_VISION.md | 6 | Planning | **Empty** |
| PROJECT_ROADMAP.md | 6 | Planning | **Empty** |
| PROJECT_LIFECYCLE.md | 6 | Planning | **Empty** |
| PROJECT_STAKEHOLDERS.md | 6 | Planning | **Empty** |
| PROJECT_RISK_MODEL.md | 6 | Planning | **Empty** |
| PROJECT_GLOSSARY.md | Cross-cutting | Reference | **Empty** |

---

## 8. Document Derivation Relationships

**Architectural Conclusion:** Based on content analysis, the following derivation
relationships exist:

`PROJECT_PHILOSOPHY.md` derives from `PROJECT_MANIFESTO.md`
— Both address motivation, but Philosophy provides the intellectual foundation
  that Manifesto communicates publicly.

`ENGINEERING_PRINCIPLES.md` realizes `PROJECT_PHILOSOPHY.md`
— Philosophy declares that engineering is a knowledge discipline;
  Engineering Principles operationalize that belief as concrete rules.

`ARCHITECTURE_PRINCIPLES.md` realizes `ENGINEERING_PRINCIPLES.md`
— Architecture Principles are the architectural application of Engineering Principles.

`GOVERNANCE_MODEL.md` implements `PROJECT_CONSTITUTION.md`
— The Constitution defines authority; the Governance Model defines how that
  authority is exercised.

`DECISION_PROCESS.md` implements `GOVERNANCE_MODEL.md`
— The Governance Model states that decisions follow a workflow;
  the Decision Process defines that workflow in detail.

`STANDARDIZATION_PROCESS.md` implements `GOVERNANCE_MODEL.md`
— The Governance Model states that standards evolve through governance;
  the Standardization Process defines that evolution in detail.

---

## 9. Documents That Reference Each Other

**Engineering Inference:** None of the 23 governance documents contain explicit
cross-reference links (hyperlinks or document IDs) to other governance documents.

**Architectural Conclusion:** The dependency relationships are implied by content
and positional authority, not by formal cross-references. This absence of formal
cross-referencing is itself a governance gap (see `08_GAPS_AND_MISSING_RELATIONSHIPS.md`).

---

## 10. Conflicting Authority Claims

**Verified Fact:** No document in the governance layer explicitly contradicts
another document's authority claim.

**Verified Fact:** The `PROJECT_CONSTITUTION.md` is the only document that explicitly
declares its own authority. No other governance document makes an explicit authority claim.

**Architectural Conclusion:** The absence of explicit authority declarations in
non-constitutional documents is consistent with the hierarchical model: lower-tier
documents derive authority from the Constitution without needing to declare it.

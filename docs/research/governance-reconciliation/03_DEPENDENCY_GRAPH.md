# 03 — Dependency Graph

Version: 1.1.0-draft

Status: Draft — Pending Human Review and Approval

Classification: Canonical Research Document

Package: docs/research/governance-reconciliation/

---

## 1. Purpose

This document constructs the official Governance Dependency Graph derived from
repository evidence.

---

## 2. Evidence Source for Dependency Graph

The `architecture/audit/GOVERNANCE_FOUNDATION_AUDIT.md` contains the following
explicit dependency definition:

**Repository Evidence:**
> "PROJECT_IDENTITY
> ↓
> PROJECT_CONSTITUTION
> ↓
> PROJECT_MANIFESTO
> ↓
> PROJECT_PHILOSOPHY
> ↓
> ENGINEERING_PRINCIPLES
> ↓
> ARCHITECTURE_PRINCIPLES
> ↓
> GOVERNANCE_MODEL
> ↓
> DECISION_PROCESS
> ↓
> STANDARDIZATION_PROCESS
>
> The dependency flow is acyclic."

*Source: `architecture/audit/GOVERNANCE_FOUNDATION_AUDIT.md`, section "Dependency Validation"*

**Verified Fact:** The Governance Foundation Audit explicitly verified this dependency
flow is acyclic.

---

## 3. Extended Governance Dependency Graph

**Governance Conclusion:** Extending the Foundation Audit's dependency chain with
the remaining governance documents and connecting governance to the standards layer:

```
PROJECT_CONSTITUTION (Tier 1 — Highest Authority)
  │
  ├─► PROJECT_IDENTITY
  │     └─► (Informative: defines what AI-Toolkit is)
  │
  ├─► PROJECT_MANIFESTO
  │     └─► (Informative: defines why AI-Toolkit exists)
  │
  ├─► PROJECT_PHILOSOPHY
  │     └─► (Informative: defines engineering worldview)
  │
  ├─► GOVERNANCE_MODEL
  │     ├─► DECISION_PROCESS
  │     └─► STANDARDIZATION_PROCESS
  │
  ├─► ENGINEERING_PRINCIPLES
  │     └─► ARCHITECTURE_PRINCIPLES
  │              └─► ECOSYSTEM_PRINCIPLES (empty)
  │
  └─► Policies (Tier 5)
        ├─► QUALITY_POLICY (empty)
        ├─► SECURITY_POLICY (empty)
        └─► RELEASE_POLICY (empty)
              │
              └─► Planning Documents (Tier 6, all empty)
                    ├─► PROJECT_VALUES
                    ├─► PROJECT_OBJECTIVES
                    ├─► PROJECT_SCOPE
                    ├─► PROJECT_SUCCESS_CRITERIA
                    ├─► LONG_TERM_VISION
                    ├─► PROJECT_ROADMAP
                    ├─► PROJECT_LIFECYCLE
                    ├─► PROJECT_STAKEHOLDERS
                    └─► PROJECT_RISK_MODEL
                          │
                          └─► Canonical Standards (Tier 7)
                                ├─► standards/css/ (Canonical Specification Standard)
                                ├─► standards/cdm/ (Canonical Document Model)
                                └─► standards/csl/ (Canonical Specification Language)
                                          │
                                          └─► Architecture Layer
                                                ├─► architecture/reference/
                                                └─► architecture/adr/
                                                        │
                                                        └─► Implementation Layer
                                                              ├─► Engineering Engines
                                                              ├─► Runtime
                                                              ├─► Dashboard
                                                              └─► AI Platform
```

**Cross-cutting:**
```
PROJECT_GLOSSARY (Cross-cutting — defines terminology for all layers)
```

---

## 4. Governance-to-Standards Dependency

**Governance Conclusion:** Based on `STANDARDIZATION_PROCESS.md` and `GOVERNANCE_MODEL.md`:

```
Governance Layer (governance/)
  ↓ governs creation of
CSS (Canonical Specification Standard)
  ↓ governs authoring of
CDM (Canonical Document Model)
CSL (Canonical Specification Language)
  ↓ govern structure of
Canonical Knowledge (knowledge/)
  ↓ consumed by
Knowledge Engine
  ↓ feeds into
Compiler
  ↓ feeds into
Validator
  ↓ feeds into
Runtime
  ↓ surfaces through
Dashboard / AI Platform
```

**Evidence for CSS governing CDM and CSL:**

**Repository Evidence** from `standards/css/CURRENT.md`:
> "Purpose: Defines how canonical standards are authored, structured, validated and
> evolved. This standard governs every specification family including CDM, CSL, CANON
> and future standards."

**Evidence for CDM governing document structure:**

**Repository Evidence** from `standards/cdm/CDM-000_DOCUMENT_MODEL.md` (by title
and filename — the CDM models canonical document structure).

**Evidence for CSL governing knowledge:**

**Repository Evidence** from `knowledge/README.md`:
> "Contents shall be in CSL format. Contents shall be the authoritative source for
> engineering knowledge."

---

## 5. ADR Dependency Graph

**Verified Fact:** Three Architecture Decision Records exist in `architecture/adr/`:
- ADR-0001: ECOSYSTEM_STRUCTURE
- ADR-0002: PLATFORM_SEPARATION
- ADR-0003: CSL_AS_INDEPENDENT_STANDARD

**Governance Conclusion:** ADRs are governance artifacts that document architectural
decisions. They depend on the governance workflow (Architecture Requirement → Audit → ADR)
and feed into canonical standards and implementations.

---

## 6. Architecture Requirements Dependency

**Verified Fact:** The `architecture/requirements/` directory contains 12 Architecture
Requirements (AR-0001 through AR-0012) covering CDM, CSL, knowledge graph, reasoning
model, execution model, audit model, maturity model, executable documents, YAML metadata,
layered architecture, lexical/address index, and human-governed canonical language.

**Governance Conclusion:** Architecture Requirements are the formal inputs to the
governance workflow. They precede ADRs and canonical standards in the dependency chain.

---

## 7. Missing Dependency Links

**Engineering Inference:** The following dependency links are implied but not formally
established in the repository:

1. No document explicitly connects `PROJECT_VALUES.md` to `ENGINEERING_PRINCIPLES.md`
   (values should inform principles, but no formal link exists because values are empty).

2. No document explicitly connects `PROJECT_SCOPE.md` to `PROJECT_OBJECTIVES.md`
   (scope should bound objectives, but no formal link exists).

3. No document explicitly connects `PROJECT_RISK_MODEL.md` to `RELEASE_POLICY.md`
   (risk governs release, but no formal link exists).

4. No document explicitly connects `PROJECT_STAKEHOLDERS.md` to `GOVERNANCE_MODEL.md`
   (stakeholders map to governance roles, but no formal link exists).

5. No document explicitly connects `PROJECT_LIFECYCLE.md` to `GOVERNANCE_MODEL.md`
   (lifecycle stages should map to governance lifecycle, but no formal link exists).

These missing links are governance gaps, not architectural errors.
They arise because the 14 empty documents have not yet been authored.

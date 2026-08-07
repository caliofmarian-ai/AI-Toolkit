# Governance Architecture — Repository Reconstruction
Version: 1.0.0
Status: Draft
Classification: Engineering Research Reference

## REPOSITORY FACT
The repository contains governance logic at five distinct levels: CSL standard governance, repository System Laws, legacy canonical index governance, runtime-governance canon, and platform-governance canon. Those layers are separately evidenced and are not fully reconciled into one explicit hierarchy document. [Source: standards/csl/CSL_CONSTITUTION.md:15-23, 803-857; docs/system-laws/SYSTEM-LAW-001_ZERO_CONTEXT_LOSS_v1.0.0.md:13-19; docs/canonical/CANONICAL_MASTER_INDEX_v1.0.0.md:8-12, 16-59; docs/canonical/v3/CANON-050_AUTONOMOUS_GOVERNANCE_SPECIFICATION_v3.0.0.md:138-183; docs/canonical/v4/CANON-058_AI_CTO_AUTONOMOUS_RUNTIME_PLATFORM_SPECIFICATION_v4.0.0.md:263-273, 319-439]

## REPOSITORY EVIDENCE
### A. CSL standard governance layer
The CSL Constitution establishes the standard-level authority model:
> "Canonical Knowledge is the highest engineering authority." [Source: standards/csl/CSL_CONSTITUTION.md:29-47]

It defines one directional authority flow:
Human Vision → Human Intent → Canonical Knowledge → Engineering Compiler → Universal Engineering Model → Engineering Artifacts → Execution. [Source: standards/csl/CSL_CONSTITUTION.md:133-172]

It also defines the CSL Foundation as the standard's governing body and says the standard evolves through RFC governance. [Source: standards/csl/CSL_CONSTITUTION.md:803-857]

### B. Repository absolute-law layer
The repository introduces System Laws as an AI-Toolkit-specific absolute layer:
- SYSTEM-LAW-001: "This law has precedence over every canonical specification." [Source: docs/system-laws/SYSTEM-LAW-001_ZERO_CONTEXT_LOSS_v1.0.0.md:15-19]
- SYSTEM-LAW-002: every future canonical specification shall comply with operational separation. [Source: docs/system-laws/SYSTEM-LAW-002_OPERATIONAL_SEPARATION_v1.0.0.md:126-130]
- SYSTEM-LAW-003: Owner final authority, explicit authorization for autonomy, no weakening of Owner authority. [Source: docs/system-laws/SYSTEM-LAW-003_HUMAN_FINAL_AUTHORITY_v1.0.0.md:15-20, 55-75, 162-176]

### C. Legacy canonical-index layer
The Canonical Master Index claims repository-level catalog authority:
> "This document is the authoritative index of every canonical document in AI Toolkit." [Source: docs/canonical/CANONICAL_MASTER_INDEX_v1.0.0.md:8-10]

It defines a precedence stack:
Canonical Master Index → System Architecture → System Invariants → CLI Specification → Engine Interface Specification → Workflow Specifications → Memory Specifications → Plugin Specifications → Test Specifications → Implementation Documents. [Source: docs/canonical/CANONICAL_MASTER_INDEX_v1.0.0.md:16-59]

It further says: "Only OWNER-approved canonical documents define platform behavior." [Source: docs/canonical/CANONICAL_MASTER_INDEX_v1.0.0.md:152-157]

### D. Runtime-governance layer (v3)
CANON-050 defines the Runtime governance hierarchy:
Level 1 Canonical Specifications → Level 2 Owner Decisions → Level 3 Architecture Rules → Level 4 Runtime Policies → Level 5 Scheduling Decisions → Level 6 Execution Decisions → Level 7 Optimization Decisions. [Source: docs/canonical/v3/CANON-050_AUTONOMOUS_GOVERNANCE_SPECIFICATION_v3.0.0.md:138-183]

CANON-050 also calls itself the canonical governance specification for Version 3 and the highest policy enforcement authority of the Runtime. [Source: docs/canonical/v3/CANON-050_AUTONOMOUS_GOVERNANCE_SPECIFICATION_v3.0.0.md:1051-1064]

CANON-047 defines the owner-interaction side of the same v3 layer, including approval workflow, communication levels, escalation, and decision history. [Source: docs/canonical/v3/CANON-047_OWNER_INTERACTION_SPECIFICATION_v3.0.0.md:188-228, 338-380, 384-520, 925-1110]

CANON-055 defines execution-side integration by stating that the Runtime Server delegates protected decisions to the Governance Engine and never bypasses governance. [Source: docs/canonical/v3/CANON-055_AI_CTO_RUNTIME_SERVER_SPECIFICATION_v3.0.0.md:1372-1392]

### E. Platform-governance layer (v4)
CANON-058 declares a six-domain platform model:
1. Canonical Architecture
2. Runtime Platform
3. Engineering Platform
4. Portfolio Platform
5. Communication Platform
6. Governance Platform [Source: docs/canonical/v4/CANON-058_AI_CTO_AUTONOMOUS_RUNTIME_PLATFORM_SPECIFICATION_v4.0.0.md:319-439]

Its Governance Platform is responsible for Authorization, Approvals, Compliance, Security, Canonical Validation, and Architecture Protection. [Source: docs/canonical/v4/CANON-058_AI_CTO_AUTONOMOUS_RUNTIME_PLATFORM_SPECIFICATION_v4.0.0.md:421-439]

It also defines a control-flow architecture:
Owner → Governance → Runtime Server → Runtime Orchestrator → Engineering Agents → Runtime Engines → Repositories → Evidence → Reports → Owner. [Source: docs/canonical/v4/CANON-058_AI_CTO_AUTONOMOUS_RUNTIME_PLATFORM_SPECIFICATION_v4.0.0.md:1333-1375]

### F. Knowledge-placement layer
The repository separates authoritative knowledge from generated and runtime assets:
- `knowledge/README.md`: authoritative source for engineering knowledge. [Source: knowledge/README.md:13-31]
- `generated/README.md`: compiler outputs are never authoritative. [Source: generated/README.md:13-30]
- `runtime/README.md`: runtime assets are implementation-specific and separated from Canonical Knowledge. [Source: runtime/README.md:13-30]

### G. Operational review and development governance layer
README and CANON-044 define implementation governance patterns:
- README lifecycle: Canonical Analysis → Architecture Review → Implementation Package → Implementation → Validation → Testing → Pull Request → Independent Review → Merge → Runtime Validation → Production Deployment → Continuous Monitoring. [Source: README.md:624-641]
- CANON-044 lifecycle: Canonical Specification → Implementation → Architecture Review → Pull Request Review → Merge → Local Synchronisation → Real Workspace Validation → Development State Update → Executive Briefing Update → Next CORE Recommendation. [Source: docs/canonical/CANON-044_AI_CTO_DEVELOPMENT_POLICY_SPECIFICATION_v1.0.0.md:36-99]

## ENGINEERING CONCLUSION
The best evidence-based reconstruction is a layered governance architecture, not a single linear stack:

```text
Humans / Owner intent
    ↓
CSL standard governance
    - CSL Manifesto (philosophy)
    - CSL Constitution (supreme CSL rules)
    - Volume VII Safety & Governance
    - RFC governance
    ↓
AI-Toolkit System Laws
    - Zero Context Loss
    - Operational Separation
    - Human Final Authority
    ↓
Repository canonical authorities (contested)
    - Legacy Canonical Master Index
    - v3 Runtime Governance (CANON-050 + CANON-047 + CANON-055)
    - v4 Platform Authority (CANON-058 + CANON-059)
    ↓
Domain governance specifications
    - Validation / governance / approval / roadmap / self-evolution / dashboard
    ↓
Operational interfaces and stores
    - Knowledge store
    - Runtime services
    - Dashboard / Telegram / GitHub / CLI
    - Generated artifacts and reports
```

The repository therefore has an architecture of governance, but not a single fully reconciled official hierarchy. The most stable cross-version rule is: human-approved canonical knowledge governs lower layers, while System Laws constrain repository behavior absolutely. [Source: standards/csl/CSL_CONSTITUTION.md:133-172; docs/system-laws/SYSTEM-LAW-001_ZERO_CONTEXT_LOSS_v1.0.0.md:15-19; docs/system-laws/SYSTEM-LAW-003_HUMAN_FINAL_AUTHORITY_v1.0.0.md:162-176]

INSUFFICIENT EVIDENCE: a single repository document that explicitly reconciles the Constitution, System Laws, Canonical Master Index, CANON-050, and CANON-058 into one uncontested hierarchy. [Source: docs/canonical/CANONICAL_MASTER_INDEX_v1.0.0.md:8-12; docs/canonical/v4/CANON-058_AI_CTO_AUTONOMOUS_RUNTIME_PLATFORM_SPECIFICATION_v4.0.0.md:263-273]

## ENGINEERING RECOMMENDATION
Adopt a formal reconciliation order for future work:
1. CSL Constitution governs the CSL standard.
2. System Laws govern repository safety and human authority.
3. One version-root AI Toolkit governance document should govern each major platform generation.
4. Domain-specific canonical documents should govern only their scoped domains.
5. Informative documents should never make independent authority claims.

This recommendation requires Owner approval because it would change the practical interpretation of repository governance. [Source: docs/system-laws/SYSTEM-LAW-003_HUMAN_FINAL_AUTHORITY_v1.0.0.md:55-75]

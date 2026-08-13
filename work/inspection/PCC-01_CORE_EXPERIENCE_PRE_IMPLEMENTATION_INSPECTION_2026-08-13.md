# PCC-01 — Core Experience Pre-Implementation Inspection

Research Program: PCC-01

Capability: Persistent Experience

Inspection Type: Pre-Implementation Software Anatomy Inspection

Human Authority: Owner

Date: 2026-08-13

Implementation Status: NOT DEMONSTRATED

Canonical Status: NOT CANON

Production Status: NOT PRODUCTION-READY

Source Plan: `work/planning/PCC-01_IMPLEMENTATION_INVENTORY_AND_BUILD_PLAN.md`

Source Plan Fingerprint: `4220024727e84c20ecedd835b8e61443050d14ce199522ab068a658a2ad10d78`

Source Human Acceptance: `work/decisions/PCC-01_IMPLEMENTATION_INVENTORY_AND_BUILD_PLAN_HUMAN_ACCEPTANCE_2026-08-13.md`

Source Human Acceptance Fingerprint: `2e7096ddc99a2b18cd29f6e16afac231d682c4412e270f656e23190dffb734e7`

Repository HEAD Inspected: `65ca32c5730fe45fdc5afd5d73372c54d380b28f`

---

## 1. Purpose

This document records the pre-implementation inspection for
PCC-01 Core Experience Implementation.

The purpose of this inspection is not to infer implementation
from filenames and not to modify the organism.

The purpose is to inspect the existing software anatomy before
constructing the first real Experience organ.

The inspection must determine:

1. what Experience-related tissue already exists;
2. what Session tissue already exists;
3. what Memory tissue already exists;
4. what Evidence tissue already exists;
5. what Provenance tissue already exists;
6. what persistence and repository tissue already exists;
7. what identity and lifecycle tissue already exists;
8. what can be inherited;
9. what must be adapted;
10. what must be constructed new;
11. what must not be used;
12. which concrete files are candidates for the first
    implementation;
13. which tests already exist;
14. which tests must accompany the first implementation.

No software implementation is performed by this inspection.

---

## 2. Epistemic State Before Inspection

- Implementation Inventory and Build Plan: ACCEPTED
- Human Acceptance: CONSERVED
- Implementation: NOT DEMONSTRATED
- Canon: NOT CANON
- Production: NOT PRODUCTION-READY

The following boundaries remain mandatory:

- **Experience != Session**
- **Experience != Memory**
- **Experience != Evidence**
- **Experience != raw dialogue**
- **Session != process**
- **Session != provider**
- **Storage != Experience**
- **Interpretation != historical fact**
- **Persistence != authority**
- **Human Acceptance != Implementation**

The restart identity invariant remains:

**ID_before_restart == ID_after_restart**

---

## 3. Accepted Plan Requirements Relevant to Core Experience

### Source Plan Section 4 — Regula fundamentală a inventarului

```text

Niciun organ existent nu este declarat automat compatibil cu PCC-01.

Existența codului nu înseamnă compatibilitate.

Asemănarea semantică nu înseamnă identitate.

Fiecare țesut trebuie examinat înainte de moștenire.

---

```

### Source Plan Section 5 — Cele patru clasificări

```text

Fiecare componentă examinată primește una dintre următoarele clasificări:

**MOȘTENIM**

Componenta poate fi utilizată fără schimbarea identității sale fundamentale.

**ADAPTĂM**

Componenta poate fi reutilizată, dar are nevoie de extensii sau modificări controlate.

**CONSTRUIM NOU**

Organul sau țesutul necesar PCC-01 nu există în forma cerută.

**NU FOLOSIM**

Componenta există, dar folosirea ei pentru rolul respectiv ar încălca anatomia PCC-01.

---

```

### Source Plan Section 6 — Frontiera Experience

```text

Experience trebuie să devină un obiect software explicit.

Experience NU poate fi doar:

- un mesaj;
- un fișier;
- un fragment de conversație;
- o intrare Memory;
- o Session;
- Evidence;
- un rezultat arbitrar al unui model;
- un dictionary fără contract;
- o înregistrare accidentală într-un storage.

**Experience != Session**

**Experience != Memory**

**Experience != Evidence**

**Experience != raw dialogue**

---

```

### Source Plan Section 14 — Inventarul — Experience

```text

Organ software PCC-01 dedicat pentru Experience:

**Clasificare: CONSTRUIM NOU**

Auditul anterior nu a demonstrat existența unui organ Python PCC-01 care să implementeze complet identitatea și ciclul Persistent Experience.

Există material experimental și documentar asociat Experience.

Acesta nu trebuie confundat cu organul executabil.

---

```

### Source Plan Section 18 — Invariantul de identitate

```text

Invariantul obligatoriu este:

**ID_before_restart == ID_after_restart**

Dacă obiectul recuperat după restart reprezintă aceeași Experience, identitatea sa trebuie păstrată.

---

```

### Source Plan Section 30 — Session subsystem existent

```text

Repository-ul conține un subsistem `session_runtime`.

Au fost identificate componente pentru:

- modele;
- runtime;
- storage.

Clasificare generală:

**MOȘTENIM / ADAPTĂM**

Nu reconstruim Session fără motiv.

---

```

### Source Plan Section 39 — Memory subsystem existent

```text

Repository-ul conține mai multe componente asociate Memory.

Clasificare:

**MOȘTENIM / ADAPTĂM**

Nu transformăm Memory în Experience.

---

```

### Source Plan Section 43 — Evidence subsystem existent

```text

Repository-ul conține mecanisme Evidence.

Clasificare:

**MOȘTENIM / ADAPTĂM**

Evidence va fi folosit pentru demonstrarea PCC-01.

---

```

### Source Plan Section 48 — Provenance existent

```text

Repository-ul conține mecanisme de provenance în zona knowledge/CDM.

Clasificare:

**ADAPTĂM / MOȘTENIM**

Nu construim provenance paralel înainte de a verifica aceste mecanisme.

---

```

### Source Plan Section 91 — Experience service

```text

Este necesar un organ fiziologic care orchestrează ciclul Experience.

**Clasificare: CONSTRUIM NOU**

Acesta nu trebuie să fie doar un wrapper peste storage.

---

```

### Source Plan Section 105 — Prima construcție

```text

Prima construcție trebuie să fie nucleul Experience.

Nu începem cu Dashboard.

Nu începem cu integrarea tuturor providerilor.

Nu începem cu Memory.

Nu începem cu UI.

---

```

### Source Plan Section 106 — Build Phase 1 — Model

```text

Construim Experience Model.

Trebuie să fie testabil independent.

---

```

### Source Plan Section 107 — Build Phase 2 — Identity

```text

Construim mecanismul de identity.

Testăm unicitatea și stabilitatea.

---

```

### Source Plan Section 108 — Build Phase 3 — Lifecycle

```text

Construim stările și tranzițiile permise.

Testăm refuzul tranzițiilor ilegale.

---

```

### Source Plan Section 109 — Build Phase 4 — Repository

```text

Construim persistența Experience.

Testăm save/load.

---

```

### Source Plan Section 110 — Build Phase 5 — Recovery

```text

Construim recovery după restart.

Acesta este punct critic PCC-01.

---

```

### Source Plan Section 111 — Build Phase 6 — Session binding

```text

Conectăm Experience cu Session existentă.

Păstrăm identitățile separate.

---

```

### Source Plan Section 112 — Build Phase 7 — Provenance

```text

Conectăm proveniența.

---

```

### Source Plan Section 113 — Build Phase 8 — Protection

```text

Construim și testăm protecția.

---

```

### Source Plan Section 114 — Build Phase 9 — Retention

```text

Construim retention.

---

```

### Source Plan Section 115 — Build Phase 10 — Forgetting

```text

Construim forgetting și diferența față de archive/delete.

---

```

### Source Plan Section 116 — Build Phase 11 — Conflict and ambiguity

```text

Construim reprezentarea conflictului și ambiguității.

---

```

### Source Plan Section 117 — Build Phase 12 — Evidence

```text

Conectăm Evidence Engine și materializăm dovezile PCC-01.

---

```

### Source Plan Section 149 — Bucla minimă reală

```text

Demonstrația minimă PCC-01 trebuie să execute:

**candidate -> Experience -> identity -> protection -> persistence -> Session binding -> process death -> process restart -> recovery -> inspection -> retention/forgetting behavior**

Această buclă trebuie să fie reală.

Nu simulată prin obiecte păstrate în același proces.

---

```

### Source Plan Section 154 — Criteriul IMPLEMENTED

```text

PCC-01 poate deveni candidat pentru verdictul:

**PCC-01 IMPLEMENTED**

numai după ce:

- organele obligatorii există;
- testele obligatorii trec;
- restart real este demonstrat;
- identity este stabilă;
- Session binding este demonstrat;
- retention/forgetting sunt demonstrate;
- Evidence este materializată;
- frontierele epistemice sunt păstrate;
- omul examinează Evidence.

---

```

### Source Plan Section 159 — Anatomia software minimă propusă

```text

Nucleul PCC-01 trebuie să conțină conceptual:

**Experience Model**

**Experience Identity**

**Experience Lifecycle**

**Experience Service**

**Experience Repository**

**Experience Session Binding**

**Experience Provenance Integration**

**Experience Protection**

**Experience Retention**

**Experience Forgetting**

**Experience Evidence Integration**

---

```

### Source Plan Section 180 — Primul milestone

```text

Primul milestone software este:

**PCC-01 CORE EXPERIENCE**

Conține:

- model;
- identity;
- lifecycle;
- service;
- repository.

---

```

### Source Plan Section 193 — Poarta umană

```text

După Evidence:

**HUMAN DECISION REQUIRED**

Software-ul nu se autodeclară PCC-01 IMPLEMENTED.

---

```

### Source Plan Section 200 — Starea actuală

```text

La momentul acestui plan:

**Implementation Status: NOT DEMONSTRATED**

**Canonical Status: NOT CANON**

**Production Status: NOT PRODUCTION-READY**

---

```

### Source Plan Section 201 — Finding principal

```text

AI-Toolkit nu pornește de la zero.

Organismul are deja organe vecine importante:

- Session;
- Memory;
- Evidence;
- provenance/knowledge structures;
- execution;
- review;
- persistence infrastructure.

Dar auditul nu a demonstrat existența organului fiziologic complet Persistent Experience.

---

```

### Source Plan Section 203 — Anatomia de construcție

```text

Fluxul propus este:

Input / event / result  
↓  
Experience Candidate  
↓  
Admission  
↓  
Experience Model  
↓  
Identity  
↓  
Validation  
↓  
Protection  
↓  
Persistence  
↓  
Session Binding  
↓  
Process Death  
↓  
Process Restart  
↓  
Recovery  
↓  
Inspection  
↓  
Retention / Archive / Forgetting  
↓  
Evidence  
↓  
Human Evaluation

---

```

### Source Plan Section 204 — Criteriul biologic

```text

Persistent Experience există cu adevărat numai dacă organismul poate trece printr-o întrerupere reală a procesului și poate reveni cu aceeași Experience identificabilă și inspectabilă.

---

```

### Source Plan Section 215 — Planul imediat după acceptare

```text

Ordinea imediată trebuie să fie:

1. verificarea căilor software exacte;
2. stabilirea package-ului PCC-01;
3. Experience Model;
4. Experience Identity;
5. Experience Lifecycle;
6. Experience Repository;
7. Experience Service;
8. testele nucleului;
9. restart harness;
10. recovery test;
11. Session adapter;
12. provenance;
13. protection;
14. retention;
15. forgetting;
16. conflict/ambiguity;
17. Evidence;
18. acceptance run.

---

```

### Source Plan Section 250 — Trasabilitatea completă

```text

Trebuie să putem urmări:

Research  
-> Reconciliation  
-> Human Acceptance  
-> Implementation Contract  
-> Human Acceptance  
-> Inventory and Build Plan  
-> Software  
-> Tests  
-> Evidence  
-> Human Decision

---

```

### Source Plan Section 266 — Matricea principală

```text

| Corp / funcție | Clasificare | Rol PCC-01 |
|---|---|---|
| Experience Core | CONSTRUIM NOU | organ central |
| Experience Model | CONSTRUIM NOU | anatomia Experience |
| Experience Identity | CONSTRUIM NOU | identitate persistentă |
| Experience Lifecycle | CONSTRUIM NOU | fiziologia stărilor |
| Experience Service | CONSTRUIM NOU | coordonare |
| Experience Repository | CONSTRUIM NOU | conservare |
| Session Runtime | MOȘTENIM / ADAPTĂM | context/session |
| Memory | MOȘTENIM / ADAPTĂM | memorie distinctă |
| Evidence Engine | MOȘTENIM / ADAPTĂM | demonstrație |
| Provenance | MOȘTENIM / ADAPTĂM | origine/trasabilitate |
| Execution Engine | ADAPTĂM DUPĂ CORE | sursă candidate |
| Autonomous Execution | ADAPTĂM DUPĂ CORE | sursă candidate |
| Review Agent | ADAPTĂM DUPĂ CORE | interpretation |
| Retention | CONSTRUIM NOU | păstrare controlată |
| Forgetting | CONSTRUIM NOU | uitare controlată |
| Conflict | CONSTRUIM NOU | contradicție explicită |
| Ambiguity | CONSTRUIM NOU | incertitudine explicită |
| CLI observability | ADAPTĂM | inspecție |
| Dashboard | ADAPTĂM ULTERIOR | observabilitate umană |

---

```

### Source Plan Section 267 — Matricea frontierelor

```text

| Frontieră | Regula |
|---|---|
| Experience / Session | Experience != Session |
| Experience / Memory | Experience != Memory |
| Experience / Evidence | Experience != Evidence |
| Experience / dialogue | Experience != raw dialogue |
| Session / process | Session != process |
| Session / provider | Session != provider |
| Storage / Experience | Storage != Experience |
| Interpretation / history | Interpretation != historical fact |
| Persistence / authority | Persistence != authority |
| Acceptance / implementation | Human Acceptance != Implementation |

---

```

### Source Plan Section 268 — Matricea porților

```text

| Poartă | Condiție |
|---|---|
| Plan Accepted | decizie umană |
| Core Built | model + identity + lifecycle + service + repository |
| Persistence Demonstrated | durable save/load |
| Restart Demonstrated | proces nou recuperează aceeași identity |
| Binding Demonstrated | Experience <-> Session recuperabil |
| Lifecycle Demonstrated | retention/archive/forgetting |
| Evidence Complete | dovezi inspectabile |
| PCC-01 IMPLEMENTED | criteriile contractului + decizie |
| PCC-01 PRODUCTION-READY | evaluare separată |
| Canon | decizie canonică separată |

---

```

### Source Plan Section 276 — Decizia asupra planului

```text

Acest document este încă:

**CANDIDATE — HUMAN ACCEPTANCE REQUIRED**

Nu autorizează automat modificarea software-ului până când omul nu îl acceptă.

---

```

### Source Plan Section 284 — Anatomia finală a planului

```text

PCC-01 trebuie construit ca un sistem de organe cooperante:

Experience Core  
+ Session integration  
+ Persistence  
+ Provenance  
+ Protection  
+ Retention  
+ Forgetting  
+ Conflict/Ambiguity  
+ Evidence  
+ Human inspection

---

```

### Source Plan Section 285 — Fiziologia finală

```text

Organismul trebuie să poată:

primi material candidat,  
decide dacă devine Experience,  
atribui identitate,  
proteja,  
persista,  
lega de Session,  
supraviețui morții procesului,  
recupera aceeași Experience,  
inspecta proveniența,  
reține sau uita controlat,  
reprezenta conflictul și ambiguitatea,  
produce Evidence,  
și permite omului să decidă dacă funcția există cu adevărat.

---

```

### Source Plan Section 286 — Criteriul final de succes

```text

Succesul nu este:

„avem un fișier Experience”.

Succesul este:

**organismul poate păstra o Experience identificabilă peste moartea și renașterea procesului, fără să o confunde cu Session, Memory sau Evidence.**

---

```

### Source Plan Section 290 — Poarta următoare

```text

Următoarea poartă este:

**HUMAN ACCEPTANCE OF PCC-01 IMPLEMENTATION INVENTORY AND BUILD PLAN**

Numai după această acceptare poate începe construcția software conform planului.

---

```

### Source Plan Section 292 — Declarația finală

```text

Acest document definește inventarul și ordinea de construcție pentru transformarea PCC-01 din anatomie acceptată în funcție software demonstrabilă.

El nu pretinde că funcția există deja.

El nu confundă Experience cu Memory.

El nu confundă Experience cu Session.

El nu confundă Experience cu Evidence.

El nu confundă persistența cu autoritatea.

El nu confundă acceptarea cu implementarea.

**PCC-01 IMPLEMENTATION INVENTORY AND BUILD PLAN COMPLETE — HUMAN DECISION REQUIRED**

**NEXT GATE: HUMAN ACCEPTANCE OF PCC-01 IMPLEMENTATION INVENTORY AND BUILD PLAN**

---

END OF PCC-01 — PERSISTENT EXPERIENCE IMPLEMENTATION INVENTORY AND BUILD PLAN
```

Extracted relevant source sections: 43

## 4. Repository Software Anatomy

### 4.1 Directories

```text
.ai
.ai/audit
.ai/audit/core021a002
.ai/audit/import_normalization
.ai/audit/python_package_normalization
.ai/audit/python_runtime_bootstrap
.ai/audit/test_infrastructure_audit
.ai/backups
.ai/backups/core021a002
.ai/batches
.ai/batches/BATCH-001
.ai/batches/BATCH-002
.ai/batches/BATCH-003
.ai/context
.ai/development_state
.ai/execution
.ai/executive
.ai/memory
.ai/planning
.ai/reports
.ai/runtime
.ai/runtime/cache
.ai/runtime/checkpoints
.ai/runtime/logs
.ai/runtime/sessions
.ai/runtime/state
.ai/self_evaluation
.ai/self_improvement
.ai/sessions
.ai/work
.copilot
.copilot/tasks
.pytest_cache
.pytest_cache/v
.pytest_cache/v/cache
architecture
architecture-proposals
architecture/adr
architecture/audit
architecture/audit/cdm
architecture/audit/model-stack
architecture/reference
architecture/reference/model-stack
architecture/requirements
architecture/requirements/backlog
architecture/requirements/templates
artifacts
audit
audit/canon-001
bin
canonical_metabolism
development
docs
docs/audits
docs/audits/canonical-system
docs/audits/copilot-review
docs/audits/rules
docs/audits/specifications
docs/audits/templates
docs/canon
docs/canonical
docs/canonical/v3
docs/canonical/v4
docs/canonical/v5
docs/foundation-completion
docs/graphql
docs/implementation
docs/mcp
docs/openapi
docs/planning
docs/research
docs/research/canonical-foundation
docs/research/governance-reconciliation
docs/system-laws
engineering-rules
generated
gestation
gestation/creator-dialogue
gestation/creator-understanding
gestation/proven-facts
gestation/research
gestation/transformations
governance
implementation-packages
implementation-packages/CORE-022
implementation-packages/CORE-023
implementation-packages/PLATFORM
knowledge
lib
lib/python
lib/python/agent_runtime
lib/python/agents
lib/python/ai_control_center
lib/python/ai_cto_scanner
lib/python/ai_platform
lib/python/audit_engine
lib/python/autonomous_execution_engine
lib/python/autonomous_planner
lib/python/autonomous_planning_engine
lib/python/batch_generator
lib/python/batch_planner
lib/python/canonical_audit
lib/python/canonical_entities
lib/python/canonical_intelligence
lib/python/canonical_parser
lib/python/canonical_repository
lib/python/cdm_engine
lib/python/cli
lib/python/common
lib/python/compliance_engine
lib/python/context_synchronization_engine
lib/python/coverage_engine
lib/python/csl_engine
lib/python/css_engine
lib/python/dashboard
lib/python/dependency_engine
lib/python/development_state_engine
lib/python/development_validator
lib/python/discovery_engine
lib/python/drift_engine
lib/python/engineering_engine
lib/python/engineering_workspace
lib/python/epistemic
lib/python/evidence_engine
lib/python/executable_repository_intelligence
lib/python/execution_coordinator
lib/python/execution_engine
lib/python/executive_briefing_engine
lib/python/foundation_audit
lib/python/github_materialization
lib/python/knowledge_engine
lib/python/knowledge_graph
lib/python/knowledge_graph_v2
lib/python/knowledge_materialization
lib/python/planning_engine
lib/python/planning_optimizer
lib/python/profiler
lib/python/progress_monitor
lib/python/project_profiles
lib/python/recommendation_engine
lib/python/reporting_engine
lib/python/repository_engine
lib/python/repository_inspector_v2
lib/python/review_agent
lib/python/rule_engine
lib/python/runtime
lib/python/self_evaluation_engine
lib/python/self_improvement_engine
lib/python/semantic_engine
lib/python/semantic_matching
lib/python/semantic_repository_intelligence
lib/python/session_runtime
lib/python/validation_engine
lib/python/workspace_index
lib/python/workspace_manager
lib/python/workspace_orchestrator
runtime
standards
standards/cdm
standards/cdm/architecture
standards/cdm/meta
standards/cdm/shared
standards/csl
standards/csl/archive
standards/csl/core
standards/csl/meta
standards/csl/migration
standards/csl/shared
standards/csl/versions
standards/css
standards/css/architecture
standards/css/meta
standards/css/templates
tests
tests/engineering
tests/epistemic
tools
tools/engineering
work
work/audit
work/audits
work/bootstrap
work/canon-v6
work/canonical
work/capabilities
work/cdm
work/checkpoints
work/contracts
work/core
work/decisions
work/digest
work/epistemic-graph
work/epistemic-graph/evidence
work/events
work/evolution
work/execution
work/genome
work/history
work/inspection
work/inventory
work/knowledge
work/life
work/lineage
work/manifest
work/memory
work/needs
work/output
work/persistent-experience
work/persistent-experience/active
work/persistent-experience/evidence
work/persistent-experience/index
work/planning
work/rebuild
work/rebuild/AR
work/rebuild/CDM-000_FOUNDATION
work/rebuild/CORE
work/rebuild/RESEARCH
work/reconciliation
work/research
work/runtime
work/scripts
work/seed
work/snapshots
work/state
work/status
work/structure
work/templates
work/trace
work/transformation-evidence
work/transformation-system
work/transformation-system/templates
work/transformations
work/transformations/TR-000001
work/witness
```

### 4.2 Software, Test and Configuration Files

```text
.ai/audit/dependency_graph.json
.ai/audit/execution_plan.json
.ai/audit/foundation_audit_001.json
.ai/audit/foundation_audit_002.json
.ai/audit/knowledge_database.json
.ai/audit/knowledge_graph_v2.json
.ai/audit/repository_inspector_v2.json
.ai/audit/repository_inventory.json
.ai/audit/repository_inventory_v2.json
.ai/audit/validation_report.json
.ai/backups/core021a002/test_knowledge_engine_v2.py
.ai/backups/core021a002/test_repository_engine_v2.py
.ai/batches/BATCH-001/metadata.json
.ai/batches/BATCH-001/steps.json
.ai/batches/BATCH-002/metadata.json
.ai/batches/BATCH-002/steps.json
.ai/context/development_context.json
.ai/context/git_context.json
.ai/context/github_context.json
.ai/context/live_context.json
.ai/context/repository_profile.json
.ai/context/synchronization_report.json
.ai/context/workspace_context.json
.ai/development_state/current_state.json
.ai/development_state/events.json
.ai/development_state/executive_snapshot.json
.ai/development_state/integrity.json
.ai/executable_repository_map.json
.ai/execution/execution.json
.ai/execution/execution_context.json
.ai/execution/execution_evidence.json
.ai/execution/execution_history.json
.ai/execution/execution_log.json
.ai/execution/execution_metrics.json
.ai/execution/execution_queue.json
.ai/execution/execution_report.json
.ai/execution/execution_results.json
.ai/execution/execution_snapshot.json
.ai/execution_state.json
.ai/executive/briefing.json
.ai/executive/owner_actions.json
.ai/executive/priorities.json
.ai/executive/recommendations.json
.ai/executive/risks.json
.ai/memory/decision.json
.ai/memory/history.json
.ai/memory/index.json
.ai/memory/knowledge_graph.json
.ai/memory/repository_profile_1.json
.ai/memory/repository_profile_2.json
.ai/memory/workflow.json
.ai/planning/execution_queue.json
.ai/planning/next_actions.json
.ai/planning/planning.json
.ai/planning/recommended_batch.json
.ai/planning/recommended_core.json
.ai/planning/recommended_issue.json
.ai/planning/recommended_milestone.json
.ai/planning/recommended_pr.json
.ai/planning/roadmap_progress.json
.ai/reports/inspect-20260807.json
.ai/runtime/cache/workspace_index/index.json
.ai/runtime/cache/workspace_index/snapshot.json
.ai/runtime/logs/runtime_periodic_20260803_125834.json
.ai/runtime/logs/runtime_periodic_20260803_125835.json
.ai/runtime/logs/runtime_periodic_20260803_130455.json
.ai/runtime/logs/runtime_periodic_20260803_130456.json
.ai/runtime/state/shutdown_state.json
.ai/runtime_repository_model.json
.ai/self_evaluation/architecture.json
.ai/self_evaluation/compliance.json
.ai/self_evaluation/confidence.json
.ai/self_evaluation/coverage.json
.ai/self_evaluation/evaluation.json
.ai/self_evaluation/evidence.json
.ai/self_evaluation/history.json
.ai/self_evaluation/quality.json
.ai/self_evaluation/regressions.json
.ai/self_evaluation/snapshot.json
.ai/self_improvement/capability_analysis.json
.ai/self_improvement/history.json
.ai/self_improvement/improvements.json
.ai/self_improvement/optimization_plan.json
.ai/self_improvement/performance.json
.ai/self_improvement/proposed_batches.json
.ai/self_improvement/proposed_cores.json
.ai/self_improvement/proposed_issues.json
.ai/self_improvement/roadmap_updates.json
.ai/self_improvement/snapshot.json
.ai/self_improvement/technical_debt.json
.ai/semantic_knowledge.json
.ai/sessions/SESSION-20260803-050009.json
.ai/sessions/SESSION-20260803-050013.json
.ai/work/development_validation.json
artifacts/engineering-project.json
docs/audits/templates/report.json
docs/openapi/runtime-api-v1.yaml
engineering-rules/dependencies.yaml
lib/__init__.py
lib/context_engine.sh
lib/execution_engine.sh
lib/git_engine.sh
lib/github_engine.sh
lib/issue_engine.sh
lib/planner_engine.sh
lib/python/__init__.py
lib/python/agent_runtime/__init__.py
lib/python/agent_runtime/base.py
lib/python/agent_runtime/models.py
lib/python/agent_runtime/registry.py
lib/python/agent_runtime/runtime.py
lib/python/agents/__init__.py
lib/python/agents/ai_cto_scanner_agent.py
lib/python/agents/development_agent.py
lib/python/agents/development_report.py
lib/python/agents/repository_inspector_agent.py
lib/python/ai_control_center/__init__.py
lib/python/ai_control_center/application.py
lib/python/ai_control_center/bootstrap.py
lib/python/ai_control_center/config.py
lib/python/ai_control_center/kernel.py
lib/python/ai_control_center/models/__init__.py
lib/python/ai_control_center/panels/__init__.py
lib/python/ai_control_center/panels/ai/__init__.py
lib/python/ai_control_center/panels/canonical/__init__.py
lib/python/ai_control_center/panels/dashboard/__init__.py
lib/python/ai_control_center/panels/development/__init__.py
lib/python/ai_control_center/panels/github/__init__.py
lib/python/ai_control_center/panels/knowledge/__init__.py
lib/python/ai_control_center/panels/railway/__init__.py
lib/python/ai_control_center/panels/repository/__init__.py
lib/python/ai_control_center/panels/repository/panel.py
lib/python/ai_control_center/panels/runtime/__init__.py
lib/python/ai_control_center/panels/workspace/__init__.py
lib/python/ai_control_center/providers/__init__.py
lib/python/ai_control_center/providers/base.py
lib/python/ai_control_center/providers/local_repository.py
lib/python/ai_control_center/registry.py
lib/python/ai_control_center/runtime/__init__.py
lib/python/ai_control_center/services/__init__.py
lib/python/ai_control_center/session/__init__.py
lib/python/ai_cto_scanner/__init__.py
lib/python/ai_cto_scanner/detectors.py
lib/python/ai_cto_scanner/engine.py
lib/python/ai_cto_scanner/report.py
lib/python/ai_cto_scanner/scoring.py
lib/python/ai_platform/__init__.py
lib/python/ai_platform/adapters.py
lib/python/ai_platform/context_builder.py
lib/python/ai_platform/model_manager.py
lib/python/ai_platform/pipeline.py
lib/python/ai_platform/prompt_library.py
lib/python/ai_platform/registry.py
lib/python/ai_platform/service.py
lib/python/ai_platform/sessions.py
lib/python/ai_platform/settings.py
lib/python/audit_engine/__init__.py
lib/python/audit_engine/audit_diff.py
lib/python/audit_engine/audit_engine.py
lib/python/audit_engine/audit_history.py
lib/python/audit_engine/audit_registry.py
lib/python/audit_engine/audit_report.py
lib/python/audit_engine/audit_rules.py
lib/python/audit_engine/audit_runner.py
lib/python/audit_engine/audit_score.py
lib/python/autonomous_execution_engine/__init__.py
lib/python/autonomous_execution_engine/engine.py
lib/python/autonomous_execution_engine/evidence.py
lib/python/autonomous_execution_engine/logger.py
lib/python/autonomous_execution_engine/models.py
lib/python/autonomous_execution_engine/persistence.py
lib/python/autonomous_execution_engine/policy.py
lib/python/autonomous_execution_engine/report.py
lib/python/autonomous_execution_engine/rollback.py
lib/python/autonomous_execution_engine/validator.py
lib/python/autonomous_planner/__init__.py
lib/python/autonomous_planner/engine.py
lib/python/autonomous_planning_engine/__init__.py
lib/python/autonomous_planning_engine/batch_planner.py
lib/python/autonomous_planning_engine/decision_engine.py
lib/python/autonomous_planning_engine/dependency_resolver.py
lib/python/autonomous_planning_engine/engine.py
lib/python/autonomous_planning_engine/execution_queue.py
lib/python/autonomous_planning_engine/issue_planner.py
lib/python/autonomous_planning_engine/milestone_planner.py
lib/python/autonomous_planning_engine/models.py
lib/python/autonomous_planning_engine/persistence.py
lib/python/autonomous_planning_engine/pr_planner.py
lib/python/autonomous_planning_engine/priority_optimizer.py
lib/python/autonomous_planning_engine/report.py
lib/python/autonomous_planning_engine/roadmap_planner.py
lib/python/autonomous_workflow_engine.py
lib/python/batch_generator/__init__.py
lib/python/batch_generator/engine.py
lib/python/batch_planner/__init__.py
lib/python/batch_planner/planner.py
lib/python/canonical_audit/__init__.py
lib/python/canonical_audit/engine.py
lib/python/canonical_entities/__init__.py
lib/python/canonical_entities/models.py
lib/python/canonical_entities/uem.py
lib/python/canonical_intelligence/__init__.py
lib/python/canonical_intelligence/engine.py
lib/python/canonical_parser/__init__.py
lib/python/canonical_parser/ast_nodes.py
lib/python/canonical_parser/csl_parser.py
lib/python/canonical_parser/diagnostics.py
lib/python/canonical_parser/lexer.py
lib/python/canonical_parser/parser.py
lib/python/canonical_parser/semantic_analyzer.py
lib/python/canonical_repository/__init__.py
lib/python/canonical_repository/repository.py
lib/python/cdm_engine/__init__.py
lib/python/cdm_engine/engine.py
lib/python/cli/__init__.py
lib/python/cli/engineering.py
lib/python/cli/main.py
lib/python/common/__init__.py
lib/python/common/models.py
lib/python/compliance_engine/__init__.py
lib/python/compliance_engine/engine.py
lib/python/context_synchronization_engine/__init__.py
lib/python/context_synchronization_engine/engine.py
lib/python/context_synchronization_engine/models.py
lib/python/context_synchronization_engine/persistence.py
lib/python/coverage_engine/__init__.py
lib/python/coverage_engine/engine.py
lib/python/csl_engine/__init__.py
lib/python/csl_engine/engine.py
lib/python/css_engine/__init__.py
lib/python/css_engine/engine.py
lib/python/dashboard/__init__.py
lib/python/dashboard/server.py
lib/python/dashboard/service.py
lib/python/decision_engine.py
lib/python/dependency_engine/__init__.py
lib/python/dependency_engine/engine.py
lib/python/dependency_engine/exporter.py
lib/python/dependency_engine/models.py
lib/python/development_state_engine/__init__.py
lib/python/development_state_engine/models.py
lib/python/development_state_engine/repository.py
lib/python/development_state_engine/runtime.py
lib/python/development_validator.py
lib/python/development_validator/__init__.py
lib/python/development_validator/main.py
lib/python/development_validator/parser.py
lib/python/development_validator/report.py
lib/python/development_validator/rules.py
lib/python/discovery_engine/__init__.py
lib/python/discovery_engine/engine.py
lib/python/drift_engine/__init__.py
lib/python/drift_engine/engine.py
lib/python/engineering_engine/__init__.py
lib/python/engineering_engine/acceptance_detector.py
lib/python/engineering_engine/backlog_generator.py
lib/python/engineering_engine/batch_planner_engine.py
lib/python/engineering_engine/build_engine.py
lib/python/engineering_engine/canonical_reference_detector.py
lib/python/engineering_engine/capability_detector.py
lib/python/engineering_engine/compiler.py
lib/python/engineering_engine/deliverable_detector.py
lib/python/engineering_engine/dependency_graph.py
lib/python/engineering_engine/dependency_reasoning_engine.py
lib/python/engineering_engine/dependency_rule_engine.py
lib/python/engineering_engine/engineering_report_engine.py
lib/python/engineering_engine/engineering_task_engine.py
lib/python/engineering_engine/engineering_workflow_engine.py
lib/python/engineering_engine/execution_engine.py
lib/python/engineering_engine/execution_package_generator.py
lib/python/engineering_engine/execution_plan_engine.py
lib/python/engineering_engine/gap_analysis.py
lib/python/engineering_engine/generator_framework.py
lib/python/engineering_engine/github_cli_client.py
lib/python/engineering_engine/github_cli_state_provider.py
lib/python/engineering_engine/github_client.py
lib/python/engineering_engine/github_comparison_engine.py
lib/python/engineering_engine/github_issue_generator.py
lib/python/engineering_engine/github_issue_state_provider.py
lib/python/engineering_engine/github_milestone_generator.py
lib/python/engineering_engine/github_project_planner.py
lib/python/engineering_engine/github_publish_engine.py
lib/python/engineering_engine/github_publish_executor.py
lib/python/engineering_engine/github_publish_script.py
lib/python/engineering_engine/github_real_client.py
lib/python/engineering_engine/github_repository_resolver.py
lib/python/engineering_engine/github_resume_engine.py
lib/python/engineering_engine/github_state_provider.py
lib/python/engineering_engine/github_sync_engine.py
lib/python/engineering_engine/github_sync_planner.py
lib/python/engineering_engine/github_sync_strategy.py
lib/python/engineering_engine/github_transaction_executor.py
lib/python/engineering_engine/github_transaction_log.py
lib/python/engineering_engine/impact_analysis.py
lib/python/engineering_engine/impact_reasoning_engine.py
lib/python/engineering_engine/import_resolver.py
lib/python/engineering_engine/ip_generator.py
lib/python/engineering_engine/knowledge_graph.py
lib/python/engineering_engine/markdown_renderer.py
lib/python/engineering_engine/models.py
lib/python/engineering_engine/package_builder.py
lib/python/engineering_engine/pipeline.py
lib/python/engineering_engine/planning_engine.py
lib/python/engineering_engine/project_exporter.py
lib/python/engineering_engine/project_importer.py
lib/python/engineering_engine/recommendation_engine.py
lib/python/engineering_engine/relationship_extractor.py
lib/python/engineering_engine/repository_audit.py
lib/python/engineering_engine/repository_model.py
lib/python/engineering_engine/repository_scanner.py
lib/python/engineering_engine/review_engine.py
lib/python/engineering_engine/roadmap_engine.py
lib/python/engineering_engine/rule_engine.py
lib/python/engineering_engine/scm_provider.py
lib/python/engineering_engine/scope_detector.py
lib/python/engineering_engine/semantic_classifier.py
lib/python/engineering_engine/semantic_entities.py
lib/python/engineering_engine/semantic_extractor.py
lib/python/engineering_engine/semantic_query_engine.py
lib/python/engineering_engine/semantic_repository_builder.py
lib/python/engineering_engine/validation_engine.py
lib/python/engineering_engine/validation_plan_engine.py
lib/python/engineering_workspace/__init__.py
lib/python/engineering_workspace/capabilities.py
lib/python/engineering_workspace/context.py
lib/python/engineering_workspace/dashboard.py
lib/python/engineering_workspace/diagnostics.py
lib/python/engineering_workspace/events.py
lib/python/engineering_workspace/knowledge.py
lib/python/engineering_workspace/manager.py
lib/python/engineering_workspace/models.py
lib/python/engineering_workspace/permissions.py
lib/python/engineering_workspace/persistence.py
lib/python/engineering_workspace/providers.py
lib/python/engineering_workspace/providers/__init__.py
lib/python/engineering_workspace/providers/filesystem_provider.py
lib/python/engineering_workspace/providers/github_provider.py
lib/python/engineering_workspace/providers/local_repository_provider.py
lib/python/engineering_workspace/providers/railway_provider.py
lib/python/engineering_workspace/providers/terminal_provider.py
lib/python/engineering_workspace/registry.py
lib/python/engineering_workspace/repository.py
lib/python/engineering_workspace/runtime.py
lib/python/engineering_workspace/service.py
lib/python/engineering_workspace/workspace.py
lib/python/epistemic/__init__.py
lib/python/epistemic/capability.py
lib/python/epistemic/memory.py
lib/python/epistemic/memory/__init__.py
lib/python/epistemic/memory/model.py
lib/python/epistemic/memory/store.py
lib/python/epistemic/session.py
lib/python/epistemic/transformation.py
lib/python/epistemic/witness.py
lib/python/evidence_engine/__init__.py
lib/python/evidence_engine/engine.py
lib/python/executable_repository_intelligence/__init__.py
lib/python/executable_repository_intelligence/engine.py
lib/python/executable_repository_intelligence/executable_dep_graph.py
lib/python/executable_repository_intelligence/file_classifier.py
lib/python/executable_repository_intelligence/injection_safety.py
lib/python/executable_repository_intelligence/models.py
lib/python/executable_repository_intelligence/persistence.py
lib/python/executable_repository_intelligence/recommendations.py
lib/python/executable_repository_intelligence/report.py
lib/python/executable_repository_intelligence/runtime_map.py
lib/python/executable_repository_intelligence/zone_classifier.py
lib/python/execution_coordinator/__init__.py
lib/python/execution_coordinator/engine.py
lib/python/execution_engine/__init__.py
lib/python/execution_engine/engine.py
lib/python/executive_briefing_engine/__init__.py
lib/python/executive_briefing_engine/decision_tracker.py
lib/python/executive_briefing_engine/engine.py
lib/python/executive_briefing_engine/generator.py
lib/python/executive_briefing_engine/insight_generator.py
lib/python/executive_briefing_engine/models.py
lib/python/executive_briefing_engine/persistence.py
lib/python/executive_briefing_engine/priority_engine.py
lib/python/executive_briefing_engine/recommendation_engine.py
lib/python/executive_briefing_engine/risk_analyzer.py
lib/python/foundation_audit.py
lib/python/foundation_audit/__init__.py
lib/python/foundation_audit/checks.py
lib/python/foundation_audit/main.py
lib/python/github_materialization/__init__.py
lib/python/github_materialization/engine.py
lib/python/knowledge_engine/__init__.py
lib/python/knowledge_engine/database.py
lib/python/knowledge_engine/engine.py
lib/python/knowledge_engine/models.py
lib/python/knowledge_graph/__init__.py
lib/python/knowledge_graph/builder.py
lib/python/knowledge_graph/graph.py
lib/python/knowledge_graph_engine.py
lib/python/knowledge_graph_v2/__init__.py
lib/python/knowledge_graph_v2/engine.py
lib/python/knowledge_materialization/__init__.py
lib/python/knowledge_materialization/engine.py
lib/python/memory_engine.py
lib/python/planning_engine/__init__.py
lib/python/planning_engine/engine.py
lib/python/planning_engine/exporter.py
lib/python/planning_engine/models.py
lib/python/planning_optimizer/__init__.py
lib/python/planning_optimizer/engine.py
lib/python/profiler/__init__.py
lib/python/profiler/engine.py
lib/python/progress_monitor/__init__.py
lib/python/progress_monitor/engine.py
lib/python/project_profiles/__init__.py
lib/python/project_profiles/trading_signals.py
lib/python/recommendation_engine/__init__.py
lib/python/recommendation_engine/engine.py
lib/python/reporting_engine/__init__.py
lib/python/reporting_engine/engine.py
lib/python/repository_engine/__init__.py
lib/python/repository_engine/classifier.py
lib/python/repository_engine/cli.py
lib/python/repository_engine/deps.py
lib/python/repository_engine/engine.py
lib/python/repository_engine/exporter.py
lib/python/repository_engine/metrics.py
lib/python/repository_engine/models.py
lib/python/repository_engine/report.py
lib/python/repository_engine/serializer.py
lib/python/repository_hygiene_audit.py
lib/python/repository_inspector_v2/__init__.py
lib/python/repository_inspector_v2/analyzer.py
lib/python/repository_inspector_v2/engine.py
lib/python/repository_inspector_v2/report.py
lib/python/repository_inventory.py
lib/python/repository_profile.py
lib/python/review_agent/__init__.py
lib/python/review_agent/engine.py
lib/python/rule_engine/__init__.py
lib/python/rule_engine/base.py
lib/python/rule_engine/engine.py
lib/python/rule_engine/governance_kernel.py
lib/python/rule_engine/models.py
lib/python/rule_engine/rules/repository_size_rule.py
lib/python/rule_engine/rules/validation_rule.py
lib/python/runtime/__init__.py
lib/python/runtime/bootstrap.py
lib/python/runtime/config.py
lib/python/runtime/diagnostics.py
lib/python/runtime/event_dispatcher.py
lib/python/runtime/event_loop.py
lib/python/runtime/health.py
lib/python/runtime/identity.py
lib/python/runtime/interfaces/__init__.py
lib/python/runtime/interfaces/api_auth.py
lib/python/runtime/interfaces/github_webhook.py
lib/python/runtime/interfaces/graphql/__init__.py
lib/python/runtime/interfaces/http_server.py
lib/python/runtime/interfaces/mcp/__init__.py
lib/python/runtime/interfaces/runtime_api.py
lib/python/runtime/interfaces/telegram_gateway.py
lib/python/runtime/job_queue.py
lib/python/runtime/lifecycle.py
lib/python/runtime/logging_service.py
lib/python/runtime/metrics.py
lib/python/runtime/process.py
lib/python/runtime/railway.py
lib/python/runtime/recovery.py
lib/python/runtime/registry.py
lib/python/runtime/reports.py
lib/python/runtime/scheduler.py
lib/python/runtime/secrets.py
lib/python/runtime/shutdown.py
lib/python/runtime/state.py
lib/python/runtime/supervisor.py
lib/python/self_evaluation_engine/__init__.py
lib/python/self_evaluation_engine/analyzers.py
lib/python/self_evaluation_engine/engine.py
lib/python/self_evaluation_engine/models.py
lib/python/self_evaluation_engine/persistence.py
lib/python/self_evaluation_engine/report.py
lib/python/self_evaluation_engine/scoring.py
lib/python/self_improvement_engine/__init__.py
lib/python/self_improvement_engine/analyzers.py
lib/python/self_improvement_engine/engine.py
lib/python/self_improvement_engine/generators.py
lib/python/self_improvement_engine/models.py
lib/python/self_improvement_engine/persistence.py
lib/python/self_improvement_engine/report.py
lib/python/semantic_engine/__init__.py
lib/python/semantic_engine/engine.py
lib/python/semantic_matching/__init__.py
lib/python/semantic_matching/matcher.py
lib/python/semantic_repository_intelligence/__init__.py
lib/python/semantic_repository_intelligence/architecture_graph.py
lib/python/semantic_repository_intelligence/ast_analyzer.py
lib/python/semantic_repository_intelligence/call_graph.py
lib/python/semantic_repository_intelligence/confidence_engine.py
lib/python/semantic_repository_intelligence/dependency_graph.py
lib/python/semantic_repository_intelligence/engine.py
lib/python/semantic_repository_intelligence/import_graph.py
lib/python/semantic_repository_intelligence/injection_point_analyzer.py
lib/python/semantic_repository_intelligence/models.py
lib/python/semantic_repository_intelligence/persistence.py
lib/python/semantic_repository_intelligence/recommendation_engine.py
lib/python/semantic_repository_intelligence/relationship_resolver.py
lib/python/session_runtime/__init__.py
lib/python/session_runtime/models.py
lib/python/session_runtime/runtime.py
lib/python/session_runtime/storage.py
lib/python/validation_engine/__init__.py
lib/python/validation_engine/csl_validator.py
lib/python/validation_engine/engine.py
lib/python/validation_engine/exporter.py
lib/python/validation_engine/models.py
lib/python/workspace_index/__init__.py
lib/python/workspace_index/builder.py
lib/python/workspace_index/exporter.py
lib/python/workspace_index/incremental.py
lib/python/workspace_index/models.py
lib/python/workspace_index/policy.py
lib/python/workspace_manager/__init__.py
lib/python/workspace_manager/engine.py
lib/python/workspace_orchestrator/__init__.py
lib/python/workspace_orchestrator/dashboard.py
lib/python/workspace_orchestrator/dependency_graph.py
lib/python/workspace_orchestrator/engine.py
lib/python/workspace_orchestrator/intelligence.py
lib/python/workspace_orchestrator/models.py
lib/python/workspace_orchestrator/persistence.py
lib/python/workspace_orchestrator/registry.py
lib/python/workspace_orchestrator/scanner.py
lib/python/workspace_orchestrator/state_manager.py
lib/repository_inspector.sh
lib/repository_profile_engine.sh
lib/repository_summary.sh
lib/review_engine.sh
lib/work_engine.sh
lib/workspace_engine.sh
railway.json
standards/cdm/shared/schemas/document.schema.json
standards/cdm/shared/schemas/header.schema.json
standards/cdm/shared/schemas/metadata.schema.json
standards/cdm/shared/schemas/relationship.schema.json
standards/cdm/shared/templates/canonical_header.yaml
standards/csl/meta/ARCHITECTURE.yaml
test_csl_grammar.py
test_csl_semantic.py
tests/engineering/test_backlog_pipeline.py
tests/engineering/test_project_export_import.py
tests/engineering/test_task_pipeline.py
tests/epistemic/test_capability.py
tests/epistemic/test_memory.py
tests/test_agent_cli.sh
tests/test_agent_runtime.sh
tests/test_ai_cto_scanner.sh
tests/test_ai_platform.sh
tests/test_autonomous_execution_engine.sh
tests/test_autonomous_planner.sh
tests/test_autonomous_planning_engine.sh
tests/test_autonomous_workflow.sh
tests/test_batch_generator.sh
tests/test_batch_planner.sh
tests/test_batch_serialization.sh
tests/test_canonical_audit.sh
tests/test_canonical_execution_stack.sh
tests/test_canonical_intelligence.sh
tests/test_canonical_parser.sh
tests/test_canonical_repository.sh
tests/test_cli.sh
tests/test_common_models.sh
tests/test_compliance_engine.sh
tests/test_context_synchronization_engine.sh
tests/test_coverage_engine.sh
tests/test_csl_governance_kernel.sh
tests/test_csl_level1_reader.sh
tests/test_csl_level2_validator.sh
tests/test_csl_level3_compiler.sh
tests/test_dashboard.sh
tests/test_dashboard_cli.sh
tests/test_dashboard_navigation.sh
tests/test_decision_engine.sh
tests/test_dependency_engine.sh
tests/test_development_agent.sh
tests/test_development_report.sh
tests/test_development_state_engine_models.sh
tests/test_development_state_persistence.sh
tests/test_development_state_runtime.sh
tests/test_development_state_runtime_integration.sh
tests/test_development_validator.sh
tests/test_development_validator_v2.sh
tests/test_discovery_engine.sh
tests/test_drift_engine.sh
tests/test_engineering_explorer.sh
tests/test_engineering_session.sh
tests/test_evidence_engine.sh
tests/test_executable_repository_intelligence.sh
tests/test_execution_coordinator.sh
tests/test_execution_engine.sh
tests/test_executive_briefing_engine.sh
tests/test_foundation_audit.sh
tests/test_foundation_audit_v2.sh
tests/test_github_materialization.sh
tests/test_incremental_workspace.sh
tests/test_integration_pipeline.sh
tests/test_knowledge_engine_v2.sh
tests/test_knowledge_graph.sh
tests/test_knowledge_graph_canonical.sh
tests/test_knowledge_graph_v2.sh
tests/test_markdown_report.sh
tests/test_memory_engine.sh
tests/test_planning_engine.sh
tests/test_planning_optimizer.sh
tests/test_profiler.sh
tests/test_progress_monitor.sh
tests/test_project_manager.sh
tests/test_python_packages.sh
tests/test_railway_bootstrap.sh
tests/test_recommendation_engine.sh
tests/test_reporting_engine.sh
tests/test_repository_analysis.sh
tests/test_repository_engine_inspect.sh
tests/test_repository_engine_v2.sh
tests/test_repository_hygiene.sh
tests/test_repository_inspector.sh
tests/test_repository_inspector_v2.sh
tests/test_repository_integration_dashboard.sh
tests/test_repository_inventory.sh
tests/test_repository_profile.sh
tests/test_repository_profile_python.sh
tests/test_review_agent.sh
tests/test_rule_engine.sh
tests/test_runtime_acceptance.sh
tests/test_runtime_bootstrap.sh
tests/test_runtime_dashboard_navigation.sh
tests/test_runtime_health.sh
tests/test_runtime_layout.sh
tests/test_runtime_lifecycle.sh
tests/test_runtime_loop.sh
tests/test_runtime_recovery.sh
tests/test_runtime_regression.sh
tests/test_runtime_scheduler.sh
tests/test_runtime_shutdown.sh
tests/test_runtime_telegram.sh
tests/test_runtime_webhooks.sh
tests/test_self_evaluation_engine.sh
tests/test_self_improvement_engine.sh
tests/test_semantic_engine.sh
tests/test_semantic_matching.sh
tests/test_semantic_repository_intelligence.sh
tests/test_session_runtime.sh
tests/test_steps_definition.sh
tests/test_trading_profile.sh
tests/test_validation_engine.sh
tests/test_workspace.sh
tests/test_workspace_index.sh
tests/test_workspace_manager.sh
tests/test_workspace_orchestrator.sh
tests/test_workspace_profile.sh
tools/engineering/generate_repository_audit.py
work/runtime/organism-runtime.sh
work/scripts/pcc01_primary_source_audit.sh
```

## 5. Existing Experience and Related Organ References

### Term: `experience`

```text
lib/python/epistemic/memory/model.py:6: It represents one preserved experience.
lib/python/epistemic/memory.py:6:     Preserve an experience exactly as it was received.
lib/python/epistemic/memory.py:39:         "# First Memory\n\nThe organism preserved its first experience.\n",
tests/epistemic/test_memory.py:11:         content="The organism preserved an experience.",
```

Matches: 4

### Term: `persistent experience`

```text
NO MATCHES
```

Matches: 0

### Term: `experience_id`

```text
NO MATCHES
```

Matches: 0

### Term: `experienceid`

```text
NO MATCHES
```

Matches: 0

### Term: `experience_store`

```text
NO MATCHES
```

Matches: 0

### Term: `experience_repository`

```text
NO MATCHES
```

Matches: 0

### Term: `experience_service`

```text
NO MATCHES
```

Matches: 0

### Term: `session`

```text
.ai/audit/dependency_graph.json:544:     "target": ".ai/work/session.md",
.ai/audit/repository_inventory_v2.json:687:     "path": ".ai/work/session.md",
.ai/audit/repository_inventory_v2.json:688:     "name": "session.md",
.ai/development_state/executive_snapshot.json:131:         "next_core": "CORE-009 — Development State Engine: Persist full development state for cross-session reasoning.",
.ai/executive/briefing.json:65:       "context": "Semantic recommendation: CORE-009 — Development State Engine: Persist full development state for cross-session reasoning.. Current context recommendation: CORE-005.",
.ai/executive/briefing.json:66:       "description": "Semantic analysis recommends implementing CORE-009 — Development State Engine: Persist full development state for cross-session reasoning. as the next CORE module, but the current recommendation is 'CORE-005'.",
.ai/executive/briefing.json:70:         "Proceed with CORE-009 — Development State Engine: Persist full development state for cross-session reasoning. as recommended by semantic analysis",
.ai/executive/briefing.json:74:       "recommended_option": "Proceed with CORE-009 — Development State Engine: Persist full development state for cross-session reasoning. as recommended by semantic analysis",
.ai/executive/briefing.json:75:       "title": "Confirm next CORE module: CORE-009 — Development State Engine: Persist full development state for cross-session reasoning.",
.ai/executive/briefing.json:145:       "description": "Semantic analysis suggests CORE-009 — Development State Engine: Persist full development state for cross-session reasoning. as the next CORE implementation.",
.ai/executive/briefing.json:147:         "suggested_next_core=CORE-009 — Development State Engine: Persist full development state for cross-session reasoning."
.ai/executive/briefing.json:154:       "title": "Implement CORE-009 — Development State Engine: Persist full development state for cross-session reasoning. as the next CORE module"
.ai/executive/briefing.json:162:   "suggested_next_core": "CORE-009 — Development State Engine: Persist full development state for cross-session reasoning.",
.ai/executive/owner_actions.json:16:       "context": "Semantic recommendation: CORE-009 — Development State Engine: Persist full development state for cross-session reasoning.. Current context recommendation: CORE-005.",
.ai/executive/owner_actions.json:17:       "description": "Semantic analysis recommends implementing CORE-009 — Development State Engine: Persist full development state for cross-session reasoning. as the next CORE module, but the current recommendation is 'CORE-005'.",
.ai/executive/owner_actions.json:21:         "Proceed with CORE-009 — Development State Engine: Persist full development state for cross-session reasoning. as recommended by semantic analysis",
.ai/executive/owner_actions.json:25:       "recommended_option": "Proceed with CORE-009 — Development State Engine: Persist full development state for cross-session reasoning. as recommended by semantic analysis",
.ai/executive/owner_actions.json:26:       "title": "Confirm next CORE module: CORE-009 — Development State Engine: Persist full development state for cross-session reasoning.",
.ai/executive/recommendations.json:47:       "description": "Semantic analysis suggests CORE-009 — Development State Engine: Persist full development state for cross-session reasoning. as the next CORE implementation.",
.ai/executive/recommendations.json:49:         "suggested_next_core=CORE-009 — Development State Engine: Persist full development state for cross-session reasoning."
.ai/executive/recommendations.json:56:       "title": "Implement CORE-009 — Development State Engine: Persist full development state for cross-session reasoning. as the next CORE module"
.ai/reports/inspect-20260807.json:562:       "path": ".ai/sessions/SESSION-20260803-050009.json",
.ai/reports/inspect-20260807.json:569:       "path": ".ai/sessions/SESSION-20260803-050013.json",
.ai/semantic_knowledge.json:93:     "next_core": "CORE-009 — Development State Engine: Persist full development state for cross-session reasoning."
.ai/sessions/SESSION-20260803-050009.json:2:   "identifier": "SESSION-20260803-050009",
.ai/sessions/SESSION-20260803-050013.json:2:   "identifier": "SESSION-20260803-050013",
lib/issue_engine.sh:46: echo "[6/7] Prepare work session"
lib/python/ai_cto_scanner/detectors.py:369:         ("Session Management", [
lib/python/ai_cto_scanner/detectors.py:375:             "path:session",
lib/python/ai_cto_scanner/report.py:276:             ("State", "State Readiness", "Implement state persistence and session management"),
lib/python/ai_cto_scanner/scoring.py:49:         persist_components = self._filter_components(state, ["Persistence", "State Store", "Session Management"])
lib/python/ai_platform/service.py:75:             session = self.sessions.append_interaction(session_id, effective_question, result["answer"], result["usage"])
lib/python/ai_platform/service.py:78:             session = self.sessions.create(
lib/python/ai_platform/service.py:93:             session = self.sessions.append_interaction(session["id"], effective_question, result["answer"], result["usage"])
lib/python/ai_platform/service.py:95:             "session_id": session["id"],
lib/python/ai_platform/service.py:123:         for session in sessions:
lib/python/ai_platform/service.py:124:             for usage in session.get("token_usage", []):
lib/python/ai_platform/sessions.py:17:         session = {
lib/python/ai_platform/sessions.py:18:             "id": payload.get("id", f"AI-SESSION-{uuid4().hex[:12].upper()}"),
lib/python/ai_platform/sessions.py:36:         self._save(session)
lib/python/ai_platform/sessions.py:37:         return session
lib/python/ai_platform/sessions.py:44:             session = self._read(path)
lib/python/ai_platform/sessions.py:45:             if session:
lib/python/ai_platform/sessions.py:46:                 items.append(session)
lib/python/ai_platform/sessions.py:54:         session = self.get(session_id)
lib/python/ai_platform/sessions.py:55:         if not session:
lib/python/ai_platform/sessions.py:56:             raise ValueError(f"unknown session {session_id}")
lib/python/ai_platform/sessions.py:58:         session.setdefault("prompt_history", []).append(question)
lib/python/ai_platform/sessions.py:59:         session.setdefault("conversation_history", []).append({"question": question, "answer": answer, "timestamp": now})
lib/python/ai_platform/sessions.py:60:         session.setdefault("token_usage", []).append(dict(usage))
lib/python/ai_platform/sessions.py:61:         session["updated_at"] = now
lib/python/ai_platform/sessions.py:62:         self._save(session)
lib/python/ai_platform/sessions.py:63:         return session
lib/python/ai_platform/sessions.py:65:     def _save(self, session: Mapping[str, Any]) -> None:
lib/python/ai_platform/sessions.py:67:         path = self.dir / f"{session['id']}.json"
lib/python/ai_platform/sessions.py:68:         path.write_text(json.dumps(dict(session), indent=2), encoding="utf-8")
lib/python/context_synchronization_engine/engine.py:1107:                     "/session",
lib/python/dashboard/server.py:64:         if path == "/session":
lib/python/dashboard/server.py:105:             "/engineering-session": "/session",
lib/python/dashboard/service.py:52:         description="Aggregates repository, workspace, reports, and engineering-session context into a single local application.",
lib/python/dashboard/service.py:56:         dependencies=["repository-engine", "engineering-session", "project-manager"],
lib/python/dashboard/service.py:60:         dashboard_pages=["/", "/projects", "/session", "/explorer", "/reports", "/runtime", "/diagnostics"],
lib/python/dashboard/service.py:101:         slug="engineering-session",
lib/python/dashboard/service.py:102:         title="Engineering Session",
lib/python/dashboard/service.py:104:         description="Shows current project, repository, branch, sprint, epic, task, runtime, AI provider, and session history.",
lib/python/dashboard/service.py:105:         architecture="Reads development state, recent events, sessions, and git context to reconstruct a live engineering session view.",
lib/python/dashboard/service.py:106:         inputs=["development state", "session artifacts", "git metadata"],
lib/python/dashboard/service.py:107:         outputs=["session summary", "session history", "recent activity"],
lib/python/dashboard/service.py:112:         dashboard_pages=["/session", "/"],
lib/python/dashboard/service.py:113:         future_roadmap="Turn session history into a full operational timeline and resumable workflow console.",
lib/python/dashboard/service.py:115:         next_milestone="Session actions and resumable execution controls.",
lib/python/dashboard/service.py:119:         why_problem="Every engineering action should belong to a visible and resumable session.",
lib/python/dashboard/service.py:120:         why_architecture="The development-state artifacts already encode session context and recent changes.",
lib/python/dashboard/service.py:187:         dashboard_pages=["/", "/session", "/runtime", "/diagnostics"],
lib/python/dashboard/service.py:196:         why_dependencies="Session state and report generation depend on runtime information being visible.",
lib/python/dashboard/service.py:352:         session = self._load_session(
lib/python/dashboard/service.py:359:         runtime = self._load_runtime(session, workspace, engineering_context=engineering_context)
lib/python/dashboard/service.py:363:             session,
lib/python/dashboard/service.py:373:             "home": self._home_payload(repository, workspace, session, reports, runtime, diagnostics),
lib/python/dashboard/service.py:375:             "session": session,
lib/python/dashboard/service.py:395:                 self._section("Engineering Session", self._definition_list(home["session_overview"])),
lib/python/dashboard/service.py:436:                     ("Session", result.get("session_id", "")),
lib/python/dashboard/service.py:459:         session = data["session"]
lib/python/dashboard/service.py:461:             "Engineering Session",
lib/python/dashboard/service.py:464:                 self._summary_grid(session["summary_cards"]),
lib/python/dashboard/service.py:465:                 self._section("Session History", self._session_history(session["session_history"])),
lib/python/dashboard/service.py:466:                 self._section("Recent Activity", self._activity_table(session["recent_activity"])),
lib/python/dashboard/service.py:806:         session: Mapping[str, Any],
lib/python/dashboard/service.py:828:                 "current_project": session.get("current_project", self.repository_root.name),
lib/python/dashboard/service.py:830:                     "project": session.get("current_project", self.repository_root.name),
lib/python/dashboard/service.py:831:                     "repository": session.get("current_repository", self.repository_root.name),
lib/python/dashboard/service.py:832:                     "branch": session.get("current_branch", ""),
lib/python/dashboard/service.py:833:                     "task": session.get("current_engineering_task", ""),
lib/python/dashboard/service.py:834:                     "identifier": session.get("session_history", [{}])[0].get("identifier", "") if session.get("session_history") else "",
lib/python/dashboard/service.py:835:                     "status": session.get("session_history", [{}])[0].get("status", "") if session.get("session_history") else "",
lib/python/dashboard/service.py:882:             ("Current Session", runtime_payload.get("current_session", {}).get("identifier", "") or runtime_payload.get("current_session", {}).get("task", "") or "n/a"),
lib/python/dashboard/service.py:924:         session: Mapping[str, Any],
lib/python/dashboard/service.py:948:                 and definition.slug in {"dashboard", "runtime", "engineering-session", "project-manager"}
lib/python/dashboard/service.py:968:                     "current_pull_request": session.get("current_branch", "") if session.get("current_branch", "") not in {"main", "master"} else "",
lib/python/dashboard/service.py:980:                     "related_issues": [session.get("current_issue", "")] if session.get("current_issue") else [],
lib/python/dashboard/service.py:1038:         session: Mapping[str, Any],
lib/python/dashboard/service.py:1046:                 {"label": "Welcome", "value": f"Engineering Operating System · {session['current_project']}"},
lib/python/dashboard/service.py:1047:                 {"label": "Current Engineering Session", "value": runtime.get("current_session", {}).get("identifier", "") or session["current_engineering_task"] or "n/a"},
lib/python/dashboard/service.py:1048:                 {"label": "Current Project", "value": session["current_project"]},
lib/python/dashboard/service.py:1049:                 {"label": "Current Repository", "value": session["current_repository"]},
lib/python/dashboard/service.py:1050:                 {"label": "Current Branch", "value": session["current_branch"] or "n/a"},
lib/python/dashboard/service.py:1051:                 {"label": "Current Engineering Task", "value": session["current_engineering_task"] or "n/a"},
lib/python/dashboard/service.py:1053:                 {"label": "Current Runtime Status", "value": runtime.get("state", session["current_runtime_status"])},
lib/python/dashboard/service.py:1054:                 {"label": "Current Sprint", "value": session["current_sprint"] or "n/a"},
lib/python/dashboard/service.py:1055:                 {"label": "Current Epic", "value": session["current_epic"] or "n/a"},
lib/python/dashboard/service.py:1056:                 {"label": "Current Issue", "value": session["current_issue"] or "n/a"},
lib/python/dashboard/service.py:1057:                 {"label": "Current AI Provider", "value": session["current_ai_provider"]},
lib/python/dashboard/service.py:1059:                 {"label": "Recent Activity", "value": str(len(session["recent_activity"]))},
lib/python/dashboard/service.py:1065:                 ("Current Project", session["current_project"]),
lib/python/dashboard/service.py:1066:                 ("Current Repository", session["current_repository"]),
lib/python/dashboard/service.py:1067:                 ("Current Workspace", session["current_workspace"]),
lib/python/dashboard/service.py:1068:                 ("Current Branch", session["current_branch"]),
lib/python/dashboard/service.py:1069:                 ("Current Engineering Session", runtime.get("current_session", {}).get("identifier", "") or "n/a"),
lib/python/dashboard/service.py:1070:                 ("Current Sprint", session["current_sprint"] or "n/a"),
lib/python/dashboard/service.py:1071:                 ("Current Epic", session["current_epic"] or "n/a"),
lib/python/dashboard/service.py:1072:                 ("Current Issue", session["current_issue"] or "n/a"),
lib/python/dashboard/service.py:1073:                 ("Current AI Provider", session["current_ai_provider"]),
lib/python/dashboard/service.py:1086:                 ("Current Project", session["current_project"]),
lib/python/dashboard/service.py:1088:                 ("Runtime Status", runtime.get("state", session["current_runtime_status"])),
lib/python/dashboard/service.py:1089:                 ("Current Sprint", session["current_sprint"] or "n/a"),
lib/python/dashboard/service.py:1090:                 ("Current Epic", session["current_epic"] or "n/a"),
lib/python/dashboard/service.py:1091:                 ("Current Issue", session["current_issue"] or "n/a"),
lib/python/dashboard/service.py:1092:                 ("Current AI Provider", session["current_ai_provider"]),
lib/python/dashboard/service.py:1097:             "recent_activity": session["recent_activity"],
lib/python/dashboard/service.py:1114:             {"href": "/engineering-session", "label": "Engineering Session"},
lib/python/dashboard/service.py:1375:             rows.append("<tr><td colspan=\"4\">No session history available.</td></tr>")
lib/python/dashboard/service.py:1376:         return "<table><thead><tr><th>Session</th><th>Status</th><th>Repository</th><th>Completed Steps</th></tr></thead><tbody>" + "".join(rows) + "</tbody></table>"
lib/python/dashboard/service.py:1450:         return "<table><thead><tr><th>Session</th><th>Project</th><th>Repository</th><th>Branch</th><th>Provider</th><th>Model</th><th>Messages</th></tr></thead><tbody>" + "".join(rows) + "</tbody></table>"
lib/python/engineering_workspace/workspace.py:108:     # Session
lib/python/engineering_workspace/workspace.py:112:     def session(self) -> Any:
lib/python/epistemic/memory/model.py:24:     session: str
lib/python/epistemic/memory/store.py:33:         session,
lib/python/epistemic/memory/store.py:49:             session=session,
lib/python/epistemic/session.py:2: Epistemic Session
lib/python/epistemic/session.py:4: A Session groups a continuous sequence of events into a single
lib/python/epistemic/session.py:9: Session gives those events a beginning, an end and a purpose.
lib/python/epistemic/session.py:20: class Session:
lib/python/epistemic/session.py:39:         session = Session(
lib/python/epistemic/session.py:41:             identifier=f"SESSION-{uuid.uuid4().hex[:8].upper()}",
lib/python/epistemic/session.py:55:             session.identifier,
lib/python/epistemic/session.py:61:         return session
lib/python/epistemic/session.py:63:     def close(self, session: Session):
lib/python/epistemic/session.py:69:             session.identifier,
lib/python/epistemic/session.py:71:             result="Session completed.",
lib/python/epistemic/session.py:75:         session.status = "CLOSED"
lib/python/epistemic/session.py:77:         return session
lib/python/epistemic/session.py:84:     session = manager.open(
lib/python/epistemic/session.py:86:         "Create the first executable session."
lib/python/epistemic/session.py:90:     manager.close(session)
lib/python/epistemic/session.py:96:     print("SESSION")
lib/python/epistemic/session.py:100:     print(session)
lib/python/executable_repository_intelligence/runtime_map.py:32:     re.compile(r"Session\s*\(|engine\s*=|create_engine|database\s*=", re.IGNORECASE),
lib/python/runtime/diagnostics.py:254:             "Expose richer session controls from the dashboard.",
lib/python/runtime/interfaces/http_server.py:98:             "/session",
lib/python/runtime/interfaces/http_server.py:298:         if normalized_path == "/session":
lib/python/runtime/interfaces/http_server.py:323:             "/engineering-session": "/session",
lib/python/semantic_repository_intelligence/architecture_graph.py:79:         ("path_contains", "session"),
lib/python/semantic_repository_intelligence/engine.py:39:      "Persist full development state for cross-session reasoning."),
lib/python/session_runtime/__init__.py:2: Session Runtime
lib/python/session_runtime/models.py:5: class Session:
lib/python/session_runtime/runtime.py:3: from .models import Session
lib/python/session_runtime/runtime.py:15:             "SESSION-%Y%m%d-%H%M%S"
lib/python/session_runtime/runtime.py:18:         session = Session(
lib/python/session_runtime/runtime.py:23:         self.storage.save(session)
lib/python/session_runtime/runtime.py:25:         return session
lib/python/session_runtime/runtime.py:27:     def checkpoint(self, session, step):
lib/python/session_runtime/runtime.py:29:         if step not in session.completed_steps:
lib/python/session_runtime/runtime.py:30:             session.completed_steps.append(step)
lib/python/session_runtime/runtime.py:32:         self.storage.save(session)
lib/python/session_runtime/runtime.py:34:         return session
lib/python/session_runtime/storage.py:12:     def save(self, session):
lib/python/session_runtime/storage.py:14:         path = self.ROOT / f"{session.identifier}.json"
lib/python/session_runtime/storage.py:17:             json.dumps(session.__dict__, indent=2),
lib/work_engine.sh:29: echo "[4/4] Work session..."
lib/work_engine.sh:31: cat > "$WORKDIR/session.md" <<EOT
lib/work_engine.sh:32: # AI Work Session
lib/work_engine.sh:46: echo "WORK SESSION READY"
lib/workspace_engine.sh:36: session.md \
tests/epistemic/test_memory.py:13:         session="SESSION-000001",
tests/epistemic/test_memory.py:27:     assert restored.session == "SESSION-000001"
tests/test_context_synchronization_engine.sh:110:             "next_core": "CORE-009 — Development State Engine: Persist full development state for cross-session reasoning.",
tests/test_dashboard_navigation.sh:25:         "/engineering-session": "Engineering Session",
tests/test_dashboard_navigation.sh:26:         "/session": "Engineering Session",
tests/test_development_state_persistence.sh:104:                 session_id="session-1",
tests/test_engineering_explorer.sh:14: for slug in ["dashboard", "project-manager", "engineering-session", "engineering-explorer", "repository-engine"]:
tests/test_engineering_session.sh:11: session = payload["session"]
tests/test_engineering_session.sh:13: assert session["current_project"] == "AI-Toolkit"
tests/test_engineering_session.sh:14: assert session["current_repository"]
tests/test_engineering_session.sh:15: assert session["current_branch"]
tests/test_engineering_session.sh:16: assert session["current_workspace"]
tests/test_engineering_session.sh:17: assert session["current_sprint"]
tests/test_engineering_session.sh:18: assert session["current_epic"]
tests/test_engineering_session.sh:19: assert session["current_engineering_task"]
tests/test_engineering_session.sh:20: assert session["current_runtime"]
tests/test_engineering_session.sh:21: assert session["current_ai_provider"]
tests/test_engineering_session.sh:22: assert session["session_history"], "expected persisted session history"
tests/test_engineering_session.sh:23: assert session["recent_activity"], "expected recent activity"
tests/test_engineering_session.sh:24: print("engineering session PASS")
tests/test_runtime_dashboard_navigation.sh:43:         "/engineering-session": "Engineering Session",
tests/test_runtime_layout.sh:90: assert_no_repo_regex "\\.ai/batches/.*(execution_state|checkpoint|profil|session|cache|log|temporary|temp)"
tests/test_session_runtime.sh:13: session = runtime.create(".")
tests/test_session_runtime.sh:15: runtime.checkpoint(session,"inspect")
tests/test_session_runtime.sh:16: runtime.checkpoint(session,"validation")
tests/test_session_runtime.sh:17: runtime.checkpoint(session,"planning")
tests/test_session_runtime.sh:21: print("Session :", session.identifier)
tests/test_session_runtime.sh:25: for step in session.completed_steps:
tests/test_session_runtime.sh:30: print("Session Runtime PASS")
```

Matches: 212

### Term: `memory`

```text
.ai/audit/dependency_graph.json:585:     "source": ".ai/memory",
.ai/audit/dependency_graph.json:586:     "target": ".ai/memory/repository_profile_1.json",
.ai/audit/dependency_graph.json:591:     "source": ".ai/memory",
.ai/audit/dependency_graph.json:592:     "target": ".ai/memory/history.json",
.ai/audit/dependency_graph.json:597:     "source": ".ai/memory",
.ai/audit/dependency_graph.json:598:     "target": ".ai/memory/repository_profile_2.json",
.ai/audit/dependency_graph.json:603:     "source": ".ai/memory",
.ai/audit/dependency_graph.json:604:     "target": ".ai/memory/index.json",
.ai/audit/dependency_graph.json:609:     "source": ".ai/memory",
.ai/audit/dependency_graph.json:610:     "target": ".ai/memory/knowledge_graph.json",
.ai/audit/dependency_graph.json:615:     "source": ".ai/memory",
.ai/audit/dependency_graph.json:616:     "target": ".ai/memory/decision.json",
.ai/audit/dependency_graph.json:621:     "source": ".ai/memory",
.ai/audit/dependency_graph.json:622:     "target": ".ai/memory/workflow.json",
.ai/audit/repository_inventory_v2.json:333:     "path": ".ai/memory",
.ai/audit/repository_inventory_v2.json:334:     "name": "memory",
.ai/audit/repository_inventory_v2.json:729:     "path": ".ai/memory/repository_profile_1.json",
.ai/audit/repository_inventory_v2.json:735:     "path": ".ai/memory/history.json",
.ai/audit/repository_inventory_v2.json:741:     "path": ".ai/memory/repository_profile_2.json",
.ai/audit/repository_inventory_v2.json:747:     "path": ".ai/memory/index.json",
.ai/audit/repository_inventory_v2.json:753:     "path": ".ai/memory/knowledge_graph.json",
.ai/audit/repository_inventory_v2.json:759:     "path": ".ai/memory/decision.json",
.ai/audit/repository_inventory_v2.json:765:     "path": ".ai/memory/workflow.json",
.ai/memory/knowledge_graph.json:170:       "type": "memory",
.ai/memory/knowledge_graph.json:172:       "path": ".ai/memory/history.json"
.ai/memory/knowledge_graph.json:175:       "type": "memory",
.ai/memory/knowledge_graph.json:177:       "path": ".ai/memory/index.json"
.ai/memory/knowledge_graph.json:180:       "type": "memory",
.ai/memory/knowledge_graph.json:182:       "path": ".ai/memory/repository_profile_1.json"
.ai/memory/knowledge_graph.json:185:       "type": "memory",
.ai/memory/knowledge_graph.json:187:       "path": ".ai/memory/repository_profile_2.json"
.ai/memory/workflow.json:12:       "engine": "Memory Engine",
.ai/runtime/cache/workspace_index/index.json:1513:       "path": ".ai/memory",
.ai/runtime/cache/workspace_index/index.json:1514:       "name": "memory"
lib/python/agent_runtime/models.py:10:     memory: Dict = field(default_factory=dict)
lib/python/agents/ai_cto_scanner_agent.py:19:     Canonical, and Project Memory dimensions.
lib/python/ai_cto_scanner/detectors.py:490: # Project Memory Detector
lib/python/ai_cto_scanner/detectors.py:495:         ("Project Memory", [
lib/python/ai_cto_scanner/detectors.py:501:             "path:memory",
lib/python/ai_cto_scanner/report.py:200:                 "Connect project memory to AI CTO context persistence layer",
lib/python/ai_cto_scanner/report.py:280:             ("ProjectMemory", "Project Memory Readiness", "Implement project memory and context persistence"),
lib/python/ai_cto_scanner/report.py:324:         if scores.get("Project Memory Readiness", 0) == 0:
lib/python/ai_cto_scanner/report.py:325:             lines.append("| No project memory infrastructure | HIGH | ProjectMemory | Implement project memory and context persistence |")
lib/python/ai_cto_scanner/report.py:384:             "- [ ] Activate project memory and resume engine",
lib/python/ai_cto_scanner/report.py:741:             "ProjectMemory": "Project Memory",
lib/python/ai_cto_scanner/scoring.py:74:         # Project Memory Readiness
lib/python/ai_cto_scanner/scoring.py:75:         memory = detection_results.get("ProjectMemory")
lib/python/ai_cto_scanner/scoring.py:76:         scores["Project Memory Readiness"] = self._score(memory)
lib/python/ai_cto_scanner/scoring.py:78:         # Context Integrity Readiness (subset of Project Memory)
lib/python/ai_cto_scanner/scoring.py:79:         integrity_components = self._filter_components(memory, ["Context Integrity", "Snapshot Engine", "Context Persistence"])
lib/python/ai_cto_scanner/scoring.py:90:             scores["Project Memory Readiness"] * 1.0,
lib/python/autonomous_workflow_engine.py:13: MEMORY = ROOT / ".ai" / "memory"
lib/python/autonomous_workflow_engine.py:15: decision_file = MEMORY / "decision.json"
lib/python/autonomous_workflow_engine.py:16: workflow_file = MEMORY / "workflow.json"
lib/python/autonomous_workflow_engine.py:35:         "engine": "Memory Engine",
lib/python/canonical_repository/repository.py:7:     """In-memory store of all CanonicalDocument entities."""
lib/python/css_engine/engine.py:42:     """In-memory representation of a loaded CSS standard."""
lib/python/decision_engine.py:12: MEMORY = ROOT / ".ai" / "memory"
lib/python/decision_engine.py:15: INDEX = MEMORY / "index.json"
lib/python/decision_engine.py:16: GRAPH = MEMORY / "knowledge_graph.json"
lib/python/decision_engine.py:54: OUT = MEMORY / "decision.json"
lib/python/epistemic/memory/model.py:2: Memory Domain
lib/python/epistemic/memory/model.py:4: A Memory is immutable.
lib/python/epistemic/memory/model.py:14: class Memory:
lib/python/epistemic/memory/store.py:2: Memory Store
lib/python/epistemic/memory/store.py:6: Append-only persistent memory.
lib/python/epistemic/memory/store.py:14: from .model import Memory
lib/python/epistemic/memory/store.py:17: ROOT = Path("work/memory")
lib/python/epistemic/memory/store.py:39:         memory = Memory(
lib/python/epistemic/memory/store.py:55:         file = ROOT / f"{memory.id}.json"
lib/python/epistemic/memory/store.py:59:             json.dumps(memory.__dict__, indent=2),
lib/python/epistemic/memory/store.py:65:         return memory
lib/python/epistemic/memory/store.py:76:         return Memory(**json.loads(file.read_text()))
lib/python/epistemic/memory/store.py:87:                 Memory(**json.loads(file.read_text()))
lib/python/epistemic/memory.py:16: class Memory:
lib/python/epistemic/memory.py:18:     def __init__(self, root="work/memory"):
lib/python/epistemic/memory.py:35:     memory = Memory()
lib/python/epistemic/memory.py:37:     artifact = memory.remember(
lib/python/epistemic/memory.py:39:         "# First Memory\n\nThe organism preserved its first experience.\n",
lib/python/epistemic/memory.py:42:     print("Memory created:")
lib/python/knowledge_graph_engine.py:42: for f in sorted((ROOT / ".ai" / "memory").glob("*")):
lib/python/knowledge_graph_engine.py:44:         add_node("memory", f.stem, f)
lib/python/knowledge_graph_engine.py:49: OUT = ROOT / ".ai" / "memory" / "knowledge_graph.json"
lib/python/memory_engine.py:15: MEMORY = ROOT / ".ai" / "memory"
lib/python/memory_engine.py:18: MEMORY.mkdir(parents=True, exist_ok=True)
lib/python/memory_engine.py:21: HISTORY = MEMORY / "history.json"
lib/python/memory_engine.py:22: INDEX = MEMORY / "index.json"
lib/python/memory_engine.py:42:     archive = MEMORY / f"repository_profile_{len(history['events']) + 1}.json"
lib/python/memory_engine.py:74: print("Memory Engine")
lib/python/runtime/metrics.py:5: In-memory metrics collector for the Runtime Server.
lib/python/runtime/metrics.py:16:     Thread-safe in-memory metrics store.
lib/python/semantic_repository_intelligence/architecture_graph.py:77:     ("Memory / State", [
lib/python/semantic_repository_intelligence/architecture_graph.py:78:         ("path_contains", "memory"),
lib/python/semantic_repository_intelligence/architecture_graph.py:80:         ("filename_contains", "memory"),
lib/python/semantic_repository_intelligence/engine.py:40:     ("CORE-010", "Project Memory Engine",
lib/python/semantic_repository_intelligence/engine.py:41:      "Build persistent project memory from semantic snapshots."),
lib/python/semantic_repository_intelligence/engine.py:222:         # If the architecture graph is complex (many nodes), memory is needed
lib/python/semantic_repository_intelligence/persistence.py:2: Semantic Repository Intelligence — Project Memory Persistence
lib/python/workspace_index/__init__.py:4: Canonical in-memory representation of the repository.
lib/python/workspace_index/models.py:42:     Canonical immutable in-memory representation of a repository.
lib/python/workspace_orchestrator/registry.py:5: WorkspaceRegistry: in-memory registry of known workspaces.
lib/python/workspace_orchestrator/registry.py:6: RepositoryRegistry: in-memory registry of repositories within a workspace.
tests/epistemic/test_memory.py:1: from lib.python.epistemic.memory.store import MemoryStore
tests/epistemic/test_memory.py:7:     memory = store.remember(
tests/epistemic/test_memory.py:9:         title="First Memory",
tests/epistemic/test_memory.py:19:     restored = store.recall(memory.id)
tests/epistemic/test_memory.py:23:     assert restored.id == memory.id
tests/epistemic/test_memory.py:25:     assert restored.content == memory.content
tests/test_ai_cto_scanner.sh:89:         'Project Memory Readiness',
tests/test_autonomous_workflow.sh:6: test -f .ai/memory/workflow.json
tests/test_autonomous_workflow.sh:10: cat .ai/memory/workflow.json
tests/test_decision_engine.sh:6: test -f .ai/memory/decision.json
tests/test_decision_engine.sh:11: cat .ai/memory/decision.json
tests/test_knowledge_graph.sh:6: test -f .ai/memory/knowledge_graph.json
tests/test_knowledge_graph.sh:12: with open(".ai/memory/knowledge_graph.json") as f:
tests/test_memory_engine.sh:6: test -f .ai/memory/history.json
tests/test_memory_engine.sh:7: test -f .ai/memory/index.json
tests/test_memory_engine.sh:11: cat .ai/memory/index.json
tests/test_memory_engine.sh:14: echo "Memory Engine PASS"
```

Matches: 119

### Term: `evidence`

```text
.ai/context/synchronization_report.json:12:       "evidence": [
.ai/execution/execution.json:29:   "evidence": {
.ai/execution/execution.json:150:               "evidence": [
.ai/execution/execution.json:162:               "evidence": [
.ai/execution/execution.json:180:               "evidence": [
.ai/execution/execution.json:196:               "evidence": [
.ai/execution/execution.json:213:               "evidence": [
.ai/execution/execution.json:225:               "evidence": [
.ai/execution/execution.json:325:               "evidence": [
.ai/execution/execution.json:341:               "evidence": [
.ai/execution/execution.json:356:               "evidence": [
.ai/execution/execution.json:371:               "evidence": [
.ai/execution/execution.json:386:               "evidence": [
.ai/execution/execution.json:401:               "evidence": [
.ai/execution/execution.json:422:               "evidence": [
.ai/execution/execution.json:439:               "evidence": [
.ai/execution/execution.json:673:       "evidence": {
.ai/execution/execution.json:683:       "evidence": {
.ai/execution/execution.json:693:       "evidence": {
.ai/execution/execution.json:703:       "evidence": {
.ai/execution/execution.json:714:       "evidence": {},
.ai/execution/execution.json:722:       "evidence": {
.ai/execution/execution.json:742:       "evidence": {
.ai/execution/execution.json:753:       "evidence": {},
.ai/execution/execution.json:761:       "evidence": {},
.ai/execution/execution.json:771:       "evidence": {
.ai/execution/execution.json:781:       "evidence": {
.ai/execution/execution.json:791:       "evidence": {
.ai/execution/execution.json:801:       "evidence": {},
.ai/execution/execution.json:811:       "evidence": {
.ai/execution/execution.json:821:       "evidence": {
.ai/execution/execution.json:831:       "evidence": {
.ai/execution/execution.json:836:         "{'id': 'ARCH-RISK-001', 'title': 'Architectural hotspot', 'description': 'lib/python/workspace_index/__init__.py is imported by many modules, creating a high-coupling hub.', 'severity': 'medium', 'affected_modules': ['lib/python/workspace_index/__init__.py'], 'evidence': ['in-degree: 13'], 'confidence': 0.85}",
.ai/execution/execution.json:837:         "{'id': 'ARCH-RISK-002', 'title': 'Architectural hotspot', 'description': 'lib/python/autonomous_planning_engine/models.py is imported by many modules, creating a high-coupling hub.', 'severity': 'medium', 'affected_modules': ['lib/python/autonomous_planning_engine/models.py'], 'evidence': ['in-degree: 11'], 'confidence': 0.85}",
.ai/execution/execution.json:838:         "{'id': 'ARCH-RISK-003', 'title': 'Architectural hotspot', 'description': 'lib/python/executive_briefing_engine/models.py is imported by many modules, creating a high-coupling hub.', 'severity': 'medium', 'affected_modules': ['lib/python/executive_briefing_engine/models.py'], 'evidence': ['in-degree: 10'], 'confidence': 0.85}",
.ai/execution/execution.json:839:         "{'id': 'ARCH-RISK-004', 'title': 'Unclassified modules', 'description': '108 modules could not be assigned to a known architectural layer.', 'severity': 'low', 'affected_modules': ['lib/python/__init__.py', 'lib/python/autonomous_execution_engine/__init__.py', 'lib/python/autonomous_execution_engine/engine.py', 'lib/python/autonomous_execution_engine/evidence.py', 'lib/python/autonomous_execution_engine/logger.py', 'lib/python/autonomous_execution_engine/persistence.py', 'lib/python/autonomous_execution_engine/policy.py', 'lib/python/autonomous_execution_engine/rollback.py', 'lib/python/autonomous_execution_engine/validator.py', 'lib/python/autonomous_planner/__init__.py'], 'evidence': ['Layer classification: Uncategorised'], 'confidence': 0.7}",
.ai/execution/execution.json:840:         "{'id': 'ARCH-RISK-005', 'title': 'High coupling detected', 'description': '15 modules have an excessive number of outbound imports.', 'severity': 'medium', 'affected_modules': ['lib/python/agents/development_agent.py', 'lib/python/ai_cto_scanner/engine.py', 'lib/python/autonomous_execution_engine/engine.py', 'lib/python/autonomous_planning_engine/__init__.py', 'lib/python/autonomous_planning_engine/engine.py', 'lib/python/canonical_intelligence/engine.py', 'lib/python/cli/main.py', 'lib/python/context_synchronization_engine/engine.py', 'lib/python/development_state_engine/runtime.py', 'lib/python/executable_repository_intelligence/engine.py'], 'evidence': ['Outbound import count exceeds threshold'], 'confidence': 0.8}"
.ai/execution/execution.json:847:       "evidence": {
.ai/execution/execution.json:857:       "evidence": {
.ai/execution/execution.json:871:       "evidence": {
.ai/execution/execution_evidence.json:122:             "evidence": [
.ai/execution/execution_evidence.json:134:             "evidence": [
.ai/execution/execution_evidence.json:152:             "evidence": [
.ai/execution/execution_evidence.json:168:             "evidence": [
.ai/execution/execution_evidence.json:185:             "evidence": [
.ai/execution/execution_evidence.json:197:             "evidence": [
.ai/execution/execution_evidence.json:297:             "evidence": [
.ai/execution/execution_evidence.json:313:             "evidence": [
.ai/execution/execution_evidence.json:328:             "evidence": [
.ai/execution/execution_evidence.json:343:             "evidence": [
.ai/execution/execution_evidence.json:358:             "evidence": [
.ai/execution/execution_evidence.json:373:             "evidence": [
.ai/execution/execution_evidence.json:394:             "evidence": [
.ai/execution/execution_evidence.json:411:             "evidence": [
.ai/execution/execution_results.json:5:       "evidence": {
.ai/execution/execution_results.json:15:       "evidence": {
.ai/execution/execution_results.json:25:       "evidence": {
.ai/execution/execution_results.json:30:         "{'id': 'ARCH-RISK-001', 'title': 'Architectural hotspot', 'description': 'lib/python/workspace_index/__init__.py is imported by many modules, creating a high-coupling hub.', 'severity': 'medium', 'affected_modules': ['lib/python/workspace_index/__init__.py'], 'evidence': ['in-degree: 13'], 'confidence': 0.85}",
.ai/execution/execution_results.json:31:         "{'id': 'ARCH-RISK-002', 'title': 'Architectural hotspot', 'description': 'lib/python/autonomous_planning_engine/models.py is imported by many modules, creating a high-coupling hub.', 'severity': 'medium', 'affected_modules': ['lib/python/autonomous_planning_engine/models.py'], 'evidence': ['in-degree: 11'], 'confidence': 0.85}",
.ai/execution/execution_results.json:32:         "{'id': 'ARCH-RISK-003', 'title': 'Architectural hotspot', 'description': 'lib/python/executive_briefing_engine/models.py is imported by many modules, creating a high-coupling hub.', 'severity': 'medium', 'affected_modules': ['lib/python/executive_briefing_engine/models.py'], 'evidence': ['in-degree: 10'], 'confidence': 0.85}",
.ai/execution/execution_results.json:33:         "{'id': 'ARCH-RISK-004', 'title': 'Unclassified modules', 'description': '108 modules could not be assigned to a known architectural layer.', 'severity': 'low', 'affected_modules': ['lib/python/__init__.py', 'lib/python/autonomous_execution_engine/__init__.py', 'lib/python/autonomous_execution_engine/engine.py', 'lib/python/autonomous_execution_engine/evidence.py', 'lib/python/autonomous_execution_engine/logger.py', 'lib/python/autonomous_execution_engine/persistence.py', 'lib/python/autonomous_execution_engine/policy.py', 'lib/python/autonomous_execution_engine/rollback.py', 'lib/python/autonomous_execution_engine/validator.py', 'lib/python/autonomous_planner/__init__.py'], 'evidence': ['Layer classification: Uncategorised'], 'confidence': 0.7}",
.ai/execution/execution_results.json:34:         "{'id': 'ARCH-RISK-005', 'title': 'High coupling detected', 'description': '15 modules have an excessive number of outbound imports.', 'severity': 'medium', 'affected_modules': ['lib/python/agents/development_agent.py', 'lib/python/ai_cto_scanner/engine.py', 'lib/python/autonomous_execution_engine/engine.py', 'lib/python/autonomous_planning_engine/__init__.py', 'lib/python/autonomous_planning_engine/engine.py', 'lib/python/canonical_intelligence/engine.py', 'lib/python/cli/main.py', 'lib/python/context_synchronization_engine/engine.py', 'lib/python/development_state_engine/runtime.py', 'lib/python/executable_repository_intelligence/engine.py'], 'evidence': ['Outbound import count exceeds threshold'], 'confidence': 0.8}"
.ai/execution/execution_results.json:41:       "evidence": {
.ai/execution/execution_results.json:51:       "evidence": {
.ai/execution/execution_results.json:65:       "evidence": {
.ai/executive/briefing.json:13:       "evidence": [
.ai/executive/briefing.json:29:       "evidence": [
.ai/executive/briefing.json:108:       "evidence": [
.ai/executive/briefing.json:129:       "evidence": [
.ai/executive/briefing.json:146:       "evidence": [
.ai/executive/recommendations.json:10:       "evidence": [
.ai/executive/recommendations.json:31:       "evidence": [
.ai/executive/recommendations.json:48:       "evidence": [
.ai/executive/risks.json:13:       "evidence": [
.ai/executive/risks.json:29:       "evidence": [
.ai/reports/inspect-20260807.json:436:       "path": ".ai/self_evaluation/evidence.json",
.ai/reports/inspect-20260807.json:2837:       "path": "lib/python/autonomous_execution_engine/evidence.py",
.ai/runtime_repository_model.json:38:         "evidence": [
.ai/runtime_repository_model.json:48:         "evidence": [
.ai/runtime_repository_model.json:58:         "evidence": [
.ai/runtime_repository_model.json:68:         "evidence": [
.ai/runtime_repository_model.json:78:         "evidence": [
.ai/runtime_repository_model.json:88:         "evidence": [
.ai/runtime_repository_model.json:98:         "evidence": [
.ai/runtime_repository_model.json:108:         "evidence": [
.ai/runtime_repository_model.json:118:         "evidence": [
.ai/runtime_repository_model.json:128:         "evidence": [
.ai/runtime_repository_model.json:138:         "evidence": [
.ai/runtime_repository_model.json:148:         "evidence": [
.ai/runtime_repository_model.json:158:         "evidence": [
.ai/runtime_repository_model.json:168:         "evidence": [
.ai/runtime_repository_model.json:178:         "evidence": [
.ai/runtime_repository_model.json:188:         "evidence": [
.ai/runtime_repository_model.json:198:         "evidence": [
.ai/runtime_repository_model.json:208:         "evidence": [
.ai/runtime_repository_model.json:218:         "evidence": [
.ai/runtime_repository_model.json:228:         "evidence": [
.ai/runtime_repository_model.json:238:         "evidence": [
.ai/runtime_repository_model.json:248:         "evidence": [
.ai/runtime_repository_model.json:258:         "evidence": [
.ai/runtime_repository_model.json:268:         "evidence": [
.ai/runtime_repository_model.json:278:         "evidence": [
.ai/runtime_repository_model.json:288:         "evidence": [
.ai/runtime_repository_model.json:298:         "evidence": [
.ai/runtime_repository_model.json:308:         "evidence": [
.ai/runtime_repository_model.json:318:         "evidence": [
.ai/runtime_repository_model.json:328:         "evidence": [
.ai/runtime_repository_model.json:338:         "evidence": [
.ai/runtime_repository_model.json:348:         "evidence": [
.ai/runtime_repository_model.json:358:         "evidence": [
.ai/runtime_repository_model.json:368:         "evidence": [
.ai/runtime_repository_model.json:378:         "evidence": [
.ai/runtime_repository_model.json:388:         "evidence": [
.ai/runtime_repository_model.json:398:         "evidence": [
.ai/runtime_repository_model.json:408:         "evidence": [
.ai/runtime_repository_model.json:418:         "evidence": [
.ai/runtime_repository_model.json:428:         "evidence": [
.ai/runtime_repository_model.json:438:         "evidence": [
.ai/runtime_repository_model.json:448:         "evidence": [
.ai/runtime_repository_model.json:458:         "evidence": [
.ai/runtime_repository_model.json:468:         "evidence": [
.ai/runtime_repository_model.json:478:         "evidence": [
.ai/runtime_repository_model.json:488:         "evidence": [
.ai/runtime_repository_model.json:498:         "evidence": [
.ai/runtime_repository_model.json:508:         "evidence": [
.ai/runtime_repository_model.json:518:         "evidence": [
.ai/runtime_repository_model.json:528:         "evidence": [
.ai/runtime_repository_model.json:538:         "evidence": [
.ai/runtime_repository_model.json:548:         "evidence": [
.ai/runtime_repository_model.json:558:         "evidence": [
.ai/runtime_repository_model.json:568:         "evidence": [
.ai/runtime_repository_model.json:578:         "evidence": [
.ai/runtime_repository_model.json:588:         "evidence": [
.ai/runtime_repository_model.json:598:         "evidence": [
.ai/runtime_repository_model.json:608:         "evidence": [
.ai/runtime_repository_model.json:618:         "evidence": [
.ai/runtime_repository_model.json:628:         "evidence": [
.ai/runtime_repository_model.json:638:         "evidence": [
.ai/runtime_repository_model.json:648:         "evidence": [
.ai/runtime_repository_model.json:658:         "evidence": [
.ai/runtime_repository_model.json:668:         "evidence": [
.ai/runtime_repository_model.json:678:         "evidence": [
.ai/runtime_repository_model.json:688:         "evidence": [
.ai/runtime_repository_model.json:698:         "evidence": [
.ai/runtime_repository_model.json:708:         "evidence": [
.ai/runtime_repository_model.json:718:         "evidence": [
.ai/runtime_repository_model.json:728:         "evidence": [
.ai/runtime_repository_model.json:738:         "evidence": [
.ai/runtime_repository_model.json:748:         "evidence": [
.ai/runtime_repository_model.json:758:         "evidence": [
.ai/runtime_repository_model.json:768:         "evidence": [
.ai/runtime_repository_model.json:778:         "evidence": [
.ai/runtime_repository_model.json:788:         "evidence": [
.ai/runtime_repository_model.json:798:         "evidence": [
.ai/runtime_repository_model.json:808:         "evidence": [
.ai/runtime_repository_model.json:818:         "evidence": [
.ai/runtime_repository_model.json:828:         "evidence": [
.ai/runtime_repository_model.json:838:         "evidence": [
.ai/runtime_repository_model.json:848:         "evidence": [
.ai/runtime_repository_model.json:858:         "evidence": [
.ai/runtime_repository_model.json:868:         "evidence": [
.ai/runtime_repository_model.json:878:         "evidence": [
.ai/runtime_repository_model.json:888:         "evidence": [
.ai/runtime_repository_model.json:898:         "evidence": [
.ai/runtime_repository_model.json:908:         "evidence": [
.ai/runtime_repository_model.json:918:         "evidence": [
.ai/runtime_repository_model.json:928:         "evidence": [
.ai/runtime_repository_model.json:938:         "evidence": [
.ai/runtime_repository_model.json:948:         "evidence": [
.ai/runtime_repository_model.json:958:         "evidence": [
.ai/runtime_repository_model.json:968:         "evidence": [
.ai/runtime_repository_model.json:978:         "evidence": [
.ai/runtime_repository_model.json:988:         "evidence": [
.ai/runtime_repository_model.json:998:         "evidence": [
.ai/runtime_repository_model.json:1008:         "evidence": [
.ai/runtime_repository_model.json:1018:         "evidence": [
.ai/runtime_repository_model.json:1028:         "evidence": [
.ai/runtime_repository_model.json:1038:         "evidence": [
.ai/runtime_repository_model.json:1048:         "evidence": [
.ai/runtime_repository_model.json:1058:         "evidence": [
.ai/runtime_repository_model.json:1068:         "evidence": [
.ai/runtime_repository_model.json:1078:         "evidence": [
.ai/runtime_repository_model.json:1088:         "evidence": [
.ai/runtime_repository_model.json:1098:         "evidence": [
.ai/runtime_repository_model.json:1108:         "evidence": [
.ai/runtime_repository_model.json:1118:         "evidence": [
.ai/runtime_repository_model.json:1128:         "evidence": [
.ai/runtime_repository_model.json:1138:         "evidence": [
.ai/runtime_repository_model.json:1148:         "evidence": [
.ai/runtime_repository_model.json:1158:         "evidence": [
.ai/runtime_repository_model.json:1168:         "evidence": [
.ai/runtime_repository_model.json:1178:         "evidence": [
.ai/runtime_repository_model.json:1188:         "evidence": [
.ai/runtime_repository_model.json:1198:         "evidence": [
.ai/runtime_repository_model.json:1208:         "evidence": [
.ai/runtime_repository_model.json:1218:         "evidence": [
.ai/runtime_repository_model.json:1228:         "evidence": [
.ai/runtime_repository_model.json:1238:         "evidence": [
.ai/runtime_repository_model.json:1248:         "evidence": [
.ai/runtime_repository_model.json:1258:         "evidence": [
.ai/runtime_repository_model.json:1268:         "evidence": [
.ai/runtime_repository_model.json:1278:         "evidence": [
.ai/runtime_repository_model.json:1288:         "evidence": [
.ai/runtime_repository_model.json:1298:         "evidence": [
.ai/runtime_repository_model.json:1308:         "evidence": [
.ai/runtime_repository_model.json:1318:         "evidence": [
.ai/runtime_repository_model.json:1328:         "evidence": [
.ai/runtime_repository_model.json:1338:         "evidence": [
.ai/runtime_repository_model.json:1348:         "evidence": [
.ai/runtime_repository_model.json:1358:         "evidence": [
.ai/runtime_repository_model.json:1368:         "evidence": [
.ai/runtime_repository_model.json:1378:         "evidence": [
.ai/runtime_repository_model.json:1388:         "evidence": [
.ai/runtime_repository_model.json:1398:         "evidence": [
.ai/runtime_repository_model.json:1408:         "evidence": [
.ai/runtime_repository_model.json:1418:         "evidence": [
.ai/runtime_repository_model.json:1428:         "evidence": [
.ai/runtime_repository_model.json:1438:         "evidence": [
.ai/runtime_repository_model.json:1448:         "evidence": [
.ai/runtime_repository_model.json:1458:         "evidence": [
.ai/runtime_repository_model.json:1468:         "evidence": [
.ai/runtime_repository_model.json:1478:         "evidence": [
.ai/runtime_repository_model.json:1488:         "evidence": [
.ai/runtime_repository_model.json:1498:         "evidence": [
.ai/runtime_repository_model.json:1508:         "evidence": [
.ai/runtime_repository_model.json:1518:         "evidence": [
.ai/runtime_repository_model.json:1528:         "evidence": [
.ai/runtime_repository_model.json:1538:         "evidence": [
.ai/runtime_repository_model.json:1548:         "evidence": [
.ai/runtime_repository_model.json:1558:         "evidence": [
.ai/runtime_repository_model.json:1568:         "evidence": [
.ai/runtime_repository_model.json:1578:         "evidence": [
.ai/runtime_repository_model.json:1588:         "evidence": [
.ai/runtime_repository_model.json:1598:         "evidence": [
.ai/runtime_repository_model.json:1608:         "evidence": [
.ai/runtime_repository_model.json:1618:         "evidence": [
.ai/runtime_repository_model.json:1628:         "evidence": [
.ai/runtime_repository_model.json:1638:         "evidence": [
.ai/runtime_repository_model.json:1648:         "evidence": [
.ai/runtime_repository_model.json:1658:         "evidence": [
.ai/runtime_repository_model.json:1668:         "evidence": [
.ai/runtime_repository_model.json:1678:         "evidence": [
.ai/runtime_repository_model.json:1688:         "evidence": [
.ai/runtime_repository_model.json:1698:         "evidence": [
.ai/runtime_repository_model.json:1708:         "evidence": [
.ai/runtime_repository_model.json:1718:         "evidence": [
.ai/runtime_repository_model.json:1728:         "evidence": [
.ai/runtime_repository_model.json:1738:         "evidence": [
.ai/runtime_repository_model.json:1748:         "evidence": [
.ai/runtime_repository_model.json:1758:         "evidence": [
.ai/runtime_repository_model.json:1768:         "evidence": [
.ai/runtime_repository_model.json:1778:         "evidence": [
.ai/runtime_repository_model.json:1788:         "evidence": [
.ai/runtime_repository_model.json:1798:         "evidence": [
.ai/runtime_repository_model.json:1808:         "evidence": [
.ai/runtime_repository_model.json:1818:         "evidence": [
.ai/runtime_repository_model.json:1828:         "evidence": [
.ai/runtime_repository_model.json:1838:         "evidence": [
.ai/runtime_repository_model.json:1848:         "evidence": [
.ai/runtime_repository_model.json:1858:         "evidence": [
.ai/runtime_repository_model.json:1868:         "evidence": [
.ai/runtime_repository_model.json:1878:         "evidence": [
.ai/runtime_repository_model.json:1888:         "evidence": [
.ai/runtime_repository_model.json:1898:         "evidence": [
.ai/runtime_repository_model.json:1908:         "evidence": [
.ai/runtime_repository_model.json:1918:         "evidence": [
.ai/runtime_repository_model.json:1928:         "evidence": [
.ai/runtime_repository_model.json:1938:         "evidence": [
.ai/runtime_repository_model.json:1948:         "evidence": [
.ai/runtime_repository_model.json:1958:         "evidence": [
.ai/runtime_repository_model.json:1968:         "evidence": [
.ai/runtime_repository_model.json:1978:         "evidence": [
.ai/runtime_repository_model.json:1988:         "evidence": [
.ai/runtime_repository_model.json:1998:         "evidence": [
.ai/runtime_repository_model.json:2008:         "evidence": [
.ai/runtime_repository_model.json:2018:         "evidence": [
.ai/runtime_repository_model.json:2028:         "evidence": [
.ai/runtime_repository_model.json:2038:         "evidence": [
.ai/runtime_repository_model.json:2048:         "evidence": [
.ai/runtime_repository_model.json:2058:         "evidence": [
.ai/runtime_repository_model.json:2068:         "evidence": [
.ai/runtime_repository_model.json:2078:         "evidence": [
.ai/runtime_repository_model.json:2088:         "evidence": [
.ai/runtime_repository_model.json:2098:         "evidence": [
.ai/runtime_repository_model.json:2108:         "evidence": [
.ai/runtime_repository_model.json:2118:         "evidence": [
.ai/runtime_repository_model.json:2128:         "evidence": [
.ai/runtime_repository_model.json:2138:         "evidence": [
.ai/runtime_repository_model.json:2148:         "evidence": [
.ai/runtime_repository_model.json:2158:         "evidence": [
.ai/runtime_repository_model.json:2168:         "evidence": [
.ai/runtime_repository_model.json:2178:         "evidence": [
.ai/runtime_repository_model.json:2188:         "evidence": [
.ai/runtime_repository_model.json:2198:         "evidence": [
.ai/runtime_repository_model.json:2208:         "evidence": [
.ai/runtime_repository_model.json:2218:         "evidence": [
.ai/runtime_repository_model.json:2228:         "evidence": [
.ai/runtime_repository_model.json:2238:         "evidence": [
.ai/runtime_repository_model.json:2248:         "evidence": [
.ai/runtime_repository_model.json:2258:         "evidence": [
.ai/runtime_repository_model.json:2268:         "evidence": [
.ai/runtime_repository_model.json:2278:         "evidence": [
.ai/runtime_repository_model.json:2288:         "evidence": [
.ai/runtime_repository_model.json:2298:         "evidence": [
.ai/runtime_repository_model.json:2308:         "evidence": [
.ai/runtime_repository_model.json:2318:         "evidence": [
.ai/runtime_repository_model.json:2328:         "evidence": [
.ai/runtime_repository_model.json:2338:         "evidence": [
.ai/runtime_repository_model.json:2348:         "evidence": [
.ai/runtime_repository_model.json:2358:         "evidence": [
.ai/runtime_repository_model.json:2368:         "evidence": [
.ai/runtime_repository_model.json:2378:         "evidence": [
.ai/runtime_repository_model.json:2388:         "evidence": [
.ai/runtime_repository_model.json:2398:         "evidence": [
.ai/runtime_repository_model.json:2408:         "evidence": [
.ai/runtime_repository_model.json:2418:         "evidence": [
.ai/runtime_repository_model.json:2428:         "evidence": [
.ai/runtime_repository_model.json:2438:         "evidence": [
.ai/runtime_repository_model.json:2448:         "evidence": [
.ai/runtime_repository_model.json:2458:         "evidence": [
.ai/runtime_repository_model.json:2468:         "evidence": [
.ai/runtime_repository_model.json:2478:         "evidence": [
.ai/runtime_repository_model.json:2488:         "evidence": [
.ai/runtime_repository_model.json:2498:         "evidence": [
.ai/runtime_repository_model.json:2508:         "evidence": [
.ai/runtime_repository_model.json:2518:         "evidence": [
.ai/runtime_repository_model.json:2528:         "evidence": [
.ai/runtime_repository_model.json:2538:         "evidence": [
.ai/runtime_repository_model.json:2548:         "evidence": [
.ai/runtime_repository_model.json:2558:         "evidence": [
.ai/runtime_repository_model.json:2568:         "evidence": [
.ai/runtime_repository_model.json:2578:         "evidence": [
.ai/runtime_repository_model.json:2588:         "evidence": [
.ai/runtime_repository_model.json:2598:         "evidence": [
.ai/runtime_repository_model.json:5891:         "evidence": [
.ai/runtime_repository_model.json:5901:         "evidence": [
.ai/runtime_repository_model.json:5910:         "evidence": [
.ai/runtime_repository_model.json:5920:         "evidence": [
.ai/runtime_repository_model.json:5930:         "evidence": [
.ai/runtime_repository_model.json:5939:         "evidence": [
.ai/runtime_repository_model.json:5948:         "evidence": [
.ai/runtime_repository_model.json:5957:         "evidence": [
.ai/runtime_repository_model.json:5967:         "evidence": [
.ai/runtime_repository_model.json:5976:         "evidence": [
.ai/runtime_repository_model.json:5985:         "evidence": [
.ai/runtime_repository_model.json:5996:         "evidence": [
.ai/runtime_repository_model.json:6006:         "evidence": [
.ai/runtime_repository_model.json:6016:         "evidence": [
.ai/runtime_repository_model.json:6026:         "evidence": [
.ai/runtime_repository_model.json:6036:         "evidence": [
.ai/runtime_repository_model.json:6046:         "evidence": [
.ai/runtime_repository_model.json:6056:         "evidence": [
.ai/runtime_repository_model.json:6066:         "evidence": [
.ai/runtime_repository_model.json:6076:         "evidence": [
.ai/runtime_repository_model.json:6086:         "evidence": [
.ai/runtime_repository_model.json:6096:         "evidence": [
.ai/runtime_repository_model.json:6106:         "evidence": [
.ai/runtime_repository_model.json:6116:         "evidence": [
.ai/runtime_repository_model.json:6126:         "evidence": [
.ai/runtime_repository_model.json:6136:         "evidence": [
.ai/runtime_repository_model.json:6146:         "evidence": [
.ai/runtime_repository_model.json:6156:         "evidence": [
.ai/runtime_repository_model.json:6167:         "evidence": [
.ai/runtime_repository_model.json:6177:         "evidence": [
.ai/runtime_repository_model.json:6187:         "evidence": [
.ai/runtime_repository_model.json:6197:         "evidence": [
.ai/runtime_repository_model.json:6207:         "evidence": [
.ai/runtime_repository_model.json:6217:         "evidence": [
.ai/runtime_repository_model.json:6227:         "evidence": [
.ai/runtime_repository_model.json:6238:         "evidence": [
.ai/runtime_repository_model.json:6248:         "evidence": [
.ai/runtime_repository_model.json:6258:         "evidence": [
.ai/runtime_repository_model.json:6268:         "evidence": [
.ai/runtime_repository_model.json:6278:         "evidence": [
.ai/runtime_repository_model.json:6288:         "evidence": [
.ai/runtime_repository_model.json:6298:         "evidence": [
.ai/runtime_repository_model.json:6308:         "evidence": [
.ai/runtime_repository_model.json:6318:         "evidence": [
.ai/runtime_repository_model.json:6328:         "evidence": [
.ai/runtime_repository_model.json:6338:         "evidence": [
.ai/runtime_repository_model.json:6348:         "evidence": [
.ai/runtime_repository_model.json:6358:         "evidence": [
.ai/runtime_repository_model.json:6368:         "evidence": [
.ai/runtime_repository_model.json:6378:         "evidence": [
.ai/runtime_repository_model.json:6388:         "evidence": [
.ai/runtime_repository_model.json:6397:         "evidence": [
.ai/runtime_repository_model.json:6407:         "evidence": [
.ai/runtime_repository_model.json:6417:         "evidence": [
.ai/runtime_repository_model.json:6427:         "evidence": [
.ai/runtime_repository_model.json:6437:         "evidence": [
.ai/runtime_repository_model.json:6447:         "evidence": [
.ai/runtime_repository_model.json:6457:         "evidence": [
.ai/runtime_repository_model.json:6467:         "evidence": [
.ai/runtime_repository_model.json:6477:         "evidence": [
.ai/runtime_repository_model.json:6491:         "evidence": [
.ai/runtime_repository_model.json:6508:         "evidence": [
.ai/runtime_repository_model.json:6523:         "evidence": [
.ai/self_evaluation/architecture.json:5:       "component": "{'id': 'ARCH-RISK-001', 'title': 'Architectural hotspot', 'description': 'lib/python/workspace_index/__init__.py is imported by many modules, creating a high-coupling hub.', 'severity': 'medium', 'affected_modules': ['lib/python/workspace_index/__init__.py'], 'evidence': ['in-degree: 13'], 'confidence': 0.85}",
.ai/self_evaluation/architecture.json:6:       "description": "{'id': 'ARCH-RISK-001', 'title': 'Architectural hotspot', 'description': 'lib/python/workspace_index/__init__.py is imported by many modules, creating a high-coupling hub.', 'severity': 'medium', 'affected_modules': ['lib/python/workspace_index/__init__.py'], 'evidence': ['in-degree: 13'], 'confidence': 0.85}",
.ai/self_evaluation/architecture.json:7:       "evidence": {
.ai/self_evaluation/architecture.json:14:       "component": "{'id': 'ARCH-RISK-002', 'title': 'Architectural hotspot', 'description': 'lib/python/autonomous_planning_engine/models.py is imported by many modules, creating a high-coupling hub.', 'severity': 'medium', 'affected_modules': ['lib/python/autonomous_planning_engine/models.py'], 'evidence': ['in-degree: 11'], 'confidence': 0.85}",
.ai/self_evaluation/architecture.json:15:       "description": "{'id': 'ARCH-RISK-002', 'title': 'Architectural hotspot', 'description': 'lib/python/autonomous_planning_engine/models.py is imported by many modules, creating a high-coupling hub.', 'severity': 'medium', 'affected_modules': ['lib/python/autonomous_planning_engine/models.py'], 'evidence': ['in-degree: 11'], 'confidence': 0.85}",
.ai/self_evaluation/architecture.json:16:       "evidence": {
.ai/self_evaluation/architecture.json:23:       "component": "{'id': 'ARCH-RISK-003', 'title': 'Architectural hotspot', 'description': 'lib/python/executive_briefing_engine/models.py is imported by many modules, creating a high-coupling hub.', 'severity': 'medium', 'affected_modules': ['lib/python/executive_briefing_engine/models.py'], 'evidence': ['in-degree: 10'], 'confidence': 0.85}",
.ai/self_evaluation/architecture.json:24:       "description": "{'id': 'ARCH-RISK-003', 'title': 'Architectural hotspot', 'description': 'lib/python/executive_briefing_engine/models.py is imported by many modules, creating a high-coupling hub.', 'severity': 'medium', 'affected_modules': ['lib/python/executive_briefing_engine/models.py'], 'evidence': ['in-degree: 10'], 'confidence': 0.85}",
.ai/self_evaluation/architecture.json:25:       "evidence": {
.ai/self_evaluation/architecture.json:32:       "component": "{'id': 'ARCH-RISK-004', 'title': 'Unclassified modules', 'description': '108 modules could not be assigned to a known architectural layer.', 'severity': 'low', 'affected_modules': ['lib/python/__init__.py', 'lib/python/autonomous_execution_engine/__init__.py', 'lib/python/autonomous_execution_engine/engine.py', 'lib/python/autonomous_execution_engine/evidence.py', 'lib/python/autonomous_execution_engine/logger.py', 'lib/python/autonomous_execution_engine/persistence.py', 'lib/python/autonomous_execution_engine/policy.py', 'lib/python/autonomous_execution_engine/rollback.py', 'lib/python/autonomous_execution_engine/validator.py', 'lib/python/autonomous_planner/__init__.py'], 'evidence': ['Layer classification: Uncategorised'], 'confidence': 0.7}",
.ai/self_evaluation/architecture.json:33:       "description": "{'id': 'ARCH-RISK-004', 'title': 'Unclassified modules', 'description': '108 modules could not be assigned to a known architectural layer.', 'severity': 'low', 'affected_modules': ['lib/python/__init__.py', 'lib/python/autonomous_execution_engine/__init__.py', 'lib/python/autonomous_execution_engine/engine.py', 'lib/python/autonomous_execution_engine/evidence.py', 'lib/python/autonomous_execution_engine/logger.py', 'lib/python/autonomous_execution_engine/persistence.py', 'lib/python/autonomous_execution_engine/policy.py', 'lib/python/autonomous_execution_engine/rollback.py', 'lib/python/autonomous_execution_engine/validator.py', 'lib/python/autonomous_planner/__init__.py'], 'evidence': ['Layer classification: Uncategorised'], 'confidence': 0.7}",
.ai/self_evaluation/architecture.json:34:       "evidence": {
.ai/self_evaluation/architecture.json:41:       "component": "{'id': 'ARCH-RISK-005', 'title': 'High coupling detected', 'description': '15 modules have an excessive number of outbound imports.', 'severity': 'medium', 'affected_modules': ['lib/python/agents/development_agent.py', 'lib/python/ai_cto_scanner/engine.py', 'lib/python/autonomous_execution_engine/engine.py', 'lib/python/autonomous_planning_engine/__init__.py', 'lib/python/autonomous_planning_engine/engine.py', 'lib/python/canonical_intelligence/engine.py', 'lib/python/cli/main.py', 'lib/python/context_synchronization_engine/engine.py', 'lib/python/development_state_engine/runtime.py', 'lib/python/executable_repository_intelligence/engine.py'], 'evidence': ['Outbound import count exceeds threshold'], 'confidence': 0.8}",
.ai/self_evaluation/architecture.json:42:       "description": "{'id': 'ARCH-RISK-005', 'title': 'High coupling detected', 'description': '15 modules have an excessive number of outbound imports.', 'severity': 'medium', 'affected_modules': ['lib/python/agents/development_agent.py', 'lib/python/ai_cto_scanner/engine.py', 'lib/python/autonomous_execution_engine/engine.py', 'lib/python/autonomous_planning_engine/__init__.py', 'lib/python/autonomous_planning_engine/engine.py', 'lib/python/canonical_intelligence/engine.py', 'lib/python/cli/main.py', 'lib/python/context_synchronization_engine/engine.py', 'lib/python/development_state_engine/runtime.py', 'lib/python/executable_repository_intelligence/engine.py'], 'evidence': ['Outbound import count exceeds threshold'], 'confidence': 0.8}",
.ai/self_evaluation/architecture.json:43:       "evidence": {
.ai/self_evaluation/compliance.json:5:       "evidence": [
.ai/self_evaluation/confidence.json:4:     "evidence": [
.ai/self_evaluation/confidence.json:5:       "Evidence items collected: 4"
.ai/self_evaluation/confidence.json:9:     "recommendation": "Increase evidence collection coverage.",
.ai/self_evaluation/coverage.json:5:       "evidence": [
.ai/self_evaluation/evaluation.json:5:       "component": "{'id': 'ARCH-RISK-001', 'title': 'Architectural hotspot', 'description': 'lib/python/workspace_index/__init__.py is imported by many modules, creating a high-coupling hub.', 'severity': 'medium', 'affected_modules': ['lib/python/workspace_index/__init__.py'], 'evidence': ['in-degree: 13'], 'confidence': 0.85}",
.ai/self_evaluation/evaluation.json:6:       "description": "{'id': 'ARCH-RISK-001', 'title': 'Architectural hotspot', 'description': 'lib/python/workspace_index/__init__.py is imported by many modules, creating a high-coupling hub.', 'severity': 'medium', 'affected_modules': ['lib/python/workspace_index/__init__.py'], 'evidence': ['in-degree: 13'], 'confidence': 0.85}",
.ai/self_evaluation/evaluation.json:7:       "evidence": {
.ai/self_evaluation/evaluation.json:14:       "component": "{'id': 'ARCH-RISK-002', 'title': 'Architectural hotspot', 'description': 'lib/python/autonomous_planning_engine/models.py is imported by many modules, creating a high-coupling hub.', 'severity': 'medium', 'affected_modules': ['lib/python/autonomous_planning_engine/models.py'], 'evidence': ['in-degree: 11'], 'confidence': 0.85}",
.ai/self_evaluation/evaluation.json:15:       "description": "{'id': 'ARCH-RISK-002', 'title': 'Architectural hotspot', 'description': 'lib/python/autonomous_planning_engine/models.py is imported by many modules, creating a high-coupling hub.', 'severity': 'medium', 'affected_modules': ['lib/python/autonomous_planning_engine/models.py'], 'evidence': ['in-degree: 11'], 'confidence': 0.85}",
.ai/self_evaluation/evaluation.json:16:       "evidence": {
.ai/self_evaluation/evaluation.json:23:       "component": "{'id': 'ARCH-RISK-003', 'title': 'Architectural hotspot', 'description': 'lib/python/executive_briefing_engine/models.py is imported by many modules, creating a high-coupling hub.', 'severity': 'medium', 'affected_modules': ['lib/python/executive_briefing_engine/models.py'], 'evidence': ['in-degree: 10'], 'confidence': 0.85}",
.ai/self_evaluation/evaluation.json:24:       "description": "{'id': 'ARCH-RISK-003', 'title': 'Architectural hotspot', 'description': 'lib/python/executive_briefing_engine/models.py is imported by many modules, creating a high-coupling hub.', 'severity': 'medium', 'affected_modules': ['lib/python/executive_briefing_engine/models.py'], 'evidence': ['in-degree: 10'], 'confidence': 0.85}",
.ai/self_evaluation/evaluation.json:25:       "evidence": {
.ai/self_evaluation/evaluation.json:32:       "component": "{'id': 'ARCH-RISK-004', 'title': 'Unclassified modules', 'description': '108 modules could not be assigned to a known architectural layer.', 'severity': 'low', 'affected_modules': ['lib/python/__init__.py', 'lib/python/autonomous_execution_engine/__init__.py', 'lib/python/autonomous_execution_engine/engine.py', 'lib/python/autonomous_execution_engine/evidence.py', 'lib/python/autonomous_execution_engine/logger.py', 'lib/python/autonomous_execution_engine/persistence.py', 'lib/python/autonomous_execution_engine/policy.py', 'lib/python/autonomous_execution_engine/rollback.py', 'lib/python/autonomous_execution_engine/validator.py', 'lib/python/autonomous_planner/__init__.py'], 'evidence': ['Layer classification: Uncategorised'], 'confidence': 0.7}",
.ai/self_evaluation/evaluation.json:33:       "description": "{'id': 'ARCH-RISK-004', 'title': 'Unclassified modules', 'description': '108 modules could not be assigned to a known architectural layer.', 'severity': 'low', 'affected_modules': ['lib/python/__init__.py', 'lib/python/autonomous_execution_engine/__init__.py', 'lib/python/autonomous_execution_engine/engine.py', 'lib/python/autonomous_execution_engine/evidence.py', 'lib/python/autonomous_execution_engine/logger.py', 'lib/python/autonomous_execution_engine/persistence.py', 'lib/python/autonomous_execution_engine/policy.py', 'lib/python/autonomous_execution_engine/rollback.py', 'lib/python/autonomous_execution_engine/validator.py', 'lib/python/autonomous_planner/__init__.py'], 'evidence': ['Layer classification: Uncategorised'], 'confidence': 0.7}",
.ai/self_evaluation/evaluation.json:34:       "evidence": {
.ai/self_evaluation/evaluation.json:41:       "component": "{'id': 'ARCH-RISK-005', 'title': 'High coupling detected', 'description': '15 modules have an excessive number of outbound imports.', 'severity': 'medium', 'affected_modules': ['lib/python/agents/development_agent.py', 'lib/python/ai_cto_scanner/engine.py', 'lib/python/autonomous_execution_engine/engine.py', 'lib/python/autonomous_planning_engine/__init__.py', 'lib/python/autonomous_planning_engine/engine.py', 'lib/python/canonical_intelligence/engine.py', 'lib/python/cli/main.py', 'lib/python/context_synchronization_engine/engine.py', 'lib/python/development_state_engine/runtime.py', 'lib/python/executable_repository_intelligence/engine.py'], 'evidence': ['Outbound import count exceeds threshold'], 'confidence': 0.8}",
.ai/self_evaluation/evaluation.json:42:       "description": "{'id': 'ARCH-RISK-005', 'title': 'High coupling detected', 'description': '15 modules have an excessive number of outbound imports.', 'severity': 'medium', 'affected_modules': ['lib/python/agents/development_agent.py', 'lib/python/ai_cto_scanner/engine.py', 'lib/python/autonomous_execution_engine/engine.py', 'lib/python/autonomous_planning_engine/__init__.py', 'lib/python/autonomous_planning_engine/engine.py', 'lib/python/canonical_intelligence/engine.py', 'lib/python/cli/main.py', 'lib/python/context_synchronization_engine/engine.py', 'lib/python/development_state_engine/runtime.py', 'lib/python/executable_repository_intelligence/engine.py'], 'evidence': ['Outbound import count exceeds threshold'], 'confidence': 0.8}",
.ai/self_evaluation/evaluation.json:43:       "evidence": {
.ai/self_evaluation/evaluation.json:69:       "evidence": [
.ai/self_evaluation/evaluation.json:79:       "evidence": [
.ai/self_evaluation/evaluation.json:83:         "{'id': 'ARCH-RISK-001', 'title': 'Architectural hotspot', 'description': 'lib/python/workspace_index/__init__.py is imported by many modules, creating a high-coupling hub.', 'severity': 'medium', 'affected_modules': ['lib/python/workspace_index/__init__.py'], 'evidence': ['in-degree: 13'], 'confidence': 0.85}",
.ai/self_evaluation/evaluation.json:84:         "{'id': 'ARCH-RISK-002', 'title': 'Architectural hotspot', 'description': 'lib/python/autonomous_planning_engine/models.py is imported by many modules, creating a high-coupling hub.', 'severity': 'medium', 'affected_modules': ['lib/python/autonomous_planning_engine/models.py'], 'evidence': ['in-degree: 11'], 'confidence': 0.85}",
.ai/self_evaluation/evaluation.json:85:         "{'id': 'ARCH-RISK-003', 'title': 'Architectural hotspot', 'description': 'lib/python/executive_briefing_engine/models.py is imported by many modules, creating a high-coupling hub.', 'severity': 'medium', 'affected_modules': ['lib/python/executive_briefing_engine/models.py'], 'evidence': ['in-degree: 10'], 'confidence': 0.85}",
.ai/self_evaluation/evaluation.json:86:         "{'id': 'ARCH-RISK-004', 'title': 'Unclassified modules', 'description': '108 modules could not be assigned to a known architectural layer.', 'severity': 'low', 'affected_modules': ['lib/python/__init__.py', 'lib/python/autonomous_execution_engine/__init__.py', 'lib/python/autonomous_execution_engine/engine.py', 'lib/python/autonomous_execution_engine/evidence.py', 'lib/python/autonomous_execution_engine/logger.py', 'lib/python/autonomous_execution_engine/persistence.py', 'lib/python/autonomous_execution_engine/policy.py', 'lib/python/autonomous_execution_engine/rollback.py', 'lib/python/autonomous_execution_engine/validator.py', 'lib/python/autonomous_planner/__init__.py'], 'evidence': ['Layer classification: Uncategorised'], 'confidence': 0.7}",
.ai/self_evaluation/evaluation.json:87:         "{'id': 'ARCH-RISK-005', 'title': 'High coupling detected', 'description': '15 modules have an excessive number of outbound imports.', 'severity': 'medium', 'affected_modules': ['lib/python/agents/development_agent.py', 'lib/python/ai_cto_scanner/engine.py', 'lib/python/autonomous_execution_engine/engine.py', 'lib/python/autonomous_planning_engine/__init__.py', 'lib/python/autonomous_planning_engine/engine.py', 'lib/python/canonical_intelligence/engine.py', 'lib/python/cli/main.py', 'lib/python/context_synchronization_engine/engine.py', 'lib/python/development_state_engine/runtime.py', 'lib/python/executable_repository_intelligence/engine.py'], 'evidence': ['Outbound import count exceeds threshold'], 'confidence': 0.8}"
.ai/self_evaluation/evaluation.json:95:       "evidence": [
.ai/self_evaluation/evaluation.json:105:       "evidence": [
.ai/self_evaluation/evaluation.json:118:       "evidence": [
.ai/self_evaluation/evaluation.json:128:       "evidence": [
.ai/self_evaluation/evaluation.json:129:         "Evidence items collected: 4"
.ai/self_evaluation/evaluation.json:133:       "recommendation": "Increase evidence collection coverage.",
.ai/self_evaluation/evaluation.json:138:       "evidence": [
.ai/self_evaluation/evaluation.json:154:       "evidence": [
.ai/self_evaluation/evaluation.json:178:       "evidence": {
.ai/self_evaluation/evidence.json:7:       "evidence": [
.ai/self_evaluation/evidence.json:17:       "evidence": [
.ai/self_evaluation/evidence.json:21:         "{'id': 'ARCH-RISK-001', 'title': 'Architectural hotspot', 'description': 'lib/python/workspace_index/__init__.py is imported by many modules, creating a high-coupling hub.', 'severity': 'medium', 'affected_modules': ['lib/python/workspace_index/__init__.py'], 'evidence': ['in-degree: 13'], 'confidence': 0.85}",
.ai/self_evaluation/evidence.json:22:         "{'id': 'ARCH-RISK-002', 'title': 'Architectural hotspot', 'description': 'lib/python/autonomous_planning_engine/models.py is imported by many modules, creating a high-coupling hub.', 'severity': 'medium', 'affected_modules': ['lib/python/autonomous_planning_engine/models.py'], 'evidence': ['in-degree: 11'], 'confidence': 0.85}",
.ai/self_evaluation/evidence.json:23:         "{'id': 'ARCH-RISK-003', 'title': 'Architectural hotspot', 'description': 'lib/python/executive_briefing_engine/models.py is imported by many modules, creating a high-coupling hub.', 'severity': 'medium', 'affected_modules': ['lib/python/executive_briefing_engine/models.py'], 'evidence': ['in-degree: 10'], 'confidence': 0.85}",
.ai/self_evaluation/evidence.json:24:         "{'id': 'ARCH-RISK-004', 'title': 'Unclassified modules', 'description': '108 modules could not be assigned to a known architectural layer.', 'severity': 'low', 'affected_modules': ['lib/python/__init__.py', 'lib/python/autonomous_execution_engine/__init__.py', 'lib/python/autonomous_execution_engine/engine.py', 'lib/python/autonomous_execution_engine/evidence.py', 'lib/python/autonomous_execution_engine/logger.py', 'lib/python/autonomous_execution_engine/persistence.py', 'lib/python/autonomous_execution_engine/policy.py', 'lib/python/autonomous_execution_engine/rollback.py', 'lib/python/autonomous_execution_engine/validator.py', 'lib/python/autonomous_planner/__init__.py'], 'evidence': ['Layer classification: Uncategorised'], 'confidence': 0.7}",
.ai/self_evaluation/evidence.json:25:         "{'id': 'ARCH-RISK-005', 'title': 'High coupling detected', 'description': '15 modules have an excessive number of outbound imports.', 'severity': 'medium', 'affected_modules': ['lib/python/agents/development_agent.py', 'lib/python/ai_cto_scanner/engine.py', 'lib/python/autonomous_execution_engine/engine.py', 'lib/python/autonomous_planning_engine/__init__.py', 'lib/python/autonomous_planning_engine/engine.py', 'lib/python/canonical_intelligence/engine.py', 'lib/python/cli/main.py', 'lib/python/context_synchronization_engine/engine.py', 'lib/python/development_state_engine/runtime.py', 'lib/python/executable_repository_intelligence/engine.py'], 'evidence': ['Outbound import count exceeds threshold'], 'confidence': 0.8}"
.ai/self_evaluation/evidence.json:33:       "evidence": [
.ai/self_evaluation/evidence.json:43:       "evidence": [
.ai/self_evaluation/evidence.json:56:       "evidence": [
.ai/self_evaluation/evidence.json:66:       "evidence": [
.ai/self_evaluation/evidence.json:67:         "Evidence items collected: 4"
.ai/self_evaluation/evidence.json:71:       "recommendation": "Increase evidence collection coverage.",
.ai/self_evaluation/evidence.json:76:       "evidence": [
.ai/self_evaluation/evidence.json:92:       "evidence": [
.ai/self_evaluation/quality.json:9:       "evidence": [
.ai/self_evaluation/quality.json:19:       "evidence": [
.ai/self_evaluation/quality.json:23:         "{'id': 'ARCH-RISK-001', 'title': 'Architectural hotspot', 'description': 'lib/python/workspace_index/__init__.py is imported by many modules, creating a high-coupling hub.', 'severity': 'medium', 'affected_modules': ['lib/python/workspace_index/__init__.py'], 'evidence': ['in-degree: 13'], 'confidence': 0.85}",
.ai/self_evaluation/quality.json:24:         "{'id': 'ARCH-RISK-002', 'title': 'Architectural hotspot', 'description': 'lib/python/autonomous_planning_engine/models.py is imported by many modules, creating a high-coupling hub.', 'severity': 'medium', 'affected_modules': ['lib/python/autonomous_planning_engine/models.py'], 'evidence': ['in-degree: 11'], 'confidence': 0.85}",
.ai/self_evaluation/quality.json:25:         "{'id': 'ARCH-RISK-003', 'title': 'Architectural hotspot', 'description': 'lib/python/executive_briefing_engine/models.py is imported by many modules, creating a high-coupling hub.', 'severity': 'medium', 'affected_modules': ['lib/python/executive_briefing_engine/models.py'], 'evidence': ['in-degree: 10'], 'confidence': 0.85}",
.ai/self_evaluation/quality.json:26:         "{'id': 'ARCH-RISK-004', 'title': 'Unclassified modules', 'description': '108 modules could not be assigned to a known architectural layer.', 'severity': 'low', 'affected_modules': ['lib/python/__init__.py', 'lib/python/autonomous_execution_engine/__init__.py', 'lib/python/autonomous_execution_engine/engine.py', 'lib/python/autonomous_execution_engine/evidence.py', 'lib/python/autonomous_execution_engine/logger.py', 'lib/python/autonomous_execution_engine/persistence.py', 'lib/python/autonomous_execution_engine/policy.py', 'lib/python/autonomous_execution_engine/rollback.py', 'lib/python/autonomous_execution_engine/validator.py', 'lib/python/autonomous_planner/__init__.py'], 'evidence': ['Layer classification: Uncategorised'], 'confidence': 0.7}",
.ai/self_evaluation/quality.json:27:         "{'id': 'ARCH-RISK-005', 'title': 'High coupling detected', 'description': '15 modules have an excessive number of outbound imports.', 'severity': 'medium', 'affected_modules': ['lib/python/agents/development_agent.py', 'lib/python/ai_cto_scanner/engine.py', 'lib/python/autonomous_execution_engine/engine.py', 'lib/python/autonomous_planning_engine/__init__.py', 'lib/python/autonomous_planning_engine/engine.py', 'lib/python/canonical_intelligence/engine.py', 'lib/python/cli/main.py', 'lib/python/context_synchronization_engine/engine.py', 'lib/python/development_state_engine/runtime.py', 'lib/python/executable_repository_intelligence/engine.py'], 'evidence': ['Outbound import count exceeds threshold'], 'confidence': 0.8}"
.ai/self_evaluation/quality.json:35:       "evidence": [
.ai/self_evaluation/quality.json:45:       "evidence": [
.ai/self_evaluation/quality.json:58:       "evidence": [
.ai/self_evaluation/quality.json:68:       "evidence": [
.ai/self_evaluation/quality.json:69:         "Evidence items collected: 4"
.ai/self_evaluation/quality.json:73:       "recommendation": "Increase evidence collection coverage.",
.ai/self_evaluation/quality.json:78:       "evidence": [
.ai/self_evaluation/quality.json:94:       "evidence": [
.ai/self_evaluation/regressions.json:12:       "evidence": {
.ai/self_improvement/capability_analysis.json:7:       "evidence": {
.ai/self_improvement/capability_analysis.json:17:       "evidence": {
.ai/self_improvement/capability_analysis.json:27:       "evidence": {
.ai/self_improvement/improvements.json:7:       "evidence": {
.ai/self_improvement/improvements.json:17:       "evidence": {
.ai/self_improvement/improvements.json:27:       "evidence": {
.ai/self_improvement/improvements.json:42:       "evidence": {
.ai/self_improvement/improvements.json:54:       "evidence": {
.ai/self_improvement/improvements.json:65:       "evidence": {
.ai/self_improvement/improvements.json:86:       "evidence": {
.ai/self_improvement/improvements.json:118:       "evidence": {
.ai/self_improvement/improvements.json:176:       "evidence": {
.ai/self_improvement/improvements.json:200:       "evidence": {
.ai/self_improvement/improvements.json:224:       "evidence": {
.ai/self_improvement/improvements.json:248:       "evidence": {
.ai/self_improvement/improvements.json:272:       "evidence": {
.ai/self_improvement/improvements.json:296:       "evidence": {
.ai/self_improvement/improvements.json:320:       "evidence": {
.ai/self_improvement/improvements.json:344:       "evidence": {
.ai/self_improvement/improvements.json:368:       "evidence": {
.ai/self_improvement/improvements.json:393:       "evidence": {
.ai/self_improvement/improvements.json:419:       "evidence": {
.ai/self_improvement/improvements.json:445:       "evidence": {
.ai/self_improvement/improvements.json:470:       "evidence": {
.ai/self_improvement/improvements.json:482:       "evidence": {
.ai/self_improvement/improvements.json:494:       "evidence": {
.ai/self_improvement/improvements.json:506:       "evidence": {
.ai/self_improvement/improvements.json:518:       "evidence": {
.ai/self_improvement/improvements.json:530:       "evidence": {
.ai/self_improvement/improvements.json:542:       "evidence": {
.ai/self_improvement/improvements.json:554:       "evidence": {
.ai/self_improvement/improvements.json:566:       "evidence": {
.ai/self_improvement/optimization_plan.json:7:       "evidence": {
.ai/self_improvement/optimization_plan.json:17:       "evidence": {
.ai/self_improvement/optimization_plan.json:27:       "evidence": {
.ai/self_improvement/optimization_plan.json:42:       "evidence": {
.ai/self_improvement/optimization_plan.json:54:       "evidence": {
.ai/self_improvement/optimization_plan.json:65:       "evidence": {
.ai/self_improvement/optimization_plan.json:86:       "evidence": {
.ai/self_improvement/optimization_plan.json:118:       "evidence": {
.ai/self_improvement/optimization_plan.json:176:       "evidence": {
.ai/self_improvement/optimization_plan.json:200:       "evidence": {
.ai/self_improvement/optimization_plan.json:224:       "evidence": {
.ai/self_improvement/optimization_plan.json:248:       "evidence": {
.ai/self_improvement/optimization_plan.json:272:       "evidence": {
.ai/self_improvement/optimization_plan.json:296:       "evidence": {
.ai/self_improvement/optimization_plan.json:320:       "evidence": {
.ai/self_improvement/optimization_plan.json:344:       "evidence": {
.ai/self_improvement/optimization_plan.json:368:       "evidence": {
.ai/self_improvement/optimization_plan.json:393:       "evidence": {
.ai/self_improvement/optimization_plan.json:419:       "evidence": {
.ai/self_improvement/optimization_plan.json:445:       "evidence": {
.ai/self_improvement/optimization_plan.json:470:       "evidence": {
.ai/self_improvement/optimization_plan.json:482:       "evidence": {
.ai/self_improvement/optimization_plan.json:494:       "evidence": {
.ai/self_improvement/optimization_plan.json:506:       "evidence": {
.ai/self_improvement/optimization_plan.json:518:       "evidence": {
.ai/self_improvement/optimization_plan.json:530:       "evidence": {
.ai/self_improvement/optimization_plan.json:542:       "evidence": {
.ai/self_improvement/optimization_plan.json:554:       "evidence": {
.ai/self_improvement/optimization_plan.json:566:       "evidence": {
.ai/self_improvement/performance.json:7:       "evidence": {
.ai/self_improvement/performance.json:19:       "evidence": {
.ai/self_improvement/performance.json:30:       "evidence": {
.ai/self_improvement/proposed_batches.json:14:       "evidence": {
.ai/self_improvement/proposed_batches.json:46:       "evidence": {
.ai/self_improvement/proposed_issues.json:19:       "evidence": {
.ai/self_improvement/proposed_issues.json:43:       "evidence": {
.ai/self_improvement/proposed_issues.json:67:       "evidence": {
.ai/self_improvement/proposed_issues.json:91:       "evidence": {
.ai/self_improvement/proposed_issues.json:115:       "evidence": {
.ai/self_improvement/proposed_issues.json:139:       "evidence": {
.ai/self_improvement/proposed_issues.json:163:       "evidence": {
.ai/self_improvement/proposed_issues.json:187:       "evidence": {
.ai/self_improvement/proposed_issues.json:211:       "evidence": {
.ai/self_improvement/proposed_issues.json:236:       "evidence": {
.ai/self_improvement/proposed_issues.json:262:       "evidence": {
.ai/self_improvement/proposed_issues.json:288:       "evidence": {
.ai/self_improvement/technical_debt.json:11:       "evidence": {
.ai/self_improvement/technical_debt.json:23:       "evidence": {
.ai/self_improvement/technical_debt.json:35:       "evidence": {
.ai/self_improvement/technical_debt.json:47:       "evidence": {
.ai/self_improvement/technical_debt.json:59:       "evidence": {
.ai/self_improvement/technical_debt.json:71:       "evidence": {
.ai/self_improvement/technical_debt.json:83:       "evidence": {
.ai/self_improvement/technical_debt.json:95:       "evidence": {
.ai/self_improvement/technical_debt.json:107:       "evidence": {
lib/python/ai_cto_scanner/detectors.py:5: Each detector scans the workspace index and file contents for evidence.
lib/python/ai_cto_scanner/detectors.py:17:     """Evidence of a detected component."""
lib/python/ai_cto_scanner/detectors.py:21:         self.files = files          # list of file paths containing evidence
lib/python/ai_cto_scanner/report.py:630:             "Evidence-based architectural recommendations generated by CORE-008B.",
lib/python/autonomous_execution_engine/__init__.py:24: from .evidence import ExecutionEvidenceCollector, ExecutionSnapshot
lib/python/autonomous_execution_engine/engine.py:41: from .evidence import ExecutionEvidenceCollector, ExecutionSnapshot
lib/python/autonomous_execution_engine/engine.py:99:     evidence: Dict[str, Any] = None,
lib/python/autonomous_execution_engine/engine.py:107:         evidence=evidence or {},
lib/python/autonomous_execution_engine/engine.py:284:                           evidence={"source": "CORE-013"})
lib/python/autonomous_execution_engine/engine.py:295:                           evidence={"source": "CORE-009"})
lib/python/autonomous_execution_engine/engine.py:306:                           evidence={"source": "CORE-010"})
lib/python/autonomous_execution_engine/engine.py:317:                           evidence={"entry_count": len(queue_data.get("entries", [])),
lib/python/autonomous_execution_engine/engine.py:341:                           evidence=policy.to_dict())
lib/python/autonomous_execution_engine/engine.py:357:                           evidence={"approval": approval, "mode": self.mode},
lib/python/autonomous_execution_engine/engine.py:398:         # STAGE: Collect Evidence
lib/python/autonomous_execution_engine/engine.py:404:                           evidence={"evidence_count": evidence_dict.get("evidence_count", 0)})
lib/python/autonomous_execution_engine/engine.py:432:                           evidence={"validator_count": len(validation_results)})
lib/python/autonomous_execution_engine/engine.py:441:                           evidence={"note": "State read-only in safe modes"})
lib/python/autonomous_execution_engine/engine.py:486:             evidence=evidence_dict,
lib/python/autonomous_execution_engine/engine.py:536:                           evidence={"artifact_count": len(paths)})
lib/python/autonomous_execution_engine/evidence.py:2: Autonomous Execution Engine — Evidence Collector and Snapshot
lib/python/autonomous_execution_engine/evidence.py:5: Collects deterministic, evidence-based execution artefacts.
lib/python/autonomous_execution_engine/evidence.py:19:     CORE-015D — Execution Evidence Collector.
lib/python/autonomous_execution_engine/evidence.py:21:     Collects observable evidence from each execution stage without
lib/python/autonomous_execution_engine/evidence.py:29:         """Record a piece of evidence."""
lib/python/autonomous_execution_engine/evidence.py:40:         """Return all collected evidence as a deterministic dict."""
lib/python/autonomous_execution_engine/models.py:174:     evidence: Dict[str, Any]
lib/python/autonomous_execution_engine/models.py:183:             "evidence": self.evidence,
lib/python/autonomous_execution_engine/models.py:201:     evidence: Dict[str, Any]
lib/python/autonomous_execution_engine/models.py:209:             "evidence": self.evidence,
lib/python/autonomous_execution_engine/models.py:301:     evidence: Dict[str, Any] = field(default_factory=dict)
lib/python/autonomous_execution_engine/models.py:322:             "evidence": self.evidence,
lib/python/autonomous_execution_engine/persistence.py:96:             "execution_evidence.json", d.get("evidence", {})
lib/python/autonomous_execution_engine/policy.py:137:                 evidence={"mode": policy.mode, "approval": approval},
lib/python/autonomous_execution_engine/policy.py:145:             evidence={"mode": policy.mode, "approval": approval},
lib/python/autonomous_execution_engine/report.py:125:             lines.append(f"- Evidence Count: {metrics.get('evidence_count', 0)}\n")
lib/python/autonomous_execution_engine/validator.py:26:     Produces deterministic, evidence-based ValidationResult objects.
lib/python/autonomous_execution_engine/validator.py:51:                 evidence={"readiness_score": score, "source": "CORE-008A"},
lib/python/autonomous_execution_engine/validator.py:59:                 evidence={"source": "CORE-008A"},
lib/python/autonomous_execution_engine/validator.py:77:                 evidence={"risk_count": len(risks), "source": "CORE-008B"},
lib/python/autonomous_execution_engine/validator.py:85:                 evidence={"source": "CORE-008B"},
lib/python/autonomous_execution_engine/validator.py:103:                 evidence={"deviation_count": len(deviations), "source": "CORE-007"},
lib/python/autonomous_execution_engine/validator.py:111:                 evidence={"source": "CORE-007"},
lib/python/autonomous_execution_engine/validator.py:123:         evidence: Dict[str, Any] = {}
lib/python/autonomous_execution_engine/validator.py:141:         evidence["checked_planning_keys"] = sorted(required_keys)
lib/python/autonomous_execution_engine/validator.py:142:         evidence["missing_planning_keys"] = sorted(missing)
lib/python/autonomous_execution_engine/validator.py:151:             evidence=evidence,
lib/python/autonomous_execution_engine/validator.py:174:             evidence={
lib/python/autonomous_planning_engine/issue_planner.py:35:     All recommendations are evidence-backed — no hardcoded issue text.
lib/python/batch_planner/planner.py:74:         criteria.append("Tests or validation evidence exist for %s." % doc.id)
lib/python/canonical_audit/engine.py:38:         report["evidence"] = {}
lib/python/canonical_audit/engine.py:57:                 report["evidence"][doc] = evidence_engine.find(base)
lib/python/canonical_entities/models.py:151:     """Evidence-backed mapping between canonical and implementation entities."""
lib/python/canonical_entities/models.py:157:     evidence: List[str] = field(default_factory=list)
lib/python/canonical_entities/models.py:171:     evidence: List[str] = field(default_factory=list)
lib/python/canonical_entities/models.py:181:     evidence: List[str] = field(default_factory=list)
lib/python/canonical_entities/models.py:194:     evidence: List[str] = field(default_factory=list)
lib/python/compliance_engine/engine.py:47:         evidence = []
lib/python/compliance_engine/engine.py:55:                 evidence.append(doc_id)
lib/python/compliance_engine/engine.py:57:         metrics.append(self._metric("Dependency Compliance", dependency_score, evidence[:10]))
lib/python/compliance_engine/engine.py:67:     def _metric(self, category, score, evidence):
lib/python/compliance_engine/engine.py:72:             evidence=list(evidence)[:10],
lib/python/compliance_engine/engine.py:99:         return metric.evidence if metric else []
lib/python/context_synchronization_engine/engine.py:643:                 evidence=(obsolete, str(live_context.get("current_recommendation", ""))),
lib/python/context_synchronization_engine/engine.py:655:                     evidence=(str(live_context.get(field, "")),),
lib/python/context_synchronization_engine/engine.py:673:                     evidence=tuple(candidates[:4]),
lib/python/context_synchronization_engine/engine.py:696:                 evidence=(str(before_value), str(after_value)),
lib/python/context_synchronization_engine/engine.py:824:                 key = (finding.category, finding.message, tuple(finding.evidence))
lib/python/context_synchronization_engine/engine.py:1352:                             or details.get("evidence", [])
lib/python/context_synchronization_engine/models.py:29:     evidence: Tuple[str, ...] = ()
lib/python/context_synchronization_engine/models.py:37:             "evidence": list(self.evidence),
lib/python/context_synchronization_engine/models.py:47:             evidence=_to_tuple(data.get("evidence", ())),
lib/python/coverage_engine/engine.py:56:     def _metric(self, category, total, covered, partial_items, evidence):
lib/python/coverage_engine/engine.py:70:             evidence=list(evidence)[:10],
lib/python/dashboard/service.py:130:         architecture="Renders capability metadata plus live implementation evidence gathered from related files, tests, and reports.",
lib/python/dashboard/service.py:146:         why_dependencies="Explorer pages depend on the dashboard shell and repository evidence to stay truthful.",
lib/python/dashboard/service.py:205:         architecture="References existing validation engine modules and tests, then exposes their current implementation evidence and roadmap.",
lib/python/dashboard/service.py:214:         known_limitations="The MVP surfaces implementation evidence but not a dedicated validation report viewer.",
lib/python/dashboard/service.py:220:         why_architecture="The explorer can reveal implemented evidence before a full dashboard surface exists.",
lib/python/drift_engine/engine.py:21:         """Detect drift between canonical repository and implementation evidence."""
lib/python/drift_engine/engine.py:53:                     list(best.evidence),
lib/python/drift_engine/engine.py:80:                     "Canonical document %s lacks clear test coverage evidence." % doc.id,
lib/python/drift_engine/engine.py:127:     def _finding(self, finding_id, category, severity, canonical_ref, implementation_ref, description, evidence, recommendation, confidence, detected_at):
lib/python/drift_engine/engine.py:135:             evidence=[item for item in evidence if item][:10],
lib/python/drift_engine/engine.py:185:                     evidence=[wf.path],
lib/python/engineering_engine/capability_detector.py:11:     evidence: str
lib/python/engineering_engine/capability_detector.py:57:                     evidence=target if exists else f"{target} not found",
lib/python/engineering_engine/gap_analysis.py:14:     evidence: str
lib/python/engineering_engine/gap_analysis.py:46:             md.write('| Component | Status | Evidence |\n')
lib/python/engineering_engine/gap_analysis.py:49:                 md.write(f'| {item.component} | {item.status} | {item.evidence} |\n')
lib/python/engineering_engine/repository_audit.py:89:             "purpose": "validation, heuristic coverage/compliance scoring, drift and evidence reporting",
lib/python/epistemic/transformation.py:13: ROOT = Path("work/transformation-evidence")
lib/python/epistemic/transformation.py:50: f"""# Transformation Evidence
lib/python/evidence_engine/__init__.py:2: Evidence Engine
lib/python/evidence_engine/engine.py:17:         evidence = {
lib/python/evidence_engine/engine.py:40:                 evidence["python"].append(rel)
lib/python/evidence_engine/engine.py:43:                 evidence["shell"].append(rel)
lib/python/evidence_engine/engine.py:46:                 evidence["tests"].append(rel)
lib/python/evidence_engine/engine.py:49:                 evidence["docs"].append(rel)
lib/python/evidence_engine/engine.py:51:         evidence["semantic"] = {}
lib/python/evidence_engine/engine.py:70:                 evidence["semantic"][filename] = score
lib/python/evidence_engine/engine.py:72:         return evidence
lib/python/executable_repository_intelligence/engine.py:186:             __slots__ = ("name", "type", "file", "line", "pattern", "confidence", "evidence")
lib/python/executable_repository_intelligence/engine.py:195:                 self.evidence = d.get("evidence", [])
lib/python/executable_repository_intelligence/file_classifier.py:331:                 evidence = ["Matched rule: %s/%s" % (category, subcategory)]
lib/python/executable_repository_intelligence/file_classifier.py:338:                     evidence=evidence,
lib/python/executable_repository_intelligence/file_classifier.py:356:                 evidence=["Language: markdown"],
lib/python/executable_repository_intelligence/file_classifier.py:368:                     evidence=["Language: %s; entry_points: %s" % (lang, entry_points)],
lib/python/executable_repository_intelligence/file_classifier.py:377:                 evidence=["Language: %s" % lang],
lib/python/executable_repository_intelligence/file_classifier.py:387:                 evidence=["Language: %s" % lang],
lib/python/executable_repository_intelligence/file_classifier.py:396:             evidence=["No matching rule or known language"],
lib/python/executable_repository_intelligence/injection_safety.py:29: # Evidence keywords suggesting unsafe dynamic execution
lib/python/executable_repository_intelligence/injection_safety.py:35: # Evidence keywords suggesting read-only behaviour
lib/python/executable_repository_intelligence/injection_safety.py:73:         evidence_text = " ".join(ip.evidence).lower()
lib/python/executable_repository_intelligence/models.py:71:     evidence: List[str]    # human-readable evidence strings
lib/python/executable_repository_intelligence/models.py:80:             "evidence": self.evidence,
lib/python/executable_repository_intelligence/models.py:236:     evidence: List[str]
lib/python/executable_repository_intelligence/models.py:243:             "evidence": self.evidence,
lib/python/executable_repository_intelligence/models.py:253:     """An evidence-based recommendation from the executable intelligence layer."""
lib/python/executable_repository_intelligence/models.py:261:     evidence: List[str]
lib/python/executable_repository_intelligence/models.py:272:             "evidence": self.evidence,
lib/python/executable_repository_intelligence/recommendations.py:5: Generates evidence-based, executable-specific recommendations.
lib/python/executable_repository_intelligence/recommendations.py:59:             if z.zone == "Runtime" and any("Documentation" in e for e in z.evidence)
lib/python/executable_repository_intelligence/recommendations.py:76:             evidence=["Zones with documentation in runtime: %d" % len(doc_in_runtime)],
lib/python/executable_repository_intelligence/recommendations.py:107:             evidence=[
lib/python/executable_repository_intelligence/recommendations.py:134:             evidence=["%s — %s" % (r.name, r.rationale) for r in unsafe[:5]],
lib/python/executable_repository_intelligence/recommendations.py:144:             if z.zone == "Runtime" and any("Generated" in e for e in z.evidence)
lib/python/executable_repository_intelligence/recommendations.py:162:             evidence=["Zones with generated artifacts in runtime: %d" % len(gen_in_runtime)],
lib/python/executable_repository_intelligence/recommendations.py:183:             evidence=["No file matched entry-point patterns"],
lib/python/executable_repository_intelligence/recommendations.py:220:             evidence=[
lib/python/executable_repository_intelligence/report.py:288:             evidence = rec.get("evidence", [])
lib/python/executable_repository_intelligence/report.py:289:             if evidence:
lib/python/executable_repository_intelligence/report.py:290:                 lines.append("**Evidence:**")
lib/python/executable_repository_intelligence/report.py:291:                 for e in evidence[:3]:
lib/python/executable_repository_intelligence/zone_classifier.py:103:                 evidence=self._build_evidence(dir_path, fcs, zone),
lib/python/executable_repository_intelligence/zone_classifier.py:141:         evidence = ["Zone: %s (%d files)" % (zone, len(fcs))]
lib/python/executable_repository_intelligence/zone_classifier.py:144:             evidence.append("%s: %d file(s)" % (cat, cnt))
lib/python/executable_repository_intelligence/zone_classifier.py:145:         return evidence
lib/python/executive_briefing_engine/generator.py:170:             if rec.evidence:
lib/python/executive_briefing_engine/generator.py:172:                 lines.append("**Evidence:**")
lib/python/executive_briefing_engine/generator.py:173:                 for ev in rec.evidence[:3]:
lib/python/executive_briefing_engine/generator.py:205:             if risk.evidence:
lib/python/executive_briefing_engine/generator.py:207:                 lines.append("**Evidence:**")
lib/python/executive_briefing_engine/generator.py:208:                 for ev in risk.evidence[:3]:
lib/python/executive_briefing_engine/models.py:43:     """Evidence-based executive recommendation."""
lib/python/executive_briefing_engine/models.py:55:     evidence: Tuple[str, ...]
lib/python/executive_briefing_engine/models.py:69:             "evidence": list(self.evidence),
lib/python/executive_briefing_engine/models.py:85:             evidence=tuple(data.get("evidence", [])),
lib/python/executive_briefing_engine/models.py:102:     evidence: Tuple[str, ...]
lib/python/executive_briefing_engine/models.py:113:             "evidence": list(self.evidence),
lib/python/executive_briefing_engine/models.py:126:             evidence=tuple(data.get("evidence", [])),
lib/python/executive_briefing_engine/recommendation_engine.py:5: Generates evidence-based executive recommendations from existing
lib/python/executive_briefing_engine/recommendation_engine.py:49:     Derives evidence-based executive recommendations from snapshot data.
lib/python/executive_briefing_engine/recommendation_engine.py:59:     dependencies, affected_components, reasoning, and evidence.
lib/python/executive_briefing_engine/recommendation_engine.py:125:                 evidence=(f"canonical_drift_findings={drift}",),
lib/python/executive_briefing_engine/recommendation_engine.py:147:                 evidence=(f"overall_coverage={coverage:.1f}%",),
lib/python/executive_briefing_engine/recommendation_engine.py:167:                 evidence=(f"overall_compliance={compliance:.1f}%",),
lib/python/executive_briefing_engine/recommendation_engine.py:187:                 evidence=(f"pending_batches={batches}",),
lib/python/executive_briefing_engine/recommendation_engine.py:227:                 evidence=tuple(str(r) for r in arch_risks[:3]),
lib/python/executive_briefing_engine/recommendation_engine.py:247:                 evidence=tuple(hotspots[:3]),
lib/python/executive_briefing_engine/recommendation_engine.py:268:                 evidence=("extension_points=[]",),
lib/python/executive_briefing_engine/recommendation_engine.py:302:                 evidence=tuple(blocked_tasks[:3]),
lib/python/executive_briefing_engine/recommendation_engine.py:324:                 evidence=(f"open_pull_requests={len(open_prs)}",),
lib/python/executive_briefing_engine/recommendation_engine.py:345:                 evidence=(f"current_recommendation={current_recommendation}",),
lib/python/executive_briefing_engine/recommendation_engine.py:383:                 evidence=tuple(r.title for r in critical_risks[:3]),
lib/python/executive_briefing_engine/recommendation_engine.py:404:                 evidence=(f"high_severity_risks={len(high_risks)}",),
lib/python/executive_briefing_engine/recommendation_engine.py:443:                 evidence=(f"semantic_recommendation_id={top_rec.get('id', 'N/A')}",),
lib/python/executive_briefing_engine/recommendation_engine.py:464:                 evidence=(f"suggested_next_core={next_core}",),
lib/python/executive_briefing_engine/recommendation_engine.py:491:             evidence=("all_health_checks_passed",),
lib/python/executive_briefing_engine/risk_analyzer.py:86:                 evidence=(description,),
lib/python/executive_briefing_engine/risk_analyzer.py:101:                 evidence=tuple(hotspots[:5]),
lib/python/executive_briefing_engine/risk_analyzer.py:131:                 evidence=(f"drift_findings={drift_count}",),
lib/python/executive_briefing_engine/risk_analyzer.py:147:                 evidence=(f"overall_coverage={coverage:.1f}%",),
lib/python/executive_briefing_engine/risk_analyzer.py:183:                 evidence=tuple(missing[:5]),
lib/python/executive_briefing_engine/risk_analyzer.py:216:                 evidence=tuple(str(b) for b in broken[:5]),
lib/python/executive_briefing_engine/risk_analyzer.py:244:                 evidence=tuple(str(c) for c in failed_checks[:5]),
lib/python/executive_briefing_engine/risk_analyzer.py:256:                 evidence=("state_sha256 is absent",),
lib/python/executive_briefing_engine/risk_analyzer.py:283:                 evidence=(f"failed_jobs={failed_jobs}",),
lib/python/executive_briefing_engine/risk_analyzer.py:305:                 evidence=(f"total_files={total_files}",),
lib/python/executive_briefing_engine/risk_analyzer.py:333:                 evidence=(f"pending_batches={batches}",),
lib/python/self_evaluation_engine/analyzers.py:6: evidence-based evaluation findings.
lib/python/self_evaluation_engine/analyzers.py:42:         evidence: List[str] = []
lib/python/self_evaluation_engine/analyzers.py:51:             evidence.append(f"CORE-007: {len(deviations)} deviation(s) detected")
lib/python/self_evaluation_engine/analyzers.py:53:             evidence.append(f"CORE-007 unavailable: {exc}")
lib/python/self_evaluation_engine/analyzers.py:62:             evidence=evidence,
lib/python/self_evaluation_engine/analyzers.py:98:         evidence: List[str] = []
lib/python/self_evaluation_engine/analyzers.py:114:                         evidence={"source": "CORE-008B"},
lib/python/self_evaluation_engine/analyzers.py:117:             evidence.append(f"CORE-008B: {len(risks)} risk(s) detected")
lib/python/self_evaluation_engine/analyzers.py:119:             evidence.append(f"CORE-008B unavailable: {exc}")
lib/python/self_evaluation_engine/analyzers.py:128:             evidence=evidence,
lib/python/self_evaluation_engine/analyzers.py:148:         evidence: List[str] = []
lib/python/self_evaluation_engine/analyzers.py:164:             evidence.append(f"CORE-008A: readiness={score:.0%}")
lib/python/self_evaluation_engine/analyzers.py:166:             evidence.append(f"CORE-008A unavailable: {exc}")
lib/python/self_evaluation_engine/analyzers.py:174:             evidence=evidence,
lib/python/self_evaluation_engine/analyzers.py:203:         evidence: List[str] = []
lib/python/self_evaluation_engine/analyzers.py:217:                     evidence={"missing_keys": sorted(missing_plan)},
lib/python/self_evaluation_engine/analyzers.py:220:         evidence.append(f"Planning keys checked: {sorted(self._REQUIRED_PLANNING_KEYS)}")
lib/python/self_evaluation_engine/analyzers.py:234:                     evidence={"missing_keys": sorted(missing_ctx)},
lib/python/self_evaluation_engine/analyzers.py:237:         evidence.append(f"Context keys checked: {sorted(self._REQUIRED_CONTEXT_KEYS)}")
lib/python/self_evaluation_engine/analyzers.py:246:             evidence=evidence,
lib/python/self_evaluation_engine/analyzers.py:296:             evidence=[f"Test coverage: {len(covered)}/{total} CORE packages"],
lib/python/self_evaluation_engine/analyzers.py:305: # Evidence Analyzer
lib/python/self_evaluation_engine/analyzers.py:309:     """Evaluate the quality of evidence produced by previous executions."""
lib/python/self_evaluation_engine/analyzers.py:312:         evidence_data = execution_data.get("evidence", {})
lib/python/self_evaluation_engine/analyzers.py:321:             evidence=[f"Evidence items collected: {count}"],
lib/python/self_evaluation_engine/analyzers.py:322:             findings=[] if count > 0 else ["No evidence items recorded in last execution"],
lib/python/self_evaluation_engine/analyzers.py:324:                 "Increase evidence collection coverage."
lib/python/self_evaluation_engine/analyzers.py:326:                 else "Evidence quality is adequate."
lib/python/self_evaluation_engine/engine.py:30:   .ai/self_evaluation/evidence.json
lib/python/self_evaluation_engine/engine.py:125:         # Evidence quality
lib/python/self_evaluation_engine/models.py:94:     """A single scored quality dimension with evidence."""
lib/python/self_evaluation_engine/models.py:99:     evidence: List[str]
lib/python/self_evaluation_engine/models.py:108:             "evidence": self.evidence,
lib/python/self_evaluation_engine/models.py:129:     evidence: Dict[str, Any]
lib/python/self_evaluation_engine/models.py:140:             "evidence": self.evidence,
lib/python/self_evaluation_engine/models.py:156:     evidence: Dict[str, Any]
lib/python/self_evaluation_engine/models.py:164:             "evidence": self.evidence,
lib/python/self_evaluation_engine/persistence.py:15:   evidence.json
lib/python/self_evaluation_engine/persistence.py:131:         # evidence.json
lib/python/self_evaluation_engine/persistence.py:132:         paths["evidence"] = self._write(
lib/python/self_evaluation_engine/persistence.py:133:             "evidence.json",
lib/python/self_evaluation_engine/scoring.py:6: All scoring is deterministic and evidence-based.
lib/python/self_evaluation_engine/scoring.py:50:                 evidence=["No quality scores provided"],
lib/python/self_evaluation_engine/scoring.py:58:         evidence: List[str] = []
lib/python/self_evaluation_engine/scoring.py:65:                 evidence.append(f"{dim}: {dim_score:.0%} (weight={weight:.0%})")
lib/python/self_evaluation_engine/scoring.py:74:             evidence=evidence,
lib/python/self_evaluation_engine/scoring.py:116:         evidence = [
lib/python/self_evaluation_engine/scoring.py:128:             evidence=evidence,
lib/python/self_improvement_engine/analyzers.py:92:                         evidence={"file": str(py_file)},
lib/python/self_improvement_engine/analyzers.py:116:                             evidence={"directory": str(pkg_dir)},
lib/python/self_improvement_engine/analyzers.py:164:                             evidence={"entry_count": len(entries), "source": "CORE-015"},
lib/python/self_improvement_engine/analyzers.py:187:                         evidence={"source": "CORE-016"},
lib/python/self_improvement_engine/analyzers.py:205:                     evidence={"directory": str(lib_python)},
lib/python/self_improvement_engine/analyzers.py:267:                         evidence={"missing_command": cmd, "source": "cli/main.py"},
lib/python/self_improvement_engine/analyzers.py:283:                         evidence={"missing_package": pkg},
lib/python/self_improvement_engine/generators.py:70:                     evidence=debt.evidence,
lib/python/self_improvement_engine/generators.py:101:                     evidence=gap.evidence,
lib/python/self_improvement_engine/generators.py:150:                     evidence={"issue_count": len(group), "priority": priority},
lib/python/self_improvement_engine/generators.py:178:         Generate CORE proposals only when the evidence justifies them.
lib/python/self_improvement_engine/generators.py:227:                     evidence={
lib/python/self_improvement_engine/generators.py:267:                     evidence={"evaluation_score": evaluation_score},
lib/python/self_improvement_engine/generators.py:285:                     evidence={"debt_count": len(high_debt)},
lib/python/self_improvement_engine/generators.py:303:                     evidence={"gap_ids": [g.gap_id for g in high_gaps]},
lib/python/self_improvement_engine/models.py:45:     evidence: Dict[str, Any]
lib/python/self_improvement_engine/models.py:56:             "evidence": self.evidence,
lib/python/self_improvement_engine/models.py:75:     evidence: Dict[str, Any]
lib/python/self_improvement_engine/models.py:85:             "evidence": self.evidence,
lib/python/self_improvement_engine/models.py:101:     evidence: Dict[str, Any]
lib/python/self_improvement_engine/models.py:109:             "evidence": self.evidence,
lib/python/self_improvement_engine/models.py:133:     evidence: Dict[str, Any]
lib/python/self_improvement_engine/models.py:151:             "evidence": self.evidence,
lib/python/self_improvement_engine/models.py:175:     evidence: Dict[str, Any]
lib/python/self_improvement_engine/models.py:189:             "evidence": self.evidence,
lib/python/self_improvement_engine/models.py:214:     evidence: Dict[str, Any]
lib/python/self_improvement_engine/models.py:231:             "evidence": self.evidence,
lib/python/self_improvement_engine/models.py:249:     evidence: Dict[str, Any]
lib/python/self_improvement_engine/models.py:259:             "evidence": self.evidence,
lib/python/semantic_matching/matcher.py:66:                             evidence=["Exact canonical component name '%s' found in %s" % (alias, wf.path)],
lib/python/semantic_matching/matcher.py:89:                             evidence=["Alias '%s' matched %s" % (alias, wf.path)],
lib/python/semantic_matching/matcher.py:115:                         evidence=[
lib/python/semantic_matching/matcher.py:131:                         evidence=["Behavioral symbol hits: %s" % ", ".join(symbol_hits[:6])],
lib/python/semantic_matching/matcher.py:155:                         evidence=partial_evidence,
lib/python/semantic_repository_intelligence/architecture_graph.py:272:                 evidence=["Import cycle: %s" % " → ".join(cycle + [cycle[0]])],
lib/python/semantic_repository_intelligence/architecture_graph.py:284:                 evidence=["in-degree: %d" % import_graph.in_degree.get(m, 0)],
lib/python/semantic_repository_intelligence/architecture_graph.py:297:                 evidence=["Layer classification: Uncategorised"],
lib/python/semantic_repository_intelligence/architecture_graph.py:309:                 evidence=["Outbound import count exceeds threshold"],
lib/python/semantic_repository_intelligence/confidence_engine.py:6: quantity of supporting evidence.
lib/python/semantic_repository_intelligence/confidence_engine.py:18:     - Number of evidence pieces (more = higher confidence)
lib/python/semantic_repository_intelligence/confidence_engine.py:27:     # Weights per evidence tier
lib/python/semantic_repository_intelligence/confidence_engine.py:37:         evidence: List[str],
lib/python/semantic_repository_intelligence/confidence_engine.py:48:         evidence:
lib/python/semantic_repository_intelligence/confidence_engine.py:49:             List of evidence strings (more items → higher score).
lib/python/semantic_repository_intelligence/confidence_engine.py:53:             Quality tier of evidence: 'ast', 'text_match', or 'heuristic'.
lib/python/semantic_repository_intelligence/confidence_engine.py:57:         # Evidence bonus: logarithmic to avoid trivially hitting 1.0
lib/python/semantic_repository_intelligence/confidence_engine.py:58:         n = max(0, len(evidence))
lib/python/semantic_repository_intelligence/confidence_engine.py:84:           - ``evidence`` (list[str])
lib/python/semantic_repository_intelligence/confidence_engine.py:95:                 evidence=finding.get("evidence", []),
lib/python/semantic_repository_intelligence/engine.py:55:     evidence-based recommendations.
lib/python/semantic_repository_intelligence/injection_point_analyzer.py:183:                     evidence=[snippet],
lib/python/semantic_repository_intelligence/injection_point_analyzer.py:203:                         evidence=["Class %s is abstract (bases: %s)" % (
lib/python/semantic_repository_intelligence/injection_point_analyzer.py:221:                             evidence=["@%s on %s" % (decorator, func.name)],
lib/python/semantic_repository_intelligence/models.py:298:     evidence: List[str]
lib/python/semantic_repository_intelligence/models.py:308:             "evidence": self.evidence,
lib/python/semantic_repository_intelligence/models.py:353:     evidence: List[str]
lib/python/semantic_repository_intelligence/models.py:363:             "evidence": self.evidence,
lib/python/semantic_repository_intelligence/models.py:380:     evidence: List[str]
lib/python/semantic_repository_intelligence/models.py:391:             "evidence": self.evidence,
lib/python/semantic_repository_intelligence/models.py:399:     """An evidence-based semantic recommendation."""
lib/python/semantic_repository_intelligence/models.py:407:     evidence: List[str]
lib/python/semantic_repository_intelligence/models.py:422:             "evidence": self.evidence,
lib/python/semantic_repository_intelligence/recommendation_engine.py:5: Generates evidence-based, prioritised recommendations from the semantic
lib/python/semantic_repository_intelligence/recommendation_engine.py:9:   - Supporting evidence
lib/python/semantic_repository_intelligence/recommendation_engine.py:90:                 evidence=[cycle_str],
lib/python/semantic_repository_intelligence/recommendation_engine.py:118:             evidence=["Orphan modules: %s" % ", ".join(sample)],
lib/python/semantic_repository_intelligence/recommendation_engine.py:145:                 evidence=["in-degree: %d" % in_deg],
lib/python/semantic_repository_intelligence/recommendation_engine.py:169:                 evidence=risk.evidence,
lib/python/semantic_repository_intelligence/recommendation_engine.py:199:                 evidence=["Extension points: %d" % ep_count, "Injection points: %d" % ip_count],
lib/python/semantic_repository_intelligence/recommendation_engine.py:224:                 evidence=["No manifest files detected"],
lib/python/semantic_repository_intelligence/recommendation_engine.py:243:                 evidence=["%d external dependencies" % dependency_graph.dependency_count],
lib/python/semantic_repository_intelligence/recommendation_engine.py:267:                 evidence=["No entry points found in call graph"],
lib/python/semantic_repository_intelligence/recommendation_engine.py:301:                 evidence=["in-degree: %d" % import_graph.in_degree.get(mod, 0)],
lib/python/semantic_repository_intelligence/recommendation_engine.py:317:                 evidence=["%d instances" % count],
lib/python/semantic_repository_intelligence/recommendation_engine.py:335:                     evidence=["in-degree: %d, out-degree: %d" % (node.in_degree, node.out_degree)],
lib/python/workspace_orchestrator/dependency_graph.py:109:                         evidence=(f"{repo.name} explicitly lists {dep} as a dependency",),
lib/python/workspace_orchestrator/dependency_graph.py:146:                             evidence=(f"Shared canonical spec: {spec}",),
lib/python/workspace_orchestrator/dependency_graph.py:173:                         evidence=tuple(f"Shared library: {lib}" for lib in sorted(shared)[:5]),
lib/python/workspace_orchestrator/intelligence.py:8: WorkspaceRecommendationEngine:  produces evidence-based workspace recommendations
lib/python/workspace_orchestrator/intelligence.py:194:     The Owner-first workflow:  one repository at a time, fully evidence-based.
lib/python/workspace_orchestrator/intelligence.py:350:             evidence=tuple(
lib/python/workspace_orchestrator/intelligence.py:372:                 evidence=tuple(f"{r.name}: canonical_status=missing" for r in missing),
lib/python/workspace_orchestrator/intelligence.py:385:                 evidence=tuple(f"{r.name}: canonical_status=partial" for r in partial),
lib/python/workspace_orchestrator/intelligence.py:403:             evidence=tuple(f"{r.name}: development_state=blocked" for r in blocked),
lib/python/workspace_orchestrator/intelligence.py:421:             evidence=tuple(
lib/python/workspace_orchestrator/intelligence.py:440:             evidence=tuple(f"{r.name}: readiness={r.readiness:.0f}%" for r in low),
lib/python/workspace_orchestrator/intelligence.py:465:             evidence=tuple(f"{r.name}: no dependency edges" for r in isolated),
lib/python/workspace_orchestrator/intelligence.py:471:     Produces evidence-based workspace recommendations for the owner.
lib/python/workspace_orchestrator/intelligence.py:507:                 evidence=("Overall workspace health is healthy",),
lib/python/workspace_orchestrator/intelligence.py:537:             evidence=(f"Ranked #{top.rank} in workspace priority list",),
lib/python/workspace_orchestrator/intelligence.py:558:                 evidence=risk.evidence,
lib/python/workspace_orchestrator/intelligence.py:581:             evidence=tuple(f"{r.name}: canonical_status=missing" for r in missing[:5]),
lib/python/workspace_orchestrator/intelligence.py:604:             evidence=(
lib/python/workspace_orchestrator/models.py:221:     evidence: Tuple[str, ...] = ()
lib/python/workspace_orchestrator/models.py:229:             "evidence": list(self.evidence),
lib/python/workspace_orchestrator/models.py:239:             evidence=tuple(data.get("evidence", [])),
lib/python/workspace_orchestrator/models.py:352:     """Evidence-based workspace-level recommendation for the owner."""
lib/python/workspace_orchestrator/models.py:364:     evidence: Tuple[str, ...] = ()
lib/python/workspace_orchestrator/models.py:378:             "evidence": list(self.evidence),
lib/python/workspace_orchestrator/models.py:394:             evidence=tuple(data.get("evidence", [])),
lib/python/workspace_orchestrator/models.py:414:     evidence: Tuple[str, ...] = ()
lib/python/workspace_orchestrator/models.py:425:             "evidence": list(self.evidence),
lib/python/workspace_orchestrator/models.py:438:             evidence=tuple(data.get("evidence", [])),
lib/python/workspace_orchestrator/persistence.py:13:   recommendations.json    evidence-based workspace recommendations
tests/test_autonomous_execution_engine.sh:143: evidence = collector.collect()
tests/test_autonomous_execution_engine.sh:144: assert evidence["evidence_count"] == 2
tests/test_autonomous_execution_engine.sh:145: assert len(evidence["items"]) == 2
tests/test_evidence_engine.sh:15: for name, evidence in audit["evidence"].items():
tests/test_evidence_engine.sh:20:         len(evidence["python"]) +
tests/test_evidence_engine.sh:21:         len(evidence["shell"]) +
tests/test_evidence_engine.sh:22:         len(evidence["tests"]) +
tests/test_evidence_engine.sh:23:         len(evidence["docs"])
tests/test_evidence_engine.sh:26:     print("Evidence:", total)
tests/test_evidence_engine.sh:30: print("Evidence Engine PASS")
tests/test_executable_repository_intelligence.sh:277:     assert 'evidence' in d
tests/test_executable_repository_intelligence.sh:403:             {'path': '.', 'zone': 'Runtime', 'file_count': 5, 'evidence': ['Zone: Runtime']},
tests/test_executable_repository_intelligence.sh:404:             {'path': 'docs', 'zone': 'Documentation', 'file_count': 3, 'evidence': ['Zone: Documentation']},
tests/test_executable_repository_intelligence.sh:409:              'evidence': ['evidence1'], 'affected_files': ['main.py']},
tests/test_executable_repository_intelligence.sh:414:              'confidence': 0.95, 'evidence': ['matched']}
tests/test_executive_briefing_engine.sh:257:             reasoning="Evidence shows drift.",
tests/test_executive_briefing_engine.sh:258:             evidence=("drift_findings=3",),
tests/test_executive_briefing_engine.sh:279:             evidence=("drift=8",),
tests/test_executive_briefing_engine.sh:480:             self.assertTrue(len(rec.evidence) >= 1, f"{rec.id} has no evidence")
tests/test_executive_briefing_engine.sh:663:                     reasoning="Drift detected.", evidence=("drift=3",),
tests/test_executive_briefing_engine.sh:671:                     evidence=("drift=2",), affected_components=(), remediation="Resolve drift.",
tests/test_self_evaluation_engine.sh:71:     evidence=["CORE-007: 0 deviations"],
tests/test_self_evaluation_engine.sh:79: assert isinstance(d["evidence"], list)
tests/test_self_evaluation_engine.sh:95:     evidence={"missing": ["planning_id"]},
tests/test_self_evaluation_engine.sh:112:     evidence={"source": "CORE-008B"},
tests/test_self_evaluation_engine.sh:211: good_evidence = ev_analyzer.analyze({"evidence": {"evidence_count": 15}})
tests/test_self_evaluation_engine.sh:296:                 "coverage", "regressions", "evidence", "history", "snapshot"):
tests/test_self_evaluation_engine.sh:339:             "architecture", "coverage", "regressions", "evidence",
tests/test_self_improvement_engine.sh:71:     evidence={"file": "old_engine.py"},
tests/test_self_improvement_engine.sh:91:     evidence={"source": "CORE-015"},
tests/test_self_improvement_engine.sh:108:     evidence={"source": "cli/main.py"},
tests/test_self_improvement_engine.sh:132:     evidence={"debt_id": "DEBT-001"},
tests/test_self_improvement_engine.sh:157:     evidence={"priority": "medium"},
tests/test_semantic_repository_intelligence.sh:222: # Zero evidence
tests/test_semantic_repository_intelligence.sh:232:     {'base_confidence': 0.7, 'evidence': ['a', 'b'], 'evidence_tier': 'ast'},
tests/test_semantic_repository_intelligence.sh:233:     {'base_confidence': 0.5, 'evidence': [], 'evidence_tier': 'heuristic'},
tests/test_semantic_repository_intelligence.sh:274:     assert 'evidence' in d
tests/test_workspace_orchestrator.sh:183:             evidence=("explicit dep",),
tests/test_workspace_orchestrator.sh:190:         assert r.evidence == ("explicit dep",)
```

Matches: 937

### Term: `provenance`

```text
lib/python/canonical_entities/models.py:106:     provenance: str = ""
lib/python/cdm_engine/engine.py:15:   - provenance preservation
lib/python/cdm_engine/engine.py:90:     provenance: str = ""
lib/python/cdm_engine/engine.py:117:             "provenance": self.provenance,
lib/python/cdm_engine/engine.py:232:             provenance=path,
lib/python/context_synchronization_engine/engine.py:936:             provenance={
lib/python/context_synchronization_engine/engine.py:976:             provenance={
lib/python/context_synchronization_engine/engine.py:1008:             provenance={
lib/python/context_synchronization_engine/engine.py:1037:             provenance={
lib/python/context_synchronization_engine/engine.py:1067:             provenance=live_context.get("sources", {}),
lib/python/context_synchronization_engine/engine.py:1099:             provenance={
lib/python/context_synchronization_engine/engine.py:1144:             provenance={
lib/python/context_synchronization_engine/engine.py:1178:             provenance={
lib/python/context_synchronization_engine/engine.py:1215:             provenance={
lib/python/context_synchronization_engine/engine.py:1245:             provenance={
lib/python/context_synchronization_engine/engine.py:1417:         provenance: Mapping[str, Any],
lib/python/context_synchronization_engine/engine.py:1428:             provenance=dict(self._sorted_mapping(provenance)),
lib/python/context_synchronization_engine/models.py:108:     provenance: Optional[Dict[str, Any]] = None
lib/python/context_synchronization_engine/models.py:122:             "provenance": _normalize_mapping(self.provenance or {}),
lib/python/context_synchronization_engine/models.py:136:             provenance=dict(_normalize_mapping(data.get("provenance", {}))),
lib/python/knowledge_graph/builder.py:33:                     provenance=doc.filename,
lib/python/knowledge_graph/builder.py:46:                         provenance=doc.id,
lib/python/knowledge_graph/builder.py:69:                             provenance=doc.id,
lib/python/knowledge_graph/builder.py:93:                             provenance=doc.id,
lib/python/knowledge_graph/graph.py:56:                     "provenance": node.provenance,
lib/python/knowledge_graph/graph.py:84:                     provenance=node_data.get("provenance", ""),
lib/python/knowledge_materialization/engine.py:168:                 provenance=doc.path,
lib/python/knowledge_materialization/engine.py:181:                     provenance=doc.identifier,
lib/python/knowledge_materialization/engine.py:225:                 provenance=std.path,
lib/python/knowledge_materialization/engine.py:240:                         provenance=source_id,
lib/python/knowledge_materialization/engine.py:266:                         provenance=source_id,
```

Matches: 31

### Term: `repository`

```text
.ai/audit/execution_plan.json:6:       "identifier": "TASK-REPOSITORY",
.ai/audit/foundation_audit_001.json:2:   "repository": "AI-Toolkit",
.ai/audit/foundation_audit_001.json:3:   "audit": "AUD-001 Repository Architecture",
.ai/audit/repository_inspector_v2.json:2:   "repository": {
.ai/audit/repository_inspector_v2.json:21:         "identifier": "TASK-REPOSITORY",
.ai/audit/repository_inventory.json:2:   "repository": "AI-Toolkit",
.ai/audit/repository_inventory_v2.json:309:     "path": "bootstrap/repository",
.ai/audit/repository_inventory_v2.json:310:     "name": "repository",
.ai/backups/core021a002/test_repository_engine_v2.py:28: print("Repository Engine PASS")
.ai/batches/BATCH-002/metadata.json:5:   "reason": "Repository semantic model can be enriched.",
.ai/context/development_context.json:22:   "repository": "caliofmarian-ai/AI-Toolkit",
.ai/context/git_context.json:10:   "repository": "AI-Toolkit",
.ai/context/github_context.json:7:   "repository": "caliofmarian-ai/AI-Toolkit"
.ai/context/live_context.json:37:   "repository": "caliofmarian-ai/AI-Toolkit",
.ai/context/live_context.json:54:     "repository": "github",
.ai/context/repository_profile.json:2:   "repository": "AI-Toolkit",
.ai/context/repository_profile.json:4:   "branch": "feature/repository-inspector",
.ai/context/synchronization_report.json:22:   "repository": "caliofmarian-ai/AI-Toolkit",
.ai/development_state/current_state.json:55:     "repository": "caliofmarian-ai/AI-Toolkit",
.ai/development_state/executive_snapshot.json:388:       "repository": "caliofmarian-ai/AI-Toolkit",
.ai/executable_repository_map.json:3:   "repository": "/home/runner/work/AI-Toolkit/AI-Toolkit",
.ai/execution/execution.json:20:     "repository": "/storage/emulated/0/AI-Projects/AI-Toolkit",
.ai/execution/execution.json:88:             "repository": "caliofmarian-ai/AI-Toolkit",
.ai/execution/execution.json:243:           "executive_summary": "The caliofmarian-ai/AI-Toolkit repository has areas requiring attention.  Architecture health: healthy. Canonical health: critical. Development health: healthy.  Repository health: healthy. Runtime health: unknown.  4 risk(s) identified.  8 recommendation(s) generated.",
.ai/execution/execution.json:445:               "reasoning": "CORE module suggestions are derived from current repository intelligence gaps and architectural extension points.",
.ai/execution/execution.json:450:           "repository": "/home/runner/work/AI-Toolkit/AI-Toolkit",
.ai/execution/execution.json:619:           "repository": "/home/runner/work/AI-Toolkit/AI-Toolkit",
.ai/execution/execution.json:666:   "repository": "/storage/emulated/0/AI-Projects/AI-Toolkit",
.ai/execution/execution_context.json:17:   "repository": "/storage/emulated/0/AI-Projects/AI-Toolkit",
.ai/execution/execution_evidence.json:60:           "repository": "caliofmarian-ai/AI-Toolkit",
.ai/execution/execution_evidence.json:215:         "executive_summary": "The caliofmarian-ai/AI-Toolkit repository has areas requiring attention.  Architecture health: healthy. Canonical health: critical. Development health: healthy.  Repository health: healthy. Runtime health: unknown.  4 risk(s) identified.  8 recommendation(s) generated.",
.ai/execution/execution_evidence.json:417:             "reasoning": "CORE module suggestions are derived from current repository intelligence gaps and architectural extension points.",
.ai/execution/execution_evidence.json:422:         "repository": "/home/runner/work/AI-Toolkit/AI-Toolkit",
.ai/execution/execution_evidence.json:591:         "repository": "/home/runner/work/AI-Toolkit/AI-Toolkit",
.ai/execution/execution_history.json:9:       "repository": "/home/runner/work/AI-Toolkit/AI-Toolkit",
.ai/execution/execution_history.json:20:       "repository": "/home/runner/work/AI-Toolkit/AI-Toolkit",
.ai/execution/execution_history.json:31:       "repository": "/home/runner/work/AI-Toolkit/AI-Toolkit",
.ai/execution/execution_history.json:42:       "repository": "/home/runner/work/AI-Toolkit/AI-Toolkit",
.ai/execution/execution_history.json:53:       "repository": "/home/runner/work/AI-Toolkit/AI-Toolkit",
.ai/execution/execution_history.json:64:       "repository": "/home/runner/work/AI-Toolkit/AI-Toolkit",
.ai/execution/execution_history.json:75:       "repository": "/home/runner/work/AI-Toolkit/AI-Toolkit",
.ai/execution/execution_history.json:86:       "repository": "/home/runner/work/AI-Toolkit/AI-Toolkit",
.ai/execution/execution_history.json:97:       "repository": "/home/runner/work/AI-Toolkit/AI-Toolkit",
.ai/execution/execution_history.json:108:       "repository": "/home/runner/work/AI-Toolkit/AI-Toolkit",
.ai/execution/execution_history.json:119:       "repository": "/home/runner/work/AI-Toolkit/AI-Toolkit",
.ai/execution/execution_history.json:130:       "repository": "/home/runner/work/AI-Toolkit/AI-Toolkit",
.ai/execution/execution_history.json:141:       "repository": "/home/runner/work/AI-Toolkit/AI-Toolkit",
.ai/execution/execution_history.json:152:       "repository": "/home/runner/work/AI-Toolkit/AI-Toolkit",
.ai/execution/execution_history.json:163:       "repository": "/home/runner/work/AI-Toolkit/AI-Toolkit",
.ai/execution/execution_history.json:174:       "repository": "/home/runner/work/AI-Toolkit/AI-Toolkit",
.ai/execution/execution_history.json:185:       "repository": "/home/runner/work/AI-Toolkit/AI-Toolkit",
.ai/execution/execution_history.json:196:       "repository": "/home/runner/work/AI-Toolkit/AI-Toolkit",
.ai/execution/execution_history.json:207:       "repository": "/storage/emulated/0/AI-Projects/AI-Toolkit",
.ai/execution/execution_history.json:215:   "repository": "/storage/emulated/0/AI-Projects/AI-Toolkit",
.ai/execution/execution_report.json:12:   "repository": "/storage/emulated/0/AI-Projects/AI-Toolkit",
.ai/executive/briefing.json:51:   "executive_summary": "The caliofmarian-ai/AI-Toolkit repository is healthy.  Architecture health: healthy. Canonical health: healthy. Development health: healthy.  Repository health: healthy. Runtime health: unknown.  2 risk(s) identified.  3 recommendation(s) generated.",
.ai/executive/briefing.json:152:       "reasoning": "CORE module suggestions are derived from current repository intelligence gaps and architectural extension points.",
.ai/executive/briefing.json:157:   "repository": "/home/runner/work/AI-Toolkit/AI-Toolkit",
.ai/executive/recommendations.json:54:       "reasoning": "CORE module suggestions are derived from current repository intelligence gaps and architectural extension points.",
.ai/memory/history.json:2:   "repository": "AI-Toolkit",
.ai/memory/index.json:2:   "repository": "AI-Toolkit",
.ai/memory/knowledge_graph.json:2:   "repository": "AI-Toolkit",
.ai/memory/repository_profile_1.json:2:   "repository": "AI-Toolkit",
.ai/memory/repository_profile_1.json:4:   "branch": "feature/repository-inspector",
.ai/memory/repository_profile_2.json:2:   "repository": "AI-Toolkit",
.ai/memory/repository_profile_2.json:4:   "branch": "feature/repository-inspector",
.ai/memory/workflow.json:7:       "engine": "Repository Inspector",
.ai/planning/execution_queue.json:151:   "repository": "/home/runner/work/AI-Toolkit/AI-Toolkit",
.ai/planning/next_actions.json:68:   "repository": "/home/runner/work/AI-Toolkit/AI-Toolkit"
.ai/planning/planning.json:152:     "repository": "/home/runner/work/AI-Toolkit/AI-Toolkit",
.ai/planning/planning.json:223:     "repository": "/home/runner/work/AI-Toolkit/AI-Toolkit"
.ai/planning/planning.json:290:   "repository": "/home/runner/work/AI-Toolkit/AI-Toolkit",
.ai/planning/planning.json:316:     "repository": "/home/runner/work/AI-Toolkit/AI-Toolkit",
.ai/planning/roadmap_progress.json:26:   "repository": "/home/runner/work/AI-Toolkit/AI-Toolkit",
.ai/reports/inspect-20260807.json:2501:       "path": "implementation-packages/CORE-022/repository-audit.md",
.ai/reports/inspect-20260807.json:2564:       "path": "implementation-packages/CORE-023/repository-audit.md",
.ai/reports/inspect-20260807.json:2592:       "path": "implementation-packages/PLATFORM/repository-audit.md",
.ai/reports/inspect-20260807.json:3145:       "path": "lib/python/canonical_repository/repository.py",
.ai/reports/inspect-20260807.json:3292:       "path": "lib/python/development_state_engine/repository.py",
.ai/reports/inspect-20260807.json:5987:       "path": "standards/csl/shared/rfc/RFC-0007-REPOSITORY-ADAPTER-ARCHITECTURE.md",
.ai/reports/inspect-20260807.json:7446:     "summary": "Repository is operationally healthy.",
.ai/reports/inspect-20260807.json:7449:         "name": "Repository has source files",
.ai/reports/inspect-20260807.json:7454:         "name": "Repository has tests",
.ai/reports/inspect-20260807.json:7459:         "name": "Repository has documentation",
.ai/reports/inspect-20260807.json:7464:         "name": "Repository has entry points",
.ai/reports/inspect-20260807.json:7469:         "name": "Repository has dependency metadata",
.ai/runtime_repository_model.json:3:   "repository": "/home/runner/work/AI-Toolkit/AI-Toolkit",
.ai/runtime_repository_model.json:6:     "repository": "/home/runner/work/AI-Toolkit/AI-Toolkit",
.ai/runtime_repository_model.json:1303:         "path": "lib/python/canonical_repository/repository.py",
.ai/runtime_repository_model.json:2892:           "name": "repository",
.ai/runtime_repository_model.json:2893:           "file": "lib/python/canonical_repository/repository.py",
.ai/runtime_repository_model.json:3870:         "lib/python/canonical_repository/repository.py",
.ai/runtime_repository_model.json:4059:         "lib/python/canonical_repository/repository.py",
.ai/runtime_repository_model.json:4506:           "target": "lib/python/canonical_repository/repository.py",
.ai/runtime_repository_model.json:4510:           "source": "lib/python/canonical_repository/repository.py",
.ai/runtime_repository_model.json:5604:         "file": "lib/python/canonical_repository/repository.py",
.ai/self_evaluation/evaluation.json:55:     "repository": "/storage/emulated/0/AI-Projects/AI-Toolkit",
.ai/self_evaluation/evaluation.json:100:       "recommendation": "Repository health is good.",
.ai/self_evaluation/evaluation.json:107:         "Context keys checked: ['current_branch', 'repository']"
.ai/self_evaluation/evaluation.json:110:         "Missing context keys: ['current_branch', 'repository']"
.ai/self_evaluation/evaluation.json:181:           "repository"
.ai/self_evaluation/evaluation.json:184:       "finding": "Missing context keys: ['current_branch', 'repository']",
.ai/self_evaluation/evaluation.json:190:   "repository": "/storage/emulated/0/AI-Projects/AI-Toolkit",
.ai/self_evaluation/evaluation.json:192:   "summary": "Evaluation EVAL-D2C6C4F0 completed. Overall engineering quality: 89% (PASS). Repository: AI-Toolkit.",
.ai/self_evaluation/evidence.json:38:       "recommendation": "Repository health is good.",
.ai/self_evaluation/evidence.json:45:         "Context keys checked: ['current_branch', 'repository']"
.ai/self_evaluation/evidence.json:48:         "Missing context keys: ['current_branch', 'repository']"
.ai/self_evaluation/history.json:7:       "repository": "/home/runner/work/AI-Toolkit/AI-Toolkit",
.ai/self_evaluation/history.json:14:       "repository": "/home/runner/work/AI-Toolkit/AI-Toolkit",
.ai/self_evaluation/history.json:21:       "repository": "/home/runner/work/AI-Toolkit/AI-Toolkit",
.ai/self_evaluation/history.json:28:       "repository": "/home/runner/work/AI-Toolkit/AI-Toolkit",
.ai/self_evaluation/history.json:35:       "repository": "/home/runner/work/AI-Toolkit/AI-Toolkit",
.ai/self_evaluation/history.json:42:       "repository": "/home/runner/work/AI-Toolkit/AI-Toolkit",
.ai/self_evaluation/history.json:49:       "repository": "/home/runner/work/AI-Toolkit/AI-Toolkit",
.ai/self_evaluation/history.json:56:       "repository": "/home/runner/work/AI-Toolkit/AI-Toolkit",
.ai/self_evaluation/history.json:63:       "repository": "/home/runner/work/AI-Toolkit/AI-Toolkit",
.ai/self_evaluation/history.json:70:       "repository": "/home/runner/work/AI-Toolkit/AI-Toolkit",
.ai/self_evaluation/history.json:77:       "repository": "/home/runner/work/AI-Toolkit/AI-Toolkit",
.ai/self_evaluation/history.json:84:       "repository": "/home/runner/work/AI-Toolkit/AI-Toolkit",
.ai/self_evaluation/history.json:91:       "repository": "/home/runner/work/AI-Toolkit/AI-Toolkit",
.ai/self_evaluation/history.json:98:       "repository": "/home/runner/work/AI-Toolkit/AI-Toolkit",
.ai/self_evaluation/history.json:105:       "repository": "/home/runner/work/AI-Toolkit/AI-Toolkit",
.ai/self_evaluation/history.json:112:       "repository": "/home/runner/work/AI-Toolkit/AI-Toolkit",
.ai/self_evaluation/history.json:119:       "repository": "/storage/emulated/0/AI-Projects/AI-Toolkit",
.ai/self_evaluation/history.json:125:   "repository": "/storage/emulated/0/AI-Projects/AI-Toolkit",
.ai/self_evaluation/quality.json:40:       "recommendation": "Repository health is good.",
.ai/self_evaluation/quality.json:47:         "Context keys checked: ['current_branch', 'repository']"
.ai/self_evaluation/quality.json:50:         "Missing context keys: ['current_branch', 'repository']"
.ai/self_evaluation/regressions.json:15:           "repository"
.ai/self_evaluation/regressions.json:18:       "finding": "Missing context keys: ['current_branch', 'repository']",
.ai/self_evaluation/snapshot.json:9:     "repository": "/storage/emulated/0/AI-Projects/AI-Toolkit",
.ai/self_improvement/history.json:8:       "repository": "/home/runner/work/AI-Toolkit/AI-Toolkit",
.ai/self_improvement/history.json:17:       "repository": "/home/runner/work/AI-Toolkit/AI-Toolkit",
.ai/self_improvement/history.json:26:       "repository": "/home/runner/work/AI-Toolkit/AI-Toolkit",
.ai/self_improvement/history.json:35:       "repository": "/home/runner/work/AI-Toolkit/AI-Toolkit",
.ai/self_improvement/history.json:44:       "repository": "/home/runner/work/AI-Toolkit/AI-Toolkit",
.ai/self_improvement/history.json:53:       "repository": "/home/runner/work/AI-Toolkit/AI-Toolkit",
.ai/self_improvement/history.json:62:       "repository": "/home/runner/work/AI-Toolkit/AI-Toolkit",
.ai/self_improvement/history.json:71:       "repository": "/home/runner/work/AI-Toolkit/AI-Toolkit",
.ai/self_improvement/history.json:80:       "repository": "/home/runner/work/AI-Toolkit/AI-Toolkit",
.ai/self_improvement/history.json:89:       "repository": "/home/runner/work/AI-Toolkit/AI-Toolkit",
.ai/self_improvement/history.json:98:       "repository": "/home/runner/work/AI-Toolkit/AI-Toolkit",
.ai/self_improvement/history.json:107:       "repository": "/storage/emulated/0/AI-Projects/AI-Toolkit",
.ai/self_improvement/history.json:114:   "repository": "/storage/emulated/0/AI-Projects/AI-Toolkit",
.ai/self_improvement/improvements.json:458:   "repository": "/storage/emulated/0/AI-Projects/AI-Toolkit",
.ai/self_improvement/optimization_plan.json:458:   "repository": "/storage/emulated/0/AI-Projects/AI-Toolkit",
.ai/self_improvement/snapshot.json:6:   "repository": "/storage/emulated/0/AI-Projects/AI-Toolkit",
.ai/semantic_knowledge.json:3:   "repository": "/home/runner/work/AI-Toolkit/AI-Toolkit",
.ai/sessions/SESSION-20260803-050009.json:3:   "repository": ".",
.ai/sessions/SESSION-20260803-050013.json:3:   "repository": ".",
lib/context_engine.sh:17: echo "## Repository"
lib/execution_engine.sh:18: echo "Repository: $ROOT" | tee "$LOG"
lib/issue_engine.sh:38: echo "[4/7] Repository summary"
lib/planner_engine.sh:19: Repository:
lib/planner_engine.sh:26: - Inspect repository
lib/python/agent_runtime/models.py:8:     repository: str = "."
lib/python/agents/ai_cto_scanner_agent.py:17:     Inspects an arbitrary repository and produces an AI CTO integration
lib/python/agents/ai_cto_scanner_agent.py:25:         repository = context.repository or "."
lib/python/agents/ai_cto_scanner_agent.py:28:         engine = AICTOScannerEngine(repository=repository, output_dir=output_dir)
lib/python/agents/ai_cto_scanner_agent.py:35:                 "repository": scan_result["repository"],
lib/python/agents/development_agent.py:40:         repository = context.repository
lib/python/agents/development_agent.py:47:         # Phase 1 — Incremental repository traversal (CORE-006)
lib/python/agents/development_agent.py:54:             lambda: IncrementalWorkspaceIndex(repository, policy=policy).build(),
lib/python/agents/development_agent.py:77:         report["repository"] = profiler.run(
lib/python/agents/development_agent.py:79:             lambda: RepositoryEngine(repository, workspace_index=workspace_index).statistics(),
lib/python/agents/development_agent.py:84:             lambda: DependencyEngine(repository, workspace_index=workspace_index).statistics(),
lib/python/agents/development_agent.py:89:             lambda: ValidationEngine(repository).statistics(),
lib/python/agents/development_agent.py:94:             lambda: PlanningEngine(repository, workspace_index=workspace_index).build_plan(),
lib/python/agents/development_agent.py:99:             lambda: RepositoryInspectorV2(repository, workspace_index=workspace_index).inspect(),
lib/python/agents/development_agent.py:104:             lambda: CanonicalAuditEngine(repository, workspace_index=workspace_index).audit(),
lib/python/agents/development_agent.py:109:             lambda: SemanticEngine(repository, workspace_index=workspace_index).analyze(),
lib/python/agents/development_agent.py:114:             lambda: KnowledgeGraphEngine(repository, workspace_index=workspace_index).build(),
lib/python/agents/development_agent.py:159:                 Path(repository).parent
lib/python/agents/development_report.py:16:         report.append(f"Repository files: {result['repository']['files']}")
lib/python/agents/repository_inspector_agent.py:13:         engine = RepositoryInspectorV2(context.repository)
lib/python/agents/repository_inspector_agent.py:22:                 "Repository inspection completed."
lib/python/ai_control_center/application.py:17:     def __init__(self, repository: str | Path):
lib/python/ai_control_center/application.py:21:         self.repository_provider = LocalRepositoryProvider(repository)
lib/python/ai_control_center/application.py:34:             "repository": self.repository_provider.summary(),
lib/python/ai_control_center/panels/repository/panel.py:4: Repository Panel
lib/python/ai_control_center/panels/repository/panel.py:6: Unified Repository View
lib/python/ai_control_center/providers/local_repository.py:4: Local Repository Provider
lib/python/ai_control_center/providers/local_repository.py:33:         return "Local Repository"
lib/python/ai_cto_scanner/__init__.py:5: Inspects an arbitrary software repository and understands its architecture.
lib/python/ai_cto_scanner/engine.py:40:     Inspects an arbitrary software repository and produces an
lib/python/ai_cto_scanner/engine.py:54:     def __init__(self, repository=".", output_dir=None):
lib/python/ai_cto_scanner/engine.py:55:         self.root = Path(repository).resolve()
lib/python/ai_cto_scanner/engine.py:104:             "repository": str(self.root),
lib/python/ai_cto_scanner/engine.py:117:         # Phase 6 — Semantic repository intelligence (CORE-008B)
lib/python/ai_cto_scanner/engine.py:122:                 repository=str(self.root),
lib/python/ai_cto_scanner/report.py:65:             "| Repository | `%s` |" % r["repository"],
lib/python/ai_cto_scanner/report.py:84:             "The AI CTO Integration Scanner analysed **`%s`** and produced the following assessment." % r["repository"],
lib/python/ai_cto_scanner/report.py:141:             "Key files and locations where AI CTO can integrate with the repository.",
lib/python/ai_cto_scanner/report.py:251:             "Components not yet detected in the repository.",
lib/python/ai_cto_scanner/report.py:319:             lines.append("| Repository not ready for AI CTO integration | CRITICAL | All | Address missing components in priority order |")
lib/python/ai_cto_scanner/report.py:452:             "> *Report generated by CORE-008A AI CTO Integration Scanner / CORE-008B Semantic Repository Intelligence.*",
lib/python/ai_cto_scanner/report.py:567:             "Modules with the highest import in-degree — the architectural backbone of the repository.",
lib/python/ai_cto_scanner/report.py:689:             "## Repository Complexity",
lib/python/ai_platform/adapters.py:58:             f"Repository health: {health}.",
lib/python/ai_platform/adapters.py:73:             answer_lines.append("Answer generated with repository-aware engineering context.")
lib/python/ai_platform/prompt_library.py:8:         {"name": "implementation_strategy", "prompt": "Generate an implementation strategy for the current repository context."},
lib/python/ai_platform/prompt_library.py:11:         {"name": "architecture_review", "prompt": "Explain the repository architecture and identify extension points."},
lib/python/ai_platform/prompt_library.py:13:     "Repository Audit": [
lib/python/ai_platform/prompt_library.py:14:         {"name": "audit_risks", "prompt": "Find architectural and delivery risks in the repository."},
lib/python/ai_platform/service.py:81:                     "repository": context.get("repository_profile", {}).get("name", ""),
lib/python/ai_platform/service.py:197:                     "repository": item.get("repository", ""),
lib/python/ai_platform/sessions.py:20:             "repository": payload.get("repository", self.root.name),
lib/python/autonomous_execution_engine/__init__.py:13:     engine = AutonomousExecutionEngine(repository="/path/to/repo")
lib/python/autonomous_execution_engine/engine.py:13:   CORE-008B Semantic Repository Intelligence
lib/python/autonomous_execution_engine/engine.py:14:   CORE-008C Executable Repository Intelligence
lib/python/autonomous_execution_engine/engine.py:84: def _execution_id(repository: str, generated_at: str) -> str:
lib/python/autonomous_execution_engine/engine.py:86:         f"{repository}{generated_at}".encode("utf-8")
lib/python/autonomous_execution_engine/engine.py:216:         engine = AutonomousExecutionEngine(repository="/path/to/repo")
lib/python/autonomous_execution_engine/engine.py:228:         repository: str = ".",
lib/python/autonomous_execution_engine/engine.py:235:         self.root = Path(repository).resolve()
lib/python/autonomous_execution_engine/engine.py:252:         self._validator = ExecutionValidator(repository=str(self.root))
lib/python/autonomous_execution_engine/engine.py:476:             repository=str(self.root),
lib/python/autonomous_execution_engine/engine.py:636:             repository=str(self.root),
lib/python/autonomous_execution_engine/logger.py:80:             "repository": result_dict.get("repository", ""),
lib/python/autonomous_execution_engine/models.py:114:     repository: str
lib/python/autonomous_execution_engine/models.py:139:             "repository": self.repository,
lib/python/autonomous_execution_engine/models.py:291:     repository: str
lib/python/autonomous_execution_engine/models.py:312:             "repository": self.repository,
lib/python/autonomous_execution_engine/models.py:341:     repository: str
lib/python/autonomous_execution_engine/models.py:353:             "repository": self.repository,
lib/python/autonomous_execution_engine/models.py:369:     """Complete ordered history of execution runs for one repository."""
lib/python/autonomous_execution_engine/models.py:371:     repository: str
lib/python/autonomous_execution_engine/models.py:378:             "repository": self.repository,
lib/python/autonomous_execution_engine/persistence.py:146:             "repository": d.get("repository", ""),
lib/python/autonomous_execution_engine/persistence.py:156:             "repository": d.get("repository", ""),
lib/python/autonomous_execution_engine/report.py:63:         lines.append(f"**Repository:** {d.get('repository', '')}\n")
lib/python/autonomous_execution_engine/validator.py:5: Runs repository, semantic, canonical and regression validation
lib/python/autonomous_execution_engine/validator.py:29:     def __init__(self, repository: str = ".") -> None:
lib/python/autonomous_execution_engine/validator.py:30:         self.repository = repository
lib/python/autonomous_execution_engine/validator.py:33:         """Repository structure validation via CORE-008A."""
lib/python/autonomous_execution_engine/validator.py:37:             scanner = AICTOScannerEngine(self.repository)
lib/python/autonomous_execution_engine/validator.py:58:                 findings=[f"Repository validation skipped: {exc}"],
lib/python/autonomous_execution_engine/validator.py:68:             engine = SemanticRepositoryEngine(repository=self.repository, persist=False)
lib/python/autonomous_execution_engine/validator.py:94:             engine = CanonicalIntelligenceEngine(repository=self.repository)
lib/python/autonomous_planning_engine/__init__.py:13:     engine = AutonomousPlanningEngine(repository="/path/to/repo")
lib/python/autonomous_planning_engine/batch_planner.py:50:     Recommends the next batch to execute from repository intelligence.
lib/python/autonomous_planning_engine/decision_engine.py:7:   - Current repository maturity   (from CanonicalIntelligence + Semantic)
lib/python/autonomous_planning_engine/decision_engine.py:51:     Detects implemented and documented COREs from the repository.
lib/python/autonomous_planning_engine/decision_engine.py:99:         or batch file in the repository (docs/, development/, README*).
lib/python/autonomous_planning_engine/engine.py:12:   CORE-008B Semantic Repository Intelligence
lib/python/autonomous_planning_engine/engine.py:13:   CORE-008C Executable Repository Intelligence
lib/python/autonomous_planning_engine/engine.py:65: def _planning_id(repository: str, generated_at: str) -> str:
lib/python/autonomous_planning_engine/engine.py:67:         f"{repository}{generated_at}".encode("utf-8")
lib/python/autonomous_planning_engine/engine.py:80:         engine = AutonomousPlanningEngine(repository="/path/to/repo")
lib/python/autonomous_planning_engine/engine.py:92:         repository: str = ".",
lib/python/autonomous_planning_engine/engine.py:100:         self.root = Path(repository).resolve()
lib/python/autonomous_planning_engine/engine.py:135:             repository=str(self.root),
lib/python/autonomous_planning_engine/engine.py:148:             repository=str(self.root),
lib/python/autonomous_planning_engine/engine.py:292:             repository=str(self.root),
lib/python/autonomous_planning_engine/engine.py:331:         # Determine next repository to prioritise (from workspace state if available)
lib/python/autonomous_planning_engine/engine.py:339:                 # WorkspacePriority is a dataclass with a .repository attribute
lib/python/autonomous_planning_engine/engine.py:341:                     top.repository if hasattr(top, "repository")
lib/python/autonomous_planning_engine/engine.py:342:                     else top.get("repository", "")
lib/python/autonomous_planning_engine/engine.py:349:             repository=str(self.root),
lib/python/autonomous_planning_engine/execution_queue.py:9:   - type   (core | issue | batch | pr | milestone | repository)
lib/python/autonomous_planning_engine/execution_queue.py:66:         repository: str,
lib/python/autonomous_planning_engine/execution_queue.py:78:         queue_id, generated_at, repository:
lib/python/autonomous_planning_engine/execution_queue.py:86:                 repository=repository,
lib/python/autonomous_planning_engine/execution_queue.py:123:             repository=repository,
lib/python/autonomous_planning_engine/issue_planner.py:34:     Recommends the next issue to open from repository intelligence.
lib/python/autonomous_planning_engine/milestone_planner.py:45:     Recommends the next milestone from repository intelligence.
lib/python/autonomous_planning_engine/models.py:42: TYPE_REPOSITORY = "repository"
lib/python/autonomous_planning_engine/models.py:108:     repository: str
lib/python/autonomous_planning_engine/models.py:116:             "repository": self.repository,
lib/python/autonomous_planning_engine/models.py:128:     """Current CORE roadmap completion status derived from the repository."""
lib/python/autonomous_planning_engine/models.py:131:     repository: str
lib/python/autonomous_planning_engine/models.py:145:             "repository": self.repository,
lib/python/autonomous_planning_engine/models.py:167:     repository: str
lib/python/autonomous_planning_engine/models.py:178:             "repository": self.repository,
lib/python/autonomous_planning_engine/models.py:198:     repository: str
lib/python/autonomous_planning_engine/models.py:213:             "repository": self.repository,
lib/python/autonomous_planning_engine/pr_planner.py:29:     Recommends the next PR to create from repository intelligence.
lib/python/autonomous_planning_engine/priority_optimizer.py:9:   - Repository health          (derived from Workspace Orchestrator)
lib/python/autonomous_planning_engine/report.py:71:         lines.append(f"**Repository:** {d.get('repository', '')}\n")
lib/python/autonomous_planning_engine/roadmap_planner.py:6: repository intelligence.  No hardcoded CORE ordering.
lib/python/autonomous_workflow_engine.py:29:         "engine": "Repository Inspector",
lib/python/canonical_audit/engine.py:6:     def __init__(self, repository=".", workspace_index=None):
lib/python/canonical_audit/engine.py:8:         self.root = Path(repository).resolve()
lib/python/canonical_intelligence/engine.py:17:     def __init__(self, repository=".", workspace_index=None, canonical_docs_path=None):
lib/python/canonical_intelligence/engine.py:18:         self.root = Path(repository).resolve()
lib/python/canonical_repository/__init__.py:1: from .repository import CanonicalRepository
lib/python/canonical_repository/repository.py:44:         repository = cls()
lib/python/canonical_repository/repository.py:46:             repository.add(document)
lib/python/canonical_repository/repository.py:47:         return repository
lib/python/cli/engineering.py:20:         ROOT / "implementation-packages" / core / "repository-audit.md"
lib/python/cli/main.py:49: def cmd_plan(repository=".", workspace=None, as_json=False, refresh=False):
lib/python/cli/main.py:60:             repository=repository,
lib/python/cli/main.py:73:             print(f"AI CTO Autonomous Planning — {repository}")
lib/python/cli/main.py:112: def cmd_agent(agent_name, repository=".", output_dir="."):
lib/python/cli/main.py:119:             repository=repository,
lib/python/cli/main.py:163:     "--repository",
lib/python/cli/main.py:167:     help="Path to the repository (default: current directory)",
lib/python/cli/main.py:174:     help="Path to the workspace root (default: parent of repository)",
lib/python/cli/main.py:179:     help="Scan a repository and generate AI_CTO_INTEGRATION_REPORT.md",
lib/python/cli/main.py:185:     help="Path to the repository to inspect (default: current directory)",
lib/python/cli/main.py:203:     help="Run executable repository intelligence (CORE-008C) and print a JSON summary",
lib/python/cli/main.py:221:     "--repository",
lib/python/cli/main.py:225:     help="Path to the repository (default: current directory)",
lib/python/cli/main.py:242:     help="Multi-Repository Workspace Orchestrator (CORE-012)",
lib/python/cli/main.py:257:     "--repository",
lib/python/cli/main.py:261:     help="Register or re-scan a single repository and update workspace state",
lib/python/cli/main.py:303:     "--repository",
lib/python/cli/main.py:307:     help="Path to the repository (default: current directory)",
lib/python/cli/main.py:314:     help="Path to the workspace root (default: parent of repository)",
lib/python/cli/main.py:322:     "--repository",
lib/python/cli/main.py:326:     help="Path to the repository (default: current directory)",
lib/python/cli/main.py:333:     help="Path to the workspace root (default: parent of repository)",
lib/python/cli/main.py:371:     "--repository",
lib/python/cli/main.py:375:     help="Path to the repository (default: current directory)",
lib/python/cli/main.py:382:     help="Path to the workspace root (default: parent of repository)",
lib/python/cli/main.py:414:     "--repository",
lib/python/cli/main.py:418:     help="Path to the repository (default: current directory)",
lib/python/cli/main.py:425:     help="Path to the workspace root (default: parent of repository)",
lib/python/cli/main.py:481:     "--repository",
lib/python/cli/main.py:485:     help="Path to the repository (default: current directory)",
lib/python/cli/main.py:492:     help="Path to the workspace root (default: parent of repository)",
lib/python/cli/main.py:518:         repository=getattr(args, "plan_repository", "."),
lib/python/cli/main.py:530:         engine = ExecutableRepositoryEngine(repository=args.path, persist=persist)
lib/python/cli/main.py:533:             "repository": result["repository"],
lib/python/cli/main.py:552:         engine = SemanticRepositoryEngine(repository=args.path, persist=False)
lib/python/cli/main.py:555:             "repository": result["repository"],
lib/python/cli/main.py:572:         cmd_agent("inspect", repository=args.path, output_dir=args.output)
lib/python/cli/main.py:579:     repository = getattr(args, "briefing_repository", ".")
lib/python/cli/main.py:584:         repository=repository,
lib/python/cli/main.py:585:         output_dir=repository,
lib/python/cli/main.py:599:         print(f"Repository:   {briefing.repository}")
lib/python/cli/main.py:629:             print(f"Repository registered: {repo.name}")
lib/python/cli/main.py:650:                 print(f"  Suggested Next: {top.repository}")
lib/python/cli/main.py:693:     repository = getattr(args, "context_repository", ".")
lib/python/cli/main.py:699:         repository=repository,
lib/python/cli/main.py:712:         print(f"  Repository:     {live.get('repository', '')}")
lib/python/cli/main.py:721:         print(f"  Context JSON:   {paths.get('live_context', str(Path(repository).resolve() / '.ai' / 'context' / 'live_context.json'))}")
lib/python/cli/main.py:722:         print(f"  Report:         {paths.get('markdown', str(Path(repository).resolve() / '.ai' / 'context' / 'AI_CTO_CONTEXT_REPORT.md'))}")
lib/python/cli/main.py:729:     repository = getattr(args, "execute_repository", ".")
lib/python/cli/main.py:747:         repository=repository,
lib/python/cli/main.py:762:         print(f"AI CTO Autonomous Execution — {repository}")
lib/python/cli/main.py:784:     repository = getattr(args, "evaluate_repository", ".")
lib/python/cli/main.py:792:         repository=repository,
lib/python/cli/main.py:804:         print(f"AI CTO Self Evaluation — {repository}")
lib/python/cli/main.py:832:     repository = getattr(args, "improve_repository", ".")
lib/python/cli/main.py:841:         repository=repository,
lib/python/cli/main.py:853:         print(f"AI CTO Self Improvement — {repository}")
lib/python/cli/main.py:880:     repository = getattr(args, "dashboard_repository", ".")
lib/python/cli/main.py:889:         repository_root=repository,
lib/python/compliance_engine/engine.py:9:     def __init__(self, repository=".", workspace_index=None):
lib/python/compliance_engine/engine.py:10:         self.root = Path(repository).resolve()
lib/python/compliance_engine/engine.py:20:         """Evaluate repository compliance against canonical expectations."""
lib/python/context_synchronization_engine/engine.py:22:     "repository",
lib/python/context_synchronization_engine/engine.py:111:             "repository": self.root.name,
lib/python/context_synchronization_engine/engine.py:213:         repository = f"{owner}/{repo}" if owner and repo else ""
lib/python/context_synchronization_engine/engine.py:215:             "available": bool(repository),
lib/python/context_synchronization_engine/engine.py:216:             "repository": repository,
lib/python/context_synchronization_engine/engine.py:448:             github_context.get("repository", ""),
lib/python/context_synchronization_engine/engine.py:449:             git_context.get("repository", ""),
lib/python/context_synchronization_engine/engine.py:450:             previous.get("repository", ""),
lib/python/context_synchronization_engine/engine.py:455:             "repository": repository_name,
lib/python/context_synchronization_engine/engine.py:678:             repository=str(live_context.get("repository", "")),
lib/python/context_synchronization_engine/engine.py:805:             "repository": str(live_context.get("repository", "")),
lib/python/context_synchronization_engine/engine.py:832:             repository=final.repository or initial.repository,
lib/python/context_synchronization_engine/engine.py:856:             repository=str(live_context.get("repository", "") or state.repository_state.repository),
lib/python/context_synchronization_engine/engine.py:929:             owner="Repository Engine",
lib/python/context_synchronization_engine/engine.py:952:                 "repository": live_context.get("repository", ""),
lib/python/context_synchronization_engine/engine.py:1000:             loader="DevelopmentState + governance repository",
lib/python/context_synchronization_engine/engine.py:1108:                     "/repository",
lib/python/context_synchronization_engine/engine.py:1135:             loader="Semantic knowledge + repository knowledge directories",
lib/python/context_synchronization_engine/engine.py:1247:                 "repository": "workspace",
lib/python/context_synchronization_engine/engine.py:1266:             repository=str(live_context.get("repository", "")),
lib/python/context_synchronization_engine/engine.py:1319:                     "repository": engineering_context.repository,
lib/python/context_synchronization_engine/engine.py:1476:             repository=str(self.root),
lib/python/context_synchronization_engine/engine.py:1495:             workspace_result = {"repository": repo.to_dict(), "dashboard": dashboard.get("dashboard_dict", {})}
lib/python/context_synchronization_engine/engine.py:1508:             "repository": live_context.get("repository", ""),
lib/python/context_synchronization_engine/engine.py:1572:     def __init__(self, repository: str = ".", workspace_root: Optional[str] = None, persist: bool = True):
lib/python/context_synchronization_engine/engine.py:1573:         self.repository = str(Path(repository).resolve())
lib/python/context_synchronization_engine/engine.py:1574:         self.workspace_root = str(Path(workspace_root).resolve()) if workspace_root else str(Path(repository).resolve().parent)
lib/python/context_synchronization_engine/engine.py:1576:         self.coordinator = SynchronizationCoordinator(self.repository, self.workspace_root)
lib/python/context_synchronization_engine/models.py:54:     repository: str
lib/python/context_synchronization_engine/models.py:67:             "repository": self.repository,
lib/python/context_synchronization_engine/models.py:87:             repository=str(data.get("repository", "")),
lib/python/context_synchronization_engine/models.py:147:     repository: str
lib/python/context_synchronization_engine/models.py:167:             "repository": self.repository,
lib/python/context_synchronization_engine/models.py:188:             repository=str(data.get("repository", "")),
lib/python/coverage_engine/engine.py:9:     def __init__(self, repository=".", workspace_index=None):
lib/python/coverage_engine/engine.py:10:         self.root = Path(repository).resolve()
lib/python/coverage_engine/engine.py:20:         """Compute coverage metrics across repository dimensions."""
lib/python/coverage_engine/engine.py:76:             "workspace", "repository", "analysis", "intelligence", "planning",
lib/python/dashboard/server.py:59:         if path == "/repository":
lib/python/dashboard/service.py:52:         description="Aggregates repository, workspace, reports, and engineering-session context into a single local application.",
lib/python/dashboard/service.py:53:         architecture="A stdlib HTTP server renders HTML pages from existing repository artifacts and engines without adding a frontend framework.",
lib/python/dashboard/service.py:54:         inputs=["repository state", "workspace state", "reports", "capability metadata"],
lib/python/dashboard/service.py:56:         dependencies=["repository-engine", "engineering-session", "project-manager"],
lib/python/dashboard/service.py:62:         known_limitations="The MVP is server-rendered and depends on locally available repository artifacts.",
lib/python/dashboard/service.py:69:         why_architecture="Server-rendered HTML keeps the MVP lightweight and aligned with the repository's existing minimal-dependency approach.",
lib/python/dashboard/service.py:78:         description="Tracks repository health, implementation progress, active branch, and workspace-level priorities.",
lib/python/dashboard/service.py:79:         architecture="Builds on WorkspaceOrchestrator persistence and dashboard summaries, then renders repository cards and tables.",
lib/python/dashboard/service.py:80:         inputs=["workspace scan results", "repository registrations", "repository reports"],
lib/python/dashboard/service.py:81:         outputs=["multi-repository summaries", "repository health table", "implementation progress overview"],
lib/python/dashboard/service.py:82:         dependencies=["repository-engine"],
lib/python/dashboard/service.py:87:         future_roadmap="Add remote repository registration and cross-repository execution workflows.",
lib/python/dashboard/service.py:92:             "Map repository readiness to implementation progress instead of introducing a second progress model.",
lib/python/dashboard/service.py:94:         why_problem="Engineering work spans multiple repositories and needs cross-repository visibility.",
lib/python/dashboard/service.py:96:         why_dependencies="Repository-level health and statistics are prerequisites for any useful project-management surface.",
lib/python/dashboard/service.py:104:         description="Shows current project, repository, branch, sprint, epic, task, runtime, AI provider, and session history.",
lib/python/dashboard/service.py:108:         dependencies=["runtime", "repository-engine"],
lib/python/dashboard/service.py:131:         inputs=["capability registry", "repository file system", "tests", "reports"],
lib/python/dashboard/service.py:133:         dependencies=["dashboard", "repository-engine"],
lib/python/dashboard/service.py:146:         why_dependencies="Explorer pages depend on the dashboard shell and repository evidence to stay truthful.",
lib/python/dashboard/service.py:151:         slug="repository-engine",
lib/python/dashboard/service.py:152:         title="Repository Engine",
lib/python/dashboard/service.py:154:         description="Surfaces repository profile, languages, stack, dependencies, health checks, and statistics.",
lib/python/dashboard/service.py:156:         inputs=["repository filesystem", "semantic analysis", "dependency manifests"],
lib/python/dashboard/service.py:157:         outputs=["repository profile", "inspection reports", "statistics"],
lib/python/dashboard/service.py:162:         dashboard_pages=["/", "/reports", "/capabilities/repository-engine"],
lib/python/dashboard/service.py:163:         future_roadmap="Add deeper trend analysis and richer diff-aware repository insights.",
lib/python/dashboard/service.py:164:         known_limitations="Insights are local to the current repository snapshot.",
lib/python/dashboard/service.py:165:         next_milestone="Expose more repository-engine detail through dashboard JSON endpoints.",
lib/python/dashboard/service.py:167:             "The dashboard reads repository-engine output directly to avoid introducing a second inspection model.",
lib/python/dashboard/service.py:169:         why_problem="All higher-order engineering tooling depends on understanding the repository accurately.",
lib/python/dashboard/service.py:203:         purpose="Surface repository validation and future validation reporting.",
lib/python/dashboard/service.py:208:         dependencies=["repository-engine"],
lib/python/dashboard/service.py:221:         why_dependencies="Validation is downstream of repository understanding and runtime state.",
lib/python/dashboard/service.py:267:         why_dependencies="CDM Engine is the foundation for Knowledge Materialization and Repository Intelligence.",
lib/python/dashboard/service.py:309:         next_milestone="Repository Intelligence consuming the Knowledge Graph instead of file scanning.",
lib/python/dashboard/service.py:356:         repository = self._load_repository_profile()
lib/python/dashboard/service.py:373:             "home": self._home_payload(repository, workspace, session, reports, runtime, diagnostics),
lib/python/dashboard/service.py:400:                 self._section("Repository Health", self._health_checks(home["repository_health"])),
lib/python/dashboard/service.py:401:                 self._section("Repository Statistics", self._metrics_table(home["repository_statistics"])),
lib/python/dashboard/service.py:402:                 self._section("Latest Repository Inspection", self._inspection_panel(home["latest_repository_inspection"])),
lib/python/dashboard/service.py:429:         response_section = "<p>Use <code>?q=Your%20question</code> on this page URL to ask repository-aware questions.</p>"
lib/python/dashboard/service.py:441:             "Repository",
lib/python/dashboard/service.py:452:                 self._section("Repository-aware Engineering Chat", response_section),
lib/python/dashboard/service.py:593:                     ("Repository Usage", ", ".join(capability["repository_usage"]) or "None"),
lib/python/dashboard/service.py:693:                 {"label": "Repository Health", "value": str(summary.get("overall_health", "unknown")).upper()},
lib/python/dashboard/service.py:725:                         "repository": session_payload.get("repository", "."),
lib/python/dashboard/service.py:743:             "current_repository": repository_state.get("repository", self.repository_root.name),
lib/python/dashboard/service.py:757:                 {"label": "Current Repository", "value": repository_state.get("repository", self.repository_root.name)},
lib/python/dashboard/service.py:771:             ("Repository Inspection", self._latest_json_path(self.repository_root / ".ai" / "reports", "inspect-*.json")),
lib/python/dashboard/service.py:823:                 "loaded_engines": ["repository", "workspace"],
lib/python/dashboard/service.py:831:                     "repository": session.get("current_repository", self.repository_root.name),
lib/python/dashboard/service.py:879:             ("Current Repository", runtime_payload.get("current_repository", str(self.repository_root))),
lib/python/dashboard/service.py:1027:                     repository=str(self.repository_root),
lib/python/dashboard/service.py:1036:         repository: Mapping[str, Any],
lib/python/dashboard/service.py:1043:         latest_inspection = repository["latest_inspection"]
lib/python/dashboard/service.py:1049:                 {"label": "Current Repository", "value": session["current_repository"]},
lib/python/dashboard/service.py:1052:                 {"label": "Repository Health", "value": str(repository["health_summary"].get("status", "unknown"))},
lib/python/dashboard/service.py:1061:                 {"label": "Repository Statistics", "value": f"files={repository['metrics'].get('total_files', 0)}, entries={repository['metrics'].get('entry_point_count', 0)}"},
lib/python/dashboard/service.py:1062:                 {"label": "Latest Repository Inspection", "value": ", ".join(repository["tech_stack"][:3]) or "n/a"},
lib/python/dashboard/service.py:1066:                 ("Current Repository", session["current_repository"]),
lib/python/dashboard/service.py:1087:                 ("Repository Health", str(repository["health_summary"].get("status", "unknown"))),
lib/python/dashboard/service.py:1099:             "repository_health": repository["health_summary"],
lib/python/dashboard/service.py:1100:             "repository_statistics": repository["metrics"],
lib/python/dashboard/service.py:1102:                 "languages": repository["languages"],
lib/python/dashboard/service.py:1103:                 "tech_stack": repository["tech_stack"],
lib/python/dashboard/service.py:1104:                 "dependency_manifests": repository["dependency_manifests"],
lib/python/dashboard/service.py:1113:             {"href": "/repository", "label": "Repository"},
lib/python/dashboard/service.py:1189:         if title == "Repository Inspection":
lib/python/dashboard/service.py:1361:         return "<table><thead><tr><th>Repository</th><th>Health</th><th>Current Branch</th><th>Last Inspection</th><th>Active Sprint</th><th>Active Issue</th><th>Repository Statistics</th><th>Implementation Progress</th></tr></thead><tbody>" + "".join(rows) + "</tbody></table>"
lib/python/dashboard/service.py:1370:                 f"<td>{escape(str(item.get('repository', '')))}</td>"
lib/python/dashboard/service.py:1376:         return "<table><thead><tr><th>Session</th><th>Status</th><th>Repository</th><th>Completed Steps</th></tr></thead><tbody>" + "".join(rows) + "</tbody></table>"
lib/python/dashboard/service.py:1441:                 f"<td>{escape(str(item.get('repository', '')))}</td>"
lib/python/dashboard/service.py:1450:         return "<table><thead><tr><th>Session</th><th>Project</th><th>Repository</th><th>Branch</th><th>Provider</th><th>Model</th><th>Messages</th></tr></thead><tbody>" + "".join(rows) + "</tbody></table>"
lib/python/development_state_engine/__init__.py:4: Canonical state models and persistence repository for CANON-030.
lib/python/development_state_engine/__init__.py:20: from .repository import DevelopmentStateRepository
lib/python/development_state_engine/models.py:103:     repository: str
lib/python/development_state_engine/models.py:120:         _require_non_empty_string("repository", self.repository)
lib/python/development_state_engine/models.py:131:             "repository": self.repository,
lib/python/development_state_engine/models.py:146:             repository=data["repository"],
lib/python/development_state_engine/repository.py:18:     """Persistence repository for DevelopmentState."""
lib/python/development_state_engine/runtime.py:34: from .repository import DevelopmentStateRepository
lib/python/development_state_engine/runtime.py:216:         repository: Optional[DevelopmentStateRepository] = None,
lib/python/development_state_engine/runtime.py:225:         self.repository = repository or DevelopmentStateRepository(self.repository_root)
lib/python/development_state_engine/runtime.py:232:         self.base_dir = self.repository.base_dir
lib/python/development_state_engine/runtime.py:236:         return self.repository.LoadState()
lib/python/development_state_engine/runtime.py:259:         self.repository.SaveState(materialized)
lib/python/development_state_engine/runtime.py:260:         self.repository.VerifyIntegrity()
lib/python/development_state_engine/runtime.py:262:             self.repository.CreateSnapshot()
lib/python/development_state_engine/runtime.py:328:             "current_repository": state.repository_state.repository,
lib/python/development_state_engine/runtime.py:472:             engine = self.canonical_engine_class(repository=str(self.repository_root))
lib/python/development_state_engine/runtime.py:499:             result = self.semantic_engine_class(repository=str(self.repository_root), persist=True).analyze()
lib/python/development_state_engine/runtime.py:515:             result = self.ai_cto_scanner_class(repository=str(self.repository_root), output_dir=str(self.repository_root)).scan()
lib/python/development_state_engine/runtime.py:531:                 provider = self.executable_intelligence_provider(repository=str(self.repository_root))
lib/python/development_state_engine/runtime.py:576:         if not self.repository.integrity_path.exists():
lib/python/development_state_engine/runtime.py:582:         payload = json.loads(self.repository.integrity_path.read_text(encoding="utf-8"))
lib/python/development_state_engine/runtime.py:701:             "current_repository": ("repository", "repository"),
lib/python/development_state_engine/runtime.py:702:             "current_branch": ("repository", "branch"),
lib/python/development_state_engine/runtime.py:725:                     "repository": repository_updates,
lib/python/development_state_engine/runtime.py:1056:                 repository=repository_name,
lib/python/discovery_engine/__init__.py:4: Repository structure discovery.
lib/python/drift_engine/engine.py:10:     def __init__(self, repository=".", workspace_index=None):
lib/python/drift_engine/engine.py:11:         self.root = Path(repository).resolve()
lib/python/drift_engine/engine.py:21:         """Detect drift between canonical repository and implementation evidence."""
lib/python/drift_engine/engine.py:41:                     "Implement the canonical module and connect it to repository architecture.",
lib/python/engineering_engine/__init__.py:7: - Repository Audit
lib/python/engineering_engine/acceptance_detector.py:9:             "Repository builds successfully",
lib/python/engineering_engine/acceptance_detector.py:12:             "Planning synchronized with repository",
lib/python/engineering_engine/build_engine.py:28:         print("[1/5] Repository Audit")
lib/python/engineering_engine/build_engine.py:30:             package / "repository-audit.md"
lib/python/engineering_engine/deliverable_detector.py:16:             ("Repository Audit", "repository-audit.md"),
lib/python/engineering_engine/dependency_reasoning_engine.py:13:     def __init__(self, repository: SemanticRepository):
lib/python/engineering_engine/dependency_reasoning_engine.py:14:         self.repository = repository
lib/python/engineering_engine/dependency_reasoning_engine.py:19:         for rel in repository.relationships:
lib/python/engineering_engine/engineering_task_engine.py:43:         repository = SemanticRepositoryBuilder(self.root).build()
lib/python/engineering_engine/engineering_task_engine.py:49:         for entity in sorted(repository.entities, key=lambda e: e.name):
lib/python/engineering_engine/engineering_workflow_engine.py:47:         repository = SemanticRepositoryBuilder(
lib/python/engineering_engine/engineering_workflow_engine.py:52:             repository
lib/python/engineering_engine/execution_package_generator.py:58:             md.write("- Repository builds successfully.\n")
lib/python/engineering_engine/gap_analysis.py:25:             GapItem('Canonical Repository', 'PARTIAL', 'Foundational canonical modules exist but provide only basic document ingestion'),
lib/python/engineering_engine/gap_analysis.py:34:             GapItem('Repository Structure RFC-0009 Alignment', 'MISSING', 'Repository lacks first-class knowledge/, generated/, and canonical runtime/ structure separation'),
lib/python/engineering_engine/gap_analysis.py:56:             md.write('## Repository-wide Findings\n\n')
lib/python/engineering_engine/gap_analysis.py:57:             md.write('- Strongest areas: runtime platform, repository scanning/intelligence, audit/planning/report generation, test volume.\n')
lib/python/engineering_engine/gap_analysis.py:59:             md.write('- Primary risks: architectural drift, duplicated subsystems, heuristic compliance being mistaken for normative conformance, missing UEM, incomplete governance, non-canonical repository structure.\n')
lib/python/engineering_engine/github_cli_client.py:13:         repository = GitHubRepositoryResolver().resolve()
lib/python/engineering_engine/github_cli_client.py:14:         self.owner = repository.owner
lib/python/engineering_engine/github_cli_client.py:15:         self.repo = repository.repo
lib/python/engineering_engine/github_cli_state_provider.py:19:         repository = GitHubRepositoryResolver().resolve()
lib/python/engineering_engine/github_cli_state_provider.py:25:                 f"repos/{repository.owner}/{repository.repo}/milestones",
lib/python/engineering_engine/github_issue_state_provider.py:25:         repository = GitHubRepositoryResolver().resolve()
lib/python/engineering_engine/github_issue_state_provider.py:33:                 f"{repository.owner}/{repository.repo}",
lib/python/engineering_engine/package_builder.py:45:                 "Repository verification",
lib/python/engineering_engine/package_builder.py:64:             "Repository Audit",
lib/python/engineering_engine/package_builder.py:77:             "Repository builds successfully",
lib/python/engineering_engine/package_builder.py:79:             "Planning is synchronized with repository",
lib/python/engineering_engine/pipeline.py:26:             package / "repository-audit.md"
lib/python/engineering_engine/planning_engine.py:30:             ('Define authoritative CSL subsystem architecture', 'CRITICAL', 'HIGH', 'Define the official subsystem map: source loader, parser, semantic analyzer, UEM, validator, compiler, generators, governance kernel, repository adapters, runtime integrations.', ['lib/python/canonical_parser', 'lib/python/canonical_repository', 'lib/python/engineering_engine']),
lib/python/engineering_engine/planning_engine.py:39:             ('Align repository structure with RFC-0009', 'HIGH', 'MEDIUM', 'Introduce canonical separation for knowledge, generated outputs, runtime assets, and implementation responsibilities.', ['.', '.ai', 'docs', 'implementation-packages']),
lib/python/engineering_engine/planning_engine.py:83:             md.write('- Phase B: normalize repository structure to CSL.\n')
lib/python/engineering_engine/repository_audit.py:63:             "missing_interfaces": ["generator framework", "repository adapter contracts", "compiler boundary"],
lib/python/engineering_engine/repository_audit.py:120:             "category": "repository-adapter-analysis",
lib/python/engineering_engine/repository_audit.py:121:             "purpose": "repository analysis, intelligence, adapter-like scanning and recommendations",
lib/python/engineering_engine/repository_audit.py:123:             "csl_compliance": "useful repository-adapter layer, not canonical core",
lib/python/engineering_engine/repository_audit.py:127:             "missing_interfaces": ["explicit repository adapter abstraction"],
lib/python/engineering_engine/repository_audit.py:131:             "risks": ["repository-centric semantics instead of CSL-centric semantics"],
lib/python/engineering_engine/repository_audit.py:197:             md.write('# Repository Inventory\n\n')
lib/python/engineering_engine/repository_audit.py:215:             md.write('Expected CSL reference architecture: Canonical Repository → CSL Parser → Semantic Analyzer → Universal Engineering Model → Validation Engine → Engineering Compiler → Artifact Generators → Safety & Governance Kernel → Runtime Integrations.\n\n')
lib/python/engineering_engine/repository_audit.py:239:             md.write('- engineering pipeline → `pipeline.py` → repository audit + gap analysis + planning + package generation + validation + review\n\n')
lib/python/engineering_engine/repository_audit.py:241:             md.write('## Repository Structure Observations\n\n')
lib/python/engineering_engine/repository_audit.py:245:             md.write('- Structural mismatch to RFC-0009: `knowledge/`, `generated/`, and a CSL-scoped `runtime/` top-level layout are not yet first-class repository directories.\n')
lib/python/engineering_engine/semantic_classifier.py:13:         repository: SemanticRepository,
lib/python/engineering_engine/semantic_classifier.py:16:         for entity in repository.entities:
lib/python/engineering_engine/semantic_classifier.py:34:         return repository
lib/python/engineering_engine/semantic_entities.py:9:     REPOSITORY = "repository"
lib/python/engineering_engine/semantic_query_engine.py:13:     def __init__(self, repository: SemanticRepository):
lib/python/engineering_engine/semantic_query_engine.py:14:         self.repository = repository
lib/python/engineering_engine/semantic_query_engine.py:24:                 for entity in self.repository.entities
lib/python/engineering_engine/semantic_query_engine.py:35:         for entity in self.repository.entities:
lib/python/engineering_engine/semantic_query_engine.py:48:             for rel in self.repository.relationships
lib/python/engineering_engine/semantic_repository_builder.py:33:         repository = SemanticExtractor().extract(graph)
lib/python/engineering_engine/semantic_repository_builder.py:35:         repository.relationships.extend(
lib/python/engineering_engine/semantic_repository_builder.py:39:         return repository
lib/python/engineering_workspace/capabilities.py:16:     # Repository
lib/python/engineering_workspace/capabilities.py:18:     READ_REPOSITORY = "repository.read"
lib/python/engineering_workspace/capabilities.py:19:     WRITE_REPOSITORY = "repository.write"
lib/python/engineering_workspace/capabilities.py:20:     INSPECT_REPOSITORY = "repository.inspect"
lib/python/engineering_workspace/workspace.py:56:     def repository(self) -> Any:
lib/python/evidence_engine/engine.py:7:     def __init__(self, repository="."):
lib/python/evidence_engine/engine.py:9:         self.root = Path(repository).resolve()
lib/python/executable_repository_intelligence/__init__.py:2: Executable Repository Intelligence — CORE-008C
lib/python/executable_repository_intelligence/__init__.py:12:     result = ExecutableRepositoryEngine(repository="/path").analyze()
lib/python/executable_repository_intelligence/engine.py:2: Executable Repository Intelligence Engine — CORE-008C
lib/python/executable_repository_intelligence/engine.py:16: The engine is the authoritative repository execution model for all future
lib/python/executable_repository_intelligence/engine.py:43:     Executable Repository Intelligence Engine.
lib/python/executable_repository_intelligence/engine.py:50:         engine = ExecutableRepositoryEngine(repository="/path/to/repo")
lib/python/executable_repository_intelligence/engine.py:59:         repository: str = ".",
lib/python/executable_repository_intelligence/engine.py:63:         self.root = Path(repository).resolve()
lib/python/executable_repository_intelligence/engine.py:80:             repository=str(self.root),
lib/python/executable_repository_intelligence/engine.py:139:             repository=str(self.root),
lib/python/executable_repository_intelligence/executable_dep_graph.py:2: Executable Repository Intelligence — Executable Dependency Graph Builder
lib/python/executable_repository_intelligence/file_classifier.py:2: Executable Repository Intelligence — File Classifier
lib/python/executable_repository_intelligence/file_classifier.py:5: Classifies every repository file into one of the canonical categories.
lib/python/executable_repository_intelligence/file_classifier.py:304:     Classifies every repository file into a canonical category.
lib/python/executable_repository_intelligence/injection_safety.py:2: Executable Repository Intelligence — Injection Safety Classifier
lib/python/executable_repository_intelligence/models.py:2: Executable Repository Intelligence — Data Models
lib/python/executable_repository_intelligence/models.py:38: # Repository zone categories
lib/python/executable_repository_intelligence/models.py:64:     """Classification of a single repository file."""
lib/python/executable_repository_intelligence/models.py:90:     """A runtime component identified in the repository."""
lib/python/executable_repository_intelligence/models.py:111:     Full runtime map of a repository.
lib/python/executable_repository_intelligence/models.py:226: # Repository Zones
lib/python/executable_repository_intelligence/models.py:285:     repository: str
lib/python/executable_repository_intelligence/models.py:301:             "repository": self.repository,
lib/python/executable_repository_intelligence/persistence.py:2: Executable Repository Intelligence — Persistence
lib/python/executable_repository_intelligence/persistence.py:5: Persists the executable repository model to:
lib/python/executable_repository_intelligence/persistence.py:25:     Saves CORE-008C analysis results to the repository's .ai directory.
lib/python/executable_repository_intelligence/persistence.py:40:         Save the full executable repository result as runtime_repository_model.json.
lib/python/executable_repository_intelligence/persistence.py:46:             "repository": str(self.root),
lib/python/executable_repository_intelligence/persistence.py:63:             "repository": str(self.root),
lib/python/executable_repository_intelligence/recommendations.py:2: Executable Repository Intelligence — Recommendation Engine
lib/python/executable_repository_intelligence/report.py:2: Executable Repository Intelligence — Execution Model Report Generator
lib/python/executable_repository_intelligence/report.py:43:         repo = r.get("repository", ".")
lib/python/executable_repository_intelligence/report.py:47:             "**CORE-008C — Executable Repository Intelligence**",
lib/python/executable_repository_intelligence/report.py:51:             "| Repository | `%s` |" % repo,
lib/python/executable_repository_intelligence/report.py:64:             "This document is the authoritative **Executable Repository Model** "
lib/python/executable_repository_intelligence/report.py:65:             "for this repository.  It distinguishes files that participate in "
lib/python/executable_repository_intelligence/report.py:98:             "## Repository Runtime Map",
lib/python/executable_repository_intelligence/report.py:161:             "All %d repository files classified into canonical categories." % len(fcs),
lib/python/executable_repository_intelligence/report.py:250:             "## Repository Zones",
lib/python/executable_repository_intelligence/runtime_map.py:2: Executable Repository Intelligence — Runtime Map Builder
lib/python/executable_repository_intelligence/zone_classifier.py:2: Executable Repository Intelligence — Zone Classifier
lib/python/executable_repository_intelligence/zone_classifier.py:5: Automatically classifies repository directories into zones:
lib/python/executable_repository_intelligence/zone_classifier.py:76:     Classifies repository directories into zones.
lib/python/executive_briefing_engine/__init__.py:6: Transforms repository state into executive decisions, priorities,
lib/python/executive_briefing_engine/engine.py:10:   CORE-008B Semantic Repository Intelligence
lib/python/executive_briefing_engine/engine.py:11:   CORE-008C Executable Repository Intelligence
lib/python/executive_briefing_engine/engine.py:56:     Transforms repository state into executive decisions, priorities,
lib/python/executive_briefing_engine/engine.py:62:         engine = ExecutiveBriefingEngine(repository="/path/to/repo")
lib/python/executive_briefing_engine/engine.py:73:         repository: str = ".",
lib/python/executive_briefing_engine/engine.py:79:         self.root = Path(repository).resolve()
lib/python/executive_briefing_engine/engine.py:231:         # Phase 10 — Repository path
lib/python/executive_briefing_engine/engine.py:232:         repository = str(
lib/python/executive_briefing_engine/engine.py:242:             repository=repository,
lib/python/executive_briefing_engine/engine.py:295:         # Repository readiness from canonical health
lib/python/executive_briefing_engine/generator.py:74:             f"> **Repository:** `{b.repository}`  \n"
lib/python/executive_briefing_engine/generator.py:86:             f"| **Repository Readiness** | {d.repository_readiness} |",
lib/python/executive_briefing_engine/generator.py:131:             ("Repository Health", b.repository_health),
lib/python/executive_briefing_engine/generator.py:150:             f"_{len(b.recommendations)} recommendation(s) derived from repository intelligence._",
lib/python/executive_briefing_engine/insight_generator.py:91:         """Derive repository health label."""
lib/python/executive_briefing_engine/insight_generator.py:127:         # Fall back to executable repository map
lib/python/executive_briefing_engine/insight_generator.py:161:                 .get("repository", "repository")
lib/python/executive_briefing_engine/insight_generator.py:178:             f"The {repo_name} repository {overall}.",
lib/python/executive_briefing_engine/insight_generator.py:182:             f"Repository health: {repo_health}. "
lib/python/executive_briefing_engine/models.py:257:     repository: str
lib/python/executive_briefing_engine/models.py:297:             "repository": self.repository,
lib/python/executive_briefing_engine/models.py:329:             repository=data.get("repository", ""),
lib/python/executive_briefing_engine/recommendation_engine.py:54:     - Executable repository intelligence
lib/python/executive_briefing_engine/recommendation_engine.py:440:                     "Derived from semantic repository intelligence analysis of the "
lib/python/executive_briefing_engine/recommendation_engine.py:461:                     "CORE module suggestions are derived from current repository "
lib/python/executive_briefing_engine/recommendation_engine.py:488:                 "No critical issues detected.  The repository is in a healthy state "
lib/python/executive_briefing_engine/risk_analyzer.py:181:                     f"{len(missing)} required components are not present in the repository."
lib/python/executive_briefing_engine/risk_analyzer.py:224:     # Repository Integrity Risks
lib/python/executive_briefing_engine/risk_analyzer.py:240:                 title=f"Repository integrity failures ({len(failed_checks)})",
lib/python/executive_briefing_engine/risk_analyzer.py:242:                     f"{len(failed_checks)} integrity checks failed for this repository."
lib/python/foundation_audit.py:13:     "repository": ROOT.name,
lib/python/foundation_audit.py:14:     "audit": "AUD-001 Repository Architecture",
lib/python/knowledge_graph/builder.py:17:         """Build the semantic graph from canonical repository contents."""
lib/python/knowledge_graph_engine.py:13:     "repository": ROOT.name,
lib/python/knowledge_graph_v2/engine.py:8:     def __init__(self, repository=".", workspace_index=None):
lib/python/knowledge_graph_v2/engine.py:10:         self.root = Path(repository).resolve()
lib/python/memory_engine.py:28:         "repository": ROOT.name,
lib/python/memory_engine.py:58:     "repository": ROOT.name,
lib/python/memory_engine.py:77: print("Repository:", ROOT.name)
lib/python/planning_engine/__init__.py:4: Coordinates Repository, Knowledge,
lib/python/planning_engine/engine.py:14:         self.repository = RepositoryEngine(root, workspace_index=workspace_index)
lib/python/planning_engine/engine.py:24:         stats = self.repository.statistics()
lib/python/planning_engine/engine.py:28:                 identifier="TASK-REPOSITORY",
lib/python/planning_optimizer/engine.py:23:     def scan(self, repository):
lib/python/planning_optimizer/engine.py:25:         root = Path(repository).resolve()
lib/python/project_profiles/trading_signals.py:18:     def inspect(self, repository):
lib/python/project_profiles/trading_signals.py:20:         discovery = DiscoveryEngine(repository)
lib/python/recommendation_engine/engine.py:12:                 "title": "Resolve repository findings",
lib/python/recommendation_engine/engine.py:13:                 "reason": "Repository score is below 100.",
lib/python/recommendation_engine/engine.py:37:                 "reason": "Repository semantic model can be enriched.",
lib/python/recommendation_engine/engine.py:44:                 "title": "Repository is healthy",
lib/python/repository_engine/__init__.py:2: Repository Engine
lib/python/repository_engine/__init__.py:3: Repository discovery and inventory.
lib/python/repository_engine/cli.py:25:         "repository": profile.name,
lib/python/repository_engine/engine.py:149:             self._check("Repository has source files", metrics.total_files > 0, f"{metrics.total_files} files")
lib/python/repository_engine/engine.py:152:             self._check("Repository has tests", metrics.test_file_count > 0, f"{metrics.test_file_count} test files")
lib/python/repository_engine/engine.py:156:                 "Repository has documentation",
lib/python/repository_engine/engine.py:163:                 "Repository has entry points",
lib/python/repository_engine/engine.py:170:                 "Repository has dependency metadata",
lib/python/repository_engine/engine.py:181:             "Repository is operationally healthy."
lib/python/repository_engine/engine.py:183:             else "Repository needs targeted improvements."
lib/python/repository_engine/engine.py:185:             else "Repository requires immediate remediation."
lib/python/repository_engine/report.py:21:         lines.append("# Repository Inspect Report")
lib/python/repository_engine/report.py:25:         lines.append(f"- **Repository:** `{profile.name}`")
lib/python/repository_engine/report.py:27:         lines.append(f"- **Repository Health:** **{health['status']}** ({health['score']}/100)")
lib/python/repository_engine/report.py:98:         lines.append("## Repository Health Summary")
lib/python/repository_hygiene_audit.py:31: print("Repository Hygiene Audit")
lib/python/repository_inspector_v2/__init__.py:2: Repository Inspector v2
lib/python/repository_inspector_v2/__init__.py:4: Autonomous repository analysis agent.
lib/python/repository_inspector_v2/analyzer.py:22:         repository = report["repository"]
lib/python/repository_inspector_v2/analyzer.py:24:         if repository["files"] < 20:
lib/python/repository_inspector_v2/analyzer.py:27:                 "message": "Repository is very small."
lib/python/repository_inspector_v2/analyzer.py:30:                 "Continue repository development."
lib/python/repository_inspector_v2/analyzer.py:36:         if dependencies["dependencies"] != repository["files"]:
lib/python/repository_inspector_v2/engine.py:16:         self.repository = RepositoryEngine(root, workspace_index=workspace_index)
lib/python/repository_inspector_v2/engine.py:24:             "repository": self.repository.statistics(),
lib/python/repository_inspector_v2/report.py:13:         lines.append("# Repository Inspection Report")
lib/python/repository_inspector_v2/report.py:15:         lines.append(f"Repository Health: **{report['repository_health']}**")
lib/python/repository_inspector_v2/report.py:18:         lines.append("## Repository")
lib/python/repository_inspector_v2/report.py:20:         for key, value in report["repository"].items():
lib/python/repository_inspector_v2/report.py:47:         lines.append("## Repository Score")
lib/python/repository_inventory.py:13:     "repository": ROOT.name,
lib/python/repository_inventory.py:75: print("Repository Inventory")
lib/python/repository_profile.py:30:     "repository": ROOT.name,
lib/python/rule_engine/rules/repository_size_rule.py:6:     NAME = "Repository Size"
lib/python/rule_engine/rules/repository_size_rule.py:10:         if report["repository"]["files"] >= 20:
lib/python/rule_engine/rules/repository_size_rule.py:16:             message="Repository contains very few files.",
lib/python/rule_engine/rules/repository_size_rule.py:17:             recommendation="Continue repository development.",
lib/python/runtime/bootstrap.py:263:             "repository": "python.repository_engine.engine:RepositoryEngine",
lib/python/runtime/bootstrap.py:384:                 repository=self.repository_root,
lib/python/runtime/diagnostics.py:221:             "repository": repository_state.get("repository", self.repository_root.name),
lib/python/runtime/interfaces/github_webhook.py:10:     discussion, repository, create, delete, ping
lib/python/runtime/interfaces/github_webhook.py:34:     "repository": "github.repository",
lib/python/runtime/interfaces/http_server.py:99:             "/repository",
lib/python/runtime/interfaces/http_server.py:300:         if normalized_path == "/repository":
lib/python/self_evaluation_engine/__init__.py:6: Evaluates every implementation against canonical architecture, repository
lib/python/self_evaluation_engine/__init__.py:13:     engine = SelfEvaluationEngine(repository="/path/to/repo")
lib/python/self_evaluation_engine/analyzers.py:9:   Repository discovery    (CORE-008A)
lib/python/self_evaluation_engine/analyzers.py:37:     def __init__(self, repository: str = ".") -> None:
lib/python/self_evaluation_engine/analyzers.py:38:         self.repository = repository
lib/python/self_evaluation_engine/analyzers.py:48:             engine = CanonicalIntelligenceEngine(repository=self.repository)
lib/python/self_evaluation_engine/analyzers.py:92:     def __init__(self, repository: str = ".") -> None:
lib/python/self_evaluation_engine/analyzers.py:93:         self.repository = repository
lib/python/self_evaluation_engine/analyzers.py:104:             engine = SemanticRepositoryEngine(repository=self.repository, persist=False)
lib/python/self_evaluation_engine/analyzers.py:138: # Repository Compliance Analyzer
lib/python/self_evaluation_engine/analyzers.py:142:     """Evaluate repository health via CORE-008A."""
lib/python/self_evaluation_engine/analyzers.py:144:     def __init__(self, repository: str = ".") -> None:
lib/python/self_evaluation_engine/analyzers.py:145:         self.repository = repository
lib/python/self_evaluation_engine/analyzers.py:155:             scanner = AICTOScannerEngine(self.repository)
lib/python/self_evaluation_engine/analyzers.py:177:                 "Improve repository readiness." if score < 0.8 else "Repository health is good."
lib/python/self_evaluation_engine/analyzers.py:190:     _REQUIRED_CONTEXT_KEYS = {"repository", "current_branch"}
lib/python/self_evaluation_engine/analyzers.py:192:     def __init__(self, repository: str = ".") -> None:
lib/python/self_evaluation_engine/analyzers.py:193:         self.repository = repository
lib/python/self_evaluation_engine/analyzers.py:273:     def __init__(self, repository: str = ".") -> None:
lib/python/self_evaluation_engine/analyzers.py:274:         self.repository = repository
lib/python/self_evaluation_engine/analyzers.py:278:         tests_dir = Path(self.repository) / "tests"
lib/python/self_evaluation_engine/engine.py:8: canonical architecture, repository standards, and engineering quality.
lib/python/self_evaluation_engine/engine.py:13:   CORE-008B Semantic Repository Intelligence
lib/python/self_evaluation_engine/engine.py:14:   CORE-008C Executable Repository Intelligence
lib/python/self_evaluation_engine/engine.py:70: def _evaluation_id(repository: str, generated_at: str) -> str:
lib/python/self_evaluation_engine/engine.py:72:         f"{repository}{generated_at}".encode("utf-8")
lib/python/self_evaluation_engine/engine.py:84:     def __init__(self, repository: str = ".") -> None:
lib/python/self_evaluation_engine/engine.py:85:         self.repository = repository
lib/python/self_evaluation_engine/engine.py:102:             CanonicalComplianceAnalyzer(self.repository).analyze()
lib/python/self_evaluation_engine/engine.py:106:         arch_score, arch_findings = ArchitectureComplianceAnalyzer(self.repository).analyze()
lib/python/self_evaluation_engine/engine.py:110:         # Repository health (CORE-008A)
lib/python/self_evaluation_engine/engine.py:112:             RepositoryComplianceAnalyzer(self.repository).analyze()
lib/python/self_evaluation_engine/engine.py:116:         reg_score, reg_findings = RegressionAnalyzer(self.repository).analyze(
lib/python/self_evaluation_engine/engine.py:123:         quality_scores.append(CoverageAnalyzer(self.repository).analyze())
lib/python/self_evaluation_engine/engine.py:149:         engine = SelfEvaluationEngine(repository="/path/to/repo")
lib/python/self_evaluation_engine/engine.py:161:         repository: str = ".",
lib/python/self_evaluation_engine/engine.py:167:         self.root = Path(repository).resolve()
lib/python/self_evaluation_engine/engine.py:175:         self._coordinator = EvaluationCoordinator(repository=str(self.root))
lib/python/self_evaluation_engine/engine.py:200:             repository=str(self.root),
lib/python/self_evaluation_engine/engine.py:238:             repository=str(self.root),
lib/python/self_evaluation_engine/engine.py:325:             f"Repository: {self.root.name}."
lib/python/self_evaluation_engine/models.py:65:     repository: str
lib/python/self_evaluation_engine/models.py:77:             "repository": self.repository,
lib/python/self_evaluation_engine/models.py:178:     repository: str
lib/python/self_evaluation_engine/models.py:196:             "repository": self.repository,
lib/python/self_evaluation_engine/persistence.py:180:             "repository": d.get("repository", ""),
lib/python/self_evaluation_engine/persistence.py:185:             "repository": d.get("repository", ""),
lib/python/self_evaluation_engine/report.py:60:         lines.append(f"**Repository:** {d.get('repository', '')}\n")
lib/python/self_improvement_engine/__init__.py:6: Continuously analyzes every repository, execution, and evaluation to
lib/python/self_improvement_engine/__init__.py:13:     engine = SelfImprovementEngine(repository="/path/to/repo")
lib/python/self_improvement_engine/analyzers.py:32:     by inspecting the repository structure.
lib/python/self_improvement_engine/analyzers.py:50:     def __init__(self, repository: str = ".") -> None:
lib/python/self_improvement_engine/analyzers.py:51:         self.repository = repository
lib/python/self_improvement_engine/analyzers.py:55:         lib_python = Path(self.repository) / "lib" / "python"
lib/python/self_improvement_engine/analyzers.py:85:                         component=str(py_file.relative_to(Path(self.repository))),
lib/python/self_improvement_engine/analyzers.py:112:                             component=str(pkg_dir.relative_to(Path(self.repository))),
lib/python/self_improvement_engine/analyzers.py:138:     def __init__(self, repository: str = ".") -> None:
lib/python/self_improvement_engine/analyzers.py:139:         self.repository = repository
lib/python/self_improvement_engine/analyzers.py:149:             persistence = ExecutionPersistence(self.repository)
lib/python/self_improvement_engine/analyzers.py:175:             persistence = EvaluationPersistence(self.repository)
lib/python/self_improvement_engine/analyzers.py:193:         # Repository size metric
lib/python/self_improvement_engine/analyzers.py:194:         lib_python = Path(self.repository) / "lib" / "python"
lib/python/self_improvement_engine/analyzers.py:245:     def __init__(self, repository: str = ".") -> None:
lib/python/self_improvement_engine/analyzers.py:246:         self.repository = repository
lib/python/self_improvement_engine/analyzers.py:252:         cli_path = Path(self.repository) / "lib" / "python" / "cli" / "main.py"
lib/python/self_improvement_engine/analyzers.py:272:         lib_python = Path(self.repository) / "lib" / "python"
lib/python/self_improvement_engine/engine.py:7: Responsibility: analyzing every repository, execution, and evaluation
lib/python/self_improvement_engine/engine.py:13:   CORE-008B Semantic Repository Intelligence
lib/python/self_improvement_engine/engine.py:14:   CORE-008C Executable Repository Intelligence
lib/python/self_improvement_engine/engine.py:59: def _plan_id(repository: str, generated_at: str) -> str:
lib/python/self_improvement_engine/engine.py:61:         f"{repository}{generated_at}".encode("utf-8")
lib/python/self_improvement_engine/engine.py:73:     def __init__(self, repository: str = ".") -> None:
lib/python/self_improvement_engine/engine.py:74:         self.repository = repository
lib/python/self_improvement_engine/engine.py:75:         self._debt_analyzer = TechnicalDebtAnalyzer(repository)
lib/python/self_improvement_engine/engine.py:76:         self._perf_analyzer = PerformanceAnalyzer(repository)
lib/python/self_improvement_engine/engine.py:77:         self._cap_analyzer = CapabilityAnalyzer(repository)
lib/python/self_improvement_engine/engine.py:108:     def __init__(self, repository: str = ".") -> None:
lib/python/self_improvement_engine/engine.py:109:         self.repository = repository
lib/python/self_improvement_engine/engine.py:158:     def __init__(self, repository: str = ".") -> None:
lib/python/self_improvement_engine/engine.py:159:         self.repository = repository
lib/python/self_improvement_engine/engine.py:160:         self._optimizer = OptimizationPlanner(repository)
lib/python/self_improvement_engine/engine.py:161:         self._evolver = EvolutionPlanner(repository)
lib/python/self_improvement_engine/engine.py:191:         engine = SelfImprovementEngine(repository="/path/to/repo")
lib/python/self_improvement_engine/engine.py:203:         repository: str = ".",
lib/python/self_improvement_engine/engine.py:209:         self.root = Path(repository).resolve()
lib/python/self_improvement_engine/engine.py:217:         self._coordinator = ImprovementCoordinator(repository=str(self.root))
lib/python/self_improvement_engine/engine.py:240:             repository=str(self.root),
lib/python/self_improvement_engine/models.py:273:     repository: str
lib/python/self_improvement_engine/models.py:288:             "repository": self.repository,
lib/python/self_improvement_engine/persistence.py:149:                 "repository": d.get("repository", ""),
lib/python/self_improvement_engine/persistence.py:180:             "repository": d.get("repository", ""),
lib/python/self_improvement_engine/persistence.py:187:             "repository": d.get("repository", ""),
lib/python/self_improvement_engine/report.py:54:         lines.append(f"**Repository:** {d.get('repository', '')}\n")
lib/python/semantic_engine/engine.py:10:     def __init__(self, repository=".", workspace_index=None):
lib/python/semantic_engine/engine.py:12:         self.root = Path(repository).resolve()
lib/python/semantic_matching/matcher.py:9:     """Semantic comparison between canonical specifications and repository implementations."""
lib/python/semantic_matching/matcher.py:14:         "architecture", "architectural", "implementation", "repository", "canonical", "support",
lib/python/semantic_matching/matcher.py:18:     def __init__(self, repository=".", workspace_index=None):
lib/python/semantic_matching/matcher.py:19:         self.root = Path(repository).resolve()
lib/python/semantic_matching/matcher.py:41:         """Match all canonical documents against repository implementations."""
lib/python/semantic_repository_intelligence/__init__.py:2: Semantic Repository Intelligence — CORE-008B
lib/python/semantic_repository_intelligence/__init__.py:4: Upgrades AI CTO from a pattern-based repository scanner into a semantic
lib/python/semantic_repository_intelligence/__init__.py:10:     result = SemanticRepositoryEngine(repository="/path").analyze()
lib/python/semantic_repository_intelligence/architecture_graph.py:2: Semantic Repository Intelligence — Architecture Graph Builder
lib/python/semantic_repository_intelligence/architecture_graph.py:5: Categorises repository modules into architectural layers, builds a directed
lib/python/semantic_repository_intelligence/ast_analyzer.py:2: Semantic Repository Intelligence — AST Analyzer
lib/python/semantic_repository_intelligence/call_graph.py:2: Semantic Repository Intelligence — Call Graph Builder
lib/python/semantic_repository_intelligence/confidence_engine.py:2: Semantic Repository Intelligence — Confidence Engine
lib/python/semantic_repository_intelligence/dependency_graph.py:2: Semantic Repository Intelligence — Dependency Graph Builder
lib/python/semantic_repository_intelligence/engine.py:2: Semantic Repository Intelligence Engine — CORE-008B
lib/python/semantic_repository_intelligence/engine.py:51:     Semantic Repository Intelligence Engine.
lib/python/semantic_repository_intelligence/engine.py:59:         engine = SemanticRepositoryEngine(repository="/path/to/repo")
lib/python/semantic_repository_intelligence/engine.py:68:         repository: str = ".",
lib/python/semantic_repository_intelligence/engine.py:72:         self.root = Path(repository).resolve()
lib/python/semantic_repository_intelligence/engine.py:137:             "repository": str(self.root),
lib/python/semantic_repository_intelligence/import_graph.py:2: Semantic Repository Intelligence — Import Graph Builder
lib/python/semantic_repository_intelligence/import_graph.py:6: paths within the repository, detects circular dependencies, identifies critical
lib/python/semantic_repository_intelligence/import_graph.py:21:     repository.  Non-Python / external imports are returned as-is with
lib/python/semantic_repository_intelligence/import_graph.py:90:             absolute path to the repository root
lib/python/semantic_repository_intelligence/injection_point_analyzer.py:2: Semantic Repository Intelligence — Injection Point Analyzer
lib/python/semantic_repository_intelligence/injection_point_analyzer.py:88:      re.compile(r"(?:class\s+\w+Service\b|class\s+\w+Client\b|class\s+\w+Repository\b)"),
lib/python/semantic_repository_intelligence/models.py:2: Semantic Repository Intelligence — Data Models
lib/python/semantic_repository_intelligence/models.py:345:     """A detected injection / extension point in the repository."""
lib/python/semantic_repository_intelligence/models.py:373:     """A semantic observation about the repository architecture."""
lib/python/semantic_repository_intelligence/models.py:432: # Repository Complexity
lib/python/semantic_repository_intelligence/models.py:437:     """Aggregate complexity metrics for the repository."""
lib/python/semantic_repository_intelligence/persistence.py:2: Semantic Repository Intelligence — Project Memory Persistence
lib/python/semantic_repository_intelligence/persistence.py:5: Persists and loads semantic analysis results to/from the repository's
lib/python/semantic_repository_intelligence/persistence.py:25:     - The repository identity and analysis timestamp
lib/python/semantic_repository_intelligence/persistence.py:52:             "repository": str(self.root),
lib/python/semantic_repository_intelligence/recommendation_engine.py:2: Semantic Repository Intelligence — Semantic Recommendation Engine
lib/python/semantic_repository_intelligence/recommendation_engine.py:110:                 "%d Python modules are never imported by any other module in the repository. "
lib/python/semantic_repository_intelligence/recommendation_engine.py:191:                     "The repository has only %d identified extension points and %d injection points. "
lib/python/semantic_repository_intelligence/recommendation_engine.py:236:                     "The repository declares %d external dependencies. "
lib/python/semantic_repository_intelligence/recommendation_engine.py:299:                 description="This module has a high in-degree and is central to the repository architecture.",
lib/python/semantic_repository_intelligence/recommendation_engine.py:315:                 description="The repository uses %d %s extension patterns." % (count, ip_type),
lib/python/semantic_repository_intelligence/relationship_resolver.py:2: Semantic Repository Intelligence — Relationship Resolver
lib/python/semantic_repository_intelligence/relationship_resolver.py:6: file paths within the repository.  Exported as a standalone class so that
lib/python/semantic_repository_intelligence/relationship_resolver.py:20:     repository and provides module-to-file lookup utilities for other graph
lib/python/semantic_repository_intelligence/relationship_resolver.py:46:         relative imports) to a relative repository file path.
lib/python/session_runtime/models.py:9:     repository: str
lib/python/session_runtime/runtime.py:12:     def create(self, repository="."):
lib/python/session_runtime/runtime.py:20:             repository=repository
lib/python/validation_engine/__init__.py:3: Repository validation framework.
lib/python/workspace_index/__init__.py:4: Canonical in-memory representation of the repository.
lib/python/workspace_index/builder.py:39:         Traverse the repository exactly once and return an immutable
lib/python/workspace_index/incremental.py:4: Implements change-aware indexing to avoid full repository rebuilds on every execution.
lib/python/workspace_index/incremental.py:7:     Repository
lib/python/workspace_index/incremental.py:52:     """Lightweight per-file state stored in the repository snapshot."""
lib/python/workspace_index/incremental.py:54:     path: str    # relative path from repository root
lib/python/workspace_index/incremental.py:62:     Lightweight image of the repository filesystem state.
lib/python/workspace_index/incremental.py:114:     current state of the repository.
lib/python/workspace_index/incremental.py:208:     current state of the repository.
lib/python/workspace_index/incremental.py:368:         """Remove all cached files for this repository root."""
lib/python/workspace_index/incremental.py:502:         Walk the repository and collect current file states (path, size, mtime).
lib/python/workspace_index/incremental.py:507:         as repository files.
lib/python/workspace_index/incremental.py:529:                 # as repository files.
lib/python/workspace_index/models.py:4: Immutable data model for the canonical repository representation.
lib/python/workspace_index/models.py:12:     """Immutable representation of a single repository file."""
lib/python/workspace_index/models.py:22:     """Immutable representation of a single repository directory."""
lib/python/workspace_index/models.py:42:     Canonical immutable in-memory representation of a repository.
lib/python/workspace_index/models.py:77:     # Repository identity
lib/python/workspace_index/models.py:181:             f"repository={self._repository_name!r}, "
lib/python/workspace_index/policy.py:2: Repository Policy
lib/python/workspace_index/policy.py:4: Single authority for repository inclusion and exclusion rules.
lib/python/workspace_index/policy.py:13:     Centralised authority for repository path filtering.
lib/python/workspace_manager/__init__.py:3: Multi-repository orchestration.
lib/python/workspace_orchestrator/__init__.py:4: Multi-Repository Workspace Orchestrator.
lib/python/workspace_orchestrator/__init__.py:12:   CORE-008B Semantic Repository Intelligence
lib/python/workspace_orchestrator/__init__.py:13:   CORE-008C Executable Repository Intelligence
lib/python/workspace_orchestrator/__init__.py:28:     # Register a specific repository
lib/python/workspace_orchestrator/dashboard.py:71:                     "repository": p.repository,
lib/python/workspace_orchestrator/dashboard.py:82:             "suggested_next_repository": top_priority.repository if top_priority else "",
lib/python/workspace_orchestrator/dashboard.py:109:             f"Workspace contains {n} repository/repositories "
lib/python/workspace_orchestrator/dashboard.py:199:         # Repository Ranking
lib/python/workspace_orchestrator/dashboard.py:202:             _add("## Repository Ranking")
lib/python/workspace_orchestrator/dashboard.py:204:             _add("| Rank | Repository | Reason | Confidence |")
lib/python/workspace_orchestrator/dashboard.py:209:                 _add(f"| {item['rank']} | **{item['repository']}** | {reason} | {conf} |")
lib/python/workspace_orchestrator/dashboard.py:212:         # Repository Readiness
lib/python/workspace_orchestrator/dashboard.py:216:             _add("## Repository Readiness")
lib/python/workspace_orchestrator/dashboard.py:218:             _add("| Repository | Health | Readiness |")
lib/python/workspace_orchestrator/dashboard.py:232:                 _add(f"### #{p['rank']} — {p['repository']}")
lib/python/workspace_orchestrator/dashboard.py:284:                     _add(f"- Target Repository: {rec['target_repository']}")
lib/python/workspace_orchestrator/dashboard.py:322:         _add(f"| Suggested Next Repository | **{next_repo or '—'}** |")
lib/python/workspace_orchestrator/dependency_graph.py:5: WorkspaceDependencyGraph: builds and queries the cross-repository dependency
lib/python/workspace_orchestrator/dependency_graph.py:24:     Builds a complete cross-repository dependency graph.
lib/python/workspace_orchestrator/dependency_graph.py:62:         """Return a list of cycles (each cycle is a list of repository names)."""
lib/python/workspace_orchestrator/dependency_graph.py:116:         (CORE-NNN patterns) in scan_scores or repository names.
lib/python/workspace_orchestrator/dependency_graph.py:178:         """Extract CORE-NNN identifiers from repository name or scan data."""
lib/python/workspace_orchestrator/engine.py:12:   CORE-008B Semantic Repository Intelligence
lib/python/workspace_orchestrator/engine.py:13:   CORE-008C Executable Repository Intelligence
lib/python/workspace_orchestrator/engine.py:65:     Multi-Repository Workspace Orchestrator — CORE-012.
lib/python/workspace_orchestrator/engine.py:75:         # Register a single specific repository
lib/python/workspace_orchestrator/engine.py:84:     3. Builds the cross-repository dependency graph
lib/python/workspace_orchestrator/engine.py:85:     4. Analyzes cross-repository relationships
lib/python/workspace_orchestrator/engine.py:134:         # 2. Scan each repository
lib/python/workspace_orchestrator/engine.py:355:     # Public API — register single repository
lib/python/workspace_orchestrator/engine.py:360:         Register or update a single repository.
lib/python/workspace_orchestrator/engine.py:362:         Scans the repository immediately using AICTOScannerEngine and
lib/python/workspace_orchestrator/engine.py:434:         repository in *workspace*.
lib/python/workspace_orchestrator/engine.py:452:                     AgentContext(repository=repo["path"]),
lib/python/workspace_orchestrator/engine.py:456:                     "repository": repo["name"],
lib/python/workspace_orchestrator/engine.py:467:                     "repository": repo["name"],
lib/python/workspace_orchestrator/intelligence.py:6: WorkspacePriorityEngine:        determines next recommended repository / work item
lib/python/workspace_orchestrator/intelligence.py:40:     executive, owner) from the individual repository models.
lib/python/workspace_orchestrator/intelligence.py:194:     The Owner-first workflow:  one repository at a time, fully evidence-based.
lib/python/workspace_orchestrator/intelligence.py:246:                 repository=repo.name,
lib/python/workspace_orchestrator/intelligence.py:268:             parts.append("repository is in critical health")
lib/python/workspace_orchestrator/intelligence.py:270:             parts.append("repository health is degraded")
lib/python/workspace_orchestrator/intelligence.py:285:             return "Restoring this repository will unblock dependent work and reduce overall risk."
lib/python/workspace_orchestrator/intelligence.py:305:     Detects workspace-level risks from repository models and dependency edges.
lib/python/workspace_orchestrator/intelligence.py:342:             title="Critical repository health detected",
lib/python/workspace_orchestrator/intelligence.py:344:                 f"{len(critical)} repository/repositories are in critical health: "
lib/python/workspace_orchestrator/intelligence.py:349:                         "Review canonical compliance and runtime status for each affected repository.",
lib/python/workspace_orchestrator/intelligence.py:371:                 remediation="Implement canonical CORE specifications for each affected repository.",
lib/python/workspace_orchestrator/intelligence.py:399:             title="Blocked repository development",
lib/python/workspace_orchestrator/intelligence.py:439:             remediation="Run 'ai inspect --execution-model' on each repository and implement missing components.",
lib/python/workspace_orchestrator/intelligence.py:464:             remediation="Review repository purpose and declare dependencies if connections exist.",
lib/python/workspace_orchestrator/intelligence.py:473:     All recommendations are derived from existing repository models.
lib/python/workspace_orchestrator/intelligence.py:524:             title=f"Work on repository: {top.repository}",
lib/python/workspace_orchestrator/intelligence.py:526:                 f"Start with {top.repository} — {top.reason} "
lib/python/workspace_orchestrator/intelligence.py:534:             target_repository=top.repository,
lib/python/workspace_orchestrator/models.py:5: Data models for the Multi-Repository Workspace Orchestrator.
lib/python/workspace_orchestrator/models.py:16: # Repository type / category constants
lib/python/workspace_orchestrator/models.py:68:     Canonical model for a single repository managed by the Workspace Orchestrator.
lib/python/workspace_orchestrator/models.py:113:     # Cross-repository relationships
lib/python/workspace_orchestrator/models.py:217:     source: str          # repository name that depends on target
lib/python/workspace_orchestrator/models.py:218:     target: str          # repository name that is depended upon
lib/python/workspace_orchestrator/models.py:405:     """Detected risk at the workspace or repository level."""
lib/python/workspace_orchestrator/models.py:449:     """Priority ranking for the next recommended repository / work item."""
lib/python/workspace_orchestrator/models.py:452:     repository: str
lib/python/workspace_orchestrator/models.py:467:             "repository": self.repository,
lib/python/workspace_orchestrator/models.py:484:             repository=data.get("repository", ""),
lib/python/workspace_orchestrator/persistence.py:9:   relationships.json      cross-repository relationships
lib/python/workspace_orchestrator/persistence.py:10:   dependencies.json       cross-repository dependency edges
lib/python/workspace_orchestrator/registry.py:32:         """Register or replace a repository entry."""
lib/python/workspace_orchestrator/registry.py:37:         """Remove a repository by name.  Returns the removed entry or None."""
lib/python/workspace_orchestrator/registry.py:45:         """Rename a registered repository.  Returns True on success."""
lib/python/workspace_orchestrator/registry.py:54:         """Update the root path for a registered repository."""
lib/python/workspace_orchestrator/registry.py:65:         """Update an existing repository (full replacement by name)."""
lib/python/workspace_orchestrator/scanner.py:6: WorkspaceScanner: scans each repository using existing CORE engines and
lib/python/workspace_orchestrator/scanner.py:68:         Return a list of dicts with 'name' and 'path' for every git repository
lib/python/workspace_orchestrator/scanner.py:106:     Scans each discovered repository using AICTOScannerEngine (CORE-008A)
lib/python/workspace_orchestrator/scanner.py:118:         Scan a single repository and return a WorkspaceRepository.
lib/python/workspace_orchestrator/scanner.py:120:         Falls back to a skeleton repository model if scanning fails.
lib/python/workspace_orchestrator/scanner.py:131:             engine = AICTOScannerEngine(repository=str(root_path), output_dir=str(root_path))
lib/python/workspace_orchestrator/scanner.py:137:         repository = self._map_to_repository(
lib/python/workspace_orchestrator/scanner.py:144:         return self._apply_synchronized_context(repository, root_path)
lib/python/workspace_orchestrator/scanner.py:219:         # Repository health from overall readiness
lib/python/workspace_orchestrator/scanner.py:273:         # Repository type and category from workspace data
lib/python/workspace_orchestrator/scanner.py:306:     def _apply_synchronized_context(self, repository: WorkspaceRepository, root: Path) -> WorkspaceRepository:
lib/python/workspace_orchestrator/scanner.py:310:             return repository
lib/python/workspace_orchestrator/scanner.py:312:         data = repository.to_dict()
lib/python/workspace_orchestrator/state_manager.py:77:         """Manually register or update a repository."""
lib/python/workspace_orchestrator/state_manager.py:82:         """Remove a repository by name.  Returns the removed entry or None."""
lib/python/workspace_orchestrator/state_manager.py:87:         """Rename a repository.  Returns True on success."""
lib/python/workspace_orchestrator/state_manager.py:92:         """Update the root path for a registered repository."""
lib/python/workspace_orchestrator/state_manager.py:97:         """Update an existing repository entry."""
lib/repository_inspector.sh:10: echo "Repository Inspector v2"
lib/repository_inspector.sh:14: echo "Repository:"
lib/repository_inspector.sh:26: echo "Repository statistics"
lib/repository_profile_engine.sh:9: echo "Repository Intelligence"
lib/repository_profile_engine.sh:45: echo "Repository Features"
lib/repository_summary.sh:6: echo "Repository Summary"
lib/repository_summary.sh:10: echo "Repository:"
lib/review_engine.sh:26: Repository:
lib/work_engine.sh:16: echo "[1/4] Repository Inspector..."
lib/work_engine.sh:20: echo "[2/4] Repository Summary..."
lib/work_engine.sh:34: Repository:
tests/test_agent_runtime.sh:26:     AgentContext(repository=".")
tests/test_ai_cto_scanner.sh:48:     engine = AICTOScannerEngine(repository='.', output_dir=tmp)
tests/test_ai_cto_scanner.sh:54:     assert 'repository' in result
tests/test_ai_cto_scanner.sh:77:     engine = AICTOScannerEngine(repository='.', output_dir=tmp)
tests/test_ai_cto_scanner.sh:111:     engine = AICTOScannerEngine(repository='.', output_dir=tmp)
tests/test_ai_platform.sh:78:         self.assertIn('Repository-aware Engineering Chat', repository_page)
tests/test_autonomous_execution_engine.sh:245:     repository="/tmp/repo",
tests/test_autonomous_execution_engine.sh:283:     repository="/tmp/repo",
tests/test_autonomous_execution_engine.sh:365:     repository=".",
tests/test_autonomous_execution_engine.sh:408:     repository=".",
tests/test_autonomous_planner.sh:16:     AgentContext(repository=".")
tests/test_autonomous_planning_engine.sh:370:         repository=tmpdir,
tests/test_autonomous_planning_engine.sh:395:         repository=tmpdir,
tests/test_autonomous_planning_engine.sh:400:         repository=tmpdir,
tests/test_autonomous_planning_engine.sh:404:         repository=tmpdir,
tests/test_autonomous_planning_engine.sh:418:         repository=tmpdir,
tests/test_autonomous_planning_engine.sh:467:     repository=".",
tests/test_batch_generator.sh:16:     AgentContext(repository=".")
tests/test_canonical_repository.sh:21: print(f"Repository: {stats['total_documents']} documents")
tests/test_canonical_repository.sh:22: print("Canonical Repository PASS")
tests/test_context_synchronization_engine.sh:100:         "repository": str(repo),
tests/test_context_synchronization_engine.sh:162:         result = ContextSynchronizationEngine(repository=self.repo, workspace_root=self.workspace).synchronize(refresh=False)
tests/test_context_synchronization_engine.sh:201:         self.assertEqual(engineering_context["repository_context"]["owner"], "Repository Engine")
tests/test_context_synchronization_engine.sh:215:         engine = ContextSynchronizationEngine(repository=self.repo, workspace_root=self.workspace)
tests/test_context_synchronization_engine.sh:244:                 "--repository",
tests/test_context_synchronization_engine.sh:277:             result = ContextSynchronizationEngine(repository=repo, workspace_root=self.workspace).synchronize(refresh=False)
tests/test_context_synchronization_engine.sh:283:         result = ContextSynchronizationEngine(repository=REPO_ROOT, workspace_root=REPO_ROOT.parent).synchronize(refresh=False)
tests/test_dashboard.sh:15:     "Current Repository",
tests/test_dashboard.sh:23:     "Repository Health",
tests/test_dashboard.sh:24:     "Repository Statistics",
tests/test_dashboard.sh:25:     "Latest Repository Inspection",
tests/test_dashboard_cli.sh:6: PORT=8102 python3 bin/ai dashboard serve --repository . --workspace .. >/tmp/ai-dashboard-cli.log 2>&1 &
tests/test_dashboard_navigation.sh:24:         "/repository": "Repository",
tests/test_development_agent.sh:19:     AgentContext(repository=".")
tests/test_development_agent.sh:28: print("Repository files:",
tests/test_development_agent.sh:29:       result.data["repository"]["files"])
tests/test_development_report.sh:16:     AgentContext(repository=".")
tests/test_development_state_engine_models.sh:44:             repository="caliofmarian-ai/AI-Toolkit",
tests/test_development_state_persistence.sh:26: from python.development_state_engine.repository import DevelopmentStateRepository
tests/test_development_state_persistence.sh:56:                 repository="caliofmarian-ai/AI-Toolkit",
tests/test_development_state_runtime.sh:41:     def __init__(self, repository=".", **_kwargs):
tests/test_development_state_runtime.sh:42:         self.repository = repository
tests/test_development_state_runtime.sh:52:     def __init__(self, repository=".", persist=True, **_kwargs):
tests/test_development_state_runtime.sh:53:         self.repository = repository
tests/test_development_state_runtime.sh:67:     def __init__(self, repository=".", output_dir=None):
tests/test_development_state_runtime.sh:68:         self.repository = repository
tests/test_development_state_runtime.sh:73:             "repository_name": Path(self.repository).name,
tests/test_engineering_explorer.sh:14: for slug in ["dashboard", "project-manager", "engineering-session", "engineering-explorer", "repository-engine"]:
tests/test_executable_repository_intelligence.sh:7: echo "Executable Repository Intelligence Test"
tests/test_executable_repository_intelligence.sh:297:         'repository': str(root),
tests/test_executable_repository_intelligence.sh:366:         'repository': str(root),
tests/test_executable_repository_intelligence.sh:429:     assert 'Repository Zones' in content
tests/test_executable_repository_intelligence.sh:443: engine = ExecutableRepositoryEngine(repository='.', persist=False)
tests/test_executable_repository_intelligence.sh:447: assert 'repository' in result
tests/test_executable_repository_intelligence.sh:498: print('Repository:', result['repository'])
tests/test_executable_repository_intelligence.sh:596:     engine = ExecutableRepositoryEngine(repository='.', persist=False)
tests/test_executable_repository_intelligence.sh:621: echo "Executable Repository Intelligence PASS"
tests/test_execution_coordinator.sh:16:     AgentContext(repository=".")
tests/test_execution_engine.sh:16:     AgentContext(repository=".")
tests/test_executive_briefing_engine.sh:79:                 "repository": "/repo",
tests/test_executive_briefing_engine.sh:345:             repository="/repo",
tests/test_executive_briefing_engine.sh:644:             repository="/repo",
tests/test_executive_briefing_engine.sh:645:             executive_summary="Repository is healthy.",
tests/test_executive_briefing_engine.sh:740:             schema_version=BRIEFING_VERSION, repository="/repo",
tests/test_executive_briefing_engine.sh:815:                 repository=tmpdir,
tests/test_executive_briefing_engine.sh:831:                 repository=tmpdir,
tests/test_executive_briefing_engine.sh:853:                 repository=tmpdir,
tests/test_executive_briefing_engine.sh:873:                 repository=tmpdir,
tests/test_executive_briefing_engine.sh:893:                 repository=tmpdir,
tests/test_executive_briefing_engine.sh:912:                 repository=tmpdir,
tests/test_executive_briefing_engine.sh:932:                 repository=tmpdir,
tests/test_executive_briefing_engine.sh:946: # AI Toolkit integration test (real repository, no refresh)
tests/test_executive_briefing_engine.sh:951:     Validates the engine against the AI Toolkit repository itself.
tests/test_executive_briefing_engine.sh:961:             repository=repo_root,
tests/test_github_materialization.sh:16:     AgentContext(repository=".")
tests/test_incremental_workspace.sh:39:     """Create a minimal fake repository tree under base."""
tests/test_integration_pipeline.sh:26:     AgentContext(repository=".")
tests/test_profiler.sh:16:     AgentContext(repository=".")
tests/test_progress_monitor.sh:25:             f'{item["repository"]}: '
tests/test_progress_monitor.sh:30:             f'{item["repository"]}: FAILED'
tests/test_recommendation_engine.sh:16:     AgentContext(repository=".")
tests/test_repository_analysis.sh:14: print("Repository Score :", report["repository_score"])
tests/test_repository_analysis.sh:18: print("Repository Analysis PASS")
tests/test_repository_engine_inspect.sh:22: grep -q "## Repository Health Summary" "$REPORT_PATH"
tests/test_repository_engine_inspect.sh:65: for key in ("repository", "path", "report_path", "profile_path"):
tests/test_repository_engine_inspect.sh:70: echo "Repository inspect CLI PASS"
tests/test_repository_engine_v2.sh:28: print("Repository Engine PASS")
tests/test_repository_inspector.sh:7: echo "Repository Inspector Test"
tests/test_repository_inspector.sh:11: echo "[1/8] Repository"
tests/test_repository_inspector_v2.sh:18: print("Repository Health :", report["repository_health"])
tests/test_repository_inspector_v2.sh:19: print("Files             :", report["repository"]["files"])
tests/test_repository_inspector_v2.sh:24: print("Repository Inspector v2 PASS")
tests/test_repository_integration_dashboard.sh:12: repository = payload["workspace"]["repositories"][0]
tests/test_repository_integration_dashboard.sh:14: assert inspection["languages"], "expected language distribution from repository engine"
tests/test_repository_integration_dashboard.sh:15: assert inspection["tech_stack"], "expected technology stack from repository engine"
tests/test_repository_integration_dashboard.sh:16: assert repository["name"] == "AI-Toolkit"
tests/test_repository_integration_dashboard.sh:17: assert repository["implementation_progress"].endswith("%")
tests/test_repository_integration_dashboard.sh:18: print("dashboard repository integration PASS")
tests/test_repository_inventory.sh:9: echo "Repository Inventory PASS"
tests/test_repository_profile.sh:6: echo "========== Repository Intelligence Test =========="
tests/test_repository_profile_python.sh:9: echo "Repository profile generated successfully."
tests/test_review_agent.sh:16:     AgentContext(repository=".")
tests/test_rule_engine.sh:15: print("Repository Score:", report["repository_score"])
tests/test_runtime_bootstrap.sh:76: assert status_payload["runtime"]["engineering_context"]["repository_context"]["owner"] == "Repository Engine"
tests/test_runtime_dashboard_navigation.sh:42:         "/repository": "Repository",
tests/test_runtime_layout.sh:43:     echo "Legacy reference found in repository: $needle" >&2
tests/test_runtime_layout.sh:83: # No legacy runtime paths remain in repository code/docs/tests
tests/test_self_evaluation_engine.sh:177:     context_data={"repository": "AI-Toolkit", "current_branch": "main"},
tests/test_self_evaluation_engine.sh:235:     repository="/tmp/repo",
tests/test_self_evaluation_engine.sh:247:     repository="/tmp/repo",
tests/test_self_evaluation_engine.sh:315:     repository=".",
tests/test_self_improvement_engine.sh:284:     repository="/tmp/repo",
tests/test_self_improvement_engine.sh:360:     repository=".",
tests/test_semantic_repository_intelligence.sh:7: echo "Semantic Repository Intelligence Test"
tests/test_semantic_repository_intelligence.sh:296: engine = SemanticRepositoryEngine(repository='.', persist=False)
tests/test_semantic_repository_intelligence.sh:300: assert 'repository' in result
tests/test_semantic_repository_intelligence.sh:347:     engine = SemanticRepositoryEngine(repository='.', persist=False)
tests/test_semantic_repository_intelligence.sh:372: echo "Semantic Repository Intelligence PASS"
tests/test_workspace_index.sh:29: assert index.repository_name, "Repository name must be set"
tests/test_workspace_index.sh:30: assert index.repository_root, "Repository root must be set"
tests/test_workspace_index.sh:61: # Test 3 — Exactly one repository traversal
tests/test_workspace_index.sh:82: print(f"[PASS] Exactly one repository traversal (os.walk called {traversal_count[0]} time)")
tests/test_workspace_orchestrator.sh:118:                 rank=1, repository="repo-a", reason="Test.",
tests/test_workspace_orchestrator.sh:418:         assert priorities[0].repository == "repo-a"
tests/test_workspace_orchestrator.sh:640:         assert priorities[0].repository == "b"   # critical first
tests/test_workspace_orchestrator.sh:641:         assert priorities[1].repository == "a"
tests/test_workspace_orchestrator.sh:660:         a_priority = next(p for p in priorities if p.repository == "a")
tests/test_workspace_orchestrator.sh:734:             rank=1, repository="a", reason="test", expected_impact="good",
tests/test_workspace_orchestrator.sh:955:                 assert p.repository
tests/test_workspace_orchestrator.sh:986:             assert "repository" in r
tests/test_workspace_profile.sh:25:     ("Repository", lambda r: RepositoryEngine(r).statistics()),
tests/test_workspace_profile.sh:49:     row = {"Repository": repo["name"]}
tests/test_workspace_profile.sh:77:     f'{"Repository":25}'
tests/test_workspace_profile.sh:99:         f'{row["Repository"]:25}'
tests/test_workspace_profile.sh:100:         f'{fmt(row["Repository"] and row["Repository"] or 0):>8}'
tools/engineering/generate_repository_audit.py:15:     / "repository-audit.md"
tools/engineering/generate_repository_audit.py:22: print("Repository Audit generated successfully")
```

Matches: 1105

### Term: `storage`

```text
.ai/audit/knowledge_graph_v2.json:58:     "lib/python/session_runtime/storage.py",
.ai/audit/knowledge_graph_v2.json:546:       "from": "lib/python/session_runtime/storage.py",
.ai/audit/knowledge_graph_v2.json:551:       "from": "lib/python/session_runtime/storage.py",
.ai/audit/knowledge_graph_v2.json:567:       "to": "storage",
.ai/context/git_context.json:11:   "repository_root": "/storage/emulated/0/AI-Projects/AI-Toolkit",
.ai/context/live_context.json:28:     "roadmap_path": "/storage/emulated/0/AI-Projects/AI-Toolkit/docs/canonical/ROADMAP_v2.0.0.md"
.ai/context/live_context.json:38:   "repository_root": "/storage/emulated/0/AI-Projects/AI-Toolkit",
.ai/context/live_context.json:59:   "workspace": "/storage/emulated/0/AI-Projects",
.ai/context/repository_profile.json:3:   "root": "/storage/emulated/0/AI-Projects/AI-Toolkit",
.ai/context/synchronization_report.json:24:   "workspace": "/storage/emulated/0/AI-Projects"
.ai/context/workspace_context.json:28:     "repository_root": "/storage/emulated/0/AI-Projects/AI-Toolkit"
.ai/context/workspace_context.json:31:   "workspace": "/storage/emulated/0/AI-Projects",
.ai/context/workspace_context.json:32:   "workspace_root": "/storage/emulated/0/AI-Projects",
.ai/execution/execution.json:12:     "environment": "/storage/emulated/0/AI-Projects/AI-Toolkit",
.ai/execution/execution.json:20:     "repository": "/storage/emulated/0/AI-Projects/AI-Toolkit",
.ai/execution/execution.json:26:     "workspace": "/storage/emulated/0/AI-Projects"
.ai/execution/execution.json:666:   "repository": "/storage/emulated/0/AI-Projects/AI-Toolkit",
.ai/execution/execution_context.json:9:   "environment": "/storage/emulated/0/AI-Projects/AI-Toolkit",
.ai/execution/execution_context.json:17:   "repository": "/storage/emulated/0/AI-Projects/AI-Toolkit",
.ai/execution/execution_context.json:23:   "workspace": "/storage/emulated/0/AI-Projects"
.ai/execution/execution_history.json:207:       "repository": "/storage/emulated/0/AI-Projects/AI-Toolkit",
.ai/execution/execution_history.json:215:   "repository": "/storage/emulated/0/AI-Projects/AI-Toolkit",
.ai/execution/execution_report.json:12:   "repository": "/storage/emulated/0/AI-Projects/AI-Toolkit",
.ai/memory/repository_profile_1.json:3:   "root": "/storage/emulated/0/AI-Projects/AI-Toolkit",
.ai/memory/repository_profile_2.json:3:   "root": "/storage/emulated/0/AI-Projects/AI-Toolkit",
.ai/reports/inspect-20260807.json:4895:       "path": "lib/python/session_runtime/storage.py",
.ai/runtime/cache/workspace_index/index.json:3:   "repository_root": "/storage/emulated/0/AI-Projects/AI-Toolkit",
.ai/runtime/cache/workspace_index/index.json:483:       "path": "lib/python/session_runtime/storage.py",
.ai/runtime/cache/workspace_index/index.json:484:       "name": "storage.py",
.ai/runtime/cache/workspace_index/snapshot.json:3:   "repository_root": "/storage/emulated/0/AI-Projects/AI-Toolkit",
.ai/runtime/cache/workspace_index/snapshot.json:319:     "lib/python/session_runtime/storage.py": {
.ai/runtime_repository_model.json:2433:         "path": "lib/python/session_runtime/storage.py",
.ai/runtime_repository_model.json:3683:           "name": "storage",
.ai/runtime_repository_model.json:3684:           "file": "lib/python/session_runtime/storage.py",
.ai/runtime_repository_model.json:3938:         "lib/python/session_runtime/storage.py",
.ai/runtime_repository_model.json:4172:         "lib/python/session_runtime/storage.py",
.ai/runtime_repository_model.json:5111:           "target": "lib/python/session_runtime/storage.py",
.ai/self_evaluation/evaluation.json:55:     "repository": "/storage/emulated/0/AI-Projects/AI-Toolkit",
.ai/self_evaluation/evaluation.json:58:     "workspace": "/storage/emulated/0/AI-Projects"
.ai/self_evaluation/evaluation.json:190:   "repository": "/storage/emulated/0/AI-Projects/AI-Toolkit",
.ai/self_evaluation/history.json:119:       "repository": "/storage/emulated/0/AI-Projects/AI-Toolkit",
.ai/self_evaluation/history.json:125:   "repository": "/storage/emulated/0/AI-Projects/AI-Toolkit",
.ai/self_evaluation/snapshot.json:9:     "repository": "/storage/emulated/0/AI-Projects/AI-Toolkit",
.ai/self_evaluation/snapshot.json:12:     "workspace": "/storage/emulated/0/AI-Projects"
.ai/self_improvement/history.json:107:       "repository": "/storage/emulated/0/AI-Projects/AI-Toolkit",
.ai/self_improvement/history.json:114:   "repository": "/storage/emulated/0/AI-Projects/AI-Toolkit",
.ai/self_improvement/improvements.json:66:         "directory": "/storage/emulated/0/AI-Projects/AI-Toolkit/lib/python"
.ai/self_improvement/improvements.json:177:         "file": "/storage/emulated/0/AI-Projects/AI-Toolkit/lib/python/autonomous_workflow_engine.py"
.ai/self_improvement/improvements.json:201:         "file": "/storage/emulated/0/AI-Projects/AI-Toolkit/lib/python/decision_engine.py"
.ai/self_improvement/improvements.json:225:         "file": "/storage/emulated/0/AI-Projects/AI-Toolkit/lib/python/development_validator.py"
.ai/self_improvement/improvements.json:249:         "file": "/storage/emulated/0/AI-Projects/AI-Toolkit/lib/python/foundation_audit.py"
.ai/self_improvement/improvements.json:273:         "file": "/storage/emulated/0/AI-Projects/AI-Toolkit/lib/python/knowledge_graph_engine.py"
.ai/self_improvement/improvements.json:297:         "file": "/storage/emulated/0/AI-Projects/AI-Toolkit/lib/python/memory_engine.py"
.ai/self_improvement/improvements.json:321:         "file": "/storage/emulated/0/AI-Projects/AI-Toolkit/lib/python/repository_hygiene_audit.py"
.ai/self_improvement/improvements.json:345:         "file": "/storage/emulated/0/AI-Projects/AI-Toolkit/lib/python/repository_inventory.py"
.ai/self_improvement/improvements.json:369:         "file": "/storage/emulated/0/AI-Projects/AI-Toolkit/lib/python/repository_profile.py"
.ai/self_improvement/improvements.json:458:   "repository": "/storage/emulated/0/AI-Projects/AI-Toolkit",
.ai/self_improvement/improvements.json:471:         "file": "/storage/emulated/0/AI-Projects/AI-Toolkit/lib/python/autonomous_workflow_engine.py"
.ai/self_improvement/improvements.json:483:         "file": "/storage/emulated/0/AI-Projects/AI-Toolkit/lib/python/decision_engine.py"
.ai/self_improvement/improvements.json:495:         "file": "/storage/emulated/0/AI-Projects/AI-Toolkit/lib/python/development_validator.py"
.ai/self_improvement/improvements.json:507:         "file": "/storage/emulated/0/AI-Projects/AI-Toolkit/lib/python/foundation_audit.py"
.ai/self_improvement/improvements.json:519:         "file": "/storage/emulated/0/AI-Projects/AI-Toolkit/lib/python/knowledge_graph_engine.py"
.ai/self_improvement/improvements.json:531:         "file": "/storage/emulated/0/AI-Projects/AI-Toolkit/lib/python/memory_engine.py"
.ai/self_improvement/improvements.json:543:         "file": "/storage/emulated/0/AI-Projects/AI-Toolkit/lib/python/repository_hygiene_audit.py"
.ai/self_improvement/improvements.json:555:         "file": "/storage/emulated/0/AI-Projects/AI-Toolkit/lib/python/repository_inventory.py"
.ai/self_improvement/improvements.json:567:         "file": "/storage/emulated/0/AI-Projects/AI-Toolkit/lib/python/repository_profile.py"
.ai/self_improvement/optimization_plan.json:66:         "directory": "/storage/emulated/0/AI-Projects/AI-Toolkit/lib/python"
.ai/self_improvement/optimization_plan.json:177:         "file": "/storage/emulated/0/AI-Projects/AI-Toolkit/lib/python/autonomous_workflow_engine.py"
.ai/self_improvement/optimization_plan.json:201:         "file": "/storage/emulated/0/AI-Projects/AI-Toolkit/lib/python/decision_engine.py"
.ai/self_improvement/optimization_plan.json:225:         "file": "/storage/emulated/0/AI-Projects/AI-Toolkit/lib/python/development_validator.py"
.ai/self_improvement/optimization_plan.json:249:         "file": "/storage/emulated/0/AI-Projects/AI-Toolkit/lib/python/foundation_audit.py"
.ai/self_improvement/optimization_plan.json:273:         "file": "/storage/emulated/0/AI-Projects/AI-Toolkit/lib/python/knowledge_graph_engine.py"
.ai/self_improvement/optimization_plan.json:297:         "file": "/storage/emulated/0/AI-Projects/AI-Toolkit/lib/python/memory_engine.py"
.ai/self_improvement/optimization_plan.json:321:         "file": "/storage/emulated/0/AI-Projects/AI-Toolkit/lib/python/repository_hygiene_audit.py"
.ai/self_improvement/optimization_plan.json:345:         "file": "/storage/emulated/0/AI-Projects/AI-Toolkit/lib/python/repository_inventory.py"
.ai/self_improvement/optimization_plan.json:369:         "file": "/storage/emulated/0/AI-Projects/AI-Toolkit/lib/python/repository_profile.py"
.ai/self_improvement/optimization_plan.json:458:   "repository": "/storage/emulated/0/AI-Projects/AI-Toolkit",
.ai/self_improvement/optimization_plan.json:471:         "file": "/storage/emulated/0/AI-Projects/AI-Toolkit/lib/python/autonomous_workflow_engine.py"
.ai/self_improvement/optimization_plan.json:483:         "file": "/storage/emulated/0/AI-Projects/AI-Toolkit/lib/python/decision_engine.py"
.ai/self_improvement/optimization_plan.json:495:         "file": "/storage/emulated/0/AI-Projects/AI-Toolkit/lib/python/development_validator.py"
.ai/self_improvement/optimization_plan.json:507:         "file": "/storage/emulated/0/AI-Projects/AI-Toolkit/lib/python/foundation_audit.py"
.ai/self_improvement/optimization_plan.json:519:         "file": "/storage/emulated/0/AI-Projects/AI-Toolkit/lib/python/knowledge_graph_engine.py"
.ai/self_improvement/optimization_plan.json:531:         "file": "/storage/emulated/0/AI-Projects/AI-Toolkit/lib/python/memory_engine.py"
.ai/self_improvement/optimization_plan.json:543:         "file": "/storage/emulated/0/AI-Projects/AI-Toolkit/lib/python/repository_hygiene_audit.py"
.ai/self_improvement/optimization_plan.json:555:         "file": "/storage/emulated/0/AI-Projects/AI-Toolkit/lib/python/repository_inventory.py"
.ai/self_improvement/optimization_plan.json:567:         "file": "/storage/emulated/0/AI-Projects/AI-Toolkit/lib/python/repository_profile.py"
.ai/self_improvement/performance.json:31:         "directory": "/storage/emulated/0/AI-Projects/AI-Toolkit/lib/python"
.ai/self_improvement/proposed_issues.json:20:         "file": "/storage/emulated/0/AI-Projects/AI-Toolkit/lib/python/autonomous_workflow_engine.py"
.ai/self_improvement/proposed_issues.json:44:         "file": "/storage/emulated/0/AI-Projects/AI-Toolkit/lib/python/decision_engine.py"
.ai/self_improvement/proposed_issues.json:68:         "file": "/storage/emulated/0/AI-Projects/AI-Toolkit/lib/python/development_validator.py"
.ai/self_improvement/proposed_issues.json:92:         "file": "/storage/emulated/0/AI-Projects/AI-Toolkit/lib/python/foundation_audit.py"
.ai/self_improvement/proposed_issues.json:116:         "file": "/storage/emulated/0/AI-Projects/AI-Toolkit/lib/python/knowledge_graph_engine.py"
.ai/self_improvement/proposed_issues.json:140:         "file": "/storage/emulated/0/AI-Projects/AI-Toolkit/lib/python/memory_engine.py"
.ai/self_improvement/proposed_issues.json:164:         "file": "/storage/emulated/0/AI-Projects/AI-Toolkit/lib/python/repository_hygiene_audit.py"
.ai/self_improvement/proposed_issues.json:188:         "file": "/storage/emulated/0/AI-Projects/AI-Toolkit/lib/python/repository_inventory.py"
.ai/self_improvement/proposed_issues.json:212:         "file": "/storage/emulated/0/AI-Projects/AI-Toolkit/lib/python/repository_profile.py"
.ai/self_improvement/snapshot.json:6:   "repository": "/storage/emulated/0/AI-Projects/AI-Toolkit",
.ai/self_improvement/technical_debt.json:12:         "file": "/storage/emulated/0/AI-Projects/AI-Toolkit/lib/python/autonomous_workflow_engine.py"
.ai/self_improvement/technical_debt.json:24:         "file": "/storage/emulated/0/AI-Projects/AI-Toolkit/lib/python/decision_engine.py"
.ai/self_improvement/technical_debt.json:36:         "file": "/storage/emulated/0/AI-Projects/AI-Toolkit/lib/python/development_validator.py"
.ai/self_improvement/technical_debt.json:48:         "file": "/storage/emulated/0/AI-Projects/AI-Toolkit/lib/python/foundation_audit.py"
.ai/self_improvement/technical_debt.json:60:         "file": "/storage/emulated/0/AI-Projects/AI-Toolkit/lib/python/knowledge_graph_engine.py"
.ai/self_improvement/technical_debt.json:72:         "file": "/storage/emulated/0/AI-Projects/AI-Toolkit/lib/python/memory_engine.py"
.ai/self_improvement/technical_debt.json:84:         "file": "/storage/emulated/0/AI-Projects/AI-Toolkit/lib/python/repository_hygiene_audit.py"
.ai/self_improvement/technical_debt.json:96:         "file": "/storage/emulated/0/AI-Projects/AI-Toolkit/lib/python/repository_inventory.py"
.ai/self_improvement/technical_debt.json:108:         "file": "/storage/emulated/0/AI-Projects/AI-Toolkit/lib/python/repository_profile.py"
lib/python/ai_cto_scanner/detectors.py:363:             r"storage\b",
lib/python/ai_cto_scanner/detectors.py:365:             r"Storage\b",
lib/python/ai_cto_scanner/detectors.py:366:             "path:storage",
lib/python/semantic_repository_intelligence/persistence.py:93:         Extract a compact summary of the analysis result for storage.
lib/python/session_runtime/runtime.py:4: from .storage import SessionStorage
lib/python/session_runtime/runtime.py:10:         self.storage = SessionStorage()
lib/python/session_runtime/runtime.py:23:         self.storage.save(session)
lib/python/session_runtime/runtime.py:32:         self.storage.save(session)
```

Matches: 114

### Term: `persistence`

```text
.ai/execution/execution.json:839:         "{'id': 'ARCH-RISK-004', 'title': 'Unclassified modules', 'description': '108 modules could not be assigned to a known architectural layer.', 'severity': 'low', 'affected_modules': ['lib/python/__init__.py', 'lib/python/autonomous_execution_engine/__init__.py', 'lib/python/autonomous_execution_engine/engine.py', 'lib/python/autonomous_execution_engine/evidence.py', 'lib/python/autonomous_execution_engine/logger.py', 'lib/python/autonomous_execution_engine/persistence.py', 'lib/python/autonomous_execution_engine/policy.py', 'lib/python/autonomous_execution_engine/rollback.py', 'lib/python/autonomous_execution_engine/validator.py', 'lib/python/autonomous_planner/__init__.py'], 'evidence': ['Layer classification: Uncategorised'], 'confidence': 0.7}",
.ai/execution/execution_results.json:33:         "{'id': 'ARCH-RISK-004', 'title': 'Unclassified modules', 'description': '108 modules could not be assigned to a known architectural layer.', 'severity': 'low', 'affected_modules': ['lib/python/__init__.py', 'lib/python/autonomous_execution_engine/__init__.py', 'lib/python/autonomous_execution_engine/engine.py', 'lib/python/autonomous_execution_engine/evidence.py', 'lib/python/autonomous_execution_engine/logger.py', 'lib/python/autonomous_execution_engine/persistence.py', 'lib/python/autonomous_execution_engine/policy.py', 'lib/python/autonomous_execution_engine/rollback.py', 'lib/python/autonomous_execution_engine/validator.py', 'lib/python/autonomous_planner/__init__.py'], 'evidence': ['Layer classification: Uncategorised'], 'confidence': 0.7}",
.ai/reports/inspect-20260807.json:2858:       "path": "lib/python/autonomous_execution_engine/persistence.py",
.ai/reports/inspect-20260807.json:2970:       "path": "lib/python/autonomous_planning_engine/persistence.py",
.ai/reports/inspect-20260807.json:3222:       "path": "lib/python/context_synchronization_engine/persistence.py",
.ai/reports/inspect-20260807.json:3915:       "path": "lib/python/executable_repository_intelligence/persistence.py",
.ai/reports/inspect-20260807.json:4020:       "path": "lib/python/executive_briefing_engine/persistence.py",
.ai/reports/inspect-20260807.json:4685:       "path": "lib/python/self_evaluation_engine/persistence.py",
.ai/reports/inspect-20260807.json:4741:       "path": "lib/python/self_improvement_engine/persistence.py",
.ai/reports/inspect-20260807.json:4853:       "path": "lib/python/semantic_repository_intelligence/persistence.py",
.ai/reports/inspect-20260807.json:5035:       "path": "lib/python/workspace_orchestrator/persistence.py",
.ai/runtime_repository_model.json:1623:         "path": "lib/python/executable_repository_intelligence/persistence.py",
.ai/runtime_repository_model.json:2373:         "path": "lib/python/semantic_repository_intelligence/persistence.py",
.ai/runtime_repository_model.json:2638:         "lib/python/executable_repository_intelligence/persistence.py",
.ai/runtime_repository_model.json:2740:           "role": "persistence",
.ai/runtime_repository_model.json:2741:           "layer": "Persistence",
.ai/runtime_repository_model.json:2838:           "role": "persistence",
.ai/runtime_repository_model.json:2839:           "layer": "Persistence",
.ai/runtime_repository_model.json:2852:           "role": "persistence",
.ai/runtime_repository_model.json:2853:           "layer": "Persistence",
.ai/runtime_repository_model.json:2866:           "role": "persistence",
.ai/runtime_repository_model.json:2867:           "layer": "Persistence",
.ai/runtime_repository_model.json:2908:           "role": "persistence",
.ai/runtime_repository_model.json:2909:           "layer": "Persistence",
.ai/runtime_repository_model.json:3083:           "role": "persistence",
.ai/runtime_repository_model.json:3084:           "layer": "Persistence",
.ai/runtime_repository_model.json:3116:           "name": "persistence",
.ai/runtime_repository_model.json:3117:           "file": "lib/python/executable_repository_intelligence/persistence.py",
.ai/runtime_repository_model.json:3461:           "role": "persistence",
.ai/runtime_repository_model.json:3462:           "layer": "Persistence",
.ai/runtime_repository_model.json:3641:           "name": "persistence",
.ai/runtime_repository_model.json:3642:           "file": "lib/python/semantic_repository_intelligence/persistence.py",
.ai/runtime_repository_model.json:3678:           "role": "persistence",
.ai/runtime_repository_model.json:3679:           "layer": "Persistence",
.ai/runtime_repository_model.json:3818:         "lib/python/executable_repository_intelligence/persistence.py",
.ai/runtime_repository_model.json:3933:         "lib/python/semantic_repository_intelligence/persistence.py",
.ai/runtime_repository_model.json:4091:         "lib/python/executable_repository_intelligence/persistence.py",
.ai/runtime_repository_model.json:4166:         "lib/python/semantic_repository_intelligence/persistence.py",
.ai/runtime_repository_model.json:4651:           "target": "lib/python/executable_repository_intelligence/persistence.py",
.ai/runtime_repository_model.json:4696:           "target": "lib/python/executable_repository_intelligence/persistence.py",
.ai/runtime_repository_model.json:4986:           "target": "lib/python/semantic_repository_intelligence/persistence.py",
.ai/runtime_repository_model.json:5066:           "target": "lib/python/semantic_repository_intelligence/persistence.py",
.ai/self_evaluation/architecture.json:32:       "component": "{'id': 'ARCH-RISK-004', 'title': 'Unclassified modules', 'description': '108 modules could not be assigned to a known architectural layer.', 'severity': 'low', 'affected_modules': ['lib/python/__init__.py', 'lib/python/autonomous_execution_engine/__init__.py', 'lib/python/autonomous_execution_engine/engine.py', 'lib/python/autonomous_execution_engine/evidence.py', 'lib/python/autonomous_execution_engine/logger.py', 'lib/python/autonomous_execution_engine/persistence.py', 'lib/python/autonomous_execution_engine/policy.py', 'lib/python/autonomous_execution_engine/rollback.py', 'lib/python/autonomous_execution_engine/validator.py', 'lib/python/autonomous_planner/__init__.py'], 'evidence': ['Layer classification: Uncategorised'], 'confidence': 0.7}",
.ai/self_evaluation/architecture.json:33:       "description": "{'id': 'ARCH-RISK-004', 'title': 'Unclassified modules', 'description': '108 modules could not be assigned to a known architectural layer.', 'severity': 'low', 'affected_modules': ['lib/python/__init__.py', 'lib/python/autonomous_execution_engine/__init__.py', 'lib/python/autonomous_execution_engine/engine.py', 'lib/python/autonomous_execution_engine/evidence.py', 'lib/python/autonomous_execution_engine/logger.py', 'lib/python/autonomous_execution_engine/persistence.py', 'lib/python/autonomous_execution_engine/policy.py', 'lib/python/autonomous_execution_engine/rollback.py', 'lib/python/autonomous_execution_engine/validator.py', 'lib/python/autonomous_planner/__init__.py'], 'evidence': ['Layer classification: Uncategorised'], 'confidence': 0.7}",
.ai/self_evaluation/evaluation.json:32:       "component": "{'id': 'ARCH-RISK-004', 'title': 'Unclassified modules', 'description': '108 modules could not be assigned to a known architectural layer.', 'severity': 'low', 'affected_modules': ['lib/python/__init__.py', 'lib/python/autonomous_execution_engine/__init__.py', 'lib/python/autonomous_execution_engine/engine.py', 'lib/python/autonomous_execution_engine/evidence.py', 'lib/python/autonomous_execution_engine/logger.py', 'lib/python/autonomous_execution_engine/persistence.py', 'lib/python/autonomous_execution_engine/policy.py', 'lib/python/autonomous_execution_engine/rollback.py', 'lib/python/autonomous_execution_engine/validator.py', 'lib/python/autonomous_planner/__init__.py'], 'evidence': ['Layer classification: Uncategorised'], 'confidence': 0.7}",
.ai/self_evaluation/evaluation.json:33:       "description": "{'id': 'ARCH-RISK-004', 'title': 'Unclassified modules', 'description': '108 modules could not be assigned to a known architectural layer.', 'severity': 'low', 'affected_modules': ['lib/python/__init__.py', 'lib/python/autonomous_execution_engine/__init__.py', 'lib/python/autonomous_execution_engine/engine.py', 'lib/python/autonomous_execution_engine/evidence.py', 'lib/python/autonomous_execution_engine/logger.py', 'lib/python/autonomous_execution_engine/persistence.py', 'lib/python/autonomous_execution_engine/policy.py', 'lib/python/autonomous_execution_engine/rollback.py', 'lib/python/autonomous_execution_engine/validator.py', 'lib/python/autonomous_planner/__init__.py'], 'evidence': ['Layer classification: Uncategorised'], 'confidence': 0.7}",
.ai/self_evaluation/evaluation.json:86:         "{'id': 'ARCH-RISK-004', 'title': 'Unclassified modules', 'description': '108 modules could not be assigned to a known architectural layer.', 'severity': 'low', 'affected_modules': ['lib/python/__init__.py', 'lib/python/autonomous_execution_engine/__init__.py', 'lib/python/autonomous_execution_engine/engine.py', 'lib/python/autonomous_execution_engine/evidence.py', 'lib/python/autonomous_execution_engine/logger.py', 'lib/python/autonomous_execution_engine/persistence.py', 'lib/python/autonomous_execution_engine/policy.py', 'lib/python/autonomous_execution_engine/rollback.py', 'lib/python/autonomous_execution_engine/validator.py', 'lib/python/autonomous_planner/__init__.py'], 'evidence': ['Layer classification: Uncategorised'], 'confidence': 0.7}",
.ai/self_evaluation/evidence.json:24:         "{'id': 'ARCH-RISK-004', 'title': 'Unclassified modules', 'description': '108 modules could not be assigned to a known architectural layer.', 'severity': 'low', 'affected_modules': ['lib/python/__init__.py', 'lib/python/autonomous_execution_engine/__init__.py', 'lib/python/autonomous_execution_engine/engine.py', 'lib/python/autonomous_execution_engine/evidence.py', 'lib/python/autonomous_execution_engine/logger.py', 'lib/python/autonomous_execution_engine/persistence.py', 'lib/python/autonomous_execution_engine/policy.py', 'lib/python/autonomous_execution_engine/rollback.py', 'lib/python/autonomous_execution_engine/validator.py', 'lib/python/autonomous_planner/__init__.py'], 'evidence': ['Layer classification: Uncategorised'], 'confidence': 0.7}",
.ai/self_evaluation/quality.json:26:         "{'id': 'ARCH-RISK-004', 'title': 'Unclassified modules', 'description': '108 modules could not be assigned to a known architectural layer.', 'severity': 'low', 'affected_modules': ['lib/python/__init__.py', 'lib/python/autonomous_execution_engine/__init__.py', 'lib/python/autonomous_execution_engine/engine.py', 'lib/python/autonomous_execution_engine/evidence.py', 'lib/python/autonomous_execution_engine/logger.py', 'lib/python/autonomous_execution_engine/persistence.py', 'lib/python/autonomous_execution_engine/policy.py', 'lib/python/autonomous_execution_engine/rollback.py', 'lib/python/autonomous_execution_engine/validator.py', 'lib/python/autonomous_planner/__init__.py'], 'evidence': ['Layer classification: Uncategorised'], 'confidence': 0.7}",
lib/python/ai_cto_scanner/detectors.py:346:         ("Persistence", [
lib/python/ai_cto_scanner/detectors.py:357:             "path:persistence",
lib/python/ai_cto_scanner/detectors.py:509:         ("Context Persistence", [
lib/python/ai_cto_scanner/report.py:200:                 "Connect project memory to AI CTO context persistence layer",
lib/python/ai_cto_scanner/report.py:276:             ("State", "State Readiness", "Implement state persistence and session management"),
lib/python/ai_cto_scanner/report.py:280:             ("ProjectMemory", "Project Memory Readiness", "Implement project memory and context persistence"),
lib/python/ai_cto_scanner/report.py:325:             lines.append("| No project memory infrastructure | HIGH | ProjectMemory | Implement project memory and context persistence |")
lib/python/ai_cto_scanner/scoring.py:16:         "Persistence": 0.8,
lib/python/ai_cto_scanner/scoring.py:47:         # Persistence Readiness (derived from State + Configuration)
lib/python/ai_cto_scanner/scoring.py:49:         persist_components = self._filter_components(state, ["Persistence", "State Store", "Session Management"])
lib/python/ai_cto_scanner/scoring.py:53:         scores["Persistence Readiness"] = min(100, int((persist_count / persist_total) * 100))
lib/python/ai_cto_scanner/scoring.py:79:         integrity_components = self._filter_components(memory, ["Context Integrity", "Snapshot Engine", "Context Persistence"])
lib/python/autonomous_execution_engine/__init__.py:72: from .persistence import ExecutionPersistence
lib/python/autonomous_execution_engine/engine.py:73: from .persistence import ExecutionPersistence
lib/python/autonomous_execution_engine/engine.py:507:             persistence = ExecutionPersistence(str(self.root))
lib/python/autonomous_execution_engine/engine.py:508:             paths = persistence.save(
lib/python/autonomous_execution_engine/engine.py:559:             from python.context_synchronization_engine.persistence import (  # type: ignore[import]
lib/python/autonomous_execution_engine/engine.py:562:             persistence = ContextPersistence(str(self.root))
lib/python/autonomous_execution_engine/engine.py:563:             return persistence.load_live_context()
lib/python/autonomous_execution_engine/engine.py:578:             from python.executive_briefing_engine.persistence import (  # type: ignore[import]
lib/python/autonomous_execution_engine/engine.py:581:             persistence = ExecutiveBriefingPersistence(str(self.root))
lib/python/autonomous_execution_engine/engine.py:582:             return persistence.load_briefing()
lib/python/autonomous_execution_engine/engine.py:588:             from python.autonomous_planning_engine.persistence import (  # type: ignore[import]
lib/python/autonomous_execution_engine/engine.py:591:             persistence = PlanningPersistence(str(self.root))
lib/python/autonomous_execution_engine/engine.py:592:             planning = persistence.load_planning()
lib/python/autonomous_execution_engine/persistence.py:2: Autonomous Execution Engine — Persistence Layer
lib/python/autonomous_execution_engine/persistence.py:30:     CORE-015G — Execution Persistence.
lib/python/autonomous_planning_engine/__init__.py:27: from .persistence import PlanningPersistence
lib/python/autonomous_planning_engine/engine.py:54: from .persistence import PlanningPersistence
lib/python/autonomous_planning_engine/engine.py:171:             persistence = PlanningPersistence(str(self.root))
lib/python/autonomous_planning_engine/engine.py:172:             paths = persistence.save(planning_result)
lib/python/autonomous_planning_engine/engine.py:202:             from python.executive_briefing_engine.persistence import (
lib/python/autonomous_planning_engine/engine.py:205:             persistence = ExecutiveBriefingPersistence(str(self.root))
lib/python/autonomous_planning_engine/engine.py:206:             return persistence.load_briefing()
lib/python/autonomous_planning_engine/engine.py:334:             from python.workspace_orchestrator.persistence import WorkspacePersistence
lib/python/autonomous_planning_engine/persistence.py:2: Autonomous Planning Engine — Persistence Layer
lib/python/autonomous_planning_engine/persistence.py:28:     CORE-014K — Planning Persistence.
lib/python/context_synchronization_engine/__init__.py:24: from .persistence import ContextPersistence
lib/python/context_synchronization_engine/engine.py:18: from .persistence import ContextPersistence
lib/python/context_synchronization_engine/engine.py:86:         self.persistence = ContextPersistence(repository_root)
lib/python/context_synchronization_engine/engine.py:90:             "live_context": self.persistence.load_json("live_context.json") or {},
lib/python/context_synchronization_engine/engine.py:91:             "report": self.persistence.load_json("synchronization_report.json") or {},
lib/python/context_synchronization_engine/engine.py:227:         self.persistence = ContextPersistence(self.root)
lib/python/context_synchronization_engine/engine.py:1299:         persistence = ContextPersistence(self.root)
lib/python/context_synchronization_engine/engine.py:1301:             "live_context": persistence.save_json("live_context.json", self._sorted_mapping(live_context)),
lib/python/context_synchronization_engine/engine.py:1302:             "development_context": persistence.save_json(
lib/python/context_synchronization_engine/engine.py:1306:             "workspace_context": persistence.save_json(
lib/python/context_synchronization_engine/engine.py:1310:             "git_context": persistence.save_json("git_context.json", self._sorted_mapping(git_context)),
lib/python/context_synchronization_engine/engine.py:1311:             "github_context": persistence.save_json("github_context.json", self._sorted_mapping(github_context)),
lib/python/context_synchronization_engine/engine.py:1312:             "synchronization_report": persistence.save_json("synchronization_report.json", report.to_dict()),
lib/python/context_synchronization_engine/engine.py:1313:             "engineering_context": persistence.save_json("engineering_context.json", engineering_context.to_dict()),
lib/python/context_synchronization_engine/engine.py:1314:             "decision_history": persistence.save_json(
lib/python/context_synchronization_engine/engine.py:1326:         paths["markdown"] = persistence.save_text("AI_CTO_CONTEXT_REPORT.md", markdown)
lib/python/coverage_engine/engine.py:77:             "execution", "review", "observability", "persistence", "autonomous",
lib/python/dashboard/service.py:18: from python.workspace_orchestrator.persistence import WorkspacePersistence
lib/python/dashboard/service.py:79:         architecture="Builds on WorkspaceOrchestrator persistence and dashboard summaries, then renders repository cards and tables.",
lib/python/dashboard/service.py:180:         architecture="Builds on runtime and development-state persistence rather than creating separate dashboard-specific state.",
lib/python/dashboard/service.py:657:         persistence = WorkspacePersistence(str(self.workspace_root))
lib/python/dashboard/service.py:658:         if not persistence.exists():
lib/python/dashboard/service.py:660:         repositories = persistence.load_repositories()
lib/python/dashboard/service.py:666:             repositories = persistence.load_repositories()
lib/python/development_state_engine/__init__.py:4: Canonical state models and persistence repository for CANON-030.
lib/python/development_state_engine/repository.py:2: Development State Engine — Persistence Layer
lib/python/development_state_engine/repository.py:18:     """Persistence repository for DevelopmentState."""
lib/python/development_state_engine/runtime.py:209:     """Coordinates state persistence, runtime events, and executive snapshots."""
lib/python/development_state_engine/runtime.py:480:         persistence = SemanticPersistence(self.repository_root)
lib/python/development_state_engine/runtime.py:481:         if persistence.exists():
lib/python/development_state_engine/runtime.py:482:             loaded = persistence.load() or {}
lib/python/executable_repository_intelligence/__init__.py:22: from .persistence import ExecutablePersistence
lib/python/executable_repository_intelligence/engine.py:36: from .persistence import ExecutablePersistence
lib/python/executable_repository_intelligence/engine.py:158:                 persistence = ExecutablePersistence(self.root)
lib/python/executable_repository_intelligence/engine.py:159:                 runtime_model_path = persistence.save_runtime_model(result)
lib/python/executable_repository_intelligence/engine.py:160:                 exec_map_path = persistence.save_executable_map(result)
lib/python/executable_repository_intelligence/engine.py:164:                 print("[CORE-008C] WARNING: Persistence failed: %s" % exc, file=sys.stderr)
lib/python/executable_repository_intelligence/models.py:95:     layer: str         # e.g. "Telegram", "Persistence", "Core"
lib/python/executable_repository_intelligence/persistence.py:2: Executable Repository Intelligence — Persistence
lib/python/executable_repository_intelligence/report.py:129:         lines.append(_list_section("Persistence Runtime", rm.get("persistence_runtime", [])))
lib/python/executable_repository_intelligence/runtime_map.py:7: and runtime subsystems (Telegram, Scheduler, Persistence, etc.).
lib/python/executable_repository_intelligence/runtime_map.py:136:                 role = "persistence" if role == "executable" else role
lib/python/executable_repository_intelligence/runtime_map.py:137:                 layer = "Persistence" if layer == "Core" else layer
lib/python/executive_briefing_engine/__init__.py:17: from .persistence import ExecutiveBriefingPersistence
lib/python/executive_briefing_engine/engine.py:44: from .persistence import ExecutiveBriefingPersistence
lib/python/executive_briefing_engine/engine.py:111:             persistence = ExecutiveBriefingPersistence(str(self.root))
lib/python/executive_briefing_engine/engine.py:112:             paths = persistence.save(briefing)
lib/python/executive_briefing_engine/persistence.py:2: Executive Briefing Engine — Persistence Layer
lib/python/runtime/bootstrap.py:539:         self.lifecycle.transition(LifecyclePhase.PERSISTENCE)
lib/python/runtime/config.py:42:     # Persistence
lib/python/runtime/lifecycle.py:10:     → PERSISTENCE → TERMINATION
lib/python/runtime/lifecycle.py:33:     PERSISTENCE = "PERSISTENCE"
lib/python/runtime/lifecycle.py:85:             LifecyclePhase.PERSISTENCE,
lib/python/self_evaluation_engine/__init__.py:53: from .persistence import EvaluationPersistence
lib/python/self_evaluation_engine/__init__.py:72:     # Persistence
lib/python/self_evaluation_engine/engine.py:61: from .persistence import EvaluationPersistence
lib/python/self_evaluation_engine/engine.py:255:             persistence = EvaluationPersistence(str(self.root))
lib/python/self_evaluation_engine/engine.py:256:             paths = persistence.save(evaluation_result, markdown=markdown)
lib/python/self_evaluation_engine/engine.py:274:             from python.autonomous_planning_engine.persistence import (  # type: ignore[import]
lib/python/self_evaluation_engine/engine.py:283:             from python.autonomous_execution_engine.persistence import (  # type: ignore[import]
lib/python/self_evaluation_engine/engine.py:292:             from python.context_synchronization_engine.persistence import (  # type: ignore[import]
lib/python/self_evaluation_engine/engine.py:301:             from python.executive_briefing_engine.persistence import (  # type: ignore[import]
lib/python/self_evaluation_engine/engine.py:310:             from python.workspace_orchestrator.persistence import (  # type: ignore[import]
lib/python/self_evaluation_engine/persistence.py:2: Self Evaluation Engine — Persistence Layer
lib/python/self_evaluation_engine/persistence.py:30:     CORE-016D — Evaluation Persistence.
lib/python/self_improvement_engine/__init__.py:48: from .persistence import ImprovementPersistence
lib/python/self_improvement_engine/__init__.py:66:     # Persistence
lib/python/self_improvement_engine/analyzers.py:146:             from python.autonomous_execution_engine.persistence import (  # type: ignore[import]
lib/python/self_improvement_engine/analyzers.py:149:             persistence = ExecutionPersistence(self.repository)
lib/python/self_improvement_engine/analyzers.py:150:             history = persistence.load_history()
lib/python/self_improvement_engine/analyzers.py:172:             from python.self_evaluation_engine.persistence import (  # type: ignore[import]
lib/python/self_improvement_engine/analyzers.py:175:             persistence = EvaluationPersistence(self.repository)
lib/python/self_improvement_engine/analyzers.py:176:             history = persistence.load_evaluation()
lib/python/self_improvement_engine/engine.py:51: from .persistence import ImprovementPersistence
lib/python/self_improvement_engine/engine.py:256:             persistence = ImprovementPersistence(str(self.root))
lib/python/self_improvement_engine/engine.py:257:             paths = persistence.save(optimization_plan, markdown=markdown)
lib/python/self_improvement_engine/engine.py:275:             from python.self_evaluation_engine.persistence import (  # type: ignore[import]
lib/python/self_improvement_engine/persistence.py:2: Self Improvement Engine — Persistence Layer
lib/python/self_improvement_engine/persistence.py:31:     CORE-017D — Improvement Persistence.
lib/python/semantic_repository_intelligence/__init__.py:23: from .persistence import SemanticPersistence
lib/python/semantic_repository_intelligence/engine.py:32: from .persistence import SemanticPersistence
lib/python/semantic_repository_intelligence/engine.py:157:                 persistence = SemanticPersistence(self.root)
lib/python/semantic_repository_intelligence/engine.py:158:                 persistence.save(result)
lib/python/semantic_repository_intelligence/persistence.py:2: Semantic Repository Intelligence — Project Memory Persistence
lib/python/workspace_orchestrator/__init__.py:74: from .persistence import WorkspacePersistence
lib/python/workspace_orchestrator/__init__.py:131:     # Persistence
lib/python/workspace_orchestrator/engine.py:57: from .persistence import WorkspacePersistence
lib/python/workspace_orchestrator/engine.py:217:             persistence = WorkspacePersistence(self.workspace_root)
lib/python/workspace_orchestrator/engine.py:218:             persistence.save(result, stats)
lib/python/workspace_orchestrator/engine.py:222:             persistence.save_dashboard(workspace_id, now, dashboard_dict)
lib/python/workspace_orchestrator/engine.py:244:         persistence = WorkspacePersistence(self.workspace_root)
lib/python/workspace_orchestrator/engine.py:246:         if not persistence.exists():
lib/python/workspace_orchestrator/engine.py:255:             # Load from persistence
lib/python/workspace_orchestrator/engine.py:256:             repositories = persistence.load_repositories()
lib/python/workspace_orchestrator/engine.py:257:             health = persistence.load_health()
lib/python/workspace_orchestrator/engine.py:258:             priorities = persistence.load_priorities()
lib/python/workspace_orchestrator/engine.py:259:             recommendations = persistence.load_recommendations()
lib/python/workspace_orchestrator/engine.py:260:             risks = persistence.load_risks()
lib/python/workspace_orchestrator/engine.py:261:             workspace_meta = persistence.load_workspace()
lib/python/workspace_orchestrator/engine.py:264:             stats_obj = persistence.load_statistics()
lib/python/workspace_orchestrator/engine.py:279:                     total_dependencies=len(persistence.load_dependencies()),
lib/python/workspace_orchestrator/engine.py:280:                     total_relationships=len(persistence.load_relationships()),
lib/python/workspace_orchestrator/engine.py:288:             dependencies = persistence.load_dependencies()
lib/python/workspace_orchestrator/engine.py:289:             relationships = persistence.load_relationships()
lib/python/workspace_orchestrator/engine.py:342:             persistence.save_dashboard(workspace_id, now, dashboard_dict)
lib/python/workspace_orchestrator/engine.py:373:             persistence = WorkspacePersistence(self.workspace_root)
lib/python/workspace_orchestrator/engine.py:423:             persistence.save(result, stats)
lib/python/workspace_orchestrator/persistence.py:2: Workspace Orchestrator — Persistence Layer
lib/python/workspace_orchestrator/persistence.py:317:         """Return True if the workspace persistence directory exists."""
lib/python/workspace_orchestrator/registry.py:20:     persistence by WorkspacePersistence.
lib/python/workspace_orchestrator/state_manager.py:17: from .persistence import WorkspacePersistence
lib/python/workspace_orchestrator/state_manager.py:26:     - Load existing state from persistence on startup
lib/python/workspace_orchestrator/state_manager.py:44:         """Load existing workspace state from persistence."""
tests/test_ai_cto_scanner.sh:85:         'Persistence Readiness',
tests/test_autonomous_execution_engine.sh:306:     persistence = ExecutionPersistence(tmpdir)
tests/test_autonomous_execution_engine.sh:307:     assert not persistence.exists()
tests/test_autonomous_execution_engine.sh:309:     paths = persistence.save(
tests/test_autonomous_execution_engine.sh:316:     assert persistence.exists()
tests/test_autonomous_execution_engine.sh:323:     loaded = persistence.load_execution()
tests/test_autonomous_execution_engine.sh:327:     history = persistence.load_history()
tests/test_autonomous_execution_engine.sh:331:     persistence.save(exec_result, report_dict={}, markdown="")
tests/test_autonomous_execution_engine.sh:332:     history2 = persistence.load_history()
tests/test_autonomous_planning_engine.sh:387:     persistence = PlanningPersistence(tmpdir)
tests/test_autonomous_planning_engine.sh:388:     assert not persistence.exists()
tests/test_autonomous_planning_engine.sh:430:     paths = persistence.save(pr)
tests/test_autonomous_planning_engine.sh:431:     assert persistence.exists()
tests/test_autonomous_planning_engine.sh:437:     loaded = persistence.load_planning()
tests/test_development_state_persistence.sh:243:     print("\nDevelopment State Persistence PASS")
tests/test_development_state_runtime_integration.sh:15: from python.semantic_repository_intelligence.persistence import SemanticPersistence
tests/test_executable_repository_intelligence.sh:290: from python.executable_repository_intelligence.persistence import ExecutablePersistence
tests/test_executive_briefing_engine.sh:728: # Persistence tests
tests/test_executive_briefing_engine.sh:754:             persistence = ExecutiveBriefingPersistence(tmpdir)
tests/test_executive_briefing_engine.sh:755:             paths = persistence.save(self._make_briefing())
tests/test_executive_briefing_engine.sh:763:             persistence = ExecutiveBriefingPersistence(tmpdir)
tests/test_executive_briefing_engine.sh:764:             paths = persistence.save(self._make_briefing())
tests/test_executive_briefing_engine.sh:772:             persistence = ExecutiveBriefingPersistence(tmpdir)
tests/test_executive_briefing_engine.sh:774:             persistence.save(briefing)
tests/test_executive_briefing_engine.sh:775:             loaded = persistence.load_briefing()
tests/test_executive_briefing_engine.sh:780:             persistence = ExecutiveBriefingPersistence(tmpdir)
tests/test_executive_briefing_engine.sh:781:             self.assertFalse(persistence.exists())
tests/test_executive_briefing_engine.sh:785:             persistence = ExecutiveBriefingPersistence(tmpdir)
tests/test_executive_briefing_engine.sh:786:             persistence.save(self._make_briefing())
tests/test_executive_briefing_engine.sh:787:             self.assertTrue(persistence.exists())
tests/test_executive_briefing_engine.sh:791:             persistence = ExecutiveBriefingPersistence(tmpdir)
tests/test_executive_briefing_engine.sh:793:             persistence.save(briefing)
tests/test_executive_briefing_engine.sh:795:             persistence.save(briefing)
tests/test_self_evaluation_engine.sh:289:     persistence = EvaluationPersistence(tmpdir)
tests/test_self_evaluation_engine.sh:290:     assert not persistence.exists()
tests/test_self_evaluation_engine.sh:292:     paths = persistence.save(eval_result, markdown=markdown)
tests/test_self_evaluation_engine.sh:293:     assert persistence.exists()
tests/test_self_evaluation_engine.sh:301:     loaded = persistence.load_evaluation()
tests/test_self_evaluation_engine.sh:305:     history = persistence.load_evaluation()
tests/test_self_improvement_engine.sh:328:     persistence = ImprovementPersistence(tmpdir)
tests/test_self_improvement_engine.sh:329:     assert not persistence.exists()
tests/test_self_improvement_engine.sh:331:     paths = persistence.save(plan, markdown=markdown)
tests/test_self_improvement_engine.sh:332:     assert persistence.exists()
tests/test_self_improvement_engine.sh:344:     loaded = persistence.load_improvements()
tests/test_self_improvement_engine.sh:349:     persistence.save(plan)
tests/test_self_improvement_engine.sh:350:     loaded2 = persistence.load_improvements()
tests/test_workspace_orchestrator.sh:351: # Tests — Persistence
tests/test_workspace_orchestrator.sh:358:         self.persistence = WorkspacePersistence(self.tmp)
tests/test_workspace_orchestrator.sh:378:         paths = self.persistence.save(result, stats)
tests/test_workspace_orchestrator.sh:385:         repos = self.persistence.load_repositories()
tests/test_workspace_orchestrator.sh:400:         self.persistence.save(result, stats)
tests/test_workspace_orchestrator.sh:401:         health = self.persistence.load_health()
tests/test_workspace_orchestrator.sh:415:         self.persistence.save(result, stats)
tests/test_workspace_orchestrator.sh:416:         priorities = self.persistence.load_priorities()
tests/test_workspace_orchestrator.sh:429:         self.persistence.save(result, stats)
tests/test_workspace_orchestrator.sh:430:         self.persistence.save(result, stats)
tests/test_workspace_orchestrator.sh:431:         history = self.persistence.load_history()
tests/test_workspace_orchestrator.sh:448:         self.persistence.save(result, stats)
tests/test_workspace_orchestrator.sh:449:         assert self.persistence.exists()
tests/test_workspace_orchestrator.sh:461:         self.persistence.save(result, stats)
```

Matches: 259

### Term: `identity`

```text
.ai/reports/inspect-20260807.json:4503:       "path": "lib/python/runtime/identity.py",
.ai/runtime/logs/runtime_periodic_20260803_125834.json:4:   "identity": {
.ai/runtime/logs/runtime_periodic_20260803_125835.json:4:   "identity": {
.ai/runtime/logs/runtime_periodic_20260803_130455.json:4:   "identity": {
.ai/runtime/logs/runtime_periodic_20260803_130456.json:4:   "identity": {
artifacts/engineering-project.json:782:         "title": "Review lib/python/runtime/identity.py",
artifacts/engineering-project.json:783:         "body": "# Review lib/python/runtime/identity.py\n\n## Priority\nMEDIUM\n\n## Objective\nSemantic review of module.\n\n## Affected Modules\n- lib/python/runtime/identity.py\n\n## Implementation Checklist\n- [ ] Analyse current implementation\n- [ ] Implement required changes\n- [ ] Execute validation\n- [ ] Perform engineering review\n\n## Acceptance Criteria\n- [ ] Implementation completed\n- [ ] Validation passes\n- [ ] No regression introduced\n- [ ] Documentation updated",
lib/python/ai_cto_scanner/report.py:277:             ("OwnerControl", "Owner Readiness", "Implement owner identity and permission layer"),
lib/python/engineering_workspace/models.py:113:     identity: WorkspaceIdentity
lib/python/engineering_workspace/workspace.py:32:     def identity(self) -> Any:
lib/python/runtime/bootstrap.py:13:     5. Initialize Runtime Identity
lib/python/runtime/bootstrap.py:33: from lib.python.runtime.identity import RuntimeIdentity
lib/python/runtime/bootstrap.py:67:         self.identity: Optional[RuntimeIdentity] = None
lib/python/runtime/bootstrap.py:129:         # Step 6 — Runtime Identity
lib/python/runtime/bootstrap.py:174:         self.identity.lifecycle_phase = LifecyclePhase.READY.value
lib/python/runtime/bootstrap.py:180:         logger.info("Bootstrap: Runtime READY — %s", self.identity.runtime_id)
lib/python/runtime/bootstrap.py:219:         self.identity = RuntimeIdentity.create()
lib/python/runtime/bootstrap.py:221:             "Bootstrap: Runtime identity created — id=%s version=%s",
lib/python/runtime/bootstrap.py:222:             self.identity.runtime_id,
lib/python/runtime/bootstrap.py:223:             self.identity.runtime_version,
lib/python/runtime/bootstrap.py:252:         self.metrics.set_gauge("runtime_id", self.identity.runtime_id)
lib/python/runtime/bootstrap.py:253:         self.metrics.set_gauge("runtime_version", self.identity.runtime_version)
lib/python/runtime/bootstrap.py:506:         self.identity.lifecycle_phase = LifecyclePhase.RUNNING.value
lib/python/runtime/bootstrap.py:524:         self.identity.lifecycle_phase = LifecyclePhase.SHUTDOWN.value
lib/python/runtime/bootstrap.py:578:             identity=self.identity,
lib/python/runtime/bootstrap.py:592:             identity=self.identity,
lib/python/runtime/bootstrap.py:608:             identity=self.identity,
lib/python/runtime/bootstrap.py:634:             "runtime_id": self.identity.runtime_id,
lib/python/runtime/bootstrap.py:635:             "lifecycle_phase": self.identity.lifecycle_phase,
lib/python/runtime/bootstrap.py:650:             identity=self.identity,
lib/python/runtime/diagnostics.py:61:         identity: Any,
lib/python/runtime/diagnostics.py:75:             "runtime_id": identity.runtime_id,
lib/python/runtime/diagnostics.py:77:             "lifecycle_phase": identity.lifecycle_phase,
lib/python/runtime/diagnostics.py:124:             "identity": identity.to_dict(),
lib/python/runtime/identity.py:2: CORE-021 — Runtime Identity
lib/python/runtime/identity.py:3: CANON-055 §8 — Runtime Identity
lib/python/runtime/identity.py:17:     """Immutable identity for a Runtime instance."""
lib/python/runtime/identity.py:32:         """Create a new Runtime Identity from the environment."""
lib/python/runtime/railway.py:7: - Logs deployment identity
lib/python/runtime/railway.py:66:     """Log Railway deployment identity at startup."""
lib/python/runtime/reports.py:30:         identity: Optional[Any] = None,
lib/python/runtime/reports.py:46:         if identity:
lib/python/runtime/reports.py:47:             report["identity"] = identity.to_dict()
lib/python/runtime/reports.py:88:         identity = report.get("identity", {})
lib/python/runtime/reports.py:89:         if identity:
lib/python/runtime/reports.py:90:             lines.append(f"Runtime ID:   {identity.get('runtime_id', 'unknown')}")
lib/python/runtime/reports.py:91:             lines.append(f"Version:      {identity.get('runtime_version', 'unknown')}")
lib/python/runtime/reports.py:92:             lines.append(f"Deployment:   {identity.get('deployment_id', 'unknown')}")
lib/python/runtime/reports.py:93:             lines.append(f"Phase:        {identity.get('lifecycle_phase', 'unknown')}")
lib/python/semantic_repository_intelligence/persistence.py:25:     - The repository identity and analysis timestamp
lib/python/workspace_index/models.py:77:     # Repository identity
lib/python/workspace_orchestrator/models.py:70:     Combines identity, tracking state, intelligence outputs, and cross-repo
lib/python/workspace_orchestrator/models.py:74:     # Identity
lib/python/workspace_orchestrator/persistence.py:7:   workspace.json          workspace identity and metadata
tests/test_runtime_bootstrap.sh:21: assert rt.identity is not None, "identity must be set"
tests/test_runtime_bootstrap.sh:51: # --- Identity has required fields ---
tests/test_runtime_bootstrap.sh:52: identity_dict = rt.identity.to_dict()
tests/test_runtime_bootstrap.sh:54:     assert identity_dict[field], f"Missing identity field: {field}"
tests/test_runtime_regression.sh:19: from lib.python.runtime.identity import RuntimeIdentity
```

Matches: 59

### Term: `lifecycle`

```text
.ai/reports/inspect-20260807.json:4573:       "path": "lib/python/runtime/lifecycle.py",
.ai/runtime/logs/runtime_periodic_20260803_125834.json:16:   "lifecycle": {
.ai/runtime/logs/runtime_periodic_20260803_125835.json:16:   "lifecycle": {
.ai/runtime/logs/runtime_periodic_20260803_130455.json:16:   "lifecycle": {
.ai/runtime/logs/runtime_periodic_20260803_130456.json:16:   "lifecycle": {
artifacts/engineering-project.json:806:         "title": "Review lib/python/runtime/lifecycle.py",
artifacts/engineering-project.json:807:         "body": "# Review lib/python/runtime/lifecycle.py\n\n## Priority\nMEDIUM\n\n## Objective\nSemantic review of module.\n\n## Affected Modules\n- lib/python/runtime/lifecycle.py\n\n## Implementation Checklist\n- [ ] Analyse current implementation\n- [ ] Implement required changes\n- [ ] Execute validation\n- [ ] Perform engineering review\n\n## Acceptance Criteria\n- [ ] Implementation completed\n- [ ] Validation passes\n- [ ] No regression introduced\n- [ ] Documentation updated",
lib/python/ai_cto_scanner/report.py:178:                 "Register AI CTO lifecycle hooks at startup",
lib/python/ai_cto_scanner/report.py:274:             ("Runtime", "Runtime Readiness", "Establish startup and lifecycle management"),
lib/python/canonical_entities/models.py:45:     """Canonical lifecycle states."""
lib/python/cdm_engine/engine.py:30: # Canonical document lifecycle states per CDM-003
lib/python/cdm_engine/engine.py:308:             warnings.append(f"CDM-V003: Status '{doc.status}' is not a standard lifecycle state")
lib/python/css_engine/engine.py:272:                 message=f"Status '{record.status}' is not a valid canonical lifecycle status",
lib/python/engineering_engine/repository_audit.py:41:             "purpose": "continuous runtime platform, HTTP/API, scheduler, lifecycle, recovery, secrets, metrics, integrations",
lib/python/engineering_workspace/service.py:8: Defines the canonical lifecycle for every Engineering Workspace service.
lib/python/epistemic/transformation.py:2: Transformation Lifecycle v1
lib/python/epistemic/transformation.py:4: The first executable lifecycle for a transformation.
lib/python/epistemic/transformation.py:95:     lifecycle = TransformationLifecycle()
lib/python/epistemic/transformation.py:97:     tr = lifecycle.begin(
lib/python/epistemic/transformation.py:99:         "Create the first executable lifecycle."
lib/python/epistemic/transformation.py:103:     lifecycle.complete(tr)
lib/python/runtime/bootstrap.py:38: from lib.python.runtime.lifecycle import LifecycleManager, LifecyclePhase
lib/python/runtime/bootstrap.py:71:         self.lifecycle: Optional[LifecycleManager] = None
lib/python/runtime/bootstrap.py:116:         # Step 2 — Initialize lifecycle manager early (tracks all phases)
lib/python/runtime/bootstrap.py:117:         self.lifecycle = LifecycleManager()
lib/python/runtime/bootstrap.py:133:         self.lifecycle.transition(LifecyclePhase.INITIALIZATION)
lib/python/runtime/bootstrap.py:138:         self.lifecycle.transition(LifecyclePhase.ENGINE_REGISTRATION)
lib/python/runtime/bootstrap.py:143:         self.lifecycle.transition(LifecyclePhase.SERVICE_REGISTRATION)
lib/python/runtime/bootstrap.py:168:         self.lifecycle.transition(LifecyclePhase.HEALTH_VERIFICATION)
lib/python/runtime/bootstrap.py:172:         self.lifecycle.transition(LifecyclePhase.READY)
lib/python/runtime/bootstrap.py:194:         self.lifecycle.transition(LifecyclePhase.CONFIGURATION)
lib/python/runtime/bootstrap.py:204:         self.lifecycle.transition(LifecyclePhase.DEPENDENCY_VALIDATION)
lib/python/runtime/bootstrap.py:205:         self.lifecycle.transition(LifecyclePhase.DISCOVERY)
lib/python/runtime/bootstrap.py:505:         self.lifecycle.transition(LifecyclePhase.RUNNING)
lib/python/runtime/bootstrap.py:523:         self.lifecycle.transition(LifecyclePhase.SHUTDOWN)
lib/python/runtime/bootstrap.py:539:         self.lifecycle.transition(LifecyclePhase.PERSISTENCE)
lib/python/runtime/bootstrap.py:542:         self.lifecycle.transition(LifecyclePhase.TERMINATION)
lib/python/runtime/bootstrap.py:579:             lifecycle=self.lifecycle,
lib/python/runtime/bootstrap.py:593:             lifecycle=self.lifecycle,
lib/python/runtime/bootstrap.py:609:             lifecycle=self.lifecycle,
lib/python/runtime/bootstrap.py:618:         self.lifecycle.transition(LifecyclePhase.MAINTENANCE)
lib/python/runtime/bootstrap.py:651:             lifecycle=self.lifecycle,
lib/python/runtime/diagnostics.py:62:         lifecycle: Any,
lib/python/runtime/diagnostics.py:119:             "lifecycle": lifecycle.to_dict(),
lib/python/runtime/event_loop.py:3: CANON-057 — Continuous Runtime Lifecycle
lib/python/runtime/interfaces/http_server.py:258:     # Lifecycle
lib/python/runtime/lifecycle.py:2: CORE-021 — Runtime Lifecycle Manager
lib/python/runtime/lifecycle.py:3: CANON-055 §6 — Runtime Lifecycle
lib/python/runtime/lifecycle.py:5: Manages the canonical lifecycle phases of the Runtime:
lib/python/runtime/lifecycle.py:12: The Runtime shall never skip lifecycle phases.
lib/python/runtime/lifecycle.py:53:     Manages lifecycle phase transitions and registered phase listeners.
lib/python/runtime/reports.py:31:         lifecycle: Optional[Any] = None,
lib/python/runtime/reports.py:48:         if lifecycle:
lib/python/runtime/reports.py:49:             report["lifecycle"] = lifecycle.to_dict()
lib/python/runtime/state.py:2: Runtime public state tracking for product-facing lifecycle visibility.
lib/python/self_improvement_engine/engine.py:104:     Coordinates the full improvement lifecycle by consuming all CORE
lib/python/self_improvement_engine/generators.py:206:                         "as part of the execution lifecycle."
lib/python/semantic_repository_intelligence/injection_point_analyzer.py:79:     ("hook", "Lifecycle Hook",
lib/python/workspace_orchestrator/state_manager.py:40:     # Lifecycle
tests/test_runtime_acceptance.sh:19: from lib.python.runtime.lifecycle import LifecyclePhase
tests/test_runtime_acceptance.sh:52: check("AC-3: Runtime survives restart", rt2.lifecycle.is_running())
tests/test_runtime_acceptance.sh:125: check("AC-11f: Graceful shutdown completes", rt2.lifecycle.is_shutdown())
tests/test_runtime_bootstrap.sh:15: from lib.python.runtime.lifecycle import LifecyclePhase
tests/test_runtime_bootstrap.sh:25: assert rt.lifecycle is not None, "lifecycle must be set"
tests/test_runtime_bootstrap.sh:43: # --- Lifecycle is in READY state after bootstrap ---
tests/test_runtime_bootstrap.sh:44: assert rt.lifecycle.is_ready(), f"Expected READY, got {rt.lifecycle.current_phase}"
tests/test_runtime_bootstrap.sh:47: history = rt.lifecycle.to_dict()["phase_history"]
tests/test_runtime_lifecycle.sh:2: # CORE-021 — Runtime Lifecycle Tests
tests/test_runtime_lifecycle.sh:3: # Tests lifecycle phase transitions.
tests/test_runtime_lifecycle.sh:10: from lib.python.runtime.lifecycle import LifecycleManager, LifecyclePhase
tests/test_runtime_lifecycle.sh:39: # --- Lifecycle listeners fire on transition ---
tests/test_runtime_lifecycle.sh:51: print("Lifecycle tests PASSED")
tests/test_runtime_regression.sh:22: from lib.python.runtime.lifecycle import LifecycleManager
```

Matches: 73

### Term: `retention`

```text
NO MATCHES
```

Matches: 0

### Term: `forgetting`

```text
NO MATCHES
```

Matches: 0

### Term: `protection`

```text
NO MATCHES
```

Matches: 0

## 6. Python Structural Index

### `.ai/backups/core021a002/test_knowledge_engine_v2.py`

PARSE ERROR: invalid syntax (<unknown>, line 4)

### `.ai/backups/core021a002/test_repository_engine_v2.py`

PARSE ERROR: invalid syntax (<unknown>, line 4)

### `lib/python/agent_runtime/base.py`

Classes:

- `BaseAgent`

Imports:

- `abc`

### `lib/python/agent_runtime/models.py`

Classes:

- `AgentContext`
- `AgentResult`

Imports:

- `dataclasses`
- `typing`

### `lib/python/agent_runtime/registry.py`

Functions:

- `build_runtime`

Imports:

- `python.agent_runtime.runtime`
- `python.agents.ai_cto_scanner_agent`
- `python.agents.development_agent`

### `lib/python/agent_runtime/runtime.py`

Classes:

- `AgentRuntime`

### `lib/python/agents/ai_cto_scanner_agent.py`

Classes:

- `AICTOScannerAgent`

Imports:

- `python.agent_runtime.base`
- `python.agent_runtime.models`
- `python.ai_cto_scanner.engine`

### `lib/python/agents/development_agent.py`

Classes:

- `DevelopmentAgent`

Imports:

- `pathlib`
- `python.agent_runtime.base`
- `python.agent_runtime.models`
- `python.agents.development_report`
- `python.autonomous_planner.engine`
- `python.batch_generator.engine`
- `python.canonical_audit.engine`
- `python.dependency_engine.engine`
- `python.execution_coordinator.engine`
- `python.execution_engine.engine`
- `python.github_materialization.engine`
- `python.knowledge_graph_v2.engine`
- `python.planning_engine.engine`
- `python.profiler.engine`
- `python.recommendation_engine.engine`
- `python.repository_engine.engine`
- `python.repository_inspector_v2.engine`
- `python.review_agent.engine`
- `python.semantic_engine.engine`
- `python.validation_engine.engine`
- `python.workspace_index`
- `python.workspace_manager.engine`

### `lib/python/agents/development_report.py`

Classes:

- `DevelopmentReport`

Imports:

- `pathlib`

### `lib/python/agents/repository_inspector_agent.py`

Classes:

- `RepositoryInspectorAgent`

Imports:

- `python.agent_runtime.base`
- `python.agent_runtime.models`
- `python.repository_inspector_v2.engine`

### `lib/python/ai_control_center/application.py`

Classes:

- `AIControlCenter`

Imports:

- `__future__`
- `ai_control_center.kernel`
- `ai_control_center.providers`
- `pathlib`

### `lib/python/ai_control_center/kernel.py`

Classes:

- `KernelContext`
- `EngineeringKernel`

Imports:

- `__future__`
- `dataclasses`
- `typing`

### `lib/python/ai_control_center/panels/repository/panel.py`

Classes:

- `RepositoryPanel`

Imports:

- `__future__`
- `dataclasses`
- `pathlib`

### `lib/python/ai_control_center/providers/base.py`

Classes:

- `Provider`

Imports:

- `__future__`
- `abc`
- `typing`

### `lib/python/ai_control_center/providers/local_repository.py`

Classes:

- `LocalRepositoryProvider`

Imports:

- `__future__`
- `base`
- `pathlib`
- `repository_engine`
- `typing`

### `lib/python/ai_cto_scanner/detectors.py`

Classes:

- `ComponentMatch`
- `DetectionResult`
- `BaseDetector`
- `TelegramDetector`
- `OwnerControlDetector`
- `RuntimeDetector`
- `StateDetector`
- `ConfigurationDetector`
- `CanonicalDetector`
- `ProjectMemoryDetector`

Imports:

- `pathlib`
- `re`

### `lib/python/ai_cto_scanner/engine.py`

Classes:

- `AICTOScannerEngine`

Imports:

- `detectors`
- `pathlib`
- `python.batch_planner`
- `python.canonical_intelligence.engine`
- `python.canonical_repository`
- `python.compliance_engine`
- `python.coverage_engine`
- `python.drift_engine`
- `python.knowledge_graph`
- `python.reporting_engine`
- `python.semantic_matching`
- `python.semantic_repository_intelligence`
- `python.workspace_index`
- `report`
- `scoring`

### `lib/python/ai_cto_scanner/report.py`

Classes:

- `AICTOReportGenerator`

Imports:

- `datetime`
- `pathlib`

### `lib/python/ai_cto_scanner/scoring.py`

Classes:

- `ReadinessScorer`

### `lib/python/ai_platform/adapters.py`

Classes:

- `ProviderDescriptor`
- `StaticProviderAdapter`

Functions:

- `builtin_adapters`

Imports:

- `__future__`
- `dataclasses`
- `os`
- `time`
- `typing`

### `lib/python/ai_platform/context_builder.py`

Classes:

- `AIContextBuilder`

Imports:

- `__future__`
- `json`
- `pathlib`
- `python.context_synchronization_engine.engine`
- `python.repository_engine.engine`
- `python.repository_engine.serializer`
- `typing`

### `lib/python/ai_platform/model_manager.py`

Classes:

- `ModelManager`

Imports:

- `__future__`
- `settings`
- `typing`

### `lib/python/ai_platform/pipeline.py`

Classes:

- `AIRequestPipeline`

Imports:

- `__future__`
- `context_builder`
- `datetime`
- `model_manager`
- `registry`
- `typing`

### `lib/python/ai_platform/prompt_library.py`

Classes:

- `PromptLibrary`

Imports:

- `__future__`
- `typing`

### `lib/python/ai_platform/registry.py`

Classes:

- `ProviderRegistry`

Imports:

- `__future__`
- `adapters`
- `datetime`
- `typing`

### `lib/python/ai_platform/service.py`

Classes:

- `AIPlatformService`

Imports:

- `__future__`
- `adapters`
- `collections`
- `context_builder`
- `model_manager`
- `pipeline`
- `prompt_library`
- `registry`
- `sessions`
- `settings`
- `typing`

### `lib/python/ai_platform/sessions.py`

Classes:

- `AISessionEngine`

Imports:

- `__future__`
- `datetime`
- `json`
- `pathlib`
- `typing`
- `uuid`

### `lib/python/ai_platform/settings.py`

Classes:

- `AISettingsStore`

Functions:

- `masked_provider_settings`

Imports:

- `__future__`
- `hashlib`
- `json`
- `pathlib`
- `typing`

### `lib/python/autonomous_execution_engine/engine.py`

Classes:

- `ExecutionScheduler`
- `ExecutionQueue`
- `ExecutionCoordinator`
- `ArtifactManager`
- `AutonomousExecutionEngine`

Functions:

- `_utcnow`
- `_execution_id`
- `_ms`
- `_stage_result`

Imports:

- `datetime`
- `evidence`
- `hashlib`
- `logger`
- `models`
- `pathlib`
- `persistence`
- `policy`
- `report`
- `rollback`
- `time`
- `typing`
- `validator`

### `lib/python/autonomous_execution_engine/evidence.py`

Classes:

- `ExecutionEvidenceCollector`
- `ExecutionSnapshot`

Functions:

- `_utcnow`

Imports:

- `datetime`
- `hashlib`
- `typing`

### `lib/python/autonomous_execution_engine/logger.py`

Classes:

- `ExecutionLogger`
- `ExecutionReporter`

Functions:

- `_utcnow`

Imports:

- `datetime`
- `typing`

### `lib/python/autonomous_execution_engine/models.py`

Classes:

- `ExecutionContext`
- `ExecutionStageResult`
- `ValidationResult`
- `ExecutionMetrics`
- `ExecutionSnapshot`
- `ExecutionResult`
- `ExecutionHistoryEntry`
- `ExecutionHistory`

Imports:

- `dataclasses`
- `typing`

### `lib/python/autonomous_execution_engine/persistence.py`

Classes:

- `ExecutionPersistence`

Imports:

- `json`
- `os`
- `pathlib`
- `tempfile`
- `typing`

### `lib/python/autonomous_execution_engine/policy.py`

Classes:

- `ExecutionPolicy`
- `ExecutionPermissions`
- `ExecutionApproval`

Imports:

- `models`
- `typing`

### `lib/python/autonomous_execution_engine/report.py`

Classes:

- `ExecutionReportGenerator`

Functions:

- `_fmt_list`
- `_score_bar`

Imports:

- `pathlib`
- `typing`

### `lib/python/autonomous_execution_engine/rollback.py`

Classes:

- `ExecutionRollbackPlanner`

Imports:

- `typing`

### `lib/python/autonomous_execution_engine/validator.py`

Classes:

- `ExecutionValidator`

Imports:

- `models`
- `time`
- `typing`

### `lib/python/autonomous_planner/engine.py`

Classes:

- `AutonomousPlanner`

### `lib/python/autonomous_planning_engine/batch_planner.py`

Classes:

- `BatchPlanner`

Functions:

- `_is_set`
- `_batch_sort_key`
- `_load_batch_status`

Imports:

- `models`
- `pathlib`
- `re`
- `typing`

### `lib/python/autonomous_planning_engine/decision_engine.py`

Classes:

- `CoreRegistry`
- `PlanningDecisionEngine`

Functions:

- `_is_set`
- `_core_sort_key`

Imports:

- `models`
- `pathlib`
- `re`
- `typing`

### `lib/python/autonomous_planning_engine/dependency_resolver.py`

Classes:

- `DependencyGraph`
- `DependencyResolver`

Functions:

- `_scan_package_core_id`
- `_build_package_core_map`
- `_extract_imports`

Imports:

- `ast`
- `pathlib`
- `re`
- `typing`

### `lib/python/autonomous_planning_engine/engine.py`

Classes:

- `AutonomousPlanningEngine`

Functions:

- `_utcnow`
- `_planning_id`

Imports:

- `batch_planner`
- `datetime`
- `decision_engine`
- `dependency_resolver`
- `execution_queue`
- `hashlib`
- `issue_planner`
- `json`
- `milestone_planner`
- `models`
- `pathlib`
- `persistence`
- `pr_planner`
- `priority_optimizer`
- `python.development_state_engine`
- `python.executive_briefing_engine`
- `report`
- `roadmap_planner`
- `typing`

### `lib/python/autonomous_planning_engine/execution_queue.py`

Classes:

- `ExecutionQueueBuilder`

Imports:

- `dependency_resolver`
- `models`
- `priority_optimizer`
- `typing`

### `lib/python/autonomous_planning_engine/issue_planner.py`

Classes:

- `IssuePlanner`

Functions:

- `_is_set`

Imports:

- `models`
- `typing`

### `lib/python/autonomous_planning_engine/milestone_planner.py`

Classes:

- `MilestonePlanner`

Functions:

- `_is_set`

Imports:

- `models`
- `typing`

### `lib/python/autonomous_planning_engine/models.py`

Classes:

- `PlanningEntry`
- `ExecutionQueue`
- `RoadmapProgress`
- `NextActions`
- `PlanningResult`

Imports:

- `dataclasses`
- `typing`

### `lib/python/autonomous_planning_engine/persistence.py`

Classes:

- `PlanningPersistence`

Imports:

- `json`
- `os`
- `pathlib`
- `tempfile`
- `typing`

### `lib/python/autonomous_planning_engine/pr_planner.py`

Classes:

- `PullRequestPlanner`

Functions:

- `_is_set`

Imports:

- `models`
- `typing`

### `lib/python/autonomous_planning_engine/priority_optimizer.py`

Classes:

- `PriorityOptimizer`

Functions:

- `_is_set`

Imports:

- `models`
- `typing`

### `lib/python/autonomous_planning_engine/report.py`

Classes:

- `PlanningReportGenerator`

Functions:

- `_fmt_list`
- `_fmt_entry`

Imports:

- `models`
- `pathlib`
- `typing`

### `lib/python/autonomous_planning_engine/roadmap_planner.py`

Classes:

- `RoadmapPlanner`

Functions:

- `_estimate_effort`

Imports:

- `models`
- `typing`

### `lib/python/batch_generator/engine.py`

Classes:

- `BatchGenerator`

Imports:

- `python.common.models`

### `lib/python/batch_planner/planner.py`

Classes:

- `BatchPlanner`

Imports:

- `python.canonical_entities`

### `lib/python/canonical_audit/engine.py`

Classes:

- `CanonicalAuditEngine`

Imports:

- `pathlib`
- `python.evidence_engine.engine`

### `lib/python/canonical_entities/models.py`

Classes:

- `NodeType`
- `EdgeType`
- `LifecycleStatus`
- `CoverageState`
- `ComplianceState`
- `DriftSeverity`
- `Priority`
- `CanonicalNode`
- `CanonicalEdge`
- `CanonicalSection`
- `CanonicalDocument`
- `SemanticMatch`
- `CoverageMetric`
- `ComplianceMetric`
- `DriftFinding`
- `PlanBatch`

Imports:

- `dataclasses`
- `enum`
- `typing`

### `lib/python/canonical_entities/uem.py`

Classes:

- `EngObjectType`
- `EngRelationType`
- `EngVisibility`
- `EngObject`
- `EngRelationship`
- `UniversalEngineeringModel`
- `UemBuilder`

Imports:

- `__future__`
- `dataclasses`
- `enum`
- `typing`

### `lib/python/canonical_intelligence/engine.py`

Classes:

- `CanonicalIntelligenceEngine`

Imports:

- `pathlib`
- `python.batch_planner`
- `python.canonical_repository`
- `python.compliance_engine`
- `python.coverage_engine`
- `python.drift_engine`
- `python.knowledge_graph`
- `python.reporting_engine`
- `python.semantic_matching`
- `typing`

### `lib/python/canonical_parser/ast_nodes.py`

Classes:

- `AstNodeType`
- `AstNode`
- `ScalarValueNode`
- `ListValueNode`
- `MapEntryNode`
- `MapValueNode`
- `AttributeNode`
- `EntityNode`
- `RelationshipNode`
- `HeaderFieldNode`
- `DocumentNode`

Imports:

- `__future__`
- `dataclasses`
- `enum`
- `lexer`
- `typing`

### `lib/python/canonical_parser/csl_parser.py`

Classes:

- `CslParser`

Imports:

- `__future__`
- `ast_nodes`
- `diagnostics`
- `lexer`
- `typing`

### `lib/python/canonical_parser/diagnostics.py`

Classes:

- `DiagnosticSeverity`
- `DiagnosticCategory`
- `Diagnostic`
- `DiagnosticCollection`

Imports:

- `__future__`
- `dataclasses`
- `enum`
- `lexer`
- `typing`

### `lib/python/canonical_parser/lexer.py`

Classes:

- `TokenType`
- `SourceLocation`
- `Token`
- `CslLexer`

Imports:

- `__future__`
- `dataclasses`
- `enum`
- `typing`

### `lib/python/canonical_parser/parser.py`

Classes:

- `CanonicalParser`

Imports:

- `pathlib`
- `python.canonical_entities`
- `re`

### `lib/python/canonical_parser/semantic_analyzer.py`

Classes:

- `SemanticAnnotation`
- `SemanticResult`
- `SemanticAnalyzer`

Imports:

- `__future__`
- `ast_nodes`
- `dataclasses`
- `diagnostics`
- `lexer`
- `typing`

### `lib/python/canonical_repository/repository.py`

Classes:

- `CanonicalRepository`

Imports:

- `pathlib`
- `python.canonical_parser`

### `lib/python/cdm_engine/engine.py`

Classes:

- `CdmSection`
- `CdmTraceabilityLink`
- `CdmDocumentObject`
- `CdmValidationResult`
- `CdmEngine`

Imports:

- `__future__`
- `dataclasses`
- `pathlib`
- `re`
- `typing`

### `lib/python/cli/engineering.py`

Functions:

- `engineering_audit`
- `engineering_gap`
- `engineering_plan`
- `engineering_execute`
- `engineering_validate`
- `engineering_build`
- `analyse`

Imports:

- `lib.python.engineering_engine.engineering_report_engine`
- `lib.python.engineering_engine.engineering_workflow_engine`
- `lib.python.engineering_engine.execution_engine`
- `lib.python.engineering_engine.gap_analysis`
- `lib.python.engineering_engine.pipeline`
- `lib.python.engineering_engine.planning_engine`
- `lib.python.engineering_engine.repository_audit`
- `lib.python.engineering_engine.validation_engine`
- `pathlib`
- `sys`

### `lib/python/cli/main.py`

Functions:

- `cmd_inventory`
- `cmd_dependencies`
- `cmd_validate`
- `cmd_plan`
- `cmd_agent`

Imports:

- `argparse`
- `json`
- `os`
- `pathlib`
- `python.agent_runtime.models`
- `python.agent_runtime.registry`
- `python.dependency_engine.engine`
- `python.planning_engine.engine`
- `python.repository_engine.engine`
- `python.validation_engine.engine`
- `sys`

### `lib/python/common/models.py`

Classes:

- `BatchStep`
- `Batch`

Imports:

- `dataclasses`
- `typing`

### `lib/python/compliance_engine/engine.py`

Classes:

- `ComplianceEngine`

Imports:

- `pathlib`
- `python.canonical_entities`

### `lib/python/context_synchronization_engine/engine.py`

Classes:

- `ContextCache`
- `GitContextProvider`
- `GitHubContextProvider`
- `DevelopmentContextProvider`
- `WorkspaceContextProvider`
- `ContextResolver`
- `ContextValidator`
- `SynchronizationReportGenerator`
- `SynchronizationCoordinator`
- `ContextSynchronizationEngine`

Functions:

- `_is_set`
- `_clean_scalar`
- `_compact_list`

Imports:

- `dataclasses`
- `datetime`
- `json`
- `models`
- `pathlib`
- `persistence`
- `python.development_state_engine`
- `re`
- `subprocess`
- `typing`

### `lib/python/context_synchronization_engine/models.py`

Classes:

- `SynchronizationFinding`
- `SynchronizationReport`
- `EngineeringContextSection`
- `EngineeringContext`

Functions:

- `_to_tuple`
- `_normalize_mapping`

Imports:

- `dataclasses`
- `typing`

### `lib/python/context_synchronization_engine/persistence.py`

Classes:

- `ContextPersistence`

Imports:

- `json`
- `os`
- `pathlib`
- `tempfile`
- `typing`

### `lib/python/coverage_engine/engine.py`

Classes:

- `CoverageEngine`

Imports:

- `pathlib`
- `python.canonical_entities`

### `lib/python/csl_engine/engine.py`

Classes:

- `CslExecutionResult`
- `CslCompileResult`
- `CslEngine`

Imports:

- `__future__`
- `dataclasses`
- `pathlib`
- `python.canonical_parser`
- `python.canonical_parser.ast_nodes`
- `typing`

### `lib/python/css_engine/engine.py`

Classes:

- `CSSStandardRecord`
- `CSSDiagnostic`
- `CSSValidationResult`
- `CSSEngine`

Imports:

- `__future__`
- `dataclasses`
- `pathlib`
- `re`
- `typing`

### `lib/python/dashboard/server.py`

Classes:

- `_DashboardRequestHandler`
- `DashboardHttpServer`

Functions:

- `serve_dashboard`

Imports:

- `__future__`
- `http.server`
- `json`
- `service`
- `threading`
- `typing`
- `urllib.parse`
- `webbrowser`

### `lib/python/dashboard/service.py`

Classes:

- `CapabilityDefinition`
- `EngineeringDashboardService`

Imports:

- `__future__`
- `dataclasses`
- `datetime`
- `html`
- `json`
- `os`
- `pathlib`
- `python.ai_platform`
- `python.context_synchronization_engine`
- `python.context_synchronization_engine.engine`
- `python.repository_engine.engine`
- `python.repository_engine.serializer`
- `python.workspace_orchestrator`
- `python.workspace_orchestrator.persistence`
- `time`
- `typing`

### `lib/python/dependency_engine/engine.py`

Classes:

- `DependencyEngine`

Imports:

- `models`
- `os`
- `pathlib`

### `lib/python/dependency_engine/exporter.py`

Classes:

- `DependencyExporter`

Imports:

- `json`
- `pathlib`

### `lib/python/dependency_engine/models.py`

Classes:

- `Dependency`

Imports:

- `dataclasses`

### `lib/python/development_state_engine/models.py`

Classes:

- `WorkspaceState`
- `RepositoryState`
- `ExecutionState`
- `PlanningState`
- `ReviewState`
- `OwnerState`
- `TelegramState`
- `SnapshotMetadata`
- `IntegrityReport`
- `DevelopmentState`

Functions:

- `_require_non_empty_string`
- `_coerce_tuple_of_strings`
- `_validate_tuple_of_strings`
- `_require_percentage`

Imports:

- `dataclasses`
- `typing`

### `lib/python/development_state_engine/repository.py`

Classes:

- `DevelopmentStateRepository`

Imports:

- `hashlib`
- `json`
- `models`
- `os`
- `pathlib`
- `re`
- `tempfile`
- `typing`

### `lib/python/development_state_engine/runtime.py`

Classes:

- `DevelopmentStateSnapshot`
- `DevelopmentStateEventBus`
- `DevelopmentStateManager`
- `DevelopmentStateEngine`

Imports:

- `dataclasses`
- `datetime`
- `hashlib`
- `json`
- `models`
- `os`
- `pathlib`
- `python.ai_cto_scanner`
- `python.canonical_intelligence`
- `python.repository_engine.engine`
- `python.semantic_repository_intelligence`
- `repository`
- `subprocess`
- `tempfile`
- `typing`

### `lib/python/development_validator/main.py`

Functions:

- `run`

Imports:

- `parser`
- `pathlib`
- `report`
- `rules`
- `sys`

### `lib/python/development_validator/parser.py`

Classes:

- `DevelopmentDocument`

Imports:

- `pathlib`

### `lib/python/development_validator/report.py`

Classes:

- `ValidationReport`

Imports:

- `json`

### `lib/python/development_validator/rules.py`

Classes:

- `Rule`
- `RequiredSectionRule`

### `lib/python/development_validator.py`

Functions:

- `validate`

Imports:

- `pathlib`
- `sys`

### `lib/python/discovery_engine/engine.py`

Classes:

- `DiscoveryEngine`

Imports:

- `pathlib`

### `lib/python/drift_engine/engine.py`

Classes:

- `DriftEngine`

Imports:

- `datetime`
- `pathlib`
- `python.canonical_entities`

### `lib/python/engineering_engine/acceptance_detector.py`

Classes:

- `AcceptanceDetector`

Imports:

- `__future__`

### `lib/python/engineering_engine/backlog_generator.py`

Classes:

- `BacklogGenerator`

Imports:

- `__future__`
- `lib.python.engineering_engine.batch_planner_engine`
- `lib.python.engineering_engine.engineering_task_engine`
- `lib.python.engineering_engine.github_issue_generator`
- `lib.python.engineering_engine.roadmap_engine`
- `pathlib`

### `lib/python/engineering_engine/batch_planner_engine.py`

Classes:

- `EngineeringBatch`
- `BatchPlannerEngine`

Imports:

- `__future__`
- `dataclasses`
- `lib.python.engineering_engine.engineering_task_engine`

### `lib/python/engineering_engine/build_engine.py`

Classes:

- `BuildEngine`

Imports:

- `__future__`
- `lib.python.engineering_engine.gap_analysis`
- `lib.python.engineering_engine.ip_generator`
- `lib.python.engineering_engine.repository_audit`
- `lib.python.engineering_engine.validation_engine`
- `pathlib`

### `lib/python/engineering_engine/canonical_reference_detector.py`

Classes:

- `CanonicalReferenceDetector`

Imports:

- `__future__`
- `pathlib`

### `lib/python/engineering_engine/capability_detector.py`

Classes:

- `CapabilityResult`
- `CapabilityDetector`

Imports:

- `__future__`
- `dataclasses`
- `pathlib`

### `lib/python/engineering_engine/compiler.py`

Classes:

- `CompilationResult`
- `EngineeringCompiler`

Imports:

- `__future__`
- `dataclasses`
- `generator_framework`
- `logging`
- `pathlib`
- `python.canonical_entities`
- `python.canonical_parser`
- `python.validation_engine`
- `typing`

### `lib/python/engineering_engine/deliverable_detector.py`

Classes:

- `DeliverableDetector`

Imports:

- `__future__`
- `pathlib`

### `lib/python/engineering_engine/dependency_graph.py`

Classes:

- `DependencyGraph`
- `DependencyGraphBuilder`

Imports:

- `__future__`
- `dataclasses`
- `lib.python.engineering_engine.import_resolver`
- `lib.python.engineering_engine.repository_model`
- `pathlib`

### `lib/python/engineering_engine/dependency_reasoning_engine.py`

Classes:

- `DependencyReasoningEngine`

Imports:

- `__future__`
- `collections`
- `lib.python.engineering_engine.semantic_entities`

### `lib/python/engineering_engine/dependency_rule_engine.py`

Classes:

- `DependencyResult`
- `DependencyRuleEngine`

Imports:

- `__future__`
- `dataclasses`
- `pathlib`

### `lib/python/engineering_engine/engineering_report_engine.py`

Classes:

- `EngineeringReportEngine`

Imports:

- `__future__`
- `lib.python.engineering_engine.engineering_workflow_engine`

### `lib/python/engineering_engine/engineering_task_engine.py`

Classes:

- `TaskPriority`
- `EngineeringTask`
- `EngineeringBacklog`
- `EngineeringTaskEngine`

Imports:

- `__future__`
- `dataclasses`
- `enum`
- `lib.python.engineering_engine.semantic_entities`
- `lib.python.engineering_engine.semantic_repository_builder`

### `lib/python/engineering_engine/engineering_workflow_engine.py`

Classes:

- `EngineeringWorkflowResult`
- `EngineeringWorkflowEngine`

Imports:

- `__future__`
- `dataclasses`
- `lib.python.engineering_engine.dependency_reasoning_engine`
- `lib.python.engineering_engine.execution_plan_engine`
- `lib.python.engineering_engine.impact_reasoning_engine`
- `lib.python.engineering_engine.recommendation_engine`
- `lib.python.engineering_engine.semantic_repository_builder`
- `lib.python.engineering_engine.validation_plan_engine`

### `lib/python/engineering_engine/execution_engine.py`

Classes:

- `ExecutionEngine`

Imports:

- `__future__`
- `lib.python.engineering_engine.execution_package_generator`
- `lib.python.engineering_engine.planning_engine`
- `pathlib`

### `lib/python/engineering_engine/execution_package_generator.py`

Classes:

- `ExecutionPackageGenerator`

Imports:

- `__future__`
- `datetime`
- `pathlib`

### `lib/python/engineering_engine/execution_plan_engine.py`

Classes:

- `ExecutionPlan`
- `ExecutionPlanEngine`

Imports:

- `__future__`
- `dataclasses`
- `lib.python.engineering_engine.recommendation_engine`

### `lib/python/engineering_engine/gap_analysis.py`

Classes:

- `GapItem`
- `GapAnalysis`

Imports:

- `__future__`
- `dataclasses`
- `datetime`
- `lib.python.engineering_engine.repository_audit`
- `pathlib`

### `lib/python/engineering_engine/generator_framework.py`

Classes:

- `ArtifactType`
- `GeneratorContext`
- `GeneratorArtifact`
- `ArtifactGenerator`
- `GeneratorRegistry`
- `GeneratorRunner`
- `UemStatisticsGenerator`

Functions:

- `default_registry`

Imports:

- `__future__`
- `abc`
- `dataclasses`
- `enum`
- `python.canonical_entities`
- `typing`

### `lib/python/engineering_engine/github_cli_client.py`

Classes:

- `GitHubCLIClient`

Imports:

- `__future__`
- `lib.python.engineering_engine.github_client`
- `lib.python.engineering_engine.github_publish_engine`
- `lib.python.engineering_engine.github_repository_resolver`

### `lib/python/engineering_engine/github_cli_state_provider.py`

Classes:

- `GitHubCLIStateProvider`

Imports:

- `__future__`
- `json`
- `lib.python.engineering_engine.github_repository_resolver`
- `lib.python.engineering_engine.github_state_provider`
- `subprocess`

### `lib/python/engineering_engine/github_client.py`

Classes:

- `GitHubClient`
- `GitHubDryRunClient`

Imports:

- `__future__`
- `abc`
- `lib.python.engineering_engine.github_publish_engine`

### `lib/python/engineering_engine/github_comparison_engine.py`

Classes:

- `ComparisonResult`
- `GitHubComparisonEngine`

Imports:

- `__future__`
- `dataclasses`
- `lib.python.engineering_engine.github_issue_generator`

### `lib/python/engineering_engine/github_issue_generator.py`

Classes:

- `GitHubIssue`
- `GitHubIssueGenerator`

Imports:

- `__future__`
- `dataclasses`
- `lib.python.engineering_engine.engineering_task_engine`

### `lib/python/engineering_engine/github_issue_state_provider.py`

Classes:

- `GitHubIssueState`
- `GitHubIssueStateProvider`

Imports:

- `__future__`
- `dataclasses`
- `json`
- `lib.python.engineering_engine.github_issue_generator`
- `lib.python.engineering_engine.github_repository_resolver`
- `subprocess`

### `lib/python/engineering_engine/github_milestone_generator.py`

Classes:

- `GitHubMilestone`
- `GitHubMilestoneGenerator`

Imports:

- `__future__`
- `dataclasses`
- `lib.python.engineering_engine.roadmap_engine`

### `lib/python/engineering_engine/github_project_planner.py`

Classes:

- `PlannedIssue`
- `GitHubProjectPlan`
- `GitHubProjectPlanner`

Imports:

- `__future__`
- `dataclasses`
- `lib.python.engineering_engine.batch_planner_engine`
- `lib.python.engineering_engine.engineering_task_engine`
- `lib.python.engineering_engine.github_issue_generator`
- `lib.python.engineering_engine.github_milestone_generator`

### `lib/python/engineering_engine/github_publish_engine.py`

Classes:

- `PublishOperation`
- `PublishPlan`
- `GitHubPublishEngine`

Imports:

- `__future__`
- `dataclasses`
- `lib.python.engineering_engine.github_project_planner`

### `lib/python/engineering_engine/github_publish_executor.py`

Classes:

- `GitHubPublishExecutor`

Imports:

- `__future__`
- `lib.python.engineering_engine.github_client`
- `lib.python.engineering_engine.github_publish_engine`

### `lib/python/engineering_engine/github_publish_script.py`

Classes:

- `GitHubPublishScript`

Imports:

- `__future__`
- `lib.python.engineering_engine.github_publish_engine`

### `lib/python/engineering_engine/github_real_client.py`

Classes:

- `GitHubRealClient`

Imports:

- `__future__`
- `lib.python.engineering_engine.github_client`
- `lib.python.engineering_engine.github_publish_engine`
- `lib.python.engineering_engine.github_repository_resolver`
- `subprocess`

### `lib/python/engineering_engine/github_repository_resolver.py`

Classes:

- `GitHubRepository`
- `GitHubRepositoryResolver`

Imports:

- `__future__`
- `dataclasses`
- `subprocess`

### `lib/python/engineering_engine/github_resume_engine.py`

Classes:

- `ResumePlan`
- `GitHubResumeEngine`

Imports:

- `__future__`
- `dataclasses`
- `lib.python.engineering_engine.github_publish_engine`
- `lib.python.engineering_engine.github_transaction_log`

### `lib/python/engineering_engine/github_state_provider.py`

Classes:

- `GitHubState`
- `GitHubStateProvider`
- `EmptyGitHubStateProvider`
- `InMemoryGitHubStateProvider`

Imports:

- `__future__`
- `abc`
- `dataclasses`

### `lib/python/engineering_engine/github_sync_engine.py`

Classes:

- `SyncAction`
- `SyncOperation`
- `SyncPlan`
- `GitHubSynchronizationEngine`

Imports:

- `__future__`
- `dataclasses`
- `enum`
- `lib.python.engineering_engine.github_project_planner`
- `lib.python.engineering_engine.github_state_provider`

### `lib/python/engineering_engine/github_sync_planner.py`

Classes:

- `PlannedSyncOperation`
- `PlannedSync`
- `GitHubSyncPlanner`

Imports:

- `__future__`
- `dataclasses`
- `lib.python.engineering_engine.github_cli_state_provider`
- `lib.python.engineering_engine.github_issue_state_provider`
- `lib.python.engineering_engine.github_project_planner`
- `lib.python.engineering_engine.github_sync_engine`

### `lib/python/engineering_engine/github_sync_strategy.py`

Classes:

- `SyncDecision`
- `SmartSyncPlan`
- `GitHubSyncStrategy`

Imports:

- `__future__`
- `dataclasses`
- `lib.python.engineering_engine.github_comparison_engine`
- `lib.python.engineering_engine.github_issue_state_provider`
- `lib.python.engineering_engine.github_project_planner`
- `lib.python.engineering_engine.github_state_provider`
- `lib.python.engineering_engine.github_sync_engine`

### `lib/python/engineering_engine/github_transaction_executor.py`

Classes:

- `GitHubTransactionalExecutor`

Imports:

- `__future__`
- `lib.python.engineering_engine.github_publish_engine`
- `lib.python.engineering_engine.github_real_client`
- `lib.python.engineering_engine.github_transaction_log`
- `pathlib`

### `lib/python/engineering_engine/github_transaction_log.py`

Classes:

- `TransactionRecord`
- `TransactionLog`
- `GitHubTransactionLogger`

Imports:

- `__future__`
- `dataclasses`
- `json`
- `pathlib`

### `lib/python/engineering_engine/impact_analysis.py`

Classes:

- `ImpactReport`
- `ImpactAnalysis`

Imports:

- `__future__`
- `dataclasses`
- `lib.python.engineering_engine.dependency_graph`

### `lib/python/engineering_engine/impact_reasoning_engine.py`

Classes:

- `ImpactReport`
- `ImpactReasoningEngine`

Imports:

- `__future__`
- `dataclasses`
- `lib.python.engineering_engine.dependency_reasoning_engine`

### `lib/python/engineering_engine/import_resolver.py`

Classes:

- `ImportResolver`

Imports:

- `__future__`
- `pathlib`

### `lib/python/engineering_engine/ip_generator.py`

Classes:

- `ImplementationPackageGenerator`

Imports:

- `__future__`
- `datetime`
- `lib.python.engineering_engine.markdown_renderer`
- `lib.python.engineering_engine.models`
- `pathlib`

### `lib/python/engineering_engine/knowledge_graph.py`

Classes:

- `KnowledgeGraph`
- `KnowledgeGraphBuilder`

Imports:

- `__future__`
- `dataclasses`
- `lib.python.engineering_engine.repository_model`

### `lib/python/engineering_engine/markdown_renderer.py`

Classes:

- `MarkdownRenderer`

Imports:

- `__future__`
- `datetime`
- `lib.python.engineering_engine.models`

### `lib/python/engineering_engine/models.py`

Classes:

- `EngineeringBatch`
- `ImplementationPackageModel`

Imports:

- `__future__`
- `dataclasses`

### `lib/python/engineering_engine/package_builder.py`

Classes:

- `PackageBuilder`

Imports:

- `__future__`
- `lib.python.engineering_engine.acceptance_detector`
- `lib.python.engineering_engine.canonical_reference_detector`
- `lib.python.engineering_engine.deliverable_detector`
- `lib.python.engineering_engine.knowledge_graph`
- `lib.python.engineering_engine.models`
- `lib.python.engineering_engine.repository_model`
- `lib.python.engineering_engine.scope_detector`
- `pathlib`

### `lib/python/engineering_engine/pipeline.py`

Classes:

- `EngineeringPipeline`

Imports:

- `__future__`
- `lib.python.engineering_engine.gap_analysis`
- `lib.python.engineering_engine.ip_generator`
- `lib.python.engineering_engine.planning_engine`
- `lib.python.engineering_engine.repository_audit`
- `lib.python.engineering_engine.review_engine`
- `lib.python.engineering_engine.validation_engine`
- `pathlib`

### `lib/python/engineering_engine/planning_engine.py`

Classes:

- `PlanningBatch`
- `PlanningEngine`

Imports:

- `__future__`
- `dataclasses`
- `lib.python.engineering_engine.gap_analysis`
- `pathlib`

### `lib/python/engineering_engine/project_exporter.py`

Classes:

- `ProjectExporter`

Imports:

- `__future__`
- `dataclasses`
- `json`
- `lib.python.engineering_engine.github_project_planner`
- `pathlib`

### `lib/python/engineering_engine/project_importer.py`

Classes:

- `ProjectImporter`

Imports:

- `__future__`
- `json`
- `lib.python.engineering_engine.github_issue_generator`
- `lib.python.engineering_engine.github_milestone_generator`
- `lib.python.engineering_engine.github_project_planner`
- `pathlib`

### `lib/python/engineering_engine/recommendation_engine.py`

Classes:

- `RecommendationReport`
- `RecommendationEngine`

Imports:

- `__future__`
- `dataclasses`
- `lib.python.engineering_engine.impact_reasoning_engine`

### `lib/python/engineering_engine/relationship_extractor.py`

Classes:

- `RelationshipExtractor`

Imports:

- `__future__`
- `lib.python.engineering_engine.repository_model`
- `lib.python.engineering_engine.semantic_entities`

### `lib/python/engineering_engine/repository_audit.py`

Classes:

- `ModuleRecord`
- `AuditResult`
- `RepositoryAudit`

Imports:

- `__future__`
- `dataclasses`
- `datetime`
- `pathlib`

### `lib/python/engineering_engine/repository_model.py`

Classes:

- `PythonModule`
- `RepositoryKnowledge`
- `RepositoryKnowledgeBuilder`

Imports:

- `__future__`
- `ast`
- `dataclasses`
- `lib.python.engineering_engine.repository_scanner`
- `pathlib`

### `lib/python/engineering_engine/repository_scanner.py`

Classes:

- `RepositoryModel`
- `RepositoryScanner`

Imports:

- `__future__`
- `dataclasses`
- `pathlib`

### `lib/python/engineering_engine/review_engine.py`

Classes:

- `ReviewResult`
- `ReviewEngine`

Imports:

- `__future__`
- `dataclasses`
- `lib.python.engineering_engine.dependency_graph`
- `lib.python.engineering_engine.impact_analysis`
- `lib.python.engineering_engine.knowledge_graph`
- `lib.python.engineering_engine.repository_model`
- `pathlib`

### `lib/python/engineering_engine/roadmap_engine.py`

Classes:

- `Roadmap`
- `RoadmapEngine`

Imports:

- `__future__`
- `dataclasses`
- `lib.python.engineering_engine.batch_planner_engine`

### `lib/python/engineering_engine/rule_engine.py`

Classes:

- `PlanningRule`
- `RuleEngine`

Imports:

- `__future__`
- `dataclasses`

### `lib/python/engineering_engine/scm_provider.py`

Classes:

- `SCMProvider`

Imports:

- `__future__`
- `abc`
- `lib.python.engineering_engine.github_publish_engine`

### `lib/python/engineering_engine/scope_detector.py`

Classes:

- `ScopeDetector`

Imports:

- `__future__`
- `lib.python.engineering_engine.knowledge_graph`

### `lib/python/engineering_engine/semantic_classifier.py`

Classes:

- `SemanticClassifier`

Imports:

- `__future__`
- `lib.python.engineering_engine.semantic_entities`

### `lib/python/engineering_engine/semantic_entities.py`

Classes:

- `EntityType`
- `SemanticEntity`
- `SemanticRelationship`
- `SemanticRepository`

Imports:

- `__future__`
- `dataclasses`
- `enum`

### `lib/python/engineering_engine/semantic_extractor.py`

Classes:

- `SemanticExtractor`

Imports:

- `__future__`
- `lib.python.engineering_engine.knowledge_graph`
- `lib.python.engineering_engine.semantic_entities`

### `lib/python/engineering_engine/semantic_query_engine.py`

Classes:

- `SemanticQueryEngine`

Imports:

- `__future__`
- `lib.python.engineering_engine.semantic_entities`

### `lib/python/engineering_engine/semantic_repository_builder.py`

Classes:

- `SemanticRepositoryBuilder`

Imports:

- `__future__`
- `lib.python.engineering_engine.knowledge_graph`
- `lib.python.engineering_engine.relationship_extractor`
- `lib.python.engineering_engine.repository_model`
- `lib.python.engineering_engine.semantic_entities`
- `lib.python.engineering_engine.semantic_extractor`
- `pathlib`

### `lib/python/engineering_engine/validation_engine.py`

Classes:

- `ValidationResult`
- `ValidationEngine`

Imports:

- `__future__`
- `dataclasses`
- `datetime`
- `pathlib`
- `subprocess`

### `lib/python/engineering_engine/validation_plan_engine.py`

Classes:

- `ValidationPlan`
- `ValidationPlanEngine`

Imports:

- `__future__`
- `dataclasses`
- `lib.python.engineering_engine.execution_plan_engine`

### `lib/python/engineering_workspace/capabilities.py`

Classes:

- `Capability`

Imports:

- `__future__`
- `enum`

### `lib/python/engineering_workspace/models.py`

Classes:

- `WorkspaceStatus`
- `ServiceStatus`
- `ProviderStatus`
- `WorkspaceIdentity`
- `WorkspaceHealth`
- `CapabilityDescriptor`
- `ProviderDescriptor`
- `ServiceDescriptor`
- `WorkspaceSession`
- `WorkspaceState`
- `EngineeringWorkspaceModel`

Imports:

- `__future__`
- `dataclasses`
- `datetime`
- `enum`
- `typing`

### `lib/python/engineering_workspace/registry.py`

Classes:

- `RegistryEntry`
- `EngineeringWorkspaceRegistry`

Imports:

- `__future__`
- `dataclasses`
- `typing`

### `lib/python/engineering_workspace/service.py`

Classes:

- `EngineeringService`

Imports:

- `__future__`
- `abc`
- `typing`

### `lib/python/engineering_workspace/workspace.py`

Classes:

- `EngineeringWorkspace`

Imports:

- `__future__`
- `abc`
- `typing`

### `lib/python/epistemic/capability.py`

Classes:

- `Capability`
- `CapabilityRegistry`

Imports:

- `dataclasses`
- `datetime`

### `lib/python/epistemic/memory/model.py`

Classes:

- `Memory`

Imports:

- `dataclasses`

### `lib/python/epistemic/memory/store.py`

Classes:

- `MemoryStore`

Imports:

- `datetime`
- `json`
- `model`
- `pathlib`
- `uuid`

### `lib/python/epistemic/memory.py`

Classes:

- `Memory`

Imports:

- `datetime`
- `pathlib`

### `lib/python/epistemic/session.py`

Classes:

- `Session`
- `SessionManager`

Imports:

- `dataclasses`
- `datetime`
- `lib.python.epistemic.chronicle`
- `uuid`

### `lib/python/epistemic/transformation.py`

Classes:

- `Transformation`
- `TransformationLifecycle`

Imports:

- `dataclasses`
- `datetime`
- `pathlib`
- `uuid`

### `lib/python/epistemic/witness.py`

Functions:

- `witness`

Imports:

- `datetime`
- `pathlib`
- `uuid`

### `lib/python/evidence_engine/engine.py`

Classes:

- `EvidenceEngine`

Imports:

- `pathlib`
- `python.semantic_engine.engine`

### `lib/python/executable_repository_intelligence/engine.py`

Classes:

- `ExecutableRepositoryEngine`

Imports:

- `collections`
- `executable_dep_graph`
- `file_classifier`
- `injection_safety`
- `models`
- `pathlib`
- `persistence`
- `python.semantic_repository_intelligence`
- `python.semantic_repository_intelligence.ast_analyzer`
- `python.semantic_repository_intelligence.import_graph`
- `recommendations`
- `report`
- `runtime_map`
- `sys`
- `typing`
- `zone_classifier`

### `lib/python/executable_repository_intelligence/executable_dep_graph.py`

Classes:

- `ExecutableDependencyGraphBuilder`

Imports:

- `models`
- `pathlib`
- `typing`

### `lib/python/executable_repository_intelligence/file_classifier.py`

Classes:

- `FileClassifier`

Functions:

- `_match_any`

Imports:

- `models`
- `pathlib`
- `re`
- `typing`

### `lib/python/executable_repository_intelligence/injection_safety.py`

Classes:

- `InjectionSafetyClassifier`

Imports:

- `models`
- `typing`

### `lib/python/executable_repository_intelligence/models.py`

Classes:

- `FileClassification`
- `RuntimeComponent`
- `RepositoryRuntimeMap`
- `ExecutableDependencyEdge`
- `ExecutableDependencyGraph`
- `InjectionSafetyRecord`
- `RepositoryZone`
- `ExecutableRecommendation`
- `ExecutableRepositoryResult`

Imports:

- `dataclasses`
- `typing`

### `lib/python/executable_repository_intelligence/persistence.py`

Classes:

- `ExecutablePersistence`

Imports:

- `datetime`
- `json`
- `pathlib`
- `typing`

### `lib/python/executable_repository_intelligence/recommendations.py`

Classes:

- `ExecutableRecommendationEngine`

Imports:

- `models`
- `typing`

### `lib/python/executable_repository_intelligence/report.py`

Classes:

- `ExecutionModelReportGenerator`

Imports:

- `datetime`
- `pathlib`
- `typing`

### `lib/python/executable_repository_intelligence/runtime_map.py`

Classes:

- `RuntimeMapBuilder`

Functions:

- `_read_text`
- `_matches_any`

Imports:

- `models`
- `pathlib`
- `re`
- `typing`

### `lib/python/executable_repository_intelligence/zone_classifier.py`

Classes:

- `ZoneClassifier`

Imports:

- `collections`
- `models`
- `pathlib`
- `typing`

### `lib/python/execution_coordinator/engine.py`

Classes:

- `ExecutionCoordinator`

Imports:

- `json`
- `pathlib`

### `lib/python/execution_engine/engine.py`

Classes:

- `ExecutionEngine`

Imports:

- `datetime`
- `json`
- `pathlib`

### `lib/python/executive_briefing_engine/decision_tracker.py`

Classes:

- `ExecutiveDecisionTracker`

Imports:

- `models`
- `typing`

### `lib/python/executive_briefing_engine/engine.py`

Classes:

- `ExecutiveBriefingEngine`

Imports:

- `datetime`
- `decision_tracker`
- `generator`
- `hashlib`
- `insight_generator`
- `json`
- `models`
- `pathlib`
- `persistence`
- `priority_engine`
- `python.development_state_engine`
- `recommendation_engine`
- `risk_analyzer`
- `typing`

### `lib/python/executive_briefing_engine/generator.py`

Classes:

- `ExecutiveBriefingGenerator`

Functions:

- `_health_badge`

Imports:

- `models`
- `pathlib`
- `typing`

### `lib/python/executive_briefing_engine/insight_generator.py`

Classes:

- `ExecutiveInsightGenerator`

Imports:

- `typing`

### `lib/python/executive_briefing_engine/models.py`

Classes:

- `ExecutiveRecommendation`
- `ExecutiveRisk`
- `ExecutivePriorityItem`
- `ExecutiveDecision`
- `OwnerDashboard`
- `ExecutiveBriefing`

Imports:

- `dataclasses`
- `typing`

### `lib/python/executive_briefing_engine/persistence.py`

Classes:

- `ExecutiveBriefingPersistence`

Imports:

- `json`
- `models`
- `os`
- `pathlib`
- `tempfile`
- `typing`

### `lib/python/executive_briefing_engine/priority_engine.py`

Classes:

- `ExecutivePriorityEngine`

Functions:

- `_is_set`

Imports:

- `models`
- `typing`

### `lib/python/executive_briefing_engine/recommendation_engine.py`

Classes:

- `ExecutiveRecommendationEngine`

Functions:

- `_is_set`

Imports:

- `models`
- `typing`

### `lib/python/executive_briefing_engine/risk_analyzer.py`

Classes:

- `ExecutiveRiskAnalyzer`

Imports:

- `models`
- `typing`

### `lib/python/foundation_audit/checks.py`

Classes:

- `AuditResult`
- `Check`
- `DirectoryStructureCheck`
- `EngineInventoryCheck`
- `CanonicalDocumentsCheck`
- `EngineTestCoverageCheck`
- `CLIIntegrationCheck`
- `DevelopmentBatchCheck`

Imports:

- `pathlib`

### `lib/python/github_materialization/engine.py`

Classes:

- `GitHubMaterializationEngine`

Imports:

- `json`
- `pathlib`

### `lib/python/knowledge_engine/database.py`

Classes:

- `KnowledgeDatabase`

Imports:

- `json`
- `models`
- `pathlib`

### `lib/python/knowledge_engine/engine.py`

Classes:

- `KnowledgeEngine`

Imports:

- `database`
- `models`

### `lib/python/knowledge_engine/models.py`

Classes:

- `Entity`
- `Relationship`

Imports:

- `dataclasses`
- `typing`

### `lib/python/knowledge_graph/builder.py`

Classes:

- `CanonicalKnowledgeGraphBuilder`

Imports:

- `python.canonical_entities`
- `python.knowledge_graph.graph`
- `re`

### `lib/python/knowledge_graph/graph.py`

Classes:

- `CanonicalKnowledgeGraph`

Imports:

- `python.canonical_entities`

### `lib/python/knowledge_graph_engine.py`

Functions:

- `add_node`
- `connect`

Imports:

- `json`
- `pathlib`

### `lib/python/knowledge_graph_v2/engine.py`

Classes:

- `KnowledgeGraphEngine`

Imports:

- `ast`
- `json`
- `pathlib`

### `lib/python/knowledge_materialization/engine.py`

Classes:

- `KnowledgeObject`
- `KnowledgeRelationship`
- `MaterializedKnowledge`
- `KnowledgeMaterializationEngine`

Imports:

- `__future__`
- `dataclasses`
- `json`
- `pathlib`
- `python.canonical_entities`
- `python.knowledge_graph.graph`
- `typing`

### `lib/python/planning_engine/engine.py`

Classes:

- `PlanningEngine`

Imports:

- `models`
- `python.dependency_engine.engine`
- `python.planning_optimizer.engine`
- `python.repository_engine.engine`
- `python.validation_engine.engine`

### `lib/python/planning_engine/exporter.py`

Classes:

- `PlanningExporter`

Imports:

- `json`
- `pathlib`

### `lib/python/planning_engine/models.py`

Classes:

- `PlanningTask`
- `ExecutionPlan`

Imports:

- `dataclasses`
- `typing`

### `lib/python/planning_optimizer/engine.py`

Classes:

- `PlanningOptimizer`

Imports:

- `pathlib`
- `time`

### `lib/python/profiler/engine.py`

Classes:

- `Profiler`

Imports:

- `time`

### `lib/python/progress_monitor/engine.py`

Classes:

- `ProgressMonitor`

Imports:

- `time`

### `lib/python/project_profiles/trading_signals.py`

Classes:

- `TradingSignalsProfile`

Imports:

- `python.discovery_engine.engine`

### `lib/python/recommendation_engine/engine.py`

Classes:

- `RecommendationEngine`

### `lib/python/reporting_engine/engine.py`

Classes:

- `ReportingEngine`

Imports:

- `dataclasses`

### `lib/python/repository_engine/classifier.py`

Classes:

- `RepositoryFileClassifier`

Imports:

- `models`
- `python.executable_repository_intelligence.file_classifier`
- `typing`

### `lib/python/repository_engine/cli.py`

Functions:

- `inspect`

Imports:

- `datetime`
- `engine`
- `pathlib`
- `report`
- `serializer`

### `lib/python/repository_engine/deps.py`

Classes:

- `DependencyDiscovery`

Imports:

- `json`
- `models`
- `pathlib`
- `python.semantic_repository_intelligence.import_graph`
- `re`

### `lib/python/repository_engine/engine.py`

Classes:

- `RepositoryEngine`

Imports:

- `classifier`
- `deps`
- `metrics`
- `models`
- `pathlib`
- `python.semantic_repository_intelligence.ast_analyzer`
- `python.semantic_repository_intelligence.models`

### `lib/python/repository_engine/exporter.py`

Classes:

- `RepositoryExporter`

Imports:

- `json`
- `pathlib`

### `lib/python/repository_engine/metrics.py`

Classes:

- `MetricsExtractor`

Imports:

- `collections`
- `models`

### `lib/python/repository_engine/models.py`

Classes:

- `RepositoryItem`
- `RepositoryMetrics`
- `DependencyMap`
- `ClassifiedFile`
- `RepositoryProfile`

Imports:

- `dataclasses`
- `typing`

### `lib/python/repository_engine/report.py`

Classes:

- `BaseRenderer`
- `MarkdownRenderer`

Imports:

- `abc`

### `lib/python/repository_engine/serializer.py`

Classes:

- `RepositoryProfileSerializer`

Imports:

- `dataclasses`
- `json`

### `lib/python/repository_inspector_v2/analyzer.py`

Classes:

- `RepositoryAnalyzer`

### `lib/python/repository_inspector_v2/engine.py`

Classes:

- `RepositoryInspectorV2`

Imports:

- `json`
- `pathlib`
- `python.dependency_engine.engine`
- `python.planning_engine.engine`
- `python.repository_engine.engine`
- `python.rule_engine.engine`
- `python.validation_engine.engine`
- `report`

### `lib/python/repository_inspector_v2/report.py`

Classes:

- `MarkdownReport`

Imports:

- `pathlib`

### `lib/python/repository_profile.py`

Functions:

- `count`
- `exists`
- `git`

Imports:

- `json`
- `os`
- `pathlib`
- `subprocess`

### `lib/python/review_agent/engine.py`

Classes:

- `ReviewAgent`

### `lib/python/rule_engine/base.py`

Classes:

- `Rule`

Imports:

- `abc`

### `lib/python/rule_engine/engine.py`

Classes:

- `RuleEngine`

Imports:

- `python.rule_engine.rules.repository_size_rule`
- `python.rule_engine.rules.validation_rule`

### `lib/python/rule_engine/governance_kernel.py`

Classes:

- `PermissionCategory`
- `Permission`
- `RiskLevel`
- `RiskClassification`
- `ApprovalStatus`
- `ApprovalRecord`
- `AuditRecord`
- `PermissionEngine`
- `PermissionDeniedError`
- `RiskEngine`
- `ApprovalEngine`
- `AuditEngine`
- `EmergencyStop`
- `EmergencyStopError`
- `GovernanceKernel`
- `ApprovalRequiredError`

Imports:

- `__future__`
- `dataclasses`
- `datetime`
- `enum`
- `logging`
- `typing`
- `uuid`

### `lib/python/rule_engine/models.py`

Classes:

- `RuleResult`

Imports:

- `dataclasses`

### `lib/python/rule_engine/rules/repository_size_rule.py`

Classes:

- `RepositorySizeRule`

Imports:

- `python.rule_engine.base`
- `python.rule_engine.models`

### `lib/python/rule_engine/rules/validation_rule.py`

Classes:

- `ValidationRule`

Imports:

- `python.rule_engine.base`
- `python.rule_engine.models`

### `lib/python/runtime/bootstrap.py`

Classes:

- `RuntimeBootstrap`

Imports:

- `lib.python.context_synchronization_engine`
- `lib.python.dashboard.service`
- `lib.python.runtime.config`
- `lib.python.runtime.diagnostics`
- `lib.python.runtime.event_dispatcher`
- `lib.python.runtime.event_loop`
- `lib.python.runtime.health`
- `lib.python.runtime.identity`
- `lib.python.runtime.interfaces.github_webhook`
- `lib.python.runtime.interfaces.http_server`
- `lib.python.runtime.interfaces.telegram_gateway`
- `lib.python.runtime.job_queue`
- `lib.python.runtime.lifecycle`
- `lib.python.runtime.logging_service`
- `lib.python.runtime.metrics`
- `lib.python.runtime.recovery`
- `lib.python.runtime.registry`
- `lib.python.runtime.reports`
- `lib.python.runtime.scheduler`
- `lib.python.runtime.secrets`
- `lib.python.runtime.state`
- `lib.python.runtime.supervisor`
- `logging`
- `os`
- `time`
- `typing`

### `lib/python/runtime/config.py`

Classes:

- `RuntimeConfig`

Imports:

- `dataclasses`
- `os`
- `typing`

### `lib/python/runtime/diagnostics.py`

Classes:

- `RuntimeDiagnosticsService`

Imports:

- `__future__`
- `datetime`
- `json`
- `lib.python.runtime.state`
- `os`
- `pathlib`
- `sys`
- `typing`

### `lib/python/runtime/event_dispatcher.py`

Classes:

- `RuntimeEvent`
- `EventDispatcher`

Imports:

- `dataclasses`
- `datetime`
- `logging`
- `threading`
- `typing`

### `lib/python/runtime/event_loop.py`

Classes:

- `EventLoop`

Imports:

- `datetime`
- `logging`
- `threading`
- `time`
- `typing`

### `lib/python/runtime/health.py`

Classes:

- `HealthCheckResult`
- `HealthService`

Imports:

- `dataclasses`
- `datetime`
- `logging`
- `typing`

### `lib/python/runtime/identity.py`

Classes:

- `RuntimeIdentity`

Imports:

- `dataclasses`
- `datetime`
- `os`
- `uuid`

### `lib/python/runtime/interfaces/api_auth.py`

Classes:

- `ApiAuth`

Imports:

- `__future__`
- `os`

### `lib/python/runtime/interfaces/github_webhook.py`

Classes:

- `GitHubWebhookHost`

Imports:

- `hashlib`
- `hmac`
- `json`
- `lib.python.runtime.event_dispatcher`
- `logging`
- `typing`

### `lib/python/runtime/interfaces/http_server.py`

Classes:

- `_RuntimeHandler`
- `RuntimeHttpServer`

Imports:

- `http.server`
- `json`
- `lib.python.runtime.interfaces.runtime_api`
- `logging`
- `threading`
- `typing`
- `urllib.parse`

### `lib/python/runtime/interfaces/runtime_api.py`

Classes:

- `RuntimeApiRouter`

Imports:

- `__future__`
- `lib.python.runtime.interfaces.api_auth`
- `typing`

### `lib/python/runtime/interfaces/telegram_gateway.py`

Classes:

- `TelegramGateway`

Imports:

- `json`
- `logging`
- `typing`

### `lib/python/runtime/job_queue.py`

Classes:

- `Job`
- `JobQueueHost`

Imports:

- `dataclasses`
- `datetime`
- `logging`
- `queue`
- `threading`
- `typing`
- `uuid`

### `lib/python/runtime/lifecycle.py`

Classes:

- `LifecyclePhase`
- `LifecycleManager`

Imports:

- `enum`
- `typing`

### `lib/python/runtime/logging_service.py`

Classes:

- `JsonFormatter`

Functions:

- `configure_logging`

Imports:

- `datetime`
- `json`
- `logging`
- `sys`

### `lib/python/runtime/metrics.py`

Classes:

- `RuntimeMetrics`

Imports:

- `datetime`
- `threading`
- `typing`

### `lib/python/runtime/process.py`

Functions:

- `main`

Imports:

- `logging`
- `os`
- `sys`

### `lib/python/runtime/railway.py`

Classes:

- `RailwayDeploymentMetadata`
- `RailwayBootstrap`

Functions:

- `load_railway_metadata`
- `log_railway_identity`

Imports:

- `dataclasses`
- `logging`
- `os`
- `typing`

### `lib/python/runtime/recovery.py`

Classes:

- `RecoveryAttempt`
- `RecoveryService`

Imports:

- `dataclasses`
- `datetime`
- `logging`
- `threading`
- `time`
- `typing`

### `lib/python/runtime/registry.py`

Classes:

- `RuntimeRegistry`

Imports:

- `typing`

### `lib/python/runtime/reports.py`

Classes:

- `RuntimeReports`

Imports:

- `datetime`
- `json`
- `logging`
- `os`
- `pathlib`
- `typing`

### `lib/python/runtime/scheduler.py`

Classes:

- `ScheduledJob`
- `SchedulerHost`

Imports:

- `dataclasses`
- `datetime`
- `logging`
- `threading`
- `time`
- `typing`

### `lib/python/runtime/secrets.py`

Classes:

- `SecretValidationResult`
- `SecretManager`

Imports:

- `dataclasses`
- `os`
- `typing`

### `lib/python/runtime/shutdown.py`

Classes:

- `GracefulShutdown`

Imports:

- `logging`
- `signal`
- `threading`
- `typing`

### `lib/python/runtime/state.py`

Classes:

- `RuntimePublicState`
- `RuntimeIssue`
- `RuntimeStateService`

Functions:

- `_utc_now`

Imports:

- `__future__`
- `dataclasses`
- `datetime`
- `enum`
- `typing`

### `lib/python/runtime/supervisor.py`

Classes:

- `ComponentStatus`
- `RuntimeSupervisor`

Imports:

- `dataclasses`
- `datetime`
- `logging`
- `threading`
- `typing`

### `lib/python/self_evaluation_engine/analyzers.py`

Classes:

- `CanonicalComplianceAnalyzer`
- `ArchitectureComplianceAnalyzer`
- `RepositoryComplianceAnalyzer`
- `RegressionAnalyzer`
- `CoverageAnalyzer`
- `EvidenceAnalyzer`
- `ImprovementAnalyzer`

Imports:

- `models`
- `typing`

### `lib/python/self_evaluation_engine/engine.py`

Classes:

- `EvaluationCoordinator`
- `SelfEvaluationEngine`

Functions:

- `_utcnow`
- `_evaluation_id`

Imports:

- `analyzers`
- `datetime`
- `hashlib`
- `models`
- `pathlib`
- `persistence`
- `report`
- `scoring`
- `typing`

### `lib/python/self_evaluation_engine/models.py`

Classes:

- `EvaluationContext`
- `QualityScore`
- `RegressionFinding`
- `ArchitectureFinding`
- `EvaluationResult`

Imports:

- `dataclasses`
- `typing`

### `lib/python/self_evaluation_engine/persistence.py`

Classes:

- `EvaluationPersistence`

Imports:

- `json`
- `os`
- `pathlib`
- `tempfile`
- `typing`

### `lib/python/self_evaluation_engine/report.py`

Classes:

- `EvaluationReportGenerator`

Functions:

- `_score_bar`
- `_fmt_list`

Imports:

- `pathlib`
- `typing`

### `lib/python/self_evaluation_engine/scoring.py`

Classes:

- `QualityScorer`
- `ConfidenceScorer`

Imports:

- `models`
- `typing`

### `lib/python/self_improvement_engine/analyzers.py`

Classes:

- `TechnicalDebtAnalyzer`
- `PerformanceAnalyzer`
- `CapabilityAnalyzer`

Imports:

- `models`
- `pathlib`
- `re`
- `time`
- `typing`

### `lib/python/self_improvement_engine/engine.py`

Classes:

- `OptimizationPlanner`
- `EvolutionPlanner`
- `ImprovementCoordinator`
- `SelfImprovementEngine`

Functions:

- `_utcnow`
- `_plan_id`

Imports:

- `analyzers`
- `datetime`
- `generators`
- `hashlib`
- `models`
- `pathlib`
- `persistence`
- `report`
- `typing`

### `lib/python/self_improvement_engine/generators.py`

Classes:

- `IssueGenerator`
- `BatchGenerator`
- `CoreProposalEngine`
- `RoadmapEvolutionEngine`

Functions:

- `_utcnow`
- `_short_hash`

Imports:

- `datetime`
- `hashlib`
- `models`
- `typing`

### `lib/python/self_improvement_engine/models.py`

Classes:

- `TechnicalDebt`
- `PerformanceMetric`
- `CapabilityGap`
- `ProposedIssue`
- `ProposedBatch`
- `CoreProposal`
- `RoadmapUpdate`
- `OptimizationPlan`

Imports:

- `dataclasses`
- `typing`

### `lib/python/self_improvement_engine/persistence.py`

Classes:

- `ImprovementPersistence`

Imports:

- `json`
- `os`
- `pathlib`
- `tempfile`
- `typing`

### `lib/python/self_improvement_engine/report.py`

Classes:

- `ImprovementReportGenerator`

Functions:

- `_fmt_list`

Imports:

- `pathlib`
- `typing`

### `lib/python/semantic_engine/engine.py`

Classes:

- `SemanticEngine`

Imports:

- `ast`
- `pathlib`

### `lib/python/semantic_matching/matcher.py`

Classes:

- `SemanticMatcher`

Imports:

- `pathlib`
- `python.canonical_entities`
- `python.semantic_engine.engine`
- `re`

### `lib/python/semantic_repository_intelligence/architecture_graph.py`

Classes:

- `ArchitectureGraphBuilder`

Functions:

- `_classify_path`

Imports:

- `collections`
- `models`
- `pathlib`
- `re`
- `typing`

### `lib/python/semantic_repository_intelligence/ast_analyzer.py`

Classes:

- `LanguageAnalyzer`
- `PythonAnalyzer`
- `TypeScriptAnalyzer`
- `JSONAnalyzer`
- `YAMLAnalyzer`
- `MarkdownAnalyzer`
- `ASTAnalyzer`

Imports:

- `ast`
- `json`
- `models`
- `pathlib`
- `re`
- `typing`

### `lib/python/semantic_repository_intelligence/call_graph.py`

Classes:

- `CallGraphBuilder`

Imports:

- `collections`
- `models`
- `pathlib`
- `typing`

### `lib/python/semantic_repository_intelligence/confidence_engine.py`

Classes:

- `ConfidenceEngine`

Imports:

- `typing`

### `lib/python/semantic_repository_intelligence/dependency_graph.py`

Classes:

- `DependencyGraphBuilder`

Functions:

- `_parse_requirements`
- `_parse_setup_py`
- `_parse_pyproject_toml`
- `_parse_package_json`
- `_parse_go_mod`

Imports:

- `json`
- `models`
- `pathlib`
- `re`
- `typing`

### `lib/python/semantic_repository_intelligence/engine.py`

Classes:

- `SemanticRepositoryEngine`

Imports:

- `architecture_graph`
- `ast_analyzer`
- `call_graph`
- `confidence_engine`
- `dependency_graph`
- `import_graph`
- `injection_point_analyzer`
- `models`
- `pathlib`
- `persistence`
- `recommendation_engine`
- `relationship_resolver`
- `typing`

### `lib/python/semantic_repository_intelligence/import_graph.py`

Classes:

- `RelationshipResolver`
- `ImportGraphBuilder`

Imports:

- `collections`
- `models`
- `os`
- `pathlib`
- `typing`

### `lib/python/semantic_repository_intelligence/injection_point_analyzer.py`

Classes:

- `InjectionPointAnalyzer`

Imports:

- `models`
- `pathlib`
- `re`
- `typing`

### `lib/python/semantic_repository_intelligence/models.py`

Classes:

- `ImportSymbol`
- `ClassSymbol`
- `FunctionSymbol`
- `ConstantSymbol`
- `FileAnalysis`
- `ImportEdge`
- `ImportGraphResult`
- `CallEdge`
- `CallGraphResult`
- `ExternalDependency`
- `DependencyGraphResult`
- `ArchitectureNode`
- `ArchitectureEdge`
- `ArchitectureRisk`
- `ArchitectureGraphResult`
- `InjectionPoint`
- `SemanticFinding`
- `SemanticRecommendation`
- `RepositoryComplexity`

Imports:

- `dataclasses`
- `typing`

### `lib/python/semantic_repository_intelligence/persistence.py`

Classes:

- `SemanticPersistence`

Imports:

- `datetime`
- `json`
- `pathlib`
- `typing`

### `lib/python/semantic_repository_intelligence/recommendation_engine.py`

Classes:

- `SemanticRecommendationEngine`

Imports:

- `confidence_engine`
- `models`
- `typing`

### `lib/python/semantic_repository_intelligence/relationship_resolver.py`

Classes:

- `RelationshipResolver`

Functions:

- `_norm`

Imports:

- `models`
- `os`
- `pathlib`
- `typing`

### `lib/python/session_runtime/models.py`

Classes:

- `Session`

Imports:

- `dataclasses`
- `typing`

### `lib/python/session_runtime/runtime.py`

Classes:

- `SessionRuntime`

Imports:

- `datetime`
- `models`
- `storage`

### `lib/python/session_runtime/storage.py`

Classes:

- `SessionStorage`

Imports:

- `json`
- `pathlib`

### `lib/python/validation_engine/csl_validator.py`

Classes:

- `ValidationCategory`
- `ValidationFinding`
- `NormativeValidationResult`
- `CslNormativeValidator`

Imports:

- `__future__`
- `dataclasses`
- `enum`
- `pathlib`
- `python.canonical_entities`
- `python.canonical_parser`
- `typing`

### `lib/python/validation_engine/engine.py`

Classes:

- `ValidationEngine`

Imports:

- `models`
- `pathlib`

### `lib/python/validation_engine/exporter.py`

Classes:

- `ValidationExporter`

Imports:

- `json`
- `pathlib`

### `lib/python/validation_engine/models.py`

Classes:

- `ValidationResult`

Imports:

- `dataclasses`

### `lib/python/workspace_index/builder.py`

Classes:

- `WorkspaceIndexBuilder`

Imports:

- `models`
- `os`
- `pathlib`
- `policy`
- `time`

### `lib/python/workspace_index/exporter.py`

Classes:

- `WorkspaceIndexExporter`

Imports:

- `json`
- `pathlib`

### `lib/python/workspace_index/incremental.py`

Classes:

- `FileSnapshot`
- `RepositorySnapshot`
- `IndexDelta`
- `IncrementalStats`
- `IncrementalBuildResult`
- `ChangeDetector`
- `IncrementalWorkspaceIndex`

Functions:

- `_index_from_dict`

Imports:

- `builder`
- `dataclasses`
- `exporter`
- `json`
- `models`
- `os`
- `pathlib`
- `policy`
- `time`
- `typing`

### `lib/python/workspace_index/models.py`

Classes:

- `WorkspaceFile`
- `WorkspaceDirectory`
- `WorkspaceStatistics`
- `WorkspaceIndex`

Imports:

- `dataclasses`

### `lib/python/workspace_index/policy.py`

Classes:

- `RepositoryPolicy`

### `lib/python/workspace_manager/engine.py`

Classes:

- `WorkspaceManager`

Imports:

- `pathlib`

### `lib/python/workspace_orchestrator/dashboard.py`

Classes:

- `WorkspaceExecutiveDashboard`
- `WorkspaceReportGenerator`

Imports:

- `datetime`
- `models`
- `pathlib`
- `typing`

### `lib/python/workspace_orchestrator/dependency_graph.py`

Classes:

- `WorkspaceDependencyGraph`
- `WorkspaceRelationshipAnalyzer`

Imports:

- `models`
- `pathlib`
- `typing`

### `lib/python/workspace_orchestrator/engine.py`

Classes:

- `WorkspaceOrchestrator`

Imports:

- `dashboard`
- `datetime`
- `dependency_graph`
- `intelligence`
- `models`
- `pathlib`
- `persistence`
- `python.agent_runtime.models`
- `python.agent_runtime.registry`
- `python.progress_monitor.engine`
- `python.workspace_manager.engine`
- `registry`
- `scanner`
- `state_manager`
- `time`
- `typing`

### `lib/python/workspace_orchestrator/intelligence.py`

Classes:

- `WorkspaceHealthEngine`
- `WorkspacePriorityEngine`
- `WorkspaceRiskAnalyzer`
- `WorkspaceRecommendationEngine`

Imports:

- `models`
- `typing`

### `lib/python/workspace_orchestrator/models.py`

Classes:

- `WorkspaceRepository`
- `WorkspaceDependencyEdge`
- `WorkspaceRelationship`
- `WorkspaceHealth`
- `WorkspaceRecommendation`
- `WorkspaceRisk`
- `WorkspacePriority`
- `WorkspaceScanResult`
- `WorkspaceStatistics`

Imports:

- `dataclasses`
- `typing`

### `lib/python/workspace_orchestrator/persistence.py`

Classes:

- `WorkspacePersistence`

Imports:

- `datetime`
- `json`
- `models`
- `os`
- `pathlib`
- `registry`
- `tempfile`
- `typing`

### `lib/python/workspace_orchestrator/registry.py`

Classes:

- `RepositoryRegistry`
- `WorkspaceRegistry`

Imports:

- `models`
- `pathlib`
- `typing`

### `lib/python/workspace_orchestrator/scanner.py`

Classes:

- `WorkspaceDiscoveryEngine`
- `WorkspaceScanner`

Imports:

- `datetime`
- `json`
- `models`
- `os`
- `pathlib`
- `python.ai_cto_scanner`
- `subprocess`
- `typing`

### `lib/python/workspace_orchestrator/state_manager.py`

Classes:

- `WorkspaceStateManager`

Imports:

- `datetime`
- `models`
- `pathlib`
- `persistence`
- `registry`
- `typing`

### `tests/engineering/test_backlog_pipeline.py`

Functions:

- `test_backlog_pipeline`

Imports:

- `lib.python.engineering_engine.backlog_generator`
- `lib.python.engineering_engine.github_milestone_generator`
- `lib.python.engineering_engine.github_project_planner`
- `pathlib`
- `sys`

### `tests/engineering/test_project_export_import.py`

Functions:

- `test_export_import_roundtrip`

Imports:

- `json`
- `lib.python.engineering_engine.batch_planner_engine`
- `lib.python.engineering_engine.engineering_task_engine`
- `lib.python.engineering_engine.github_milestone_generator`
- `lib.python.engineering_engine.github_project_planner`
- `lib.python.engineering_engine.project_exporter`
- `lib.python.engineering_engine.project_importer`
- `lib.python.engineering_engine.roadmap_engine`
- `pathlib`
- `sys`

### `tests/engineering/test_task_pipeline.py`

Functions:

- `test_task_pipeline`

Imports:

- `lib.python.engineering_engine.batch_planner_engine`
- `lib.python.engineering_engine.engineering_task_engine`
- `lib.python.engineering_engine.roadmap_engine`
- `pathlib`
- `sys`

### `tests/epistemic/test_capability.py`

Functions:

- `test_capability_registry`

Imports:

- `lib.python.epistemic.capability`

### `tests/epistemic/test_memory.py`

Functions:

- `test_memory_roundtrip`

Imports:

- `lib.python.epistemic.memory.store`

Python files structurally indexed: 308

## 7. Existing Test Anatomy

### 7.1 Test Files

```text
.ai/backups/core021a002/test_knowledge_engine_v2.py
.ai/backups/core021a002/test_repository_engine_v2.py
test_csl_grammar.py
test_csl_semantic.py
tests/engineering/test_backlog_pipeline.py
tests/engineering/test_project_export_import.py
tests/engineering/test_task_pipeline.py
tests/epistemic/test_capability.py
tests/epistemic/test_memory.py
```

### 7.2 Test Definitions

- `.ai/backups/core021a002/test_knowledge_engine_v2.py`: PARSE ERROR: invalid syntax (<unknown>, line 4)
- `.ai/backups/core021a002/test_repository_engine_v2.py`: PARSE ERROR: invalid syntax (<unknown>, line 4)
#### `tests/engineering/test_backlog_pipeline.py`

- line 18: `test_backlog_pipeline`

#### `tests/engineering/test_project_export_import.py`

- line 30: `test_export_import_roundtrip`

#### `tests/engineering/test_task_pipeline.py`

- line 18: `test_task_pipeline`

#### `tests/epistemic/test_capability.py`

- line 4: `test_capability_registry`

#### `tests/epistemic/test_memory.py`

- line 3: `test_memory_roundtrip`

Test definitions found: 5

## 8. PCC-01 Software Relevance Ranking

This ranking is an inspection aid only. A high score does not prove behavioral suitability.

### 1. `lib/python/context_synchronization_engine/engine.py` — score 352

- evidence: 6
- persistence: 15
- provenance: 13
- repository: 40
- session: 1

### 2. `lib/python/dashboard/service.py` — score 349

- evidence: 5
- persistence: 7
- repository: 86
- session: 84

### 3. `lib/python/autonomous_execution_engine/engine.py` — score 262

- evidence: 16
- persistence: 12
- repository: 10

### 4. `lib/python/self_evaluation_engine/analyzers.py` — score 260

- evidence: 33
- repository: 27

### 5. `lib/python/runtime/bootstrap.py` — score 237

- identity: 24
- lifecycle: 25
- persistence: 1
- repository: 2

### 6. `lib/python/workspace_orchestrator/intelligence.py` — score 228

- evidence: 16
- repository: 20

### 7. `lib/python/workspace_orchestrator/engine.py` — score 210

- persistence: 21
- repository: 14

### 8. `lib/python/workspace_orchestrator/models.py` — score 205

- evidence: 16
- identity: 2
- repository: 13

### 9. `lib/python/self_improvement_engine/analyzers.py` — score 193

- evidence: 7
- persistence: 6
- repository: 19

### 10. `lib/python/self_improvement_engine/models.py` — score 175

- evidence: 21
- repository: 3

### 11. `lib/python/self_evaluation_engine/engine.py` — score 172

- evidence: 2
- persistence: 8
- repository: 21

### 12. `lib/python/ai_cto_scanner/report.py` — score 169

- evidence: 1
- identity: 1
- lifecycle: 2
- memory: 8
- persistence: 4
- repository: 9
- session: 1

### 13. `lib/python/executive_briefing_engine/recommendation_engine.py` — score 164

- evidence: 18
- repository: 4

### 14. `lib/python/ai_platform/sessions.py` — score 162

- repository: 2
- session: 19

### 15. `lib/python/epistemic/session.py` — score 160

- session: 20

### 16. `lib/python/autonomous_execution_engine/validator.py` — score 159

- evidence: 13
- repository: 11

### 17. `lib/python/semantic_repository_intelligence/recommendation_engine.py` — score 142

- evidence: 14
- repository: 6

### 18. `lib/python/executable_repository_intelligence/models.py` — score 140

- evidence: 11
- persistence: 1
- repository: 9

### 19. `lib/python/autonomous_execution_engine/models.py` — score 137

- evidence: 9
- repository: 13

### 20. `lib/python/self_improvement_engine/engine.py` — score 133

- lifecycle: 1
- persistence: 4
- repository: 24

### 21. `lib/python/autonomous_planning_engine/engine.py` — score 129

- persistence: 7
- repository: 16

### 22. `lib/python/semantic_repository_intelligence/models.py` — score 129

- evidence: 13
- repository: 5

### 23. `lib/python/development_state_engine/runtime.py` — score 128

- persistence: 4
- repository: 21

### 24. `lib/python/context_synchronization_engine/models.py` — score 125

- evidence: 5
- provenance: 5
- repository: 10

### 25. `lib/python/session_runtime/runtime.py` — score 119

- repository: 3
- session: 11
- storage: 4

### 26. `lib/python/executive_briefing_engine/models.py` — score 113

- evidence: 11
- repository: 5

### 27. `lib/python/epistemic/memory/store.py` — score 112

- memory: 11
- session: 3

### 28. `lib/python/self_evaluation_engine/models.py` — score 110

- evidence: 10
- repository: 6

### 29. `lib/python/executive_briefing_engine/risk_analyzer.py` — score 108

- evidence: 11
- repository: 4

### 30. `lib/python/semantic_repository_intelligence/confidence_engine.py` — score 101

- evidence: 12
- repository: 1

### 31. `lib/python/cli/main.py` — score 100

- repository: 70

### 32. `lib/python/ai_cto_scanner/scoring.py` — score 99

- memory: 7
- persistence: 5
- session: 1

### 33. `lib/python/executable_repository_intelligence/engine.py` — score 99

- evidence: 3
- persistence: 5
- repository: 8

### 34. `lib/python/ai_cto_scanner/detectors.py` — score 97

- evidence: 3
- memory: 3
- persistence: 3
- session: 2
- storage: 3

### 35. `lib/python/executable_repository_intelligence/report.py` — score 92

- evidence: 5
- persistence: 1
- repository: 9

### 36. `tests/epistemic/test_memory.py` — score 92

- experience: 1
- memory: 6
- session: 4

### 37. `lib/python/semantic_repository_intelligence/engine.py` — score 91

- evidence: 1
- memory: 3
- persistence: 3
- repository: 6
- session: 1

### 38. `lib/python/runtime/reports.py` — score 86

- identity: 11
- lifecycle: 4

### 39. `lib/python/self_improvement_engine/generators.py` — score 85

- evidence: 10
- lifecycle: 1

### 40. `lib/python/epistemic/memory.py` — score 80

- experience: 2
- memory: 7

### 41. `lib/python/executable_repository_intelligence/file_classifier.py` — score 79

- evidence: 8
- repository: 3

### 42. `lib/python/executable_repository_intelligence/recommendations.py` — score 77

- evidence: 9
- repository: 1

### 43. `lib/python/drift_engine/engine.py` — score 76

- evidence: 7
- repository: 4

### 44. `lib/python/executive_briefing_engine/engine.py` — score 76

- persistence: 3
- repository: 11

### 45. `lib/python/evidence_engine/engine.py` — score 74

- evidence: 8
- repository: 2

### 46. `lib/python/semantic_repository_intelligence/architecture_graph.py` — score 74

- evidence: 4
- memory: 3
- repository: 2
- session: 1

### 47. `lib/python/executive_briefing_engine/generator.py` — score 73

- evidence: 6
- repository: 5

### 48. `lib/python/self_evaluation_engine/scoring.py` — score 72

- evidence: 9

### 49. `lib/python/ai_platform/service.py` — score 71

- repository: 3
- session: 7

### 50. `lib/python/compliance_engine/engine.py` — score 71

- evidence: 7
- repository: 3

### 51. `lib/python/memory_engine.py` — score 71

- memory: 7
- repository: 3

### 52. `lib/python/agents/development_agent.py` — score 70

- repository: 14

### 53. `lib/python/autonomous_planning_engine/models.py` — score 70

- repository: 14

### 54. `lib/python/workspace_orchestrator/dashboard.py` — score 70

- repository: 14

### 55. `lib/python/engineering_engine/repository_audit.py` — score 68

- evidence: 1
- lifecycle: 1
- repository: 11

### 56. `lib/python/self_evaluation_engine/persistence.py` — score 66

- evidence: 4
- persistence: 2
- repository: 4

### 57. `lib/python/semantic_matching/matcher.py` — score 65

- evidence: 5
- repository: 5

### 58. `lib/python/workspace_orchestrator/scanner.py` — score 65

- repository: 13

### 59. `lib/python/runtime/diagnostics.py` — score 63

- identity: 5
- lifecycle: 3
- repository: 2
- session: 1

### 60. `lib/python/workspace_index/incremental.py` — score 55

- repository: 11

### 61. `lib/python/engineering_engine/gap_analysis.py` — score 54

- evidence: 3
- repository: 6

### 62. `lib/python/runtime/lifecycle.py` — score 53

- lifecycle: 5
- persistence: 4

### 63. `lib/python/canonical_entities/models.py` — score 52

- evidence: 5
- lifecycle: 1
- provenance: 1

### 64. `lib/python/coverage_engine/engine.py` — score 51

- evidence: 3
- persistence: 1
- repository: 4

### 65. `lib/python/workspace_orchestrator/state_manager.py` — score 51

- lifecycle: 1
- persistence: 3
- repository: 5

### 66. `lib/python/workspace_orchestrator/dependency_graph.py` — score 49

- evidence: 3
- repository: 5

### 67. `lib/python/autonomous_execution_engine/evidence.py` — score 48

- evidence: 6

### 68. `lib/python/workspace_orchestrator/registry.py` — score 48

- memory: 2
- persistence: 1
- repository: 5

### 69. `lib/python/executable_repository_intelligence/zone_classifier.py` — score 47

- evidence: 4
- repository: 3

### 70. `lib/python/runtime/interfaces/http_server.py` — score 47

- lifecycle: 1
- repository: 2
- session: 4

### 71. `lib/python/epistemic/transformation.py` — score 46

- evidence: 2
- lifecycle: 6

### 72. `lib/python/autonomous_workflow_engine.py` — score 45

- memory: 5
- repository: 1

### 73. `lib/python/cdm_engine/engine.py` — score 45

- lifecycle: 2
- provenance: 5

### 74. `lib/python/semantic_repository_intelligence/persistence.py` — score 45

- identity: 1
- memory: 1
- persistence: 1
- repository: 4
- storage: 1

### 75. `lib/python/epistemic/memory/model.py` — score 44

- experience: 1
- memory: 3
- session: 1

### 76. `lib/python/self_improvement_engine/persistence.py` — score 44

- persistence: 2
- repository: 6

### 77. `lib/python/workspace_index/models.py` — score 44

- identity: 1
- memory: 1
- repository: 6

### 78. `lib/python/agents/ai_cto_scanner_agent.py` — score 43

- memory: 1
- repository: 7

### 79. `lib/python/autonomous_execution_engine/persistence.py` — score 42

- evidence: 1
- persistence: 2
- repository: 4

### 80. `lib/python/decision_engine.py` — score 40

- memory: 5

## 9. Inspection Boundary

The evidence above describes existing repository anatomy.

It does not by itself prove that any existing component satisfies PCC-01 behavior.

Behavioral inheritance decisions require inspection of the concrete implementation and tests.

No existing Session, Memory, Evidence, Provenance, Repository, Storage or persistence component may be collapsed into Experience merely because its name or text appears relevant.

## 10. Required Next Analysis

Using this inspection report, the next analysis must determine:

1. the first Experience organ to construct;
2. the exact existing tissue to inherit;
3. the exact existing tissue to adapt;
4. the exact new tissue to construct;
5. the existing tissue that must not be used;
6. the concrete implementation files;
7. the concrete test files;
8. the evidence required before any implementation claim;
9. the smallest real restart continuity demonstration.

Implementation remains: **NOT DEMONSTRATED**

Canonical status remains: **NOT CANON**

Production status remains: **NOT PRODUCTION-READY**

---

END OF PCC-01 — CORE EXPERIENCE PRE-IMPLEMENTATION INSPECTION

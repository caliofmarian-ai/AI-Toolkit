# AI CTO Execution Model

**CORE-008C — Executable Repository Intelligence**

| Field | Value |
| ----- | ----- |
| Repository | `/home/runner/work/AI-Toolkit/AI-Toolkit` |
| Generated | 2026-08-03 04:26 UTC |
| Executable Files | 160 |
| Non-Executable Files | 97 |
| Total Files | 257 |

## Executive Summary

This document is the authoritative **Executable Repository Model** for this repository.  It distinguishes files that participate in **runtime execution** from documentation, generated artifacts, and informational files.

### File Category Distribution

| Category | Files |
| -------- | ----- |
| Bootstrap | 48 |
| Canonical Specification | 65 |
| Configuration | 8 |
| Documentation | 19 |
| Executable Code | 108 |
| Reports | 3 |
| Runtime Entry Point | 4 |
| Tests | 2 |

### Directory Zone Distribution

| Zone | Directories |
| ---- | ----------- |
| Documentation | 5 |
| Generated | 5 |
| Runtime | 49 |
| Testing | 1 |


## Repository Runtime Map

**Main Entry Point:** `lib/python/development_validator/main.py`

**Scheduler Entry:** `lib/python/ai_cto_scanner/detectors.py`

**Execution Chain:**

- `lib/python/development_validator/main.py`

**Bootstrap Sequence:**

- `lib/python/__init__.py`
- `lib/python/agent_runtime/__init__.py`
- `lib/python/agents/__init__.py`
- `lib/python/ai_cto_scanner/__init__.py`
- `lib/python/ai_cto_scanner/detectors.py`
- `lib/python/ai_cto_scanner/report.py`
- `lib/python/autonomous_planner/__init__.py`
- `lib/python/batch_generator/__init__.py`
- `lib/python/batch_planner/__init__.py`
- `lib/python/canonical_audit/__init__.py`
- `lib/python/canonical_entities/__init__.py`
- `lib/python/canonical_entities/models.py`
- `lib/python/canonical_intelligence/__init__.py`
- `lib/python/canonical_parser/__init__.py`
- `lib/python/canonical_repository/__init__.py`

**Background Workers:**

- `lib/python/ai_cto_scanner/detectors.py`
- `lib/python/executable_repository_intelligence/models.py`
- `lib/python/executable_repository_intelligence/report.py`
- `lib/python/executable_repository_intelligence/runtime_map.py`

**Telegram Runtime:**

- `lib/python/agents/ai_cto_scanner_agent.py`
- `lib/python/ai_cto_scanner/detectors.py`
- `lib/python/ai_cto_scanner/engine.py`
- `lib/python/ai_cto_scanner/report.py`
- `lib/python/ai_cto_scanner/scoring.py`
- `lib/python/executable_repository_intelligence/models.py`
- `lib/python/executable_repository_intelligence/report.py`
- `lib/python/executable_repository_intelligence/runtime_map.py`
- `lib/python/semantic_repository_intelligence/engine.py`
- `lib/python/semantic_repository_intelligence/models.py`

**Owner Runtime:**

- `lib/python/agents/ai_cto_scanner_agent.py`
- `lib/python/ai_cto_scanner/detectors.py`
- `lib/python/ai_cto_scanner/engine.py`
- `lib/python/ai_cto_scanner/report.py`
- `lib/python/ai_cto_scanner/scoring.py`
- `lib/python/executable_repository_intelligence/models.py`
- `lib/python/executable_repository_intelligence/report.py`
- `lib/python/executable_repository_intelligence/runtime_map.py`

**Admin Runtime:**

- `lib/python/ai_cto_scanner/detectors.py`
- `lib/python/ai_cto_scanner/report.py`
- `lib/python/executable_repository_intelligence/models.py`
- `lib/python/executable_repository_intelligence/report.py`
- `lib/python/executable_repository_intelligence/runtime_map.py`

**Persistence Runtime:**

- `lib/python/agents/ai_cto_scanner_agent.py`
- `lib/python/agents/repository_inspector_agent.py`
- `lib/python/ai_cto_scanner/detectors.py`
- `lib/python/ai_cto_scanner/engine.py`
- `lib/python/canonical_audit/engine.py`
- `lib/python/canonical_entities/models.py`
- `lib/python/canonical_intelligence/engine.py`
- `lib/python/cli/main.py`
- `lib/python/executable_repository_intelligence/engine.py`
- `lib/python/executable_repository_intelligence/runtime_map.py`
- `lib/python/repository_inspector_v2/engine.py`
- `lib/python/semantic_repository_intelligence/engine.py`
- `lib/python/session_runtime/runtime.py`

**Shutdown Hooks:**

- `lib/python/executable_repository_intelligence/models.py`
- `lib/python/executable_repository_intelligence/report.py`
- `lib/python/executable_repository_intelligence/runtime_map.py`
- `lib/python/semantic_repository_intelligence/injection_point_analyzer.py`

**Restart Hooks:**

- `lib/python/ai_cto_scanner/detectors.py`
- `lib/python/ai_cto_scanner/report.py`
- `lib/python/executable_repository_intelligence/models.py`
- `lib/python/executable_repository_intelligence/report.py`
- `lib/python/executable_repository_intelligence/runtime_map.py`
- `lib/python/semantic_repository_intelligence/injection_point_analyzer.py`

**Resume Hooks:**

- `lib/python/ai_cto_scanner/detectors.py`
- `lib/python/ai_cto_scanner/report.py`
- `lib/python/executable_repository_intelligence/models.py`
- `lib/python/executable_repository_intelligence/report.py`
- `lib/python/executable_repository_intelligence/runtime_map.py`

### Runtime Components

| Component | File | Role | Layer |
| --------- | ---- | ---- | ----- |
| __init__ | `lib/python/agent_runtime/__init__.py` | executable | Core |
| base | `lib/python/agent_runtime/base.py` | executable | Core |
| models | `lib/python/agent_runtime/models.py` | executable | Core |
| registry | `lib/python/agent_runtime/registry.py` | executable | Core |
| runtime | `lib/python/agent_runtime/runtime.py` | executable | Core |
| __init__ | `lib/python/agents/__init__.py` | executable | Core |
| ai_cto_scanner_agent | `lib/python/agents/ai_cto_scanner_agent.py` | telegram | Telegram |
| development_agent | `lib/python/agents/development_agent.py` | executable | Core |
| development_report | `lib/python/agents/development_report.py` | executable | Core |
| repository_inspector_agent | `lib/python/agents/repository_inspector_agent.py` | persistence | Persistence |
| __init__ | `lib/python/ai_cto_scanner/__init__.py` | executable | Core |
| detectors | `lib/python/ai_cto_scanner/detectors.py` | telegram | Telegram |
| engine | `lib/python/ai_cto_scanner/engine.py` | telegram | Telegram |
| report | `lib/python/ai_cto_scanner/report.py` | telegram | Telegram |
| scoring | `lib/python/ai_cto_scanner/scoring.py` | telegram | Telegram |
| __init__ | `lib/python/autonomous_planner/__init__.py` | executable | Core |
| engine | `lib/python/autonomous_planner/engine.py` | executable | Core |
| autonomous_workflow_engine | `lib/python/autonomous_workflow_engine.py` | executable | Core |
| __init__ | `lib/python/batch_generator/__init__.py` | executable | Core |
| engine | `lib/python/batch_generator/engine.py` | executable | Core |
| __init__ | `lib/python/batch_planner/__init__.py` | executable | Core |
| planner | `lib/python/batch_planner/planner.py` | executable | Core |
| __init__ | `lib/python/canonical_audit/__init__.py` | executable | Core |
| engine | `lib/python/canonical_audit/engine.py` | persistence | Persistence |
| __init__ | `lib/python/canonical_entities/__init__.py` | executable | Core |
| _…134 more_  | | | |


## File Classifications

All 257 repository files classified into canonical categories.

| Path | Category | Executable | Confidence |
| ---- | -------- | ---------- | ---------- |
| `.ai/batches/BATCH-001/checklist.md` | Documentation | ✗ | 0.90 |
| `.ai/batches/BATCH-001/implementation_plan.md` | Documentation | ✗ | 0.90 |
| `.ai/batches/BATCH-001/issue.md` | Documentation | ✗ | 0.90 |
| `.ai/batches/BATCH-001/metadata.json` | Configuration | ✗ | 0.70 |
| `.ai/batches/BATCH-001/pull_request.md` | Documentation | ✗ | 0.90 |
| `.ai/batches/BATCH-001/steps.json` | Configuration | ✗ | 0.70 |
| `.ai/batches/BATCH-002/checklist.md` | Documentation | ✗ | 0.90 |
| `.ai/batches/BATCH-002/implementation_plan.md` | Documentation | ✗ | 0.90 |
| `.ai/batches/BATCH-002/issue.md` | Documentation | ✗ | 0.90 |
| `.ai/batches/BATCH-002/metadata.json` | Configuration | ✗ | 0.70 |
| `.ai/batches/BATCH-002/pull_request.md` | Documentation | ✗ | 0.90 |
| `.ai/batches/BATCH-002/steps.json` | Configuration | ✗ | 0.70 |
| `.ai/executable_repository_map.json` | Configuration | ✗ | 0.70 |
| `.ai/execution_state.json` | Configuration | ✗ | 0.70 |
| `.ai/runtime_repository_model.json` | Configuration | ✗ | 0.70 |
| `.ai/semantic_knowledge.json` | Configuration | ✗ | 0.70 |
| `AI_CTO_EXECUTION_MODEL.md` | Reports | ✗ | 0.95 |
| `AI_CTO_INTEGRATION_REPORT.md` | Reports | ✗ | 0.95 |
| `README.md` | Documentation | ✗ | 0.90 |
| `audit/canon-001/CANON-001_REPORT.md` | Reports | ✗ | 0.85 |
| `development/BATCH-000_DEVELOPMENT_VALIDATOR_v1.0.md` | Documentation | ✗ | 0.90 |
| `development/BATCH-001_AUTONOMOUS_WORKFLOW_SYSTEM_v2.0.md` | Documentation | ✗ | 0.90 |
| `development/BATCH-002_SELF_KNOWLEDGE_SYSTEM_v1.0.md` | Documentation | ✗ | 0.90 |
| `docs/ROADMAP.md` | Documentation | ✗ | 0.90 |
| `docs/audits/CANON-AUDIT-001_CANONICAL_FOUNDATION_AUDIT_v1.0.0.md` | Canonical Specification | ✗ | 0.95 |
| `docs/audits/CORE-005_WORKSPACE_INDEX_IMPLEMENTATION.md` | Documentation | ✗ | 0.90 |
| `docs/audits/CORE-006_INCREMENTAL_WORKSPACE_INDEX.md` | Documentation | ✗ | 0.90 |
| `docs/audits/FOUNDATION_AUDIT_REPORT_v1.0.0.md` | Documentation | ✗ | 0.90 |
| `docs/canonical/AI_TOOLKIT_SYSTEM_ARCHITECTURE_v1.0.0.md` | Canonical Specification | ✗ | 0.95 |
| `docs/canonical/AUTONOMOUS_AGENT_SPEC_v1.0.0.md` | Canonical Specification | ✗ | 0.95 |
| `docs/canonical/AUTONOMOUS_WORKFLOW_SPEC_v1.0.0.md` | Canonical Specification | ✗ | 0.95 |
| `docs/canonical/CANON-001_AI_TOOLKIT_ARCHITECTURE_v2.0.md` | Canonical Specification | ✗ | 0.95 |
| `docs/canonical/CANON-002_DEVELOPMENT_WORKFLOW_v2.0.md` | Canonical Specification | ✗ | 0.95 |
| `docs/canonical/CANON-003_REPOSITORY_STANDARDS_v2.0.md` | Canonical Specification | ✗ | 0.95 |
| `docs/canonical/CANON-004_AI_AGENT_SPECIFICATION_v2.0.md` | Canonical Specification | ✗ | 0.95 |
| `docs/canonical/CANON-005_WORKSPACE_INDEX_SPECIFICATION_v2.0.md` | Canonical Specification | ✗ | 0.95 |
| `docs/canonical/CANON-006_OBSERVABILITY_SPECIFICATION_v2.0.md` | Canonical Specification | ✗ | 0.95 |
| `docs/canonical/CANON-007_AUTONOMOUS_EXECUTION_SPECIFICATION_v2.0.md` | Canonical Specification | ✗ | 0.95 |
| `docs/canonical/CANON-008_PERFORMANCE_BENCHMARK_SPECIFICATION_v2.0.md` | Canonical Specification | ✗ | 0.95 |
| `docs/canonical/CANON-009_TESTING_AND_VALIDATION_SPECIFICATION_v2.0.md` | Canonical Specification | ✗ | 0.95 |
| `docs/canonical/CANON-010_AI_TOOLKIT_ROADMAP_AND_EVOLUTION_v2.0.md` | Canonical Specification | ✗ | 0.95 |
| `docs/canonical/CANON-011_SYSTEM_INVARIANTS_v2.0.md` | Canonical Specification | ✗ | 0.95 |
| `docs/canonical/CANON-012_CANONICAL_INTELLIGENCE_SPECIFICATION_v1.0.0.md` | Canonical Specification | ✗ | 0.95 |
| `docs/canonical/CANON-013_CANONICAL_KNOWLEDGE_GRAPH_SPECIFICATION_v1.0.0.md` | Canonical Specification | ✗ | 0.95 |
| `docs/canonical/CANON-014_SEMANTIC_MATCHING_SPECIFICATION_v1.0.0.md` | Canonical Specification | ✗ | 0.95 |
| `docs/canonical/CANON-015_COVERAGE_AND_COMPLIANCE_SPECIFICATION_v1.0.0.md` | Canonical Specification | ✗ | 0.95 |
| `docs/canonical/CANON-016_ARCHITECTURE_DRIFT_SPECIFICATION_v1.0.0.md` | Canonical Specification | ✗ | 0.95 |
| `docs/canonical/CANON-017_INTELLIGENT_BATCH_PLANNING_SPECIFICATION_v1.0.0.md` | Canonical Specification | ✗ | 0.95 |
| `docs/canonical/CANON-018_CANONICAL_INTELLIGENCE_REPORTING_SPECIFICATION_v1.0.0.md` | Canonical Specification | ✗ | 0.95 |
| `docs/canonical/CANON-019_CANONICAL_VALIDATION_AND_GOVERNANCE_SPECIFICATION_v1.0.0.md` | Canonical Specification | ✗ | 0.95 |
| _…207 more files_ | | | |


## Executable Dependency Graph

Contains **only executable files**.  Documentation, generated artifacts, and reports are excluded.

| Metric | Value |
| ------ | ----- |
| Executable nodes | 160 |
| Executable edges | 201 |
| Excluded files | 97 |

### Dependency Edges (sample)

| Source | Target | Kind |
| ------ | ------ | ---- |
| `lib/python/agent_runtime/registry.py` | `lib/python/agent_runtime/runtime.py` | import |
| `lib/python/agent_runtime/registry.py` | `lib/python/agents/ai_cto_scanner_agent.py` | import |
| `lib/python/agent_runtime/registry.py` | `lib/python/agents/development_agent.py` | import |
| `lib/python/agents/ai_cto_scanner_agent.py` | `lib/python/agent_runtime/base.py` | import |
| `lib/python/agents/ai_cto_scanner_agent.py` | `lib/python/agent_runtime/models.py` | import |
| `lib/python/agents/ai_cto_scanner_agent.py` | `lib/python/ai_cto_scanner/engine.py` | import |
| `lib/python/agents/development_agent.py` | `lib/python/agent_runtime/base.py` | import |
| `lib/python/agents/development_agent.py` | `lib/python/agent_runtime/models.py` | import |
| `lib/python/agents/development_agent.py` | `lib/python/agents/development_report.py` | import |
| `lib/python/agents/development_agent.py` | `lib/python/autonomous_planner/engine.py` | import |
| `lib/python/agents/development_agent.py` | `lib/python/batch_generator/engine.py` | import |
| `lib/python/agents/development_agent.py` | `lib/python/canonical_audit/engine.py` | import |
| `lib/python/agents/development_agent.py` | `lib/python/dependency_engine/engine.py` | import |
| `lib/python/agents/development_agent.py` | `lib/python/execution_coordinator/engine.py` | import |
| `lib/python/agents/development_agent.py` | `lib/python/execution_engine/engine.py` | import |
| `lib/python/agents/development_agent.py` | `lib/python/github_materialization/engine.py` | import |
| `lib/python/agents/development_agent.py` | `lib/python/knowledge_graph_v2/engine.py` | import |
| `lib/python/agents/development_agent.py` | `lib/python/planning_engine/engine.py` | import |
| `lib/python/agents/development_agent.py` | `lib/python/profiler/engine.py` | import |
| `lib/python/agents/development_agent.py` | `lib/python/recommendation_engine/engine.py` | import |
| _…181 more_ | | |


## Injection Safety

| Safety Verdict | Count |
| -------------- | ----- |
| READ_ONLY | 1 |
| SAFE | 5 |
| SAFE_WITH_CONDITIONS | 43 |
| UNSAFE | 2 |

### ⚠ UNSAFE Injection Points

- **Event Bus** in `lib/python/semantic_repository_intelligence/injection_point_analyzer.py`: Injection point uses dynamic code execution (compile(). Arbitrary code may be injected.
- **Event Bus** in `lib/python/semantic_repository_intelligence/injection_point_analyzer.py`: Injection point uses dynamic code execution (compile(). Arbitrary code may be injected.

### ⚡ SAFE WITH CONDITIONS (43)

- **Dependency Injection Container** in `lib/python/agent_runtime/models.py`
- **Dependency Injection Container** in `lib/python/agent_runtime/models.py`
- **Dependency Injection Container** in `lib/python/agent_runtime/models.py`
- **Dependency Injection Container** in `lib/python/agent_runtime/models.py`
- **Service Registry** in `lib/python/agent_runtime/registry.py`
- **Service Registry** in `lib/python/agent_runtime/registry.py`
- **Service Registry** in `lib/python/agent_runtime/runtime.py`
- **Scheduled Task Hook** in `lib/python/ai_cto_scanner/detectors.py`
- **Dependency Injection Container** in `lib/python/canonical_entities/models.py`
- **Dependency Injection Container** in `lib/python/canonical_entities/models.py`


## Repository Zones

| Directory | Zone | Files |
| --------- | ---- | ----- |
| `.` | Generated | 3 |
| `.ai` | Generated | 4 |
| `.ai/batches/BATCH-001` | Generated | 6 |
| `.ai/batches/BATCH-002` | Generated | 6 |
| `audit/canon-001` | Generated | 1 |
| `development` | Documentation | 3 |
| `docs` | Documentation | 1 |
| `docs/audits` | Documentation | 4 |
| `docs/canonical` | Documentation | 64 |
| `docs/system-laws` | Documentation | 3 |
| `lib/python` | Runtime | 10 |
| `lib/python/agent_runtime` | Runtime | 5 |
| `lib/python/agents` | Runtime | 5 |
| `lib/python/ai_cto_scanner` | Runtime | 5 |
| `lib/python/autonomous_planner` | Runtime | 2 |
| `lib/python/batch_generator` | Runtime | 2 |
| `lib/python/batch_planner` | Runtime | 2 |
| `lib/python/canonical_audit` | Runtime | 2 |
| `lib/python/canonical_entities` | Runtime | 2 |
| `lib/python/canonical_intelligence` | Runtime | 2 |
| `lib/python/canonical_parser` | Runtime | 2 |
| `lib/python/canonical_repository` | Runtime | 2 |
| `lib/python/cli` | Runtime | 2 |
| `lib/python/common` | Runtime | 2 |
| `lib/python/compliance_engine` | Runtime | 2 |
| `lib/python/coverage_engine` | Runtime | 2 |
| `lib/python/dependency_engine` | Runtime | 4 |
| `lib/python/development_validator` | Runtime | 5 |
| `lib/python/discovery_engine` | Runtime | 2 |
| `lib/python/drift_engine` | Runtime | 2 |
| _…30 more_ | | |


## Recommendations

### 🟡 EXEC-REC-001 — Improve entry-point isolation

4 runtime entry points detected (lib/python/cli/main.py, lib/python/development_validator.py, lib/python/development_validator/main.py). Consider consolidating into a single well-defined entry point or clearly separating concerns between entry points.

**Evidence:**
- Entry points: lib/python/cli/main.py, lib/python/development_validator.py, lib/python/development_validator/main.py, lib/python/foundation_audit/main.py

**Affected files:** `lib/python/cli/main.py`, `lib/python/development_validator.py`, `lib/python/development_validator/main.py`, `lib/python/foundation_audit/main.py`

### 🔴 EXEC-REC-002 — Eliminate unsafe injection points

2 UNSAFE injection points detected in: lib/python/semantic_repository_intelligence/injection_point_analyzer.py. These use dynamic code execution (eval, exec, subprocess, etc.) which allows arbitrary code injection. Replace with safe, statically-typed alternatives.

**Evidence:**
- Event Bus — Injection point uses dynamic code execution (compile(). Arbitrary code may be injected.
- Event Bus — Injection point uses dynamic code execution (compile(). Arbitrary code may be injected.

**Affected files:** `lib/python/semantic_repository_intelligence/injection_point_analyzer.py`

### 🟡 EXEC-REC-003 — Reduce coupling in high-dependency executable modules

5 executable module(s) have high in-degree (≥5 dependents): lib/python/workspace_index/__init__.py, lib/python/semantic_repository_intelligence/models.py, lib/python/canonical_entities/__init__.py. Consider splitting these into smaller, more focused modules to reduce coupling and improve testability.

**Evidence:**
- lib/python/workspace_index/__init__.py: 13 dependents
- lib/python/semantic_repository_intelligence/models.py: 9 dependents
- lib/python/canonical_entities/__init__.py: 8 dependents

**Affected files:** `lib/python/workspace_index/__init__.py`, `lib/python/semantic_repository_intelligence/models.py`, `lib/python/canonical_entities/__init__.py`, `lib/python/executable_repository_intelligence/models.py`, `lib/python/agent_runtime/models.py`


# Repository Inventory

Generated: 2026-08-05T01:16:41.594319+00:00

## Executive Summary

| Metric | Value |
|-------|------:|
| Module Families Audited | 8 |
| Entrypoints | 3 |
| Legacy Shell Modules | 12 |
| Top-Level Directories | 14 |

Status: PHASE 1 IMPLEMENTATION AUDIT COMPLETE

## Architecture Map

- Standards layer: standards/csl
- Human documentation layer: docs, development, implementation-packages
- Runtime layer: lib/python/runtime
- Compiler/intelligence layer: canonical_*, engineering_engine, planning_engine, validation_engine, knowledge_graph*
- Agent/execution layer: agent_runtime, agents, autonomous_*
- Generated/runtime-state layer: .ai

Expected CSL reference architecture: Canonical Repository → CSL Parser → Semantic Analyzer → Universal Engineering Model → Validation Engine → Engineering Compiler → Artifact Generators → Safety & Governance Kernel → Runtime Integrations.

## Module Inventory

### runtime

- Path: `lib/python/runtime`
- Category: runtime
- Purpose: continuous runtime platform, HTTP/API, scheduler, lifecycle, recovery, secrets, metrics, integrations
- Current implementation status: comparatively mature
- CSL compliance: partial: runtime integrations are strong but not direct proof of CSL core conformance
- Reusable without changes: yes
- Requires refactoring: yes
- Must be replaced: no
- Missing interfaces: stronger auth/governance integration across endpoints
- Missing tests: end-to-end governance enforcement around external actions
- Missing documentation: explicit CSL integration role
- Dependencies: lib/python/runtime/interfaces, bin/runtime-server
- Risks: platform may outrun standard-core implementation maturity

### engineering_engine

- Path: `lib/python/engineering_engine`
- Category: compiler-orchestration
- Purpose: orchestration, audits, planning, GitHub/project automation, artifact generation
- Current implementation status: broad and active
- CSL compliance: low-to-partial: useful application layer but not a CSL compiler core
- Reusable without changes: no
- Requires refactoring: yes
- Must be replaced: no
- Missing interfaces: generator framework, repository adapter contracts, compiler boundary
- Missing tests: deterministic generation guarantees, traceability guarantees
- Missing documentation: subsystem boundaries
- Dependencies: lib/python/runtime, implementation-packages, bin/ai
- Risks: central monolith, responsibility overlap, hard to certify for conformance

### canonical_foundation

- Path: `lib/python/canonical_*`
- Category: csl-core-foundation
- Purpose: foundational CSL document ingestion and canonical analysis
- Current implementation status: implemented at basic document/section parsing level
- CSL compliance: Level 1-ish / partial Level 2 support only
- Reusable without changes: no
- Requires refactoring: yes
- Must be replaced: no
- Missing interfaces: source loader abstraction, AST model, diagnostics interface
- Missing tests: lexer tests, grammar tests, negative conformance tests
- Missing documentation: supported CSL subset, known limitations
- Dependencies: lib/python/canonical_entities
- Risks: current parser is markdown-section parser, not CSL grammar/parser

### validation_and_compliance

- Path: `lib/python/{validation_engine,compliance_engine,coverage_engine,drift_engine,evidence_engine}`
- Category: validation-compliance
- Purpose: validation, heuristic coverage/compliance scoring, drift and evidence reporting
- Current implementation status: present but partial
- CSL compliance: partial: not equivalent to mandated lexical/syntax/semantic/dependency/governance validation
- Reusable without changes: no
- Requires refactoring: yes
- Must be replaced: no
- Missing interfaces: validator pipeline contracts, formal conformance report contract, diagnostics/error-code alignment
- Missing tests: CSL conformance-driven validator tests
- Missing documentation: scoring semantics vs normative compliance
- Dependencies: lib/python/workspace_index, lib/python/semantic_matching
- Risks: heuristic reporting may overstate compliance

### graph_and_semantics

- Path: `lib/python/{knowledge_graph,knowledge_graph_v2,canonical_intelligence,semantic_matching}`
- Category: semantic-model
- Purpose: graph and semantic representation for downstream analysis
- Current implementation status: partially implemented and fragmented
- CSL compliance: partial support only; no explicit first-class Universal Engineering Model
- Reusable without changes: no
- Requires refactoring: yes
- Must be replaced: yes
- Missing interfaces: explicit Universal Engineering Model API
- Missing tests: semantic equivalence tests, deterministic model generation tests
- Missing documentation: single authoritative model boundary
- Dependencies: lib/python/canonical_entities, lib/python/semantic_engine
- Risks: version drift, duplicate graph semantics

### repository_intelligence

- Path: `lib/python/{semantic_repository_intelligence,executable_repository_intelligence,repository_engine,repository_inspector_v2}`
- Category: repository-adapter-analysis
- Purpose: repository analysis, intelligence, adapter-like scanning and recommendations
- Current implementation status: extensive
- CSL compliance: useful repository-adapter layer, not canonical core
- Reusable without changes: yes
- Requires refactoring: yes
- Must be replaced: no
- Missing interfaces: explicit repository adapter abstraction
- Missing tests: adapter/conformance boundary tests
- Missing documentation: relationship to CSL compiler pipeline
- Dependencies: lib/python/workspace_index, lib/python/semantic_engine
- Risks: repository-centric semantics instead of CSL-centric semantics

### governance_automation

- Path: `lib/python/{autonomous_execution_engine,autonomous_planning_engine,workspace_orchestrator,agent_runtime,agents,rule_engine}`
- Category: governance-automation
- Purpose: higher-order automation, orchestration, and policy/rule evaluation
- Current implementation status: active partial implementations
- CSL compliance: partial downstream capability; governance kernel incomplete
- Reusable without changes: no
- Requires refactoring: yes
- Must be replaced: no
- Missing interfaces: governance kernel hooks, approval/risk/permission contracts, audit/emergency-stop integration
- Missing tests: approval chain tests, policy enforcement tests, emergency stop tests
- Missing documentation: mandatory governance architecture mapping
- Dependencies: lib/python/runtime, lib/python/development_state_engine
- Risks: automation layer exists before mandatory governance kernel is formalized

### legacy_compatibility

- Path: `lib/*.sh and duplicated top-level lib/python/*.py modules`
- Category: legacy-compatibility
- Purpose: legacy utilities, entry modules, and compatibility shims
- Current implementation status: mixed
- CSL compliance: low
- Reusable without changes: no
- Requires refactoring: yes
- Must be replaced: yes
- Missing interfaces: canonical wrappers for retained compatibility paths
- Missing tests: consistent regression coverage for shims
- Missing documentation: deprecation and migration guidance
- Dependencies: bin/ai, lib/python packaged modules
- Risks: architectural duplication, migration drag, mixed import styles

## Dependency Graph

- CLI/bin → `lib/python/cli/engineering.py` → `lib/python/engineering_engine/*`
- runtime process → `lib/python/runtime/bootstrap.py` → runtime subsystems and interfaces
- canonical components → `canonical_repository` → `canonical_parser` → `canonical_entities`
- compliance path → `compliance_engine` → `workspace_index` + coverage/match inputs
- engineering pipeline → `pipeline.py` → repository audit + gap analysis + planning + package generation + validation + review

## Repository Structure Observations

- Top-level directories: .ai, .copilot, architecture-proposals, artifacts, audit, bin, development, docs, engineering-rules, implementation-packages, lib, standards, tests, tools
- Entrypoints: bin/ai, bin/ai.bak, bin/runtime-server
- Legacy shell modules: lib/context_engine.sh, lib/execution_engine.sh, lib/git_engine.sh, lib/github_engine.sh, lib/issue_engine.sh, lib/planner_engine.sh, lib/repository_inspector.sh, lib/repository_profile_engine.sh, lib/repository_summary.sh, lib/review_engine.sh, lib/work_engine.sh, lib/workspace_engine.sh
- Structural mismatch to RFC-0009: `knowledge/`, `generated/`, and a CSL-scoped `runtime/` top-level layout are not yet first-class repository directories.

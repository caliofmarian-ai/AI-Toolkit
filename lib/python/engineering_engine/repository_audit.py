from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path


@dataclass(slots=True)
class ModuleRecord:
    name: str
    path: str
    category: str
    purpose: str
    status: str
    csl_compliance: str
    reusable_without_changes: bool
    requires_refactoring: bool
    must_be_replaced: bool
    missing_interfaces: list[str] = field(default_factory=list)
    missing_tests: list[str] = field(default_factory=list)
    missing_documentation: list[str] = field(default_factory=list)
    dependencies: list[str] = field(default_factory=list)
    risks: list[str] = field(default_factory=list)


@dataclass(slots=True)
class AuditResult:
    modules: list[ModuleRecord]
    entrypoints: list[str]
    legacy_shell_modules: list[str]
    top_level_directories: list[str]


class RepositoryAudit:

    MODULE_FAMILIES = [
        {
            "name": "runtime",
            "path": "lib/python/runtime",
            "category": "runtime",
            "purpose": "continuous runtime platform, HTTP/API, scheduler, lifecycle, recovery, secrets, metrics, integrations",
            "status": "comparatively mature",
            "csl_compliance": "partial: runtime integrations are strong but not direct proof of CSL core conformance",
            "reusable_without_changes": True,
            "requires_refactoring": True,
            "must_be_replaced": False,
            "missing_interfaces": ["stronger auth/governance integration across endpoints"],
            "missing_tests": ["end-to-end governance enforcement around external actions"],
            "missing_documentation": ["explicit CSL integration role"],
            "dependencies": ["lib/python/runtime/interfaces", "bin/runtime-server"],
            "risks": ["platform may outrun standard-core implementation maturity"],
        },
        {
            "name": "engineering_engine",
            "path": "lib/python/engineering_engine",
            "category": "compiler-orchestration",
            "purpose": "orchestration, audits, planning, GitHub/project automation, artifact generation",
            "status": "broad and active",
            "csl_compliance": "low-to-partial: useful application layer but not a CSL compiler core",
            "reusable_without_changes": False,
            "requires_refactoring": True,
            "must_be_replaced": False,
            "missing_interfaces": ["generator framework", "repository adapter contracts", "compiler boundary"],
            "missing_tests": ["deterministic generation guarantees", "traceability guarantees"],
            "missing_documentation": ["subsystem boundaries"],
            "dependencies": ["lib/python/runtime", "implementation-packages", "bin/ai"],
            "risks": ["central monolith", "responsibility overlap", "hard to certify for conformance"],
        },
        {
            "name": "canonical_foundation",
            "path": "lib/python/canonical_*",
            "category": "csl-core-foundation",
            "purpose": "foundational CSL document ingestion and canonical analysis",
            "status": "implemented at basic document/section parsing level",
            "csl_compliance": "Level 1-ish / partial Level 2 support only",
            "reusable_without_changes": False,
            "requires_refactoring": True,
            "must_be_replaced": False,
            "missing_interfaces": ["source loader abstraction", "AST model", "diagnostics interface"],
            "missing_tests": ["lexer tests", "grammar tests", "negative conformance tests"],
            "missing_documentation": ["supported CSL subset", "known limitations"],
            "dependencies": ["lib/python/canonical_entities"],
            "risks": ["current parser is markdown-section parser, not CSL grammar/parser"],
        },
        {
            "name": "validation_and_compliance",
            "path": "lib/python/{validation_engine,compliance_engine,coverage_engine,drift_engine,evidence_engine}",
            "category": "validation-compliance",
            "purpose": "validation, heuristic coverage/compliance scoring, drift and evidence reporting",
            "status": "present but partial",
            "csl_compliance": "partial: not equivalent to mandated lexical/syntax/semantic/dependency/governance validation",
            "reusable_without_changes": False,
            "requires_refactoring": True,
            "must_be_replaced": False,
            "missing_interfaces": ["validator pipeline contracts", "formal conformance report contract", "diagnostics/error-code alignment"],
            "missing_tests": ["CSL conformance-driven validator tests"],
            "missing_documentation": ["scoring semantics vs normative compliance"],
            "dependencies": ["lib/python/workspace_index", "lib/python/semantic_matching"],
            "risks": ["heuristic reporting may overstate compliance"],
        },
        {
            "name": "graph_and_semantics",
            "path": "lib/python/{knowledge_graph,knowledge_graph_v2,canonical_intelligence,semantic_matching}",
            "category": "semantic-model",
            "purpose": "graph and semantic representation for downstream analysis",
            "status": "partially implemented and fragmented",
            "csl_compliance": "partial support only; no explicit first-class Universal Engineering Model",
            "reusable_without_changes": False,
            "requires_refactoring": True,
            "must_be_replaced": True,
            "missing_interfaces": ["explicit Universal Engineering Model API"],
            "missing_tests": ["semantic equivalence tests", "deterministic model generation tests"],
            "missing_documentation": ["single authoritative model boundary"],
            "dependencies": ["lib/python/canonical_entities", "lib/python/semantic_engine"],
            "risks": ["version drift", "duplicate graph semantics"],
        },
        {
            "name": "repository_intelligence",
            "path": "lib/python/{semantic_repository_intelligence,executable_repository_intelligence,repository_engine,repository_inspector_v2}",
            "category": "repository-adapter-analysis",
            "purpose": "repository analysis, intelligence, adapter-like scanning and recommendations",
            "status": "extensive",
            "csl_compliance": "useful repository-adapter layer, not canonical core",
            "reusable_without_changes": True,
            "requires_refactoring": True,
            "must_be_replaced": False,
            "missing_interfaces": ["explicit repository adapter abstraction"],
            "missing_tests": ["adapter/conformance boundary tests"],
            "missing_documentation": ["relationship to CSL compiler pipeline"],
            "dependencies": ["lib/python/workspace_index", "lib/python/semantic_engine"],
            "risks": ["repository-centric semantics instead of CSL-centric semantics"],
        },
        {
            "name": "governance_automation",
            "path": "lib/python/{autonomous_execution_engine,autonomous_planning_engine,workspace_orchestrator,agent_runtime,agents,rule_engine}",
            "category": "governance-automation",
            "purpose": "higher-order automation, orchestration, and policy/rule evaluation",
            "status": "active partial implementations",
            "csl_compliance": "partial downstream capability; governance kernel incomplete",
            "reusable_without_changes": False,
            "requires_refactoring": True,
            "must_be_replaced": False,
            "missing_interfaces": ["governance kernel hooks", "approval/risk/permission contracts", "audit/emergency-stop integration"],
            "missing_tests": ["approval chain tests", "policy enforcement tests", "emergency stop tests"],
            "missing_documentation": ["mandatory governance architecture mapping"],
            "dependencies": ["lib/python/runtime", "lib/python/development_state_engine"],
            "risks": ["automation layer exists before mandatory governance kernel is formalized"],
        },
        {
            "name": "legacy_compatibility",
            "path": "lib/*.sh and duplicated top-level lib/python/*.py modules",
            "category": "legacy-compatibility",
            "purpose": "legacy utilities, entry modules, and compatibility shims",
            "status": "mixed",
            "csl_compliance": "low",
            "reusable_without_changes": False,
            "requires_refactoring": True,
            "must_be_replaced": True,
            "missing_interfaces": ["canonical wrappers for retained compatibility paths"],
            "missing_tests": ["consistent regression coverage for shims"],
            "missing_documentation": ["deprecation and migration guidance"],
            "dependencies": ["bin/ai", "lib/python packaged modules"],
            "risks": ["architectural duplication", "migration drag", "mixed import styles"],
        },
    ]

    def __init__(self, repository_root: Path):
        self.root = repository_root

    def run(self) -> AuditResult:
        top_level_directories = sorted(
            p.name for p in self.root.iterdir() if p.is_dir() and not p.name.startswith('.git')
        )
        entrypoints = sorted(
            str(p.relative_to(self.root))
            for p in (self.root / 'bin').glob('*')
            if p.is_file()
        )
        legacy_shell_modules = sorted(
            str(p.relative_to(self.root))
            for p in (self.root / 'lib').glob('*.sh')
            if p.is_file()
        )
        modules = [ModuleRecord(**item) for item in self.MODULE_FAMILIES]
        return AuditResult(
            modules=modules,
            entrypoints=entrypoints,
            legacy_shell_modules=legacy_shell_modules,
            top_level_directories=top_level_directories,
        )

    def write_markdown(self, output: Path):
        result = self.run()
        output.parent.mkdir(parents=True, exist_ok=True)

        with output.open('w', encoding='utf-8') as md:
            md.write('# Repository Inventory

')
            md.write(f'Generated: {datetime.now(UTC).isoformat()}

')

            md.write('## Executive Summary

')
            md.write('| Metric | Value |
')
            md.write('|-------|------:|
')
            md.write(f'| Module Families Audited | {len(result.modules)} |
')
            md.write(f'| Entrypoints | {len(result.entrypoints)} |
')
            md.write(f'| Legacy Shell Modules | {len(result.legacy_shell_modules)} |
')
            md.write(f'| Top-Level Directories | {len(result.top_level_directories)} |

')
            md.write('Status: PHASE 1 IMPLEMENTATION AUDIT COMPLETE

')

            md.write('## Architecture Map

')
            md.write('- Standards layer: standards/csl
')
            md.write('- Human documentation layer: docs, development, implementation-packages
')
            md.write('- Runtime layer: lib/python/runtime
')
            md.write('- Compiler/intelligence layer: canonical_*, engineering_engine, planning_engine, validation_engine, knowledge_graph*
')
            md.write('- Agent/execution layer: agent_runtime, agents, autonomous_*
')
            md.write('- Generated/runtime-state layer: .ai

')
            md.write('Expected CSL reference architecture: Canonical Repository → CSL Parser → Semantic Analyzer → Universal Engineering Model → Validation Engine → Engineering Compiler → Artifact Generators → Safety & Governance Kernel → Runtime Integrations.

')

            md.write('## Module Inventory

')
            for module in result.modules:
                md.write(f'### {module.name}

')
                md.write(f'- Path: `{module.path}`
')
                md.write(f'- Category: {module.category}
')
                md.write(f'- Purpose: {module.purpose}
')
                md.write(f'- Current implementation status: {module.status}
')
                md.write(f'- CSL compliance: {module.csl_compliance}
')
                md.write(f'- Reusable without changes: {"yes" if module.reusable_without_changes else "no"}
')
                md.write(f'- Requires refactoring: {"yes" if module.requires_refactoring else "no"}
')
                md.write(f'- Must be replaced: {"yes" if module.must_be_replaced else "no"}
')
                md.write(f'- Missing interfaces: {", ".join(module.missing_interfaces) if module.missing_interfaces else "none"}
')
                md.write(f'- Missing tests: {", ".join(module.missing_tests) if module.missing_tests else "none"}
')
                md.write(f'- Missing documentation: {", ".join(module.missing_documentation) if module.missing_documentation else "none"}
')
                md.write(f'- Dependencies: {", ".join(module.dependencies) if module.dependencies else "none"}
')
                md.write(f'- Risks: {", ".join(module.risks) if module.risks else "none"}

')

            md.write('## Dependency Graph

')
            md.write('- CLI/bin → `lib/python/cli/engineering.py` → `lib/python/engineering_engine/*`
')
            md.write('- runtime process → `lib/python/runtime/bootstrap.py` → runtime subsystems and interfaces
')
            md.write('- canonical components → `canonical_repository` → `canonical_parser` → `canonical_entities`
')
            md.write('- compliance path → `compliance_engine` → `workspace_index` + coverage/match inputs
')
            md.write('- engineering pipeline → `pipeline.py` → repository audit + gap analysis + planning + package generation + validation + review

')

            md.write('## Repository Structure Observations

')
            md.write(f'- Top-level directories: {", ".join(result.top_level_directories)}
')
            md.write(f'- Entrypoints: {", ".join(result.entrypoints)}
')
            md.write(f'- Legacy shell modules: {", ".join(result.legacy_shell_modules)}
')
            md.write('- Structural mismatch to RFC-0009: `knowledge/`, `generated/`, and a CSL-scoped `runtime/` top-level layout are not yet first-class repository directories.
')

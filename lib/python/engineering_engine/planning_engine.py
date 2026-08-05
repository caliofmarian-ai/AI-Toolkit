from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from lib.python.engineering_engine.gap_analysis import GapAnalysis


@dataclass(slots=True)
class PlanningBatch:
    id: str
    title: str
    priority: str
    status: str
    risk: str
    rationale: str
    affected_modules: list[str]
    objective: str
    suggested_tests: list[str]


class PlanningEngine:

    def __init__(self, root: Path):
        self.root = root

    def plan(self, core: str):
        gaps = GapAnalysis(self.root).analyse()
        batch_specs = [
            ('Define authoritative CSL subsystem architecture', 'CRITICAL', 'HIGH', 'Define the official subsystem map: source loader, parser, semantic analyzer, UEM, validator, compiler, generators, governance kernel, repository adapters, runtime integrations.', ['lib/python/canonical_parser', 'lib/python/canonical_repository', 'lib/python/engineering_engine']),
            ('Inventory and classify modules', 'HIGH', 'MEDIUM', 'Classify every existing module into keep/refactor/replace/deprecate and freeze legacy modules as compatibility-only.', ['lib/python', 'lib/*.sh', 'bin']),
            ('Publish formal compliance declaration', 'HIGH', 'MEDIUM', 'Create the supported feature declaration, conformance statement, known limitations register, and deviation register.', ['docs', 'standards/csl', 'implementation-packages']),
            ('Build canonical source loader and parser boundary', 'CRITICAL', 'HIGH', 'Replace the markdown-section parser approach with a real CSL lexical/syntax parsing boundary and diagnostics contract.', ['lib/python/canonical_parser', 'lib/python/canonical_entities']),
            ('Add AST, semantic analysis, and UEM', 'CRITICAL', 'HIGH', 'Introduce first-class AST, semantic analyzer, and Universal Engineering Model subsystems.', ['lib/python/canonical_entities', 'lib/python/knowledge_graph', 'lib/python/knowledge_graph_v2', 'lib/python/canonical_intelligence']),
            ('Rework validation to normative CSL categories', 'CRITICAL', 'HIGH', 'Implement lexical, syntax, semantic, relationship, constraint, dependency, governance, and safety validation with deterministic diagnostics.', ['lib/python/validation_engine', 'lib/python/compliance_engine']),
            ('Reframe audit and planning outputs as generators', 'HIGH', 'MEDIUM', 'Move existing audit/planning/report engines behind compiler/UEM-driven generator contracts.', ['lib/python/engineering_engine', 'implementation-packages']),
            ('Consolidate duplicate graph and engine subsystems', 'HIGH', 'HIGH', 'Collapse overlapping graph, planning, execution, and validation abstractions around the authoritative CSL core.', ['lib/python/engineering_engine', 'lib/python/autonomous_*', 'lib/python/workspace_*']),
            ('Implement governance kernel', 'CRITICAL', 'HIGH', 'Promote rule/policy pieces into mandatory permission, risk, approval, audit, authorization, and emergency-stop services.', ['lib/python/rule_engine', 'lib/python/autonomous_execution_engine', 'lib/python/runtime']),
            ('Align repository structure with RFC-0009', 'HIGH', 'MEDIUM', 'Introduce canonical separation for knowledge, generated outputs, runtime assets, and implementation responsibilities.', ['.', '.ai', 'docs', 'implementation-packages']),
            ('Remap tests to CSL conformance levels', 'HIGH', 'MEDIUM', 'Map and expand tests to core reader, validator, compiler, reference implementation, and platform conformance categories.', ['tests', 'standards/csl/tests']),
            ('Publish Phase 1 status and migration path', 'MEDIUM', 'LOW', 'Publish conformance status, supported/unsupported capabilities, known limitations, and migration guidance.', ['docs', 'implementation-packages']),
        ]

        batches = []
        for index, spec in enumerate(batch_specs, start=1):
            title, priority, risk, rationale, affected = spec
            status = 'READY' if index <= 3 else 'PLANNED'
            missing_components = [item.component for item in gaps if item.status == 'MISSING']
            if any(keyword in title.lower() for keyword in ['parser', 'validation', 'governance', 'compliance']):
                touched = [component for component in missing_components if component.lower() in title.lower() or component.lower() in rationale.lower()]
                if touched:
                    rationale = f"{rationale} Missing components addressed: {', '.join(sorted(touched))}."
            batches.append(
                PlanningBatch(
                    id=f'{core}-{index:03d}',
                    title=title,
                    priority=priority,
                    status=status,
                    risk=risk,
                    rationale=rationale,
                    affected_modules=affected,
                    objective=title,
                    suggested_tests=[
                        'tests/test_canonical_parser.sh',
                        'tests/test_compliance_engine.sh',
                        'tests/test_validation_engine.sh',
                    ],
                )
            )
        return batches

    def write_markdown(self, core: str):
        package = self.root / 'implementation-packages' / core
        package.mkdir(parents=True, exist_ok=True)
        report = package / 'planning-report.md'
        batches = self.plan(core)

        with report.open('w', encoding='utf-8') as md:
            md.write('# Phase 1 Implementation Roadmap\n\n')
            md.write(f'CORE: {core}\n\n')
            md.write('## Refactoring Plan\n\n')
            md.write('- Phase A: establish canonical implementation boundaries.\n')
            md.write('- Phase B: normalize repository structure to CSL.\n')
            md.write('- Phase C: consolidate duplicate engines and graph implementations.\n')
            md.write('- Phase D: implement compliance infrastructure.\n')
            md.write('- Phase E: harden governance kernel.\n')
            md.write('- Phase F: realign tests to CSL conformance levels.\n\n')
            md.write('## Ordered Implementation Plan\n\n')
            md.write('| Batch | Status | Risk | Priority | Affected |\n')
            md.write('|-------|--------|------|----------|----------|\n')
            for batch in batches:
                md.write(f"| {batch.id} | {batch.status} | {batch.risk} | {batch.priority} | {', '.join(batch.affected_modules)} |\n")
            md.write('\n## Details\n\n')
            for batch in batches:
                md.write(f'### {batch.id}\n\n')
                md.write(f'Objective: {batch.title}\n\n')
                md.write(f'Status: {batch.status}\n\n')
                md.write(f'Risk: {batch.risk}\n\n')
                md.write(f'Priority: {batch.priority}\n\n')
                md.write(f'Affected modules: {", ".join(batch.affected_modules)}\n\n')
                md.write(f'Reason: {batch.rationale}\n\n')
                md.write(f'Suggested tests: {", ".join(batch.suggested_tests)}\n\n')
        return report

    def build_package_model(self, core: str):
        return self.plan(core)

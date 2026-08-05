from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from lib.python.engineering_engine.repository_audit import RepositoryAudit


@dataclass(slots=True)
class GapItem:
    component: str
    status: str
    evidence: str


class GapAnalysis:

    def __init__(self, root: Path):
        self.root = root

    def analyse(self):
        audit = RepositoryAudit(self.root).run()
        return [
            GapItem('Canonical Repository', 'PARTIAL', 'Foundational canonical modules exist but provide only basic document ingestion'),
            GapItem('CSL Parser', 'MISSING', 'Current parser is a markdown section parser, not a CSL grammar/parser'),
            GapItem('Semantic Analyzer', 'MISSING', 'Semantic analysis is fragmented across intelligence modules, not unified as a CSL semantic analyzer'),
            GapItem('Universal Engineering Model', 'MISSING', 'No explicit first-class UEM API is published'),
            GapItem('Validation Engine', 'PARTIAL', 'Validation exists but does not implement mandated lexical/syntax/semantic/dependency/governance stack'),
            GapItem('Engineering Compiler', 'MISSING', 'No deterministic end-to-end CSL compiler pipeline is present'),
            GapItem('Artifact Generators', 'PARTIAL', 'Generators exist in planning/reporting/package modules but are not compiler-driven outputs from a UEM'),
            GapItem('Safety and Governance Kernel', 'MISSING', 'Rule/policy components exist without a single mandatory permission/risk/approval/audit/emergency-stop kernel'),
            GapItem('Runtime Integrations', 'IMPLEMENTED', 'Runtime subsystem is comparatively mature and aligned to integration/platform concerns'),
            GapItem('Repository Structure RFC-0009 Alignment', 'MISSING', 'Repository lacks first-class knowledge/, generated/, and canonical runtime/ structure separation'),
            GapItem('Conformance Publication', 'MISSING', 'Supported level, unsupported features, limitations, and compatibility statement are not formally published'),
            GapItem('Legacy Compatibility Isolation', 'MISSING', f'{len(audit.legacy_shell_modules)} legacy shell modules and duplicated top-level Python modules still contribute to architectural drift'),
        ]

    def write_markdown(self, output: Path):
        output.parent.mkdir(parents=True, exist_ok=True)
        results = self.analyse()

        with output.open('w', encoding='utf-8') as md:
            md.write('# CSL Compliance Matrix\n\n')
            md.write(f'Generated: {datetime.now(UTC).isoformat()}\n\n')
            md.write('| Component | Status | Evidence |\n')
            md.write('|-----------|--------|----------|\n')
            for item in results:
                md.write(f'| {item.component} | {item.status} | {item.evidence} |\n')

            summary = {status: sum(1 for item in results if item.status == status) for status in ['IMPLEMENTED', 'PARTIAL', 'MISSING']}
            md.write('\n## Summary\n\n')
            md.write(f"- Implemented: {summary.get('IMPLEMENTED', 0)}\n")
            md.write(f"- Partial: {summary.get('PARTIAL', 0)}\n")
            md.write(f"- Missing: {summary.get('MISSING', 0)}\n\n")
            md.write('## Repository-wide Findings\n\n')
            md.write('- Strongest areas: runtime platform, repository scanning/intelligence, audit/planning/report generation, test volume.\n')
            md.write('- Weakest areas: true CSL grammar/parser, AST, explicit semantic analysis, first-class UEM, deterministic compiler pipeline, diagnostics/error-code registry, generator framework, formal conformance declaration, governance kernel completeness.\n')
            md.write('- Primary risks: architectural drift, duplicated subsystems, heuristic compliance being mistaken for normative conformance, missing UEM, incomplete governance, non-canonical repository structure.\n')

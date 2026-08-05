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
        results = []

        results.append(GapItem(
            component='Canonical Repository',
            status='PARTIAL',
            evidence='Foundational canonical modules exist but provide only basic document ingestion',
        ))
        results.append(GapItem(
            component='CSL Parser',
            status='MISSING',
            evidence='Current parser is a markdown section parser, not a CSL grammar/parser',
        ))
        results.append(GapItem(
            component='Semantic Analyzer',
            status='MISSING',
            evidence='Semantic analysis is fragmented across intelligence modules, not unified as a CSL semantic analyzer',
        ))
        results.append(GapItem(
            component='Universal Engineering Model',
            status='MISSING',
            evidence='No explicit first-class UEM API is published',
        ))
        results.append(GapItem(
            component='Validation Engine',
            status='PARTIAL',
            evidence='Validation exists but does not implement mandated lexical/syntax/semantic/dependency/governance stack',
        ))
        results.append(GapItem(
            component='Engineering Compiler',
            status='MISSING',
            evidence='No deterministic end-to-end CSL compiler pipeline is present',
        ))
        results.append(GapItem(
            component='Artifact Generators',
            status='PARTIAL',
            evidence='Generators exist in planning/reporting/package modules but are not compiler-driven outputs from a UEM',
        ))
        results.append(GapItem(
            component='Safety and Governance Kernel',
            status='MISSING',
            evidence='Rule/policy components exist without a single mandatory permission/risk/approval/audit/emergency-stop kernel',
        ))
        results.append(GapItem(
            component='Runtime Integrations',
            status='IMPLEMENTED',
            evidence='Runtime subsystem is comparatively mature and aligned to integration/platform concerns',
        ))
        results.append(GapItem(
            component='Repository Structure RFC-0009 Alignment',
            status='MISSING',
            evidence='Repository lacks first-class knowledge/, generated/, and canonical runtime/ structure separation',
        ))
        results.append(GapItem(
            component='Conformance Publication',
            status='MISSING',
            evidence='Supported level, unsupported features, limitations, and compatibility statement are not formally published',
        ))
        results.append(GapItem(
            component='Legacy Compatibility Isolation',
            status='MISSING',
            evidence=f'{len(audit.legacy_shell_modules)} legacy shell modules and duplicated top-level Python modules still contribute to architectural drift',
        ))
        return results

    def write_markdown(self, output: Path):
        output.parent.mkdir(parents=True, exist_ok=True)
        results = self.analyse()

        with output.open('w', encoding='utf-8') as md:
            md.write('# CSL Compliance Matrix

')
            md.write(f'Generated: {datetime.now(UTC).isoformat()}

')
            md.write('| Component | Status | Evidence |
')
            md.write('|-----------|--------|----------|
')
            for item in results:
                md.write(f'| {item.component} | {item.status} | {item.evidence} |
')

            summary = {status: sum(1 for item in results if item.status == status) for status in ['IMPLEMENTED', 'PARTIAL', 'MISSING']}
            md.write('
## Summary

')
            md.write(f"- Implemented: {summary.get('IMPLEMENTED', 0)}
")
            md.write(f"- Partial: {summary.get('PARTIAL', 0)}
")
            md.write(f"- Missing: {summary.get('MISSING', 0)}

")
            md.write('## Repository-wide Findings

')
            md.write('- Strongest areas: runtime platform, repository scanning/intelligence, audit/planning/report generation, test volume.
')
            md.write('- Weakest areas: true CSL grammar/parser, AST, explicit semantic analysis, first-class UEM, deterministic compiler pipeline, diagnostics/error-code registry, generator framework, formal conformance declaration, governance kernel completeness.
')
            md.write('- Primary risks: architectural drift, duplicated subsystems, heuristic compliance being mistaken for normative conformance, missing UEM, incomplete governance, non-canonical repository structure.
')

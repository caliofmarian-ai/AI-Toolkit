# CSL Compliance Matrix

Generated: 2026-08-05T01:16:41.595396+00:00

| Component | Status | Evidence |
|-----------|--------|----------|
| Canonical Repository | PARTIAL | Foundational canonical modules exist but provide only basic document ingestion |
| CSL Parser | MISSING | Current parser is a markdown section parser, not a CSL grammar/parser |
| Semantic Analyzer | MISSING | Semantic analysis is fragmented across intelligence modules, not unified as a CSL semantic analyzer |
| Universal Engineering Model | MISSING | No explicit first-class UEM API is published |
| Validation Engine | PARTIAL | Validation exists but does not implement mandated lexical/syntax/semantic/dependency/governance stack |
| Engineering Compiler | MISSING | No deterministic end-to-end CSL compiler pipeline is present |
| Artifact Generators | PARTIAL | Generators exist in planning/reporting/package modules but are not compiler-driven outputs from a UEM |
| Safety and Governance Kernel | MISSING | Rule/policy components exist without a single mandatory permission/risk/approval/audit/emergency-stop kernel |
| Runtime Integrations | IMPLEMENTED | Runtime subsystem is comparatively mature and aligned to integration/platform concerns |
| Repository Structure RFC-0009 Alignment | MISSING | Repository lacks first-class knowledge/, generated/, and canonical runtime/ structure separation |
| Conformance Publication | MISSING | Supported level, unsupported features, limitations, and compatibility statement are not formally published |
| Legacy Compatibility Isolation | MISSING | 12 legacy shell modules and duplicated top-level Python modules still contribute to architectural drift |

## Summary

- Implemented: 1
- Partial: 3
- Missing: 8

## Repository-wide Findings

- Strongest areas: runtime platform, repository scanning/intelligence, audit/planning/report generation, test volume.
- Weakest areas: true CSL grammar/parser, AST, explicit semantic analysis, first-class UEM, deterministic compiler pipeline, diagnostics/error-code registry, generator framework, formal conformance declaration, governance kernel completeness.
- Primary risks: architectural drift, duplicated subsystems, heuristic compliance being mistaken for normative conformance, missing UEM, incomplete governance, non-canonical repository structure.

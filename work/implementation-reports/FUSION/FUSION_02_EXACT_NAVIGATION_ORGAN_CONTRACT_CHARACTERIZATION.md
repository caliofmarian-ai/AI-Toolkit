# FUSION-02 — Exact Navigation Organ Contract Characterization

## Starting Authority

bb8e3257d4d8ddf38ec1c55c7d3ac9a37b34d987

## Purpose

Determine the exact demonstrated repository organ contracts for the next read-only cognitive navigation capability before any production mutation.

This characterization exists specifically to prevent capability-name matching from being mistaken for physiological compatibility.

## Conserved Physiology

HUMAN RAW SOURCE
→ INFORMATION NEED
→ NEED EVALUATION
→ NAVIGATION PLAN
→ OPTIONAL READ-ONLY SEARCH
→ RETRIEVED CANDIDATE EVIDENCE
→ BOUNDED WORKING CONTEXT
→ LEGACY CONVERSATION CONTEXT
→ PROVIDER COGNITIVE CONTEXT
→ PROVIDER

## Conserved Invariants

- Search is already implemented and must not be duplicated.
- Working Context is already implemented and must not be duplicated.
- Retrieval does not confer epistemic authority.
- Human authority remains preserved.
- UNKNOWN remains a legitimate epistemic outcome.
- Navigation remains read-only.
- Repository-relative source identity remains preserved.
- Full repository state must not silently become Working Context.
- CDM/CSS Knowledge Materialization remains separate.
- No CSL mutation is authorized.
- No UEM mutation is authorized.

## Critical Audit Finding

A matching method name is not sufficient evidence that an existing organ satisfies a cognitive navigation contract.

Capability-name equality does not establish physiological equivalence.

## RepositoryInspectorV2.inspect

Demonstrated contract:

- accepts repository-root state through the inspector instance
- gathers repository statistics
- gathers dependency statistics
- gathers validation statistics
- builds a repository plan
- evaluates repository health
- returns a repository-wide report
- demonstrated read-only in isolated runtime characterization

Therefore RepositoryInspectorV2.inspect is a real inspection organ, but it is repository-wide inspection.

It is not demonstrated as a bounded reader or inspector of the source identities selected into Working Context.

Directly wiring it into Working Context as source inspection is NOT AUTHORIZED by this characterization.

## Epistemic Transformation Organ

The existing epistemic Transformation anatomy contains its own inspection and reference-resolution physiology.

Those semantics belong to Transformation artifacts and epistemic relations and must not be silently generalized into repository-source inspection.

## Candidate Contracts

### lib/python/repository_inspector_v2/engine.py

- method: `inspect`
- line: 21
- arguments: `self`

### lib/python/epistemic/transformation.py

- method: `resolve_reference`
- line: 597
- arguments: `self`, `reference`

### lib/python/epistemic/transformation.py

- method: `inspect`
- line: 635
- arguments: `self`, `identifier`

### lib/python/engineering_engine/github_repository_resolver.py

- method: `resolve`
- line: 15
- arguments: `self`

### lib/python/engineering_engine/import_resolver.py

- method: `resolve`
- line: 21
- arguments: `self`, `imported`

### lib/python/semantic_repository_intelligence/import_graph.py

- method: `resolve`
- line: 29
- arguments: `self`, `source_path`, `module`, `level`

### lib/python/semantic_repository_intelligence/relationship_resolver.py

- method: `resolve_import`
- line: 41
- arguments: `self`, `source_path`, `module`, `level`

### lib/python/semantic_repository_intelligence/relationship_resolver.py

- method: `resolve_symbol`
- line: 79
- arguments: `self`, `qualified_name`

### lib/python/executable_repository_intelligence/runtime_map.py

- method: `_read_text`
- line: 61
- arguments: `root`, `path_str`

### lib/python/semantic_matching/matcher.py

- method: `_read_file`
- line: 204
- arguments: `self`, `relative_path`

## Exact Architectural Consequence

The next cognitive navigation mutation must not be selected by method name alone.

Any INSPECT integration must demonstrate an explicit boundary between:

1. the bounded source identities already selected into Working Context,
2. the repository organ performing inspection,
3. the inspection result returned as candidate evidence,
4. the Journey state recording epistemic gain or absence of gain.

The integration must not inject an entire repository profile into Working Context by default.

## Capability State After Characterization

- search: IMPLEMENTED
- Working Context: IMPLEMENTED
- inspect: REQUIRED BUT EXACT COGNITIVE CONTRACT NOT YET IMPLEMENTED
- resolve: REQUIRED BUT NOT IMPLEMENTED
- read: REQUIRED BUT NOT IMPLEMENTED
- provenance: NOT YET MATERIALIZED AS FULL COGNITIVE PROVENANCE
- journey traversal: SEARCH STEP ONLY

## Selection Verdict

INSPECT remains the first structural capability candidate.

However RepositoryInspectorV2.inspect must NOT be directly treated as bounded source inspection.

The smallest safe next production mutation is an explicit read-only INSPECT navigation boundary whose input and output contracts are independently demonstrated before service-level integration.

The mutation must reuse existing organs where their contracts actually match and must not create duplicate physiology.

## Production Mutation

NONE

## Canon Mutation

NONE

## CSL Mutation

NONE

## UEM Mutation

NONE

## Knowledge Materialization Mutation

NONE

## Next Authorized Stage

DIRECT GITHUB AUDIT OF THIS EXACT ORGAN CONTRACT CHARACTERIZATION.

THEN CHARACTERIZE THE SMALLEST BOUNDED READ-ONLY INSPECT NAVIGATION INPUT/OUTPUT CONTRACT.

NO SERVICE INTEGRATION UNTIL THAT CONTRACT IS DEMONSTRATED.

## Generated

2026-08-17T21:57:35.263058+00:00

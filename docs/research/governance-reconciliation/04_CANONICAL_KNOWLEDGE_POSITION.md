# Canonical Knowledge Position
Version: 1.0.0
Status: Draft
Classification: Engineering Research Reference

## REPOSITORY FACT
Canonical Knowledge is treated as the highest or authoritative engineering source in both the CSL standard and the AI-Toolkit repository structure. [Source: standards/csl/CSL_CONSTITUTION.md:29-47; knowledge/README.md:13-31]

## REPOSITORY EVIDENCE
### 1. Canonical Knowledge is the highest engineering authority in CSL
The Constitution states:
> "Canonical Knowledge is the highest engineering authority." [Source: standards/csl/CSL_CONSTITUTION.md:29-47]

It further states that every engineering artifact derives authority exclusively from Canonical Knowledge and that lower layers may not redefine higher layers. [Source: standards/csl/CSL_CONSTITUTION.md:45-47, 133-172]

The Manifesto reinforces the same ordering:
- "Knowledge First."
- "Canonical Before Implementation."
- "Engineering knowledge shall exist only once." [Source: standards/csl/CSL_MANIFESTO.md:157-217]

### 2. The repository gives Canonical Knowledge a concrete home
`knowledge/README.md` states:
- "This directory stores project-specific Canonical Knowledge."
- "Contents shall be the authoritative source for engineering knowledge." [Source: knowledge/README.md:13-31]

By contrast:
- `generated/README.md` says generated outputs are "never authoritative." [Source: generated/README.md:13-30]
- `runtime/README.md` says runtime assets are implementation-specific and separate from Canonical Knowledge. [Source: runtime/README.md:13-30]

### 3. Canonical Knowledge sits above compiler output and generated artifacts
The Constitution's authority flow places Canonical Knowledge above the Engineering Compiler, Universal Engineering Model, Engineering Artifacts, and Execution. [Source: standards/csl/CSL_CONSTITUTION.md:133-172]

The CSL glossary defines the Compiler as "A system that transforms Canonical Knowledge into the Universal Engineering Model and Engineering Artifacts." [Source: standards/csl/reference/glossary/GLOSSARY.md:65-68]

`generated/README.md` confirms repository placement of that principle by stating that generated contents are produced from the Universal Engineering Model and may be regenerated at any time. [Source: generated/README.md:13-27]

### 4. Canonical Knowledge is not only storage; it is a graphable and governable platform domain
CANON-012 says Canonical Intelligence transforms canonical documentation into structured architectural knowledge and that canonical documentation is always authoritative. [Source: docs/canonical/CANON-012_CANONICAL_INTELLIGENCE_SPECIFICATION_v1.0.0.md:11-18, 55-99]

CANON-013 says the Canonical Knowledge Graph links architectural concepts extracted from canonical specifications to repository implementations and becomes the semantic backbone of Canonical Intelligence. [Source: docs/canonical/CANON-013_CANONICAL_KNOWLEDGE_GRAPH_SPECIFICATION_v1.0.0.md:11-18]

CANON-058 defines Platform Knowledge categories including Canonical Knowledge, Repository Knowledge, Engineering Knowledge, Governance Knowledge, and Runtime Knowledge. It says knowledge is cumulative, versioned, traceable, and shall never silently disappear. [Source: docs/canonical/v4/CANON-058_AI_CTO_AUTONOMOUS_RUNTIME_PLATFORM_SPECIFICATION_v4.0.0.md:471-503]

### 5. Canonical Knowledge evolves through a governed cycle
The Manifesto defines the Canonical Engineering Cycle as:
Idea → Discussion → Proposal → Approval → Canonical Knowledge → Validation → Compilation → Engineering Artifacts → Execution → Observation → Learning → Knowledge Update → Recompilation. [Source: standards/csl/CSL_MANIFESTO.md:711-767]

The Constitution adds control points:
- Every Canonical Knowledge revision shall be validated before compilation. [Source: standards/csl/CSL_CONSTITUTION.md:451-477]
- Critical actions require explicit human approval. [Source: standards/csl/CSL_CONSTITUTION.md:511-560]
- Evolution must preserve engineering intent, historical context, traceability, and compatibility whenever possible. [Source: standards/csl/CSL_CONSTITUTION.md:683-707]

RFC-0008 gives Canonical Knowledge a distribution mechanism through Knowledge Packages. [Source: standards/csl/rfc/RFC-0008-KNOWLEDGE-PACKAGE-FORMAT.md:17-39]
RFC-0010 defines how versioning and migration preserve Canonical Knowledge through change. [Source: standards/csl/rfc/RFC-0010-VERSIONING-AND-MIGRATION-POLICY.md:177-229, 295-353]

### 6. Human authority controls Canonical Knowledge changes
The Constitution says AI shall never modify Canonical Knowledge without human authorization. [Source: standards/csl/CSL_CONSTITUTION.md:787-799]

Safety & Governance Volume VII says AI shall never modify Canonical Knowledge without authorization. [Source: standards/csl/specification/07_SAFETY_AND_GOVERNANCE.md:217-247]

CANON-058 says Engineering Agents may contribute new knowledge but may never modify canonical knowledge without governance approval. [Source: docs/canonical/v4/CANON-058_AI_CTO_AUTONOMOUS_RUNTIME_PLATFORM_SPECIFICATION_v4.0.0.md:1205-1223]

## ENGINEERING CONCLUSION
Canonical Knowledge belongs above runtime behavior, above implementation, above generated artifacts, and above repository-local reports. In repository terms, it is distributed primarily across `docs/canonical/` and `knowledge/`, then operationalized by Canonical Intelligence, the Knowledge Graph, validators, governance mechanisms, and the compiler chain. [Source: knowledge/README.md:13-31; generated/README.md:13-30; docs/canonical/CANON-012_CANONICAL_INTELLIGENCE_SPECIFICATION_v1.0.0.md:13-18; docs/canonical/CANON-013_CANONICAL_KNOWLEDGE_GRAPH_SPECIFICATION_v1.0.0.md:13-18]

Canonical Knowledge does evolve, but only through governed approval, validation, migration, and preservation flows. The repository's evidence does not support any model in which runtime state, AI output, or generated artifacts can override Canonical Knowledge. [Source: standards/csl/CSL_CONSTITUTION.md:29-47, 451-560, 763-799; generated/README.md:25-30]

## ENGINEERING RECOMMENDATION
If AI Toolkit wants a repository-local answer to "Where does Canonical Knowledge belong?", the most evidence-faithful answer is: in `knowledge/` and canonical specifications, governed by human-approved canonical processes, interpreted through validators and compiler-like infrastructure, and never superseded by generated or runtime artifacts. That rule should be published explicitly in a future repository governance constitution or master authority map. [Source: knowledge/README.md:13-31; standards/csl/CSL_CONSTITUTION.md:29-47]

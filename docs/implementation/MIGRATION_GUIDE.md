# Phase 1 Migration Guide

Version: 1.0.0

Status: Canonical

Classification: Migration Documentation

CORE: CORE-023-012

---

# 1. Purpose

This guide describes migration paths for consumers of AI-Toolkit APIs after Phase 1 implementation.

Phase 1 adds new canonical APIs without breaking existing interfaces.

---

# 2. New APIs in Phase 1

## 2.1 CSL Lexer

```python
from python.canonical_parser import CslLexer, TokenType

lexer = CslLexer(source_text, source_name="file.md")
tokens = lexer.tokenize()
```

No migration required. This is a new API.

## 2.2 CSL Grammar Parser and AST

```python
from python.canonical_parser import CslParser, DocumentNode

parser = CslParser()
doc = parser.parse_text(source_text, source_name="file.md")
# doc is a DocumentNode with typed children
sections = doc.sections()
```

The existing `CanonicalParser.parse_file()` is preserved and unchanged.

Use `CslParser` for new code that needs AST access.

## 2.3 Semantic Analyzer

```python
from python.canonical_parser import CslParser, SemanticAnalyzer

parser = CslParser()
doc = parser.parse_text(text)
analyzer = SemanticAnalyzer()
result = analyzer.analyze(doc)
# result.purpose, result.objectives, result.dependencies, etc.
```

No migration required. This is a new API.

## 2.4 Universal Engineering Model

```python
from python.canonical_entities import UniversalEngineeringModel, UemBuilder, EngObjectType

builder = UemBuilder()
uem = builder.build(semantic_results)

# Query objects
docs = uem.objects_by_type(EngObjectType.DOCUMENT)
obj = uem.get_object("CANON-001")
```

No migration required. This is a new API.

## 2.5 Normative Validation

```python
from python.validation_engine import CslNormativeValidator

validator = CslNormativeValidator()
result = validator.validate_file("docs/canonical/CANON-001.md")

if result.passed():
    print("Valid")
for finding in result.errors():
    print(f"ERROR [{finding.code}]: {finding.message}")
```

The existing `ValidationEngine.validate()` is preserved and unchanged.

Use `CslNormativeValidator` for new CSL-normative validation.

## 2.6 Engineering Compiler

```python
from python.engineering_engine.compiler import EngineeringCompiler

compiler = EngineeringCompiler()
result = compiler.compile("docs/canonical")

if result.succeeded():
    uem = result.uem
    artifacts = result.artifacts
```

No migration required. This is a new API.

## 2.7 Generator Framework

```python
from python.engineering_engine.generator_framework import (
    ArtifactGenerator, GeneratorContext, GeneratorArtifact,
    ArtifactType, default_registry
)

class MyGenerator(ArtifactGenerator):
    generator_id = "my-generator"
    artifact_type = ArtifactType.REPORT

    def generate(self, context):
        uem = context.uem
        return [GeneratorArtifact(
            artifact_type=self.artifact_type,
            name="my-report",
            content={},
            generator_id=self.generator_id,
            uem_object_ids=[o.obj_id for o in uem.all_objects()],
        )]

compiler = EngineeringCompiler()
compiler.register_generator(MyGenerator())
```

## 2.8 Governance Kernel

```python
from python.rule_engine import (
    GovernanceKernel, Permission, PermissionCategory, RiskLevel
)

kernel = GovernanceKernel()
kernel.permissions.grant(Permission(PermissionCategory.EXECUTE, "compile"))

try:
    approval = kernel.authorize("compile", actor="ci-runner")
    # proceed with action
except ApprovalRequiredError as e:
    # human approval required
    pass
except EmergencyStopError:
    # all operations halted
    pass
```

---

# 3. Deprecated Modules

The following modules are frozen as compatibility-only.

Do not use them in new code.

| Module | Replacement |
|--------|------------|
| `lib/python/knowledge_graph_engine.py` | `lib/python/canonical_entities/uem.py` |
| `lib/python/knowledge_graph_v2/` | `lib/python/canonical_entities/uem.py` |
| `lib/python/decision_engine.py` | No direct replacement in Phase 1 |
| `lib/python/foundation_audit.py` | `lib/python/canonical_audit/` |
| `lib/python/memory_engine.py` | No direct replacement in Phase 1 |
| `lib/python/repository_inventory.py` | `lib/python/canonical_repository/` |
| `lib/python/repository_profile.py` | `lib/python/canonical_repository/` |
| `lib/python/autonomous_workflow_engine.py` | `lib/python/autonomous_workflow_engine/` |
| `lib/python/development_validator.py` | `lib/python/development_validator/` |

---

# 4. Shell Module Migration

Shell modules in `lib/*.sh` are frozen as compatibility-only.

All future development shall use Python modules.

| Shell Module | Python Equivalent |
|-------------|------------------|
| lib/context_engine.sh | lib/python/context_synchronization_engine |
| lib/execution_engine.sh | lib/python/execution_engine |
| lib/git_engine.sh | lib/python/engineering_engine/scm_provider.py |
| lib/github_engine.sh | lib/python/engineering_engine/github_cli_client.py |
| lib/planner_engine.sh | lib/python/planning_engine |
| lib/review_engine.sh | lib/python/review_agent |

---

# 5. Directory Structure Changes

Phase 1 introduces RFC-0009 canonical directories:

| Directory | Purpose |
|-----------|---------|
| `knowledge/` | Project-specific Canonical Knowledge |
| `generated/` | Engineering Artifacts (compiler output) |
| `runtime/` | Runtime implementation assets |

Canonical Knowledge remains in `docs/canonical/`.

Generated artifacts shall be placed in `generated/` in future phases.

---

# 6. Breaking Changes

**None.** Phase 1 adds new APIs without removing or modifying existing public interfaces.

---

# 7. Identifier Namespace Migration

Phase 1 now reserves the `ATK-` prefix for AI-Toolkit-generated runtime identifiers.

Examples:

- `ATK-VAL-*` for validation checks
- `ATK-RULE-*` for rule-engine findings
- `ATK-PLAN-*` for planning identifiers
- `ATK-EXEC-*` for execution identifiers
- `ATK-EVAL-*` for self-evaluation identifiers
- `ATK-SNAP-*` for generated snapshots
- `ATK-STATE-*`, `ATK-WS-*`, `ATK-REPO-*`, `ATK-REVIEW-*`, `ATK-OWNER-*`, `ATK-TELEGRAM-*`, `ATK-INTEGRITY-*` for development-state records

This change reduces collisions with generic identifiers from external systems such as CI platforms, issue trackers, REST APIs, and provider SDKs.

Compatibility notes:

- CSL canonical document references such as `CANON-001` remain unchanged.
- Semantic diagnostic codes such as `SEM-001` remain unchanged in Phase 1 because they are part of the CSL-facing diagnostics contract.
- Parser metadata inference is now non-authoritative: inferred values are stored separately from declared metadata and do not satisfy explicit metadata requirements.

---

End of Phase 1 Migration Guide.

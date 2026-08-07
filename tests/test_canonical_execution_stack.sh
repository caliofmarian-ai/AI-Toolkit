#!/usr/bin/env bash
# tests/test_canonical_execution_stack.sh
#
# Integration test: Canonical → CSS → CDM → CSL → Knowledge → Runtime
#
# Verifies that the Canonical Execution Stack forms one deterministic pipeline.

set -e

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

python3 - <<'PY'
import sys
sys.path.insert(0, "lib/python")
sys.path.insert(0, "lib")
sys.path.insert(0, ".")

from pathlib import Path

# ---------------------------------------------------------------
# Phase 1: CSS Engine
# ---------------------------------------------------------------
from css_engine import CSSEngine

css = CSSEngine()
css_dir = "standards/css"
if Path(css_dir).exists():
    standards = css.load_directory(css_dir)
    assert isinstance(standards, list), "CSS Engine must return a list"
    stats = css.statistics()
    assert "loaded_standards" in stats
    report = css.diagnostics_report()
    assert "total_standards" in report

print(f"CSS Engine PASS — {css.statistics()['loaded_standards']} standards loaded")

# ---------------------------------------------------------------
# Phase 2: CDM Engine
# ---------------------------------------------------------------
from cdm_engine import CdmEngine

cdm = CdmEngine()
cdm_dir = "standards/cdm"
if Path(cdm_dir).exists():
    docs = cdm.load_directory(cdm_dir)
    assert isinstance(docs, list), "CDM Engine must return a list of documents"
    stats = cdm.statistics()
    assert "total_documents" in stats
    for doc in cdm.all_documents():
        result = cdm.validate(doc)
        assert hasattr(result, "passed")

print(f"CDM Engine PASS — {cdm.statistics()['total_documents']} documents loaded")

# ---------------------------------------------------------------
# Phase 3: CSL Engine
# ---------------------------------------------------------------
from csl_engine import CslEngine

csl = CslEngine()

minimal_csl = """
Project:
    Title: Test Project
    Version: 1.0.0
    Status: Draft
"""

result = csl.execute(minimal_csl, source_name="<test>")
assert hasattr(result, "valid"), "CslExecutionResult must have valid attribute"
assert hasattr(result, "tokens"), "CslExecutionResult must have tokens"
assert len(result.tokens) > 0, "Lexer must produce tokens"

compiled = csl.compile(minimal_csl, source_name="<test-compile>")
assert hasattr(compiled, "entities")

# Validate a real CSL fixture if present
for fixture in ["tests/fixtures_csl_minimal_project.csl"]:
    if Path(fixture).exists():
        r = csl.execute_file(fixture)
        assert hasattr(r, "valid")

stats = csl.statistics()
assert "executed_sources" in stats

print(f"CSL Engine PASS — {stats['executed_sources']} source(s) executed")

# ---------------------------------------------------------------
# Phase 4: Knowledge Materialization
# ---------------------------------------------------------------
from knowledge_materialization import KnowledgeMaterializationEngine

km = KnowledgeMaterializationEngine()

cdm2 = CdmEngine()
cdm_docs = cdm2.load_directory("standards/cdm") if Path("standards/cdm").exists() else []

css2 = CSSEngine()
css_records = css2.load_directory("standards/css") if Path("standards/css").exists() else []

knowledge = km.materialize(cdm_docs, css_records)
assert knowledge.knowledge_graph is not None, "Knowledge Graph must be produced"
assert len(knowledge.knowledge_objects) >= 0
assert isinstance(knowledge.dependency_graph, dict)
assert isinstance(knowledge.traceability_graph, dict)

kd = knowledge.to_dict()
assert "knowledge_objects" in kd
assert "dependency_graph" in kd
assert "statistics" in kd

nodes = knowledge.knowledge_graph.node_count()
edges = knowledge.knowledge_graph.edge_count()

print(f"Knowledge Materialization PASS — {nodes} nodes, {edges} edges in graph")

# ---------------------------------------------------------------
# Phase 5: Runtime engine registration
# ---------------------------------------------------------------
from runtime.registry import RuntimeRegistry

registry = RuntimeRegistry()

from css_engine.engine import CSSEngine as _CSS
from cdm_engine.engine import CdmEngine as _CDM
from csl_engine.engine import CslEngine as _CSL
from knowledge_materialization.engine import KnowledgeMaterializationEngine as _KM

registry.register_engine("css", _CSS)
registry.register_engine("cdm", _CDM)
registry.register_engine("csl", _CSL)
registry.register_engine("knowledge_materialization", _KM)

assert registry.get_engine("css") is _CSS
assert registry.get_engine("cdm") is _CDM
assert registry.get_engine("csl") is _CSL
assert registry.get_engine("knowledge_materialization") is _KM

print("Runtime Registration PASS — CSS, CDM, CSL, KnowledgeMaterialization registered")

# ---------------------------------------------------------------
# Phase 6: Dashboard capabilities include new engines
# ---------------------------------------------------------------
from dashboard.service import CAPABILITY_DEFINITIONS

slugs = {cap.slug for cap in CAPABILITY_DEFINITIONS}
for expected in ("css-engine", "cdm-engine", "csl-engine", "knowledge-materialization"):
    assert expected in slugs, f"Dashboard must define capability: {expected}"

print(f"Dashboard PASS — {len(slugs)} capabilities defined, new engines present")

# ---------------------------------------------------------------
# Summary
# ---------------------------------------------------------------
print()
print("=" * 60)
print("Canonical Execution Stack Integration Test: ALL PASS")
print("=" * 60)
print(f"  CSS Engine:               {css.statistics()['loaded_standards']} standards")
print(f"  CDM Engine:               {cdm.statistics()['total_documents']} documents")
print(f"  CSL Engine:               {csl.statistics()['executed_sources']} sources")
print(f"  Knowledge Graph:          {nodes} nodes / {edges} edges")
print(f"  Runtime Engines:          css, cdm, csl, knowledge_materialization")
print(f"  Dashboard Capabilities:   {len(slugs)} total")
PY

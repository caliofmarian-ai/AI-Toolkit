#!/usr/bin/env bash
set -e

# CSL Conformance Level 3 — Compiler Tests
# Tests that the implementation builds UEM and generates artifacts
# CSL Reference: CONFORMANCE_LEVELS.md Level 3
# CORE: CORE-023-011

python3 - <<'PY'
import sys
sys.path.insert(0, "lib")

from python.engineering_engine.compiler import EngineeringCompiler
from python.canonical_entities import UniversalEngineeringModel, EngObjectType

print("=== CSL Level 3: Compiler ===")

compiler = EngineeringCompiler()
result = compiler.compile("docs/canonical")

# L3-01: UEM construction
assert result.uem is not None, "L3-01 FAIL: UEM not constructed"
assert len(result.uem) > 0, "L3-01 FAIL: UEM is empty"
print(f"L3-01 PASS: UEM constructed with {len(result.uem)} Engineering Objects")

# L3-02: No compilation errors
assert len(result.errors) == 0, f"L3-02 FAIL: {len(result.errors)} compilation errors: {result.errors[:3]}"
print("L3-02 PASS: Compilation succeeded without errors")

# L3-03: Validation results present
assert len(result.validation_results) > 0, "L3-03 FAIL: No validation results"
print(f"L3-03 PASS: {len(result.validation_results)} validation results")

# L3-04: All validation categories present in at least one result
all_cats = set()
for vr in result.validation_results:
    all_cats.update(vr.category_results.keys())
required_cats = {"LEXICAL", "SYNTAX", "SEMANTIC", "RELATIONSHIP", "CONSTRAINT", "DEPENDENCY", "GOVERNANCE", "SAFETY"}
missing = required_cats - all_cats
assert not missing, f"L3-04 FAIL: missing validation categories: {missing}"
print("L3-04 PASS: All 8 normative validation categories present")

# L3-05: Artifact generation
assert len(result.artifacts) > 0, "L3-05 FAIL: No artifacts generated"
print(f"L3-05 PASS: {len(result.artifacts)} artifacts generated")

# L3-06: Traceability preserved
for artifact in result.artifacts:
    assert artifact.generator_id, f"L3-06 FAIL: artifact has no generator_id: {artifact.name}"
print("L3-06 PASS: All artifacts have traceability (generator_id)")

# L3-07: Deterministic compilation
result2 = compiler.compile("docs/canonical")
assert len(result.uem) == len(result2.uem), "L3-07 FAIL: non-deterministic compilation (UEM size differs)"
assert len(result.artifacts) == len(result2.artifacts), "L3-07 FAIL: non-deterministic artifact generation"
print("L3-07 PASS: Deterministic compilation confirmed")

# L3-08: UEM has DOCUMENT objects
doc_objs = result.uem.objects_by_type(EngObjectType.DOCUMENT)
assert len(doc_objs) > 0, "L3-08 FAIL: UEM has no DOCUMENT objects"
print(f"L3-08 PASS: UEM contains {len(doc_objs)} DOCUMENT objects")

print("\nCSL Level 3 (Compiler): ALL PASS")
PY

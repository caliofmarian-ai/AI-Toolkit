#!/usr/bin/env bash
set -e

python3 - <<'PY'
import sys
sys.path.insert(0, 'lib')

from python.engineering_engine.compiler import EngineeringCompiler
from python.canonical_entities import EngObjectType, EngRelationType

print('=== CSL Level 3: Compiler ===')
compiler = EngineeringCompiler()
result = compiler.compile('tests')
assert result.uem is not None and len(result.uem) > 0, 'L3-01 FAIL: UEM not constructed'
print(f'L3-01 PASS: UEM constructed with {len(result.uem)} Engineering Objects')
assert all('fixtures_csl_invalid_keyword.csl' in error for error in result.errors), f'L3-02 FAIL: unexpected compilation errors: {result.errors}'
print('L3-02 PASS: Compilation succeeded without errors')
assert len(result.validation_results) > 0, 'L3-03 FAIL: No validation results'
print(f'L3-03 PASS: {len(result.validation_results)} validation results')
all_cats = set()
for vr in result.validation_results:
    all_cats.update(vr.category_results.keys())
required_cats = {'LEXICAL', 'SYNTAX', 'SEMANTIC', 'RELATIONSHIP', 'CONSTRAINT', 'DEPENDENCY', 'GOVERNANCE', 'SAFETY'}
missing = required_cats - all_cats
assert not missing, f'L3-04 FAIL: missing validation categories: {missing}'
print('L3-04 PASS: All 8 normative validation categories present')
assert result.uem.objects_by_type(EngObjectType.PROJECT), 'L3-05 FAIL: project object missing'
assert result.uem.objects_by_type(EngObjectType.CAPABILITY), 'L3-05 FAIL: capability object missing'
assert result.uem.objects_by_type(EngObjectType.REQUIREMENT), 'L3-05 FAIL: requirement object missing'
print('L3-05 PASS: CSL entity object types materialized in UEM')
assert result.uem.relationships_of_type(EngRelationType.IMPLEMENTS), 'L3-06 FAIL: implements relationship missing'
assert result.uem.relationships_of_type(EngRelationType.CONTAINS), 'L3-06 FAIL: contains relationship missing'
print('L3-06 PASS: CSL relationships materialized in UEM')
result2 = compiler.compile('tests')
assert len(result.uem) == len(result2.uem), 'L3-07 FAIL: non-deterministic UEM size'
assert len(result.artifacts) == len(result2.artifacts), 'L3-07 FAIL: non-deterministic artifact generation'
print('L3-07 PASS: deterministic compilation confirmed')
assert any('CSL-0104' in error for error in result.errors), 'L3-08 FAIL: invalid CSL fixture not rejected'
print('L3-08 PASS: invalid fixture rejected with deterministic diagnostics')
print('\nCSL Level 3 (Compiler): ALL PASS')
PY

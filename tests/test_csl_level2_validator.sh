#!/usr/bin/env bash
set -e

python3 - <<'PY'
import sys
from pathlib import Path
sys.path.insert(0, 'lib')

from python.validation_engine import CslNormativeValidator, ValidationCategory

print('=== CSL Level 2: Core Validator ===')
validator = CslNormativeValidator()
source = Path('tests/fixtures_csl_minimal_project.csl').read_text(encoding='utf-8')
result = validator.validate_text(source, 'fixtures_csl_minimal_project.csl')
for index, category in enumerate([ValidationCategory.LEXICAL, ValidationCategory.SYNTAX, ValidationCategory.SEMANTIC, ValidationCategory.RELATIONSHIP, ValidationCategory.CONSTRAINT, ValidationCategory.DEPENDENCY, ValidationCategory.GOVERNANCE, ValidationCategory.SAFETY], start=1):
    assert category.value in result.category_results, f'L2-{index:02d} FAIL: missing {category.value}'
    print(f'L2-{index:02d} PASS: {category.value} validation executed')
result1 = validator.validate_text(source, 'fixtures_csl_minimal_project.csl')
result2 = validator.validate_text(source, 'fixtures_csl_minimal_project.csl')
assert [(f.code, f.message) for f in result1.findings] == [(f.code, f.message) for f in result2.findings], 'L2-09 FAIL: non-deterministic diagnostics'
print('L2-09 PASS: deterministic diagnostics confirmed')
bad_source = Path('tests/fixtures_csl_invalid_keyword.csl').read_text(encoding='utf-8')
bad_result = validator.validate_text(bad_source, 'fixtures_csl_invalid_keyword.csl')
assert any(f.code == 'CSL-0104' for f in bad_result.findings), 'L2-10 FAIL: reserved keyword conflict not detected'
print('L2-10 PASS: reserved keyword conflict detected')
print('\nCSL Level 2 (Core Validator): ALL PASS')
PY

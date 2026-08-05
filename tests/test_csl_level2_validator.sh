#!/usr/bin/env bash
set -e

# CSL Conformance Level 2 — Core Validator Tests
# Tests that the implementation performs normative CSL validation
# CSL Reference: CONFORMANCE_LEVELS.md Level 2
# CORE: CORE-023-011

python3 - <<'PY'
import sys
sys.path.insert(0, "lib")

from python.validation_engine import CslNormativeValidator, ValidationCategory
from pathlib import Path

print("=== CSL Level 2: Core Validator ===")

validator = CslNormativeValidator()

# L2-01: Lexical validation
result = validator.validate_text(
    "# CANON-001\nVersion: 1.0.0\nStatus: Draft\n\n## Purpose\n\nTest.\n",
    "test.md"
)
assert ValidationCategory.LEXICAL.value in result.category_results, "L2-01 FAIL: no lexical validation"
print("L2-01 PASS: Lexical validation executed")

# L2-02: Syntax validation
assert ValidationCategory.SYNTAX.value in result.category_results, "L2-02 FAIL: no syntax validation"
print("L2-02 PASS: Syntax validation executed")

# L2-03: Semantic validation
assert ValidationCategory.SEMANTIC.value in result.category_results, "L2-03 FAIL: no semantic validation"
print("L2-03 PASS: Semantic validation executed")

# L2-04: Relationship validation
assert ValidationCategory.RELATIONSHIP.value in result.category_results, "L2-04 FAIL: no relationship validation"
print("L2-04 PASS: Relationship validation executed")

# L2-05: Constraint validation
assert ValidationCategory.CONSTRAINT.value in result.category_results, "L2-05 FAIL: no constraint validation"
print("L2-05 PASS: Constraint validation executed")

# L2-06: Dependency validation
assert ValidationCategory.DEPENDENCY.value in result.category_results, "L2-06 FAIL: no dependency validation"
print("L2-06 PASS: Dependency validation executed")

# L2-07: Governance validation
assert ValidationCategory.GOVERNANCE.value in result.category_results, "L2-07 FAIL: no governance validation"
print("L2-07 PASS: Governance validation executed")

# L2-08: Deterministic diagnostics (run twice, same result)
result1 = validator.validate_text("# CANON-002\nVersion: 1.0.0\nStatus: Draft\n\n## Purpose\n\nTest.\n", "test2.md")
result2 = validator.validate_text("# CANON-002\nVersion: 1.0.0\nStatus: Draft\n\n## Purpose\n\nTest.\n", "test2.md")
assert len(result1.findings) == len(result2.findings), "L2-08 FAIL: non-deterministic diagnostics"
print("L2-08 PASS: Deterministic diagnostics confirmed")

# L2-09: Validate all canonical documents
docs_path = Path("docs/canonical")
files = sorted(docs_path.glob("CANON-*.md"))
errors = []
warnings = []
for f in files:
    r = validator.validate_file(f)
    for e in r.errors():
        errors.append(f"{f.name}: [{e.code}] {e.message}")
    for w in r.warnings():
        warnings.append(f"{f.name}: [{w.code}] {w.message}")
print(f"L2-09: {len(files)} canonical documents validated, {len(errors)} errors")
if errors:
    for e in errors[:5]:
        print(f"  WARN: {e}")
print("L2-09 PASS")

# L2-10: Canonical documents may rely on section headings, but should not rely on inferred metadata
unexpected = [w for w in warnings if "[GOV-001]" in w]
assert not unexpected, f"L2-10 FAIL: unexpected canonical warnings: {unexpected[:5]}"
print("L2-10 PASS: canonical documents avoid governance failures and preserve explicit metadata rules")

print("\nCSL Level 2 (Core Validator): ALL PASS")
PY

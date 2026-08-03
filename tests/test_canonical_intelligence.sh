#!/data/data/com.termux/files/usr/bin/bash
set -e

python3 - <<'PY'
import sys
sys.path.insert(0, "lib")

from python.canonical_intelligence import CanonicalIntelligenceEngine

engine = CanonicalIntelligenceEngine(".")
result = engine.run()

assert "canonical_repository" in result
assert "coverage" in result
assert "compliance" in result
assert "drift" in result
assert "batches" in result
assert "reports" in result

stats = engine.statistics(result)
print(f"Documents: {stats['canonical_documents']}")
print(f"Coverage: {stats['overall_coverage']:.0%}")
print(f"Compliance: {stats['overall_compliance']:.0%}")
print(f"Drift findings: {stats['drift_findings']}")
print(f"Batches: {stats['batches']}")
print()
print("Canonical Intelligence Engine PASS")
PY

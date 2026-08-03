#!/usr/bin/env bash
# CORE-021 — Runtime Health Tests
# Tests the Health Service liveness and readiness checks.
set -e

python3 - <<'PY'
import sys
sys.path.insert(0, "lib")

from python.runtime.health import HealthService

# --- Liveness always returns healthy ---
hs = HealthService()
result = hs.check_liveness()
assert result.healthy, "Liveness must always be True"

# --- Readiness is not ready before startup_complete ---
result = hs.check_readiness()
assert not result.ready, "Should not be ready before mark_startup_complete"

# --- Readiness is ready after startup_complete with no failed checks ---
hs.mark_startup_complete()
result = hs.check_readiness()
assert result.ready, f"Should be ready: {result}"

# --- Failed check makes readiness return healthy=False ---
hs2 = HealthService()
hs2.register_check("always_fail", lambda: False)
hs2.mark_startup_complete()
result = hs2.check_readiness()
assert not result.healthy, "healthy must be False when check fails"
assert not result.ready, "ready must be False when check fails"

# --- Exception in check is handled gracefully ---
hs3 = HealthService()
hs3.register_check("raises", lambda: 1/0)
hs3.mark_startup_complete()
result = hs3.check_readiness()
assert not result.healthy
assert "details" in hs3.to_dict(result)

# --- to_dict returns expected keys ---
hs4 = HealthService()
hs4.mark_startup_complete()
result = hs4.check_readiness()
d = hs4.to_dict(result)
for key in ["healthy", "ready", "checks", "timestamp", "details"]:
    assert key in d, f"Missing key: {key}"

print("Health tests PASSED")
PY

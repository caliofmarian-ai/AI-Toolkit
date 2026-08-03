#!/usr/bin/env bash
# CORE-021 — Runtime Recovery Tests
# Tests the Recovery Service.
set -e

python3 - <<'PY'
import sys
sys.path.insert(0, "lib")

from python.runtime.recovery import RecoveryService

# --- Successful recovery resets counter ---
rec = RecoveryService(max_attempts=3)
success = rec.attempt(lambda: True, "test")
assert success
assert rec._attempt_count == 0, "Counter should reset after success"

# --- Failed attempt increments counter ---
rec2 = RecoveryService(max_attempts=3)
success = rec2.attempt(lambda: False, "test fail")
assert not success
assert rec2._attempt_count == 1

# --- Exhausted callback fires after max_attempts ---
exhausted = []
rec3 = RecoveryService(max_attempts=2)
rec3.on_exhausted(lambda: exhausted.append(True))
rec3.attempt(lambda: False, "fail 1")
rec3.attempt(lambda: False, "fail 2")
assert len(exhausted) == 1, f"Exhausted callback should have fired once: {exhausted}"

# --- Exception in recovery_fn is handled ---
rec4 = RecoveryService(max_attempts=3)
success = rec4.attempt(lambda: 1/0, "exception")
assert not success

# --- summary returns expected keys ---
summary = rec4.summary()
for key in ["max_attempts", "current_attempt_count", "history"]:
    assert key in summary, f"Missing key: {key}"

print("Recovery tests PASSED")
PY

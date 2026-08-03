#!/usr/bin/env bash
# CORE-021 — Runtime Lifecycle Tests
# Tests lifecycle phase transitions.
set -e

python3 - <<'PY'
import sys
sys.path.insert(0, "lib")

from lib.python.runtime.lifecycle import LifecycleManager, LifecyclePhase

# --- Transitions work correctly ---
lc = LifecycleManager()
assert lc.current_phase == LifecyclePhase.BOOT

lc.transition(LifecyclePhase.INITIALIZATION)
assert lc.current_phase == LifecyclePhase.INITIALIZATION

lc.transition(LifecyclePhase.CONFIGURATION)
lc.transition(LifecyclePhase.READY)
assert lc.is_ready()
assert not lc.is_running()

lc.transition(LifecyclePhase.RUNNING)
assert lc.is_running()
assert lc.is_ready()

lc.transition(LifecyclePhase.SHUTDOWN)
assert lc.is_shutdown()
assert not lc.is_running()

# --- Phase history is preserved ---
history = lc.to_dict()["phase_history"]
assert history[0] == "BOOT"
assert "READY" in history
assert "RUNNING" in history
assert "SHUTDOWN" in history

# --- Lifecycle listeners fire on transition ---
fired = []
lc2 = LifecycleManager()
lc2.on_phase(LifecyclePhase.READY, lambda p: fired.append(p))
lc2.transition(LifecyclePhase.READY)
assert fired == [LifecyclePhase.READY], f"Listener not fired: {fired}"

# --- to_dict returns expected keys ---
d = lc.to_dict()
for key in ["current_phase", "phase_history", "is_ready", "is_running"]:
    assert key in d, f"Missing key: {key}"

print("Lifecycle tests PASSED")
PY

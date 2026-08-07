#!/usr/bin/env bash
# CORE-021 — Runtime Bootstrap Tests
# Tests the canonical bootstrap startup sequence.
set -e

python3 - <<'PY'
import sys, os
sys.path.insert(0, "lib")
os.environ["RUNTIME_LOOP_INTERVAL_SECONDS"] = "300"
os.environ["SCHEDULER_INTERVAL_SECONDS"] = "300"
os.environ["RUNTIME_HTTP_PORT"] = "19001"
os.environ["JSON_LOGS"] = "false"

from lib.python.runtime.bootstrap import RuntimeBootstrap
from lib.python.runtime.lifecycle import LifecyclePhase

# --- Bootstrap creates all required services ---
rt = RuntimeBootstrap()
rt.bootstrap()

assert rt.identity is not None, "identity must be set"
assert rt.config is not None, "config must be set"
assert rt.secrets is not None, "secrets must be set"
assert rt.registry is not None, "registry must be set"
assert rt.lifecycle is not None, "lifecycle must be set"
assert rt.supervisor is not None, "supervisor must be set"
assert rt.health is not None, "health must be set"
assert rt.recovery is not None, "recovery must be set"
assert rt.scheduler is not None, "scheduler must be set"
assert rt.event_loop is not None, "event_loop must be set"
assert rt.dispatcher is not None, "dispatcher must be set"
assert rt.job_queue is not None, "job_queue must be set"
assert rt.metrics is not None, "metrics must be set"
assert rt.reports is not None, "reports must be set"
assert rt.runtime_state is not None, "runtime_state must be set"
assert rt.diagnostics is not None, "diagnostics must be set"
assert rt.dashboard_service is not None, "dashboard_service must be set"
assert rt.http_server is not None, "http_server must be set"
assert rt.github_webhook is not None, "github_webhook must be set"
assert rt.telegram is not None, "telegram must be set"

# --- Lifecycle is in READY state after bootstrap ---
assert rt.lifecycle.is_ready(), f"Expected READY, got {rt.lifecycle.current_phase}"

# --- Phase history contains all mandatory phases ---
history = rt.lifecycle.to_dict()["phase_history"]
for phase in ["BOOT", "INITIALIZATION", "CONFIGURATION", "READY"]:
    assert phase in history, f"Missing phase {phase} in history"

# --- Identity has required fields ---
identity_dict = rt.identity.to_dict()
for field in ["runtime_id", "runtime_version", "start_timestamp", "lifecycle_phase"]:
    assert identity_dict[field], f"Missing identity field: {field}"

# --- Registry has expected services ---
services = rt.registry.list_services()
for svc in ["health", "scheduler", "event_dispatcher", "event_loop", "job_queue"]:
    assert svc in services, f"Missing service: {svc}"

# --- Engines registered ---
engines = rt.registry.list_engines()
assert len(engines) >= 1, "Expected at least one engine registered"

# --- Runtime status snapshot is persisted ---
import pathlib
status_path = pathlib.Path(rt.config.state_dir) / "runtime_status.json"
assert status_path.exists(), f"Missing runtime status snapshot: {status_path}"

# Clean up
rt.stop()

print("Bootstrap tests PASSED")
PY

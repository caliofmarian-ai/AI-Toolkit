#!/usr/bin/env bash
# CORE-021 — Railway Bootstrap Tests
# Tests Railway deployment metadata loading.
set -e

python3 - <<'PY'
import sys, os
sys.path.insert(0, "lib")

from python.runtime.railway import RailwayBootstrap, load_railway_metadata

# --- Metadata loads from environment ---
os.environ["RAILWAY_PROJECT_ID"] = "test-project"
os.environ["RAILWAY_SERVICE_ID"] = "test-service"
os.environ["RAILWAY_DEPLOYMENT_ID"] = "test-deployment"
os.environ["RAILWAY_ENVIRONMENT"] = "testing"
os.environ["PORT"] = "9080"

meta = load_railway_metadata()
assert meta.project_id == "test-project"
assert meta.service_id == "test-service"
assert meta.deployment_id == "test-deployment"
assert meta.environment == "testing"
assert meta.port == 9080

# --- RailwayBootstrap.initialize works ---
rb = RailwayBootstrap()
assert rb.is_railway(), "Should detect Railway when RAILWAY_ENVIRONMENT is set"
loaded_meta = rb.initialize()
assert loaded_meta is not None
assert rb.metadata is not None
assert rb.metadata.project_id == "test-project"

# --- is_railway returns False without RAILWAY_ENVIRONMENT ---
del os.environ["RAILWAY_ENVIRONMENT"]
rb2 = RailwayBootstrap()
assert not rb2.is_railway(), "Should not detect Railway without env var"

# --- to_dict includes required fields ---
d = meta.to_dict()
for field in ["project_id", "service_id", "deployment_id", "environment", "port"]:
    assert field in d, f"Missing field: {field}"

print("Railway bootstrap tests PASSED")
PY

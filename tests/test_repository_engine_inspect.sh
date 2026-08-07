#!/usr/bin/env bash
set -e

ROOT="${1:-.}"

python3 "$ROOT/bin/ai" inspect "$ROOT" >/tmp/ai_toolkit_inspect_output.json

TODAY="$(date -u +%Y%m%d)"
REPORT_PATH="$ROOT/.ai/reports/inspect-$TODAY.md"
PROFILE_PATH="$ROOT/.ai/reports/inspect-$TODAY.json"

# --- Markdown report exists and contains expected sections ---
test -f "$REPORT_PATH"

grep -q "## Summary" "$REPORT_PATH"
grep -q "## File Distribution" "$REPORT_PATH"
grep -q "## Language Distribution" "$REPORT_PATH"
grep -q "## Tech Stack" "$REPORT_PATH"
grep -q "## Entry Points" "$REPORT_PATH"
grep -q "## Test Coverage Ratio" "$REPORT_PATH"
grep -q "## Documentation Coverage" "$REPORT_PATH"
grep -q "## Repository Health Summary" "$REPORT_PATH"
grep -q "## Dependencies" "$REPORT_PATH"

# --- JSON profile exists and is valid JSON ---
test -f "$PROFILE_PATH"
python3 -c "import json, sys; json.load(open('$PROFILE_PATH'))" || { echo "FAIL: JSON profile is not valid JSON"; exit 1; }

# --- JSON profile has required top-level keys ---
python3 - "$PROFILE_PATH" <<'PY'
import json, sys
profile = json.load(open(sys.argv[1]))
required = ["path", "name", "metrics", "classified_files", "tech_stack", "entry_points", "dependencies", "health_summary"]
for key in required:
    assert key in profile, f"Missing key in profile: {key}"

metrics = profile["metrics"]
assert isinstance(metrics["total_files"], int), "total_files must be int"
assert metrics["total_files"] > 0, "total_files must be > 0"
assert isinstance(metrics["language_distribution"], dict), "language_distribution must be dict"
assert len(metrics["language_distribution"]) > 0, "language_distribution must not be empty"

assert isinstance(profile["classified_files"], list), "classified_files must be list"
assert len(profile["classified_files"]) > 0, "classified_files must not be empty"

cf = profile["classified_files"][0]
for field in ("path", "file_class", "category", "language", "is_executable"):
    assert field in cf, f"classified_file missing field: {field}"

health = profile["health_summary"]
assert health["status"] in ("HEALTHY", "ATTENTION", "RISK"), "unexpected health status"
assert isinstance(health["score"], int), "health score must be int"
assert isinstance(health["checks"], list) and len(health["checks"]) > 0, "health checks must be non-empty list"

deps = profile["dependencies"]
assert isinstance(deps["internal_import_nodes"], int), "internal_import_nodes must be int"

print("JSON profile validation PASS")
PY

# --- CLI result JSON has expected keys ---
python3 - /tmp/ai_toolkit_inspect_output.json <<'PY'
import json, sys
result = json.load(open(sys.argv[1]))
for key in ("repository", "path", "report_path", "profile_path"):
    assert key in result, f"Missing key in CLI result: {key}"
print("CLI result JSON PASS")
PY

echo "Repository inspect CLI PASS"

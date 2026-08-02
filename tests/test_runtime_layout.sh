#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
AI_ROOT="$ROOT/.ai"
RUNTIME_ROOT="$AI_ROOT/runtime"

assert_dir() {
  local path="$1"
  [ -d "$path" ] || {
    echo "Missing directory: $path" >&2
    exit 1
  }
}

assert_file_absent() {
  local path="$1"
  [ ! -e "$path" ] || {
    echo "Path must not exist: $path" >&2
    exit 1
  }
}

assert_gitignore_line() {
  local line="$1"
  grep -Fx "$line" "$ROOT/.gitignore" >/dev/null || {
    echo "Missing .gitignore entry: $line" >&2
    exit 1
  }
}

assert_not_gitignore_line() {
  local line="$1"
  if grep -Fx "$line" "$ROOT/.gitignore" >/dev/null; then
    echo "Unexpected .gitignore entry: $line" >&2
    exit 1
  fi
}

assert_no_repo_reference() {
  local needle="$1"
  if git -C "$ROOT" grep -nF -- "$needle" -- . ":(exclude)tests/test_runtime_layout.sh" >/dev/null; then
    echo "Legacy reference found in repository: $needle" >&2
    git -C "$ROOT" grep -nF -- "$needle" -- . ":(exclude)tests/test_runtime_layout.sh" >&2
    exit 1
  fi
}

assert_no_repo_regex() {
  local pattern="$1"
  if git -C "$ROOT" grep -nE -- "$pattern" -- . ":(exclude)tests/test_runtime_layout.sh" >/dev/null; then
    echo "Invalid runtime/batch path reference detected: $pattern" >&2
    git -C "$ROOT" grep -nE -- "$pattern" -- . ":(exclude)tests/test_runtime_layout.sh" >&2
    exit 1
  fi
}

# Canonical runtime structure
assert_dir "$RUNTIME_ROOT"
assert_dir "$RUNTIME_ROOT/checkpoints"
assert_dir "$RUNTIME_ROOT/logs"
assert_dir "$RUNTIME_ROOT/sessions"
assert_dir "$RUNTIME_ROOT/state"
assert_dir "$RUNTIME_ROOT/cache"

# Execution state location rule
legacy_execution_state_rel=".ai/"
legacy_execution_state_rel="${legacy_execution_state_rel}execution_state.json"
assert_file_absent "$ROOT/$legacy_execution_state_rel"

# Runtime directories are git-ignored
assert_gitignore_line ".ai/runtime/state/*"
assert_gitignore_line ".ai/runtime/cache/*"
assert_gitignore_line ".ai/runtime/logs/*"
assert_gitignore_line ".ai/runtime/checkpoints/*"
assert_gitignore_line ".ai/runtime/sessions/*"

# Batch artifacts remain valid as source-generated artifacts area
assert_dir "$AI_ROOT/batches"
assert_not_gitignore_line ".ai/batches/"
assert_not_gitignore_line ".ai/batches/*"

# No legacy runtime paths remain in repository code/docs/tests
legacy_sessions_rel=".ai/"
legacy_sessions_rel="${legacy_sessions_rel}sessions/"
assert_no_repo_reference "$legacy_execution_state_rel"
assert_no_repo_reference "$legacy_sessions_rel"

# Runtime artifacts must not point into .ai/batches
assert_no_repo_regex "\\.ai/batches/.*(execution_state|checkpoint|profil|session|cache|log|temporary|temp)"

echo "Runtime layout checks passed"

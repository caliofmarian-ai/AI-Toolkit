#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

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

# Canonical runtime structure
assert_dir "$ROOT/.ai/runtime"
assert_dir "$ROOT/.ai/runtime/checkpoints"
assert_dir "$ROOT/.ai/runtime/logs"
assert_dir "$ROOT/.ai/runtime/sessions"
assert_dir "$ROOT/.ai/runtime/state"
assert_dir "$ROOT/.ai/runtime/cache"

# Execution state location rule
assert_file_absent "$ROOT/.ai/execution_state.json"

# Runtime directories are git-ignored
assert_gitignore_line ".ai/runtime/state/*"
assert_gitignore_line ".ai/runtime/cache/*"
assert_gitignore_line ".ai/runtime/logs/*"
assert_gitignore_line ".ai/runtime/checkpoints/*"
assert_gitignore_line ".ai/runtime/sessions/*"

# Batch artifacts remain valid as source-generated artifacts area
assert_dir "$ROOT/.ai/batches"
assert_not_gitignore_line ".ai/batches/"
assert_not_gitignore_line ".ai/batches/*"

echo "Runtime layout checks passed"

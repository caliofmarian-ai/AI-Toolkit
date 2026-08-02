#!/data/data/com.termux/files/usr/bin/bash

set -e

ROOT="${1:-$(pwd)}"
ROOT="$(cd "$ROOT" && pwd)"

OUT="$ROOT/.ai/context/project_context.md"

mkdir -p "$(dirname "$OUT")"

{
echo "# Project Context"
echo
echo "Generated: $(date)"
echo
echo "## Repository"
echo "$ROOT"
echo

echo "## Branch"
git -C "$ROOT" branch --show-current 2>/dev/null || true
echo

echo "## Remote"
git -C "$ROOT" remote -v 2>/dev/null || true
echo

echo "## Statistics"
echo "- Files: $(find "$ROOT" -type f | wc -l)"
echo "- Directories: $(find "$ROOT" -type d | wc -l)"
echo "- Python: $(find "$ROOT" -type f -name '*.py' | wc -l)"
echo "- Markdown: $(find "$ROOT" -type f -name '*.md' | wc -l)"
echo "- JSON: $(find "$ROOT" -type f -name '*.json' | wc -l)"
echo

echo "## Top Level"
find "$ROOT" -maxdepth 1 | sort
echo

echo "## Canonical Documents"
find "$ROOT" -path "*/canonical/*" -type f | sort
echo

echo "## Tests"
find "$ROOT" -type d -name tests | sort
echo

echo "## Railway"
find "$ROOT" \( -name railway.json -o -name railway.toml \)
echo

echo "## GitHub Actions"
find "$ROOT" -path "*/.github/workflows/*" -type f
echo

echo "## End"
} > "$OUT"

echo
echo "Context generated:"
echo "$OUT"

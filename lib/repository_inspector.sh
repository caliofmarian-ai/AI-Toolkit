#!/data/data/com.termux/files/usr/bin/bash

set -e

ROOT="${1:-.}"

ROOT="$(cd "$ROOT" && pwd)"

echo "=================================="
echo "Repository Inspector v2"
echo "=================================="

echo
echo "Repository:"
echo "$ROOT"

echo
echo "Branch:"
git -C "$ROOT" branch --show-current

echo
echo "Remote:"
git -C "$ROOT" remote -v || true

echo
echo "Repository statistics"

echo "Files: $(find "$ROOT" -type f | wc -l)"
echo "Directories: $(find "$ROOT" -type d | wc -l)"
echo "Markdown: $(find "$ROOT" -name '*.md' | wc -l)"
echo "Shell: $(find "$ROOT" -name '*.sh' | wc -l)"
echo "Python: $(find "$ROOT" -name '*.py' | wc -l)"
echo "JSON: $(find "$ROOT" -name '*.json' | wc -l)"

echo
echo "Canonical documents"

find "$ROOT/docs/canonical" -type f 2>/dev/null | sort

echo
echo "Engines"

find "$ROOT/lib" -maxdepth 1 -name "*engine*.sh" | sort

echo
echo "Tests"

find "$ROOT/tests" -type f 2>/dev/null | sort

echo
echo "Inspection completed successfully."


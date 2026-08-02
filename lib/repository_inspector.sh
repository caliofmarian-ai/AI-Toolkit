#!/data/data/com.termux/files/usr/bin/bash

ROOT="${1:-.}"

echo "=================================="
echo "Repository Inspector"
echo "=================================="

echo
echo "Repository:"
git -C "$ROOT" rev-parse --show-toplevel 2>/dev/null || echo "Not a git repository"

echo
echo "Branch:"
git -C "$ROOT" branch --show-current 2>/dev/null

echo
echo "Remote:"
git -C "$ROOT" remote -v 2>/dev/null

echo
echo "Languages:"
find "$ROOT" -type f | sed 's|.*\.||' | sort | uniq -c | sort -nr | head -20

echo
echo "Important folders:"
find "$ROOT" -maxdepth 2 -type d | sort

echo
echo "GitHub:"
find "$ROOT" -maxdepth 2 -name ".github"

echo
echo "Railway:"
find "$ROOT" -iname "railway.json" -o -iname "railway.toml"

echo
echo "Tests:"
find "$ROOT" -type d -name "tests"

echo
echo "Canonical docs:"
find "$ROOT" -path "*/canonical/*" -type f

echo
echo "Inspection complete."

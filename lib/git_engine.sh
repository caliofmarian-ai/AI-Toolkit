#!/data/data/com.termux/files/usr/bin/bash

ROOT="${1:-.}"

cd "$ROOT" || exit 1

echo "=================================="
echo "Git Engine"
echo "=================================="
echo

echo "Repository:"
git rev-parse --show-toplevel 2>/dev/null
echo

echo "Branch:"
git branch --show-current
echo

echo "Status:"
git status --short
echo

echo "Last Commit:"
git log -1 --oneline
echo

echo "Remotes:"
git remote -v
echo

echo "Local Branches:"
git branch
echo

echo "Done."

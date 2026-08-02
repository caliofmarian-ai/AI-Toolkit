#!/data/data/com.termux/files/usr/bin/bash

ROOT="${1:-.}"
ROOT="$(cd "$ROOT" && pwd)"

echo "=================================="
echo "Workspace Status"
echo "=================================="

echo
echo "Context:"
ls -1 "$ROOT/.ai/context" 2>/dev/null || true

echo
echo "Work:"
ls -1 "$ROOT/.ai/work" 2>/dev/null || true

echo
echo "Git status:"
git -C "$ROOT" status --short

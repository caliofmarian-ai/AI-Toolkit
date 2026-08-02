#!/data/data/com.termux/files/usr/bin/bash
set -e

ROOT="${1:-.}"

echo "=================================="
echo "Repository Inspector Test"
echo "=================================="

echo
echo "[1/8] Repository"
git -C "$ROOT" rev-parse --show-toplevel

echo
echo "[2/8] Branch"
git -C "$ROOT" branch --show-current

echo
echo "[3/8] Git Status"
git -C "$ROOT" status --short

echo
echo "[4/8] File count"
find "$ROOT" -type f | wc -l

echo
echo "[5/8] Directory count"
find "$ROOT" -type d | wc -l

echo
echo "[6/8] Canonical documents"
find "$ROOT/docs/canonical" -type f 2>/dev/null | sort

echo
echo "[7/8] Engines"
find "$ROOT/lib" -maxdepth 1 -name "*engine*.sh" 2>/dev/null | sort

echo
echo "[8/8] Result"

echo "PASS"


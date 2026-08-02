#!/data/data/com.termux/files/usr/bin/bash

set -e

ROOT="${1:-.}"
ROOT="$(cd "$ROOT" && pwd)"

OUT="$ROOT/.ai/work/review.md"

mkdir -p "$(dirname "$OUT")"

echo "=================================="
echo "Review Engine"
echo "=================================="

cd "$ROOT"

STATUS="$(git status --short)"
FILES_CHANGED="$(git diff --name-only | wc -l)"
INSERTIONS="$(git diff --numstat | awk '{i+=$1} END{print i+0}')"
DELETIONS="$(git diff --numstat | awk '{d+=$2} END{print d+0}')"

cat > "$OUT" <<EOT
# AI Review Report

Repository:
$ROOT

Generated:
$(date)

## Summary

Files changed: $FILES_CHANGED

Insertions: $INSERTIONS

Deletions: $DELETIONS

## Git Status

$STATUS

Status:
READY
EOT

echo
echo "Review report:"
echo "$OUT"

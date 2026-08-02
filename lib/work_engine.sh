#!/data/data/com.termux/files/usr/bin/bash

set -e

ROOT="${1:-$(pwd)}"
ROOT="$(cd "$ROOT" && pwd)"

WORKDIR="$ROOT/.ai/work"
mkdir -p "$WORKDIR"

echo "=================================="
echo "AI Toolkit Work Engine"
echo "=================================="
echo

echo "[1/4] Repository Inspector..."
bash "$(dirname "$0")/repository_inspector.sh" "$ROOT"

echo
echo "[2/4] Repository Summary..."
bash "$(dirname "$0")/repository_summary.sh" "$ROOT" \
> "$WORKDIR/repository_summary.txt"

echo
echo "[3/4] Context Engine..."
bash "$(dirname "$0")/context_engine.sh" "$ROOT"

echo
echo "[4/4] Work session..."

cat > "$WORKDIR/session.md" <<EOT
# AI Work Session

Repository:
$ROOT

Generated:
$(date)

Status:
READY
EOT

echo
echo "=================================="
echo "WORK SESSION READY"
echo "=================================="
echo
echo "Workspace:"
echo "$WORKDIR"

#!/data/data/com.termux/files/usr/bin/bash
set -e

ROOT="${1:-.}"

python3 "$ROOT/bin/ai" inspect "$ROOT" >/tmp/ai_toolkit_inspect_output.json

TODAY="$(date -u +%Y%m%d)"
REPORT_PATH="$ROOT/.ai/reports/inspect-$TODAY.md"

test -f "$REPORT_PATH"

grep -q "## Summary" "$REPORT_PATH"
grep -q "## File Distribution" "$REPORT_PATH"
grep -q "## Language Distribution" "$REPORT_PATH"
grep -q "## Tech Stack" "$REPORT_PATH"
grep -q "## Entry Points" "$REPORT_PATH"
grep -q "## Test Coverage Ratio" "$REPORT_PATH"
grep -q "## Documentation Coverage" "$REPORT_PATH"

echo "Repository inspect CLI PASS"

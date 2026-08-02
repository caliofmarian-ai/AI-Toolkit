#!/data/data/com.termux/files/usr/bin/bash
set -e

echo
echo "===== STEP DEFINITIONS ====="

for dir in .ai/batches/*; do

    [ -d "$dir" ] || continue

    echo
    echo "$dir"

    python3 - <<PY
import json

data=json.load(open("$dir/steps.json"))

print("Status:",data["status"])

for step in data["steps"]:
    print(step["id"],step["status"],step["name"])
PY

done

echo
echo "STEP DEFINITION PASS"

#!/data/data/com.termux/files/usr/bin/bash

ROOT="${1:-.}"
ROOT="$(cd "$ROOT" && pwd)"

echo "=================================="
echo "Workspace Status"
echo "=================================="

echo
echo "Context"

find "$ROOT/.ai/context" -maxdepth 1 -type f | sort

echo
echo "Work"

find "$ROOT/.ai/work" -maxdepth 1 -type f | sort

echo
echo "Workspace validation"

ERROR=0

if [ -f "$ROOT/.ai/context/project-context.md" ]; then
    echo "ERROR: legacy filename detected"
    ERROR=1
fi

if [ ! -f "$ROOT/.ai/context/project_context.md" ]; then
    echo "ERROR: project_context.md missing"
    ERROR=1
fi

for FILE in \
session.md \
repository_summary.txt \
plan.md \
review.md \
execution.log
do
    if [ ! -f "$ROOT/.ai/work/$FILE" ]; then
        echo "ERROR: missing $FILE"
        ERROR=1
    fi
done

echo
echo "Git status"
git -C "$ROOT" status --short

echo

if [ "$ERROR" -eq 0 ]; then
    echo "Workspace: PASS"
    exit 0
else
    echo "Workspace: FAIL"
    exit 1
fi

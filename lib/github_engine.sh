#!/data/data/com.termux/files/usr/bin/bash

set -e

ACTION="${1:-help}"
ISSUE="${2:-}"

case "$ACTION" in

issue)

if [ -z "$ISSUE" ]; then
    echo "Usage:"
    echo "ai github issue <number>"
    exit 1
fi

echo "=================================="
echo "GitHub Issue"
echo "=================================="
echo

gh issue view "$ISSUE"

;;

issues)

echo "=================================="
echo "Open Issues"
echo "=================================="
echo

gh issue list

;;

prs)

echo "=================================="
echo "Pull Requests"
echo "=================================="
echo

gh pr list

;;

milestones)

echo "=================================="
echo "Milestones"
echo "=================================="
echo

gh api repos/:owner/:repo/milestones \
--jq '.[] | "\(.number)  \(.title)"'

;;

*)

echo "Available:"
echo
echo "github issues"
echo "github issue <number>"
echo "github prs"
echo "github milestones"

;;

esac

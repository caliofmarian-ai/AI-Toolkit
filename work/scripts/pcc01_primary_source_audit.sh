#!/usr/bin/env bash
set -euo pipefail

ROOT="$HOME/storage/shared/AI-Projects/AI-Toolkit"
REPORT="work/audits/PCC-01_PERSISTENT_EXPERIENCE_PRIMARY_SOURCE_AUDIT_2026-08-12.md"
CONTRACT="work/research/PRODUCTION_CANON_CONTRACT.md"

cd "$ROOT" || exit 1

echo "=========================================================="
echo "PCC-01 — PERSISTENT EXPERIENCE AUDIT"
echo "=========================================================="

test -s "$CONTRACT" || {
    echo "ERROR: Missing/empty: $CONTRACT"
    exit 1
}

test -e "$REPORT" || {
    echo "ERROR: Report blank does not exist: $REPORT"
    exit 1
}

BRANCH="$(git branch --show-current)"
HEAD="$(git rev-parse HEAD)"
NOW="$(date -u '+%Y-%m-%dT%H:%M:%SZ')"

if [ "$BRANCH" != "main" ]; then
    echo "ERROR: Expected main, found: $BRANCH"
    exit 1
fi

echo "Branch: $BRANCH"
echo "HEAD:   ${HEAD:0:7}"
echo "Report: $REPORT"
echo
echo "Collecting repository evidence..."

{
    echo "# PCC-01 — Persistent Experience Primary Source and Implementation Audit"
    echo
    echo "Generated: $NOW"
    echo
    echo "Repository: AI-Toolkit"
    echo
    echo "Branch: $BRANCH"
    echo
    echo "HEAD: $HEAD"
    echo
    echo "Status: Raw Evidence Collection"
    echo
    echo "This document records repository-observable evidence."
    echo
    echo "It does not establish Canon, reconcile conflicting sources, or promote research material into production authority."
    echo
    echo "---"
    echo
    echo "# 1. Repository State"
    echo
    echo '```text'
    git status --short
    echo '```'

    echo
    echo "---"
    echo
    echo "# 2. Persistent Experience Related Material"
    echo
    echo '```text'

    find work \
        -type f \
        \(\
            -iname '*persistent*experience*' \
            -o -iname '*experience*' \
            -o -iname '*transformation*' \
            -o -iname '*witness*' \
            -o -iname '*FT-0026*' \
       \) \
        2>/dev/null \
        | sort

    echo '```'

    echo
    echo "---"
    echo
    echo "# 3. Research Inventory"
    echo
    echo '```text'

    find work/research \
        -maxdepth 2 \
        -type f \
        2>/dev/null \
        | sort

    echo '```'

    echo
    echo "---"
    echo
    echo "# 4. Primary Research — Birth of Persistent Experience"
    echo

    EP_FILE="$(
        find work/research \
            -maxdepth 1 \
            -type f \
            -name 'EP-0001_Birth_of_Persistent_Experience_*.md' \
            2>/dev/null \
            | sort \
            | head -n 1
    )"

    if [ -n "${EP_FILE:-}" ] && [ -s "$EP_FILE" ]; then
        echo "Source: \`$EP_FILE\`"
        echo
        echo '```text'
        cat "$EP_FILE"
        echo '```'
    else
        echo "**NOT FOUND:** EP-0001_Birth_of_Persistent_Experience"
    fi

    echo
    echo "---"
    echo
    echo "# 5. Evidence — FT-0026"
    echo

    FT_FILE="$(
        find work/evidence \
            -type f \
            -name 'FT-0026*.md' \
            2>/dev/null \
            | sort \
            | head -n 1
    )"

    if [ -n "${FT_FILE:-}" ] && [ -s "$FT_FILE" ]; then
        echo "Source: \`$FT_FILE\`"
        echo
        echo '```text'
        cat "$FT_FILE"
        echo '```'
    else
        echo "**NOT FOUND:** FT-0026"
    fi

    echo
    echo "---"
    echo
    echo "# 6. Persistent Experience Inventory"
    echo
    echo '```text'

    if [ -d work/persistent-experience ]; then
        find work/persistent-experience \
            -type f \
            | sort
    else
        echo "DIRECTORY NOT FOUND: work/persistent-experience"
    fi

    echo '```'

    echo
    echo "---"
    echo
    echo "# 7. Persistent Experience Preserved Content"

    if [ -d work/persistent-experience ]; then
        while IFS= read -r FILE; do
            [ -n "$FILE" ] || continue

            echo
            echo "## Source — \`$FILE\`"
            echo
            echo '```text'

            if [ -s "$FILE" ]; then
                cat "$FILE"
            else
                echo "[EMPTY FILE]"
            fi

            echo '```'

        done < <(
            find work/persistent-experience \
                -type f \
                | sort
        )
    else
        echo
        echo "Persistent Experience directory not found."
    fi

    echo
    echo "---"
    echo
    echo "# 8. Transformation and Witness Material"

    for DIR in \
        work/transformations \
        work/transformation \
        work/witnesses \
        work/witness
    do
        [ -d "$DIR" ] || continue

        echo
        echo "## Directory — \`$DIR\`"

        while IFS= read -r FILE; do
            [ -n "$FILE" ] || continue

            echo
            echo "### Source — \`$FILE\`"
            echo
            echo '```text'

            if [ -s "$FILE" ]; then
                cat "$FILE"
            else
                echo "[EMPTY FILE]"
            fi

            echo '```'

        done < <(
            find "$DIR" \
                -type f \
                | sort
        )
    done

    echo
    echo "---"
    echo
    echo "# 9. Repository References"
    echo
    echo '```text'

    grep -RniI \
        --exclude-dir=.git \
        --exclude='PRODUCTION_CANON_CONTRACT.md' \
        --exclude='PCC-01_PERSISTENT_EXPERIENCE_PRIMARY_SOURCE_AUDIT_2026-08-12.md' \
        -E \
        'Persistent Experience|persistent.experience|Terminal Capture|terminal.capture|EXP-[0-9]|Transformation Witness|experience witness' \
        . \
        2>/dev/null \
        | head -n 1000 \
        || true

    echo '```'

    echo
    echo "---"
    echo
    echo "# 10. Likely Executable Implementation Files"
    echo
    echo '```text'

    find bin lib scripts tests \
        -type f \
        2>/dev/null \
        | while IFS= read -r FILE; do
            if grep -qiE \
                'persistent.?experience|terminal.?capture|experience.?capture|transformation.?witness|EXP-[0-9]' \
                "$FILE" 2>/dev/null; then
                echo "$FILE"
            fi
        done \
        | sort -u

    echo '```'

    echo
    echo "---"
    echo
    echo "# 11. Executable Implementation Content"

    while IFS= read -r FILE; do
        [ -n "$FILE" ] || continue

        echo
        echo "## Implementation — \`$FILE\`"
        echo
        echo "Lines: $(wc -l < "$FILE")"
        echo
        echo '```text'
        cat "$FILE"
        echo '```'

    done < <(
        find bin lib scripts tests \
            -type f \
            2>/dev/null \
            | while IFS= read -r FILE; do
                if grep -qiE \
                    'persistent.?experience|terminal.?capture|experience.?capture|transformation.?witness|EXP-[0-9]' \
                    "$FILE" 2>/dev/null; then
                    echo "$FILE"
                fi
            done \
            | sort -u
    )

    echo
    echo "---"
    echo
    echo "# 12. Relevant Git History"
    echo
    echo '```text'

    git log \
        --all \
        --date=iso \
        --pretty=format:'%h | %ad | %an | %s' \
        -- \
        work/persistent-experience \
        work/research \
        work/evidence \
        bin \
        lib \
        scripts \
        tests \
        2>/dev/null \
        | head -n 300 \
        || true

    echo
    echo '```'

    echo
    echo "---"
    echo
    echo "# 13. Evidence Boundary"
    echo
    echo "This audit records repository-observable evidence."
    echo
    echo "It does not by itself determine:"
    echo
    echo "- which research statements are canonical;"
    echo "- which statements remain hypotheses;"
    echo "- whether older implementations remain authoritative;"
    echo "- whether existing implementation satisfies PCC-01;"
    echo "- whether observed code is currently operational;"
    echo "- whether missing repository evidence proves historical non-existence."

    echo
    echo "---"
    echo
    echo "# 14. Next Required Analysis"
    echo
    echo "This evidence must next be used to determine:"
    echo
    echo "1. primary source of every PCC-01 requirement;"
    echo "2. authority status;"
    echo "3. confirmed versus research-only requirements;"
    echo "4. contradictions and superseded interpretations;"
    echo "5. existing implementation capability;"
    echo "6. missing implementation capability;"
    echo "7. required provenance;"
    echo "8. acceptance evidence;"
    echo "9. acceptance tests;"
    echo "10. exact controlled implementation task."

} > "$REPORT"

echo
echo "=========================================================="
echo "VERIFY GENERATED AUDIT"
echo "=========================================================="

test -s "$REPORT" || {
    echo "ERROR: Audit report is empty."
    exit 1
}

for SECTION in \
    "# 1. Repository State" \
    "# 4. Primary Research — Birth of Persistent Experience" \
    "# 5. Evidence — FT-0026" \
    "# 7. Persistent Experience Preserved Content" \
    "# 10. Likely Executable Implementation Files" \
    "# 11. Executable Implementation Content" \
    "# 13. Evidence Boundary" \
    "# 14. Next Required Analysis"
do
    grep -Fxq "$SECTION" "$REPORT" || {
        echo "ERROR: Missing report section: $SECTION"
        exit 1
    }
done

echo
echo "REPORT:"
ls -lh "$REPORT"

echo
echo "LINES:"
wc -l "$REPORT"

echo
echo "SHA-256:"
sha256sum "$REPORT"

echo
echo "GIT STATUS:"
git status --short

echo
echo "=========================================================="
echo "PCC-01 AUDIT COMPLETE"
echo "=========================================================="
echo
echo "Audit generated:"
echo "$REPORT"
echo
echo "No commit created."
echo "Nothing pushed."
echo "=========================================================="
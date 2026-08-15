#!/usr/bin/env bash
set -euo pipefail

echo "=========================================================="
echo "AI-TOOLKIT"
echo "ERROR MEMORY AND RECURRENCE PREVENTION"
echo "RUN 001 — METABOLIC CLASSIFICATION AND CLOSURE"
echo "=========================================================="

EXPECTED_BRANCH="organ/error-memory-run-001"
EXPECTED_BASE="6bce0542bbc8192f2cc7ad45f8eedd725a2c6d89"

MEMORY_BODY="work/memory/4a428ce072924985834ba2a272fef6ee.json"

REPORT_DIR="work/implementation-reports/ERROR-MEMORY"
RECOVERY_REPORT="$REPORT_DIR/ERROR_MEMORY_RUN001_METABOLIC_CLASSIFICATION_AND_CLOSURE.md"
EXECUTION_RECORD="$REPORT_DIR/ERROR_MEMORY_RUN001_EXECUTION_RECORD.md"
RECOVERY_BASH="$REPORT_DIR/ERROR_MEMORY_RUN001_METABOLIC_CLASSIFICATION_AND_CLOSURE_EXECUTED_BASH.sh"

IMPLEMENTATION="lib/python/epistemic/error_memory.py"
FOCUSED_TEST="tests/epistemic/test_error_memory.py"

mkdir -p "$REPORT_DIR"

echo
echo "[1/9] Verify exact interrupted execution state"

CURRENT_BRANCH="$(git branch --show-current)"
CURRENT_HEAD="$(git rev-parse HEAD)"

echo "CURRENT BRANCH: $CURRENT_BRANCH"
echo "CURRENT HEAD:   $CURRENT_HEAD"
echo "EXPECTED BASE:  $EXPECTED_BASE"

if [ "$CURRENT_BRANCH" != "$EXPECTED_BRANCH" ]; then
    echo "STOP: expected branch $EXPECTED_BRANCH but found $CURRENT_BRANCH"
    exit 1
fi

if [ "$CURRENT_HEAD" != "$EXPECTED_BASE" ]; then
    echo "STOP: HEAD changed since the demonstrated interrupted execution."
    echo "Nothing has been deleted or reset."
    exit 1
fi

git fetch origin --quiet

REMOTE_BASE="$(git rev-parse origin/pcc-06/living-project-image-run-002)"

if [ "$REMOTE_BASE" != "$EXPECTED_BASE" ]; then
    echo "STOP: conserved PCC-06 takeover authority changed."
    echo "EXPECTED: $EXPECTED_BASE"
    echo "REMOTE:   $REMOTE_BASE"
    exit 1
fi

test -f "$IMPLEMENTATION" || {
    echo "STOP: Error Memory implementation body is missing."
    exit 1
}

test -f "$FOCUSED_TEST" || {
    echo "STOP: Error Memory focused examination body is missing."
    exit 1
}

test -f "$MEMORY_BODY" || {
    echo "STOP: expected metabolic Memory body is missing:"
    echo "$MEMORY_BODY"
    exit 1
}

echo "PASS: interrupted RUN 001 state preserved"

echo
echo "[2/9] Classify the Memory body from its ACTUAL local content"

python - "$MEMORY_BODY" <<'PY'
import json
import sys
from datetime import datetime
from pathlib import Path

path = Path(sys.argv[1])

try:
    body = json.loads(path.read_text(encoding="utf-8"))
except Exception as exc:
    raise SystemExit(
        f"STOP: metabolic body is not valid JSON: {exc}"
    )

expected_keys = {
    "id",
    "timestamp",
    "title",
    "content",
    "session",
    "capability",
}

actual_keys = set(body)

if actual_keys != expected_keys:
    raise SystemExit(
        "STOP: Memory body schema does not match the demonstrated "
        f"MemoryStore product.\n"
        f"Expected keys: {sorted(expected_keys)}\n"
        f"Actual keys:   {sorted(actual_keys)}"
    )

expected_id = path.stem

if body["id"] != expected_id:
    raise SystemExit(
        "STOP: Memory identity does not equal filename identity."
    )

expected_values = {
    "title": "First Memory",
    "content": "The organism preserved an experience.",
    "session": "SESSION-000001",
    "capability": "CAP-0001",
}

for field, expected in expected_values.items():
    actual = body.get(field)
    if actual != expected:
        raise SystemExit(
            f"STOP: field {field!r} does not match the demonstrated "
            f"test_memory_roundtrip product.\n"
            f"Expected: {expected!r}\n"
            f"Actual:   {actual!r}"
        )

try:
    timestamp = datetime.fromisoformat(body["timestamp"])
except Exception as exc:
    raise SystemExit(
        f"STOP: timestamp is not ISO-8601: {exc}"
    )

if timestamp.tzinfo is None or timestamp.utcoffset() is None:
    raise SystemExit(
        "STOP: timestamp is not timezone-aware."
    )

print("PASS: actual local JSON matches the demonstrated MemoryStore product")
print(f"ID:         {body['id']}")
print(f"TITLE:      {body['title']}")
print(f"SESSION:    {body['session']}")
print(f"CAPABILITY: {body['capability']}")
print(f"TIMESTAMP:  {body['timestamp']}")
PY

echo
echo "CLASSIFICATION:"
echo "  producer anatomy: MemoryStore.remember()"
echo "  triggering examination: test_memory_roundtrip"
echo "  repository location: work/memory/<memory-id>.json"
echo "  semantic class: persistent software body produced by executed physiology"
echo "  entire Experience: NO"
echo "  unexpected anatomical mutation: NO"
echo
echo "PASS: metabolic body classified before conservation"

echo
echo "[3/9] Conserve the recurrence-prevention precedent"

cat > "$RECOVERY_REPORT" <<'MD'
# Error Memory and Recurrence Prevention
## RUN 001 — Metabolic Classification and Closure

### Physiological context

Error Memory RUN 001 formed the minimum anatomy required to conserve
demonstrated failures and make recurrence-prevention knowledge available
to later engineering activity.

The first focused examination demonstrated:

- 18 focused Error Memory examinations passed.

The corrected neighboring examination demonstrated:

- 83 neighboring epistemic examinations passed.

The complete epistemic regression demonstrated:

- 276 epistemic examinations passed.

No new test execution was required for this closure because those
observations belong to the interrupted execution being conserved here.

## Failure recurrence discovered during RUN 001

Two distinct engineering failures were demonstrated.

### Recurrence 1 — incorrect examination import topology

The first neighboring examination was invoked without both repository
import roots required by the existing epistemic test population.

The resulting `ModuleNotFoundError` failures were examination invocation
defects, not failures of the Error Memory organ.

The corrected execution supplied both:

- `lib`
- `lib/python`

and subsequently demonstrated:

- 83 neighboring examinations passed;
- 276 complete epistemic examinations passed.

### Recurrence 2 — metabolic product misclassified as unexpected mutation

During the complete regression a new body appeared under:

`work/memory/4a428ce072924985834ba2a272fef6ee.json`

Repository inspection established that `MemoryStore` persists Memory
through `work/memory/<id>.json`.

Repository inspection also established that
`tests/epistemic/test_memory.py::test_memory_roundtrip` invokes
`MemoryStore.remember()` using:

- title: `First Memory`
- content: `The organism preserved an experience.`
- session: `SESSION-000001`
- capability: `CAP-0001`

The recovery execution inspected the ACTUAL local JSON before
classification and required:

- filename identity equals internal Memory identity;
- exact demonstrated Memory schema;
- exact fixed test values;
- timezone-aware ISO-8601 timestamp.

Only after those conditions were satisfied was the body classified.

## Classification

The JSON is a persistent software body produced by executed physiology.

It is not the entire Experience.

Its mere existence does not make it Canon.

Its mere persistence does not grant authority.

Its appearance during regression is not, by itself, evidence of an
uncontrolled anatomical mutation.

The producer, triggering examination, content, provenance and semantics
must be inspected before classification.

## Recurrence-prevention rule demonstrated

A transformation-boundary validator MUST NOT classify a newly appearing
repository body solely from its path or from the fact that it was not in
the intended source-file list.

Before rejecting such a body it must determine, where demonstrable:

1. producer;
2. triggering execution;
3. actual content;
4. provenance;
5. semantic class;
6. whether it is intended anatomy, Evidence, metabolic product,
   historical conservation, or genuinely unexplained mutation.

Unknown must remain UNKNOWN.

Unclassified must remain UNCLASSIFIED.

No unexplained body may be silently deleted.

## Additional physiological debt discovered

`test_memory_roundtrip` uses the repository-relative persistent
`work/memory` store rather than an isolated temporary test substrate.

Therefore complete epistemic regression can produce a persistent Memory
body in the repository.

This RUN does NOT redesign that older physiology because doing so would
expand Error Memory RUN 001 beyond its legitimate boundary.

The condition is conserved as discovered physiological debt for later
inspection.

## Boundary

This closure does not modify Canon.

It does not modify PCC-06.

It does not claim autonomous authority for Error Memory.

It does not rewrite historical execution.

It does not rerun already demonstrated examinations merely to reproduce
the same evidence.

## Demonstrated execution

Focused Error Memory:
18 passed.

Neighboring epistemic physiology after import-topology correction:
83 passed.

Complete epistemic regression:
276 passed.

## Result

Error Memory RUN 001 has demonstrated both:

- conservation of failure/recurrence knowledge;
- use of that knowledge to distinguish an execution defect from an organ
  defect and a legitimate metabolic product from an unexplained
  repository mutation.

Human Authority remains sovereign.
MD

echo "PASS: recurrence-prevention precedent conserved"

echo
echo "[4/9] Conserve execution evidence without manufacturing a rerun"

cat > "$EXECUTION_RECORD" <<EOF
# Error Memory RUN 001 — Execution Record

## Repository authority

Base:
\`$EXPECTED_BASE\`

Transformation branch:
\`$EXPECTED_BRANCH\`

## Demonstrated execution sequence

### Focused Error Memory examination

Result:

\`18 passed in 0.31s\`

### First neighboring examination

Result:

Collection failed with five \`ModuleNotFoundError\` errors because the
invocation did not expose both legitimate repository import roots.

Classification:

EXAMINATION INVOCATION DEFECT.

It was not classified as Error Memory organ failure.

### Corrected neighboring examination

Required import roots:

- repository \`lib\`
- repository \`lib/python\`

Result:

\`83 passed in 0.93s\`

### Complete epistemic regression

Result:

\`276 passed in 2.61s\`

### Metabolic repository effect

Observed body:

\`$MEMORY_BODY\`

The closure inspected its actual local content before conservation.

It matched the demonstrated product of
\`MemoryStore.remember()\` triggered by
\`test_memory_roundtrip\`.

## Evidence semantics

The 18, 83 and 276 passing observations are historical observations from
this same interrupted RUN 001 execution.

They were NOT rerun during closure.

This record conserves those observations without falsely representing
them as a new execution.

## Canonical authority

Canon modified:
NO.

Canonical admission claimed:
NO.

Human Authority remains sovereign.
EOF

echo "PASS: interrupted execution evidence conserved"

echo
echo "[5/9] Verify transformation boundary before staging"

ALLOWED_PREFIXES=(
    "lib/python/epistemic/error_memory.py"
    "tests/epistemic/test_error_memory.py"
    "work/implementation-reports/ERROR-MEMORY/"
    "$MEMORY_BODY"
)

mapfile -t CHANGED_PATHS < <(
    {
        git diff --name-only
        git diff --cached --name-only
        git ls-files --others --exclude-standard
    } | sort -u
)

UNEXPECTED=()

for path in "${CHANGED_PATHS[@]}"; do
    [ -n "$path" ] || continue

    allowed=0

    for prefix in "${ALLOWED_PREFIXES[@]}"; do
        if [ "$path" = "$prefix" ] || [[ "$path" == "$prefix"* ]]; then
            allowed=1
            break
        fi
    done

    if [ "$allowed" -ne 1 ]; then
        UNEXPECTED+=("$path")
    fi
done

if [ "${#UNEXPECTED[@]}" -gt 0 ]; then
    echo "STOP: repository contains effects outside the demonstrated RUN 001 boundary:"
    printf '  %s\n' "${UNEXPECTED[@]}"
    echo
    echo "Nothing has been deleted, reset, committed or hidden."
    exit 1
fi

echo "PASS: all current effects belong to the inspected RUN 001 boundary"

echo
echo "[6/9] Stage the coherent transformation"

git add -- "$IMPLEMENTATION"
git add -- "$FOCUSED_TEST"
git add -- "$REPORT_DIR"
git add -- "$MEMORY_BODY"

echo
echo "----- STAGED RUN 001 BODIES -----"
git diff --cached --name-status

echo
echo "----- STAGED DIFF STAT -----"
git diff --cached --stat

if git diff --cached --quiet; then
    echo "STOP: nothing staged for Error Memory RUN 001."
    exit 1
fi

echo
echo "[7/9] Examine staged production anatomy and conservation integrity"

# Production anatomy and focused examination must satisfy normal whitespace
# integrity. Historical executed Bash bodies are conserved as executed and
# are therefore not rewritten merely to satisfy cosmetic normalization.

git diff --cached --check -- \
    "$IMPLEMENTATION" \
    "$FOCUSED_TEST" \
    "$RECOVERY_REPORT" \
    "$EXECUTION_RECORD"

echo "PASS: production anatomy and current semantic reports pass diff integrity"

python -m py_compile "$IMPLEMENTATION" "$FOCUSED_TEST"

echo "PASS: Python parser accepts Error Memory anatomy and examination"

echo
echo "[8/9] Commit and push demonstrated RUN 001"

git commit -m "error-memory: form recurrence prevention organ and conserve RUN 001"

HEAD_NOW="$(git rev-parse HEAD)"

echo "COMMIT: $HEAD_NOW"

git push -u origin "$EXPECTED_BRANCH"

git fetch origin "$EXPECTED_BRANCH" --quiet

REMOTE_HEAD="$(git rev-parse "origin/$EXPECTED_BRANCH")"

if [ "$HEAD_NOW" != "$REMOTE_HEAD" ]; then
    echo "STOP: local Error Memory commit differs from remote branch."
    exit 1
fi

echo "PASS: Error Memory RUN 001 conserved in GitHub"

echo
echo "[9/9] Verify final repository state"

if [ -n "$(git status --porcelain)" ]; then
    echo "STOP: repository contains unclassified effects after conservation."
    git status --short
    exit 1
fi

echo
echo "=========================================================="
echo "ERROR MEMORY AND RECURRENCE PREVENTION"
echo "RUN 001 — SUCCESS"
echo "=========================================================="
echo "BRANCH:                     $EXPECTED_BRANCH"
echo "BASE:                       $EXPECTED_BASE"
echo "HEAD:                       $HEAD_NOW"
echo "LOCAL == REMOTE:            PASS"
echo "WORKTREE:                   CLEAN"
echo "ERROR MEMORY ORGAN:         FORMED"
echo "FOCUSED EXAMINATION:        18 PASSED — CONSERVED"
echo "NEIGHBORING EXAMINATION:    83 PASSED — CONSERVED"
echo "EPISTEMIC REGRESSION:       276 PASSED — CONSERVED"
echo "TESTS RERUN DURING CLOSURE: NO"
echo "IMPORT TOPOLOGY FAILURE:    CLASSIFIED"
echo "METABOLIC MEMORY BODY:      CLASSIFIED FROM ACTUAL CONTENT"
echo "RECURRENCE PRECEDENT:       CONSERVED"
echo "UNEXPLAINED BODY DELETED:   NO"
echo "CANON MODIFIED:             NO"
echo "PCC-06 MODIFIED:            NO"
echo "AUTONOMOUS AUTHORITY:       NO"
echo "IMPLEMENTATION REPORT:      CONSERVED"
echo "EXECUTION RECORD:           CONSERVED"
echo "EXECUTED BASH:              CONSERVED"
echo "GIT CONSERVATION:           PASS"
echo "=========================================================="
echo
echo "After execution, tell the AI partner only:"
echo "Am executat."
echo
echo "The AI partner must inspect the Git branch directly."
echo "=========================================================="

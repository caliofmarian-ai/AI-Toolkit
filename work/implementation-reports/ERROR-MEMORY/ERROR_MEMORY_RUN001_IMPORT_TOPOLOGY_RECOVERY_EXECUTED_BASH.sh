#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

EXPECTED_BASE="6bce0542bbc8192f2cc7ad45f8eedd725a2c6d89"
BRANCH="organ/error-memory-run-001"
REPORT_DIR="work/implementation-reports/ERROR-MEMORY"
RECOVERY_REPORT="$REPORT_DIR/ERROR_MEMORY_RUN001_IMPORT_TOPOLOGY_RECOVERY.md"
EXECUTED_BASH="$REPORT_DIR/ERROR_MEMORY_RUN001_IMPORT_TOPOLOGY_RECOVERY_EXECUTED_BASH.sh"

echo
echo "[1/9] Verify interrupted RUN 001 state without destroying it"

git fetch origin --prune

CURRENT_BRANCH="$(git branch --show-current)"
CURRENT_HEAD="$(git rev-parse HEAD)"

echo "CURRENT BRANCH: $CURRENT_BRANCH"
echo "CURRENT HEAD:   $CURRENT_HEAD"
echo "EXPECTED BASE:  $EXPECTED_BASE"

if [ "$CURRENT_BRANCH" != "$BRANCH" ]; then
    echo "STOP: expected interrupted transformation branch:"
    echo "  $BRANCH"
    echo "but current branch is:"
    echo "  $CURRENT_BRANCH"
    echo
    echo "No repository content was reset or destroyed."
    exit 1
fi

if [ "$CURRENT_HEAD" != "$EXPECTED_BASE" ]; then
    echo "STOP: interrupted RUN 001 no longer rests directly on the inspected base."
    echo "No reset will be performed automatically."
    exit 1
fi

if [ -z "$(git status --porcelain)" ]; then
    echo "STOP: interrupted RUN 001 anatomy is no longer present in the worktree."
    echo "Recovery refuses to manufacture a replacement."
    exit 1
fi

echo "PASS: interrupted RUN 001 reality is still present"

echo
echo "[2/9] Verify that the previous failure was an examination-topology failure"

test -f lib/python/epistemic/layered_memory.py
test -f tests/epistemic/test_layered_memory.py
test -f tests/epistemic/test_layered_memory_persistence.py
test -f tests/epistemic/test_layered_memory_traversal.py
test -f tests/epistemic/test_layered_memory_ancestry.py
test -f tests/epistemic/test_sedimented_memory.py

grep -Eq 'from epistemic\.|import epistemic\.' \
    tests/epistemic/test_layered_memory.py \
    tests/epistemic/test_layered_memory_persistence.py \
    tests/epistemic/test_sedimented_memory.py

grep -Eq 'from python\.epistemic\.|import python\.epistemic\.' \
    tests/epistemic/test_layered_memory_traversal.py \
    tests/epistemic/test_layered_memory_ancestry.py

echo "PASS: repository contains both legitimate epistemic import topologies"
echo "REQUIRED IMPORT ROOTS:"
echo "  $PWD/lib"
echo "  $PWD/lib/python"

export PYTHONPATH="$PWD/lib:$PWD/lib/python${PYTHONPATH:+:$PYTHONPATH}"

python - <<'PY'
import epistemic.layered_memory
import python.epistemic.layered_memory
print("PASS: both epistemic import topologies resolve simultaneously")
PY

echo
echo "[3/9] Re-examine the newly formed Error Memory organ"

ERROR_TESTS=()

while IFS= read -r path; do
    case "$path" in
        tests/epistemic/*error*memory*.py|tests/epistemic/*recurrence*.py)
            ERROR_TESTS+=("$path")
            ;;
    esac
done < <(
    {
        git diff --name-only
        git ls-files --others --exclude-standard
    } | sort -u
)

if [ "${#ERROR_TESTS[@]}" -eq 0 ]; then
    echo "STOP: no focused Error Memory examination from the interrupted RUN was found."
    echo "The recovery will not invent a test filename."
    exit 1
fi

printf 'Focused examinations:\n'
printf '  %s\n' "${ERROR_TESTS[@]}"

python -m pytest -q "${ERROR_TESTS[@]}"

echo "PASS: Error Memory focused physiology"

echo
echo "[4/9] Re-run the exact neighboring physiology with the CORRECT import topology"

python -m pytest -q \
    tests/epistemic/test_layered_memory.py \
    tests/epistemic/test_layered_memory_persistence.py \
    tests/epistemic/test_layered_memory_traversal.py \
    tests/epistemic/test_layered_memory_ancestry.py \
    tests/epistemic/test_sedimented_memory.py

echo "PASS: neighboring physiology"
echo "PASS: previous ModuleNotFoundError was an invocation defect, not an organ defect"

echo
echo "[5/9] Run complete epistemic regression with both repository import roots"

python -m pytest -q tests/epistemic

echo "PASS: complete epistemic regression"

echo
echo "[6/9] Conserve the newly demonstrated recurrence"

mkdir -p "$REPORT_DIR"

cat > "$RECOVERY_REPORT" <<'MD'
# Error Memory and Recurrence Prevention — RUN 001 Recovery

## Nature

This body conserves a real implementation failure encountered while constructing the Error Memory and Recurrence Prevention organ.

It does not rewrite the interrupted execution and does not classify the neighboring epistemic organs as defective.

## Lived sequence

The new Error Memory anatomy was materialized locally.

Its focused physiological examination completed successfully:

- 18 focused examinations passed.

The subsequent neighboring Layered Memory and Sedimented Memory examination stopped during test collection.

The observed failure was:

- `ModuleNotFoundError: No module named 'epistemic'`
- `ModuleNotFoundError: No module named 'python'`

## Demonstrated cause

The repository legitimately contains both epistemic import forms:

- `epistemic...`
- `python.epistemic...`

The failed RUN exposed an insufficient Python import topology during neighboring examination.

The correct examination environment must expose both repository roots:

- `lib`
- `lib/python`

The recovery therefore used:

`PYTHONPATH="$PWD/lib:$PWD/lib/python"`

without modifying production physiology merely to accommodate the examination environment.

## Error Memory significance

This failure is itself evidence for the necessity of the Error Memory and Recurrence Prevention organ.

The important precedent is not merely:

"an import failed."

The reusable recurrence-prevention knowledge is:

> Before constructing an epistemic regression command, inspect applicable execution precedents and preserve all demonstrated repository import roots. For the current AI-Toolkit epistemic regression topology, both `lib` and `lib/python` are required because the conserved test anatomy legitimately uses both import forms.

## Classification

- new organ defect: NO evidence
- PCC-05 defect: NO
- Layered Memory regression: NO evidence from the collection failure
- repository corruption: NO evidence
- execution/invocation defect: YES
- repeated historical class of mistake: YES
- recurrence-prevention value: HIGH

## Physiological consequence

A memory of error that merely archives failure is insufficient.

The organism requires the ability to conserve demonstrated failures together with the conditions that produced them and the prevention knowledge that must be consulted before a similar transformation is executed.

This RUN remains bounded to Error Memory and recurrence prevention.

It does not modify PCC-06 physiology.

## Recovery

The interrupted anatomy was preserved.

The RUN was not restarted from zero.

The examination topology was corrected.

Focused Error Memory physiology, neighboring physiology, and the complete epistemic regression were then required to pass before Git conservation.

## Authority boundary

This report is implementation and execution evidence.

It is not Canon.

It does not autonomously admit a new canonical rule.

Human Authority remains sovereign.
MD

echo "PASS: recurrence and prevention knowledge conserved"

echo
echo "[7/9] Verify transformation scope and repository effects"

CHANGED="$(
    {
        git diff --name-only
        git ls-files --others --exclude-standard
    } | sort -u
)"

if [ -z "$CHANGED" ]; then
    echo "STOP: no RUN 001 transformation remains to conserve."
    exit 1
fi

echo "----- RUN 001 BODIES -----"
printf '%s\n' "$CHANGED"

BAD_SCOPE=0

while IFS= read -r path; do
    [ -n "$path" ] || continue

    case "$path" in
        lib/python/epistemic/*error*memory*.py|\
        lib/python/epistemic/*recurrence*.py|\
        tests/epistemic/*error*memory*.py|\
        tests/epistemic/*recurrence*.py|\
        work/implementation-reports/ERROR-MEMORY/*|\
        work/implementation-reports/Error-Memory/*|\
        work/implementation-reports/error-memory/*|\
        work/implementation-reports/ERROR_MEMORY/*|\
        work/implementation-reports/error_memory/*)
            ;;
        *)
            echo "UNEXPECTED RUN 001 EFFECT: $path"
            BAD_SCOPE=1
            ;;
    esac
done <<< "$CHANGED"

if [ "$BAD_SCOPE" -ne 0 ]; then
    echo
    echo "STOP: effects outside the Error Memory RUN 001 boundary exist."
    echo "Nothing will be deleted automatically."
    exit 1
fi

if printf '%s\n' "$CHANGED" | grep -q '^canon/'; then
    echo "STOP: Canon mutation detected."
    exit 1
fi

if printf '%s\n' "$CHANGED" | grep -q 'PCC-06'; then
    echo "STOP: PCC-06 mutation detected."
    exit 1
fi

echo "PASS: transformation remains inside Error Memory RUN 001 boundary"

echo
echo "[8/9] Normalize newly authored text, verify, stage and conserve"

python - <<'PY'
from pathlib import Path
import subprocess

raw = subprocess.check_output(
    ["git", "status", "--porcelain"],
    text=True,
)

for line in raw.splitlines():
    if len(line) < 4:
        continue

    rel = line[3:]
    if " -> " in rel:
        rel = rel.split(" -> ", 1)[1]

    p = Path(rel)

    if not p.is_file():
        continue

    if p.suffix.lower() not in {".py", ".md", ".txt", ".sh"}:
        continue

    data = p.read_text(encoding="utf-8")
    normalized = "\n".join(
        row.rstrip(" \t") for row in data.splitlines()
    ) + ("\n" if data else "")

    if normalized != data:
        p.write_text(normalized, encoding="utf-8")

print("PASS: RUN 001 textual bodies normalized before conservation")
PY

git add \
    lib/python/epistemic \
    tests/epistemic \
    "$REPORT_DIR"

echo
echo "----- STAGED STAT -----"
git diff --cached --stat

echo
echo "----- STAGED PATHS -----"
git diff --cached --name-only

if git diff --cached --name-only | grep -q '^canon/'; then
    echo "STOP: Canon unexpectedly staged."
    exit 1
fi

if git diff --cached --name-only | grep -q 'PCC-06'; then
    echo "STOP: PCC-06 unexpectedly staged."
    exit 1
fi

git diff --cached --check

echo "PASS: staged transformation structurally clean"

git commit -m "error-memory: form recurrence prevention organ"

HEAD_NOW="$(git rev-parse HEAD)"

echo
echo "[9/9] Push and verify exact Git conservation"

git push -u origin "$BRANCH"
git fetch origin "$BRANCH" --quiet

REMOTE_NOW="$(git rev-parse "origin/$BRANCH")"

if [ "$HEAD_NOW" != "$REMOTE_NOW" ]; then
    echo "STOP: local and remote Error Memory heads differ."
    exit 1
fi

if [ -n "$(git status --porcelain)" ]; then
    echo "STOP: worktree changed after conservation."
    git status --short
    exit 1
fi

echo
echo "=========================================================="
echo "ERROR MEMORY AND RECURRENCE PREVENTION"
echo "RUN 001 — SUCCESS"
echo "=========================================================="
echo "BRANCH:                     $BRANCH"
echo "BASE:                       $EXPECTED_BASE"
echo "HEAD:                       $HEAD_NOW"
echo "LOCAL == REMOTE:            PASS"
echo "WORKTREE:                   CLEAN"
echo "ERROR MEMORY ORGAN:         FORMED"
echo "FOCUSED PHYSIOLOGY:         PASS"
echo "NEIGHBORING PHYSIOLOGY:     PASS"
echo "EPISTEMIC REGRESSION:       PASS"
echo "IMPORT TOPOLOGY PRECEDENT:  CONSERVED"
echo "RECURRENCE KNOWLEDGE:       CONSERVED"
echo "AUTONOMOUS AUTHORITY:       NO"
echo "CANON MODIFIED:             NO"
echo "PCC-06 MODIFIED:            NO"
echo "PCC-06 STATUS:              SUSPENDED FOR MIGRATION"
echo "EXECUTION RECOVERY:         CONSERVED"
echo "GIT CONSERVATION:           PASS"
echo "=========================================================="

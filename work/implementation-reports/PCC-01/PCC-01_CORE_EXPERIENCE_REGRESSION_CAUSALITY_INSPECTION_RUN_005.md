# PCC-01 — CORE EXPERIENCE REGRESSION CAUSALITY INSPECTION — RUN 005

**Purpose:** Determine whether the repository-wide test failure observed in RUN 004 belongs to PCC-01 or already exists independently in the accepted baseline.

**Expected baseline:** `d477d2523343b8e583eb43aec0091c608eb6d038`

**Software modification:** NONE

**Git conservation:** NONE

---

## 1. Baseline Verification

```text
Expected:    d477d2523343b8e583eb43aec0091c608eb6d038
LOCAL:       d477d2523343b8e583eb43aec0091c608eb6d038
origin/main: d477d2523343b8e583eb43aec0091c608eb6d038
PASS: baseline unchanged
```

## 2. Current Working Tree

```text
?? lib/python/experience/
?? tests/experience/
?? work/implementation-reports/
```

## 3. Failing Historical Test

```text
from python.engineering_engine.compiler import EngineeringCompiler

compiler = EngineeringCompiler()
result = compiler.compile("docs/canonical", run_generators=False)

print("=" * 80)
print("CSL SEMANTIC COMPILATION TEST")
print("=" * 80)

print("\nSTATISTICS")
for k, v in result.stats.items():
    print(f"{k}: {v}")

print("\nVALIDATION RESULTS")
print("Validation objects:", len(result.validation_results))

for i, validation in enumerate(result.validation_results[:10], 1):
    print("-" * 60)
    print("Validation", i)
    print("Type:", type(validation).__name__)

    for attr in dir(validation):
        if attr.startswith("_"):
            continue
        try:
            value = getattr(validation, attr)
            if callable(value):
                continue
            print(f"{attr}: {value}")
        except Exception:
            pass

print("\nUEM STATISTICS")
print(result.uem.statistics())

print("\nDOCUMENT LOOKUP")

for doc in [
    "CANON-001",
    "CANON-010",
    "CANON-032",
    "CANON-067"
]:
    print("-" * 40)
    print(doc)

    obj = result.uem.get_object(doc)

    if obj is None:
        print("NOT FOUND")
    else:
        print("Name:", obj.name)
        print("Version:", obj.version)
        print("Status:", obj.status)
        print("Source:", obj.source_document)

print("\nRELATIONSHIP COUNTS")

rels = result.uem.all_relationships()

print("Relationships:", len(rels))

contains = {}

for rel in rels:
    key = rel.relation_type.name
    contains[key] = contains.get(key, 0) + 1

for k, v in sorted(contains.items()):
    print(k, "=", v)

print("\n" + "=" * 80)
print("SEMANTIC TEST FINISHED")
print("=" * 80)
```

## 4. Baseline Version of Historical Test

```text
from python.engineering_engine.compiler import EngineeringCompiler

compiler = EngineeringCompiler()
result = compiler.compile("docs/canonical", run_generators=False)

print("=" * 80)
print("CSL SEMANTIC COMPILATION TEST")
print("=" * 80)

print("\nSTATISTICS")
for k, v in result.stats.items():
    print(f"{k}: {v}")

print("\nVALIDATION RESULTS")
print("Validation objects:", len(result.validation_results))

for i, validation in enumerate(result.validation_results[:10], 1):
    print("-" * 60)
    print("Validation", i)
    print("Type:", type(validation).__name__)

    for attr in dir(validation):
        if attr.startswith("_"):
            continue
        try:
            value = getattr(validation, attr)
            if callable(value):
                continue
            print(f"{attr}: {value}")
        except Exception:
            pass

print("\nUEM STATISTICS")
print(result.uem.statistics())

print("\nDOCUMENT LOOKUP")

for doc in [
    "CANON-001",
    "CANON-010",
    "CANON-032",
    "CANON-067"
]:
    print("-" * 40)
    print(doc)

    obj = result.uem.get_object(doc)

    if obj is None:
        print("NOT FOUND")
    else:
        print("Name:", obj.name)
        print("Version:", obj.version)
        print("Status:", obj.status)
        print("Source:", obj.source_document)

print("\nRELATIONSHIP COUNTS")

rels = result.uem.all_relationships()

print("Relationships:", len(rels))

contains = {}

for rel in rels:
    key = rel.relation_type.name
    contains[key] = contains.get(key, 0) + 1

for k, v in sorted(contains.items()):
    print(k, "=", v)

print("\n" + "=" * 80)
print("SEMANTIC TEST FINISHED")
print("=" * 80)
```

## 5. Verify Historical Test Is Unmodified

```text
Worktree SHA: 396fefbe8f1765195de87ee74092919fbac767c7c13b124489f41c56b9afdfcb
Baseline SHA: 396fefbe8f1765195de87ee74092919fbac767c7c13b124489f41c56b9afdfcb
PASS: test_csl_semantic.py is identical to accepted baseline
```

## 6. PCC-01 Import Reference Search

```text
PASS: no direct PCC-01 Experience references found in inspected historical CSL path
```

## 7. Run Historical Test With PCC-01 Present

```text

==================================== ERRORS ====================================
____________________ ERROR collecting test_csl_semantic.py _____________________
test_csl_semantic.py:34: in <module>
    print(result.uem.statistics())
          ^^^^^^^^^^^^^^^^^^^^^
E   AttributeError: 'NoneType' object has no attribute 'statistics'
------------------------------- Captured stdout --------------------------------
================================================================================
CSL SEMANTIC COMPILATION TEST
================================================================================

STATISTICS

VALIDATION RESULTS
Validation objects: 0

UEM STATISTICS
=========================== short test summary info ============================
ERROR test_csl_semantic.py - AttributeError: 'NoneType' object has no attribu...
!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
1 error in 0.91s

Exit code with local PCC-01 tissue present: 2
```

## 8. Run Baseline Historical Test in Isolated Temporary Worktree

```text
Preparing worktree (detached HEAD d477d25)
Updating files:  36% (501/1357)Updating files:  37% (503/1357)Updating files:  38% (516/1357)Updating files:  39% (530/1357)Updating files:  40% (543/1357)Updating files:  41% (557/1357)Updating files:  42% (570/1357)Updating files:  43% (584/1357)Updating files:  44% (598/1357)Updating files:  45% (611/1357)Updating files:  46% (625/1357)Updating files:  47% (638/1357)Updating files:  48% (652/1357)Updating files:  49% (665/1357)Updating files:  50% (679/1357)Updating files:  51% (693/1357)Updating files:  52% (706/1357)Updating files:  53% (720/1357)Updating files:  54% (733/1357)Updating files:  55% (747/1357)Updating files:  56% (760/1357)Updating files:  57% (774/1357)Updating files:  58% (788/1357)Updating files:  59% (801/1357)Updating files:  60% (815/1357)Updating files:  61% (828/1357)Updating files:  62% (842/1357)Updating files:  63% (855/1357)Updating files:  64% (869/1357)Updating files:  65% (883/1357)Updating files:  66% (896/1357)Updating files:  67% (910/1357)Updating files:  68% (923/1357)Updating files:  69% (937/1357)Updating files:  70% (950/1357)Updating files:  71% (964/1357)Updating files:  72% (978/1357)Updating files:  73% (991/1357)Updating files:  74% (1005/1357)Updating files:  75% (1018/1357)Updating files:  76% (1032/1357)Updating files:  77% (1045/1357)Updating files:  78% (1059/1357)Updating files:  79% (1073/1357)Updating files:  80% (1086/1357)Updating files:  81% (1100/1357)Updating files:  82% (1113/1357)Updating files:  83% (1127/1357)Updating files:  84% (1140/1357)Updating files:  85% (1154/1357)Updating files:  86% (1168/1357)Updating files:  87% (1181/1357)Updating files:  88% (1195/1357)Updating files:  89% (1208/1357)Updating files:  90% (1222/1357)Updating files:  91% (1235/1357)Updating files:  92% (1249/1357)Updating files:  93% (1263/1357)Updating files:  93% (1270/1357)Updating files:  94% (1276/1357)Updating files:  95% (1290/1357)Updating files:  96% (1303/1357)Updating files:  97% (1317/1357)Updating files:  98% (1330/1357)Updating files:  99% (1344/1357)Updating files: 100% (1357/1357)Updating files: 100% (1357/1357), done.

==================================== ERRORS ====================================
____________________ ERROR collecting test_csl_semantic.py _____________________
test_csl_semantic.py:34: in <module>
    print(result.uem.statistics())
          ^^^^^^^^^^^^^^^^^^^^^
E   AttributeError: 'NoneType' object has no attribute 'statistics'
------------------------------- Captured stdout --------------------------------
================================================================================
CSL SEMANTIC COMPILATION TEST
================================================================================

STATISTICS

VALIDATION RESULTS
Validation objects: 0

UEM STATISTICS
=========================== short test summary info ============================
ERROR test_csl_semantic.py - AttributeError: 'NoneType' object has no attribu...
!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
1 error in 0.79s

Exit code on clean accepted baseline: 2
```

## 9. Causality Classification

**Classification:** PRE-EXISTING BASELINE FAILURE

The historical test fails both with the local PCC-01 tissue and on an isolated clean checkout of the accepted baseline.

Therefore this inspection does not attribute that failure to PCC-01.

## 10. Reverify PCC-01 Dedicated Suite

```text
..................................                                       [100%]
34 passed in 0.47s
PASS: dedicated PCC-01 Core Experience suite
```

## 11. Final Repository Integrity

```text
HEAD:
d477d2523343b8e583eb43aec0091c608eb6d038

origin/main:
d477d2523343b8e583eb43aec0091c608eb6d038

Git status:
?? lib/python/experience/
?? tests/experience/
?? work/implementation-reports/
```

## 12. Epistemic Interpretation

A failure in an unrelated historical test is not automatically Evidence against PCC-01.

Likewise, 34 passing PCC-01 tests are not sufficient to declare complete PCC-01 implementation.

This inspection distinguishes correlation from demonstrated causality.

## 13. PCC-01 Status

**Implementation Status:** NOT DEMONSTRATED

**Canonical Status:** NOT CANON

**Production Status:** NOT PRODUCTION-READY


**ID_before_restart == ID_after_restart** remains undemonstrated across real process death.

## 14. Conservation

No `git add` performed.

No commit performed.

No push performed.

## 15. Final Result

**RUN 005 SCRIPT: PASS**

**Causality classification:** PRE-EXISTING BASELINE FAILURE

**NEXT REQUIRED ACTION:** GPT inspection of RUN 005 before any conservation decision.

---

END OF PCC-01 CORE EXPERIENCE REGRESSION CAUSALITY INSPECTION — RUN 005

==========================================================
RUN 005 COMPLETE
==========================================================
REPORT:
work/implementation-reports/PCC-01/PCC-01_CORE_EXPERIENCE_REGRESSION_CAUSALITY_INSPECTION_RUN_005.md

Send this Markdown file to GPT.

NO git add
NO commit
NO push
==========================================================
[?2004h[0;32m~/.../AI-Projects/AI-Toolkit[0m [0;97m$[0m [K[0;32m~/.../AI-Projects/AI-Toolkit[0m [0;97m$[0m [K[0;32m~/.../AI-Projects/AI-Toolkit[0m [0;97m$[0m [H[2J[0;32m~/.../AI-Projects/AI-Toolkit[0m [0;97m$[0m cd ~/storage/shared/AI-Projects/AI-Toolkit || exit 1

set -uo pipefail

EXPECTED_HEAD="d477d2523343b8e583eb43aec0091c608eb6d038"

PKG="lib/python/experience"
TESTS="tests/experience"

REPORT_DIR="work/implementation-reports/PCC-01"
REPORT="$REPORT_DIR/PCC-01_CORE_EXPERIENCE_FINAL_INSPECTION_AND_CONSERVATION_RUN_006.md"

COMMIT_MESSAGE="feat: preserve PCC-01 core experience foundation"

mkdir -p "$REPORT_DIR"
: > "$REPORT"

exec > >(tee -a "$REPORT") 2>&1
set -e

COMMIT_CREATED="NO"
PUSH_COMPLETED="NO"

trap 'RC=$?; if [ "$RC" -ne 0 ]; then
    echo
    echo "## EXECUTION FAILURE"
    echo
    echo "Exit code: $RC"
    echo
    echo "Commit created before failure: $COMMIT_CREATED"
    echo "Push completed before failure: $PUSH_COMPLETED"
    echo
    echo "HEAD at failure:"
    echo "\`\`\`text"
    git rev-parse HEAD 2>/dev/null || true
    echo "\`\`\`"
    echo
    echo "Git status at failure:"
    echo "\`\`\`text"
    git status --short 2>/dev/null || true
    echo "\`\`\`"
    echo
    echo "**RUN 006: FAIL**"
    echo
    echo "Report preserved at:"
    echo "\`$REPORT\`"
fi' EXIT

echo "# PCC-01 — CORE EXPERIENCE FINAL INSPECTION AND CONSERVATION — RUN 006"
echo
echo "**Stage:** Core Experience conservation"
echo
echo "**Execution date:** 2026-08-13"
echo
echo "**Expected baseline:** \`$EXPECTED_HEAD\`"
echo
echo "**Commit message:** \`$COMMIT_MESSAGE\`"
echo
echo "**Purpose:** Final inspection and Git conservation of the first executable Core Experience foundation." 
echo
echo "---"

echo
echo "## 1. Baseline Verification"
echo
echo '```text'

git fetch origin main --quiet

LOCAL="$(git rev-parse HEAD)"
REMOTE="$(git rev-parse origin/main)"

echo "Expected:    $EXPECTED_HEAD"
echo "LOCAL:       $LOCAL"
echo "origin/main: $REMOTE"

if [ "$LOCAL" != "$EXPECTED_HEAD" ]; then
    echo "FAIL: local HEAD differs from expected baseline"
    exit 1
fi

if [ "$REMOTE" != "$EXPECTED_HEAD" ]; then
    echo "FAIL: origin/main differs from expected baseline"
    exit 1
fi

echo "PASS: LOCAL == expected baseline"
echo "PASS: origin/main == expected baseline"
echo '```'

echo
echo "## 2. Required Software Anatomy"
echo
echo '```text'

SOFTWARE_FILES=(
    "$PKG/__init__.py"
    "$PKG/identity.py"
    "$PKG/model.py"
    "$PKG/lifecycle.py"
    "$PKG/repository.py"
    "$PKG/service.py"
    "$TESTS/test_experience_identity.py"
    "$TESTS/test_experience_model.py"
    "$TESTS/test_experience_lifecycle.py"
    "$TESTS/test_experience_repository.py"
    "$TESTS/test_experience_service.py"
    "$TESTS/test_experience_core.py"
)

for FILE in "${SOFTWARE_FILES[@]}"; do
    if [ ! -f "$FILE" ]; then
        echo "FAIL: required Core Experience tissue missing:"
        echo "$FILE"
        exit 1
    fi

    echo "PASS: $FILE"
done

echo
echo "PASS: all 12 required Core Experience files exist"
echo '```'

echo
echo "## 3. Required Implementation Reports"
echo
echo '```text'

RUN_001="$REPORT_DIR/PCC-01_CORE_EXPERIENCE_IDENTITY_MODEL_LIFECYCLE_IMPLEMENTATION_REPORT.md"
RUN_002="$REPORT_DIR/PCC-01_CORE_EXPERIENCE_IDENTITY_MODEL_LIFECYCLE_IMPLEMENTATION_REPORT_RUN_002.md" 
RUN_003="$REPORT_DIR/PCC-01_CORE_EXPERIENCE_REPOSITORY_SERVICE_IMPLEMENTATION_REPORT_RUN_003.md"
RUN_004="$REPORT_DIR/PCC-01_CORE_EXPERIENCE_REGRESSION_VERIFICATION_REPORT_RUN_004.md"
RUN_005="$REPORT_DIR/PCC-01_CORE_EXPERIENCE_REGRESSION_CAUSALITY_INSPECTION_RUN_005.md"

REPORT_FILES=(
    "$RUN_001"
    "$RUN_002"
    "$RUN_003"
    "$RUN_004"
    "$RUN_005"
    "$REPORT"
)

for FILE in "${REPORT_FILES[@]}"; do
    if [ ! -f "$FILE" ]; then
        echo "FAIL: required implementation report missing:"
        echo "$FILE"
        exit 1
    fi

    echo "PASS: $FILE"
done

echo "PASS: RUN 001 -> RUN 006 report lineage present"
echo '```'

echo
echo "## 4. Verify Historical Investigation Conclusions"
echo
echo '```text'

grep -Fq \
    '**Classification:** PRE-EXISTING BASELINE FAILURE' \
    "$RUN_005" || {
        echo "FAIL: RUN 005 does not contain expected causality classification"
        exit 1
    }

grep -Fq \
    'PASS: dedicated PCC-01 Core Experience suite' \
    "$RUN_005" || {
        echo "FAIL: RUN 005 does not contain dedicated PCC-01 PASS"
        exit 1
    }

grep -Fq \
    '**Implementation Status:** NOT DEMONSTRATED' \
    "$RUN_005" || {
        echo "FAIL: RUN 005 epistemic implementation status altered"
        exit 1
    }

grep -Fq \
    '**Canonical Status:** NOT CANON' \
    "$RUN_005" || {
        echo "FAIL: RUN 005 canonical status altered"
        exit 1
    }

grep -Fq \
    '**Production Status:** NOT PRODUCTION-READY' \
    "$RUN_005" || {
        echo "FAIL: RUN 005 production status altered"
        exit 1
    }

echo "PASS: unrelated CSL failure classified as pre-existing"
echo "PASS: PCC-01 dedicated suite previously passed"
echo "PASS: epistemic status preserved"
echo '```'

echo
echo "## 5. Working Tree Boundary Before Conservation"
echo
echo '```text'

STATUS="$(git status --porcelain)"

UNEXPECTED="$(
    printf '%s\n' "$STATUS" |
    grep -vE '^\?\? lib/python/experience(/|$)' |
    grep -vE '^\?\? tests/experience(/|$)' |
    grep -vE '^\?\? work/implementation-reports(/|$)' |
    sed '/^$/d' || true
)"

if [ -n "$UNEXPECTED" ]; then
    echo "FAIL: unexpected working-tree changes:"
    echo "$UNEXPECTED"
    exit 1
fi

echo "$STATUS"
echo
echo "PASS: only authorized PCC-01 software/tests/reports are untracked"
echo '```'

echo
echo "## 6. Fresh Dedicated Behavioral Verification"
echo
echo '```text'

export PYTHONPATH="$PWD:$PWD/lib${PYTHONPATH:+:$PYTHONPATH}"

python -m pytest -q "$TESTS"

echo "PASS: fresh dedicated PCC-01 Core Experience suite"
echo '```'

echo
echo "## 7. Central Identity Behavior Within Current Process"
echo
echo '```text'

python - <<'PY'
from lib.python.experience.repository import InMemoryExperienceRepository
from lib.python.experience.service import ExperienceService

repository = InMemoryExperienceRepository()
service = ExperienceService(repository)

created = service.create_experience()
identity = created.experience_id

active = service.activate_experience(identity)
loaded_active = service.get_experience(identity)
closed = service.close_experience(identity)
loaded_closed = service.get_experience(identity)

assert active.experience_id == identity
assert loaded_active.experience_id == identity
assert closed.experience_id == identity
assert loaded_closed.experience_id == identity

print(f"Experience identity: {identity}")
print("PASS: identity preserved through create -> activate -> load -> close -> load")
print("NON-CLAIM: no real process death/restart occurred")
PY

echo '```'

echo
echo "## 8. Epistemic Boundary Inspection"
echo
echo '```text'

python - <<'PY'
from dataclasses import fields

from lib.python.experience.model import Experience

actual = {field.name for field in fields(Experience)}

forbidden = {
    "session",
    "session_id",
    "memory",
    "memory_id",
    "evidence",
    "evidence_id",
    "dialogue",
    "raw_dialogue",
    "provider",
    "process",
    "authority",
}

intersection = actual & forbidden

print("Experience fields:", sorted(actual))
print("Forbidden intersection:", sorted(intersection))

assert not intersection

print("PASS: Experience model does not collapse neighboring epistemic organs")
PY

echo
echo "Experience != Session"
echo "Experience != Memory"
echo "Experience != Evidence"
echo "Experience != raw dialogue"
echo "Session != process"
echo "Session != provider"
echo "Storage != Experience"
echo "Interpretation != historical fact"
echo "Persistence != authority"
echo "Human Acceptance != Implementation"
echo '```'

echo
echo "## 9. Software Integrity Before Staging"
echo
echo '```text'

for FILE in "${SOFTWARE_FILES[@]}"; do
    sha256sum "$FILE"
done

echo '```'

echo
echo "## 10. Verify Empty Staging Area"
echo
echo '```text'

STAGED_BEFORE="$(git diff --cached --name-only)"

if [ -n "$STAGED_BEFORE" ]; then
    echo "FAIL: staging area is not empty:"
    echo "$STAGED_BEFORE"
    exit 1
fi

echo "PASS: staging area empty"
echo '```'

echo
echo "## 11. Prepare RUN 006 Report for Conservation"
echo
echo "The following artifacts are authorized for this conservation:"
echo
echo "- Core Experience software tissue"
echo "- Core Experience dedicated tests"
echo "- RUN 001 through RUN 006 implementation/inspection reports"
echo
echo "No Canon document is authorized."
echo
echo "No unrelated repository tissue is authorized."

echo
echo "## 12. PCC-01 Status Before Commit"
echo
echo "**Implementation Status:** NOT DEMONSTRATED"
echo
echo "**Canonical Status:** NOT CANON"
echo
echo "**Production Status:** NOT PRODUCTION-READY"
echo
echo
echo "The real restart invariant remains undemonstrated:"
echo
echo "**ID_before_restart == ID_after_restart**"
echo
echo
echo "The current in-memory Repository is explicitly process-local."

echo
echo "## 13. Conservation Intent"
echo
echo "This commit conserves a tested Core Experience foundation."
echo
echo "It does NOT declare complete PCC-01 implementation."
echo
echo "It does NOT modify Canon."
echo
echo "It does NOT claim production readiness."
echo
echo "It does NOT claim real process restart continuity."

echo
echo "## 14. Pre-Commit Report Marker"
echo
echo "**PRE-COMMIT INSPECTION:** PASS"
echo
echo
echo "RUN 006 will now stage only the explicitly authorized PCC-01 paths."

# Flush output so the report contains the complete pre-commit record.
sync

echo
echo "## 15. Stage Authorized PCC-01 Artifacts"
echo
echo '```text'

git add \
    "$PKG" \
    "$TESTS" \
    "$REPORT_DIR"

STAGED="$(git diff --cached --name-only)"

echo "$STAGED"

EXPECTED_STAGED_FILE="$(mktemp)"
ACTUAL_STAGED_FILE="$(mktemp)"

{
    for FILE in "${SOFTWARE_FILES[@]}"; do
        echo "$FILE"
    done

    for FILE in "${REPORT_FILES[@]}"; do
        echo "$FILE"
    done
} | sort -u > "$EXPECTED_STAGED_FILE"

printf '%s\n' "$STAGED" | sed '/^$/d' | sort -u > "$ACTUAL_STAGED_FILE"

if ! diff -u "$EXPECTED_STAGED_FILE" "$ACTUAL_STAGED_FILE"; then
    echo "FAIL: staged file set differs from authorized file set"
    git reset
    rm -f "$EXPECTED_STAGED_FILE" "$ACTUAL_STAGED_FILE"
    exit 1
fi

rm -f "$EXPECTED_STAGED_FILE" "$ACTUAL_STAGED_FILE"

echo
echo "PASS: staged set contains exactly authorized PCC-01 artifacts"
echo '```'

echo
echo "## 16. Verify No Canon Modification"
echo
echo '```text'

if git diff --cached --name-only | grep -E '(^|/)canon(/|$)|^docs/canonical/' >/dev/null; then
    echo "FAIL: Canon path detected in staged set"
    git reset
    exit 1
fi

echo "PASS: no Canon path staged"
echo '```'

echo
echo "## 17. Commit Core Experience Foundation"
echo
echo '```text'

OLD_HEAD="$(git rev-parse HEAD)"

git commit -m "$COMMIT_MESSAGE"

COMMIT_CREATED="YES"

NEW_HEAD="$(git rev-parse HEAD)"

echo "OLD HEAD: $OLD_HEAD"
echo "NEW HEAD: $NEW_HEAD"
echo "PASS: conservation commit created"
echo '```'

echo
echo "## 18. Verify Commit Scope"
echo
echo '```text'

COMMITTED="$(git diff-tree --no-commit-id --name-only -r "$NEW_HEAD" | sort -u)"

echo "$COMMITTED"

COMMITTED_FILE="$(mktemp)"
EXPECTED_COMMITTED_FILE="$(mktemp)"

printf '%s\n' "$COMMITTED" | sed '/^$/d' | sort -u > "$COMMITTED_FILE"

{
    for FILE in "${SOFTWARE_FILES[@]}"; do
        echo "$FILE"
    done

    for FILE in "${REPORT_FILES[@]}"; do
        echo "$FILE"
    done
} | sort -u > "$EXPECTED_COMMITTED_FILE"

if ! diff -u "$EXPECTED_COMMITTED_FILE" "$COMMITTED_FILE"; then
    echo "FAIL: commit scope differs from authorized scope"
    rm -f "$COMMITTED_FILE" "$EXPECTED_COMMITTED_FILE"
    exit 1
fi

rm -f "$COMMITTED_FILE" "$EXPECTED_COMMITTED_FILE"

echo
echo "PASS: commit contains exactly authorized PCC-01 artifacts"
echo '```'

echo
echo "## 19. Push Conservation Commit"
echo
echo '```text'

git push origin main
PUSH_COMPLETED="YES"

git fetch origin main --quiet

LOCAL_AFTER="$(git rev-parse HEAD)"
REMOTE_AFTER="$(git rev-parse origin/main)"

echo "LOCAL:       $LOCAL_AFTER"
echo "origin/main: $REMOTE_AFTER"

if [ "$LOCAL_AFTER" != "$REMOTE_AFTER" ]; then
    echo "FAIL: LOCAL != origin/main after push"
    exit 1
fi

echo "PASS: LOCAL == origin/main"
echo '```'

echo
echo "## 20. Final Working Tree"
echo
echo '```text'

FINAL_STATUS="$(git status --short)"

if [ -n "$FINAL_STATUS" ]; then
    echo "$FINAL_STATUS"
    echo "FAIL: working tree not clean after conservation"
    exit 1
fi

echo "(clean)"
echo "PASS: working tree clean"
echo '```'

echo
echo "## 21. Final Epistemic State"
echo
echo "**Core Experience foundation:** CONSERVED"
echo
echo "**Implementation Status:** NOT DEMONSTRATED"
echo
echo "**Canonical Status:** NOT CANON"
echo
echo "**Production Status:** NOT PRODUCTION-READY"
echo
echo
echo "Conservation means the tested tissue is preserved in repository history."
echo
echo "Conservation does NOT mean complete PCC-01 implementation or Human Acceptance of final behavior." 
echo
echo
echo "**ID_before_restart == ID_after_restart** remains to be demonstrated across real process death." 

echo
echo "## 22. Final Result"
echo
echo "**RUN 006: PASS**"
echo
echo "**Core Experience foundation:** CONSERVED"
echo
echo "**New HEAD:** \`$LOCAL_AFTER\`"
echo
echo "**LOCAL == origin/main:** YES"
echo
echo "**Working tree:** CLEAN"
echo
echo
echo "**NEXT PCC-01 PHASE:** Session Binding"
echo
echo "---"
echo
echo "END OF PCC-01 CORE EXPERIENCE FINAL INSPECTION AND CONSERVATION — RUN 006"

# The report changed after the commit because final synchronization results
[7m# were appended. Amend ONLY the report so the committed report contains its[27m
[7m# own final result.[27m
[7mgit add "$REPORT"[27m

[7mPOST_STAGE="$(git diff --cached --name-only)"[27m

[7mif [ "$POST_STAGE" != "$REPORT" ]; then[27m
[7m    echo[27m
[7m    echo "FAIL: unexpected path staged during final report amendment"[27m
[7m    echo "$POST_STAGE"[27m
[7m    exit 1[27m
[7mfi[27m

[7mgit commit --amend --no-edit[27m

[7mFINAL_HEAD="$(git rev-parse HEAD)"[27m

[7mgit push --force-with-lease origin main[27m
[7mgit fetch origin main --quiet[27m

[7mFINAL_REMOTE="$(git rev-parse origin/main)"[27m

[7mif [ "$FINAL_HEAD" != "$FINAL_REMOTE" ]; then[27m
[7m    echo "FAIL: final amended HEAD differs from origin/main"[27m
[7m    exit 1[27m
[7mfi[27m

[7mif [ -n "$(git status --porcelain)" ]; then[27m
[7m    echo "FAIL: final working tree is not clean"[27m
[7m    git status --short[27m
[7m    exit 1[27m
[7mfi[27m

[7mtrap - EXIT[27m

[7mecho[27m
[7mecho "=========================================================="[27m
[7mecho "RUN 006 COMPLETE"[27m
[7mecho "=========================================================="[27m
[7mecho "FINAL HEAD:"[27m
[7mecho "$FINAL_HEAD"[27m
[7mecho[27m
[7mecho "origin/main:"[27m
[7mecho "$FINAL_REMOTE"[27m
[7mecho[27m
[7mecho "REPORT:"[27m
[7mecho "$REPORT"[27m
[7mecho[27m
[7mecho "CORE EXPERIENCE FOUNDATION CONSERVED"[27m
[7mecho[27m
[7mecho "PCC-01 remains NOT DEMONSTRATED"[27m
[7mecho "NOT CANON"[27m
[7mecho "NOT PRODUCTION-READY"[27m
[7mecho[27m
[7mecho "NEXT PHASE:"[27m
[7mecho "SESSION BINDING"[27m
[7mecho "=========================================================="[27m[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A# were appended. Amend ONLY the report so the committed report contains its
# own final result.
git add "$REPORT"

POST_STAGE="$(git diff --cached --name-only)"

if [ "$POST_STAGE" != "$REPORT" ]; then
    echo
    echo "FAIL: unexpected path staged during final report amendment"
    echo "$POST_STAGE"
    exit 1
fi

git commit --amend --no-edit

FINAL_HEAD="$(git rev-parse HEAD)"

git push --force-with-lease origin main
git fetch origin main --quiet

FINAL_REMOTE="$(git rev-parse origin/main)"

if [ "$FINAL_HEAD" != "$FINAL_REMOTE" ]; then
    echo "FAIL: final amended HEAD differs from origin/main"
    exit 1
fi

if [ -n "$(git status --porcelain)" ]; then
    echo "FAIL: final working tree is not clean"
    git status --short
    exit 1
fi

trap - EXIT

echo
echo "=========================================================="
echo "RUN 006 COMPLETE"
echo "=========================================================="
echo "FINAL HEAD:"
echo "$FINAL_HEAD"
echo
echo "origin/main:"
echo "$FINAL_REMOTE"
echo
echo "REPORT:"
echo "$REPORT"
echo
echo "CORE EXPERIENCE FOUNDATION CONSERVED"
echo
echo "PCC-01 remains NOT DEMONSTRATED"
echo "NOT CANON"
echo "NOT PRODUCTION-READY"
echo
echo "NEXT PHASE:"
echo "SESSION BINDING"
echo "=========================================================="
[?2004l# PCC-01 — CORE EXPERIENCE FINAL INSPECTION AND CONSERVATION — RUN 006

**Stage:** Core Experience conservation

**Execution date:** 2026-08-13

**Expected baseline:** `d477d2523343b8e583eb43aec0091c608eb6d038`

**Commit message:** `feat: preserve PCC-01 core experience foundation`

**Purpose:** Final inspection and Git conservation of the first executable Core Experience foundation.

---

## 1. Baseline Verification

```text
Expected:    d477d2523343b8e583eb43aec0091c608eb6d038
LOCAL:       d477d2523343b8e583eb43aec0091c608eb6d038
origin/main: d477d2523343b8e583eb43aec0091c608eb6d038
PASS: LOCAL == expected baseline
PASS: origin/main == expected baseline
```

## 2. Required Software Anatomy

```text
PASS: lib/python/experience/__init__.py
PASS: lib/python/experience/identity.py
PASS: lib/python/experience/model.py
PASS: lib/python/experience/lifecycle.py
PASS: lib/python/experience/repository.py
PASS: lib/python/experience/service.py
PASS: tests/experience/test_experience_identity.py
PASS: tests/experience/test_experience_model.py
PASS: tests/experience/test_experience_lifecycle.py
PASS: tests/experience/test_experience_repository.py
PASS: tests/experience/test_experience_service.py
PASS: tests/experience/test_experience_core.py

PASS: all 12 required Core Experience files exist
```

## 3. Required Implementation Reports

```text
PASS: work/implementation-reports/PCC-01/PCC-01_CORE_EXPERIENCE_IDENTITY_MODEL_LIFECYCLE_IMPLEMENTATION_REPORT.md
PASS: work/implementation-reports/PCC-01/PCC-01_CORE_EXPERIENCE_IDENTITY_MODEL_LIFECYCLE_IMPLEMENTATION_REPORT_RUN_002.md
PASS: work/implementation-reports/PCC-01/PCC-01_CORE_EXPERIENCE_REPOSITORY_SERVICE_IMPLEMENTATION_REPORT_RUN_003.md
PASS: work/implementation-reports/PCC-01/PCC-01_CORE_EXPERIENCE_REGRESSION_VERIFICATION_REPORT_RUN_004.md
PASS: work/implementation-reports/PCC-01/PCC-01_CORE_EXPERIENCE_REGRESSION_CAUSALITY_INSPECTION_RUN_005.md
PASS: work/implementation-reports/PCC-01/PCC-01_CORE_EXPERIENCE_FINAL_INSPECTION_AND_CONSERVATION_RUN_006.md
PASS: RUN 001 -> RUN 006 report lineage present
```

## 4. Verify Historical Investigation Conclusions

```text
PASS: unrelated CSL failure classified as pre-existing
PASS: PCC-01 dedicated suite previously passed
PASS: epistemic status preserved
```

## 5. Working Tree Boundary Before Conservation

```text
?? lib/python/experience/
?? tests/experience/
?? work/implementation-reports/

PASS: only authorized PCC-01 software/tests/reports are untracked
```

## 6. Fresh Dedicated Behavioral Verification

```text
..................................                                       [100%]
34 passed in 0.47s
PASS: fresh dedicated PCC-01 Core Experience suite
```

## 7. Central Identity Behavior Within Current Process

```text
Experience identity: 5fa551d5-4d9f-4ee8-b92b-58235143d309
PASS: identity preserved through create -> activate -> load -> close -> load
NON-CLAIM: no real process death/restart occurred
```

## 8. Epistemic Boundary Inspection

```text
Experience fields: ['created_at', 'experience_id', 'state']
Forbidden intersection: []
PASS: Experience model does not collapse neighboring epistemic organs

Experience != Session
Experience != Memory
Experience != Evidence
Experience != raw dialogue
Session != process
Session != provider
Storage != Experience
Interpretation != historical fact
Persistence != authority
Human Acceptance != Implementation
```

## 9. Software Integrity Before Staging

```text
0fa836364d5ad2adbd9aedbc3d806df3c46210584690dec1b2ff82bcc4a344cb  lib/python/experience/__init__.py
4b9299f4d90c453cb194094783c774c201710a389c805f366924a738df944fc3  lib/python/experience/identity.py
a9ca99c19189144eff0ae37c3a0f272c7a363b5b41b21dab9347eb12c6d89ead  lib/python/experience/model.py
3fc9433b7e768bded4bc39b988400b8532b887b5b2e86c7c714332e5afa87020  lib/python/experience/lifecycle.py
5d3ebb6e40664613dc2d36a70a7b7e23adb17edff0680fdac2ed1b99e3215787  lib/python/experience/repository.py
0e72d60cf8714eaee6d974a254080957127cb704fd26ebffaabec4995e22620e  lib/python/experience/service.py
a2b349569f991e1406ffce2d8dfc34fc569c36b4cec0147b6cdc68f279284f9f  tests/experience/test_experience_identity.py
c71fd9dfd8811a350aabc17580ec6c65ca52ba66da43c8e6baa03e59656446db  tests/experience/test_experience_model.py
ccc9fbe02aa331e8590ab1fb5b96747cf9dcd26b616fbfb8aebd43bac09a00df  tests/experience/test_experience_lifecycle.py
f04969f7c1d0ed62e2a476572303ddfda68a552967164923ef6cce7061836837  tests/experience/test_experience_repository.py
ce4d4ce1fa74b6880ac9250d7e776db99c77bf6d142156dd865e03a4fb348a56  tests/experience/test_experience_service.py
d1a18ccaee74ac0420d35b4d479e8e34f420f1d9d7f42c896edac87801464422  tests/experience/test_experience_core.py
```

## 10. Verify Empty Staging Area

```text
PASS: staging area empty
```

## 11. Prepare RUN 006 Report for Conservation

The following artifacts are authorized for this conservation:

- Core Experience software tissue
- Core Experience dedicated tests
- RUN 001 through RUN 006 implementation/inspection reports

No Canon document is authorized.

No unrelated repository tissue is authorized.

## 12. PCC-01 Status Before Commit

**Implementation Status:** NOT DEMONSTRATED

**Canonical Status:** NOT CANON

**Production Status:** NOT PRODUCTION-READY


The real restart invariant remains undemonstrated:

**ID_before_restart == ID_after_restart**


The current in-memory Repository is explicitly process-local.

## 13. Conservation Intent

This commit conserves a tested Core Experience foundation.

It does NOT declare complete PCC-01 implementation.

It does NOT modify Canon.

It does NOT claim production readiness.

It does NOT claim real process restart continuity.

## 14. Pre-Commit Report Marker

**PRE-COMMIT INSPECTION:** PASS


RUN 006 will now stage only the explicitly authorized PCC-01 paths.

## 15. Stage Authorized PCC-01 Artifacts

```text

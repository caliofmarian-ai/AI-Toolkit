# PCC-01 — CORE EXPERIENCE POST-CONSERVATION RECOVERY INSPECTION — RUN 007

**Purpose:** Inspect the partial terminal state left by RUN 006 without modifying conserved software or historical reports.

**Expected conserved HEAD:** `e8f4f230d9021a8acb469f465df651dff5b21c84`

**Software modification:** NONE

**Historical report modification:** NONE

**Git conservation:** NONE

---

## 1. Verify Conserved HEAD

```text
Expected:    e8f4f230d9021a8acb469f465df651dff5b21c84
LOCAL:       e8f4f230d9021a8acb469f465df651dff5b21c84
origin/main: e8f4f230d9021a8acb469f465df651dff5b21c84
PASS: LOCAL == conserved HEAD
PASS: origin/main == conserved HEAD
```

## 2. Verify Conservation Commit

```text
Commit:
e8f4f230d9021a8acb469f465df651dff5b21c84
feat: preserve PCC-01 core experience foundation

Files in commit: 18
PASS: conservation commit exists with expected message
PASS: conservation commit contains 18 files
```

## 3. Verify Conserved Core Experience Anatomy

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

PASS: all 12 Core Experience software/test files are conserved
```

## 4. Current Working Tree

```text
 M work/implementation-reports/PCC-01/PCC-01_CORE_EXPERIENCE_FINAL_INSPECTION_AND_CONSERVATION_RUN_006.md
 M work/implementation-reports/PCC-01/PCC-01_CORE_EXPERIENCE_REGRESSION_CAUSALITY_INSPECTION_RUN_005.md
?? work/implementation-reports/PCC-01/PCC-01_CORE_EXPERIENCE_POST_CONSERVATION_RECOVERY_INSPECTION_RUN_007.md
```

## 5. RUN 005 Integrity Investigation

```text
Working-tree SHA: 00f293c7600581e740064dcadefec4d7dcc6582b416754fed4236d7520d94846
Committed SHA:    c432a36cdbf9a896f6952bc3c7dd64bd603e05b7ed1435e6e46d153ba1fe7d9e
CLASSIFICATION: RUN 005 MODIFIED AFTER CONSERVATION

Diff statistics:
 ...ENCE_REGRESSION_CAUSALITY_INSPECTION_RUN_005.md | 121 +++++++++++++++++++++
 1 file changed, 121 insertions(+)

Diff:
diff --git a/work/implementation-reports/PCC-01/PCC-01_CORE_EXPERIENCE_REGRESSION_CAUSALITY_INSPECTION_RUN_005.md b/work/implementation-reports/PCC-01/PCC-01_CORE_EXPERIENCE_REGRESSION_CAUSALITY_INSPECTION_RUN_005.md
index e2491bd..6650dca 100644
--- a/work/implementation-reports/PCC-01/PCC-01_CORE_EXPERIENCE_REGRESSION_CAUSALITY_INSPECTION_RUN_005.md
+++ b/work/implementation-reports/PCC-01/PCC-01_CORE_EXPERIENCE_REGRESSION_CAUSALITY_INSPECTION_RUN_005.md
@@ -1228,3 +1228,124 @@ RUN 006 will now stage only the explicitly authorized PCC-01 paths.
 ## 15. Stage Authorized PCC-01 Artifacts
 
 ```text
+lib/python/experience/__init__.py
+lib/python/experience/identity.py
+lib/python/experience/lifecycle.py
+lib/python/experience/model.py
+lib/python/experience/repository.py
+lib/python/experience/service.py
+tests/experience/test_experience_core.py
+tests/experience/test_experience_identity.py
+tests/experience/test_experience_lifecycle.py
+tests/experience/test_experience_model.py
+tests/experience/test_experience_repository.py
+tests/experience/test_experience_service.py
+work/implementation-reports/PCC-01/PCC-01_CORE_EXPERIENCE_FINAL_INSPECTION_AND_CONSERVATION_RUN_006.md
+work/implementation-reports/PCC-01/PCC-01_CORE_EXPERIENCE_IDENTITY_MODEL_LIFECYCLE_IMPLEMENTATION_REPORT.md
+work/implementation-reports/PCC-01/PCC-01_CORE_EXPERIENCE_IDENTITY_MODEL_LIFECYCLE_IMPLEMENTATION_REPORT_RUN_002.md
+work/implementation-reports/PCC-01/PCC-01_CORE_EXPERIENCE_REGRESSION_CAUSALITY_INSPECTION_RUN_005.md
+work/implementation-reports/PCC-01/PCC-01_CORE_EXPERIENCE_REGRESSION_VERIFICATION_REPORT_RUN_004.md
+work/implementation-reports/PCC-01/PCC-01_CORE_EXPERIENCE_REPOSITORY_SERVICE_IMPLEMENTATION_REPORT_RUN_003.md
+
+PASS: staged set contains exactly authorized PCC-01 artifacts
+```
+
+## 16. Verify No Canon Modification
+
+```text
+PASS: no Canon path staged
+```
+
+## 17. Commit Core Experience Foundation
+
+```text
+[main e8f4f23] feat: preserve PCC-01 core experience foundation
+ 18 files changed, 2351 insertions(+)
+ create mode 100644 lib/python/experience/__init__.py
+ create mode 100644 lib/python/experience/identity.py
+ create mode 100644 lib/python/experience/lifecycle.py
+ create mode 100644 lib/python/experience/model.py
+ create mode 100644 lib/python/experience/repository.py
+ create mode 100644 lib/python/experience/service.py
+ create mode 100644 tests/experience/test_experience_core.py
+ create mode 100644 tests/experience/test_experience_identity.py
+ create mode 100644 tests/experience/test_experience_lifecycle.py
+ create mode 100644 tests/experience/test_experience_model.py
+ create mode 100644 tests/experience/test_experience_repository.py
+ create mode 100644 tests/experience/test_experience_service.py
+ create mode 100644 work/implementation-reports/PCC-01/PCC-01_CORE_EXPERIENCE_FINAL_INSPECTION_AND_CONSERVATION_RUN_006.md
+ create mode 100644 work/implementation-reports/PCC-01/PCC-01_CORE_EXPERIENCE_IDENTITY_MODEL_LIFECYCLE_IMPLEMENTATION_REPORT.md
+ create mode 100644 work/implementation-reports/PCC-01/PCC-01_CORE_EXPERIENCE_IDENTITY_MODEL_LIFECYCLE_IMPLEMENTATION_REPORT_RUN_002.md
+ create mode 100644 work/implementation-reports/PCC-01/PCC-01_CORE_EXPERIENCE_REGRESSION_CAUSALITY_INSPECTION_RUN_005.md
+ create mode 100644 work/implementation-reports/PCC-01/PCC-01_CORE_EXPERIENCE_REGRESSION_VERIFICATION_REPORT_RUN_004.md
+ create mode 100644 work/implementation-reports/PCC-01/PCC-01_CORE_EXPERIENCE_REPOSITORY_SERVICE_IMPLEMENTATION_REPORT_RUN_003.md
+OLD HEAD: d477d2523343b8e583eb43aec0091c608eb6d038
+NEW HEAD: e8f4f230d9021a8acb469f465df651dff5b21c84
+PASS: conservation commit created
+```
+
+## 18. Verify Commit Scope
+
+```text
+lib/python/experience/__init__.py
+lib/python/experience/identity.py
+lib/python/experience/lifecycle.py
+lib/python/experience/model.py
+lib/python/experience/repository.py
+lib/python/experience/service.py
+tests/experience/test_experience_core.py
+tests/experience/test_experience_identity.py
+tests/experience/test_experience_lifecycle.py
+tests/experience/test_experience_model.py
+tests/experience/test_experience_repository.py
+tests/experience/test_experience_service.py
+work/implementation-reports/PCC-01/PCC-01_CORE_EXPERIENCE_FINAL_INSPECTION_AND_CONSERVATION_RUN_006.md
+work/implementation-reports/PCC-01/PCC-01_CORE_EXPERIENCE_IDENTITY_MODEL_LIFECYCLE_IMPLEMENTATION_REPORT.md
+work/implementation-reports/PCC-01/PCC-01_CORE_EXPERIENCE_IDENTITY_MODEL_LIFECYCLE_IMPLEMENTATION_REPORT_RUN_002.md
+work/implementation-reports/PCC-01/PCC-01_CORE_EXPERIENCE_REGRESSION_CAUSALITY_INSPECTION_RUN_005.md
+work/implementation-reports/PCC-01/PCC-01_CORE_EXPERIENCE_REGRESSION_VERIFICATION_REPORT_RUN_004.md
+work/implementation-reports/PCC-01/PCC-01_CORE_EXPERIENCE_REPOSITORY_SERVICE_IMPLEMENTATION_REPORT_RUN_003.md
+
+PASS: commit contains exactly authorized PCC-01 artifacts
+```
+
+## 19. Push Conservation Commit
+
+```text
+To https://github.com/caliofmarian-ai/AI-Toolkit.git
+   d477d25..e8f4f23  main -> main
+LOCAL:       e8f4f230d9021a8acb469f465df651dff5b21c84
+origin/main: e8f4f230d9021a8acb469f465df651dff5b21c84
+PASS: LOCAL == origin/main
+```
+
+## 20. Final Working Tree
+
+```text
+ M work/implementation-reports/PCC-01/PCC-01_CORE_EXPERIENCE_FINAL_INSPECTION_AND_CONSERVATION_RUN_006.md
+ M work/implementation-reports/PCC-01/PCC-01_CORE_EXPERIENCE_REGRESSION_CAUSALITY_INSPECTION_RUN_005.md
+FAIL: working tree not clean after conservation
+logout
+
+## EXECUTION FAILURE
+
+Exit code: 1
+
+Commit created before failure: YES
+Push completed before failure: YES
+
+HEAD at failure:
+```text
+e8f4f230d9021a8acb469f465df651dff5b21c84
+```
+
+Git status at failure:
+```text
+ M work/implementation-reports/PCC-01/PCC-01_CORE_EXPERIENCE_FINAL_INSPECTION_AND_CONSERVATION_RUN_006.md
+ M work/implementation-reports/PCC-01/PCC-01_CORE_EXPERIENCE_REGRESSION_CAUSALITY_INSPECTION_RUN_005.md
+```
+
+**RUN 006: FAIL**
+
+Report preserved at:
+`work/implementation-reports/PCC-01/PCC-01_CORE_EXPERIENCE_FINAL_INSPECTION_AND_CONSERVATION_RUN_006.md`
```

## 6. RUN 006 Integrity Investigation

```text
Working-tree SHA: 6b29f94c77f4a1386855d7b8cd317aaea073ac1919217235ffb6f3dc8d53ee28
Committed SHA:    54265afd8b091268a546bad5a25fc1dd886a90e875e6df4fa398a0cf9c2c7dfa
CLASSIFICATION: RUN 006 MODIFIED AFTER CONSERVATION

Diff statistics:
 ...CE_FINAL_INSPECTION_AND_CONSERVATION_RUN_006.md | 121 +++++++++++++++++++++
 1 file changed, 121 insertions(+)

Diff:
diff --git a/work/implementation-reports/PCC-01/PCC-01_CORE_EXPERIENCE_FINAL_INSPECTION_AND_CONSERVATION_RUN_006.md b/work/implementation-reports/PCC-01/PCC-01_CORE_EXPERIENCE_FINAL_INSPECTION_AND_CONSERVATION_RUN_006.md
index 3417c9a..0959d37 100644
--- a/work/implementation-reports/PCC-01/PCC-01_CORE_EXPERIENCE_FINAL_INSPECTION_AND_CONSERVATION_RUN_006.md
+++ b/work/implementation-reports/PCC-01/PCC-01_CORE_EXPERIENCE_FINAL_INSPECTION_AND_CONSERVATION_RUN_006.md
@@ -179,3 +179,124 @@ RUN 006 will now stage only the explicitly authorized PCC-01 paths.
 ## 15. Stage Authorized PCC-01 Artifacts
 
 ```text
+lib/python/experience/__init__.py
+lib/python/experience/identity.py
+lib/python/experience/lifecycle.py
+lib/python/experience/model.py
+lib/python/experience/repository.py
+lib/python/experience/service.py
+tests/experience/test_experience_core.py
+tests/experience/test_experience_identity.py
+tests/experience/test_experience_lifecycle.py
+tests/experience/test_experience_model.py
+tests/experience/test_experience_repository.py
+tests/experience/test_experience_service.py
+work/implementation-reports/PCC-01/PCC-01_CORE_EXPERIENCE_FINAL_INSPECTION_AND_CONSERVATION_RUN_006.md
+work/implementation-reports/PCC-01/PCC-01_CORE_EXPERIENCE_IDENTITY_MODEL_LIFECYCLE_IMPLEMENTATION_REPORT.md
+work/implementation-reports/PCC-01/PCC-01_CORE_EXPERIENCE_IDENTITY_MODEL_LIFECYCLE_IMPLEMENTATION_REPORT_RUN_002.md
+work/implementation-reports/PCC-01/PCC-01_CORE_EXPERIENCE_REGRESSION_CAUSALITY_INSPECTION_RUN_005.md
+work/implementation-reports/PCC-01/PCC-01_CORE_EXPERIENCE_REGRESSION_VERIFICATION_REPORT_RUN_004.md
+work/implementation-reports/PCC-01/PCC-01_CORE_EXPERIENCE_REPOSITORY_SERVICE_IMPLEMENTATION_REPORT_RUN_003.md
+
+PASS: staged set contains exactly authorized PCC-01 artifacts
+```
+
+## 16. Verify No Canon Modification
+
+```text
+PASS: no Canon path staged
+```
+
+## 17. Commit Core Experience Foundation
+
+```text
+[main e8f4f23] feat: preserve PCC-01 core experience foundation
+ 18 files changed, 2351 insertions(+)
+ create mode 100644 lib/python/experience/__init__.py
+ create mode 100644 lib/python/experience/identity.py
+ create mode 100644 lib/python/experience/lifecycle.py
+ create mode 100644 lib/python/experience/model.py
+ create mode 100644 lib/python/experience/repository.py
+ create mode 100644 lib/python/experience/service.py
+ create mode 100644 tests/experience/test_experience_core.py
+ create mode 100644 tests/experience/test_experience_identity.py
+ create mode 100644 tests/experience/test_experience_lifecycle.py
+ create mode 100644 tests/experience/test_experience_model.py
+ create mode 100644 tests/experience/test_experience_repository.py
+ create mode 100644 tests/experience/test_experience_service.py
+ create mode 100644 work/implementation-reports/PCC-01/PCC-01_CORE_EXPERIENCE_FINAL_INSPECTION_AND_CONSERVATION_RUN_006.md
+ create mode 100644 work/implementation-reports/PCC-01/PCC-01_CORE_EXPERIENCE_IDENTITY_MODEL_LIFECYCLE_IMPLEMENTATION_REPORT.md
+ create mode 100644 work/implementation-reports/PCC-01/PCC-01_CORE_EXPERIENCE_IDENTITY_MODEL_LIFECYCLE_IMPLEMENTATION_REPORT_RUN_002.md
+ create mode 100644 work/implementation-reports/PCC-01/PCC-01_CORE_EXPERIENCE_REGRESSION_CAUSALITY_INSPECTION_RUN_005.md
+ create mode 100644 work/implementation-reports/PCC-01/PCC-01_CORE_EXPERIENCE_REGRESSION_VERIFICATION_REPORT_RUN_004.md
+ create mode 100644 work/implementation-reports/PCC-01/PCC-01_CORE_EXPERIENCE_REPOSITORY_SERVICE_IMPLEMENTATION_REPORT_RUN_003.md
+OLD HEAD: d477d2523343b8e583eb43aec0091c608eb6d038
+NEW HEAD: e8f4f230d9021a8acb469f465df651dff5b21c84
+PASS: conservation commit created
+```
+
+## 18. Verify Commit Scope
+
+```text
+lib/python/experience/__init__.py
+lib/python/experience/identity.py
+lib/python/experience/lifecycle.py
+lib/python/experience/model.py
+lib/python/experience/repository.py
+lib/python/experience/service.py
+tests/experience/test_experience_core.py
+tests/experience/test_experience_identity.py
+tests/experience/test_experience_lifecycle.py
+tests/experience/test_experience_model.py
+tests/experience/test_experience_repository.py
+tests/experience/test_experience_service.py
+work/implementation-reports/PCC-01/PCC-01_CORE_EXPERIENCE_FINAL_INSPECTION_AND_CONSERVATION_RUN_006.md
+work/implementation-reports/PCC-01/PCC-01_CORE_EXPERIENCE_IDENTITY_MODEL_LIFECYCLE_IMPLEMENTATION_REPORT.md
+work/implementation-reports/PCC-01/PCC-01_CORE_EXPERIENCE_IDENTITY_MODEL_LIFECYCLE_IMPLEMENTATION_REPORT_RUN_002.md
+work/implementation-reports/PCC-01/PCC-01_CORE_EXPERIENCE_REGRESSION_CAUSALITY_INSPECTION_RUN_005.md
+work/implementation-reports/PCC-01/PCC-01_CORE_EXPERIENCE_REGRESSION_VERIFICATION_REPORT_RUN_004.md
+work/implementation-reports/PCC-01/PCC-01_CORE_EXPERIENCE_REPOSITORY_SERVICE_IMPLEMENTATION_REPORT_RUN_003.md
+
+PASS: commit contains exactly authorized PCC-01 artifacts
+```
+
+## 19. Push Conservation Commit
+
+```text
+To https://github.com/caliofmarian-ai/AI-Toolkit.git
+   d477d25..e8f4f23  main -> main
+LOCAL:       e8f4f230d9021a8acb469f465df651dff5b21c84
+origin/main: e8f4f230d9021a8acb469f465df651dff5b21c84
+PASS: LOCAL == origin/main
+```
+
+## 20. Final Working Tree
+
+```text
+ M work/implementation-reports/PCC-01/PCC-01_CORE_EXPERIENCE_FINAL_INSPECTION_AND_CONSERVATION_RUN_006.md
+ M work/implementation-reports/PCC-01/PCC-01_CORE_EXPERIENCE_REGRESSION_CAUSALITY_INSPECTION_RUN_005.md
+FAIL: working tree not clean after conservation
+logout
+
+## EXECUTION FAILURE
+
+Exit code: 1
+
+Commit created before failure: YES
+Push completed before failure: YES
+
+HEAD at failure:
+```text
+e8f4f230d9021a8acb469f465df651dff5b21c84
+```
+
+Git status at failure:
+```text
+ M work/implementation-reports/PCC-01/PCC-01_CORE_EXPERIENCE_FINAL_INSPECTION_AND_CONSERVATION_RUN_006.md
+ M work/implementation-reports/PCC-01/PCC-01_CORE_EXPERIENCE_REGRESSION_CAUSALITY_INSPECTION_RUN_005.md
+```
+
+**RUN 006: FAIL**
+
+Report preserved at:
+`work/implementation-reports/PCC-01/PCC-01_CORE_EXPERIENCE_FINAL_INSPECTION_AND_CONSERVATION_RUN_006.md`
```

## 7. Verify Software Has No Post-Commit Mutation

```text
PASS: Core Experience software/tests exactly match conserved HEAD
```

## 8. Fresh Core Experience Behavioral Verification

```text
..................................                                       [100%]
34 passed in 0.41s
PASS: fresh Core Experience behavioral suite
```

## 9. Verify RUN 005 Historical Conclusion In Conserved Version

```text
PASS: conserved RUN 005 records PRE-EXISTING BASELINE FAILURE
PASS: conserved RUN 005 records 34 passing PCC-01 tests
```

## 10. Conservation Assessment

The Core Experience software foundation is already present in commit:

`e8f4f230d9021a8acb469f465df651dff5b21c84`

and that commit is already synchronized with `origin/main`.

RUN 006 failed only after that conservation commit and push had completed.

This RUN does not repair or overwrite RUN 005 or RUN 006.

Their post-conservation working-tree differences are preserved for inspection.

## 11. Epistemic Status

**Core Experience foundation:** CONSERVED IN GIT

**PCC-01 Implementation Status:** NOT DEMONSTRATED

**Canonical Status:** NOT CANON

**Production Status:** NOT PRODUCTION-READY


**ID_before_restart == ID_after_restart** remains undemonstrated across real process death.

## 12. Repository State After Read-Only Inspection

```text
 M work/implementation-reports/PCC-01/PCC-01_CORE_EXPERIENCE_FINAL_INSPECTION_AND_CONSERVATION_RUN_006.md
 M work/implementation-reports/PCC-01/PCC-01_CORE_EXPERIENCE_REGRESSION_CAUSALITY_INSPECTION_RUN_005.md
?? work/implementation-reports/PCC-01/PCC-01_CORE_EXPERIENCE_POST_CONSERVATION_RECOVERY_INSPECTION_RUN_007.md
```

## 13. Safety Record

No `git add` performed.

No commit performed.

No push performed.

No software modified.

No historical report overwritten.

## 14. Final Result

**RUN 007: PASS**

**Conservation commit:** `e8f4f230d9021a8acb469f465df651dff5b21c84`

**LOCAL == origin/main:** YES

**NEXT REQUIRED ACTION:** GPT inspection of RUN 007 before deciding how to reconcile the two modified report files.

---

END OF PCC-01 CORE EXPERIENCE POST-CONSERVATION RECOVERY INSPECTION — RUN 007

==========================================================
RUN 007 COMPLETE
==========================================================
REPORT:
work/implementation-reports/PCC-01/PCC-01_CORE_EXPERIENCE_POST_CONSERVATION_RECOVERY_INSPECTION_RUN_007.md

Send this Markdown file to GPT.

NO git add
NO commit
NO push
==========================================================
[?2004h[0;32m~/.../AI-Projects/AI-Toolkit[0m [0;97m$[0m [K[0;32m~/.../AI-Projects/AI-Toolkit[0m [0;97m$[0m [K[0;32m~/.../AI-Projects/AI-Toolkit[0m [0;97m$[0m [H[2J[0;32m~/.../AI-Projects/AI-Toolkit[0m [0;97m$[0m cd ~/storage/shared/AI-Projects/AI-Toolkit || exit 1

set -uo pipefail

EXPECTED_HEAD="e8f4f230d9021a8acb469f465df651dff5b21c84"

REPORT_DIR="work/implementation-reports/PCC-01"

RUN005="$REPORT_DIR/PCC-01_CORE_EXPERIENCE_REGRESSION_CAUSALITY_INSPECTION_RUN_005.md"
RUN006="$REPORT_DIR/PCC-01_CORE_EXPERIENCE_FINAL_INSPECTION_AND_CONSERVATION_RUN_006.md"
RUN007="$REPORT_DIR/PCC-01_CORE_EXPERIENCE_POST_CONSERVATION_RECOVERY_INSPECTION_RUN_007.md"
REPORT="$REPORT_DIR/PCC-01_CORE_EXPERIENCE_REPORT_RECONCILIATION_RUN_008.md"

COMMIT_MESSAGE="research: preserve PCC-01 post-conservation recovery evidence"

mkdir -p "$REPORT_DIR"
: > "$REPORT"

# IMPORTANT:
# RUN 008 intentionally does NOT redirect the whole shell through tee.
# That mechanism caused the RUN 005/RUN 006 contamination.
#
# All report content is written explicitly only to RUN 008.

write_report() {
    printf '%s\n' "$*" >> "$REPORT"
}

section() {
    printf '\n%s\n' "$*" >> "$REPORT"
}

fail() {
    section "## EXECUTION FAILURE"
    write_report ""
    write_report "**RUN 008: FAIL**"
    write_report ""
    write_report "Reason: $1"
    write_report ""
    write_report "HEAD:"
    write_report '```text'
    git rev-parse HEAD >> "$REPORT" 2>&1 || true
    write_report '```'
    write_report ""
    write_report "Git status:"
    write_report '```text'
    git status --short >> "$REPORT" 2>&1 || true
    write_report '```'
    write_report ""
    write_report "No automatic force-push was performed."
    echo "FAIL: $1"
    echo "REPORT: $REPORT"
    exit 1
}

write_report "# PCC-01 — CORE EXPERIENCE REPORT RECONCILIATION — RUN 008"
write_report ""
write_report "**Purpose:** Reconcile post-conservation report contamination without modifying conserved Core Experience software." 
write_report ""
write_report "**Expected baseline:** \`$EXPECTED_HEAD\`"
write_report ""
write_report "**Software modification:** NONE"
write_report ""
write_report "**Canon modification:** NONE"
write_report ""
write_report "---"

echo "=========================================================="
echo "PCC-01 CORE EXPERIENCE"
echo "RUN 008 — REPORT RECONCILIATION"
echo "=========================================================="

section "## 1. Baseline Verification"
write_report ""
write_report '```text'

git fetch origin main --quiet || fail "git fetch origin main failed"

LOCAL="$(git rev-parse HEAD)"
REMOTE="$(git rev-parse origin/main)"

write_report "Expected:    $EXPECTED_HEAD"
write_report "LOCAL:       $LOCAL"
write_report "origin/main: $REMOTE"

[ "$LOCAL" = "$EXPECTED_HEAD" ] ||
    fail "local HEAD differs from expected conserved HEAD"

[ "$REMOTE" = "$EXPECTED_HEAD" ] ||
    fail "origin/main differs from expected conserved HEAD"

write_report "PASS: LOCAL == expected conserved HEAD"
write_report "PASS: origin/main == expected conserved HEAD"
write_report '```'

echo "PASS: baseline verified"

section "## 2. Verify Expected Working-Tree Incident"
write_report ""
write_report '```text'

STATUS_BEFORE="$(git status --short)"
printf '%s\n' "$STATUS_BEFORE" >> "$REPORT"

EXPECTED_DIRTY="$(
    git status --porcelain |
    grep -vE "^ M $RUN005$" |
    grep -vE "^ M $RUN006$" |
    grep -vE "^\?\? $RUN007$" |
    grep -vE "^\?\? $REPORT$" |
    sed '/^$/d' || true
)"

if [ -n "$EXPECTED_DIRTY" ]; then
    write_report ""
    write_report "Unexpected paths:"
    printf '%s\n' "$EXPECTED_DIRTY" >> "$REPORT"
    write_report '```'
    fail "working tree contains changes outside RUN 005, RUN 006, RUN 007 and RUN 008"
fi

write_report ""
write_report "PASS: working tree contains only the known report incident and recovery reports"
write_report '```'

echo "PASS: incident boundary verified"

section "## 3. Preserve Pre-Reconciliation Integrity Evidence"
write_report ""
write_report '```text'

for FILE in "$RUN005" "$RUN006" "$RUN007"; do
    [ -f "$FILE" ] || fail "required report missing: $FILE"
    SHA="$(sha256sum "$FILE" | awk '{print $1}')"
    write_report "$SHA  $FILE"
done

write_report '```'

section "## 4. Verify RUN 005 and RUN 006 Are Conserved in HEAD"
write_report ""
write_report '```text'

for FILE in "$RUN005" "$RUN006"; do
    if ! git cat-file -e "$EXPECTED_HEAD:$FILE" 2>/dev/null; then
        fail "conserved historical report missing from HEAD: $FILE"
    fi

    COMMITTED_SHA="$(
        git show "$EXPECTED_HEAD:$FILE" |
        sha256sum |
        awk '{print $1}'
    )"

    CURRENT_SHA="$(sha256sum "$FILE" | awk '{print $1}')"

    write_report "FILE: $FILE"
    write_report "Committed SHA: $COMMITTED_SHA"
    write_report "Current SHA:   $CURRENT_SHA"

    if [ "$COMMITTED_SHA" = "$CURRENT_SHA" ]; then
        write_report "STATE: already identical"
    else
        write_report "STATE: post-conservation modification confirmed"
    fi

    write_report ""
done

write_report "PASS: authoritative historical bytes are recoverable from conserved HEAD"
write_report '```'

section "## 5. Restore Historical Reports From Conserved Commit"
write_report ""
write_report '```text'

git restore --source="$EXPECTED_HEAD" --worktree -- "$RUN005" "$RUN006" ||
    fail "could not restore RUN 005/RUN 006 from conserved HEAD"

for FILE in "$RUN005" "$RUN006"; do
    COMMITTED_SHA="$(
        git show "$EXPECTED_HEAD:$FILE" |
        sha256sum |
        awk '{print $1}'
    )"

    RESTORED_SHA="$(sha256sum "$FILE" | awk '{print $1}')"

    write_report "FILE: $FILE"
    write_report "Committed SHA: $COMMITTED_SHA"
    write_report "Restored SHA:  $RESTORED_SHA"

    [ "$COMMITTED_SHA" = "$RESTORED_SHA" ] ||
        fail "restored historical report does not match conserved bytes: $FILE"

    write_report "PASS: exact historical bytes restored"
    write_report ""
done

write_report '```'

echo "PASS: RUN 005 and RUN 006 restored exactly"

section "## 6. Verify Core Experience Software Remains Untouched"
write_report ""
write_report '```text'

SOFTWARE_DIRTY="$(
    git status --porcelain -- lib/python/experience tests/experience |
    sed '/^$/d' || true
)"

if [ -n "$SOFTWARE_DIRTY" ]; then
    printf '%s\n' "$SOFTWARE_DIRTY" >> "$REPORT"
    write_report '```'
    fail "Core Experience software/tests changed during reconciliation"
fi

write_report "PASS: Core Experience software/tests unchanged"
write_report '```'

section "## 7. Fresh Core Experience Behavioral Verification"
write_report ""
write_report '```text'

export PYTHONPATH="$PWD:$PWD/lib${PYTHONPATH:+:$PYTHONPATH}"

TEST_OUTPUT="$(python -m pytest -q tests/experience 2>&1)" || {
    printf '%s\n' "$TEST_OUTPUT" >> "$REPORT"
    write_report '```'
    fail "dedicated Core Experience suite failed"
}

printf '%s\n' "$TEST_OUTPUT" >> "$REPORT"
write_report "PASS: dedicated Core Experience suite"
write_report '```'

echo "$TEST_OUTPUT"
echo "PASS: Core Experience suite"

section "## 8. Post-Reconciliation Working Tree"
write_report ""
write_report '```text'

STATUS_AFTER_RESTORE="$(git status --short)"
printf '%s\n' "$STATUS_AFTER_RESTORE" >> "$REPORT"

UNEXPECTED_AFTER="$(
    git status --porcelain |
    grep -vE "^\?\? $RUN007$" |
    grep -vE "^\?\? $REPORT$" |
    sed '/^$/d' || true
)"

if [ -n "$UNEXPECTED_AFTER" ]; then
    write_report ""
    write_report "Unexpected paths:"
    printf '%s\n' "$UNEXPECTED_AFTER" >> "$REPORT"
    write_report '```'
    fail "historical reports were not reconciled cleanly"
fi

write_report ""
write_report "PASS: RUN 005 and RUN 006 no longer differ from conserved HEAD"
write_report "PASS: only RUN 007 and RUN 008 remain unconserved"
write_report '```'

section "## 9. Epistemic Status"
write_report ""
write_report "**Core Experience foundation:** CONSERVED"
write_report ""
write_report "**PCC-01 Implementation Status:** NOT DEMONSTRATED"
write_report ""
write_report "**Canonical Status:** NOT CANON"
write_report ""
write_report "**Production Status:** NOT PRODUCTION-READY"
write_report ""
write_report "The central invariant remains undemonstrated across real process death:"
write_report ""
write_report "**ID_before_restart == ID_after_restart**"

section "## 10. Reconciliation Interpretation"
write_report ""
write_report "RUN 005 and RUN 006 acquired post-conservation output that was not part of their conserved historical state." 
write_report ""
write_report "RUN 008 restored those two historical reports byte-for-byte from commit \`$EXPECTED_HEAD\`." 
write_report ""
write_report "RUN 007 is retained as evidence of the incident and recovery inspection."
write_report ""
write_report "No Core Experience software was rewritten during reconciliation."

section "## 11. Prepare Recovery Evidence Conservation"
write_report ""
write_report "Authorized new artifacts:"
write_report ""
write_report "- \`$RUN007\`"
write_report "- \`$REPORT\`"
write_report ""
write_report "No historical report modification is authorized."
write_report ""
write_report "No software modification is authorized."
write_report ""
write_report "No Canon modification is authorized."

section "## 12. Pre-Conservation Result"
write_report ""
write_report "**REPORT RECONCILIATION:** PASS"
write_report ""
write_report "**RUN 005 restored:** YES"
write_report ""
write_report "**RUN 006 restored:** YES"
write_report ""
write_report "**Core Experience tests:** PASS"
write_report ""
write_report "**NEXT:** conserve RUN 007 + RUN 008 recovery evidence"

# RUN 008 report is now complete before staging.
sync

echo
echo "[Conservation] Stage only RUN 007 + RUN 008"

git add -- "$RUN007" "$REPORT" ||
    fail "could not stage RUN 007 and RUN 008"

STAGED="$(git diff --cached --name-only)"

EXPECTED_STAGED="$(
    printf '%s\n%s\n' "$RUN007" "$REPORT" |
    sort
)"

ACTUAL_STAGED="$(
    printf '%s\n' "$STAGED" |
    sed '/^$/d' |
    sort
)"

if [ "$ACTUAL_STAGED" != "$EXPECTED_STAGED" ]; then
    git reset
    fail "staging area contains paths outside RUN 007 and RUN 008"
fi

echo "PASS: exactly RUN 007 + RUN 008 staged"

# Historical reports must now be clean.
if [ -n "$(git status --porcelain -- "$RUN005" "$RUN006")" ]; then
    git reset
    fail "RUN 005 or RUN 006 still differs from conserved HEAD"
fi

# Software must still be clean.
if [ -n "$(git status --porcelain -- lib/python/experience tests/experience)" ]; then
    git reset
    fail "software changed before recovery evidence commit"
fi

git commit -m "$COMMIT_MESSAGE" ||
    fail "recovery evidence commit failed"

NEW_HEAD="$(git rev-parse HEAD)"

echo "PASS: recovery evidence commit created"
echo "NEW HEAD: $NEW_HEAD"

[7mCOMMITTED_FILES="$([27m
[7m    git diff-tree --no-commit-id --name-only -r "$NEW_HEAD" |[27m
[7m    sort[27m
[7m)"[27m

[7mif [ "$COMMITTED_FILES" != "$EXPECTED_STAGED" ]; then[27m
[7m    fail "recovery evidence commit contains unexpected paths"[27m
[7mfi[27m

[7mecho "PASS: commit contains exactly RUN 007 + RUN 008"[27m

[7mgit push origin main ||[27m
[7m    fail "push failed"[27m

[7mgit fetch origin main --quiet ||[27m
[7m    fail "post-push fetch failed"[27m

[7mLOCAL_FINAL="$(git rev-parse HEAD)"[27m
[7mREMOTE_FINAL="$(git rev-parse origin/main)"[27m

[7m[ "$LOCAL_FINAL" = "$REMOTE_FINAL" ] ||[27m
[7m    fail "LOCAL != origin/main after recovery evidence conservation"[27m

[7mFINAL_STATUS="$(git status --porcelain)"[27m

[7mif [ -n "$FINAL_STATUS" ]; then[27m
[7m    echo "$FINAL_STATUS"[27m
[7m    fail "working tree is not clean after RUN 008 conservation"[27m
[7mfi[27m

[7mecho[27m
[7mecho "=========================================================="[27m
[7mecho "RUN 008 COMPLETE"[27m
[7mecho "=========================================================="[27m
[7mecho "REPORT RECONCILIATION: PASS"[27m
[7mecho[27m
[7mecho "RUN 005: RESTORED TO CONSERVED BYTES"[27m
[7mecho "RUN 006: RESTORED TO CONSERVED BYTES"[27m
[7mecho[27m
[7mecho "RUN 007 + RUN 008: CONSERVED"[27m
[7mecho[27m
[7mecho "FINAL HEAD:"[27m
[7mecho "$LOCAL_FINAL"[27m
[7mecho[27m
[7mecho "origin/main:"[27m
[7mecho "$REMOTE_FINAL"[27m
[7mecho[27m
[7mecho "WORKING TREE: CLEAN"[27m
[7mecho[27m
[7mecho "PCC-01:"[27m
[7mecho "Implementation Status: NOT DEMONSTRATED"[27m
[7mecho "Canonical Status: NOT CANON"[27m
[7mecho "Production Status: NOT PRODUCTION-READY"[27m
[7mecho[27m
[7mecho "NEXT:"[27m
[7mecho "SESSION BINDING — only after inspection of RUN 008"[27m
[7mecho "=========================================================="[27m[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[ACOMMITTED_FILES="$(
    git diff-tree --no-commit-id --name-only -r "$NEW_HEAD" |
    sort
)"

if [ "$COMMITTED_FILES" != "$EXPECTED_STAGED" ]; then
    fail "recovery evidence commit contains unexpected paths"
fi

echo "PASS: commit contains exactly RUN 007 + RUN 008"

git push origin main ||
    fail "push failed"

git fetch origin main --quiet ||
    fail "post-push fetch failed"

LOCAL_FINAL="$(git rev-parse HEAD)"
REMOTE_FINAL="$(git rev-parse origin/main)"

[ "$LOCAL_FINAL" = "$REMOTE_FINAL" ] ||
    fail "LOCAL != origin/main after recovery evidence conservation"

FINAL_STATUS="$(git status --porcelain)"

if [ -n "$FINAL_STATUS" ]; then
    echo "$FINAL_STATUS"
    fail "working tree is not clean after RUN 008 conservation"
fi

echo
echo "=========================================================="
echo "RUN 008 COMPLETE"
echo "=========================================================="
echo "REPORT RECONCILIATION: PASS"
echo
echo "RUN 005: RESTORED TO CONSERVED BYTES"
echo "RUN 006: RESTORED TO CONSERVED BYTES"
echo
echo "RUN 007 + RUN 008: CONSERVED"
echo
echo "FINAL HEAD:"
echo "$LOCAL_FINAL"
echo
echo "origin/main:"
echo "$REMOTE_FINAL"
echo
echo "WORKING TREE: CLEAN"
echo
echo "PCC-01:"
echo "Implementation Status: NOT DEMONSTRATED"
echo "Canonical Status: NOT CANON"
echo "Production Status: NOT PRODUCTION-READY"
echo
echo "NEXT:"
echo "SESSION BINDING — only after inspection of RUN 008"
echo "=========================================================="
[?2004l==========================================================
PCC-01 CORE EXPERIENCE
RUN 008 — REPORT RECONCILIATION
==========================================================
PASS: baseline verified
PASS: incident boundary verified
PASS: RUN 005 and RUN 006 restored exactly
..................................                                       [100%]
34 passed in 0.38s
PASS: Core Experience suite

[Conservation] Stage only RUN 007 + RUN 008

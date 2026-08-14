# PCC-01 — RUN 055 — Privacy Boundary Implementation

## Purpose

Resolve the Production-Ready privacy gap identified by RUN 052.

## Git authority

- Baseline: `8366c72463154ef0211a9f4656cf7b7525500eeb`
- Local HEAD before conservation: `8366c72463154ef0211a9f4656cf7b7525500eeb`
- origin/main before conservation: `8366c72463154ef0211a9f4656cf7b7525500eeb`

## Evidence-derived anatomy

Core Experience itself contains only identity, creation time, and lifecycle state.

Its persistence envelope adds only schema_version.

Raw dialogue, Memory, Evidence, Session, provider, and authority are not persisted inside Core Experience.

The actual privacy exposure boundary identified in GitHub is Experience Evidence integration, where inherited EvidenceEngine results enter PCC-01 as an arbitrary mapping.

## Implemented physiology

- dedicated Experience privacy boundary
- explicit sensitive-field classification
- recursive structural redaction
- source mappings are not mutated
- ordinary evidence is conserved
- privacy boundary applied to Experience -> Evidence results

- Experience identity remains unchanged

## Scope boundary

This mechanism performs structural redaction of explicitly sensitive fields.

It does not claim to detect arbitrary secrets embedded in unrestricted prose.

## Governance result

privacy: **IMPLEMENTED + DEMONSTRATED + CONSERVED**

PCC-01: **IMPLEMENTED**

PCC-01 Production-Ready: **NOT YET DECLARED**

Remaining Production-Ready concerns:

- operational observability
- performance
- deployment behavior

PCC-01 canonical status: **NOT CANON**

## Implementation diff

```diff
diff --git a/lib/python/experience/evidence_integration.py b/lib/python/experience/evidence_integration.py
index f3a91b6..2a30869 100644
--- a/lib/python/experience/evidence_integration.py
+++ b/lib/python/experience/evidence_integration.py
@@ -23,6 +23,7 @@ from typing import Any, Mapping
 from lib.python.evidence_engine.engine import EvidenceEngine

 from .identity import ExperienceId
+from .privacy import redact_private_data


 class ExperienceEvidenceIntegrationError(Exception):
@@ -100,9 +101,10 @@ class ExperienceEvidenceIntegrator:
             )

         evidence = self._evidence_engine.find(keyword.strip())
+        privacy_safe_evidence = redact_private_data(evidence)

         return ExperienceEvidenceReference(
             experience_id=experience_id,
             keyword=keyword.strip(),
-            evidence=evidence,
+            evidence=privacy_safe_evidence,
         )
```

## Bash executed — complete

```bash
#!/data/data/com.termux/files/usr/bin/bash
set -uo pipefail

cd "$HOME/storage/shared/AI-Projects/AI-Toolkit" || exit 1

export GIT_PAGER=cat
export GH_PAGER=cat
export PAGER=cat
export PYTHONPATH="$PWD:$PWD/lib${PYTHONPATH:+:$PYTHONPATH}"

BASE="8366c72463154ef0211a9f4656cf7b7525500eeb"

PRIVACY="lib/python/experience/privacy.py"
EVIDENCE="lib/python/experience/evidence_integration.py"
TEST="tests/experience/test_experience_privacy.py"
REPORT="work/implementation-reports/PCC-01/PCC-01_RUN055_PRIVACY_IMPLEMENTATION.md"

SELF="$PREFIX/tmp/pcc01_run055.sh"
OUT="$PREFIX/tmp/pcc01_run055.output"

: > "$OUT"
exec > >(tee -a "$OUT") 2>&1

fail() {
    code="${1:-1}"

    echo
    echo "=========================================================="
    echo "RUN 055 STOPPED SAFELY"
    echo "=========================================================="
    echo "Exit code: $code"
    echo "NO commit/push after failure"
    echo "PCC-01 remains IMPLEMENTED"
    echo "Production-Ready remains NOT DECLARED"
    echo "=========================================================="

    exit "$code"
}

echo "=========================================================="
echo "PCC-01 — RUN 055"
echo "PRIVACY BOUNDARY"
echo "EVIDENCE-DERIVED IMPLEMENTATION"
echo "=========================================================="

echo
echo "[1/9] Verify synchronized Git authority"

git fetch origin main --quiet || fail $?

LOCAL="$(git rev-parse HEAD)"
REMOTE="$(git rev-parse origin/main)"

echo "Expected:    $BASE"
echo "LOCAL:       $LOCAL"
echo "origin/main: $REMOTE"

[ "$LOCAL" = "$BASE" ] || fail 1
[ "$REMOTE" = "$BASE" ] || fail 1

[ -z "$(git diff --name-only)" ] || {
    echo "ERROR: tracked working tree not clean"
    git diff --name-only
    fail 1
}

[ -z "$(git diff --cached --name-only)" ] || {
    echo "ERROR: staging area not clean"
    git diff --cached --name-only
    fail 1
}

echo "PASS: Git authority"

echo
echo "[2/9] Verify exact privacy-relevant anatomy"

python - <<'PY'
from lib.python.experience.model import Experience
from lib.python.experience.persistence import serialize_experience

experience = Experience.create()
representation = serialize_experience(experience)

assert set(representation) == {
    "schema_version",
    "experience_id",
    "created_at",
    "state",
}

for forbidden in (
    "dialogue",
    "memory",
    "evidence",
    "provider",
    "authority",
    "session",
):
    assert forbidden not in representation

print("PASS: Core Experience persistence is minimal")
print("PASS: raw dialogue absent")
print("PASS: Memory absent")
print("PASS: Evidence absent")
print("PASS: Session/provider/authority absent")
PY

[ $? -eq 0 ] || fail $?

grep -Fq \
    'evidence: Mapping[str, Any]' \
    "$EVIDENCE" || {
        echo "ERROR: expected Evidence exposure boundary changed"
        fail 1
    }

echo "PASS: Evidence mapping exposure boundary confirmed"

echo
echo "[3/9] Verify no duplicate Experience privacy organ"

[ ! -e "$PRIVACY" ] || {
    echo "ERROR: Experience privacy organ already exists"
    fail 1
}

[ ! -e "$TEST" ] || {
    echo "ERROR: RUN 055 privacy test already exists"
    fail 1
}

echo "PASS: no duplicate privacy organ"

echo
echo "[4/9] Build Experience privacy organ"

cat > "$PRIVACY" <<'PY'
"""Privacy boundary for PCC-01 Persistent Experience.

Privacy does not redefine Experience, Memory, Evidence, or authority.

The boundary minimizes information leaving Experience integrations and
redacts values associated with explicitly sensitive field names.

Redaction is structural and conservative. It does not claim to discover
arbitrary secrets hidden inside unrestricted prose.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any


REDACTED = "[REDACTED]"

_SENSITIVE_FIELD_NAMES = frozenset(
    {
        "password",
        "passwd",
        "secret",
        "token",
        "access_token",
        "refresh_token",
        "authorization",
        "api_key",
        "apikey",
        "private_key",
        "credential",
        "credentials",
        "email",
        "phone",
        "phone_number",
        "address",
        "date_of_birth",
        "dob",
        "ssn",
        "personal_data",
        "pii",
    }
)


def _normalized_field_name(value: Any) -> str:
    return str(value).strip().lower().replace("-", "_").replace(" ", "_")


def is_sensitive_field_name(value: Any) -> bool:
    """Return whether a mapping key is explicitly privacy-sensitive."""

    return _normalized_field_name(value) in _SENSITIVE_FIELD_NAMES


def redact_private_data(value: Any) -> Any:
    """Return a privacy-safe structural copy of integration data.

    Mapping values under explicitly sensitive field names are replaced
    by REDACTED. Nested mappings and ordinary containers are traversed.

    Input objects are never mutated.
    """

    if isinstance(value, Mapping):
        return {
            key: (
                REDACTED
                if is_sensitive_field_name(key)
                else redact_private_data(item)
            )
            for key, item in value.items()
        }

    if isinstance(value, list):
        return [redact_private_data(item) for item in value]

    if isinstance(value, tuple):
        return tuple(redact_private_data(item) for item in value)

    if isinstance(value, set):
        return {redact_private_data(item) for item in value}

    return value
PY

python -m py_compile "$PRIVACY" || fail $?

echo "PASS: privacy organ syntax"

echo
echo "[5/9] Connect privacy boundary to Evidence integration"

python - "$EVIDENCE" <<'PY'
from pathlib import Path
import sys

path = Path(sys.argv[1])
text = path.read_text(encoding="utf-8")

old_import = '''from .identity import ExperienceId
'''

new_import = '''from .identity import ExperienceId
from .privacy import redact_private_data
'''

if text.count(old_import) != 1:
    raise SystemExit(
        "ERROR: exact Experience identity import boundary changed"
    )

text = text.replace(old_import, new_import, 1)

old_find = '''        evidence = self._evidence_engine.find(keyword.strip())

        return ExperienceEvidenceReference(
            experience_id=experience_id,
            keyword=keyword.strip(),
            evidence=evidence,
        )
'''

new_find = '''        evidence = self._evidence_engine.find(keyword.strip())
        privacy_safe_evidence = redact_private_data(evidence)

        return ExperienceEvidenceReference(
            experience_id=experience_id,
            keyword=keyword.strip(),
            evidence=privacy_safe_evidence,
        )
'''

if text.count(old_find) != 1:
    raise SystemExit(
        "ERROR: exact Evidence integration return boundary changed"
    )

text = text.replace(old_find, new_find, 1)

path.write_text(text, encoding="utf-8")

print("PASS: privacy boundary connected at Experience -> Evidence output")
PY

python -m py_compile "$EVIDENCE" || fail $?

echo
echo "[6/9] Build contract-derived behavioral examination"

cat > "$TEST" <<'PY'
from copy import deepcopy

from lib.python.experience.model import Experience
from lib.python.experience.persistence import serialize_experience
from lib.python.experience.privacy import (
    REDACTED,
    is_sensitive_field_name,
    redact_private_data,
)


def test_core_experience_persistence_remains_data_minimal():
    experience = Experience.create().activate()

    representation = serialize_experience(experience)

    assert set(representation) == {
        "schema_version",
        "experience_id",
        "created_at",
        "state",
    }


def test_sensitive_field_names_are_explicitly_recognized():
    for field in (
        "password",
        "secret",
        "token",
        "access_token",
        "refresh-token",
        "authorization",
        "api key",
        "private_key",
        "credentials",
        "email",
        "phone",
        "phone_number",
        "address",
        "date_of_birth",
        "dob",
        "ssn",
        "personal_data",
        "pii",
    ):
        assert is_sensitive_field_name(field)


def test_non_sensitive_domain_fields_are_not_reclassified():
    for field in (
        "experience_id",
        "created_at",
        "state",
        "schema_version",
        "keyword",
        "semantic",
    ):
        assert not is_sensitive_field_name(field)


def test_top_level_sensitive_values_are_redacted():
    source = {
        "result": "ordinary evidence",
        "token": "secret-token",
        "email": "person@example.invalid",
    }

    result = redact_private_data(source)

    assert result == {
        "result": "ordinary evidence",
        "token": REDACTED,
        "email": REDACTED,
    }


def test_nested_sensitive_values_are_redacted():
    source = {
        "semantic": {
            "result": "ordinary",
            "credentials": {
                "username": "ordinary-name",
                "password": "do-not-expose",
            },
        },
        "items": [
            {
                "phone_number": "000000",
                "fact": "preserve this",
            }
        ],
    }

    result = redact_private_data(source)

    assert result["semantic"]["result"] == "ordinary"
    assert result["semantic"]["credentials"] == REDACTED
    assert result["items"][0]["phone_number"] == REDACTED
    assert result["items"][0]["fact"] == "preserve this"


def test_redaction_does_not_mutate_source_evidence():
    source = {
        "semantic": {
            "api_key": "private",
            "fact": "public",
        }
    }
    original = deepcopy(source)

    redact_private_data(source)

    assert source == original


def test_ordinary_evidence_structure_is_conserved():
    source = {
        "semantic": {
            "fact": "the organism remembers evidence",
        },
        "files": [
            "a.md",
            "b.md",
        ],
        "count": 2,
    }

    assert redact_private_data(source) == source


def test_redaction_handles_nested_containers():
    source = {
        "items": (
            {"secret": "one"},
            {"fact": "two"},
        ),
    }

    result = redact_private_data(source)

    assert result == {
        "items": (
            {"secret": REDACTED},
            {"fact": "two"},
        )
    }


def test_privacy_boundary_does_not_change_experience_identity():
    experience = Experience.create()
    before = experience.experience_id

    redact_private_data(
        {
            "experience_id": str(experience.experience_id),
            "secret": "private",
        }
    )

    assert experience.experience_id == before
PY

python -m py_compile "$TEST" || fail $?

echo "PASS: privacy behavioral examination syntax"

echo
echo "[7/9] Execute privacy, Evidence integration and complete regression"

python -m pytest -q \
    "$TEST" \
    tests/experience/test_experience_evidence_integration.py || fail $?

echo "PASS: privacy + Evidence integration"

python -m pytest -q tests/experience || fail $?

echo "PASS: complete Experience regression"

echo
echo "[8/9] Verify exact mutation boundary and generate epic-thread"

EXPECTED="$PREFIX/tmp/pcc01_run055.expected"
ACTUAL="$PREFIX/tmp/pcc01_run055.actual"

cat > "$EXPECTED" <<EOF
$EVIDENCE
$PRIVACY
$TEST
EOF

{
    git diff --name-only
    git ls-files --others --exclude-standard -- "$PRIVACY" "$TEST"
} | sort -u > "$ACTUAL"

sort -o "$EXPECTED" "$EXPECTED"

if ! diff -u "$EXPECTED" "$ACTUAL"; then
    echo "ERROR: mutation outside RUN 055 boundary"
    fail 1
fi

echo "PASS: exact mutation boundary"

mkdir -p "$(dirname "$REPORT")"

{
    echo "# PCC-01 — RUN 055 — Privacy Boundary Implementation"
    echo
    echo "## Purpose"
    echo
    echo "Resolve the Production-Ready privacy gap identified by RUN 052."
    echo
    echo "## Git authority"
    echo
    echo "- Baseline: \`$BASE\`"
    echo "- Local HEAD before conservation: \`$LOCAL\`"
    echo "- origin/main before conservation: \`$REMOTE\`"
    echo
    echo "## Evidence-derived anatomy"
    echo
    echo "Core Experience itself contains only identity, creation time, and lifecycle state."
    echo
    echo "Its persistence envelope adds only schema_version."
    echo
    echo "Raw dialogue, Memory, Evidence, Session, provider, and authority are not persisted inside Core Experience."
    echo
    echo "The actual privacy exposure boundary identified in GitHub is Experience Evidence integration, where inherited EvidenceEngine results enter PCC-01 as an arbitrary mapping."
    echo
    echo "## Implemented physiology"
    echo
    echo "- dedicated Experience privacy boundary"
    echo "- explicit sensitive-field classification"
    echo "- recursive structural redaction"
    echo "- source mappings are not mutated"
    echo "- ordinary evidence is conserved"
    echo "- privacy boundary applied to Experience -> Evidence results"
    echo
    echo "- Experience identity remains unchanged"
    echo
    echo "## Scope boundary"
    echo
    echo "This mechanism performs structural redaction of explicitly sensitive fields."
    echo
    echo "It does not claim to detect arbitrary secrets embedded in unrestricted prose."
    echo
    echo "## Governance result"
    echo
    echo "privacy: **IMPLEMENTED + DEMONSTRATED + CONSERVED**"
    echo
    echo "PCC-01: **IMPLEMENTED**"
    echo
    echo "PCC-01 Production-Ready: **NOT YET DECLARED**"
    echo
    echo "Remaining Production-Ready concerns:"
    echo
    echo "- operational observability"
    echo "- performance"
    echo "- deployment behavior"
    echo
    echo "PCC-01 canonical status: **NOT CANON**"
    echo
    echo "## Implementation diff"
    echo
    echo '```diff'
    git diff -- "$EVIDENCE" "$PRIVACY" "$TEST"
    echo '```'
    echo
    echo "## Bash executed — complete"
    echo
    echo '```bash'
    cat "$SELF"
    echo '```'
    echo
    echo "## Terminal output — complete"
    echo
    echo '```text'
    cat "$OUT"
    echo '```'
} > "$REPORT"

python - "$REPORT" <<'PY'
from pathlib import Path
import sys

path = Path(sys.argv[1])
text = path.read_text(encoding="utf-8")
clean = "\n".join(line.rstrip(" \t") for line in text.splitlines())

if text.endswith("\n"):
    clean += "\n"

path.write_text(clean, encoding="utf-8")
PY

[ -s "$REPORT" ] || fail 1

echo "PASS: autosufficient epic-thread generated"
sha256sum "$REPORT"

echo
echo "[9/9] Conserve implementation and evidence in GitHub"

git add -- \
    "$EVIDENCE" \
    "$PRIVACY" \
    "$TEST" \
    "$REPORT" || fail $?

EXPECTED_STAGED="$PREFIX/tmp/pcc01_run055.expected_staged"

{
    cat "$EXPECTED"
    echo "$REPORT"
} | sort > "$EXPECTED_STAGED"

git diff --cached --name-only | sort > \
    "$PREFIX/tmp/pcc01_run055.actual_staged"

if ! diff -u \
    "$EXPECTED_STAGED" \
    "$PREFIX/tmp/pcc01_run055.actual_staged"
then
    echo "ERROR: staging boundary violated"
    git reset --quiet
    fail 1
fi

git diff --cached --check || {
    echo "ERROR: staged integrity failure"
    git reset --quiet
    fail 1
}

git commit -m \
    "feat: add PCC-01 privacy boundary" || fail $?

FINAL_HEAD="$(git rev-parse HEAD)"

git push origin main || fail $?
git fetch origin main --quiet || fail $?

FINAL_REMOTE="$(git rev-parse origin/main)"

[ "$FINAL_HEAD" = "$FINAL_REMOTE" ] || fail 1

echo
echo "=========================================================="
echo "RUN 055 COMPLETE"
echo "=========================================================="
echo
echo "FINAL HEAD:"
echo "$FINAL_HEAD"
echo
echo "LOCAL == origin/main:"
echo "PASS"
echo
echo "PRIVACY:"
echo "IMPLEMENTED + DEMONSTRATED + CONSERVED"
echo
echo "REMAINING PRODUCTION CONCERNS:"
echo "3"
echo
echo "operational observability"
echo "performance"
echo "deployment behavior"
echo
echo "PCC-01:"
echo "IMPLEMENTED"
echo
echo "PCC-01 PRODUCTION-READY:"
echo "NOT YET DECLARED"
echo
echo "PCC-01 CANONICAL STATUS:"
echo "NOT CANON"
echo
echo "EPIC-THREAD MD:"
echo "$REPORT"
echo
echo "NEXT:"
echo "GPT verifies RUN 055 directly in GitHub before deriving RUN 056."
echo "=========================================================="
```

## Terminal output — complete

```text
==========================================================
PCC-01 — RUN 055
PRIVACY BOUNDARY
EVIDENCE-DERIVED IMPLEMENTATION
==========================================================

[1/9] Verify synchronized Git authority
Expected:    8366c72463154ef0211a9f4656cf7b7525500eeb
LOCAL:       8366c72463154ef0211a9f4656cf7b7525500eeb
origin/main: 8366c72463154ef0211a9f4656cf7b7525500eeb
PASS: Git authority

[2/9] Verify exact privacy-relevant anatomy
PASS: Core Experience persistence is minimal
PASS: raw dialogue absent
PASS: Memory absent
PASS: Evidence absent
PASS: Session/provider/authority absent
PASS: Evidence mapping exposure boundary confirmed

[3/9] Verify no duplicate Experience privacy organ
PASS: no duplicate privacy organ

[4/9] Build Experience privacy organ
PASS: privacy organ syntax

[5/9] Connect privacy boundary to Evidence integration
PASS: privacy boundary connected at Experience -> Evidence output

[6/9] Build contract-derived behavioral examination
PASS: privacy behavioral examination syntax

[7/9] Execute privacy, Evidence integration and complete regression
..................                                                       [100%]
18 passed in 0.57s
PASS: privacy + Evidence integration
........................................................................ [ 33%]
........................................................................ [ 66%]
........................................................................ [ 99%]
..                                                                       [100%]
218 passed in 3.65s
PASS: complete Experience regression

[8/9] Verify exact mutation boundary and generate epic-thread
PASS: exact mutation boundary
```

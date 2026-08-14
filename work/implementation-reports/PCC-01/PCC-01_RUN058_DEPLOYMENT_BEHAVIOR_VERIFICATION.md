# PCC-01 — RUN 058 — Deployment Behavior Verification

## Purpose

Resolve the final Production-Ready concern identified by RUN 052: deployment behavior.

## Git authority

- Baseline: `11bde8de1dec8f92857d7185c73d7275be03be10`
- Local HEAD: `11bde8de1dec8f92857d7185c73d7275be03be10`
- origin/main: `11bde8de1dec8f92857d7185c73d7275be03be10`

## Actual deployment anatomy

- Railway start command: `bash bin/runtime-server`
- Railway health path: `/health`
- Railway restart policy: `ON_FAILURE`
- runtime HTTP host: `0.0.0.0`
- runtime port: Railway `PORT` with runtime fallback
- runtime state boundary: `.ai/runtime/state`

## PCC-01 deployment physiology

RUN 058 adds an explicit deployment boundary for the Experience persistence path.

Default store:

`.ai/runtime/state/experience.json`

Override:

`PCC01_EXPERIENCE_STORE`

An absolute override allows deployment infrastructure to bind PCC-01 to externally durable mounted storage without changing Experience identity or persistence semantics.

## Behavioral evidence

- default runtime-state binding
- external durable-path binding
- relative repository-root binding
- parent preparation
- repository reconstruction
- Experience identity survival
- active-state survival
- idempotent deployment preparation
- invalid configuration rejection

## Governance

deployment behavior: **IMPLEMENTED + DEMONSTRATED + CONSERVED**

Remaining Production-Ready concerns after RUN 058: **0 candidate concerns**

This does NOT itself declare PCC-01 Production-Ready.

A closure reaudit and human Production-Ready gate remain required.

PCC-01 canonical status remains **NOT CANON**.

## Implementation diff

```diff
```

## Complete Bash executed

```bash
#!/data/data/com.termux/files/usr/bin/bash
set -uo pipefail

cd "$HOME/storage/shared/AI-Projects/AI-Toolkit" || exit 1

export PYTHONPATH="$PWD:$PWD/lib${PYTHONPATH:+:$PYTHONPATH}"
export GIT_PAGER=cat
export GH_PAGER=cat
export PAGER=cat

BASE="11bde8de1dec8f92857d7185c73d7275be03be10"

DEPLOY="lib/python/experience/deployment.py"
TEST="tests/experience/test_experience_deployment_behavior.py"
REPORT="work/implementation-reports/PCC-01/PCC-01_RUN058_DEPLOYMENT_BEHAVIOR_VERIFICATION.md"

SELF="$PREFIX/tmp/pcc01_run058.sh"
OUT="$PREFIX/tmp/pcc01_run058.output"

: > "$OUT"
exec > >(tee -a "$OUT") 2>&1

fail() {
    code="${1:-1}"

    echo
    echo "=========================================================="
    echo "RUN 058 STOPPED SAFELY"
    echo "=========================================================="
    echo "Exit code: $code"
    echo "NO commit/push after failure"
    echo "PCC-01 remains IMPLEMENTED"
    echo "Production-Ready remains NOT DECLARED"
    echo "=========================================================="

    exit "$code"
}

echo "=========================================================="
echo "PCC-01 — RUN 058"
echo "DEPLOYMENT BEHAVIOR"
echo "GIT-EVIDENCE-DERIVED VERIFICATION"
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
echo "[2/9] Verify actual deployment anatomy"

python - <<'PY'
import json
from pathlib import Path

railway = json.loads(Path("railway.json").read_text())
runtime_server = Path("bin/runtime-server").read_text()
config = Path("lib/python/runtime/config.py").read_text()
http_server = Path(
    "lib/python/runtime/interfaces/http_server.py"
).read_text()

assert railway["deploy"]["startCommand"] == "bash bin/runtime-server"
assert railway["deploy"]["healthcheckPath"] == "/health"
assert railway["deploy"]["restartPolicyType"] == "ON_FAILURE"

assert "python3 -m python.runtime.process" in runtime_server
assert 'AI_TOOLKIT_REPOSITORY_ROOT' in runtime_server
assert ".ai/runtime/state" in runtime_server

assert 'os.environ.get("PORT"' in config
assert 'http_host: str = "0.0.0.0"' in config

assert '"/health"' in http_server
assert '"/ready"' in http_server

print("PASS: Railway start command")
print("PASS: Railway health boundary")
print("PASS: Railway restart-on-failure policy")
print("PASS: runtime-server entry point")
print("PASS: Railway PORT consumption")
print("PASS: 0.0.0.0 deployment binding")
print("PASS: runtime state directory preparation")
print("PASS: health/readiness HTTP anatomy")
PY

[ $? -eq 0 ] || fail $?

echo
echo "[3/9] Verify exact PCC-01 persistence deployment substrate"

python - <<'PY'
import inspect

from lib.python.experience.persistent_repository import (
    JsonFileExperienceRepository,
)

signature = inspect.signature(JsonFileExperienceRepository)

print("JsonFileExperienceRepository:", signature)

repository = JsonFileExperienceRepository

assert hasattr(repository, "add")
assert hasattr(repository, "get")
assert hasattr(repository, "save")
assert hasattr(repository, "contains")

print("PASS: deployable persistent Experience repository")
print("PASS: persistence path is externally selectable")
print("PASS: repository can be reconstructed after process restart")
PY

[ $? -eq 0 ] || fail $?

echo
echo "[4/9] Verify no duplicate deployment organ"

[ ! -e "$DEPLOY" ] || {
    echo "ERROR: PCC-01 deployment organ already exists"
    fail 1
}

[ ! -e "$TEST" ] || {
    echo "ERROR: PCC-01 deployment test already exists"
    fail 1
}

echo "PASS: no duplicate deployment organ"

echo
echo "[5/9] Build deployment boundary organ"

cat > "$DEPLOY" <<'PY'
"""Deployment boundary for PCC-01 Persistent Experience.

This organ translates deployment configuration into a durable Experience
repository location.

Deployment != Experience.
Deployment != Memory.
Deployment != authority.

The persistent location is explicit so a production runtime may bind PCC-01
to durable storage supplied by its deployment environment.
"""

from __future__ import annotations

import os
from pathlib import Path

from .persistent_repository import JsonFileExperienceRepository


DEFAULT_EXPERIENCE_STORE = ".ai/runtime/state/experience.json"
EXPERIENCE_STORE_ENV = "PCC01_EXPERIENCE_STORE"


class ExperienceDeploymentConfigurationError(RuntimeError):
    """Raised when PCC-01 deployment storage cannot be prepared."""


def experience_store_path(
    *,
    environment: dict[str, str] | None = None,
    repository_root: str | Path | None = None,
) -> Path:
    """Resolve the durable Experience store for this deployment.

    PCC01_EXPERIENCE_STORE may be absolute or relative.

    Relative paths are anchored to AI_TOOLKIT_REPOSITORY_ROOT when supplied,
    matching the existing runtime deployment boundary.
    """

    env = os.environ if environment is None else environment

    configured = env.get(
        EXPERIENCE_STORE_ENV,
        DEFAULT_EXPERIENCE_STORE,
    ).strip()

    if not configured:
        raise ExperienceDeploymentConfigurationError(
            "PCC-01 Experience store path cannot be empty"
        )

    path = Path(configured).expanduser()

    if path.is_absolute():
        return path

    if repository_root is None:
        root_value = env.get(
            "AI_TOOLKIT_REPOSITORY_ROOT",
            os.getcwd(),
        )
        root = Path(root_value)
    else:
        root = Path(repository_root)

    return root / path


def prepare_experience_repository(
    *,
    environment: dict[str, str] | None = None,
    repository_root: str | Path | None = None,
) -> JsonFileExperienceRepository:
    """Prepare the persistent Experience repository for deployment."""

    path = experience_store_path(
        environment=environment,
        repository_root=repository_root,
    )

    try:
        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )
    except OSError as exc:
        raise ExperienceDeploymentConfigurationError(
            f"cannot prepare PCC-01 persistence directory: {path.parent}"
        ) from exc

    if path.exists() and path.is_dir():
        raise ExperienceDeploymentConfigurationError(
            f"PCC-01 Experience store must be a file path: {path}"
        )

    return JsonFileExperienceRepository(path)
PY

python -m py_compile "$DEPLOY" || fail $?

echo "PASS: deployment boundary syntax"

echo
echo "[6/9] Build deployment behavioral examination"

cat > "$TEST" <<'PY'
from lib.python.experience.deployment import (
    DEFAULT_EXPERIENCE_STORE,
    EXPERIENCE_STORE_ENV,
    ExperienceDeploymentConfigurationError,
    experience_store_path,
    prepare_experience_repository,
)
from lib.python.experience.model import Experience
from lib.python.experience.persistent_repository import (
    JsonFileExperienceRepository,
)


def test_default_deployment_store_uses_runtime_state_boundary(tmp_path):
    path = experience_store_path(
        environment={},
        repository_root=tmp_path,
    )

    assert path == tmp_path / DEFAULT_EXPERIENCE_STORE
    assert path == tmp_path / ".ai/runtime/state/experience.json"


def test_deployment_store_can_be_bound_to_external_durable_location(
    tmp_path,
):
    durable = tmp_path / "mounted-volume" / "pcc01.json"

    path = experience_store_path(
        environment={
            EXPERIENCE_STORE_ENV: str(durable),
        },
        repository_root=tmp_path / "repository",
    )

    assert path == durable


def test_relative_deployment_store_uses_repository_root_environment(
    tmp_path,
):
    root = tmp_path / "repository"

    path = experience_store_path(
        environment={
            "AI_TOOLKIT_REPOSITORY_ROOT": str(root),
            EXPERIENCE_STORE_ENV: "durable/experience.json",
        }
    )

    assert path == root / "durable/experience.json"


def test_prepare_creates_required_parent_anatomy(tmp_path):
    root = tmp_path / "repository"

    repository = prepare_experience_repository(
        environment={},
        repository_root=root,
    )

    assert isinstance(
        repository,
        JsonFileExperienceRepository,
    )
    assert (root / ".ai/runtime/state").is_dir()


def test_experience_survives_repository_reconstruction(tmp_path):
    durable = tmp_path / "volume" / "experience.json"

    environment = {
        EXPERIENCE_STORE_ENV: str(durable),
    }

    first_process = prepare_experience_repository(
        environment=environment,
    )

    experience = Experience.create()
    first_process.add(experience)

    original_identity = experience.experience_id

    del first_process

    second_process = prepare_experience_repository(
        environment=environment,
    )

    recovered = second_process.get(original_identity)

    assert recovered.experience_id == original_identity
    assert second_process.contains(original_identity)


def test_active_state_survives_repository_reconstruction(tmp_path):
    durable = tmp_path / "volume" / "experience.json"
    environment = {
        EXPERIENCE_STORE_ENV: str(durable),
    }

    process_a = prepare_experience_repository(
        environment=environment,
    )

    experience = Experience.create().activate()
    process_a.add(experience)

    identity = experience.experience_id

    del process_a

    process_b = prepare_experience_repository(
        environment=environment,
    )

    recovered = process_b.get(identity)

    assert recovered.experience_id == identity
    assert recovered.state.value == "ACTIVE"


def test_repeated_deployment_preparation_is_idempotent(tmp_path):
    environment = {
        EXPERIENCE_STORE_ENV: str(
            tmp_path / "volume" / "experience.json"
        )
    }

    first = prepare_experience_repository(
        environment=environment,
    )
    second = prepare_experience_repository(
        environment=environment,
    )

    assert isinstance(first, JsonFileExperienceRepository)
    assert isinstance(second, JsonFileExperienceRepository)


def test_empty_store_configuration_is_rejected(tmp_path):
    try:
        experience_store_path(
            environment={
                EXPERIENCE_STORE_ENV: "   ",
            },
            repository_root=tmp_path,
        )
    except ExperienceDeploymentConfigurationError:
        pass
    else:
        raise AssertionError(
            "empty deployment store configuration accepted"
        )


def test_directory_cannot_be_used_as_experience_store(tmp_path):
    store = tmp_path / "volume"
    store.mkdir()

    try:
        prepare_experience_repository(
            environment={
                EXPERIENCE_STORE_ENV: str(store),
            }
        )
    except ExperienceDeploymentConfigurationError:
        pass
    else:
        raise AssertionError(
            "directory accepted as Experience persistence file"
        )


def test_deployment_configuration_does_not_redefine_experience(tmp_path):
    environment = {
        EXPERIENCE_STORE_ENV: str(
            tmp_path / "volume-a" / "experience.json"
        )
    }

    repository = prepare_experience_repository(
        environment=environment,
    )

    experience = Experience.create()
    identity = experience.experience_id

    repository.add(experience)

    assert repository.get(identity).experience_id == identity
    assert experience.experience_id == identity
PY

python -m py_compile "$TEST" || fail $?

echo "PASS: deployment behavioral examination syntax"

echo
echo "[7/9] Execute deployment + restart + complete regression"

python -m pytest -q \
    "$TEST" \
    tests/experience/test_experience_real_process_restart.py \
    tests/experience/test_experience_persistence.py \
    tests/experience/test_experience_persistence_migration.py || fail $?

echo "PASS: deployment/restart persistence behavior"

python -m pytest -q tests/experience || fail $?

echo "PASS: complete Experience regression"

echo
echo "[8/9] Verify exact mutation boundary and generate epic-thread"

EXPECTED="$PREFIX/tmp/pcc01_run058.expected"
ACTUAL="$PREFIX/tmp/pcc01_run058.actual"

cat > "$EXPECTED" <<EOF
$DEPLOY
$TEST
EOF

{
    git diff --name-only
    git ls-files --others --exclude-standard -- "$DEPLOY" "$TEST"
} | sort -u > "$ACTUAL"

sort -o "$EXPECTED" "$EXPECTED"

if ! diff -u "$EXPECTED" "$ACTUAL"; then
    echo "ERROR: RUN 058 mutation boundary violated"
    fail 1
fi

echo "PASS: exact mutation boundary"

mkdir -p "$(dirname "$REPORT")"

{
    echo "# PCC-01 — RUN 058 — Deployment Behavior Verification"
    echo
    echo "## Purpose"
    echo
    echo "Resolve the final Production-Ready concern identified by RUN 052: deployment behavior."
    echo
    echo "## Git authority"
    echo
    echo "- Baseline: \`$BASE\`"
    echo "- Local HEAD: \`$LOCAL\`"
    echo "- origin/main: \`$REMOTE\`"
    echo
    echo "## Actual deployment anatomy"
    echo
    echo "- Railway start command: \`bash bin/runtime-server\`"
    echo "- Railway health path: \`/health\`"
    echo "- Railway restart policy: \`ON_FAILURE\`"
    echo "- runtime HTTP host: \`0.0.0.0\`"
    echo "- runtime port: Railway \`PORT\` with runtime fallback"
    echo "- runtime state boundary: \`.ai/runtime/state\`"
    echo
    echo "## PCC-01 deployment physiology"
    echo
    echo "RUN 058 adds an explicit deployment boundary for the Experience persistence path."
    echo
    echo "Default store:"
    echo
    echo "\`.ai/runtime/state/experience.json\`"
    echo
    echo "Override:"
    echo
    echo "\`PCC01_EXPERIENCE_STORE\`"
    echo
    echo "An absolute override allows deployment infrastructure to bind PCC-01 to externally durable mounted storage without changing Experience identity or persistence semantics."
    echo
    echo "## Behavioral evidence"
    echo
    echo "- default runtime-state binding"
    echo "- external durable-path binding"
    echo "- relative repository-root binding"
    echo "- parent preparation"
    echo "- repository reconstruction"
    echo "- Experience identity survival"
    echo "- active-state survival"
    echo "- idempotent deployment preparation"
    echo "- invalid configuration rejection"
    echo
    echo "## Governance"
    echo
    echo "deployment behavior: **IMPLEMENTED + DEMONSTRATED + CONSERVED**"
    echo
    echo "Remaining Production-Ready concerns after RUN 058: **0 candidate concerns**"
    echo
    echo "This does NOT itself declare PCC-01 Production-Ready."
    echo
    echo "A closure reaudit and human Production-Ready gate remain required."
    echo
    echo "PCC-01 canonical status remains **NOT CANON**."
    echo
    echo "## Implementation diff"
    echo
    echo '```diff'
    git diff -- "$DEPLOY" "$TEST"
    echo '```'
    echo
    echo "## Complete Bash executed"
    echo
    echo '```bash'
    cat "$SELF"
    echo '```'
    echo
    echo "## Complete terminal output"
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

clean = "\n".join(
    line.rstrip(" \t")
    for line in text.splitlines()
) + "\n"

path.write_text(clean, encoding="utf-8")
PY

[ -s "$REPORT" ] || fail 1

echo "PASS: autosufficient epic-thread generated"
sha256sum "$REPORT"

echo
echo "[9/9] Conserve RUN 058 in GitHub"

git add -- "$DEPLOY" "$TEST" "$REPORT" || fail $?

EXPECTED_STAGED="$PREFIX/tmp/pcc01_run058.expected_staged"
ACTUAL_STAGED="$PREFIX/tmp/pcc01_run058.actual_staged"

{
    echo "$DEPLOY"
    echo "$TEST"
    echo "$REPORT"
} | sort > "$EXPECTED_STAGED"

git diff --cached --name-only | sort > "$ACTUAL_STAGED"

if ! diff -u "$EXPECTED_STAGED" "$ACTUAL_STAGED"; then
    echo "ERROR: staged mutation boundary violated"
    git reset --quiet
    fail 1
fi

git diff --cached --check || {
    echo "ERROR: staged integrity failure"
    git reset --quiet
    fail 1
}

git commit -m \
    "feat: add PCC-01 deployment persistence boundary" || fail $?

FINAL_HEAD="$(git rev-parse HEAD)"

git push origin main || fail $?
git fetch origin main --quiet || fail $?

FINAL_REMOTE="$(git rev-parse origin/main)"

[ "$FINAL_HEAD" = "$FINAL_REMOTE" ] || fail 1

echo
echo "=========================================================="
echo "RUN 058 COMPLETE"
echo "=========================================================="
echo
echo "FINAL HEAD:"
echo "$FINAL_HEAD"
echo
echo "LOCAL == origin/main:"
echo "PASS"
echo
echo "DEPLOYMENT BEHAVIOR:"
echo "IMPLEMENTED + DEMONSTRATED + CONSERVED"
echo
echo "REMAINING PRODUCTION CONCERNS:"
echo "0 CANDIDATE CONCERNS"
echo
echo "PCC-01:"
echo "IMPLEMENTED"
echo
echo "PCC-01 PRODUCTION-READY:"
echo "NOT YET DECLARED — CLOSURE REAUDIT REQUIRED"
echo
echo "PCC-01 CANONICAL STATUS:"
echo "NOT CANON"
echo
echo "EPIC-THREAD MD:"
echo "$REPORT"
echo
echo "NEXT:"
echo "GPT verifies RUN 058 directly in GitHub."
echo "Then perform Production-Ready closure reaudit before any human gate."
echo "=========================================================="
```

## Complete terminal output

```text
==========================================================
PCC-01 — RUN 058
DEPLOYMENT BEHAVIOR
GIT-EVIDENCE-DERIVED VERIFICATION
==========================================================

[1/9] Verify synchronized Git authority
Expected:    11bde8de1dec8f92857d7185c73d7275be03be10
LOCAL:       11bde8de1dec8f92857d7185c73d7275be03be10
origin/main: 11bde8de1dec8f92857d7185c73d7275be03be10
PASS: Git authority

[2/9] Verify actual deployment anatomy
PASS: Railway start command
PASS: Railway health boundary
PASS: Railway restart-on-failure policy
PASS: runtime-server entry point
PASS: Railway PORT consumption
PASS: 0.0.0.0 deployment binding
PASS: runtime state directory preparation
PASS: health/readiness HTTP anatomy

[3/9] Verify exact PCC-01 persistence deployment substrate
JsonFileExperienceRepository: (path: 'str | Path') -> 'None'
PASS: deployable persistent Experience repository
PASS: persistence path is externally selectable
PASS: repository can be reconstructed after process restart

[4/9] Verify no duplicate deployment organ
PASS: no duplicate deployment organ

[5/9] Build deployment boundary organ
PASS: deployment boundary syntax

[6/9] Build deployment behavioral examination
PASS: deployment behavioral examination syntax

[7/9] Execute deployment + restart + complete regression
........................................                                 [100%]
40 passed in 1.48s
PASS: deployment/restart persistence behavior
........................................................................ [ 29%]
........................................................................ [ 58%]
........................................................................ [ 88%]
.............................                                            [100%]
245 passed in 4.71s
PASS: complete Experience regression

[8/9] Verify exact mutation boundary and generate epic-thread
PASS: exact mutation boundary
```

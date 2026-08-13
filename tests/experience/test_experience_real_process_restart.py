from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

WRITER = (
    PROJECT_ROOT
    / "tests"
    / "experience"
    / "harness"
    / "pcc01_restart_writer.py"
)

READER = (
    PROJECT_ROOT
    / "tests"
    / "experience"
    / "harness"
    / "pcc01_restart_reader.py"
)


def subprocess_environment() -> dict[str, str]:
    env = os.environ.copy()

    roots = [
        str(PROJECT_ROOT),
        str(PROJECT_ROOT / "lib"),
    ]

    existing = env.get("PYTHONPATH")

    if existing:
        roots.append(existing)

    env["PYTHONPATH"] = os.pathsep.join(roots)

    return env


def test_identity_survives_real_process_death_and_new_process_recovery(
    tmp_path,
):
    store = tmp_path / "experience-store.json"
    before_evidence = tmp_path / "before.json"
    after_evidence = tmp_path / "after.json"

    env = subprocess_environment()

    # Process A is created as an independent Python interpreter.
    process_a = subprocess.run(
        [
            sys.executable,
            str(WRITER),
            str(store),
            str(before_evidence),
        ],
        cwd=PROJECT_ROOT,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    assert process_a.returncode == 0, process_a.stderr

    # subprocess.run() returning proves Process A has terminated.
    assert before_evidence.is_file()

    before = json.loads(
        before_evidence.read_text(encoding="utf-8")
    )

    assert before["role"] == "process_a_writer"
    assert isinstance(before["pid"], int)
    assert before["pid"] > 0

    # Only after Process A has terminated do we launch Process B.
    process_b = subprocess.run(
        [
            sys.executable,
            str(READER),
            str(store),
            str(before_evidence),
            str(after_evidence),
        ],
        cwd=PROJECT_ROOT,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    assert process_b.returncode == 0, process_b.stderr
    assert after_evidence.is_file()

    after = json.loads(
        after_evidence.read_text(encoding="utf-8")
    )

    assert after["role"] == "process_b_reader"

    # Distinct OS process evidence.
    assert after["pid"] != before["pid"]
    assert after["process_a_pid"] == before["pid"]

    # Central PCC-01 identity invariant.
    assert (
        after["experience_id_before"]
        == after["experience_id_after"]
    )

    assert after["identity_equal"] is True

    # The Experience lifecycle state also survived persistence.
    assert after["state_after"] == before["state"]

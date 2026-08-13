from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

WRITER = (
    ROOT
    / "tests"
    / "experience"
    / "harness"
    / "pcc01_protection_restart_writer.py"
)

READER = (
    ROOT
    / "tests"
    / "experience"
    / "harness"
    / "pcc01_protection_restart_reader.py"
)


def run_process(script: Path, *args: Path):
    env = os.environ.copy()

    env["PYTHONPATH"] = (
        f"{ROOT}:{ROOT / 'lib'}"
        + (
            f":{env['PYTHONPATH']}"
            if env.get("PYTHONPATH")
            else ""
        )
    )

    return subprocess.run(
        [
            sys.executable,
            str(script),
            *(str(arg) for arg in args),
        ],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )


def test_protection_survives_real_process_restart(tmp_path):
    experience_store = tmp_path / "experience.json"
    protection_store = tmp_path / "protection.json"

    before_file = tmp_path / "process_a.json"
    after_file = tmp_path / "process_b.json"

    process_a = run_process(
        WRITER,
        experience_store,
        protection_store,
        before_file,
    )

    assert process_a.returncode == 0, (
        "Process A failed.\n"
        f"STDOUT:\n{process_a.stdout}\n"
        f"STDERR:\n{process_a.stderr}"
    )

    before = json.loads(
        before_file.read_text(encoding="utf-8")
    )

    assert before["protection_state"] == "protected"
    assert before["protection_is_protected"] is True

    # subprocess.run() has returned.
    # Process A is therefore terminated before Process B starts.

    process_b = run_process(
        READER,
        experience_store,
        protection_store,
        before_file,
        after_file,
    )

    assert process_b.returncode == 0, (
        "Process B failed.\n"
        f"STDOUT:\n{process_b.stdout}\n"
        f"STDERR:\n{process_b.stderr}"
    )

    after = json.loads(
        after_file.read_text(encoding="utf-8")
    )

    # Real process boundary.
    assert before["pid"] != after["pid"]

    # Central PCC-01 identity invariant.
    assert (
        before["experience_id"]
        == after["experience_id"]
    )

    # Protection remains attached to that same identity.
    assert (
        before["protection_experience_id"]
        == before["experience_id"]
    )

    assert (
        after["protection_experience_id"]
        == after["experience_id"]
    )

    assert (
        before["protection_experience_id"]
        == after["protection_experience_id"]
    )

    # Protection physiology survives process death.
    assert before["protection_state"] == "protected"
    assert after["protection_state"] == "protected"

    assert before["protection_is_protected"] is True
    assert after["protection_is_protected"] is True

    # Persistence does not become authority.
    assert (
        after["unauthorized_operation_rejected"]
        is True
    )

    assert (
        after["explicit_authorization_accepted"]
        is True
    )

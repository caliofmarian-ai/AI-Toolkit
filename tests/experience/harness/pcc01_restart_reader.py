"""Process B for the PCC-01 real restart proof.

This program starts in a separate Python interpreter after Process A
has exited. It reads Process A evidence, reconstructs the persisted
ExperienceId, recovers the Experience from storage, and records the
post-restart identity.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

from lib.python.experience.identity import ExperienceId
from lib.python.experience.persistent_repository import (
    JsonFileExperienceRepository,
)


def main() -> int:
    if len(sys.argv) != 4:
        raise SystemExit(
            "usage: pcc01_restart_reader.py "
            "STORE_PATH BEFORE_EVIDENCE_PATH AFTER_EVIDENCE_PATH"
        )

    store_path = Path(sys.argv[1])
    before_path = Path(sys.argv[2])
    after_path = Path(sys.argv[3])

    before = json.loads(
        before_path.read_text(encoding="utf-8")
    )

    before_id = ExperienceId.from_string(
        before["experience_id"]
    )

    repository = JsonFileExperienceRepository(store_path)
    recovered = repository.get(before_id)

    evidence = {
        "role": "process_b_reader",
        "pid": os.getpid(),
        "process_a_pid": before["pid"],
        "experience_id_before": before["experience_id"],
        "experience_id_after": str(recovered.experience_id),
        "identity_equal": (
            before["experience_id"]
            == str(recovered.experience_id)
        ),
        "state_after": recovered.state.value,
        "store_path": str(store_path),
    }

    after_path.write_text(
        json.dumps(
            evidence,
            sort_keys=True,
            indent=2,
        ) + "\n",
        encoding="utf-8",
    )

    print(json.dumps(evidence, sort_keys=True))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

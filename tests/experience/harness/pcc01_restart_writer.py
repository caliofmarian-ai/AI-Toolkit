"""Process A for the PCC-01 real restart proof.

This program creates one Experience, persists it, records its identity
and PID, and then exits normally.

A later independent Python interpreter must recover that Experience.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

from lib.python.experience.model import Experience
from lib.python.experience.persistent_repository import (
    JsonFileExperienceRepository,
)


def main() -> int:
    if len(sys.argv) != 3:
        raise SystemExit(
            "usage: pcc01_restart_writer.py STORE_PATH EVIDENCE_PATH"
        )

    store_path = Path(sys.argv[1])
    evidence_path = Path(sys.argv[2])

    repository = JsonFileExperienceRepository(store_path)

    experience = Experience.create().activate()
    repository.add(experience)

    evidence = {
        "role": "process_a_writer",
        "pid": os.getpid(),
        "experience_id": str(experience.experience_id),
        "state": experience.state.value,
        "store_path": str(store_path),
    }

    evidence_path.write_text(
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

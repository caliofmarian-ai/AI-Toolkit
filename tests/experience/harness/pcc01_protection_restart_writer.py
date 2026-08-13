from __future__ import annotations

import json
import os
import sys
from pathlib import Path

from lib.python.experience.model import Experience
from lib.python.experience.persistent_repository import (
    JsonFileExperienceRepository,
)
from lib.python.experience.protection import (
    ExperienceProtection,
    ProtectionState,
)
from lib.python.experience.protection_repository import (
    JsonFileProtectionRepository,
)


def main() -> None:
    if len(sys.argv) != 4:
        raise SystemExit(
            "usage: writer.py "
            "<experience_store> "
            "<protection_store> "
            "<evidence_file>"
        )

    experience_store = Path(sys.argv[1])
    protection_store = Path(sys.argv[2])
    evidence_file = Path(sys.argv[3])

    experience = Experience.create()

    protection = ExperienceProtection.protected(
        experience.experience_id
    )

    if protection.state is not ProtectionState.PROTECTED:
        raise RuntimeError(
            "Process A failed to establish PROTECTED state"
        )

    experience_repository = JsonFileExperienceRepository(
        experience_store
    )

    protection_repository = JsonFileProtectionRepository(
        protection_store
    )

    # Protection is persisted first.
    #
    # This does NOT yet claim atomic coordination between the two
    # repositories. It prevents this experiment from acknowledging
    # durable Experience before Protection has itself been written.
    protection_repository.add(protection)

    experience_repository.add(experience)

    recovered_protection = protection_repository.get(
        experience.experience_id
    )

    recovered_experience = experience_repository.get(
        experience.experience_id
    )

    if (
        recovered_experience.experience_id
        != experience.experience_id
    ):
        raise RuntimeError(
            "Process A Experience verification failed"
        )

    if (
        recovered_protection.experience_id
        != experience.experience_id
    ):
        raise RuntimeError(
            "Process A Protection identity verification failed"
        )

    if recovered_protection.state is not ProtectionState.PROTECTED:
        raise RuntimeError(
            "Process A Protection state verification failed"
        )

    evidence = {
        "pid": os.getpid(),
        "experience_id": str(experience.experience_id),
        "experience_state": experience.state.value,
        "protection_experience_id": str(
            protection.experience_id
        ),
        "protection_state": protection.state.value,
        "protection_is_protected": protection.is_protected,
    }

    evidence_file.write_text(
        json.dumps(
            evidence,
            indent=2,
            sort_keys=True,
        ) + "\n",
        encoding="utf-8",
    )

    print(json.dumps(evidence, sort_keys=True))


if __name__ == "__main__":
    main()

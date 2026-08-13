from __future__ import annotations

import json
import os
import sys
from pathlib import Path

from lib.python.experience.identity import ExperienceId
from lib.python.experience.persistent_repository import (
    JsonFileExperienceRepository,
)
from lib.python.experience.protection import ProtectionState
from lib.python.experience.protection_repository import (
    JsonFileProtectionRepository,
)


def main() -> None:
    if len(sys.argv) != 5:
        raise SystemExit(
            "usage: reader.py "
            "<experience_store> "
            "<protection_store> "
            "<before_evidence> "
            "<after_evidence>"
        )

    experience_store = Path(sys.argv[1])
    protection_store = Path(sys.argv[2])
    before_file = Path(sys.argv[3])
    after_file = Path(sys.argv[4])

    before = json.loads(
        before_file.read_text(encoding="utf-8")
    )

    experience_id = ExperienceId.from_string(
        before["experience_id"]
    )

    experience_repository = JsonFileExperienceRepository(
        experience_store
    )

    protection_repository = JsonFileProtectionRepository(
        protection_store
    )

    recovered_experience = experience_repository.get(
        experience_id
    )

    recovered_protection = protection_repository.get(
        experience_id
    )

    if recovered_experience.experience_id != experience_id:
        raise RuntimeError(
            "Process B recovered wrong Experience identity"
        )

    if recovered_protection.experience_id != experience_id:
        raise RuntimeError(
            "Process B recovered wrong Protection identity"
        )

    if recovered_protection.state is not ProtectionState.PROTECTED:
        raise RuntimeError(
            "Process B did not recover PROTECTED state"
        )

    # Persisted PROTECTED state must not become authority.
    authorization_rejected = False

    try:
        recovered_protection.require_authorized(
            authorized=False
        )
    except Exception:
        authorization_rejected = True

    if not authorization_rejected:
        raise RuntimeError(
            "persisted PROTECTED state incorrectly granted authority"
        )

    # Explicit authorization remains separately required.
    recovered_protection.require_authorized(
        authorized=True
    )

    evidence = {
        "pid": os.getpid(),
        "experience_id": str(
            recovered_experience.experience_id
        ),
        "experience_state": recovered_experience.state.value,
        "protection_experience_id": str(
            recovered_protection.experience_id
        ),
        "protection_state": recovered_protection.state.value,
        "protection_is_protected": (
            recovered_protection.is_protected
        ),
        "unauthorized_operation_rejected": (
            authorization_rejected
        ),
        "explicit_authorization_accepted": True,
    }

    after_file.write_text(
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

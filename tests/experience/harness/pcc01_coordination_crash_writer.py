from pathlib import Path
import json
import os
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "lib" / "python"))

from experience.model import Experience
from experience.protection import ExperienceProtection
from experience.persistent_repository import JsonFileExperienceRepository
from experience.protection_repository import JsonFileProtectionRepository
from experience.coordination_journal import JsonFileCoordinationJournal
from experience.persistence_coordinator import ExperiencePersistenceCoordinator

storage = Path(sys.argv[1])
result = Path(sys.argv[2])
storage.mkdir(parents=True, exist_ok=True)

experience_repo = JsonFileExperienceRepository(storage / "experience.json")
protection_repo = JsonFileProtectionRepository(storage / "protection.json")
journal = JsonFileCoordinationJournal(storage / "coordination.json")

experience = Experience.create()

protection = ExperienceProtection.protected(
        experience.experience_id
    )

coordinator = ExperiencePersistenceCoordinator(
    experience_repo,
    protection_repo,
    journal,
)

original_advance = journal.advance

def crash_after_experience_written(operation_id, stage):
    record = original_advance(operation_id, stage)
    if getattr(stage, "name", str(stage)) == "EXPERIENCE_WRITTEN":
        result.write_text(
            json.dumps({
                "pid": os.getpid(),
                "experience_id": str(experience.experience_id),
                "stage": "EXPERIENCE_WRITTEN",
            }),
            encoding="utf-8",
        )
        os._exit(73)
    return record

journal.advance = crash_after_experience_written

coordinator.persist(experience, protection)
raise RuntimeError("Process A should have terminated before COMPLETE")

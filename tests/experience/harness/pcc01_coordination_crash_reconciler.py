from pathlib import Path
import json
import os
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "lib" / "python"))

from experience.identity import ExperienceId
from experience.persistent_repository import JsonFileExperienceRepository
from experience.protection_repository import JsonFileProtectionRepository
from experience.coordination_journal import JsonFileCoordinationJournal
from experience.persistence_coordinator import ExperiencePersistenceCoordinator

storage = Path(sys.argv[1])
writer_result = Path(sys.argv[2])
reader_result = Path(sys.argv[3])

before = json.loads(writer_result.read_text(encoding="utf-8"))

experience_repo = JsonFileExperienceRepository(storage / "experience.json")
protection_repo = JsonFileProtectionRepository(storage / "protection.json")
journal = JsonFileCoordinationJournal(storage / "coordination.json")

coordinator = ExperiencePersistenceCoordinator(
    experience_repo,
    protection_repo,
    journal,
)

pairs = coordinator.reconcile_incomplete()

if len(pairs) != 1:
    raise RuntimeError(f"Expected exactly one reconciled pair, got {len(pairs)}")

pair = pairs[0]
after_id = str(pair.experience.experience_id)

if after_id != before["experience_id"]:
    raise RuntimeError(
        f"Identity changed across restart: {before[chr(39)+chr(34)+"experience_id"+chr(34)+chr(39)]} != {after_id}"
    )

incomplete = journal.incomplete_records()
if incomplete:
    raise RuntimeError(
        f"Durable operation remained incomplete: {len(incomplete)}"
    )

reader_result.write_text(
    json.dumps({
        "pid": os.getpid(),
        "experience_id": after_id,
        "reconciled_pairs": len(pairs),
        "incomplete_records": len(incomplete),
    }),
    encoding="utf-8",
)

print(after_id)

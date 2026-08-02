#!/usr/bin/env python3

import json
import shutil
from datetime import datetime
from pathlib import Path
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()

MEMORY = ROOT / ".ai" / "memory"
CONTEXT = ROOT / ".ai" / "context"

MEMORY.mkdir(parents=True, exist_ok=True)

PROFILE = CONTEXT / "repository_profile.json"

history = MEMORY / "history.json"

if history.exists():
    data = json.loads(history.read_text(encoding="utf-8"))
else:
    data = {
        "repository": ROOT.name,
        "events": []
    }

event = {
    "timestamp": datetime.utcnow().isoformat() + "Z",
    "type": "repository_profile"
}

if PROFILE.exists():
    archive = MEMORY / f"repository_profile_{len(data['events'])+1}.json"
    shutil.copy2(PROFILE, archive)
    event["file"] = archive.name
    event["status"] = "saved"
else:
    event["status"] = "missing_profile"

data["events"].append(event)

history.write_text(
    json.dumps(data, indent=2),
    encoding="utf-8"
)

print("==================================")
print("Memory Engine")
print("==================================")
print()
print("Repository:", ROOT.name)
print("Events:", len(data["events"]))
print("History:", history)
print()
print("Done.")

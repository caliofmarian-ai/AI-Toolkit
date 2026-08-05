# DEPRECATED: This module is frozen for compatibility only.
# See docs/implementation/MODULE_CLASSIFICATION.md — Disposition: DEPRECATE
# Do not add features. Use the canonical module packages instead.

#!/usr/bin/env python3

import json
import shutil
from datetime import datetime, UTC
from pathlib import Path
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()

MEMORY = ROOT / ".ai" / "memory"
CONTEXT = ROOT / ".ai" / "context"

MEMORY.mkdir(parents=True, exist_ok=True)

PROFILE = CONTEXT / "repository_profile.json"
HISTORY = MEMORY / "history.json"
INDEX = MEMORY / "index.json"

if HISTORY.exists():
    history = json.loads(HISTORY.read_text(encoding="utf-8"))
else:
    history = {
        "repository": ROOT.name,
        "events": []
    }

timestamp = datetime.now(UTC).isoformat()

event = {
    "timestamp": timestamp,
    "type": "repository_profile"
}

latest_profile = None

if PROFILE.exists():
    archive = MEMORY / f"repository_profile_{len(history['events']) + 1}.json"
    shutil.copy2(PROFILE, archive)
    latest_profile = archive.name
    event["file"] = archive.name
    event["status"] = "saved"
else:
    event["status"] = "missing_profile"

history["events"].append(event)

HISTORY.write_text(
    json.dumps(history, indent=2),
    encoding="utf-8"
)

index = {
    "repository": ROOT.name,
    "created": history["events"][0]["timestamp"],
    "last_update": timestamp,
    "events": len(history["events"]),
    "latest_profile": latest_profile,
    "latest_plan": "plan.md" if (ROOT / ".ai/work/plan.md").exists() else None,
    "latest_review": "review.md" if (ROOT / ".ai/work/review.md").exists() else None,
    "latest_execution": "execution.log" if (ROOT / ".ai/work/execution.log").exists() else None
}

INDEX.write_text(
    json.dumps(index, indent=2),
    encoding="utf-8"
)

print("==================================")
print("Memory Engine")
print("==================================")
print()
print("Repository:", ROOT.name)
print("Events:", len(history["events"]))
print("History:", HISTORY)
print("Index:", INDEX)
print()
print("Done.")

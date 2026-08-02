#!/usr/bin/env python3

import json
from pathlib import Path

from checks import (
    DirectoryStructureCheck,
    EngineInventoryCheck,
    CanonicalDocumentsCheck,
)

ROOT = Path(".").resolve()

checks = [
    DirectoryStructureCheck(),
    EngineInventoryCheck(),
    CanonicalDocumentsCheck(),
]

report = {
    "checks": [],
    "warnings": []
}

score = 0
maximum = 0

for check in checks:

    r = check.run(ROOT)

    score += r.score
    maximum += r.max_score

    report["checks"].append({
        "name": r.name,
        "score": r.score,
        "maximum": r.max_score
    })

    report["warnings"].extend(r.warnings)

report["score"] = round(score / maximum * 100)

out = ROOT / ".ai" / "audit" / "foundation_audit_002.json"
out.parent.mkdir(parents=True, exist_ok=True)

out.write_text(
    json.dumps(report, indent=2),
    encoding="utf-8"
)

print("==================================")
print("Foundation Audit v2")
print("==================================")
print()

for c in report["checks"]:
    print(
        f'{c["name"]}: {c["score"]}/{c["maximum"]}'
    )

print()
print("Global Score:", report["score"])

if report["warnings"]:
    print()
    print("Warnings")
    for w in report["warnings"]:
        print("-", w)

print()
print("Saved:", out)

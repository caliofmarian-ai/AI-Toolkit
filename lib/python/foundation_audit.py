# DEPRECATED: This module is frozen for compatibility only.
# See docs/implementation/MODULE_CLASSIFICATION.md — Disposition: DEPRECATE
# Do not add features. Use the canonical module packages instead.

#!/usr/bin/env python3

import json
from pathlib import Path

ROOT = Path(".").resolve()

report = {
    "repository": ROOT.name,
    "audit": "AUD-001 Repository Architecture",
    "status": "PASS",
    "score": 0,
    "metrics": {},
    "warnings": []
}

required = {
    "bin": "CLI",
    "lib": "Libraries",
    "development": "Development",
    "docs": "Documentation",
    "tests": "Tests",
    ".ai": "AI Workspace"
}

score = 0

for folder, label in required.items():
    if (ROOT / folder).exists():
        score += 15
    else:
        report["warnings"].append(f"Missing directory: {folder}")

report["metrics"]["directories"] = len([p for p in ROOT.iterdir() if p.is_dir()])
report["metrics"]["files"] = len(list(ROOT.rglob("*")))

report["metrics"]["engines"] = len(list((ROOT/"lib").rglob("*engine*"))) if (ROOT/"lib").exists() else 0
report["metrics"]["canonical_docs"] = len(list((ROOT/"docs/canonical").glob("*.md"))) if (ROOT/"docs/canonical").exists() else 0
report["metrics"]["tests"] = len(list((ROOT/"tests").rglob("*"))) if (ROOT/"tests").exists() else 0

report["score"] = min(score + 10,100)

out = ROOT / ".ai" / "audit" / "foundation_audit_001.json"
out.parent.mkdir(parents=True, exist_ok=True)

out.write_text(json.dumps(report, indent=2), encoding="utf-8")

print("======================================")
print("FOUNDATION AUDIT")
print("======================================")
print()
print("Audit :", report["audit"])
print("Score :", report["score"])
print()

for k,v in report["metrics"].items():
    print(f"{k}: {v}")

if report["warnings"]:
    print()
    print("Warnings")
    for w in report["warnings"]:
        print("-",w)

print()
print("Saved:",out)

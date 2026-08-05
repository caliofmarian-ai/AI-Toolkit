# DEPRECATED: This module is frozen for compatibility only.
# See docs/implementation/MODULE_CLASSIFICATION.md — Disposition: DEPRECATE
# Do not add features. Use the canonical module packages instead.

#!/usr/bin/env python3

import json
from pathlib import Path

ROOT = Path(".").resolve()

report = {
    "repository": ROOT.name,
    "engines": [],
    "python_modules": [],
    "tests": [],
    "canonical_documents": [],
    "development_batches": [],
    "audit_modules": [],
    "cli_commands": []
}

# Engines (.sh)
for f in sorted((ROOT / "lib").glob("*engine*.sh")):
    report["engines"].append(str(f.relative_to(ROOT)))

# Python modules
if (ROOT / "lib/python").exists():
    for f in sorted((ROOT / "lib/python").rglob("*.py")):
        report["python_modules"].append(str(f.relative_to(ROOT)))

# Tests
if (ROOT / "tests").exists():
    for f in sorted((ROOT / "tests").glob("*")):
        report["tests"].append(str(f.relative_to(ROOT)))

# Canonical docs
if (ROOT / "docs/canonical").exists():
    for f in sorted((ROOT / "docs/canonical").glob("*.md")):
        report["canonical_documents"].append(str(f.relative_to(ROOT)))

# Development batches
if (ROOT / "development").exists():
    for f in sorted((ROOT / "development").glob("BATCH-*")):
        report["development_batches"].append(str(f.relative_to(ROOT)))

# Audit modules
audit = ROOT / "lib/python/foundation_audit"
if audit.exists():
    for f in sorted(audit.glob("*.py")):
        report["audit_modules"].append(str(f.relative_to(ROOT)))

# CLI
launcher = ROOT / "bin" / "ai"
if launcher.exists():
    text = launcher.read_text(encoding="utf-8")

    for cmd in [
        "discover",
        "inspect",
        "context",
        "work",
        "git",
        "github",
        "issue"
    ]:
        if cmd in text:
            report["cli_commands"].append(cmd)

out = ROOT / ".ai" / "audit" / "repository_inventory.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(report, indent=2), encoding="utf-8")

print("==================================")
print("Repository Inventory")
print("==================================")
print()

for key in [
    "engines",
    "python_modules",
    "tests",
    "canonical_documents",
    "development_batches",
    "audit_modules",
    "cli_commands"
]:
    print(f"{key}: {len(report[key])}")

print()
print("Saved:", out)

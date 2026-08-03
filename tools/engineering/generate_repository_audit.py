#!/usr/bin/env python3

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from lib.python.engineering_engine.repository_audit import RepositoryAudit

output = (
    ROOT
    / "implementation-packages"
    / "CORE-022"
    / "repository-audit.md"
)

RepositoryAudit(ROOT).write_markdown(output)

print()
print("========================================")
print("Repository Audit generated successfully")
print("========================================")
print(output)

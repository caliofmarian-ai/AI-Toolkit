#!/usr/bin/env python3

from pathlib import Path

ROOT = Path(".")

patterns = [
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".DS_Store",
]

extensions = [
    ".pyc",
    ".pyo"
]

issues = []

for path in ROOT.rglob("*"):

    if path.name in patterns:
        issues.append(path)

    if path.suffix in extensions:
        issues.append(path)

print("==================================")
print("Repository Hygiene Audit")
print("==================================")
print()

if not issues:
    print("PASS")
else:
    print("FOUND", len(issues), "issues")
    print()

    for item in issues:
        print(item)

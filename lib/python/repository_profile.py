# DEPRECATED: This module is frozen for compatibility only.
# See docs/implementation/MODULE_CLASSIFICATION.md — Disposition: DEPRECATE
# Do not add features. Use the canonical module packages instead.

#!/usr/bin/env python3

import json
import os
import subprocess
from pathlib import Path

ROOT = Path(os.path.abspath(os.sys.argv[1] if len(os.sys.argv) > 1 else "."))

def count(pattern):
    return len(list(ROOT.rglob(pattern)))

def exists(name):
    return (ROOT / name).exists()

def git(cmd):
    try:
        return subprocess.check_output(
            ["git", "-C", str(ROOT)] + cmd,
            text=True
        ).strip()
    except Exception:
        return ""

profile = {
    "repository": ROOT.name,
    "root": str(ROOT),
    "branch": git(["branch", "--show-current"]),
    "languages": [],
    "package_managers": [],
    "features": {},
    "statistics": {},
}

if count("*.py"):
    profile["languages"].append("Python")

if count("*.sh"):
    profile["languages"].append("Shell")

if count("*.js"):
    profile["languages"].append("JavaScript")

if count("*.ts"):
    profile["languages"].append("TypeScript")

if count("*.md"):
    profile["languages"].append("Markdown")

if exists("requirements.txt"):
    profile["package_managers"].append("pip")

if exists("pyproject.toml"):
    profile["package_managers"].append("poetry")

if exists("package.json"):
    profile["package_managers"].append("npm")

if exists("pnpm-lock.yaml"):
    profile["package_managers"].append("pnpm")

profile["features"] = {
    "git": exists(".git"),
    "tests": exists("tests"),
    "canonical": exists("docs/canonical"),
    "plugins": exists("plugins"),
    "railway": exists("railway.json"),
    "github_actions": exists(".github/workflows"),
}

profile["statistics"] = {
    "engines": len(list((ROOT / "lib").glob("*engine*.sh"))) if (ROOT / "lib").exists() else 0,
    "tests": count("test*.sh"),
    "canonical_documents": len(list((ROOT / "docs/canonical").glob("*.md"))) if (ROOT / "docs/canonical").exists() else 0,
}

ctx = ROOT / ".ai" / "context"
ctx.mkdir(parents=True, exist_ok=True)

outfile = ctx / "repository_profile.json"

outfile.write_text(
    json.dumps(profile, indent=2),
    encoding="utf-8"
)

print(json.dumps(profile, indent=2))

print()
print("Profile saved:")
print(outfile)

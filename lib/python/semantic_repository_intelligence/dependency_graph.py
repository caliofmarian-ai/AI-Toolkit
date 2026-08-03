"""
Semantic Repository Intelligence — Dependency Graph Builder
CORE-008B

Parses manifest files (requirements.txt, setup.py, pyproject.toml,
package.json, Cargo.toml, go.mod) to build a graph of external package
dependencies.
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from .models import DependencyGraphResult, ExternalDependency, FileAnalysis


# ---------------------------------------------------------------------------
# Manifest parsers
# ---------------------------------------------------------------------------

_REQ_LINE_RE = re.compile(
    r"^\s*([A-Za-z0-9_\-\.]+)\s*([><=!~^][^;#\s]*)?",
)
_SETUP_INSTALL_RE = re.compile(
    r"""install_requires\s*=\s*\[([^\]]+)\]""",
    re.DOTALL,
)
_SETUP_PKG_RE = re.compile(r"""['"]([\w\-\.]+)[^'"]*['"]""")

_TOML_SECTION_RE = re.compile(r"^\[([^\]]+)\]", re.MULTILINE)
_TOML_DEP_RE = re.compile(
    r"""^([\w\-\.]+)\s*=\s*['"]([^'"]+)['"]""",
    re.MULTILINE,
)
_GO_REQUIRE_RE = re.compile(
    r"""^\s+([\w./\-]+)\s+(v[\d.]+(?:-[\w.]+)?)""",
    re.MULTILINE,
)


def _parse_requirements(text: str, source_file: str) -> List[ExternalDependency]:
    deps = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith(("#", "-r", "--")):
            continue
        m = _REQ_LINE_RE.match(line)
        if m:
            name = m.group(1)
            version = (m.group(2) or "").strip()
            deps.append(ExternalDependency(
                name=name, version_spec=version,
                source_file=source_file, ecosystem="pip",
            ))
    return deps


def _parse_setup_py(text: str, source_file: str) -> List[ExternalDependency]:
    deps = []
    m = _SETUP_INSTALL_RE.search(text)
    if m:
        for pkg_m in _SETUP_PKG_RE.finditer(m.group(1)):
            name = pkg_m.group(1)
            deps.append(ExternalDependency(
                name=name, version_spec="",
                source_file=source_file, ecosystem="pip",
            ))
    return deps


def _parse_pyproject_toml(text: str, source_file: str) -> List[ExternalDependency]:
    deps = []
    in_deps = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("["):
            in_deps = stripped in (
                "[tool.poetry.dependencies]",
                "[project.dependencies]",
                "[dependencies]",
            )
            continue
        if in_deps and "=" in stripped:
            m = _TOML_DEP_RE.match(stripped)
            if m:
                deps.append(ExternalDependency(
                    name=m.group(1), version_spec=m.group(2),
                    source_file=source_file, ecosystem="pip",
                ))
    return deps


def _parse_package_json(text: str, source_file: str) -> List[ExternalDependency]:
    deps = []
    try:
        data = json.loads(text)
    except (json.JSONDecodeError, ValueError):
        return deps
    for key in ("dependencies", "devDependencies", "peerDependencies"):
        block = data.get(key, {})
        if isinstance(block, dict):
            for name, version in sorted(block.items()):
                deps.append(ExternalDependency(
                    name=name, version_spec=str(version),
                    source_file=source_file, ecosystem="npm",
                ))
    return deps


def _parse_go_mod(text: str, source_file: str) -> List[ExternalDependency]:
    deps = []
    in_require = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped == "require (":
            in_require = True
            continue
        if in_require and stripped == ")":
            in_require = False
            continue
        if in_require or stripped.startswith("require "):
            m = _GO_REQUIRE_RE.match(line)
            if m:
                deps.append(ExternalDependency(
                    name=m.group(1), version_spec=m.group(2),
                    source_file=source_file, ecosystem="go",
                ))
    return deps


# File name → parser function mapping
_MANIFEST_PARSERS = {
    "requirements.txt": _parse_requirements,
    "requirements-dev.txt": _parse_requirements,
    "requirements_dev.txt": _parse_requirements,
    "setup.py": _parse_setup_py,
    "pyproject.toml": _parse_pyproject_toml,
    "package.json": _parse_package_json,
    "go.mod": _parse_go_mod,
}

# Also handle requirements files by pattern
_REQUIREMENTS_RE = re.compile(r"requirements.*\.txt$", re.IGNORECASE)


class DependencyGraphBuilder:
    """
    Builds a DependencyGraph by parsing manifest files found in the workspace.
    """

    def build(
        self,
        file_analyses: Dict[str, FileAnalysis],
        root: Path,
    ) -> DependencyGraphResult:
        external: List[ExternalDependency] = []
        seen_names = set()

        # Parse manifest files
        for path in sorted(file_analyses.keys()):
            filename = Path(path).name
            abs_path = root / path

            parser = _MANIFEST_PARSERS.get(filename)
            if parser is None and _REQUIREMENTS_RE.match(filename):
                parser = _parse_requirements

            if parser is None:
                continue

            try:
                text = abs_path.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue

            deps = parser(text, path)
            for dep in deps:
                key = (dep.name.lower(), dep.ecosystem)
                if key not in seen_names:
                    seen_names.add(key)
                    external.append(dep)

        # Collect internal Python module paths
        internal = sorted(
            p for p, fa in file_analyses.items() if fa.language == "python"
        )

        return DependencyGraphResult(
            external_dependencies=sorted(external, key=lambda d: (d.ecosystem, d.name)),
            internal_modules=internal,
            dependency_count=len(external),
        )

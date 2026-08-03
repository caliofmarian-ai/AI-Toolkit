"""
Executable Repository Intelligence — File Classifier
CORE-008C

Classifies every repository file into one of the canonical categories.
Reuses CORE-008B FileAnalysis data to avoid duplicate AST parsing.
"""

import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from .models import FileClassification


# ---------------------------------------------------------------------------
# Classification rules
#
# Each rule is (category, subcategory, is_executable, confidence, [matchers])
# where matchers is a list of (kind, value) pairs:
#   kind ∈ {"path_contains", "path_startswith", "extension", "filename",
#            "filename_re", "path_re"}
# ---------------------------------------------------------------------------

_RULES: List[Tuple[str, str, bool, float, List[Tuple[str, str]]]] = [
    # ---- Temporary --------------------------------------------------------
    ("Temporary", "Temp file", False, 0.95, [
        ("path_contains", "/tmp/"),
        ("path_contains", "/.tmp/"),
    ]),
    ("Temporary", "Temp file", False, 0.90, [
        ("extension", ".tmp"),
        ("extension", ".swp"),
        ("extension", ".bak"),
    ]),
    ("Temporary", "Cache file", False, 0.90, [
        ("extension", ".pyc"),
        ("path_contains", "/__pycache__/"),
        ("path_contains", "/.pytest_cache/"),
        ("path_contains", "/.mypy_cache/"),
    ]),

    # ---- Generated Artifact -----------------------------------------------
    ("Generated Artifact", "Compiled output", False, 0.95, [
        ("extension", ".pyo"),
        ("extension", ".so"),
        ("extension", ".dll"),
        ("extension", ".egg"),
        ("path_contains", "/dist/"),
        ("path_contains", "/build/"),
        ("path_contains", "/.eggs/"),
    ]),
    ("Generated Artifact", "Lock file", False, 0.90, [
        ("filename", "package-lock.json"),
        ("filename", "yarn.lock"),
        ("filename", "poetry.lock"),
        ("filename", "Pipfile.lock"),
        ("filename", "Cargo.lock"),
    ]),

    # ---- Reports -----------------------------------------------------------
    ("Reports", "Integration report", False, 0.95, [
        ("filename", "AI_CTO_INTEGRATION_REPORT.md"),
    ]),
    ("Reports", "Execution model", False, 0.95, [
        ("filename", "AI_CTO_EXECUTION_MODEL.md"),
    ]),
    ("Reports", "Report file", False, 0.85, [
        ("path_contains", "/reports/"),
        ("filename_re", r".*[Rr]eport.*\.md$"),
        ("filename_re", r".*[Rr]eport.*\.html$"),
    ]),
    ("Reports", "Audit report", False, 0.85, [
        ("path_contains", "/audit/"),
    ]),

    # ---- Canonical Specification -------------------------------------------
    ("Canonical Specification", "Canonical document", False, 0.95, [
        ("path_contains", "/canonical/"),
        ("filename_re", r"^CANON-.*\.md$"),
    ]),

    # ---- Documentation -----------------------------------------------------
    ("Documentation", "Markdown documentation", False, 0.90, [
        ("extension", ".md"),
        ("extension", ".rst"),
        ("extension", ".txt"),
    ]),
    ("Documentation", "Documentation directory", False, 0.90, [
        ("path_startswith", "docs/"),
        ("path_contains", "/docs/"),
    ]),
    ("Documentation", "License file", False, 0.95, [
        ("filename_re", r"^LICENSE"),
        ("filename_re", r"^LICENCE"),
        ("filename_re", r"^COPYING"),
    ]),
    ("Documentation", "Changelog", False, 0.90, [
        ("filename_re", r"^CHANGELOG"),
        ("filename_re", r"^CHANGES"),
        ("filename_re", r"^HISTORY"),
    ]),
    ("Documentation", "Readme", False, 0.95, [
        ("filename_re", r"^README"),
    ]),

    # ---- Infrastructure ---------------------------------------------------
    ("Infrastructure", "Docker", False, 0.95, [
        ("filename_re", r"^Dockerfile"),
        ("filename", "docker-compose.yml"),
        ("filename", "docker-compose.yaml"),
        ("filename", ".dockerignore"),
    ]),
    ("Infrastructure", "CI/CD pipeline", False, 0.95, [
        ("path_contains", "/.github/"),
        ("path_contains", "/.gitlab-ci"),
        ("filename", ".travis.yml"),
        ("filename", "Jenkinsfile"),
        ("filename", ".circleci"),
    ]),
    ("Infrastructure", "Makefile", False, 0.90, [
        ("filename", "Makefile"),
        ("filename", "makefile"),
        ("filename", "GNUmakefile"),
    ]),
    ("Infrastructure", "Deployment script", False, 0.85, [
        ("path_contains", "/deploy/"),
        ("path_contains", "/deployment/"),
        ("path_contains", "/infrastructure/"),
        ("path_contains", "/k8s/"),
        ("path_contains", "/helm/"),
    ]),

    # ---- Assets -----------------------------------------------------------
    ("Assets", "Image", False, 0.95, [
        ("extension", ".png"),
        ("extension", ".jpg"),
        ("extension", ".jpeg"),
        ("extension", ".gif"),
        ("extension", ".svg"),
        ("extension", ".ico"),
        ("extension", ".webp"),
    ]),
    ("Assets", "Font", False, 0.95, [
        ("extension", ".ttf"),
        ("extension", ".woff"),
        ("extension", ".woff2"),
        ("extension", ".eot"),
    ]),
    ("Assets", "CSS stylesheet", False, 0.90, [
        ("extension", ".css"),
        ("extension", ".scss"),
        ("extension", ".sass"),
        ("extension", ".less"),
    ]),

    # ---- Tests ------------------------------------------------------------
    ("Tests", "Test file", False, 0.95, [
        ("path_contains", "/tests/"),
        ("path_contains", "/test/"),
        ("path_contains", "/spec/"),
        ("filename_re", r"^test_.*\.py$"),
        ("filename_re", r".*_test\.py$"),
        ("filename_re", r".*\.test\.ts$"),
        ("filename_re", r".*\.spec\.ts$"),
        ("filename_re", r".*\.test\.js$"),
        ("filename_re", r".*\.spec\.js$"),
        ("filename_re", r"^test_.*\.sh$"),
    ]),

    # ---- Scripts ----------------------------------------------------------
    ("Scripts", "Shell script", True, 0.90, [
        ("extension", ".sh"),
        ("extension", ".bash"),
        ("path_contains", "/bin/"),
    ]),

    # ---- Environment ------------------------------------------------------
    ("Environment", "Env file", False, 0.95, [
        ("filename_re", r"^\.env"),
    ]),
    ("Environment", "Environment config", False, 0.85, [
        ("extension", ".env"),
    ]),

    # ---- Configuration ----------------------------------------------------
    ("Configuration", "Python config/manifest", False, 0.90, [
        ("filename", "setup.py"),
        ("filename", "setup.cfg"),
        ("filename", "pyproject.toml"),
        ("filename", "Pipfile"),
        ("filename", "requirements.txt"),
        ("filename_re", r"^requirements.*\.txt$"),
        ("filename", "tox.ini"),
        ("filename", "pytest.ini"),
        ("filename", ".flake8"),
        ("filename", "mypy.ini"),
    ]),
    ("Configuration", "Node.js manifest", False, 0.90, [
        ("filename", "package.json"),
        ("filename", "tsconfig.json"),
        ("filename", ".eslintrc"),
        ("filename", ".eslintrc.json"),
        ("filename", ".babelrc"),
    ]),
    ("Configuration", "YAML config", False, 0.80, [
        ("extension", ".yml"),
        ("extension", ".yaml"),
    ]),
    ("Configuration", "TOML config", False, 0.80, [
        ("extension", ".toml"),
    ]),
    ("Configuration", "INI config", False, 0.80, [
        ("extension", ".ini"),
        ("extension", ".cfg"),
    ]),
    ("Configuration", "Git config", False, 0.95, [
        ("filename", ".gitignore"),
        ("filename", ".gitattributes"),
    ]),

    # ---- Deprecated -------------------------------------------------------
    ("Deprecated", "Backup file", False, 0.90, [
        ("extension", ".bak"),
        ("filename_re", r".*\.bak$"),
        ("filename_re", r".*\.old$"),
    ]),

    # ---- Extension Point --------------------------------------------------
    ("Extension Point", "Plugin file", True, 0.80, [
        ("filename_re", r".*plugin.*\.py$"),
        ("filename_re", r".*extension.*\.py$"),
        ("path_contains", "/plugins/"),
        ("path_contains", "/extensions/"),
    ]),

    # ---- Plugin API -------------------------------------------------------
    ("Plugin API", "Plugin interface", True, 0.80, [
        ("filename_re", r".*plugin.*interface.*\.py$"),
        ("path_contains", "/plugin_api/"),
    ]),

    # ---- Bootstrap --------------------------------------------------------
    ("Bootstrap", "Bootstrap/init file", True, 0.85, [
        ("filename", "__init__.py"),
        ("filename", "bootstrap.py"),
        ("filename_re", r"^bootstrap.*\.py$"),
        ("path_contains", "/bootstrap/"),
    ]),

    # ---- Runtime Entry Point ----------------------------------------------
    ("Runtime Entry Point", "Main entry point", True, 0.95, [
        ("filename", "__main__.py"),
        ("filename", "main.py"),
        ("filename", "app.py"),
        ("filename", "run.py"),
        ("filename", "server.py"),
        ("filename", "start.py"),
        ("filename", "bot.py"),
        ("filename_re", r"^main\..*$"),
        ("filename_re", r"^run\..*$"),
    ]),

    # ---- Public API -------------------------------------------------------
    ("Public API", "API surface", True, 0.85, [
        ("path_contains", "/api/"),
        ("filename_re", r".*_api\.py$"),
        ("filename_re", r"^api.*\.py$"),
    ]),

    # ---- Internal API -----------------------------------------------------
    ("Internal API", "Internal interface", True, 0.75, [
        ("filename_re", r".*interface.*\.py$"),
        ("filename_re", r".*contract.*\.py$"),
        ("filename_re", r".*protocol.*\.py$"),
    ]),
]


# ---------------------------------------------------------------------------
# Classifier
# ---------------------------------------------------------------------------

def _match_any(path_str: str, filename: str, matchers: List[Tuple[str, str]]) -> bool:
    """Return True if the path matches any of the given matchers."""
    for kind, value in matchers:
        if kind == "path_contains" and value in ("/" + path_str):
            return True
        elif kind == "path_startswith" and path_str.startswith(value):
            return True
        elif kind == "extension" and path_str.endswith(value):
            return True
        elif kind == "filename" and filename == value:
            return True
        elif kind == "filename_re" and re.match(value, filename):
            return True
        elif kind == "path_re" and re.search(value, path_str):
            return True
    return False


class FileClassifier:
    """
    Classifies every repository file into a canonical category.

    Reuses CORE-008B FileAnalysis metadata to enrich classification
    without re-parsing source files.
    """

    def classify_all(
        self,
        file_analyses: Dict,   # path → FileAnalysis (from CORE-008B)
        root: Path,
    ) -> List[FileClassification]:
        """
        Classify all files and return a sorted, deterministic list.
        """
        results: List[FileClassification] = []
        for path_str in sorted(file_analyses.keys()):
            fa = file_analyses[path_str]
            fc = self._classify(path_str, fa)
            results.append(fc)
        return results

    def _classify(self, path_str: str, fa) -> FileClassification:
        filename = Path(path_str).name

        # Walk rules in order; first match wins
        for category, subcategory, is_exec, confidence, matchers in _RULES:
            if _match_any(path_str, filename, matchers):
                evidence = ["Matched rule: %s/%s" % (category, subcategory)]
                return FileClassification(
                    path=path_str,
                    category=category,
                    subcategory=subcategory,
                    is_executable=is_exec,
                    confidence=confidence,
                    evidence=evidence,
                )

        # Fall through to language-based classification
        return self._language_fallback(path_str, filename, fa)

    def _language_fallback(self, path_str: str, filename: str, fa) -> FileClassification:
        """Classify by language detected by AST analyzer."""
        lang = getattr(fa, "language", "unknown")
        entry_points = getattr(fa, "entry_points", [])

        if lang == "markdown":
            return FileClassification(
                path=path_str,
                category="Documentation",
                subcategory="Markdown documentation",
                is_executable=False,
                confidence=0.85,
                evidence=["Language: markdown"],
            )

        if lang in ("python", "typescript", "javascript"):
            # Has entry points → Runtime Entry Point
            if entry_points:
                return FileClassification(
                    path=path_str,
                    category="Runtime Entry Point",
                    subcategory="Detected entry point",
                    is_executable=True,
                    confidence=0.85,
                    evidence=["Language: %s; entry_points: %s" % (lang, entry_points)],
                )
            # Otherwise it's executable code
            return FileClassification(
                path=path_str,
                category="Executable Code",
                subcategory=lang.capitalize() + " module",
                is_executable=True,
                confidence=0.80,
                evidence=["Language: %s" % lang],
            )

        if lang in ("json", "yaml"):
            return FileClassification(
                path=path_str,
                category="Configuration",
                subcategory=lang.upper() + " config",
                is_executable=False,
                confidence=0.70,
                evidence=["Language: %s" % lang],
            )

        return FileClassification(
            path=path_str,
            category="Unknown",
            subcategory="Unclassified",
            is_executable=False,
            confidence=0.30,
            evidence=["No matching rule or known language"],
        )

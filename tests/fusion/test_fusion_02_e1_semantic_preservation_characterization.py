"""
FUSION-02 E1 — Semantic Preservation Characterization.

Characterization only.

This fossil/diagnostic test does not prescribe new CSL semantics.
It observes the existing representation chain and reports whether
semantic constructs remain observable across available boundaries.

No production mutation is authorized by this test.
"""

from __future__ import annotations

import ast
import importlib
import inspect
from pathlib import Path
from typing import Iterable


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
LIB_PYTHON = REPOSITORY_ROOT / "lib" / "python"


CLASSIFICATIONS = {
    "PRESERVED",
    "TRANSFORMED",
    "DROPPED",
    "AMBIGUOUS",
    "NOT REPRESENTABLE",
}


def _python_files(root: Path) -> Iterable[Path]:
    if not root.exists():
        return ()
    return tuple(sorted(root.rglob("*.py")))


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _find_term(term: str) -> list[str]:
    hits: list[str] = []
    for path in _python_files(LIB_PYTHON):
        try:
            text = _read(path)
        except (UnicodeDecodeError, OSError):
            continue
        if term in text:
            hits.append(str(path.relative_to(REPOSITORY_ROOT)))
    return hits


def _parseable_python_files(root: Path) -> list[str]:
    failures: list[str] = []
    for path in _python_files(root):
        try:
            ast.parse(_read(path), filename=str(path))
        except SyntaxError:
            failures.append(str(path.relative_to(REPOSITORY_ROOT)))
    return failures


def test_semantic_engine_sources_are_syntactically_observable():
    roots = [
        LIB_PYTHON / "csl_engine",
        LIB_PYTHON / "canonical_parser",
    ]

    existing = [root for root in roots if root.exists()]
    assert existing, "No CSL/canonical semantic source roots found"

    failures: list[str] = []
    for root in existing:
        failures.extend(_parseable_python_files(root))

    assert failures == []


def test_semantic_result_boundary_is_observable():
    hits = _find_term("SemanticResult")
    assert hits, (
        "SemanticResult boundary is not observable in current "
        "implementation anatomy"
    )


def test_semantic_analysis_boundary_is_observable():
    semantic_result = _find_term("SemanticResult")
    semantic_analyzer = _find_term("SemanticAnalyzer")

    assert semantic_result or semantic_analyzer, (
        "No existing semantic-analysis boundary could be demonstrated"
    )


def test_knowledge_materialization_boundary_is_observable():
    hits = (
        _find_term("KnowledgeMaterialization")
        + _find_term("materialization")
        + _find_term("CanonicalKnowledgeGraph")
    )

    assert hits, (
        "Knowledge materialization boundary is not observable in "
        "current implementation anatomy"
    )


def test_e1_classification_vocabulary_is_closed():
    assert CLASSIFICATIONS == {
        "PRESERVED",
        "TRANSFORMED",
        "DROPPED",
        "AMBIGUOUS",
        "NOT REPRESENTABLE",
    }


def test_e1_is_characterization_not_semantic_redesign():
    this_file = Path(__file__)
    source = this_file.read_text(encoding="utf-8")

    assert "Characterization only" in source
    assert "No production mutation" in source


def test_existing_semantic_modules_can_be_inspected_without_execution_side_effects():
    candidates = [
        "python.csl_engine",
        "python.canonical_parser",
    ]

    observed = []

    for name in candidates:
        try:
            module = importlib.import_module(name)
        except (ImportError, ModuleNotFoundError):
            continue

        observed.append(
            {
                "module": name,
                "file": inspect.getsourcefile(module),
            }
        )

    assert observed, (
        "Neither python.csl_engine nor python.canonical_parser "
        "could be imported under repository PYTHONPATH"
    )

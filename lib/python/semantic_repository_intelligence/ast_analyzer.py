"""
Semantic Repository Intelligence — AST Analyzer
CORE-008B

Extracts symbols, imports, and structural information from source files.
Supports Python (via ast module), TypeScript, JavaScript, JSON, YAML, and
Markdown.  Designed for language-plugin extensibility.
"""

import ast
import json
import re
from pathlib import Path
from typing import Dict, List, Optional

from .models import (
    ClassSymbol,
    ConstantSymbol,
    FileAnalysis,
    FunctionSymbol,
    ImportSymbol,
)

# ---------------------------------------------------------------------------
# Language plugin interface
# ---------------------------------------------------------------------------

class LanguageAnalyzer:
    """Base class for language-specific file analyzers."""

    EXTENSIONS: List[str] = []

    def can_handle(self, extension: str) -> bool:
        return extension in self.EXTENSIONS

    def analyze(self, path: str, text: str) -> FileAnalysis:  # pragma: no cover
        raise NotImplementedError


# ---------------------------------------------------------------------------
# Python analyzer
# ---------------------------------------------------------------------------

class PythonAnalyzer(LanguageAnalyzer):
    """Full AST-based analyzer for Python source files."""

    EXTENSIONS = [".py"]

    def analyze(self, path: str, text: str) -> FileAnalysis:
        result = FileAnalysis(path=path, language="python")
        try:
            tree = ast.parse(text, filename=path)
        except SyntaxError as exc:
            result.error = "SyntaxError: %s" % exc
            return result

        module_globals: set = set()

        for node in ast.walk(tree):
            # Top-level class definitions
            if isinstance(node, ast.ClassDef):
                bases = [self._name(b) for b in node.bases]
                methods = [
                    n.name
                    for n in node.body
                    if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
                ]
                is_abstract = any(
                    b in ("ABC", "ABCMeta") or "Abstract" in b
                    for b in bases
                )
                decorators = [self._name(d) for d in node.decorator_list]
                result.classes.append(ClassSymbol(
                    name=node.name,
                    bases=bases,
                    methods=methods,
                    is_abstract=is_abstract,
                    decorators=decorators,
                    line=node.lineno,
                ))

            # Top-level and nested function definitions
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                args = [a.arg for a in node.args.args]
                is_method = len(node.args.args) > 0 and node.args.args[0].arg == "self"
                decorators = [self._name(d) for d in node.decorator_list]
                calls = []
                for child in ast.walk(node):
                    if isinstance(child, ast.Call):
                        name = self._name(child.func)
                        if name and name not in calls:
                            calls.append(name)
                result.functions.append(FunctionSymbol(
                    name=node.name,
                    args=args,
                    is_async=isinstance(node, ast.AsyncFunctionDef),
                    is_method=is_method,
                    decorators=decorators,
                    calls=sorted(calls),
                    line=node.lineno,
                ))
                if node.name in ("main", "__main__"):
                    result.entry_points.append(node.name)

            # Imports
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    result.imports.append(ImportSymbol(
                        module=alias.name,
                        names=[alias.asname or alias.name],
                        alias=alias.asname,
                        is_relative=False,
                        level=0,
                        line=node.lineno,
                    ))

            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                names = [alias.name for alias in node.names]
                result.imports.append(ImportSymbol(
                    module=module,
                    names=names,
                    alias=None,
                    is_relative=(node.level or 0) > 0,
                    level=node.level or 0,
                    line=node.lineno,
                ))

            # Module-level constants (ALL_CAPS or simple assigned literals)
            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        name = target.id
                        if name.isupper() or name not in module_globals:
                            value_type = self._value_type(node.value)
                            result.constants.append(ConstantSymbol(
                                name=name,
                                value_type=value_type,
                                line=node.lineno,
                            ))
                        module_globals.add(name)

        # Detect `if __name__ == "__main__":` pattern
        for node in ast.walk(tree):
            if isinstance(node, ast.If):
                test = node.test
                if (
                    isinstance(test, ast.Compare)
                    and isinstance(test.left, ast.Name)
                    and test.left.id == "__name__"
                ):
                    if "__main__" not in result.entry_points:
                        result.entry_points.append("__main__")

        return result

    def _name(self, node) -> str:
        """Extract a dotted name from an AST node."""
        if isinstance(node, ast.Name):
            return node.id
        if isinstance(node, ast.Attribute):
            prefix = self._name(node.value)
            return "%s.%s" % (prefix, node.attr) if prefix else node.attr
        if isinstance(node, ast.Subscript):
            return self._name(node.value)
        return ""

    def _value_type(self, node) -> str:
        if isinstance(node, ast.Constant):
            return type(node.value).__name__
        if isinstance(node, ast.Dict):
            return "dict"
        if isinstance(node, (ast.List, ast.Tuple, ast.Set)):
            return "list"
        if isinstance(node, ast.Call):
            return "call"
        return "other"


# ---------------------------------------------------------------------------
# TypeScript / JavaScript analyzer (regex-based)
# ---------------------------------------------------------------------------

_TS_CLASS_RE = re.compile(
    r"^(?:export\s+)?(?:abstract\s+)?class\s+(\w+)(?:\s+extends\s+([\w<>, ]+))?",
    re.MULTILINE,
)
_TS_FUNC_RE = re.compile(
    r"^(?:export\s+)?(?:async\s+)?function\s+(\w+)\s*\(",
    re.MULTILINE,
)
_TS_ARROW_RE = re.compile(
    r"^(?:export\s+)?(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s+)?\(",
    re.MULTILINE,
)
_TS_IMPORT_RE = re.compile(
    r"""^import\s+(?:{[^}]+}|[\w*]+(?:\s*,\s*{[^}]+})?|\*\s+as\s+\w+)\s+from\s+['"]([^'"]+)['"]""",
    re.MULTILINE,
)
_TS_REQUIRE_RE = re.compile(
    r"""require\s*\(\s*['"]([^'"]+)['"]\s*\)""",
    re.MULTILINE,
)
_TS_CONST_RE = re.compile(
    r"^(?:export\s+)?const\s+([A-Z_][A-Z0-9_]*)\s*=",
    re.MULTILINE,
)


class TypeScriptAnalyzer(LanguageAnalyzer):
    """Regex-based analyzer for TypeScript and JavaScript files."""

    EXTENSIONS = [".ts", ".tsx", ".js", ".jsx", ".mjs"]

    def analyze(self, path: str, text: str) -> FileAnalysis:
        lang = "typescript" if path.endswith((".ts", ".tsx")) else "javascript"
        result = FileAnalysis(path=path, language=lang)
        lines = text.splitlines()

        for m in _TS_CLASS_RE.finditer(text):
            bases = [b.strip() for b in (m.group(2) or "").split(",")] if m.group(2) else []
            is_abstract = "abstract class" in text[max(0, m.start() - 10):m.start() + len(m.group(0))]
            line = text[:m.start()].count("\n") + 1
            result.classes.append(ClassSymbol(
                name=m.group(1),
                bases=[b for b in bases if b],
                methods=[],
                is_abstract=is_abstract,
                decorators=[],
                line=line,
            ))

        for m in _TS_FUNC_RE.finditer(text):
            is_async = "async" in text[max(0, m.start() - 6):m.start() + len(m.group(0))]
            line = text[:m.start()].count("\n") + 1
            result.functions.append(FunctionSymbol(
                name=m.group(1),
                args=[],
                is_async=is_async,
                is_method=False,
                decorators=[],
                calls=[],
                line=line,
            ))
            if m.group(1) == "main":
                result.entry_points.append("main")

        for m in _TS_ARROW_RE.finditer(text):
            line = text[:m.start()].count("\n") + 1
            result.functions.append(FunctionSymbol(
                name=m.group(1),
                args=[],
                is_async=False,
                is_method=False,
                decorators=[],
                calls=[],
                line=line,
            ))

        for m in _TS_IMPORT_RE.finditer(text):
            line = text[:m.start()].count("\n") + 1
            result.imports.append(ImportSymbol(
                module=m.group(1),
                names=[],
                alias=None,
                is_relative=m.group(1).startswith("."),
                level=0,
                line=line,
            ))

        for m in _TS_REQUIRE_RE.finditer(text):
            line = text[:m.start()].count("\n") + 1
            result.imports.append(ImportSymbol(
                module=m.group(1),
                names=[],
                alias=None,
                is_relative=m.group(1).startswith("."),
                level=0,
                line=line,
            ))

        for m in _TS_CONST_RE.finditer(text):
            line = text[:m.start()].count("\n") + 1
            result.constants.append(ConstantSymbol(
                name=m.group(1),
                value_type="other",
                line=line,
            ))

        return result


# ---------------------------------------------------------------------------
# JSON analyzer
# ---------------------------------------------------------------------------

class JSONAnalyzer(LanguageAnalyzer):
    """Structural analyzer for JSON files."""

    EXTENSIONS = [".json"]

    def analyze(self, path: str, text: str) -> FileAnalysis:
        result = FileAnalysis(path=path, language="json")
        try:
            data = json.loads(text)
        except (json.JSONDecodeError, ValueError) as exc:
            result.error = "JSONDecodeError: %s" % exc
            return result

        if isinstance(data, dict):
            for key in sorted(data.keys()):
                value = data[key]
                vtype = (
                    "dict" if isinstance(value, dict)
                    else "list" if isinstance(value, list)
                    else type(value).__name__
                )
                result.constants.append(ConstantSymbol(name=key, value_type=vtype, line=0))

            # Detect package.json dependencies
            if "dependencies" in data or "devDependencies" in data:
                for dep_key in ("dependencies", "devDependencies"):
                    deps = data.get(dep_key, {})
                    if isinstance(deps, dict):
                        for name in sorted(deps.keys()):
                            result.imports.append(ImportSymbol(
                                module=name,
                                names=[],
                                alias=None,
                                is_relative=False,
                                level=0,
                                line=0,
                            ))

        return result


# ---------------------------------------------------------------------------
# YAML analyzer
# ---------------------------------------------------------------------------

_YAML_KEY_RE = re.compile(r"^(\s*)([A-Za-z_][\w-]*):\s*", re.MULTILINE)


class YAMLAnalyzer(LanguageAnalyzer):
    """Structural analyzer for YAML files."""

    EXTENSIONS = [".yaml", ".yml"]

    def analyze(self, path: str, text: str) -> FileAnalysis:
        result = FileAnalysis(path=path, language="yaml")
        # Collect top-level keys (no leading indentation)
        seen = set()
        for m in _YAML_KEY_RE.finditer(text):
            indent = len(m.group(1))
            if indent == 0:
                key = m.group(2)
                if key not in seen:
                    seen.add(key)
                    line = text[:m.start()].count("\n") + 1
                    result.constants.append(ConstantSymbol(name=key, value_type="yaml_key", line=line))
        return result


# ---------------------------------------------------------------------------
# Markdown analyzer
# ---------------------------------------------------------------------------

_MD_HEADING_RE = re.compile(r"^(#{1,6})\s+(.+)$", re.MULTILINE)
_MD_CODE_FENCE_RE = re.compile(r"^```(\w+)?", re.MULTILINE)


class MarkdownAnalyzer(LanguageAnalyzer):
    """Structural analyzer for Markdown files."""

    EXTENSIONS = [".md", ".markdown"]

    def analyze(self, path: str, text: str) -> FileAnalysis:
        result = FileAnalysis(path=path, language="markdown")
        for m in _MD_HEADING_RE.finditer(text):
            level = len(m.group(1))
            title = m.group(2).strip()
            line = text[:m.start()].count("\n") + 1
            result.constants.append(ConstantSymbol(
                name="h%d:%s" % (level, title[:80]),
                value_type="heading",
                line=line,
            ))
        return result


# ---------------------------------------------------------------------------
# ASTAnalyzer — main entry point
# ---------------------------------------------------------------------------

# Maximum file size to analyse (bytes) — avoids OOM on giant generated files
_MAX_FILE_SIZE = 512_000

# Ordered list of language analyzers — first match wins
_LANGUAGE_ANALYZERS: List[LanguageAnalyzer] = [
    PythonAnalyzer(),
    TypeScriptAnalyzer(),
    JSONAnalyzer(),
    YAMLAnalyzer(),
    MarkdownAnalyzer(),
]


class ASTAnalyzer:
    """
    Multi-language AST analyzer.

    Extracts semantic symbols from all supported source files in the workspace.
    Designed for extensibility — new languages can be registered via
    ``ASTAnalyzer.register_analyzer()``.
    """

    # Class-level analyzer registry allows future language plugins
    _analyzers: List[LanguageAnalyzer] = list(_LANGUAGE_ANALYZERS)

    @classmethod
    def register_analyzer(cls, analyzer: LanguageAnalyzer) -> None:
        """Register a new language analyzer plugin."""
        cls._analyzers.insert(0, analyzer)

    def __init__(self, root, workspace_index=None):
        self.root = Path(root).resolve()
        self._workspace_index = workspace_index

    def _get_index(self):
        if self._workspace_index is not None:
            return self._workspace_index
        from python.workspace_index import WorkspaceIndexBuilder
        return WorkspaceIndexBuilder(self.root).build()

    def analyze(self) -> Dict[str, FileAnalysis]:
        """
        Analyze all supported files in the workspace.

        Returns a dict mapping relative file path → FileAnalysis, sorted by path.
        """
        index = self._get_index()
        results: Dict[str, FileAnalysis] = {}

        for wf in sorted(index.files, key=lambda f: f.path):
            if wf.size > _MAX_FILE_SIZE:
                continue
            ext = wf.extension.lower()
            analyzer = self._find_analyzer(ext)
            if analyzer is None:
                continue
            abs_path = Path(self.root) / wf.path
            try:
                text = abs_path.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            file_analysis = analyzer.analyze(wf.path, text)
            results[wf.path] = file_analysis

        return results

    def _find_analyzer(self, extension: str) -> Optional[LanguageAnalyzer]:
        for analyzer in self._analyzers:
            if analyzer.can_handle(extension):
                return analyzer
        return None

"""
Semantic Repository Intelligence — Injection Point Analyzer
CORE-008B

Detects injection and extension points in source code:

  - Decorator-based extension hooks
  - Abstract base classes / plugin interfaces
  - Dependency injection containers
  - Middleware chains
  - Event buses and signal dispatchers
  - Service boundaries
  - Hook registration patterns
"""

import re
from pathlib import Path
from typing import Dict, List

from .models import FileAnalysis, InjectionPoint


# ---------------------------------------------------------------------------
# Pattern definitions
# ---------------------------------------------------------------------------

# Each pattern is (type, name_template, regex, confidence_base)
_PYTHON_PATTERNS: List[tuple] = [
    # Decorators that register handlers
    ("decorator", "Message Handler Hook",
     re.compile(r"@(?:dp|router)\.(?:message|callback_query|inline_query|chosen_inline|poll)\b"),
     0.90),
    ("decorator", "CLI Command Hook",
     re.compile(r"@(?:app|cli|group|sub)\.command\b"),
     0.85),
    ("decorator", "Route Handler Hook",
     re.compile(r"@(?:app|bp|router)\.(?:route|get|post|put|delete|patch)\b"),
     0.85),
    ("decorator", "Scheduled Task Hook",
     re.compile(r"@(?:scheduler|cron|task|periodic)\b"),
     0.80),
    ("decorator", "Event Listener Hook",
     re.compile(r"@(?:event|on_event|listen|signal|receiver)\b"),
     0.80),

    # Plugin / abstract interfaces
    ("plugin_interface", "Abstract Plugin Interface",
     re.compile(r"class\s+\w+\s*\([^)]*(?:ABC|ABCMeta|Abstract\w+)[^)]*\)"),
     0.90),
    ("plugin_interface", "Protocol Interface",
     re.compile(r"class\s+\w+\s*\([^)]*Protocol[^)]*\)"),
     0.85),

    # Dependency injection
    ("di_container", "Dependency Injection Container",
     re.compile(r"(?:inject|container|provide|singleton|factory)\s*[=(]"),
     0.70),
    ("di_container", "Service Registry",
     re.compile(r"(?:register|register_service|ServiceRegistry|ServiceLocator)\s*\("),
     0.80),

    # Middleware chains
    ("middleware", "Middleware Registration",
     re.compile(r"(?:app|dp|router|bot)\.(?:middleware|use|add_middleware)\s*\("),
     0.85),
    ("middleware", "ASGI/WSGI Middleware",
     re.compile(r"class\s+\w+Middleware\b"),
     0.80),

    # Event buses
    ("event_bus", "Event Bus",
     re.compile(r"(?:EventBus|event_bus|emit\b|publish\b|subscribe\b|on_event\b)"),
     0.75),
    ("event_bus", "Signal Dispatcher",
     re.compile(r"(?:Signal|dispatch|send_signal|fire_event)\s*\("),
     0.70),

    # Hooks
    ("hook", "Lifecycle Hook",
     re.compile(r"(?:on_startup|on_shutdown|on_ready|before_start|after_stop|on_restart)\s*\("),
     0.85),
    ("hook", "Plugin Hook Registration",
     re.compile(r"(?:register_hook|add_hook|hook_into|install_plugin)\s*\("),
     0.80),

    # Service boundaries
    ("service_boundary", "Service Entry Point",
     re.compile(r"(?:class\s+\w+Service\b|class\s+\w+Client\b|class\s+\w+Repository\b)"),
     0.80),
    ("service_boundary", "API Gateway Pattern",
     re.compile(r"(?:class\s+\w+Gateway\b|class\s+\w+Adapter\b|class\s+\w+Proxy\b)"),
     0.75),
]

# TypeScript / JavaScript patterns
_TS_PATTERNS: List[tuple] = [
    ("decorator", "TS Decorator Hook",
     re.compile(r"@(?:Injectable|Component|Pipe|Guard|Interceptor|Controller)\b"),
     0.90),
    ("middleware", "Express Middleware",
     re.compile(r"app\.use\s*\("),
     0.80),
    ("event_bus", "EventEmitter",
     re.compile(r"(?:EventEmitter|\.emit\s*\(|\.on\s*\(|\.once\s*\()"),
     0.70),
    ("di_container", "DI Container (TS)",
     re.compile(r"(?:Container\.get|inject\(|provide\()"),
     0.75),
]


class InjectionPointAnalyzer:
    """
    Analyzes source files to detect injection and extension points.
    """

    def analyze(
        self,
        file_analyses: Dict[str, FileAnalysis],
        root: Path,
    ) -> List[InjectionPoint]:
        """
        Scan all files for injection / extension point patterns.

        Returns a sorted, deduplicated list of InjectionPoint objects.
        """
        results: List[InjectionPoint] = []

        for path, analysis in sorted(file_analyses.items()):
            abs_path = root / path
            try:
                text = abs_path.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue

            if analysis.language == "python":
                patterns = _PYTHON_PATTERNS
            elif analysis.language in ("typescript", "javascript"):
                patterns = _TS_PATTERNS
            else:
                continue

            results.extend(self._scan(path, text, patterns, analysis))

        # Also detect injection points from AST-level class/decorator info
        results.extend(self._ast_injection_points(file_analyses))

        # Sort and deduplicate by (file, name, line)
        seen = set()
        deduped: List[InjectionPoint] = []
        for ip in sorted(results, key=lambda x: (x.file, x.name, x.line)):
            key = (ip.file, ip.name, ip.line)
            if key not in seen:
                seen.add(key)
                deduped.append(ip)

        return deduped

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _scan(
        self,
        path: str,
        text: str,
        patterns: List[tuple],
        analysis: FileAnalysis,
    ) -> List[InjectionPoint]:
        results = []
        lines = text.splitlines()
        for ip_type, name, regex, confidence in patterns:
            for m in regex.finditer(text):
                line_no = text[:m.start()].count("\n") + 1
                snippet = lines[line_no - 1].strip()[:120] if line_no <= len(lines) else ""
                results.append(InjectionPoint(
                    name=name,
                    type=ip_type,
                    file=path,
                    line=line_no,
                    pattern=regex.pattern[:80],
                    confidence=confidence,
                    evidence=[snippet],
                ))
        return results

    def _ast_injection_points(
        self, file_analyses: Dict[str, FileAnalysis]
    ) -> List[InjectionPoint]:
        """Derive injection points from the already-parsed AST data."""
        results = []
        for path, analysis in sorted(file_analyses.items()):
            # Abstract base classes are plugin interfaces
            for cls in analysis.classes:
                if cls.is_abstract:
                    results.append(InjectionPoint(
                        name=cls.name,
                        type="plugin_interface",
                        file=path,
                        line=cls.line,
                        pattern="abstract class",
                        confidence=0.90,
                        evidence=["Class %s is abstract (bases: %s)" % (
                            cls.name, ", ".join(cls.bases[:3]) or "ABC"
                        )],
                    ))
            # Decorated functions are hook candidates
            for func in analysis.functions:
                for decorator in func.decorators:
                    if any(kw in decorator.lower() for kw in (
                        "route", "command", "handler", "listener", "hook",
                        "middleware", "event", "task", "schedule",
                    )):
                        results.append(InjectionPoint(
                            name="%s.%s" % (decorator, func.name),
                            type="decorator",
                            file=path,
                            line=func.line,
                            pattern="@%s" % decorator,
                            confidence=0.80,
                            evidence=["@%s on %s" % (decorator, func.name)],
                        ))
        return results

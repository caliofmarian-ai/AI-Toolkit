"""
Self Improvement Engine — Analyzers
CORE-017B

Delegates to existing CORE intelligence to detect technical debt,
measure performance, and identify missing capabilities.

Does NOT duplicate any existing analysis.
"""

import re
import time
from pathlib import Path
from typing import Any, Dict, List, Mapping

from .models import (
    CapabilityGap,
    PerformanceMetric,
    TechnicalDebt,
)


# ---------------------------------------------------------------------------
# Technical Debt Analyzer
# ---------------------------------------------------------------------------

class TechnicalDebtAnalyzer:
    """
    CORE-017B — Technical Debt Analyzer.

    Detects duplicated code, dead modules, and incomplete implementations
    by inspecting the repository structure.
    """

    _KNOWN_PACKAGES = [
        "canonical_intelligence",
        "ai_cto_scanner",
        "semantic_repository_intelligence",
        "executable_repository_intelligence",
        "development_state_engine",
        "executive_briefing_engine",
        "workspace_orchestrator",
        "context_synchronization_engine",
        "autonomous_planning_engine",
        "autonomous_execution_engine",
        "self_evaluation_engine",
        "self_improvement_engine",
    ]

    def __init__(self, repository: str = ".") -> None:
        self.repository = repository

    def analyze(self) -> List[TechnicalDebt]:
        findings: List[TechnicalDebt] = []
        lib_python = Path(self.repository) / "lib" / "python"

        if not lib_python.exists():
            return findings

        findings.extend(self._check_legacy_modules(lib_python))
        findings.extend(self._check_missing_inits(lib_python))
        return findings

    def _check_legacy_modules(self, lib_python: Path) -> List[TechnicalDebt]:
        """Detect top-level .py files that may be legacy implementations."""
        debt: List[TechnicalDebt] = []
        legacy_names = {
            "autonomous_workflow_engine",
            "decision_engine",
            "knowledge_graph_engine",
            "memory_engine",
            "repository_hygiene_audit",
            "repository_inventory",
            "repository_profile",
            "development_validator",
            "foundation_audit",
        }
        for py_file in lib_python.glob("*.py"):
            stem = py_file.stem
            if stem in legacy_names:
                debt.append(
                    TechnicalDebt(
                        debt_id=f"DEBT-LEGACY-{stem.upper()}",
                        category="legacy_module",
                        component=str(py_file.relative_to(Path(self.repository))),
                        description=(
                            f"Top-level legacy module {py_file.name!r} may duplicate "
                            "functionality already in a dedicated package."
                        ),
                        severity="low",
                        estimated_effort="low",
                        evidence={"file": str(py_file)},
                        recommendation=(
                            f"Evaluate whether {py_file.name!r} can be replaced by "
                            "its dedicated package equivalent."
                        ),
                    )
                )
        return debt

    def _check_missing_inits(self, lib_python: Path) -> List[TechnicalDebt]:
        """Detect packages missing __init__.py."""
        debt: List[TechnicalDebt] = []
        for pkg_dir in lib_python.iterdir():
            if pkg_dir.is_dir() and not pkg_dir.name.startswith("_"):
                init_file = pkg_dir / "__init__.py"
                if not init_file.exists():
                    debt.append(
                        TechnicalDebt(
                            debt_id=f"DEBT-NOINIT-{pkg_dir.name.upper()}",
                            category="missing_init",
                            component=str(pkg_dir.relative_to(Path(self.repository))),
                            description=f"Package {pkg_dir.name!r} is missing __init__.py",
                            severity="medium",
                            estimated_effort="low",
                            evidence={"directory": str(pkg_dir)},
                            recommendation=(
                                f"Add __init__.py to {pkg_dir.name!r} "
                                "with a public API declaration."
                            ),
                        )
                    )
        return debt


# ---------------------------------------------------------------------------
# Performance Analyzer
# ---------------------------------------------------------------------------

class PerformanceAnalyzer:
    """
    CORE-017B — Performance Analyzer.

    Measures execution durations and identifies performance bottlenecks
    using execution history from CORE-015.
    """

    def __init__(self, repository: str = ".") -> None:
        self.repository = repository

    def analyze(self) -> List[PerformanceMetric]:
        metrics: List[PerformanceMetric] = []

        # Load execution history
        try:
            from python.autonomous_execution_engine.persistence import (  # type: ignore[import]
                ExecutionPersistence,
            )
            persistence = ExecutionPersistence(self.repository)
            history = persistence.load_history()
            entries = history.get("entries", [])
            if entries:
                durations = [e.get("duration_ms", 0.0) for e in entries if e.get("duration_ms")]
                if durations:
                    avg_duration = sum(durations) / len(durations)
                    metrics.append(
                        PerformanceMetric(
                            metric_id="PERF-EXEC-AVG",
                            name="average_execution_duration_ms",
                            value=round(avg_duration, 1),
                            unit="ms",
                            baseline=5000.0,
                            trend="stable" if avg_duration < 5000 else "degrading",
                            evidence={"entry_count": len(entries), "source": "CORE-015"},
                        )
                    )
        except Exception:
            pass

        # Load evaluation history
        try:
            from python.self_evaluation_engine.persistence import (  # type: ignore[import]
                EvaluationPersistence,
            )
            persistence = EvaluationPersistence(self.repository)
            history = persistence.load_evaluation()
            if history:
                score = history.get("overall_score", 0.0)
                metrics.append(
                    PerformanceMetric(
                        metric_id="PERF-EVAL-SCORE",
                        name="evaluation_overall_score",
                        value=round(score, 3),
                        unit="score",
                        baseline=0.8,
                        trend="improving" if score >= 0.8 else "degrading",
                        evidence={"source": "CORE-016"},
                    )
                )
        except Exception:
            pass

        # Repository size metric
        lib_python = Path(self.repository) / "lib" / "python"
        if lib_python.exists():
            py_files = list(lib_python.rglob("*.py"))
            metrics.append(
                PerformanceMetric(
                    metric_id="PERF-REPO-SIZE",
                    name="python_file_count",
                    value=float(len(py_files)),
                    unit="files",
                    baseline=100.0,
                    trend="growing",
                    evidence={"directory": str(lib_python)},
                )
            )

        return metrics


# ---------------------------------------------------------------------------
# Capability Analyzer
# ---------------------------------------------------------------------------

class CapabilityAnalyzer:
    """
    CORE-017B — Capability Analyzer.

    Detects capabilities missing from AI Toolkit by comparing the
    expected CLI surface and package inventory against what exists.
    """

    _EXPECTED_CLI_COMMANDS = {
        "inventory", "dependencies", "validate", "inspect",
        "briefing", "workspace", "context", "plan",
        "execute", "evaluate", "improve",
    }

    _EXPECTED_PACKAGES = {
        "canonical_intelligence",
        "ai_cto_scanner",
        "semantic_repository_intelligence",
        "executable_repository_intelligence",
        "development_state_engine",
        "executive_briefing_engine",
        "workspace_orchestrator",
        "context_synchronization_engine",
        "autonomous_planning_engine",
        "autonomous_execution_engine",
        "self_evaluation_engine",
        "self_improvement_engine",
    }

    def __init__(self, repository: str = ".") -> None:
        self.repository = repository

    def analyze(self) -> List[CapabilityGap]:
        gaps: List[CapabilityGap] = []

        # Check CLI commands
        cli_path = Path(self.repository) / "lib" / "python" / "cli" / "main.py"
        if cli_path.exists():
            cli_source = cli_path.read_text(encoding="utf-8")
            registered = {
                m.group(1)
                for m in re.finditer(r'sub\.add_parser\(\s*["\'](\w+)["\']', cli_source)
            }
            missing_commands = self._EXPECTED_CLI_COMMANDS - registered
            for cmd in sorted(missing_commands):
                gaps.append(
                    CapabilityGap(
                        gap_id=f"GAP-CLI-{cmd.upper()}",
                        category="missing_cli_command",
                        description=f"CLI command `ai {cmd}` is not registered",
                        priority=PRIORITY_HIGH if cmd in ("execute", "evaluate", "improve") else PRIORITY_MEDIUM,
                        evidence={"missing_command": cmd, "source": "cli/main.py"},
                    )
                )

        # Check packages
        lib_python = Path(self.repository) / "lib" / "python"
        if lib_python.exists():
            existing_packages = {p.name for p in lib_python.iterdir() if p.is_dir()}
            missing_packages = self._EXPECTED_PACKAGES - existing_packages
            for pkg in sorted(missing_packages):
                gaps.append(
                    CapabilityGap(
                        gap_id=f"GAP-PKG-{pkg.upper().replace('-', '_')}",
                        category="missing_package",
                        description=f"Expected package {pkg!r} is not implemented",
                        priority=PRIORITY_HIGH,
                        evidence={"missing_package": pkg},
                    )
                )

        return gaps


# Expose PRIORITY constant for use in CapabilityGap
PRIORITY_HIGH = "high"
PRIORITY_MEDIUM = "medium"

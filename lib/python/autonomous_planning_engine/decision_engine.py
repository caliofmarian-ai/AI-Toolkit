"""
Autonomous Planning Engine — Planning Decision Engine
CORE-014D

Derives current planning context from existing CORE engine intelligence:

  - Current repository maturity   (from CanonicalIntelligence + Semantic)
  - Current development phase     (from implemented CORE count)
  - Completed COREs               (from lib/python directory scan + imports)
  - Incomplete COREs              (from documentation + CORE roadmap)
  - Blocked work                  (from DevelopmentStateEngine blocked_tasks)
  - Highest-priority task         (from ExecutiveBriefingEngine priorities)
  - Next CORE                     (lowest CORE number not yet implemented)

No decisions are hardcoded — everything is derived from live intelligence.
"""

import re
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Set, Tuple

from .models import (
    MATURITY_ADVANCED,
    MATURITY_DEVELOPING,
    MATURITY_EARLY,
    MATURITY_MATURE,
    PHASE_AUTONOMY,
    PHASE_FOUNDATION,
    PHASE_INTELLIGENCE,
    PHASE_PRODUCTION,
)

_CORE_RE = re.compile(r"\bCORE-(\d{3}[A-Z]?)\b")
_EMPTY = frozenset({"", "UNSPECIFIED", "None", "null", "N/A"})


def _is_set(value: Any) -> bool:
    return bool(value) and str(value).strip() not in _EMPTY


def _core_sort_key(core_id: str) -> Tuple[int, str]:
    """Sort key for CORE IDs: numeric part first, then suffix."""
    m = re.match(r"CORE-(\d+)([A-Z]?)", core_id)
    if m:
        return (int(m.group(1)), m.group(2))
    return (9999, core_id)


class CoreRegistry:
    """
    Detects implemented and documented COREs from the repository.

    Implemented COREs: engine package directories that contain a CORE-xxx
    reference in at least one source file.

    Documented COREs: any CORE-xxx mentioned in docs/, development/,
    or the README.
    """

    def __init__(self, repository_root: Path) -> None:
        self.root = repository_root
        self._lib_python = repository_root / "lib" / "python"

    def implemented(self) -> List[str]:
        """Return sorted list of CORE IDs with a corresponding engine package."""
        cores: Set[str] = set()
        if not self._lib_python.is_dir():
            return []
        for package_dir in self._lib_python.iterdir():
            if not package_dir.is_dir():
                continue
            if not (package_dir / "__init__.py").exists():
                continue
            for py_file in package_dir.glob("*.py"):
                try:
                    head = py_file.read_text(encoding="utf-8", errors="replace")[:3000]
                except OSError:
                    continue
                for m in _CORE_RE.finditer(head):
                    core_id = f"CORE-{m.group(1)}"
                    # Only register if the numeric part is <= 3 digits to avoid
                    # false positives from things like CORE-001-DRAFT
                    if re.fullmatch(r"CORE-\d{3}[A-Z]?", core_id):
                        cores.add(core_id.split("-")[0] + "-" + m.group(1).rstrip("ABCDEFGHIJKLMNOPQRSTUVWXYZ").lstrip("0") or "0")
                        # Recompute properly
                        numeric = m.group(1)
                        cores.add(f"CORE-{numeric}")
        # Return base CORE IDs only (strip sub-letters like CORE-008A → CORE-008)
        base: Set[str] = set()
        for c in cores:
            m = re.fullmatch(r"CORE-(\d+)([A-Z]?)", c)
            if m:
                base.add(f"CORE-{m.group(1).zfill(3)}")
        return sorted(base, key=_core_sort_key)

    def documented(self) -> List[str]:
        """
        Return sorted list of all CORE IDs mentioned in any documentation
        or batch file in the repository (docs/, development/, README*).
        """
        cores: Set[str] = set()
        search_dirs = [
            self.root / "docs",
            self.root / "development",
        ]
        search_files = list(self.root.glob("README*"))

        for d in search_dirs:
            if d.is_dir():
                for f in d.rglob("*"):
                    if f.is_file():
                        try:
                            content = f.read_text(encoding="utf-8", errors="replace")
                        except OSError:
                            continue
                        for m in _CORE_RE.finditer(content):
                            cores.add(f"CORE-{m.group(1)}")

        for f in search_files:
            try:
                content = f.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            for m in _CORE_RE.finditer(content):
                cores.add(f"CORE-{m.group(1)}")

        base: Set[str] = set()
        for c in cores:
            m = re.fullmatch(r"CORE-(\d+)([A-Z]?)", c)
            if m:
                base.add(f"CORE-{m.group(1).zfill(3)}")
        return sorted(base, key=_core_sort_key)


class PlanningDecisionEngine:
    """
    CORE-014D — Planning Decision Engine.

    Derives the complete planning context from existing intelligence.
    The result is a fully serialisable dict suitable for downstream
    planners and the report generator.
    """

    def __init__(self, repository_root: str = ".") -> None:
        self.root = Path(repository_root).resolve()
        self._registry = CoreRegistry(self.root)

    def decide(
        self,
        snapshot: Mapping[str, Any],
        briefing: Mapping[str, Any],
    ) -> Dict[str, Any]:
        """
        Derive the full planning decision context.

        Parameters
        ----------
        snapshot:
            DevelopmentStateManager.GenerateExecutiveSnapshot output.
        briefing:
            ExecutiveBriefingEngine.generate()['briefing_dict'] or {}.
        """
        implemented = self._registry.implemented()
        documented = self._registry.documented()
        # All known COREs = union of implemented and documented.
        # This ensures incomplete is always a meaningful set: COREs documented
        # but not yet implemented.  If documented ⊂ implemented, incomplete = [].
        all_known = sorted(set(implemented) | set(documented), key=_core_sort_key)
        incomplete = [c for c in all_known if c not in set(implemented)]
        blocked = self._blocked_cores(snapshot)
        next_core = self._next_core(implemented, all_known, blocked)

        phase = self._compute_phase(implemented)
        maturity = self._compute_maturity(snapshot, implemented)

        return {
            "implemented_cores": implemented,
            "documented_cores": list(all_known),
            "incomplete_cores": incomplete,
            "blocked_cores": blocked,
            "next_core": next_core,
            "current_phase": phase,
            "repository_maturity": maturity,
            "completion_percentage": self._completion_pct(implemented, all_known),
            "highest_priority_task": self._highest_priority(snapshot, briefing),
            "blocked_tasks": self._blocked_tasks(snapshot),
            "current_milestone": self._current_milestone(snapshot),
            "current_batch": self._current_batch(snapshot),
            "current_branch": self._current_branch(snapshot),
            "suggested_next_batch": self._suggested_next_batch(briefing, snapshot),
            "suggested_next_pr": self._suggested_next_pr(briefing),
            "repository_health": self._repository_health(snapshot),
            "canonical_coverage": self._canonical_coverage(snapshot),
        }

    # ------------------------------------------------------------------
    # Derived fields
    # ------------------------------------------------------------------

    def _next_core(
        self,
        implemented: List[str],
        documented: List[str],
        blocked: List[str],
    ) -> Optional[str]:
        """Return the lowest-numbered undone, unblocked documented CORE."""
        impl_set = set(implemented)
        blocked_set = set(blocked)
        for core in sorted(documented, key=_core_sort_key):
            if core not in impl_set and core not in blocked_set:
                return core
        return None

    def _compute_phase(self, implemented: List[str]) -> str:
        n = len(implemented)
        if n >= 14:
            return PHASE_PRODUCTION
        if n >= 10:
            return PHASE_AUTONOMY
        if n >= 5:
            return PHASE_INTELLIGENCE
        return PHASE_FOUNDATION

    def _compute_maturity(
        self, snapshot: Mapping[str, Any], implemented: List[str]
    ) -> str:
        integrations = snapshot.get("integrations", {})
        canonical = integrations.get("canonical_intelligence", {})
        coverage = float(canonical.get("average_coverage", 0.0))
        n = len(implemented)

        if n >= 12 and coverage >= 80:
            return MATURITY_ADVANCED
        if n >= 8 and coverage >= 60:
            return MATURITY_MATURE
        if n >= 4:
            return MATURITY_DEVELOPING
        return MATURITY_EARLY

    @staticmethod
    def _completion_pct(implemented: List[str], documented: List[str]) -> float:
        if not documented:
            return 0.0
        return round(len(implemented) / len(documented) * 100, 1)

    @staticmethod
    def _blocked_cores(snapshot: Mapping[str, Any]) -> List[str]:
        state = snapshot.get("state", {})
        blocked = state.get("workspace_state", {}).get("blocked_tasks", [])
        return [t for t in (blocked or []) if _CORE_RE.match(str(t))]

    @staticmethod
    def _blocked_tasks(snapshot: Mapping[str, Any]) -> List[str]:
        state = snapshot.get("state", {})
        return list(state.get("workspace_state", {}).get("blocked_tasks", []) or [])

    @staticmethod
    def _highest_priority(
        snapshot: Mapping[str, Any], briefing: Mapping[str, Any]
    ) -> str:
        # First check executive briefing priorities
        for item in briefing.get("priorities", []):
            p = item.get("priority", "")
            if p in ("critical", "high"):
                return str(item.get("title", ""))
        # Fallback: development state current task
        state = snapshot.get("state", {})
        return str(
            state.get("workspace_state", {}).get("current_task", "")
            or state.get("workspace_state", {}).get("current_batch", "")
        )

    @staticmethod
    def _current_milestone(snapshot: Mapping[str, Any]) -> str:
        state = snapshot.get("state", {})
        return str(
            state.get("workspace_state", {}).get("current_milestone", "") or ""
        )

    @staticmethod
    def _current_batch(snapshot: Mapping[str, Any]) -> str:
        state = snapshot.get("state", {})
        return str(
            state.get("workspace_state", {}).get("current_batch", "") or ""
        )

    @staticmethod
    def _current_branch(snapshot: Mapping[str, Any]) -> str:
        state = snapshot.get("state", {})
        return str(
            state.get("repository_state", {}).get("branch", "") or ""
        )

    @staticmethod
    def _suggested_next_batch(
        briefing: Mapping[str, Any], snapshot: Mapping[str, Any]
    ) -> str:
        val = briefing.get("suggested_next_batch", "")
        if _is_set(val):
            return str(val)
        state = snapshot.get("state", {})
        return str(
            state.get("planning_state", {}).get("recommended_batch", "") or ""
        )

    @staticmethod
    def _suggested_next_pr(briefing: Mapping[str, Any]) -> str:
        val = briefing.get("suggested_next_pr", "")
        return str(val) if _is_set(val) else ""

    @staticmethod
    def _repository_health(snapshot: Mapping[str, Any]) -> str:
        integrations = snapshot.get("integrations", {})
        scanner = integrations.get("ai_cto_scanner", {})
        return str(scanner.get("overall_health", "unknown") or "unknown")

    @staticmethod
    def _canonical_coverage(snapshot: Mapping[str, Any]) -> float:
        integrations = snapshot.get("integrations", {})
        canonical = integrations.get("canonical_intelligence", {})
        return float(canonical.get("average_coverage", 0.0) or 0.0)

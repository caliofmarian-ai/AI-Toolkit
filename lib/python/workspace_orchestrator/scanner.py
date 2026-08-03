"""
Workspace Orchestrator — Scanner
CORE-012

WorkspaceDiscoveryEngine: discovers git repositories in a workspace root.
WorkspaceScanner: scans each repository using existing CORE engines and
                  produces a WorkspaceRepository model.
"""

import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from python.ai_cto_scanner import AICTOScannerEngine

from .models import (
    HEALTH_CRITICAL,
    HEALTH_DEGRADED,
    HEALTH_HEALTHY,
    HEALTH_UNKNOWN,
    REPO_CATEGORY_AI,
    REPO_CATEGORY_BACKEND,
    REPO_CATEGORY_DOCUMENTATION,
    REPO_CATEGORY_FRONTEND,
    REPO_CATEGORY_INFRASTRUCTURE,
    REPO_CATEGORY_UNKNOWN,
    REPO_TYPE_LIBRARY,
    REPO_TYPE_PLATFORM,
    REPO_TYPE_SERVICE,
    REPO_TYPE_TOOL,
    REPO_TYPE_UNKNOWN,
    RISK_CRITICAL,
    RISK_HIGH,
    RISK_LOW,
    RISK_MEDIUM,
    STATUS_ACTIVE,
    STATUS_ANALYZED,
    STATUS_ARCHIVED,
    STATUS_BLOCKED,
    STATUS_COMPLIANT,
    STATUS_IDLE,
    STATUS_MISSING,
    STATUS_PARTIAL,
    STATUS_UNKNOWN,
    WorkspaceRepository,
)


class WorkspaceDiscoveryEngine:
    """
    Discovers git repositories under a workspace root directory.

    Supports:
    - Automatic discovery of git repos (walks up to two levels deep)
    - Manual registration via register()
    - Refresh of existing entries
    - Removal and relocation
    """

    def __init__(self, workspace_root: str = ".") -> None:
        self.workspace_root = Path(workspace_root).resolve()

    def discover(self) -> List[Dict[str, str]]:
        """
        Return a list of dicts with 'name' and 'path' for every git repository
        found directly under workspace_root (non-recursive, one level deep).
        """
        repos = []
        if not self.workspace_root.is_dir():
            return repos
        for item in sorted(self.workspace_root.iterdir()):
            if not item.is_dir():
                continue
            if (item / ".git").exists():
                repos.append({"name": item.name, "path": str(item)})
        return repos

    def discover_nested(self, max_depth: int = 2) -> List[Dict[str, str]]:
        """
        Recursively discover git repos up to *max_depth* levels deep.
        """
        repos = []
        self._walk(self.workspace_root, depth=0, max_depth=max_depth, results=repos)
        return repos

    def _walk(self, directory: Path, depth: int, max_depth: int, results: List) -> None:
        if depth > max_depth:
            return
        if (directory / ".git").exists():
            results.append({"name": directory.name, "path": str(directory)})
            return  # Do not recurse into git repos
        if depth < max_depth:
            try:
                for item in sorted(directory.iterdir()):
                    if item.is_dir() and not item.name.startswith("."):
                        self._walk(item, depth + 1, max_depth, results)
            except PermissionError:
                pass


class WorkspaceScanner:
    """
    Scans each discovered repository using AICTOScannerEngine (CORE-008A)
    and produces a populated WorkspaceRepository model.

    The scanner does NOT duplicate existing engine logic.  It delegates all
    analysis to AICTOScannerEngine and maps the results to the workspace model.
    """

    def __init__(self) -> None:
        self._now = datetime.now(timezone.utc).isoformat()

    def scan_repository(self, name: str, root: str) -> WorkspaceRepository:
        """
        Scan a single repository and return a WorkspaceRepository.

        Falls back to a skeleton repository model if scanning fails.
        """
        root_path = Path(root).resolve()

        # Gather git metadata independently (fast, no external engine)
        git_info = self._gather_git_info(root_path)

        # Run AI CTO Scanner (CORE-008A) — the canonical intelligence layer
        scan_data: Dict[str, Any] = {}
        scan_error: Optional[str] = None
        try:
            engine = AICTOScannerEngine(repository=str(root_path))
            scan_data = engine.scan()
        except Exception as exc:  # noqa: BLE001
            scan_error = str(exc)

        # Map scanner output to WorkspaceRepository
        return self._map_to_repository(
            name=name,
            root=str(root_path),
            git_info=git_info,
            scan_data=scan_data,
            scan_error=scan_error,
        )

    def _gather_git_info(self, root: Path) -> Dict[str, str]:
        """Collect lightweight git metadata without relying on external engines."""
        info: Dict[str, str] = {
            "current_branch": "",
            "default_branch": "main",
        }
        git_dir = root / ".git"
        if not git_dir.exists():
            return info

        # Current branch
        try:
            result = subprocess.run(
                ["git", "-C", str(root), "rev-parse", "--abbrev-ref", "HEAD"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if result.returncode == 0:
                info["current_branch"] = result.stdout.strip()
        except Exception:  # noqa: BLE001
            pass

        # Default branch (HEAD pointer from remote, or fall back to 'main')
        try:
            result = subprocess.run(
                ["git", "-C", str(root), "symbolic-ref", "refs/remotes/origin/HEAD"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if result.returncode == 0:
                ref = result.stdout.strip()
                if ref.startswith("refs/remotes/origin/"):
                    info["default_branch"] = ref.replace("refs/remotes/origin/", "")
        except Exception:  # noqa: BLE001
            pass

        return info

    def _map_to_repository(
        self,
        name: str,
        root: str,
        git_info: Dict[str, str],
        scan_data: Dict[str, Any],
        scan_error: Optional[str],
    ) -> WorkspaceRepository:
        """Map raw scanner output to a WorkspaceRepository model."""

        now = self._now

        if scan_error or not scan_data:
            # Minimal model when scanner fails
            return WorkspaceRepository(
                name=name,
                display_name=name,
                description="",
                repository_root=root,
                default_branch=git_info.get("default_branch", "main"),
                current_branch=git_info.get("current_branch", ""),
                repository_health=HEALTH_UNKNOWN,
                development_state=STATUS_UNKNOWN,
                last_scan=now,
            )

        scores = scan_data.get("scores", {})
        detection = scan_data.get("detection", {})
        canonical_stats = scan_data.get("canonical_stats", {})
        workspace_data = scan_data.get("workspace", {})

        overall_readiness = float(scores.get("Overall AI CTO Readiness", 0))

        # Repository health from overall readiness
        if overall_readiness >= 85:
            repo_health = HEALTH_HEALTHY
        elif overall_readiness >= 60:
            repo_health = HEALTH_DEGRADED
        else:
            repo_health = HEALTH_CRITICAL

        # Canonical status from compliance
        canonical_compliance = float(canonical_stats.get("overall_compliance", 0))
        drift_findings = int(canonical_stats.get("drift_findings", 0))
        if canonical_compliance >= 0.85 and drift_findings == 0:
            canonical_status = STATUS_COMPLIANT
        elif canonical_compliance >= 0.5 or drift_findings <= 5:
            canonical_status = STATUS_PARTIAL
        else:
            canonical_status = STATUS_MISSING

        # Semantic status
        semantic_score = float(scores.get("Development Readiness", 0))
        if semantic_score >= 80:
            semantic_status = STATUS_ANALYZED
        elif semantic_score >= 40:
            semantic_status = STATUS_PARTIAL
        else:
            semantic_status = STATUS_MISSING

        # Runtime status from Runtime Readiness score
        runtime_score = float(scores.get("Runtime Readiness", 0))
        if runtime_score >= 80:
            runtime_status = HEALTH_HEALTHY
        elif runtime_score >= 40:
            runtime_status = HEALTH_DEGRADED
        else:
            runtime_status = HEALTH_CRITICAL

        # Development status from current context
        development_status = STATUS_ACTIVE

        # Owner status from Owner Readiness
        owner_score = float(scores.get("Owner Readiness", 0))
        if owner_score >= 80:
            owner_status = STATUS_ACTIVE
        elif owner_score >= 40:
            owner_status = STATUS_IDLE
        else:
            owner_status = STATUS_BLOCKED

        # Risk status
        risk_status = self._derive_risk_status(scores, canonical_stats)

        # Priority (lower = more urgent)
        priority = self._derive_priority(repo_health, canonical_status, risk_status)

        # Repository type and category from workspace data
        repo_type = self._classify_type(scan_data, root)
        repo_category = self._classify_category(scan_data, root)

        # Development state
        dev_state = self._derive_dev_state(scores, detection)

        # Description from readme or canonical docs
        description = self._extract_description(root)

        return WorkspaceRepository(
            name=name,
            display_name=name,
            description=description,
            repository_root=root,
            repository_type=repo_type,
            repository_category=repo_category,
            default_branch=git_info.get("default_branch", "main"),
            current_branch=git_info.get("current_branch", ""),
            development_state=dev_state,
            repository_health=repo_health,
            readiness=overall_readiness,
            canonical_status=canonical_status,
            semantic_status=semantic_status,
            runtime_status=runtime_status,
            development_status=development_status,
            owner_status=owner_status,
            risk_status=risk_status,
            priority=priority,
            last_scan=now,
            scan_scores=dict(scores),
        )

    # ------------------------------------------------------------------
    # Classification helpers
    # ------------------------------------------------------------------

    def _derive_risk_status(
        self, scores: Dict[str, Any], canonical_stats: Dict[str, Any]
    ) -> str:
        overall = float(scores.get("Overall AI CTO Readiness", 0))
        drift = int(canonical_stats.get("drift_findings", 0))
        if overall < 40 or drift > 20:
            return RISK_CRITICAL
        if overall < 60 or drift > 10:
            return RISK_HIGH
        if overall < 80 or drift > 5:
            return RISK_MEDIUM
        return RISK_LOW

    def _derive_priority(
        self, health: str, canonical: str, risk: str
    ) -> int:
        """Return integer priority 1–9 (1 = most urgent)."""
        if risk == RISK_CRITICAL or health == HEALTH_CRITICAL:
            return 1
        if risk == RISK_HIGH or health == HEALTH_DEGRADED:
            return 2
        if canonical == STATUS_MISSING:
            return 3
        if canonical == STATUS_PARTIAL:
            return 4
        if risk == RISK_MEDIUM:
            return 5
        return 6

    def _classify_type(self, scan_data: Dict[str, Any], root: str) -> str:
        root_path = Path(root)
        name_lower = root_path.name.lower()
        # Heuristic based on directory name / detected components
        if "toolkit" in name_lower or "tool" in name_lower:
            return REPO_TYPE_TOOL
        if "platform" in name_lower:
            return REPO_TYPE_PLATFORM
        if "lib" in name_lower or "sdk" in name_lower:
            return REPO_TYPE_LIBRARY
        if "service" in name_lower or "api" in name_lower or "server" in name_lower:
            return REPO_TYPE_SERVICE
        return REPO_TYPE_UNKNOWN

    def _classify_category(self, scan_data: Dict[str, Any], root: str) -> str:
        root_path = Path(root)
        name_lower = root_path.name.lower()
        if "ai" in name_lower or "ml" in name_lower or "intelligence" in name_lower:
            return REPO_CATEGORY_AI
        if "docs" in name_lower or "documentation" in name_lower:
            return REPO_CATEGORY_DOCUMENTATION
        if "infra" in name_lower or "deploy" in name_lower or "k8s" in name_lower:
            return REPO_CATEGORY_INFRASTRUCTURE
        if "frontend" in name_lower or "ui" in name_lower or "web" in name_lower:
            return REPO_CATEGORY_FRONTEND
        if "backend" in name_lower or "api" in name_lower or "server" in name_lower:
            return REPO_CATEGORY_BACKEND
        # Check for Python / AI files
        py_files = list(root_path.rglob("*.py")) if root_path.exists() else []
        if len(py_files) > 20:
            return REPO_CATEGORY_AI
        return REPO_CATEGORY_UNKNOWN

    def _derive_dev_state(
        self, scores: Dict[str, Any], detection: Dict[str, Any]
    ) -> str:
        state_det = detection.get("State", {})
        state_comps = state_det.get("detected_components", []) if isinstance(state_det, dict) else []
        if any("blocked" in str(c).lower() for c in state_comps):
            return STATUS_BLOCKED
        owner_score = float(scores.get("Owner Readiness", 0))
        if owner_score >= 80:
            return STATUS_ACTIVE
        if owner_score >= 40:
            return STATUS_IDLE
        overall = float(scores.get("Overall AI CTO Readiness", 0))
        if overall < 30:
            return STATUS_ARCHIVED
        return STATUS_ACTIVE

    def _extract_description(self, root: str) -> str:
        """Try to extract a one-line description from README.md."""
        root_path = Path(root)
        readme = root_path / "README.md"
        if not readme.exists():
            return ""
        try:
            with open(str(readme), encoding="utf-8", errors="ignore") as fh:
                for line in fh:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        return line[:200]
        except Exception:  # noqa: BLE001
            pass
        return ""

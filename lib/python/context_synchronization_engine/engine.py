import json
import re
import subprocess
from dataclasses import replace
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple

from python.development_state_engine import DevelopmentStateEngine

from .models import SCHEMA_VERSION, SynchronizationFinding, SynchronizationReport
from .persistence import ContextPersistence

_EMPTY_SENTINELS = frozenset({"", "UNSPECIFIED", "None", "null", "N/A"})
_CONTEXT_FIELDS = (
    "repository",
    "workspace",
    "repository_root",
    "current_branch",
    "current_commit",
    "current_tag",
    "current_issue",
    "current_pull_request",
    "current_batch",
    "current_milestone",
    "current_epic",
    "current_roadmap",
    "current_sprint",
    "current_recommendation",
    "next_core",
    "next_batch",
    "next_issue",
    "next_pr",
    "owner_decisions",
    "pending_approvals",
    "open_blockers",
    "development_progress",
    "executive_status",
    "workspace_status",
)
_IMPLEMENTED_CORE_MARKERS = {
    "CORE-007": ("lib/python/canonical_intelligence",),
    "CORE-008A": ("lib/python/ai_cto_scanner",),
    "CORE-008B": ("lib/python/semantic_repository_intelligence",),
    "CORE-008C": ("lib/python/executable_repository_intelligence",),
    "CORE-009": ("lib/python/development_state_engine",),
    "CORE-010": ("lib/python/executive_briefing_engine",),
    "CORE-012": ("lib/python/workspace_orchestrator",),
    "CORE-013": ("lib/python/context_synchronization_engine",),
}


def _is_set(value: Any) -> bool:
    if isinstance(value, str):
        return value.strip() not in _EMPTY_SENTINELS
    return value not in (None, [], (), {}, "")


def _clean_scalar(value: Any) -> Any:
    if isinstance(value, str):
        stripped = value.strip()
        return stripped if stripped not in _EMPTY_SENTINELS else ""
    return value


def _compact_list(values: Iterable[Any]) -> List[str]:
    seen = set()
    items: List[str] = []
    for value in values or ():
        cleaned = str(value).strip()
        if not cleaned or cleaned in seen:
            continue
        seen.add(cleaned)
        items.append(cleaned)
    return items


class ContextCache:
    def __init__(self, repository_root: str = "."):
        self.persistence = ContextPersistence(repository_root)

    def load(self) -> Dict[str, Any]:
        return {
            "live_context": self.persistence.load_json("live_context.json") or {},
            "report": self.persistence.load_json("synchronization_report.json") or {},
        }


class GitContextProvider:
    def __init__(self, repository_root: str = "."):
        self.root = Path(repository_root).resolve()

    def collect(self) -> Dict[str, Any]:
        branch = self._git("rev-parse", "--abbrev-ref", "HEAD")
        commit = self._git("rev-parse", "HEAD")
        remote_url = self._git("config", "--get", "remote.origin.url")
        default_branch = self._default_branch()
        current_tag = self._git("tag", "--points-at", "HEAD").splitlines()[:1]
        branch_core = self._extract_core(branch)
        branch_issue = self._extract_issue(branch, branch_core)
        return {
            "repository_root": str(self.root),
            "repository": self.root.name,
            "remote_url": remote_url,
            "default_branch": default_branch,
            "current_branch": branch,
            "current_commit": commit,
            "current_tag": current_tag[0].strip() if current_tag else "",
            "current_issue": branch_issue,
            "active_core": branch_core,
            "next_pr": branch if branch and branch not in {default_branch, "main", "master"} else "",
            "timestamp": self._git("show", "-s", "--format=%cI", "HEAD") or "1970-01-01T00:00:00+00:00",
        }

    def _default_branch(self) -> str:
        ref = self._git("symbolic-ref", "refs/remotes/origin/HEAD")
        if ref.startswith("refs/remotes/origin/"):
            return ref.rsplit("/", 1)[-1]
        return "main"

    def _extract_core(self, branch: str) -> str:
        match = re.search(r"(CORE[-_]?\d{3}[A-Z]?)", branch or "", flags=re.IGNORECASE)
        if not match:
            return ""
        value = match.group(1).replace("_", "-").upper()
        if not value.startswith("CORE-"):
            value = value.replace("CORE", "CORE-")
        return value

    def _extract_issue(self, branch: str, branch_core: str) -> str:
        if branch_core:
            return branch_core
        match = re.search(r"(?:issue|task|pr)[-_]?(\d+)", branch or "", flags=re.IGNORECASE)
        return f"ISSUE-{match.group(1)}" if match else ""

    def _git(self, *args: str) -> str:
        try:
            result = subprocess.run(
                ["git", "-C", str(self.root), *args],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                text=True,
            )
            return result.stdout.strip()
        except Exception:
            return ""


class GitHubContextProvider:
    def __init__(self, repository_root: str = "."):
        self.root = Path(repository_root).resolve()

    def collect(self, git_context: Optional[Mapping[str, Any]] = None) -> Dict[str, Any]:
        remote_url = str((git_context or {}).get("remote_url", "") or "")
        owner = ""
        repo = ""
        if remote_url:
            match = re.search(r"[:/]([^/:]+)/([^/]+?)(?:\.git)?$", remote_url)
            if match:
                owner = match.group(1)
                repo = match.group(2)
        repository = f"{owner}/{repo}" if owner and repo else ""
        return {
            "available": bool(repository),
            "repository": repository,
            "owner": owner,
            "repo": repo,
            "remote_url": remote_url,
            "current_pull_request": "",
        }


class DevelopmentContextProvider:
    def __init__(self, repository_root: str = "."):
        self.root = Path(repository_root).resolve()
        self.persistence = ContextPersistence(self.root)

    def collect(self) -> Dict[str, Any]:
        state_engine = DevelopmentStateEngine(self.root)
        state = state_engine.LoadCurrentState(create_if_missing=True)
        snapshot = state_engine.manager.GenerateExecutiveSnapshot(
            state,
            refresh_integrations=False,
            timestamp=self._deterministic_timestamp(state),
        ).to_dict()
        executive = self._load_json(self.root / ".ai" / "executive" / "briefing.json")
        owner_actions = self._load_json(self.root / ".ai" / "executive" / "owner_actions.json")
        semantic = self._load_json(self.root / ".ai" / "semantic_knowledge.json")
        batches = self._load_batches()
        roadmap = self._load_roadmap()
        review_state = snapshot.get("state", {}).get("review_state", {})
        workspace_state = snapshot.get("state", {}).get("workspace_state", {})
        owner_state = snapshot.get("state", {}).get("owner_state", {})
        planning_state = snapshot.get("state", {}).get("planning_state", {})
        return {
            "state": state.to_dict(),
            "snapshot": snapshot,
            "current_context": snapshot.get("current_context", {}),
            "executive": executive,
            "owner_actions": owner_actions,
            "semantic": semantic,
            "batches": batches,
            "roadmap": roadmap,
            "owner_decisions": _compact_list(owner_state.get("manual_decisions", ())),
            "pending_approvals": _compact_list(review_state.get("pending_reviews", ())),
            "open_blockers": _compact_list(workspace_state.get("blocked_tasks", ())),
            "development_progress": float(workspace_state.get("estimated_progress", 0.0) or 0.0),
            "executive_status": str(executive.get("owner_dashboard", {}).get("overall_health", "") or ""),
            "workspace_status": str(snapshot.get("state", {}).get("repository_state", {}).get("repository_health", "") or ""),
            "current_recommendation": str(planning_state.get("recommended_batch", "") or ""),
        }

    def _deterministic_timestamp(self, state) -> str:
        snapshot_meta = state.snapshot_metadata.created_at or ""
        semantic = self._load_json(self.root / ".ai" / "semantic_knowledge.json")
        timestamps = [snapshot_meta, str(semantic.get("captured_at", ""))]
        timestamps.extend(str(batch.get("completed_at", "")) for batch in self._load_batches())
        normalized = sorted(value.replace("Z", "+00:00") for value in timestamps if value)
        return normalized[-1] if normalized else "1970-01-01T00:00:00+00:00"

    def _load_batches(self) -> List[Dict[str, Any]]:
        batches_dir = self.root / ".ai" / "batches"
        items: List[Dict[str, Any]] = []
        if not batches_dir.is_dir():
            return items
        for path in sorted(batches_dir.glob("*/metadata.json")):
            payload = self._load_json(path)
            if payload:
                payload["source_path"] = str(path)
                items.append(payload)
        return sorted(
            items,
            key=lambda item: (
                str(item.get("completed_at", "")),
                str(item.get("identifier", "")),
            ),
            reverse=True,
        )

    def _load_roadmap(self) -> Dict[str, Any]:
        docs_dir = self.root / "docs" / "canonical"
        candidates = sorted(docs_dir.glob("ROADMAP*.md")) if docs_dir.is_dir() else []
        if not candidates:
            return {}
        path = candidates[-1]
        lines = path.read_text(encoding="utf-8").splitlines()
        title = ""
        phases: List[Dict[str, str]] = []
        index = 0
        while index < len(lines):
            line = lines[index].strip()
            if not title and line.startswith("# "):
                title = line[2:].strip()
            if re.match(r"^# PHASE\s+\d+\s+—", line):
                status = ""
                probe = index + 1
                while probe < len(lines) and probe < index + 6:
                    candidate = lines[probe].strip()
                    if candidate.startswith("Status:"):
                        status = candidate.split(":", 1)[1].strip()
                        break
                    if candidate.startswith("# "):
                        break
                    probe += 1
                phases.append({"title": line.lstrip("# ").strip(), "status": status})
            index += 1
        current_phase = ""
        for phase in phases:
            if phase.get("status", "").upper() != "COMPLETE":
                current_phase = phase.get("title", "")
                break
        if not current_phase and phases:
            current_phase = phases[-1].get("title", "")
        return {
            "path": str(path),
            "title": title,
            "phases": phases,
            "current_phase": current_phase,
        }

    def _load_json(self, path: Path) -> Dict[str, Any]:
        if not path.exists():
            return {}
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return {}


class WorkspaceContextProvider:
    def __init__(self, repository_root: str = ".", workspace_root: Optional[str] = None):
        self.root = Path(repository_root).resolve()
        self.workspace_root = Path(workspace_root).resolve() if workspace_root else self.root.parent

    def collect(self) -> Dict[str, Any]:
        workspace_path = self.workspace_root / ".ai" / "workspace"
        dashboard = self._load_json(workspace_path / "dashboard.json")
        workspace = self._load_json(workspace_path / "workspace.json")
        repositories = self._load_json(workspace_path / "repositories.json")
        current_repo = {}
        for repo in repositories.get("repositories", []):
            if str(repo.get("repository_root", "")) == str(self.root):
                current_repo = repo
                break
        return {
            "workspace": str(self.workspace_root),
            "workspace_status": str(dashboard.get("workspace_summary", {}).get("overall_health", "") or ""),
            "dashboard": dashboard,
            "workspace_meta": workspace,
            "repository_context": current_repo,
        }

    def _load_json(self, path: Path) -> Dict[str, Any]:
        if not path.exists():
            return {}
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return {}


class ContextResolver:
    def __init__(self, repository_root: str = "."):
        self.root = Path(repository_root).resolve()

    def resolve(
        self,
        git_context: Mapping[str, Any],
        github_context: Mapping[str, Any],
        development_context: Mapping[str, Any],
        workspace_context: Mapping[str, Any],
        cache: Mapping[str, Any],
    ) -> Dict[str, Any]:
        previous = cache.get("live_context", {})
        development_current = development_context.get("current_context", {})
        roadmap = development_context.get("roadmap", {})
        semantic = development_context.get("semantic", {}).get("analysis", {})
        batches = development_context.get("batches", [])
        active_core = str(git_context.get("active_core", "") or "")
        current_batch = self._current_batch(development_current.get("current_batch", ""), batches)
        next_batch = self._next_batch(batches, current_batch)
        current_milestone = self._first_set(
            development_current.get("current_milestone", ""),
            roadmap.get("current_phase", ""),
            workspace_context.get("repository_context", {}).get("current_milestone", ""),
            previous.get("current_milestone", ""),
        )
        current_epic = self._first_set(
            development_current.get("current_epic", ""),
            active_core,
            previous.get("current_epic", ""),
            roadmap.get("title", ""),
        )
        current_recommendation, next_core, obsolete = self._resolve_next_core(
            active_core=active_core,
            current_recommendation=development_context.get("current_recommendation", ""),
            semantic_next_core=semantic.get("next_core", ""),
            previous=previous.get("current_recommendation", ""),
        )
        current_issue = self._first_set(
            git_context.get("current_issue", ""),
            development_current.get("current_issue", ""),
            workspace_context.get("repository_context", {}).get("current_issue", ""),
            previous.get("current_issue", ""),
            active_core,
        )
        current_pull_request = self._first_set(
            github_context.get("current_pull_request", ""),
            development_current.get("current_pull_request", ""),
            workspace_context.get("repository_context", {}).get("current_pull_request", ""),
            previous.get("current_pull_request", ""),
        )
        workspace_name = self._first_set(
            workspace_context.get("workspace", ""),
            development_current.get("current_workspace", ""),
            previous.get("workspace", ""),
            self.root.parent.name,
        )
        repository_name = self._first_set(
            github_context.get("repository", ""),
            git_context.get("repository", ""),
            previous.get("repository", ""),
        )
        live_context = {
            "schema_version": SCHEMA_VERSION,
            "generated_at": self._generated_at(git_context, development_context, workspace_context),
            "repository": repository_name,
            "workspace": workspace_name,
            "repository_root": str(self.root),
            "current_branch": self._first_set(git_context.get("current_branch", ""), previous.get("current_branch", "")),
            "current_commit": self._first_set(git_context.get("current_commit", ""), previous.get("current_commit", "")),
            "current_tag": self._first_set(git_context.get("current_tag", ""), previous.get("current_tag", "")),
            "current_issue": current_issue,
            "current_pull_request": current_pull_request,
            "current_batch": current_batch,
            "current_milestone": current_milestone,
            "current_epic": current_epic,
            "current_roadmap": self._first_set(roadmap.get("title", ""), previous.get("current_roadmap", "")),
            "current_sprint": self._first_set(active_core, development_context.get("state", {}).get("planning_state", {}).get("current_sprint", ""), previous.get("current_sprint", "")),
            "current_recommendation": current_recommendation,
            "next_core": next_core,
            "next_batch": next_batch,
            "next_issue": self._first_set(active_core, current_issue, previous.get("next_issue", "")),
            "next_pr": self._first_set(git_context.get("next_pr", ""), previous.get("next_pr", "")),
            "owner_decisions": development_context.get("owner_decisions", []),
            "pending_approvals": development_context.get("pending_approvals", []),
            "open_blockers": development_context.get("open_blockers", []),
            "development_progress": round(self._progress(development_context, batches), 4),
            "executive_status": self._first_set(development_context.get("executive_status", ""), previous.get("executive_status", ""), "unknown"),
            "workspace_status": self._first_set(workspace_context.get("workspace_status", ""), previous.get("workspace_status", ""), development_context.get("workspace_status", ""), "unknown"),
            "metadata": {
                "obsolete_recommendation": obsolete,
                "implemented_cores": self._implemented_cores(),
                "roadmap_path": roadmap.get("path", ""),
            },
        }
        live_context["sources"] = self._sources(git_context, github_context, development_context, workspace_context, previous, live_context)
        return self._sorted_mapping(live_context)

    def _resolve_next_core(self, *, active_core: str, current_recommendation: str, semantic_next_core: str, previous: str) -> Tuple[str, str, str]:
        implemented = set(self._implemented_cores())
        semantic_core = self._extract_core(str(semantic_next_core or ""))
        obsolete = semantic_core if semantic_core and semantic_core in implemented else ""
        candidate = ""
        if active_core:
            candidate = active_core
        elif semantic_core and semantic_core not in implemented:
            candidate = semantic_core
        elif _is_set(current_recommendation):
            candidate = str(current_recommendation).strip()
        elif _is_set(previous):
            candidate = str(previous).strip()
        return candidate, candidate, obsolete

    def _implemented_cores(self) -> List[str]:
        implemented = []
        for core, markers in sorted(_IMPLEMENTED_CORE_MARKERS.items()):
            if any((self.root / marker).exists() for marker in markers):
                implemented.append(core)
        return implemented

    def _generated_at(self, git_context: Mapping[str, Any], development_context: Mapping[str, Any], workspace_context: Mapping[str, Any]) -> str:
        timestamps = [
            str(git_context.get("timestamp", "")),
            str(development_context.get("snapshot", {}).get("generated_at", "")),
            str(development_context.get("executive", {}).get("generated_at", "")),
            str(workspace_context.get("workspace_meta", {}).get("generated_at", "")),
        ]
        timestamps.extend(str(batch.get("completed_at", "")) for batch in development_context.get("batches", []))
        normalized = sorted(value.replace("Z", "+00:00") for value in timestamps if value)
        return normalized[-1] if normalized else "1970-01-01T00:00:00+00:00"

    def _sources(
        self,
        git_context: Mapping[str, Any],
        github_context: Mapping[str, Any],
        development_context: Mapping[str, Any],
        workspace_context: Mapping[str, Any],
        previous: Mapping[str, Any],
        live_context: Mapping[str, Any],
    ) -> Dict[str, str]:
        development_current = development_context.get("current_context", {})
        repo_context = workspace_context.get("repository_context", {})
        sources: Dict[str, str] = {}
        for field in _CONTEXT_FIELDS:
            value = live_context.get(field)
            if not _is_set(value):
                continue
            if field in {"current_branch", "current_commit", "current_tag"} and _clean_scalar(git_context.get(field, "")) == value:
                sources[field] = "git"
            elif _clean_scalar(github_context.get(field, "")) == value:
                sources[field] = "github"
            elif _clean_scalar(development_current.get(field, "")) == value or _clean_scalar(development_context.get(field, "")) == value:
                sources[field] = "development_state"
            elif _clean_scalar(repo_context.get(field, "")) == value or _clean_scalar(workspace_context.get(field, "")) == value:
                sources[field] = "workspace"
            elif _clean_scalar(previous.get(field, "")) == value:
                sources[field] = "cache"
            else:
                sources[field] = "derived"
        return dict(sorted(sources.items()))

    def _current_batch(self, current_value: Any, batches: Sequence[Mapping[str, Any]]) -> str:
        if _is_set(current_value):
            return str(current_value).strip()
        for batch in batches:
            status = str(batch.get("status", "")).upper()
            if status and status != "COMPLETED":
                return str(batch.get("identifier", ""))
        return str(batches[0].get("identifier", "")) if batches else ""

    def _next_batch(self, batches: Sequence[Mapping[str, Any]], current_batch: str) -> str:
        for batch in batches:
            identifier = str(batch.get("identifier", ""))
            status = str(batch.get("status", "")).upper()
            if identifier and identifier != current_batch and status != "COMPLETED":
                return identifier
        return ""

    def _progress(self, development_context: Mapping[str, Any], batches: Sequence[Mapping[str, Any]]) -> float:
        explicit = development_context.get("development_progress", 0.0)
        if explicit:
            return max(0.0, min(100.0, float(explicit)))
        total = len(batches)
        if total:
            completed = sum(1 for batch in batches if str(batch.get("status", "")).upper() == "COMPLETED")
            return round((completed / float(total)) * 100.0, 4)
        return 0.0

    def _first_set(self, *values: Any) -> Any:
        for value in values:
            cleaned = _clean_scalar(value)
            if _is_set(cleaned):
                return cleaned
        return "" if all(not isinstance(value, (list, tuple, dict)) for value in values) else []

    def _extract_core(self, text: str) -> str:
        match = re.search(r"(CORE-\d{3}[A-Z]?)", text or "", flags=re.IGNORECASE)
        return match.group(1).upper() if match else ""

    def _sorted_mapping(self, value: Any) -> Any:
        if isinstance(value, Mapping):
            return {str(key): self._sorted_mapping(item) for key, item in sorted(value.items(), key=lambda pair: str(pair[0]))}
        if isinstance(value, tuple):
            return [self._sorted_mapping(item) for item in value]
        if isinstance(value, list):
            return [self._sorted_mapping(item) for item in value]
        return value


class ContextValidator:
    def validate(
        self,
        live_context: Mapping[str, Any],
        git_context: Mapping[str, Any],
        development_context: Mapping[str, Any],
        workspace_context: Mapping[str, Any],
        cache: Mapping[str, Any],
    ) -> SynchronizationReport:
        findings: List[SynchronizationFinding] = []
        corrected_fields: List[str] = []
        missing_fields: List[str] = []
        conflicts: Dict[str, Tuple[str, ...]] = {}
        previous = cache.get("live_context", {})
        dev_current = development_context.get("current_context", {})
        repo_context = workspace_context.get("repository_context", {})

        findings.extend(self._field_finding("stale_branch", "current_branch", dev_current.get("current_branch", ""), live_context.get("current_branch", ""), corrected_fields))
        findings.extend(self._field_finding("stale_pr", "current_pull_request", dev_current.get("current_pull_request", ""), live_context.get("current_pull_request", ""), corrected_fields))
        findings.extend(self._field_finding("stale_issue", "current_issue", dev_current.get("current_issue", ""), live_context.get("current_issue", ""), corrected_fields))
        findings.extend(self._field_finding("stale_batch", "current_batch", dev_current.get("current_batch", ""), live_context.get("current_batch", ""), corrected_fields))
        findings.extend(self._field_finding("stale_milestone", "current_milestone", dev_current.get("current_milestone", ""), live_context.get("current_milestone", ""), corrected_fields))
        findings.extend(self._field_finding("stale_epic", "current_epic", dev_current.get("current_epic", ""), live_context.get("current_epic", ""), corrected_fields))

        obsolete = str(live_context.get("metadata", {}).get("obsolete_recommendation", "") or "")
        if obsolete:
            findings.append(SynchronizationFinding(
                category="obsolete_core_recommendation",
                severity="warning",
                message=f"Invalidated obsolete CORE recommendation: {obsolete}",
                evidence=(obsolete, str(live_context.get("current_recommendation", ""))),
                corrected=True,
            ))
            corrected_fields.append("current_recommendation")
            corrected_fields.append("next_core")

        for field in ("current_issue", "current_batch", "current_milestone", "current_epic", "current_recommendation"):
            if not _is_set(dev_current.get(field, "")) and _is_set(live_context.get(field, "")):
                findings.append(SynchronizationFinding(
                    category="missing_synchronization",
                    severity="warning",
                    message=f"Filled missing synchronized field: {field}",
                    evidence=(str(live_context.get(field, "")),),
                    corrected=True,
                ))
                missing_fields.append(field)

        for field in ("current_branch", "current_issue", "current_pull_request", "current_batch", "current_milestone", "current_epic", "current_recommendation"):
            candidates = _compact_list([
                git_context.get(field, ""),
                dev_current.get(field, ""),
                repo_context.get(field, ""),
                previous.get(field, ""),
            ])
            if len(candidates) > 1:
                conflicts[field] = tuple(candidates)
                findings.append(SynchronizationFinding(
                    category="conflicting_context",
                    severity="warning",
                    message=f"Resolved conflicting context for {field}",
                    evidence=tuple(candidates[:4]),
                    corrected=True,
                ))

        return SynchronizationReport(
            repository=str(live_context.get("repository", "")),
            workspace=str(live_context.get("workspace", "")),
            generated_at=str(live_context.get("generated_at", "")),
            findings=tuple(findings),
            corrected_fields=tuple(sorted(set(corrected_fields))),
            missing_fields=tuple(sorted(set(missing_fields))),
            conflicts=dict(sorted(conflicts.items())),
        )

    def _field_finding(self, category: str, field: str, before: Any, after: Any, corrected_fields: List[str]) -> List[SynchronizationFinding]:
        before_value = _clean_scalar(before)
        after_value = _clean_scalar(after)
        if _is_set(before_value) and _is_set(after_value) and before_value != after_value:
            corrected_fields.append(field)
            return [SynchronizationFinding(
                category=category,
                severity="warning",
                message=f"Corrected {field} from stale value to synchronized value",
                evidence=(str(before_value), str(after_value)),
                corrected=True,
            )]
        return []


class SynchronizationReportGenerator:
    def generate(self, live_context: Mapping[str, Any], report: SynchronizationReport) -> str:
        lines = [
            "# AI CTO Context Synchronization Report",
            "",
            f"Generated: {live_context.get('generated_at', '')}",
            "",
            "## Live Context",
            "",
        ]
        for key in _CONTEXT_FIELDS:
            value = live_context.get(key)
            if isinstance(value, list):
                rendered = ", ".join(value) if value else ""
            else:
                rendered = str(value or "")
            lines.append(f"- **{key.replace('_', ' ').title()}**: {rendered}")
        lines.extend(["", "## Synchronization Findings", ""])
        if report.findings:
            for finding in report.findings:
                lines.append(f"- [{finding.severity.upper()}] {finding.category}: {finding.message}")
        else:
            lines.append("- No synchronization defects detected.")
        lines.extend(["", "## Corrected Fields", ""])
        lines.append(", ".join(report.corrected_fields) if report.corrected_fields else "None")
        lines.extend(["", "## Missing Fields Filled", ""])
        lines.append(", ".join(report.missing_fields) if report.missing_fields else "None")
        return "\n".join(lines).rstrip() + "\n"


class SynchronizationCoordinator:
    def __init__(self, repository_root: str = ".", workspace_root: Optional[str] = None):
        self.root = Path(repository_root).resolve()
        self.workspace_root = Path(workspace_root).resolve() if workspace_root else self.root.parent

    def synchronize(self, refresh: bool = False) -> Dict[str, Any]:
        cache = ContextCache(self.root).load()
        git_context = GitContextProvider(self.root).collect()
        github_context = GitHubContextProvider(self.root).collect(git_context)
        development_context = DevelopmentContextProvider(self.root).collect()
        workspace_context = WorkspaceContextProvider(self.root, self.workspace_root).collect()
        live_context = ContextResolver(self.root).resolve(
            git_context,
            github_context,
            development_context,
            workspace_context,
            cache,
        )
        report = ContextValidator().validate(
            live_context,
            git_context,
            development_context,
            workspace_context,
            cache,
        )
        updated_state = self._synchronize_development_state(development_context.get("state", {}), live_context)
        paths = self._persist(live_context, git_context, github_context, development_context, workspace_context, report)
        downstream = self._refresh_downstream(live_context, refresh=refresh)
        result = {
            "schema_version": SCHEMA_VERSION,
            "generated_at": live_context.get("generated_at", ""),
            "repository": str(live_context.get("repository", "")),
            "workspace": str(live_context.get("workspace", "")),
            "live_context": live_context,
            "development_context": self._build_development_context(live_context, development_context),
            "workspace_context": self._build_workspace_context(live_context, workspace_context, downstream),
            "git_context": self._sorted_mapping(git_context),
            "github_context": self._sorted_mapping(github_context),
            "synchronization_report": report.to_dict(),
            "paths": paths,
            "updated_state_identifier": updated_state.identifier,
        }
        return self._sorted_mapping(result)

    def _synchronize_development_state(self, state_dict: Mapping[str, Any], live_context: Mapping[str, Any]):
        engine = DevelopmentStateEngine(self.root)
        state = engine.LoadCurrentState(create_if_missing=True)
        workspace_state = replace(
            state.workspace_state,
            active_workspace=str(live_context.get("workspace", "") or state.workspace_state.active_workspace),
            current_milestone=str(live_context.get("current_milestone", "") or state.workspace_state.current_milestone),
            current_batch=str(live_context.get("current_batch", "") or state.workspace_state.current_batch),
            current_task=str(live_context.get("current_issue", "") or state.workspace_state.current_task),
            current_objective=str(live_context.get("current_recommendation", "") or state.workspace_state.current_objective),
            estimated_progress=float(live_context.get("development_progress", state.workspace_state.estimated_progress) or 0.0),
            blocked_tasks=tuple(_compact_list(live_context.get("open_blockers", []) or state.workspace_state.blocked_tasks)),
        )
        repository_state = replace(
            state.repository_state,
            repository=str(live_context.get("repository", "") or state.repository_state.repository),
            branch=str(live_context.get("current_branch", "") or state.repository_state.branch),
            head_commit=str(live_context.get("current_commit", "") or state.repository_state.head_commit),
            open_pull_requests=tuple(_compact_list([live_context.get("current_pull_request", "")] + list(state.repository_state.open_pull_requests))),
            tags=tuple(_compact_list([live_context.get("current_tag", "")] + list(state.repository_state.tags))),
            release=str(live_context.get("current_tag", "") or state.repository_state.release),
            repository_health=str(live_context.get("workspace_status", "") or state.repository_state.repository_health),
        )
        planning_state = replace(
            state.planning_state,
            current_roadmap=str(live_context.get("current_epic", "") or live_context.get("current_roadmap", "") or state.planning_state.current_roadmap),
            current_sprint=str(live_context.get("current_sprint", "") or state.planning_state.current_sprint),
            recommended_batch=str(live_context.get("current_recommendation", "") or state.planning_state.recommended_batch),
            priority_queue=tuple(_compact_list([live_context.get("next_core", ""), live_context.get("next_batch", ""), live_context.get("next_issue", "")] + list(state.planning_state.priority_queue))),
        )
        review_state = replace(
            state.review_state,
            pending_reviews=tuple(_compact_list(live_context.get("pending_approvals", []) or state.review_state.pending_reviews)),
            open_prs=tuple(_compact_list([live_context.get("current_pull_request", "")] + list(state.review_state.open_prs))),
            approval_status="PENDING" if live_context.get("pending_approvals", []) else state.review_state.approval_status,
        )
        updated = replace(
            state,
            workspace_state=workspace_state,
            repository_state=repository_state,
            planning_state=planning_state,
            review_state=review_state,
        )
        return engine.SaveCurrentState(
            updated,
            source_event="context_synchronized",
            timestamp=str(live_context.get("generated_at", "")),
            event_context={
                "current_workspace": live_context.get("workspace", ""),
                "current_branch": live_context.get("current_branch", ""),
                "current_milestone": live_context.get("current_milestone", ""),
                "current_epic": live_context.get("current_epic", ""),
                "current_issue": live_context.get("current_issue", ""),
                "current_pull_request": live_context.get("current_pull_request", ""),
                "current_batch": live_context.get("current_batch", ""),
                "current_task": live_context.get("current_issue", ""),
                "current_recommendation": live_context.get("current_recommendation", ""),
            },
            event_payload={"synchronization": "core-013"},
            refresh_integrations=False,
        )

    def _persist(
        self,
        live_context: Mapping[str, Any],
        git_context: Mapping[str, Any],
        github_context: Mapping[str, Any],
        development_context: Mapping[str, Any],
        workspace_context: Mapping[str, Any],
        report: SynchronizationReport,
    ) -> Dict[str, str]:
        persistence = ContextPersistence(self.root)
        paths = {
            "live_context": persistence.save_json("live_context.json", self._sorted_mapping(live_context)),
            "development_context": persistence.save_json(
                "development_context.json",
                self._build_development_context(live_context, development_context),
            ),
            "workspace_context": persistence.save_json(
                "workspace_context.json",
                self._build_workspace_context(live_context, workspace_context, {}),
            ),
            "git_context": persistence.save_json("git_context.json", self._sorted_mapping(git_context)),
            "github_context": persistence.save_json("github_context.json", self._sorted_mapping(github_context)),
            "synchronization_report": persistence.save_json("synchronization_report.json", report.to_dict()),
        }
        markdown = SynchronizationReportGenerator().generate(live_context, report)
        paths["markdown"] = persistence.save_text("AI_CTO_CONTEXT_REPORT.md", markdown)
        return paths

    def _refresh_downstream(self, live_context: Mapping[str, Any], refresh: bool) -> Dict[str, Any]:
        from python.executive_briefing_engine import ExecutiveBriefingEngine
        from python.workspace_orchestrator import WorkspaceOrchestrator

        briefing = ExecutiveBriefingEngine(
            repository=str(self.root),
            output_dir=str(self.root),
            persist=True,
            refresh_integrations=False,
        ).generate()
        orchestrator = WorkspaceOrchestrator(
            workspace_root=str(self.workspace_root),
            output_dir=str(self.workspace_root),
            persist=True,
        )
        if refresh or not (self.workspace_root / ".ai" / "workspace" / "workspace.json").exists():
            workspace_result = orchestrator.scan(refresh=refresh)
            workspace_paths = {
                "workspace_json": str(self.workspace_root / ".ai" / "workspace" / "workspace.json"),
                "dashboard_md": str(self.workspace_root / "AI_CTO_WORKSPACE_DASHBOARD.md"),
            }
        else:
            repo = orchestrator.register_repository(str(self.root))
            dashboard = orchestrator.dashboard()
            workspace_result = {"repository": repo.to_dict(), "dashboard": dashboard.get("dashboard_dict", {})}
            workspace_paths = dashboard.get("paths", {})
        return {
            "briefing_id": briefing.get("briefing").briefing_id if briefing.get("briefing") else "",
            "briefing_paths": briefing.get("paths", {}),
            "workspace": workspace_result,
            "workspace_paths": workspace_paths,
        }

    def _build_development_context(self, live_context: Mapping[str, Any], development_context: Mapping[str, Any]) -> Dict[str, Any]:
        return self._sorted_mapping({
            "schema_version": SCHEMA_VERSION,
            "generated_at": live_context.get("generated_at", ""),
            "repository": live_context.get("repository", ""),
            "current_context": {key: live_context.get(key, "") for key in (
                "current_branch",
                "current_issue",
                "current_pull_request",
                "current_batch",
                "current_milestone",
                "current_epic",
                "current_roadmap",
                "current_sprint",
                "current_recommendation",
                "next_core",
                "next_batch",
                "next_issue",
                "next_pr",
            )},
            "owner_decisions": live_context.get("owner_decisions", []),
            "pending_approvals": live_context.get("pending_approvals", []),
            "open_blockers": live_context.get("open_blockers", []),
            "development_progress": live_context.get("development_progress", 0.0),
            "state_identifier": development_context.get("state", {}).get("identifier", ""),
        })

    def _build_workspace_context(self, live_context: Mapping[str, Any], workspace_context: Mapping[str, Any], downstream: Mapping[str, Any]) -> Dict[str, Any]:
        return self._sorted_mapping({
            "schema_version": SCHEMA_VERSION,
            "generated_at": live_context.get("generated_at", ""),
            "workspace": live_context.get("workspace", ""),
            "workspace_root": workspace_context.get("workspace", ""),
            "workspace_status": live_context.get("workspace_status", ""),
            "executive_status": live_context.get("executive_status", ""),
            "repository_context": workspace_context.get("repository_context", {}),
            "dashboard": workspace_context.get("dashboard", {}),
            "refreshed_paths": downstream.get("workspace_paths", {}),
        })

    def _sorted_mapping(self, value: Any) -> Any:
        if isinstance(value, Mapping):
            return {str(key): self._sorted_mapping(item) for key, item in sorted(value.items(), key=lambda pair: str(pair[0]))}
        if isinstance(value, tuple):
            return [self._sorted_mapping(item) for item in value]
        if isinstance(value, list):
            return [self._sorted_mapping(item) for item in value]
        return value


class ContextSynchronizationEngine:
    def __init__(self, repository: str = ".", workspace_root: Optional[str] = None, persist: bool = True):
        self.repository = str(Path(repository).resolve())
        self.workspace_root = str(Path(workspace_root).resolve()) if workspace_root else str(Path(repository).resolve().parent)
        self.persist = persist
        self.coordinator = SynchronizationCoordinator(self.repository, self.workspace_root)

    def synchronize(self, refresh: bool = False) -> Dict[str, Any]:
        return self.coordinator.synchronize(refresh=refresh)

    def synchronize_context(self, refresh: bool = False) -> Dict[str, Any]:
        return self.synchronize(refresh=refresh)

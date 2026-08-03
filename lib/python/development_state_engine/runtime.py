"""
Development State Engine — Runtime Orchestration
CORE-009C
"""

import hashlib
import json
import os
import subprocess
import tempfile
from dataclasses import dataclass, replace
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple, Union

from python.ai_cto_scanner import AICTOScannerEngine
from python.canonical_intelligence import CanonicalIntelligenceEngine
from python.repository_engine.engine import RepositoryEngine
from python.semantic_repository_intelligence import SemanticPersistence, SemanticRepositoryEngine

from .models import (
    MODEL_VERSION,
    DevelopmentState,
    ExecutionState,
    IntegrityReport,
    OwnerState,
    PlanningState,
    RepositoryState,
    ReviewState,
    SnapshotMetadata,
    TelegramState,
    WorkspaceState,
)
from .repository import DevelopmentStateRepository


_RUNTIME_CONTEXT_KEYS = (
    "current_workspace",
    "current_repository",
    "current_branch",
    "current_milestone",
    "current_epic",
    "current_issue",
    "current_pull_request",
    "current_batch",
    "current_task",
    "current_executor",
    "current_recommendation",
    "current_canon_version",
)


@dataclass(frozen=True)
class DevelopmentStateSnapshot:
    generated_at: str
    current_context: Dict[str, Any]
    state: Dict[str, Any]
    integrity: Dict[str, Any]
    integrations: Dict[str, Any]
    recent_events: List[Dict[str, Any]]
    schema_version: str = MODEL_VERSION

    def to_dict(self) -> Dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "generated_at": self.generated_at,
            "current_context": dict(sorted(self.current_context.items())),
            "state": self.state,
            "integrity": self.integrity,
            "integrations": self.integrations,
            "recent_events": self.recent_events,
        }


class DevelopmentStateEventBus:
    """Persistent event stream for runtime orchestration."""

    SCHEMA_VERSION = MODEL_VERSION

    def __init__(self, repository_root: Union[str, Path] = "."):
        self.repository_root = Path(repository_root).resolve()
        self.base_dir = self.repository_root / ".ai" / "development_state"
        self.events_path = self.base_dir / "events.json"

    def LoadEvents(self) -> Dict[str, Any]:
        if not self.events_path.exists():
            return {
                "schema_version": self.SCHEMA_VERSION,
                "event_count": 0,
                "events": [],
            }
        payload = self._read_json(self.events_path)
        events = self._normalize_events(payload.get("events", []))
        return {
            "schema_version": payload.get("schema_version", self.SCHEMA_VERSION),
            "event_count": len(events),
            "events": events,
        }

    def Publish(
        self,
        event_type: str,
        payload: Optional[Mapping[str, Any]] = None,
        context: Optional[Mapping[str, Any]] = None,
        timestamp: Optional[str] = None,
    ) -> Dict[str, Any]:
        document = self.LoadEvents()
        events = list(document["events"])
        normalized_payload = self._sorted_mapping(payload or {})
        normalized_context = self._sorted_mapping(context or {})
        fingerprint = self._fingerprint(event_type, normalized_payload, normalized_context)

        for event in events:
            if event.get("fingerprint") == fingerprint:
                return event

        event = {
            "event_type": event_type,
            "timestamp": timestamp or self._utcnow(),
            "sequence_number": (events[-1]["sequence_number"] + 1) if events else 1,
            "fingerprint": fingerprint,
            "payload": normalized_payload,
            "context": normalized_context,
        }
        events.append(event)
        document = {
            "schema_version": self.SCHEMA_VERSION,
            "event_count": len(events),
            "events": self._normalize_events(events),
        }
        self._atomic_write_json(self.events_path, document)
        return event

    def RecentEvents(self, limit: int = 10) -> List[Dict[str, Any]]:
        events = self.LoadEvents()["events"]
        return events[-limit:] if limit > 0 else []

    def _normalize_events(self, events: Iterable[Mapping[str, Any]]) -> List[Dict[str, Any]]:
        normalized: List[Dict[str, Any]] = []
        seen = set()
        for event in events:
            fingerprint = str(event.get("fingerprint", ""))
            if not fingerprint or fingerprint in seen:
                continue
            seen.add(fingerprint)
            normalized.append(
                {
                    "event_type": str(event.get("event_type", "runtime")),
                    "timestamp": str(event.get("timestamp", "")),
                    "sequence_number": int(event.get("sequence_number", 0)),
                    "fingerprint": fingerprint,
                    "payload": self._sorted_mapping(event.get("payload", {})),
                    "context": self._sorted_mapping(event.get("context", {})),
                }
            )
        normalized.sort(
            key=lambda item: (
                item["sequence_number"],
                item["timestamp"],
                item["event_type"],
                item["fingerprint"],
            )
        )
        for index, event in enumerate(normalized, start=1):
            event["sequence_number"] = index
        return normalized

    def _fingerprint(self, event_type: str, payload: Mapping[str, Any], context: Mapping[str, Any]) -> str:
        material = {
            "event_type": event_type,
            "payload": payload,
            "context": context,
        }
        serialized = json.dumps(material, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()

    def _sorted_mapping(self, value: Any) -> Any:
        if isinstance(value, Mapping):
            return {str(k): self._sorted_mapping(v) for k, v in sorted(value.items(), key=lambda item: str(item[0]))}
        if isinstance(value, (list, tuple)):
            return [self._sorted_mapping(item) for item in value]
        return value

    def _read_json(self, path: Path) -> Dict[str, Any]:
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON at {path}") from exc

    def _atomic_write_json(self, path: Path, payload: Mapping[str, Any]):
        path.parent.mkdir(parents=True, exist_ok=True)
        content = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
        fd, tmp_path = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent))
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as fh:
                fh.write(content)
                fh.flush()
                os.fsync(fh.fileno())
            os.replace(tmp_path, path)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def _utcnow(self) -> str:
        return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class DevelopmentStateManager:
    """Coordinates state persistence, runtime events, and executive snapshots."""

    SCHEMA_VERSION = MODEL_VERSION

    def __init__(
        self,
        repository_root: Union[str, Path] = ".",
        repository: Optional[DevelopmentStateRepository] = None,
        event_bus: Optional[DevelopmentStateEventBus] = None,
        repository_engine_class=RepositoryEngine,
        canonical_engine_class=CanonicalIntelligenceEngine,
        semantic_engine_class=SemanticRepositoryEngine,
        ai_cto_scanner_class=AICTOScannerEngine,
        executable_intelligence_provider=None,
    ):
        self.repository_root = Path(repository_root).resolve()
        self.repository = repository or DevelopmentStateRepository(self.repository_root)
        self.event_bus = event_bus or DevelopmentStateEventBus(self.repository_root)
        self.repository_engine_class = repository_engine_class
        self.canonical_engine_class = canonical_engine_class
        self.semantic_engine_class = semantic_engine_class
        self.ai_cto_scanner_class = ai_cto_scanner_class
        self.executable_intelligence_provider = executable_intelligence_provider
        self.base_dir = self.repository.base_dir
        self.executive_snapshot_path = self.base_dir / "executive_snapshot.json"

    def LoadCurrentState(self) -> Optional[DevelopmentState]:
        return self.repository.LoadState()

    def SaveCurrentState(
        self,
        state: DevelopmentState,
        *,
        create_snapshot: bool = False,
        snapshot_trigger: str = "runtime_update",
        source_event: str = "state_saved",
        snapshot_tags: Sequence[str] = (),
        timestamp: Optional[str] = None,
        event_payload: Optional[Mapping[str, Any]] = None,
        event_context: Optional[Mapping[str, Any]] = None,
        refresh_integrations: bool = False,
    ) -> DevelopmentState:
        materialized = self._prepare_state(
            state,
            create_snapshot=create_snapshot,
            snapshot_trigger=snapshot_trigger,
            source_event=source_event,
            snapshot_tags=snapshot_tags,
            timestamp=timestamp,
        )
        self.repository.SaveState(materialized)
        self.repository.VerifyIntegrity()
        if create_snapshot:
            self.repository.CreateSnapshot()
        integrity = self._load_integrity_document()
        context = self.BuildCurrentContext(materialized)
        if event_context:
            context.update(self._normalized_context(event_context))
        payload = {
            "state_identifier": materialized.identifier,
            "schema_version": materialized.schema_version,
            "snapshot_id": materialized.snapshot_metadata.identifier,
            "state_sha256": integrity.get("state_sha256", ""),
        }
        if event_payload:
            payload.update(self._sorted_mapping(event_payload))
        self.event_bus.Publish(source_event, payload=payload, context=context, timestamp=timestamp)
        self.WriteExecutiveSnapshot(materialized, refresh_integrations=refresh_integrations, timestamp=timestamp)
        return materialized

    def WriteExecutiveSnapshot(
        self,
        state: Optional[DevelopmentState] = None,
        *,
        refresh_integrations: bool = False,
        timestamp: Optional[str] = None,
    ) -> DevelopmentStateSnapshot:
        state = state or self.LoadCurrentState()
        if state is None:
            raise ValueError("No current development state found")
        snapshot = self.GenerateExecutiveSnapshot(
            state,
            refresh_integrations=refresh_integrations,
            timestamp=timestamp,
        )
        self._atomic_write_json(self.executive_snapshot_path, snapshot.to_dict())
        return snapshot

    def GenerateExecutiveSnapshot(
        self,
        state: DevelopmentState,
        *,
        refresh_integrations: bool = False,
        timestamp: Optional[str] = None,
    ) -> DevelopmentStateSnapshot:
        return DevelopmentStateSnapshot(
            generated_at=timestamp or self._utcnow(),
            current_context=self.BuildCurrentContext(state),
            state={
                "identifier": state.identifier,
                "schema_version": state.schema_version,
                "workspace_state": state.workspace_state.to_dict(),
                "repository_state": state.repository_state.to_dict(),
                "execution_state": state.execution_state.to_dict(),
                "planning_state": state.planning_state.to_dict(),
                "review_state": state.review_state.to_dict(),
                "owner_state": state.owner_state.to_dict(),
                "telegram_state": state.telegram_state.to_dict(),
                "snapshot_metadata": state.snapshot_metadata.to_dict(),
                "integrity_report": state.integrity_report.to_dict(),
            },
            integrity=self._load_integrity_document(),
            integrations=self._integration_snapshot(state, refresh=refresh_integrations),
            recent_events=self.event_bus.RecentEvents(),
        )

    def BuildCurrentContext(self, state: DevelopmentState) -> Dict[str, Any]:
        current = {
            "current_workspace": state.workspace_state.active_workspace,
            "current_repository": state.repository_state.repository,
            "current_branch": state.repository_state.branch,
            "current_milestone": state.workspace_state.current_milestone,
            "current_epic": state.planning_state.current_roadmap,
            "current_issue": state.workspace_state.current_task,
            "current_pull_request": self._first_non_empty(
                state.review_state.open_prs,
                state.repository_state.open_pull_requests,
            ),
            "current_batch": state.workspace_state.current_batch,
            "current_task": state.workspace_state.current_task,
            "current_executor": state.execution_state.current_executor,
            "current_recommendation": state.planning_state.recommended_batch,
            "current_canon_version": state.schema_version,
        }
        for event in self.event_bus.LoadEvents()["events"]:
            for key in _RUNTIME_CONTEXT_KEYS:
                value = event.get("context", {}).get(key)
                if value not in (None, "", []):
                    current[key] = value
        return dict(sorted(current.items()))

    def _prepare_state(
        self,
        state: DevelopmentState,
        *,
        create_snapshot: bool,
        snapshot_trigger: str,
        source_event: str,
        snapshot_tags: Sequence[str],
        timestamp: Optional[str],
    ) -> DevelopmentState:
        effective_time = timestamp or self._utcnow()
        snapshot = state.snapshot_metadata
        sequence_number = snapshot.sequence_number + 1 if create_snapshot else snapshot.sequence_number
        snapshot_id = snapshot.identifier
        if create_snapshot:
            snapshot_id = f"SNAP-{sequence_number:06d}"
        snapshot = replace(
            snapshot,
            identifier=snapshot_id,
            trigger=snapshot_trigger,
            created_at=effective_time,
            source_event=source_event,
            sequence_number=sequence_number,
            tags=self._dedupe_strings(snapshot_tags or snapshot.tags),
        )
        normalized = replace(
            state,
            workspace_state=self._normalize_workspace_state(state.workspace_state),
            repository_state=self._normalize_repository_state(state.repository_state),
            execution_state=self._normalize_execution_state(state.execution_state),
            planning_state=self._normalize_planning_state(state.planning_state),
            review_state=self._normalize_review_state(state.review_state),
            owner_state=self._normalize_owner_state(state.owner_state),
            telegram_state=self._normalize_telegram_state(state.telegram_state),
            snapshot_metadata=snapshot,
        )
        normalized.validate()
        return normalized

    def _normalize_workspace_state(self, state: WorkspaceState) -> WorkspaceState:
        return replace(
            state,
            completed_tasks=self._dedupe_strings(state.completed_tasks),
            blocked_tasks=self._dedupe_strings(state.blocked_tasks),
        )

    def _normalize_repository_state(self, state: RepositoryState) -> RepositoryState:
        return replace(
            state,
            open_pull_requests=self._dedupe_strings(state.open_pull_requests),
            tags=self._dedupe_strings(state.tags),
        )

    def _normalize_execution_state(self, state: ExecutionState) -> ExecutionState:
        return replace(
            state,
            running_jobs=self._dedupe_strings(state.running_jobs),
            completed_jobs=self._dedupe_strings(state.completed_jobs),
            failed_jobs=self._dedupe_strings(state.failed_jobs),
            execution_queue=self._dedupe_strings(state.execution_queue),
            retry_queue=self._dedupe_strings(state.retry_queue),
            execution_history=self._dedupe_strings(state.execution_history),
        )

    def _normalize_planning_state(self, state: PlanningState) -> PlanningState:
        return replace(
            state,
            priority_queue=self._dedupe_strings(state.priority_queue),
            dependencies=self._dedupe_strings(state.dependencies),
        )

    def _normalize_review_state(self, state: ReviewState) -> ReviewState:
        return replace(
            state,
            pending_reviews=self._dedupe_strings(state.pending_reviews),
            open_prs=self._dedupe_strings(state.open_prs),
            architecture_findings=self._dedupe_strings(state.architecture_findings),
            canonical_findings=self._dedupe_strings(state.canonical_findings),
        )

    def _normalize_owner_state(self, state: OwnerState) -> OwnerState:
        return replace(
            state,
            owner_priorities=self._dedupe_strings(state.owner_priorities),
            manual_decisions=self._dedupe_strings(state.manual_decisions),
            overrides=self._dedupe_strings(state.overrides),
            pinned_tasks=self._dedupe_strings(state.pinned_tasks),
            deferred_tasks=self._dedupe_strings(state.deferred_tasks),
        )

    def _normalize_telegram_state(self, state: TelegramState) -> TelegramState:
        return replace(
            state,
            subscribed_channels=self._dedupe_strings(state.subscribed_channels),
            pending_notifications=self._dedupe_strings(state.pending_notifications),
        )

    def _integration_snapshot(self, state: DevelopmentState, refresh: bool) -> Dict[str, Any]:
        return {
            "repository_intelligence": self._repository_intelligence(),
            "canonical_intelligence": self._canonical_intelligence(refresh),
            "semantic_repository_intelligence": self._semantic_repository_intelligence(refresh),
            "ai_cto_scanner": self._ai_cto_scanner(refresh),
            "executable_repository_intelligence": self._executable_repository_intelligence(state, refresh),
        }

    def _repository_intelligence(self) -> Dict[str, Any]:
        engine = self.repository_engine_class(root=str(self.repository_root))
        return {
            "repository_root": str(self.repository_root),
            "statistics": engine.statistics(),
        }

    def _canonical_intelligence(self, refresh: bool) -> Dict[str, Any]:
        docs_path = self.repository_root / "docs" / "canonical"
        snapshot = {
            "available": docs_path.is_dir(),
            "canonical_docs_path": str(docs_path),
        }
        if not refresh or not docs_path.is_dir():
            return snapshot
        try:
            engine = self.canonical_engine_class(repository=str(self.repository_root))
            result = engine.run()
            snapshot.update(engine.statistics(result))
        except Exception as exc:
            snapshot["error"] = str(exc)
        return self._sorted_mapping(snapshot)

    def _semantic_repository_intelligence(self, refresh: bool) -> Dict[str, Any]:
        persistence = SemanticPersistence(self.repository_root)
        if persistence.exists():
            loaded = persistence.load() or {}
            analysis = loaded.get("analysis", {})
            return self._sorted_mapping(
                {
                    "schema_version": loaded.get("schema_version", MODEL_VERSION),
                    "captured_at": loaded.get("captured_at", ""),
                    "analysis": analysis,
                }
            )
        snapshot = {
            "schema_version": MODEL_VERSION,
            "captured_at": "",
            "analysis": {},
        }
        if not refresh:
            return snapshot
        try:
            result = self.semantic_engine_class(repository=str(self.repository_root), persist=True).analyze()
            snapshot["captured_at"] = self._utcnow()
            snapshot["analysis"] = self._compact_semantic_result(result)
        except Exception as exc:
            snapshot["error"] = str(exc)
        return self._sorted_mapping(snapshot)

    def _ai_cto_scanner(self, refresh: bool) -> Dict[str, Any]:
        report_path = self.repository_root / "AI_CTO_INTEGRATION_REPORT.md"
        snapshot = {
            "report_exists": report_path.exists(),
            "report_path": str(report_path),
        }
        if not refresh:
            return snapshot
        try:
            result = self.ai_cto_scanner_class(repository=str(self.repository_root), output_dir=str(self.repository_root)).scan()
            snapshot.update(
                {
                    "repository_name": result.get("repository_name", self.repository_root.name),
                    "scores": result.get("scores", {}),
                    "workspace": result.get("workspace", {}),
                    "detection_categories": sorted(result.get("detection", {}).keys()),
                }
            )
        except Exception as exc:
            snapshot["error"] = str(exc)
        return self._sorted_mapping(snapshot)

    def _executable_repository_intelligence(self, state: DevelopmentState, refresh: bool) -> Dict[str, Any]:
        if self.executable_intelligence_provider is not None:
            try:
                provider = self.executable_intelligence_provider(repository=str(self.repository_root))
                if hasattr(provider, "analyze"):
                    return self._sorted_mapping(provider.analyze())
                if hasattr(provider, "snapshot"):
                    return self._sorted_mapping(provider.snapshot())
            except Exception as exc:
                return {"error": str(exc), "provider": type(self.executable_intelligence_provider).__name__}
        execution_events = [
            event for event in self.event_bus.LoadEvents()["events"]
            if event.get("event_type") == "execution"
        ]
        return {
            "provider": "runtime_execution_state",
            "refresh_requested": bool(refresh),
            "running_jobs": len(state.execution_state.running_jobs),
            "completed_jobs": len(state.execution_state.completed_jobs),
            "failed_jobs": len(state.execution_state.failed_jobs),
            "execution_history": len(state.execution_state.execution_history),
            "recorded_events": len(execution_events),
        }

    def _compact_semantic_result(self, result: Mapping[str, Any]) -> Dict[str, Any]:
        recommendations = result.get("recommendations", [])
        recommendation = recommendations[0] if recommendations else {}
        return {
            "import_graph": {
                "node_count": result.get("import_graph", {}).get("node_count", 0),
                "edge_count": result.get("import_graph", {}).get("edge_count", 0),
            },
            "architecture_graph": {
                "node_count": result.get("architecture_graph", {}).get("node_count", 0),
                "edge_count": result.get("architecture_graph", {}).get("edge_count", 0),
                "hotspots": result.get("architecture_graph", {}).get("hotspots", [])[:5],
            },
            "complexity": result.get("complexity", {}),
            "recommendation_count": len(recommendations),
            "top_recommendation": {
                "id": recommendation.get("id", ""),
                "title": recommendation.get("title", ""),
                "priority": recommendation.get("priority", ""),
            },
            "next_core": result.get("next_core", ""),
        }

    def _load_integrity_document(self) -> Dict[str, Any]:
        if not self.repository.integrity_path.exists():
            return {
                "schema_version": self.SCHEMA_VERSION,
                "state_sha256": "",
                "snapshot_history": [],
            }
        payload = json.loads(self.repository.integrity_path.read_text(encoding="utf-8"))
        payload.setdefault("snapshot_history", [])
        return self._sorted_mapping(payload)

    def _normalized_context(self, value: Mapping[str, Any]) -> Dict[str, Any]:
        return {key: value for key, value in self._sorted_mapping(value).items() if key in _RUNTIME_CONTEXT_KEYS or value not in (None, "")}

    def _sorted_mapping(self, value: Any) -> Any:
        if isinstance(value, Mapping):
            return {str(k): self._sorted_mapping(v) for k, v in sorted(value.items(), key=lambda item: str(item[0]))}
        if isinstance(value, tuple):
            return [self._sorted_mapping(item) for item in value]
        if isinstance(value, list):
            return [self._sorted_mapping(item) for item in value]
        return value

    def _atomic_write_json(self, path: Path, payload: Mapping[str, Any]):
        path.parent.mkdir(parents=True, exist_ok=True)
        content = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
        fd, tmp_path = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent))
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as fh:
                fh.write(content)
                fh.flush()
                os.fsync(fh.fileno())
            os.replace(tmp_path, path)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def _dedupe_strings(self, values: Iterable[str]) -> Tuple[str, ...]:
        seen = set()
        result = []
        for value in values:
            if not isinstance(value, str):
                continue
            cleaned = value.strip()
            if not cleaned or cleaned in seen:
                continue
            seen.add(cleaned)
            result.append(cleaned)
        return tuple(result)

    def _first_non_empty(self, *groups: Iterable[str]) -> str:
        for group in groups:
            for value in group:
                if value:
                    return value
        return ""

    def _utcnow(self) -> str:
        return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class DevelopmentStateEngine:
    """Public runtime API for CORE-009C orchestration."""

    def __init__(self, repository_root: Union[str, Path] = ".", manager: Optional[DevelopmentStateManager] = None, **manager_kwargs):
        self.repository_root = Path(repository_root).resolve()
        self.manager = manager or DevelopmentStateManager(self.repository_root, **manager_kwargs)

    def LoadCurrentState(self, create_if_missing: bool = False) -> Optional[DevelopmentState]:
        state = self.manager.LoadCurrentState()
        if state is None and create_if_missing:
            state = self._bootstrap_state()
            state = self.SaveCurrentState(state, source_event="bootstrap", refresh_integrations=False)
        return state

    def SaveCurrentState(
        self,
        state: DevelopmentState,
        *,
        create_snapshot: bool = False,
        snapshot_trigger: str = "runtime_update",
        source_event: str = "state_saved",
        snapshot_tags: Sequence[str] = (),
        timestamp: Optional[str] = None,
        event_payload: Optional[Mapping[str, Any]] = None,
        event_context: Optional[Mapping[str, Any]] = None,
        refresh_integrations: bool = False,
    ) -> DevelopmentState:
        return self.manager.SaveCurrentState(
            state,
            create_snapshot=create_snapshot,
            snapshot_trigger=snapshot_trigger,
            source_event=source_event,
            snapshot_tags=snapshot_tags,
            timestamp=timestamp,
            event_payload=event_payload,
            event_context=event_context,
            refresh_integrations=refresh_integrations,
        )

    def UpdateState(
        self,
        changes: Optional[Mapping[str, Any]] = None,
        *,
        timestamp: Optional[str] = None,
        create_snapshot: bool = False,
        snapshot_trigger: str = "state_update",
        source_event: str = "state_updated",
        refresh_integrations: bool = False,
        **kwargs,
    ) -> DevelopmentState:
        state = self.LoadCurrentState(create_if_missing=True)
        updates = dict(changes or {})
        updates.update(kwargs)
        runtime_context = {}

        workspace_updates: Dict[str, Any] = {}
        repository_updates: Dict[str, Any] = {}
        execution_updates: Dict[str, Any] = {}
        planning_updates: Dict[str, Any] = {}
        review_updates: Dict[str, Any] = {}
        owner_updates: Dict[str, Any] = {}
        telegram_updates: Dict[str, Any] = {}

        alias_map = {
            "current_workspace": ("workspace", "active_workspace"),
            "current_repository": ("repository", "repository"),
            "current_branch": ("repository", "branch"),
            "current_milestone": ("workspace", "current_milestone"),
            "current_epic": ("planning", "current_roadmap"),
            "current_batch": ("workspace", "current_batch"),
            "current_task": ("workspace", "current_task"),
            "current_executor": ("execution", "current_executor"),
            "current_recommendation": ("planning", "recommended_batch"),
        }
        section_lookup = {
            "workspace_state": workspace_updates,
            "repository_state": repository_updates,
            "execution_state": execution_updates,
            "planning_state": planning_updates,
            "review_state": review_updates,
            "owner_state": owner_updates,
            "telegram_state": telegram_updates,
        }

        for key, value in updates.items():
            if key in alias_map:
                section, field = alias_map[key]
                {
                    "workspace": workspace_updates,
                    "repository": repository_updates,
                    "execution": execution_updates,
                    "planning": planning_updates,
                }[section][field] = value
            elif key in ("current_issue", "current_pull_request", "current_canon_version"):
                runtime_context[key] = value
            elif key in section_lookup and isinstance(value, Mapping):
                section_lookup[key].update(value)
            else:
                runtime_context[key] = value

        updated = replace(
            state,
            workspace_state=replace(state.workspace_state, **workspace_updates) if workspace_updates else state.workspace_state,
            repository_state=replace(state.repository_state, **repository_updates) if repository_updates else state.repository_state,
            execution_state=replace(state.execution_state, **execution_updates) if execution_updates else state.execution_state,
            planning_state=replace(state.planning_state, **planning_updates) if planning_updates else state.planning_state,
            review_state=replace(state.review_state, **review_updates) if review_updates else state.review_state,
            owner_state=replace(state.owner_state, **owner_updates) if owner_updates else state.owner_state,
            telegram_state=replace(state.telegram_state, **telegram_updates) if telegram_updates else state.telegram_state,
        )
        return self.SaveCurrentState(
            updated,
            create_snapshot=create_snapshot,
            snapshot_trigger=snapshot_trigger,
            source_event=source_event,
            timestamp=timestamp,
            event_payload={"changes": self.manager._sorted_mapping(updates)},
            event_context=runtime_context,
            refresh_integrations=refresh_integrations,
        )

    def RecordExecution(
        self,
        execution_id: str,
        *,
        status: str,
        executor: Optional[str] = None,
        details: Optional[Mapping[str, Any]] = None,
        timestamp: Optional[str] = None,
    ) -> DevelopmentState:
        state = self.LoadCurrentState(create_if_missing=True)
        running = list(state.execution_state.running_jobs)
        completed = list(state.execution_state.completed_jobs)
        failed = list(state.execution_state.failed_jobs)
        queue = [job for job in state.execution_state.execution_queue if job != execution_id]
        retry_queue = list(state.execution_state.retry_queue)
        history = list(state.execution_state.execution_history)

        for bucket in (running, completed, failed, history):
            if execution_id in bucket and bucket is not history:
                bucket[:] = [value for value in bucket if value != execution_id]
        if execution_id not in history:
            history.append(execution_id)

        if status.upper() in {"RUNNING", "QUEUED"} and execution_id not in running:
            running.append(execution_id)
        elif status.upper() in {"COMPLETED", "SUCCESS", "SUCCEEDED"} and execution_id not in completed:
            completed.append(execution_id)
        elif status.upper() in {"FAILED", "ERROR"} and execution_id not in failed:
            failed.append(execution_id)
            if execution_id not in retry_queue:
                retry_queue.append(execution_id)

        updated = replace(
            state,
            execution_state=replace(
                state.execution_state,
                current_executor=executor or state.execution_state.current_executor,
                running_jobs=tuple(running),
                completed_jobs=tuple(completed),
                failed_jobs=tuple(failed),
                execution_queue=tuple(queue),
                retry_queue=tuple(retry_queue),
                execution_history=tuple(history),
            ),
        )
        return self.SaveCurrentState(
            updated,
            source_event="execution",
            timestamp=timestamp,
            event_payload={"execution_id": execution_id, "status": status, "details": dict(details or {})},
            event_context={"current_executor": executor or updated.execution_state.current_executor},
        )

    def RecordDecision(
        self,
        decision_id: str,
        *,
        decision: str,
        recommendation: Optional[str] = None,
        timestamp: Optional[str] = None,
        details: Optional[Mapping[str, Any]] = None,
    ) -> DevelopmentState:
        state = self.LoadCurrentState(create_if_missing=True)
        updated = replace(
            state,
            owner_state=replace(
                state.owner_state,
                manual_decisions=tuple(list(state.owner_state.manual_decisions) + [decision_id]),
            ),
            planning_state=replace(
                state.planning_state,
                recommended_batch=recommendation or state.planning_state.recommended_batch,
            ),
        )
        return self.SaveCurrentState(
            updated,
            create_snapshot=True,
            snapshot_trigger="owner_decision",
            source_event="decision",
            snapshot_tags=("decision", decision_id),
            timestamp=timestamp,
            event_payload={"decision_id": decision_id, "decision": decision, "details": dict(details or {})},
            event_context={"current_recommendation": recommendation or updated.planning_state.recommended_batch},
        )

    def RecordWorkspaceEvent(
        self,
        event_name: str,
        *,
        workspace: Optional[str] = None,
        milestone: Optional[str] = None,
        epic: Optional[str] = None,
        batch: Optional[str] = None,
        task: Optional[str] = None,
        timestamp: Optional[str] = None,
        details: Optional[Mapping[str, Any]] = None,
    ) -> DevelopmentState:
        state = self.LoadCurrentState(create_if_missing=True)
        updated = replace(
            state,
            workspace_state=replace(
                state.workspace_state,
                active_workspace=workspace or state.workspace_state.active_workspace,
                current_milestone=milestone or state.workspace_state.current_milestone,
                current_batch=batch or state.workspace_state.current_batch,
                current_task=task or state.workspace_state.current_task,
            ),
            planning_state=replace(
                state.planning_state,
                current_roadmap=epic or state.planning_state.current_roadmap,
            ),
        )
        return self.SaveCurrentState(
            updated,
            source_event="workspace_event",
            timestamp=timestamp,
            event_payload={"event_name": event_name, "details": dict(details or {})},
            event_context={
                "current_workspace": updated.workspace_state.active_workspace,
                "current_milestone": updated.workspace_state.current_milestone,
                "current_epic": updated.planning_state.current_roadmap,
                "current_batch": updated.workspace_state.current_batch,
                "current_task": updated.workspace_state.current_task,
            },
        )

    def RecordValidation(
        self,
        validation_id: str,
        *,
        status: str,
        findings: Sequence[str] = (),
        timestamp: Optional[str] = None,
    ) -> DevelopmentState:
        state = self.LoadCurrentState(create_if_missing=True)
        updated = replace(
            state,
            review_state=replace(
                state.review_state,
                testing_status=status,
                canonical_findings=tuple(list(state.review_state.canonical_findings) + list(findings)),
            ),
        )
        return self.SaveCurrentState(
            updated,
            source_event="validation",
            timestamp=timestamp,
            event_payload={"validation_id": validation_id, "status": status, "findings": list(findings)},
        )

    def RecordMerge(
        self,
        merge_id: str,
        *,
        branch: Optional[str] = None,
        head_commit: Optional[str] = None,
        timestamp: Optional[str] = None,
    ) -> DevelopmentState:
        state = self.LoadCurrentState(create_if_missing=True)
        updated = replace(
            state,
            repository_state=replace(
                state.repository_state,
                branch=branch or state.repository_state.branch,
                head_commit=head_commit or self._git_value("rev-parse", "HEAD") or state.repository_state.head_commit,
                latest_merge=merge_id,
            ),
        )
        return self.SaveCurrentState(
            updated,
            create_snapshot=True,
            snapshot_trigger="merge",
            source_event="merge",
            snapshot_tags=("merge", merge_id),
            timestamp=timestamp,
            event_payload={"merge_id": merge_id},
            event_context={"current_branch": updated.repository_state.branch},
        )

    def RecordPullRequest(
        self,
        pull_request_id: str,
        *,
        status: str = "OPEN",
        timestamp: Optional[str] = None,
    ) -> DevelopmentState:
        state = self.LoadCurrentState(create_if_missing=True)
        open_pull_requests = list(state.repository_state.open_pull_requests)
        open_prs = list(state.review_state.open_prs)
        pending = list(state.review_state.pending_reviews)
        if status.upper() in {"OPEN", "PENDING"}:
            if pull_request_id not in open_pull_requests:
                open_pull_requests.append(pull_request_id)
            if pull_request_id not in open_prs:
                open_prs.append(pull_request_id)
            if pull_request_id not in pending:
                pending.append(pull_request_id)
        else:
            open_pull_requests = [value for value in open_pull_requests if value != pull_request_id]
            open_prs = [value for value in open_prs if value != pull_request_id]
            pending = [value for value in pending if value != pull_request_id]
        updated = replace(
            state,
            repository_state=replace(state.repository_state, open_pull_requests=tuple(open_pull_requests)),
            review_state=replace(state.review_state, open_prs=tuple(open_prs), pending_reviews=tuple(pending)),
        )
        return self.SaveCurrentState(
            updated,
            create_snapshot=True,
            snapshot_trigger="pull_request",
            source_event="pull_request",
            snapshot_tags=("pull_request", pull_request_id),
            timestamp=timestamp,
            event_payload={"pull_request_id": pull_request_id, "status": status},
            event_context={"current_pull_request": pull_request_id},
        )

    def RecordIssue(
        self,
        issue_id: str,
        *,
        task: Optional[str] = None,
        status: str = "OPEN",
        timestamp: Optional[str] = None,
    ) -> DevelopmentState:
        state = self.LoadCurrentState(create_if_missing=True)
        updated = replace(
            state,
            workspace_state=replace(
                state.workspace_state,
                current_task=task or issue_id,
            ),
        )
        return self.SaveCurrentState(
            updated,
            source_event="issue",
            timestamp=timestamp,
            event_payload={"issue_id": issue_id, "status": status, "task": task or issue_id},
            event_context={"current_issue": issue_id, "current_task": task or issue_id},
        )

    def RecordBatch(
        self,
        batch_id: str,
        *,
        status: str = "ACTIVE",
        recommendation: Optional[str] = None,
        timestamp: Optional[str] = None,
    ) -> DevelopmentState:
        state = self.LoadCurrentState(create_if_missing=True)
        updated = replace(
            state,
            workspace_state=replace(state.workspace_state, current_batch=batch_id),
            planning_state=replace(
                state.planning_state,
                recommended_batch=recommendation or state.planning_state.recommended_batch,
            ),
        )
        return self.SaveCurrentState(
            updated,
            create_snapshot=True,
            snapshot_trigger="batch_completion" if status.upper() == "COMPLETED" else "batch_update",
            source_event="batch",
            snapshot_tags=("batch", batch_id, status.lower()),
            timestamp=timestamp,
            event_payload={"batch_id": batch_id, "status": status},
            event_context={
                "current_batch": batch_id,
                "current_recommendation": recommendation or updated.planning_state.recommended_batch,
            },
        )

    def GenerateExecutiveSnapshot(self, *, refresh_integrations: bool = True, timestamp: Optional[str] = None) -> DevelopmentStateSnapshot:
        state = self.LoadCurrentState(create_if_missing=True)
        return self.manager.WriteExecutiveSnapshot(state, refresh_integrations=refresh_integrations, timestamp=timestamp)

    def _bootstrap_state(self) -> DevelopmentState:
        timestamp = self.manager._utcnow()
        branch = self._git_value("rev-parse", "--abbrev-ref", "HEAD") or "UNKNOWN"
        head_commit = self._git_value("rev-parse", "HEAD") or "UNKNOWN"
        repository_name = self._git_value("config", "--get", "remote.origin.url") or self.repository_root.name
        identifier_seed = f"{self.repository_root}-{branch}-{head_commit}"
        identifier = hashlib.sha256(str(identifier_seed).encode("utf-8")).hexdigest()[:12].upper()
        return DevelopmentState(
            identifier=f"DEV-{identifier}",
            workspace_state=WorkspaceState(
                identifier="WS-001",
                active_project=self.repository_root.name,
                active_workspace=self.repository_root.name,
                current_milestone="UNSPECIFIED",
                current_batch="UNSPECIFIED",
                current_task="UNSPECIFIED",
                completed_tasks=(),
                blocked_tasks=(),
                current_objective="",
                estimated_progress=0.0,
            ),
            repository_state=RepositoryState(
                identifier="REPO-001",
                repository=repository_name,
                branch=branch,
                head_commit=head_commit,
                open_pull_requests=(),
                latest_merge="",
                tags=(),
                release="",
                repository_health="UNKNOWN",
            ),
            execution_state=ExecutionState(
                identifier="EXEC-001",
                current_executor="runtime",
                running_jobs=(),
                completed_jobs=(),
                failed_jobs=(),
                execution_queue=(),
                retry_queue=(),
                execution_history=(),
            ),
            planning_state=PlanningState(
                identifier="PLAN-001",
                current_roadmap="UNSPECIFIED",
                current_sprint="UNSPECIFIED",
                recommended_batch="UNSPECIFIED",
                priority_queue=(),
                estimated_roi=0.0,
                estimated_time=0.0,
                dependencies=(),
            ),
            review_state=ReviewState(
                identifier="REV-001",
                pending_reviews=(),
                open_prs=(),
                architecture_findings=(),
                canonical_findings=(),
                testing_status="UNKNOWN",
                approval_status="PENDING",
            ),
            owner_state=OwnerState(
                identifier="OWN-001",
                owner_priorities=(),
                manual_decisions=(),
                overrides=(),
                pinned_tasks=(),
                deferred_tasks=(),
            ),
            telegram_state=TelegramState(
                identifier="TG-001",
                session_id="UNBOUND",
                chat_id="UNBOUND",
                active_thread="",
                last_message_at="",
                subscribed_channels=(),
                pending_notifications=(),
            ),
            snapshot_metadata=SnapshotMetadata(
                identifier="SNAP-000000",
                trigger="bootstrap",
                created_at=timestamp,
                source_event="bootstrap",
                sequence_number=0,
                tags=("bootstrap",),
            ),
            integrity_report=IntegrityReport(
                identifier="INT-001",
                repository_integrity=100.0,
                canonical_integrity=100.0,
                memory_integrity=100.0,
                execution_integrity=100.0,
                planning_integrity=100.0,
                resume_integrity=100.0,
                overall_context_integrity_score=100.0,
            ),
        )

    def _git_value(self, *args: str) -> str:
        try:
            result = subprocess.run(
                ["git", *args],
                cwd=str(self.repository_root),
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                text=True,
            )
            return result.stdout.strip()
        except Exception:
            return ""

"""
Development State Engine — Persistence Layer
CORE-009B
"""

import hashlib
import json
import os
import re
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Union

from .models import DevelopmentState, MODEL_VERSION


class DevelopmentStateRepository:
    """Persistence repository for DevelopmentState."""

    CURRENT_SCHEMA_VERSION = MODEL_VERSION
    _LEGACY_NO_VERSION = "0.0.0"

    def __init__(self, repository_root: Union[str, Path] = "."):
        self.repository_root = Path(repository_root).resolve()
        self.base_dir = self.repository_root / ".ai" / "development_state"
        self.current_state_path = self.base_dir / "current_state.json"
        self.snapshots_dir = self.base_dir / "snapshots"
        self.integrity_path = self.base_dir / "integrity.json"

    # ------------------------------------------------------------------
    # Public API (requested interface)
    # ------------------------------------------------------------------

    def LoadState(self) -> Optional[DevelopmentState]:
        """Load current state with integrity verification and migration."""
        if not self.current_state_path.exists():
            return None

        payload = self._read_json(self.current_state_path)
        payload = self._migrate_payload(payload)

        self.VerifyIntegrity(payload)
        return DevelopmentState.from_dict(payload)

    def SaveState(self, state: DevelopmentState) -> Path:
        """Persist current state using atomic deterministic writes."""
        state.validate()
        payload = state.to_dict()
        payload["schema_version"] = self.CURRENT_SCHEMA_VERSION

        self._ensure_layout()
        serialized = self._serialize(payload)
        self._atomic_write_text(self.current_state_path, serialized)

        current_integrity = self._safe_read_integrity()
        history = current_integrity.get("snapshot_history", [])
        self._write_integrity(payload, history)

        return self.current_state_path

    def CreateSnapshot(self) -> Path:
        """Create immutable snapshot from current state and track history."""
        state = self.LoadState()
        if state is None:
            raise ValueError("No current development state found")

        payload = state.to_dict()
        snapshot_name = self._snapshot_filename(
            state.snapshot_metadata.identifier,
            state.snapshot_metadata.sequence_number,
        )
        snapshot_path = self.snapshots_dir / snapshot_name

        self._ensure_layout()
        self._atomic_write_text(snapshot_path, self._serialize(payload))

        integrity = self._safe_read_integrity()
        history: List[Dict[str, Any]] = list(integrity.get("snapshot_history", []))
        entry = {
            "snapshot_id": state.snapshot_metadata.identifier,
            "sequence_number": state.snapshot_metadata.sequence_number,
            "file": snapshot_name,
            "state_sha256": self._hash_payload(payload),
        }
        if not any(item.get("file") == snapshot_name for item in history):
            history.append(entry)
            history.sort(key=lambda x: (int(x.get("sequence_number", 0)), x.get("file", "")))

        self._write_integrity(payload, history)
        return snapshot_path

    def RestoreSnapshot(self, snapshot_reference: str) -> DevelopmentState:
        """Restore current state from snapshot id, snapshot filename, or path."""
        snapshot_path = self._resolve_snapshot_path(snapshot_reference)
        payload = self._migrate_payload(self._read_json(snapshot_path))
        state = DevelopmentState.from_dict(payload)
        self.SaveState(state)
        return state

    def ExportState(self, target_path: Union[str, Path]) -> Path:
        """Export current state JSON to an external path."""
        state = self.LoadState()
        if state is None:
            raise ValueError("No current development state found")

        export_path = Path(target_path)
        if not export_path.is_absolute():
            export_path = (self.repository_root / export_path).resolve()

        self._atomic_write_text(export_path, self._serialize(state.to_dict()))
        return export_path

    def ImportState(self, source_path: Union[str, Path]) -> DevelopmentState:
        """Import state JSON from external path with migration support."""
        source = Path(source_path)
        if not source.is_absolute():
            source = (self.repository_root / source).resolve()

        payload = self._migrate_payload(self._read_json(source))
        state = DevelopmentState.from_dict(payload)
        self.SaveState(state)
        return state

    def VerifyIntegrity(self, payload: Optional[Mapping[str, Any]] = None) -> bool:
        """Verify current state hash against integrity metadata."""
        if payload is None:
            if not self.current_state_path.exists():
                return True
            payload = self._migrate_payload(self._read_json(self.current_state_path))

        integrity = self._read_json(self.integrity_path)
        expected = integrity.get("state_sha256")
        if not isinstance(expected, str) or not expected:
            raise ValueError("Integrity file missing state hash")

        actual = self._hash_payload(payload)
        if actual != expected:
            raise ValueError("Integrity verification failed for development state")

        return True

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _ensure_layout(self):
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.snapshots_dir.mkdir(parents=True, exist_ok=True)

    def _serialize(self, payload: Mapping[str, Any]) -> str:
        return json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"

    def _hash_payload(self, payload: Mapping[str, Any]) -> str:
        return hashlib.sha256(self._serialize(payload).encode("utf-8")).hexdigest()

    def _atomic_write_text(self, path: Path, content: str):
        path.parent.mkdir(parents=True, exist_ok=True)
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

    def _read_json(self, path: Path) -> Dict[str, Any]:
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON at {path}") from exc

    def _safe_read_integrity(self) -> Dict[str, Any]:
        if not self.integrity_path.exists():
            return {"schema_version": self.CURRENT_SCHEMA_VERSION, "snapshot_history": []}
        return self._read_json(self.integrity_path)

    def _write_integrity(self, payload: Mapping[str, Any], snapshot_history: List[Dict[str, Any]]):
        integrity_payload = {
            "schema_version": self.CURRENT_SCHEMA_VERSION,
            "state_sha256": self._hash_payload(payload),
            "snapshot_history": snapshot_history,
        }
        self._atomic_write_text(self.integrity_path, self._serialize(integrity_payload))

    def _snapshot_filename(self, snapshot_id: str, sequence_number: int) -> str:
        clean_id = re.sub(r"[^a-zA-Z0-9_.-]", "_", snapshot_id)
        return f"{sequence_number:06d}__{clean_id}.json"

    def _resolve_snapshot_path(self, snapshot_reference: str) -> Path:
        candidate = Path(snapshot_reference)
        if candidate.is_absolute() and candidate.exists():
            return candidate

        by_name = self.snapshots_dir / snapshot_reference
        if by_name.exists():
            return by_name

        if candidate.suffix != ".json":
            name_matches = sorted(self.snapshots_dir.glob(f"*__{snapshot_reference}.json"))
            if name_matches:
                return name_matches[-1]

        integrity = self._safe_read_integrity()
        history = integrity.get("snapshot_history", [])
        for entry in reversed(history):
            if entry.get("snapshot_id") == snapshot_reference:
                path = self.snapshots_dir / str(entry.get("file", ""))
                if path.exists():
                    return path

        raise ValueError(f"Snapshot not found: {snapshot_reference}")

    def _migrate_payload(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        version = payload.get("schema_version")
        if not version:
            version = self._LEGACY_NO_VERSION

        if version == self.CURRENT_SCHEMA_VERSION:
            return payload

        if version not in {"0.9.0", self._LEGACY_NO_VERSION}:
            raise ValueError(f"Unsupported development state schema version: {version}")

        migrated = dict(payload)
        migrated["schema_version"] = self.CURRENT_SCHEMA_VERSION
        for key in (
            "workspace_state",
            "repository_state",
            "execution_state",
            "planning_state",
            "review_state",
            "owner_state",
            "telegram_state",
            "snapshot_metadata",
            "integrity_report",
        ):
            if key in migrated and isinstance(migrated[key], dict):
                nested = dict(migrated[key])
                if not nested.get("schema_version"):
                    nested["schema_version"] = self.CURRENT_SCHEMA_VERSION
                migrated[key] = nested

        return migrated

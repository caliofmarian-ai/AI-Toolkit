from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from .chat_models import ChatAttachment


class AttachmentStore:
    """Persist chat attachments locally and deduplicate by content hash."""

    def __init__(self, repository_root: str = ".", storage_root: Optional[str] = None) -> None:
        self.repository_root = Path(repository_root).resolve()
        self.storage_dir = Path(storage_root).resolve() if storage_root else self.repository_root / ".ai" / "attachments"
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.index_path = self.storage_dir / "index.json"
        self._registry: Dict[str, Dict[str, Any]] = self._load_registry()

    def _load_registry(self) -> Dict[str, Dict[str, Any]]:
        if not self.index_path.exists():
            return {}
        try:
            payload = json.loads(self.index_path.read_text(encoding="utf-8"))
            if isinstance(payload, dict):
                return payload
        except (OSError, ValueError):
            pass
        return {}

    def _save_registry(self) -> None:
        self.index_path.write_text(json.dumps(self._registry, indent=2, sort_keys=True), encoding="utf-8")

    def _build_storage_path(self, sha256: str, original_name: str) -> Path:
        suffix = ""
        if "." in original_name:
            suffix = Path(original_name).suffix
        return self.storage_dir / f"{sha256}{suffix}"

    def _dedup_key(self, content: bytes) -> str:
        return hashlib.sha256(content).hexdigest()

    def add_attachment(
        self,
        *,
        session_id: str,
        original_name: str,
        content: Union[bytes, str],
        mime_type: str = "application/octet-stream",
        linked_thread_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        ocr_text: Optional[str] = None,
        preview_url: Optional[str] = None,
    ) -> ChatAttachment:
        payload = content.encode("utf-8") if isinstance(content, str) else bytes(content)
        sha256 = self._dedup_key(payload)

        if sha256 in self._registry:
            existing = self._registry[sha256]
            attachment = ChatAttachment.from_dict(existing)
            return attachment

        storage_path = self._build_storage_path(sha256, original_name)
        storage_path.write_bytes(payload)

        attachment = ChatAttachment(
            id="",
            session_id=session_id,
            original_name=original_name,
            mime_type=mime_type,
            size=len(payload),
            sha256=sha256,
            storage_path=str(storage_path),
            ocr_text=ocr_text,
            preview_url=preview_url,
            linked_thread_id=linked_thread_id,
            metadata=dict(metadata or {}),
        )
        self._registry[sha256] = attachment.to_dict()
        self._save_registry()
        return attachment

    def get_attachment(self, attachment_id: str) -> Optional[ChatAttachment]:
        for item in self._registry.values():
            if str(item.get("id")) == str(attachment_id):
                return ChatAttachment.from_dict(item)
        return None

    def get_attachment_by_hash(self, sha256: str) -> Optional[ChatAttachment]:
        item = self._registry.get(sha256)
        if not item:
            return None
        return ChatAttachment.from_dict(item)

    def list_attachments(self, session_id: Optional[str] = None) -> List[ChatAttachment]:
        items: List[ChatAttachment] = []
        for value in self._registry.values():
            attachment = ChatAttachment.from_dict(value)
            if session_id is None or attachment.session_id == session_id:
                items.append(attachment)
        return items

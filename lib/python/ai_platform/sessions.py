from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Mapping
from uuid import uuid4


class AISessionEngine:
    def __init__(self, repository_root: str = ".") -> None:
        self.root = Path(repository_root).resolve()
        self.dir = self.root / ".ai" / "ai_sessions"

    def create(self, payload: Mapping[str, Any]) -> Dict[str, Any]:
        now = datetime.now(timezone.utc).isoformat()
        session = {
            "id": payload.get("id", f"AI-SESSION-{uuid4().hex[:12].upper()}"),
            "project": payload.get("project", self.root.name),
            "repository": payload.get("repository", self.root.name),
            "branch": payload.get("branch", ""),
            "issue": payload.get("issue", ""),
            "epic": payload.get("epic", ""),
            "sprint": payload.get("sprint", ""),
            "workspace": payload.get("workspace", ""),
            "repository_profile": payload.get("repository_profile", {}),
            "engineering_context": payload.get("engineering_context", {}),
            "selected_provider": payload.get("selected_provider", ""),
            "selected_model": payload.get("selected_model", ""),
            "prompt_history": list(payload.get("prompt_history", [])),
            "conversation_history": list(payload.get("conversation_history", [])),
            "token_usage": list(payload.get("token_usage", [])),
            "created_at": payload.get("created_at", now),
            "updated_at": now,
        }
        self._save(session)
        return session

    def list_sessions(self) -> List[Dict[str, Any]]:
        if not self.dir.exists():
            return []
        items = []
        for path in sorted(self.dir.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True):
            session = self._read(path)
            if session:
                items.append(session)
        return items

    def get(self, session_id: str) -> Dict[str, Any]:
        path = self.dir / f"{session_id}.json"
        return self._read(path)

    def append_interaction(self, session_id: str, question: str, answer: str, usage: Mapping[str, Any]) -> Dict[str, Any]:
        session = self.get(session_id)
        if not session:
            raise ValueError(f"unknown session {session_id}")
        now = datetime.now(timezone.utc).isoformat()
        session.setdefault("prompt_history", []).append(question)
        session.setdefault("conversation_history", []).append({"question": question, "answer": answer, "timestamp": now})
        session.setdefault("token_usage", []).append(dict(usage))
        session["updated_at"] = now
        self._save(session)
        return session

    def _save(self, session: Mapping[str, Any]) -> None:
        self.dir.mkdir(parents=True, exist_ok=True)
        path = self.dir / f"{session['id']}.json"
        path.write_text(json.dumps(dict(session), indent=2), encoding="utf-8")

    def _read(self, path: Path) -> Dict[str, Any]:
        if not path.exists():
            return {}
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return {}

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
            "raw_sources": list(payload.get("raw_sources", [])),
            "experience_id": payload.get("experience_id", ""),
            "journey_reference": dict(
                payload.get("journey_reference", {})
            ),
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

    def bind_experience(
        self,
        session_id: str,
        experience_id: str,
    ) -> Dict[str, Any]:
        session = self.get(session_id)
        if not session:
            raise ValueError(f"unknown session {session_id}")

        existing = str(session.get("experience_id", "")).strip()
        if existing and existing != experience_id:
            raise ValueError(
                f"session {session_id} already belongs to Experience {existing}"
            )

        session["experience_id"] = experience_id
        session["updated_at"] = datetime.now(timezone.utc).isoformat()
        self._save(session)
        return session

    def bind_journey(
        self,
        session_id: str,
        journey: Mapping[str, Any],
    ) -> Dict[str, Any]:
        """Persist only the cognitive Journey reference owned by a session."""
        session = self.get(session_id)

        if not session:
            raise ValueError(f"unknown session {session_id}")

        if not isinstance(journey, Mapping):
            raise TypeError("journey must be a mapping")

        journey_id = str(
            journey.get("journey_id", "")
        ).strip()

        need_id = str(
            journey.get("need_id", "")
        ).strip()

        if not journey_id:
            raise ValueError("journey_id must not be empty")

        if not need_id:
            raise ValueError("journey need_id must not be empty")

        reference = {
            "journey_id": journey_id,
            "need_id": need_id,
            "status": str(
                journey.get("status", "UNKNOWN")
            ).strip() or "UNKNOWN",
            "step_count": int(
                journey.get("step_count", 0)
            ),
            "epistemic_gain": bool(
                journey.get("epistemic_gain", False)
            ),
            "stopping_reason": str(
                journey.get("stopping_reason", "")
            ),
        }

        # A Conversation is durable across multiple human requests.
        # Each request may legitimately begin a new Journey.
        # The session therefore owns the CURRENT Journey reference;
        # Journey identity is not the lifetime identity of Conversation.
        session["journey_reference"] = reference
        session["updated_at"] = (
            datetime.now(timezone.utc).isoformat()
        )

        self._save(session)

        return session

    def mark_journey_interruption(
        self,
        session_id: str,
        *,
        reason: str,
    ) -> Dict[str, Any]:
        """Persist a non-authoritative interruption checkpoint."""
        session = self.get(session_id)

        if not session:
            raise ValueError(f"unknown session {session_id}")

        reference = session.get(
            "journey_reference",
            {},
        )

        if not isinstance(reference, Mapping) or not reference:
            return session

        reason = str(reason).strip()

        if not reason:
            reason = "runtime-interruption"

        checkpoint = dict(reference)
        checkpoint["status"] = "INTERRUPTED"
        checkpoint["stopping_reason"] = reason
        checkpoint["authority_conferred"] = False
        checkpoint["human_authority_preserved"] = True
        checkpoint["restart_recoverable"] = True

        session["journey_reference"] = checkpoint
        session["updated_at"] = (
            datetime.now(timezone.utc).isoformat()
        )

        self._save(session)

        return session

    def journey_reference(
        self,
        session_id: str,
    ) -> Dict[str, Any]:
        """Read the compact Journey reference owned by a session."""
        session = self.get(session_id)

        if not session:
            raise ValueError(f"unknown session {session_id}")

        reference = session.get(
            "journey_reference",
            {},
        )

        if not isinstance(reference, Mapping):
            return {}

        return dict(reference)

    def append_raw_source(
        self,
        session_id: str,
        source: Mapping[str, Any],
    ) -> Dict[str, Any]:
        session = self.get(session_id)
        if not session:
            raise ValueError(f"unknown session {session_id}")

        item = dict(source)

        if item.get("session_id") != session_id:
            raise ValueError("raw source session identity mismatch")

        sources = session.setdefault("raw_sources", [])
        expected_sequence = len(sources) + 1

        if item.get("sequence") != expected_sequence:
            raise ValueError(
                "raw source temporal sequence does not continue session order"
            )

        sources.append(item)
        session["updated_at"] = datetime.now(timezone.utc).isoformat()
        self._save(session)
        return session

    def conversation_sources(
        self,
        session_id: str,
    ) -> List[Dict[str, Any]]:
        session = self.get(session_id)
        if not session:
            raise ValueError(f"unknown session {session_id}")
        return list(session.get("raw_sources", []))

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

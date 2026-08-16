"""
FUSION-02 — durable AI conversation / Persistent Experience integration.

This module is relational tissue between existing organs.

It does NOT create:
- another AI session engine;
- another Experience model;
- another Provenance system;
- another memory architecture;
- Evidence from conversation;
- Canon from conversation;
- Sedimentation from conversation.

Epistemic distinctions remain explicit:

RAW CONVERSATION != Evidence
RAW CONVERSATION != Claim
RAW CONVERSATION != Knowledge
RAW CONVERSATION != Canon
AI statement != Evidence
Persistence != authority
"""

from __future__ import annotations

from dataclasses import asdict, replace
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping
from uuid import uuid4

from python.epistemic.provenance import Source
from python.experience.deployment import prepare_experience_repository
from python.experience.identity import ExperienceId
from python.experience.model import Experience
from python.experience.session_binding import SessionBinding


class ConversationExperienceBridge:
    """Connect existing AI Session physiology to existing Experience physiology."""

    def __init__(self, repository_root: str | Path = ".") -> None:
        self.repository_root = Path(repository_root).resolve()
        self.experiences = prepare_experience_repository(
            repository_root=self.repository_root,
        )

    def ensure_experience(
        self,
        session: Mapping[str, Any],
    ) -> tuple[Experience, SessionBinding]:
        session_id = str(session.get("id", "")).strip()
        if not session_id:
            raise ValueError("AI session requires stable identity")

        existing = str(session.get("experience_id", "")).strip()

        if existing:
            experience_id = ExperienceId(existing)
            experience = self.experiences.get(experience_id)
        else:
            experience = Experience.create().activate()
            self.experiences.add(experience)

        binding = SessionBinding.create(
            session_id=session_id,
            experience_id=experience.experience_id,
        )

        return experience, binding

    @staticmethod
    def raw_source(
        *,
        session: Mapping[str, Any],
        experience: Experience,
        actor: str,
        content: str,
        sequence: int,
        provider: str = "",
        model: str = "",
    ) -> dict[str, Any]:
        actor = actor.strip().upper()
        if actor not in {"HUMAN", "AI"}:
            raise ValueError("raw conversation actor must be HUMAN or AI")

        if not isinstance(content, str) or not content:
            raise ValueError("raw conversation content must not be empty")

        session_id = str(session["id"])
        project = str(session.get("project", ""))
        repository = str(session.get("repository", ""))
        timestamp = datetime.now(timezone.utc).isoformat()

        event_id = (
            f"RAW-{session_id}-{sequence:06d}-"
            f"{uuid4().hex[:8].upper()}"
        )

        source = Source(
            identifier=event_id,
            title=f"{actor} raw conversation source",
            kind=actor,
            reference=(
                f"ai-session:{session_id}"
                f"#raw-source:{sequence}"
            ),
        )

        return {
            "event_id": event_id,
            "source": asdict(source),
            "source_semantics": "RAW_SOURCE_NOT_EVIDENCE",
            "session_id": session_id,
            "experience_id": str(experience.experience_id),
            "project": project,
            "repository": repository,
            "actor": actor,
            "sequence": sequence,
            "timestamp": timestamp,
            "content": content,
            "provider": provider,
            "model": model,
            "epistemic_status": {
                "raw_source": True,
                "evidence": False,
                "claim": False,
                "knowledge": False,
                "canon": False,
                "sedimentation": False,
                "automatic_authority": False,
            },
        }

    def recover_experience(
        self,
        experience_id: str,
    ) -> Experience:
        return self.experiences.get(ExperienceId(experience_id))

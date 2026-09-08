"""
FUSION-02 — bounded reconstruction of AI Partner conversation context.

This module connects already-existing physiology.

It does not create another:
- session engine;
- Experience repository;
- Provenance system;
- memory architecture;
- epistemic organism.

RAW conversation remains RAW source.

Context inclusion does not promote a source to Evidence, Claim,
Knowledge, Sedimentation, or Canon.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Mapping

from python.ai_platform.context_builder import AIContextBuilder


class ConversationContextReconstructor:
    """Build inspectable bounded context for the next AI Partner turn."""

    SCHEMA = "FUSION-02-CONVERSATION-CONTEXT-1"

    def __init__(
        self,
        repository_root: str | Path = ".",
        workspace_root: str | Path | None = None,
        *,
        max_raw_sources: int = 12,
        max_source_chars: int = 6000,
        max_handoff_sources: int = 4,
        max_handoff_chars: int = 12000,
    ) -> None:
        self.repository_root = Path(repository_root).resolve()
        self.workspace_root = (
            Path(workspace_root).resolve()
            if workspace_root
            else self.repository_root.parent
        )
        self.max_raw_sources = max(1, int(max_raw_sources))
        self.max_source_chars = max(256, int(max_source_chars))
        self.max_handoff_sources = max(1, int(max_handoff_sources))
        self.max_handoff_chars = max(512, int(max_handoff_chars))

        self.base_context_builder = AIContextBuilder(
            str(self.repository_root),
            str(self.workspace_root),
        )

        # Import locally to preserve the existing organism while avoiding
        # package-initialization recursion:
        #
        # runtime.organism
        # -> ai_platform.sessions
        # -> ai_platform.__init__
        # -> service
        # -> conversation_context
        #
        # This is topology control, not a second organism.
        from python.runtime.organism import EpistemicOrganismAccess

        self.organism = EpistemicOrganismAccess(self.repository_root)

    @staticmethod
    def _json_safe(value: Any) -> Any:
        json.dumps(value)
        return value

    def _bounded_raw_sources(
        self,
        sources: list[Mapping[str, Any]],
    ) -> list[dict[str, Any]]:
        bounded = []

        for source in sources[-self.max_raw_sources:]:
            item = dict(source)
            content = str(item.get("content", ""))

            if len(content) > self.max_source_chars:
                item["content"] = content[: self.max_source_chars]
                item["content_truncated"] = True
                item["original_content_chars"] = len(content)
            else:
                item["content_truncated"] = False

            bounded.append(item)

        return bounded

    def _bounded_handoff_sources(
        self,
        recovered: Mapping[str, Any],
    ) -> list[dict[str, Any]]:
        engineering_context = recovered.get("engineering_context", {})
        if not isinstance(engineering_context, Mapping):
            return []

        references = engineering_context.get("handoff_sources", [])
        if not isinstance(references, list):
            return []

        bounded: list[dict[str, Any]] = []

        for reference in references[-self.max_handoff_sources:]:
            if not isinstance(reference, Mapping):
                continue

            relative = str(reference.get("path", "")).strip()
            if not relative:
                continue

            target = (self.repository_root / relative).resolve()
            try:
                target.relative_to(self.repository_root)
            except ValueError:
                continue

            if not target.is_file():
                continue

            try:
                content = target.read_text(encoding="utf-8")
            except OSError:
                continue

            digest = hashlib.sha256(content.encode("utf-8")).hexdigest()
            expected = str(reference.get("content_sha256", "")).strip()
            integrity_verified = not expected or digest == expected

            item = dict(reference)
            item["content_sha256_observed"] = digest
            item["integrity_verified"] = integrity_verified
            item["content_truncated"] = False

            if not integrity_verified:
                item["content"] = ""
                item["integrity_error"] = "CONTENT_SHA256_MISMATCH"
                bounded.append(item)
                continue

            if len(content) > self.max_handoff_chars:
                item["content"] = content[: self.max_handoff_chars]
                item["content_truncated"] = True
                item["original_content_chars"] = len(content)
            else:
                item["content"] = content

            bounded.append(item)

        return bounded

    def _error_memory_context(self) -> dict[str, Any]:
        paths = [
            (
                self.repository_root
                / "work"
                / "implementation-reports"
                / "PCC-04"
                / "PCC-04_RUN006D_IMPORT_TOPOLOGY_RECOVERY.md"
            ),
            (
                self.repository_root
                / "work"
                / "implementation-reports"
                / "FUSION"
                / "FUSION_01_DEMONSTRATED_FAILURE_PRECEDENTS.md"
            ),
            (
                self.repository_root
                / "work"
                / "implementation-reports"
                / "FUSION"
                / "FUSION_02_TERMUX_EXECUTION_ERROR_MEMORY.md"
            ),
        ]

        available = []

        for path in paths:
            if path.exists():
                available.append(
                    {
                        "path": str(path.relative_to(self.repository_root)),
                        "semantics": "DEMONSTRATED_FAILURE_OR_RECOVERY_EVIDENCE",
                    }
                )

        return {
            "physiology": "demonstrated-failure history",
            "dedicated_executable_service": False,
            "available_precedents": available,
            "epistemic_status": "EVIDENCE_NOT_CANON",
        }

    def build(
        self,
        session_id: str,
        *,
        partner_identity: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        recovered = self.organism.conversation_session(session_id)
        raw_sources = self._bounded_raw_sources(
            list(recovered.get("raw_sources", []))
        )
        handoff_sources = self._bounded_handoff_sources(recovered)

        base = self.base_context_builder.build()
        organism_state = self.organism.state()

        partner = dict(partner_identity or {})

        if not partner:
            ai_sources = [
                source
                for source in raw_sources
                if source.get("actor") == "AI"
            ]

            latest_ai = ai_sources[-1] if ai_sources else {}

            partner = {
                "provider": latest_ai.get("provider", ""),
                "model": latest_ai.get("model", ""),
            }

        context = {
            "schema": self.SCHEMA,
            "bounded": {
                "max_raw_sources": self.max_raw_sources,
                "max_source_chars": self.max_source_chars,
                "raw_sources_included": len(raw_sources),
                "max_handoff_sources": self.max_handoff_sources,
                "max_handoff_chars": self.max_handoff_chars,
                "handoff_sources_included": len(handoff_sources),
            },
            "active_project": {
                "project": recovered.get("project", ""),
                "repository": recovered.get("repository", ""),
                "branch": base.get("current_branch", ""),
                "workspace": (
                    base.get("workspace", {}).get("workspace", "")
                    if isinstance(base.get("workspace"), dict)
                    else ""
                ),
            },
            "active_session": {
                "session_id": recovered.get("session_id"),
                "experience_id": (
                    recovered.get("experience", {}).get("experience_id")
                ),
            },
            "ai_partner": partner,
            "conversation": {
                "semantics": "RAW_SOURCE_NOT_EVIDENCE",
                "sources": raw_sources,
            },
            "handoff": {
                "semantics": "PROVENANCE_BEARING_EVIDENCE_INPUT_NOT_AUTHORITY",
                "sources": handoff_sources,
                "source_count": len(handoff_sources),
                "epistemic_status": {
                    "evidence_input": True,
                    "canon": False,
                    "layered_memory": False,
                    "persistent_experience": False,
                    "automatic_sedimentation": False,
                    "automatic_authority": False,
                    "human_authority_preserved": True,
                },
            },
            "persistent_experience": recovered.get("experience", {}),
            "provenance": {
                "semantics": (
                    "Source identity and origin are preserved; "
                    "context inclusion grants no epistemic authority."
                ),
                "sources": [
                    {
                        "event_id": source.get("event_id"),
                        "source": source.get("source", {}),
                        "actor": source.get("actor"),
                        "sequence": source.get("sequence"),
                        "timestamp": source.get("timestamp"),
                        "epistemic_status": source.get(
                            "epistemic_status", {}
                        ),
                    }
                    for source in raw_sources
                ],
                "handoff_sources": [
                    {
                        "path": source.get("path"),
                        "content_sha256": source.get("content_sha256"),
                        "integrity_verified": source.get(
                            "integrity_verified", False
                        ),
                        "classification": source.get("classification"),
                        "source_semantics": source.get("source_semantics"),
                    }
                    for source in handoff_sources
                ],
            },
            "error_memory": self._error_memory_context(),
            "organism": {
                "schema": organism_state.get("schema"),
                "layered_memory": organism_state.get(
                    "layered_memory", {}
                ),
                "persistent_experience": organism_state.get(
                    "persistent_experience", {}
                ),
                "provenance": organism_state.get("provenance", {}),
                "error_memory": organism_state.get("error_memory", {}),
                "human_authority": organism_state.get(
                    "human_authority", {}
                ),
                "migration_boundaries": organism_state.get(
                    "migration_boundaries", {}
                ),
            },
            "engineering": {
                "repository_profile": base.get(
                    "repository_profile", {}
                ),
                "repository_health": base.get(
                    "repository_health", {}
                ),
                "current_sprint": base.get("current_sprint", ""),
                "current_epic": base.get("current_epic", ""),
                "current_issue": base.get("current_issue", ""),
                "runtime_status": base.get("runtime_status", {}),
            },
            "epistemic_boundaries": {
                "raw_conversation_is_evidence": False,
                "raw_conversation_is_canon": False,
                "ai_statement_is_evidence": False,
                "handoff_context_is_canon": False,
                "handoff_context_is_memory": False,
                "handoff_context_grants_authority": False,
                "context_inclusion_grants_authority": False,
                "automatic_sedimentation": False,
                "human_authority_preserved": True,
            },
        }

        self._json_safe(context)
        return context

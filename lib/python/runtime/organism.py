"""
FUSION-01 — Controlled runtime-facing access to the existing epistemic organism.

This module is an access boundary, not a second organism.

It observes existing physiology without creating parallel epistemic ownership.
It does not create Canon, accept Sedimentation, replace CSL, resume PCC-06,
implement Living Project Image, implement Epic Thread, or fuse AISessionEngine.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from python.runtime.owner_access import OwnerAccessBoundary
from python.ai_platform.sessions import AISessionEngine
from python.experience.deployment import (
    experience_store_path,
    prepare_experience_repository,
)
from python.experience.identity import ExperienceId
from python.experience.repository import ExperienceNotFoundError
from python.ai_platform.historical_experience_recovery import (
    historical_continuity,
)

from python.experience.persistent_repository import (
    JsonFileExperienceRepository,
)
from python.epistemic.layered_memory import LayeredMemoryRepository
from python.epistemic.provenance import Provenance
from python.epistemic.sedimentation import (
    SedimentationAuthority,
    SedimentationRepository,
)


class EpistemicOrganismAccess:
    """Controlled read-oriented Runtime access to existing epistemic physiology."""

    def __init__(
        self,
        repository_root: str | Path = ".",
        *,
        state_root: str | Path | None = None,
    ) -> None:
        self.repository_root = Path(repository_root).resolve()
        self.state_root = (
            Path(state_root).expanduser().resolve()
            if state_root is not None
            else None
        )

        self.persistent_experience_repository_class = (
            JsonFileExperienceRepository
        )
        self.layered_memory_repository_class = LayeredMemoryRepository
        self.sedimentation_repository_class = SedimentationRepository
        self.provenance_class = Provenance
        self.owner_access = OwnerAccessBoundary()

    @property
    def memory_root(self) -> Path:
        return self.repository_root / "work" / "memory"

    def _persistent_experience_state(self) -> dict[str, Any]:
        return {
            "physiology": "JsonFileExperienceRepository",
            "implementation": (
                "lib.python.experience.persistent_repository."
                "JsonFileExperienceRepository"
            ),
            "runtime_reachable": True,
            "storage_state": "UNKNOWN",
            "reason": (
                "Persistent Experience physiology is executable and reachable, "
                "but FUSION-01 does not invent a production store path."
            ),
            "authority": "Persistence is not authority.",
        }

    def _layered_memory_state(self) -> dict[str, Any]:
        path = self.memory_root / "layered_memory.json"

        try:
            repository = LayeredMemoryRepository.load(self.memory_root)
            nodes = repository.layered_memory.nodes()

            return {
                "physiology": "LayeredMemoryRepository",
                "implementation": (
                    "lib.python.epistemic.layered_memory."
                    "LayeredMemoryRepository"
                ),
                "runtime_reachable": True,
                "persistent_body": str(
                    path.relative_to(self.repository_root)
                ),
                "persistent_body_exists": path.exists(),
                "node_count": len(nodes),
                "state": "AVAILABLE",
            }
        except Exception as exc:
            return {
                "physiology": "LayeredMemoryRepository",
                "implementation": (
                    "lib.python.epistemic.layered_memory."
                    "LayeredMemoryRepository"
                ),
                "runtime_reachable": True,
                "persistent_body": str(
                    path.relative_to(self.repository_root)
                ),
                "persistent_body_exists": path.exists(),
                "node_count": None,
                "state": "UNAVAILABLE",
                "error": f"{type(exc).__name__}: {exc}",
            }

    def _sedimentation_state(self) -> dict[str, Any]:
        path = self.memory_root / "sedimentation.json"

        try:
            repository = SedimentationRepository.load(self.memory_root)
            items = repository.all()

            counts = {
                authority.value: sum(
                    1
                    for item in items
                    if item.authority is authority
                )
                for authority in SedimentationAuthority
            }

            return {
                "physiology": "SedimentationRepository",
                "implementation": (
                    "lib.python.epistemic.sedimentation."
                    "SedimentationRepository"
                ),
                "runtime_reachable": True,
                "persistent_body": str(
                    path.relative_to(self.repository_root)
                ),
                "persistent_body_exists": path.exists(),
                "sedimentation_count": len(items),
                "authority_counts": counts,
                "state": "AVAILABLE",
                "human_authority": {
                    "preserved": True,
                    "automatic_acceptance": False,
                    "automatic_rejection": False,
                },
            }
        except Exception as exc:
            return {
                "physiology": "SedimentationRepository",
                "implementation": (
                    "lib.python.epistemic.sedimentation."
                    "SedimentationRepository"
                ),
                "runtime_reachable": True,
                "persistent_body": str(
                    path.relative_to(self.repository_root)
                ),
                "persistent_body_exists": path.exists(),
                "sedimentation_count": None,
                "authority_counts": None,
                "state": "UNAVAILABLE",
                "error": f"{type(exc).__name__}: {exc}",
                "human_authority": {
                    "preserved": True,
                    "automatic_acceptance": False,
                    "automatic_rejection": False,
                },
            }

    def _provenance_state(self) -> dict[str, Any]:
        Provenance()

        return {
            "physiology": "Provenance",
            "implementation": "lib.python.epistemic.provenance.Provenance",
            "runtime_reachable": True,
            "executable_anatomy": True,
            "persistent_runtime_state": "UNKNOWN",
            "reason": (
                "Existing Provenance anatomy is executable. "
                "FUSION-01 does not invent a persistence contract."
            ),
        }

    def _error_memory_state(self) -> dict[str, Any]:
        precedents = [
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

        available = [
            str(path.relative_to(self.repository_root))
            for path in precedents
            if path.exists()
        ]

        return {
            "physiology": (
                "Error Memory / demonstrated-failure history"
            ),
            "runtime_reachable": bool(available),
            "dedicated_executable_service": "UNKNOWN",
            "demonstrated_precedents": available,
            "precedent_count": len(available),
            "state": (
                "AVAILABLE_AS_EVIDENCE"
                if available
                else "UNKNOWN"
            ),
            "reason": (
                "Demonstrated failures and recoveries remain Evidence. "
                "No dedicated ErrorMemory service is fabricated."
            ),
            "epistemic_boundary": {
                "evidence_is_canon": False,
                "automatic_sedimentation": False,
                "human_authority_preserved": True,
            },
        }

    def conversation_session(
        self,
        session_id: str,
    ) -> dict[str, Any]:
        """
        Recover one existing AI session and its bound Persistent Experience.

        Raw sources remain raw sources.
        No Evidence, Claim, Knowledge, Sedimentation, or Canon is created.
        """
        sessions = AISessionEngine(
            str(self.repository_root),
            state_root=(
                str(self.state_root)
                if self.state_root is not None
                else None
            ),
        )
        session = sessions.get(session_id)

        if not session:
            raise ValueError(f"unknown session {session_id}")

        experience_id = str(
            session.get("experience_id", "")
        ).strip()

        experience_state: dict[str, Any]

        if experience_id:
            deployment_environment = (
                {
                    "AI_TOOLKIT_STATE_ROOT": str(
                        self.state_root
                    )
                }
                if self.state_root is not None
                else None
            )

            repository = prepare_experience_repository(
                environment=deployment_environment,
                repository_root=self.repository_root,
            )

            try:
                experience = repository.get(
                    ExperienceId(experience_id)
                )
            except ExperienceNotFoundError:
                continuity = historical_continuity(session)
                experience_state = {
                    "experience_id": str(continuity.experience_id),
                    "state": continuity.historical_state.value,
                    "created_at": None,
                    "recovered": True,
                    "historical_continuity": True,
                    "recovery_provenance": (
                        continuity.recovery_provenance
                    ),
                    "exact_created_at_recoverable": (
                        continuity.exact_created_at_recoverable
                    ),
                }
            else:
                experience_state = {
                    "experience_id": str(experience.experience_id),
                    "state": experience.state.value,
                    "created_at": experience.created_at.isoformat(),
                    "recovered": True,
                    "historical_continuity": False,
                }
        else:
            experience_state = {
                "experience_id": None,
                "state": "UNBOUND",
                "recovered": False,
            }

        return {
            "session_id": session["id"],
            "project": session.get("project", ""),
            "repository": session.get("repository", ""),
            "experience": experience_state,
            "raw_sources": list(
                session.get("raw_sources", [])
            ),
            "epistemic_boundaries": {
                "raw_source_is_evidence": False,
                "raw_source_is_canon": False,
                "ai_statement_is_evidence": False,
                "automatic_sedimentation": False,
                "human_authority_preserved": True,
            },
        }

    def state(self) -> dict[str, Any]:
        payload = {
            "schema": "FUSION-01-EPISTEMIC-ORGANISM-STATE-1",
            "boundary": {
                "name": type(self).__name__,
                "mode": "READ_ONLY_RUNTIME_OBSERVATION",
                "second_runtime": False,
                "second_server": False,
                "second_dashboard": False,
                "second_memory_architecture": False,
            },
            "persistent_experience": (
                self._persistent_experience_state()
            ),
            "layered_memory": self._layered_memory_state(),
            "sedimentation": self._sedimentation_state(),
            "provenance": self._provenance_state(),
            "error_memory": self._error_memory_state(),
            "human_authority": {
                "preserved": True,
                "runtime_may_accept_sedimentation": False,
                "runtime_may_mutate_canon": False,
                "runtime_may_replace_csl": False,
            },
            "owner_access": self.owner_access.public_state(),
            "migration_boundaries": {
                "pcc_06": "SUSPENDED_FOR_MIGRATION",
                "living_project_image": "DEFERRED",
                "epic_thread": "DEFERRED",
                "ai_session_engine_fusion": "FUSION_02_ACTIVE",
            },
        }

        json.dumps(payload, ensure_ascii=False, sort_keys=True)

        return payload

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

    def __init__(self, repository_root: str | Path = ".") -> None:
        self.repository_root = Path(repository_root).resolve()

        self.persistent_experience_repository_class = (
            JsonFileExperienceRepository
        )
        self.layered_memory_repository_class = LayeredMemoryRepository
        self.sedimentation_repository_class = SedimentationRepository
        self.provenance_class = Provenance

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
        precedent = (
            self.repository_root
            / "work"
            / "implementation-reports"
            / "PCC-04"
            / "PCC-04_RUN006D_IMPORT_TOPOLOGY_RECOVERY.md"
        )

        return {
            "physiology": (
                "Error Memory / demonstrated-failure history"
            ),
            "runtime_reachable": precedent.exists(),
            "dedicated_executable_service": "UNKNOWN",
            "demonstrated_precedent": (
                str(precedent.relative_to(self.repository_root))
                if precedent.exists()
                else None
            ),
            "state": (
                "AVAILABLE_AS_EVIDENCE"
                if precedent.exists()
                else "UNKNOWN"
            ),
            "reason": (
                "Historical demonstrated failure remains Evidence. "
                "No dedicated ErrorMemory service is fabricated."
            ),
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
            "migration_boundaries": {
                "pcc_06": "SUSPENDED_FOR_MIGRATION",
                "living_project_image": "DEFERRED",
                "epic_thread": "DEFERRED",
                "ai_session_engine_fusion": "DEFERRED_TO_FUSION_02",
            },
        }

        json.dumps(payload, ensure_ascii=False, sort_keys=True)

        return payload

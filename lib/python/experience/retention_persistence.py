"""Durable persistence physiology for PCC-01 Experience Retention.

Storage preserves the observable Retention state.
Storage does not create Retention authority and does not redefine
Experience identity.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any

from .identity import ExperienceId
from .retention import ExperienceRetention, RetentionState


class ExperienceRetentionPersistenceError(Exception):
    """Base error for durable Retention persistence."""


class ExperienceRetentionNotFoundError(
    ExperienceRetentionPersistenceError
):
    """Raised when durable Retention evidence does not exist."""


class ExperienceRetentionRepository:
    """Filesystem-backed durable repository for Retention state."""

    def __init__(self, root: str | Path) -> None:
        self._root = Path(root)

    def save(
        self,
        retention: ExperienceRetention,
    ) -> None:
        if not isinstance(retention, ExperienceRetention):
            raise TypeError(
                "retention must be an ExperienceRetention"
            )

        self._root.mkdir(parents=True, exist_ok=True)

        target = self._path(retention.experience_id)

        payload = {
            "experience_id": str(retention.experience_id),
            "state": retention.state.value,
            "reason": retention.reason,
            "retained_at": (
                retention.retained_at.isoformat()
                if retention.retained_at is not None
                else None
            ),
        }

        with NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=self._root,
            prefix=".retention-",
            suffix=".tmp",
            delete=False,
        ) as handle:
            temporary = Path(handle.name)
            json.dump(
                payload,
                handle,
                sort_keys=True,
                separators=(",", ":"),
            )
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())

        try:
            os.replace(temporary, target)
        finally:
            if temporary.exists():
                temporary.unlink()

    def load(
        self,
        experience_id: ExperienceId,
    ) -> ExperienceRetention:
        if not isinstance(experience_id, ExperienceId):
            raise TypeError(
                "experience_id must be an ExperienceId"
            )

        target = self._path(experience_id)

        if not target.is_file():
            raise ExperienceRetentionNotFoundError(
                f"no Retention state for Experience {experience_id}"
            )

        with target.open(
            "r",
            encoding="utf-8",
        ) as handle:
            payload: dict[str, Any] = json.load(handle)

        stored_id = ExperienceId.from_string(
            payload["experience_id"]
        )

        if stored_id != experience_id:
            raise ExperienceRetentionPersistenceError(
                "stored Retention identity does not match requested Experience"
            )

        state = RetentionState(payload["state"])

        if state is RetentionState.UNRETAINED:
            return ExperienceRetention.unretained(
                experience_id
            )

        from datetime import datetime

        retained_at_raw = payload["retained_at"]

        if not isinstance(retained_at_raw, str):
            raise ExperienceRetentionPersistenceError(
                "retained Retention state requires retained_at"
            )

        retained_at = datetime.fromisoformat(
            retained_at_raw
        )

        return ExperienceRetention(
            experience_id=stored_id,
            state=RetentionState.RETAINED,
            reason=payload["reason"],
            retained_at=retained_at,
        )

    def contains(
        self,
        experience_id: ExperienceId,
    ) -> bool:
        if not isinstance(experience_id, ExperienceId):
            raise TypeError(
                "experience_id must be an ExperienceId"
            )

        return self._path(experience_id).is_file()

    def _path(
        self,
        experience_id: ExperienceId,
    ) -> Path:
        return self._root / f"{experience_id}.json"

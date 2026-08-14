"""Durable evidence of controlled PCC-01 Experience Forgetting.

This repository conserves the fact that controlled forgetting occurred.

It deliberately does not pretend that missing storage equals forgetting.
Accidental absence and explicit forgetting remain epistemically distinct.
"""

from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any

from .forgetting import ExperienceForgetting, ForgettingState
from .identity import ExperienceId


class ExperienceForgettingPersistenceError(Exception):
    """Base error for durable Forgetting persistence."""


class ExperienceForgettingNotFoundError(
    ExperienceForgettingPersistenceError
):
    """No explicit forgetting record exists for this identity."""


class ExperienceForgettingRepository:
    """Filesystem-backed durable record of forgetting physiology."""

    def __init__(self, root: str | Path) -> None:
        self._root = Path(root)

    def save(
        self,
        forgetting: ExperienceForgetting,
    ) -> None:
        if not isinstance(forgetting, ExperienceForgetting):
            raise TypeError(
                "forgetting must be an ExperienceForgetting"
            )

        self._root.mkdir(parents=True, exist_ok=True)
        target = self._path(forgetting.experience_id)

        payload = {
            "experience_id": str(forgetting.experience_id),
            "state": forgetting.state.value,
            "reason": forgetting.reason,
            "forgotten_at": (
                forgetting.forgotten_at.isoformat()
                if forgetting.forgotten_at is not None
                else None
            ),
        }

        with NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=self._root,
            prefix=".forgetting-",
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
    ) -> ExperienceForgetting:
        if not isinstance(experience_id, ExperienceId):
            raise TypeError(
                "experience_id must be an ExperienceId"
            )

        target = self._path(experience_id)

        if not target.is_file():
            raise ExperienceForgettingNotFoundError(
                f"no explicit forgetting record for Experience {experience_id}"
            )

        with target.open("r", encoding="utf-8") as handle:
            payload: dict[str, Any] = json.load(handle)

        stored_id = ExperienceId.from_string(
            payload["experience_id"]
        )

        if stored_id != experience_id:
            raise ExperienceForgettingPersistenceError(
                "stored forgetting identity does not match requested Experience"
            )

        state = ForgettingState(payload["state"])

        if state is ForgettingState.PRESENT:
            return ExperienceForgetting.present(
                stored_id
            )

        forgotten_at_raw = payload["forgotten_at"]

        if not isinstance(forgotten_at_raw, str):
            raise ExperienceForgettingPersistenceError(
                "forgotten state requires forgotten_at"
            )

        return ExperienceForgetting(
            experience_id=stored_id,
            state=ForgettingState.FORGOTTEN,
            reason=payload["reason"],
            forgotten_at=datetime.fromisoformat(
                forgotten_at_raw
            ),
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

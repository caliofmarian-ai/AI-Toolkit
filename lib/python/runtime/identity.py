"""
CORE-021 — Runtime Identity
CANON-055 §8 — Runtime Identity

Every Runtime instance owns a unique Runtime Identifier that is
immutable during Runtime execution.
"""

import os
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class RuntimeIdentity:
    """Immutable identity for a Runtime instance."""

    runtime_id: str
    runtime_version: str
    build_version: str
    git_commit: str
    git_branch: str
    deployment_id: str
    railway_deployment_id: str
    workspace_id: str
    repository_id: str
    start_timestamp: str
    lifecycle_phase: str = "BOOT"

    @classmethod
    def create(cls) -> "RuntimeIdentity":
        """Create a new Runtime Identity from the environment."""
        now = datetime.now(timezone.utc).isoformat()
        runtime_id = os.environ.get("RUNTIME_ID") or f"runtime-{uuid.uuid4().hex[:12]}"
        return cls(
            runtime_id=runtime_id,
            runtime_version=os.environ.get("RUNTIME_VERSION", "3.0.0"),
            build_version=os.environ.get("BUILD_VERSION", "unknown"),
            git_commit=os.environ.get("RAILWAY_GIT_COMMIT_SHA", "unknown"),
            git_branch=os.environ.get("RAILWAY_GIT_BRANCH", "unknown"),
            deployment_id=os.environ.get("RAILWAY_DEPLOYMENT_ID", "local"),
            railway_deployment_id=os.environ.get("RAILWAY_DEPLOYMENT_ID", "local"),
            workspace_id=os.environ.get("WORKSPACE_ID", "default"),
            repository_id=os.environ.get("REPOSITORY_ID", "ai-toolkit"),
            start_timestamp=now,
        )

    def to_dict(self) -> dict:
        return {
            "runtime_id": self.runtime_id,
            "runtime_version": self.runtime_version,
            "build_version": self.build_version,
            "git_commit": self.git_commit,
            "git_branch": self.git_branch,
            "deployment_id": self.deployment_id,
            "railway_deployment_id": self.railway_deployment_id,
            "workspace_id": self.workspace_id,
            "repository_id": self.repository_id,
            "start_timestamp": self.start_timestamp,
            "lifecycle_phase": self.lifecycle_phase,
        }

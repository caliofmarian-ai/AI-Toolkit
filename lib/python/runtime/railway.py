"""
CORE-021 — Railway Bootstrap
CANON-056 — Railway Deployment Architecture

Provides Railway-specific startup logic:
- Reads RAILWAY_* environment variables
- Logs deployment identity
- Validates required Railway configuration

This module is invoked by the runtime-server entrypoint when deployed
on Railway.
"""

import logging
import os
from dataclasses import dataclass
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class RailwayDeploymentMetadata:
    """Metadata available from Railway environment variables."""

    is_railway: bool
    project_id: str
    service_id: str
    deployment_id: str
    environment: str
    environment_id: str
    git_commit_sha: str
    git_branch: str
    git_repository: str
    public_domain: str
    private_domain: str
    port: int

    def to_dict(self) -> dict:
        return {
            "is_railway": self.is_railway,
            "project_id": self.project_id,
            "service_id": self.service_id,
            "deployment_id": self.deployment_id,
            "environment": self.environment,
            "environment_id": self.environment_id,
            "git_commit_sha": self.git_commit_sha,
            "git_branch": self.git_branch,
            "git_repository": self.git_repository,
            "public_domain": self.public_domain,
            "private_domain": self.private_domain,
            "port": self.port,
        }


def load_railway_metadata() -> RailwayDeploymentMetadata:
    """Load Railway deployment metadata from environment variables."""
    repository_owner = os.environ.get(
        "RAILWAY_GIT_REPO_OWNER",
        "",
    ).strip()
    repository_name = os.environ.get(
        "RAILWAY_GIT_REPO_NAME",
        "",
    ).strip()
    repository = (
        repository_owner + "/" + repository_name
        if repository_owner and repository_name
        else repository_name
    )

    return RailwayDeploymentMetadata(
        is_railway=bool(os.environ.get("RAILWAY_ENVIRONMENT")),
        project_id=os.environ.get("RAILWAY_PROJECT_ID", "local"),
        service_id=os.environ.get("RAILWAY_SERVICE_ID", "local"),
        deployment_id=os.environ.get("RAILWAY_DEPLOYMENT_ID", "local"),
        environment=os.environ.get("RAILWAY_ENVIRONMENT", "local"),
        environment_id=os.environ.get(
            "RAILWAY_ENVIRONMENT_ID",
            "local",
        ),
        git_commit_sha=os.environ.get("RAILWAY_GIT_COMMIT_SHA", "unknown"),
        git_branch=os.environ.get("RAILWAY_GIT_BRANCH", "unknown"),
        git_repository=repository,
        public_domain=os.environ.get("RAILWAY_PUBLIC_DOMAIN", ""),
        private_domain=os.environ.get("RAILWAY_PRIVATE_DOMAIN", ""),
        port=int(os.environ.get("PORT", "8080")),
    )


def log_railway_identity(metadata: RailwayDeploymentMetadata) -> None:
    """Log Railway deployment identity at startup."""
    logger.info(
        "Railway deployment: project=%s service=%s deployment=%s env=%s commit=%s",
        metadata.project_id,
        metadata.service_id,
        metadata.deployment_id,
        metadata.environment,
        metadata.git_commit_sha[:8] if metadata.git_commit_sha != "unknown" else "unknown",
    )
    if metadata.public_domain:
        logger.info("Railway public domain: %s", metadata.public_domain)


class RailwayBootstrap:
    """
    Railway-specific bootstrap that enriches the Runtime with
    Railway deployment metadata.
    """

    def __init__(self):
        self._metadata: Optional[RailwayDeploymentMetadata] = None

    def initialize(self) -> RailwayDeploymentMetadata:
        """Load and log Railway deployment metadata."""
        self._metadata = load_railway_metadata()
        log_railway_identity(self._metadata)
        return self._metadata

    @property
    def metadata(self) -> Optional[RailwayDeploymentMetadata]:
        return self._metadata

    def is_railway(self) -> bool:
        """Return True when running inside a Railway deployment."""
        return bool(os.environ.get("RAILWAY_ENVIRONMENT"))

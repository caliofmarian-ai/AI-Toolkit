"""
CANON-081 Engineering Workspace

CORE-022 Engineering Workspace Kernel

Canonical Model Definitions

This module defines the canonical data model for the Engineering
Workspace. It intentionally contains no business logic.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional
from datetime import datetime


class WorkspaceStatus(Enum):
    UNKNOWN = "unknown"
    INITIALIZING = "initializing"
    READY = "ready"
    DEGRADED = "degraded"
    ERROR = "error"


class ServiceStatus(Enum):
    UNKNOWN = "unknown"
    REGISTERED = "registered"
    ACTIVE = "active"
    DISABLED = "disabled"
    FAILED = "failed"


class ProviderStatus(Enum):
    UNKNOWN = "unknown"
    AVAILABLE = "available"
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    FAILED = "failed"


@dataclass(slots=True)
class WorkspaceIdentity:
    workspace_id: str
    name: str
    version: str
    created_at: datetime
    repository_root: Optional[str] = None


@dataclass(slots=True)
class WorkspaceHealth:
    overall_status: WorkspaceStatus = WorkspaceStatus.UNKNOWN
    message: str = ""
    last_check: Optional[datetime] = None
    checks: Dict[str, str] = field(default_factory=dict)


@dataclass(slots=True)
class CapabilityDescriptor:
    capability_id: str
    name: str
    description: str = ""
    enabled: bool = True


@dataclass(slots=True)
class ProviderDescriptor:
    provider_id: str
    name: str
    provider_type: str
    status: ProviderStatus = ProviderStatus.UNKNOWN
    capabilities: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class ServiceDescriptor:
    service_id: str
    name: str
    service_type: str
    status: ServiceStatus = ServiceStatus.UNKNOWN
    dependencies: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class WorkspaceSession:
    session_id: str
    started_at: datetime
    user: str = "owner"
    current_repository: Optional[str] = None
    current_branch: Optional[str] = None
    current_issue: Optional[str] = None
    current_pull_request: Optional[str] = None
    current_batch: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class WorkspaceState:
    status: WorkspaceStatus = WorkspaceStatus.UNKNOWN
    providers: Dict[str, ProviderDescriptor] = field(default_factory=dict)
    services: Dict[str, ServiceDescriptor] = field(default_factory=dict)
    capabilities: Dict[str, CapabilityDescriptor] = field(default_factory=dict)
    sessions: Dict[str, WorkspaceSession] = field(default_factory=dict)


@dataclass(slots=True)
class EngineeringWorkspaceModel:
    identity: WorkspaceIdentity
    health: WorkspaceHealth = field(default_factory=WorkspaceHealth)
    state: WorkspaceState = field(default_factory=WorkspaceState)

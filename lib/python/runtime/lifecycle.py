"""
CORE-021 — Runtime Lifecycle Manager
CANON-055 §6 — Runtime Lifecycle

Manages the canonical lifecycle phases of the Runtime:

    BOOT → INITIALIZATION → CONFIGURATION → DEPENDENCY_VALIDATION
    → DISCOVERY → ENGINE_REGISTRATION → SERVICE_REGISTRATION
    → HEALTH_VERIFICATION → READY → RUNNING → SHUTDOWN
    → PERSISTENCE → TERMINATION

The Runtime shall never skip lifecycle phases.
"""

from enum import Enum
from typing import Callable, Dict, List, Optional


class LifecyclePhase(str, Enum):
    BOOT = "BOOT"
    INITIALIZATION = "INITIALIZATION"
    CONFIGURATION = "CONFIGURATION"
    DEPENDENCY_VALIDATION = "DEPENDENCY_VALIDATION"
    DISCOVERY = "DISCOVERY"
    ENGINE_REGISTRATION = "ENGINE_REGISTRATION"
    SERVICE_REGISTRATION = "SERVICE_REGISTRATION"
    HEALTH_VERIFICATION = "HEALTH_VERIFICATION"
    READY = "READY"
    RUNNING = "RUNNING"
    MAINTENANCE = "MAINTENANCE"
    RECOVERY = "RECOVERY"
    SHUTDOWN = "SHUTDOWN"
    PERSISTENCE = "PERSISTENCE"
    TERMINATION = "TERMINATION"


_PHASE_ORDER = [
    LifecyclePhase.BOOT,
    LifecyclePhase.INITIALIZATION,
    LifecyclePhase.CONFIGURATION,
    LifecyclePhase.DEPENDENCY_VALIDATION,
    LifecyclePhase.DISCOVERY,
    LifecyclePhase.ENGINE_REGISTRATION,
    LifecyclePhase.SERVICE_REGISTRATION,
    LifecyclePhase.HEALTH_VERIFICATION,
    LifecyclePhase.READY,
    LifecyclePhase.RUNNING,
]


class LifecycleManager:
    """
    Manages lifecycle phase transitions and registered phase listeners.
    """

    def __init__(self):
        self._phase: LifecyclePhase = LifecyclePhase.BOOT
        self._listeners: Dict[LifecyclePhase, List[Callable]] = {}
        self._phase_history: List[str] = [LifecyclePhase.BOOT.value]

    @property
    def current_phase(self) -> LifecyclePhase:
        return self._phase

    def transition(self, phase: LifecyclePhase) -> None:
        """Transition to *phase* and invoke registered listeners."""
        self._phase = phase
        self._phase_history.append(phase.value)
        for listener in self._listeners.get(phase, []):
            listener(phase)

    def on_phase(self, phase: LifecyclePhase, callback: Callable) -> None:
        """Register *callback* to be invoked when entering *phase*."""
        self._listeners.setdefault(phase, []).append(callback)

    def is_ready(self) -> bool:
        return self._phase in (LifecyclePhase.READY, LifecyclePhase.RUNNING)

    def is_running(self) -> bool:
        return self._phase == LifecyclePhase.RUNNING

    def is_shutdown(self) -> bool:
        return self._phase in (
            LifecyclePhase.SHUTDOWN,
            LifecyclePhase.PERSISTENCE,
            LifecyclePhase.TERMINATION,
        )

    def to_dict(self) -> dict:
        return {
            "current_phase": self._phase.value,
            "phase_history": list(self._phase_history),
            "is_ready": self.is_ready(),
            "is_running": self.is_running(),
        }

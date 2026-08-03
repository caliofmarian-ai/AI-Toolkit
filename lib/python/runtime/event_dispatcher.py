"""
CORE-021 — Runtime Event Dispatcher
CANON-055 §5

The Event Dispatcher implements a publish-subscribe event bus.
Runtime components publish events; handlers subscribed to an event
type are invoked synchronously in the dispatcher thread.
"""

import logging
import threading
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class RuntimeEvent:
    """A canonical Runtime event."""

    event_type: str
    source: str
    payload: Any = None
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    event_id: str = field(default_factory=lambda: __import__("uuid").uuid4().hex)

    def to_dict(self) -> dict:
        return {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "source": self.source,
            "timestamp": self.timestamp,
            "payload": self.payload,
        }


class EventDispatcher:
    """
    Synchronous publish-subscribe event dispatcher.

    Handlers are invoked in registration order.  Exceptions in handlers
    are caught and logged so that one failing handler does not prevent
    others from receiving the event.
    """

    def __init__(self):
        self._handlers: Dict[str, List[Callable[[RuntimeEvent], None]]] = {}
        self._event_count = 0
        self._lock = threading.Lock()

    def subscribe(self, event_type: str, handler: Callable[[RuntimeEvent], None]) -> None:
        """Subscribe *handler* to events of *event_type*."""
        with self._lock:
            self._handlers.setdefault(event_type, []).append(handler)

    def subscribe_all(self, handler: Callable[[RuntimeEvent], None]) -> None:
        """Subscribe *handler* to ALL event types."""
        self.subscribe("*", handler)

    def publish(self, event: RuntimeEvent) -> None:
        """Publish *event* to all matching handlers."""
        with self._lock:
            specific = list(self._handlers.get(event.event_type, []))
            wildcard = list(self._handlers.get("*", []))
            self._event_count += 1

        for handler in specific + wildcard:
            try:
                handler(event)
            except Exception as exc:
                logger.error(
                    "EventDispatcher: handler %s raised for %s: %s",
                    getattr(handler, "__name__", repr(handler)),
                    event.event_type,
                    exc,
                )

    def emit(self, event_type: str, source: str, payload: Any = None) -> RuntimeEvent:
        """Convenience helper: create and publish an event."""
        event = RuntimeEvent(event_type=event_type, source=source, payload=payload)
        self.publish(event)
        return event

    def summary(self) -> dict:
        with self._lock:
            return {
                "event_count": self._event_count,
                "subscribed_types": sorted(self._handlers.keys()),
                "handler_counts": {k: len(v) for k, v in self._handlers.items()},
            }

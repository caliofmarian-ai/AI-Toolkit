from __future__ import annotations

from typing import Callable


from lib.python.runtime.interfaces.api_auth import ApiAuth


class RuntimeApiRouter:

    def __init__(
        self,
        health: Callable[[], dict],
        runtime: Callable[[], dict],
        status: Callable[[], dict],
        metrics: Callable[[], dict],
    ):
        self._health = health
        self._runtime = runtime
        self._status = status
        self._metrics = metrics
        self.auth = ApiAuth()

    def runtime(self) -> dict:
        return self._runtime()

    def health(self) -> dict:
        return self._health()

    def status(self) -> dict:
        return self._status()

    def metrics(self) -> dict:
        return self._metrics()

    def reports(self) -> dict:
        return {
            "reports": [],
            "status": "not_implemented",
        }

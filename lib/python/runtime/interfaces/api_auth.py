from __future__ import annotations

import os


class ApiAuth:

    def __init__(self):
        self.api_key = os.getenv("RUNTIME_API_KEY", "")
        self.bearer = os.getenv("RUNTIME_BEARER_TOKEN", "")

    def authorized(self, headers) -> bool:

        if not self.api_key and not self.bearer:
            return True

        api_key = headers.get("X-API-Key", "")

        auth = headers.get("Authorization", "")

        if self.api_key and api_key == self.api_key:
            return True

        if self.bearer and auth == f"Bearer {self.bearer}":
            return True

        return False

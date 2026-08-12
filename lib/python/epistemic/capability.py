"""
Epistemic Capability Model

A capability is the smallest demonstrable unit of evolution.
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Capability:

    identifier: str

    name: str

    description: str

    acquired_from: str

    acquired_at: str

    verified: bool = False


class CapabilityRegistry:

    def __init__(self):

        self._capabilities = []

    def acquire(self, capability):

        self._capabilities.append(capability)

    def list(self):

        return self._capabilities

    def exists(self, identifier):

        return any(c.identifier == identifier for c in self._capabilities)


if __name__ == "__main__":

    registry = CapabilityRegistry()

    registry.acquire(

        Capability(

            identifier="CAP-0001",

            name="I VERIFY MYSELF",

            description="The organism can verify its own structural integrity.",

            acquired_from="Bootstrap",

            acquired_at=datetime.utcnow().isoformat(),

            verified=False,

        )

    )

    print()

    print("Capabilities")

    print("============")

    for capability in registry.list():

        print(capability)


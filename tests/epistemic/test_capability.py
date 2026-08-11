from lib.python.epistemic.capability import Capability
from lib.python.epistemic.capability import CapabilityRegistry

def test_capability_registry():

    registry = CapabilityRegistry()

    capability = Capability(
        identifier="CAP-0001",
        name="I VERIFY MYSELF",
        description="Structural verification",
        acquired_from="Bootstrap",
        acquired_at="2026-01-01T00:00:00",
        verified=False,
    )

    registry.acquire(capability)

    assert registry.exists("CAP-0001")

    capabilities = registry.list()

    assert len(capabilities) == 1

    assert capabilities[0].name == "I VERIFY MYSELF"

    print()

    print("===================================")
    print("CAPABILITY VERIFIED")
    print("===================================")


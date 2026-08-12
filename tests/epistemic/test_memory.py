from lib.python.epistemic.memory.store import MemoryStore

def test_memory_roundtrip():

    store = MemoryStore()

    memory = store.remember(

        title="First Memory",

        content="The organism preserved an experience.",

        session="SESSION-000001",

        capability="CAP-0001",

    )

    restored = store.recall(memory.id)

    assert restored is not None

    assert restored.id == memory.id

    assert restored.content == memory.content

    assert restored.session == "SESSION-000001"

    assert restored.capability == "CAP-0001"

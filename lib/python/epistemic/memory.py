"""
Capability:
    I REMEMBER

Purpose:
    Preserve an experience exactly as it was received.

This is intentionally simple.
The first capability is preservation, not intelligence.
"""

from pathlib import Path
from datetime import datetime


class Memory:

    def __init__(self, root="work/memory"):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def remember(self, name: str, content: str):

        timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")

        filename = self.root / f"{timestamp}_{name}.md"

        filename.write_text(content, encoding="utf-8")

        return filename


if __name__ == "__main__":

    memory = Memory()

    artifact = memory.remember(
        "first_memory",
        "# First Memory\n\nThe organism preserved its first experience.\n",
    )

    print("Memory created:")
    print(artifact)

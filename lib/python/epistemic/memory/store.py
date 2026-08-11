"""
Memory Store

Version 1

Append-only persistent memory.
"""

from pathlib import Path
from uuid import uuid4
from datetime import datetime, UTC
import json

from .model import Memory


ROOT = Path("work/memory")

ROOT.mkdir(parents=True, exist_ok=True)


class MemoryStore:


    def remember(

        self,

        title,

        content,

        session,

        capability,

    ):

        memory = Memory(

            id=uuid4().hex,

            timestamp=datetime.now(UTC).isoformat(),

            title=title,

            content=content,

            session=session,

            capability=capability,

        )

        file = ROOT / f"{memory.id}.json"

        file.write_text(

            json.dumps(memory.__dict__, indent=2),

            encoding="utf-8",

        )

        return memory


    def recall(self, identifier):

        file = ROOT / f"{identifier}.json"

        if not file.exists():

            return None

        return Memory(**json.loads(file.read_text()))


    def list(self):

        result = []

        for file in sorted(ROOT.glob("*.json")):

            result.append(

                Memory(**json.loads(file.read_text()))

            )

        return result

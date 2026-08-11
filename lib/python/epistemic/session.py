"""
Epistemic Session

A Session groups a continuous sequence of events into a single
transformation journey.

Chronicle records events.

Session gives those events a beginning, an end and a purpose.
"""

from dataclasses import dataclass
from datetime import datetime, UTC
import uuid

from lib.python.epistemic.chronicle import Chronicle


@dataclass
class Session:

    identifier: str

    purpose: str

    started_at: str

    status: str


class SessionManager:

    def __init__(self):

        self.chronicle = Chronicle()

    def open(self, purpose: str):

        session = Session(

            identifier=f"SESSION-{uuid.uuid4().hex[:8].upper()}",

            purpose=purpose,

            started_at=datetime.now(UTC).isoformat(),

            status="OPEN",

        )

        self.chronicle.append(

            "SessionOpened",

            session.identifier,

            purpose=purpose,

        )

        return session

    def close(self, session: Session):

        self.chronicle.append(

            "SessionClosed",

            session.identifier,

            result="Session completed.",

        )

        session.status = "CLOSED"

        return session


if __name__ == "__main__":

    manager = SessionManager()

    session = manager.open(

        "Create the first executable session."

    )

    manager.close(session)

    print()

    print("========================================")

    print("SESSION")

    print("========================================")

    print(session)

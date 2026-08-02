from datetime import datetime

from .models import Session
from .storage import SessionStorage

class SessionRuntime:

    def __init__(self):

        self.storage = SessionStorage()

    def create(self, repository="."):

        identifier = datetime.now().strftime(
            "SESSION-%Y%m%d-%H%M%S"
        )

        session = Session(
            identifier=identifier,
            repository=repository
        )

        self.storage.save(session)

        return session

    def checkpoint(self, session, step):

        if step not in session.completed_steps:
            session.completed_steps.append(step)

        self.storage.save(session)

        return session

import json
from pathlib import Path

class SessionStorage:

    ROOT = Path(".ai/sessions")

    def __init__(self):

        self.ROOT.mkdir(parents=True, exist_ok=True)

    def save(self, session):

        path = self.ROOT / f"{session.identifier}.json"

        path.write_text(
            json.dumps(session.__dict__, indent=2),
            encoding="utf-8"
        )

    def load(self, identifier):

        path = self.ROOT / f"{identifier}.json"

        if not path.exists():
            return None

        return json.loads(
            path.read_text(encoding="utf-8")
        )

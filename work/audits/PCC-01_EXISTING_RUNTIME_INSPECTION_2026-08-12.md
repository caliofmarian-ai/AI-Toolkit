# PCC-01 — Existing Runtime Inspection

HEAD: 079e9e762f543d611ce265f74cda4c7b9c340210

---

# Source — `lib/python/epistemic/session.py`

```python
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
```

---

# Source — `lib/python/epistemic/transformation.py`

```python
"""
Transformation Lifecycle v1

The first executable lifecycle for a transformation.
"""

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import uuid


ROOT = Path("work/transformation-evidence")


@dataclass
class Transformation:

    identifier: str

    need: str

    started_at: str

    status: str



class TransformationLifecycle:

    def begin(self, need: str):

        identifier = uuid.uuid4().hex[:12]

        tr = Transformation(

            identifier=identifier,

            need=need,

            started_at=datetime.utcnow().isoformat(),

            status="RUNNING",

        )

        artifact = ROOT / f"{identifier}.md"

        artifact.write_text(
f"""# Transformation Evidence

ID

{identifier}

STATUS

RUNNING

STARTED

{tr.started_at}

NEED

{need}

""",
encoding="utf-8")

        return tr


    def complete(self, transformation):

        artifact = ROOT / f"{transformation.identifier}.md"

        with artifact.open("a", encoding="utf-8") as fp:

            fp.write("""

STATUS

COMPLETED

ENDED

%s

""" % datetime.utcnow().isoformat())


if __name__ == "__main__":

    lifecycle = TransformationLifecycle()

    tr = lifecycle.begin(

        "Create the first executable lifecycle."

    )

    lifecycle.complete(tr)

    print()

    print("Transformation")

    print(tr.identifier)

    print("Completed.")

```

---

# Source — `lib/python/epistemic/witness.py`

```python
from pathlib import Path
from datetime import datetime
import uuid

ROOT = Path("work/witness")
ROOT.mkdir(parents=True, exist_ok=True)

def witness(
    need: str,
    dialogue: str,
    implementation: str,
    execution: str,
    result: str,
    knowledge: str,
):

    identifier = f"WT-{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}-{uuid.uuid4().hex[:8]}"

    artifact = ROOT / f"{identifier}.md"

    artifact.write_text(
f"""# Witness

Identifier
{identifier}

Created
{datetime.utcnow().isoformat()}Z

## Need
{need}

## Dialogue
{dialogue}

## Implementation
{implementation}

## Execution
{execution}

## Result
{result}

## Knowledge
{knowledge}

""",
encoding="utf-8")

    return artifact


if __name__ == "__main__":

    artifact = witness(

        need="Create the first Witness.",

        dialogue="Creator and AI agreed that no transformation may exist without a witness.",

        implementation="Implemented witness.py",

        execution="Executed from Termux.",

        result="Witness artifact created.",

        knowledge="Every transformation must leave behind a single witness artifact.",

    )

    print()
    print("=======================================")
    print("WITNESS CREATED")
    print("=======================================")
    print(artifact)
```

---

# Source — `lib/python/session_runtime/models.py`

```python
from dataclasses import dataclass, field
from typing import Dict, List

@dataclass
class Session:

    identifier: str

    repository: str

    status: str = "ACTIVE"

    completed_steps: List[str] = field(default_factory=list)

    metadata: Dict = field(default_factory=dict)
```

---

# Source — `lib/python/session_runtime/runtime.py`

```python
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
```

---

# Source — `lib/python/session_runtime/storage.py`

```python
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
```


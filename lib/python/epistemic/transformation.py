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


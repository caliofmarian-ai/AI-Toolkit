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

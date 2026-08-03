import json
from pathlib import Path
from datetime import datetime


class ExecutionEngine:

    ROOT = Path(".ai/batches")

    def execute(self, generated_batches):

        results = []

        for batch in generated_batches:

            directory = self.ROOT / batch.identifier
            metadata_file = directory / "metadata.json"

            if not metadata_file.exists():
                continue

            batch.status = "COMPLETED"
            completed = datetime.utcnow().isoformat()

            payload = batch.to_dict()
            payload["completed_at"] = completed

            metadata_file.write_text(
                json.dumps(payload, indent=2),
                encoding="utf-8"
            )

            (directory / "execution.log").write_text(
                f"Execution completed: {completed}\n",
                encoding="utf-8"
            )

            results.append({
                "batch": batch.identifier,
                "status": batch.status,
            })

        return results

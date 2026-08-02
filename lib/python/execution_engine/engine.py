from python.common.models import Batch

import json
from pathlib import Path
from datetime import datetime


class ExecutionEngine:

    ROOT = Path(".ai/batches")

    def execute(self):

        results = []

        if not self.ROOT.exists():
            return results

        for directory in sorted(self.ROOT.iterdir()):

            if not directory.is_dir():
                continue

            metadata_file = directory / "metadata.json"

            if not metadata_file.exists():
                continue

            metadata = Batch.from_dict(
                json.loads(
                    metadata_file.read_text(encoding="utf-8")
                )
            )

            metadata.status = "COMPLETED"
            completed = datetime.utcnow().isoformat()

            payload = metadata.to_dict()
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
                "batch": metadata.identifier,
                "status": metadata.status,
            })

        return results

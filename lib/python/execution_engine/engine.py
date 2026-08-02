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

            metadata = json.loads(
                metadata_file.read_text(encoding="utf-8")
            )

            metadata["status"] = "COMPLETED"
            metadata["completed_at"] = datetime.utcnow().isoformat()

            metadata_file.write_text(
                json.dumps(metadata, indent=2),
                encoding="utf-8"
            )

            (directory / "execution.log").write_text(
                f'Execution completed: {metadata["completed_at"]}\n',
                encoding="utf-8"
            )

            results.append({
                "batch": metadata["identifier"],
                "status": metadata["status"],
            })

        return results

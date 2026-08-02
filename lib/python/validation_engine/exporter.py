import json
from pathlib import Path


class ValidationExporter:

    @staticmethod
    def export(results, filename):

        data = []

        for r in results:

            data.append({
                "identifier": r.identifier,
                "target": r.target,
                "passed": r.passed,
                "message": r.message,
                "severity": r.severity
            })

        Path(filename).parent.mkdir(parents=True, exist_ok=True)

        Path(filename).write_text(
            json.dumps(data, indent=2),
            encoding="utf-8"
        )

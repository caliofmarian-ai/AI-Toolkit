import json
from pathlib import Path


class DependencyExporter:

    @staticmethod
    def export(dependencies, filename):

        data = []

        for dep in dependencies:

            data.append(
                {
                    "source": dep.source,
                    "target": dep.target,
                    "type": dep.dependency_type,
                    "status": dep.status
                }
            )

        Path(filename).parent.mkdir(parents=True, exist_ok=True)

        Path(filename).write_text(
            json.dumps(data, indent=2),
            encoding="utf-8"
        )

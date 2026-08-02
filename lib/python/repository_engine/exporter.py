import json
from pathlib import Path


class RepositoryExporter:

    @staticmethod
    def export(inventory, filename):

        data = []

        for item in inventory:

            data.append(
                {
                    "path": item.path,
                    "name": item.name,
                    "type": item.item_type,
                    "size": item.size,
                }
            )

        Path(filename).parent.mkdir(parents=True, exist_ok=True)

        Path(filename).write_text(
            json.dumps(data, indent=2),
            encoding="utf-8",
        )

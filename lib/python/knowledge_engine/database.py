from pathlib import Path
import json

from .models import Entity


class KnowledgeDatabase:

    def __init__(self):

        self.entities = {}

    def add(self, entity: Entity):

        self.entities[entity.identifier] = entity

    def get(self, identifier):

        return self.entities.get(identifier)

    def all(self):

        return list(self.entities.values())

    def save(self, filename):

        data = {}

        for key, value in self.entities.items():

            data[key] = value.__dict__

        Path(filename).write_text(
            json.dumps(data, indent=2),
            encoding="utf-8"
        )

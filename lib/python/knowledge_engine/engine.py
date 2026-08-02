from .models import Entity
from .database import KnowledgeDatabase


class KnowledgeEngine:

    def __init__(self):

        self.db = KnowledgeDatabase()

    def register(self,
                 identifier,
                 name,
                 entity_type):

        entity = Entity(
            identifier=identifier,
            name=name,
            entity_type=entity_type,
        )

        self.db.add(entity)

        return entity

    def entities(self):

        return self.db.all()

    def export(self, filename):

        self.db.save(filename)

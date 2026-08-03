from pathlib import Path

from python.canonical_parser import CanonicalParser


class CanonicalRepository:
    """In-memory store of all CanonicalDocument entities."""

    def __init__(self):
        self._documents = {}
        self._filenames = {}

    def add(self, doc):
        self._documents[doc.id] = doc
        self._filenames[doc.filename] = doc.id

    def get_by_id(self, doc_id):
        return self._documents.get(doc_id)

    def get_by_filename(self, filename):
        doc_id = self._filenames.get(filename)
        return self._documents.get(doc_id) if doc_id is not None else None

    def get_by_dependency(self, dep_id):
        return [doc for doc in self.all_documents() if dep_id in doc.dependencies]

    def all_documents(self):
        return [self._documents[key] for key in sorted(self._documents)]

    def all_ids(self):
        return sorted(self._documents)

    def dependency_graph(self):
        return dict((doc.id, list(doc.dependencies)) for doc in self.all_documents())

    def dependents_of(self, doc_id):
        return [doc.id for doc in self.get_by_dependency(doc_id)]

    @classmethod
    def load_from_directory(cls, docs_path):
        """Load all CANON-*.md from docs_path, parse and store."""
        docs_path = Path(docs_path)
        parser = CanonicalParser()
        repository = cls()
        for document in parser.parse_directory(docs_path):
            repository.add(document)
        return repository

    def statistics(self):
        status_counts = {}
        section_total = 0
        dependency_total = 0
        objective_total = 0
        for doc in self.all_documents():
            key = doc.status.value
            status_counts[key] = status_counts.get(key, 0) + 1
            section_total += len(doc.sections)
            dependency_total += len(doc.dependencies)
            objective_total += len(doc.objectives)
        return {
            "total_documents": len(self._documents),
            "total_sections": section_total,
            "total_dependencies": dependency_total,
            "total_objectives": objective_total,
            "status_counts": status_counts,
            "document_ids": self.all_ids(),
        }

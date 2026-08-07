from typing import Dict, List

from python.executable_repository_intelligence.file_classifier import (
    FileClassifier as ExecutableFileClassifier,
)

from .models import ClassifiedFile


_CATEGORY_TO_CLASS = {
    "Executable Code": "source",
    "Runtime Entry Point": "source",
    "Public API": "source",
    "Internal API": "source",
    "Plugin API": "source",
    "Extension Point": "source",
    "Tests": "test",
    "Configuration": "config",
    "Environment": "config",
    "Documentation": "doc",
    "Canonical Specification": "doc",
    "Reports": "doc",
    "Generated Artifact": "generated",
    "Temporary": "generated",
    "Assets": "generated",
    "Deprecated": "unknown",
    "Infrastructure": "build",
    "Scripts": "build",
    "Bootstrap": "build",
}


class RepositoryFileClassifier:

    def __init__(self):
        self._classifier = ExecutableFileClassifier()

    def get_file_class(self, category: str) -> str:
        return _CATEGORY_TO_CLASS.get(category, "unknown")

    def classify_all(self, file_analyses: Dict, root) -> List[ClassifiedFile]:
        executable_classes = self._classifier.classify_all(file_analyses, root)
        results: List[ClassifiedFile] = []
        for item in executable_classes:
            language = "unknown"
            analysis = file_analyses.get(item.path)
            if analysis is not None:
                language = getattr(analysis, "language", "unknown")
            results.append(
                ClassifiedFile(
                    path=item.path,
                    file_class=self.get_file_class(item.category),
                    category=item.category,
                    language=language,
                    is_executable=item.is_executable,
                )
            )
        return sorted(results, key=lambda row: row.path)

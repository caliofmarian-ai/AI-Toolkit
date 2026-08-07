from collections import Counter

from .models import RepositoryMetrics


class MetricsExtractor:

    def extract(self, index, classified_files, entry_points) -> RepositoryMetrics:
        total_files = index.statistics.total_files
        total_directories = index.statistics.total_directories

        language_distribution = Counter(
            item.language for item in classified_files if item.language != "unknown"
        )
        file_class_distribution = Counter(item.file_class for item in classified_files)

        test_file_count = file_class_distribution.get("test", 0)
        documentation_file_count = file_class_distribution.get("doc", 0)

        documentation_coverage_ratio = (
            documentation_file_count / total_files if total_files > 0 else 0.0
        )
        test_coverage_ratio = test_file_count / total_files if total_files > 0 else 0.0

        return RepositoryMetrics(
            total_files=total_files,
            total_directories=total_directories,
            language_distribution=dict(sorted(language_distribution.items())),
            file_class_distribution=dict(sorted(file_class_distribution.items())),
            test_file_count=test_file_count,
            documentation_file_count=documentation_file_count,
            entry_point_count=len(entry_points),
            documentation_coverage_ratio=documentation_coverage_ratio,
            test_coverage_ratio=test_coverage_ratio,
        )

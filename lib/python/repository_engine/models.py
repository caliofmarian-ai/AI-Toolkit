from dataclasses import dataclass
from typing import Dict, List

@dataclass
class RepositoryItem:

    path: str

    name: str

    item_type: str

    size: int


@dataclass
class RepositoryMetrics:

    total_files: int

    total_directories: int

    language_distribution: Dict[str, int]

    file_class_distribution: Dict[str, int]

    test_file_count: int

    documentation_file_count: int

    entry_point_count: int

    documentation_coverage_ratio: float

    test_coverage_ratio: float


@dataclass
class DependencyMap:

    manifests: Dict[str, List[str]]

    internal_import_edges: int

    internal_import_nodes: int

    unresolved_imports: int


@dataclass
class ClassifiedFile:

    path: str

    file_class: str

    category: str

    language: str

    is_executable: bool


@dataclass
class RepositoryProfile:

    path: str

    name: str

    metrics: RepositoryMetrics

    classified_files: List[ClassifiedFile]

    tech_stack: List[str]

    entry_points: List[str]

    dependencies: DependencyMap

    health_summary: Dict[str, object]

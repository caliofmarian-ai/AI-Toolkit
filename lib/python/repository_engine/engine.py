from pathlib import Path

from .models import RepositoryItem
from .models import RepositoryProfile
from .classifier import RepositoryFileClassifier
from .metrics import MetricsExtractor
from .deps import DependencyDiscovery

from python.semantic_repository_intelligence.ast_analyzer import ASTAnalyzer
from python.semantic_repository_intelligence.models import FileAnalysis


class RepositoryEngine:

    def __init__(self, root=".", workspace_index=None):

        self.root = Path(root).resolve()
        self._workspace_index = workspace_index

    def _get_index(self):
        if self._workspace_index is not None:
            return self._workspace_index
        from python.workspace_index import WorkspaceIndexBuilder
        return WorkspaceIndexBuilder(self.root).build()

    def discover(self):

        index = self._get_index()

        inventory = []

        for f in index.files:
            inventory.append(
                RepositoryItem(
                    path=f.path,
                    name=f.name,
                    item_type="file",
                    size=f.size,
                )
            )

        for d in index.directories:
            inventory.append(
                RepositoryItem(
                    path=d.path,
                    name=d.name,
                    item_type="directory",
                    size=0,
                )
            )

        return inventory

    def statistics(self):

        index = self._get_index()

        return {
            "items": index.statistics.total_files + index.statistics.total_directories,
            "files": index.statistics.total_files,
            "directories": index.statistics.total_directories,
        }

    def profile(self):

        index = self._get_index()

        file_analyses = ASTAnalyzer(self.root, workspace_index=index).analyze()
        for file_item in index.files:
            if file_item.path not in file_analyses:
                file_analyses[file_item.path] = FileAnalysis(
                    path=file_item.path,
                    language="unknown",
                )

        classifier = RepositoryFileClassifier()
        classified_files = classifier.classify_all(file_analyses, self.root)

        entry_points = {
            path
            for path, analysis in file_analyses.items()
            if getattr(analysis, "entry_points", [])
        }
        entry_points.update(
            {
                item.path
                for item in classified_files
                if item.category == "Runtime Entry Point"
            }
        )
        entry_points = sorted(entry_points)

        metrics = MetricsExtractor().extract(index, classified_files, entry_points)
        dependencies = DependencyDiscovery().discover(self.root, file_analyses)
        tech_stack = self._detect_tech_stack(file_analyses)
        health_summary = self._build_health_summary(metrics, dependencies)

        return RepositoryProfile(
            path=str(self.root),
            name=self.root.name,
            metrics=metrics,
            classified_files=classified_files,
            tech_stack=tech_stack,
            entry_points=entry_points,
            dependencies=dependencies,
            health_summary=health_summary,
        )

    def _detect_tech_stack(self, file_analyses):
        stack = []

        languages = {analysis.language for analysis in file_analyses.values()}
        language_map = {
            "python": "Python",
            "javascript": "JavaScript",
            "typescript": "TypeScript",
            "yaml": "YAML",
            "json": "JSON",
            "markdown": "Markdown",
        }
        for key, label in language_map.items():
            if key in languages:
                stack.append(label)

        markers = [
            ("requirements.txt", "pip"),
            ("pyproject.toml", "Poetry/PEP 621"),
            ("package.json", "Node.js/npm"),
            ("pnpm-lock.yaml", "pnpm"),
            ("yarn.lock", "Yarn"),
            ("go.mod", "Go modules"),
            ("Gemfile", "Ruby/Bundler"),
            (".github/workflows", "GitHub Actions"),
            ("railway.json", "Railway"),
            ("Dockerfile", "Docker"),
            ("docker-compose.yml", "Docker Compose"),
            ("docker-compose.yaml", "Docker Compose"),
        ]

        for rel, label in markers:
            if (self.root / rel).exists():
                stack.append(label)

        return sorted(set(stack))

    def _build_health_summary(self, metrics, dependencies):
        checks = []
        checks.append(
            self._check("Repository has source files", metrics.total_files > 0, f"{metrics.total_files} files")
        )
        checks.append(
            self._check("Repository has tests", metrics.test_file_count > 0, f"{metrics.test_file_count} test files")
        )
        checks.append(
            self._check(
                "Repository has documentation",
                metrics.documentation_file_count > 0,
                f"{metrics.documentation_file_count} documentation files",
            )
        )
        checks.append(
            self._check(
                "Repository has entry points",
                metrics.entry_point_count > 0,
                f"{metrics.entry_point_count} entry points",
            )
        )
        checks.append(
            self._check(
                "Repository has dependency metadata",
                bool(dependencies.manifests),
                f"{len(dependencies.manifests)} manifest files",
            )
        )

        passed = sum(1 for row in checks if row["passed"])
        score = int((passed / len(checks)) * 100) if checks else 0
        status = "HEALTHY" if score >= 80 else "ATTENTION" if score >= 50 else "RISK"

        summary = (
            "Repository is operationally healthy."
            if status == "HEALTHY"
            else "Repository needs targeted improvements."
            if status == "ATTENTION"
            else "Repository requires immediate remediation."
        )

        return {
            "status": status,
            "score": score,
            "summary": summary,
            "checks": checks,
        }

    def _check(self, name, passed, message):
        return {
            "name": name,
            "passed": bool(passed),
            "message": message,
        }

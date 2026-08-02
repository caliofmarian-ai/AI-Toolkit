from pathlib import Path
import time


class PlanningOptimizer:

    DEFAULT_EXCLUDES = {
        ".git",
        ".ai",
        "__pycache__",
        ".pytest_cache",
        "node_modules",
        ".next",
        ".expo",
        ".turbo",
        "dist",
        "build",
        "coverage",
        "android/build",
        "ios/Pods",
    }

    def scan(self, repository):

        root = Path(repository).resolve()

        started = time.perf_counter()

        files = []

        for path in root.rglob("*"):

            if not path.is_file():
                continue

            text = str(path)

            skip = False

            for excluded in self.DEFAULT_EXCLUDES:
                if excluded in text:
                    skip = True
                    break

            if skip:
                continue

            files.append(path)

        elapsed = time.perf_counter() - started

        return {
            "files": files,
            "count": len(files),
            "elapsed": elapsed,
        }

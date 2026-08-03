"""
Executable Repository Intelligence — Runtime Map Builder
CORE-008C

Builds a RepositoryRuntimeMap from CORE-008B semantic analysis output.
Identifies main entry points, bootstrap sequences, execution chains,
and runtime subsystems (Telegram, Scheduler, Persistence, etc.).
"""

import re
from pathlib import Path
from typing import Dict, List, Optional, Set

from .models import (
    FileClassification,
    RepositoryRuntimeMap,
    RuntimeComponent,
)


# Patterns for recognising runtime subsystems
_TELEGRAM_PATTERNS = [
    re.compile(r"aiogram|telebot|telegram|python-telegram-bot", re.IGNORECASE),
    re.compile(r"Bot\s*\(|Dispatcher\s*\(|dp\s*=", re.IGNORECASE),
]
_SCHEDULER_PATTERNS = [
    re.compile(r"apscheduler|schedule|celery|rq\b|dramatiq", re.IGNORECASE),
    re.compile(r"scheduler\s*=|Scheduler\s*\(|cron\b|periodic_task", re.IGNORECASE),
]
_PERSISTENCE_PATTERNS = [
    re.compile(r"sqlalchemy|peewee|tortoise|databases|asyncpg|psycopg|aiosqlite|redis|mongo", re.IGNORECASE),
    re.compile(r"Session\s*\(|engine\s*=|create_engine|database\s*=", re.IGNORECASE),
]
_OWNER_PATTERNS = [
    re.compile(r"owner|admin_id|OWNER_ID|owner_check|is_owner", re.IGNORECASE),
]
_ADMIN_PATTERNS = [
    re.compile(r"admin|moderator|ADMIN_ID|admin_check|is_admin", re.IGNORECASE),
]
_BACKGROUND_PATTERNS = [
    re.compile(r"asyncio\.create_task|loop\.run_until_complete|threading\.Thread|multiprocessing\.Process", re.IGNORECASE),
    re.compile(r"worker|background|daemon\s*=\s*True", re.IGNORECASE),
]
_SHUTDOWN_PATTERNS = [
    re.compile(r"on_shutdown|atexit|signal\.signal|SIGTERM|SIGINT|shutdown_hook|cleanup", re.IGNORECASE),
]
_RESTART_PATTERNS = [
    re.compile(r"restart|on_restart|restart_hook|respawn", re.IGNORECASE),
]
_RESUME_PATTERNS = [
    re.compile(r"resume|on_resume|resume_hook|recover", re.IGNORECASE),
]
_BOOTSTRAP_PATTERNS = [
    re.compile(r"bootstrap|setup|configure|init_app|create_app|build_app|startup|on_startup", re.IGNORECASE),
]
_ENTRY_FILENAME_RE = re.compile(
    r"^(main|app|run|server|bot|start|__main__)\.py$", re.IGNORECASE
)


def _read_text(root: Path, path_str: str) -> str:
    try:
        return (root / path_str).read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


def _matches_any(text: str, patterns: List[re.Pattern]) -> bool:
    for p in patterns:
        if p.search(text):
            return True
    return False


class RuntimeMapBuilder:
    """
    Builds a RepositoryRuntimeMap by walking executable files.

    Uses CORE-008B FileAnalysis data (entry_points, functions, imports)
    and the FileClassification results to determine runtime topology.
    """

    def build(
        self,
        file_classifications: List[FileClassification],
        file_analyses: Dict,   # path → FileAnalysis (CORE-008B)
        root: Path,
    ) -> RepositoryRuntimeMap:
        """Build and return the RepositoryRuntimeMap."""
        exec_files = {fc.path for fc in file_classifications if fc.is_executable}

        # Locate main entry point
        main_entry_point = self._find_main_entry(file_analyses, exec_files)

        # Build execution chain from the main entry point
        execution_chain = self._build_execution_chain(
            main_entry_point, file_analyses, exec_files
        )

        # Identify bootstrap files
        bootstrap_sequence = self._find_bootstrap(file_classifications, file_analyses, root)

        # Classify runtime subsystems
        telegram_runtime: List[str] = []
        owner_runtime: List[str] = []
        admin_runtime: List[str] = []
        persistence_runtime: List[str] = []
        background_workers: List[str] = []
        scheduler_entry: Optional[str] = None
        shutdown_hooks: List[str] = []
        restart_hooks: List[str] = []
        resume_hooks: List[str] = []
        runtime_components: List[RuntimeComponent] = []

        for path_str in sorted(exec_files):
            text = _read_text(root, path_str)
            if not text:
                continue

            role = "executable"
            layer = "Core"

            if _matches_any(text, _TELEGRAM_PATTERNS):
                telegram_runtime.append(path_str)
                role = "telegram"
                layer = "Telegram"

            if _matches_any(text, _OWNER_PATTERNS):
                owner_runtime.append(path_str)

            if _matches_any(text, _ADMIN_PATTERNS):
                admin_runtime.append(path_str)

            if _matches_any(text, _PERSISTENCE_PATTERNS):
                persistence_runtime.append(path_str)
                role = "persistence" if role == "executable" else role
                layer = "Persistence" if layer == "Core" else layer

            if _matches_any(text, _BACKGROUND_PATTERNS):
                background_workers.append(path_str)
                role = "worker" if role == "executable" else role

            if _matches_any(text, _SCHEDULER_PATTERNS):
                if scheduler_entry is None:
                    scheduler_entry = path_str
                role = "scheduler" if role == "executable" else role
                layer = "Scheduler" if layer == "Core" else layer

            if _matches_any(text, _SHUTDOWN_PATTERNS):
                shutdown_hooks.append(path_str)

            if _matches_any(text, _RESTART_PATTERNS):
                restart_hooks.append(path_str)

            if _matches_any(text, _RESUME_PATTERNS):
                resume_hooks.append(path_str)

            # Build dependencies from import graph
            deps = self._direct_deps(path_str, file_analyses, exec_files)

            runtime_components.append(RuntimeComponent(
                name=Path(path_str).stem,
                file=path_str,
                role=role,
                layer=layer,
                dependencies=sorted(deps),
            ))

        # Initialization order: bootstrap first, then by execution chain, then rest
        init_order = self._compute_init_order(
            bootstrap_sequence, execution_chain, exec_files
        )

        # Deduplicate lists, preserving first-seen order
        def _dedup(lst):
            seen: Set[str] = set()
            result = []
            for x in lst:
                if x not in seen:
                    seen.add(x)
                    result.append(x)
            return result

        return RepositoryRuntimeMap(
            main_entry_point=main_entry_point,
            execution_chain=_dedup(execution_chain),
            bootstrap_sequence=_dedup(bootstrap_sequence),
            runtime_components=sorted(runtime_components, key=lambda c: c.file),
            initialization_order=_dedup(init_order),
            scheduler_entry=scheduler_entry,
            background_workers=_dedup(background_workers),
            telegram_runtime=_dedup(telegram_runtime),
            owner_runtime=_dedup(owner_runtime),
            admin_runtime=_dedup(admin_runtime),
            persistence_runtime=_dedup(persistence_runtime),
            shutdown_hooks=_dedup(shutdown_hooks),
            restart_hooks=_dedup(restart_hooks),
            resume_hooks=_dedup(resume_hooks),
        )

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _find_main_entry(self, file_analyses: Dict, exec_files: Set[str]) -> Optional[str]:
        """Return the primary entry point file path."""
        # Priority 1: files with __main__ entry point + matching filename
        for path_str in sorted(exec_files):
            filename = Path(path_str).name
            fa = file_analyses.get(path_str)
            if fa and "__main__" in getattr(fa, "entry_points", []):
                if _ENTRY_FILENAME_RE.match(filename):
                    return path_str

        # Priority 2: filename match only
        for path_str in sorted(exec_files):
            filename = Path(path_str).name
            if _ENTRY_FILENAME_RE.match(filename):
                return path_str

        # Priority 3: any file with a __main__ entry point
        for path_str in sorted(exec_files):
            fa = file_analyses.get(path_str)
            if fa and "__main__" in getattr(fa, "entry_points", []):
                return path_str

        return None

    def _build_execution_chain(
        self,
        entry: Optional[str],
        file_analyses: Dict,
        exec_files: Set[str],
        max_depth: int = 8,
    ) -> List[str]:
        """BFS from the main entry point following import dependencies."""
        if not entry:
            return []

        chain: List[str] = []
        visited: Set[str] = set()
        queue = [entry]

        while queue and len(chain) < max_depth:
            current = queue.pop(0)
            if current in visited:
                continue
            visited.add(current)
            chain.append(current)

            fa = file_analyses.get(current)
            if not fa:
                continue

            for imp in sorted(getattr(fa, "imports", []), key=lambda i: i.module):
                resolved = getattr(imp, "resolved", None)
                if resolved and resolved in exec_files and resolved not in visited:
                    queue.append(resolved)

        return chain

    def _find_bootstrap(
        self,
        file_classifications: List[FileClassification],
        file_analyses: Dict,
        root: Path,
    ) -> List[str]:
        """Identify bootstrap files from classifications and text patterns."""
        results: List[str] = []
        seen: Set[str] = set()

        # Files explicitly classified as Bootstrap
        for fc in file_classifications:
            if fc.category == "Bootstrap" and fc.path not in seen:
                results.append(fc.path)
                seen.add(fc.path)

        # Scan executable code for bootstrap patterns
        for fc in file_classifications:
            if not fc.is_executable or fc.path in seen:
                continue
            text = _read_text(root, fc.path)
            if _matches_any(text, _BOOTSTRAP_PATTERNS):
                results.append(fc.path)
                seen.add(fc.path)

        return sorted(results)

    def _direct_deps(
        self, path_str: str, file_analyses: Dict, exec_files: Set[str]
    ) -> Set[str]:
        """Return the set of executable files directly imported by path_str."""
        fa = file_analyses.get(path_str)
        if not fa:
            return set()
        deps = set()
        for imp in getattr(fa, "imports", []):
            resolved = getattr(imp, "resolved", None)
            if resolved and resolved in exec_files:
                deps.add(resolved)
        return deps

    def _compute_init_order(
        self,
        bootstrap: List[str],
        chain: List[str],
        exec_files: Set[str],
    ) -> List[str]:
        """
        Produce an initialization order: bootstrap → execution chain → remaining.
        """
        seen: Set[str] = set()
        order: List[str] = []

        for p in bootstrap + chain:
            if p not in seen:
                seen.add(p)
                order.append(p)

        for p in sorted(exec_files):
            if p not in seen:
                seen.add(p)
                order.append(p)

        return order

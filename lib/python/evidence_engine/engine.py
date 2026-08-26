from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable

from python.semantic_engine.engine import SemanticEngine


class EvidenceEngine:

    _STOP_WORDS = frozenset(
        {
            "a",
            "about",
            "ai",
            "al",
            "ale",
            "and",
            "are",
            "as",
            "at",
            "care",
            "ce",
            "cel",
            "cea",
            "cele",
            "cu",
            "de",
            "din",
            "do",
            "does",
            "este",
            "for",
            "from",
            "i",
            "in",
            "inspect",
            "inspecteaza",
            "inspectează",
            "is",
            "la",
            "mai",
            "me",
            "moment",
            "momentul",
            "of",
            "on",
            "please",
            "repository",
            "repositoryul",
            "repository-ul",
            "repo",
            "sa",
            "să",
            "show",
            "spune",
            "the",
            "this",
            "to",
            "what",
            "which",
            "with",
            "you",
        }
    )

    def __init__(self, repository="."):

        self.root = Path(repository).resolve()

    @staticmethod
    def _normalize(value: str) -> str:
        value = value.casefold()
        value = value.replace("-", " ")
        value = value.replace("_", " ")
        value = value.replace("/", " ")
        value = value.replace("\\", " ")
        return " ".join(value.split())

    @classmethod
    def _query_terms(cls, query: str) -> tuple[str, ...]:
        raw = re.findall(
            r"[0-9A-Za-zÀ-ÖØ-öø-ÿ_./-]+",
            query.casefold(),
        )

        terms = []

        for token in raw:
            for part in cls._normalize(token).split():
                if len(part) < 2:
                    continue
                if part in cls._STOP_WORDS:
                    continue
                if part not in terms:
                    terms.append(part)

        return tuple(terms)

    @classmethod
    def _match_score(
        cls,
        query: str,
        relative_path: str,
    ) -> int:
        query_normalized = cls._normalize(query)
        path_normalized = cls._normalize(relative_path)
        name_normalized = cls._normalize(
            Path(relative_path).name
        )

        if query_normalized and query_normalized in path_normalized:
            return 10000

        terms = cls._query_terms(query)

        if not terms:
            return 0

        score = 0

        for term in terms:
            if term in name_normalized:
                score += 100
            elif term in path_normalized:
                score += 25

        return score

    def _repository_files(self) -> Iterable[Path]:
        for file in self.root.rglob("*"):

            if not file.is_file():
                continue

            if ".git" in file.parts:
                continue

            yield file

    @staticmethod
    def _readable_text_source(path: Path) -> bool:
        """Certify real non-empty UTF-8 matter before retrieval."""
        try:
            if not path.is_file():
                return False

            if path.stat().st_size <= 0:
                return False

            content = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            return False

        return bool(content)

    def find(self, keyword):

        semantic = SemanticEngine(self.root).analyze()

        evidence = {
            "python": [],
            "shell": [],
            "tests": [],
            "docs": [],
        }

        ranked = []

        for file in self._repository_files():

            rel = str(file.relative_to(self.root))
            score = self._match_score(
                str(keyword),
                rel,
            )

            if score <= 0:
                continue

            if not self._readable_text_source(file):
                continue

            ranked.append(
                (
                    -score,
                    rel.casefold(),
                    rel,
                    file,
                )
            )

        ranked.sort()

        for _, _, rel, file in ranked:

            name = file.name.casefold()

            if file.suffix == ".py":
                if "test" in name or "tests" in file.parts:
                    evidence["tests"].append(rel)
                else:
                    evidence["python"].append(rel)

            elif file.suffix == ".sh":
                evidence["shell"].append(rel)

            elif file.suffix == ".md":
                evidence["docs"].append(rel)

            elif "test" in name:
                evidence["tests"].append(rel)

        evidence["semantic"] = {}

        terms = self._query_terms(str(keyword))

        for filename, data in semantic.items():

            score = []

            for cls in data["classes"]:
                normalized = self._normalize(cls)
                if any(term in normalized for term in terms):
                    score.append(("class", cls))

            for fn in data["functions"]:
                normalized = self._normalize(fn)
                if any(term in normalized for term in terms):
                    score.append(("function", fn))

            for imp in data["imports"]:
                normalized = self._normalize(imp)
                if any(term in normalized for term in terms):
                    score.append(("import", imp))

            if score:
                semantic_path = Path(str(filename))

                try:
                    if semantic_path.is_absolute():
                        resolved_semantic_path = (
                            semantic_path.resolve()
                        )
                    else:
                        resolved_semantic_path = (
                            self.root
                            / semantic_path
                        ).resolve()

                    relative_semantic_path = (
                        resolved_semantic_path
                        .relative_to(self.root)
                        .as_posix()
                    )
                except (OSError, ValueError):
                    continue

                semantic_source = (
                    self.root
                    / relative_semantic_path
                )

                if not self._readable_text_source(
                    semantic_source
                ):
                    continue

                evidence["semantic"][
                    relative_semantic_path
                ] = score

        return evidence

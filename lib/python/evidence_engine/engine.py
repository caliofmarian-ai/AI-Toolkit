from __future__ import annotations

import hashlib
import json
import re
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path, PurePosixPath
from typing import Iterable, Mapping

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

    @staticmethod
    def _checkpoint_request(question: str):
        """Extract explicit GitHub coordinates without guessing."""
        text = str(question or "")

        def labelled(name: str) -> str:
            match = re.search(
                rf"(?im)^\s*(?:[-*]\s*)?{name}[^:\n]*:\s*"
                r"[`\"']?([^`\"'\n]+)",
                text,
            )
            return match.group(1).strip() if match else ""

        repository = labelled("repository")
        branch = labelled("branch")
        commit = labelled("commit")

        if not repository:
            match = re.search(
                r"\b([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)\b",
                text,
            )
            repository = match.group(1) if match else ""

        if not commit:
            match = re.search(r"\b[0-9a-fA-F]{40}\b", text)
            commit = match.group(0) if match else ""

        repository = repository.strip(" `\"'")
        branch = branch.strip(" `\"'")
        commit = commit.strip(" `\"'").lower()

        if not re.fullmatch(
            r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+",
            repository,
        ):
            return None

        if not re.fullmatch(r"[0-9a-f]{40}", commit):
            return None

        paths = []

        for candidate in re.findall(r"`([^`]+)`", text):
            candidate = candidate.strip()

            if not candidate.startswith(
                (
                    "audit/",
                    "canon/",
                    "docs/",
                    "lib/",
                    "standards/",
                    "tests/",
                    "tools/",
                    "work/",
                )
            ):
                continue

            identity = PurePosixPath(candidate)

            if identity.is_absolute() or ".." in identity.parts:
                continue

            normalized = identity.as_posix()

            if normalized not in paths:
                paths.append(normalized)

            if len(paths) >= 4:
                break

        if not paths:
            return None

        return {
            "repository": repository,
            "branch": branch,
            "commit": commit,
            "paths": paths,
        }

    @staticmethod
    def _github_json(url: str):
        request = urllib.request.Request(
            url,
            headers={
                "Accept": "application/vnd.github+json",
                "User-Agent": "AI-Toolkit-EvidenceEngine/1",
                "X-GitHub-Api-Version": "2022-11-28",
            },
            method="GET",
        )

        with urllib.request.urlopen(request, timeout=20) as response:
            raw = response.read(2_000_000)

        return json.loads(raw.decode("utf-8"))

    @staticmethod
    def _github_raw(url: str) -> bytes:
        """Read one complete native GitHub blob without application truncation."""
        request = urllib.request.Request(
            url,
            headers={
                "Accept": "application/vnd.github.raw+json",
                "User-Agent": "AI-Toolkit-EvidenceEngine/1",
                "X-GitHub-Api-Version": "2022-11-28",
            },
            method="GET",
        )

        chunks = []

        with urllib.request.urlopen(request, timeout=30) as response:
            while True:
                chunk = response.read(1_048_576)

                if not chunk:
                    break

                chunks.append(chunk)

        return b"".join(chunks)

    @staticmethod
    def _git_blob_sha(raw: bytes) -> str:
        header = f"blob {len(raw)}\0".encode("ascii")
        return hashlib.sha1(header + raw).hexdigest()

    @staticmethod
    def _lossless_text_segments(content: str):
        """Page complete text for cognition without limiting the file."""
        page_characters = 12_000
        pieces = [
            content[offset:offset + page_characters]
            for offset in range(0, len(content), page_characters)
        ]

        if not pieces:
            pieces = [""]

        segments = []
        character_cursor = 0
        byte_cursor = 0
        segment_count = len(pieces)

        for index, piece in enumerate(pieces, start=1):
            encoded = piece.encode("utf-8")
            character_end = character_cursor + len(piece)
            byte_end = byte_cursor + len(encoded)

            segments.append(
                {
                    "segment_index": index,
                    "segment_count": segment_count,
                    "character_start": character_cursor,
                    "character_end": character_end,
                    "byte_start": byte_cursor,
                    "byte_end": byte_end,
                    "content": piece,
                    "content_sha256": hashlib.sha256(
                        encoded
                    ).hexdigest(),
                }
            )

            character_cursor = character_end
            byte_cursor = byte_end

        if "".join(item["content"] for item in segments) != content:
            raise ValueError("lossless-segmentation-failed")

        return segments

    @staticmethod
    def _checkpoint_status(observations) -> str:
        requested = len(observations)
        retrieved = sum(
            1
            for item in observations
            if item.get("status") == "RETRIEVED"
        )

        if requested and retrieved == requested:
            return "RETRIEVED"

        if retrieved:
            return "PARTIAL"

        return "NOT_AVAILABLE"

    @staticmethod
    def _checkpoint_unknown(request, reason: str):
        return {
            "schema": "FUSION-02-GITHUB-CHECKPOINT-RETRIEVAL-1",
            "capability": "read-checkpoint",
            "keyword": "exact-github-checkpoint",
            "read_only": True,
            "authority_conferred": False,
            "working_context_materialized": False,
            "source_identity_kind": "repository-relative-path",
            "source_paths": [],
            "result": {
                "python": [],
                "shell": [],
                "tests": [],
                "docs": [],
                "semantic": {},
            },
            "read_observations": [],
            "epistemic_class": "COMMITTED_REPOSITORY_EVIDENCE",
            "uncertainties": [reason],
            "checkpoint_identity": {
                "repository": request["repository"],
                "requested_branch": request["branch"],
                "requested_commit": request["commit"],
                "resolved_commit": "",
                "branch_head_commit": "",
                "branch_head_matches_commit": False,
                "requested_path_count": len(request["paths"]),
                "retrieved_path_count": 0,
                "complete_files": False,
                "status": "NOT_AVAILABLE",
                "read_only": True,
                "authority_conferred": False,
                "human_authority_preserved": True,
            },
        }

    def find_github_checkpoint(self, question: str):
        """Read bounded bytes from one explicit immutable GitHub commit."""
        request = self._checkpoint_request(question)

        if request is None:
            return None

        repository = request["repository"]
        branch = request["branch"]
        commit = request["commit"]
        encoded_repository = "/".join(
            urllib.parse.quote(part, safe="")
            for part in repository.split("/")
        )
        api_root = (
            "https://api.github.com/repos/"
            + encoded_repository
        )

        try:
            commit_payload = self._github_json(
                api_root
                + "/commits/"
                + urllib.parse.quote(commit, safe="")
            )
        except (
            OSError,
            UnicodeError,
            ValueError,
            urllib.error.URLError,
        ) as exc:
            return self._checkpoint_unknown(
                request,
                "commit-retrieval-unavailable:"
                + type(exc).__name__,
            )

        if not isinstance(commit_payload, Mapping):
            return self._checkpoint_unknown(
                request,
                "commit-response-invalid",
            )

        resolved_commit = str(
            commit_payload.get("sha", "")
        ).lower()

        if resolved_commit != commit:
            return self._checkpoint_unknown(
                request,
                "commit-identity-mismatch",
            )

        branch_head = ""
        uncertainties = []

        if branch:
            try:
                branch_payload = self._github_json(
                    api_root
                    + "/branches/"
                    + urllib.parse.quote(branch, safe="")
                )

                if not isinstance(branch_payload, Mapping):
                    raise ValueError("branch-response-invalid")

                branch_commit = branch_payload.get("commit", {})

                if not isinstance(branch_commit, Mapping):
                    raise ValueError("branch-commit-invalid")

                branch_head = str(
                    branch_commit.get(
                        "sha",
                        "",
                    )
                ).lower()
            except (
                OSError,
                UnicodeError,
                ValueError,
                urllib.error.URLError,
            ) as exc:
                uncertainties.append(
                    "branch-retrieval-unavailable:"
                    + type(exc).__name__
                )

            if branch_head and branch_head != commit:
                uncertainties.append(
                    "branch-head-differs-from-requested-commit"
                )

        observations = []
        result = {
            "python": [],
            "shell": [],
            "tests": [],
            "docs": [],
            "semantic": {},
        }

        for source_path in request["paths"]:
            encoded_path = urllib.parse.quote(
                source_path,
                safe="/",
            )
            url = (
                api_root
                + "/contents/"
                + encoded_path
                + "?ref="
                + urllib.parse.quote(commit, safe="")
            )

            try:
                payload = self._github_json(url)

                if not isinstance(payload, Mapping):
                    raise ValueError("requested-path-is-not-a-file")

                if payload.get("type") != "file":
                    raise ValueError("requested-path-is-not-a-file")

                blob_sha = str(payload.get("sha", "")).lower()

                if not re.fullmatch(r"[0-9a-f]{40}", blob_sha):
                    raise ValueError("blob-identity-unavailable")

                raw = self._github_raw(
                    api_root
                    + "/git/blobs/"
                    + urllib.parse.quote(blob_sha, safe="")
                )

                declared_size = int(payload.get("size", len(raw)))

                if declared_size != len(raw):
                    raise ValueError("blob-byte-count-mismatch")

                if self._git_blob_sha(raw) != blob_sha:
                    raise ValueError("blob-identity-mismatch")

                content = raw.decode("utf-8")
                segments = self._lossless_text_segments(content)
            except (
                OSError,
                TypeError,
                UnicodeError,
                ValueError,
                urllib.error.URLError,
            ) as exc:
                uncertainty = (
                    "file-retrieval-unavailable:"
                    + str(exc or type(exc).__name__)
                )
                observations.append(
                    {
                        "source_path": source_path,
                        "status": "UNKNOWN",
                        "content": "",
                        "content_segments": [],
                        "epistemic_gain": False,
                        "repository_identity": repository,
                        "requested_branch": branch,
                        "requested_commit": commit,
                        "resolved_commit": resolved_commit,
                        "branch_head_commit": branch_head,
                        "blob_sha": "",
                        "byte_count": 0,
                        "character_count": 0,
                        "segment_count": 0,
                        "content_sha256": "",
                        "blob_sha_verified": False,
                        "complete_file": False,
                        "content_complete": False,
                        "uncertainty": uncertainty,
                        "read_only": True,
                        "bounded": True,
                        "authority_conferred": False,
                    }
                )
                uncertainties.append(
                    source_path + ":" + uncertainty
                )
                continue

            observations.append(
                {
                    "source_path": source_path,
                    "status": "RETRIEVED",
                    "content": content,
                    "content_segments": segments,
                    "epistemic_gain": True,
                    "repository_identity": repository,
                    "requested_branch": branch,
                    "requested_commit": commit,
                    "resolved_commit": resolved_commit,
                    "branch_head_commit": branch_head,
                    "blob_sha": blob_sha,
                    "byte_count": len(raw),
                    "character_count": len(content),
                    "segment_count": len(segments),
                    "content_sha256": hashlib.sha256(raw).hexdigest(),
                    "blob_sha_verified": True,
                    "complete_file": True,
                    "content_complete": True,
                    "read_only": True,
                    "bounded": True,
                    "authority_conferred": False,
                }
            )

            suffix = PurePosixPath(source_path).suffix.casefold()

            if suffix == ".py":
                family = (
                    "tests"
                    if source_path.startswith("tests/")
                    else "python"
                )
            elif suffix == ".sh":
                family = "shell"
            else:
                family = "docs"

            result[family].append(source_path)

        source_paths = [
            item["source_path"]
            for item in observations
            if item["status"] == "RETRIEVED"
        ]

        status = self._checkpoint_status(observations)

        if branch and not branch_head and status == "RETRIEVED":
            status = "PARTIAL"

        return {
            "schema": "FUSION-02-GITHUB-CHECKPOINT-RETRIEVAL-1",
            "capability": "read-checkpoint",
            "keyword": "exact-github-checkpoint",
            "read_only": True,
            "authority_conferred": False,
            "working_context_materialized": False,
            "source_identity_kind": "repository-relative-path",
            "source_paths": source_paths,
            "result": result,
            "read_observations": observations,
            "epistemic_class": "COMMITTED_REPOSITORY_EVIDENCE",
            "uncertainties": uncertainties,
            "checkpoint_identity": {
                "repository": repository,
                "requested_branch": branch,
                "requested_commit": commit,
                "resolved_commit": resolved_commit,
                "branch_head_commit": branch_head,
                "branch_head_matches_commit": bool(
                    branch_head and branch_head == commit
                ),
                "requested_path_count": len(request["paths"]),
                "retrieved_path_count": len(source_paths),
                "complete_files": (
                    len(source_paths) == len(request["paths"])
                ),
                "status": status,
                "read_only": True,
                "authority_conferred": False,
                "human_authority_preserved": True,
            },
        }

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

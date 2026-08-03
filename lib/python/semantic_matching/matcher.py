import re
from pathlib import Path

from python.canonical_entities import SemanticMatch
from python.semantic_engine.engine import SemanticEngine


class SemanticMatcher:
    """Semantic comparison between canonical specifications and repository implementations."""

    _STOPWORDS = set([
        "the", "and", "for", "with", "from", "that", "this", "shall", "must", "toolkit",
        "specification", "specifications", "document", "documents", "system", "subsystem",
        "architecture", "architectural", "implementation", "repository", "canonical", "support",
        "supports", "purpose", "objectives", "workflow", "layer", "layers", "validation",
    ])

    def __init__(self, repository=".", workspace_index=None):
        self.root = Path(repository).resolve()
        self._workspace_index = workspace_index
        self._documents = {}
        self._semantic_report = {}

    def _get_index(self):
        if self._workspace_index is not None:
            return self._workspace_index
        from python.workspace_index import WorkspaceIndexBuilder
        return WorkspaceIndexBuilder(self.root).build()

    def match_document(self, doc, index):
        """Find implementations that satisfy the given canonical document."""
        self._documents[doc.id] = doc
        files = self._candidate_files(index)
        matches = []
        matches.extend(self._compute_exact_match(doc.id, files))
        matches.extend(self._compute_alias_match(doc, files))
        matches.extend(self._compute_semantic_match(doc, files))
        return self._deduplicate(matches)

    def match_all(self, repo):
        """Match all canonical documents against repository implementations."""
        index = self._get_index()
        self._semantic_report = SemanticEngine(self.root, workspace_index=index).analyze()
        results = {}
        for doc in repo.all_documents():
            results[doc.id] = self.match_document(doc, index)
        return results

    def _compute_exact_match(self, doc_id, files):
        doc = self._documents[doc_id]
        exact_slug = self._title_slug(doc)
        aliases = set([exact_slug])
        if exact_slug.endswith("_specification"):
            aliases.add(exact_slug[:-14].rstrip("_"))
        matches = []
        for wf in files:
            ref = self._normalized_ref(wf.path)
            for alias in aliases:
                if alias and alias in ref:
                    matches.append(
                        SemanticMatch(
                            canonical_id=doc_id,
                            implementation_ref=wf.path,
                            match_level=1,
                            confidence=1.0,
                            evidence=["Exact canonical component name '%s' found in %s" % (alias, wf.path)],
                            notes="Exact file/module alignment",
                        )
                    )
                    break
        return matches

    def _compute_alias_match(self, doc, files):
        aliases = self._aliases(doc)
        matches = []
        for wf in files:
            ref = self._normalized_ref(wf.path)
            stem = self._normalized_ref(Path(wf.name).stem)
            for alias in aliases:
                if not alias:
                    continue
                if alias == stem or alias in ref:
                    matches.append(
                        SemanticMatch(
                            canonical_id=doc.id,
                            implementation_ref=wf.path,
                            match_level=2,
                            confidence=0.9,
                            evidence=["Alias '%s' matched %s" % (alias, wf.path)],
                            notes="Normalized alias alignment",
                        )
                    )
                    break
        return matches

    def _compute_semantic_match(self, doc, files):
        keyword_tokens = [token for token in self._document_tokens(doc) if len(token) > 2]
        matches = []

        for wf in files:
            content = self._read_file(wf.path)
            lowered_content = content.lower()
            ref = wf.path.lower()
            path_hits = [token for token in keyword_tokens if token in ref]
            content_hits = [token for token in keyword_tokens if token in lowered_content]
            symbol_hits = self._symbol_hits(wf.path, keyword_tokens)

            if len(set(path_hits + content_hits)) >= 2:
                matches.append(
                    SemanticMatch(
                        canonical_id=doc.id,
                        implementation_ref=wf.path,
                        match_level=3,
                        confidence=0.75,
                        evidence=[
                            "Architectural keywords matched: %s" % ", ".join(sorted(set(path_hits + content_hits))[:6]),
                            "Matched file %s" % wf.path,
                        ],
                        notes="Architectural keyword alignment",
                    )
                )
                continue

            if symbol_hits:
                matches.append(
                    SemanticMatch(
                        canonical_id=doc.id,
                        implementation_ref=wf.path,
                        match_level=4,
                        confidence=0.5,
                        evidence=["Behavioral symbol hits: %s" % ", ".join(symbol_hits[:6])],
                        notes="AST symbol alignment",
                    )
                )
                continue

            partial_score = 0
            partial_evidence = []
            if path_hits:
                partial_score += 1
                partial_evidence.append("Path token hits: %s" % ", ".join(sorted(set(path_hits))[:4]))
            if content_hits:
                partial_score += 1
                partial_evidence.append("Content token hits: %s" % ", ".join(sorted(set(content_hits))[:4]))
            if symbol_hits:
                partial_score += 1
                partial_evidence.append("Symbol token hits: %s" % ", ".join(symbol_hits[:4]))
            if partial_score >= 2:
                matches.append(
                    SemanticMatch(
                        canonical_id=doc.id,
                        implementation_ref=wf.path,
                        match_level=5,
                        confidence=0.3,
                        evidence=partial_evidence,
                        notes="Composite partial alignment",
                    )
                )

        return matches

    def _candidate_files(self, index):
        candidates = []
        seen = set()
        for wf in index.files:
            if wf.extension in (".py", ".sh") or "test" in wf.path.lower():
                if wf.path not in seen:
                    seen.add(wf.path)
                    candidates.append(wf)
        return candidates

    def _aliases(self, doc):
        aliases = []
        title_slug = self._title_slug(doc)
        aliases.append(title_slug)
        title_no_spec = re.sub(r"_specification$", "", title_slug)
        if title_no_spec and title_no_spec not in aliases:
            aliases.append(title_no_spec)
        aliases.append(doc.id.lower().replace("-", "_"))
        tokens = self._document_tokens(doc)
        aliases.extend(["_".join(tokens[:2]), "_".join(tokens[:3])])
        return [alias.strip("_") for alias in aliases if alias and alias.strip("_")]

    def _document_tokens(self, doc):
        values = [doc.title, doc.purpose] + list(doc.objectives) + list(doc.scope_included)
        tokens = []
        seen = set()
        for value in values:
            for token in re.split(r"[^a-zA-Z0-9]+", value.lower()):
                if not token or token in self._STOPWORDS or token.startswith("canon"):
                    continue
                if token not in seen:
                    seen.add(token)
                    tokens.append(token)
        return tokens

    def _title_slug(self, doc):
        title = re.sub(r"\b(spec|specification|v\d+[\.\d]*)\b", " ", doc.title, flags=re.IGNORECASE)
        return self._normalized_ref(title)

    def _normalized_ref(self, value):
        return re.sub(r"[^a-zA-Z0-9]+", "_", value.lower()).strip("_")

    def _read_file(self, relative_path):
        file_path = self.root / relative_path
        try:
            return file_path.read_text(encoding="utf-8")
        except Exception:
            return ""

    def _symbol_hits(self, file_path, tokens):
        symbols = self._semantic_report.get(file_path, {})
        hits = []
        for category in ("classes", "functions", "imports"):
            for symbol in symbols.get(category, []):
                lowered = symbol.lower()
                for token in tokens:
                    if token in lowered:
                        hits.append("%s:%s" % (category[:-1], symbol))
                        break
        return hits

    def _deduplicate(self, matches):
        best = {}
        for match in matches:
            current = best.get(match.implementation_ref)
            if current is None or match.confidence > current.confidence or (
                match.confidence == current.confidence and match.match_level < current.match_level
            ):
                best[match.implementation_ref] = match
        return [best[key] for key in sorted(best)]

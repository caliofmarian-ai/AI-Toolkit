import re
from pathlib import Path

from python.canonical_entities import CanonicalDocument, CanonicalSection, LifecycleStatus


class CanonicalParser:
    """Parse CANON-*.md files into CanonicalDocument entities."""

    _FILENAME_RE = re.compile(r"(CANON-\d+)_.*_v(\d+\.\d+.*)\.md$")
    _DOC_REF_RE = re.compile(r"CANON-\d+")

    def parse_file(self, path):
        """Parse a single CANON-*.md file."""
        path = Path(path)
        text = path.read_text(encoding="utf-8")
        lines = text.splitlines()
        doc_id, filename_version = self._parse_filename(path.name)
        title = self._extract_title(lines, doc_id)
        explicit_version = self._match_line(lines, r"^Version:\s*(.+)$")
        version = explicit_version or filename_version or "0.0.0"
        status = self._extract_status(lines)
        sections = self._parse_sections(doc_id, lines)
        section_map = dict((section.title.lower(), section.content) for section in sections)

        purpose = self._extract_purpose(section_map.get("purpose", ""))
        objectives = self._extract_bullets(section_map.get("objectives", ""))
        if not objectives:
            objectives = self._extract_bullets(section_map.get("goals", ""))
        dependencies = self._extract_dependencies(section_map.get("dependencies", ""))
        invariants = self._extract_bullets(section_map.get("invariants", ""), include_plain_lines=True)
        scope_included, scope_excluded = self._extract_scope(section_map.get("scope", ""))

        return CanonicalDocument(
            id=doc_id,
            filename=path.name,
            title=title,
            version=version,
            status=status,
            purpose=purpose,
            objectives=objectives,
            scope_included=scope_included,
            scope_excluded=scope_excluded,
            dependencies=dependencies,
            invariants=invariants,
            sections=sections,
        )

    def parse_directory(self, docs_path):
        """Parse all CANON-*.md files in a directory."""
        docs_path = Path(docs_path)
        documents = []
        for path in sorted(docs_path.glob("CANON-*.md")):
            if path.is_file():
                documents.append(self.parse_file(path))
        return documents

    def _parse_filename(self, filename):
        match = self._FILENAME_RE.match(filename)
        if match:
            return match.group(1), match.group(2)
        ref = self._DOC_REF_RE.search(filename)
        return (ref.group(0) if ref else Path(filename).stem, "0.0.0")

    def _extract_title(self, lines, doc_id):
        for line in lines:
            stripped = line.strip()
            if not stripped.startswith("# "):
                continue
            title = stripped[2:].strip()
            title = re.sub(r"^%s\s*[—-]\s*" % re.escape(doc_id), "", title).strip()
            return title or doc_id
        return doc_id

    def _extract_status(self, lines):
        explicit = self._match_line(lines, r"^Status:\s*(.+)$")
        if explicit:
            return self._map_status(explicit)
        for index, line in enumerate(lines):
            if line.strip().lower() == "## status":
                for candidate in lines[index + 1:]:
                    stripped = candidate.strip()
                    if not stripped:
                        continue
                    if stripped.startswith("#"):
                        break
                    return self._map_status(stripped)
        return LifecycleStatus.DRAFT

    def _match_line(self, lines, pattern):
        regex = re.compile(pattern)
        for line in lines:
            match = regex.match(line.strip())
            if match:
                return match.group(1).strip()
        return None

    def _parse_sections(self, doc_id, lines):
        sections = []
        current_title = None
        current_content = []
        section_index = 0
        seen_title = False

        for raw_line in lines:
            line = raw_line.rstrip("\n")
            if line.startswith("# "):
                heading = line[2:].strip()
                if not seen_title:
                    seen_title = True
                    continue
                if current_title is not None:
                    sections.append(self._build_section(doc_id, current_title, current_content, section_index))
                    section_index += 1
                current_title = heading
                current_content = []
                continue
            if current_title is not None:
                current_content.append(line)

        if current_title is not None:
            sections.append(self._build_section(doc_id, current_title, current_content, section_index))
        return sections

    def _build_section(self, doc_id, title, content_lines, index):
        slug = self._slugify(title)
        content = "\n".join(content_lines).strip()
        return CanonicalSection(
            id="%s:section:%s" % (doc_id, slug or str(index)),
            document_id=doc_id,
            title=title,
            content=content,
            index=index,
        )

    def _extract_purpose(self, content):
        lines = []
        for line in content.splitlines():
            stripped = line.strip()
            if not stripped or stripped == "---":
                continue
            if stripped.startswith("#"):
                break
            lines.append(stripped)
        return " ".join(lines).strip()

    def _extract_bullets(self, content, include_plain_lines=False):
        items = []
        for line in content.splitlines():
            stripped = line.strip()
            if not stripped or stripped == "---":
                continue
            if stripped.startswith("- "):
                items.append(stripped[2:].strip().rstrip(";"))
            elif include_plain_lines and not stripped.endswith(":") and not stripped.startswith("#"):
                items.append(stripped)
        return items

    def _extract_dependencies(self, content):
        dependencies = []
        seen = set()
        for ref in self._DOC_REF_RE.findall(content):
            if ref not in seen:
                seen.add(ref)
                dependencies.append(ref)
        return dependencies

    def _extract_scope(self, content):
        included = []
        excluded = []
        state = None
        for line in content.splitlines():
            stripped = line.strip()
            lowered = stripped.lower()
            if lowered.startswith("included"):
                state = "included"
                continue
            if lowered.startswith("excluded"):
                state = "excluded"
                continue
            if stripped.startswith("- "):
                item = stripped[2:].strip()
                if state == "excluded":
                    excluded.append(item)
                else:
                    included.append(item)
        return included, excluded

    def _map_status(self, raw_status):
        status = raw_status.strip().lower().replace("-", " ")
        mapping = {
            "draft": LifecycleStatus.DRAFT,
            "review": LifecycleStatus.REVIEW,
            "approved": LifecycleStatus.APPROVED,
            "canonical": LifecycleStatus.APPROVED,
            "implemented": LifecycleStatus.IMPLEMENTED,
            "maintained": LifecycleStatus.MAINTAINED,
            "deprecated": LifecycleStatus.DEPRECATED,
            "archived": LifecycleStatus.ARCHIVED,
        }
        return mapping.get(status, LifecycleStatus.DRAFT)

    def _slugify(self, value):
        value = re.sub(r"[^a-zA-Z0-9]+", "_", value.strip().lower())
        return value.strip("_")

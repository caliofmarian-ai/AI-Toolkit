from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List

from .ast_nodes import DocumentNode, EntityNode, ListValueNode, MapValueNode, ScalarValueNode
from .diagnostics import DiagnosticCategory, DiagnosticCollection
from .lexer import RESERVED_KEYWORDS


@dataclass(frozen=True)
class SemanticAnnotation:
    node_id: str
    semantic_type: str
    properties: Dict[str, object] = field(default_factory=dict)
    canonical_refs: List[str] = field(default_factory=list)
    source_ref: str = ''


@dataclass
class SemanticResult:
    doc_id: str
    title: str
    version: str
    status: str
    classification: str = ''
    source_path: str = ''
    entities: List[Dict] = field(default_factory=list)
    relationships: List[Dict] = field(default_factory=list)
    annotations: List[SemanticAnnotation] = field(default_factory=list)
    diagnostics: DiagnosticCollection = field(default_factory=DiagnosticCollection)


class SemanticAnalyzer:
    def analyze(self, doc: DocumentNode) -> SemanticResult:
        diagnostics = DiagnosticCollection()
        doc_id = doc.header_value('Identifier') or doc.title or doc.doc_type or 'UNIDENTIFIED'
        result = SemanticResult(doc_id=doc_id, title=doc.title, version=doc.version, status=doc.status, classification=doc.classification, source_path=doc.source_path, diagnostics=diagnostics)
        if self._contains_reserved_keyword_conflict(doc):
            diagnostics.error('CSL-0104', 'Reserved keyword used as identifier', DiagnosticCategory.SEMANTIC, doc.source_path)
        identifiers = set()
        for entity in doc.entities():
            entity_data = self._entity(entity, doc_id, identifiers, diagnostics)
            result.entities.append(entity_data)
            result.annotations.append(SemanticAnnotation(entity_data['identifier'], entity.entity_type, entity_data['properties'], source_ref=doc.source_path))
        known_ids = {entity['identifier'] for entity in result.entities}
        for relationship in doc.relationships():
            if relationship.source not in known_ids:
                diagnostics.error('CSL-0201', f'Unresolvable reference: {relationship.source}', DiagnosticCategory.RELATIONSHIP, doc.source_path)
            if relationship.target not in known_ids:
                diagnostics.error('CSL-0201', f'Unresolvable reference: {relationship.target}', DiagnosticCategory.RELATIONSHIP, doc.source_path)
            result.relationships.append({'source': relationship.source, 'relation_type': relationship.relation_type, 'target': relationship.target, 'attributes': {a.name: self._value(a.value) for a in relationship.attributes}})
        for field in ('Title', 'Version', 'Status'):
            if not doc.header_value(field):
                diagnostics.error('CSL-0203', f'Required property missing: {field}', DiagnosticCategory.SEMANTIC, doc.source_path)
        return result

    def _contains_reserved_keyword_conflict(self, doc: DocumentNode) -> bool:
        keywords = RESERVED_KEYWORDS - {'Relationship'}
        for raw_line in doc.source_text.splitlines():
            stripped = raw_line.strip()
            if not stripped or stripped.startswith('#') or ':' not in stripped:
                continue
            name = stripped.split(':', 1)[0].strip()
            if name in keywords:
                if not any(name == entity.entity_type for entity in doc.entities()) or raw_line.startswith('    '):
                    return True
        return False

    def _entity(self, entity: EntityNode, fallback: str, identifiers: set, diagnostics: DiagnosticCollection) -> Dict:
        identifier = self._scalar(entity, 'Identifier') or f'{fallback}:{entity.entity_type}:{len(identifiers)}'
        if identifier in identifiers:
            diagnostics.error('CSL-0200', f'Duplicate identifier within the same scope: {identifier}', DiagnosticCategory.SEMANTIC)
        identifiers.add(identifier)
        for attribute in entity.attributes:
            if attribute.name in RESERVED_KEYWORDS or attribute.name == entity.entity_type:
                diagnostics.error('CSL-0104', f'Reserved keyword used as identifier: {attribute.name}', DiagnosticCategory.SEMANTIC)
        props = {a.name: self._value(a.value) for a in entity.attributes}
        return {'identifier': identifier, 'entity_type': entity.entity_type, 'name': props.get('Name', props.get('Title', identifier)), 'version': props.get('Version', ''), 'status': props.get('Status', ''), 'visibility': props.get('Visibility', 'Public'), 'properties': props}

    def _scalar(self, entity: EntityNode, name: str) -> str:
        attribute = entity.get_attribute(name)
        if attribute and isinstance(attribute.value, ScalarValueNode):
            return str(attribute.value.value)
        return ''

    def _value(self, value):
        if isinstance(value, ScalarValueNode):
            if value.value_type == 'integer':
                return int(value.value)
            if value.value_type == 'decimal':
                return float(value.value)
            if value.value_type == 'boolean':
                return value.value == 'true'
            if value.value_type == 'null':
                return None
            return value.value
        if isinstance(value, ListValueNode):
            return [self._value(item) for item in value.items]
        if isinstance(value, MapValueNode):
            return {entry.key: self._value(entry.value) for entry in value.entries}
        return None

from __future__ import annotations

from typing import List

from .ast_nodes import AttributeNode, DocumentNode, EntityNode, HeaderFieldNode, ListValueNode, MapEntryNode, MapValueNode, RelationshipNode, ScalarValueNode
from .diagnostics import Diagnostic, DiagnosticCategory, DiagnosticSeverity
from .lexer import CslLexer, SourceLocation, Token, TokenType


class CslParser:
    def __init__(self) -> None:
        self._tokens: List[Token] = []
        self._pos = 0
        self._diagnostics: List[Diagnostic] = []

    @property
    def diagnostics(self) -> List[Diagnostic]:
        return list(self._diagnostics)

    def parse_text(self, text: str, source_name: str = '') -> DocumentNode:
        self._diagnostics = []
        self._tokens = CslLexer(text, source_name=source_name).tokenize()
        self._pos = 0
        document = DocumentNode(node_type=None, location=self._peek().location, source_path=source_name, source_text=text)
        document.__post_init__()
        while self._peek().token_type != TokenType.EOF:
            if self._match(TokenType.NEWLINE, TokenType.COMMENT):
                continue
            if self._peek().token_type != TokenType.KEYWORD:
                self._error(self._peek(), 'CSL-0100', 'Expected declaration keyword')
                self._advance()
                continue
            name = self._advance().value
            if not self._consume(TokenType.COLON, 'CSL-0106', f"Missing ':' after {name}"):
                break
            if name == 'Relationship':
                relationship = self._parse_relationship()
                if relationship:
                    document.declarations.append(relationship)
            else:
                entity = self._parse_entity(name)
                if entity:
                    document.declarations.append(entity)
        self._populate_header_fields(document)
        return document

    def _parse_entity(self, entity_type: str):
        entity = EntityNode(node_type=None, location=self._previous().location, entity_type=entity_type)
        entity.__post_init__()
        if self._peek().token_type == TokenType.NEWLINE:
            self._advance()
        if not self._consume(TokenType.INDENT, 'CSL-0103', f'Missing indented block for {entity_type}'):
            return entity
        while self._peek().token_type not in (TokenType.DEDENT, TokenType.EOF):
            if self._match(TokenType.NEWLINE, TokenType.COMMENT):
                continue
            if self._peek().token_type == TokenType.KEYWORD and self._peek().value != 'Relationship':
                child_type = self._advance().value
                self._consume(TokenType.COLON, 'CSL-0106', f"Missing ':' after nested {child_type}")
                child = self._parse_entity(child_type)
                entity.children.append(child)
                continue
            attribute = self._parse_attribute()
            if attribute:
                entity.attributes.append(attribute)
        self._consume(TokenType.DEDENT, 'CSL-0103', f'Missing dedent for {entity_type}')
        return entity

    def _parse_relationship(self):
        location = self._previous().location
        if self._peek().token_type == TokenType.NEWLINE:
            self._advance()
        if not self._consume(TokenType.INDENT, 'CSL-0103', 'Missing indented block for Relationship'):
            return None
        source = self._consume_identifier('CSL-0106', 'Missing relationship source')
        relation = self._consume_identifier('CSL-0106', 'Missing relationship verb')
        target = self._consume_identifier('CSL-0106', 'Missing relationship target')
        relationship = RelationshipNode(node_type=None, location=location, source=source, relation_type=relation, target=target)
        relationship.__post_init__()
        self._consume(TokenType.NEWLINE, 'CSL-0106', 'Missing newline after relationship expression')
        while self._peek().token_type not in (TokenType.DEDENT, TokenType.EOF):
            if self._match(TokenType.NEWLINE, TokenType.COMMENT):
                continue
            attribute = self._parse_attribute()
            if attribute:
                relationship.attributes.append(attribute)
        self._consume(TokenType.DEDENT, 'CSL-0103', 'Missing dedent for Relationship block')
        return relationship

    def _parse_attribute(self):
        token = self._peek()
        if token.token_type != TokenType.IDENTIFIER:
            self._error(token, 'CSL-0100', 'Expected attribute identifier')
            self._advance()
            return None
        name = self._advance().value
        self._consume(TokenType.COLON, 'CSL-0106', f"Missing ':' after attribute {name}")
        if self._peek().token_type == TokenType.NEWLINE:
            self._advance()
            if self._peek().token_type == TokenType.INDENT:
                self._advance()
                value = self._parse_indented_list(token.location)
                self._consume(TokenType.DEDENT, 'CSL-0103', f'Missing dedent for attribute {name}')
            else:
                value = ScalarValueNode(node_type=None, location=token.location, value_type='null', value='')
                value.__post_init__()
        else:
            value = self._parse_value()
            self._consume(TokenType.NEWLINE, 'CSL-0106', f'Missing newline after attribute {name}')
        attribute = AttributeNode(node_type=None, location=token.location, name=name, value=value)
        attribute.__post_init__()
        return attribute

    def _parse_indented_list(self, location):
        items = []
        while self._peek().token_type not in (TokenType.DEDENT, TokenType.EOF):
            if self._match(TokenType.NEWLINE, TokenType.COMMENT):
                continue
            self._consume(TokenType.DASH, 'CSL-0106', 'Missing list item marker')
            items.append(self._parse_value())
            self._consume(TokenType.NEWLINE, 'CSL-0106', 'Missing newline after list item')
        node = ListValueNode(node_type=None, location=location, items=items)
        node.__post_init__()
        return node

    def _parse_value(self):
        token = self._peek()
        if token.token_type == TokenType.LBRACKET:
            return self._parse_inline_list()
        if token.token_type == TokenType.LBRACE:
            return self._parse_map()
        if token.token_type in {TokenType.STRING, TokenType.INTEGER, TokenType.DECIMAL, TokenType.BOOLEAN, TokenType.DATE, TokenType.TIMESTAMP, TokenType.DURATION, TokenType.VERSION, TokenType.NULL, TokenType.IDENTIFIER, TokenType.KEYWORD}:
            self._advance()
            node = ScalarValueNode(node_type=None, location=token.location, value_type=token.token_type.value.lower(), value=token.value)
            node.__post_init__()
            return node
        self._error(token, 'CSL-0100', 'Unexpected token in value')
        self._advance()
        node = ScalarValueNode(node_type=None, location=token.location, value_type='invalid', value='')
        node.__post_init__()
        return node

    def _parse_inline_list(self):
        start = self._advance()
        items = []
        while self._peek().token_type not in (TokenType.RBRACKET, TokenType.EOF):
            items.append(self._parse_value())
            if self._peek().token_type == TokenType.COMMA:
                self._advance()
            else:
                break
        self._consume(TokenType.RBRACKET, 'CSL-0106', 'Missing closing ]')
        node = ListValueNode(node_type=None, location=start.location, items=items)
        node.__post_init__()
        return node

    def _parse_map(self):
        start = self._advance()
        entries = []
        while self._peek().token_type not in (TokenType.RBRACE, TokenType.EOF):
            key_token = self._peek()
            if key_token.token_type not in (TokenType.STRING, TokenType.IDENTIFIER):
                self._error(key_token, 'CSL-0100', 'Expected map key')
                self._advance()
                break
            self._advance()
            self._consume(TokenType.COLON, 'CSL-0106', 'Missing : after map key')
            value = self._parse_value()
            entries.append(MapEntryNode(key_token.value, value))
            if self._peek().token_type == TokenType.COMMA:
                self._advance()
            else:
                break
        self._consume(TokenType.RBRACE, 'CSL-0106', 'Missing closing }')
        node = MapValueNode(node_type=None, location=start.location, entries=entries)
        node.__post_init__()
        return node

    def _populate_header_fields(self, document: DocumentNode):
        entity = next((item for item in document.declarations if isinstance(item, EntityNode)), None)
        if entity is None:
            return
        for field_name in ('Identifier', 'Title', 'Version', 'Status', 'Classification'):
            attribute = entity.get_attribute(field_name)
            if attribute:
                field = HeaderFieldNode(node_type=None, location=attribute.location, name=field_name, value=attribute.value)
                field.__post_init__()
                document.header_fields.append(field)

    def _consume_identifier(self, code: str, message: str) -> str:
        token = self._peek()
        if token.token_type not in (TokenType.IDENTIFIER, TokenType.KEYWORD):
            self._error(token, code, message)
            return ''
        self._advance()
        return token.value

    def _consume(self, token_type: TokenType, code: str, message: str) -> bool:
        if self._peek().token_type == token_type:
            self._advance()
            return True
        self._error(self._peek(), code, message)
        return False

    def _match(self, *token_types: TokenType) -> bool:
        if self._peek().token_type in token_types:
            self._advance()
            return True
        return False

    def _peek(self) -> Token:
        return self._tokens[self._pos]

    def _previous(self) -> Token:
        return self._tokens[self._pos - 1]

    def _advance(self) -> Token:
        token = self._tokens[self._pos]
        if token.token_type != TokenType.EOF:
            self._pos += 1
        return token

    def _error(self, token: Token, code: str, message: str):
        self._diagnostics.append(Diagnostic(DiagnosticSeverity.ERROR, DiagnosticCategory.SYNTAX, code, message, token.location.source, token.location))

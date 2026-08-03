import re

from python.canonical_entities import CanonicalEdge, CanonicalNode, EdgeType, NodeType
from python.knowledge_graph.graph import CanonicalKnowledgeGraph


class CanonicalKnowledgeGraphBuilder:
    """Build canonical knowledge graph from a CanonicalRepository."""

    _STOPWORDS = set([
        "the", "and", "for", "with", "from", "that", "this", "shall", "must",
        "toolkit", "specification", "canonical", "support", "supports", "future",
        "implementation", "architectural", "architecture", "system", "subsystem",
    ])

    def build(self, repo):
        """Build the semantic graph from canonical repository contents."""
        graph = CanonicalKnowledgeGraph()

        for doc in repo.all_documents():
            graph.add_node(
                CanonicalNode(
                    id=doc.id,
                    node_type=NodeType.DOCUMENT,
                    name=doc.title,
                    source_document=doc.filename,
                    version=doc.version,
                    metadata={
                        "status": doc.status.value,
                        "objectives": len(doc.objectives),
                        "dependencies": len(doc.dependencies),
                    },
                    provenance=doc.filename,
                )
            )

            for section in doc.sections:
                graph.add_node(
                    CanonicalNode(
                        id=section.id,
                        node_type=NodeType.SECTION,
                        name=section.title,
                        source_document=doc.filename,
                        version=doc.version,
                        metadata={"index": section.index},
                        provenance=doc.id,
                    )
                )
                graph.add_edge(
                    CanonicalEdge(
                        source_id=doc.id,
                        target_id=section.id,
                        edge_type=EdgeType.CONTAINS,
                        confidence=1.0,
                        metadata={},
                    )
                )

            for dependency in doc.dependencies:
                if graph.get_node(dependency) is None and repo.get_by_id(dependency) is None:
                    graph.add_node(
                        CanonicalNode(
                            id=dependency,
                            node_type=NodeType.DOCUMENT,
                            name=dependency,
                            source_document="",
                            version="",
                            metadata={"placeholder": True},
                            provenance=doc.id,
                        )
                    )
                graph.add_edge(
                    CanonicalEdge(
                        source_id=doc.id,
                        target_id=dependency,
                        edge_type=EdgeType.DEPENDS_ON,
                        confidence=1.0,
                        metadata={},
                    )
                )

            for phrase in self._extract_concepts(doc):
                node_id = "concept:%s" % self._slugify(phrase)
                if graph.get_node(node_id) is None:
                    graph.add_node(
                        CanonicalNode(
                            id=node_id,
                            node_type=self._classify_node_type(phrase),
                            name=phrase,
                            source_document=doc.filename,
                            version=doc.version,
                            metadata={"derived": True},
                            provenance=doc.id,
                        )
                    )
                graph.add_edge(
                    CanonicalEdge(
                        source_id=doc.id,
                        target_id=node_id,
                        edge_type=EdgeType.DEFINES,
                        confidence=0.75,
                        metadata={"derived_from": "objectives_scope"},
                    )
                )

        return graph

    def _extract_concepts(self, doc):
        concepts = []
        seen = set()
        for value in [doc.title] + list(doc.objectives) + list(doc.scope_included):
            phrase = value.strip("- ").strip()
            if not phrase:
                continue
            tokens = [token for token in self._tokenize(phrase) if token not in self._STOPWORDS]
            if not tokens:
                continue
            if len(tokens) > 4:
                tokens = tokens[:4]
            normalized = " ".join(tokens)
            if normalized not in seen:
                seen.add(normalized)
                concepts.append(normalized)
        return concepts

    def _classify_node_type(self, phrase):
        lowered = phrase.lower()
        mapping = [
            ("engine", NodeType.ENGINE),
            ("service", NodeType.SERVICE),
            ("interface", NodeType.INTERFACE),
            ("strategy", NodeType.STRATEGY),
            ("pipeline", NodeType.PIPELINE),
            ("runtime", NodeType.RUNTIME),
            ("config", NodeType.CONFIGURATION),
            ("parameter", NodeType.PARAMETER),
            ("event", NodeType.EVENT),
            ("state", NodeType.STATE),
            ("test", NodeType.TEST),
            ("batch", NodeType.BATCH),
            ("recommend", NodeType.RECOMMENDATION),
            ("module", NodeType.MODULE),
            ("component", NodeType.COMPONENT),
        ]
        for token, node_type in mapping:
            if token in lowered:
                return node_type
        return NodeType.COMPONENT

    def _tokenize(self, value):
        return [token for token in re.split(r"[^a-zA-Z0-9]+", value.lower()) if token]

    def _slugify(self, value):
        return re.sub(r"[^a-zA-Z0-9]+", "_", value.lower()).strip("_")

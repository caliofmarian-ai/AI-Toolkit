from python.canonical_entities import CanonicalEdge, CanonicalNode, EdgeType, NodeType


class CanonicalKnowledgeGraph:
    """Directed semantic graph of canonical architectural concepts."""

    def __init__(self):
        self._nodes = {}
        self._edges = []

    def add_node(self, node):
        self._nodes[node.id] = node

    def add_edge(self, edge):
        self._edges.append(edge)

    def get_node(self, node_id):
        return self._nodes.get(node_id)

    def get_nodes_by_type(self, node_type):
        return [node for node in self._nodes.values() if node.node_type == node_type]

    def get_edges_from(self, node_id):
        return [edge for edge in self._edges if edge.source_id == node_id]

    def get_edges_to(self, node_id):
        return [edge for edge in self._edges if edge.target_id == node_id]

    def neighbors(self, node_id):
        neighbors = []
        for edge in self.get_edges_from(node_id):
            neighbors.append(edge.target_id)
        for edge in self.get_edges_to(node_id):
            neighbors.append(edge.source_id)
        return sorted(set(neighbors))

    def node_count(self):
        return len(self._nodes)

    def edge_count(self):
        return len(self._edges)

    def orphan_nodes(self):
        return [node for node in self._nodes.values() if not self.get_edges_from(node.id) and not self.get_edges_to(node.id)]

    def to_dict(self):
        return {
            "nodes": [
                {
                    "id": node.id,
                    "node_type": node.node_type.value,
                    "name": node.name,
                    "source_document": node.source_document,
                    "version": node.version,
                    "metadata": dict(node.metadata),
                    "provenance": node.provenance,
                }
                for node in sorted(self._nodes.values(), key=lambda item: item.id)
            ],
            "edges": [
                {
                    "source_id": edge.source_id,
                    "target_id": edge.target_id,
                    "edge_type": edge.edge_type.value,
                    "confidence": edge.confidence,
                    "metadata": dict(edge.metadata),
                }
                for edge in self._edges
            ],
        }

    @classmethod
    def from_dict(cls, data):
        graph = cls()
        for node_data in data.get("nodes", []):
            graph.add_node(
                CanonicalNode(
                    id=node_data["id"],
                    node_type=NodeType(node_data["node_type"]),
                    name=node_data["name"],
                    source_document=node_data.get("source_document", ""),
                    version=node_data.get("version", ""),
                    metadata=node_data.get("metadata", {}),
                    provenance=node_data.get("provenance", ""),
                )
            )
        for edge_data in data.get("edges", []):
            graph.add_edge(
                CanonicalEdge(
                    source_id=edge_data["source_id"],
                    target_id=edge_data["target_id"],
                    edge_type=EdgeType(edge_data["edge_type"]),
                    confidence=float(edge_data.get("confidence", 0.0)),
                    metadata=edge_data.get("metadata", {}),
                )
            )
        return graph

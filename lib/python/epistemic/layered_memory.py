"""Layered Memory structural anatomy for PCC-05.

Layered Memory organizes semantic Memory produced by PCC-04 into a
navigable depth structure.

It does not own Persistent Experience, Evidence, Knowledge, CSL, or
Progressive Recall.

A higher memory position must never destroy the route toward deeper
preserved reality.  This module therefore preserves structural
relationships and the existing SedimentedMemory provenance reference
instead of copying raw Experience or Evidence into Memory.

Structural depth describes position only.  It does not establish truth,
authority, certainty, importance, or canonical status.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable
from uuid import uuid4

from .sedimented_memory import SedimentedMemory


class LayeredMemoryError(RuntimeError):
    """Base failure for Layered Memory anatomy."""


class LayeredMemoryIdentityError(LayeredMemoryError):
    """Raised when layered-memory identity is invalid."""


class LayeredMemoryRelationshipError(LayeredMemoryError):
    """Raised when a memory relationship would violate anatomy."""


class LayeredMemoryNavigationError(LayeredMemoryError):
    """Raised when requested navigation cannot be established safely."""


@dataclass(frozen=True)
class LayeredMemoryNodeId:
    """Stable structural identity of one Layered Memory node."""

    value: str

    def __post_init__(self) -> None:
        if not isinstance(self.value, str) or not self.value.strip():
            raise LayeredMemoryIdentityError(
                "Layered Memory node identity must be a non-empty string."
            )

    @classmethod
    def create(cls) -> "LayeredMemoryNodeId":
        return cls(f"LMEM-{uuid4().hex}")

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class LayeredMemoryNode:
    """One semantic Memory positioned inside navigable memory depth.

    ``depth`` is structural only.

    ``parent_ids`` and ``child_ids`` are navigation relationships.
    They do not imply authority, truth, chronology, or provenance.

    Provenance remains owned by the wrapped SedimentedMemory and by the
    deeper epistemic structures to which that Memory refers.
    """

    node_id: LayeredMemoryNodeId
    memory: SedimentedMemory
    depth: int
    parent_ids: tuple[LayeredMemoryNodeId, ...] = ()
    child_ids: tuple[LayeredMemoryNodeId, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.memory, SedimentedMemory):
            raise LayeredMemoryRelationshipError(
                "Layered Memory nodes require real SedimentedMemory."
            )

        if not isinstance(self.depth, int) or isinstance(self.depth, bool):
            raise LayeredMemoryRelationshipError(
                "Layered Memory depth must be an integer."
            )

        if self.depth < 0:
            raise LayeredMemoryRelationshipError(
                "Layered Memory depth cannot be negative."
            )

        if len(set(self.parent_ids)) != len(self.parent_ids):
            raise LayeredMemoryRelationshipError(
                "Duplicate parent relationships are forbidden."
            )

        if len(set(self.child_ids)) != len(self.child_ids):
            raise LayeredMemoryRelationshipError(
                "Duplicate child relationships are forbidden."
            )

        if self.node_id in self.parent_ids:
            raise LayeredMemoryRelationshipError(
                "A Layered Memory node cannot parent itself."
            )

        if self.node_id in self.child_ids:
            raise LayeredMemoryRelationshipError(
                "A Layered Memory node cannot contain itself as child."
            )

    @property
    def provenance_identifier(self) -> str:
        """Expose, but do not replace, PCC-04 provenance navigation."""

        return self.memory.provenance_identifier

    @property
    def sedimentation_identifier(self) -> str:
        """Expose the Sedimentation from which this Memory originated."""

        return self.memory.sedimentation_identifier


@dataclass(frozen=True)
class LayeredMemoryPath:
    """One explicit navigation path through Layered Memory."""

    node_ids: tuple[LayeredMemoryNodeId, ...]

    def __post_init__(self) -> None:
        if not self.node_ids:
            raise LayeredMemoryNavigationError(
                "A Layered Memory path cannot be empty."
            )


class LayeredMemory:
    """Navigable structural anatomy for semantic Memory.

    This is intentionally storage-independent.

    Persistence, Progressive Recall, and CSL integration belong to later
    PCC-05/PCC-06/PCC-07 physiology and must not be smuggled into the
    structural anatomy.
    """

    def __init__(self) -> None:
        self._nodes: dict[LayeredMemoryNodeId, LayeredMemoryNode] = {}

    def __len__(self) -> int:
        return len(self._nodes)

    def nodes(self) -> tuple[LayeredMemoryNode, ...]:
        return tuple(self._nodes.values())

    def get(self, node_id: LayeredMemoryNodeId) -> LayeredMemoryNode:
        try:
            return self._nodes[node_id]
        except KeyError as exc:
            raise LayeredMemoryNavigationError(
                f"Unknown Layered Memory node: {node_id}"
            ) from exc

    def add_root(
        self,
        memory: SedimentedMemory,
        *,
        node_id: LayeredMemoryNodeId | None = None,
    ) -> LayeredMemoryNode:
        identifier = node_id or LayeredMemoryNodeId.create()

        if identifier in self._nodes:
            raise LayeredMemoryIdentityError(
                f"Layered Memory node already exists: {identifier}"
            )

        node = LayeredMemoryNode(
            node_id=identifier,
            memory=memory,
            depth=0,
        )

        self._nodes[identifier] = node
        return node

    def add_child(
        self,
        parent_id: LayeredMemoryNodeId,
        memory: SedimentedMemory,
        *,
        node_id: LayeredMemoryNodeId | None = None,
    ) -> LayeredMemoryNode:
        parent = self.get(parent_id)
        identifier = node_id or LayeredMemoryNodeId.create()

        if identifier in self._nodes:
            raise LayeredMemoryIdentityError(
                f"Layered Memory node already exists: {identifier}"
            )

        child = LayeredMemoryNode(
            node_id=identifier,
            memory=memory,
            depth=parent.depth + 1,
            parent_ids=(parent.node_id,),
        )

        updated_parent = LayeredMemoryNode(
            node_id=parent.node_id,
            memory=parent.memory,
            depth=parent.depth,
            parent_ids=parent.parent_ids,
            child_ids=parent.child_ids + (child.node_id,),
        )

        self._nodes[parent.node_id] = updated_parent
        self._nodes[child.node_id] = child

        return child

    def parents(
        self,
        node_id: LayeredMemoryNodeId,
    ) -> tuple[LayeredMemoryNode, ...]:
        node = self.get(node_id)
        return tuple(self.get(item) for item in node.parent_ids)

    def children(
        self,
        node_id: LayeredMemoryNodeId,
    ) -> tuple[LayeredMemoryNode, ...]:
        node = self.get(node_id)
        return tuple(self.get(item) for item in node.child_ids)

    def toward_surface(
        self,
        node_id: LayeredMemoryNodeId,
    ) -> LayeredMemoryPath:
        """Navigate from a deeper node toward a structural root."""

        current = self.get(node_id)
        path = [current.node_id]
        visited = {current.node_id}

        while current.parent_ids:
            if len(current.parent_ids) != 1:
                raise LayeredMemoryNavigationError(
                    "RUN 001 supports one structural parent per node."
                )

            parent = self.get(current.parent_ids[0])

            if parent.node_id in visited:
                raise LayeredMemoryNavigationError(
                    "Layered Memory cycle detected."
                )

            if parent.depth >= current.depth:
                raise LayeredMemoryNavigationError(
                    "Parent depth must be shallower than child depth."
                )

            path.append(parent.node_id)
            visited.add(parent.node_id)
            current = parent

        return LayeredMemoryPath(tuple(path))

    def toward_depth(
        self,
        node_id: LayeredMemoryNodeId,
    ) -> tuple[LayeredMemoryNode, ...]:
        """Return all reachable descendants, shallowest first."""

        start = self.get(node_id)
        discovered: list[LayeredMemoryNode] = []
        queue = list(self.children(start.node_id))
        visited = {start.node_id}

        while queue:
            node = queue.pop(0)

            if node.node_id in visited:
                raise LayeredMemoryNavigationError(
                    "Layered Memory cycle detected."
                )

            visited.add(node.node_id)
            discovered.append(node)
            queue.extend(self.children(node.node_id))

        return tuple(discovered)

    def provenance_route(
        self,
        node_id: LayeredMemoryNodeId,
    ) -> tuple[str, str]:
        """Expose the existing route out of Memory toward deeper reality.

        The first identity is the Sedimentation that produced Memory.
        The second is the provenance identity already preserved by PCC-04.

        RUN 001 does not pretend that it owns or materializes the deeper
        Experience/Evidence graph.
        """

        node = self.get(node_id)

        return (
            node.sedimentation_identifier,
            node.provenance_identifier,
        )

    def memories_at_depth(
        self,
        depth: int,
    ) -> tuple[LayeredMemoryNode, ...]:
        if not isinstance(depth, int) or isinstance(depth, bool) or depth < 0:
            raise LayeredMemoryNavigationError(
                "Requested depth must be a non-negative integer."
            )

        return tuple(
            node
            for node in self._nodes.values()
            if node.depth == depth
        )

    def add_chain(
        self,
        memories: Iterable[SedimentedMemory],
    ) -> tuple[LayeredMemoryNode, ...]:
        """Materialize a simple depth chain without semantic invention."""

        material = tuple(memories)

        if not material:
            raise LayeredMemoryRelationshipError(
                "A Layered Memory chain requires at least one Memory."
            )

        created = [self.add_root(material[0])]

        for memory in material[1:]:
            created.append(
                self.add_child(created[-1].node_id, memory)
            )

        return tuple(created)

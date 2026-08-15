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

from .sedimented_memory import (
    SedimentedMemory,
    SedimentedMemoryId,
)


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


# ---------------------------------------------------------------------------
# PCC-05 — Conservation of Layered Memory in Time
# Technical execution: RUN 002
# ---------------------------------------------------------------------------

from pathlib import Path as _Path
import json as _json


class LayeredMemoryPersistenceError(LayeredMemoryError):
    """Layered Memory could not be safely preserved or reconstructed."""


class LayeredMemoryRepository:
    """Durable body for Layered Memory.

    The repository preserves the existing LayeredMemory anatomy across
    process death.

    It does not redefine Memory semantics and does not own Experience,
    Evidence, Sedimentation, Knowledge, CSL, or Progressive Recall.

    The physical JSON representation is a versioned recipient, not the
    identity or meaning of Layered Memory.
    """

    _FILENAME = "layered_memory.json"
    _SCHEMA = "PCC-05-LAYERED-MEMORY-1"

    def __init__(self, layered_memory: LayeredMemory | None = None) -> None:
        if layered_memory is not None and not isinstance(
            layered_memory,
            LayeredMemory,
        ):
            raise TypeError(
                "layered_memory must be LayeredMemory or None"
            )

        self._layered_memory = layered_memory or LayeredMemory()

    @property
    def layered_memory(self) -> LayeredMemory:
        return self._layered_memory

    def save(self, directory: str | _Path) -> _Path:
        root = _Path(directory)
        root.mkdir(parents=True, exist_ok=True)

        path = root / self._FILENAME

        payload = {
            "schema": self._SCHEMA,
            "nodes": [
                {
                    "node_id": str(node.node_id),
                    "depth": node.depth,
                    "parent_ids": [
                        str(item) for item in node.parent_ids
                    ],
                    "child_ids": [
                        str(item) for item in node.child_ids
                    ],
                    "memory": {
                        "memory_id": str(node.memory.memory_id),
                        "sedimentation_identifier":
                            node.memory.sedimentation_identifier,
                        "meaning": node.memory.meaning,
                        "provenance_identifier":
                            node.memory.provenance_identifier,
                        "uncertainty": node.memory.uncertainty,
                    },
                }
                for node in self._layered_memory.nodes()
            ],
        }

        try:
            path.write_text(
                _json.dumps(
                    payload,
                    indent=2,
                    ensure_ascii=False,
                ) + "\n",
                encoding="utf-8",
            )
        except OSError as exc:
            raise LayeredMemoryPersistenceError(
                f"could not preserve Layered Memory: {exc}"
            ) from exc

        return path

    @classmethod
    def load(
        cls,
        directory: str | _Path,
    ) -> "LayeredMemoryRepository":
        path = _Path(directory) / cls._FILENAME

        if not path.exists():
            return cls()

        try:
            payload = _json.loads(
                path.read_text(encoding="utf-8")
            )
        except (OSError, _json.JSONDecodeError) as exc:
            raise LayeredMemoryPersistenceError(
                f"could not reconstruct Layered Memory: {exc}"
            ) from exc

        if not isinstance(payload, dict):
            raise LayeredMemoryPersistenceError(
                "Layered Memory persistent body must be an object"
            )

        if payload.get("schema") != cls._SCHEMA:
            raise LayeredMemoryPersistenceError(
                "unsupported Layered Memory persistence schema"
            )

        raw_nodes = payload.get("nodes")

        if not isinstance(raw_nodes, list):
            raise LayeredMemoryPersistenceError(
                "Layered Memory nodes must be represented as a list"
            )

        layered = LayeredMemory()

        try:
            reconstructed: dict[
                LayeredMemoryNodeId,
                LayeredMemoryNode,
            ] = {}

            for raw in raw_nodes:
                if not isinstance(raw, dict):
                    raise TypeError(
                        "each persisted node must be an object"
                    )

                raw_memory = raw["memory"]

                if not isinstance(raw_memory, dict):
                    raise TypeError(
                        "persisted Memory must be an object"
                    )

                memory = SedimentedMemory(
                    memory_id=SedimentedMemoryId(
                        raw_memory["memory_id"]
                    ),
                    sedimentation_identifier=raw_memory[
                        "sedimentation_identifier"
                    ],
                    meaning=raw_memory["meaning"],
                    provenance_identifier=raw_memory[
                        "provenance_identifier"
                    ],
                    uncertainty=raw_memory.get("uncertainty"),
                )

                node = LayeredMemoryNode(
                    node_id=LayeredMemoryNodeId(
                        raw["node_id"]
                    ),
                    memory=memory,
                    depth=raw["depth"],
                    parent_ids=tuple(
                        LayeredMemoryNodeId(item)
                        for item in raw["parent_ids"]
                    ),
                    child_ids=tuple(
                        LayeredMemoryNodeId(item)
                        for item in raw["child_ids"]
                    ),
                )

                if node.node_id in reconstructed:
                    raise LayeredMemoryIdentityError(
                        "duplicate persisted Layered Memory identity"
                    )

                reconstructed[node.node_id] = node

            cls._validate_reconstructed(reconstructed)

            layered._nodes.update(reconstructed)

        except (
            KeyError,
            TypeError,
            ValueError,
            LayeredMemoryError,
        ) as exc:
            raise LayeredMemoryPersistenceError(
                f"invalid persisted Layered Memory anatomy: {exc}"
            ) from exc

        return cls(layered)

    @staticmethod
    def _validate_reconstructed(
        nodes: dict[LayeredMemoryNodeId, LayeredMemoryNode],
    ) -> None:
        for node in nodes.values():
            if node.depth == 0 and node.parent_ids:
                raise LayeredMemoryRelationshipError(
                    "surface Memory cannot have a parent"
                )

            if node.depth > 0 and not node.parent_ids:
                raise LayeredMemoryRelationshipError(
                    "deeper Memory must preserve a path toward surface"
                )

            if len(node.parent_ids) > 1:
                raise LayeredMemoryRelationshipError(
                    "RUN 002 supports one structural parent per node"
                )

            for parent_id in node.parent_ids:
                if parent_id not in nodes:
                    raise LayeredMemoryRelationshipError(
                        "persisted parent does not exist"
                    )

                parent = nodes[parent_id]

                if node.node_id not in parent.child_ids:
                    raise LayeredMemoryRelationshipError(
                        "parent/child relationship is not reciprocal"
                    )

                if parent.depth + 1 != node.depth:
                    raise LayeredMemoryRelationshipError(
                        "persisted depth relationship is invalid"
                    )

            for child_id in node.child_ids:
                if child_id not in nodes:
                    raise LayeredMemoryRelationshipError(
                        "persisted child does not exist"
                    )

                child = nodes[child_id]

                if node.node_id not in child.parent_ids:
                    raise LayeredMemoryRelationshipError(
                        "child/parent relationship is not reciprocal"
                    )

                if child.depth != node.depth + 1:
                    raise LayeredMemoryRelationshipError(
                        "persisted child depth is invalid"
                    )

        # Every deeper node must actually be able to return to a root.
        for node in nodes.values():
            current = node
            visited: set[LayeredMemoryNodeId] = set()

            while current.parent_ids:
                if current.node_id in visited:
                    raise LayeredMemoryRelationshipError(
                        "persisted Layered Memory contains a cycle"
                    )

                visited.add(current.node_id)
                current = nodes[current.parent_ids[0]]

            if current.depth != 0:
                raise LayeredMemoryRelationshipError(
                    "persisted Memory cannot reach structural surface"
                )

# ---------------------------------------------------------------------------
# PCC-05 — Bidirectional Travel Through Layered Memory
# Technical execution: RUN 003
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class LayeredMemoryTraversal:
    """One living position while travelling through Layered Memory.

    The traversal remembers the exact structural route actually travelled.

    It does not choose relevance, summarize Memory, perform Progressive
    Recall, create CSL, or assign epistemic authority.

    ``trail`` begins at the position where this traversal entered Memory
    and ends at the current position.
    """

    layered_memory: LayeredMemory
    trail: tuple[LayeredMemoryNodeId, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.layered_memory, LayeredMemory):
            raise LayeredMemoryNavigationError(
                "Traversal requires real LayeredMemory."
            )

        if not self.trail:
            raise LayeredMemoryNavigationError(
                "Traversal requires an entry position."
            )

        for node_id in self.trail:
            self.layered_memory.get(node_id)

        for parent_id, child_id in zip(
            self.trail,
            self.trail[1:],
        ):
            parent = self.layered_memory.get(parent_id)

            if child_id not in parent.child_ids:
                raise LayeredMemoryNavigationError(
                    "Traversal trail must follow real child relationships."
                )

    @classmethod
    def enter(
        cls,
        layered_memory: LayeredMemory,
        node_id: LayeredMemoryNodeId,
    ) -> "LayeredMemoryTraversal":
        """Enter Layered Memory at one existing position."""

        layered_memory.get(node_id)
        return cls(layered_memory, (node_id,))

    @property
    def current(self) -> LayeredMemoryNode:
        """Return the Memory position currently inhabited."""

        return self.layered_memory.get(self.trail[-1])

    @property
    def entry(self) -> LayeredMemoryNode:
        """Return the position where this traversal entered Memory."""

        return self.layered_memory.get(self.trail[0])

    @property
    def travelled_path(self) -> LayeredMemoryPath:
        """Expose the exact structural route travelled so far."""

        return LayeredMemoryPath(self.trail)

    def deeper_options(self) -> tuple[LayeredMemoryNode, ...]:
        """Expose immediate deeper positions without choosing one."""

        return self.layered_memory.children(self.current.node_id)

    def enter_deeper(
        self,
        child_id: LayeredMemoryNodeId,
    ) -> "LayeredMemoryTraversal":
        """Travel exactly one structural layer deeper."""

        current = self.current

        if child_id not in current.child_ids:
            raise LayeredMemoryNavigationError(
                "Requested Memory is not an immediate deeper position."
            )

        return LayeredMemoryTraversal(
            self.layered_memory,
            self.trail + (child_id,),
        )

    def can_return(self) -> bool:
        """Whether this traversal can return along its travelled route."""

        return len(self.trail) > 1

    def return_toward_surface(self) -> "LayeredMemoryTraversal":
        """Return exactly one step along the route actually travelled."""

        if not self.can_return():
            raise LayeredMemoryNavigationError(
                "Traversal is already at its entry position."
            )

        return LayeredMemoryTraversal(
            self.layered_memory,
            self.trail[:-1],
        )

    def return_to_entry(self) -> "LayeredMemoryTraversal":
        """Return to the position where this traversal entered Memory."""

        return LayeredMemoryTraversal(
            self.layered_memory,
            (self.trail[0],),
        )

    def provenance_route(self) -> tuple[str, str]:
        """Expose the current Memory's existing exit toward deeper reality."""

        return self.layered_memory.provenance_route(
            self.current.node_id
        )

from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class Entity:

    identifier: str

    name: str

    entity_type: str

    version: str = "1.0.0"

    status: str = "ACTIVE"

    attributes: Dict = field(default_factory=dict)

    relationships: List[str] = field(default_factory=list)


@dataclass
class Relationship:

    source: str

    target: str

    relation: str

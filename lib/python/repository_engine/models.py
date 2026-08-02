from dataclasses import dataclass

@dataclass
class RepositoryItem:

    path: str

    name: str

    item_type: str

    size: int

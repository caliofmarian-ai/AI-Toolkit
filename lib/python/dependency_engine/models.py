from dataclasses import dataclass

@dataclass
class Dependency:

    source: str

    target: str

    dependency_type: str

    status: str = "ACTIVE"

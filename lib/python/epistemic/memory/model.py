"""
Memory Domain

A Memory is immutable.

It represents one preserved experience.
"""

from dataclasses import dataclass


@dataclass(frozen=True)

class Memory:

    id: str

    timestamp: str

    title: str

    content: str

    session: str

    capability: str

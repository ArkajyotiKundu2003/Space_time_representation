"""
Process and framed partial order conversion utilities.
"""

from typing import List, Optional
from dataclasses import dataclass


@dataclass
class Process:
    name: str
    inputs: List[str]
    outputs: List[str]
    metadata: Optional[dict] = None

    def __repr__(self):
        return f"Process(name={self.name}, inputs={self.inputs}, outputs={self.outputs})"

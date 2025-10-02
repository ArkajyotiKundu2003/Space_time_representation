"""
Implementation objects represent decompositions of a Process into boxes (components)
and the associated Framed Partial Order (FPO).
We use networkx.DiGraph to represent the partial order between boxes and frame elements.
"""

from typing import List, Dict, Optional, Tuple
import networkx as nx
from dataclasses import dataclass, field
from src.core.processes import Process


@dataclass
class Component:
    """A box/process used inside an implementation"""
    name: str
    inputs: List[str] = field(default_factory=list)
    outputs: List[str] = field(default_factory=list)
    metadata: Optional[dict] = None


class FramedPartialOrder:
    def __init__(self, inputs: List[str], outputs: List[str]):
        self.graph = nx.DiGraph()
        self.frame_inputs = list(inputs)
        self.frame_outputs = list(outputs)
        # create nodes for frame elements
        for i in self.frame_inputs + self.frame_outputs:
            self.graph.add_node(i, frame=True)

    def add_internal(self, name: str):
        self.graph.add_node(name, frame=False)
        return name

    def add_order(self, a: str, b: str):
        """Add order a <= b (edge a->b)"""
        self.graph.add_edge(a, b)
        if not nx.is_directed_acyclic_graph(self.graph):
            self.graph.remove_edge(a, b)
            raise ValueError("Order would create cycle")

    def nodes(self):
        return list(self.graph.nodes)

    def is_earlier(self, a, b):
        if a == b:
            return True
        return nx.has_path(self.graph, a, b)

    def copy(self):
        new = FramedPartialOrder(self.frame_inputs, self.frame_outputs)
        new.graph = self.graph.copy()
        return new

    def __repr__(self):
        return f"FPO(inputs={len(self.frame_inputs)}, outputs={len(self.frame_outputs)}, nodes={len(self.graph.nodes)})"


@dataclass
class Implementation:
    process: Process
    fpo: FramedPartialOrder
    components: List[Component] = field(default_factory=list)
    name: Optional[str] = None

    def add_component(self, comp: Component):
        self.components.append(comp)

    def __repr__(self):
        return f"Implementation(process={self.process.name}, name={self.name}, components={len(self.components)})"


class ImplementationSet:
    def __init__(self, implementations: List[Implementation] = None):
        self.implementations = implementations or []

    def add(self, impl: Implementation):
        self.implementations.append(impl)

"""
Spacetime partial order implementation (discrete).
Uses networkx.DiGraph to represent order relations (x -> y means x <= y).
"""

from typing import Iterable, List
import networkx as nx


class Spacetime:
    """
    A simple discrete spacetime represented by a partial order (DAG).
    Points are labeled strings.
    """

    def __init__(self):
        self._graph = nx.DiGraph()

    def add_point(self, label: str):
        self._graph.add_node(label)

    def add_relation(self, earlier: str, later: str):
        """Add causal relation (earlier <= later). If it creates a cycle, raises."""
        self._graph.add_edge(earlier, later)
        if not nx.is_directed_acyclic_graph(self._graph):
            self._graph.remove_edge(earlier, later)
            raise ValueError("Adding relation would create cycle")

    def points(self) -> List[str]:
        return list(self._graph.nodes)

    def is_earlier(self, a: str, b: str) -> bool:
        """Return True if a <= b in the partial order (a is in causal past of b)"""
        if a == b:
            return True
        return nx.has_path(self._graph, a, b)

    def predecessors(self, label: str) -> Iterable[str]:
        return self._graph.predecessors(label)

    def successors(self, label: str) -> Iterable[str]:
        return self._graph.successors(label)

    def __repr__(self):
        return f"Spacetime(points={len(self._graph.nodes)})"

    def as_nx(self):
        return self._graph.copy()

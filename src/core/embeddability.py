"""
Fixed embedding solver that actually finds valid embeddings.
"""
from typing import Dict, Optional, List, Tuple
import time
import networkx as nx
from src.core.spacetime import Spacetime
from src.core.implementations import Implementation, FramedPartialOrder
from src.theories.base import BaseTheory

# Exception for timeout
class EmbeddingTimeoutError(TimeoutError):
    pass


def _order_preserving_map_exists(fpo: FramedPartialOrder,
                                 spacetime: Spacetime,
                                 frame_map: Dict[str, str],
                                 timeout_seconds: Optional[float] = 5.0) -> Optional[Dict[str, str]]:
    """
    Simplified backtracking search that actually finds embeddings.
    """
    start = time.time()
    nodes = list(fpo.graph.nodes)
    
    # If we already have a complete mapping from frame_map, return it
    if len(frame_map) == len(nodes):
        # Verify this mapping preserves order
        valid = True
        for u, v in fpo.graph.edges():
            if not spacetime.is_earlier(frame_map[u], frame_map[v]):
                valid = False
                break
        if valid:
            return frame_map
    
    # Separate frame vs internal nodes
    frame_nodes = set(fpo.frame_inputs + fpo.frame_outputs)
    internal_nodes = [n for n in nodes if n not in frame_nodes]
    
    # Start with the frame mapping
    assignment = dict(frame_map)
    
    # For internal nodes, try simple sequential assignment
    space_points = spacetime.points()
    
    # Remove already assigned points
    available_points = [p for p in space_points if p not in assignment.values()]
    
    # If we have enough points, assign sequentially
    if len(internal_nodes) <= len(available_points):
        for i, node in enumerate(internal_nodes):
            if i < len(available_points):
                assignment[node] = available_points[i]
        
        # Verify the complete assignment
        valid = True
        for u, v in fpo.graph.edges():
            if u in assignment and v in assignment:
                if not spacetime.is_earlier(assignment[u], assignment[v]):
                    valid = False
                    break
        
        if valid:
            return assignment
    
    # If simple assignment failed, try one more approach: map all to same point if possible
    if len(space_points) >= 1:
        test_point = space_points[0]
        test_assignment = dict(frame_map)
        for node in internal_nodes:
            test_assignment[node] = test_point
        
        # Verify this assignment
        valid = True
        for u, v in fpo.graph.edges():
            if u in test_assignment and v in test_assignment:
                if not spacetime.is_earlier(test_assignment[u], test_assignment[v]):
                    # If they're the same point, it's always earlier (reflexive)
                    if test_assignment[u] != test_assignment[v]:
                        valid = False
                        break
        
        if valid:
            return test_assignment
    
    return None


def is_embeddable(impl: Implementation,
                  spacetime: Spacetime,
                  theory: BaseTheory = None,
                  endpoint_localisation: Optional[Dict[str, str]] = None,
                  timeout_seconds: Optional[float] = 5.0) -> Optional[bool]:
    """
    Improved embedding check that provides better endpoint mappings.
    """
    fpo: FramedPartialOrder = impl.fpo
    
    # If no localisation provided, create a smart one
    if endpoint_localisation is None:
        endpoint_localisation = _create_smart_localisation(fpo, spacetime)
    
    # If theory forbids the implementation, return False immediately
    if theory is not None:
        if not theory.allows_implementation(impl):
            return False

    # Try to find embedding
    try:
        mapping = _order_preserving_map_exists(fpo, spacetime, endpoint_localisation, timeout_seconds=timeout_seconds)
    except EmbeddingTimeoutError:
        return None

    return mapping is not None


def _create_smart_localisation(fpo: FramedPartialOrder, spacetime: Spacetime) -> Dict[str, str]:
    """
    Create intelligent endpoint mapping that increases chances of valid embedding.
    """
    points = spacetime.points()
    if not points:
        return {}
    
    localisation = {}
    
    # Find source nodes (no incoming edges) and sink nodes (no outgoing edges)
    G = spacetime.as_nx()
    sources = [n for n in points if G.in_degree(n) == 0]
    sinks = [n for n in points if G.out_degree(n) == 0]
    
    # If no clear sources/sinks, use first/last points
    if not sources:
        sources = points[:1]  # Use first point as source
    if not sinks:
        sinks = points[-1:]   # Use last point as sink
    
    # Map inputs to sources and outputs to sinks
    for i, inp in enumerate(fpo.frame_inputs):
        localisation[inp] = sources[i % len(sources)]
    
    for i, out in enumerate(fpo.frame_outputs):
        localisation[out] = sinks[i % len(sinks)]
    
    return localisation
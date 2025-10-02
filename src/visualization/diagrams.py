import matplotlib.pyplot as plt
import networkx as nx
from src.core.implementations import Implementation
import numpy as np

def draw_process_diagram(impl: Implementation, fig=None):
    """
    Draw process diagram on provided figure or create new one.
    """
    if fig is None:
        fig = plt.figure(figsize=(12, 8))
    
    ax = fig.add_subplot(111)
    fpo = impl.fpo
    G = fpo.graph
    
    # Create hierarchical layout
    pos = _hierarchical_layout(G, fpo.frame_inputs, fpo.frame_outputs)
    
    # Define node groups
    frame_nodes = set(fpo.frame_inputs + fpo.frame_outputs)
    input_nodes = [n for n in frame_nodes if n in fpo.frame_inputs]
    output_nodes = [n for n in frame_nodes if n in fpo.frame_outputs]
    internal_nodes = [n for n in G.nodes() if n not in frame_nodes]
    
    # Draw edges
    nx.draw_networkx_edges(G, pos, ax=ax, arrows=True, arrowsize=20, 
                          edge_color='gray', width=2, alpha=0.7)
    
    # Draw nodes with different styles
    nx.draw_networkx_nodes(G, pos, nodelist=input_nodes, ax=ax,
                          node_size=1200, node_color='lightgreen', 
                          node_shape='s', edgecolors='darkgreen', linewidths=2)
    nx.draw_networkx_nodes(G, pos, nodelist=output_nodes, ax=ax,
                          node_size=1200, node_color='lightcoral', 
                          node_shape='s', edgecolors='darkred', linewidths=2)
    nx.draw_networkx_nodes(G, pos, nodelist=internal_nodes, ax=ax,
                          node_size=1000, node_color='lightblue', 
                          node_shape='o', edgecolors='darkblue', linewidths=2)
    
    # Draw labels
    labels = {node: node for node in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels, ax=ax, font_size=10, font_weight='bold')
    
    ax.set_title(f"Process: {impl.process.name} | Implementation: {impl.name}", 
                fontsize=12, fontweight='bold', pad=20)
    ax.axis('off')
    
    return fig

def _hierarchical_layout(G, inputs, outputs):
    """Create hierarchical layout."""
    pos = {}
    
    input_nodes = list(inputs)
    output_nodes = list(outputs)
    internal_nodes = [n for n in G.nodes() if n not in inputs and n not in outputs]
    
    # Position inputs on left
    for i, node in enumerate(input_nodes):
        pos[node] = (0, i - len(input_nodes)/2)
    
    # Position outputs on right  
    for i, node in enumerate(output_nodes):
        pos[node] = (4, i - len(output_nodes)/2)
    
    # Position internal nodes in middle
    for i, node in enumerate(internal_nodes):
        pos[node] = (2, i - len(internal_nodes)/2)
    
    return pos
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from src.core.implementations import Implementation
from src.core.spacetime import Spacetime

def plot_embedding_result(impl: Implementation, spacetime: Spacetime, theory, mapping=None, fig=None):
    """
    Plot embedding result on provided figure.
    """
    if fig is None:
        fig = plt.figure(figsize=(14, 6))
    
    # Create two subplots
    ax1 = fig.add_subplot(121)  # Spacetime structure
    ax2 = fig.add_subplot(122)  # Embedding result
    
    _plot_spacetime_structure(ax1, spacetime)
    _plot_embedding_mapping(ax2, impl, spacetime, theory, mapping)
    
    fig.suptitle(f"Embedding Analysis: {impl.process.name} → {theory.name if theory else 'No Theory'}", 
                fontsize=14, fontweight='bold')
    
    return fig

def _plot_spacetime_structure(ax, spacetime):
    """Plot spacetime causal structure."""
    Gs = spacetime.as_nx()
    if len(Gs.nodes()) == 0:
        ax.text(0.5, 0.5, "No spacetime points", ha='center', va='center', fontstyle='italic')
        ax.set_title("Spacetime Structure", fontweight='bold')
        return
    
    # Use spring layout
    pos = nx.spring_layout(Gs, seed=42)
    
    # Draw edges
    nx.draw_networkx_edges(Gs, pos, ax=ax, edge_color='red', arrows=True, 
                          arrowsize=20, width=2, alpha=0.7)
    
    # Draw nodes
    nx.draw_networkx_nodes(Gs, pos, ax=ax, node_size=800, 
                          node_color='lightyellow', edgecolors='darkred', 
                          linewidths=2)
    
    # Draw labels
    nx.draw_networkx_labels(Gs, pos, ax=ax, font_size=10, font_weight='bold')
    
    ax.set_title("Spacetime Causal Structure", fontweight='bold', fontsize=12)
    ax.grid(True, alpha=0.3)
    ax.set_facecolor('#f8f9fa')

def _plot_embedding_mapping(ax, impl, spacetime, theory, mapping):
    """Plot the embedding mapping."""
    Gs = spacetime.as_nx()
    if len(Gs.nodes()) == 0:
        ax.text(0.5, 0.5, "No spacetime points", ha='center', va='center', fontstyle='italic')
        ax.set_title("Embedding Result", fontweight='bold')
        return
    
    pos = nx.spring_layout(Gs, seed=42)
    
    # Draw base spacetime
    nx.draw_networkx_nodes(Gs, pos, ax=ax, node_size=600,
                          node_color='lightgrey', edgecolors='darkgrey', 
                          linewidths=1, alpha=0.6)
    nx.draw_networkx_labels(Gs, pos, {n: n for n in Gs.nodes()}, ax=ax, 
                           font_size=8, font_color='darkgrey')
    nx.draw_networkx_edges(Gs, pos, ax=ax, edge_color='lightgrey', 
                          arrows=True, arrowsize=15, alpha=0.4)
    
    if mapping:
        # Draw successful embedding
        result_text = "✅ EMBEDDABLE"
        result_color = 'green'
        
        for fpo_node, space_point in mapping.items():
            x, y = pos[space_point]
            
            if fpo_node in impl.fpo.frame_inputs:
                color, marker, size = 'green', 's', 800
            elif fpo_node in impl.fpo.frame_outputs:
                color, marker, size = 'red', 's', 800
            else:
                color, marker, size = 'blue', 'o', 600
            
            ax.scatter(x, y, s=size, c=color, marker=marker, 
                      edgecolors='black', linewidth=2, zorder=3)
            
            # Add label
            ax.annotate(f"{fpo_node}", (x, y), 
                       xytext=(10, 10), textcoords='offset points',
                       fontsize=9, fontweight='bold',
                       bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.9))
    else:
        # Failed embedding
        result_text = "❌ NOT EMBEDDABLE"
        result_color = 'red'
        ax.text(0.5, 0.5, "No valid embedding found", 
               ha='center', va='center', fontsize=12, fontweight='bold',
               transform=ax.transAxes)
    
    ax.set_title("Embedding Result", fontweight='bold', fontsize=12)
    ax.text(0.5, -0.1, result_text, transform=ax.transAxes, ha='center',
            fontsize=12, fontweight='bold', color='white',
            bbox=dict(boxstyle="round,pad=0.5", facecolor=result_color, edgecolor='black'))
    ax.grid(True, alpha=0.3)
    ax.set_facecolor('#f8f9fa')
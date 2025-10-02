#!/usr/bin/env python3
"""
Simplified demo without user input - automatically runs examples and saves images.
"""
import os
import datetime
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt

from src.core.processes import Process
from src.core.implementations import Implementation, FramedPartialOrder, Component
from src.core.spacetime import Spacetime
from src.core.embeddability import is_embeddable, EmbeddingTimeoutError
from src.theories.classical import ClassicalTheory
from src.theories.quantum import QuantumTheory
from src.theories.boxworld import BoxWorldTheory
from src.examples.pr_box import pr_box_process, pr_box_implementations
from src.examples.bell import bell_process, bell_implementations
from src.examples.cnot import cnot_process, cnot_implementations
from src.visualization.diagrams import draw_process_diagram
from src.visualization.spacetime import plot_embedding_result

import logging
logging.basicConfig(level=logging.INFO)

# Global variable to track output directory
OUTPUT_DIR = None


def setup_output_directory():
    """Create output directory for saving images"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"spacetime_demo_{timestamp}"
    os.makedirs(output_dir, exist_ok=True)
    print(f"📁 Output directory created: {output_dir}")
    return output_dir


def save_plot(fig, description, step_counter):
    """Save matplotlib figure properly"""
    if OUTPUT_DIR is None:
        return step_counter
        
    # Clean description for filename
    filename = description.replace(' ', '_').replace(':', '').replace('→', 'to')
    filename = f"{step_counter:02d}_{filename}.png"
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    fig.savefig(filepath, dpi=150, bbox_inches='tight', facecolor='white')
    print(f"💾 Saved: {filename}")
    plt.close(fig)  # Close the figure to free memory
    return step_counter + 1


def create_simple_spacetime():
    """Create a simple spacetime for testing"""
    spacetime = Spacetime()
    spacetime.add_point("A")
    spacetime.add_point("B")
    spacetime.add_point("C")
    spacetime.add_relation("A", "B")
    spacetime.add_relation("B", "C")
    return spacetime


def create_bell_spacetime():
    """Create spacetime for Bell scenarios"""
    spacetime = Spacetime()
    # Alice's region
    spacetime.add_point("Alice_in")
    spacetime.add_point("Alice_out")
    spacetime.add_relation("Alice_in", "Alice_out")
    
    # Bob's region
    spacetime.add_point("Bob_in") 
    spacetime.add_point("Bob_out")
    spacetime.add_relation("Bob_in", "Bob_out")
    
    # No relations between Alice and Bob (spacelike separated)
    return spacetime


def create_parallel_spacetime():
    """Create spacetime with parallel paths"""
    spacetime = Spacetime()
    spacetime.add_point("Start")
    spacetime.add_point("Path1_mid")
    spacetime.add_point("Path2_mid")
    spacetime.add_point("End")
    
    spacetime.add_relation("Start", "Path1_mid")
    spacetime.add_relation("Path1_mid", "End")
    spacetime.add_relation("Start", "Path2_mid")
    spacetime.add_relation("Path2_mid", "End")
    
    return spacetime


def run_demo_example(process_name, process_func, impls_func, spacetime, theory, step_counter):
    """Run demo for a single process and save visualizations"""
    print(f"\n🎯 Processing: {process_name} with {theory.name}")
    print("-" * 50)
    
    process = process_func()
    implementations = impls_func()
    
    # Show process diagram for first implementation
    if implementations:
        impl = implementations[0]
        print(f"📊 Showing process structure: {impl.name}")
        fig = plt.figure(figsize=(12, 8))
        draw_process_diagram(impl, fig)
        step_counter = save_plot(fig, f"{process_name}_{theory.name}_Process", step_counter)
    
    # Test implementations (limit to 2 to save time)
    for i, impl in enumerate(implementations[:2]):
        print(f"  Testing implementation {i+1}: {impl.name}")
        
        try:
            # Use short timeout for demo
            emb = is_embeddable(impl, spacetime, theory=theory, timeout_seconds=3)
            
            if emb is True:
                print("    ✅ EMBEDDABLE")
                fig = plt.figure(figsize=(14, 6))
                plot_embedding_result(impl, spacetime, theory, fig=fig)
                step_counter = save_plot(fig, f"{process_name}_{theory.name}_Embedding_Success", step_counter)
                
            elif emb is False:
                print("    ❌ NOT EMBEDDABLE")
                fig = plt.figure(figsize=(14, 6))
                plot_embedding_result(impl, spacetime, theory, fig=fig)
                step_counter = save_plot(fig, f"{process_name}_{theory.name}_Embedding_Failed", step_counter)
                
            else:
                print("    ⏰ TIMEOUT")
                # Still create a visualization for timeout cases
                fig = plt.figure(figsize=(14, 6))
                plot_embedding_result(impl, spacetime, theory, fig=fig)
                step_counter = save_plot(fig, f"{process_name}_{theory.name}_Embedding_Timeout", step_counter)
                
        except EmbeddingTimeoutError:
            print("    ⏰ TIMEOUT")
        except Exception as e:
            print(f"    💥 ERROR: {e}")
    
    return step_counter


def main():
    """Main demo function"""
    global OUTPUT_DIR
    OUTPUT_DIR = setup_output_directory()
    step_counter = 1
    
    print("🚀 Spacetime Process Embedding Demo")
    print("=" * 50)
    print("Running automated demo with 3 processes and 3 theories...")
    
    # Define theories
    theories = [ClassicalTheory(), QuantumTheory(), BoxWorldTheory()]
    
    # Define spacetimes
    spacetimes = [
        ("Simple_Chain", create_simple_spacetime()),
        ("Bell_Like", create_bell_spacetime()),
        ("Parallel", create_parallel_spacetime())
    ]
    
    # Define processes
    processes = [
        ("PR_Box", pr_box_process, pr_box_implementations),
        ("Bell_Correlation", bell_process, bell_implementations),
        ("CNOT_Gate", cnot_process, cnot_implementations)
    ]
    
    # Run demos
    total_demos = len(theories) * len(spacetimes) * len(processes)
    current_demo = 0
    
    for spacetime_name, spacetime in spacetimes:
        print(f"\n🔭 Using Spacetime: {spacetime_name}")
        print(f"   Points: {spacetime.points()}")
        print(f"   Relations: {len(spacetime.as_nx().edges())}")
        
        for theory in theories:
            print(f"\n  🎯 Theory: {theory.name}")
            
            for process_name, process_func, impls_func in processes:
                current_demo += 1
                print(f"\n    📊 [{current_demo}/{total_demos}] Process: {process_name}")
                
                step_counter = run_demo_example(
                    process_name, process_func, impls_func, 
                    spacetime, theory, step_counter
                )
    
    # Summary
    print(f"\n{'='*50}")
    print("🎉 DEMO COMPLETED!")
    print(f"{'='*50}")
    print(f"📁 All images saved in: {OUTPUT_DIR}")
    print(f"🖼️  Total images generated: {step_counter - 1}")
    
    # Show generated files
    print(f"\n📋 Generated files:")
    image_files = [f for f in os.listdir(OUTPUT_DIR) if f.endswith('.png')]
    for file in sorted(image_files):
        print(f"   {file}")
    
    print(f"\n✨ Demo completed successfully!")
    print(f"   Check the '{OUTPUT_DIR}' folder for all generated images.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Demo interrupted by user")
    except Exception as e:
        print(f"\n\n💥 Error: {e}")
        import traceback
        traceback.print_exc()
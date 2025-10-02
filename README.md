# Spacetime Process Embedding Framework

A Python framework for analyzing how computational processes can be embedded in spacetime structures while preserving causal order.

# Quick Start

# Create virtual environment

python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Install dependencies

pip install networkx matplotlib numpy pytest

# Run the demo

python run.py

# What This Framework Does

This tool answers the question: "Can a computational process be physically realized in a given spacetime structure?"

# Core Problem

Process: A computational operation with inputs and outputs (e.g., quantum gate, logical operation)
Spacetime: A causal structure of events with "before/after" relationships
Embedding: Mapping process components to spacetime events while preserving causal order
Theory Constraints: Different physical theories (Classical/Quantum/BoxWorld) allow different implementations

# Real-World Examples

Quantum Entanglement: Can Bell correlations be explained by common causes or require nonlocal connections?
PR Box: Theoretical super-quantum correlations - what spacetime structures allow them?
Distributed Computing: How to map computational steps to physical locations with timing constraints?

# Project Structure

spacetime_process/
├── run.py                              # Main demo executable
├── requirements.txt                    # Python dependencies
├── src/
│   ├── core/                          # Framework core components
│   │   ├── processes.py               # Process data structures
│   │   ├── implementations.py         # Implementation and FPO classes
│   │   ├── spacetime.py               # Spacetime partial order
│   │   └── embeddability.py           # Embedding solver algorithm
│   ├── theories/                      # Physical theory implementations
│   │   ├── base.py                    # Base theory class
│   │   ├── classical.py               # Classical physics constraints
│   │   ├── quantum.py                 # Quantum mechanics constraints
│   │   └── boxworld.py                # Generalized probability theories
│   ├── examples/                      # Pre-built process examples
│   │   ├── pr_box.py                  # PR Box nonlocal correlations
│   │   ├── bell.py                    # Quantum entanglement examples
│   │   ├── cnot.py                    # Quantum gate implementations
│   │   └── simple_valid.py            # Guaranteed working examples
│   └── visualization/                 # Plotting and diagram generation
│       ├── diagrams.py                # Process structure visualization
│       └── spacetime.py               # Spacetime embedding plots
└── tests/                             # Test suite
    └── test_basic.py                  # Core functionality tests

# Key Components Explained

1. Processes & Implementations
Process: Abstract specification (inputs → outputs)
Implementation: Concrete decomposition into components with causal structure
Framed Partial Order (FPO): Mathematical representation of causal relationships

2. Spacetime Structures
Discrete events with causal (before/after) relationships
Represented as directed acyclic graphs (DAGs)
Can model relativistic causality, distributed systems, etc.

3. Physical Theories
Classical: Local operations, no super-luminal signaling
Quantum: Allows entanglement, superposition, quantum operations
BoxWorld: Super-quantum correlations (like PR boxes)

4. Embedding Solver
Backtracking algorithm that finds order-preserving maps
Respects theory-specific constraints
Handles complex causal structures with timeouts

# What You'll See When Running

After running python run.py:

1. Creates output folder with timestamp (e.g., spacetime_results_20231201_143022/)

2. Tests multiple combinations:

   A. 4 process types × 3 spacetime structures × 3 theories = 36 tests
   B. Each test generates 2 images (process diagram + embedding result)

3. Generates visualizations:
   A. Process Diagrams: Show causal structure of implementations
   B. Spacetime Embeddings: Show mapping attempts with success/failure indicators
   C. Color-coded results: Green checkmarks for valid embeddings, red X for failures

4. Provides summary statistics:
   A. Total valid embeddings found
   B. Success rates per theory and spacetime
   C. File listing of all generated images

# Example Output Files

spacetime_results_20231201_143022/
├── 01_Classical_Theory_Linear_direct_connection_process.png
├── 02_Classical_Theory_Linear_direct_connection_embedding.png
├── 03_Classical_Theory_Linear_simple_chain_process.png
├── 04_Classical_Theory_Linear_simple_chain_embedding.png
├── 05_Quantum_Theory_Parallel_fanout_process.png
├── 06_Quantum_Theory_Parallel_fanout_embedding.png
... (54 total files)

# Interpreting Results

Valid Embedding (✅)
Process can be physically realized in that spacetime
All causal constraints are satisfied
Theory-specific rules are obeyed

# nvalid Embedding (❌)

Process violates causal structure
Theory constraints are broken (e.g., classical theory rejecting quantum components)
No possible mapping preserves order relationships

# Timeout (⏰)

Embedding solver couldn't find answer in time
Problem is computationally complex
Try simpler processes or longer timeouts

# Advanced Usage

1. Creating Custom Processes
   from src.core.processes import Process
   from src.core.implementations import Implementation, FramedPartialOrder, Component

   # Define your process

   process = Process("My Algorithm", ["input"], ["output"])
   fpo = FramedPartialOrder(["input"], ["output"])
   processor = fpo.add_internal("compute")
   fpo.add_order("input", processor)
   fpo.add_order(processor, "output")
   impl = Implementation(process, fpo, [Component("algorithm")])

2. Custom Spacetime
   from src.core.spacetime import Spacetime
   spacetime = Spacetime()
   spacetime.add_point("node1")
   spacetime.add_point("node2")
   spacetime.add_point("node3")
   spacetime.add_relation("node1", "node2")
   spacetime.add_relation("node2", "node3")

3. Testing Embeddings
   from src.core.embeddability import is_embeddable
   from src.theories.quantum import QuantumTheory

   theory = QuantumTheory()
   result = is_embeddable(impl, spacetime, theory=theory, timeout_seconds=10)

# Research Applications

1. Quantum Foundations
Study nonlocal correlations and causal structure
Analyze spacetime constraints on quantum protocols
Explore theory-independent physical principles

2. Computer Science
Causal structure of distributed algorithms
Spacetime embeddings of computational processes
Resource theories of communication

3. Physics
Relativistic quantum information
Causal inference in physical systems
Process theory approaches to spacetime

4. Requirements
Python 3.8+
NetworkX 2.8+: Graph operations and causal structures
Matplotlib 3.5+: Visualization and plotting
NumPy 1.23+: Numerical computations
pytest 7.0+: Testing framework

5. Troubleshooting
Common Issues
Blank images: Matplotlib backend issues - code uses 'Agg' backend for saving
Import errors: Check Python path and project structure
Timeouts: Complex embeddings may need longer timeout settings

Verification

# Test basic functionality

python -c "import networkx, matplotlib; print('Dependencies OK')"

# Run tests

pytest tests/ -v

# Extending the Framework

1. Adding New Theories
Create new file in src/theories/
Subclass BaseTheory
Implement allows_implementation() method
Add to demo in run.py

2. Adding New Processes
Create new file in src/examples/
Implement functions returning Implementation objects
Import and add to demo processes list

3. Theory Background
This implements concepts from:
Categorical Quantum Mechanics
Resource Theories
Causal Structure in relativity
Generalized Probabilistic Theories

4. License
Academic and research use. Please cite appropriately in publications.

# Run python run.py to start exploring spacetime process embeddings
#   S p a c e _ t i m e _ r e p r e s e n t a t i o n  
 
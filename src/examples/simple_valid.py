"""
Simple examples that guarantee valid embeddings.
"""
from src.core.processes import Process
from src.core.implementations import Implementation, FramedPartialOrder, Component

def create_simple_identity_process():
    """Simple identity process that should always embed"""
    process = Process("Identity", ["In"], ["Out"])
    
    fpo = FramedPartialOrder(["In"], ["Out"])
    # Just connect input directly to output
    fpo.add_order("In", "Out")
    
    impl = Implementation(process, fpo, [], name="direct_connection")
    return impl

def create_simple_chain_process():
    """Simple chain: Input → Processor → Output"""
    process = Process("Simple Chain", ["Start"], ["End"])
    
    fpo = FramedPartialOrder(["Start"], ["End"])
    processor = fpo.add_internal("Processor")
    fpo.add_order("Start", processor)
    fpo.add_order(processor, "End")
    
    impl = Implementation(process, fpo, [Component("Transformer")], name="simple_chain")
    return impl

def create_parallel_process():
    """Two parallel chains that should embed easily"""
    process = Process("Parallel", ["In1", "In2"], ["Out1", "Out2"])
    
    fpo = FramedPartialOrder(["In1", "In2"], ["Out1", "Out2"])
    
    # First chain
    proc1 = fpo.add_internal("Proc1")
    fpo.add_order("In1", proc1)
    fpo.add_order(proc1, "Out1")
    
    # Second chain (independent)
    proc2 = fpo.add_internal("Proc2") 
    fpo.add_order("In2", proc2)
    fpo.add_order(proc2, "Out2")
    
    impl = Implementation(process, fpo, [
        Component("Worker1"),
        Component("Worker2")
    ], name="parallel_chains")
    return impl

def create_fanout_process():
    """One input fans out to two outputs"""
    process = Process("Fanout", ["Input"], ["Out1", "Out2"])
    
    fpo = FramedPartialOrder(["Input"], ["Out1", "Out2"])
    splitter = fpo.add_internal("Splitter")
    
    fpo.add_order("Input", splitter)
    fpo.add_order(splitter, "Out1")
    fpo.add_order(splitter, "Out2")
    
    impl = Implementation(process, fpo, [Component("Duplicator")], name="fanout")
    return impl

def get_all_simple_processes():
    """Return all simple processes that should embed easily"""
    return [
        create_simple_identity_process(),
        create_simple_chain_process(), 
        create_parallel_process(),
        create_fanout_process()
    ]
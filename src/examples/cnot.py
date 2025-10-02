from src.core.processes import Process
from src.core.implementations import Implementation, FramedPartialOrder, Component

def cnot_process():
    return Process(name="CNOT", inputs=["q1","q2"], outputs=["q1_out","q2_out"])

def cnot_implementations():
    # monolithic CNOT
    fpo0 = FramedPartialOrder(inputs=["q1","q2"], outputs=["q1_out","q2_out"])
    impl0 = Implementation(process=cnot_process(), fpo=fpo0, name="monolithic")

    # decomposition into three gates (Hadamard + CZ + Hadamard) - zigzag-like depending on mapping
    fpo1 = FramedPartialOrder(inputs=["q1","q2"], outputs=["q1_out","q2_out"])
    h1 = fpo1.add_internal("H1")
    cz = fpo1.add_internal("CZ")
    h2 = fpo1.add_internal("H2")
    # order chain: q1 -> H1 -> CZ -> H2 -> q1_out ; q2 -> CZ -> q2_out
    fpo1.add_order("q1", h1)
    fpo1.add_order(h1, cz)
    fpo1.add_order(cz, h2)
    fpo1.add_order(h2, "q1_out")
    fpo1.add_order("q2", cz)
    fpo1.add_order(cz, "q2_out")
    impl1 = Implementation(process=cnot_process(), fpo=fpo1, name="H_CZ_H")
    impl1.add_component(Component("H1", metadata={"quantum": True}))
    impl1.add_component(Component("CZ", metadata={"quantum": True}))
    impl1.add_component(Component("H2", metadata={"quantum": True}))

    # zigzag-ish alternative (swap and local ops)
    fpo2 = FramedPartialOrder(inputs=["q1","q2"], outputs=["q1_out","q2_out"])
    s1 = fpo2.add_internal("s1")
    s2 = fpo2.add_internal("s2")
    fpo2.add_order("q1", s1)
    fpo2.add_order(s1, s2)
    fpo2.add_order(s2, "q1_out")
    fpo2.add_order("q2", s2)
    fpo2.add_order(s1, "q2_out")
    impl2 = Implementation(process=cnot_process(), fpo=fpo2, name="zigzag_variant")
    impl2.add_component(Component("s1", metadata={"quantum": True}))
    impl2.add_component(Component("s2", metadata={"quantum": True}))

    return [impl0, impl1, impl2]

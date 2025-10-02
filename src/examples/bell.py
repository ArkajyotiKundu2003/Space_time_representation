from src.core.processes import Process
from src.core.implementations import Implementation, FramedPartialOrder, Component

def bell_process():
    return Process(name="Bell Correlation", inputs=["X","Y"], outputs=["A","B"])

def bell_implementations():
    # monolithic
    fpo1 = FramedPartialOrder(inputs=["X","Y"], outputs=["A","B"])
    impl1 = Implementation(process=bell_process(), fpo=fpo1, name="monolithic")
    impl1.add_component(Component("Bell_monolithic"))

    # quantum implementation: shared entangled state s, local measurements f,g
    fpo2 = FramedPartialOrder(inputs=["X","Y"], outputs=["A","B"])
    s = fpo2.add_internal("s")   # entangled state
    f = fpo2.add_internal("f")
    g = fpo2.add_internal("g")
    fpo2.add_order(s, f)
    fpo2.add_order(s, g)
    fpo2.add_order("X", f)
    fpo2.add_order("Y", g)
    fpo2.add_order(f, "A")
    fpo2.add_order(g, "B")
    impl2 = Implementation(process=bell_process(), fpo=fpo2, name="quantum_common_cause")
    impl2.add_component(Component("s", metadata={"quantum": True}))
    impl2.add_component(Component("f", metadata={"quantum": True}))
    impl2.add_component(Component("g", metadata={"quantum": True}))

    # classical implementation that relies on one-way communication (Alice -> Bob)
    fpo3 = FramedPartialOrder(inputs=["X","Y"], outputs=["A","B"])
    a = fpo3.add_internal("a")  # Alice's box sending message to Bob
    b = fpo3.add_internal("b")
    fpo3.add_order("X", a)
    fpo3.add_order(a, "A")
    fpo3.add_order(a, b)
    fpo3.add_order("Y", b)
    fpo3.add_order(b, "B")
    impl3 = Implementation(process=bell_process(), fpo=fpo3, name="one_way_comm")
    impl3.add_component(Component("a"))
    impl3.add_component(Component("b"))

    return [impl1, impl2, impl3]

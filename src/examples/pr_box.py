from src.core.processes import Process
from src.core.implementations import Implementation, FramedPartialOrder, Component

def pr_box_process():
    return Process(name="PR Box", inputs=["X", "Y"], outputs=["A", "B"])

def pr_box_implementations():
    # Implementation 1: monolithic box (no decomposition)
    fpo1 = FramedPartialOrder(inputs=["X","Y"], outputs=["A","B"])
    impl1 = Implementation(process=pr_box_process(), fpo=fpo1, components=[Component("PR_monolithic")], name="monolithic")

    # Implementation 2: decomposed with common cause s and local operations f,g (boxworld allows this)
    fpo2 = FramedPartialOrder(inputs=["X","Y"], outputs=["A","B"])
    # internal node representing shared resource s
    s = fpo2.add_internal("s")
    # order: s -> f -> A ; s -> g -> B ; inputs -> f/g maybe
    f = fpo2.add_internal("f")
    g = fpo2.add_internal("g")
    fpo2.add_order(s, f)
    fpo2.add_order(s, g)
    fpo2.add_order("X", f)
    fpo2.add_order("Y", g)
    fpo2.add_order(f, "A")
    fpo2.add_order(g, "B")
    impl2 = Implementation(process=pr_box_process(), fpo=fpo2, name="common_cause")
    impl2.add_component(Component("s", metadata={"boxworld": True}))
    impl2.add_component(Component("f"))
    impl2.add_component(Component("g"))

    return [impl1, impl2]

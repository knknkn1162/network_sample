from cml import Cml
import ini as ini

cml = Cml()
lab = cml.lab
print(f"token: {cml.auth_token}")

s0 = lab.create_node(ini.iosvl2_0.__name__, "iosvl2", 450, 100)
s0.config = f"hostname {ini.iosvl2_0.__name__}"
s1 = lab.create_node(ini.iosvl2_1.__name__, "iosvl2", 100, 600)
s1.config = f"hostname {ini.iosvl2_1.__name__}"
s2 = lab.create_node(ini.iosvl2_2.__name__, "iosvl2", 700, 600)
s2.config = f"hostname {ini.iosvl2_2.__name__}"


c0 = lab.create_node(ini.server_0.__name__, "server", 900, 600)
c1 = lab.create_node(ini.server_1.__name__, "server", 900, 900)

lab.create_link(
    s0.create_interface(ini.iosvl2_0.g0_0.slot),
    s1.create_interface(ini.iosvl2_1.g0_0.slot),
)
lab.create_link(
    s0.create_interface(ini.iosvl2_0.g0_1.slot),
    s2.create_interface(ini.iosvl2_2.g0_0.slot),
)
lab.create_link(
    s1.create_interface(ini.iosvl2_0.g0_1.slot),
    s2.create_interface(ini.iosvl2_2.g0_1.slot),
)

lab.create_link(
    s2.create_interface(ini.iosvl2_2.g0_2.slot),
    c0.create_interface(ini.server_0.eth0.slot),
)
lab.create_link(
    s2.create_interface(ini.iosvl2_2.g0_3.slot),
    c1.create_interface(ini.server_0.eth0.slot),
)


print("start nodes..")
lab.start()

# print nodes and interfaces states:
for node in lab.nodes():
    print(vars(node))
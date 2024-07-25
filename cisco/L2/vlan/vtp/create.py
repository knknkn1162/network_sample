from cml import Cml
import ini as ini

cml = Cml()
lab = cml.lab
print(f"token: {cml.auth_token}")

r0 = lab.create_node(ini.iosvl2_0.__name__, "iosvl2", 200, 400)
r0.config = f"hostname {ini.iosvl2_0.__name__}"
r1 = lab.create_node(ini.iosvl2_1.__name__, "iosvl2", 450, 400)
r1.config = f"hostname {ini.iosvl2_1.__name__}"
r2 = lab.create_node(ini.iosvl2_2.__name__, "iosvl2", 700, 400)
r2.config = f"hostname {ini.iosvl2_2.__name__}"

c0 = lab.create_node(ini.server_0.__name__, "server", 200, 600)
c1 = lab.create_node(ini.server_1.__name__, "server", 200, 200)
c2 = lab.create_node(ini.server_2.__name__, "server", 700, 600)

lab.create_link(
    c0.create_interface(ini.server_0.eth0.slot),
    r0.create_interface(ini.iosvl2_0.g0_0.slot),
)
lab.create_link(
    c1.create_interface(ini.server_1.eth0.slot),
    r0.create_interface(ini.iosvl2_0.g0_1.slot),
)
lab.create_link(
    r0.create_interface(ini.iosvl2_0.g0_2.slot),
    r1.create_interface(ini.iosvl2_1.g0_0.slot),
)
lab.create_link(
    r1.create_interface(ini.iosvl2_1.g0_1.slot),
    r2.create_interface(ini.iosvl2_2.g0_0.slot),
)
lab.create_link(
    r2.create_interface(ini.iosvl2_2.g0_1.slot),
    c2.create_interface(ini.server_2.eth0.slot),
)

print("start nodes..")
lab.start()

# print nodes and interfaces states:
for node in lab.nodes():
    print(vars(node))
from cml import Cml
import ini as ini

cml = Cml()
lab = cml.lab
print(f"token: {cml.auth_token}")

r0 = lab.create_node(ini.iosvl2_0.__name__, "iosvl2", 300, 200)
r0.config = f"hostname {ini.iosvl2_0.__name__}"
c0 = lab.create_node(ini.server_0.__name__, "server", 0, 200)
c1 = lab.create_node(ini.server_1.__name__, "server", 600, 200)

lab.create_link(
    r0.create_interface(ini.iosvl2_0.g0_0.slot),
    c0.create_interface(ini.server_0.eth0.slot),
)
lab.create_link(
    r0.create_interface(ini.iosvl2_0.g0_1.slot),
    c1.create_interface(ini.server_1.eth0.slot),
)

print("start nodes..")
lab.start(wait=False)

# print nodes and interfaces states:
for node in lab.nodes():
    print(vars(node))
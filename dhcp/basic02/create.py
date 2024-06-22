from cml import Cml
import ini as ini

cml = Cml()
lab = cml.lab
print(f"token: {cml.auth_token}")

r0 = lab.create_node(ini.iosv_0.__name__, "iosv", 700, 200)
r0.config = f"hostname {ini.iosv_0.__name__}"

r1 = lab.create_node(ini.iosv_1.__name__, "iosv", 100, 200)
r1.config = f"hostname {ini.iosv_1.__name__}"

s0 = lab.create_node(ini.iosvl2_0.__name__, "iosvl2", 400, 200)
s0.config = f"hostname {ini.iosvl2_0.__name__}"

c0 = lab.create_node(ini.server_0.__name__, "server", 200, 400)
c1 = lab.create_node(ini.server_1.__name__, "server", 400, 400)

lab.create_link(
    c0.create_interface(ini.server_0.eth0.slot),
    s0.create_interface(ini.iosvl2_0.g0_0.slot),
)
lab.create_link(
    c1.create_interface(ini.server_1.eth0.slot),
    s0.create_interface(ini.iosvl2_0.g0_1.slot)
)
lab.create_link(
    r1.create_interface(ini.iosv_1.g0_0.slot),
    s0.create_interface(ini.iosvl2_0.g0_2.slot)
)
lab.create_link(
    s0.create_interface(ini.iosvl2_0.g0_3.slot),
    r0.create_interface(ini.iosv_0.g0_0.slot)
)

print("start nodes..")
lab.start()

# print nodes and interfaces states:
for node in lab.nodes():
    print(vars(node))
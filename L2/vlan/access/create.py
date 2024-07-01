from cml import Cml, Lab
import ini as ini
import time

cml = Cml()
lab = cml.lab
print(f"token: {cml.auth_token}")

# DHCP client

c0 = lab.create_node(ini.server_0.__name__, "server", 200, 400)
c1 = lab.create_node(ini.server_1.__name__, "server", 400, 400)
c2 = lab.create_node(ini.server_2.__name__, "server", 600, 400)
c3 = lab.create_node(ini.server_3.__name__, "server", 800, 400)

s0 = lab.create_node(ini.iosvl2_0.__name__, "iosvl2", 500, 100)
s0.config = f"hostname {ini.iosvl2_0.__name__}"

lab.create_link(
    c0.create_interface(ini.server_0.eth0.slot),
    s0.create_interface(ini.iosvl2_0.g0_0.slot),
)
lab.create_link(
    c1.create_interface(ini.server_1.eth0.slot),
    s0.create_interface(ini.iosvl2_0.g0_1.slot),
)
lab.create_link(
    c2.create_interface(ini.server_2.eth0.slot),
    s0.create_interface(ini.iosvl2_0.g0_2.slot),
)
lab.create_link(
    c3.create_interface(ini.server_3.eth0.slot),
    s0.create_interface(ini.iosvl2_0.g0_3.slot),
)

print("start nodes..")
lab.start(wait=False)
time.sleep(15)

# print nodes and interfaces states:
for node in lab.nodes():
    print(vars(node))
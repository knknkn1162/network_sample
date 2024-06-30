from cml import Cml, Lab
import ini as ini
import time

cml = Cml()
lab = cml.lab
print(f"token: {cml.auth_token}")

# DHCP client
r0 = lab.create_node(ini.iosv_0.__name__, "iosv", 600, 400)
r0.config = f"hostname {ini.iosv_0.__name__}"

c0 = lab.create_node(ini.server_0.__name__, "server", 200, 400)
c1 = lab.create_node(ini.server_1.__name__, "server", 800, 400)

s0 = lab.create_node(ini.iosvl2_0.__name__, "iosvl2", 400, 400)


lab.create_link(
    c0.create_interface(ini.server_0.eth0.slot),
    s0.create_interface(ini.iosvl2_0.g0_0.slot),
)
lab.create_link(
    s0.create_interface(ini.iosvl2_0.g0_1.slot),
    r0.create_interface(ini.iosv_0.g0_0.slot),
)
lab.create_link(
    r0.create_interface(ini.iosv_0.g0_1.slot),
    c1.create_interface(ini.server_1.eth0.slot)
)

print("start nodes..")
lab.start(wait=False)
time.sleep(15)

# print nodes and interfaces states:
for node in lab.nodes():
    print(vars(node))
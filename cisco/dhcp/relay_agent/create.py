from cml import Cml, Lab
import ini as ini
import time

cml = Cml()
lab = cml.lab
print(f"token: {cml.auth_token}")

# relay
r0 = lab.create_node(ini.iosv_0.__name__, "iosv", 600, 400)
r0.config = f"hostname {ini.iosv_0.__name__}"
# DHCP server
r1 = lab.create_node(ini.iosv_1.__name__, "iosv", 900, 400)
r1.config = f"hostname {ini.iosv_1.__name__}"

c0 = lab.create_node(ini.server_0.__name__, "server", 200, 100)
c1 = lab.create_node(ini.server_1.__name__, "server", 200, 700)

s0 = lab.create_node(ini.switch_0.__name__, "unmanaged_switch", 400, 400)


lab.create_link(
    c0.create_interface(ini.server_0.eth0.slot),
    s0.create_interface(ini.switch_0.port0.slot),
)
lab.create_link(
    c1.create_interface(ini.server_1.eth0.slot),
    s0.create_interface(ini.switch_0.port1.slot),
)
lab.create_link(
    r0.create_interface(ini.iosv_0.g0_0.slot),
    s0.create_interface(ini.switch_0.port2.slot),
)
lab.create_link(
    r0.create_interface(ini.iosv_0.g0_1.slot),
    r1.create_interface(ini.iosv_1.g0_0.slot),
)



print("start nodes..")
lab.start(wait=False)
time.sleep(15)

# print nodes and interfaces states:
for node in lab.nodes():
    print(vars(node))
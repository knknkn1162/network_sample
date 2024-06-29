from cml import Cml, Lab
import ini as ini
import time

cml = Cml()
lab = cml.lab
print(f"token: {cml.auth_token}")

r0 = lab.create_node(ini.iosv_0.__name__, "iosv", 700, 100)
r0.config = f"hostname {ini.iosv_0.__name__}"
r1 = lab.create_node(ini.iosv_1.__name__, "iosv", 700, 900)
r1.config = f"hostname {ini.iosv_1.__name__}"
r2 = lab.create_node(ini.iosv_2.__name__, "iosv", 1000, 500)
r2.config = f"hostname {ini.iosv_2.__name__}"

s0 = lab.create_node(ini.sw_0.__name__, "unmanaged_switch", 400, 500)
s0.config = f"hostname {ini.sw_0.__name__}"

c0 = lab.create_node(ini.server_0.__name__, "server", 100, 500)


lab.create_link(
    c0.create_interface(ini.server_0.eth0.slot),
    s0.create_interface(ini.sw_0.port0.slot),
)

lab.create_link(
    s0.create_interface(ini.sw_0.port1.slot),
    r0.create_interface(ini.iosv_0.g0_0.slot),
)

lab.create_link(
    s0.create_interface(ini.sw_0.port2.slot),
    r1.create_interface(ini.iosv_1.g0_0.slot),
)

lab.create_link(
    r0.create_interface(ini.iosv_0.g0_1.slot),
    r2.create_interface(ini.iosv_2.g0_0.slot),
)

lab.create_link(
    r1.create_interface(ini.iosv_1.g0_1.slot),
    r2.create_interface(ini.iosv_2.g0_1.slot),
)

print("start nodes..")
lab.start(wait=False)
time.sleep(15)

# print nodes and interfaces states:
for node in lab.nodes():
    print(vars(node))
from cml import Cml
import ini as ini

cml = Cml()
lab = cml.lab
print(f"token: {cml.auth_token}")

r0 = lab.create_node(ini.iosv_0.__name__, "iosv", 100, 100)
r0.config = f"hostname {ini.iosv_0.__name__}"
r1 = lab.create_node(ini.iosv_1.__name__, "iosv", 700, 100)
r1.config = f"hostname {ini.iosv_1.__name__}"
r2 = lab.create_node(ini.iosv_2.__name__, "iosv", 100, 700)
r2.config = f"hostname {ini.iosv_2.__name__}"
r3 = lab.create_node(ini.iosv_3.__name__, "iosv", 700, 700)
r3.config = f"hostname {ini.iosv_3.__name__}"

s0 = lab.create_node(ini.switch_0.__name__, "unmanaged_switch", 400, 400)

lab.create_link(
    s0.create_interface(ini.switch_0.port0.slot),
    r0.create_interface(ini.iosv_0.g0_0.slot),
)
lab.create_link(
    s0.create_interface(ini.switch_0.port1.slot),
    r1.create_interface(ini.iosv_1.g0_0.slot),
)
lab.create_link(
    s0.create_interface(ini.switch_0.port2.slot),
    r2.create_interface(ini.iosv_2.g0_0.slot),
)
lab.create_link(
    s0.create_interface(ini.switch_0.port3.slot),
    r3.create_interface(ini.iosv_3.g0_0.slot),
)

print("start nodes..")
lab.start(wait=False)

# print nodes and interfaces states:
for node in lab.nodes():
    print(vars(node))
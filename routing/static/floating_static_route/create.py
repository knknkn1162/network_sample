from cml import Cml, Lab
import ini as ini
import time

cml = Cml()
lab = cml.lab
print(f"token: {cml.auth_token}")

r0 = lab.create_node(ini.iosv_0.__name__, "iosv", 100, 300)
r0.config = f"hostname {ini.iosv_0.__name__}"
r1 = lab.create_node(ini.iosv_1.__name__, "iosv", 400, 100)
r1.config = f"hostname {ini.iosv_1.__name__}"
r2 = lab.create_node(ini.iosv_2.__name__, "iosv", 400, 500)
r2.config = f"hostname {ini.iosv_2.__name__}"
r3 = lab.create_node(ini.iosv_3.__name__, "iosv", 800, 300)
r3.config = f"hostname {ini.iosv_3.__name__}"
r4 = lab.create_node(ini.iosv_4.__name__, "iosv", 1000, 300)
r4.config = f"hostname {ini.iosv_4.__name__}"


lab.create_link(
    r0.create_interface(ini.iosv_0.g0_0.slot),
    r1.create_interface(ini.iosv_1.g0_0.slot),
)

lab.create_link(
    r0.create_interface(ini.iosv_0.g0_1.slot),
    r2.create_interface(ini.iosv_2.g0_0.slot),
)

lab.create_link(
    r1.create_interface(ini.iosv_0.g0_1.slot),
    r3.create_interface(ini.iosv_3.g0_0.slot),
)

lab.create_link(
    r2.create_interface(ini.iosv_2.g0_1.slot),
    r3.create_interface(ini.iosv_3.g0_1.slot),
)

lab.create_link(
    r3.create_interface(ini.iosv_3.g0_2.slot),
    r4.create_interface(ini.iosv_4.g0_0.slot),
)

print("start nodes..")
lab.start(wait=False)
time.sleep(15)

# print nodes and interfaces states:
for node in lab.nodes():
    print(vars(node))
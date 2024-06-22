from cml import Cml
import ini as ini

cml = Cml()
lab = cml.lab
print(f"token: {cml.auth_token}")

r0 = lab.create_node(ini.iosv_0.__name__, "iosv", 100, 100)
r0.config = f"hostname {ini.iosv_0.__name__}"
r1 = lab.create_node(ini.iosv_1.__name__, "iosv", 100, 700)
r1.config = f"hostname {ini.iosv_1.__name__}"

r201 = lab.create_node(ini.iosv_201.__name__, "iosv", 900, 400)
r201.config = f"hostname {ini.iosv_201.__name__}"

r202 = lab.create_node(ini.iosv_202.__name__, "iosv", 900, 600)
r202.config = f"hostname {ini.iosv_202.__name__}"


lab.create_link(
    r0.create_interface(ini.iosv_0.g0_0.slot),
    r1.create_interface(ini.iosv_1.g0_0.slot),
)
lab.create_link(
    r1.create_interface(ini.iosv_1.g0_1.slot),
    r201.create_interface(ini.iosv_201.g0_0.slot),
)
lab.create_link(
    r1.create_interface(ini.iosv_1.g0_2.slot),
    r202.create_interface(ini.iosv_202.g0_0.slot),
)

print("start nodes..")
lab.start(wait=False)

# print nodes and interfaces states:
for node in lab.nodes():
    print(vars(node))
from cml import Cml
import ini as ini

cml = Cml()
lab = cml.lab
print(f"token: {cml.auth_token}")

r0 = lab.create_node(ini.ospf0.iosv_0.__name__, "iosv", 100, 100)
r0.config = f"hostname {ini.ospf0.iosv_0.__name__}"
r1 = lab.create_node(ini.bgp0.iosv_1.__name__, "iosv", 400, 100)
r1.config = f"hostname {ini.bgp0.iosv_1.__name__}"
r2 = lab.create_node(ini.bgp0.iosv_2.__name__, "iosv", 700, 100)
r2.config = f"hostname {ini.bgp0.iosv_2.__name__}"


lab.create_link(
    r0.create_interface(ini.ospf0.iosv_0.g0_0.slot),
    r1.create_interface(ini.ospf0.iosv_1.g0_0.slot),
)
lab.create_link(
    r1.create_interface(ini.bgp0.iosv_1.g0_1.slot),
    r2.create_interface(ini.bgp0.iosv_2.g0_0.slot),
)

print("start nodes..")
lab.start(wait=False)

# print nodes and interfaces states:
for node in lab.nodes():
    print(vars(node))
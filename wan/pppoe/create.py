from cml import Cml
import ini as ini

cml = Cml()
lab = cml.lab
print(f"token: {cml.auth_token}")

r0 = lab.create_node(ini.iosv_0.__name__, "iosv", 300, 300)
r0.config = f"hostname {ini.iosv_0.__name__}"
r1 = lab.create_node(ini.iosv_1.__name__, "iosv", 700, 300)
r1.config = f"hostname {ini.iosv_1.__name__}"

c0 = lab.create_node(ini.server_0.__name__, "server", 300, 600)
c1 = lab.create_node(ini.server_1.__name__, "server", 700, 600)

lab.create_link(
    r0.create_interface(ini.iosv_0.g0_0.slot),
    c0.create_interface(ini.server_0.eth0.slot),
)
lab.create_link(
    r0.create_interface(ini.iosv_0.g0_1.slot),
    r1.create_interface(ini.iosv_1.g0_1.slot),
)
lab.create_link(
    r1.create_interface(ini.iosv_0.g0_0.slot),
    c1.create_interface(ini.server_1.eth0.slot),
)

print("start nodes..")
lab.start(wait=False)

# print nodes and interfaces states:
for node in lab.nodes():
    print(vars(node))
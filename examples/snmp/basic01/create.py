from cml import Cml, Lab
import ini as ini
import time

cml = Cml()
lab = cml.lab
print(f"token: {cml.auth_token}")

r0 = lab.create_node(ini.iosv_0.__name__, "iosv", 700, 300)
r0.config = f"hostname {ini.iosv_0.__name__}"

c0 = lab.create_node(ini.server_0.__name__, "server", 100, 300)


lab.create_link(
    c0.create_interface(ini.server_0.eth0.slot),
    r0.create_interface(ini.iosv_0.g0_0.slot),
)

print("start nodes..")
lab.start(wait=False)
time.sleep(15)

# print nodes and interfaces states:
for node in lab.nodes():
    print(vars(node))
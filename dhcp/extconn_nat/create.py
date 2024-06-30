from cml import Cml, Lab
import ini as ini
import time

cml = Cml()
lab = cml.lab
print(f"token: {cml.auth_token}")

# DHCP client
r0 = lab.create_node(ini.iosv_0.__name__, "iosv", 100, 400)
r0.config = f"hostname {ini.iosv_0.__name__}"

ext0 = lab.create_node(ini.ext_conn0.__name__, "external_connector", 600,400)

lab.create_link(
    r0.create_interface(ini.iosv_0.g0_0.slot),
    ext0.create_interface(ini.ext_conn0.slot),
)

print("start nodes..")
lab.start(wait=False)
time.sleep(15)

# print nodes and interfaces states:
for node in lab.nodes():
    print(vars(node))
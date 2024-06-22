from cml import Cml
import ini as ini

cml = Cml()
lab = cml.lab
print(f"token: {cml.auth_token}")

r0 = lab.create_node(ini.iosv_0.__name__, "iosv", 700, 400)
r0.config = f"hostname {ini.iosv_0.__name__}"

c0 = lab.create_node(ini.server_0.__name__, "server", 200, 400)

lab.create_link(
    c0.create_interface(ini.server_0.eth0.slot),
    r0.create_interface(ini.iosv_0.g0_0.slot),
)

print("start nodes..")
lab.start()

# print nodes and interfaces states:
for node in lab.nodes():
    print(vars(node))
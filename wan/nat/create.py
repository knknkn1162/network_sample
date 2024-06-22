from cml import Cml
import ini as ini

cml = Cml()
lab = cml.lab
print(f"token: {cml.auth_token}")

r0 = lab.create_node(ini.iosv_0.__name__, "iosv", 300, 200)
r0.config = f"hostname {ini.iosv_0.__name__}"
r1 = lab.create_node(ini.iosv_1.__name__, "iosv", 400, 200)
r1.config = f"hostname {ini.iosv_1.__name__}"
risp = lab.create_node(ini.iosv_isp.__name__, "iosv", 500, 200)
risp.config = f"hostname {ini.iosv_isp.__name__}"

c0 = lab.create_node(ini.server_0.__name__, "server", 200, 400)
csrv = lab.create_node(ini.server_srv.__name__, "server", 600, 400)

lab.create_link(
    c0.create_interface(ini.server_0.eth0.slot),
    r0.create_interface(ini.iosv_0.g0_1.slot),
)
lab.create_link(
    r0.create_interface(ini.iosv_0.g0_0.slot),
    r1.create_interface(ini.iosv_1.g0_0.slot)
)
lab.create_link(
    r1.create_interface(ini.iosv_1.g0_1.slot),
    risp.create_interface(ini.iosv_isp.g0_0.slot)
)
lab.create_link(
    risp.create_interface(ini.iosv_isp.g0_1.slot),
    csrv.create_interface(ini.server_srv.eth0.slot)
)

print("start nodes..")
lab.start()

# print nodes and interfaces states:
for node in lab.nodes():
    print(vars(node))
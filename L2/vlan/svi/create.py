from cml import Cml
import ini as ini

cml = Cml()
lab = cml.lab
print(f"token: {cml.auth_token}")
r1 = lab.create_node(ini.iosvl2.__name__, "iosvl2", 300, 200)
r1.config = f"hostname {ini.iosvl2.__name__}"

c1 = lab.create_node(ini.server_1.__name__, "server", 250, 400)
c2 = lab.create_node(ini.server_2.__name__, "server", 350, 400)
c3 = lab.create_node(ini.server_3.__name__, "server", 450, 400)
c4 = lab.create_node(ini.server_4.__name__, "server", 550, 400)
c5 = lab.create_node(ini.server_5.__name__, "server", 750, 200)

lab.create_link(
    r1.create_interface(ini.iosvl2.g0_0.slot),
    c1.create_interface(ini.server_1.eth0.slot)
)
lab.create_link(
    r1.create_interface(ini.iosvl2.g0_1.slot),
    c2.create_interface(ini.server_2.eth0.slot)
)
lab.create_link(
    r1.create_interface(ini.iosvl2.g0_2.slot),
    c3.create_interface(ini.server_3.eth0.slot)
)
lab.create_link(
    r1.create_interface(ini.iosvl2.g0_3.slot),
    c4.create_interface(ini.server_4.eth0.slot)
)

lab.create_link(
    r1.create_interface(ini.iosvl2.g0_4.slot),
    c5.create_interface(ini.server_5.eth0.slot)
)

print("start nodes..")
lab.start()

# print nodes and interfaces states:
for node in lab.nodes():
    print(vars(node))
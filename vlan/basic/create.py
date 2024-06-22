from cml import Cml
import ini as ini
import time

cml = Cml()
lab = cml.lab
print(cml.auth_token)
r1 = lab.create_node(ini.iosvl2_1.__name__, "iosvl2", 300, 200)
r1.config = f"hostname {ini.iosvl2_1.__name__}"
r2 = lab.create_node(ini.iosvl2_2.__name__, "iosvl2", 500, 200)
r2.config = f"hostname {ini.iosvl2_2.__name__}"

c1 = lab.create_node(ini.server_1.__name__, "server", 250, 400)
c2 = lab.create_node(ini.server_2.__name__, "server", 350, 400)
c3 = lab.create_node(ini.server_3.__name__, "server", 450, 400)
c4 = lab.create_node(ini.server_4.__name__, "server", 550, 400)

lab.create_link(
  r1.create_interface(ini.iosvl2_1.g0_0.slot),
  c1.create_interface(ini.server_1.eth0.slot)
)
lab.create_link(
  r1.create_interface(ini.iosvl2_1.g0_1.slot),
  c2.create_interface(ini.server_2.eth0.slot)
)
lab.create_link(
  r1.create_interface(ini.iosvl2_1.g0_2.slot),
  r2.create_interface(ini.iosvl2_2.g0_2.slot)
)
lab.create_link(
  r2.create_interface(ini.iosvl2_2.g0_0.slot),
  c3.create_interface(ini.server_3.eth0.slot)
)
lab.create_link(
  r2.create_interface(ini.iosvl2_2.g0_1.slot),
  c4.create_interface(ini.server_4.eth0.slot)
)


print("end")
print("starting..")
lab.start()

# print nodes and interfaces states:
for node in lab.nodes():
    print(vars(node))
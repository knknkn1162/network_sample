from cml import Cml
import ini as ini

cml = Cml()
lab = cml.lab
print(f"token: {cml.auth_token}")

s0 = lab.create_node(ini.iosvl2_0.__name__, "iosvl2", 100, 300)
s0.config = f"hostname {ini.iosvl2_0.__name__}"
s1 = lab.create_node(ini.iosvl2_1.__name__, "iosvl2", 500, 300)
s1.config = f"hostname {ini.iosvl2_1.__name__}"

lab.create_link(
    s0.create_interface(ini.iosvl2_0.g0_0.slot),
    s1.create_interface(ini.iosvl2_1.g0_0.slot),
)
lab.create_link(
    s0.create_interface(ini.iosvl2_0.g0_1.slot),
    s1.create_interface(ini.iosvl2_1.g0_1.slot),
)

print("start nodes..")
lab.start()

# print nodes and interfaces states:
for node in lab.nodes():
    print(vars(node))
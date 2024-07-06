from cml import Cml
import ini as ini
import time
from logger import start_log
start_log("cml")

cml = Cml()
lab = cml.lab

r0 = lab.create_iosvl2(ini.iosvl2_0.__name__, 200, 600, slots=3)
r1 = lab.create_iosvl2(ini.iosvl2_1.__name__, 450, 100, slots=2)
r2 = lab.create_iosvl2(ini.iosvl2_2.__name__, 700, 600, slots=3)

c0 = lab.create_server(ini.server_0.__name__, 0, 600, slots=1)
c1 = lab.create_server(ini.server_1.__name__, 900, 600, slots=1)

r0.create_links([r1[0], r2[0], c0[0]])
r1.create_links([r0[0], r2[0]])
r2.create_links([r1[1], r0[1], c1[0]])
c0.create_links([r0[2]])
c1.create_links([r2[2]])

lab.start()

# print nodes and interfaces states:
lab.print_nodes()
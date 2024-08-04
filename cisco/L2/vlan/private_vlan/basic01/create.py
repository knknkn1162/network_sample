from cmlmag.cml import Cml
import ini as ini
import time

def main():
    cml = Cml()
    lab = cml.lab

    s0 = lab.create_iosvl2(ini.iosvl2_0.__name__, 500, 400, slots=6)
    # client
    c0 = lab.create_server(ini.server_0.__name__, 200, 700, slots=1)
    c1 = lab.create_server(ini.server_1.__name__, 400, 700, slots=1)
    c2 = lab.create_server(ini.server_2.__name__, 600, 700, slots=1)
    c3 = lab.create_server(ini.server_3.__name__, 800, 700, slots=1)
    c4 = lab.create_server(ini.server_4.__name__, 500, 100, slots=1)
    c5 = lab.create_server(ini.server_5.__name__, 1000, 700, slots=1)

    c0.create_links([s0[0]])
    c1.create_links([s0[1]])
    c2.create_links([s0[2]])
    c3.create_links([s0[3]])
    c4.create_links([s0[4]])
    c5.create_links([s0[5]])

    s0.create_links([c0[0], c1[0], c2[0], c3[0], c4[0], c5[0]])

    lab.start(wait_time=15)

    # print nodes and interfaces states:
    lab.print_nodes()

if __name__ == '__main__':
    main()